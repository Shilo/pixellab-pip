#!/usr/bin/env python3
"""pad_sprite.py <sprite.png> <out.png> <canvas_w> <canvas_h> <x> [y]

Copy a sprite onto a larger transparent canvas without scaling or changing its pixels, so a motion has room.
y defaults to feet on the bottom edge (the lowest drawn row, not the file's bottom). Prints the placement
offset as JSON {"offset": [x, y]}: where the sprite's top-left sits on the padded canvas.
"""

from __future__ import annotations

import json
import sys

from _assembly import require_pillow, preflight_outputs

if len(sys.argv) not in (6, 7) or sys.argv[1] in ("-h", "--help"):
    sys.exit(__doc__)
Image = require_pillow()

src, out = sys.argv[1], sys.argv[2]
w, h, x = (int(v) for v in sys.argv[3:6])
im = Image.open(src).convert("RGBA")
bbox = im.getbbox()
feet = bbox[3] if bbox else im.height   # rows below this are empty
y = int(sys.argv[6]) if len(sys.argv) == 7 else h - feet
if x < 0 or y < 0 or x + im.width > w or y + feet > h:
    sys.exit(f"sprite {im.width}x{feet} at ({x}, {y}) does not fit the {w}x{h} canvas")
preflight_outputs([out], [src])
canvas = Image.new("RGBA", (w, h))
canvas.alpha_composite(im.crop((0, 0, im.width, feet)), (x, y))
canvas.save(out)
print(json.dumps({"offset": [x, y]}))
