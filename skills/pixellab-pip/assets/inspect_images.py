#!/usr/bin/env python3
"""Read-only image/frame facts and optional explicit dimension/count checks."""

from __future__ import annotations

import argparse
import json

from PIL import Image, ImageSequence


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive integer") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return number


def image_size(value: str) -> tuple[int, int]:
    parts = value.split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("expected WIDTHxHEIGHT, both positive integers")
    return positive_int(parts[0]), positive_int(parts[1])


def inspect_images(
    paths: list[str],
    expected_size: tuple[int, int] | None = None,
    expected_frames: int | None = None,
) -> dict:
    files, errors, total = [], [], 0
    for path in paths:
        item = {"path": path, "frames": []}
        files.append(item)
        try:
            with Image.open(path) as image:
                is_gif = image.format == "GIF"
                if is_gif:
                    item["loop"] = image.info.get("loop")
                for index, frame in enumerate(ImageSequence.Iterator(image)):
                    frame.load()  # Decode all pixels, including later animated frames.
                    alpha = frame.convert("RGBA").getchannel("A")
                    facts = {
                        "index": index,
                        "size": list(frame.size),
                        "alpha_extrema": list(alpha.getextrema()),
                        "bounds": alpha.getbbox(),
                    }
                    if is_gif:
                        facts["duration_ms"] = frame.info.get("duration")
                    item["frames"].append(facts)
                    total += 1
                    if expected_size is not None and frame.size != expected_size:
                        errors.append(
                            f"{path} frame {index}: size {frame.width}x{frame.height}; "
                            f"expected {expected_size[0]}x{expected_size[1]}"
                        )
        except (OSError, ValueError, SyntaxError, EOFError, Image.DecompressionBombError) as exc:
            errors.append(f"{path}: {type(exc).__name__}: {exc}")
    if expected_frames is not None and total != expected_frames:
        errors.append(f"decoded {total} frames; expected {expected_frames}")
    return {"files": files, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="image files in intended frame order")
    parser.add_argument("--expect-size", type=image_size, metavar="WIDTHxHEIGHT")
    parser.add_argument("--expect-frames", type=positive_int, metavar="COUNT",
                        help="expected total decoded frames across all inputs")
    args = parser.parse_args()
    report = inspect_images(args.paths, args.expect_size, args.expect_frames)
    print(json.dumps(report, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
