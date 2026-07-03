#!/usr/bin/env python3
"""Simulate deterministic PixelLab MCP tileset results.

This does not predict PixelLab's generated art. It previews the 16 returned
corner patterns for MCP-style create_topdown_tileset and
create_sidescroller_tileset requests with a simple deterministic renderer.
"""

from __future__ import annotations

import argparse
import hashlib
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

# Native compact PixelLab order observed in 15-tileset downloads.
PIXELLAB_TILE_ORDER = [13, 10, 4, 12, 6, 8, 0, 1, 11, 3, 2, 5, 15, 14, 9, 7]
PIXELLAB_BIT_ORDER = [("NW", 8), ("NE", 4), ("SW", 2), ("SE", 1)]
PIXELLAB_FILLED_BIT = 0

# Website/export layouts derived from observed PixelLab Maps downloads for a
# 16px sidescroller sheet. Values are native 15-tileset cell indexes.
EXPORT_LAYOUTS = {
    "15-tileset": {
        "columns": 4,
        "rows": 4,
        "cells": list(range(16)),
        "format": "tileset15",
        "spritesheet_layout": "tileset15_4x4",
    },
    "wang": {
        "columns": 5,
        "rows": 4,
        "cells": [13, 3, 0, 7, 10, 1, 6, 11, 2, 5, 8, 9, 15, 4, 14, 6, 12, 12, 12, 12],
        "format": "wang",
        "spritesheet_layout": "wang_5x4",
    },
    "godot-3x3": {
        "columns": 24,
        "rows": 8,
        "cells": [
            7, 10, 7, 9, 9, 9, 9, 10, 12, 8, 9, 9, 9, 9, 15, 12, 7, 9, 15, 8, 9, 9, 9, 10,
            11, 1, 11, 13, 0, 13, 0, 1, 0, 13, 0, 12, 12, 13, 0, 13, 11, 12, 12, 12, 12, 12, 12, 1,
            11, 1, 11, 8, 15, 8, 15, 1, 11, 8, 15, 12, 12, 8, 15, 1, 11, 12, 12, 12, 6, 6, 12, 8,
            11, 1, 11, 13, 0, 13, 0, 1, 11, 12, 12, 12, 12, 12, 12, 1, 11, 12, 12, 12, 6, 6, 12, 13,
            11, 1, 11, 8, 15, 8, 15, 1, 11, 12, 12, 12, 12, 12, 12, 1, 15, 12, 12, 12, 12, 12, 12, 1,
            2, 5, 2, 3, 3, 3, 3, 5, 11, 13, 0, 12, 12, 13, 0, 1, 0, 12, 12, 12, 12, 12, 12, 1,
            7, 10, 7, 9, 9, 9, 9, 10, 15, 8, 15, 12, 12, 8, 15, 8, 11, 12, 12, 12, 12, 12, 12, 1,
            2, 5, 2, 3, 3, 3, 3, 5, 12, 13, 3, 3, 3, 3, 0, 12, 2, 3, 3, 3, 0, 13, 3, 5,
        ],
        "format": "godot_3x3",
        "spritesheet_layout": "godot_3x3_24x8",
    },
}
DEFAULT_OUT_DIR = Path(".local") / "mcp-tileset-sim-output"
MCP_TOOLS = {
    "create_sidescroller_tileset": {
        "required": ("lower_description", "transition_description"),
        "allowed": {
            "lower_description",
            "transition_description",
            "transition_size",
            "tile_size",
            "outline",
            "shading",
            "detail",
            "tile_strength",
            "base_tile_id",
            "tileset_adherence",
            "tileset_adherence_freedom",
            "text_guidance_scale",
            "seed",
        },
        "defaults": {
            "tile_size": {"width": 16, "height": 16},
            "transition_size": 0.0,
            "detail": None,
            "shading": None,
            "outline": None,
            "tile_strength": 1.0,
            "base_tile_id": None,
            "tileset_adherence": 100.0,
            "tileset_adherence_freedom": 500.0,
            "text_guidance_scale": 8.0,
            "seed": None,
        },
        "tile_sizes": {(16, 16), (32, 32)},
        "transition_sizes": {0.0, 0.25, 0.5},
    },
    "create_topdown_tileset": {
        "required": ("lower_description", "upper_description"),
        "allowed": {
            "lower_description",
            "upper_description",
            "transition_description",
            "transition_size",
            "tile_size",
            "outline",
            "shading",
            "detail",
            "view",
            "mode",
            "tile_strength",
            "lower_base_tile_id",
            "upper_base_tile_id",
            "tileset_adherence",
            "tileset_adherence_freedom",
            "text_guidance_scale",
            "spread_x",
            "slope_size",
            "raggedness",
        },
        "defaults": {
            "transition_description": None,
            "tile_size": {"width": 16, "height": 16},
            "mode": "standard",
            "view": "high top-down",
            "transition_size": 0.0,
            "detail": None,
            "shading": None,
            "outline": None,
            "tile_strength": 1.0,
            "lower_base_tile_id": None,
            "upper_base_tile_id": None,
            "tileset_adherence": 100.0,
            "tileset_adherence_freedom": 500.0,
            "text_guidance_scale": 8.0,
            "spread_x": 0.5,
            "slope_size": 0.0,
            "raggedness": 0.0,
        },
        "tile_sizes": {(16, 16), (32, 32), (64, 64)},
        "transition_sizes": {0.0, 0.25, 0.5, 1.0},
    },
}


