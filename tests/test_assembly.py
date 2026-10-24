from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import PIL
from PIL import Image, ImageSequence
from test_helpers import load_module


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS = REPO_ROOT / "skills/pixellab-pip/assets"
assembly = load_module("assembly_security_guard", ASSETS / "_assembly.py")


def run(script: str, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ASSETS / script), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def frame(color, size=(8, 10), box=(2, 2, 6, 9)) -> Image.Image:
    image = Image.new("RGBA", size)
    if color:
        image.paste(color, box)
    return image


def save_frames(folder: Path, frames) -> list[Path]:
    paths = []
    for index, image in enumerate(frames):
        path = folder / f"f_{index}.png"
        image.save(path)
        paths.append(path)
    return paths


class PadSpriteTests(unittest.TestCase):
    def test_pad_feet_on_bottom_edge(self) -> None:
        # empty rows under the feet must not leave the feet above the canvas edge
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "s.png", Path(tmp) / "p.png"
            frame((90, 90, 90, 255), (20, 30), (5, 0, 15, 25)).save(src)
            r = run("pad_sprite.py", src, out, 40, 50, 5)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout), {"offset": [5, 25]})
            padded = Image.open(out)
            self.assertEqual(padded.size, (40, 50))
            self.assertEqual(padded.getpixel((10, 49))[3], 255)
            self.assertEqual(padded.getpixel((10, 24))[3], 0)

    def test_pad_refuses_a_sprite_that_does_not_fit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "s.png", Path(tmp) / "p.png"
            frame((90, 90, 90, 255), (20, 30), (0, 0, 20, 30)).save(src)
            r = run("pad_sprite.py", src, out, 30, 30, 15)
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse(out.exists())


class MakeSheetTests(unittest.TestCase):
    def test_sheet_frame_count_equals_input(self) -> None:
        red, blue = (255, 0, 0, 255), (0, 0, 255, 255)
        frames = [frame(red), frame(red), frame(blue), frame(None), frame(None)]
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), frames)
            stem = Path(tmp) / "k_idle"
            r = run("make_sheet.py", stem, *paths)
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(stem.with_suffix(".json").read_text())
            sheet = Image.open(stem.with_suffix(".png")).convert("RGBA")
            self.assertEqual(len(data["frames"]), 5)
            self.assertEqual(data["meta"]["pixellab"]["frame_count"], 5)
            self.assertEqual(sheet.size, (40, 10))
            for index, source in enumerate(frames):
                rect = data["frames"][index]["frame"]
                cell = sheet.crop((rect["x"], rect["y"], rect["x"] + rect["w"], rect["y"] + rect["h"]))
                self.assertEqual(list(cell.getdata()), list(source.getdata()))

    def test_hit_hold_moves_to_hit(self) -> None:
        # durations are the caller's metadata: the hold stays where given and the hit frame is recorded
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), [frame((k * 40, 0, 0, 255)) for k in range(5)])
            stem = Path(tmp) / "k_attack"
            r = run("make_sheet.py", stem, *paths, "--durations", "160,60,140,60,120", "--hit", "2",
                    "--pad", "24,56", "--facing", "right", "--godot", "sprites/hero")
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(stem.with_suffix(".json").read_text())
            self.assertEqual([f["duration"] for f in data["frames"]], [160, 60, 140, 60, 120])
            self.assertEqual(data["meta"]["pixellab"],
                             {"frame_count": 5, "hit_frame": 2, "pad_offset": {"x": 24, "y": 56}, "facing": "right"})
            tres = stem.with_suffix(".tres").read_text()
            self.assertIn('path="res://sprites/hero/k_attack.png"', tres)
            self.assertEqual(tres.count('"texture": SubResource('), 5)

    def test_sheet_refuses_mixed_sizes_and_bad_durations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), [frame((255, 0, 0, 255)), frame((255, 0, 0, 255), (9, 10))])
            self.assertNotEqual(run("make_sheet.py", Path(tmp) / "a", *paths).returncode, 0)
            self.assertNotEqual(run("make_sheet.py", Path(tmp) / "b", paths[0], "--durations", "1,2").returncode, 0)
            self.assertNotEqual(run("make_sheet.py", Path(tmp) / "c", paths[0], "--hit", "1").returncode, 0)


