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
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
# 16px sidescroller sheet. Values are source positions in the native 4x4
# 15-tileset sheet, not wang bitmask values.
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
        "transition_range": (0.0, 1.0),
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
            "seed",
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
            "seed": None,
            "spread_x": 0.5,
            "slope_size": 0.0,
            "raggedness": 0.0,
        },
        "tile_sizes": {(16, 16), (32, 32), (64, 64)},
        "transition_range": (0.0, 1.0),
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
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
RECIPE_TEXTURES = {"solid", "sparse", "broken", "speckle", "dither", "stripe", "none"}
RECIPE_PLACEMENTS = {"all", "auto", "boundary", "interior", "none", "top"}
OPENCODE_RENDERER_MODELS = {
    "deepseek-v4-pro": "deepseek/deepseek-v4-pro",
}
RECIPE_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "lower", "upper", "transition"],
    "properties": {
        "summary": {"type": "string"},
        "lower": {"$ref": "#/$defs/terrain"},
        "upper": {"$ref": "#/$defs/terrain"},
        "transition": {
            "type": "object",
            "additionalProperties": False,
            "required": ["label", "color", "accent_color", "texture", "placement"],
            "properties": {
                "label": {"type": "string"},
                "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                "accent_color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                "texture": {"type": "string", "enum": sorted(RECIPE_TEXTURES)},
                "placement": {"type": "string", "enum": sorted(RECIPE_PLACEMENTS)},
            },
        },
    },
    "$defs": {
        "terrain": {
            "type": "object",
            "additionalProperties": False,
            "required": ["label", "color", "accent_color", "texture", "placement"],
            "properties": {
                "label": {"type": "string"},
                "color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                "accent_color": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                "texture": {"type": "string", "enum": sorted(RECIPE_TEXTURES)},
                "placement": {"type": "string", "enum": sorted(RECIPE_PLACEMENTS)},
            },
        }
    },
}


