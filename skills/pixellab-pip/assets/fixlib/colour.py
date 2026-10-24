"""Colour maths shared by the doctor and the finishing helpers: OKLab and the colour groups (skin, white/grey/black
neutrals, hue families). Needs numpy only."""
import numpy as np


def oklab(rgb: np.ndarray) -> np.ndarray:
    """sRGB 0-255 (..., 3) to OKLab."""
    c = rgb.astype(np.float64) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    lms = c @ np.array([[0.4122214708, 0.2119034982, 0.0883024619], [0.5363325363, 0.6806995451, 0.2817188376],
                        [0.0514459929, 0.1073969566, 0.6299787005]])
    lms = np.cbrt(lms)
    return lms @ np.array([[0.2104542553, 1.9779984951, 0.0259040371], [0.7936177850, -2.4285922050, 0.7827717662],
                           [-0.0040720468, 0.4505937099, -0.8086757660]])


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
