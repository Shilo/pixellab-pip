"""Paint a random test map from top-down 16-tile Wang tilesets the way an engine autotiles them, so seams,
wrong corners and a chain that does not match show up before the tiles go into a game.

    python tileset_preview.py <out.png> <sheet.png> [<sheet2.png> ...] [--cells 24] [--scale 2]

Each sheet needs its metadata beside it as <sheet>.json (the `/mcp/tilesets/{id}/image` sheet and its
`/metadata` JSON, per references/tileset.md). Several sheets = a chain in order (sea>beach, then beach>grass):
one more terrain level per sheet, each border drawn with the sheet for its two levels. Also writes
<out>_tiles.png: every tile with its corners (NW NE SW SE, 1 = upper); check the diagonals 0110 / 1001 there,
a random map rarely uses them. Needs Pillow and numpy; without them prints a skipped status and exits 3.
"""
import argparse
import json
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("out")
ap.add_argument("sheets", nargs="+")
ap.add_argument("--cells", type=int, default=24)
ap.add_argument("--scale", type=int, default=2)
a = ap.parse_args()
from _assembly import require_numpy, preflight_outputs  # noqa: E402

require_numpy()
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

if a.cells < 1 or a.scale < 1:
    ap.error("--cells and --scale must be positive")
out = Path(a.out)
tiles_png = out.with_name(out.stem + "_tiles.png")
preflight_outputs([out, tiles_png], a.sheets + [str(Path(p).with_suffix('.json')) for p in a.sheets])
sets = []   # per sheet: {(NW, NE, SW, SE) as 0/1: tile image}
for sheet in a.sheets:
    meta = Path(sheet).with_suffix(".json")
    img = Image.open(sheet).convert("RGBA")
    tiles = json.loads(meta.read_text(encoding="utf-8"))["tileset_data"]["tiles"]
    if any("transition" in t["corners"].values() for t in tiles):
        # ponytail: 16-tile sets only; 25-tile cliff sets need the wall-row rule (a wall fills the cell below)
        sys.exit(f"{meta} is a 25-tile set (transition corners); this preview handles 16-tile sets")
    lut = {}
    for t in tiles:
        b, c = t["bounding_box"], t["corners"]
        if (min(b['x'], b['y']) < 0 or min(b['width'], b['height']) <= 0
                or b['x'] + b['width'] > img.width or b['y'] + b['height'] > img.height):
            sys.exit("tile bounding box falls outside the source sheet")
        key = tuple(int(c[k] == "upper") for k in ("NW", "NE", "SW", "SE"))
        lut.setdefault(key, img.crop((b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"])))
    missing = [k for k in np.ndindex(2, 2, 2, 2) if k not in lut]
    if missing:
        sys.exit(f"{meta} lacks corner combinations {missing}")
    sets.append(lut)

tw, th = sets[0][(0, 0, 0, 0)].size
if any(t.size != (tw, th) for lut in sets for t in lut.values()):
    sys.exit("all tiles in the chain must have identical dimensions")
levels, cells = len(sets) + 1, a.cells
rng = np.random.default_rng(1)
coarse = rng.random((cells // 6 + 2, cells // 6 + 2))
field = np.asarray(Image.fromarray((coarse * 255).astype(np.uint8)).resize((cells + 1, cells + 1), Image.BICUBIC),
                   dtype=np.float32) / 255
v = np.clip((field * levels).astype(int), 0, levels - 1)
for _ in range(levels):   # neighbouring corners may differ by one level only (one tileset per cell)
    p = np.pad(v, 1, mode="edge")
    nb = np.min([p[1 + dy:p.shape[0] - 1 + dy, 1 + dx:p.shape[1] - 1 + dx]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    v = np.minimum(v, nb + 1)

m = Image.new("RGBA", (cells * tw, cells * th))
for y in range(cells):
    for x in range(cells):
        c = (v[y, x], v[y, x + 1], v[y + 1, x], v[y + 1, x + 1])
        low = min(min(c), levels - 2)
        m.paste(sets[low][tuple(int(k > low) for k in c)], (x * tw, y * th))
m.resize((m.width * a.scale, m.height * a.scale), Image.NEAREST).save(a.out)

pad = 14
sheet = Image.new("RGBA", (16 * (tw + 4) + 4, len(sets) * (th + pad + 4) + 4), (40, 40, 48, 255))
d = ImageDraw.Draw(sheet)
for r, lut in enumerate(sets):
    for i, k in enumerate(sorted(lut)):
        x, y = 4 + i * (tw + 4), 4 + r * (th + pad + 4)
        sheet.paste(lut[k], (x, y))
        d.text((x, y + th + 1), "".join(map(str, k)), fill=(220, 220, 220, 255))
out = Path(a.out)
tiles_png = out.with_name(out.stem + "_tiles.png")
sheet.resize((sheet.width * a.scale, sheet.height * a.scale), Image.NEAREST).save(tiles_png)
print(json.dumps({"written": [str(out), str(tiles_png)], "cells": cells, "terrain_levels": levels, "purpose": "inspection only; random map plus all corner combinations"}))
