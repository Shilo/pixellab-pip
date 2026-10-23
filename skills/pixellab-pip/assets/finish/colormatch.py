"""colormatch.py - fix the colour drift of generated key poses and in-betweens. Clean-up; writes copies only.

Each frame's mean brightness is scaled to the standing sprite's, then every opaque pixel is snapped to the standing
sprite's own colours. Run it after scrub.py and before building the sheet or GIF.

    python colormatch.py <standing.png> <frames...> --out DIR

Writes DIR/<same names> and DIR/derivative.json.
"""
import argparse
import os

import _derive

_derive.require_numpy()
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("standing")
ap.add_argument("frames", nargs="+")
ap.add_argument("--out", required=True)
a = ap.parse_args()
files = _derive.expand(a.frames)
run = _derive.Run("colormatch", "cleanup", a.out, [a.standing] + files)
ref = np.array(Image.open(a.standing).convert("RGBA"))
pal = np.unique(ref[ref[..., 3] > 0][:, :3], axis=0).astype(float)
target = ref[ref[..., 3] > 0][:, :3].mean()
for f in files:
    x = np.array(Image.open(f).convert("RGBA")).astype(float)
    m = x[..., 3] > 0
    name = os.path.basename(f)
    if not m.any():
        run.save(Image.open(f).convert("RGBA"), name, empty=True)
        continue
    k = target / max(x[m][:, :3].mean(), 1e-6)
    px = np.clip(x[m][:, :3] * k, 0, 255)
    x[m, :3] = pal[((px[:, None, :] - pal[None]) ** 2).sum(2).argmin(1)]
    run.save(Image.fromarray(x.astype("uint8")), name, brightness_scale=round(float(k), 3))
    print("%s x%.2f" % (name, k))
run.done()
