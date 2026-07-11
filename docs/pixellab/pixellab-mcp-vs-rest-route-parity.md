# PixelLab MCP vs REST v2 Route Parity

Last reviewed: 2026-07-11.

Purpose: a route-level comparison of PixelLab's hosted MCP tool surface against the public REST v2 API — the missing features both ways: every REST v2 asset/management endpoint with no MCP counterpart, and every MCP tool with no REST v2 counterpart. (Two non-asset REST infrastructure routes are handled separately below.) This is the parity map behind SKILL.md's rule "do not assume a REST endpoint has an MCP equivalent just because MCP is configured." It complements the *service*-level comparison in [Official PixelLab MCP Service Comparison](../tools/official-pixellab-mcp-service-comparison.md) and the *label*-level crosswalk in [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md); this file is the *endpoint*-level view.

## Snapshots Compared

Parity is a moving target because both surfaces ship independently. This review compares:

- **REST v2 index:** `https://api.pixellab.ai/v2/llms.txt`, fetched 2026-07-11 and cross-checked against `https://api.pixellab.ai/v2/openapi.json` the same day. `llms.txt` is the curated published index; OpenAPI is the fuller machine-readable schema. Where both agree a route is absent (e.g., any tileset/tile `delete`), it is treated as genuinely absent, not an index abbreviation.
- **MCP inventory:** `https://api.pixellab.ai/mcp/docs`, auto-generated snapshot dated 2026-07-02 (cached locally). This is the authoritative public MCP tool list; the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` is not.

Absence from a snapshot is not proof of absence from the live API. When a route or tool matters for code, re-verify against current OpenAPI/MCP docs (SKILL.md → Current Docs Refresh).

## How To Read This

Three surfaces are conflated in casual usage; they are not the same contract:

- **MCP tools** are called through an MCP client (bare or host-prefixed such as `mcp__pixellab__create_character`). They are not HTTP paths; do not curl a tool name as `/v2/...`.
- **REST v2 endpoints** are HTTP paths under `https://api.pixellab.ai/v2`.
- **Managed-asset animation** (`/animate-character`, `/characters/animations`, `/objects/{id}/animations`) and **raw animation** (`/animate-with-text*`, `/animate-with-skeleton`, `/interpolation-v2`, …) are different endpoint families. MCP exposes the managed-asset ones only. This is the single most important distinction in the whole map: MCP has no *standalone* raw-animation tool — animation, interpolation, and rotation are bundled into the managed `animate_*` / `create_*` tools and need a managed-asset context, even though several accept supplied images as `*_base64` inputs.

## At a Glance

**Matching basis:** counterparts are judged by **functional capability, not tool name** — a REST endpoint counts as "covered" if any MCP tool or documented MCP parameter does the same job, even under a different name or bundled into a broader tool (and the reverse for MCP tools). A scoped or partial overlap (for example, an MCP capability that works only on a managed asset) is marked partial (◐), not dropped.

