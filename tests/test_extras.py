from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from test_helpers import REPO_ROOT, load_module

ASSETS = REPO_ROOT / "skills/pixellab-pip/assets"
manifest = load_module("manifest", ASSETS / "manifest.py")
HAS_NUMPY = importlib.util.find_spec("numpy") is not None


def run(script: str, *args, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ASSETS / script), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


class ExtrasTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_history_sums_manifests(self) -> None:
        root = self.dir / "pixellab-pip-generations"
        for run_name, entries in {
            "knight": [("a", 6, "ok", "kept"), ("b", 6, "ok", "rerolled"), ("c", 6, "failed", None)],
            "slime": [("d", 1, "ok", "kept")],
        }.items():
            for job_id, gens, status, outcome in entries:
                entry = {"job_id": job_id, "tool": "MCP animate_image", "status": status,
                         "reported_usage": {"generations": gens}}
                if outcome:
                    entry["outcome"] = outcome
                manifest.add_job(str(root / run_name), entry)
        (root / "empty").mkdir()   # a folder without a manifest is not a run

        r = run("history.py", "--root", root, "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        runs = {item["name"]: item for item in json.loads(r.stdout)}
        self.assertEqual(set(runs), {"knight", "slime"})
        self.assertEqual(runs["knight"]["jobs"], 3)
        self.assertEqual(runs["knight"]["spent"], 12)   # the failed job is refunded
        self.assertEqual(runs["knight"]["outcomes"], {"kept": 1, "rerolled": 1})
        self.assertEqual(runs["slime"]["spent"], 1)

        r = run("history.py", "--root", root, "--json", "--runs", "1")
        self.assertEqual(len(json.loads(r.stdout)), 1)

    @unittest.skipUnless(HAS_NUMPY, "numpy is not installed")
    def test_showcase_finds_existing_moves(self) -> None:
        # only attack + skill exist: the default move list must not ask for idle
        for move in ("attack", "skill"):
            sheet = Image.new("RGBA", (48, 20))
            for k in range(3):
                sheet.paste((200, 40 * k, 60, 255), (16 * k + 4, 4, 16 * k + 12, 20))
            sheet.save(self.dir / f"k_{move}.png")
            frames = [{"frame": {"x": 16 * k, "y": 0, "w": 16, "h": 20}, "duration": 100} for k in range(3)]
            (self.dir / f"k_{move}.json").write_text(json.dumps({"frames": frames}), encoding="utf-8")
        r = run("showcase_gif.py", self.dir, "k")
        self.assertEqual(r.returncode, 0, r.stderr)
        with Image.open(self.dir / "k_showcase.gif") as gif:
            self.assertGreaterEqual(gif.n_frames, 3)
            # e2e demo: final GIFs carry no baked background unless asked (Asset Integrity)
            self.assertEqual(gif.convert("RGBA").getpixel((0, 0))[3], 0)
        # review: half-transparent edge pixels were blended onto the magenta key and came out pink
        soft = Image.new("RGBA", (16, 20))
        soft.paste((200, 40, 60, 255), (4, 4, 12, 20))
        soft.paste((200, 40, 60, 120), (4, 3, 12, 4))
        soft.save(self.dir / "s_attack.png")
        (self.dir / "s_attack.json").write_text(json.dumps({"frames": [{"frame": {"x": 0, "y": 0, "w": 16, "h": 20},
                                                                      "duration": 100}]}), encoding="utf-8")
        self.assertEqual(run("showcase_gif.py", self.dir, "s").returncode, 0)
        with Image.open(self.dir / "s_showcase.gif") as gif:
            px = list(gif.convert("RGBA").getdata())
        self.assertFalse([p for p in px if p[3] and p[0] > 200 and p[2] > 120 and p[1] < 100])   # any magenta mix
        r = run("showcase_gif.py", self.dir, "k", "--bg", "discord", "--out", self.dir / "dark.gif")
        self.assertEqual(r.returncode, 0, r.stderr)
        with Image.open(self.dir / "dark.gif") as gif:
            self.assertEqual(gif.convert("RGBA").getpixel((0, 0)), (43, 45, 49, 255))
        # a relative --out is from the caller's folder, not <dir>
        r = run("showcase_gif.py", self.dir.name, "k", "--out", "show.gif", cwd=self.dir.parent)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.dir.parent / "show.gif").exists())
        (self.dir.parent / "show.gif").unlink()

    @unittest.skipUnless(HAS_NUMPY, "numpy is not installed")
    def test_normal_map_directx_flips_green(self) -> None:
        sprite = Image.new("RGBA", (16, 16))
        sprite.paste((180, 150, 120, 255), (3, 3, 13, 13))
        normal = Image.new("RGBA", (16, 16))
        normal.paste((128, 200, 220, 255), (3, 3, 13, 13))   # tilted "up" in OpenGL terms
        sprite.save(self.dir / "s.png")
        normal.save(self.dir / "n.png")
        gl = run("normal_map.py", "preview", self.dir / "gl.gif", self.dir / "s.png", self.dir / "n.png")
        dx = run("normal_map.py", "preview", self.dir / "dx.gif", self.dir / "s.png", self.dir / "n.png", "--directx")
        self.assertEqual((gl.returncode, dx.returncode), (0, 0), gl.stderr + dx.stderr)
        with Image.open(self.dir / "gl_lights.png") as a, Image.open(self.dir / "dx_lights.png") as b:
            a, b = a.convert("RGB"), b.convert("RGB")
        # rows = light from left, top, right: the top-lit row is brighter for OpenGL "up" than flipped DirectX
        top = (8, 16 + 8)
        self.assertGreater(sum(a.getpixel(top)), sum(b.getpixel(top)))

    @unittest.skipUnless(HAS_NUMPY, "numpy is not installed")
    def test_tileset_preview_single_sheet(self) -> None:
        sheet, tiles = Image.new("RGBA", (16, 16)), []
        for i in range(16):
            bits = [(i >> s) & 1 for s in (3, 2, 1, 0)]
            x, y = (i % 4) * 4, (i // 4) * 4
            sheet.paste((40 + 50 * sum(bits), 120, 60, 255), (x, y, x + 4, y + 4))
            tiles.append({"bounding_box": {"x": x, "y": y, "width": 4, "height": 4},
                          "corners": dict(zip(("NW", "NE", "SW", "SE"),
                                              ("upper" if b else "lower" for b in bits)))})
        sheet.save(self.dir / "sheet.png")
        (self.dir / "sheet.json").write_text(json.dumps({"tileset_data": {"tiles": tiles}}), encoding="utf-8")
        r = run("tileset_preview.py", self.dir / "map.png", self.dir / "sheet.png", "--cells", "6")
        self.assertEqual(r.returncode, 0, r.stderr)
        with Image.open(self.dir / "map.png") as m:
            self.assertEqual(m.size, (6 * 4 * 2, 6 * 4 * 2))
        self.assertTrue((self.dir / "map_tiles.png").exists())

    def test_numpy_helpers_skip_without_numpy(self) -> None:
        for script, args in (("tileset_preview.py", ["m.png", "s.png"]),
                             ("normal_map.py", ["preview", "o.gif", "s.png", "n.png"]),
                             ("showcase_gif.py", [".", "k"])):
            code = ("import runpy, sys; sys.modules['numpy'] = None; "
                    f"sys.argv = [{script!r}] + {args!r}; runpy.run_path({str(ASSETS / script)!r}, run_name='__main__')")
            r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=self.dir)
            self.assertEqual(r.returncode, 3, script + r.stderr)
            self.assertEqual(json.loads(r.stdout)["status"], "skipped", script)


if __name__ == "__main__":
    unittest.main()
