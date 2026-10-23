"""scrub.py - clear the flashes and streaks a generator paints into frames. Clean-up; writes copies only.

Raw clip mode: <dir> holds an animate_image clip (0.png .. N.png). In each named frame, pixels whose colour is far
from every colour of the first and last frame (the key poses) are cleared, then detached specks under 12 px.
    python scrub.py <dir> <frame>... --out DIR [--tol 40] [--keep-main] [--clear-right X | --clear-left X]
Single pose mode: one key pose with a beam or muzzle flash painted in; no colour test, only what you name goes.
    python scrub.py <pose.png> [--box x0,y0,x1,y1] [--clear-right X] [--keep-main] --out DIR

--tol: colour distance to the key poses' palette; lower (20-25) catches trails in the character's own hues.
--clear-right X / --clear-left X: also clear every column right (left) of X - for shots, where the generator paints
its own muzzle flash in front of the barrel partly in sprite colours. X = the barrel tip in the aim pose.
--keep-main: keep only the biggest piece (pose mode) or pieces near it (clip mode).
Writes DIR/<frame>_s.png (pose mode: DIR/<pose>_s.png) and DIR/derivative.json.
"""
import argparse
import glob
import os
import re

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

SPECK = 12   # detached clusters smaller than this many pixels are cleared too

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("src", help="a raw clip folder, or one key pose .png")
ap.add_argument("frames", nargs="*", help="frame names in the folder, e.g. 3 4 5 or 0*")
ap.add_argument("--out", required=True)
ap.add_argument("--tol", type=float, default=40)
ap.add_argument("--clear-right", type=int)
ap.add_argument("--clear-left", type=int)
ap.add_argument("--box", help="x0,y0,x1,y1 (pose mode)")
ap.add_argument("--keep-main", action="store_true")
a = ap.parse_args()


def sides(al):
    if a.clear_right is not None:
        al[:, a.clear_right + 1:] = 0
    if a.clear_left is not None:
        al[:, :a.clear_left] = 0


if a.src.lower().endswith(".png"):   # one key pose: clear only what was named
    run = _derive.Run("scrub", "cleanup", a.out, [a.src])
    x = np.array(Image.open(a.src).convert("RGBA"))
    al = x[..., 3]
    before = int((al > 0).sum())
    if a.box:
        x0, y0, x1, y1 = (int(v) for v in a.box.split(","))
        al[y0:y1 + 1, x0:x1 + 1] = 0
    sides(al)
    if a.keep_main:
        lab, n = ndimage.label(al > 0, structure=np.ones((3, 3)))
        if n:
            sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
            al[(lab > 0) & (lab != int(np.argmax(sizes)) + 1)] = 0
    name = os.path.basename(a.src)[:-4] + "_s.png"
    cleared = before - int((al > 0).sum())
    run.save(Image.fromarray(x), name, cleared=cleared)
    print(name, "cleared", cleared)
    run.done()
    raise SystemExit(0)

if not a.frames:
    ap.error("name the frames to scrub, e.g. 3 4 5 or 0*")
nums = [int(m.group(1)) for m in (re.match(r"(\d+)\.png$", os.path.basename(q))
                                  for q in glob.glob(os.path.join(a.src, "*.png"))) if m]
if not nums:
    ap.error("no numbered frames (0.png ...) in %s" % a.src)
keys = [os.path.join(a.src, "%d.png" % k) for k in (0, max(nums))]   # the two key poses: first and last frame
names = _derive.frames(a.src, a.frames)
paths = [os.path.join(a.src, f + ".png") for f in names]
run = _derive.Run("scrub", "cleanup", a.out, list(dict.fromkeys(keys + paths)))
pal = set()
for k in keys:
    x = np.array(Image.open(k).convert("RGBA"))
    pal |= {tuple(p[:3]) for p in x.reshape(-1, 4) if p[3] > 0}
P = np.array(sorted(pal), dtype=np.int32)
for f, path in zip(names, paths):
    x = np.array(Image.open(path).convert("RGBA"))
    m = x[..., 3] > 0
    px = x[m][:, :3].astype(np.int32)
    dist = np.min(((px[:, None, :] - P[None, :, :]) ** 2).sum(-1), axis=1)
    keep = dist < a.tol ** 2
    al = x[..., 3].copy()
    al[m] = np.where(keep, al[m], 0)
    sides(al)
    lab, n = ndimage.label(al > 0, structure=np.ones((3, 3)))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    al[np.isin(lab, np.nonzero(sizes < SPECK)[0] + 1)] = 0
    if a.keep_main and n:
        near = ndimage.binary_dilation(lab == int(np.argmax(sizes)) + 1, iterations=6)
        for c in range(1, n + 1):
            if not (near & (lab == c)).any():
                al[lab == c] = 0
    x[..., 3] = al
    cleared = int(m.sum()) - int((al > 0).sum())
    run.save(Image.fromarray(x), f + "_s.png", cleared=cleared)
    print(f, "cleared", cleared, "of", int(m.sum()))
run.done()
