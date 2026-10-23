"""slash_layer.py - lift a generated slash out of one animation and lay it on another. New pixels (a recoloured,
shaded effect layer); writes copies only.

  python slash_layer.py extract <raw_frame.png> <scrubbed_frame.png> --out DIR [--to air]
      the effect = pixels scrub.py removed from that frame, recoloured with an effect ramp and depth-shaded (rim,
      light core, dithered body): DIR/<raw name>_fx.png holds only the slash
  python slash_layer.py apply <frame.png> <effect.png> --out DIR [--behind] [--fade 0.5] [--offset dx,dy]
      lays the effect on a frame (in front by default; --behind puts the character on top); --fade thins it with an
      ordered-dither mask for a trailing frame; --offset moves the effect (x right, y down) when the clip it came from
      drew the arc somewhere else. Writes DIR/<frame name>.

Both swings must share the same canvas and key poses (e.g. a 7-frame and an 11-frame animate_image from the same
A/B poses) so the slash lands where the blade passes. Each run also writes DIR/derivative.json.
"""
import argparse
import os

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

RAMPS = {"air": ["#5a7896", "#8fb4d8", "#bcd8f0", "#e8f4ff", "#ffffff"],
         "fire": ["#6e1409", "#b3260e", "#e8561a", "#f8a531", "#ffe08a"],
         "arcane": ["#2d0f4a", "#5a1f86", "#8f45c4", "#c48af0", "#f0d8ff"],
         "holy": ["#4a3410", "#b29352", "#debd77", "#fff2c4", "#ffffff"],
         "shadow": ["#0a0a12", "#1c1a2e", "#34304f", "#57527a", "#8a84b0"]}
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("mode", choices=["extract", "apply"])
ap.add_argument("a")
ap.add_argument("b")
ap.add_argument("--out", required=True)
ap.add_argument("--to", default="air", choices=list(RAMPS))
ap.add_argument("--behind", action="store_true")
ap.add_argument("--fade", type=float, default=0.0)
ap.add_argument("--offset", default="0,0", help="dx,dy to move the effect by")
a = ap.parse_args()
run = _derive.Run("slash_layer", "new_pixels", a.out, [a.a, a.b])

if a.mode == "extract":
    raw = np.array(Image.open(a.a).convert("RGBA"))
    sc = np.array(Image.open(a.b).convert("RGBA"))
    m = (raw[..., 3] > 0) & (sc[..., 3] == 0)
    ramp = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in RAMPS[a.to]])
    depth = ndimage.distance_transform_cdt(m, metric="chessboard")
    out = np.zeros_like(raw)
    q = np.clip(depth, 1, len(ramp) - 1)
    out[..., :3][m] = ramp[q[m]]
    out[..., 3][m] = 255
    yy, xx = np.indices(m.shape)
    out[..., 3][m & (depth > 4) & ((yy + xx) % 2 == 0)] = 0
    name = os.path.splitext(os.path.basename(a.a))[0] + "_fx.png"
    run.save(Image.fromarray(out), name, effect_px=int(m.sum()), ramp=a.to)
    print("effect", int(m.sum()), "px ->", name)
else:
    fr = Image.open(a.a).convert("RGBA")
    fx = np.array(Image.open(a.b).convert("RGBA"))
    if a.fade > 0:
        h, w = fx.shape[:2]
        fx[..., 3][np.tile(BAYER, (h // 4 + 1, w // 4 + 1))[:h, :w] < a.fade] = 0
    dx, dy = (int(v) for v in a.offset.split(","))
    if dx or dy:   # shift, cutting what leaves the canvas
        moved = np.zeros_like(fx)
        h, w = fx.shape[:2]
        moved[max(0, dy):h + min(0, dy), max(0, dx):w + min(0, dx)] = fx[max(0, -dy):h - max(0, dy), max(0, -dx):w - max(0, dx)]
        fx = moved
    layer = Image.fromarray(fx)
    base = Image.new("RGBA", fr.size)
    for part in ((layer, fr) if a.behind else (fr, layer)):
        base.alpha_composite(part)
    run.save(base, os.path.basename(a.a), effect=os.path.basename(a.b), behind=a.behind, fade=a.fade, offset=[dx, dy])
    print("->", os.path.join(a.out, os.path.basename(a.a)))
run.done()
