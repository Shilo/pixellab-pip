"""recolor_trail.py - turn a swing trail painted in the character's own colours into an effect, or delete it.
Clean-up; writes copies only.

animate_image often paints a swing trail in the character's own colours (a red smear behind a red tabard), which no
colour filter can scrub. This finds the trail - pixels of the chosen hue that are thin strokes (not a solid area like
a tabard) and lie away from the rest of the body - and recolours it by brightness into an effect ramp, or deletes it.

    python recolor_trail.py <dir> <frame>... --out DIR [--hue red] [--to air] [--ref standing.png]
    python recolor_trail.py raw 3 4 5 --hue red --to air --ref hero.png --out trail
    python recolor_trail.py raw 3 4 --from-scrub scrubbed --to air --out trail   # what scrub.py removed IS the slash

--ref (recommended): the trail is every pixel of the hue whose colour is not in the standing sprite's palette;
generators paint trails brighter and purer than the character's own colours.
--to none: delete the trail; where it crosses the body the pixels stay (no hole), and the trail's own thin outline,
often in the hero's colours, goes with it.
--from-scrub DIR: the trail = pixels scrub.py cleared, read from DIR/<frame>_s.png (scrub's --out folder).
Writes DIR/<frame>_t.png and DIR/derivative.json.
"""
import argparse
import colorsys
import glob
import os
import re

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

RAMPS = {   # dark -> bright
    "air": ["#5a7896", "#8fb4d8", "#bcd8f0", "#e8f4ff", "#ffffff"],
    "fire": ["#6e1409", "#b3260e", "#e8561a", "#f8a531", "#ffe08a"],
    "arcane": ["#2d0f4a", "#5a1f86", "#8f45c4", "#c48af0", "#f0d8ff"],
    "holy": ["#4a3410", "#b29352", "#debd77", "#fff2c4", "#ffffff"],
    "shadow": ["#0a0a12", "#1c1a2e", "#34304f", "#57527a", "#8a84b0"],
}
HUES = {"red": (330, 20), "orange": (15, 45), "yellow": (40, 70), "green": (70, 170),
        "cyan": (170, 200), "blue": (200, 255), "purple": (255, 330)}

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("dir")
ap.add_argument("frames", nargs="+")
ap.add_argument("--out", required=True)
ap.add_argument("--hue", default="red", help="a named range, any (needs --ref or --from-scrub), or LO,HI degrees")
ap.add_argument("--to", default="air", choices=list(RAMPS) + ["none"], help="none = delete the trail")
ap.add_argument("--ref", help="the standing sprite: hue pixels not in its palette are the trail")
ap.add_argument("--tol", type=float, default=30)
ap.add_argument("--outside-keys", action="store_true",
                help="trail = hue pixels outside the two key poses' silhouettes (frame 0 and the last frame)")
ap.add_argument("--above", type=int, default=0, help="only rows above this y count (keeps low cloak tails out)")
ap.add_argument("--from-scrub", metavar="DIR", help="scrub.py's --out folder: what it cleared is the trail")
ap.add_argument("--body-gap", type=int, default=4, help="trail pixels must be this far from non-hue body pixels")
ap.add_argument("--thick", type=int, default=5, help="solid areas of the hue at least this thick are kept")
a = ap.parse_args()
if a.hue == "any" and not a.ref and not a.from_scrub:
    ap.error("--hue any needs --ref (the standing sprite) or --from-scrub")
names = _derive.frames(a.dir, a.frames)
paths = [os.path.join(a.dir, f + ".png") for f in names]
inputs = ([a.ref] if a.ref else []) + paths
if a.from_scrub:
    inputs += [os.path.join(a.from_scrub, f + "_s.png") for f in names]
keys = None
if a.outside_keys:
    nums = [int(m.group(1)) for m in (re.match(r"(\d+)\.png$", os.path.basename(q))
                                      for q in glob.glob(os.path.join(a.dir, "*.png"))) if m]
    kp = [os.path.join(a.dir, "0.png"), os.path.join(a.dir, "%d.png" % max(nums))]
    inputs += kp
    k0, k1 = (np.array(Image.open(p).convert("RGBA"))[..., 3] > 0 for p in kp)
    keys = ndimage.binary_dilation(k0 | k1, iterations=a.body_gap)
