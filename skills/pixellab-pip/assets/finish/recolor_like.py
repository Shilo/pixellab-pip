"""recolor_like.py - recolour frames drawn in an old still's colours into a new still's. Clean-up; writes copies only.

Both stills show the same pose. Each source colour takes the hue and saturation of what the new still has at the
same spot and the lightness of the colour at its brightness rank, so the result keeps the source's contrast. Shades
the still does not use take their nearest mapped colour; colours the stills do not share keep the rank map.
--keep-thin REDRAWN_DIR: instead of the recoloured frame, write the same-named frame from REDRAWN_DIR (a redraw)
with the recoloured frame's thin parts pasted over it (blades, staffs, fingers: what a 5 px opening removes from the
silhouette), dropping redrawn pixels just around them that the source does not have.
Also reports frames that repeat an earlier one (draw those once).

    python recolor_like.py old/still.png new/still.png old/attack_*.png --out DIR [--keep-thin redrawn]

Writes DIR/<same names> and DIR/derivative.json.
"""
import argparse
import os

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

from recolor_groups import oklab, rgb_of  # noqa: E402

ALPHA, MAP_MIN, MAP_DIST, THIN, BAND = 128, 6, 90, 2, 3


def _lum(x):
    return x @ [0.299, 0.587, 0.114]


def still_map(src, new):
    """{source colour: median new colour under it}, stills aligned feet to feet and centre to centre."""
    a, b = np.array(src.convert("RGBA")), np.array(new.convert("RGBA"))
    ba, bb = src.getbbox(), new.getbbox()
    if not ba or not bb:
        return {}
    dx, dy = round((bb[0] + bb[2] - ba[0] - ba[2]) / 2), bb[3] - ba[3]
    ys, xs = np.nonzero(a[..., 3] >= ALPHA)
    ty, tx = ys + dy, xs + dx
    ok = (ty >= 0) & (ty < b.shape[0]) & (tx >= 0) & (tx < b.shape[1])
    ys, xs, ty, tx = ys[ok], xs[ok], ty[ok], tx[ok]
    ok = b[ty, tx, 3] >= ALPHA
    s, d = a[ys[ok], xs[ok], :3].astype(int), b[ty[ok], tx[ok], :3].astype(int)
    key = (s[:, 0] << 16) | (s[:, 1] << 8) | s[:, 2]
    return {((k >> 16) & 255, (k >> 8) & 255, k & 255): np.median(d[key == k], axis=0)
            for k in np.unique(key) if (key == k).sum() >= MAP_MIN}


def recolour(img, src, new):
    def ranked(im):
        x = np.array(im.convert("RGBA")).reshape(-1, 4)
        x = x[x[:, 3] >= ALPHA][:, :3].astype(float)
        return x[np.argsort(_lum(x))]
    old, nw = ranked(src), ranked(new)
    x = np.array(img.convert("RGBA")).astype(float)
    on = x[..., 3] >= ALPHA
    if not on.any() or not len(old) or not len(nw):
        return img.convert("RGBA")
    q = np.searchsorted(_lum(old), _lum(x[on][:, :3])) / len(old)
    x[on, :3] = nw[np.clip((q * len(nw)).astype(int), 0, len(nw) - 1)]
    by_rank = x.copy()
    cmap = still_map(src, new)
    if cmap:
        keys, vals = np.array(list(cmap), float), np.array(list(cmap.values()))
        orig = np.array(img.convert("RGBA"))[..., :3].astype(float)
        cols, inv = np.unique(orig[on], axis=0, return_inverse=True)
        d = np.abs(cols[:, None, :] - keys[None]).sum(-1)
        near = d.argmin(1)
        use = d[np.arange(len(cols)), near] <= MAP_DIST
        px, sel = x[on], use[inv.ravel()]
        px[sel, :3] = vals[near[inv.ravel()][sel]]
        x[on] = px
        lab = oklab(np.clip(x[..., :3], 0, 255))          # mapped hue and chroma, rank lightness
        lab[..., 0] = oklab(np.clip(by_rank[..., :3], 0, 255))[..., 0]
        x[on, :3] = rgb_of(lab)[on]
    return Image.fromarray(x.astype(np.uint8), "RGBA")


def keep_thin(drawn, guide, search=3):
    d, g = np.array(drawn.convert("RGBA")), np.array(guide.convert("RGBA"))
    if d.shape != g.shape:
        return drawn
    da, ga = d[..., 3] > 0, g[..., 3] > 0
    best = (-1.0, 0, 0)
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            s = np.roll(np.roll(ga, dy, 0), dx, 1)
            iou = (s & da).sum() / max(1, (s | da).sum())
            if iou > best[0]:
                best = (iou, dx, dy)
    g = np.roll(np.roll(g, best[2], 0), best[1], 1)
    ga = g[..., 3] > 0
    sq = np.ones((3, 3), bool)
    thin = ga & ~ndimage.binary_opening(ga, structure=np.ones((2 * THIN + 1,) * 2, bool))
    thin = ndimage.binary_dilation(thin, structure=sq) & ga
    band = ndimage.binary_dilation(thin, structure=np.ones((2 * BAND + 1,) * 2, bool))
    d[band & ~ga & ~ndimage.binary_dilation(ga & ~thin, structure=sq)] = 0
    d[thin] = g[thin]
    return Image.fromarray(d, "RGBA")


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("source_still")
ap.add_argument("new_still")
ap.add_argument("frames", nargs="+")
ap.add_argument("--out", required=True)
ap.add_argument("--keep-thin", metavar="REDRAWN_DIR")
a = ap.parse_args()
files = _derive.expand(a.frames)
redrawn = [os.path.join(a.keep_thin, os.path.basename(f)) for f in files] if a.keep_thin else []
run = _derive.Run("recolor_like", "cleanup", a.out, [a.source_still, a.new_still] + files + redrawn)
src, new = Image.open(a.source_still), Image.open(a.new_still)
seen: dict = {}
for f in files:
    x = np.asarray(Image.open(f).convert("RGBA"), dtype=np.int16)
    rep = next((p for p, b in seen.items() if b.shape == x.shape and np.abs(x - b).mean() < 1.0), None)
    if rep:
        print("repeat: %s = %s (draw once)" % (os.path.basename(f), os.path.basename(rep)))
    else:
        seen[f] = x
    rec = recolour(Image.open(f), src, new)
    name = os.path.basename(f)
    if a.keep_thin:
        rec = keep_thin(Image.open(os.path.join(a.keep_thin, name)), rec)
    change = {"repeat_of": os.path.basename(rep)} if rep else {}
    if a.keep_thin:
        change["thin_parts_on_redraw"] = True
    run.save(rec, name, **change)
    print("wrote", os.path.join(a.out, name))
run.done()
