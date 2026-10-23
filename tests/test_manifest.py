from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_helpers import REPO_ROOT, load_module

SCRIPT = REPO_ROOT / "skills/pixellab-pip/assets/manifest.py"
manifest = load_module("manifest", SCRIPT)


def job(job_id: str, gens: float, status: str = "ok") -> dict:
    return {"job_id": job_id, "tool": "MCP animate_image", "seed": 7, "status": status,
            "reported_usage": {"generations": gens}, "waited_s": 40, "outputs": ["raw/0.png"]}


def bounded_plan() -> dict:
    return {"scope": "one knight attack", "generation_cap": 12.5, "retry_limit": 2,
            "retries_used": 0, "remaining_work": ["review exact poses", "interpolate approved poses"],
            "approval_context": "Current user approved this named chain in the conversation."}


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

    def test_plan_cli_initializes_only_empty_runs_and_preserves_existing_audit(self) -> None:
        with tempfile.TemporaryDirectory() as source:
            path = Path(source) / "plan.json"
            path.write_text(json.dumps(bounded_plan()), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "plan", self.run, str(path)],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["authority"])
        manifest.add_job(self.run, job("first", 3))
        ledger = Path(self.run) / "manifest.json"
        data = json.loads(ledger.read_text(encoding="utf-8"))
        data["audit"] = "retain"
        data["plan"]["old_note"] = "retain too"
        ledger.write_text(json.dumps(data), encoding="utf-8")
        updated = {**bounded_plan(), "retries_used": 1, "remaining_work": []}
        manifest.set_plan(self.run, updated)
        data = json.loads(ledger.read_text(encoding="utf-8"))
        self.assertEqual(data["jobs"][0]["job_id"], "first")
        self.assertEqual(data["audit"], "retain")
        self.assertEqual(data["plan"], {**updated, "old_note": "retain too"})

    def test_invalid_plan_preserves_ledger_bytes(self) -> None:
        manifest.add_job(self.run, job("a", 3))
        ledger = Path(self.run) / "manifest.json"
        before = ledger.read_bytes()
        invalid = [{**bounded_plan(), "generation_cap": value} for value in (-1, float("nan"), True, "12")]
        invalid += [{**bounded_plan(), key: value} for key, value in
                    (("retry_limit", 1.5), ("retry_limit", True), ("retries_used", 3),
                     ("retries_used", -1), ("remaining_work", "unfinished"), ("remaining_work", [""]),
                     ("scope", " "), ("approval_context", ""))]
        invalid += [None, {"scope": "missing fields"}, {**bounded_plan(), "unexpected": 1}]
        for plan in invalid:
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                manifest.set_plan(self.run, plan)
            self.assertEqual(ledger.read_bytes(), before)

    def test_plan_does_not_initialize_missing_resume_accounting(self) -> None:
        source = Path(self.run) / "existing.png"
        source.write_bytes(b"unchanged")
        with self.assertRaisesRegex(ValueError, "missing manifest in a nonempty run"):
            manifest.set_plan(self.run, bounded_plan())
        self.assertFalse((Path(self.run) / "manifest.json").exists())
        self.assertEqual(source.read_bytes(), b"unchanged")

    def test_plan_cli_invalid_input_leaves_existing_ledger_unchanged(self) -> None:
        manifest.add_job(self.run, job("a", 4))
        ledger = Path(self.run) / "manifest.json"
        before = ledger.read_bytes()
        with tempfile.TemporaryDirectory() as source:
            path = Path(source) / "plan.json"
            for raw in (b'{"scope":', b'[]', b' ' * (1024 * 1024 + 1)):
                path.write_bytes(raw)
                result = subprocess.run([sys.executable, str(SCRIPT), "plan", self.run, str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(ledger.read_bytes(), before)

    def test_unrecognized_old_plan_does_not_break_unrelated_ledger_updates(self) -> None:
        ledger = Path(self.run) / "manifest.json"
        ledger.write_text(json.dumps({"jobs": [], "plan": {"historical": "unknown schema"}}), encoding="utf-8")
        manifest.add_job(self.run, job("a", 2))
        self.assertEqual(json.loads(ledger.read_text(encoding="utf-8"))["plan"], {"historical": "unknown schema"})

    def test_failed_status_does_not_prove_a_refund(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        manifest.add_job(self.run, job("b", 9, status="failed"))
        self.assertEqual(manifest.spent(self.run), 15)
        self.assertEqual(manifest.committed(self.run), 15)
        manifest.add_job(self.run, {"job_id": "b", "reported_usage": {"generations": 0}})
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
                                    "estimated_usage": {"generations": 4}})
        with self.assertRaisesRegex(ValueError, "unknown generations"):
            manifest.spent(self.run)
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

    def test_download_retries_preserve_status_and_all_saved_outputs(self) -> None:
        manifest.add_job(self.run, job("a", 6))
        manifest.add_job(self.run, {"job_id": "a", "status": "submitted"})
        manifest.add_job(self.run, {"job_id": "a", "status": "ok", "outputs": ["copy/0.png", "raw/0.png"]})
        entry = manifest.jobs(self.run)[0]
        self.assertEqual(entry["status"], "ok")
        self.assertEqual(entry["outputs"], ["raw/0.png", "copy/0.png"])
        self.assertEqual(manifest.spent(self.run), 6)

    def test_null_usage_is_unknown_not_zero(self) -> None:
        manifest.add_job(self.run, {"job_id": "a", "status": "ok", "reported_usage": None})
        for fn in (manifest.spent, manifest.committed):
            with self.assertRaisesRegex(ValueError, "unknown generations"):
                fn(self.run)

    def test_unknown_charge_keeps_estimate_across_failure(self) -> None:
        for status in ("submitted", "timeout", "failed", "ok"):
            manifest.add_job(self.run, {"job_id": "a", "status": status, "estimated_usage": {"generations": 7}})
            self.assertEqual(manifest.committed(self.run), 7)
            with self.assertRaises(ValueError):
                manifest.spent(self.run)
        manifest.add_job(self.run, {"job_id": "a", "reported_usage": {"generations": 0}})
        self.assertEqual(manifest.committed(self.run), 0)

    def test_invalid_shape_or_usage_never_replaces_existing_bytes(self) -> None:
        path = Path(self.run) / "manifest.json"
        for bad in ({"calls": [], "audit": "keep"}, {"jobs": {}}, {"jobs": [None]},
                    {"jobs": [job("a", 1), job("a", 2)]}):
            raw = json.dumps(bad)
            path.write_text(raw, encoding="utf-8")
            with self.assertRaises(ValueError):
                manifest.add_job(self.run, job("next", 1))
            self.assertEqual(path.read_text(encoding="utf-8"), raw)
        path.unlink()
        for bad in (-1, float("nan"), float("inf"), True, "5", None):
            with self.assertRaises(ValueError):
                manifest.add_job(self.run, job("bad", bad))
        self.assertFalse(path.exists())

    def test_preserves_root_request_and_usage_metadata(self) -> None:
        path = Path(self.run) / "manifest.json"
        original = job("a", 1)
        original["reported_usage"]["usd"] = 0.04
        original["request"] = {"description": "a blue knight"}
        path.write_text(json.dumps({"jobs": [original], "audit": {"keep": True}}), encoding="utf-8")
        manifest.add_job(self.run, {"job_id": "a", "reported_usage": {"generations": 2}, "status": "ok"})
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["audit"], {"keep": True})
        self.assertEqual(data["jobs"][0]["request"], original["request"])
        self.assertEqual(data["jobs"][0]["reported_usage"], {"generations": 2, "usd": 0.04})
        self.assertNotIn("created_at", data["jobs"][0])  # do not invent a historical date

    def test_cli_estimate_is_not_reported_charge(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "add", self.run, "a", "--estimate", "5"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = manifest.jobs(self.run)[0]
        self.assertNotIn("reported_usage", entry)
        self.assertIn("created_at", entry)
        self.assertEqual(manifest.committed(self.run), 5)
        self.assertEqual(manifest.main(["spent", self.run]), 2)

    def test_concurrent_process_mutations_keep_all_jobs_and_outcomes(self) -> None:
        manifest.add_job(self.run, job("base", 2))
        snippets = [f"manifest.add_job({self.run!r}, {job(str(i), 6)!r})" for i in range(6)]
        snippets += [f"manifest.set_outcome({self.run!r}, 'base', 'kept')",
                     f"manifest.add_job({self.run!r}, {{'job_id': 'base', 'status': 'ok'}})",
                     f"manifest.set_plan({self.run!r}, {bounded_plan()!r})"]
        processes = []
        for snippet in snippets:
            code = (f"import sys,time; sys.path.insert(0,{str(SCRIPT.parent)!r}); import manifest; "
                    "original=manifest._read; "
                    "manifest._read=lambda *a,**k: (lambda data: (time.sleep(.1),data)[1])(original(*a,**k)); "
                    + snippet)
            processes.append(subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE))
        for process in processes:
            _, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, stderr)
        self.assertEqual(len(manifest.jobs(self.run)), 7)
        self.assertEqual(manifest.committed(self.run), 38)
        self.assertEqual(manifest.jobs(self.run)[0]["outcome"], "kept")
        self.assertEqual(json.loads((Path(self.run) / "manifest.json").read_text(encoding="utf-8"))["plan"], bounded_plan())

    def test_abandoned_lock_is_not_stolen(self) -> None:
        lock = Path(self.run) / ".manifest.lock"
        lock.touch()
        original_timeout = manifest.LOCK_TIMEOUT
        manifest.LOCK_TIMEOUT = 0
        try:
            with self.assertRaisesRegex(ValueError, "verify no writer"):
                manifest.add_job(self.run, job("a", 1))
        finally:
            manifest.LOCK_TIMEOUT = original_timeout
        self.assertTrue(lock.exists())

    def test_transient_permission_error_retries_exclusive_lock_acquisition(self) -> None:
        original_open = manifest.os.open
        attempts = []

        def deny_once(path, flags, *args, **kwargs):
            if Path(path).name == ".manifest.lock":
                attempts.append(flags)
                if len(attempts) == 1:
                    raise PermissionError(13, "temporarily unavailable", str(path))
            return original_open(path, flags, *args, **kwargs)

        with patch.object(manifest.os, "open", side_effect=deny_once):
            manifest.add_job(self.run, job("a", 3))
        self.assertEqual(len(attempts), 2)
        self.assertTrue(all(flags & manifest.os.O_EXCL for flags in attempts))
        self.assertEqual(manifest.spent(self.run), 3)
        self.assertFalse((Path(self.run) / ".manifest.lock").exists())

    def test_transient_replace_denial_retries_same_prepared_file_under_lock(self) -> None:
        manifest.add_job(self.run, job("a", 3))
        ledger = Path(self.run) / "manifest.json"
        before = ledger.read_bytes()
        original_replace = manifest.os.replace
        attempts = []

        def deny_once(source, destination):
            self.assertTrue((Path(self.run) / ".manifest.lock").exists())
            self.assertEqual(ledger.read_bytes(), before)
            prepared = Path(source).read_bytes()
            attempts.append((source, destination, prepared))
            if len(attempts) == 1:
                raise PermissionError(13, "reader temporarily prevents replacement")
            return original_replace(source, destination)

        with patch.object(manifest.os, "replace", side_effect=deny_once):
            manifest.set_plan(self.run, bounded_plan())
        self.assertEqual(len(attempts), 2)
        self.assertEqual(attempts[0], attempts[1])
        data = json.loads(ledger.read_text(encoding="utf-8"))
        self.assertEqual(data["jobs"][0]["job_id"], "a")
        self.assertEqual(data["plan"], bounded_plan())
        self.assertEqual(list(Path(self.run).glob(".manifest.*.tmp")), [])
        self.assertFalse((Path(self.run) / ".manifest.lock").exists())

    def test_persistent_replace_denial_preserves_manifest_and_cleans_owned_files(self) -> None:
        manifest.add_job(self.run, job("a", 3))
        ledger = Path(self.run) / "manifest.json"
        before = ledger.read_bytes()
        with patch.object(manifest, "LOCK_TIMEOUT", 0), patch.object(manifest.os, "replace", side_effect=PermissionError(13, "access denied")):
            with self.assertRaisesRegex(ValueError, "existing manifest left unchanged"):
                manifest.set_plan(self.run, bounded_plan())
        self.assertEqual(ledger.read_bytes(), before)
        self.assertEqual(list(Path(self.run).glob(".manifest.*.tmp")), [])
        self.assertFalse((Path(self.run) / ".manifest.lock").exists())

    def test_persistent_permission_error_preserves_unowned_lock_and_manifest(self) -> None:
        manifest.add_job(self.run, job("a", 3))
        path = Path(self.run) / "manifest.json"
        before = path.read_bytes()
        lock = Path(self.run) / ".manifest.lock"
        lock.write_text("unowned")
        with patch.object(manifest, "LOCK_TIMEOUT", 0), patch.object(manifest.os, "open", side_effect=PermissionError(13, "access denied")):
            with self.assertRaisesRegex(ValueError, "check directory permissions"):
                manifest.add_job(self.run, job("b", 4))
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(lock.read_text(), "unowned")


if __name__ == "__main__":
    unittest.main()
