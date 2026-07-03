# PixelLab DualGrid Tileset Export System

Last reviewed: 2026-07-03.

Purpose: document the observed DualGrid/Wang export contract for PixelLab tilesets so local tools can simulate the deterministic parts of tileset assembly before spending generations.

This note is about structure, JSON fields, export layout, and verification. It does not claim to simulate PixelLab's image model, prompt interpretation, palette drift, or texture generation.

## Sources Reviewed

- Official REST v2 OpenAPI: `https://api.pixellab.ai/v2/openapi.json`
- Official MCP docs: `https://api.pixellab.ai/mcp/docs`
- Official Create Tileset docs: `https://www.pixellab.ai/docs/tools/create-tileset`
- Local PixelLab Pip routing references: `skills/pixellab-pip/SKILL.md`, `skills/pixellab-pip/references/tilesets.md`, and `skills/pixellab-pip/references/aseprite-cli.md`
- Local PixelLab research docs for public API, website endpoint, Aseprite extension, and endpoint-crosswalk behavior
- Observed PixelLab top-down and sidescroller tileset metadata from local generation outputs
- DualGrid background references: Lexaloffle DualGrid post, KaffeMedBulla DualGrid tileset notes, and `pablogila/TileMapDual`

## Short Version

PixelLab top-down and sidescroller tileset outputs use corner-based DualGrid/Wang-style structure. In observed compact exports, PixelLab returns a 4x4 sheet with 16 tiles, metadata format `tileset15`, and a `4x4_wildcard` pattern system. Sidescroller outputs are expected to be compact 16-tile platform sheets; top-down outputs can expand for full-transition or Pro-style cases and must be verified by returned metadata and image dimensions.

The deterministic contract is:

- Each display tile represents four neighboring terrain cells: `NW`, `NE`, `SW`, and `SE`.
- Observed compact metadata encodes terrain as `lower = 0`, `upper = 1`, and `wildcard = 255`.
- PixelLab `wang_N` names use bit weights `NW = 8`, `NE = 4`, `SW = 2`, `SE = 1`, where `1` means upper/background and `0` means lower/platform.
- In observed compact sheets, the PixelLab/Lexaloffle row-major order is:

```text
13, 10,  4, 12
 6,  8,  0,  1
11,  3,  2,  5
15, 14,  9,  7
```

This is not the same atlas order as some third-party DualGrid implementations. For example, `TileMapDualLegacy` uses `TOP_LEFT = 1`, `LOW_LEFT = 2`, `TOP_RIGHT = 4`, and `LOW_RIGHT = 8`, then maps the resulting key to atlas coordinates. That is useful research background, but it is not exposed as a PixelLab website/MCP export layout in the simulator.

## DualGrid Math

DualGrid uses a display grid offset from the world/logic grid. A display tile samples the four world cells around it:

```text
NW NE
SW SE
```

The four sampled values become a 4-bit key. PixelLab's observed key is:

```text
bitmask = NW*8 + NE*4 + SW*2 + SE*1
```

With PixelLab terrain encoding, the expected center `2x2` pattern is the four corner values and the outer ring is wildcard:

```text
255 255 255 255
255  NW  NE 255
255  SW  SE 255
255 255 255 255
```

For PixelLab sidescroller platform tests, this means `wang_0` is the fully filled lower/platform tile and `wang_15` is the fully upper/background tile. This can feel inverted if you are coming from TileMapDual examples where bit `1` often means filled terrain.

Do not treat downloaded `pattern_4x4` fields as the strongest authority. Local fixtures show many PixelLab metadata surfaces where `pattern_4x4` disagrees with the tile `name`, `corners`, and visual sheet position, across both top-down and sidescroller outputs. For reverse-engineering checks, prefer `wang_N`, `corners`, returned tile order, bounding boxes, and the actual spritesheet. Use locally computed patterns as `expected_pattern_4x4`.

## Compact Export Shape

Observed compact PixelLab tilesets usually include:

- `format: "tileset15"`
- `layout.type: "tileset15"`
- `layout.grid_size: { "width": 4, "height": 4 }`
- `layout.tile_count: 16`
- `tileset_data.spritesheet_layout: "tileset15_4x4"`
- `tileset_data.spritesheet_grid: { "cols": 4, "rows": 4 }`
- `pattern_system.type: "4x4_wildcard"`
- `pattern_system.terrain_encoding.lower: 0`
- `pattern_system.terrain_encoding.upper: 1`
- `pattern_system.terrain_encoding.wildcard: 255`

Top-down exports are not always compact across every PixelLab surface. Current MCP docs expose compact-oriented transition values `0`, `0.25`, and `0.5`; REST schema and local live findings also include expanded `tileset15_4x8` behavior for `transition_size: 1.0`. Any tool that needs a strict 4x4 sheet must verify `total_tiles`, `spritesheet_grid`, `spritesheet_layout`, and downloaded PNG dimensions before treating the output as compact.

Each returned tile may include:

- `id`
- `name`, usually `wang_N`
- `image` in REST `GET /v2/tilesets/{tileset_id}` results
- `corners` with `NW`, `NE`, `SW`, and `SE`
- `pattern_4x4`
- `bounding_box`
- `original_position`
- optional `description`
- optional `connections`

Use `bounding_box` or the returned tile order to assemble the delivered sheet. Do not sort final exports by `wang_N`, `original_position`, `pattern_4x4`, or inferred corner key unless you are deliberately remapping to another engine convention.

## Public Automation Surfaces

MCP routes:

