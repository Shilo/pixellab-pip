#!/usr/bin/env python3
"""Pack same-size animation frames, in the given order, into one spritesheet row.

Writes <out_stem>.png and <out_stem>.json (Aseprite "array" JSON: frames[].frame and duration ms, meta.size/image,
plus meta.pixellab: frame_count, hit_frame, optional pad_offset and facing). --godot [RES_DIR] also writes
<out_stem>.tres, a Godot 4 SpriteFrames resource with per-frame durations. Every frame is written exactly once;
durations are metadata only and never repeat or drop frames.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

from _assembly import expand, open_still, require_pillow, preflight_outputs

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("out_stem")
ap.add_argument("frames", nargs="+")
ap.add_argument("--durations", help="milliseconds per frame, comma-separated, one per frame")
ap.add_argument("--fps", type=float, default=12, help="even timing when --durations is absent")
ap.add_argument("--hit", type=int, help="explicit 0-based contact/damage frame")
ap.add_argument("--pad", help="X,Y: where the source sprite's top-left sits on these frames")
ap.add_argument("--facing", choices=["left", "right"])
ap.add_argument("--godot", nargs="?", const="", metavar="RES_DIR", help="also write .tres; RES_DIR under res://")
ap.add_argument("--loop", action="store_true", help="the Godot animation loops (idle, walk); default plays once")
a = ap.parse_args()
Image = require_pillow()

paths = expand(a.frames)
ims = [open_still(p) for p in paths]
n = len(ims)
w, h = ims[0].size
if any(im.size != (w, h) for im in ims):
    sys.exit("frames differ in size; pad them to one canvas first (pad_sprite.py)")
if not math.isfinite(a.fps) or a.fps <= 0:
    ap.error("--fps must be positive and finite")
dur = [int(v) for v in a.durations.split(",")] if a.durations else [round(1000 / a.fps)] * n
if len(dur) != n or min(dur) <= 0:
    sys.exit(f"--durations needs {n} positive values, one per frame")
hit = a.hit
if hit is not None and not 0 <= hit < n:
    sys.exit(f"--hit must be 0..{n - 1}")

outputs = [a.out_stem + ".png", a.out_stem + ".json"] + ([a.out_stem + ".tres"] if a.godot is not None else [])
preflight_outputs(outputs, paths)
if a.pad:
    px, py = (int(v) for v in a.pad.split(","))
sheet = Image.new("RGBA", (w * n, h))
frames = []
for k, im in enumerate(ims):
    sheet.paste(im, (k * w, 0))
    frames.append({"filename": os.path.basename(paths[k]), "frame": {"x": k * w, "y": 0, "w": w, "h": h},
                   "rotated": False, "trimmed": False, "spriteSourceSize": {"x": 0, "y": 0, "w": w, "h": h},
                   "sourceSize": {"w": w, "h": h}, "duration": dur[k]})
png = a.out_stem + ".png"
sheet.save(png)
extra = {"frame_count": n}
if hit is not None:
    extra["hit_frame"] = hit
if a.pad:
    px, py = (int(v) for v in a.pad.split(","))
    extra["pad_offset"] = {"x": px, "y": py}
if a.facing:
    extra["facing"] = a.facing
meta = {"app": "pixellab-pip make_sheet.py", "image": os.path.basename(png), "format": "RGBA8888",
        "size": {"w": sheet.width, "h": sheet.height}, "scale": "1", "pixellab": extra}
with open(a.out_stem + ".json", "w", encoding="utf-8") as f:
    json.dump({"frames": frames, "meta": meta}, f, indent=1)
written = [png, a.out_stem + ".json"]

if a.godot is not None:
    base = min(dur)
    res = "res://" + "/".join(p for p in (a.godot.strip("/\\").replace("\\", "/"), os.path.basename(png)) if p)
    lines = [f'[gd_resource type="SpriteFrames" load_steps={n + 2} format=3]', "",
             f'[ext_resource type="Texture2D" path="{res}" id="1"]', ""]
    for k, f in enumerate(frames):
        r = f["frame"]
        lines += [f'[sub_resource type="AtlasTexture" id="f{k}"]', 'atlas = ExtResource("1")',
                  f'region = Rect2({r["x"]}, {r["y"]}, {r["w"]}, {r["h"]})', ""]
    anim = ", ".join('{"duration": %.3f, "texture": SubResource("f%d")}' % (d / base, k) for k, d in enumerate(dur))
    name = os.path.basename(a.out_stem)
    lines += ["[resource]", 'animations = [{"frames": [%s], "loop": %s, "name": &"%s", "speed": %.3f}]'
              % (anim, "true" if a.loop else "false", name, 1000.0 / base)]
    with open(a.out_stem + ".tres", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    written.append(a.out_stem + ".tres")

print(json.dumps({"written": written, "frames": n, "frame_size": [w, h]}))
