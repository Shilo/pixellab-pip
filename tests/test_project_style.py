from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from test_helpers import REPO_ROOT

STYLE = REPO_ROOT / "skills/pixellab-pip/assets/project_style.py"
ANALYZE = REPO_ROOT / "skills/pixellab-pip/assets/analyze_style.py"


def run(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(STYLE), *args], cwd=cwd, capture_output=True, text=True)


class ProjectStyleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def profile(self) -> dict:
        return json.loads((self.dir / "pixellab.json").read_text(encoding="utf-8"))

    def test_no_style_exit_4(self) -> None:
        r = run(self.dir, "show")
        self.assertEqual(r.returncode, 4)
        self.assertEqual(json.loads(r.stdout)["status"], "no_style")

    def test_old_profile_without_style_asks(self) -> None:
        # a pre-merge Game Art profile: project fields and house-style words, but no chosen style
        (self.dir / "pixellab.json").write_text(json.dumps(
            {"game": "x", "out": "pixellab_out", "look": "dark fantasy pixel art", "seed": 7}), encoding="utf-8")
        r = run(self.dir, "show")
        self.assertEqual(r.returncode, 4, r.stdout)

    def test_example_needs_explicit_pick(self) -> None:
        r = run(self.dir, "list")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Side-view dark fantasy", r.stdout)            # offered...
        self.assertFalse((self.dir / "pixellab.json").exists())       # ...but nothing written
        r = run(self.dir, "example", "Side-view dark fantasy", "--use")
        self.assertEqual(r.returncode, 0, r.stderr)
        shown = json.loads(run(self.dir, "show").stdout)
        self.assertEqual(shown["name"], "Side-view dark fantasy")
        self.assertEqual(shown["style"]["view"], "side")

    def test_save_from_json_and_use(self) -> None:
        (self.dir / "s.json").write_text(json.dumps({"look": "neon on black", "view": "side"}), encoding="utf-8")
        self.assertEqual(run(self.dir, "save", "cyber", "--from", "s.json", "--use").returncode, 0)
        self.assertEqual(json.loads(run(self.dir, "show").stdout)["style"]["look"], "neon on black")

    def test_rename_collision_refused(self) -> None:
        (self.dir / "s.json").write_text(json.dumps({"look": "a"}), encoding="utf-8")
        run(self.dir, "save", "one", "--from", "s.json")
        run(self.dir, "save", "two", "--from", "s.json")
        r = run(self.dir, "rename", "one", "two")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(set(self.profile()["styles"]), {"one", "two"})

    def test_anchor_path_relative_to_project(self) -> None:
        (self.dir / "art").mkdir()
        Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(self.dir / "art" / "hero.png")
        (self.dir / "s.json").write_text(json.dumps({"look": "a"}), encoding="utf-8")
        run(self.dir, "save", "one", "--from", "s.json", "--use")
        sub = self.dir / "deep" / "er"
        sub.mkdir(parents=True)
        r = run(sub, "anchor", "heroes", str(self.dir / "art" / "hero.png"), "--profile", str(self.dir / "pixellab.json"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.profile()["styles"]["one"]["anchors"]["heroes"], "art/hero.png")
        r = run(self.dir, "anchor", "heroes", "missing.png")
        self.assertNotEqual(r.returncode, 0)

    def test_side_view_examples_carry_animation_values(self) -> None:
        # e2e run 2: "Side-view sci-fi" had no canvas, frame or timing values, so the run borrowed dark fantasy's
        sys.path.insert(0, str(STYLE.parent))
        import project_style
        for name, ex in project_style.EXAMPLES.items():
            if ex.get("view") == "side":
                self.assertIn("canvas_overhead", ex.get("anim", {}), name)
                self.assertIn("timing_ms", ex.get("anim", {}), name)

    def test_atomic_save(self) -> None:
        (self.dir / "s.json").write_text(json.dumps({"look": "a"}), encoding="utf-8")
        run(self.dir, "save", "one", "--from", "s.json")
        self.assertEqual(list(self.dir.glob("*.tmp")), [])
        self.profile()

    def test_analyze_measures_without_writing_frames(self) -> None:
        img = Image.new("RGBA", (32, 32))
        for x in range(8, 24):
            for y in range(4, 30):
                img.putpixel((x, y), (200, 50, 50, 255))
        img.save(self.dir / "ref.png")
        r = subprocess.run([sys.executable, str(ANALYZE), str(self.dir / "ref.png"), "--out", str(self.dir / "a")],
                           capture_output=True, text=True)
        if r.returncode == 3:
            self.skipTest("numpy missing")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.dir / "a" / "analysis.json").exists())
        self.assertFalse((self.dir / "a" / "native").exists())


if __name__ == "__main__":
    unittest.main()