- `create_topdown_tileset`
- `get_topdown_tileset`
- `create_sidescroller_tileset`
- `get_sidescroller_tileset`
- `create_tiles_pro`
- `get_tiles_pro`

REST v2 routes:

- `POST /v2/create-tileset`
- `POST /v2/tilesets`
- `GET /v2/tilesets/{tileset_id}`
- `POST /v2/create-tileset-sidescroller`
- `POST /v2/tilesets-sidescroller`
- `GET /v2/background-jobs/{job_id}`
- `POST /v2/create-tiles-pro`
- `GET /v2/tiles-pro/{tile_id}`

REST top-down tileset creation uses `CreateTilesetRequest`. Key fields are `lower_description`, `upper_description`, `transition_description`, `tile_size`, `mode`, `view`, `transition_size`, style controls, guidance/adherence controls, base tile IDs, reference images, `color_image`, and `seed`.

Current MCP `create_topdown_tileset` docs expose the main descriptions, transition size, tile size, mode, Pro shape controls, style controls, view, adherence/guidance controls, and base tile IDs. They do not expose the REST reference-image, palette-image, or seed fields.

REST sidescroller tileset creation uses `CreateTilesetSidescrollerRequest`. It uses `lower_description` for the platform body and `transition_description` for the top/surface layer. REST exposes `lower_reference_image`, `transition_reference_image`, and `color_image`. Current MCP sidescroller docs expose the main descriptions, tile size, style controls, guidance/adherence controls, `base_tile_id`, and seed, but not the REST reference or palette image fields.

`create_tiles_pro` and `POST /v2/create-tiles-pro` are for independent shaped tile variants, not a connected Wang/DualGrid terrain tileset.

## Website And Aseprite Boundaries

The website Create Tileset surface and Aseprite extension are useful evidence for product behavior, but they are not the stable automation target for Pip.

The website has an internal/root Create Tileset route with fields such as `use_pro`, `use_sidescroller`, and `tileset_mode`. That route uses website session auth and is not the public REST v2 tileset contract.

The Aseprite extension has local tileset workflows and operation URLs, but those are editor integration behavior, not public REST or MCP. Stable automation should use:

```text
PixelLab MCP or REST v2
-> downloaded PNGs and metadata
-> local assembly, verification, Aseprite CLI import/export, or palette checks
```

For strict 1-bit results, Aseprite or local palette verification can create an explicitly labeled derivative after PixelLab generation, but the untouched PixelLab output must be kept and reported separately.

## Simulator Contract

The local MCP tileset simulator lives at:

```text
dev-tools/pixellab_mcp_tileset_sim.py
```

Use `dev-tools/pixellab_mcp_tileset_sim.md` as the agent-facing runbook. This document is the evidence/background note, not the fastest way to operate the tool.

The simulator accepts MCP-style request JSON from a file or stdin, writes to `.local/mcp-tileset-sim-output/latest` by default, and supports `--output NAME` to compare attempts under separate child directories.

The current simulator covers the compact 16-tile layout for MCP-style `create_sidescroller_tileset` and `create_topdown_tileset` requests. It should focus on:

- Request-field shape and local schema validation
- Bitmask and corner math
- PixelLab compact 4x4 layout order
- PixelLab website export repacking for `15-tileset`, `wang`, and `godot-3x3`
- Pattern report generation
- Palette and dimension verification
- Deterministic semantic rendering from description text
- Template-mask previews from observed PixelLab sheets

It writes `tileset.png`, `native-tileset.png`, component previews, `corner-key-preview.png`, and `sim-report.json`. The report contains simulator-only evidence such as the exact request JSON, omitted MCP defaults used for simulation, output paths, native 15-tileset source cells, exported cell placements, computed corner patterns, and optional AI render recipes. It does not attempt to reproduce PixelLab MCP create/get JSON responses.

It validates the MCP-facing route fields used by local simulation. REST-only fields such as reference images and `color_image` are intentionally outside this MCP simulator. It rejects top-down cases that may export as expanded sheets, because it does not yet simulate expanded top-down transition sheets.

The platform preview is a per-tile schematic. It can highlight tile edges that would become internal seams in a composed map, and template-sheet mode treats any opaque pixel as occupied, including decorative top/transition pixels.

The simulator should not claim to predict:

- Exact PixelLab imagery
- Prompt adherence
- Palette enforcement from text
- Whether generated white/edge pixels land in the desired visual place
- Internal backend model behavior not exposed by public metadata

## Reverse-Engineering Next Steps

To get closer to a reliable local preflight, collect fixtures for each generated test:

- Request JSON
- MCP tool or REST endpoint used
- Background job response
- Final `GET /v2/tilesets/{tileset_id}` response when available
- Downloaded spritesheet PNG
- Metadata JSON
- Palette statistics
- Sheet dimensions
- Tile order and `wang_N` names
- Whether the result is compact `4x4` or expanded

Then add simulator checks in this order:

1. Validate the request against the route family.
2. Predict expected compact or expanded output dimensions where known.
3. Emit the PixelLab/Lexaloffle 4x4 layout.
4. Emit PixelLab website export layouts such as Wang and Godot 3x3 when requested.
5. Compare a returned PixelLab sheet's alpha/occupancy mask against expected `wang_N` corner classes.
6. Verify exact palette requirements separately from structural correctness.

The practical target is a simulator that can say, "this MCP JSON is structurally plausible and should export as this DualGrid layout," before a live generation. It should not promise that PixelLab will obey a difficult visual prompt such as exact 1-bit edge-only highlights.
