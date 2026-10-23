#!/usr/bin/env python3
"""preview_gif.py <out.gif> <frame1.png> ... [--durations 100,100,200] [--fps 12] [--scale 2]

A faithful looping preview: exactly the given frames in the given order, transparent background, 1:1 unless
--scale, each frame at --durations (ms, one per frame) or --fps. GIF holds 1-bit alpha and delays in 10 ms
steps; alpha is thresholded at 128 and delays rounded. After writing, the GIF is decoded back and checked
frame by frame (count, alpha, colours, delays); a mismatch exits 1. Prints JSON; "exact" describes decoded
colour/alpha fidelity, not timing. It is false when the
frames have partial alpha or more than 255 colours (alpha and count are then still checked).
"""

from __future__ import annotations

import argparse
import json
import math
import sys

from _assembly import expand, require_pillow, preflight_outputs

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("out")
ap.add_argument("frames", nargs="+")
ap.add_argument("--durations")
ap.add_argument("--fps", type=float, default=12)
ap.add_argument("--scale", type=int, default=1)
a = ap.parse_args()
Image = require_pillow()

paths = expand(a.frames)
if a.scale < 1 or not math.isfinite(a.fps) or a.fps <= 0:
    ap.error("--scale and --fps must be positive")
fs = [Image.open(p).convert("RGBA") for p in paths]
fs = [f.resize((f.width * a.scale, f.height * a.scale), Image.NEAREST) for f in fs]
ms = [int(v) for v in a.durations.split(",")] if a.durations else [round(1000 / a.fps)] * len(fs)
if len(ms) != len(fs):
    sys.exit(f"--durations has {len(ms)} values for {len(fs)} frames: give one duration per frame")

from _gif import write_gif
preflight_outputs([a.out], paths)
try:
    report = write_gif(a.out, fs, ms)
except ValueError as exc:
    sys.exit(str(exc))
print(json.dumps(report))
