"""Synthetic pixel art for the finishing-helper tests: one small figure and a smooth walk.
Canvas 48x56, figure at (8, 6): feet on row 53, a 1 px staff at x = 33. Needs numpy."""
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


def figure() -> np.ndarray:
    a = np.zeros((H, W, 4), np.uint8)
    ox, oy = 8, 6
    _box(a, ox + 12, oy + 2, ox + 20, oy + 6, HAIR)
    _box(a, ox + 12, oy + 6, ox + 20, oy + 14, SKIN)
    a[oy + 9, ox + 14, :3] = OUT
    a[oy + 9, ox + 17, :3] = OUT
    _box(a, ox + 10, oy + 14, ox + 22, oy + 34, BLUE)
    _box(a, ox + 17, oy + 14, ox + 22, oy + 34, SHADE)
    _box(a, ox + 10, oy + 34, ox + 16, oy + 43, SHADE)
    _box(a, ox + 17, oy + 34, ox + 23, oy + 43, SHADE)
    _box(a, ox + 10, oy + 43, ox + 16, oy + 48, BOOT)
    _box(a, ox + 17, oy + 43, ox + 23, oy + 48, BOOT)
    _box(a, ox + 22, oy + 22, ox + 25, oy + 27, SKIN)
    _box(a, ox + 25, oy + 4, ox + 26, oy + 48, STAFF)
    return a


def shift(f, dx, dy):
    """Moved by (dx, dy); what leaves the canvas is gone."""
    g = np.zeros_like(f)
    h, w = f.shape[:2]
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    g[yd, xd] = f[ys, xs]
    return g


def walk(n: int = 8) -> list:
    dx = [0, 1, 1, 0, 0, -1, -1, 0]
    return [shift(figure(), dx[i % len(dx)], 0) for i in range(n)]


def bright(f, k):
    g = f.copy()
    on = g[..., 3] > 0
    g[on, :3] = np.clip(g[on, :3].astype(float) * k, 0, 255).astype(np.uint8)
    return g


def png(a, path):
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    Image.fromarray(a, "RGBA").save(path)
    return str(path)


def save(frames, folder, stem):
    return [png(f, os.path.join(str(folder), "%s_%d.png" % (stem, i))) for i, f in enumerate(frames, 1)]
