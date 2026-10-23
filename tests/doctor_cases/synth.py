"""Synthetic pixel art for the /pga-fix tests: one small figure, a smooth walk, and defect injectors.
Canvas 48x56, figure 32x48 at (8, 6): feet on row 53, head top on row 8, a 1 px staff at x = 33."""
import os

import numpy as np
from PIL import Image

OUT = (30, 25, 40)
BLUE, SHADE = (60, 90, 170), (40, 60, 120)
SKIN, HAIR = (225, 170, 130), (90, 60, 30)
BOOT, STAFF = (70, 50, 35), (150, 110, 60)
W, H = 48, 56


def _box(a, x0, y0, x1, y1, rgb):
    a[y0:y1, x0:x1, :3] = rgb
    a[y0:y1, x0:x1, 3] = 255


def figure(scale: int = 1) -> np.ndarray:
    a = np.zeros((H, W, 4), np.uint8)
    ox, oy = 8, 6
    _box(a, ox + 12, oy + 2, ox + 20, oy + 6, HAIR)
    _box(a, ox + 12, oy + 6, ox + 20, oy + 14, SKIN)
    a[oy + 9, ox + 14, :3] = OUT
    a[oy + 9, ox + 17, :3] = OUT
    _box(a, ox + 10, oy + 14, ox + 22, oy + 34, BLUE)
    _box(a, ox + 17, oy + 14, ox + 22, oy + 34, SHADE)
    _box(a, ox + 10, oy + 34, ox + 16, oy + 43, SHADE)       # legs 6 px wide: limbs aren't "thin" like a staff
    _box(a, ox + 17, oy + 34, ox + 23, oy + 43, SHADE)
    _box(a, ox + 10, oy + 43, ox + 16, oy + 48, BOOT)
    _box(a, ox + 17, oy + 43, ox + 23, oy + 48, BOOT)
    _box(a, ox + 22, oy + 22, ox + 25, oy + 27, SKIN)          # hand (3 x 5: thin, part of the staff's thin detail)
    _box(a, ox + 25, oy + 4, ox + 26, oy + 48, STAFF)         # 1 px staff
    return upscale(a, scale) if scale > 1 else a


def walk(n: int = 8, scale: int = 1) -> list:
    dx = [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0]
    return [shift(figure(scale), dx[i % len(dx)] * scale, 0) for i in range(n)]


def shift(f, dx, dy):
    """Moved by (dx, dy); what leaves the canvas is gone (no wrap-around)."""
    g = np.zeros_like(f)
    h, w = f.shape[:2]
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    g[yd, xd] = f[ys, xs]
    return g


def upscale(f, k):
    return np.repeat(np.repeat(f, k, 0), k, 1)


def bright(f, k):
    g = f.copy()
    on = g[..., 3] > 0
    g[on, :3] = np.clip(g[on, :3].astype(float) * k, 0, 255).astype(np.uint8)
    return g


def speck(f, xy, rgb=OUT, size=1):
    g = f.copy()
    x, y = xy
    _box(g, x, y, x + size, y + size, rgb)
    return g


def flash(f, box, rgb=(255, 240, 120)):
    g = f.copy()
    _box(g, *box, rgb)
    return g


def drop_staff(f):
    g = f.copy()
    g[(g[..., :3] == STAFF).all(-1)] = 0
    return g


def cut_staff(f):
    g = f.copy()
    st = (g[..., :3] == STAFF).all(-1)
    st[26:36] = False                                         # keep only the stub held at the hand (rows 26-35)
    g[st] = 0
    return g


def blur_edges(f):
    """Half-transparent, in-between colours around the silhouette (anti-aliasing)."""
    from scipy import ndimage
    g = f.copy()
    on = g[..., 3] > 0
    ring = ndimage.binary_dilation(on) & ~on
    g[ring, :3] = BLUE
    g[ring, 3] = 110
    inner = on & ~ndimage.binary_erosion(on)
    g[inner, :3] = (g[inner, :3].astype(int) * 3 // 4 + 40).astype(np.uint8)
    return g


def cut_left(f, n):
    """The figure pushed n px off the left edge."""
    return shift(f, -(8 + n), 0)


def solid_bg(f, rgb):
    g = f.copy()
    off = g[..., 3] == 0
    g[off, :3] = rgb
    g[..., 3] = 255
    return g


def png(a, path):
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    Image.fromarray(a, "RGBA").save(path)
    return str(path)


def save(frames, folder, stem):
    os.makedirs(folder, exist_ok=True)
    out = []
    for i, f in enumerate(frames, 1):
        p = os.path.join(folder, '%s_%d.png' % (stem, i))
        Image.fromarray(f, 'RGBA').save(p)
        out.append(p)
    return out


def specks_many(f, n=120):
    """n single-px specks in the empty left part of the canvas (far from the body), 2 px apart."""
    g = f.copy()
    for k in range(n):
        x, y = 1 + (k % 7) * 2, (k // 7) * 2 + 1
        g[y, x, :3], g[y, x, 3] = OUT, 255
    return g


def pinholes(f, n=45):
    """n enclosed 1 px transparent holes in the body (a grid inside the torso)."""
    g = f.copy()
    on = g[..., 3] > 0
    ys, xs = np.nonzero(on)
    cells = sorted({(y, x) for y, x in zip(ys, xs) if y % 2 == 0 and x % 2 == 0 and on[y - 1:y + 2, x - 1:x + 2].all()})[:n]
    for y, x in cells:
        g[y, x, 3] = 0
    return g


def noisy(f, seed=1):
    """Every body pixel nudged by a few levels: many near-duplicate colours (a blurred or dithered redraw)."""
    g = f.copy()
    on = g[..., 3] > 0
    r = np.random.default_rng(seed).integers(-6, 7, (on.sum(), 3))
    g[on, :3] = np.clip(g[on, :3].astype(int) + r, 0, 255)
    return g
