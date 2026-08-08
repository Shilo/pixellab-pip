# PixelLab MCP vs REST v2 Route Parity

Last reviewed: 2026-08-07.

> 2026-08-07 REST OpenAPI refresh: the inventory stayed at 79 REST paths and 76 MCP tools, but `GenerateWithStyleV2Request` changed. `image_size` is no longer required and remains only as an optional deprecated schema property; the endpoint now documents a square output derived from the largest dimension across its 1–4 `style_images` (bounded to 16–512). MCP had no corresponding schema change; its raw documentation changed only in the generated timestamp.

> 2026-08-06 refresh: REST v2 grew from 74 to 79 paths and MCP from 71 to 76 tools. Both surfaces now support attaching a portrait to a managed character, generating mood-specific vocal visemes, rendering a talking GIF, and producing a lip-sync timing plan. REST `POST /lip-sync` additionally supports stateless plans via `viseme_count`, while MCP `get_lip_sync` requires a managed character, so that row is partial. Counts are now 24 REST-only/partial endpoints (9 ◐), 17 MCP-only tools, and 76 total MCP tools. This refresh also added URL alternatives to the MCP raw-image tools, managed character/object style IDs on both surfaces, shared `state_name` fields, `drift_threshold` on REST animation v3, and removed the retired font `image_size` field.

> 2026-07-27 live behavior verification: the endpoint/tool shapes remain mapped as below, but equal
> request-schema coverage does not guarantee equal validation timing or successful semantics.
> `create_image_pixen` accepts 17px width through MCP, submits the job, then fails it with an
> internal 500; REST rejects the same request synchronously with 422 because its schema enforces a
> multiple-of-four dimension. `create_image_pixflux` rejects 16×16 through both surfaces because the
> live service also requires at least 1,024 total pixels. MCP and REST `inpaint-v3` produced the same
> faulty mask behavior in this run (the requested white region stayed unchanged while outside pixels
> changed), so they are mutually equivalent but both violate the documented mask contract. REST
> building generation also exposed a roughly 30-second top-level-status lag after
> `last_response.type=message_done`; MCP getters separately showed progress/ETA lag, including
> `processing 100%`. Pro reference-image composition worked, while partial and combined style-copy
> outputs did not visibly adopt the supplied gray-green palette; that is an output-fidelity finding,
> not a field-parity difference. A repeated failed Pixen job caused no net balance change. See
> `pixellab-mcp-new-tools-test-results.md` for the full matrix.