run = _derive.Run("recolor_trail", "cleanup", a.out, list(dict.fromkeys(inputs)))
lo, hi = tuple(float(v) for v in a.hue.split(",")) if "," in a.hue else HUES.get(a.hue, (0, 360))
refpal = None
if a.ref:
    r = np.array(Image.open(a.ref).convert("RGBA"))
    refpal = np.unique(r[r[..., 3] > 0][:, :3], axis=0).astype(np.int32)
ramp = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in RAMPS.get(a.to, RAMPS["air"])])

for f, path in zip(names, paths):
    x = np.array(Image.open(path).convert("RGBA"))
    op = x[..., 3] > 0
    rgb = x[..., :3].astype(float) / 255
    h, s = np.zeros(op.shape), np.zeros(op.shape)
    for (yy, xx) in zip(*np.nonzero(op)):
        h[yy, xx], s[yy, xx], _ = colorsys.rgb_to_hsv(*rgb[yy, xx])
    deg = h * 360
    if a.hue == "any":
        inhue = op.copy()
    else:
        inhue = op & (s > 0.35) & ((deg >= lo) & (deg <= hi) if lo < hi else ((deg >= lo) | (deg <= hi)))
    solid = ndimage.binary_opening(inhue, structure=np.ones((a.thick, a.thick)))
    solid = ndimage.binary_dilation(solid, iterations=2) & inhue        # keep the whole tabard, not just its core
    body = ndimage.binary_dilation(op & ~inhue, iterations=a.body_gap)  # skin, armour, hair, sword...
    trail = inhue & ~solid & ~body
    if refpal is not None:   # colour test against the original sprite beats the shape test
        px = x[..., :3][inhue].astype(np.int32)
        d = np.min(((px[:, None, :] - refpal[None, :, :]) ** 2).sum(-1), axis=1)
        trail = np.zeros_like(inhue)
        trail[inhue] = d > a.tol ** 2
    if keys is not None:
        trail = inhue & ~keys & ~body
    if a.from_scrub:
        sc = np.array(Image.open(os.path.join(a.from_scrub, f + "_s.png")).convert("RGBA"))
        trail = op & (sc[..., 3] == 0)
    if a.above:
        trail[a.above:] = False
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    if trail.any() and a.to == "none":
        # where the streak crosses the body (an axe head, the torso) deleting it would punch a hole: keep those
        solid_rest = ndimage.binary_opening(op & ~trail, structure=np.ones((2, 2)))   # minus 1 px strands
        gone = trail & ~ndimage.binary_closing(solid_rest, structure=np.ones((5, 5)))
        x[..., 3][gone] = 0
        # the streak's own outline is left as thin strands hugging the gap: drop thin bits that mostly touch it
        rest = op & ~gone
        thin = rest & ~ndimage.binary_opening(rest, structure=np.ones((3, 3)))
        near = ndimage.binary_dilation(gone, structure=np.ones((3, 3)))
        lab, n = ndimage.label(thin, structure=np.ones((3, 3)))
        for i in range(1, n + 1):
            c = lab == i
            if (c & near).sum() * 2 > c.sum():
                x[..., 3][c] = 0
                gone |= c
        trail = gone
    elif trail.any():
        lv = lum[trail]
        if np.percentile(lv, 90) - np.percentile(lv, 10) > 0.15:   # the trail has its own shading: map it
            q = np.clip(((lv - lv.min()) / (lv.max() - lv.min()) * (len(ramp) - 1)).round().astype(int), 0, len(ramp) - 1)
            x[..., :3][trail] = ramp[q]
        else:   # a flat smear: shade by depth - rim in the ramp's mid tone, white core, dithered deep inside
            depth = ndimage.distance_transform_cdt(trail, metric="chessboard")
            q = np.clip(depth, 1, len(ramp) - 1)
            x[..., :3][trail] = ramp[q[trail]]
            yy, xx = np.indices(trail.shape)
            x[..., 3][trail & (depth > 4) & ((yy + xx) % 2 == 0)] = 0
    key = "deleted" if a.to == "none" else "recoloured"
    run.save(Image.fromarray(x), f + "_t.png", **{key: int(trail.sum())})
    print(f, key, int(trail.sum()), "px")
run.done(to=a.to)
