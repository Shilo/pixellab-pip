"""Faithful GIF encoding and decoded fidelity checks shared by standard previews.

GIF quantizes alpha at 128, colour to at most 255 entries, and delay to 10 ms.
Composition, requested playback transformations and output collision checks belong to callers.
"""
from io import BytesIO
import math
from _assembly import require_pillow


def write_gif(path, frames, durations):
    Image = require_pillow()
    from PIL import ImageSequence, GifImagePlugin
    fs = [f.convert("RGBA") for f in frames]
    if not fs or len(fs) != len(durations):
        raise ValueError("give one positive duration per frame")
    if any(f.size != fs[0].size for f in fs):
        raise ValueError("GIF frames differ in size; pad first")
    if any(isinstance(d, bool) or not isinstance(d, (int, float)) or not math.isfinite(d)
           or d <= 0 or d > 655350 for d in durations):
        raise ValueError("GIF durations must be finite positive milliseconds, at most 655350")
    ms = [max(10, round(d / 10) * 10) for d in durations]
    colors = sorted({px[:3] for f in fs for px in f.getdata() if px[3] >= 128})
    pal_im = None
    if len(colors) > 255:   # more colours than a GIF holds: one shared 255-colour palette, no dithering
        strip = Image.new("RGB", (sum(f.width for f in fs), max(f.height for f in fs)))
        x = 0
        for f in fs:
            strip.paste(f.convert("RGB"), (x, 0))
            x += f.width
        pal_im = strip.quantize(255, method=0, dither=0)
        colors = [tuple(pal_im.getpalette()[i * 3:i * 3 + 3]) for i in range(255)]
    exact = pal_im is None and all(px[3] in (0, 255) for f in fs for px in f.getdata())
    lut = {c: i + 1 for i, c in enumerate(colors)}   # index 0 = transparent

    out = []
    for k, f in enumerate(fs):
        if pal_im is None:
            idx = [lut[px[:3]] if px[3] >= 128 else 0 for px in f.getdata()]
        else:
            q = f.convert("RGB").quantize(palette=pal_im, dither=0).getdata()
            idx = [q[i] + 1 if px[3] >= 128 else 0 for i, px in enumerate(f.getdata())]
        im = Image.new("P", f.size)
        im.putdata(idx)
        im.putpalette([0, 0, 0] + [v for c in colors for v in c])
        out.append(im)
    buffer = BytesIO()
    # Write each full frame explicitly: save_all merges identical opaque frames and loses their indices.
    header, _ = GifImagePlugin.getheader(out[0], info={"loop": 0, "transparency": 0, "optimize": False})
    buffer.write(b"".join(header))
    for image, duration in zip(out, ms):
        buffer.write(b"".join(GifImagePlugin.getdata(image, duration=duration, disposal=2, transparency=0)))
    buffer.write(b";")

    buffer.seek(0)
    with Image.open(buffer) as gif:
        got = [(g.convert("RGBA"), g.info.get("duration")) for g in ImageSequence.Iterator(gif)]
    problems = []
    if len(got) != len(fs):
        problems.append(f"{len(got)} frames decoded, {len(fs)} given")
    for k, ((g, d), f) in enumerate(zip(got, fs)):
        want = [(0 if px[3] < 128 else 255) for px in f.getdata()]
        if g.size != f.size or [px[3] for px in g.getdata()] != want or d != ms[k]:
            problems.append(f"frame {k + 1}: alpha or delay differs")
        elif any(w and gp[:3] != ep for w, gp, ep in zip(want, g.getdata(), out[k].convert('RGB').getdata())):
            problems.append(f"frame {k + 1}: colours differ")
    report = {"written": str(path), "frames": len(got), "durations_ms": ms,
              "exact": exact, "colors_quantized": pal_im is not None,
              "alpha_thresholded": any(px[3] not in (0, 255) for f in fs for px in f.getdata()), "problems": problems}
    if problems:
        raise ValueError("GIF verification failed: " + "; ".join(problems))
    with open(path, "xb") as handle:
        handle.write(buffer.getvalue())
    return report
