"""blade_trail.py - paint a weapon trail through stepped key poses, plus an optional flash-step afterimage.
New pixels (a locally painted trail); writes copies only. Prefer a vfx_workbench trail when it can do the job.

For moves the generator's in-betweens get wrong (a carried prop flips sides, a blade appears twice): step through
checked key poses and let a trail show the swing. One path runs through the blade tips; each frame's trail ends at
its head position on that path, thick at the leading edge, dark outline, steel ramp.

    python blade_trail.py --frames idle.png draw.png ext.png ext.png --path "70,91 124,93 185,75" \
        --spans "x,x,0:1,0.55:1" --thick "0,0,8,5" --dither "0,0,0,1" --out DIR \
        [--ghost idle.png --ghost-on "0,1,0,0"] [--behind] [--ramp "#8a9ab8,#d8e0ec,#ffffff"] [--outline "#282c3c"]

--spans: per frame "t0:t1" along the path (0 = first point, 1 = last) or "x" for no trail.
--ghost: a pose drawn 50% dithered behind the frame (the stance left behind in a flash-step).
--behind: the trail goes under the body (speed lines behind a figure).
Writes DIR/0.png ... in order and DIR/derivative.json.
"""
import argparse
import sys

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402


def catmull(points):
    pts = np.array(points, float)

    def at(t):
        n = len(pts) - 1
        s = min(max(t, 0.0) * n, n - 1e-6)
        i, u = int(s), s - int(s)
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n)]
        return 0.5 * (2 * p1 + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)
    return at


def smear(shape, path, t0, t1, thick):
    """Intensity 0..1 of a tapered trail from t0 (tail, thin) to t1 (head, thick, sharp tip)."""
    h, w = shape
    m = np.zeros((h, w))
    for t in np.linspace(t0, t1, 1500):
        k = (t - t0) / max(t1 - t0, 1e-6)
        width = thick * k ** 1.2 * (1 if k < 0.93 else (1 - k) / 0.07)
        x, y = path(t)
        for d in np.arange(-width / 2, width / 2 + 0.01, 0.5):
            xi, yi = int(round(x)), int(round(y + d))
            if 0 <= xi < w and 0 <= yi < h:
                m[yi, xi] = max(m[yi, xi], 1 - abs(d) / (width / 2 + 1e-3))
    return m


def paint(m, ramp, outline, dither=False):
    h, w = m.shape
    on = m > 0
    out = np.zeros((h, w, 4), np.uint8)
    lvl = np.clip((m * len(ramp)).astype(int), 0, len(ramp) - 1)
    for i, c in enumerate(ramp):
        out[on & (lvl == i)] = (*c, 255)
    out[ndimage.binary_dilation(on, np.ones((3, 3), bool)) & ~on] = (*outline, 255)
    if dither:
        yy, xx = np.mgrid[0:h, 0:w]
        out[(yy + xx) % 2 == 1] = 0
    return Image.fromarray(out, "RGBA")


def ghost(img, tint=(70, 90, 130), amount=0.5):
    g = np.array(img.convert("RGBA")).copy()
    yy, xx = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    g[(yy + xx) % 2 == 1] = 0
    g[..., :3] = (g[..., :3] * (1 - amount) + np.array(tint) * amount).astype(np.uint8)
    return Image.fromarray(g, "RGBA")


def hexes(s):
    return [tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) for c in s.split(",")]


def _span(s):
    return None if s.strip() in ("x", "-", "") else tuple(float(v) for v in s.split(":"))


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--frames", nargs="+", required=True)
ap.add_argument("--path", required=True, help='"x,y x,y ..." through the blade tips, tail to head')
ap.add_argument("--spans", required=True)
ap.add_argument("--thick")
ap.add_argument("--dither")
ap.add_argument("--ghost")
ap.add_argument("--ghost-on")
ap.add_argument("--ramp", help='dark to light, e.g. "#8a9ab8,#d8e0ec,#ffffff"')
ap.add_argument("--outline", default="#282c3c")
ap.add_argument("--behind", action="store_true")
ap.add_argument("--out", required=True)
a = ap.parse_args()
n = len(a.frames)
spans = [_span(s) for s in a.spans.split(",")]
thick = [float(v) for v in (a.thick or ",".join(["8"] * n)).split(",")]
dither = [int(v) for v in (a.dither or ",".join(["0"] * n)).split(",")]
gon = [int(v) for v in a.ghost_on.split(",")] if a.ghost_on else None
if not (len(spans) == len(thick) == len(dither) == n) or (gon and len(gon) != n):
    sys.exit("--spans, --thick, --dither and --ghost-on need one value per frame (%d)" % n)
run = _derive.Run("blade_trail", "new_pixels", a.out, a.frames + ([a.ghost] if a.ghost else []))
path = catmull([tuple(float(v) for v in p.split(",")) for p in a.path.split()])
ramp = hexes(a.ramp) if a.ramp else [(138, 154, 184), (216, 224, 236), (255, 255, 255)]
outline = hexes(a.outline)[0]
ghost_img = Image.open(a.ghost) if a.ghost else None
for i, f in enumerate(a.frames):
    body = Image.open(f).convert("RGBA")
    c = Image.new("RGBA", body.size)
    if ghost_img is not None and gon and gon[i]:
        c.alpha_composite(ghost(ghost_img))
    trail = None
    if spans[i] is not None and thick[i] > 0:
        trail = paint(smear(body.size[::-1], path, *spans[i], thick[i]), ramp, outline, bool(dither[i]))
    for part in ((trail, body) if a.behind else (body, trail)):
        if part is not None:
            c.alpha_composite(part)
    run.save(c, "%d.png" % i, body=f, trail=trail is not None, ghost=bool(ghost_img is not None and gon and gon[i]))
run.done(behind=a.behind)
print("%d frames -> %s" % (n, a.out))
