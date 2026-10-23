"""The local half of create_normal_map: pack frames, split the returned strip, preview the lighting.

    python normal_map.py gif <out.gif> <frame1.png> <frame2.png> ...
        pack animation frames into one GIF to upload (the MCP tool reads a GIF's frames; a PNG strip is ONE image)
    python normal_map.py split <strip_n.png> <frame1.png> <frame2.png> ...
        cut the returned strip and save <frame>_n.png beside each frame
    python normal_map.py preview <out.gif> <sprite.png> <normal.png> [--frames N] [--scale 2] [--directx]
        a light circling the sprite (a strip of N frames plays while it circles), plus <out>_lights.png with rows
        lit from the left, top and right; flat or banded areas are the parts that do not change with the light.
        --directx for a DirectX map (green = down, Unreal); the default is OpenGL.

Needs Pillow and numpy; without them prints a skipped status and exits 3.
"""
import argparse
import glob
import json
import math
import re
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
try:
    import numpy as np
    from PIL import Image
except ImportError as exc:
    print(json.dumps({"status": "skipped", "reason": f"needs numpy and Pillow: {exc}"}))
    sys.exit(3)


def expand(paths):
    """cmd/PowerShell pass *.png literally: expand it here, in natural order (2.png before 10.png)."""
    out = []
    for p in paths:
        hits = glob.glob(p) if ("*" in p or "?" in p) else []
        out += sorted(hits, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]) or [p]
    return out


if a.cmd == "gif":
    frames = [Image.open(f).convert("RGBA") for f in expand(a.inputs)]
    w, h = frames[0].size
    if any(f.size != (w, h) for f in frames):
        sys.exit("frames differ in size: pad them to one canvas first")
    pal = []
    for f in frames:   # GIF alpha is on/off: index 255 = transparent, the rest = up to 255 colours
        p = f.convert("RGB").quantize(255)
        p.paste(255, mask=Image.fromarray(((np.asarray(f)[..., 3] < 128) * 255).astype(np.uint8)))
        pal.append(p)
    pal[0].save(a.out, save_all=True, append_images=pal[1:], duration=100, loop=0, disposal=2, transparency=255,
                optimize=False)   # optimize remaps the palette and loses the transparent index
    print(f"{a.out}  {len(frames)} frames {w}x{h}: upload it and pass the upload as the image")

elif a.cmd == "split":
    strip, names = Image.open(a.out).convert("RGBA"), expand(a.inputs)
    w = strip.width // len(names)
    if w * len(names) != strip.width:
        sys.exit(f"strip is {strip.width} px wide, not a multiple of {len(names)} frames")
    for i, n in enumerate(names):
        dst = Path(n).with_name(Path(n).stem + "_n.png")
        strip.crop((i * w, 0, (i + 1) * w, strip.height)).save(dst)
        print(dst)

else:
    if len(a.inputs) != 2:
        sys.exit("preview takes <out.gif> <sprite.png> <normal.png>")
    sprite, normal = (Image.open(p).convert("RGBA") for p in a.inputs)
    if sprite.size != normal.size:
        sys.exit(f"sprite {sprite.size} and map {normal.size} differ in size")
    alb = np.asarray(sprite, dtype=np.float32) / 255
    nrm = np.asarray(normal, dtype=np.float32)[..., :3] / 127.5 - 1    # OpenGL: x right, y up, z out
    if a.directx:
        nrm[..., 1] *= -1                                               # DirectX: green points down
    nrm /= np.maximum(np.linalg.norm(nrm, axis=2, keepdims=True), 1e-6)
    n, fw = a.frames, sprite.width // a.frames

    def shade(angle):
        """The whole strip lit from angle (0 = right, pi/2 = top), on a dark ground."""
        light = np.array([math.cos(angle), math.sin(angle), 0.6])
        light /= np.linalg.norm(light)
        lit = np.clip(nrm @ light, 0, 1) * 0.85 + 0.25                  # lambert + ambient
        img = np.dstack([np.clip(alb[..., :3] * lit[..., None], 0, 1), alb[..., 3:]]) * 255
        bg = Image.new("RGBA", sprite.size, (40, 40, 48, 255))
        bg.alpha_composite(Image.fromarray(img.astype(np.uint8), "RGBA"))
        return bg.convert("RGB")

    steps = max(24, n * 3)
    gifs = []
    for s in range(steps):
        f = s * n // steps
        frame = shade(2 * math.pi * s / steps).crop((f * fw, 0, (f + 1) * fw, sprite.height))
        gifs.append(frame.resize((fw * a.scale, sprite.height * a.scale), Image.NEAREST))
    gifs[0].save(a.out, save_all=True, append_images=gifs[1:], duration=80, loop=0)
    sheet = Image.new("RGB", (sprite.width, sprite.height * 3))
    for i, angle in enumerate((math.pi, math.pi / 2, 0)):
        sheet.paste(shade(angle), (0, i * sprite.height))
    still = Path(a.out).with_name(Path(a.out).stem + "_lights.png")
    sheet.save(still)
    print(f"{a.out}  {steps} steps, light circles once\n{still}  rows: light from left, top, right")
