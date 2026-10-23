"""recolor_groups.py - a colour variant of a sprite and its frames. Clean-up; writes copies only.

Colours are sorted into groups (skin, white/grey/black neutrals, hue families); each named group goes to a named
colour while every pixel keeps its place on the light-to-dark ramp. Exact per colour, so pixels stay pixels; the
still and every frame get the same mapping. A frame colour the still lacks takes the group of its nearest still
colour. Skin never moves unless named.

    python recolor_groups.py hero.png --groups --out DIR                        # what the sprite is made of
    python recolor_groups.py hero.png frames/*.png --swap red=indigo --swap blue=#b9ad94 --out DIR

--groups writes nothing. Otherwise writes DIR/<same names> (the still too) and DIR/derivative.json.
"""
import argparse
import os

import _derive

_derive.require_numpy()
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402


def oklab(rgb: np.ndarray) -> np.ndarray:
    """sRGB 0-255 (..., 3) to OKLab."""
    c = rgb.astype(np.float64) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    lms = c @ np.array([[0.4122214708, 0.2119034982, 0.0883024619], [0.5363325363, 0.6806995451, 0.2817188376],
                        [0.0514459929, 0.1073969566, 0.6299787005]])
    lms = np.cbrt(lms)
    return lms @ np.array([[0.2104542553, 1.9779984951, 0.0259040371], [0.7936177850, -2.4285922050, 0.7827717662],
                           [-0.0040720468, 0.4505937099, -0.8086757660]])


def rgb_of(lab: np.ndarray) -> np.ndarray:
    """OKLab -> sRGB 0-255 (clipped)."""
    m1 = np.array([[1.0, 1.0, 1.0], [0.3963377774, -0.1055613458, -0.0894841775], [0.2158037573, -0.0638541728, -1.2914855480]])
    lms = (lab @ m1) ** 3
    m2 = np.array([[4.0767416621, -1.2684380046, -0.0041960863], [-3.3077115913, 2.6097574011, -0.7034186147],
                   [0.2309699292, -0.3413193965, 1.7076147010]])
    c = np.clip(lms @ m2, 0, 1)
    c = np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)
    return np.round(c * 255).astype(np.uint8)


# target colours as OKLCH (lightness, chroma, hue degrees): picked off sRGB swatches
NAMED = {
    "crimson": (0.44, 0.16, 22), "red": (0.56, 0.19, 28), "scarlet": (0.60, 0.20, 35), "orange": (0.70, 0.16, 55),
    "gold": (0.78, 0.13, 85), "yellow": (0.88, 0.15, 100), "olive": (0.58, 0.10, 115), "green": (0.60, 0.15, 145),
    "emerald": (0.55, 0.12, 160), "teal": (0.60, 0.09, 195), "cyan": (0.75, 0.10, 210), "blue": (0.55, 0.15, 255),
    "navy": (0.35, 0.10, 265), "indigo": (0.42, 0.14, 285), "purple": (0.50, 0.15, 305), "violet": (0.55, 0.16, 295),
    "magenta": (0.60, 0.20, 335), "pink": (0.75, 0.11, 355), "brown": (0.45, 0.07, 60), "white": (0.95, 0.01, 90),
    "silver": (0.78, 0.01, 250), "grey": (0.60, 0.00, 0), "black": (0.22, 0.01, 280), "bone": (0.88, 0.03, 85),
}
HUES = [("red", 0, 40), ("orange", 40, 70), ("yellow", 70, 110), ("green", 110, 170), ("teal", 170, 220),
        ("blue", 220, 275), ("purple", 275, 330), ("pink", 330, 360)]


def _lch(lab: np.ndarray) -> np.ndarray:
    return np.stack([lab[..., 0], np.hypot(lab[..., 1], lab[..., 2]), np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360], -1)


def group_of(rgb: np.ndarray) -> np.ndarray:
    """Group name per colour, (N, 3) uint8 -> (N,) str."""
    out = np.empty(len(rgb), dtype=object)
    for i, (l, c, h) in enumerate(_lch(oklab(rgb))):
        if c < 0.035 or (c < 0.07 and l >= 0.62 and 50 <= h <= 110):   # cream and its shadows count as white
            out[i] = "white" if l >= 0.62 else ("black" if l < 0.38 else "grey")
        elif 30 <= h <= 75 and 0.06 <= c <= 0.13 and 0.55 <= l <= 0.85:
            out[i] = "skin"
        else:
            out[i] = next(n for n, lo, hi in HUES if lo <= h < hi)
    return out


