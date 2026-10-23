#!/usr/bin/env python3
"""preview_gif.py <out.gif> <frame1.png> ... [--durations 100,100,200] [--fps 12] [--scale 2]

A faithful looping preview: exactly the given frames in the given order, transparent background, 1:1 unless
--scale, each frame at --durations (ms, one per frame) or --fps. GIF holds 1-bit alpha and delays in 10 ms
steps; alpha is thresholded at 128 and delays rounded. After writing, the GIF is decoded back and checked
frame by frame (count, alpha, colours, delays); a mismatch exits 1. Prints JSON; "exact" is false when the
frames have partial alpha or more than 255 colours (alpha and count are then still checked).
"""

from __future__ import annotations

import argparse
import json
import sys

from _assembly import expand, require_pillow

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("out")
ap.add_argument("frames", nargs="+")
ap.add_argument("--durations")
ap.add_argument("--fps", type=float, default=12)
ap.add_argument("--scale", type=int, default=1)
a = ap.parse_args()
Image = require_pillow()
from PIL import ImageSequence  # noqa: E402

fs = [Image.open(p).convert("RGBA") for p in expand(a.frames)]
fs = [f.resize((f.width * a.scale, f.height * a.scale), Image.NEAREST) for f in fs]
ms = [int(v) for v in a.durations.split(",")] if a.durations else [round(1000 / a.fps)] * len(fs)
if len(ms) != len(fs):
    sys.exit(f"--durations has {len(ms)} values for {len(fs)} frames: give one duration per frame")
ms = [max(10, round(d / 10) * 10) for d in ms]

colors = sorted({px[:3] for f in fs for px in f.getdata() if px[3] >= 128})
pal_im = None
if len(colors) > 255:   # more colours than a GIF holds: one shared 255-colour palette, no dithering
    strip = Image.new("RGB", (sum(f.width for f in fs), max(f.height for f in fs)))
    x = 0
    for f in fs:
        strip.paste(f.convert("RGB"), (x, 0))
        x += f.width
    pal_im = strip.quantize(255, method=0, dither=0)
    colors = [tuple(pal_im.getpalette()[i * 3:i * 3 + 3]) for i in range(255)]
exact = pal_im is None and all(px[3] in (0, 255) for f in fs for px in f.getdata())
lut = {c: i + 1 for i, c in enumerate(colors)}   # index 0 = transparent

out = []
for k, f in enumerate(fs):
    if pal_im is None:
        idx = [lut[px[:3]] if px[3] >= 128 else 0 for px in f.getdata()]
    else:
        q = f.convert("RGB").quantize(palette=pal_im, dither=0).getdata()
        idx = [q[i] + 1 if px[3] >= 128 else 0 for i, px in enumerate(f.getdata())]
    im = Image.new("P", f.size)
    im.putdata(idx)
    # entry 0 is never shown; a per-frame colour there stops GIF writers from merging repeated frames
    im.putpalette([k % 256, k // 256 % 256, 0] + [v for c in colors for v in c])
    out.append(im)
out[0].save(a.out, save_all=True, append_images=out[1:], duration=ms, loop=0, disposal=2,
            transparency=0, optimize=False)

with Image.open(a.out) as gif:
    got = [(g.convert("RGBA"), g.info.get("duration")) for g in ImageSequence.Iterator(gif)]
problems = []
if len(got) != len(fs):
    problems.append(f"{len(got)} frames decoded, {len(fs)} given")   # ponytail: opaque repeats can still merge
for k, ((g, d), f) in enumerate(zip(got, fs)):
    want = [(0 if px[3] < 128 else 255) for px in f.getdata()]
    if [px[3] for px in g.getdata()] != want or d != ms[k]:
        problems.append(f"frame {k + 1}: alpha or delay differs")
    elif exact and any(w and gp[:3] != fp[:3] for w, gp, fp in zip(want, g.getdata(), f.getdata())):
        problems.append(f"frame {k + 1}: colours differ")
report = {"written": a.out, "frames": len(got), "durations_ms": ms, "exact": exact, "problems": problems}
print(json.dumps(report))
sys.exit(1 if problems else 0)
