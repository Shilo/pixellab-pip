"""The animation doctor under Pip's rules: optional dependencies skip cleanly, and re-roll plans name the original
job from the run's manifest.json."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_helpers import REPO_ROOT, load_module

FIX = REPO_ROOT / "skills/pixellab-pip/assets/fix.py"


class DoctorRuleTests(unittest.TestCase):
    def test_doctor_skips_without_numpy(self) -> None:
        code = ("import runpy, sys; sys.modules['numpy'] = None; sys.argv = ['fix.py', 'frames']; "
                f"runpy.run_path({str(FIX)!r}, run_name='__main__')")
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertEqual(json.loads(r.stdout)["status"], "skipped")
        self.assertNotIn("Traceback", r.stderr)

    def test_plan_names_the_job_from_the_run_manifest(self) -> None:
        try:
            sys.path.insert(0, str(REPO_ROOT / "tests" / "doctor_cases"))
            import synth
        except ImportError as exc:   # numpy missing: the doctor is optional
            self.skipTest(str(exc))
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "run"
            fs = synth.walk(6)
            fs[2] = synth.drop_staff(fs[2])
            paths = synth.save(fs, run / "anim" / "clip", "hero_attack")
            outs = [str(Path(p).relative_to(run)).replace("\\", "/") for p in paths]
            (run / "manifest.json").write_text(json.dumps({"jobs": [
                {"job_id": "j-1", "tool": "MCP animate_image", "status": "ok",
                 "reported_usage": {"generations": 4}, "outputs": outs}]}), encoding="utf-8")
            r = subprocess.run([sys.executable, str(FIX), str(run / "anim" / "clip"), "--out", str(Path(tmp) / "o"),
                                "--check-only"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            report = json.loads((Path(tmp) / "o" / "fix_report.json").read_text(encoding="utf-8"))
            plans = report["anims"][0]["plans"]
            self.assertTrue(plans and plans[0]["job"]["job_id"] == "j-1", plans)

    def test_table_with_frames_still_checks_them(self) -> None:
        # e2e demo: --table printed the table and exited, so the frames were never checked
        try:
            sys.path.insert(0, str(REPO_ROOT / "tests" / "doctor_cases"))
            import synth
        except ImportError as exc:
            self.skipTest(str(exc))
        with tempfile.TemporaryDirectory() as tmp:
            synth.save(synth.walk(4), Path(tmp) / "clip", "hero_attack")
            r = subprocess.run([sys.executable, str(FIX), str(Path(tmp) / "clip"), "--out", str(Path(tmp) / "o"),
                                "--check-only", "--table"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((Path(tmp) / "o" / "fix_report.json").exists())

    def test_no_drop_proposed_for_an_effect_frame(self) -> None:
        # e2e run 2: --fx 7 marked the swing smear "not judged", yet the doctor proposed dropping it
        try:
            sys.path.insert(0, str(REPO_ROOT / "tests" / "doctor_cases"))
            import conftest  # noqa: F401  (puts the doctor's folder on the path)
            import synth
            from test_measure_clean import anim
        except ImportError as exc:
            self.skipTest(str(exc))
        fix = load_module("fix_doctor", FIX)
        fs = synth.walk(6)
        g = fs[3].copy()   # a change free fixes can't cure, so only a drop is left to offer
        head = ((g[..., :3] == synth.SKIN).all(-1) | (g[..., :3] == synth.HAIR).all(-1)) & (g[..., 3] > 0)
        g[head, :3] = (200, 60, 60)
        fs[3] = g
        _, res = fix.doctor(anim(fs), set(), None, None, "r.json", False, fx={3})
        self.assertFalse([c for c in res["changes"] if 3 in c.frames], res["changes"])

    def test_refuses_an_output_folder_that_holds_the_inputs(self) -> None:
        # final review: --out equal to the input folder wrote over raw PixelLab frames
        try:
            sys.path.insert(0, str(REPO_ROOT / "tests" / "doctor_cases"))
            import synth
        except ImportError as exc:
            self.skipTest(str(exc))
        with tempfile.TemporaryDirectory() as tmp:
            fs = synth.walk(4)
            fs[2] = synth.bright(fs[2], 1.6)
            paths = synth.save(fs, Path(tmp) / "clip", "hero_attack")
            before = [Path(p).read_bytes() for p in paths]
            r = subprocess.run([sys.executable, str(FIX), str(Path(tmp) / "clip"), "--out", str(Path(tmp) / "clip")],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertNotIn("Traceback", r.stderr)
            self.assertEqual([Path(p).read_bytes() for p in paths], before)


if __name__ == "__main__":
    unittest.main()