class ContactSheetTests(unittest.TestCase):
    def test_contact_sheet_wraps_at_10(self) -> None:
        # 20 frames once came out as one 10,368 px row
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), [frame((255, 0, 0, 255), (10, 10), (0, 0, 10, 10))] * 12)
            out = Path(tmp) / "s.png"
            r = run("contact_sheet.py", out, *paths)
            self.assertEqual(r.returncode, 0, r.stderr)
            sheet = Image.open(out).convert("RGBA")
            row = sheet.height // 2
            self.assertEqual(sheet.width, 100)
            self.assertEqual(sheet.getpixel((15, row + 5)), (255, 0, 0, 255))   # 12th frame, second row
            self.assertEqual(sheet.getpixel((25, row + 5))[3], 0)               # no 13th frame

    def test_contact_sheet_keeps_order_and_labels(self) -> None:
        colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255)]
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), [frame(c, (10, 10), (0, 0, 10, 10)) for c in colors])
            out = Path(tmp) / "s.png"
            r = run("contact_sheet.py", out, *paths)
            self.assertEqual(r.returncode, 0, r.stderr)
            sheet = Image.open(out).convert("RGBA")
            self.assertEqual([sheet.getpixel((10 * k + 5, 5)) for k in range(3)], colors)
            self.assertEqual(sheet.getpixel((5, 5))[3], 255)
            label = sheet.crop((0, 10, 10, sheet.height))
            self.assertIsNotNone(label.getchannel("A").getbbox())          # a label strip under each candidate


class FaithfulPreviewTests(unittest.TestCase):
    def test_faithful_gif_identical_frames(self) -> None:
        # GIF writers merge repeated frames; a faithful preview keeps every frame, its pixels and its timing
        red, blue = (255, 0, 0, 255), (0, 0, 255, 255)
        frames = [frame(red), frame(red), frame(blue), frame(None), frame(None)]
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), frames)
            out = Path(tmp) / "p.gif"
            r = run("preview_gif.py", out, *paths, "--durations", "100,100,200,100,300")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(json.loads(r.stdout)["exact"])
            with Image.open(out) as gif:
                decoded = [(f.convert("RGBA"), f.info.get("duration")) for f in ImageSequence.Iterator(gif)]
            self.assertEqual(len(decoded), 5)
            self.assertEqual([d for _, d in decoded], [100, 100, 200, 100, 300])
            for (image, _), source in zip(decoded, frames):
                self.assertEqual(image.size, source.size)
                for got, want in zip(image.getdata(), source.getdata()):
                    self.assertEqual(got[3], want[3])
                    if want[3]:
                        self.assertEqual(got, want)

    def test_faithful_needs_one_duration_per_frame(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), [frame((255, 0, 0, 255))] * 2)
            r = run("preview_gif.py", Path(tmp) / "p.gif", *paths, "--durations", "100")
            self.assertNotEqual(r.returncode, 0)


