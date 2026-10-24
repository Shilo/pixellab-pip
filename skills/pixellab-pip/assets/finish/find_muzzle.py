"""find_muzzle.py - find the shot frame and the muzzle in a generated shooting animation, for dir8_finish's spec.
Read-only: prints a suggestion, writes nothing.

animate_image / animate_character paint a flash of their own on the shot (white orb, yellow star, beam lines, cyan
sparks). It is usually the wrong colour, but it sits right at the muzzle. This lists the bright blobs on every frame
and guesses:
  shot frame = the frame with the biggest bright blob (>= --min px),
  muzzle     = where that blob meets the gun (its pixels closest to the character's light pixels).

    python find_muzzle.py <frames_dir> [--min 60]

<frames_dir> holds 0.png .. N.png (fetch.py's frame names). Check the guess on the frame before using it: it is off
when the flash covers the body or overlaps the gun; then read the muzzle off the frame by eye.
"""
import argparse
import os

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("frames_dir")
ap.add_argument("--min", type=int, default=60)
a = ap.parse_args()
n = 0
while os.path.exists(os.path.join(a.frames_dir, "%d.png" % n)):
    n += 1
if n == 0:
    raise SystemExit("no 0.png .. N.png frames in " + a.frames_dir)


def bright_mask(px):
    rgb, opaque = px[..., :3], px[..., 3] > 0
    white = rgb.min(-1) > 200
    yellow = (rgb[..., 0] > 200) & (rgb[..., 1] > 170) & (rgb[..., 2] < 140)
    cyan = (rgb[..., 1] > 200) & (rgb[..., 2] > 200) & (rgb[..., 0] < 160)
    return opaque & (white | yellow | cyan)


best = None   # (size, frame, labels, label id, pixels)
for i in range(n):
    with Image.open(os.path.join(a.frames_dir, "%d.png" % i)) as im:
        px = np.array(im.convert("RGBA")).astype(int)
    lab, k = ndimage.label(bright_mask(px), structure=np.ones((3, 3)))
    blobs = []
    for j in range(1, k + 1):
        ys, xs = np.nonzero(lab == j)
        if len(xs) >= 6:
            blobs.append((len(xs), j, int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
    blobs.sort(reverse=True)
    print(i, [(b[0], "x%d-%d" % (b[2], b[3]), "y%d-%d" % (b[4], b[5])) for b in blobs[:3]])
    if blobs and blobs[0][0] >= a.min and (best is None or blobs[0][0] > best[0]):
        best = (blobs[0][0], i, lab, blobs[0][1], px)

if best is None:
    print("no flash >= %d px: pick the shot frame by eye (the frame where the arm is fully extended)" % a.min)
    raise SystemExit(0)
size, shot, lab, j, px = best
flash = lab == j
body = (px[..., 3] > 0) & ~ndimage.binary_dilation(flash, iterations=2)
blab, bn = ndimage.label(body, structure=np.ones((3, 3)))   # the character = the biggest piece, not stray sparks
if bn > 1:
    body = blab == (int(np.argmax(ndimage.sum(np.ones_like(blab), blab, range(1, bn + 1)))) + 1)
light = body & (px[..., :3].min(-1) > 120)                  # light pixels: the gun (white / metal) if it has any
target = light if light.sum() >= 4 else body
dist = ndimage.distance_transform_edt(~target)              # distance of every pixel to the nearest gun pixel
fy, fx = np.nonzero(flash)
near = dist[fy, fx] <= dist[fy, fx].min() + 1.0             # the flash pixels touching the gun
mx, my = int(np.median(fx[near])), int(np.median(fy[near]))
print("\nshot frame %d (flash %d px), muzzle ~(%d, %d)" % (shot, size, mx, my))
print('spec: {"shot": %d, "muzzle": [%d, %d], "angle": <deg, + = down>, "clear": {"%d": [[%d, %d, %d, %d]]}}'
      % (shot, mx, my, shot, int(fx.min()), int(fy.min()), int(fx.max()) + 1, int(fy.max()) + 1))
print('if the flash covers the body, ask before using "replace": {"%d": %d} instead of a clear box'
      % (shot, max(0, shot - 1)))
