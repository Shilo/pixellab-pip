# PixelLab MCP vs REST v2 Route Parity

Last reviewed: 2026-07-11.

Purpose: a route-level comparison of PixelLab's hosted MCP tool surface against the public REST v2 API, and an explicit inventory of every REST v2 asset/management endpoint that has no MCP counterpart (two non-asset infrastructure routes are handled separately below). This is the parity map behind SKILL.md's rule "do not assume a REST endpoint has an MCP equivalent just because MCP is configured." It complements the *service*-level comparison in [Official PixelLab MCP Service Comparison](../tools/official-pixellab-mcp-service-comparison.md) and the *label*-level crosswalk in [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md); this file is the *endpoint*-level view.

## Snapshots Compared

Parity is a moving target because both surfaces ship independently. This review compares:

- **REST v2 index:** `https://api.pixellab.ai/v2/llms.txt`, fetched 2026-07-11. This is the curated published endpoint index; `https://api.pixellab.ai/v2/openapi.json` is the fuller machine-readable schema and may surface management routes (list/get/delete for some families) that `llms.txt` abbreviates.
- **MCP inventory:** `https://api.pixellab.ai/mcp/docs`, auto-generated snapshot dated 2026-07-02 (cached locally). This is the authoritative public MCP tool list; the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` is not.

Absence from a snapshot is not proof of absence from the live API. When a route or tool matters for code, re-verify against current OpenAPI/MCP docs (SKILL.md → Current Docs Refresh).

## How To Read This

Three surfaces are conflated in casual usage; they are not the same contract:

- **MCP tools** are called through an MCP client (bare or host-prefixed such as `mcp__pixellab__create_character`). They are not HTTP paths; do not curl a tool name as `/v2/...`.
- **REST v2 endpoints** are HTTP paths under `https://api.pixellab.ai/v2`.
- **Managed-asset animation** (`/animate-character`, `/characters/animations`, `/objects/{id}/animations`) and **raw animation** (`/animate-with-text*`, `/animate-with-skeleton`, `/interpolation-v2`, …) are different endpoint families. MCP exposes the managed-asset ones only. This is the single most important distinction in the whole map: MCP can animate a character/object it created, but it has no tool to animate an arbitrary supplied image.

## Coverage Matrix

Parity legend: **=** covered by a dedicated MCP tool or a documented tool parameter; **~** covered only via an inferred, undocumented parameter value on a broader MCP tool; **REST-only** no MCP tool documented. On multi-helper rows, `=` is capability-level (create + retrieve); see the note after the tables about `list`/`delete` routes that `llms.txt` omits.

### Characters

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-character-with-4-directions` | `create_character(n_directions=4)` | = |
| `POST /create-character-with-8-directions` | `create_character(n_directions=8)` | = |
| `POST /create-character-v3` | `create_character(mode="v3")` | ~ |
| `POST /create-character-pro` | `create_character(mode=…)` | ~ |
| `POST /create-character-state` | `create_character_state` | = |
| `POST /animate-character`, `POST /characters/animations` | `animate_character` | = |
| `GET /characters` | `list_characters` | = |
| `GET /characters/{id}` | `get_character` | = |
| `DELETE /characters/{id}` | `delete_character` | = |
| `GET /characters/{id}/zip` | — | **REST-only** |
| `PATCH /characters/{id}/tags` | — | **REST-only** |
| `POST /portrait-character-pro` | `create_portrait_character` + `get_portrait_character` | = |
| (managed animation delete) | `delete_animation` | MCP-only in snapshot |

### Objects & Map Objects

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-1-direction-object` | `create_1_direction_object` | = |
| `POST /create-8-direction-object` | `create_8_direction_object` | = |
| `POST /objects/{id}/animations` | `animate_object` | = |
| `POST /objects/{id}/states` | `create_object_state` | = |
| `POST /objects/{id}/select-frames` | `select_object_frames` | = |
| `POST /objects/{id}/dismiss-review` | `dismiss_review` | = |
| `GET /objects`, `GET /objects/{id}`, `DELETE /objects/{id}` | `list_objects`, `get_object`, `delete_object` | = |
| `PATCH /objects/{id}/tags` | — | **REST-only** |
| `POST /map-objects` | `create_map_object` + `get_map_object` | = |

