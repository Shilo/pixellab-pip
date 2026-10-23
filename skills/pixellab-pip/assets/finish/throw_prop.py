"""throw_prop.py - fly a thrown weapon (spear, axe, dagger) out of the release pose onto the frames after it.
New pixels (the prop pasted where it never was); writes copies only.

The release pose shows the weapon just leaving the hand, apart from the body. This lifts that piece (the biggest
group of pixels that does not touch the body) and pastes it onto each following frame, one --step further each
time; whatever leaves the canvas is cut. The --onto frames keep every pixel they have: the weapon goes on empty
space only. Ground-snap first.

    python throw_prop.py release.png --onto follow.png follow.png --step 40,-17 [--turn 1] --out DIR

--step: pixels per frame (x right, y down) along the throw. --turn: quarter turns per frame, clockwise (a tumbling
axe: 1). Writes DIR/0.png ... (one per --onto frame, in order) and DIR/derivative.json.
"""
import argparse
import sys

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("release")
ap.add_argument("--onto", nargs="+", required=True)
ap.add_argument("--step", required=True, help="dx,dy per frame")
ap.add_argument("--turn", type=int, default=0, help="quarter turns per frame, clockwise")
ap.add_argument("--out", required=True)
a = ap.parse_args()
dx, dy = (int(v) for v in a.step.split(","))
rel = np.array(Image.open(a.release).convert("RGBA"))
lab, n = ndimage.label(rel[..., 3] > 0, np.ones((3, 3)))
if n < 2:
    sys.exit("no weapon apart from the body in %s - the release pose must show it already out of the hand" % a.release)
run = _derive.Run("throw_prop", "new_pixels", a.out, [a.release] + a.onto)
sizes = ndimage.sum(np.ones(lab.shape), lab, range(1, n + 1))
sizes[int(np.argmax(sizes))] = 0   # the body
prop = lab == int(np.argmax(sizes)) + 1
ys, xs = np.nonzero(prop)
piece = np.where(prop[..., None], rel, 0)[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
for k, f in enumerate(a.onto, 1):
    im = np.array(Image.open(f).convert("RGBA"))
    h, w = im.shape[:2]
    p = np.rot90(piece, -a.turn * k) if a.turn else piece   # turned about its centre
    py, px = np.nonzero(p[..., 3] > 0)
    ny = (py + round(cy + dy * k - (p.shape[0] - 1) / 2)).astype(int)
    nx = (px + round(cx + dx * k - (p.shape[1] - 1) / 2)).astype(int)
    keep = (ny >= 0) & (ny < h) & (nx >= 0) & (nx < w)
    ny, nx, py, px = ny[keep], nx[keep], py[keep], px[keep]
    free = im[ny, nx, 3] == 0   # never paint over the character
    im[ny[free], nx[free]] = p[py[free], px[free]]
    run.save(Image.fromarray(im, "RGBA"), "%d.png" % (k - 1), onto=f, prop_px=int(free.sum()))
    print("%d.png: weapon %d px on canvas" % (k - 1, int(free.sum())))
run.done(step=[dx, dy], turn=a.turn)
