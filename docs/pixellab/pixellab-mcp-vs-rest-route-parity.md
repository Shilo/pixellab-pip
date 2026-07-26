# PixelLab MCP vs REST v2 Route Parity

Last reviewed: 2026-07-26.

> 2026-07-26 21:03 follow-up: within the same day, MCP replaced the brand-new generic `create_image` with three model-specific tools matching REST's own image-model split: `create_image_pixflux` (= full parity with `create-image-pixflux`), `create_image_pixen` (= full parity with `create-image-pixen`), and `create_image_pro` (= full parity with `generate-image-v2`, via matching `reference_images`/`style_image_base64`/`style_copy` fields — but not `generate-with-style-v2`, whose `style_images` array + `style_description` shape it does not match). `get_image` is unchanged (shared getter, now documented as returning `create_image_pixflux` results too). This closes 3 more of the 7 "Raw image generation" gaps outright (bitforge, `generate-with-style-v2`, and `generate-ui-v2` remain REST-only). Counts below reflect the new state (REST-only 27→24, MCP tool count 69→71, ◐ 9→8 — `create-image-pixflux` graduates from ◐ to `=`).
>
> 2026-07-26 refresh: MCP added 7 tools closing most of the former "MCP has no raw-image primitive" gap: `create_image`+`get_image` (generic text-to-image, ◐ partial vs the model-split REST image routes — see the 21:03 follow-up above, this tool was replaced within the hour), `edit_image` (= full parity with `edit-image`), `inpaint_image` (= full parity with `inpaint`), `animate_image` (= full parity with `animate-with-text-v3`, ◐ partial vs `interpolation-v2` — tier unconfirmed), and `create_path_tiles`/`create_building_kit` (= full parity, siblings of `create_tiles_pro` sharing its get/list/delete tools; REST folds all three into `create-tiles-pro` via `tile_feature: "roads"/"tileset"/"building"`). None of these are new REST surface — REST already had `edit-image`, `inpaint`, `animate-with-text-v3`, and the `tile_feature`/`building_*` fields on `create-tiles-pro`; MCP simply exposes them now. Counts at the time reflected REST-only 30→27, MCP tool count 62→69, MCP-only still 17.
>
> 2026-07-19 refresh: REST v2 added `DELETE` routes for tilesets, sidescroller tilesets, isometric tiles, tiles-pro, and managed character animations, plus `GET` list routes for sidescroller tilesets and tiles-pro — closing the seven "MCP-only delete/list helper" gaps this doc previously listed. MCP added `update_character_tags` / `update_object_tags`, closing the two `PATCH .../tags` "REST-only" gaps. Counts below reflect the new state (REST-only 32→30, MCP-only 24→17).

Purpose: a route-level comparison of PixelLab's hosted MCP tool surface against the public REST v2 API — the missing features both ways: every REST v2 asset/management endpoint with no MCP counterpart, and every MCP tool with no REST v2 counterpart. (Two non-asset REST infrastructure routes are handled separately below.) This is the parity map behind SKILL.md's rule "do not assume a REST endpoint has an MCP equivalent just because MCP is configured." It complements the *service*-level comparison in [Official PixelLab MCP Service Comparison](../tools/official-pixellab-mcp-service-comparison.md) and the *label*-level crosswalk in [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md); this file is the *endpoint*-level view.

## Snapshots Compared

Parity is a moving target because both surfaces ship independently. This review compares:

- **REST v2 index:** `https://api.pixellab.ai/v2/llms.txt`, cross-checked against `https://api.pixellab.ai/v2/openapi.json`, cached snapshot 2026-07-26. `llms.txt` is the curated published index; OpenAPI is the fuller machine-readable schema. Where both agree a route is absent, it is treated as genuinely absent, not an index abbreviation.
- **MCP inventory:** `https://api.pixellab.ai/mcp/docs`, auto-generated snapshot 2026-07-26 (cached locally). This is the authoritative public MCP tool list; the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` is not.

Absence from a snapshot is not proof of absence from the live API. When a route or tool matters for code, re-verify against current OpenAPI/MCP docs (SKILL.md → Current Docs Refresh).

## How To Read This

Three surfaces are conflated in casual usage; they are not the same contract:

- **MCP tools** are called through an MCP client (bare or host-prefixed such as `mcp__pixellab__create_character`). They are not HTTP paths; do not curl a tool name as `/v2/...`.
- **REST v2 endpoints** are HTTP paths under `https://api.pixellab.ai/v2`.
- **Managed-asset animation** (`/animate-character`, `/characters/animations`, `/objects/{id}/animations`) and **raw animation** (`/animate-with-text*`, `/animate-with-skeleton`, `/interpolation-v2`, …) are different endpoint families. MCP `animate_character`/`animate_object` cover the managed-asset family only (need a character/object ID). As of the 2026-07-26 refresh, MCP also has a standalone raw-animation tool, `animate_image`, that takes a `first_frame_base64` directly — no managed asset required — matching `animate-with-text-v3` and, via its optional `last_frame_base64`, `interpolation-v2`. Skeleton-keypoint animation, animation-frame editing, outfit transfer, and single-image rotate remain REST-only.