### Tiles & Tilesets

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-tileset`, `POST /tilesets`, `GET /tilesets`, `GET /tilesets/{id}` | `create_topdown_tileset`, `get_topdown_tileset`, `list_topdown_tilesets` | = |
| `POST /create-tileset-sidescroller`, `POST /tilesets-sidescroller` | `create_sidescroller_tileset`, `get_sidescroller_tileset`, `list_sidescroller_tilesets` | = |
| `POST /create-isometric-tile`, `GET /isometric-tiles`, `GET /isometric-tiles/{id}` | `create_isometric_tile`, `list_isometric_tiles`, `get_isometric_tile` | = |
| `POST /create-tiles-pro`, `GET /tiles-pro/{id}` | `create_tiles_pro`, `get_tiles_pro`, `list_tiles_pro` | = |
| (tileset/tile delete) | `delete_topdown_tileset`, `delete_sidescroller_tileset`, `delete_isometric_tile`, `delete_tiles_pro` | MCP-only in snapshot |

### Fonts, UI, Account

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /generate-font-pro` | `create_font` + `get_font` | = |
| `POST /create-ui-asset`, `GET /ui-assets`, `GET /ui-assets/{id}`, `DELETE /ui-assets/{id}` | `create_ui_asset`, `list_ui_assets`, `get_ui_asset`, `delete_ui_asset` | = |
| `POST /generate-ui-v2` | — | **REST-only** |
| `GET /balance` | `get_balance` | = |
| `GET /background-jobs/{job_id}` | per-resource `get_*` tools | different model |

