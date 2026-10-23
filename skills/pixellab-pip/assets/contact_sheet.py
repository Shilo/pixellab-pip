#!/usr/bin/env python3
"""contact_sheet.py <out.png> a.png b.png ... [--cols 10] [--scale 0.5]

A selection/review preview: images left to right in the given order on a transparent canvas, each with
a label 1..N centred under it. A long list wraps after --cols images. --scale resizes the
images (nearest neighbour) before labelling; 0.5 costs about a quarter of the image tokens.
"""

from __future__ import annotations

import json
import math
import sys

from _assembly import expand, require_pillow, preflight_outputs

args = sys.argv[2:]
if not args or sys.argv[1] in ("-h", "--help"):
    sys.exit(__doc__)


def option(name: str, cast, default):
    if name not in args:
        return default
    i = args.index(name)
    value = cast(args[i + 1])
    del args[i:i + 2]
    return value


scale = option("--scale", float, 1.0)
cols = option("--cols", int, 10)
Image = require_pillow()
from PIL import ImageDraw, ImageFont  # noqa: E402

if cols < 1 or not math.isfinite(scale) or scale <= 0:
    sys.exit("--cols and --scale must be positive")
paths = expand(args)
preflight_outputs([sys.argv[1]], paths)
groups = [paths[i:i + cols] for i in range(0, len(paths), cols)]   # wrapped: 20 frames aren't a 10,000 px strip
rows = []
for group in groups:
    row = []
    for path in group:
        im = Image.open(path).convert("RGBA")
        if scale != 1.0:
            im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.NEAREST)
        row.append(im)
    rows.append(row)

font = ImageFont.load_default()


def text_image(text: str):
    """The label's glyph pixels as a white-on-dark chip (bitmap and TrueType default fonts alike)."""
    mask = Image.new("L", (12 * len(text) + 12, 32))
    ImageDraw.Draw(mask).text((4, 4), text, font=font, fill=255)
    mask = mask.crop(mask.getbbox())
    chip = Image.new("RGBA", (mask.width + 4, mask.height + 2), (40, 40, 48, 255))
    chip.paste((255, 255, 255, 255), (2, 1), mask)
    return chip


labels = [text_image(str(i + 1)) for i in range(sum(len(r) for r in rows))]
cw = max(im.width for r in rows for im in r)
ch = max(im.height for r in rows for im in r)
row_h = ch + max(chip.height for chip in labels) + 2
out = Image.new("RGBA", (cw * max(len(r) for r in rows), row_h * len(rows)))
chips = iter(labels)
for y, row in enumerate(rows):
    for x, im in enumerate(row):
        out.alpha_composite(im, (x * cw + (cw - im.width) // 2, y * row_h + ch - im.height))
        chip = next(chips)
        out.alpha_composite(chip, (x * cw + max(0, (cw - chip.width) // 2), y * row_h + ch + 2))
out.save(sys.argv[1])
print(json.dumps({"written": sys.argv[1], "labels": len(labels), "size": list(out.size)}))
