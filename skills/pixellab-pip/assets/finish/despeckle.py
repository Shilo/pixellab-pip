"""despeckle.py - clear lone pixels from animation frames. Clean-up; writes copies only.

animate_image in-betweens leave single pixels that match none of their neighbours: a white dot on a black coat, a
pink dot on a hair edge. Each pixel unlike all 8 of its neighbours takes their median colour; an opaque pixel with
no opaque neighbour (a stray) goes transparent. Two or more alike pixels together (a highlight, an eye glint) stay.

    python despeckle.py frames/*.png --out DIR [--ref still.png] [--tol 90]

--ref: the clean still the frames were made from. A one-pixel detail is the same shape as a speck (a 1 px eye
differs from the skin around it as much as noise does), so lone pixels whose colour is one of the still's own
lone-pixel colours are kept as detail.
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
ap.add_argument("--ref")
ap.add_argument("--tol", type=int, default=90)
a = ap.parse_args()
files = _derive.expand(a.frames)
run = _derive.Run("despeckle", "cleanup", a.out, files + ([a.ref] if a.ref else []))
OFF = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]


def lone(im):
    """(speck, stray, neighbours, opaque neighbours) masks for one RGBA frame."""
    h, w = im.shape[:2]
    pad = np.zeros((h + 2, w + 2, 4), np.int32)
    pad[1:-1, 1:-1] = im
    op = im[..., 3] > 0
    nb = np.stack([pad[1 + dy:h + 1 + dy, 1 + dx:w + 1 + dx] for dy, dx in OFF])     # 8 x h x w x 4
    nb_op = nb[..., 3] > 0
    alike = nb_op & (np.abs(nb[..., :3] - im[None, ..., :3].astype(np.int32)).sum(-1) < a.tol)
    stray = op & (nb_op.sum(0) == 0)   # (one neighbour is a line end - a whip tip, a hair strand - and stays)
    return op & ~stray & (alike.sum(0) == 0), stray, nb, nb_op


details = np.zeros((0, 3), np.int32)
if a.ref:
    ref = np.array(Image.open(a.ref).convert("RGBA"))
    details = ref[lone(ref)[0]][:, :3].astype(np.int32)   # the still's own one-pixel details (eyes, runes)
for f in files:
    im = np.array(Image.open(f).convert("RGBA"))
    speck, stray, nb, nb_op = lone(im)
    kept = 0
    if len(details) and speck.any():
        known = (np.abs(im[speck][:, None, :3].astype(np.int32) - details[None]).sum(-1) < a.tol).any(1)
        speck[speck] = ~known
        kept = int(known.sum())
    out = im.copy()
    if speck.any():
        cols = np.where(nb_op[..., None], nb[..., :3], np.nan)                         # median of the opaque ones
        out[speck, :3] = np.round(np.nanmedian(cols[:, speck], axis=0)).astype(np.uint8)
    out[stray, 3] = 0
    name = os.path.basename(f)
    run.save(Image.fromarray(out), name, specks=int(speck.sum()), strays=int(stray.sum()), kept_as_detail=kept)
    print("%s: %d specks, %d strays, %d kept as detail" % (name, int(speck.sum()), int(stray.sum()), kept))
run.done()
