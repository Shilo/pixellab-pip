from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from test_helpers import bark


def run(*argv: str) -> tuple[int, dict]:
    original = sys.argv
    sys.argv = ["bark.py", *argv]
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            rc = bark.main()
    finally:
        sys.argv = original
    return rc, json.loads(out.getvalue())


class ApprovalLevelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.original = bark.SKILL_CONFIG
        bark.SKILL_CONFIG = Path(self.tmp.name) / "pixellab-pip.json"
        bark.SKILL_CONFIG.write_text('{"bark": true}\n', encoding="utf-8")

    def tearDown(self) -> None:
        bark.SKILL_CONFIG = self.original
        self.tmp.cleanup()

    def test_default_level_is_ask(self) -> None:
        rc, out = run("level")
        self.assertEqual(rc, 0)
        self.assertEqual((out["level"], out["budget"], out["retries"]), ("ask", None, 0))

    def test_auto_on_maps_to_auto(self) -> None:
        run("auto-on")
        self.assertEqual(run("level")[1]["level"], "auto")

    def test_plan_with_budget_persists(self) -> None:
        run("level", "plan", "45", "2")
        rc, out = run("level")
        self.assertEqual((out["level"], out["budget"], out["retries"]), ("plan", 45, 2))
        data = json.loads(bark.SKILL_CONFIG.read_text(encoding="utf-8"))
        self.assertIs(data["auto"], False)   # the per-job gate still shows the plan
        self.assertIs(data["bark"], True)    # other settings kept

    def test_extra_numbers_are_refused(self) -> None:
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            run("level", "plan", "100", "2", "7")
        self.assertEqual(cm.exception.code, 2)

    def test_level_auto_turns_auto_on(self) -> None:
        run("level", "auto", "100", "1")
        self.assertIs(json.loads(bark.SKILL_CONFIG.read_text(encoding="utf-8"))["auto"], True)

    def test_auto_off_after_a_level_returns_to_ask(self) -> None:
        # final review: auto-off left level=auto in place, so spending carried on after "auto off"
        run("level", "auto", "40")
        run("auto-off")
        self.assertEqual(run("level")[1]["level"], "ask")
        run("level", "plan", "40")
        run("auto-on")
        self.assertEqual(run("level")[1]["level"], "auto")

    def test_unknown_level_exit_2(self) -> None:
        with self.assertRaises(SystemExit) as ctx, redirect_stdout(io.StringIO()):
            original = sys.argv
            sys.argv = ["bark.py", "level", "yolo"]
            try:
                bark.main()
            finally:
                sys.argv = original
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