## At a Glance

**Matching basis:** counterparts are judged by **functional capability, not tool name** — a REST endpoint counts as "covered" if any MCP tool or documented MCP parameter does the same job, even under a different name or bundled into a broader tool (and the reverse for MCP tools). A scoped or partial overlap (for example, an MCP capability that works only on a managed asset) is marked partial (◐), not dropped.

**On both surfaces — full functional parity, so they live in the [Coverage Matrix](#coverage-matrix) below, not in the gap lists:** characters (4/8-direction, v3, pro, state, animate, list/get/delete), **portrait ↔ character conversion** (`portrait-character-pro` ↔ `create_portrait_character`), objects (1/8-direction, state, animate, review, list/get/delete), map objects, top-down / sidescroller / isometric / pro tilesets & tiles, **path/road tiles and building kits** (`create-tiles-pro` `tile_feature` ↔ `create_path_tiles`/`create_building_kit`), structured UI assets, **pixel font Pro** (`generate-font-pro` ↔ `create_font`), balance, **tag setting** (`PATCH .../tags` ↔ `update_character_tags` / `update_object_tags`), **raw text-to-image on PixFlux and Pixen** (`create-image-pixflux`/`create-image-pixen` ↔ `create_image_pixflux`/`create_image_pixen`), **Pro image generation with labelled/style references** (`generate-image-v2` ↔ `create_image_pro`), **arbitrary-image edit** (`edit-image` ↔ `edit_image`), **arbitrary-image inpaint** (`inpaint` ↔ `inpaint_image`), and **raw text-driven animation** (`animate-with-text-v3` ↔ `animate_image`). There is no vocal / voice / lip-sync / audio animation capability on either surface as of these snapshots.

**Missing from MCP — REST v2 has it, no dedicated MCP tool (24 endpoints; ◐ = partial overlap via a broader tool).** See [REST v2 Endpoints With No MCP Counterpart](#rest-v2-endpoints-with-no-mcp-counterpart).

| Category | # | REST v2 endpoints |
|---|---|---|
| Raw image generation | 4 | `create-image-pixflux-background` (◐), `create-image-bitforge`, `generate-with-style-v2`, `generate-ui-v2` |
| Image edit / convert / resize | 5 | `edit-images-v2`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background` |
| Inpaint | 1 | `inpaint-v3` (◐) |
| Raw animation / rotation / skeleton | 10 | `animate-with-text`, `animate-with-text-v2`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, `rotate` |
| Prompt enhancement | 3 | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, `enhance-animation-v3-prompt` |
| Managed-asset ZIP export | 1 | `characters/{id}/zip` (the two `.../tags` PATCH routes now have MCP `update_character_tags` / `update_object_tags`) |

`create-image-pixen`, `create-image-pixflux`, and `generate-image-v2` are no longer in this list — they graduated to full `=` parity via `create_image_pixen`/`create_image_pixflux`/`create_image_pro` (2026-07-26 21:03 follow-up) and now live in the "full parity" prose above and the Coverage Matrix.

◐ **Partial overlap** (8 of the 24 — no *dedicated, tier-matched* MCP tool, but a broader or tier-unconfirmed MCP tool covers a scoped version). `create-image-pixflux-background` folds into MCP `create_image_pixflux(no_background=false)` — same tool as the now-fully-matched `create-image-pixflux`, but this is a background-removal-complexity variant, not a separate model, so it stays partial rather than graduating; `inpaint-v3`'s Pro tier is unconfirmed against the untagged `inpaint_image`; the `animate-with-text`/`-v2` family and `interpolation-v2` fold into MCP `animate_character`/`animate_object` via `mode` and the `custom_start_frame_base64`/`end_frame_base64` frame anchors, and `interpolation-v2` additionally overlaps raw (non-managed) `animate_image` via its `last_frame_base64` anchor — tier parity with the Pro `interpolation-v2` model is unconfirmed either way; `generate-8-rotations-v2`/`-v3` → `create_8_direction_object`/`create_character` 8-direction output; `characters/{id}/zip` → `get_character` download link. (`generate-with-style-v2` and `generate-ui-v2` are **not** here — `create_image_pro`'s single `style_image_base64`+`style_copy` does not match `generate-with-style-v2`'s multi-image `style_images`+`style_description` shape, and MCP's only UI tool, `create_ui_asset`, is a structured panel builder, not a freeform UI generator; see the UI note in the Coverage Matrix.) Per-endpoint notes are below.

**Missing from REST v2 — MCP has it, no REST endpoint (17 tools).** See [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

| Category | # | MCP tools |
|---|---|---|
| Projects | 1 | `list_projects` |
| Chat (game-building agent) | 3 | `chat_list_conversations`, `chat_get_messages`, `chat_send_message` |
| Sandbox (code execution) | 8 | `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync` |
| Deployed agents | 3 | `agent_list`, `agent_inspect`, `agent_talk` |
| MCP meta | 2 | `agent_help`, `agent_feedback` |

## Practical Picking Rule

MCP is a managed-asset tool layer inside an agent that, as of the 2026-07-26 refresh, also exposes six raw-image primitives needing no managed asset ID: `create_image_pixflux`, `create_image_pixen`, `create_image_pro` (each a dedicated model, not one generic tool), plus `get_image`, `edit_image`, `inpaint_image`, `animate_image`. REST v2 remains the complete HTTP API for the remaining model/version choices and code control.

| Use MCP when | Use REST v2 when |
|---|---|
| You're in an MCP-enabled agent and want a managed asset (character, object, tileset, tile, isometric, tiles-pro, font, portrait, UI panel, map object) with IDs, polling, and list/get/delete helpers, **or** raw PixFlux/Pixen/Pro image generate, edit, inpaint, or animate on a supplied image | You need BitForge (`coverage_percentage`), multi-image style reference (`generate-with-style-v2`), batch/code/backend control or exact schemas, or any of the 24 REST-only operations (multi-source edit, image-to-pixelart, resize, background removal, most raw animation/rotation/skeleton, prompt enhancement, ZIP export) |
| You need the platform layer — projects, chat, sandbox, deployed agents (MCP-only) | You need a freeform UI image (`generate-ui-v2`) or any capability with no MCP tool |

One line: **MCP is the convenient managed-asset path inside an agent, plus PixFlux/Pixen/Pro raw-image generate/edit/inpaint/animate; REST v2 remains the complete API for BitForge, multi-image style reference, code control, and the remaining REST-only operations.**

## Coverage Matrix

Parity legend (functional, not name-based): **=** covered by a dedicated MCP tool or a documented tool parameter; **~** covered only via an inferred, undocumented parameter value on a broader MCP tool; **◐** partial — a broader MCP tool produces the *same kind of output* in a scoped form (e.g., managed-asset-only), but no dedicated MCP tool exists. A merely adjacent MCP capability that yields a *different* asset type (e.g., a generation-time control such as `create_map_object`'s `inpainting`, or `style_images` on object creation) is **none** with a note, not ◐; **none** / **REST-only** no MCP tool documented. On multi-helper rows, `=` is capability-level (create + retrieve + list/delete). This matrix is comprehensive and REST-keyed — every REST v2 endpoint appears in a table below; MCP tools with no REST endpoint are listed separately in [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

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
| `PATCH /characters/{id}/tags` | `update_character_tags` | = |
| `POST /portrait-character-pro` | `create_portrait_character` + `get_portrait_character` | = |
| `DELETE /characters/{id}/animations` | `delete_animation` | = |

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
| `PATCH /objects/{id}/tags` | `update_object_tags` | = |
| `POST /map-objects`, `GET /map-objects/{id}` | `create_map_object` + `get_map_object` | = |

### Tiles & Tilesets

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-tileset`, `POST /tilesets`, `GET /tilesets`, `GET /tilesets/{id}`, `DELETE /tilesets/{id}` | `create_topdown_tileset`, `get_topdown_tileset`, `list_topdown_tilesets`, `delete_topdown_tileset` | = |
| `POST /create-tileset-sidescroller`, `POST /tilesets-sidescroller`, `GET /tilesets-sidescroller`, `GET /tilesets-sidescroller/{id}`, `DELETE /tilesets-sidescroller/{id}` | `create_sidescroller_tileset`, `get_sidescroller_tileset`, `list_sidescroller_tilesets`, `delete_sidescroller_tileset` | = |
| `POST /create-isometric-tile`, `GET /isometric-tiles`, `GET /isometric-tiles/{id}`, `DELETE /isometric-tiles/{id}` | `create_isometric_tile`, `list_isometric_tiles`, `get_isometric_tile`, `delete_isometric_tile` | = |
| `POST /create-tiles-pro`, `GET /tiles-pro`, `GET /tiles-pro/{id}`, `DELETE /tiles-pro/{id}` | `create_tiles_pro`, `get_tiles_pro`, `list_tiles_pro`, `delete_tiles_pro` | = |
| `POST /create-tiles-pro` (`tile_feature: "roads"`) | `create_path_tiles` (shares `get_tiles_pro`/`list_tiles_pro`/`delete_tiles_pro` — no dedicated getter) | = |
| `POST /create-tiles-pro` (`tile_feature: "building"`, `building_*` fields) | `create_building_kit` (shares `get_tiles_pro`/`list_tiles_pro`/`delete_tiles_pro` — no dedicated getter) | = |

### Fonts, UI, Account

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /generate-font-pro` | `create_font` + `get_font` | = |
| `POST /create-ui-asset`, `GET /ui-assets`, `GET /ui-assets/{id}`, `DELETE /ui-assets/{id}` | `create_ui_asset`, `list_ui_assets`, `get_ui_asset`, `delete_ui_asset` | = |
| `POST /generate-ui-v2` (freeform UI; no `pieces`/`elements`) | — (MCP has no freeform UI generator) | none |
| `GET /balance` | `get_balance` | = |
| `GET /background-jobs/{job_id}` | per-resource `get_*` tools | different model |

**Note on UI generation.** MCP `create_ui_asset` — structured `pieces`/`elements` with labeled sub-parts — has a full REST equivalent, `POST /create-ui-asset` (same `pieces`/`elements`, plus REST-only `style_image` and `project_id`); that is the `=` row above. REST's *other* UI endpoint, `POST /generate-ui-v2`, is a simpler freeform generator (text + optional `concept_image`, no `pieces`/`elements`) with **no** MCP counterpart — MCP exposes no freeform UI-image tool. Details: [`pixellab-ui-generation-surfaces-research.md`](pixellab-ui-generation-surfaces-research.md).

**Note on async retrieval and management rows.** Where a `=` row bundles MCP `get_*` / `list_*` helpers against a single REST `POST`, REST retrieval is via `GET /background-jobs/{job_id}` (the generic async poll) plus, where present, a dedicated GET such as `/tilesets/{id}`, `/isometric-tiles/{id}`, `/tiles-pro/{id}`, or `/characters/{id}`. So MCP `get_*` tools are never true gaps. As of the 2026-07-19 snapshot REST v2 also exposes the *list* routes for sidescroller tilesets (`GET /tilesets-sidescroller`) and tiles-pro (`GET /tiles-pro`), and *delete* routes for every tile/tileset family and for managed character animations — so these families now have full create/retrieve/list/delete parity on both surfaces. (Before 2026-07-19 the `list`/`delete` half was MCP-only.)

### Create Image (raw generation)

MCP briefly shipped a single generic `create_image` tool on 2026-07-26, then replaced it the same day (21:03 follow-up) with three model-specific tools mirroring REST's own split: `create_image_pixflux`, `create_image_pixen`, `create_image_pro` — each needs no managed asset and shares `get_image` as its getter. Field-for-field, `create_image_pixflux` matches `CreateImagePixfluxRequest` (`init_image`↔`init_image_base64`, `color_image`↔`color_image_base64`, `view`/`direction`/`isometric`/`outline`/`shading`/`detail`/`text_guidance_scale`/`no_background`/`seed`); `create_image_pixen` matches `CreateImagePixenRequest` (`view`/`direction`/`outline`/`detail`/`no_background`/`seed`); `create_image_pro` matches `GenerateImageV2Request` (`reference_images`↔`reference_images`, `style_image`↔`style_image_base64`, `style_options`↔`style_copy`, `image_size`↔`width`+`height`). REST-only extras on each (`background_removal_task`, deprecated `negative_description`, `enhance_prompt`) are minor and don't block full parity. (Freeform UI generation `generate-ui-v2` is grouped with the structured UI endpoint in *Fonts, UI, Account* above.)

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /create-image-pixen` | `create_image_pixen` + `get_image` | = |
| `POST /create-image-pixflux` | `create_image_pixflux` + `get_image` | = |
| `POST /create-image-pixflux-background` | `create_image_pixflux(no_background=false)` + `get_image` | ◐ |
| `POST /create-image-bitforge` (pose-guided via `skeleton_keypoints`) | — | none |
| `POST /generate-image-v2` (Pro) | `create_image_pro` + `get_image` | = |
| `POST /generate-with-style-v2` (Pro, style ref) | `create_image_pro`'s single `style_image_base64`+`style_copy` is a narrower shape than this endpoint's multi-image `style_images`(1-4)+`style_description`; `style_images` also appears on `create_1/8_direction_object`, `create_tiles_pro` (managed only, different output) | none |

### Image Edit, Convert, Resize

As of the 2026-07-26 refresh, MCP `edit_image` (pro) edits an arbitrary supplied image by text instruction or reference image — full parity with `edit-image`. `edit-images-v2`'s multi-*source* combine (several distinct images merged into one) is still a different operation from `edit_image`'s `images_base64` list (the *same* edit applied to each of several frames, e.g. animation directions), so that one stays a gap. Convert/resize/remove-background remain REST-only. `create_*_state` (managed asset variant by description) is a separate, unrelated operation from either.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /edit-image` | `edit_image` | = |
| `POST /edit-images-v2` (Pro, multi-source) | `edit_image(images_base64=[...])` applies one edit across several frames — a batch-consistency operation, not a multi-source combine | none |
| `POST /image-to-pixelart` | — | none |
| `POST /image-to-pixelart-pro` (Pro) | — | none |
| `POST /resize` | — | none |
| `POST /remove-background` | generation-time `no_background` only, not post-hoc removal | none |

### Inpaint

As of the 2026-07-26 refresh, MCP `inpaint_image` regenerates a masked region of an arbitrary supplied image (rectangular `mask_x/y/width/height` or a custom `mask_image_base64`) — full parity with base `inpaint`. It carries no `(pro)` tag, so treat `inpaint-v3`'s Pro tier as still unmatched.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /inpaint` | `inpaint_image` | = |
| `POST /inpaint-v3` (Pro) | `inpaint_image` covers the base inpaint capability but is not documented as Pro-tier | ◐ |

### Raw Animation, Rotation, Skeleton

As of the 2026-07-26 refresh, MCP `animate_image` is a standalone raw-animation tool — `first_frame_base64`+`action`, no managed asset required — that fully matches `animate-with-text-v3` and, via its optional `last_frame_base64`, also covers `interpolation-v2`'s start+end frame capability (tier vs Pro unconfirmed). Everything else keeps the prior shape: **API separates, MCP combines.** REST exposes animation as versioned, single-purpose endpoints; MCP additionally folds text animation and interpolation into managed `animate_character`/`animate_object`, selected by `mode` and the `custom_start_frame_base64`/`end_frame_base64` frame anchors (a start frame alone ≈ single-anchor animation; start **and** end ≈ interpolation). `animate-with-text`/`-v2` take a `reference_image` (a subject/style role, not a frame anchor, and not available on `animate_image` either), so they still overlap only partially via the text-animation capability, on the managed tools. Managed animation (`/animate-character`, `/characters/animations`, `/objects/{id}/animations` = `animate_*`) is a full `=` — see the Characters/Objects tables above.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /animate-with-text` (base; `reference_image`+`action`) | `animate_*(action_description)` (modern `mode="v3"`), managed | ◐ |
| `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) | `animate_*(action_description)`; no matching Pro/v2 mode is documented in MCP, managed | ◐ |
| `POST /animate-with-text-v3` (new; `first_frame`+`action`) | `animate_image(first_frame_base64, action)` — no managed asset needed | = |
| `POST /interpolation-v2` (Pro; `start_image`+`end_image`) | `animate_image(first_frame_base64, last_frame_base64)`, no managed asset, but not documented as Pro-tier | ◐ |
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

### 1. Raw image generation (4) — MCP now has PixFlux, Pixen, and Pro; BitForge and multi-image style remain gaps

MCP briefly shipped one generic `create_image` tool on 2026-07-26, then split it the same day (21:03 follow-up) into `create_image_pixflux`, `create_image_pixen`, and `create_image_pro`, each needing no managed asset and matching its REST counterpart field-for-field — closing three of the seven rows below outright:

- `POST /create-image-pixen` — = full parity: `create_image_pixen` + `get_image`
- `POST /create-image-pixflux` — = full parity: `create_image_pixflux` + `get_image`
- `POST /create-image-pixflux-background` — ◐ partial: `create_image_pixflux(no_background=false)` produces full-bleed images too, but this is a background-removal-complexity variant of the same tool, not a separate model
- `POST /create-image-bitforge` — none: no MCP tool has `coverage_percentage` (BitForge's one unique control) or `skeleton_keypoints` pose guidance
- `POST /generate-image-v2` (Pro) — = full parity: `create_image_pro` + `get_image` (`reference_images`, `style_image_base64`↔`style_image`, `style_copy`↔`style_options` all match)
- `POST /generate-with-style-v2` (Pro, style reference) — none: `create_image_pro`'s single `style_image_base64`+`style_copy` doesn't match this endpoint's multi-image `style_images`(1-4)+`style_description` shape
- `POST /generate-ui-v2` (freeform UI image; no `pieces`/`elements`) — none: MCP's only UI tool, `create_ui_asset`, is a structured panel builder (its REST twin is `create-ui-asset`), not a freeform generator, and lacks `concept_image`; MCP has no `generate-ui-v2` equivalent

### 2. Image edit / convert / resize (5) — MCP now edits arbitrary images, but not multi-source or convert/resize

Since 2026-07-26, MCP `edit_image` (pro) edits an arbitrary supplied image by text instruction or reference image — this closed the `edit-image` gap (now a full `=` match, see the Coverage Matrix). Still REST-only:

- `POST /edit-images-v2` (Pro, multi-source) — `edit_image(images_base64=[...])` applies the *same* edit across several frames (batch consistency), not a multi-source combine of several *different* images into one output
- `POST /image-to-pixelart`
- `POST /image-to-pixelart-pro` (Pro)
- `POST /resize`
- `POST /remove-background`

Note: MCP `create_map_object` may accept `background_image` / `inpainting` parameters. Those are map-object generation controls, not generic replacements for `edit-images-v2` or `inpaint-v3`.

### 3. Inpaint (1) — MCP now inpaints arbitrary images at base tier

Since 2026-07-26, MCP `inpaint_image` regenerates a masked region (rectangular or custom mask) of an arbitrary supplied image, closing the `inpaint` gap (now a full `=` match). Still open:

- `POST /inpaint-v3` (Pro) — ◐ partial: `inpaint_image` covers the base capability but carries no `(pro)` tag, so Pro-tier parity is unconfirmed

### 4. Raw animation, rotation, skeleton (10) — MCP now has a standalone raw-animation tool too

Since 2026-07-26, MCP `animate_image` animates an arbitrary supplied image directly — `first_frame_base64`+`action`, no managed asset — closing the `animate-with-text-v3` gap (now a full `=` match) and, via its optional `last_frame_base64`, partially covering `interpolation-v2` as well. MCP `animate_character` / `animate_object` separately require a managed `character_id`/`object_id` and **combine** the REST text-animation and interpolation endpoints into those two tools, selected by `mode` plus the `custom_start_frame_base64` / `end_frame_base64` frame anchors — so several rows below are still ◐ partial via that managed-asset path. Fully REST-only: skeleton/keypoint animation, animation-frame editing, outfit transfer, single-image rotate.

- `POST /animate-with-text` (base/legacy; `reference_image`+`action`) — ◐ partial: capability covered by MCP `animate_*` `action_description` (modern `mode="v3"`), managed asset only — `reference_image`'s subject/style role has no match on raw `animate_image` either
- `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) — ◐ partial: same as above, and MCP documents no matching Pro/v2 mode, so the version match is unconfirmed; managed asset only
- `POST /interpolation-v2` (Pro; `start_image`+`end_image`) — ◐ partial: MCP `animate_image(first_frame_base64, last_frame_base64)` covers the capability with no managed asset needed, but is not documented as Pro-tier; `animate_*(mode="v3", custom_start_frame_base64, end_frame_base64)` covers the managed-asset case
- `POST /generate-8-rotations-v2` (Pro) — ◐ partial: MCP `create_8_direction_object(reference_image_base64=…)` / `create_character(n_directions=8)` emit 8 directions, but regenerate the subject rather than rotating the exact input
- `POST /generate-8-rotations-v3` — ◐ partial: same managed-asset overlap as `-v2`
- `POST /edit-animation-v2` (Pro) — fully REST-only (no MCP tool edits arbitrary animation frames)
- `POST /transfer-outfit-v2` (Pro) — fully REST-only (no MCP outfit transfer)
- `POST /animate-with-skeleton` (`skeleton_keypoints`) — fully REST-only (MCP tools accept no keypoint arrays)
- `POST /estimate-skeleton` — fully REST-only
- `POST /rotate` (single arbitrary rotation) — fully REST-only

There is no public raw *4-rotation batch* route: the batch rotation routes are 8-direction only. The *managed* animation endpoints `/animate-character`, `/characters/animations`, `/objects/{id}/animations` are full `=` matches to MCP `animate_*` and appear in the Characters/Objects matrix tables, not this list. `animate-with-text-v3` is likewise a full `=` match now (via raw `animate_image`) and no longer appears in this gap list.

### 5. Prompt enhancement (3) — no MCP prompt-helper tools

MCP exposes `agent_help` (a docs Q&A knowledge agent), which is not a prompt rewriter:

- `POST /enhance-pixen-prompt`
- `POST /enhance-character-v3-prompt`
- `POST /enhance-animation-v3-prompt`

### 6. Managed-asset ZIP export (1) — MCP has create/get/list/delete/tags but not this

MCP covers the asset lifecycle except a full-bundle ZIP export:

- `GET /characters/{id}/zip` (full-bundle ZIP export) — ◐ partial: MCP `get_character` returns a download link, but no documented full-bundle ZIP export

(The `PATCH /characters/{id}/tags` and `PATCH /objects/{id}/tags` set-tags routes were listed here before 2026-07-19; MCP now covers them with `update_character_tags` / `update_object_tags`.)

### Not counted as asset gaps

- `GET /background-jobs/{job_id}` — REST's generic async poll. MCP deliberately uses per-resource `get_*` tools instead, so this is a different async model, not a missing capability.
- `GET /llms.txt` — the docs index itself, not an asset operation.

**Total: 24 asset/management REST v2 endpoints with no *dedicated, tier-matched* MCP counterpart** (4 image gen + 5 edit + 1 inpaint + 10 animation/rotation + 3 prompt enhance + 1 ZIP export). Of these, 8 have partial overlap via a broader or tier-unconfirmed MCP tool (◐): `create-image-pixflux-background`, `inpaint-v3`, the `animate-with-text` family (`animate-with-text`, `-v2`), `interpolation-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, and `characters/{id}/zip`.

## MCP Tools With No REST v2 Counterpart

The mirror of the gap list above: MCP tools with no public REST v2 endpoint. Grouped by why the gap exists. Of the 71 MCP tools in the snapshot, 17 have no REST v2 counterpart — all in the platform layer. (Before 2026-07-19 there were also 7 `delete`/`list` lifecycle helpers here; REST v2 has since added matching routes, and MCP added `update_character_tags` / `update_object_tags`.)

### Platform, agent, sandbox, chat (17) — genuinely MCP-only

No public REST v2 art API covers these; they exist only as MCP tools. Every platform tool except `get_balance` (which maps to `GET /balance`) is here. There is no REST fallback to offer — if these tools are not visible, the capability is unavailable.

- **Projects:** `list_projects`
- **Chat (game-building agent):** `chat_list_conversations`, `chat_get_messages`, `chat_send_message`
- **Sandbox (code execution):** `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`
- **Deployed agents:** `agent_list`, `agent_inspect`, `agent_talk`
- **MCP meta:** `agent_help` (docs Q&A knowledge agent), `agent_feedback`

Handle these per [`mcp-platform-tools.md`](../../skills/pixellab-pip/references/mcp-platform-tools.md) — most are account reads or state-changing actions that need explicit approval.

### Formerly MCP-only, now on REST too (as of 2026-07-19)

The 2026-07-19 snapshot added REST routes for the `delete` / `list` lifecycle helpers this section previously listed as MCP-only, so they are no longer gaps: `delete_topdown_tileset` (`DELETE /tilesets/{id}`), `delete_sidescroller_tileset` (`DELETE /tilesets-sidescroller/{id}`), `delete_isometric_tile` (`DELETE /isometric-tiles/{id}`), `delete_tiles_pro` (`DELETE /tiles-pro/{id}`), `delete_animation` (`DELETE /characters/{id}/animations`), `list_sidescroller_tilesets` (`GET /tilesets-sidescroller`), `list_tiles_pro` (`GET /tiles-pro`).

### Not counted as MCP-only

- Per-resource `get_*` tools map to a dedicated REST GET where one exists — `GET /generate-font-pro/{job_id}` (`get_font`), `GET /map-objects/{id}` (`get_map_object`), `GET /portrait-character-pro/{job_id}` (`get_portrait_character`), `GET /tilesets-sidescroller/{id}` (`get_sidescroller_tileset`) — and otherwise to the generic `GET /background-jobs/{job_id}` async poll. Either way they are not gaps.
- `pixellab://docs/...` resources (Godot/Unity/Python/Wang/sidescroller/isometric/overview integration guides) are MCP-only, but they are documentation, not an API surface.

**Total: 17 MCP tools with no REST v2 counterpart** — all in the platform layer. (The 7 `delete`/`list` lifecycle helpers counted here before 2026-07-19 now have REST routes.) The 2026-07-26 refresh and its same-day 21:03 follow-up together added 9 net MCP tools (62→71 total in the snapshot: +7 raw-image/tile-kit tools, then -1 `create_image` +3 `create_image_pixflux`/`create_image_pixen`/`create_image_pro`), but every one of them has a REST counterpart, so this platform-only count is unchanged.

## Routing Implications

These follow from the gaps above and are already encoded in SKILL.md's Intent Router and Surface Rules — this section states *why*, not new rules:

- Categories 1, 2 (multi-source only), 3 (Pro tier only), and 5 are why the Intent Router still sends model-specific/Pro image generation, multi-source edit, image-to-pixelart, resize, background removal, and prompt enhancement to REST v2 even in an MCP-enabled agent.
- Category 4 no longer means a user asking to "animate this sprite I attached" is REST-only — MCP `animate_image` now animates a raw supplied image directly, no managed character/object id needed. Skeleton/keypoint animation, animation-frame editing, outfit transfer, and single-image rotate remain REST-only.
- Managed asset types (character, object, tileset, tile, font, UI asset, map object) are the overlap zone: prefer MCP when its tools are visible, fall back to the matching REST endpoint otherwise. Raw-image generate/edit/inpaint/animate are now a second, smaller overlap zone (one generic MCP model vs REST's full model/version split).

## Caveats

- Snapshot-bound: both the MCP inventory and the REST index/OpenAPI are the 2026-07-26 cached snapshots. Both can drift; the doc-watch cache workflow ([`pixellab-doc-watch-cache.md`](pixellab-doc-watch-cache.md)) is how drift is detected.
- MCP↔REST are not guaranteed pixel-identical for the same prompt/seed even where parity is `=`; treat them as one workflow family with overlapping controls, REST generally exposing the fuller documented schema.
- `~` rows (`create-character-pro` and `create-character-v3` via the `create_character` `mode` parameter) are inferred capability mappings: the MCP snapshot documents `mode` with a `standard` default but does not enumerate `v3`/`pro` values, so the exact mapping is not proven from public docs. SKILL.md nonetheless defaults `create_character` to `mode="v3"`.
- This spike compares only public REST v2 and public MCP. Website/Map Workshop, Pixelorama/editor, Aseprite-extension, and legacy v1 routes are out of scope here; see [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md) for those surfaces.
