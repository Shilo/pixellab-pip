from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_helpers import REPO_ROOT, load_module

ASSETS = REPO_ROOT / "skills/pixellab-pip/assets"
sys.path.insert(0, str(ASSETS))
paperdoll = load_module("paperdoll", ASSETS / "paperdoll.py")
Image = paperdoll.require_pillow()


def run(*args):
    return subprocess.run([sys.executable, str(ASSETS / "paperdoll.py"), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8")


class PaperdollTests(unittest.TestCase):
    def test_exact_overlay_and_cli_compose(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = Image.new("RGBA", (4, 4))
            base.putpixel((1, 1), (200, 100, 50, 255))
            edit = base.copy()
            edit.putpixel((1, 1), (40, 50, 60, 255))
            edit.putpixel((1, 0), (90, 100, 110, 120))
            base.save(root / "base.png")
            edit.save(root / "edit.png")
            original = (root / "base.png").read_bytes()
            result = run("extract", root / "base.png", root / "edit.png", "--region", 1, 0, 2, 2,
                         "--out", root / "cut")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "needs_visual_review")
            self.assertFalse(report["changes"]["semantic_layer_verified"])
            self.assertEqual(report["changes"]["changed_pixels"], 2)
            with Image.open(root / "cut/layer.png") as layer:
                self.assertEqual(layer.getpixel((1, 0)), (90, 100, 110, 120))
            result = run("compose", root / "base.png", root / "cut/layer.png", "--out", root / "stack")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with Image.open(root / "stack/composite.png") as combined:
                self.assertEqual(combined.tobytes(), edit.tobytes())
            self.assertEqual((root / "base.png").read_bytes(), original)

    def test_deletions_and_blended_alpha_are_refused(self):
        base = Image.new("RGBA", (2, 2), (100, 50, 20, 255))
        for pixel in [(0, 0, 0, 0), (200, 100, 40, 128)]:
            with self.subTest(pixel=pixel):
                edit = base.copy()
                edit.putpixel((0, 0), pixel)
                with self.assertRaisesRegex(ValueError, "cannot be reproduced"):
                    paperdoll.extract(base, edit)

    def test_outside_region_and_invalid_boxes_cannot_hide_redraws(self):
        base = Image.new("RGBA", (3, 3), (100, 50, 20, 255))
        edit = Image.new("RGBA", (3, 3), (200, 100, 40, 255))
        with self.assertRaisesRegex(ValueError, "outside"):
            paperdoll.extract(base, edit, [0, 0, 1, 1])
        for region in [[0, 0, 4, 3], [-1, 0, 1, 1], [1, 1, 1, 2]]:
            with self.subTest(region=region), self.assertRaisesRegex(ValueError, "region"):
                paperdoll.extract(base, edit, region)

    def test_hidden_rgb_is_not_a_change_and_sizes_must_match(self):
        base = Image.new("RGBA", (2, 2), (20, 30, 40, 0))
        with self.assertRaisesRegex(ValueError, "no visible change"):
            paperdoll.extract(base, Image.new("RGBA", (2, 2)))
        with self.assertRaisesRegex(ValueError, "same canvas"):
            paperdoll.extract(base, Image.new("RGBA", (3, 2)))

    def test_composition_uses_source_over_not_pixel_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = Image.new("RGBA", (1, 1), (20, 40, 60, 255))
            layer = Image.new("RGBA", (1, 1), (200, 100, 50, 128))
            base.save(root / "base.png")
            layer.save(root / "layer.png")
            result = run("compose", root / "base.png", root / "layer.png", "--out", root / "out")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with Image.open(root / "out/composite.png") as combined:
                self.assertEqual(combined.tobytes(), Image.alpha_composite(base, layer).tobytes())

    def test_no_outputs_for_invalid_inputs_or_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Image.new("RGBA", (2, 2), "red").save(root / "base.png")
            Image.new("RGBA", (3, 3), "blue").save(root / "wrong.png")
            result = run("compose", root / "base.png", root / "wrong.png", "--out", root / "out")
            self.assertEqual(result.returncode, 1)
            self.assertFalse((root / "out").exists())
            result = run("compose", root / "base.png", root / "base.png", "--out", root)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(Image.open(root / "base.png").getpixel((0, 0)), (255, 0, 0, 255))
            self.assertFalse((root / "composite.png").exists())

    def test_animated_input_and_outdated_pillow_are_refused_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Image.new("RGBA", (2, 2), "red").save(root / "anim.gif", save_all=True,
                        append_images=[Image.new("RGBA", (2, 2), "blue")], duration=100)
            result = run("compose", root / "anim.gif", root / "anim.gif", "--out", root / "out")
            self.assertEqual(result.returncode, 1)
            self.assertIn("2 frames", result.stderr)
            self.assertFalse((root / "out").exists())
            package = root / "PIL"
            package.mkdir()
            (package / "__init__.py").write_text('__version__ = "12.0.0"\n', encoding="utf-8")
            (package / "Image.py").write_text('raise AssertionError("decoder imported")\n', encoding="utf-8")
            result = subprocess.run([sys.executable, "-S", str(ASSETS / "paperdoll.py"), "extract",
                                    "missing.png", "missing.png", "--out", str(root / "out")],
                                   env={**os.environ, "PYTHONPATH": str(root)}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "skipped")
            self.assertFalse((root / "out").exists())

    def test_partial_output_is_removed_on_write_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out, source = root / "out", root / "source.png"
            image = Image.new("RGBA", (1, 1), "red")
            image.save(source)
            original = source.read_bytes()

            def fail_record(report, stream, **kwargs):
                self.assertTrue((out / "layer.png").is_file())
                stream.write('{"status":')
                raise OSError("write failed")

            for stage, patcher in (
                ("image", mock.patch.object(Image.Image, "save", side_effect=OSError("write failed"))),
                ("metadata", mock.patch.object(paperdoll.json, "dump", side_effect=fail_record)),
            ):
                with self.subTest(stage=stage), patcher:
                    with self.assertRaisesRegex(OSError, "write failed"):
                        paperdoll.write_outputs(out, image, "layer.png", [source],
                                                {"status": "needs_visual_review"})
                self.assertEqual(list(out.iterdir()), [])
                self.assertEqual(source.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