def recipe_json_schema(tool: str) -> dict[str, Any]:
    schema = json.loads(json.dumps(RECIPE_JSON_SCHEMA))
    if tool == "create_sidescroller_tileset":
        schema["required"] = ["summary", "lower", "transition"]
        schema["properties"].pop("upper", None)
    return schema
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
            "Render local PNG previews from PixelLab MCP create_topdown_tileset "
            "or create_sidescroller_tileset JSON."
        ),
        epilog=(
            "Agent pattern:\n"
            "  Pass MCP JSON by stdin or file.\n"
            "  Inspect tileset.png, components/*.png, and sim-report.json under "
            ".local/mcp-tileset-sim-output/<output>.\n\n"
            "Examples:\n"
            "  '{\"lower_description\":\"stone brick\",\"transition_description\":\"moss\",\"transition_size\":0.25}' "
            "| python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset --output attempt-a\n"
            "  '{\"lower_description\":\"ocean\",\"upper_description\":\"sand\",\"transition_description\":\"foam\",\"transition_size\":0.25}' "
            "| python dev-tools/pixellab_mcp_tileset_sim.py create_topdown_tileset --layout wang --output attempt-b"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
        choices=["deterministic", "codex", "claude", *sorted(OPENCODE_RENDERER_MODELS)],
        default="deterministic",
        help="Renderer backend. AI renderers create a constrained semantic recipe before local rendering.",
    )
    parser.add_argument(
        "--agent-timeout",
        type=int,
        default=180,
        help="Timeout in seconds for AI renderers.",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=8,
        help="Nearest-neighbor scale for enlarged preview PNGs.",
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
        try:
            raw = request_json.read_text(encoding="utf-8")
        except OSError as exc:
            raise SystemExit(f"Could not read request JSON file: {request_json}") from exc
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Request JSON is invalid: {exc.msg} at line {exc.lineno}, column {exc.colno}.") from exc
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
    min_transition, max_transition = config["transition_range"]
    if raw_transition < min_transition or raw_transition > max_transition:
        raise SystemExit(f"{tool} transition_size must be between {min_transition} and {max_transition}.")
    if raw_transition not in {0.0, 0.25, 0.5, 1.0}:
        warnings.append(
            f"{tool} transition_size {raw_transition} is not one of PixelLab's documented guidepost values; "
            "the compact renderer uses the numeric value directly."
        )
    if tool == "create_topdown_tileset" and raw_transition >= 1.0:
        raise SystemExit(
            "This is a valid top-down tileset request shape, but transition_size 1.0 can export an expanded "
            "23-tile/4x8-style sheet that this compact simulator does not render."
        )
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
                raise SystemExit(
                    "This is a valid top-down Pro request shape, but observed PixelLab Pro outputs can expand at "
                    "transition_size 0.5. This compact simulator only renders Pro requests below 0.5."
                )
            warnings.append("Top-down pro mode below transition_size 0.5 is approximated with the compact deterministic renderer.")
        if raw_transition > 0 and not str(request_value(tool, request, "transition_description") or "").strip():
            warnings.append("Top-down transition_size > 0 normally needs a transition_description for meaningful output.")

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
    if outline is not None and outline not in {"single color black outline", "single color outline", "selective outline", "lineless"}:
        raise SystemExit("outline must be single color black outline, single color outline, selective outline, or lineless.")
    return warnings


def transition_pixels(tool: str, request: dict[str, Any], tile_height: int) -> int:
    raw = float(request_value(tool, request, "transition_size"))
    min_transition, max_transition = MCP_TOOLS[tool]["transition_range"]
    if raw < min_transition or raw > max_transition:
        raise SystemExit("transition_size is invalid for this MCP tool.")
    return max(1, round(tile_height * raw)) if raw > 0 else 0


def effective_transition_pixels(tool: str, request: dict[str, Any], tile_height: int) -> int:
    pixels = transition_pixels(tool, request, tile_height)
    text = str(request.get("transition_description") or "").lower()
    if re.search(r"\b(outline|border|rim)\b", text) and not re.search(
        r"\b(cap|surface|grass|snow|moss|dirt|wall face)\b",
        text,
    ):
        return min(pixels, max(1, tile_height // 8))
    return pixels


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


def transition_description_color(
    description: str,
    fallback: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    text = description.lower()
    outline_words = list(re.finditer(r"\b(border|outline|edge)\b", text))
    color_words = list(re.finditer(r"\b(black|white)\b", text))
    candidates: list[tuple[int, str]] = []
    for outline_word in outline_words:
        for color_word in color_words:
            distance = min(abs(outline_word.start() - color_word.end()), abs(color_word.start() - outline_word.end()))
            if distance <= 32:
                candidates.append((distance, color_word.group(1)))
    if candidates:
        color_name = min(candidates, key=lambda candidate: candidate[0])[1]
        return (255, 255, 255, 255) if color_name == "white" else (0, 0, 0, 255)
    return description_color(description, fallback)


def detail_pixel_base_color(
    description: str,
    terrain_base: tuple[int, int, int, int],
    parsed_base: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    text = description.lower()
    if re.search(r"\b(sparse|broken|speckle|fleck|chip|crack|highlight|pixel)\w*\b", text):
        if re.search(r"\b(?:(?:pure|single|tiny|small|isolated)\s+)*white\s+(?:(?:pure|single|tiny|small|isolated)\s+)*(?:pixel|pixels|speckle|speckles|fleck|flecks|chip|chips|crack|cracks|highlight|highlights)", text):
            return terrain_base
        if re.search(r"\b(?:(?:pure|single|tiny|small|isolated)\s+)*black\s+(?:(?:pure|single|tiny|small|isolated)\s+)*(?:pixel|pixels|speckle|speckles|fleck|flecks|chip|chips|crack|cracks|highlight|highlights)", text):
            return terrain_base
    return parsed_base


def color_from_hex(value: Any) -> tuple[int, int, int, int] | None:
    if not isinstance(value, str) or not HEX_COLOR.match(value):
        return None
    return (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16), 255)


def section_from_recipe(recipe: dict[str, Any] | None, name: str) -> dict[str, Any]:
    if not recipe:
        return {}
    value = recipe.get(name)
    return value if isinstance(value, dict) else {}


def recipe_color(
    recipe: dict[str, Any] | None,
    section: str,
    key: str,
    fallback: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    parsed = color_from_hex(section_from_recipe(recipe, section).get(key))
    return parsed or fallback


def lighten(color: tuple[int, int, int, int], amount: int = 36) -> tuple[int, int, int, int]:
    return (min(255, color[0] + amount), min(255, color[1] + amount), min(255, color[2] + amount), color[3])


def texture_pixel(
    description: str,
    x: int,
    y: int,
    base: tuple[int, int, int, int],
    recipe_section: dict[str, Any] | None = None,
    allow_texture: bool = True,
    tile_width: int | None = None,
    tile_height: int | None = None,
) -> tuple[int, int, int, int]:
    text = description.lower()
    recipe_section = recipe_section or {}
    recipe_texture = str(recipe_section.get("texture", "")).lower()
    sparse_mod = 53 if re.search(r"\b(extremely sparse|isolated|single[- ]?pixel|tiny|small|minimal|few)\b", text) else 37 if "sparse" in text else 23
    accent = color_from_hex(recipe_section.get("accent_color")) or lighten(base, 60)
    if re.search(r"\b(?:(?:pure|single|tiny|small|isolated)\s+)*white\s+(?:(?:pure|single|tiny|small|isolated)\s+)*(?:pixel|pixels|speckle|speckles|fleck|flecks|chip|chips|crack|cracks|highlight|highlights)", text):
        accent = (255, 255, 255, 255)
    elif re.search(r"\b(?:(?:pure|single|tiny|small|isolated)\s+)*black\s+(?:(?:pure|single|tiny|small|isolated)\s+)*(?:pixel|pixels|speckle|speckles|fleck|flecks|chip|chips|crack|cracks|highlight|highlights)", text):
        accent = (0, 0, 0, 255)
    if re.search(r"\b(tile[- ]?border|border grid|tile grid|grid)\b", text):
        right = tile_width - 1 if tile_width else x
        bottom = tile_height - 1 if tile_height else y
        if x in {0, right} or y in {0, bottom}:
            return accent
    if not allow_texture:
        return base
    if recipe_texture == "none":
        return base
    if recipe_texture in {"sparse", "broken", "speckle"} and ((x * 13 + y * 5) % sparse_mod == 0):
        return accent
    if recipe_texture == "stripe" and y % 5 == 0:
        return accent
    if recipe_texture == "dither" and ((x + y) % 2 == 0):
        return accent
    if "1-bit" in text or "one-bit" in text:
        if "sparse" in text and ((x * 11 + y * 7) % (sparse_mod + 6) == 0):
            return (255, 255, 255, 255) if base[:3] == (0, 0, 0) else (0, 0, 0, 255)
        return base
    if re.search(r"\b(speckle|sparse|broken|noise)\b", text) and ((x * 13 + y * 5) % sparse_mod == 0):
        return accent
    if re.search(r"\b(stripe|stripes|line|lines|horizontal)\b", text) and y % 5 == 0:
        return accent
    if re.search(r"\bdither(?:ed|ing)?\b", text) and ((x + y) % 2 == 0):
        return accent
    return base


def description_placement(tool: str, section: str, description: str) -> str:
    text = description.lower()
    if re.search(r"\b(no texture|no decoration|no detail|solid|flat|empty)\b", text):
        if not re.search(r"\b(edge|border|outline|rim|contour|highlight|speckle|fleck|chip|crack|dither|stripe|grid)\b", text):
            return "none"
    if re.search(r"\b(edge|border|outline|rim|contour|edge-highlight|edge highlight)\b", text):
        return "boundary"
    if tool == "create_sidescroller_tileset" and re.search(r"\b(top|cap|surface|upper|grass|snow|moss)\b", text):
        return "top"
    if re.search(r"\b(interior|inside|center|middle)\b", text):
        return "interior"
    if re.search(r"\b(speckle|fleck|chip|crack|dither|stripe|grid|texture|highlight|line)\b", text):
        return "all"
    if section == "transition":
        return "top" if tool == "create_sidescroller_tileset" else "boundary"
    return "all"


def section_placement(
    tool: str,
    section: str,
    description: str,
    recipe_section: dict[str, Any] | None,
) -> str:
    text = description.lower()
    placement = str((recipe_section or {}).get("placement", "auto")).lower()
    if placement == "auto" or placement not in RECIPE_PLACEMENTS:
        return description_placement(tool, section, description)
    if (
        tool == "create_sidescroller_tileset"
        and section == "lower"
        and placement in {"all", "boundary", "interior"}
        and re.search(r"\b(sparse|speckle|fleck|chip|crack|highlight)\b", text)
        and not re.search(r"\b(interior|inside|center|middle)\b", text)
    ):
        if re.search(r"\b(side|vertical|end[- ]?cap|outside|edge|border|outline|rim)\b", text):
            return "boundary"
        return "top"
    return placement


def placement_allows_texture(
    placement: str,
    x: int,
    y: int,
    tile_width: int,
    tile_height: int,
    thickness: int,
    edge_mask: Image.Image,
    top_mask: Image.Image | None = None,
) -> bool:
    if placement == "none":
        return False
    if placement in {"all", "auto"}:
        return True
    top_height = max(1, thickness or tile_height // 4)
    if placement == "top":
        if top_mask is not None:
            return bool(top_mask.getpixel((x, y)))
        return y < top_height
    is_boundary = bool(edge_mask.getpixel((x, y)))
    if placement == "boundary":
        return is_boundary
    if placement == "interior":
        return not is_boundary and y >= top_height
    return True


def agent_recipe_prompt(tool: str, request: dict[str, Any], tile_width: int, tile_height: int) -> str:
    upper_line = (
        '  "upper": {"label": "upper/background terrain", "color": "#RRGGBB", '
        '"accent_color": "#RRGGBB", "texture": "solid|sparse|broken|speckle|dither|stripe|none", "placement": "auto|all|top|boundary|interior|none"},\n'
        if tool == "create_topdown_tileset"
        else ""
    )
    return (
        "You are helping a local PixelLab MCP tileset simulator interpret descriptions. "
        "Return JSON only, with no Markdown. Do not draw pixels and do not call tools. "
        "Your job is to choose a compact semantic rendering recipe; the simulator will "
        "handle DualGrid math, masks, and export layout composition.\n\n"
        "Schema:\n"
        "{\n"
        '  "summary": "short plain-English interpretation",\n'
        '  "lower": {"label": "terrain/platform body", "color": "#RRGGBB", "accent_color": "#RRGGBB", "texture": "solid|sparse|broken|speckle|dither|stripe|none", "placement": "auto|all|top|boundary|interior|none"},\n'
        f"{upper_line}"
        '  "transition": {"label": "edge/top transition", "color": "#RRGGBB", "accent_color": "#RRGGBB", "texture": "solid|sparse|broken|speckle|dither|stripe|none", "placement": "auto|all|top|boundary|interior|none"}\n'
        "}\n\n"
        "Rules:\n"
        "- Use only valid #RRGGBB colors.\n"
        "- For 1-bit or monochrome prompts, prefer only #000000 and #FFFFFF.\n"
        "- For sidescroller requests, lower is the platform body and transition is the top/surface layer.\n"
        "- For top-down requests, lower and upper are the two terrain classes and transition is their boundary style.\n"
        "- The input descriptions are inside lower_description, upper_description, and transition_description.\n"
        "- placement controls where accent/detail pixels appear; use boundary for edge/rim/outline wording, top for sidescroller caps/surface, none for solid/no texture.\n"
        "- Never return an error object; always infer the best recipe from the JSON fields provided.\n"
        "- Do not include keys outside the schema.\n\n"
        f"Tool: {tool}\n"
        f"Tile size: {tile_width}x{tile_height}\n"
        f"MCP request JSON:\n{json.dumps(request, indent=2, sort_keys=True)}\n"
    )


def opencode_agent_recipe_prompt(tool: str, request: dict[str, Any], tile_width: int, tile_height: int) -> str:
    required_sections = "summary, lower, transition"
    upper_shape = ""
    topdown_rule = ""
    if tool == "create_topdown_tileset":
        required_sections = "summary, lower, upper, transition"
        upper_shape = (
            ', "upper": {"label": "short label", "color": "#RRGGBB", '
            '"accent_color": "#RRGGBB", "texture": "solid", "placement": "all"}'
        )
        topdown_rule = "For top-down, lower and upper are terrain classes; transition is their boundary style. "
    return (
        "Output raw JSON only. Your entire response must be a single JSON object. "
        "No markdown, no code fence, no explanation. "
        f"Interpret this PixelLab MCP request for {tool}. "
        f"Required top-level keys: {required_sections}. "
        "Do not include any other keys, including size, transition_size, confidence, notes, or errors. "
        "Each terrain section has exactly label, color, accent_color, texture, placement. "
        "The transition section has exactly label, color, accent_color, texture, placement. "
        "Valid textures are exactly: solid, sparse, broken, speckle, dither, stripe, none. "
        "Valid placements are exactly: all, auto, boundary, interior, none, top. "
        "placement controls where accent/detail pixels appear; use boundary for edge/rim/outline wording, top for sidescroller caps/surface, none for solid/no texture. "
        "Use valid #RRGGBB colors. For 1-bit or monochrome prompts, use only #000000 and #FFFFFF. "
        "For sidescroller, lower is the platform body and transition is the top/surface layer. "
        f"{topdown_rule}"
        "Return this exact object shape with inferred values: "
        '{"summary":"short interpretation", '
        '"lower":{"label":"short label","color":"#RRGGBB","accent_color":"#RRGGBB","texture":"solid","placement":"all"}'
        f"{upper_shape}, "
        '"transition":{"label":"short label","color":"#RRGGBB","accent_color":"#RRGGBB","texture":"solid","placement":"auto"}}. '
        f"Tile size: {tile_width}x{tile_height}. "
        f"MCP request JSON: {json.dumps(request, sort_keys=True)}"
    )


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    fence_match = re.fullmatch(r"```(?:json)?\s*(\{.*\})\s*```", stripped, flags=re.IGNORECASE | re.DOTALL)
    if fence_match:
        stripped = fence_match.group(1).strip()
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError as exc:
        excerpt = stripped[:500]
        raise SystemExit(f"AI renderer did not return exactly one JSON object: {exc.msg}. Output excerpt: {excerpt}") from exc
    if not isinstance(data, dict):
        raise SystemExit("AI renderer JSON must be an object.")
    return data


def opencode_text_from_jsonl(stdout: str) -> str:
    chunks: list[str] = []
    saw_jsonl_event = False
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        saw_jsonl_event = True
        part = event.get("part")
        if event.get("type") == "text" and isinstance(part, dict) and isinstance(part.get("text"), str):
            chunks.append(part["text"])
    if chunks:
        return "".join(chunks).strip()
    if saw_jsonl_event:
        raise SystemExit("OpenCode renderer returned JSONL events but no text response.")
    return stdout.strip()


def require_hex(value: Any, field: str, renderer: str) -> str:
    if not isinstance(value, str) or not HEX_COLOR.match(value):
        raise SystemExit(f"--renderer {renderer} returned invalid {field}; expected #RRGGBB.")
    return value.upper()


def validate_ai_recipe(data: dict[str, Any], renderer: str, tool: str) -> dict[str, Any]:
    allowed_top = {"summary", "lower", "transition"}
    if tool == "create_topdown_tileset":
        allowed_top.add("upper")
    unknown_top = sorted(set(data) - allowed_top)
    if unknown_top:
        raise SystemExit(f"--renderer {renderer} returned unknown recipe fields: {', '.join(unknown_top)}.")
    recipe: dict[str, Any] = {
        "renderer": renderer,
        "summary": str(data.get("summary", ""))[:500],
        "raw": data,
    }
    section_names = ("lower", "upper", "transition") if tool == "create_topdown_tileset" else ("lower", "transition")
    for section_name in section_names:
        section_in = data.get(section_name)
        section_out: dict[str, Any] = {}
        if not isinstance(section_in, dict):
            raise SystemExit(f"--renderer {renderer} returned missing or invalid {section_name} section.")
        allowed_section = {"label", "color", "accent_color", "texture", "placement"}
        unknown_section = sorted(set(section_in) - allowed_section)
        if unknown_section:
            raise SystemExit(
                f"--renderer {renderer} returned unknown {section_name} fields: {', '.join(unknown_section)}."
            )
        section_out["label"] = str(section_in.get("label", section_name))[:120]
        section_out["color"] = require_hex(section_in.get("color"), f"{section_name}.color", renderer)
        section_out["accent_color"] = require_hex(section_in.get("accent_color"), f"{section_name}.accent_color", renderer)
        texture = str(section_in.get("texture", "")).lower()
        if texture not in RECIPE_TEXTURES:
            raise SystemExit(f"--renderer {renderer} returned invalid {section_name}.texture: {texture}.")
        section_out["texture"] = texture
        placement = str(section_in.get("placement", "auto")).lower()
        if placement not in RECIPE_PLACEMENTS:
            raise SystemExit(f"--renderer {renderer} returned invalid {section_name}.placement: {placement}.")
        section_out["placement"] = placement
        recipe[section_name] = section_out
    required_sections = ("lower", "transition") if tool == "create_sidescroller_tileset" else ("lower", "upper")
    missing = [section for section in required_sections if "color" not in recipe[section]]
    if missing:
        raise SystemExit(f"--renderer {renderer} returned an incomplete recipe; missing colors for: {', '.join(missing)}.")
    return recipe


def text_prefers_black_base_with_white_detail(description: str) -> bool:
    text = description.lower()
    has_bw_palette = re.search(r"\b(1-bit|one-bit|monochrome|black[- ]and[- ]white|black and white|black/white)\b", text)
    has_white_detail = re.search(
        r"\bwhite\s+(?:(?:dirt|soil|stone|brick|rock|dust|tiny|small|isolated|single[- ]?pixel|speckled|stippled)\s+)*(?:pixel|pixels|speckle|speckles|speckled|fleck|flecks|chip|chips|grain|grains|crack|cracks|line|lines|stipple|stippled|texture|details?)\b",
        text,
    )
    has_dark_material = re.search(r"\bblack|dark|dungeon|wall|floor|dirt|soil|stone|brick|rock|cave\b", text)
    explicit_white_base = re.search(
        r"\b(?:pure|solid|flat|mostly|all|entire|filled|base|terrain|surface)\s+white\b|\bwhite\s+(?:(?:dirt|soil|stone|brick|rock|grass)\s+)?(?:terrain|surface|base|fill|floor|wall)\b",
        text,
    )
    return bool(has_bw_palette and has_white_detail and has_dark_material and not explicit_white_base)


def text_is_unsupported_topdown_wall_face_stripes(description: str) -> bool:
    text = description.lower()
    mentions_wall_face = re.search(r"\b(front face|wall front|vertical wall face|wall face)\b", text)
    mentions_thin_horizontal_lines = re.search(r"\b(horizontal|repeated|thin)\b.*\b(line|lines|stripe|stripes)\b|\b(line|lines|stripe|stripes)\b.*\b(horizontal|repeated|thin)\b", text)
    mentions_1bit_bw = re.search(r"\b(1-bit|one-bit|black and white|black[- ]and[- ]white|monochrome)\b", text)
    return bool(mentions_wall_face and mentions_thin_horizontal_lines and mentions_1bit_bw)


def text_is_topdown_black_texture_that_live_dulls(description: str) -> bool:
    text = description.lower()
    if re.search(r"\b(crack|cracks|scratch|scratches|highlight|highlights)\b", text):
        return False
    has_black_surface = re.search(r"\bblack|dark|dungeon|wall|floor|terrain|surface|transition\b", text)
    has_sparse_white_detail = re.search(
        r"\b(sparse|speckle|speckled|fleck|flecks|stipple|stippled|dust|chipped|isolated|single[- ]?pixel|tiny|small|minimal)\b.*\bwhite\b|\bwhite\b.*\b(sparse|speckle|speckled|fleck|flecks|stipple|stippled|dust|chipped|isolated|single[- ]?pixel|tiny|small|minimal)\b",
        text,
    )
    has_outline_intent = re.search(r"\b(edge|outline|rim|border|contour|edge-highlight|edge highlight|outside)\b", text)
    explicit_white_base = re.search(
        r"\b(?:pure|solid|flat|mostly|all|entire|filled|base|terrain|surface)\s+white\b|\bwhite\s+(?:(?:dirt|soil|stone|brick|rock|grass)\s+)?(?:terrain|surface|base|fill|floor|wall)\b",
        text,
    )
    return bool(has_black_surface and has_sparse_white_detail and not has_outline_intent and not explicit_white_base)


def text_is_unspecified_bw_topdown_edge(description: str) -> bool:
    text = description.lower()
    has_bw_edge = re.search(r"\b(1-bit|one-bit|monochrome|black and white|black[- ]and[- ]white)\b", text) and re.search(r"\bedge\b", text)
    return bool(has_bw_edge and not text_has_explicit_white_edge(description))


def text_has_explicit_white_edge(description: str) -> bool:
    text = description.lower()
    return bool(
        re.search(
            r"\bwhite\s+(?:(?:pixel|pixels|sparse|clean|crisp)\s+)*(?:edge|outline|rim|border|highlight|highlights|line|lines)\b|\b(?:edge|outline|rim|border|highlight|highlights|line|lines)\s+white\b",
            text,
        )
    )


def normalize_ai_recipe_for_request(recipe: dict[str, Any], tool: str, request: dict[str, Any]) -> dict[str, Any]:
    section_fields = {
        "lower": "lower_description",
        "transition": "transition_description",
    }
    if tool == "create_topdown_tileset":
        section_fields["upper"] = "upper_description"
    for section, field in section_fields.items():
        section_recipe = recipe.get(section)
        if not isinstance(section_recipe, dict):
            continue
        description = str(request.get(field) or "")
        if tool == "create_topdown_tileset" and text_is_unsupported_topdown_wall_face_stripes(description):
            section_recipe["color"] = "#000000"
            section_recipe["accent_color"] = "#000000"
            section_recipe["texture"] = "none"
            section_recipe["placement"] = "none"
            continue
        if tool == "create_topdown_tileset" and section == "transition" and text_has_explicit_white_edge(description):
            section_recipe["color"] = "#FFFFFF"
            section_recipe["accent_color"] = "#FFFFFF"
            section_recipe["texture"] = "solid"
            section_recipe["placement"] = "boundary"
            continue
        if tool == "create_topdown_tileset" and text_is_topdown_black_texture_that_live_dulls(description):
            section_recipe["color"] = "#000000"
            section_recipe["accent_color"] = "#000000"
            section_recipe["texture"] = "none"
            section_recipe["placement"] = "none"
            continue
        if tool == "create_topdown_tileset" and section == "transition" and text_is_unspecified_bw_topdown_edge(description):
            section_recipe["color"] = "#000000"
            section_recipe["accent_color"] = "#000000"
            section_recipe["texture"] = "none"
            section_recipe["placement"] = "none"
            continue
        if text_prefers_black_base_with_white_detail(description):
            section_recipe["color"] = "#000000"
            section_recipe["accent_color"] = "#FFFFFF"
            if section_recipe.get("texture") == "solid":
                section_recipe["texture"] = "sparse"
    return recipe


def run_ai_renderer(
    renderer: str,
    tool: str,
    request: dict[str, Any],
    tile_width: int,
    tile_height: int,
    timeout: int,
) -> dict[str, Any] | None:
    if renderer == "deterministic":
        return None
    if timeout < 1:
        raise SystemExit("--agent-timeout must be at least 1 second.")

    executable_name = "opencode" if renderer in OPENCODE_RENDERER_MODELS else renderer
    executable = shutil.which(executable_name)
    if executable is None:
        raise SystemExit(f"--renderer {renderer} requires the {executable_name} CLI on PATH.")

    prompt = (
        opencode_agent_recipe_prompt(tool, request, tile_width, tile_height)
        if renderer in OPENCODE_RENDERER_MODELS
        else agent_recipe_prompt(tool, request, tile_width, tile_height)
    )
    if renderer == "codex":
        temp_dir = tempfile.TemporaryDirectory(prefix="pixellab-sim-codex-")
        schema_path = Path(temp_dir.name) / "recipe-schema.json"
        stdout_path = Path(temp_dir.name) / "last-message.json"
        schema_path.write_text(json.dumps(recipe_json_schema(tool)), encoding="utf-8")
        command = [
            executable,
            "exec",
            "--cd",
            os.getcwd(),
            "--sandbox",
            "read-only",
            "--ephemeral",
            "--ignore-rules",
            "--color",
            "never",
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(stdout_path),
            "-",
        ]
        stdin_text = prompt
    elif renderer == "claude":
        command = [
            executable,
            "-p",
            "--safe-mode",
            "--no-session-persistence",
            "--permission-mode",
            "dontAsk",
            "--tools=",
            "--json-schema",
            json.dumps(recipe_json_schema(tool)),
            prompt,
        ]
        stdout_path = None
        stdin_text = None
    elif renderer in OPENCODE_RENDERER_MODELS:
        command = [
            executable,
            "run",
            "--pure",
            "--model",
            OPENCODE_RENDERER_MODELS[renderer],
            "--format",
            "json",
            "--dir",
            os.getcwd(),
            prompt,
        ]
        stdout_path = None
        stdin_text = None
    else:  # pragma: no cover - argparse prevents this
        raise SystemExit(f"Unsupported renderer: {renderer}")

    try:
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                input=stdin_text,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raise SystemExit(f"--renderer {renderer} timed out after {timeout} seconds.") from exc
        if result.returncode != 0:
            stderr = result.stderr.strip()[-1200:]
            raise SystemExit(f"--renderer {renderer} failed with exit code {result.returncode}: {stderr}")
        if renderer in OPENCODE_RENDERER_MODELS:
            output_text = opencode_text_from_jsonl(result.stdout)
        else:
            output_text = stdout_path.read_text(encoding="utf-8") if stdout_path and stdout_path.exists() else result.stdout
        recipe = validate_ai_recipe(extract_json_object(output_text), renderer, tool)
        recipe = normalize_ai_recipe_for_request(recipe, tool, request)
        recipe["agent_stdout_excerpt"] = result.stdout.strip()[:2000]
        return recipe
    finally:
        if renderer == "codex":
            temp_dir.cleanup()


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


def top_surface_mask(lower_mask: Image.Image, thickness: int) -> Image.Image:
    if thickness <= 0:
        return Image.new("1", lower_mask.size, 0)
    width, height = lower_mask.size
    top = Image.new("1", lower_mask.size, 0)
    pixels = lower_mask.load()
    out = top.load()
    for x in range(width):
        first_filled = None
        for y in range(height):
            if pixels[x, y]:
                first_filled = y
                break
        if first_filled is None or first_filled == 0:
            continue
        for y in range(first_filled, min(height, first_filled + thickness)):
            if pixels[x, y]:
                out[x, y] = 1
    return top


def draw_tileset(
    tool: str,
    request: dict[str, Any],
    tile_width: int,
    tile_height: int,
    draw_grid: bool,
    tiles: list[tuple[str, dict[str, str], int]],
    template_sheet: Image.Image | None = None,
    render_recipe: dict[str, Any] | None = None,
) -> Image.Image:
    background = COLORS["transparent"] if tool == "create_sidescroller_tileset" else COLORS["preview_background"]
    sheet = Image.new("RGBA", (tile_width * 4, tile_height * 4), background)
    draw = ImageDraw.Draw(sheet)
    thickness = effective_transition_pixels(tool, request, tile_height)
    lower_color = recipe_color(
        render_recipe,
        "lower",
        "color",
        description_color(str(request.get("lower_description", "")), (50, 50, 54, 255)),
    )
    upper_color = recipe_color(
        render_recipe,
        "upper",
        "color",
        description_color(str(request.get("upper_description", "")), (184, 184, 188, 255)),
    )
    transition_color = recipe_color(
        render_recipe,
        "transition",
        "color",
        detail_pixel_base_color(
            str(request.get("transition_description") or ""),
            lower_color,
            transition_description_color(str(request.get("transition_description") or ""), lighten(lower_color, 76)),
        ),
    )
    lower_recipe = section_from_recipe(render_recipe, "lower")
    upper_recipe = section_from_recipe(render_recipe, "upper")
    transition_recipe = section_from_recipe(render_recipe, "transition")
    lower_description = str(request.get("lower_description", ""))
    upper_description = str(request.get("upper_description", ""))
    transition_description = str(request.get("transition_description") or "")
    lower_placement = section_placement(tool, "lower", lower_description, lower_recipe)
    upper_placement = section_placement(tool, "upper", upper_description, upper_recipe)
    transition_placement = section_placement(tool, "transition", transition_description, transition_recipe)

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
        exposed_top_mask = top_surface_mask(lower_mask, thickness) if tool == "create_sidescroller_tileset" else None
        for y in range(tile_height):
            for x in range(tile_width):
                terrain = terrain_at(corners, x, y, tile_width, tile_height)
                if tool == "create_topdown_tileset":
                    description_field = "lower_description" if terrain == LOWER else "upper_description"
                    base = lower_color if terrain == LOWER else upper_color
                    recipe_section = lower_recipe if terrain == LOWER else upper_recipe
                    description = lower_description if terrain == LOWER else upper_description
                    placement = lower_placement if terrain == LOWER else upper_placement
                    color = texture_pixel(
                        description,
                        x,
                        y,
                        base,
                        recipe_section,
                        placement_allows_texture(placement, x, y, tile_width, tile_height, thickness, edge_mask, exposed_top_mask),
                        tile_width,
                        tile_height,
                    )
                    if transition_placement != "none" and edge_mask.getpixel((x, y)):
                        color = texture_pixel(
                            transition_description,
                            x,
                            y,
                            transition_color,
                            transition_recipe,
                            placement_allows_texture(transition_placement, x, y, tile_width, tile_height, thickness, edge_mask, exposed_top_mask),
                            tile_width,
                            tile_height,
                        )
                    sheet.putpixel((ox + x, oy + y), color)
                elif lower_mask.getpixel((x, y)):
                    use_transition = (
                        transition_placement != "none"
                        and thickness
                        and (
                            bool(exposed_top_mask.getpixel((x, y)))
                            if transition_placement in {"auto", "top"} and exposed_top_mask is not None
                            else bool(edge_mask.getpixel((x, y)))
                        )
                    )
                    if use_transition:
                        color = texture_pixel(
                            transition_description,
                            x,
                            y,
                            transition_color,
                            transition_recipe,
                            placement_allows_texture(transition_placement, x, y, tile_width, tile_height, thickness, edge_mask, exposed_top_mask),
                            tile_width,
                            tile_height,
                        )
                    else:
                        color = texture_pixel(
                            lower_description,
                            x,
                            y,
                            lower_color,
                            lower_recipe,
                            placement_allows_texture(lower_placement, x, y, tile_width, tile_height, thickness, edge_mask, exposed_top_mask),
                            tile_width,
                            tile_height,
                        )
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


def draw_component_previews(
    tool: str,
    request: dict[str, Any],
    tile_width: int,
    tile_height: int,
    native_tileset: Image.Image,
    render_recipe: dict[str, Any] | None,
) -> dict[str, Image.Image]:
    lower_color = recipe_color(
        render_recipe,
        "lower",
        "color",
        description_color(str(request.get("lower_description", "")), (50, 50, 54, 255)),
    )
    upper_color = recipe_color(
        render_recipe,
        "upper",
        "color",
        description_color(str(request.get("upper_description", "")), (184, 184, 188, 255)),
    )
    transition_color = recipe_color(
        render_recipe,
        "transition",
        "color",
        detail_pixel_base_color(
            str(request.get("transition_description") or ""),
            lower_color,
            transition_description_color(str(request.get("transition_description") or ""), lighten(lower_color, 76)),
        ),
    )
    sections = {
        "component_lower": ("lower_description", lower_color, section_from_recipe(render_recipe, "lower")),
        "component_transition": ("transition_description", transition_color, section_from_recipe(render_recipe, "transition")),
    }
    if tool == "create_topdown_tileset":
        sections["component_upper"] = ("upper_description", upper_color, section_from_recipe(render_recipe, "upper"))
    previews: dict[str, Image.Image] = {}
    for key, (field, color, recipe_section) in sections.items():
        image = Image.new("RGBA", (tile_width, tile_height), COLORS["transparent"] if tool == "create_sidescroller_tileset" else COLORS["preview_background"])
        for y in range(tile_height):
            for x in range(tile_width):
                image.putpixel((x, y), texture_pixel(str(request.get(field) or ""), x, y, color, recipe_section, True, tile_width, tile_height))
        previews[key] = image

    center_index = PIXELLAB_TILE_ORDER.index(0)
    sx = (center_index % 4) * tile_width
    sy = (center_index // 4) * tile_height
    previews["component_center_tile"] = native_tileset.crop((sx, sy, sx + tile_width, sy + tile_height))
    return previews


def save_scaled(image: Image.Image, path: Path, scale: int) -> list[Path]:
    written = [path]
    image.save(path)
    if scale > 1:
        scaled = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        scaled_path = path.with_name(path.stem + f"-x{scale}" + path.suffix)
        scaled.save(scaled_path)
        written.append(scaled_path)
    return written


def remove_known_outputs(output_dir: Path) -> None:
    patterns = (
        "corner-key-preview*.png",
        "native-tileset*.png",
        "component-lower*.png",
        "component-upper*.png",
        "component-transition*.png",
        "component-center-tile*.png",
        "components/*.png",
        "tileset*.png",
        "sim-report.json",
    )
    if not output_dir.exists():
        return
    for pattern in patterns:
        for path in output_dir.glob(pattern):
            if path.is_file():
                path.unlink()


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
    renderer: str,
    render_recipe: dict[str, Any] | None,
    warnings: list[str],
    tile_width: int,
    tile_height: int,
    layout: str,
    tiles: list[tuple[str, dict[str, str], int]],
    output_files: dict[str, list[Path]],
    sim_run_id: str,
) -> dict[str, Any]:
    spec = EXPORT_LAYOUTS[layout]
    return {
        "source": "PixelLab MCP tileset simulator",
        "tool": tool,
        "sim_run_id": sim_run_id,
        "renderer": renderer,
        "render_recipe": render_recipe,
        "limits": [
            "This simulates PixelLab MCP request shape and compact tileset layout locally.",
            "It writes local PNG layout previews and does not attempt to reproduce PixelLab MCP create/get JSON.",
            "Renderers use simple keyword/semantic colors or AI-authored semantic recipes and do not predict PixelLab's model taste.",
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
        "output_files": {key: [str(path) for path in paths] for key, paths in output_files.items()},
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
        assert all(isinstance(cell, int) and 0 <= cell < len(PIXELLAB_TILE_ORDER) for cell in spec["cells"]), layout


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
    render_recipe = run_ai_renderer(args.renderer, args.tool, request, tile_width, tile_height, args.agent_timeout)
    tiles = make_tiles()

    output_dir = output_dir_from_name(args.output)
    component_dir = output_dir / "components"
    output_dir.mkdir(parents=True, exist_ok=True)
    component_dir.mkdir(parents=True, exist_ok=True)
    remove_known_outputs(output_dir)
    output_paths = {
        "corner_preview": output_dir / "corner-key-preview.png",
        "native_tileset": output_dir / "native-tileset.png",
        "component_lower": output_dir / "component-lower.png",
        "component_transition": output_dir / "component-transition.png",
        "component_center_tile": output_dir / "component-center-tile.png",
        "lower_tile": component_dir / "lower-tile.png",
        "transition_tile": component_dir / "transition-tile.png",
        "center_tile": component_dir / "center-tile.png",
        "tileset": output_dir / "tileset.png",
        "sim_report": output_dir / "sim-report.json",
    }
    if args.tool == "create_topdown_tileset":
        output_paths["component_upper"] = output_dir / "component-upper.png"
        output_paths["upper_tile"] = component_dir / "upper-tile.png"
    else:
        output_paths["top_tile"] = component_dir / "top-tile.png"

    template_sheet = None
    if args.template_sheet:
        if args.tool != "create_sidescroller_tileset":
            raise SystemExit("--template-sheet is only supported for create_sidescroller_tileset.")
        try:
            template_sheet = Image.open(args.template_sheet).convert("RGBA")
        except OSError as exc:
            raise SystemExit(f"Could not read template sheet image: {args.template_sheet}") from exc
        expected_size = (tile_width * 4, tile_height * 4)
        if template_sheet.size != expected_size:
            raise SystemExit(f"Template sheet must be {expected_size[0]}x{expected_size[1]}, got {template_sheet.size}.")

    corner = draw_corner_preview(tile_width, tile_height, args.draw_grid, tiles)
    native_tileset = draw_tileset(args.tool, request, tile_width, tile_height, False, tiles, template_sheet, render_recipe)
    tileset = compose_export_sheet(native_tileset, args.layout, tile_width, tile_height, args.draw_grid)
    component_previews = draw_component_previews(args.tool, request, tile_width, tile_height, native_tileset, render_recipe)

    written_files: dict[str, list[Path]] = {}
    written_files["corner_preview"] = save_scaled(corner, output_paths["corner_preview"], args.scale)
    written_files["native_tileset"] = save_scaled(native_tileset, output_paths["native_tileset"], args.scale)
    for key, image in component_previews.items():
        written_files[key] = save_scaled(image, output_paths[key], args.scale)
    component_aliases = {
        "lower_tile": component_previews["component_lower"],
        "transition_tile": component_previews["component_transition"],
        "center_tile": component_previews["component_center_tile"],
    }
    if args.tool == "create_topdown_tileset":
        component_aliases["upper_tile"] = component_previews["component_upper"]
    else:
        component_aliases["top_tile"] = component_previews["component_transition"]
    for key, image in component_aliases.items():
        written_files[key] = save_scaled(image, output_paths[key], args.scale)
    written_files["tileset"] = save_scaled(tileset, output_paths["tileset"], args.scale)

    sim_run_id = stable_id(
        "run",
        {"tool": args.tool, "request": request, "layout": args.layout, "renderer": args.renderer, "output": str(output_dir)},
    )
    sim_report = build_report(
        args.tool,
        request,
        args.renderer,
        render_recipe,
        warnings,
        tile_width,
        tile_height,
        args.layout,
        tiles,
        written_files | {"sim_report": [output_paths["sim_report"]]},
        sim_run_id,
    )
    if args.template_sheet:
        sim_report["template_sheet"] = str(args.template_sheet)
    with output_paths["sim_report"].open("w", encoding="utf-8") as handle:
        json.dump(sim_report, handle, indent=2)

    for key in (
        "corner_preview",
        "native_tileset",
        "component_lower",
        "component_upper",
        "component_transition",
        "component_center_tile",
        "lower_tile",
        "upper_tile",
        "top_tile",
        "transition_tile",
        "center_tile",
        "tileset",
        "sim_report",
    ):
        if key in output_paths:
            print(f"Wrote {output_paths[key]}")


if __name__ == "__main__":
    main()