class OutputIntegrityTests(unittest.TestCase):
    def test_outdated_or_uncertain_pillow_is_blocked_before_decode(self):
        for version in ("12.3.0", "13.0.0rc1", "13.0.0.dev0", "unknown"):
            with self.subTest(version=version), patch.object(PIL, "__version__", version), patch.object(Image, "open", side_effect=AssertionError("decoder must not run")):
                with self.assertRaisesRegex(ImportError, "Pillow 13.0.0"):
                    assembly.load_pillow()
        self.assertIs(assembly.load_pillow(), Image)

    def test_all_guarded_helper_families_skip_before_old_pillow_decodes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, args in (("preview_gif.py", ["preview.gif", "input.png"]),
                               ("normal_map.py", ["preview", "preview.gif", "input.png", "normal.png"]),
                               ("fetch.py", ["j", "raw.png", "--run", "run", "--url", "https://backblaze.pixellab.ai/file/x.png"])):
                script = ASSETS / name
                code = (f"import PIL,runpy,sys; PIL.__version__='12.3.0'; sys.path.insert(0,{str(ASSETS)!r}); "
                        f"sys.argv={[name, *args]!r}; runpy.run_path({str(script)!r},run_name='__main__')")
                result = subprocess.run([sys.executable, "-c", code], cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], "skipped")
            self.assertEqual(list(root.iterdir()), [])

    def test_all_destinations_are_preflighted_before_source_or_sidecar_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "source.png"
            frame((40, 80, 120, 255)).save(src)
            before = src.read_bytes()
            for script, args in (
                    ("pad_sprite.py", [src, src, 8, 10, 0, 0]),
                    ("contact_sheet.py", [src, src]),
                    ("make_sheet.py", [src.with_suffix(""), src]),
                    ("preview_gif.py", [src, src])):
                with self.subTest(script=script):
                    self.assertNotEqual(run(script, *args).returncode, 0)
                    self.assertEqual(src.read_bytes(), before)
            stem = root / "export"
            stem.with_suffix(".json").write_text("old sidecar")
            self.assertNotEqual(run("make_sheet.py", stem, src).returncode, 0)
            self.assertFalse(stem.with_suffix(".png").exists())
            self.assertEqual(stem.with_suffix(".json").read_text(), "old sidecar")

    def test_hardlink_alias_is_protected(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            src, alias = Path(tmp) / "source.png", Path(tmp) / "alias.png"
            frame((40, 80, 120, 255)).save(src)
            try:
                os.link(src, alias)
            except OSError as exc:
                self.skipTest(str(exc))
            before = src.read_bytes()
            self.assertNotEqual(run("pad_sprite.py", src, alias, 8, 10, 0, 0).returncode, 0)
            self.assertEqual(src.read_bytes(), before)

    def test_dangling_symlink_is_an_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, alias, target = root / "source.png", root / "alias.png", root / "unexpected.png"
            frame((40, 80, 120, 255)).save(src)
            try:
                alias.symlink_to(target)
            except OSError as exc:
                self.skipTest(str(exc))
            self.assertNotEqual(run("pad_sprite.py", src, alias, 8, 10, 0, 0).returncode, 0)
            self.assertTrue(alias.is_symlink())
            self.assertFalse(target.exists())

    def test_unrequested_hit_metadata_is_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_frames(Path(tmp), [frame((200, 0, 0, 255))])
            stem = Path(tmp) / "idle"
            self.assertEqual(run("make_sheet.py", stem, *paths).returncode, 0)
            data = json.loads(stem.with_suffix(".json").read_text())
            self.assertNotIn("hit_frame", data["meta"]["pixellab"])

    def test_gif_opaque_repeats_partial_alpha_and_invalid_timing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            opaque = Image.new("RGBA", (4, 4), (200, 30, 70, 255))
            paths = save_frames(root, [opaque, opaque, frame((10, 60, 150, 120), (4, 4), (0, 0, 4, 4))])
            out = root / "preview.gif"
            result = run("preview_gif.py", out, *paths)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)["exact"])
            with Image.open(out) as image:
                self.assertEqual(image.n_frames, 3)
            for timing in ("0,100,100", "-1,100,100"):
                bad = root / ("bad" + timing.split(',')[0] + ".gif")
                self.assertNotEqual(run("preview_gif.py", bad, *paths, "--durations", timing).returncode, 0)
                self.assertFalse(bad.exists())

    def test_gif_quantization_preserves_declared_frames_and_reports_approximation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Image.new("RGBA", (20, 20))
            source.putdata([(i % 256, (i * 7) % 256, (i // 256) * 50, 255) for i in range(400)])
            paths = save_frames(Path(tmp), [source, source])
            result = run("preview_gif.py", Path(tmp) / "many.gif", *paths)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertFalse(report["exact"])
            self.assertTrue(report["colors_quantized"])
            self.assertEqual(report["frames"], 2)


if __name__ == "__main__":
    unittest.main()
