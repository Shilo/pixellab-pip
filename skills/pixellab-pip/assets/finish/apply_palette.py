"""apply_palette.py - snap every opaque pixel to the nearest colour of a fixed palette (no dithering). Clean-up;
writes copies only.

<palette> = a palette.png of swatches, a .hex/.txt file (one #rrggbb per line), a JSON file with
{"colours": {"palette": [...]}}, comma-separated hex, or "auto" (the images' own N main colours, with --colors N).
--colors N with a palette file keeps its first N colours. Transparent pixels stay transparent.

    python apply_palette.py "#1a1c2c,#5d275d,#b13e53" frames/*.png --out DIR
    python apply_palette.py auto frames/*.png --colors 16 --out DIR

Writes DIR/<same names> and DIR/derivative.json.
"""
import argparse
import json
import os

import _derive

_derive.require_numpy()
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("palette")
ap.add_argument("images", nargs="+")
ap.add_argument("--out", required=True)
ap.add_argument("--colors", type=int, default=0)
a = ap.parse_args()
files = _derive.expand(a.images)
pal_file = a.palette != "auto" and os.path.isfile(a.palette)
run = _derive.Run("apply_palette", "cleanup", a.out, ([a.palette] if pal_file else []) + files)


def hexes(h):
    return [tuple(int(x.strip().lstrip("#")[j:j + 2], 16) for j in (0, 2, 4)) for x in h if x.strip()]


n = a.colors
if a.palette == "auto":
    px = np.concatenate([np.array(Image.open(f).convert("RGBA")).reshape(-1, 4) for f in files])
    px = px[px[:, 3] > 0][:, :3]
    q = Image.fromarray(px.reshape(1, -1, 3).astype(np.uint8)).quantize(colors=n or 16, method=Image.MAXCOVERAGE, dither=0)   # median cut drops small accents (a belt, straps)
    pal = np.array(q.getpalette()[:3 * (n or 16)]).reshape(-1, 3)
elif a.palette.endswith(".json"):
    pal = np.array(hexes(json.load(open(a.palette, encoding="utf-8"))["colours"]["palette"]))
elif a.palette.endswith(".png"):
    pal = np.unique(np.array(Image.open(a.palette).convert("RGB")).reshape(-1, 3), axis=0)
elif pal_file:
    pal = np.array(hexes(open(a.palette, encoding="utf-8").read().split()))
else:
    pal = np.array(hexes(a.palette.split(",")))
if n and a.palette != "auto":
    pal = pal[:n]
pal = pal.astype(np.int32)
for f in files:
    x = np.array(Image.open(f).convert("RGBA"))
    m = x[..., 3] > 0
    px = x[m][:, :3].astype(np.int32)
    idx = ((px[:, None, :] - pal[None, :, :]) ** 2).sum(-1).argmin(1)
    x[..., :3][m] = pal[idx]
    used = len(np.unique(pal[idx], axis=0))
    run.save(Image.fromarray(x), os.path.basename(f), colours=used)
    print(os.path.basename(f), "%d colours" % used)
run.done(palette=["#%02x%02x%02x" % tuple(c) for c in pal])
