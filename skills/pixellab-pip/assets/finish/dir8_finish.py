"""dir8_finish.py - finish a multi-direction shot or attack: clear the generator's own flashes, drop detached specks,
put a vfx_workbench effect at the muzzle (rotated to each direction), mirror the other side. Clean-up; writes copies
only.

    python dir8_finish.py <spec.json> --out DIR

spec.json (paths relative to the spec):
{
  "speck": 40,                          # detached pixel blobs smaller than this go (before the flash goes on)
  "total": 12,                          # optional: hold the last frame until every direction has this many
  "flash": {"sheet": "vfx/flash.png", "json": "vfx/flash.json", "anchor": [3, 14]},
                                        # a vfx_workbench export; anchor = the effect's origin, it points right
                                        # (no json: "frame_w": N for a strip of N px wide frames)
  "dirs": {
    "east":  {"src": "anim/east",  "shot": 6, "muzzle": [186, 67], "angle": 0,
              "clear": {"6": [[187, 38, 224, 96]]}},           # boxes to erase on a frame (the generator's flash)
    "south": {"src": "anim/south", "shot": 8, "muzzle": [124, 58], "angle": 90,
              "replace": {"8": 7}}                             # frame 8 = a copy of frame 7 (a flash covers the body)
  },
  "mirror": {"west": "east", "south-west": "south-east"}
}
angle: degrees, + = clockwise on screen (90 = pointing down, -90 = up). The effect plays from the shot frame, one
effect frame per frame. "total" and "replace" change the frame count or order: use them only when the user asked.
Writes DIR/<direction>/0..N.png and DIR/derivative.json.
"""
import argparse
import json
import os

import _derive

_derive.require_numpy(scipy=True)
import numpy as np  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
from scipy import ndimage  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("spec")
ap.add_argument("--out", required=True)
a = ap.parse_args()
base = os.path.dirname(os.path.abspath(a.spec))
spec = json.load(open(a.spec, encoding="utf-8"))


def P(p):
    return p if os.path.isabs(p) else os.path.join(base, p)


SPECK = int(spec.get("speck", 40))
TOTAL = int(spec.get("total", 0))
fl = spec.get("flash")
sources = {}
for d, c in spec["dirs"].items():
    src, n = P(c["src"]), 0
    while os.path.exists(os.path.join(src, "%d.png" % n)):
        n += 1
    sources[d] = [os.path.join(src, "%d.png" % i) for i in range(n)]
inputs = [a.spec] + [p for ps in sources.values() for p in ps]
if fl:
    inputs += [P(fl["sheet"])] + ([P(fl["json"])] if fl.get("json") else [])
run = _derive.Run("dir8_finish", "cleanup", a.out, inputs)

flash_frames, anchor = [], (0, 0)
if fl:
    sheet = Image.open(P(fl["sheet"])).convert("RGBA")
    anchor = tuple(fl.get("anchor", [0, 0]))
    if fl.get("json"):
        for f in json.load(open(P(fl["json"]), encoding="utf-8"))["frames"]:
            r = f["frame"]
            flash_frames.append(sheet.crop((r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"])))
    else:
        fw = int(fl["frame_w"])
        flash_frames = [sheet.crop((x, 0, x + fw, sheet.height)) for x in range(0, sheet.width, fw)]


def rotated(img, angle):
    s = 2 * max(img.size) + 8
    c = Image.new("RGBA", (s, s))
    c.alpha_composite(img, (s // 2 - anchor[0], s // 2 - anchor[1]))
    return c.rotate(-angle, resample=Image.NEAREST), s // 2


def despeck(im):
    x = np.array(im)
    lab, n = ndimage.label(x[..., 3] > 0, structure=np.ones((3, 3)))
    gone = 0
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        drop = (lab > 0) & ~np.isin(lab, [k + 1 for k, sz in enumerate(sizes) if sz >= SPECK])
        gone = int(drop.sum())
        x[drop] = 0
    return Image.fromarray(x), gone


summary = {}
for d, c in spec["dirs"].items():
    frames = [Image.open(p).convert("RGBA") for p in sources[d]]
    notes = [{} for _ in frames]
    for f, fr in c.get("replace", {}).items():
        frames[int(f)] = frames[int(fr)].copy()
        notes[int(f)]["copy_of"] = int(fr)
    for f, boxes in c.get("clear", {}).items():
        x = np.array(frames[int(f)])
        for x0, y0, x1, y1 in boxes:
            x[y0:y1, x0:x1] = 0
        frames[int(f)] = Image.fromarray(x)
        notes[int(f)]["cleared_boxes"] = boxes
    for i, f in enumerate(frames):
        frames[i], notes[i]["specks_px"] = despeck(f)
    held = 0
    while len(frames) < TOTAL:
        frames.append(frames[-1].copy())
        notes.append({"held": True})
        held += 1
    shot, (mx, my), ang = int(c["shot"]), c["muzzle"], float(c.get("angle", 0))
    for k, ff in enumerate(flash_frames):
        if shot + k >= len(frames):
            break
        img, ctr = rotated(ff, ang)
        frames[shot + k].alpha_composite(img, (int(mx) - ctr, int(my) - ctr))
        notes[shot + k]["effect_frame"] = k
    for i, f in enumerate(frames):
        run.save(f, "%s/%d.png" % (d, i), **notes[i])
    summary[d] = {"frames": len(frames), "held": held, "shot": shot}
    print(d, len(frames), "frames, shot", shot)

for w, e in spec.get("mirror", {}).items():
    i = 0
    while os.path.exists(os.path.join(a.out, e, "%d.png" % i)):
        run.save(ImageOps.mirror(Image.open(os.path.join(a.out, e, "%d.png" % i))), "%s/%d.png" % (w, i), mirror_of=e)
        i += 1
    summary[w] = {"frames": i, "mirror_of": e}
    print(w, "= mirrored", e)
run.done(directions=summary)