**On both surfaces — full functional parity, so they live in the [Coverage Matrix](#coverage-matrix) below, not in the gap lists:** characters (4/8-direction, v3, pro, state, animate, list/get/delete), **portrait ↔ character conversion** (`portrait-character-pro` ↔ `create_portrait_character`), objects (1/8-direction, state, animate, review, list/get/delete), map objects, top-down / sidescroller / isometric / pro tilesets & tiles, structured UI assets, **pixel font Pro** (`generate-font-pro` ↔ `create_font`), and balance. There is no vocal / voice / lip-sync / audio animation capability on either surface as of these snapshots.

**Missing from MCP — REST v2 has it, no dedicated MCP tool (32 endpoints; ◐ = partial overlap via a broader tool).** See [REST v2 Endpoints With No MCP Counterpart](#rest-v2-endpoints-with-no-mcp-counterpart).

| Category | # | REST v2 endpoints |
|---|---|---|
| Raw image generation | 7 | `create-image-pixen`, `create-image-pixflux`, `create-image-pixflux-background`, `create-image-bitforge`, `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2` |
| Image edit / convert / resize | 6 | `edit-image`, `edit-images-v2`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background` |
| Inpaint | 2 | `inpaint`, `inpaint-v3` |
| Raw animation / rotation / skeleton | 11 | `animate-with-text`, `animate-with-text-v2`, `animate-with-text-v3`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, `rotate` |
| Prompt enhancement | 3 | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, `enhance-animation-v3-prompt` |
| Managed-asset export & tagging | 3 | `characters/{id}/zip`, `characters/{id}/tags` (PATCH), `objects/{id}/tags` (PATCH) |

◐ **Partial overlap** (8 of the 32 — no *dedicated* MCP tool, but a broader MCP tool covers a managed-asset-scoped version). The general pattern: **REST separates a capability into versioned, single-purpose endpoints; MCP combines them into one managed-asset tool.** the `animate-with-text` family (`animate-with-text`, `-v2`, `-v3`) and `interpolation-v2` fold into MCP `animate_character`/`animate_object` via `mode` and — for `-v3`/interpolation — the `custom_start_frame_base64`/`end_frame_base64` frame anchors (start frame alone ≈ single-anchor animation, start **and** end ≈ interpolation); `generate-8-rotations-v2`/`-v3` → `create_8_direction_object`/`create_character` 8-direction output; `generate-ui-v2` → `create_ui_asset` (structured panels); `characters/{id}/zip` → `get_character` download link. Per-endpoint notes are below.

**Missing from REST v2 — MCP has it, no REST endpoint (24 tools).** See [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

| Category | # | MCP tools |
|---|---|---|
| Projects | 1 | `list_projects` |
| Chat (game-building agent) | 3 | `chat_list_conversations`, `chat_get_messages`, `chat_send_message` |
| Sandbox (code execution) | 8 | `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync` |
| Deployed agents | 3 | `agent_list`, `agent_inspect`, `agent_talk` |
| MCP meta | 2 | `agent_help`, `agent_feedback` |
| Delete/list helpers (no REST route in llms.txt **or** OpenAPI) | 7 | `delete_topdown_tileset`, `delete_sidescroller_tileset`, `delete_isometric_tile`, `delete_tiles_pro`, `delete_animation`, `list_sidescroller_tilesets`, `list_tiles_pro` |

## Coverage Matrix

Parity legend (functional, not name-based): **=** covered by a dedicated MCP tool or a documented tool parameter; **~** covered only via an inferred, undocumented parameter value on a broader MCP tool; **◐** partial — a broader MCP tool produces the *same kind of output* in a scoped form (e.g., managed-asset-only), but no dedicated MCP tool exists. A merely adjacent MCP capability that yields a *different* asset type (e.g., a generation-time control such as `create_map_object`'s `inpainting`, or `style_images` on object creation) is **none** with a note, not ◐; **none** / **REST-only** no MCP tool documented. On multi-helper rows, `=` is capability-level (create + retrieve); see the note after the tables about the `list`/`delete` routes REST v2 lacks entirely. This matrix is comprehensive and REST-keyed — every REST v2 endpoint appears in a table below; MCP tools with no REST endpoint are listed separately in [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

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
| `GET /characters/{id}/zip` | `get_character` download link (no full ZIP bundle) | ◐ |
| `PATCH /characters/{id}/tags` | — | **REST-only** |
| `POST /portrait-character-pro` | `create_portrait_character` + `get_portrait_character` | = |
| (managed animation delete) | `delete_animation` | MCP-only |

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
| (tileset/tile delete) | `delete_topdown_tileset`, `delete_sidescroller_tileset`, `delete_isometric_tile`, `delete_tiles_pro` | MCP-only |

### Fonts, UI, Account

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /generate-font-pro` | `create_font` + `get_font` | = |
| `POST /create-ui-asset`, `GET /ui-assets`, `GET /ui-assets/{id}`, `DELETE /ui-assets/{id}` | `create_ui_asset`, `list_ui_assets`, `get_ui_asset`, `delete_ui_asset` | = |
| `POST /generate-ui-v2` | `create_ui_asset` (structured panels only) | ◐ |
| `GET /balance` | `get_balance` | = |
| `GET /background-jobs/{job_id}` | per-resource `get_*` tools | different model |

**Note on async retrieval and management rows.** Where a `=` row bundles MCP `get_*` / `list_*` helpers against a single REST `POST`, REST retrieval is via `GET /background-jobs/{job_id}` (the generic async poll) plus, where present, a dedicated GET such as `/tilesets/{id}`, `/isometric-tiles/{id}`, `/tiles-pro/{id}`, or `/characters/{id}`. So MCP `get_*` tools are never true gaps. Neither `llms.txt` nor OpenAPI, however, exposes a *list* route for sidescroller tilesets or tiles-pro, or a *delete* route for any tile/tileset family — even though MCP has tools for all of them. Those `list`/`delete` tools are genuinely MCP-only (verified 2026-07-11; see [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart)), so `=` here means create-plus-retrieve parity; the `list`/`delete` half of those families has no REST route at all.

### Create Image (raw generation)

MCP has no generic text-to-image tool — it only generates managed asset types — so these are REST-only except UI, which has a structured MCP form.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /create-image-pixen` | — | none |
| `POST /create-image-pixflux` | — | none |
| `POST /create-image-pixflux-background` | — | none |
| `POST /create-image-bitforge` (pose-guided via `skeleton_keypoints`) | — | none |
| `POST /generate-image-v2` (Pro) | — | none |
| `POST /generate-with-style-v2` (Pro, style ref) | `style_images` on `create_1/8_direction_object`, `create_tiles_pro` (managed only, different output) | none |
| `POST /generate-ui-v2` (loose UI image) | `create_ui_asset` (structured panels) | ◐ |

### Image Edit, Convert, Resize

No MCP tool edits an arbitrary supplied image. `create_*_state` edits a *managed* asset by description (a re-rendered variant), a different operation.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /edit-image` | `create_character_state`/`create_object_state` (managed variant, not in-place edit) | none |
| `POST /edit-images-v2` (Pro, multi-source) | — | none |
| `POST /image-to-pixelart` | — | none |
| `POST /image-to-pixelart-pro` (Pro) | — | none |
| `POST /resize` | — | none |
| `POST /remove-background` | generation-time `no_background` only, not post-hoc removal | none |

### Inpaint

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /inpaint` | — | none |
| `POST /inpaint-v3` (Pro) | `create_map_object(inpainting=…)` is map-object-scoped, not a generic inpaint | none |

### Raw Animation, Rotation, Skeleton

**API separates, MCP combines.** REST exposes animation as versioned, single-purpose endpoints; MCP folds text animation and interpolation into `animate_character`/`animate_object`, selected by `mode` and the `custom_start_frame_base64`/`end_frame_base64` frame anchors (a start frame alone ≈ single-anchor animation; start **and** end ≈ interpolation). This frame-anchor mapping is exact for `animate-with-text-v3` (`first_frame`) and `interpolation-v2` (`start_image`+`end_image`); `animate-with-text`/`-v2` take a `reference_image` instead (a subject/style role, not a frame anchor), so they overlap only via the text-animation capability. Both MCP tools require a managed `character_id`/`object_id`, so raw-image animation is at most ◐ (managed-scoped). Managed animation (`/animate-character`, `/characters/animations`, `/objects/{id}/animations` = `animate_*`) is a full `=` — see the Characters/Objects tables above.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /animate-with-text` (base; `reference_image`+`action`) | `animate_*(action_description)` (modern `mode="v3"`), managed | ◐ |
| `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) | `animate_*(action_description)`; no matching Pro/v2 mode is documented in MCP, managed | ◐ |
| `POST /animate-with-text-v3` (new; `first_frame`+`action`) | `animate_*(mode="v3", custom_start_frame_base64)`, managed | ◐ |
| `POST /interpolation-v2` (Pro; `start_image`+`end_image`) | `animate_*(mode="v3", custom_start_frame_base64 + end_frame_base64)`, managed | ◐ |
| `POST /generate-8-rotations-v2` (Pro) | `create_8_direction_object(reference_image_base64)` / `create_character(n_directions=8)`, regenerates, managed | ◐ |
| `POST /generate-8-rotations-v3` | same as `-v2` | ◐ |
| `POST /edit-animation-v2` (Pro) | — | none |
| `POST /transfer-outfit-v2` (Pro) | — | none |
| `POST /animate-with-skeleton` (`skeleton_keypoints`) | — (no MCP keypoint input) | none |
| `POST /estimate-skeleton` | — | none |
| `POST /rotate` (single arbitrary rotation) | — | none |

### Prompt Enhancement

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /enhance-pixen-prompt` | — (`agent_help` is docs Q&A, not a rewriter) | none |
| `POST /enhance-character-v3-prompt` | — | none |
| `POST /enhance-animation-v3-prompt` | — | none |

### Infrastructure (non-asset)

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `GET /background-jobs/{job_id}` | per-resource `get_*` polling | different model |
| `GET /llms.txt` | `pixellab://docs/*` resources | different form |

## REST v2 Endpoints With No MCP Counterpart

This is the core deliverable. As of the snapshots above, these REST v2 endpoints have no documented MCP tool. Route them to REST v2; do not wait for or invent an MCP equivalent. Grouped by why the gap exists.

### 1. Raw image generation (7) — MCP has no text-to-image primitive

MCP only creates *managed asset types* (character, object, tileset, tile, font, UI asset, map object). It exposes no generic "generate an image" tool, so every raw image model is REST-only:

- `POST /create-image-pixen`
- `POST /create-image-pixflux`
- `POST /create-image-pixflux-background`
- `POST /create-image-bitforge`
- `POST /generate-image-v2` (Pro)
- `POST /generate-with-style-v2` (Pro, style reference) — note: MCP exposes style-guided generation only as `style_images` on managed object/tile creation, not as arbitrary styled-image output
- `POST /generate-ui-v2` (loose/raw UI image) — ◐ partial: MCP `create_ui_asset` generates structured UI panels; only the loose raw-image variant is REST-only

### 2. Image edit / convert / resize (6) — MCP has no raw-image-editing tools

MCP operates on assets it created, not on arbitrary supplied images:

- `POST /edit-image` — closest MCP analog is `create_character_state`/`create_object_state`, which edit a *managed* asset by description (a regenerated variant), not an in-place edit of a supplied image
- `POST /edit-images-v2` (Pro, multi-source)
- `POST /image-to-pixelart`
- `POST /image-to-pixelart-pro` (Pro)
- `POST /resize`
- `POST /remove-background`

Note: MCP `create_map_object` may accept `background_image` / `inpainting` parameters. Those are map-object generation controls, not generic replacements for `edit-image` or `inpaint`.

### 3. Inpaint (2) — no generic MCP inpaint tool

- `POST /inpaint`
- `POST /inpaint-v3` (Pro)

### 4. Raw animation, rotation, skeleton (11) — MCP folds animation into two managed tools

MCP `animate_character` / `animate_object` require a managed `character_id`/`object_id`, so none of these raw endpoints has a *dedicated* MCP tool. But MCP **combines** the separate REST text-animation and interpolation endpoints into those two tools, selected by `mode` plus the `custom_start_frame_base64` / `end_frame_base64` frame anchors — so several are ◐ partial (managed-scoped). The frame axis is orthogonal to the version: a start frame alone ≈ single-anchor animation; adding an end frame ≈ interpolation. This maps cleanly for `animate-with-text-v3` (`first_frame`) and `interpolation-v2` (`start_image`+`end_image`); `animate-with-text`/`-v2` take a `reference_image` (a subject/style role, not a frame anchor), so they overlap only via the text-animation capability. Fully REST-only: skeleton/keypoint animation, animation-frame editing, outfit transfer, single-image rotate.

- `POST /animate-with-text` (base/legacy; `reference_image`+`action`) — ◐ partial: capability covered by MCP `animate_*` `action_description` (modern `mode="v3"`), managed asset only
- `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) — ◐ partial: the text-animation capability is covered by MCP `animate_*` `action_description`, but MCP documents no matching Pro/v2 mode, so the version match is unconfirmed; managed asset only
- `POST /animate-with-text-v3` (new; `first_frame`+`action`+`frame_count`) — ◐ partial: MCP `animate_*(mode="v3", action_description, custom_start_frame_base64)`, managed asset only
- `POST /interpolation-v2` (Pro; `start_image`+`end_image`) — ◐ partial: MCP `animate_*(mode="v3")` with `custom_start_frame_base64` **and** `end_frame_base64`, but only on a managed asset and emitted as a named animation
- `POST /generate-8-rotations-v2` (Pro) — ◐ partial: MCP `create_8_direction_object(reference_image_base64=…)` / `create_character(n_directions=8)` emit 8 directions, but regenerate the subject rather than rotating the exact input
- `POST /generate-8-rotations-v3` — ◐ partial: same managed-asset overlap as `-v2`
- `POST /edit-animation-v2` (Pro) — fully REST-only (no MCP tool edits arbitrary animation frames)
- `POST /transfer-outfit-v2` (Pro) — fully REST-only (no MCP outfit transfer)
- `POST /animate-with-skeleton` (`skeleton_keypoints`) — fully REST-only (MCP tools accept no keypoint arrays)
- `POST /estimate-skeleton` — fully REST-only
- `POST /rotate` (single arbitrary rotation) — fully REST-only

There is no public raw *4-rotation batch* route: the batch rotation routes are 8-direction only. The *managed* animation endpoints `/animate-character`, `/characters/animations`, `/objects/{id}/animations` are full `=` matches to MCP `animate_*` and appear in the Characters/Objects matrix tables, not this list.

### 5. Prompt enhancement (3) — no MCP prompt-helper tools

MCP exposes `agent_help` (a docs Q&A knowledge agent), which is not a prompt rewriter:

- `POST /enhance-pixen-prompt`
- `POST /enhance-character-v3-prompt`
- `POST /enhance-animation-v3-prompt`

### 6. Managed-asset export & tagging (3) — MCP has create/get/list/delete but not these

MCP covers the asset lifecycle except a full-bundle ZIP export and tag mutation:

- `GET /characters/{id}/zip` (full-bundle ZIP export) — ◐ partial: MCP `get_character` returns a download link, but no documented full-bundle ZIP export
- `PATCH /characters/{id}/tags` (set tags; MCP `list_characters` can *filter* by tags but cannot set them)
- `PATCH /objects/{id}/tags` (set tags)

### Not counted as asset gaps

- `GET /background-jobs/{job_id}` — REST's generic async poll. MCP deliberately uses per-resource `get_*` tools instead, so this is a different async model, not a missing capability.
- `GET /llms.txt` — the docs index itself, not an asset operation.

**Total: 32 asset/management REST v2 endpoints with no *dedicated* MCP counterpart** (7 image gen + 6 edit + 2 inpaint + 11 animation/rotation + 3 prompt enhance + 3 export/tags). Of these, 8 have partial, managed-asset-scoped functional overlap via a broader MCP tool (◐): the `animate-with-text` family (`animate-with-text`, `-v2`, `-v3`), `interpolation-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, `generate-ui-v2`, and `characters/{id}/zip`.

## MCP Tools With No REST v2 Counterpart

The mirror of the gap list above: MCP tools with no public REST v2 endpoint. Grouped by why the gap exists. Of the 60 MCP tools in the snapshot, 24 have no REST v2 counterpart: 17 in the platform layer, plus 7 `delete`/`list` lifecycle helpers absent from both `llms.txt` and OpenAPI.

### 1. Platform, agent, sandbox, chat (17) — genuinely MCP-only

No public REST v2 art API covers these; they exist only as MCP tools. Every platform tool except `get_balance` (which maps to `GET /balance`) is here. There is no REST fallback to offer — if these tools are not visible, the capability is unavailable.

- **Projects:** `list_projects`
- **Chat (game-building agent):** `chat_list_conversations`, `chat_get_messages`, `chat_send_message`
- **Sandbox (code execution):** `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`
- **Deployed agents:** `agent_list`, `agent_inspect`, `agent_talk`
- **MCP meta:** `agent_help` (docs Q&A knowledge agent), `agent_feedback`

Handle these per [`mcp-platform-tools.md`](../../skills/pixellab-pip/references/mcp-platform-tools.md) — most are account reads or state-changing actions that need explicit approval.

### 2. Management `delete`/`list` helpers with no REST route (7)

MCP documents these `delete` / `list` tools, but neither the `llms.txt` index nor the OpenAPI schema exposes a matching REST route (verified 2026-07-11 — REST v2 documents `DELETE` only for characters, objects, and UI assets, and no `list` route for sidescroller tilesets or tiles-pro). So MCP is the only surface that can delete a tileset/tile or a managed animation, or list those collections:

- **Deletes** (no REST *delete* route for any tile/tileset family, nor a managed-animation delete): `delete_topdown_tileset`, `delete_sidescroller_tileset`, `delete_isometric_tile`, `delete_tiles_pro`, `delete_animation`
- **Lists** (no REST *list* route): `list_sidescroller_tilesets`, `list_tiles_pro`

### Not counted as MCP-only

- Per-resource `get_*` tools without a dedicated REST GET (`get_font`, `get_map_object`, `get_portrait_character`, `get_sidescroller_tileset`) are not gaps: async retrieval maps to REST `GET /background-jobs/{job_id}` plus dedicated GETs where present.
- `pixellab://docs/...` resources (Godot/Unity/Python/Wang/sidescroller/isometric/overview integration guides) are MCP-only, but they are documentation, not an API surface.

**Total: 24 MCP tools with no REST v2 counterpart** — 17 in the platform layer, plus 7 `delete`/`list` lifecycle helpers absent from both `llms.txt` and OpenAPI.

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
