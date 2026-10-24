"""The local half of create_normal_map: pack frames, split the returned strip, preview the lighting.

    python normal_map.py gif <out.gif> <frame1.png> <frame2.png> ...
        pack animation frames into one GIF to upload when GIF transport is selected; MCP also accepts documented strips/animation references
    python normal_map.py split <strip_n.png> <frame1.png> <frame2.png> ...
        cut the returned strip and save <frame>_n.png beside each frame
    python normal_map.py preview <out.gif> <sprite.png> <normal.png> [--frames N] [--scale 2] [--directx]
        a light circling the sprite (a strip of N frames plays while it circles), plus <out>_lights.png with rows
        lit from the left, top and right; flat or banded areas are the parts that do not change with the light.
        --directx for a DirectX map (green = down, Unreal); the default is OpenGL.

Needs Pillow and numpy; without them prints a skipped status and exits 3.
"""
import argparse
import json
import math
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("cmd", choices=("gif", "split", "preview"))
ap.add_argument("out")
ap.add_argument("inputs", nargs="+")
ap.add_argument("--frames", type=int, default=1)
ap.add_argument("--scale", type=int, default=2)
ap.add_argument("--directx", action="store_true")
a = ap.parse_args()
from _assembly import expand, open_still, require_numpy, require_pillow, preflight_outputs
from _gif import write_gif  # noqa: E402

if a.cmd == "preview":
    require_numpy()
    import numpy as np  # noqa: E402
else:
    require_pillow()
from PIL import Image  # noqa: E402


if a.frames < 1 or a.scale < 1:
    ap.error("--frames and --scale must be positive")
if a.cmd == "gif":
    paths = expand(a.inputs)
    preflight_outputs([a.out], paths)
    frames = [open_still(f) for f in paths]
    w, h = frames[0].size
    if any(f.size != (w, h) for f in frames):
        sys.exit("frames differ in size: pad them to one canvas first")
    result = write_gif(a.out, frames, [100] * len(frames))
    result['purpose'] = 'upload conversion; GIF quantizes colour/alpha'
    print(json.dumps(result))

elif a.cmd == "split":
    strip, names = open_still(a.out), expand(a.inputs)
    w = strip.width // len(names)
    if w * len(names) != strip.width:
        sys.exit(f"strip is {strip.width} px wide, not a multiple of {len(names)} frames")
    expected = [Image.open(n).size for n in names]
    if any(size != (w, strip.height) for size in expected):
        sys.exit("normal strip cells must match every corresponding source frame size")
    destinations = [Path(n).with_name(Path(n).stem + "_n.png") for n in names]
    preflight_outputs(destinations, [a.out] + names)
    for i, dst in enumerate(destinations):
        strip.crop((i * w, 0, (i + 1) * w, strip.height)).save(dst)
    print(json.dumps({"written": [str(p) for p in destinations], "frames": len(names)}))

else:
    if len(a.inputs) != 2:
        sys.exit("preview takes <out.gif> <sprite.png> <normal.png>")
    sprite, normal = (open_still(p) for p in a.inputs)
    if sprite.size != normal.size:
        sys.exit(f"sprite {sprite.size} and map {normal.size} differ in size")
    if sprite.width % a.frames:
        ap.error("strip width must divide exactly by --frames")
    still = Path(a.out).with_name(Path(a.out).stem + "_lights.png")
    preflight_outputs([a.out, still], a.inputs)
    alb = np.asarray(sprite, dtype=np.float32) / 255
    nrm = np.asarray(normal, dtype=np.float32)[..., :3] / 127.5 - 1    # OpenGL: x right, y up, z out
    if a.directx:
        nrm[..., 1] *= -1  # DirectX: green points down
    nrm /= np.maximum(np.linalg.norm(nrm, axis=2, keepdims=True), 1e-6)
    n, fw = a.frames, sprite.width // a.frames

    def shade(angle):
        """The whole strip lit from angle (0 = right, pi/2 = top), keeping source alpha."""
        light = np.array([math.cos(angle), math.sin(angle), 0.6])
        light /= np.linalg.norm(light)
        lit = np.clip(nrm @ light, 0, 1) * 0.85 + 0.25                  # lambert + ambient
        img = np.dstack([np.clip(alb[..., :3] * lit[..., None], 0, 1), alb[..., 3:]]) * 255
        return Image.fromarray(img.astype(np.uint8), "RGBA")


    steps = max(24, n * 3)
    gifs = []
    for s in range(steps):
        f = s * n // steps
        frame = shade(2 * math.pi * s / steps).crop((f * fw, 0, (f + 1) * fw, sprite.height))
        gifs.append(frame.resize((fw * a.scale, sprite.height * a.scale), Image.NEAREST))
    result = write_gif(a.out, gifs, [80] * len(gifs))
    sheet = Image.new("RGBA", (sprite.width, sprite.height * 3))
    for i, angle in enumerate((math.pi, math.pi / 2, 0)):
        sheet.paste(shade(angle), (0, i * sprite.height))
    still = Path(a.out).with_name(Path(a.out).stem + "_lights.png")
    sheet.save(still)
    result.update({"lighting_inspection": str(still), "purpose": "derived lighting inspection; source colours transformed"})
    print(json.dumps(result))
