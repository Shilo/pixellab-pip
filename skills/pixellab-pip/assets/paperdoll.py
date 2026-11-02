"""Extract an exact changed-pixel overlay or compose accepted layers; no PixelLab calls.

An overlay that reproduces an edit is a candidate, not proof of a reusable equipment layer.
No alignment, thresholding, recolouring or removal of changed pixels is performed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _assembly import open_still, preflight_outputs, require_pillow


def visible_equal(a, b):
    return a[3] == b[3] and (a[3] == 0 or a[:3] == b[:3])


def extract(base, edit, region=None):
    """Copy changed edit pixels, refusing changes an ordinary overlay cannot reproduce."""
    Image = require_pillow()
    if base.size != edit.size:
        raise ValueError("base and edit must have the same canvas size and registration")
    width, height = base.size
    if region is not None:
        x0, y0, x1, y1 = region
        if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
            raise ValueError("region must be a nonempty in-canvas box; right/bottom are exclusive")
    layer = Image.new("RGBA", base.size)
    changed = over_body = 0
    for y in range(height):
        for x in range(width):
            before, after = base.getpixel((x, y)), edit.getpixel((x, y))
            if visible_equal(before, after):
                continue
            if region is not None and not (x0 <= x < x1 and y0 <= y < y1):
                raise ValueError("edit changes pixels outside the expected region; no pixels were clipped")
            layer.putpixel((x, y), after)
            changed += 1
            over_body += before[3] > 0
    if not changed:
        raise ValueError("no visible change to extract")
    combined = Image.alpha_composite(base, layer)
    if any(not visible_equal(a, b) for a, b in zip(combined.get_flattened_data(), edit.get_flattened_data())):
        raise ValueError("edit cannot be reproduced by copied pixels over this base (erasure or blended alpha)")
    return layer, {"changed_pixels": changed, "changed_base_pixels": over_body,
                   "region": region, "reproduces_edit": True, "semantic_layer_verified": False}


def write_outputs(out, image, name, inputs, report):
    """Preflight the complete output set; remove this run's partial files on write failure."""
    out = Path(out)
    destinations = [out / name, out / "derivative.json"]
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError("choose a fresh output folder")
    preflight_outputs(destinations, inputs)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    try:
        with destinations[0].open("xb") as stream:
            written.append(destinations[0])
            image.save(stream, format="PNG")
        with destinations[1].open("x", encoding="utf-8") as stream:
            written.append(destinations[1])
            json.dump(report, stream, indent=2)
            stream.write("\n")
    except Exception:
        for path in reversed(written):
            path.unlink()
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    cut = commands.add_parser("extract", help="copy exact changed pixels into a candidate overlay")
    cut.add_argument("base")
    cut.add_argument("edit")
    cut.add_argument("--region", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    cut.add_argument("--out", required=True)
    stack = commands.add_parser("compose", help="alpha-composite accepted layers in the supplied order")
    stack.add_argument("base")
    stack.add_argument("layers", nargs="+")
    stack.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    Image = require_pillow()
    try:
        inputs = [args.base, args.edit] if args.command == "extract" else [args.base, *args.layers]
        images = [open_still(path) for path in inputs]
        if args.command == "extract":
            result, changes = extract(*images, region=args.region)
            name = "layer.png"
        else:
            result = images[0]
            for layer in images[1:]:
                if layer.size != result.size:
                    raise ValueError("every layer must match the base canvas size")
                result = Image.alpha_composite(result, layer)
            changes = {"layers": len(images) - 1, "order": "as supplied, bottom to top"}
            name = "composite.png"
        report = {"helper": "paperdoll", "operation": args.command, "inputs": inputs,
                  "status": "needs_visual_review", "changes": changes}
        write_outputs(args.out, result, name, inputs, report)
        print(json.dumps(report))
        return 0
    except (ValueError, OSError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
