from __future__ import annotations

import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from test_helpers import REPO_ROOT, load_module

sim = load_module("tileset_validation_sim", REPO_ROOT / "dev-tools/pixellab_mcp_tileset_sim.py")


class TilesetValidationTests(unittest.TestCase):
    def test_palette_requests_validate_without_claiming_rendered_palette(self):
        base = {"lower_description": "water", "upper_description": "grass", "mode": "pro"}
        for fields in ({"palette": ["#000000", "#ffffff"]}, {"max_colors": 2},
                       {"palette": ["000000", "ffffff"]},
                       {"palette": ["#000000", "#ffffff"], "palette_name": "1-bit", "max_colors": 2}):
            warnings = sim.validate_request("create_topdown_tileset", {**base, **fields}, 16, 16)
            self.assertTrue(any("does not enforce palette" in w for w in warnings))
            with self.assertRaisesRegex(SystemExit, "require mode='pro'"):
                sim.validate_request("create_topdown_tileset", {**base, **fields, "mode": "standard"}, 16, 16)
        for fields in ({"palette": ["#000000"]}, {"palette": ["", "#ffffff"]}, {"palette": [0, "#ffffff"]}, {"palette": True},
                       {"palette_name": "1-bit"}, {"max_colors": True}, {"max_colors": 1}, {"max_colors": 65}):
            with self.subTest(fields=fields), self.assertRaises(SystemExit):
                sim.validate_request("create_topdown_tileset", {**base, **fields}, 16, 16)
        with self.assertRaisesRegex(SystemExit, "MCP tools"):
            sim.validate_request("create_topdown_tileset", {**base, "outline": "single color black outline"}, 16, 16)
        with self.assertRaisesRegex(SystemExit, "Fields not exposed"):
            sim.validate_request("create_sidescroller_tileset", {"lower_description": "rock", "transition_description": "grass", "palette": ["#000000", "#ffffff"]}, 16, 16)

    def test_preview_refuses_ambiguous_and_tall_layouts_without_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Image.new("RGBA", (16, 32), (40, 80, 120, 255)).save(root / "sheet.png")
            tiles = [{"bounding_box": {"x": i % 4 * 4, "y": i // 4 * 4, "width": 4, "height": 4},
                      "corners": dict(zip(("NW", "NE", "SW", "SE"), ("upper" if b else "lower" for b in bits)))}
                     for i, bits in enumerate(itertools.product((0, 1), repeat=4))]
            unknown = json.loads(json.dumps(tiles))
            unknown[0]["corners"]["NW"] = "unknown"
            for i, case in enumerate((tiles + tiles[:9], tiles[:-1] + [tiles[0]], unknown, tiles)):
                (root / "sheet.json").write_text(json.dumps({"tileset_data": {"tiles": case}}), encoding="utf-8")
                out = root / f"map{i}.png"
                p = subprocess.run([sys.executable, str(REPO_ROOT / "skills/pixellab-pip/assets/tileset_preview.py"),
                                    str(out), str(root / "sheet.png"), "--cells", "6"], capture_output=True, text=True)
                self.assertEqual(p.returncode == 0, i == 3, p.stderr)
                self.assertEqual(out.exists(), i == 3)
                self.assertEqual(out.with_stem(out.stem + "_tiles").exists(), i == 3)
