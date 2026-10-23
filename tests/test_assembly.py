from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageSequence


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS = REPO_ROOT / "skills/pixellab-pip/assets"


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


if __name__ == "__main__":
    unittest.main()