def bitmask_to_corners(bitmask: int, filled_bit: int, bit_order: list[tuple[str, int]]) -> dict[str, str]:
    return {
        corner: LOWER if bool(bitmask & weight) == bool(filled_bit) else UPPER
        for corner, weight in bit_order
    }


def make_tiles() -> list[tuple[str, dict[str, str], int]]:
    return [
        (f"wang_{bitmask}", bitmask_to_corners(bitmask, PIXELLAB_FILLED_BIT, PIXELLAB_BIT_ORDER), bitmask)
        for bitmask in PIXELLAB_TILE_ORDER
    ]


COLORS = {
    "transparent": (0, 0, 0, 0),
    "preview_background": (255, 255, 255, 255),
    LOWER: (0, 0, 0, 255),
    UPPER: (255, 255, 255, 255),
    "grid": (255, 0, 255, 255),
    "boundary": (255, 255, 255, 255),
}
KEYWORD_COLORS = [
    ("#000000", (0, 0, 0, 255)),
    ("pure black", (0, 0, 0, 255)),
    ("black", (0, 0, 0, 255)),
    ("#ffffff", (255, 255, 255, 255)),
    ("pure white", (255, 255, 255, 255)),
    ("white", (255, 255, 255, 255)),
    ("grass", (84, 154, 65, 255)),
    ("moss", (77, 132, 75, 255)),
    ("water", (56, 132, 214, 255)),
    ("ocean", (42, 101, 184, 255)),
    ("sand", (218, 189, 118, 255)),
    ("snow", (232, 238, 240, 255)),
    ("stone", (112, 112, 120, 255)),
    ("rock", (100, 100, 108, 255)),
    ("metal", (120, 132, 138, 255)),
    ("lava", (226, 74, 38, 255)),
    ("ice", (150, 216, 232, 255)),
    ("wood", (128, 80, 44, 255)),
    ("dirt", (104, 72, 42, 255)),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render a local PixelLab MCP-style tileset result from a "
            "create_topdown_tileset or create_sidescroller_tileset request."
        )
    )
    parser.add_argument("tool", choices=sorted(MCP_TOOLS))
    parser.add_argument(
        "request_json",
        nargs="?",
        type=Path,
        help="Optional JSON request file. If omitted, reads JSON from stdin when present, otherwise uses an empty request.",
    )
    parser.add_argument(
        "--renderer",
        choices=["deterministic"],
        default="deterministic",
        help="Renderer backend. Only deterministic local rendering is currently implemented.",
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
        choices=sorted(EXPORT_LAYOUTS),
        default="15-tileset",
        help="PixelLab export layout to simulate. Defaults to 15-tileset.",
    )
    parser.add_argument(
        "--output",
        help=(
            "Optional leaf directory name under .local/mcp-tileset-sim-output. "
            "Defaults to latest."
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


WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def output_dir_from_name(name: str | None) -> Path:
    leaf = name or "latest"
    if leaf in {".", ".."} or "/" in leaf or "\\" in leaf or ":" in leaf:
        raise SystemExit("--output must be a leaf directory name, not a path.")
    if leaf != leaf.rstrip(". "):
        raise SystemExit("--output cannot end with a dot or space.")
    if not leaf or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for char in leaf):
        raise SystemExit("--output may contain only letters, numbers, dots, underscores, and hyphens.")
    if leaf.rstrip(". ").upper() in WINDOWS_RESERVED_NAMES:
        raise SystemExit("--output cannot be a reserved Windows device name.")
    return DEFAULT_OUT_DIR / leaf


def load_request(request_json: Path | None) -> dict[str, Any]:
    raw = ""
    if request_json is not None:
        raw = request_json.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    if not raw.strip():
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise SystemExit("Request JSON must be an object.")
    return data


def request_value(tool: str, request: dict[str, Any], key: str) -> Any:
    if key in request:
        return request[key]
    return MCP_TOOLS[tool]["defaults"].get(key)


def tile_size_from_request(tool: str, request: dict[str, Any]) -> tuple[int, int]:
    tile_size = request_value(tool, request, "tile_size") or {"width": 16, "height": 16}
    if not isinstance(tile_size, dict):
        raise SystemExit("tile_size must be an object with width and height.")
    if "width" not in tile_size or "height" not in tile_size:
        raise SystemExit("tile_size must include both width and height.")
    if (
        isinstance(tile_size["width"], bool)
        or isinstance(tile_size["height"], bool)
        or not isinstance(tile_size["width"], int)
        or not isinstance(tile_size["height"], int)
    ):
        raise SystemExit("tile_size width and height must be integers.")
    width = tile_size["width"]
    height = tile_size["height"]
    if width <= 0 or height <= 0:
        raise SystemExit("tile_size width and height must be positive.")
    return width, height


def validate_request(
    tool: str,
    request: dict[str, Any],
    tile_width: int,
    tile_height: int,
) -> list[str]:
    config = MCP_TOOLS[tool]
    warnings: list[str] = []
    unknown_fields = sorted(set(request) - set(config["allowed"]))
    if unknown_fields:
        raise SystemExit(f"Fields not exposed by {tool} MCP schema: {', '.join(unknown_fields)}.")
    for field in config["required"]:
        if field not in request:
            raise SystemExit(f"{tool} requires {field}.")
        if not isinstance(request[field], str):
            raise SystemExit(f"{tool} requires {field} to be a string.")

    optional_text = request.get("transition_description")
    if optional_text is not None and not isinstance(optional_text, str):
        raise SystemExit("transition_description must be a string or null.")
    for field in ("base_tile_id", "lower_base_tile_id", "upper_base_tile_id"):
        if field in request and request[field] is not None and not isinstance(request[field], str):
            raise SystemExit(f"{field} must be a string or null.")
    for field in (
        "transition_size",
        "tile_strength",
        "tileset_adherence",
        "tileset_adherence_freedom",
        "text_guidance_scale",
        "spread_x",
        "slope_size",
        "raggedness",
    ):
        if field in request and (isinstance(request[field], bool) or not isinstance(request[field], (int, float))):
            raise SystemExit(f"{field} must be a number.")
    if "seed" in request and request["seed"] is not None:
        if isinstance(request["seed"], bool) or not isinstance(request["seed"], int):
            raise SystemExit("seed must be an integer or null.")

    if (tile_width, tile_height) not in config["tile_sizes"]:
        raise SystemExit(f"{tool} does not support tile_size {tile_width}x{tile_height}.")
    raw_transition = float(request_value(tool, request, "transition_size"))
    if raw_transition not in config["transition_sizes"]:
        values = ", ".join(str(value) for value in sorted(config["transition_sizes"]))
        raise SystemExit(f"{tool} transition_size must be one of {values}.")
    if tool == "create_topdown_tileset" and raw_transition == 1.0:
        raise SystemExit("Top-down transition_size 1.0 expands beyond compact output and is not simulated.")

    if tool == "create_topdown_tileset":
        mode = request_value(tool, request, "mode")
        if mode not in {"standard", "pro"}:
            raise SystemExit("create_topdown_tileset mode must be standard or pro.")
        if mode == "standard" and tile_width == 64:
            raise SystemExit("create_topdown_tileset standard mode supports 16x16 or 32x32; use pro for 64x64.")
        if request_value(tool, request, "view") not in {"low top-down", "high top-down"}:
            raise SystemExit("create_topdown_tileset view must be low top-down or high top-down.")
        if mode == "pro":
            if raw_transition >= 0.5:
                raise SystemExit("Top-down pro mode with transition_size >= 0.5 can expand beyond compact output and is not simulated.")
            warnings.append("Top-down pro mode is simulated only for compact transition_size 0.0 or 0.25 cases.")

    detail = request_value(tool, request, "detail")
    if detail is not None and detail not in {"low detail", "medium detail", "highly detailed"}:
        raise SystemExit("detail must be low detail, medium detail, or highly detailed.")
    shading = request_value(tool, request, "shading")
    if shading is not None and shading not in {
        "flat shading",
        "basic shading",
        "medium shading",
        "detailed shading",
        "highly detailed shading",
    }:
        raise SystemExit("shading is not a recognized PixelLab MCP shading value.")
    outline = request_value(tool, request, "outline")
    if outline is not None and outline not in {"single color outline", "selective outline", "lineless"}:
        raise SystemExit("outline must be single color outline, selective outline, or lineless.")
    return warnings


def transition_pixels(tool: str, request: dict[str, Any], tile_height: int) -> int:
    raw = float(request_value(tool, request, "transition_size"))
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
    sheet = Image.new("RGBA", (tile_width * 4, tile_height * 4), COLORS["preview_background"])
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


def description_color(description: str, fallback: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    text = description.lower()
    for token, color in KEYWORD_COLORS:
        if token in text:
            return color
    return fallback


def lighten(color: tuple[int, int, int, int], amount: int = 36) -> tuple[int, int, int, int]:
    return (min(255, color[0] + amount), min(255, color[1] + amount), min(255, color[2] + amount), color[3])


def texture_pixel(description: str, x: int, y: int, base: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    text = description.lower()
    if "1-bit" in text or "one-bit" in text:
        if "sparse" in text and ((x * 11 + y * 7) % 29 == 0):
            return (255, 255, 255, 255) if base[:3] == (0, 0, 0) else (0, 0, 0, 255)
        return base
    if any(word in text for word in ("speckle", "sparse", "broken", "noise")) and ((x * 13 + y * 5) % 23 == 0):
        return lighten(base, 60)
    if any(word in text for word in ("stripe", "line", "horizontal")) and y % 5 == 0:
        return lighten(base, 52)
    if "dither" in text and ((x + y) % 2 == 0):
        return lighten(base, 44)
    return base


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
                    if nx < 0 or ny < 0 or nx >= width or ny >= height:
                        continue
                    if not pixels[nx, ny]:
                        found_empty_neighbor = True
                        break
                if found_empty_neighbor:
                    break
            out[x, y] = 1 if found_empty_neighbor else 0
    return boundary


def draw_tileset(
    tool: str,
    request: dict[str, Any],
    tile_width: int,
    tile_height: int,
    draw_grid: bool,
    tiles: list[tuple[str, dict[str, str], int]],
    template_sheet: Image.Image | None = None,
) -> Image.Image:
    background = COLORS["transparent"] if tool == "create_sidescroller_tileset" else COLORS["preview_background"]
    sheet = Image.new("RGBA", (tile_width * 4, tile_height * 4), background)
    draw = ImageDraw.Draw(sheet)
    thickness = transition_pixels(tool, request, tile_height)
    lower_color = description_color(str(request.get("lower_description", "")), (50, 50, 54, 255))
    upper_color = description_color(str(request.get("upper_description", "")), (184, 184, 188, 255))
    transition_color = description_color(str(request.get("transition_description") or ""), lighten(lower_color, 76))

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
                terrain = terrain_at(corners, x, y, tile_width, tile_height)
                if tool == "create_topdown_tileset":
                    description_field = "lower_description" if terrain == LOWER else "upper_description"
                    base = lower_color if terrain == LOWER else upper_color
                    color = texture_pixel(str(request.get(description_field, "")), x, y, base)
                    if edge_mask.getpixel((x, y)):
                        color = texture_pixel(str(request.get("transition_description") or ""), x, y, transition_color)
                    sheet.putpixel((ox + x, oy + y), color)
                elif lower_mask.getpixel((x, y)):
                    if thickness and y < thickness:
                        color = texture_pixel(str(request.get("transition_description") or ""), x, y, transition_color)
                    else:
                        color = texture_pixel(str(request.get("lower_description", "")), x, y, lower_color)
                    sheet.putpixel((ox + x, oy + y), color)
        if draw_grid:
            draw.rectangle((ox, oy, ox + tile_width - 1, oy + tile_height - 1), outline=COLORS["grid"])
    return sheet


def compose_export_sheet(
    native_sheet: Image.Image,
    layout: str,
    tile_width: int,
    tile_height: int,
    draw_grid: bool,
) -> Image.Image:
    spec = EXPORT_LAYOUTS[layout]
    out = Image.new(
        "RGBA",
        (spec["columns"] * tile_width, spec["rows"] * tile_height),
        COLORS["transparent"],
    )
    for index, source_index in enumerate(spec["cells"]):
        sx = (source_index % 4) * tile_width
        sy = (source_index // 4) * tile_height
        dx = (index % spec["columns"]) * tile_width
        dy = (index // spec["columns"]) * tile_height
        out.alpha_composite(native_sheet.crop((sx, sy, sx + tile_width, sy + tile_height)), (dx, dy))
    if draw_grid:
        draw = ImageDraw.Draw(out)
        for row in range(spec["rows"]):
            for col in range(spec["columns"]):
                x = col * tile_width
                y = row * tile_height
                draw.rectangle((x, y, x + tile_width - 1, y + tile_height - 1), outline=COLORS["grid"])
    return out


def save_scaled(image: Image.Image, path: Path, scale: int) -> None:
    image.save(path)
    if scale > 1:
        scaled = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        scaled.save(path.with_name(path.stem + f"-x{scale}" + path.suffix))


def stable_id(prefix: str, payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    digest = hashlib.sha1(encoded).hexdigest()
    return f"sim-{prefix}-{digest[:12]}"


def tile_records(
    tile_width: int,
    tile_height: int,
    tiles: list[tuple[str, dict[str, str], int]],
) -> list[dict[str, Any]]:
    return [
        {
            "id": stable_id("tile", {"name": name, "layout": "15-tileset", "bitmask": bitmask}),
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
            "bit_order": ", ".join(f"{corner}={weight}" for corner, weight in PIXELLAB_BIT_ORDER),
        }
        for index, (name, corners, bitmask) in enumerate(tiles)
    ]


def export_cell_records(
    layout: str,
    tile_width: int,
    tile_height: int,
    tiles: list[tuple[str, dict[str, str], int]],
) -> list[dict[str, Any]]:
    spec = EXPORT_LAYOUTS[layout]
    return [
        {
            "export_col": index % spec["columns"],
            "export_row": index // spec["columns"],
            "source_native_index": source_index,
            "source_tile_name": tiles[source_index][0],
            "bounding_box": {
                "x": (index % spec["columns"]) * tile_width,
                "y": (index // spec["columns"]) * tile_height,
                "width": tile_width,
                "height": tile_height,
            },
        }
        for index, source_index in enumerate(spec["cells"])
    ]


def build_report(
    tool: str,
    request: dict[str, Any],
    warnings: list[str],
    tile_width: int,
    tile_height: int,
    layout: str,
    tiles: list[tuple[str, dict[str, str], int]],
    output_files: dict[str, Path],
    sim_run_id: str,
) -> dict[str, Any]:
    spec = EXPORT_LAYOUTS[layout]
    return {
        "source": "PixelLab MCP tileset simulator",
        "tool": tool,
        "sim_run_id": sim_run_id,
        "renderer": "deterministic",
        "limits": [
            "This simulates PixelLab MCP request shape and compact tileset layout locally.",
            "It writes local PNG layout previews and does not attempt to reproduce PixelLab MCP create/get JSON.",
            "The deterministic renderer uses simple keyword/semantic colors and does not predict PixelLab's model taste.",
            "expected_pattern_4x4 is derived from corners; observed PixelLab metadata often disagrees across surfaces.",
            "Boundary preview is per-tile schematic and does not model cross-tile seam continuity.",
            "Template alpha masks count any opaque pixel as occupied, including upper/detail pixels.",
            "When template_sheet is used, fill masks are copied from that observed PixelLab output.",
            "Expanded top-down sheets are not simulated.",
        ],
        "warnings": warnings,
        "request": request,
        "mcp_defaults_used_for_omitted_fields": {
            key: value
            for key, value in MCP_TOOLS[tool]["defaults"].items()
            if key not in request
        },
        "output_files": {key: str(path) for key, path in output_files.items()},
        "terrain_encoding": {LOWER: 0, UPPER: 1, "wildcard": WILDCARD},
        "sheet_layout": {
            "columns": spec["columns"],
            "rows": spec["rows"],
            "layout": layout,
            "filled_bit": PIXELLAB_FILLED_BIT,
            "native_tile_order": PIXELLAB_TILE_ORDER,
            "export_cell_sources": spec["cells"],
            "bit_weights": {corner: weight for corner, weight in PIXELLAB_BIT_ORDER},
            "note": "bit_weights describe the tile key; filled_bit controls which key value maps to lower terrain.",
        },
        "native_tiles": tile_records(tile_width, tile_height, tiles),
        "export_cells": export_cell_records(layout, tile_width, tile_height, tiles),
    }


def self_check() -> None:
    assert bitmask_to_corners(13, PIXELLAB_FILLED_BIT, PIXELLAB_BIT_ORDER) == {
        "NW": UPPER,
        "NE": UPPER,
        "SW": LOWER,
        "SE": UPPER,
    }
    assert bitmask_to_corners(0, PIXELLAB_FILLED_BIT, PIXELLAB_BIT_ORDER) == {
        "NW": LOWER,
        "NE": LOWER,
        "SW": LOWER,
        "SE": LOWER,
    }
    for layout, spec in EXPORT_LAYOUTS.items():
        assert len(spec["cells"]) == spec["columns"] * spec["rows"], layout


def main() -> None:
    self_check()
    args = parse_args()
    if args.scale < 1:
        raise SystemExit("--scale must be at least 1.")
    request = load_request(args.request_json)
    tile_width, tile_height = tile_size_from_request(args.tool, request)
    warnings = validate_request(
        args.tool,
        request,
        tile_width,
        tile_height,
    )
    tiles = make_tiles()

    output_dir = output_dir_from_name(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_files = {
        "corner_preview": output_dir / "corner-key-preview.png",
        "tileset": output_dir / "tileset.png",
        "sim_report": output_dir / "sim-report.json",
    }

    template_sheet = None
    if args.template_sheet:
        template_sheet = Image.open(args.template_sheet).convert("RGBA")
        expected_size = (tile_width * 4, tile_height * 4)
        if template_sheet.size != expected_size:
            raise SystemExit(f"Template sheet must be {expected_size[0]}x{expected_size[1]}, got {template_sheet.size}.")

    corner = draw_corner_preview(tile_width, tile_height, args.draw_grid, tiles)
    native_tileset = draw_tileset(args.tool, request, tile_width, tile_height, False, tiles, template_sheet)
    tileset = compose_export_sheet(native_tileset, args.layout, tile_width, tile_height, args.draw_grid)

    save_scaled(corner, output_files["corner_preview"], args.scale)
    save_scaled(tileset, output_files["tileset"], args.scale)

    sim_run_id = stable_id(
        "run",
        {"tool": args.tool, "request": request, "layout": args.layout, "output": str(output_dir)},
    )
    sim_report = build_report(
        args.tool,
        request,
        warnings,
        tile_width,
        tile_height,
        args.layout,
        tiles,
        output_files,
        sim_run_id,
    )
    if args.template_sheet:
        sim_report["template_sheet"] = str(args.template_sheet)
    with output_files["sim_report"].open("w", encoding="utf-8") as handle:
        json.dump(sim_report, handle, indent=2)

    print(f"Wrote {output_files['corner_preview']}")
    print(f"Wrote {output_files['tileset']}")
    print(f"Wrote {output_files['sim_report']}")


if __name__ == "__main__":
    main()