> 2026-07-26 live re-verification (post-split): every REST path in this doc re-checked against a freshly fetched `openapi.json` (74 paths) and every MCP tool name re-checked against a live reconnected MCP session (71 tools). The `create_image` → `create_image_pixflux`/`create_image_pixen`/`create_image_pro` split is confirmed live, and all counts below (23 REST-only, 8 ◐, 17 MCP-only, 71 MCP tools) hold. Two corrections, both misattributed field provenance rather than upstream drift: (1) `AnimateWithTextV3Request` carries its **own** optional `last_frame` ("Optional last frame to guide the animation endpoint"), so `animate_image` matches `animate-with-text-v3` field-complete (`first_frame`/`last_frame`/`action`/`frame_count`/`seed`/`no_background`; REST-only extra `enhance_prompt`) — and the `interpolation-v2` ◐ rests on *that v3 field*, not on an MCP capability beyond v3. It stays ◐, now for a confirmed reason rather than an unconfirmed one: the Pro `interpolation-v2` model itself is still unmatched. (2) `create_8_direction_object` takes a *single* `style_image`, not the plural `style_images` array — that array is on `create_1_direction_object` and `create_tiles_pro` only. Spot-confirmed unchanged and exact: `create-image-pixflux-background` still resolves to the identical `CreateImagePixfluxRequest`; `crop_to_mask` still exists only on `InpaintV3Request`; `EditImagesV2Request` still has `edit_images`+`method`+`reference_image` while base `EditImageRequest` has single `image`+`color_image`+`text_guidance_scale`; `usage_description` still present on `generate_image_v2`'s `ReferenceImage`; `StyleOptions` is still the four booleans matching `style_copy`; `tile_feature` is still `roads`/`tileset`/`building` on REST while MCP's `create_tiles_pro` accepts only `"tileset"`.
>
> 2026-07-26 re-audit: a full field-by-field re-check of every REST request schema against every MCP tool description (not just the diffed changes) found four more corrections beyond the two refresh notes below — none from new upstream drift, all from closer reading of the same cached snapshot: (1) `create-image-pixflux-background` uses the byte-identical `CreateImagePixfluxRequest` schema as `create-image-pixflux` (same Pydantic model, confirmed via the raw OpenAPI path definitions) — it graduates from ◐ to full `=` via `create_image_pixflux`. (2) MCP `edit_image` is documented "(pro)" and takes a *list* of images plus an optional reference-image mode switch — that is `EditImagesV2Request`'s shape (`edit_images` list + `method`: text/reference + `reference_image`), not base `EditImageRequest` (single image, text-only, has `color_image`/`text_guidance_scale` that `edit_image` lacks). The base/Pro assignment was backwards: `edit-images-v2` is now the `=` match, base `edit-image` is ◐ (partial, via the broader Pro tool). (3) Same root cause for inpaint: MCP `inpaint_image` has `crop_to_mask`, a field that exists **only** on `InpaintV3Request` — base `InpaintRequest` has no such field and instead carries a pile of PixFlux-style weak-guidance controls (`direction`/`isometric`/`shading`/`outline`/`detail`/`text_guidance_scale`/`init_image`/`color_image`) that `inpaint_image` doesn't have. `inpaint-v3` is now the `=` match, base `inpaint` is ◐. (4) `DELETE /objects/{object_id}/animations` — the object-side twin of the already-listed `DELETE /characters/{character_id}/animations` — was missing from the Coverage Matrix entirely; `delete_animation`'s own docstring confirms it handles both characters and objects, so this is `=`, not a gap, and was never counted as one. Re-verified and unchanged: `create_image_pro` ↔ `generate-image-v2` is airtight — even the nested `usage_description` field on REST's `reference_images` array matches the MCP tool's "usage" label name-for-name. Counts below reflect the corrected state (REST-only 24→23; composition of the 8 ◐ items changed but the count didn't).
>
> 2026-07-26 21:03 follow-up: within the same day, MCP replaced the brand-new generic `create_image` with three model-specific tools matching REST's own image-model split: `create_image_pixflux`, `create_image_pixen`, and `create_image_pro` (via matching `reference_images`/`style_image_base64`/`style_copy` fields — but not `generate-with-style-v2`, whose `style_images` array + `style_description` shape it does not match). `get_image` is unchanged (shared getter, now documented as returning `create_image_pixflux` results too). This closed 3 of the 7 "Raw image generation" gaps outright at the time (bitforge, `generate-with-style-v2`, and `generate-ui-v2` remained REST-only; the re-audit above found a 4th, `create-image-pixflux-background`). Counts at the time reflected REST-only 27→24, MCP tool count 69→71, ◐ 9→8.
>
> 2026-07-26 refresh: MCP added 7 tools closing most of the former "MCP has no raw-image primitive" gap: `create_image`+`get_image` (generic text-to-image, ◐ partial vs the model-split REST image routes — see the 21:03 follow-up above, this tool was replaced within the hour), `edit_image` (= full parity with `edit-image`), `inpaint_image` (= full parity with `inpaint`), `animate_image` (= full parity with `animate-with-text-v3`, ◐ partial vs `interpolation-v2` — tier unconfirmed), and `create_path_tiles`/`create_building_kit` (= full parity, siblings of `create_tiles_pro` sharing its get/list/delete tools; REST folds all three into `create-tiles-pro` via `tile_feature: "roads"/"tileset"/"building"`). None of these are new REST surface — REST already had `edit-image`, `inpaint`, `animate-with-text-v3`, and the `tile_feature`/`building_*` fields on `create-tiles-pro`; MCP simply exposes them now. Counts at the time reflected REST-only 30→27, MCP tool count 62→69, MCP-only still 17.
>
> 2026-07-19 refresh: REST v2 added `DELETE` routes for tilesets, sidescroller tilesets, isometric tiles, tiles-pro, and managed character animations, plus `GET` list routes for sidescroller tilesets and tiles-pro — closing the seven "MCP-only delete/list helper" gaps this doc previously listed. MCP added `update_character_tags` / `update_object_tags`, closing the two `PATCH .../tags` "REST-only" gaps. Counts below reflect the new state (REST-only 32→30, MCP-only 24→17).