def groups(img: Image.Image) -> dict:
    """{group: share of opaque pixels}, biggest first."""
    x = np.array(img.convert("RGBA"))
    cols, n = np.unique(x[x[..., 3] >= 128][:, :3], axis=0, return_counts=True)
    tot: dict = {}
    for name, k in zip(group_of(cols), n):
        tot[name] = tot.get(name, 0) + int(k)
    s = sum(tot.values()) or 1
    return dict(sorted(((k, round(v / s, 3)) for k, v in tot.items()), key=lambda kv: -kv[1]))


def parse(swaps: list) -> dict:
    """GROUP=COLOUR, COLOUR a name from NAMED or #rrggbb (added to NAMED as its OKLCH)."""
    out = {}
    for s in swaps:
        g, c = (v.strip() for v in s.split("="))
        if c.startswith("#") and len(c) == 7:
            l, ch, h = _lch(oklab(np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)]], np.uint8)))[0]
            NAMED[c] = (float(l), float(ch), float(h))
        elif c not in NAMED:
            raise SystemExit("unknown colour %r (known: %s, or #rrggbb)" % (c, ", ".join(sorted(NAMED))))
        out[g] = c
    return out


class Swap:
    """Built on the still: its colours' groups and each group's mean lightness; applied to any image of that body."""

    def __init__(self, still: Image.Image, swaps: dict):
        x = np.array(still.convert("RGBA"))
        self.cols = np.unique(x[x[..., 3] >= 128][:, :3], axis=0)
        self.lab = oklab(self.cols)
        self.grp = group_of(self.cols)
        self.swaps = swaps
        self.mean_l = {g: float(self.lab[self.grp == g][:, 0].mean()) for g in set(self.grp)}

    def colour(self, rgb: np.ndarray) -> np.ndarray:
        lab = oklab(rgb)
        g = self.grp[((lab[:, None] - self.lab[None]) ** 2).sum(-1).argmin(1)]
        out = rgb.copy()
        for name, target in self.swaps.items():
            sel = g == name
            if not sel.any():
                continue
            tl, tc, th = NAMED[target]
            l = np.clip(tl + (lab[sel, 0] - self.mean_l.get(name, tl)), 0.05, 0.98)   # the ramp kept around tl
            c = np.full(sel.sum(), tc) * np.clip(1.0 - np.abs(l - tl) * 0.8, 0.4, 1.0)   # ramp ends a little greyer
            h = np.radians(th)
            out[sel] = rgb_of(np.stack([l, c * np.cos(h), c * np.sin(h)], -1))
        return out

    def __call__(self, img: Image.Image) -> Image.Image:
        x = np.array(img.convert("RGBA"))
        on = x[..., 3] > 0
        if on.any():
            cols, inv = np.unique(x[on][:, :3], axis=0, return_inverse=True)
            x[on, :3] = self.colour(cols)[inv.ravel()]
        return Image.fromarray(x, "RGBA")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("still")
    ap.add_argument("frames", nargs="*")
    ap.add_argument("--out", required=True)
    ap.add_argument("--swap", action="append", default=[], metavar="GROUP=COLOUR")
    ap.add_argument("--groups", action="store_true")
    a = ap.parse_args()
    still = Image.open(a.still).convert("RGBA")
    if a.groups or not a.swap:
        for g, share in groups(still).items():
            print("%-7s %5.1f%%" % (g, share * 100))
        print("colours:", ", ".join(sorted(NAMED)))
        raise SystemExit(0)
    files = [a.still] + _derive.expand(a.frames)
    run = _derive.Run("recolor_groups", "cleanup", a.out, files)
    swaps = parse(a.swap)
    swap = Swap(still, swaps)
    for f in files:
        run.save(swap(Image.open(f)), os.path.basename(f))
    run.done(swaps=swaps)
    print("%d image(s) -> %s" % (len(files), a.out))
