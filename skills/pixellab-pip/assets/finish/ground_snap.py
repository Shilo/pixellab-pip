"""ground_snap.py - put floating frames back on the feet line. Clean-up; writes copies only.

Generated key poses and their in-betweens are often drawn a few to ~20 px higher on the padded canvas than the
standing sprite (kneels, lunges, crouches), so in the game the character hops off the ground. For grounded moves
(a foot or knee always on the floor) this moves each frame down so its lowest opaque pixel sits on the standing
sprite's feet line (pad_y + the sprite's lowest opaque row). Frames on or below the line are copied unchanged; a frame
below the line is flagged (something hangs lower: a robe, an effect) - look at it. Not for jumps, leaps or flyers.

    python ground_snap.py <standing_sprite.png> <pad_x,pad_y> <frame.png>... --out DIR [--fx 5,6] [--check]

--fx 5,6: frames with no feet on purpose (smoke-only frames of a vanish) are copied unchanged. Numbers are positions
in the frame list, counting from 1 (with 0.png ... 9.png, --fx 5,6 means 4.png and 5.png).
--check: only print each frame's gap (negative = floating); writes nothing.
Writes every frame, moved or not, to DIR/<same names> so DIR holds the whole clip, plus DIR/derivative.json.
"""
import argparse
import os

import _derive

_derive.require_numpy()
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("sprite")
ap.add_argument("pad")
ap.add_argument("frames", nargs="+")
ap.add_argument("--out")
ap.add_argument("--check", action="store_true")
ap.add_argument("--fx", default="", help="positions (from 1) of frames with no feet on purpose: left alone")
a = ap.parse_args()
frames = _derive.expand(a.frames)
_derive.require_visible(a.sprite)
st = np.array(Image.open(a.sprite).convert("RGBA"))[..., 3] > 0
feet = int(a.pad.split(",")[1]) + int(np.nonzero(st.any(1))[0].max())
fx = {int(v) - 1 for v in a.fx.split(",") if v.strip()}
if not a.check and not a.out:
    ap.error("--out is required unless --check")
run = None if a.check else _derive.Run("ground_snap", "cleanup", a.out, [a.sprite] + frames)
for n, f in enumerate(frames):
    im = Image.open(f).convert("RGBA")
    al = np.array(im)[..., 3] > 0
    name = os.path.basename(f)
    if not al.any() or n in fx:   # empty or smoke-only frames have no feet to judge
        print("  fx  %s" % f if al.any() else "EMPTY %s" % f)
        if run:
            run.save(im, name, moved=0, fx=n in fx)
        continue
    gap = int(np.nonzero(al.any(1))[0].max()) - feet
    below = gap > 0
    print("%+4d  %s%s" % (gap, f, "   below the feet line: something hangs lower (a robe, an effect?)"
                          " - not moved, look at it" if below else ""))
    if not run:
        continue
    out = Image.new("RGBA", im.size)
    out.alpha_composite(im, (0, -min(gap, 0)))
    change = {"moved": -min(gap, 0)}
    if below:
        change["below_feet"] = gap
    run.save(out, name, **change)
if run:
    run.done(feet_line=feet)
