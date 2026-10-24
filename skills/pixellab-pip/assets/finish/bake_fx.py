"""bake_fx.py - bake an effect clip (a vfx_workbench export) into a character's frames: one set of frames with the
body, the projectile and the impact. New pixels (a composite); writes copies only.

    python bake_fx.py body0.png body1.png ... --fx burst.png [--json burst.json] --at 250,70 --from 9 [--widen 320]
                      [--anchor x,y] --out DIR

--fx: the exported sprite sheet (frames read from its .json; without one, square frames side by side).
--at x,y: where the effect's centre goes, in body-frame pixels (the impact point).
--anchor x,y: put this point of the effect frame on --at instead of its centre (the export's "anchor (origin)",
e.g. where a beam starts: --at <the eye> --anchor <the export's origin>).
--from N: the body frame (1-based position in the list) the effect's first frame lands on. When the effect runs past
the last body frame, that frame is held until the effect ends - the body freezes for that long (reported as
held_frames; fine for a held beam or a cast).
--widen W: grow every frame to W pixels wide, the new room on the right; feet and the pad offset stay put.
Writes DIR/0.png ... and DIR/derivative.json; give the sheet the body timing, then the effect's own frame times.
"""
import argparse
import json
import os
import sys

import _derive

_derive.require_numpy()
from PIL import Image  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("frames", nargs="+")
ap.add_argument("--fx", required=True)
ap.add_argument("--json")
ap.add_argument("--at", required=True, help="x,y of the effect centre")
ap.add_argument("--from", dest="start", type=int, required=True, help="1-based body frame of the first effect frame")
ap.add_argument("--widen", type=int, default=0)
ap.add_argument("--anchor", help="x,y inside the effect frame that goes on --at (default: its centre)")
ap.add_argument("--out", required=True)
a = ap.parse_args()
if a.start < 1 or a.widen < 0:
    ap.error("--from must be positive and --widen nonnegative")
frames = _derive.expand(a.frames)
js = a.json or os.path.splitext(a.fx)[0] + ".json"
run = _derive.Run("bake_fx", "new_pixels", a.out, frames + [a.fx] + ([js] if os.path.exists(js) else []))

sheet = Image.open(a.fx).convert("RGBA")
if os.path.exists(js):
    frs = json.load(open(js, encoding="utf-8"))["frames"]
    frs = frs if isinstance(frs, list) else list(frs.values())
    boxes = [(f["frame"]["x"], f["frame"]["y"], f["frame"]["x"] + f["frame"]["w"], f["frame"]["y"] + f["frame"]["h"])
             for f in frs]
    print("effect timing in its json: %s ms" % ",".join(str(f.get("duration", "?")) for f in frs))
else:
    s = sheet.height
    if sheet.width % s:
        sys.exit("effect strip width must divide into square cells; supply JSON for other layouts")
    boxes = [(x, 0, x + s, s) for x in range(0, sheet.width, s)]
fx = [sheet.crop(b) for b in boxes]

body = [Image.open(f).convert("RGBA") for f in frames]
w = max(a.widen, max(b.width for b in body))
h = max(b.height for b in body)
first = a.start - 1
n = max(len(body), first + len(fx))
cx, cy = (int(v) for v in a.at.split(","))
for i in range(n):
    c = Image.new("RGBA", (w, h))
    b = body[min(i, len(body) - 1)]
    c.alpha_composite(b, (0, h - b.height))
    k = i - first
    change = {"body": os.path.basename(frames[min(i, len(body) - 1)])}
    if 0 <= k < len(fx):
        e = fx[k]
        ax, ay = (int(v) for v in a.anchor.split(",")) if a.anchor else (e.width // 2, e.height // 2)
        c.alpha_composite(e, (cx - ax, cy - ay))
        change["effect_frame"] = k
    run.save(c, "%d.png" % i, **change)
run.done(held_frames=n - len(body), width=w)
print("%d frames (%d body + %d held) -> %s" % (n, len(body), n - len(body), a.out))
