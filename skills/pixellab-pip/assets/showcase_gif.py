"""One looping GIF of every move of a character side by side, for sharing (Discord, a devlog).

    python showcase_gif.py <dir> <name> [--moves attack,skill] [--scale 2] [--bg none|discord] [--out file.gif]

Reads <name>_<move>.png sheets with Aseprite-style JSON beside them (<name>_<move>.json, `frames` as a list or
hash of {frame: {x, y, w, h}, duration}). Default moves: every such pair in <dir>, known moves first
(idle, walk, run, attack, skill, cast, hurt, death). Feet on one line, a label under each move, each move on its
own timing, one shared palette. Transparent by default; `--bg discord` bakes a Discord-dark background only when
the user asks for one. Default output <dir>/<name>_showcase.gif; a relative
--out is from the caller's folder. Needs Pillow and numpy; without them prints a skipped status and exits 3.
"""
import argparse
import json
import os
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("dir")
ap.add_argument("name")
ap.add_argument("--moves", default="")
ap.add_argument("--scale", type=int, default=2)
ap.add_argument("--bg", choices=("none", "discord"), default="none")
ap.add_argument("--out")
a = ap.parse_args()
try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    print(json.dumps({"status": "skipped", "reason": f"needs numpy and Pillow: {exc}"}))
    sys.exit(3)

folder, prefix = Path(a.dir), a.name
ORDER = ["idle", "walk", "run", "attack", "skill", "cast", "hurt", "death"]
if a.moves:
    names = a.moves.split(",")
else:
    have = [p.stem[len(prefix) + 1:] for p in folder.glob(f"{prefix}_*.png") if p.with_suffix(".json").exists()]
    names = sorted(have, key=lambda m: (ORDER.index(m) if m in ORDER else len(ORDER), m))
    if not names:
        sys.exit(f"no {prefix}_<move>.png + .json sheets in {folder}")

anims = []
for n in names:
    sheet = Image.open(folder / f"{prefix}_{n}.png").convert("RGBA")
    frs = json.loads((folder / f"{prefix}_{n}.json").read_text(encoding="utf-8"))["frames"]
    frs = frs if isinstance(frs, list) else list(frs.values())
    fr, du = [], []
    for f in frs:
        r = f["frame"]
        im = sheet.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
        if a.bg == "none":   # a GIF pixel is opaque or clear: blending a soft edge onto the key colour would tint it
            im.putalpha(im.getchannel("A").point(lambda v: 255 if v >= 128 else 0))
        fr.append(im.resize((im.width * a.scale, im.height * a.scale), Image.NEAREST))
        du.append(max(20, int(f.get("duration", 100))))
    anims.append((fr, du))


def bbox(frames):
    m = np.zeros(frames[0].size[::-1], bool)
    for f in frames:
        m |= np.array(f)[..., 3] > 0
    ys, xs = np.nonzero(m)
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else (0, 0, 1, 1)


CLEAR = a.bg == "none"
BG, pad, lab, T = ((255, 0, 255, 255) if CLEAR else (43, 45, 49, 255)), 12, 26, 4000   # magenta = the clear key
crops = [bbox(fr) for fr, _ in anims]
H = max(b[3] for b in crops)
W = sum(b[2] - b[0] for b in crops) + pad * (len(anims) + 1)
Ht = H + pad * 2 + lab
pts = {0}   # every moment a move changes frame, within T ms
for _, du in anims:
    t = 0
    while t < T:
        for d in du:
            t += d
            if t < T:
                pts.add(t)
pts = sorted(pts)


def frame_at(fr, du, t):
    t %= sum(du)
    for f, d in zip(fr, du):
        if t < d:
            return f
        t -= d
    return fr[-1]


try:
    font = ImageFont.truetype("arialbd.ttf", 16)
except OSError:
    font = ImageFont.load_default()
rgb, durs = [], []
for i, t in enumerate(pts):
    c = Image.new("RGBA", (W, Ht), BG)
    d = ImageDraw.Draw(c)
    if CLEAR:
        d.fontmode = "1"   # no anti-aliasing: blended edge pixels would keep a magenta fringe
    x = pad
    for (fr, du), b, label in zip(anims, crops, (n.capitalize() for n in names)):
        f = frame_at(fr, du, t).crop((b[0], 0, b[2], b[3]))
        c.alpha_composite(f, (x, pad + H - f.height))
        d.text((x + (f.width - d.textlength(label, font=font)) / 2, pad + H + 5), label, fill=(220, 221, 222), font=font)
        x += f.width + pad
    rgb.append(c.convert("RGB"))
    durs.append((pts[i + 1] if i + 1 < len(pts) else T) - t)
# the palette sees the labels (rgb[0]) and every source frame once; sampling output frames can miss phases
srcs = [f for fr, _ in anims for f in fr]
sample = Image.new("RGB", (max(W, max(f.width for f in srcs)), Ht + sum(f.height for f in srcs)), BG[:3])
sample.paste(rgb[0], (0, 0))
y = Ht
for f in srcs:
    sample.paste(f, (0, y), f)
    y += f.height
pal = sample.quantize(colors=128, method=0)
frames = [f.quantize(palette=pal, dither=0) for f in rgb]
extra = {}
if CLEAR:   # the key colour's palette index becomes the GIF's transparent index
    extra = {"transparency": frames[0].getpixel((0, 0)), "disposal": 2}
out = Path(a.out) if a.out else folder / f"{prefix}_showcase.gif"
frames[0].save(out, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=False, **({"disposal": 1} | extra))
print(f"{out}  {len(frames)} frames {frames[0].size[0]}x{frames[0].size[1]} {os.path.getsize(out) / 1e6:.2f} MB")
