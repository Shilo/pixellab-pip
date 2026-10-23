from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_helpers import REPO_ROOT, load_module

SCRIPT = REPO_ROOT / "skills/pixellab-pip/assets/manifest.py"
manifest = load_module("manifest", SCRIPT)


def job(job_id: str, gens: float, status: str = "ok") -> dict:
    return {"job_id": job_id, "tool": "MCP animate_image", "seed": 7, "status": status,
            "reported_usage": {"generations": gens}, "waited_s": 40, "outputs": ["raw/0.png"]}


class ManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.run = self.tmp.name

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_add_job_round_trip(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        self.assertEqual(manifest.jobs(self.run)[0]["job_id"], "a")
        self.assertEqual(manifest.jobs(self.run)[0]["waited_s"], 40)

    def test_failed_job_costs_nothing(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        manifest.add_job(self.run, job("b", 9, status="failed"))
        self.assertEqual(manifest.spent(self.run), 6)

    def test_outcome_set_later(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        manifest.set_outcome(self.run, "a", "kept", "frames 1-9 used")
        entry = manifest.jobs(self.run)[0]
        self.assertEqual((entry["outcome"], entry["outcome_note"]), ("kept", "frames 1-9 used"))

    def test_budget_spent_survives_restart(self) -> None:
        for job_id, gens in (("a", 6), ("b", 4.5)):
            code = (f"import json,sys; sys.path.insert(0, {str(SCRIPT.parent)!r}); import manifest; "
                    f"manifest.add_job({self.run!r}, json.loads({json.dumps(json.dumps(job(job_id, gens)))}))")
            subprocess.run([sys.executable, "-c", code], check=True)
        out = subprocess.run([sys.executable, str(SCRIPT), "spent", self.run], check=True,
                             capture_output=True, text=True).stdout
        self.assertEqual(json.loads(out)["spent"], 10.5)

    def test_atomic_write_leaves_valid_json(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        self.assertEqual(list(Path(self.run).glob("*.tmp")), [])
        json.loads((Path(self.run) / "manifest.json").read_text(encoding="utf-8"))

    def test_same_job_twice_is_one_entry(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        manifest.add_job(self.run, job("a", 6))
        self.assertEqual(len(manifest.jobs(self.run)), 1)
        self.assertEqual(manifest.spent(self.run), 6)

    def test_submitted_job_counts_toward_the_budget(self) -> None:
        # final review: a job interrupted before its download was missing from the spend, so a resumed plan
        # could spend its budget twice
        manifest.add_job(self.run, job("a", 6))
        manifest.add_job(self.run, {"job_id": "b", "tool": "MCP animate_image", "status": "submitted",
                                    "reported_usage": {"generations": 4}})
        self.assertEqual(manifest.spent(self.run), 6)
        self.assertEqual(manifest.committed(self.run), 10)
        out = subprocess.run([sys.executable, str(SCRIPT), "committed", self.run], check=True,
                             capture_output=True, text=True).stdout
        self.assertEqual(json.loads(out)["committed"], 10)

    def test_committed_sums_every_run_of_one_plan(self) -> None:
        # e2e demo: one plan made three run folders (still, attack, skill); the budget is their sum
        other = tempfile.TemporaryDirectory()
        self.addCleanup(other.cleanup)
        manifest.add_job(self.run, job("a", 18))
        manifest.add_job(other.name, job("b", 44))
        out = subprocess.run([sys.executable, str(SCRIPT), "committed", self.run, other.name], check=True,
                             capture_output=True, text=True).stdout
        self.assertEqual(json.loads(out)["committed"], 62)

    def test_outcome_and_done_from_the_command_line(self) -> None:
        # e2e run 3: no command set a job's outcome, and a character job fetch.py can't download stayed "submitted"
        manifest.add_job(self.run, {"job_id": "c", "tool": "MCP create_character", "status": "submitted",
                                    "reported_usage": {"generations": 1}})
        for args in (["done", self.run, "c"], ["outcome", self.run, "c", "kept", "the canonical rotation"]):
            subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True, text=True)
        (entry,) = manifest.jobs(self.run)
        self.assertEqual((entry["status"], entry["outcome"], entry["outcome_note"]), ("ok", "kept", "the canonical rotation"))
        self.assertEqual(manifest.spent(self.run), 1)

    def test_typo_never_lowers_the_budget(self) -> None:
        # review: a mistyped run folder added 0 to committed, and outcome/done reported success on nothing
        missing = str(Path(self.run) / "nope")
        manifest.add_job(self.run, job("a", 6))
        for args in (["committed", self.run, missing], ["outcome", self.run, "zzz", "kept"], ["done", missing, "a"]):
            r = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, args)
        self.assertFalse(Path(missing).exists())

    def test_refetch_keeps_the_reported_usage(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        manifest.add_job(self.run, {"job_id": "a", "status": "ok", "waited_s": 3})
        self.assertEqual(manifest.spent(self.run), 6)

    def test_null_usage_counts_as_zero(self) -> None:
        manifest.add_job(self.run, {"job_id": "a", "status": "ok", "reported_usage": None})
        self.assertEqual(manifest.spent(self.run), 0)


if __name__ == "__main__":
    unittest.main()
