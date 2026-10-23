"""despeckle.py - clear lone pixels from animation frames. Clean-up; writes copies only.

animate_image in-betweens leave single pixels that match none of their neighbours: a white dot on a black coat, a
pink dot on a hair edge. Each pixel unlike all 8 of its neighbours takes their median colour; an opaque pixel with
no opaque neighbour (a stray) goes transparent. Two or more alike pixels together (a highlight, an eye glint) stay.

    python despeckle.py frames/*.png --out DIR [--tol 90]

--tol: colour distance (sum of |dR|+|dG|+|dB|) under which a neighbour counts as alike.
Writes DIR/<same names> and DIR/derivative.json.
"""
import argparse
import os

import _derive

_derive.require_numpy()
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("frames", nargs="+")
ap.add_argument("--out", required=True)
ap.add_argument("--tol", type=int, default=90)
a = ap.parse_args()
files = _derive.expand(a.frames)
run = _derive.Run("despeckle", "cleanup", a.out, files)
OFF = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]
for f in files:
    im = np.array(Image.open(f).convert("RGBA"))
    h, w = im.shape[:2]
    pad = np.zeros((h + 2, w + 2, 4), np.int32)
    pad[1:-1, 1:-1] = im
    op = im[..., 3] > 0
    nb = np.stack([pad[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx] for dy, dx in OFF])     # 8 x h x w x 4
    nb_op = nb[..., 3] > 0
    alike = nb_op & (np.abs(nb[..., :3] - im[None, ..., :3].astype(np.int32)).sum(-1) < a.tol)
    stray = op & (nb_op.sum(0) == 0)   # (one neighbour is a line end - a whip tip, a hair strand - and stays)
    speck = op & ~stray & (alike.sum(0) == 0)
    out = im.copy()
    if speck.any():
        cols = np.where(nb_op[..., None], nb[..., :3], np.nan)                         # median of the opaque ones
        out[speck, :3] = np.round(np.nanmedian(cols[:, speck], axis=0)).astype(np.uint8)
    out[stray, 3] = 0
    name = os.path.basename(f)
    run.save(Image.fromarray(out), name, specks=int(speck.sum()), strays=int(stray.sum()))
    print("%s: %d specks, %d strays" % (name, int(speck.sum()), int(stray.sum())))
run.done()