Purpose: a route-level comparison of PixelLab's hosted MCP tool surface against the public REST v2 API — the missing features both ways: every REST v2 asset/management endpoint with no MCP counterpart, and every MCP tool with no REST v2 counterpart. (Two non-asset REST infrastructure routes are handled separately below.) This is the parity map behind SKILL.md's rule "do not assume a REST endpoint has an MCP equivalent just because MCP is configured." It complements the *service*-level comparison in [Official PixelLab MCP Service Comparison](../tools/official-pixellab-mcp-service-comparison.md) and the *label*-level crosswalk in [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md); this file is the *endpoint*-level view.

## Snapshots Compared

Parity is a moving target because both surfaces ship independently. This review compares:

- **REST v2 index:** `https://api.pixellab.ai/v2/llms.txt`, cross-checked against `https://api.pixellab.ai/v2/openapi.json`, cached snapshot 2026-08-07. `llms.txt` is the curated published index; OpenAPI is the fuller machine-readable schema. Where both agree a route is absent, it is treated as genuinely absent, not an index abbreviation.
- **MCP inventory:** `https://api.pixellab.ai/mcp/docs`, auto-generated snapshot 2026-08-07 (cached locally). This is the authoritative public MCP tool list; the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` is not.

Absence from a snapshot is not proof of absence from the live API. When a route or tool matters for code, re-verify against current OpenAPI/MCP docs (SKILL.md → Current Docs Refresh).

## How To Read This

Three surfaces are conflated in casual usage; they are not the same contract:

- **MCP tools** are called through an MCP client (bare or host-prefixed such as `mcp__pixellab__create_character`). They are not HTTP paths; do not curl a tool name as `/v2/...`.
- **REST v2 endpoints** are HTTP paths under `https://api.pixellab.ai/v2`.
- **Managed-asset animation** (`/animate-character`, `/characters/animations`, `/objects/{id}/animations`) and **raw animation** (`/animate-with-text*`, `/animate-with-skeleton`, `/interpolation-v2`, …) are different endpoint families. MCP `animate_character`/`animate_object` cover managed assets, while `animate_image` takes preferred frame URLs or inline base64 directly. It functionally matches `animate-with-text-v3` and partially covers interpolation at v3 tier; REST retains `drift_threshold`, prompt enhancement, skeleton/keypoint animation, frame editing, outfit transfer, and single-image rotate controls.

## At a Glance

**Matching basis:** counterparts are judged by **functional capability, not tool name** — a REST endpoint counts as "covered" if any MCP tool or documented MCP parameter does the same job, even under a different name or bundled into a broader tool (and the reverse for MCP tools). A scoped or partial overlap (for example, an MCP capability that works only on a managed asset) is marked partial (◐), not dropped.