**Note on async retrieval and management rows.** Where a `=` row bundles MCP `get_*` / `list_*` helpers against a single REST `POST`, REST retrieval is via `GET /background-jobs/{job_id}` (the generic async poll) plus, where present, a dedicated GET such as `/tilesets/{id}`, `/isometric-tiles/{id}`, `/tiles-pro/{id}`, or `/characters/{id}`. So MCP `get_*` tools are never true gaps. `llms.txt`, however, lists no *list* route for sidescroller tilesets or tiles-pro, and no *delete* route for any tile/tileset family — even though MCP has tools for all of them. Those are almost certainly `llms.txt` abbreviations of routes that exist in OpenAPI (see [The Reverse](#the-reverse-mcp-surfaces-with-no-rest-v2-counterpart)), so `=` here means create-plus-retrieve parity, not that every MCP helper has a line in `llms.txt`.

## REST v2 Endpoints With No MCP Counterpart

This is the core deliverable. As of the snapshots above, these REST v2 endpoints have no documented MCP tool. Route them to REST v2; do not wait for or invent an MCP equivalent. Grouped by why the gap exists.

### 1. Raw image generation (7) — MCP has no text-to-image primitive

MCP only creates *managed asset types* (character, object, tileset, tile, font, UI asset, map object). It exposes no generic "generate an image" tool, so every raw image model is REST-only:

- `POST /create-image-pixen`
- `POST /create-image-pixflux`
- `POST /create-image-pixflux-background`
- `POST /create-image-bitforge`
- `POST /generate-image-v2` (Pro)
- `POST /generate-with-style-v2` (Pro, style reference)
- `POST /generate-ui-v2` (loose/raw UI image — distinct from managed `create_ui_asset`)

### 2. Image edit / convert / resize (6) — MCP has no raw-image-editing tools

MCP operates on assets it created, not on arbitrary supplied images:

- `POST /edit-image`
- `POST /edit-images-v2` (Pro, multi-source)
- `POST /image-to-pixelart`
- `POST /image-to-pixelart-pro` (Pro)
- `POST /resize`
- `POST /remove-background`

Note: MCP `create_map_object` may accept `background_image` / `inpainting` parameters. Those are map-object generation controls, not generic replacements for `edit-image` or `inpaint`.

### 3. Inpaint (2) — no generic MCP inpaint tool

- `POST /inpaint`
- `POST /inpaint-v3` (Pro)

### 4. Raw animation, rotation, skeleton (11) — MCP animates managed assets only

MCP `animate_character` / `animate_object` require an MCP-managed asset id. Animating a raw supplied sprite, rigging it, interpolating frames, transferring an outfit onto an animation, or rotating an arbitrary image are all REST-only:

- `POST /animate-with-text`
- `POST /animate-with-text-v2` (Pro)
- `POST /animate-with-text-v3`
- `POST /animate-with-skeleton`
- `POST /estimate-skeleton`
- `POST /edit-animation-v2` (Pro)
- `POST /interpolation-v2` (Pro)
- `POST /transfer-outfit-v2` (Pro)
- `POST /generate-8-rotations-v2` (Pro)
- `POST /generate-8-rotations-v3`
- `POST /rotate`

There is no public raw 4-rotation route; raw rotation is 8-direction only.

### 5. Prompt enhancement (3) — no MCP prompt-helper tools

MCP exposes `agent_help` (a docs Q&A knowledge agent), which is not a prompt rewriter:

- `POST /enhance-pixen-prompt`
- `POST /enhance-character-v3-prompt`
- `POST /enhance-animation-v3-prompt`

### 6. Managed-asset export & tagging (3) — MCP has create/get/list/delete but not these

MCP covers the asset lifecycle except ZIP export and tag mutation:

- `GET /characters/{id}/zip` (ZIP export)
- `PATCH /characters/{id}/tags` (set tags; MCP `list_characters` can *filter* by tags but cannot set them)
- `PATCH /objects/{id}/tags` (set tags)

### Not counted as asset gaps

- `GET /background-jobs/{job_id}` — REST's generic async poll. MCP deliberately uses per-resource `get_*` tools instead, so this is a different async model, not a missing capability.
- `GET /llms.txt` — the docs index itself, not an asset operation.

**Total: 32 asset/management REST v2 endpoints with no MCP counterpart** (7 image gen + 6 edit + 2 inpaint + 11 animation/rotation + 3 prompt enhance + 3 export/tags).

## The Reverse: MCP Surfaces With No REST v2 Counterpart

For completeness (the request was REST→MCP gaps, but the reverse informs routing too):

- **Platform / agent tooling — genuinely MCP-only.** No public REST v2 art API covers these: `list_projects`, `chat_list_conversations`, `chat_get_messages`, `chat_send_message`, `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`, `agent_list`, `agent_inspect`, `agent_talk`, `agent_help`, `agent_feedback`. Handle these per [`mcp-platform-tools.md`](../../skills/pixellab-pip/references/mcp-platform-tools.md) (most are account reads or state-changing actions needing approval).
- **Managed `delete`/`list` helpers not surfaced in `llms.txt`.** MCP documents `delete_topdown_tileset`, `delete_sidescroller_tileset`, `delete_isometric_tile`, `delete_tiles_pro`, `delete_animation`, plus `list_sidescroller_tilesets` and `list_tiles_pro`, while the current `llms.txt` index lists no matching REST *delete* route for any tile/tileset family and no *list* route for sidescroller tilesets or tiles-pro. Per-resource `get_*` tools are deliberately excluded here — they are not gaps, since async retrieval maps to REST `GET /background-jobs/{job_id}` plus dedicated GETs where present. The missing `delete`/`list` routes are most likely `llms.txt` abbreviation rather than a true REST gap — verify against OpenAPI before assuming a route is missing.
- **`pixellab://docs/...` resources.** Godot/Unity/Python/Wang/sidescroller/isometric/overview integration guides are MCP resources with no REST equivalent (they are documentation, not an API).

## Routing Implications

These follow from the gaps above and are already encoded in SKILL.md's Intent Router and Surface Rules — this section states *why*, not new rules:

- Everything in categories 1–5 is why the Intent Router sends generic images, backgrounds, loose UI, edits, inpaint, resize, background removal, raw animation, rotation, skeleton, interpolation, outfit transfer, and prompt enhancement to REST v2 even in an MCP-enabled agent.
- Category 4 is why a user asking to "animate this sprite I attached" cannot be served by MCP `animate_character` — that tool needs a managed character id, so an image-anchored animation request routes to REST raw animation (or first creating/importing a managed asset).
- Managed asset types (character, object, tileset, tile, font, UI asset, map object) are the overlap zone: prefer MCP when its tools are visible, fall back to the matching REST endpoint otherwise.

## Caveats

- Snapshot-bound: MCP inventory is the 2026-07-02 auto-generated docs; REST index is 2026-07-11 `llms.txt`. Both can drift; the doc-watch cache workflow ([`pixellab-doc-watch-cache.md`](pixellab-doc-watch-cache.md)) is how drift is detected.
- MCP↔REST are not guaranteed pixel-identical for the same prompt/seed even where parity is `=`; treat them as one workflow family with overlapping controls, REST generally exposing the fuller documented schema.
- `~` rows (`create-character-pro` and `create-character-v3` via the `create_character` `mode` parameter) are inferred capability mappings: the MCP snapshot documents `mode` with a `standard` default but does not enumerate `v3`/`pro` values, so the exact mapping is not proven from public docs. SKILL.md nonetheless defaults `create_character` to `mode="v3"`.
- This spike compares only public REST v2 and public MCP. Website/Map Workshop, Pixelorama/editor, Aseprite-extension, and legacy v1 routes are out of scope here; see [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md) for those surfaces.
