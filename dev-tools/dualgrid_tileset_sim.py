#!/usr/bin/env python3
"""Simulate deterministic PixelLab MCP DualGrid tileset structure.

This does not predict PixelLab's generated art. It previews the 16 returned
corner patterns for MCP-style create_topdown_tileset and
create_sidescroller_tileset requests.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover - friendly CLI failure
    raise SystemExit("Pillow is required: python -m pip install pillow") from exc


LOWER = "lower"
UPPER = "upper"
WILDCARD = 255

# 4x4 atlas layouts. PixelLab currently returns the same row-major order as
# the Lexaloffle reference image. TileMapDual's Godot preset stores the same
# 16 bitmasks at different atlas coordinates.
LAYOUTS = {
    "pixellab": [13, 10, 4, 12, 6, 8, 0, 1, 11, 3, 2, 5, 15, 14, 9, 7],
    "lexaloffle-row": [13, 10, 4, 12, 6, 8, 0, 1, 11, 3, 2, 5, 15, 14, 9, 7],
    "tilemapdual-standard": [4, 10, 13, 12, 9, 14, 15, 7, 2, 3, 11, 5, 0, 8, 6, 1],
}
DEFAULT_OUT_DIR = Path(".local") / "dualgrid-sim-output"
MCP_TOOLS = {
    "create_sidescroller_tileset": {
        "required": ("lower_description", "transition_description"),
        "default_request": {
            "lower_description": "",
            "transition_description": "",
            "tile_size": {"width": 16, "height": 16},
            "transition_size": 0.0,
            "detail": "low detail",
            "shading": "flat shading",
            "outline": "lineless",
        },
        "tile_sizes": {(16, 16), (32, 32)},
        "transition_sizes": {0.0, 0.25, 0.5},
    },
    "create_topdown_tileset": {
        "required": ("lower_description", "upper_description"),
        "default_request": {
            "lower_description": "",
            "upper_description": "",
            "transition_description": "",
            "tile_size": {"width": 16, "height": 16},
            "mode": "standard",
            "view": "high top-down",
            "transition_size": 0.0,
            "detail": "low detail",
            "shading": "flat shading",
            "outline": "lineless",
        },
        "tile_sizes": {(16, 16), (32, 32), (64, 64)},
        "transition_sizes": {0.0, 0.25, 0.5, 1.0},
    },
}

# PixelLab bit order from observed metadata and the Lexaloffle reference:
#   1 2  -> NW NE
#   3 4  -> SW SE
# Interpreted as an offset/index: NW=8, NE=4, SW=2, SE=1.
#
# TileMapDual's legacy enum uses TOP_LEFT=1, LOW_LEFT=2,
# TOP_RIGHT=4, LOW_RIGHT=8. Its atlas order needs the matching key scheme.
BIT_ORDERS = {
    "pixellab": [("NW", 8), ("NE", 4), ("SW", 2), ("SE", 1)],
    "lexaloffle-row": [("NW", 8), ("NE", 4), ("SW", 2), ("SE", 1)],
    "tilemapdual-standard": [("NW", 1), ("NE", 4), ("SW", 2), ("SE", 8)],
}
DEFAULT_FILLED_BITS = {
    "pixellab": 0,
    "lexaloffle-row": 0,
    "tilemapdual-standard": 1,
}


def bitmask_to_corners(bitmask: int, filled_bit: int, bit_order: list[tuple[str, int]]) -> dict[str, str]:
    return {
        corner: LOWER if bool(bitmask & weight) == bool(filled_bit) else UPPER
        for corner, weight in bit_order
    }


def make_tiles(layout: str, filled_bit: int) -> list[tuple[str, dict[str, str], int]]:
    name_prefix = "wang" if layout in {"pixellab", "lexaloffle-row"} and filled_bit == 0 else f"{layout}_key"
    return [
        (f"{name_prefix}_{bitmask}", bitmask_to_corners(bitmask, filled_bit, BIT_ORDERS[layout]), bitmask)
        for bitmask in LAYOUTS[layout]
    ]


COLORS = {
    "transparent": (0, 0, 0, 0),
    "upper_preview": (255, 255, 255, 255),
    LOWER: (0, 0, 0, 255),
    UPPER: (255, 255, 255, 255),
    "grid": (255, 0, 255, 255),
    "boundary": (255, 255, 255, 255),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render a schematic PixelLab MCP DualGrid/Wang tileset from a "
            "create_topdown_tileset or create_sidescroller_tileset request."
        )
    )
    parser.add_argument("tool", choices=sorted(MCP_TOOLS))
    parser.add_argument(
        "request_json",
        nargs="?",
        type=Path,
        help="Optional JSON request file. If omitted, reads JSON from stdin when present, otherwise uses a minimal empty request.",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=8,
        help="Nearest-neighbor scale for human-readable preview PNGs.",
    )
    parser.add_argument(
        "--draw-grid",
        action="store_true",
        help="Draw magenta tile boundaries on preview images.",
    )
    parser.add_argument(
        "--layout",
        choices=sorted(LAYOUTS),
        default="pixellab",
        help="Atlas order to simulate. Defaults to pixellab.",
    )
    parser.add_argument(
        "--filled-bit",
        type=int,
        choices=[0, 1],
        default=None,
        help=(
            "Which bit value represents filled/lower terrain. Defaults to 0 for "
            "PixelLab/Lexaloffle layouts and 1 for TileMapDual."
        ),
    )
    parser.add_argument(
        "--template-sheet",
        type=Path,
        help=(
            "Optional existing 4x4 PixelLab sidescroller sheet. When supplied, "
            "the simulator reuses its alpha masks as the DualGrid fill shapes."
        ),
    )
    return parser.parse_args()


def load_request(tool: str, request_json: Path | None) -> dict[str, Any]:
    base = dict(MCP_TOOLS[tool]["default_request"])
    raw = ""
    if request_json is not None:
        raw = request_json.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    if not raw.strip():
        return base
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise SystemExit("Request JSON must be an object.")
    base.update(data)
    return base


def tile_size_from_request(request: dict[str, Any]) -> tuple[int, int]:
    tile_size = request.get("tile_size", {"width": 16, "height": 16})
    width = int(tile_size.get("width", 16))
    height = int(tile_size.get("height", 16))
    if width <= 0 or height <= 0:
        raise SystemExit("tile_size width and height must be positive.")
    return width, height


def validate_request(tool: str, request: dict[str, Any], tile_width: int, tile_height: int) -> list[str]:
    config = MCP_TOOLS[tool]
    warnings: list[str] = []
    for field in config["required"]:
        if field not in request:
            raise SystemExit(f"{tool} requires {field}.")

    if (tile_width, tile_height) not in config["tile_sizes"]:
        raise SystemExit(f"{tool} does not support tile_size {tile_width}x{tile_height}.")
    if tool == "create_topdown_tileset":
        mode = request.get("mode", "standard")
        if mode not in {"standard", "pro"}:
            raise SystemExit("create_topdown_tileset mode must be standard or pro.")
        if mode == "standard" and tile_width == 64:
            raise SystemExit("create_topdown_tileset standard mode supports 16x16 or 32x32; use pro for 64x64.")
        if request.get("view", "high top-down") not in {"low top-down", "high top-down"}:
            raise SystemExit("create_topdown_tileset view must be low top-down or high top-down.")
        if mode == "pro":
            warnings.append("Top-down pro mode may not preserve the compact 4x4 output shape.")

    raw_transition = float(request.get("transition_size", 0.0))
    if raw_transition not in config["transition_sizes"]:
        values = ", ".join(str(value) for value in sorted(config["transition_sizes"]))
        raise SystemExit(f"{tool} transition_size must be one of {values}.")
    if tool == "create_topdown_tileset" and raw_transition == 1.0:
        warnings.append("Top-down transition_size 1.0 can expand beyond a compact 4x4 sheet.")

    detail = request.get("detail")
    if detail is not None and detail not in {"low detail", "medium detail", "highly detailed"}:
        raise SystemExit("detail must be low detail, medium detail, or highly detailed.")
    shading = request.get("shading")
    if shading is not None and shading not in {
        "flat shading",
        "basic shading",
        "medium shading",
        "detailed shading",
        "highly detailed shading",
    }:
        raise SystemExit("shading is not a recognized PixelLab MCP shading value.")
    outline = request.get("outline")
    if outline is not None and outline not in {"single color outline", "selective outline", "lineless"}:
        raise SystemExit("outline must be single color outline, selective outline, or lineless.")
    return warnings


def transition_pixels(tool: str, request: dict[str, Any], tile_height: int) -> int:
    raw = float(request.get("transition_size", 0.0))
    if raw not in MCP_TOOLS[tool]["transition_sizes"]:
        raise SystemExit("transition_size is invalid for this MCP tool.")
    return max(1, round(tile_height * raw)) if raw > 0 else 0


def expected_pattern_4x4(corners: dict[str, str]) -> dict[str, list[int]]:
    value = {LOWER: 0, UPPER: 1}
    return {
        "row_0": [WILDCARD, WILDCARD, WILDCARD, WILDCARD],
        "row_1": [WILDCARD, value[corners["NW"]], value[corners["NE"]], WILDCARD],
        "row_2": [WILDCARD, value[corners["SW"]], value[corners["SE"]], WILDCARD],
        "row_3": [WILDCARD, WILDCARD, WILDCARD, WILDCARD],
    }


def quadrant_at(x: int, y: int, tile_width: int, tile_height: int) -> str:
    horizontal = "W" if x < tile_width / 2 else "E"
    vertical = "N" if y < tile_height / 2 else "S"
    return vertical + horizontal


def terrain_at(corners: dict[str, str], x: int, y: int, width: int, height: int) -> str:
    return corners[quadrant_at(x, y, width, height)]


def draw_corner_preview(
    tile_width: int,
    tile_height: int,
    draw_grid: bool,
    tiles: list[tuple[str, dict[str, str], int]],
) -> Image.Image:
    sheet = Image.new("RGBA", (tile_width * 4, tile_height * 4), COLORS["upper_preview"])
    draw = ImageDraw.Draw(sheet)
    half_w = tile_width // 2
    half_h = tile_height // 2

    for index, (_, corners, _) in enumerate(tiles):
        ox = (index % 4) * tile_width
        oy = (index // 4) * tile_height
        rects = {
            "NW": (ox, oy, ox + half_w - 1, oy + half_h - 1),
            "NE": (ox + half_w, oy, ox + tile_width - 1, oy + half_h - 1),
            "SW": (ox, oy + half_h, ox + half_w - 1, oy + tile_height - 1),
            "SE": (ox + half_w, oy + half_h, ox + tile_width - 1, oy + tile_height - 1),
        }
        for corner, terrain in corners.items():
            draw.rectangle(rects[corner], fill=COLORS[terrain])
        if draw_grid:
            draw.rectangle((ox, oy, ox + tile_width - 1, oy + tile_height - 1), outline=COLORS["grid"])
    return sheet


def dualgrid_lower_mask(corners: dict[str, str], tile_width: int, tile_height: int) -> Image.Image:
    """Draw a stylized DualGrid lower-terrain mask.

    PixelLab's generated art is not a literal geometric mask, but observed
    sidescroller outputs behave like this: one lower corner creates a corner
    chunk, two adjacent lower corners create an edge strip, three lower corners
    create a mostly solid tile with one missing corner, all lower is solid, and
    all upper is empty.
    """

    mask = Image.new("1", (tile_width, tile_height), 0)
    draw = ImageDraw.Draw(mask)
    lower = {name for name, value in corners.items() if value == LOWER}
    if not lower:
        return mask
    if len(lower) == 4:
        draw.rectangle((0, 0, tile_width - 1, tile_height - 1), fill=1)
        return mask

    x_mid = tile_width // 2
    y_mid = tile_height // 2
    left = x_mid - 1
    right = x_mid
    top = y_mid - 1
    bottom = y_mid

    rects = {
        "NW": (0, 0, left, top),
        "NE": (right, 0, tile_width - 1, top),
        "SW": (0, bottom, left, tile_height - 1),
        "SE": (right, bottom, tile_width - 1, tile_height - 1),
    }
    for corner in lower:
        draw.rectangle(rects[corner], fill=1)

    # Adjacent lower corners are connected across the shared tile edge.
    if {"NW", "NE"}.issubset(lower):
        draw.rectangle((0, 0, tile_width - 1, top), fill=1)
    if {"SW", "SE"}.issubset(lower):
        draw.rectangle((0, bottom, tile_width - 1, tile_height - 1), fill=1)
    if {"NW", "SW"}.issubset(lower):
        draw.rectangle((0, 0, left, tile_height - 1), fill=1)
    if {"NE", "SE"}.issubset(lower):
        draw.rectangle((right, 0, tile_width - 1, tile_height - 1), fill=1)

    # Diagonal pairs stay separated in DualGrid-style tiles.
    return mask


def boundary_mask(lower_mask: Image.Image, thickness: int) -> Image.Image:
    if thickness <= 0:
        return Image.new("1", lower_mask.size, 0)
    width, height = lower_mask.size
    boundary = Image.new("1", lower_mask.size, 0)
    pixels = lower_mask.load()
    out = boundary.load()
    for y in range(height):
        for x in range(width):
            if not pixels[x, y]:
                continue
            found_empty_neighbor = False
            for dy in range(-thickness, thickness + 1):
                for dx in range(-thickness, thickness + 1):
                    nx = x + dx
                    ny = y + dy
                    if nx < 0 or ny < 0 or nx >= width or ny >= height or not pixels[nx, ny]:
                        found_empty_neighbor = True
                        break
                if found_empty_neighbor:
                    break
            out[x, y] = 1 if found_empty_neighbor else 0
    return boundary


def draw_platform_preview(
    tool: str,
    request: dict[str, Any],
    tile_width: int,
    tile_height: int,
    draw_grid: bool,
    tiles: list[tuple[str, dict[str, str], int]],
    template_sheet: Image.Image | None = None,
) -> Image.Image:
    sheet = Image.new("RGBA", (tile_width * 4, tile_height * 4), COLORS["upper_preview"])
    draw = ImageDraw.Draw(sheet)
    thickness = transition_pixels(tool, request, tile_height)

    for index, (_, corners, _) in enumerate(tiles):
        ox = (index % 4) * tile_width
        oy = (index // 4) * tile_height
        if template_sheet is None:
            lower_mask = dualgrid_lower_mask(corners, tile_width, tile_height)
        else:
            crop = template_sheet.crop((ox, oy, ox + tile_width, oy + tile_height)).convert("RGBA")
            lower_mask = Image.new("1", (tile_width, tile_height), 0)
            for y in range(tile_height):
                for x in range(tile_width):
                    lower_mask.putpixel((x, y), 1 if crop.getpixel((x, y))[3] else 0)
        edge_mask = boundary_mask(lower_mask, thickness)
        for y in range(tile_height):
            for x in range(tile_width):
                if lower_mask.getpixel((x, y)):
                    color = COLORS["boundary"] if edge_mask.getpixel((x, y)) else COLORS[LOWER]
                    sheet.putpixel((ox + x, oy + y), color)
        if draw_grid:
            draw.rectangle((ox, oy, ox + tile_width - 1, oy + tile_height - 1), outline=COLORS["grid"])
    return sheet


def save_scaled(image: Image.Image, path: Path, scale: int) -> None:
    image.save(path)
    if scale > 1:
        scaled = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        scaled.save(path.with_name(path.stem + f"-x{scale}" + path.suffix))


def build_report(
    tool: str,
    request: dict[str, Any],
    warnings: list[str],
    tile_width: int,
    tile_height: int,
    layout: str,
    filled_bit: int,
    tiles: list[tuple[str, dict[str, str], int]],
) -> dict[str, Any]:
    return {
        "source": "PixelLab MCP DualGrid metadata-derived simulator",
        "tool": tool,
        "limits": [
            "This simulates DualGrid/Wang corner layout only.",
            "It does not predict PixelLab's AI texture, palette, or exact compositing.",
            "expected_pattern_4x4 is derived from corners; observed PixelLab metadata often disagrees across surfaces.",
            "Boundary preview is per-tile schematic and does not model cross-tile seam continuity.",
            "Template alpha masks count any opaque pixel as occupied, including upper/detail pixels.",
            "When template_sheet is used, fill masks are copied from that observed PixelLab output.",
        ],
        "warnings": warnings,
        "request": {
            "lower_description": request.get("lower_description", ""),
            "upper_description": request.get("upper_description", ""),
            "transition_description": request.get("transition_description", ""),
            "tile_size": {"width": tile_width, "height": tile_height},
            "transition_size": request.get("transition_size", 0.0),
            "mode": request.get("mode"),
            "view": request.get("view"),
            "detail": request.get("detail"),
            "shading": request.get("shading"),
            "outline": request.get("outline"),
        },
        "terrain_encoding": {LOWER: 0, UPPER: 1, "wildcard": WILDCARD},
        "sheet_layout": {
            "columns": 4,
            "rows": 4,
            "layout": layout,
            "filled_bit": filled_bit,
            "tile_order": LAYOUTS[layout],
            "bit_weights": {corner: weight for corner, weight in BIT_ORDERS[layout]},
            "note": "bit_weights describe the tile key; filled_bit controls which key value maps to lower terrain.",
        },
        "tiles": [
            {
                "name": name,
                "sheet_col": index % 4,
                "sheet_row": index // 4,
                "bounding_box": {
                    "x": (index % 4) * tile_width,
                    "y": (index // 4) * tile_height,
                    "width": tile_width,
                    "height": tile_height,
                },
                "corners": corners,
                "expected_pattern_4x4": expected_pattern_4x4(corners),
                "bitmask": bitmask,
                "bitmask_binary": format(bitmask, "04b"),
                "bit_order": ", ".join(f"{corner}={weight}" for corner, weight in BIT_ORDERS[layout]),
            }
            for index, (name, corners, bitmask) in enumerate(tiles)
        ],
    }


def self_check() -> None:
    pixel_order = BIT_ORDERS["pixellab"]
    assert bitmask_to_corners(13, 0, pixel_order) == {
        "NW": UPPER,
        "NE": UPPER,
        "SW": LOWER,
        "SE": UPPER,
    }
    assert bitmask_to_corners(0, 0, pixel_order) == {
        "NW": LOWER,
        "NE": LOWER,
        "SW": LOWER,
        "SE": LOWER,
    }
    tilemapdual_order = BIT_ORDERS["tilemapdual-standard"]
    assert bitmask_to_corners(1, 1, tilemapdual_order) == {
        "NW": LOWER,
        "NE": UPPER,
        "SW": UPPER,
        "SE": UPPER,
    }


def main() -> None:
    self_check()
    args = parse_args()
    request = load_request(args.tool, args.request_json)
    tile_width, tile_height = tile_size_from_request(request)
    warnings = validate_request(args.tool, request, tile_width, tile_height)
    filled_bit = args.filled_bit if args.filled_bit is not None else DEFAULT_FILLED_BITS[args.layout]
    tiles = make_tiles(args.layout, filled_bit)

    DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)

    template_sheet = None
    if args.template_sheet:
        template_sheet = Image.open(args.template_sheet).convert("RGBA")
        expected_size = (tile_width * 4, tile_height * 4)
        if template_sheet.size != expected_size:
            raise SystemExit(f"Template sheet must be {expected_size[0]}x{expected_size[1]}, got {template_sheet.size}.")

    corner = draw_corner_preview(tile_width, tile_height, args.draw_grid, tiles)
    platform = draw_platform_preview(args.tool, request, tile_width, tile_height, args.draw_grid, tiles, template_sheet)

    save_scaled(corner, DEFAULT_OUT_DIR / "dualgrid-corner-preview.png", args.scale)
    save_scaled(platform, DEFAULT_OUT_DIR / "dualgrid-tileset-preview.png", args.scale)

    report = build_report(args.tool, request, warnings, tile_width, tile_height, args.layout, filled_bit, tiles)
    if args.template_sheet:
        report["template_sheet"] = str(args.template_sheet)
    with (DEFAULT_OUT_DIR / "dualgrid-patterns.json").open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    print(f"Wrote {DEFAULT_OUT_DIR / 'dualgrid-corner-preview.png'}")
    print(f"Wrote {DEFAULT_OUT_DIR / 'dualgrid-tileset-preview.png'}")
    print(f"Wrote {DEFAULT_OUT_DIR / 'dualgrid-patterns.json'}")


if __name__ == "__main__":
    main()