**On both surfaces — full functional parity, so they live in the [Coverage Matrix](#coverage-matrix) below, not in the gap lists:** characters (4/8-direction, v3, pro, state, animate, list/get/delete), **portrait ↔ character conversion** (`portrait-character-pro` ↔ `create_portrait_character`), **managed portraits and talking output** (portrait attachment, vocal-viseme generation, and talking GIF rendering), objects (1/8-direction, state, animate, review, list/get/delete, **including per-object animation delete** — `DELETE /objects/{id}/animations` ↔ `delete_animation`), map objects, top-down / sidescroller / isometric / pro tilesets & tiles, **path/road tiles and building kits** (`create-tiles-pro` `tile_feature` ↔ `create_path_tiles`/`create_building_kit`), structured UI assets, **pixel font Pro** (`generate-font-pro` ↔ `create_font`), balance, **tag setting** (`PATCH .../tags` ↔ `update_character_tags` / `update_object_tags`), **raw text-to-image on PixFlux (both the base and background-oriented path share one identical schema) and Pixen** (`create-image-pixflux`/`create-image-pixflux-background`/`create-image-pixen` ↔ `create_image_pixflux`/`create_image_pixen`), **Pro image generation with labelled/style references** (`generate-image-v2` ↔ `create_image_pro`), **arbitrary-image edit at Pro tier** (`edit-images-v2` ↔ `edit_image`), **arbitrary-image inpaint at Pro tier** (`inpaint-v3` ↔ `inpaint_image`), and **raw text-driven animation** (`animate-with-text-v3` ↔ `animate_image`). Lip-sync planning overlaps too, but only partially because MCP lacks REST's stateless form.

**Missing from MCP — REST v2 has it, no dedicated or fully equivalent MCP tool (24 endpoints; ◐ = partial overlap via a broader or narrower tool).** See [REST v2 Endpoints With No MCP Counterpart](#rest-v2-endpoints-with-no-mcp-counterpart).

| Category | # | REST v2 endpoints |
|---|---|---|
| Raw image generation | 3 | `create-image-bitforge`, `generate-with-style-v2`, `generate-ui-v2` |
| Image edit / convert / resize | 5 | `edit-image` (◐), `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background` |
| Inpaint | 1 | `inpaint` (◐) |
| Raw animation / rotation / skeleton | 10 | `animate-with-text`, `animate-with-text-v2`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, `rotate` |
| Prompt enhancement | 3 | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, `enhance-animation-v3-prompt` |
| Managed-asset ZIP export | 1 | `characters/{id}/zip` (the two `.../tags` PATCH routes now have MCP `update_character_tags` / `update_object_tags`) |
| Talking portraits | 1 | `lip-sync` (◐: MCP is managed-character only; REST also supports stateless `viseme_count`) |

`create-image-pixen`, `create-image-pixflux`, `create-image-pixflux-background`, `generate-image-v2`, `edit-images-v2`, and `inpaint-v3` are no longer in this list — they graduated to full `=` parity (see the 2026-07-26 re-audit note above) and now live in the "full parity" prose and the Coverage Matrix. Base `edit-image` and base `inpaint` newly *entered* this list in their place — the earlier snapshot had the base/Pro assignment backwards for both families.

◐ **Partial overlap** (9 of the 24 — no *dedicated, tier-matched* MCP tool, or MCP covers only a narrower form). The existing eight are base `edit-image`, base `inpaint`, `animate-with-text`, `animate-with-text-v2`, `interpolation-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, and `characters/{id}/zip`. The ninth is `lip-sync`: MCP returns the same managed-character plan, but only REST can produce a stateless plan from `viseme_count`. Per-endpoint notes are below.

**Missing from REST v2 — MCP has it, no REST endpoint (17 tools).** See [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

| Category | # | MCP tools |
|---|---|---|
| Projects | 1 | `list_projects` |
| Chat (game-building agent) | 3 | `chat_list_conversations`, `chat_get_messages`, `chat_send_message` |
| Sandbox (code execution) | 8 | `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_write`, `sandbox_edit`, `sandbox_sync` |
| Deployed agents | 3 | `agent_list`, `agent_inspect`, `agent_talk` |
| MCP meta | 2 | `agent_help`, `agent_feedback` |

## Practical Picking Rule

MCP is a managed-asset tool layer inside an agent that also exposes seven raw-image primitives plus talking-portrait helpers. REST v2 remains the complete HTTP API for the remaining model/version choices, stateless lip sync, and code control.

| Use MCP when | Use REST v2 when |
|---|---|
| You're in an MCP-enabled agent and want a managed asset with IDs and lifecycle helpers, raw PixFlux/Pixen/Pro-tier image work, or a managed talking-portrait workflow | You need BitForge, multi-image style reference, base-tier edit/inpaint controls, stateless lip sync, batch/code/backend control, exact schemas, or any of the 24 REST-only/partial operations |
| You need the platform layer — projects, chat, sandbox, deployed agents (MCP-only) | You need a freeform UI image (`generate-ui-v2`) or any capability with no MCP tool |

One line: **MCP is the convenient managed-asset, raw-image, and managed talking-portrait path inside an agent; REST v2 remains the complete API for stateless lip sync, exact code control, and the remaining REST-only operations.**

## Coverage Matrix

Parity legend (functional, not name-based): **=** covered by a dedicated MCP tool or a documented tool parameter; **~** covered only via an inferred, undocumented parameter value on a broader MCP tool; **◐** partial — a broader MCP tool produces the *same kind of output* in a scoped form (e.g., managed-asset-only), but no dedicated MCP tool exists. A merely adjacent MCP capability that yields a *different* asset type (e.g., a generation-time control such as `create_map_object`'s `inpainting`, or `style_images` on object creation) is **none** with a note, not ◐; **none** / **REST-only** no MCP tool documented. On multi-helper rows, `=` is capability-level (create + retrieve + list/delete). This matrix is comprehensive and REST-keyed — every REST v2 endpoint appears in a table below; MCP tools with no REST endpoint are listed separately in [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

### Characters

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-character-with-4-directions` | `create_character(n_directions=4)` | = |
| `POST /create-character-with-8-directions` | `create_character(n_directions=8)` | = |
| `POST /create-character-v3` | `create_character(mode="v3")` | = |
| `POST /create-character-pro` | `create_character(mode="pro")` | ◐ |
| `POST /create-character-state` | `create_character_state` | = |
| `POST /animate-character`, `POST /characters/animations` | `animate_character` | = |
| `GET /characters` | `list_characters` | = |
| `GET /characters/{id}` | `get_character` | = |
| `DELETE /characters/{id}` | `delete_character` | = |
| `GET /characters/{id}/zip` | `get_character` download link (no full ZIP bundle) | ◐ |
| `PATCH /characters/{id}/tags` | `update_character_tags` | = |
| `POST /portrait-character-pro` | `create_portrait_character` + `get_portrait_character` | = |
| `POST /characters/{id}/portrait` | `set_character_portrait` | = |
| `POST /vocal-animation`, `GET /vocal-animation/{job_id}` | `create_vocal_animation` + `get_vocal_animation` | = |
| `POST /talking-gif` | `create_talking_gif` | = |
| `POST /lip-sync` | `get_lip_sync` covers managed characters; REST also accepts stateless `viseme_count` | ◐ |
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
| `DELETE /objects/{id}/animations` | `delete_animation` (same tool as the character row above — its docstring explicitly covers "a character or object") | = |
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

MCP's three model-specific raw-image tools mirror REST's PixFlux, Pixen, and Pro split and share `get_image`. Their generation controls provide functional parity, while MCP additionally accepts preferred URL forms for PixFlux init/color images and Pro reference/style images. REST retains a few route-specific extras such as `background_removal_task`, deprecated `negative_description`, and `enhance_prompt`. `POST /create-image-pixflux-background` still uses the same `CreateImagePixfluxRequest` as `/create-image-pixflux`, so one MCP tool covers both URLs.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /create-image-pixen` | `create_image_pixen` + `get_image` | = |
| `POST /create-image-pixflux` | `create_image_pixflux` + `get_image` | = |
| `POST /create-image-pixflux-background` | `create_image_pixflux` + `get_image` — byte-identical request schema (`CreateImagePixfluxRequest`) to the row above | = |
| `POST /create-image-bitforge` (`coverage_percentage`, `skeleton_keypoints`/`skeleton_guidance_scale` pose guidance, `inpainting_image`/`mask_image`, `style_image`/`style_strength`) | — no MCP tool combines any of BitForge's unique controls | none |
| `POST /generate-image-v2` (Pro) | `create_image_pro` + `get_image` | = |
| `POST /generate-with-style-v2` (Pro, style ref) | `create_image_pro`'s single style image (URL or base64) plus `style_copy` is narrower than this endpoint's required 1–4-image `style_images` array with optional `style_description`; REST derives a square output size from the style images rather than accepting a supported `image_size` control | none |

### Image Edit, Convert, Resize

**Re-audit correction:** MCP `edit_image` is the Pro workflow matching `EditImagesV2Request`: it accepts 1–16 edit targets plus optional reference mode, now through preferred URLs or inline base64. Base `EditImageRequest` is text-only and has `color_image`/`text_guidance_scale`, so it remains only partially covered. Convert/resize/remove-background remain REST-only.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /edit-image` (base; single `image`, text-only, has `color_image`/`text_guidance_scale`) | `edit_image` can perform a single-image, text-only edit as a subset of its range, but is fundamentally the Pro/batch/reference-mode tool, not a dedicated base-tier match | ◐ |
| `POST /edit-images-v2` (Pro; `edit_images` list of 1-16, `method`: text or reference) | `edit_image` — matches the list-of-images shape and the text-vs-reference mode switch; MCP's own docstring tags it "(pro)" | = |
| `POST /image-to-pixelart` | — | none |
| `POST /image-to-pixelart-pro` (Pro) | — | none |
| `POST /resize` | — | none |
| `POST /remove-background` | generation-time `no_background` only, not post-hoc removal | none |

### Inpaint

**Re-audit correction:** the prior snapshot had the base/Pro assignment backwards here too. MCP `inpaint_image` has a `crop_to_mask` field ("Confine generated content to the mask boundary for clean edges") — that field exists **only** on `InpaintV3Request` (`"Whether to crop generated content to mask boundary (ensures clean edges)"`, worded almost identically). Base `InpaintRequest` has no `crop_to_mask` at all, and instead carries a full set of PixFlux-style weak-guidance generation controls (`direction`, `isometric`, `shading`, `outline`, `detail`, `text_guidance_scale`, `init_image`, `color_image`, `negative_description`, `extra_guidance_scale`, `oblique_projection`) that `inpaint_image` does not expose. `inpaint_image`'s rectangular `mask_x/y/width/height` shorthand doesn't map to a live REST field either way — `InpaintV3Request`'s own `bounding_box` is explicitly marked `"(deprecated)"` in its description, so MCP likely builds a full `mask_image` internally rather than calling a deprecated field. Net: `inpaint-v3` is the full `=` match; base `inpaint` drops to ◐.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /inpaint` (base; no `crop_to_mask`, has `direction`/`isometric`/`shading`/`outline`/`detail`/`text_guidance_scale`/`init_image`/`color_image`) | `inpaint_image` covers the core mask-regenerate job but lacks all of base's extra weak-guidance controls, and is fundamentally the Pro-shaped tool, not a dedicated base-tier match | ◐ |
| `POST /inpaint-v3` (Pro; `crop_to_mask`, `bounding_box`/`context_image` both marked deprecated) | `inpaint_image` — matches on `crop_to_mask` and the white=generate/black=preserve mask convention | = |

### Raw Animation, Rotation, Skeleton

MCP `animate_image` is a standalone raw-animation tool — preferred frame URLs or inline base64 plus `action`, no managed asset required — that functionally matches `animate-with-text-v3`, including its optional `last_frame`. REST now additionally exposes `drift_threshold` and `enhance_prompt`, so the match is not field-complete. The same MCP last-frame anchor partially reaches the Pro `interpolation-v2` capability through the v3 model. Managed animation remains a separate full-parity family.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /animate-with-text` (base; `reference_image`+`action`) | `animate_*(action_description)` (modern `mode="v3"`), managed | ◐ |
| `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) | `animate_*(action_description)`; no matching Pro/v2 mode is documented in MCP, managed | ◐ |
| `POST /animate-with-text-v3` (new; `first_frame`+optional `last_frame`+`action`) | `animate_image` — no managed asset needed; functionally equivalent, but REST additionally exposes `drift_threshold` and `enhance_prompt`, while MCP accepts frame URLs | = |
| `POST /interpolation-v2` (Pro; *required* `start_image`+`end_image`) | `animate_image(first_frame_base64, last_frame_base64)` reaches the same start+end capability — but that `last_frame_base64` is `animate-with-text-v3`'s own optional `last_frame`, so this is the v3 model doing interpolation, not the Pro `interpolation-v2` model | ◐ |
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

### 1. Raw image generation (3) — MCP now has PixFlux, Pixen, and Pro (both PixFlux paths included); BitForge and multi-image style remain gaps

MCP briefly shipped one generic `create_image` tool on 2026-07-26, then split it the same day (21:03 follow-up) into `create_image_pixflux`, `create_image_pixen`, and `create_image_pro`, each needing no managed asset and matching its REST counterpart field-for-field — closing four of the seven rows below outright (a re-audit found the fourth: `create-image-pixflux-background` uses the byte-identical `CreateImagePixfluxRequest` schema, confirmed from the raw OpenAPI path definitions, not just a same-named coincidence):

- `POST /create-image-pixen` — = full parity: `create_image_pixen` + `get_image`
- `POST /create-image-pixflux` — = full parity: `create_image_pixflux` + `get_image`
- `POST /create-image-pixflux-background` — = full parity: same tool, same schema (`CreateImagePixfluxRequest`) — this is a second URL for the identical operation, not a distinct model
- `POST /create-image-bitforge` — none: no MCP tool has `coverage_percentage` (BitForge's one unique control), `skeleton_keypoints`/`skeleton_guidance_scale` pose guidance, or its `inpainting_image`/`mask_image`/`style_image`/`style_strength` combination
- `POST /generate-image-v2` (Pro) — = functional parity: `create_image_pro` + `get_image`; MCP also accepts reference/style URLs
- `POST /generate-with-style-v2` (Pro, style reference) — none: `create_image_pro` takes one style image (URL or base64), not this route's required 1–4-image `style_images` array; REST derives the square output size from those images and exposes no supported `image_size` control
- `POST /generate-ui-v2` (freeform UI image; no `pieces`/`elements`) — none: MCP's only UI tool, `create_ui_asset`, is a structured panel builder (its REST twin is `create-ui-asset`), not a freeform generator, and lacks `concept_image`; MCP has no `generate-ui-v2` equivalent

### 2. Image edit / convert / resize (5) — MCP's edit tool is Pro-tier (edit-images-v2), not base edit-image

**Re-audit correction:** MCP `edit_image` is tagged **"(pro)"** in its own description and takes a *list* of images plus an optional reference-image mode switch — that shape matches `EditImagesV2Request` (`edit_images` list of 1-16 + `method`: text/reference + `reference_image`), not base `EditImageRequest` (single `image`, text-only, has `color_image`/`text_guidance_scale` that `edit_image` lacks). So `edit-images-v2` is the full `=` match; base `edit-image` is ◐ (a scoped subset of the broader Pro tool). Still REST-only or partial:

- `POST /edit-image` (base) — ◐ partial: `edit_image` can perform a single-image, text-only edit as a subset of its range, but is the Pro/batch tool, not a dedicated base-tier match
- `POST /image-to-pixelart`
- `POST /image-to-pixelart-pro` (Pro)
- `POST /resize`
- `POST /remove-background`

Note: MCP `create_map_object` may accept `background_image` / `inpainting` parameters. Those are map-object generation controls, not generic replacements for `edit-image` or `inpaint`.

### 3. Inpaint (1) — MCP's inpaint tool is Pro-tier (inpaint-v3), not base inpaint

**Re-audit correction:** MCP `inpaint_image` has a `crop_to_mask` field that exists **only** on `InpaintV3Request` — base `InpaintRequest` has no such field and instead carries PixFlux-style weak-guidance controls (`direction`, `isometric`, `shading`, `outline`, `detail`, `text_guidance_scale`, `init_image`, `color_image`) that `inpaint_image` doesn't expose. So `inpaint-v3` is the full `=` match; base `inpaint` is ◐. Still open:

- `POST /inpaint` (base) — ◐ partial: `inpaint_image` covers the core mask-regenerate job but lacks base's extra weak-guidance generation controls, and is fundamentally the Pro-shaped tool, not a dedicated base-tier match

### 4. Raw animation, rotation, skeleton (10) — MCP now has a standalone raw-animation tool too

MCP `animate_image` animates an arbitrary supplied image directly from frame URLs or inline base64, closing the core `animate-with-text-v3` gap and partially covering interpolation at v3 tier. MCP `animate_character` / `animate_object` separately require managed assets. Fully REST-only: skeleton/keypoint animation, animation-frame editing, outfit transfer, and single-image rotate.

- `POST /animate-with-text` (base/legacy; `reference_image`+`action`) — ◐ partial: capability covered by MCP `animate_*` `action_description` (modern `mode="v3"`), managed asset only — `reference_image`'s subject/style role has no match on raw `animate_image` either
- `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) — ◐ partial: same as above, and MCP documents no matching Pro/v2 mode, so the version match is unconfirmed; managed asset only
- `POST /interpolation-v2` (Pro; *required* `start_image`+`end_image`) — ◐ partial: MCP `animate_image(first_frame_base64, last_frame_base64)` covers the capability with no managed asset needed, but `last_frame_base64` is `animate-with-text-v3`'s own optional `last_frame` field — so it is the v3 model interpolating, not the Pro `interpolation-v2` model; `animate_*(mode="v3", custom_start_frame_base64, end_frame_base64)` covers the managed-asset case
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

### 7. Talking portraits (1) — MCP lip sync is managed-character only

- `POST /lip-sync` — ◐ partial: MCP `get_lip_sync` returns the same plan for a character with stored visemes, but REST can also produce a stateless plan from `viseme_count` without a managed character. Portrait attachment, vocal animation create/get, and talking GIF rendering have full MCP counterparts.

### Not counted as asset gaps

- `GET /background-jobs/{job_id}` — REST's generic async poll. MCP deliberately uses per-resource `get_*` tools instead, so this is a different async model, not a missing capability.
- `GET /llms.txt` — the docs index itself, not an asset operation.

**Total: 24 asset/management REST v2 endpoints with no fully equivalent, dedicated MCP counterpart** (3 image gen + 5 edit + 1 inpaint + 10 animation/rotation + 3 prompt enhance + 1 ZIP export + 1 talking-portrait route). Nine have partial overlap: the previous eight plus stateless `lip-sync`.

## MCP Tools With No REST v2 Counterpart

The mirror of the gap list above: MCP tools with no public REST v2 endpoint. Grouped by why the gap exists. Of the 76 MCP tools in the snapshot, 17 have no REST v2 counterpart — all in the platform layer.

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

**Total: 17 MCP tools with no REST v2 counterpart** — all in the platform layer. The five talking-portrait tools added in this refresh all have REST counterparts, so this count is unchanged.

## Routing Implications

These follow from the gaps above and are already encoded in SKILL.md's Intent Router and Surface Rules — this section states *why*, not new rules:

- Category 1 (BitForge, multi-image style, freeform UI), category 2's base `edit-image` (◐, not a dedicated match — route there when the extra `color_image`/`text_guidance_scale` controls matter or Pro-tier `edit_image` overreaches) and its remaining `image-to-pixelart`/`resize`/`remove-background` gaps, category 3's base `inpaint` (◐, same reasoning — its weak-guidance controls aren't on `inpaint_image`), and category 5 are why the Intent Router still sends those specific operations to REST v2 even in an MCP-enabled agent.
- Category 4 no longer means a user asking to "animate this sprite I attached" is REST-only — MCP `animate_image` now animates a raw supplied image directly, no managed character/object id needed. Skeleton/keypoint animation, animation-frame editing, outfit transfer, and single-image rotate remain REST-only.
- Managed asset types (character, object, tileset, tile, font, UI asset, map object) are the overlap zone: prefer MCP when its tools are visible, fall back to the matching REST endpoint otherwise. Raw-image generate/edit/inpaint/animate are now a second overlap zone: MCP covers PixFlux, Pixen, and Pro-tier generate/edit/inpaint/animate; REST remains necessary for BitForge, multi-image style reference, and the base (non-Pro) edit/inpaint tiers.

## Caveats

- Snapshot-bound: both the MCP inventory and the REST index/OpenAPI are the 2026-08-07 cached snapshots. Both can drift; the doc-watch cache workflow ([`pixellab-doc-watch-cache.md`](pixellab-doc-watch-cache.md)) is how drift is detected.
- MCP↔REST are not guaranteed pixel-identical for the same prompt/seed even where parity is `=`; treat them as one workflow family with overlapping controls, REST generally exposing the fuller documented schema.
- Re-audit correction: `create_character`'s `mode` is now documented as `Literal["standard", "pro", "v3"]` with per-value cost and behavior text (this doc previously said the MCP snapshot didn't enumerate `v3`/`pro` — that was stale). `create-character-v3` ↔ `create_character(mode="v3")` is now `=`: fields match (`description`, `detail`, `outline`, `view`, `reference_image_base64`/`reference_image`, `size`/`image_size`, `name`, `seed`), and MCP docs explicitly say v3 "is the only mode that accepts `reference_image_base64` (rotate an existing sprite)" — the exact REST v3 capability. `create-character-pro` ↔ `create_character(mode="pro")` is only `◐`: REST's `method` (`create_with_style`/`create_from_concept`/`rotate_character`), `concept_image`, and `style_description` have no MCP counterpart, and MCP's `mode="pro"` rejects `reference_image_base64` (v3-only) — so REST pro's `rotate_character`/`create_from_concept` methods are REST-only. SKILL.md's default of `create_character` to `mode="v3"` is well-supported by this.
- This spike compares only public REST v2 and public MCP. Website/Map Workshop, Pixelorama/editor, Aseprite-extension, and legacy v1 routes are out of scope here; see [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md) for those surfaces.
- Methodology note (2026-07-26 re-audit): base-vs-Pro tier assignments in this doc are now checked by diffing full REST request-schema field lists (property names, required lists, and descriptions) against each MCP tool's documented parameters and its own prose tags (e.g. a tool's description literally saying "(pro)"), not by matching on name similarity alone. Two families (`edit-image`/`edit-images-v2`, `inpaint`/`inpaint-v3`) had the base/Pro assignment backwards in an earlier pass specifically because the base-tier endpoint's name is the more obvious lexical match to the MCP tool's name, even though its field shape didn't match. Treat any future "obviously-named" match in this doc as unconfirmed until the schema fields are actually compared.
