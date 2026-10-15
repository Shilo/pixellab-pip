from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
HELPER = REPO_ROOT / "skills/pixellab-pip/assets/inspect_images.py"


class ImageInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)

    def run_helper(self, *args: str, expected_exit: int = 0) -> dict:
        result = subprocess.run(
            [sys.executable, str(HELPER), *args], cwd=self.root,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, expected_exit, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def save_animation(self, name: str, **options) -> Path:
        frames = [Image.new("RGB", (8, 8), color) for color in ("red", "green", "blue")]
        path = self.root / name
        frames[0].save(path, save_all=True, append_images=frames[1:], **options)
        return path

    def test_alpha_facts_and_read_only_source_integrity(self) -> None:
        Image.new("RGB", (4, 3), "red").save(self.root / "rgb.png")
        palette = Image.new("P", (4, 3), 0)
        palette.putpalette([0, 0, 0, 255, 0, 0] + [0] * 762)
        palette.putpixel((2, 1), 1)
        palette.save(self.root / "palette.png", transparency=0)
        partial = Image.new("RGBA", (4, 3), (100, 10, 20, 0))
        partial.putpixel((1, 2), (100, 10, 20, 120))
        partial.save(self.root / "partial.png")
        Image.new("RGBA", (4, 3), (100, 10, 20, 0)).save(self.root / "empty.png")
        before = {p.name: hashlib.sha256(p.read_bytes()).digest() for p in self.root.iterdir()}
        report = self.run_helper("rgb.png", "palette.png", "partial.png", "empty.png",
                                 "--expect-size", "4x3", "--expect-frames", "4")
        frames = [item["frames"][0] for item in report["files"]]
        self.assertEqual([f["alpha_extrema"] for f in frames],
                         [[255, 255], [0, 255], [0, 120], [0, 0]])
        self.assertEqual([f["bounds"] for f in frames],
                         [[0, 0, 4, 3], [2, 1, 3, 2], [1, 2, 2, 3], None])
        self.assertEqual(report["errors"], [])
        self.assertTrue(all("duration_ms" not in f for f in frames))
        self.assertTrue(all("loop" not in f for f in report["files"]))
        after = {p.name: hashlib.sha256(p.read_bytes()).digest() for p in self.root.iterdir()}
        self.assertEqual(before, after)

    def test_preserves_input_order_and_duplicate_inputs(self) -> None:
        for name in ("a.png", "z.png"):
            Image.new("RGB", (8, 8), "red").save(self.root / name)
        report = self.run_helper("z.png", "./a.png", "z.png", "--expect-frames", "3")
        self.assertEqual([f["path"] for f in report["files"]], ["z.png", "./a.png", "z.png"])

    def test_last_input_and_last_internal_frame_dimension_checks(self) -> None:
        Image.new("RGB", (8, 8), "red").save(self.root / "good.png")
        frames = [Image.new("RGB", size, "red") for size in ((8, 8), (8, 8), (9, 8))]
        frames[0].save(self.root / "last.tiff", save_all=True, append_images=frames[1:])
        report = self.run_helper("good.png", "last.tiff", "--expect-size", "8x8",
                                 "--expect-frames", "4", expected_exit=1)
        self.assertEqual([f["size"] for f in report["files"][1]["frames"]],
                         [[8, 8], [8, 8], [9, 8]])
        self.assertEqual(len(report["errors"]), 1)
        self.assertIn("last.tiff frame 2", report["errors"][0])

    def test_gif_variable_durations_missing_delay_and_loop(self) -> None:
        self.save_animation("timed.gif", duration=[40, 80, 120], loop=0)
        self.save_animation("zero.gif", duration=[40, 0, 120])
        # Remove frame 1's complete graphics-control extension, so its delay
        # is absent rather than an explicitly encoded zero.
        data = (self.root / "zero.gif").read_bytes()
        marker = b"\x21\xf9\x04"
        second_control = data.find(marker, data.index(marker) + 8)
        self.assertGreater(second_control, 0)
        (self.root / "missing.gif").write_bytes(data[:second_control] + data[second_control + 8:])
        self.save_animation("finite.gif", duration=50, loop=2)
        report = self.run_helper("timed.gif", "missing.gif", "finite.gif", "zero.gif",
                                 "--expect-frames", "12")
        self.assertEqual([f["loop"] for f in report["files"]], [0, None, 2, None])
        self.assertEqual([f["duration_ms"] for f in report["files"][0]["frames"]], [40, 80, 120])
        self.assertEqual([f["duration_ms"] for f in report["files"][1]["frames"]], [40, None, 120])
        self.assertEqual([f["duration_ms"] for f in report["files"][3]["frames"]], [40, 0, 120])
        self.assertEqual([f["index"] for f in report["files"][0]["frames"]], [0, 1, 2])

    def test_late_corruption_retains_decoded_frames_and_continues(self) -> None:
        animation = self.save_animation("late.gif", duration=40)
        animation.write_bytes(animation.read_bytes()[:-9])
        Image.new("RGB", (8, 8), "red").save(self.root / "good.png")
        report = self.run_helper("late.gif", "missing.png", "good.png", expected_exit=1)
        self.assertEqual(len(report["files"][0]["frames"]), 2)
        self.assertEqual(report["files"][1]["frames"], [])
        self.assertEqual(len(report["files"][2]["frames"]), 1)
        self.assertEqual(len(report["errors"]), 2)
        self.assertTrue(any("late.gif" in error for error in report["errors"]))
        self.assertTrue(any("missing.png" in error for error in report["errors"]))

    def test_total_expected_frame_count_mismatch(self) -> None:
        self.save_animation("timed.gif", duration=40)
        report = self.run_helper("timed.gif", "--expect-frames", "4", expected_exit=1)
        self.assertEqual(report["errors"], ["decoded 3 frames; expected 4"])

    def test_invalid_expectations_are_argument_errors(self) -> None:
        for args in (("--expect-size", "0x8"), ("--expect-size", "8"),
                     ("--expect-size", "8xno"), ("--expect-frames", "-1"),
                     ("--expect-frames", "0"), ("--expect-frames", "1.5")):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(HELPER), "input.png", *args],
                                        cwd=self.root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
