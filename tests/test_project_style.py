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

    def test_missing_reference_is_listed_and_missing_source_is_named(self) -> None:
        (self.dir / "pixellab.json").write_text(json.dumps({"look": "town", "reference": "art/old.png"}), encoding="utf-8")
        r = run(self.dir, "show")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("reference", json.loads(r.stdout)["invalid_anchors"])
        r = run(self.dir, "save", "town", "--from", "typo.json")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not found", r.stdout + r.stderr)

    def test_outdated_pillow_preserves_profile_reads_and_blocks_new_anchor(self) -> None:
        import os
        package = self.dir / "PIL"
        package.mkdir()
        (package / "__init__.py").write_text('__version__ = "12.3.0"\n', encoding="utf-8")
        (package / "Image.py").write_text('raise AssertionError("unsafe decoder imported")\n', encoding="utf-8")
        image = self.dir / "hero.png"
        Image.new("RGBA", (4, 4), (20, 40, 80, 255)).save(image)
        profile = self.dir / "pixellab.json"
        profile.write_text(json.dumps({"look": "town", "max_cost": 0, "anchors": {"heroes": "hero.png"},
                                       "styles": {"town": {}}, "active_style": "town"}), encoding="utf-8")
        before = profile.read_bytes()
        env = {**os.environ, "PYTHONPATH": str(self.dir), "PYTHONDONTWRITEBYTECODE": "1"}
        shown = subprocess.run([sys.executable, "-S", str(STYLE), "show"], cwd=self.dir, env=env,
                               capture_output=True, text=True)
        self.assertEqual(shown.returncode, 0, shown.stdout + shown.stderr)
        data = json.loads(shown.stdout)
        self.assertEqual(data["unverified_anchors"], ["heroes"])
        self.assertEqual(data["legacy_limits"], {"max_cost": 0})
        self.assertEqual(shown.stderr, "")
        saved = subprocess.run([sys.executable, "-S", str(STYLE), "anchor", "icons", str(image)],
                               cwd=self.dir, env=env, capture_output=True, text=True)
        self.assertNotEqual(saved.returncode, 0)
        self.assertIn("13", saved.stderr)
        self.assertEqual(saved.stdout, "")
        self.assertEqual(profile.read_bytes(), before)

    def test_legacy_top_level_appearance_is_read_without_mutation(self) -> None:
        # a pre-merge Game Art profile: project fields and house-style words, but no chosen style
        (self.dir / "pixellab.json").write_text(json.dumps(
            {"game": "x", "out": "pixellab_out", "look": "dark fantasy pixel art", "seed": 7}), encoding="utf-8")
        r = run(self.dir, "show")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(json.loads(r.stdout)["style"]["look"], "dark fantasy pixel art")
        self.assertNotIn("styles", self.profile())

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

    def test_recursive_selection_and_optout_keep_limits_without_mutation(self) -> None:
        image = self.dir / "hero.png"
        Image.new("RGBA", (8, 8), (20, 40, 80, 255)).save(image)
        profile = {"look": "old", "anchors": {"heroes": "hero.png"}, "max_cost": 0,
                   "ask_above": 3, "custom": {"keep": True},
                   "anim": {"frames": 8, "timing_ms": {"hit": 120, "frame": 80}},
                   "styles": {"main": {"look": "main", "auto": True, "engine": "unknown", "anim": {"timing_ms": {"hit": 200}}},
                              "other": {"look": "other", "anchors": {"heroes": None}, "negatives": []}},
                   "active_style": "main"}
        path = self.dir / "pixellab.json"
        path.write_text(json.dumps(profile), encoding="utf-8")
        before = path.read_bytes()
        shown = json.loads(run(self.dir, "show").stdout)
        self.assertEqual(shown["style"]["anim"], {"frames": 8, "timing_ms": {"hit": 200, "frame": 80}})
        self.assertEqual(shown["style"]["anchors"], {"heroes": "hero.png"})
        self.assertNotIn("auto", shown["style"])
        self.assertNotIn("engine", shown["style"])
        other = json.loads(run(self.dir, "show", "--style", "other").stdout)
        self.assertEqual(other["name"], "other")
        self.assertIsNone(other["style"]["anchors"]["heroes"])
        disabled = run(self.dir, "show", "--no-style")
        self.assertEqual(disabled.returncode, 4)
        self.assertEqual(json.loads(disabled.stdout)["legacy_limits"], {"max_cost": 0, "ask_above": 3})
        self.assertEqual(path.read_bytes(), before)

    def test_bad_profiles_and_limits_never_get_overwritten(self) -> None:
        path = self.dir / "pixellab.json"
        (self.dir / "style.json").write_text('{"look":"new"}', encoding="utf-8")
        cases = [[], {"styles": []}, {"styles": {"bad": []}}, {"styles": {"bad": {"anchors": []}}},
                 {"active_style": "missing"}, {"max_cost": -1}, {"max_cost": True},
                 {"ask_above": "unknown"}, {"max_cost": float("nan")}, {"sizes": {"hero": [0, 8]}},
                 {"anim": {"frames": []}}, {"anim": {"timing_ms": {"hit": "bad"}}}]
        for profile in cases:
            with self.subTest(profile=profile):
                path.write_text(json.dumps(profile), encoding="utf-8")
                before = path.read_bytes()
                result = run(self.dir, "save", "new", "--from", "style.json", "--use")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(path.read_bytes(), before)

    def test_save_does_not_select_or_replace_implicitly(self) -> None:
        (self.dir / "s.json").write_text('{"look":"a"}', encoding="utf-8")
        self.assertEqual(run(self.dir, "save", "one", "--from", "s.json").returncode, 0)
        self.assertNotIn("active_style", self.profile())
        before = (self.dir / "pixellab.json").read_bytes()
        self.assertNotEqual(run(self.dir, "save", "one", "--from", "s.json").returncode, 0)
        self.assertEqual((self.dir / "pixellab.json").read_bytes(), before)
        self.assertEqual(run(self.dir, "save", "one", "--from", "s.json", "--replace", "--use").returncode, 0)
        self.assertEqual(self.profile()["active_style"], "one")

    def test_anchor_validation_selection_and_replacement(self) -> None:
        (self.dir / "s.json").write_text('{"look":"a"}', encoding="utf-8")
        run(self.dir, "save", "one", "--from", "s.json", "--use")
        run(self.dir, "save", "two", "--from", "s.json")
        (self.dir / "bad.png").write_text("not an image", encoding="utf-8")
        self.assertNotEqual(run(self.dir, "anchor", "monsters", "bad.png").returncode, 0)
        Image.new("RGBA", (8, 8), (20, 40, 80, 255)).save(self.dir / "good.png")
        self.assertEqual(run(self.dir, "anchor", "monsters", "good.png", "--style", "two").returncode, 0)
        self.assertNotIn("anchors", self.profile()["styles"]["one"])
        self.assertEqual(self.profile()["active_style"], "one")
        self.assertNotEqual(run(self.dir, "anchor", "monsters", "good.png", "--style", "two").returncode, 0)
        self.assertEqual(run(self.dir, "anchor", "monsters", "good.png", "--style", "two", "--replace").returncode, 0)

    def test_missing_anchor_and_unknown_style_are_clear_errors(self) -> None:
        (self.dir / "pixellab.json").write_text(json.dumps(
            {"styles": {"one": {"anchors": {"heroes": "missing.png"}}}, "active_style": "one"}), encoding="utf-8")
        shown = run(self.dir, "show")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertIn("heroes", json.loads(shown.stdout)["invalid_anchors"])
        self.assertNotEqual(run(self.dir, "show", "--style", "unknown").returncode, 0)

    def test_source_relative_reference_rebased_and_checked_from_other_cwd(self) -> None:
        source = self.dir / "source"
        source.mkdir()
        Image.new("RGBA", (8, 8), (30, 50, 70, 255)).save(source / "hero.png")
        (source / "style.json").write_text('{"reference":"hero.png"}', encoding="utf-8")
        profile = self.dir / "pixellab.json"
        result = run(source, "save", "one", "--from", "style.json", "--profile", str(profile), "--use")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.profile()["styles"]["one"]["reference"], "source/hero.png")
        self.assertEqual(run(source, "show", "--profile", str(profile)).returncode, 0)
        (source / "hero.png").write_text("corrupt", encoding="utf-8")
        shown = run(source, "show", "--profile", str(profile))
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertIn("unreadable", json.loads(shown.stdout)["invalid_anchors"]["reference"])

    def test_rename_empty_name_preserves_profile(self) -> None:
        (self.dir / "s.json").write_text('{"look":"a"}', encoding="utf-8")
        run(self.dir, "save", "one", "--from", "s.json", "--use")
        before = (self.dir / "pixellab.json").read_bytes()
        self.assertNotEqual(run(self.dir, "rename", "one", "").returncode, 0)
        self.assertEqual((self.dir / "pixellab.json").read_bytes(), before)

    def test_failed_atomic_replace_preserves_profile(self) -> None:
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location("style_atomic", STYLE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = self.dir / "pixellab.json"
        path.write_text('{"custom":1}', encoding="utf-8")
        with patch.object(module.os, "replace", side_effect=OSError("failed write")):
            with self.assertRaises(OSError):
                module.save(str(path), {"custom": 2})
        self.assertEqual(json.loads(path.read_text()), {"custom": 1})
        self.assertEqual(list(self.dir.glob(".pixellab.*.tmp")), [])

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

    def test_analyzer_does_not_infer_large_scale_from_padding(self) -> None:
        image = Image.new("RGBA", (256, 256))
        for x, y, color in ((13, 27, (200, 30, 40, 255)), (15, 29, (30, 200, 40, 255))):
            image.putpixel((x, y), color)
        source = self.dir / "padded.png"
        image.save(source)
        before = source.read_bytes()
        result = subprocess.run([sys.executable, str(ANALYZE), str(source), "--out", str(self.dir / "analysis")], capture_output=True, text=True)
        if result.returncode == 3:
            self.skipTest("numpy missing")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads((self.dir / "analysis/analysis.json").read_text())
        self.assertEqual(report["files"][0]["native_scale"], 1)
        self.assertIn("advisory", report)
        self.assertEqual(source.read_bytes(), before)
        small = Image.new("RGBA", (8, 8))
        for x, y, color in ((1, 2, (200, 30, 40, 255)), (5, 6, (30, 200, 40, 255))):
            small.putpixel((x, y), color)
        small.resize((32, 32), Image.NEAREST).save(self.dir / "upscaled.png")
        result = subprocess.run([sys.executable, str(ANALYZE), str(self.dir / "upscaled.png"), "--out", str(self.dir / "up")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.dir / "up/analysis.json").read_text())["files"][0]["native_scale"], 4)

    def test_analyzer_empty_art_and_existing_output_fail_without_writes(self) -> None:
        image = Image.new("RGBA", (8, 8))
        source = self.dir / "palette.png"
        image.save(source)
        result = subprocess.run([sys.executable, str(ANALYZE), str(source), "--out", str(self.dir / "empty")], capture_output=True, text=True)
        if result.returncode == 3:
            self.skipTest("numpy missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.dir / "empty").exists())
        image.putpixel((2, 3), (120, 20, 40, 255))
        image.save(source)
        before = source.read_bytes()
        result = subprocess.run([sys.executable, str(ANALYZE), str(source), "--out", str(self.dir)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse((self.dir / "analysis.json").exists())


if __name__ == "__main__":
    unittest.main()
