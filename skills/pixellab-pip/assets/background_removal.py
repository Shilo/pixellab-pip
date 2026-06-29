#!/usr/bin/env python3
"""Conservative background removal and validation for PixelLab outputs.

This helper is intentionally deterministic. It removes:
- edge-connected pixels matching the sampled background color.

It also analyzes enclosed background-colored components so callers can safely
fall back to PixelLab when local deterministic removal is uncertain.

It never repaints RGB values. Removed pixels keep their original RGB and get
alpha set to 0.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - exercised by missing runtime
    print(f"error: Pillow is required: {exc}", file=sys.stderr)
    sys.exit(3)


RGBA = tuple[int, int, int, int]
RGB = tuple[int, int, int]


def parse_rgb(value: str) -> RGB | None:
    if value == "auto":
        return None
    parts = value.split(",")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("expected auto or R,G,B")
    try:
        rgb = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("RGB values must be integers") from exc
    if any(channel < 0 or channel > 255 for channel in rgb):
        raise argparse.ArgumentTypeError("RGB values must be 0..255")
    return rgb  # type: ignore[return-value]


def pixel_luma(pixel: RGBA) -> float:
    r, g, b, _ = pixel
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def pixel_saturation(pixel: RGBA) -> int:
    r, g, b, _ = pixel
    return max(r, g, b) - min(r, g, b)


def color_close(pixel: RGBA, bg: RGB, tolerance: int) -> bool:
    if pixel[3] == 0:
        return False
    return max(abs(pixel[i] - bg[i]) for i in range(3)) <= tolerance


def idx_to_xy(index: int, width: int) -> tuple[int, int]:
    return index % width, index // width


def neighbors4(index: int, width: int, height: int) -> list[int]:
    x, y = idx_to_xy(index, width)
    out: list[int] = []
    if x > 0:
        out.append(index - 1)
    if x + 1 < width:
        out.append(index + 1)
    if y > 0:
        out.append(index - width)
    if y + 1 < height:
        out.append(index + width)
    return out


def neighbors8(index: int, width: int, height: int) -> list[int]:
    x, y = idx_to_xy(index, width)
    out: list[int] = []
    for dy in (-1, 0, 1):
        yy = y + dy
        if yy < 0 or yy >= height:
            continue
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            xx = x + dx
            if 0 <= xx < width:
                out.append((yy * width) + xx)
    return out


def sample_background(
    pixels: list[RGBA], width: int, height: int, min_edge_share: float
) -> tuple[RGB, dict[str, Any]]:
    edge: list[RGB] = []
    for x in range(width):
        for index in (x, ((height - 1) * width) + x):
            pixel = pixels[index]
            if pixel[3] > 0:
                edge.append(pixel[:3])
    for y in range(1, height - 1):
        for index in ((y * width), (y * width) + width - 1):
            pixel = pixels[index]
            if pixel[3] > 0:
                edge.append(pixel[:3])
    if not edge:
        raise ValueError("no opaque edge pixels available for background sampling")
    color, count = Counter(edge).most_common(1)[0]
    share = count / len(edge)
    report = {
        "edge_opaque_pixels": len(edge),
        "edge_dominant_rgb": color,
        "edge_dominant_count": count,
        "edge_dominant_share": round(share, 3),
    }
    if share < min_edge_share:
        raise ValueError(
            "auto background sampling is ambiguous; pass --bg-color R,G,B "
            f"or use PixelLab fallback (dominant edge share {share:.3f})"
        )
    return color, report


def flood_edge_background(bg_like: list[bool], width: int, height: int) -> set[int]:
    queue: deque[int] = deque()
    seen: set[int] = set()

    for x in range(width):
        queue.append(x)
        queue.append(((height - 1) * width) + x)
    for y in range(height):
        queue.append(y * width)
        queue.append((y * width) + width - 1)

    while queue:
        index = queue.popleft()
        if index in seen or not bg_like[index]:
            continue
        seen.add(index)
        for neighbor in neighbors4(index, width, height):
            if neighbor not in seen and bg_like[neighbor]:
                queue.append(neighbor)
    return seen


def connected_components(mask: list[bool], width: int, height: int) -> list[list[int]]:
    visited: set[int] = set()
    components: list[list[int]] = []

    for start, enabled in enumerate(mask):
        if not enabled or start in visited:
            continue
        component: list[int] = []
        queue: deque[int] = deque([start])
        visited.add(start)
        while queue:
            index = queue.popleft()
            component.append(index)
            for neighbor in neighbors4(index, width, height):
                if mask[neighbor] and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        components.append(component)
    return components


def component_bbox(component: list[int], width: int) -> tuple[int, int, int, int]:
    xs: list[int] = []
    ys: list[int] = []
    for index in component:
        x, y = idx_to_xy(index, width)
        xs.append(x)
        ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def touches_exterior(index: int, exterior: set[int], width: int, height: int) -> bool:
    return any(neighbor in exterior for neighbor in neighbors8(index, width, height))


def classify_enclosed_component(
    component: list[int],
    *,
    pixels: list[RGBA],
    component_mask: set[int],
    exterior: set[int],
    outline_mask: list[bool],
    width: int,
    height: int,
    min_area: int,
    max_area_ratio: float,
    outline_coverage: float,
    max_exterior_outline_ratio: float,
) -> dict[str, Any]:
    image_area = width * height
    area = len(component)
    boundary: set[int] = set()
    direct_exterior = 0

    for index in component:
        for neighbor in neighbors8(index, width, height):
            if neighbor not in component_mask:
                boundary.add(neighbor)
                if neighbor in exterior:
                    direct_exterior += 1

    outline = [index for index in boundary if outline_mask[index]]
    exterior_outline = [
        index for index in outline if touches_exterior(index, exterior, width, height)
    ]
    opaque_boundary = [index for index in boundary if pixels[index][3] > 0]

    outline_ratio = len(outline) / max(1, len(opaque_boundary))
    exterior_outline_ratio = len(exterior_outline) / max(1, len(outline))
    bbox = component_bbox(component, width)

    report = {
        "area": area,
        "bbox": bbox,
        "boundary_pixels": len(boundary),
        "outline_ratio": round(outline_ratio, 3),
        "exterior_outline_ratio": round(exterior_outline_ratio, 3),
        "direct_exterior_contacts": direct_exterior,
    }

    if area < min_area:
        report["reason"] = "too_small"
        return report
    if area / image_area > max_area_ratio:
        report["reason"] = "too_large"
        return report
    if direct_exterior:
        report["reason"] = "touches_exterior_background"
        return report
    if outline_ratio < outline_coverage:
        report["reason"] = "weak_outline_boundary"
        return report
    if exterior_outline_ratio > max_exterior_outline_ratio:
        report["reason"] = "mostly_exterior_silhouette_outline"
        return report

    report["reason"] = "strong_outline_enclosed_bg_like"
    return report


def remove_background(args: argparse.Namespace) -> dict[str, Any]:
    source = Path(args.input)
    target = Path(args.output)
    if not source.exists():
        raise FileNotFoundError(source)

    image = Image.open(source).convert("RGBA")
    width, height = image.size
    pixels: list[RGBA] = list(image.getdata())

    if args.bg_color is not None:
        bg_color = args.bg_color
        sample_report: dict[str, Any] = {
            "mode": "explicit",
            "background_rgb": bg_color,
        }
    else:
        bg_color, sample_report = sample_background(
            pixels, width, height, args.min_edge_color_share
        )
        sample_report["mode"] = "auto"
    bg_like = [color_close(pixel, bg_color, args.tolerance) for pixel in pixels]

    exterior = flood_edge_background(bg_like, width, height)
    original_opaque = sum(1 for pixel in pixels if pixel[3] > 0)

    outline_mask = [
        pixel[3] > 0
        and not bg_like[index]
        and (
            pixel_luma(pixel) <= args.outline_luma
            or (
                pixel_luma(pixel) <= args.gray_outline_luma
                and pixel_saturation(pixel) <= args.gray_outline_saturation
            )
        )
        for index, pixel in enumerate(pixels)
    ]

    remaining_bg = [
        is_bg and index not in exterior for index, is_bg in enumerate(bg_like)
    ]
    components = connected_components(remaining_bg, width, height)

    remove: set[int] = set(exterior)
    enclosed_components: list[dict[str, Any]] = []

    for component in components:
        component_mask = set(component)
        component_report = classify_enclosed_component(
            component,
            pixels=pixels,
            component_mask=component_mask,
            exterior=exterior,
            outline_mask=outline_mask,
            width=width,
            height=height,
            min_area=args.min_enclosed_area,
            max_area_ratio=args.max_enclosed_area_ratio,
            outline_coverage=args.outline_coverage,
            max_exterior_outline_ratio=args.max_exterior_outline_ratio,
        )
        enclosed_components.append(component_report)

    output_pixels: list[RGBA] = []
    for index, pixel in enumerate(pixels):
        if index in remove and pixel[3] != 0:
            output_pixels.append((pixel[0], pixel[1], pixel[2], 0))
        else:
            output_pixels.append(pixel)

    output = Image.new("RGBA", (width, height))
    output.putdata(output_pixels)
    target.parent.mkdir(parents=True, exist_ok=True)
    output.save(target)

    significant_unresolved = [
        component
        for component in enclosed_components
        if component["reason"] != "too_small"
        and component["area"] >= args.min_enclosed_area
    ]
    remaining_bg_like = [
        index
        for index, is_bg in enumerate(bg_like)
        if is_bg and index not in remove and pixels[index][3] > 0
    ]
    remaining_opaque = sum(
        1 for index, pixel in enumerate(pixels) if index not in remove and pixel[3] > 0
    )
    removed_opaque = original_opaque - remaining_opaque
    removed_opaque_ratio = removed_opaque / max(1, original_opaque)
    enclosed_reasons = Counter(component["reason"] for component in enclosed_components)
    fallback_reasons: list[str] = []
    if remaining_bg_like:
        fallback_reasons.append("remaining_background_like_pixels")
    if significant_unresolved:
        fallback_reasons.append("significant_unresolved_enclosed_components")
    if removed_opaque_ratio >= args.max_removed_opaque_ratio:
        fallback_reasons.append("nearly_all_opaque_pixels_removed")
    if len(exterior) == 0:
        fallback_reasons.append("no_edge_connected_background_removed")
    status = "needs_pixellab_fallback" if fallback_reasons else "passed_conservative_checks"
    report: dict[str, Any] = {
        "input": str(source),
        "output": str(target),
        "width": width,
        "height": height,
        "background_rgb": bg_color,
        "background_sample": sample_report,
        "tolerance": args.tolerance,
        "removed_edge_connected_pixels": len(exterior),
        "removed_enclosed_pixels": 0,
        "original_opaque_pixels": original_opaque,
        "remaining_opaque_pixels": remaining_opaque,
        "removed_opaque_ratio": round(removed_opaque_ratio, 4),
        "remaining_background_like_pixels": len(remaining_bg_like),
        "local_result_status": status,
        "fallback_reasons": fallback_reasons,
        "significant_unresolved_enclosed_component_count": len(significant_unresolved),
        "significant_unresolved_enclosed_components_sample": significant_unresolved[
            : args.max_rejected_report
        ],
        "enclosed_background_like_component_count": len(enclosed_components),
        "enclosed_background_like_component_reasons": dict(enclosed_reasons),
        "enclosed_background_like_components_sample": enclosed_components[
            : args.max_rejected_report
        ],
        "method": "edge_connected_background_removal_with_enclosed_component_validation",
    }
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove edge-connected pixel-art backgrounds and report enclosed uncertainty."
    )
    parser.add_argument("input", help="Input PNG path")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument(
        "--bg-color",
        default=None,
        type=parse_rgb,
        metavar="auto|R,G,B",
        help="Background RGB. Defaults to auto-sampled most common edge color.",
    )
    parser.add_argument("--tolerance", type=int, default=2)
    parser.add_argument("--min-edge-color-share", type=float, default=0.6)
    parser.add_argument("--min-enclosed-area", type=int, default=4)
    parser.add_argument("--max-enclosed-area-ratio", type=float, default=0.10)
    parser.add_argument("--outline-coverage", type=float, default=0.75)
    parser.add_argument("--max-exterior-outline-ratio", type=float, default=0.25)
    parser.add_argument("--outline-luma", type=int, default=80)
    parser.add_argument("--gray-outline-luma", type=int, default=125)
    parser.add_argument("--gray-outline-saturation", type=int, default=24)
    parser.add_argument("--max-removed-opaque-ratio", type=float, default=0.95)
    parser.add_argument("--max-rejected-report", type=int, default=25)
    parser.add_argument("--report", help="Optional JSON report path")
    parser.add_argument("--quiet", action="store_true", help="Do not print JSON report")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.quiet and not args.report:
        print("error: --quiet requires --report", file=sys.stderr)
        return 2

    try:
        report = remove_background(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if not args.quiet:
        print(json.dumps(report, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
