# PixelLab MCP vs REST v2 Route Parity

Last reviewed: 2026-10-29 (UTC snapshot).

> **2026-10-29 UTC refresh:** all seven public sources completed without failure. Inventories remain **102 REST path templates (113 operations), 275 schemas, and 118 MCP tools**, with no route/tool additions or removals; the 29 REST-only/partial operations and 40 MCP-only tools are unchanged. REST `POST /generate-font-pro` and MCP `create_font` add `glyph_px` 12 and 24 (now 8/12/16/24/32/64). REST `POST /create-tiles-pro` and MCP `create_tiles_pro` revise the generation estimate from 15–30 seconds to 1–2 minutes. MCP now renders numeric validation bounds across existing parameters, documents exact humanoid template frame counts and rejected invented ids, reiterates that `create_character` has no seed, and accepts JSON-string `direction_images` for clients unable to send an object. Its Pro Flash creation/edit/inpaint guidance now quotes a 5/6/9-generation longest-side ladder plus separate rotations, with free exact-size estimates through the existing `get_pro_flash_capabilities`; REST's unchanged provisional five-generation text is not a ceiling for those MCP prices. UI and Pro edit costs now explain aspect-adjusted bands. MCP also documents a 16-independent-tile limit and clarifies map-compatible implicit-height isometric floors; unblended terrain pairs now meet at a hard seam rather than black tiles. See the focused references for operational details. Website changes are build hashes/IDs only; REST `llms.txt` and both docs shells are unchanged.

> **2026-10-25 live follow-up:** a fresh comparison of the official [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json), [REST endpoint index](https://api.pixellab.ai/v2/llms.txt), and [MCP tool guide](https://api.pixellab.ai/mcp/docs) confirms **102 REST path templates (113 operations), 275 schemas, and 118 MCP tools**. No route or tool was added or removed since the preceding snapshot. Reclassifying the existing routes yields **29 REST operations without a full dedicated MCP match** (16 partial, 13 with no documented overlap) and **40 MCP tools without a REST workflow counterpart**. The MCP docs now cover exact-pixel and batched map-object placement (including layer-only moves), saving a full sheet over an existing top-down or sidescroller tileset, linking saved VFX effects into projects, and the `roof_profile` control for building kits; REST `CreateTilesProRequest` has no `roof_profile` field. At that snapshot the MCP docs said only square or 1:2 tall tiles could be placed on maps (the 2026-10-29 clarification above supersedes this), and that sandbox playtests use the session's own browser. REST OpenAPI, `llms.txt`, and the REST docs shells were unchanged in this refresh; the website docs and MCP page had raw-byte changes only, with unchanged normalized summaries. No source failed.
> **2026-10-25 earlier refresh:** the inventory is unchanged at **102 REST paths, 275 schemas, and 118 MCP tools**; nothing was added or removed. Standard top-down and sidescroller tilesets now run on Pixen: MCP prices them at 1 generation (Pro 15, or 25 for top-down tiles above 32px), and both surfaces mark `outline`, `text_guidance_scale`, `tile_strength`, `tileset_adherence`, and `tileset_adherence_freedom` as no-effect on top-down, as MCP also does on sidescroller. Top-down standard defaults to round `shape_style`, takes any `transition_size` from 0 to 1 (16px tiles only above 0.5), ignores `view` (always high top-down), and REST `color_image` now has no effect (use `target_palette` on Pro). MCP `create_sidescroller_tileset` gains `mode` (`standard`/`pro`) and `enhance`, with `base_tile_id` now Pro-only; the REST sidescroller schema did not change, so those two fields are MCP-only. `POST /normal-map` and `create_normal_map` both gain `mode` (`lite` default at 0.1 generation, `pro` 0.5), `kind`, and five tuning fields. Pixen `no_background: true` above 65,536 px is now refused rather than returned opaque on both surfaces. REST `estimate-skeleton` accepts any size up to 256×256 at 0.1 generation, and the Skeleton v3 description now names it as `POST`. MCP `create_character` now defaults to `mode="v3"` and recommends `create_character_pro_flash(template_id=...)` for a text-only quadruped; `wait_for_jobs` gains `min_finished`; `add_to_project` accepts gallery images and folder projects; the managed MCP PixMiniMax mode now says "every tier"; and previously truncated MCP cost lines (Create Image Pro candidate-sheet billing, inpaint, PixMiniMax upscaled-canvas steps, Skeleton v3 steps) are complete. REST `/vfx` documents extra Pro change cost for large effects and a Lite surcharge from 700 characters. All seven sources completed without failures; the website pages changed only their title and footer links.

> **2026-10-19 refresh:** MCP grew from 117 to **118 tools** with `place_map_tiles`; REST v2 grew from 101 to **102 paths** and 273 to **275 schemas** with `POST /vfx`, `VfxRequest`, and `VfxResponse`. Neither surface removed a route/tool. MCP `place_map_tiles` and the new `create_map(tile_group_id=...)` option add tile-layer maps built from tiles-pro, path, or building tile groups (place, stack, erase, and add groups); `get_map` crops use q/r on tile layers. MCP `vfx_workbench` gains a partial REST counterpart, `/vfx`: PixelLab's description-driven effects artist, documented as the same artist as the website VFX creator, with lite/pro pricing quoted at submit and charged on delivery. Because the workbench is agent-authored, `/vfx` joins the REST partial list and `vfx_workbench` leaves the MCP-only list. 17 more MCP tools gained `palette`/`palette_name`/`max_colors`, and the existing `TargetPalette` schema spread from two to 25 REST request schemas (27 paths); REST limits it to `mode="pro"` on 8-direction characters, top-down tilesets, and object animation, and MCP `animate_character` has no palette field. MCP `animate_image_pixminimax` and REST no longer state a Tier 1 gate for PixMiniMax (the MCP `animate_character` mode text still does), and REST now labels managed character `mode="pro"` legacy. Other MCP changes: `get_image` downloads `gallery:<id>` images, `create_tiles_pro.style_images` accepts reference entries, `create_image_pixen` says transparency holds only up to about 65,536 px of canvas area, `inpaint_image` restates its cost as 10 generations up to 256×256 (the sentence is truncated upstream), and `agent_feedback` broadened its scope with an `area` field. All seven sources completed without failures; the website pages changed only their analytics beacon, and the REST docs/ReDoc shells were unchanged.

> **2026-10-15 refresh:** REST v2 grew from 100 to **101 paths** and 270 to **273 schemas** with `POST /normal-map`, `NormalMapRequest`, `NormalMapResponse`, and `TargetPalette`; MCP grew from 116 to **117 tools** with `create_normal_map`. Neither surface removed a route/tool. The new normal-map workflow is full parity. The refresh also added hex-palette controls to Pro image generation and REST Pro animation, five top-down Pro border controls, Pro character concept-image inputs, larger-canvas template-animation batch pricing, and an MCP managed-v3 frame/pixel budget; see the focused references below. All seven sources completed without failures. Website docs had raw build churn only; the website MCP page also changed its Raw Images copy to distinguish PixFlux palette images from Pro hex palettes. The REST docs and ReDoc shell sources were unchanged. The 0.4.130 VFX API announcement is not represented by a current public REST v2 route/schema in this refresh.

> **2026-10-11 refresh:** REST v2 remained at 100 paths and 270 schemas with no paths or schemas added or removed. `CreateTilesetRequest` said Pro `spread_x` and `slope_size` had no effect, `raggedness` shaped the border, Pro `transition_size` described upper-terrain height (and values above 0.4 produced tall walls and 25 tiles), and Pro lower/upper reference images made the shared terrain match an existing tileset tile exactly. MCP grew from 115 to 116 tools with `vfx_workbench`; its updated top-down tileset descriptions also marked `spread_x` and `slope_size` as no-effect fields in Pro. There were no removals. The seven-source refresh completed without failures; website artifacts changed at the raw build/hash level but their visible text was unchanged.

> **2026-10-08 refresh (Version 0.4.128):** REST v2 now has 100 paths and 270 schemas; MCP has 115 tools. REST added `POST /image-to-pixelart-pro-flash` and `POST /uploads/{ticket}`; MCP added `image_to_pixelart_pro_flash` and `get_upload_url`. No paths or tools were removed. Pro Tools now cost 10/15/25 generations by image size; exact tiers at 256 and 384 are ambiguous because the announcement's ranges overlap. MCP and REST v3 character-reference workflows now support quadrupeds with the matching template, and MCP can preserve supplied directional sprites through `direction_images`; when the south-facing reference and supplied images cover every requested view, PixelLab imports those views for 0.25 generation total. MCP `remove_map_object` accepts `placement_id` for one placement or `asset_id` to remove every placement of that asset; `get_tiles_pro` documents bit meanings for edge/4, edge/6, and corner/4. Upload tickets are user-bound and valid for 15 minutes. Pro Flash image conversion costs 6 generations and automatically detects output scale. The release also announces an experimental website Create VFX page, with MCP support planned; no API/tool is currently documented. The note about forthcoming Aseprite/Pixelorama visual prices has no values, so existing editor pricing remains unchanged. All seven refreshed sources were complete without failures; website normalized changes were analytics/build noise.

> **2026-10-05 refresh:** REST v2 grew from 97 to 98 paths and from 265 to 267 schemas; MCP remains at 113 tools. REST added `POST /uploads`, a temporary, no-generation image-reference upload. `CreateCharacterAnimationRequest` now documents managed PixMiniMax (`mode="pixminimax"`) on both managed endpoints, PixMiniMax-specific captions and frame limits, and custom anchors/`keep_first_frame` for v3 and PixMiniMax; REST retains `mode="pro"`, absent from the current MCP mode list. MCP `animate_character` now exposes managed PixMiniMax. At that snapshot, MCP `create_character(mode="v3")` accepted reference images only for mannequin characters, while REST accepted matching quadruped `template_id` references. MCP renamed `agent_help` to `search_help` (one removed, one added; no net tool-count change), clarified exact Skeleton v3 keypoint labels/order and draw-depth fields, added top-down tileset image/metadata download paths, and documented `create_font`'s 10×8 row-major glyph atlas. No REST paths were removed; there was no net MCP tool-count change. All seven sources refreshed without failure. Website pages changed only in generated build assets; normalized visible content was unchanged.

> **2026-10-03 refresh:** REST v2 grew from 95 to 97 paths and from 263 to 265 schemas; MCP grew from 110 to 113 tools. REST added `DELETE /background-jobs/{job_id}`, `DELETE /characters/{character_id}/animations/{animation_group_id}`, and `DELETE /characters/{character_id}/animations/{animation_group_id}/directions/{direction}`; the new routes are covered by `cancel_job` and `delete_animation`. MCP added `list_images`, `save_to_asset`, and `transfer_outfit`; the first two are MCP-only, while `transfer_outfit` closes the former REST-only `POST /transfer-outfit-v2` gap. Other contract changes include one-state character deletion semantics, explicit animation-group deletion guidance, PixMiniMax caption fields (`subject_description`, `initial_pose`, `view`, and independent facing `direction`), queue-position/wait-estimate fields plus REST cancellation, native Pro Flash sizes `48x48` and `128x128`, and removal of the documented Tier 1 gate from Skeleton v3. No REST paths or MCP tools were removed. The website sources changed only in raw build output; their normalized content did not change.

> **2026-09-25 refresh (Version 0.4.125):** REST v2 grew from 93 to 95 paths and from 258 to 263 schemas; MCP grew from 106 to 110 tools. REST added `POST /animate-with-skeleton-v3` (full parity with MCP `animate_with_skeleton_v3`) and `POST /image-to-text` (REST-only). MCP added `pixelart_workbench`, `remove_from_project`, and `wait_for_jobs` beyond the new Skeleton v3 match. No REST paths or MCP tools were removed; one unused `Keypoint` schema was removed, six schemas were added, and six existing schemas changed. Other contract changes: `animate_character(mode="skeleton-v3")`, managed-animation group IDs for appends, MCP object creation's optional `name` (no REST `name` field), map support in `add_to_project`, project-ID targeting in `sandbox_undeploy`, `edit-image-pixen` multiple-of-four and transparent-padding rules, and null prompt-enhancement usage clarification. PixMiniMax's 64×64/40-frame estimate fell from 12 to 6 generations. The release announcement adds PixelArt Workbench and Skeleton v3 availability in Character Creator, Aseprite, and Pixelorama; its roughly 70% token-reduction estimate is not independently measured here. All seven sources fetched without failure. The website docs had no visible text changes; the website `/mcp` page only reordered its tool list.

> 2026-09-12 display-name refresh: the public REST and MCP contracts now use the Pro Flash display name. Seven REST paths, 12 schema names, and six MCP tool names changed; route fields and documented behavior did not. Use only the current `pro-flash` paths and `pro_flash` tools listed below. The original family addition raised REST v2 from 86 to 93 paths and 246 to 258 schemas, and MCP from 100 to 106 tools. Five matched art operations cover image creation, character creation, object creation, one-image edit, and masked edit; `get_pro_flash_capabilities` matches REST `GET /pro-flash/capabilities`. REST alone exposes `GET /pro-flash/cost`, a provisional price estimator, which is a non-asset infrastructure gap rather than a missing art operation. The asset-gap count remains 25 and the MCP-only count remains 35. This family is not interchangeable with older Pro: image creation yields one image, character creation always eight directions, object creation one or eight, and edits keep native dimensions. The MCP page's character examples mistakenly invoke `create_character` with unrelated fields and its four-direction tip conflicts with the eight-only parameter; the REST OpenAPI and live tool schema should decide exact calls. No paid generation was used to validate visual quality or exact-mask behavior.

> 2026-09-08 refresh: the largest drift since this doc began — REST v2 grew from 79 to 85 paths and MCP from 76 to 99 tools. REST added a **Cleanup** family (`POST /correct-pixelart`, `POST /reduce-colors`, `POST /unzoom`), a cheap Pixen edit (`POST /edit-image-pixen`), and packed spritesheet exports (`GET /characters/{character_id}/spritesheet`, `GET /objects/{object_id}/spritesheet`). MCP added matching `correct_pixelart`, `reduce_colors`, `unzoom_image`, `edit_image_pixen`, plus `image_to_pixelart` — which closes a long-standing REST-only gap — and 18 tools with no REST counterpart: ten map tools (`create_map`, `delete_map`, `list_maps`, `get_map`, `edit_map`, `view_map`, `place_map_object`, `list_map_objects`, `move_map_object`, `remove_map_object`), four sandbox tools (`sandbox_deploy_worker`, `sandbox_undeploy`, `sandbox_playtest`, `sandbox_read_image`), `add_to_project`, `search_knowledge`, `cancel_job`, and `list_jobs`. Counts move to 25 REST-only/partial endpoints (9 ◐) and 35 MCP-only tools. Field-level changes worth routing on: MCP `create_ui_asset` gained `style_image_base64` and `project_id`, so those are no longer REST-only; `create_map_object`'s 8-hour auto-delete is gone (map objects are permanent and placeable on maps); `create_character_state` gained `override_width`/`override_height` (REST `override_frame_size`, a `FrameSize` of 32–256 in multiples of 4); `list_characters`/`list_objects` gained `search`; `create-tiles-pro` `tile_size` max dropped 256→128; `create-1-direction-object` min size 32→16 and `create-8-direction-object` 32→24; `image-to-pixelart` output max 320→512 and input max 1280→2048, plus new `fixer`/`init_image_strength`; `create-tileset` gained `enhance` (default `true`, `shape_style` only) and now rejects `shape_style` together with `mode="pro"`. MCP tileset cost text was corrected upward (top-down standard 1–4 generations, usually 3–4; sidescroller 2–3 — not 1), and the edit/inpaint cost line no longer names a "Gemini tier". The OpenAPI document was also reorganized into 22 new tag groups and its prose rewritten, and `llms.txt` gained two stated conventions — within each section the first endpoint listed is the intended default, and a `(legacy)` heading marker (no heading currently carries it). Those are documentation conventions, not contract changes, and they describe PixelLab's own sidebar ordering rather than this repository's cost- and benchmark-driven route preferences.

> 2026-09-12 refresh: REST v2 added `POST /animate-pixminimax` and schemas `AnimatePixminimaxRequest`/`AnimatePixminimaxResponse` (paths 85→86; schemas 244→246). MCP added the full-parity `animate_image_pixminimax` tool (tools 99→100). The new operation is beta, accepts first/end frame anchors, 4–40 generated frames in multiples of four on a canvas up to 256×256, and is publicly described as powered by MiniMax H3. The REST request also adds PixMiniMax-specific `enhance_prompt`, `direction`, and `drift_threshold` controls; the existing animation enhancer adds `engine="pixminimax"`. The refresh also clarifies REST `Create1DirectionObjectRequest.item_descriptions`: supplying fewer descriptions does not shrink the size-derived grid; remaining slots are generated from the top-level `description`. No route or tool was removed. Website docs and MCP page HTML changed in the refresh but did not yield an additional public schema change.

> 2026-09-13 product update (Version 0.4.123): the release notes add product/UI capabilities without changing the cached public REST/MCP inventory. Pro Flash (Beta) advertises a single-image option at 4–6 generations with a 256×256 maximum; current REST `POST /v2/create-image-pro-flash` still documents a provisional five-generation first-image estimate. PixMiniMax is available to Tier 1+ subscribers and is surfaced in Character Creator, Creator, Aseprite, and Pixelorama; its public programmatic parity remains REST `POST /v2/animate-pixminimax` ↔ MCP `animate_image_pixminimax`. Game Builder is available to Tier 1+ subscribers, Creator now queues work, and Map Workshop exports for Godot and Unity. These are first-party product-surface behaviors; no dedicated public REST v2 Game Builder or map-export route is documented. MCP map CRUD and object placement remain the public map tools, and the snapshot counts at that time were 93 REST paths, 258 schemas, and 106 MCP tools.

> 2026-08-09 refresh: the inventory remains 79 REST paths and 76 MCP tools. `shape_style` was added to the shared top-down tileset request/tool (`POST /create-tileset` / `POST /tilesets` ↔ `create_topdown_tileset`): `square` or `round`, with continuous 0–1 `transition_size` and an extended 4x8 sheet above 0.5. REST additionally documents square 16px/32px support and limits an omitted-`shape_style` `transition_size` to 0, 0.25, 0.5, or 1.0; the MCP docs do not state those two constraints. This is a field-availability and behavior-parity change, not a new route or tool.

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

Purpose: a route-level comparison of PixelLab's hosted MCP tool surface against the public REST v2 API — the missing features both ways: every REST v2 asset/management operation without a full MCP match (with partial overlap labeled separately), and every MCP tool with no REST v2 counterpart. (Non-asset REST infrastructure routes are handled separately below.) This is the parity map behind SKILL.md's rule "do not assume a REST endpoint has an MCP equivalent just because MCP is configured." It complements the *service*-level comparison in [Official PixelLab MCP Service Comparison](../tools/official-pixellab-mcp-service-comparison.md) and the *label*-level crosswalk in [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md); this file is the *endpoint*-level view.

## Snapshots Compared

Parity is a moving target because both surfaces ship independently. This review compares:

- **REST v2 index:** [official `llms.txt`](https://api.pixellab.ai/v2/llms.txt), cross-checked against the [OpenAPI spec](https://api.pixellab.ai/v2/openapi.json), refreshed snapshot 2026-10-25 (102 path templates / 113 operations; 275 schemas). `llms.txt` is the curated published index; OpenAPI is the fuller machine-readable schema. Where both agree a route is absent, it is treated as genuinely absent, not an index abbreviation.
- **MCP inventory:** [official MCP tool guide](https://api.pixellab.ai/mcp/docs), auto-generated snapshot 2026-10-25 (118 tools). This is the authoritative public MCP tool list; the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` is not.

Absence from a snapshot is not proof of absence from the live API. When a route or tool matters for code, re-verify against current OpenAPI/MCP docs (SKILL.md → Current Docs Refresh).

## How To Read This

Three surfaces are conflated in casual usage; they are not the same contract:

- **MCP tools** are called through an MCP client (bare or host-prefixed such as `mcp__pixellab__create_character`). They are not HTTP paths; do not curl a tool name as `/v2/...`.
- **REST v2 endpoints** are HTTP paths under `https://api.pixellab.ai/v2`.
- **Managed-asset animation** (`/animate-character`, `/characters/animations`, `/objects/{id}/animations`) and **raw animation** (`/animate-with-text*`, `/animate-pixminimax`, Skeleton v3, legacy `/animate-with-skeleton`, `/interpolation-v2`, …) are different endpoint families. MCP `animate_character`/`animate_object` cover managed assets, while `animate_image`, `animate_image_pixminimax`, `animate_with_skeleton_v3`, and `transfer_outfit` take raw inputs directly. REST retains route-specific drift correction, prompt enhancement, legacy skeleton estimation/animation, and single-image rotate controls; animation-frame editing has partial overlap through MCP `edit_image`, which applies one edit consistently across a list of frames.

## At a Glance

**Matching basis:** counterparts are judged by **functional capability, not tool name** — a REST endpoint counts as "covered" if any MCP tool or documented MCP parameter does the same job, even under a different name or bundled into a broader tool (and the reverse for MCP tools). A scoped or partial overlap (for example, an MCP capability that works only on a managed asset) is marked partial (◐), not dropped.

**Current parity context:** REST `DELETE /background-jobs/{job_id}` matches MCP `cancel_job`; the two character-animation delete routes match MCP `delete_animation`; and REST `POST /transfer-outfit-v2` matches MCP `transfer_outfit`. Skeleton v3 remains full core-workflow parity, but the REST schema exposes `drift_threshold` beyond MCP. PixelArt Workbench and MCP `list_images`/`save_to_asset` have no REST workflow counterpart. MCP `vfx_workbench` has a partial REST counterpart, `POST /vfx`: both produce saved animated effects, but the MCP workbench is agent-authored while REST runs PixelLab's own effects artist from a description. Several broader MCP tools partially overlap REST operations without a full match: `create_image_pro` supports one style image for `generate-with-style-v2`, `image_to_pixelart_pro_flash` covers automatic-scale conversion through a different model than `image-to-pixelart-pro`, and `edit_image` can apply one edit consistently across animation frames for `edit-animation-v2`. REST `POST /image-to-text` has no MCP counterpart. A shared route label means core workflow coverage, not identical schemas; the matrix calls out material one-sided modes and controls.

**On both surfaces — core workflow parity, so they live in the [Coverage Matrix](#coverage-matrix) below, not in the gap lists:** characters (4/8-direction, v3, Pro Flash, state, and common managed animation modes, including one-state deletion and animation-group/direction deletion; REST-only managed Pro animation differences are partial), **portrait ↔ character conversion** (`portrait-character-pro` ↔ `create_portrait_character`), **managed portraits and talking output** (portrait attachment, vocal-viseme generation, and talking GIF rendering), objects (1/8-direction, Pro Flash, state, animate, review, list/get/delete, **including per-object animation delete** — `DELETE /objects/{id}/animations` ↔ `delete_animation`), map objects, top-down / sidescroller / isometric / pro tilesets & tiles, **path/road tiles and building kits** (`create-tiles-pro` `tile_feature` ↔ `create_path_tiles`/`create_building_kit`), structured UI assets, **pixel font Pro** (`generate-font-pro` ↔ `create_font`), balance, **tag setting** (`PATCH .../tags` ↔ `update_character_tags` / `update_object_tags`), **raw text-to-image on PixFlux (both the base and background-oriented path share one identical schema) and Pixen** (`create-image-pixflux`/`create-image-pixflux-background`/`create-image-pixen` ↔ `create_image_pixflux`/`create_image_pixen`), **Pro image generation with labelled/style and hex-palette controls** (`generate-image-v2` ↔ `create_image_pro`), **normal-map generation** (`POST /normal-map` ↔ `create_normal_map`), **Pro Flash one-image generation, edit, inpaint, and pixel-art conversion**, **arbitrary-image edit at Pro tier** (`edit-images-v2` ↔ `edit_image`), **arbitrary-image inpaint at Pro tier** (`inpaint-v3` ↔ `inpaint_image`), **raw text-driven animation** (`animate-with-text-v3` ↔ `animate_image`), **raw PixMiniMax animation** (`animate-pixminimax` ↔ `animate_image_pixminimax`), **outfit transfer** (`transfer-outfit-v2` ↔ `transfer_outfit`), **Pixen-tier image edit** (`edit-image-pixen` ↔ `edit_image_pixen`), **image-to-pixel-art conversion** (`image-to-pixelart` ↔ `image_to_pixelart`), and the **Cleanup family** (`correct-pixelart` ↔ `correct_pixelart`, `reduce-colors` ↔ `reduce_colors`, `unzoom` ↔ `unzoom_image`). REST background-job cancellation also overlaps MCP job control. Lip-sync planning overlaps too, but only partially because MCP lacks REST's stateless form. Pro Flash is core-workflow parity, not field-for-field parity; MCP has URL/source-ID conveniences and REST has a separate cost estimator.

**REST v2 operations without a full MCP match (29; ◐ = partial overlap via a broader or narrower tool).** Of these, 16 have partial overlap and 13 have no documented MCP overlap. See [REST v2 Operations Without a Full MCP Match](#rest-v2-operations-without-a-full-mcp-match).

| Category | # | REST v2 endpoints |
|---|---|---|
| Raw image generation | 3 | `create-image-bitforge`, `generate-with-style-v2` (◐), `generate-ui-v2` |
| Image edit / convert / resize / prompt description | 5 | `edit-image` (◐), `image-to-pixelart-pro` (◐), `image-to-text`, `resize`, `remove-background` |
| Inpaint | 1 | `inpaint` (◐) |
| Raw animation / rotation / skeleton | 9 | `animate-with-text` (◐), `animate-with-text-v2` (◐), `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2` (◐), `interpolation-v2` (◐), `generate-8-rotations-v2` (◐), `generate-8-rotations-v3` (◐), `rotate` |
| Managed-character route differences | 3 | `create-character-pro` (◐), `animate-character` and `characters/animations` (◐) |
| Prompt enhancement | 3 | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, `enhance-animation-v3-prompt` |
| Managed-asset export | 3 | `characters/{id}/zip` (◐), `characters/{id}/spritesheet`, `objects/{id}/spritesheet` (the two `.../tags` PATCH routes now have MCP `update_character_tags` / `update_object_tags`) |
| Talking portraits | 1 | `lip-sync` (◐: MCP is managed-character only; REST also supports stateless `viseme_count`) |
| Animated VFX | 1 | `vfx` (◐: MCP `vfx_workbench` is agent-authored, not PixelLab's effects artist) |

`create-image-pixen`, `create-image-pixflux`, `create-image-pixflux-background`, `generate-image-v2`, `edit-images-v2`, `inpaint-v3`, and (since the 2026-09-08 refresh) `image-to-pixelart` are no longer in this list — they graduated to full `=` parity (see the 2026-07-26 re-audit note above) and now live in the "full parity" prose and the Coverage Matrix. Base `edit-image` and base `inpaint` newly *entered* this list in their place — the earlier snapshot had the base/Pro assignment backwards for both families. `transfer-outfit-v2` also graduated in this refresh via MCP `transfer_outfit`.

◐ **Partial overlap** (16 of the 29 — no *dedicated, tier-matched* MCP tool, or MCP covers only a narrower form). These are `create-character-pro`, `generate-with-style-v2`, base `edit-image`, `image-to-pixelart-pro`, base `inpaint`, `animate-with-text`, `animate-with-text-v2`, `interpolation-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, `edit-animation-v2`, `characters/{id}/zip`, stateless `lip-sync`, `animate-character` and `characters/animations` in REST-only legacy `pro` mode, and `vfx`. Per-endpoint notes are below.

**Missing from REST v2 — MCP has it, no REST endpoint (40 tools).** See [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

| Category | # | MCP tools |
|---|---|---|
| Maps | 11 | `create_map`, `delete_map`, `list_maps`, `get_map`, `edit_map`, `view_map`, `place_map_tiles`, `place_map_object`, `list_map_objects`, `move_map_object`, `remove_map_object` |
| Projects | 3 | `list_projects`, `add_to_project`, `remove_from_project` |
| Chat (game-building agent) | 3 | `chat_list_conversations`, `chat_get_messages`, `chat_send_message` |
| Sandbox (code execution + deploy) | 12 | `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_read_image`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`, `sandbox_deploy_worker`, `sandbox_undeploy`, `sandbox_playtest` |
| Deployed agents | 3 | `agent_list`, `agent_inspect`, `agent_talk` |
| Job control | 2 | `list_jobs`, `wait_for_jobs` |
| MCP meta | 3 | `search_help`, `agent_feedback`, `search_knowledge` |
| Pixel-art commands | 1 | `pixelart_workbench` |
| Gallery and asset save | 2 | `list_images`, `save_to_asset` |

## Practical Picking Rule

MCP is a managed-asset tool layer inside an agent that also exposes raw-image primitives (including Pro Flash, Skeleton v3, and the Cleanup family), PixelArt Workbench, animated VFX Workbench, gallery browsing/save-back, and talking-portrait helpers. REST v2 remains the complete HTTP API for image-to-text, legacy skeleton estimation/animation, stateless lip sync, and code control.

| Use MCP when | Use REST v2 when |
|---|---|
| You're in an MCP-enabled agent and want a managed asset with IDs and lifecycle helpers, raw PixFlux/Pixen/Pro-tier or Skeleton v3 image work, animated VFX via `vfx_workbench`, gallery browse/save-back, PixelArt Workbench commands, pixel-art cleanup, outfit transfer, or a managed talking-portrait workflow | You need BitForge, multi-image style references (MCP covers one), base-tier edit/inpaint controls, image-to-text, the older Pro image-to-pixel-art tier (MCP Pro Flash performs the same conversion through a different model), legacy skeleton estimation/animation, stateless lip sync, packed spritesheet/ZIP export, batch/code/backend control, exact schemas, PixelLab's own VFX artist (`/vfx`), or any of the 29 REST-only/partial operations |
| You need the platform layer — maps, projects, chat, sandbox, deployed agents, active-job list/all-job wait, or other MCP-only helpers | You need a freeform UI image (`generate-ui-v2`) or any capability with no MCP tool |

One line: **MCP is the convenient managed-asset, raw-image, and managed talking-portrait path inside an agent; REST v2 remains the complete API for stateless lip sync, exact code control, and the remaining REST-only operations.**

## Coverage Matrix

Parity legend (functional, not name-based): **=** covered by a dedicated MCP tool or a documented tool parameter; **~** covered only via an inferred, undocumented parameter value on a broader MCP tool; **◐** partial — a broader MCP tool produces the *same kind of output* in a scoped form (e.g., managed-asset-only), but no dedicated MCP tool exists. A merely adjacent MCP capability that yields a *different* asset type (e.g., a generation-time control such as `create_map_object`'s `inpainting`, or `style_images` on object creation) is **none** with a note, not ◐; **none** / **REST-only** no MCP tool documented. On multi-helper rows, `=` is capability-level (create + retrieve + list/delete). This matrix is comprehensive and REST-keyed — every REST v2 endpoint appears in a table below; MCP tools with no REST endpoint are listed separately in [MCP Tools With No REST v2 Counterpart](#mcp-tools-with-no-rest-v2-counterpart).

### Characters

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-character-with-4-directions` | `create_character(n_directions=4)` | = |
| `POST /create-character-with-8-directions` | `create_character(n_directions=8)` | = |
| `POST /create-character-v3` | `create_character(mode="v3")` | = core workflow — both surfaces support matching quadruped references and `direction_images`; REST additionally documents `no_background`, `enhance_prompt`, and `seed`, while MCP exposes `proportions` and accepts JSON-string `direction_images` when object serialization is unavailable. |
| `POST /create-character-pro` | `create_character(mode="pro")`, including concept images and `style_character_id`; separate MCP v3 mode supports exact-sprite rotation | ◐ — MCP has the concept and rotation workflows, but REST alone exposes the Pro route's `method` selector (`create_with_style`, `create_from_concept`, `rotate_character`) and `style_description`. |
| `POST /create-character-pro-flash` | `create_character_pro_flash` — eight views; MCP adds first-frame URL while both accept an owned source-image ID | =, core workflow |
| `POST /create-character-state` | `create_character_state` | = |
| `POST /animate-character`, `POST /characters/animations` | `animate_character` for `template`, `skeleton-v3`, `v3`, and `pixminimax`; REST also exposes legacy `pro` and `target_palette` | ◐ — REST `mode="pro"` and the palette field have no current MCP equivalent. |
| `GET /characters` | `list_characters` | = |
| `GET /characters/{id}` | `get_character` | = |
| `DELETE /characters/{id}` | `delete_character` — deletes one state; repeat per state to remove a multi-state group | = |
| `GET /characters/{id}/zip` | `get_character` download link (no full ZIP bundle) | ◐ |
| `PATCH /characters/{id}/tags` | `update_character_tags` | = |
| `POST /portrait-character-pro`, `GET /portrait-character-pro/{job_id}` | `create_portrait_character` + `get_portrait_character` | = |
| `POST /characters/{id}/portrait` | `set_character_portrait` | = |
| `POST /vocal-animation`, `GET /vocal-animation/{job_id}` | `create_vocal_animation` + `get_vocal_animation` | = |
| `POST /talking-gif` | `create_talking_gif` | = |
| `POST /lip-sync` | `get_lip_sync` covers managed characters; REST also accepts stateless `viseme_count` | ◐ |
| `DELETE /characters/{id}/animations` | `delete_animation` — legacy name/group selector; the REST route now prefers the ID-specific rows below | = |
| `DELETE /characters/{id}/animations/{animation_group_id}` | `delete_animation` with `animation_group_id` and no direction | = |
| `DELETE /characters/{id}/animations/{animation_group_id}/directions/{direction}` | `delete_animation` with `animation_group_id` and `direction` | = |
| `GET /characters/{id}/spritesheet` (ZIP: one packed uniform-grid sheet + layout JSON) | — (no MCP spritesheet export) | none |

**Deletion response shapes in this snapshot:** `DELETE /characters/{id}` returns `DeleteCharacterResponse`; `group_id` identifies the character group and nullable `next_state_id` identifies the most recently updated remaining state, or is null when the deleted state was the last one. The legacy animation delete response no longer has `storage_errors`. Group-wide `DELETE /characters/{id}/animations/{animation_group_id}` returns `DeleteAnimationGroupResponse` with required `animation_group_id`, `deleted_directions`, and `label`, plus optional `usage`.

### Objects & Map Objects

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-1-direction-object` | `create_1_direction_object` | = |
| `POST /create-8-direction-object` | `create_8_direction_object` | = |
| `POST /create-object-pro-flash` | `create_object_pro_flash` — one or eight views; MCP adds first-frame URL | =, core workflow |
| `POST /objects/{id}/animations` | `animate_object` | = |
| `POST /objects/{id}/states` | `create_object_state` | = |
| `POST /objects/{id}/select-frames` | `select_object_frames` | = |
| `POST /objects/{id}/dismiss-review` | `dismiss_review` | = |
| `GET /objects`, `GET /objects/{id}`, `DELETE /objects/{id}` | `list_objects`, `get_object`, `delete_object` | = |
| `DELETE /objects/{id}/animations` | `delete_animation` (same tool as the character row above — its docstring explicitly covers "a character or object") | = |
| `PATCH /objects/{id}/tags` | `update_object_tags` | = |
| `GET /objects/{id}/spritesheet` (ZIP: one packed uniform-grid sheet + layout JSON) | — (no MCP spritesheet export) | none |
| `POST /map-objects`, `GET /map-objects/{id}` | `create_map_object` + `get_map_object` | = core workflow — REST additionally exposes `init_image`, `init_image_strength`, `color_image`, `text_guidance_scale`, and `seed`; MCP has no equivalent parameters for those controls. |

### Tiles & Tilesets

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /create-tileset`, `POST /tilesets`, `GET /tilesets`, `GET /tilesets/{id}`, `DELETE /tilesets/{id}` | `create_topdown_tileset`, `get_topdown_tileset`, `list_topdown_tilesets`, `delete_topdown_tileset` | = — both expose `roundness`, `boundary_amplitude`, `boundary_seed`, `step_slope`, and `connect_diagonals` for Pro; standard `shape_style` remains separate. See `tileset.md` for exact restrictions. |
| `POST /create-tileset-sidescroller`, `POST /tilesets-sidescroller`, `GET /tilesets-sidescroller`, `GET /tilesets-sidescroller/{id}`, `DELETE /tilesets-sidescroller/{id}` | `create_sidescroller_tileset`, `get_sidescroller_tileset`, `list_sidescroller_tilesets`, `delete_sidescroller_tileset` | = standard workflow; MCP-only `mode="pro"`, `enhance`, and Pro `base_tile_id`; REST-only `lower_reference_image`, `transition_reference_image`, and `color_image`. |
| `POST /create-isometric-tile`, `GET /isometric-tiles`, `GET /isometric-tiles/{id}`, `DELETE /isometric-tiles/{id}` | `create_isometric_tile`, `list_isometric_tiles`, `get_isometric_tile`, `delete_isometric_tile` | = |
| `POST /create-tiles-pro`, `GET /tiles-pro`, `GET /tiles-pro/{id}`, `DELETE /tiles-pro/{id}` | `create_tiles_pro`, `get_tiles_pro`, `list_tiles_pro`, `delete_tiles_pro` | = |
| `POST /create-tiles-pro` (`tile_feature: "roads"`) | `create_path_tiles` (shares `get_tiles_pro`/`list_tiles_pro`/`delete_tiles_pro` — no dedicated getter) | = |
| `POST /create-tiles-pro` (`tile_feature: "building"`, `building_*` fields) | `create_building_kit` (shares `get_tiles_pro`/`list_tiles_pro`/`delete_tiles_pro` — no dedicated getter) | = core workflow; MCP-only `roof_profile` (`gable`/`round`, materials layout only), absent from REST `CreateTilesProRequest` |

`create_tiles_pro` map compatibility depends on the input: omit `tile_height` or use `tile_size` or twice that value. The MCP guide explicitly allows a flat 2:1 isometric floor by omitting `tile_height` and setting `tile_view_angle=30`, `tile_depth_ratio=0`. Its limit of 16 independent tiles per call does not apply to connectable sets and is not stated in REST. Both surfaces now estimate generation at 1–2 minutes.

### Fonts, UI, Account

| REST v2 | MCP tool | Parity |
|---|---|---|
| `POST /generate-font-pro`, `GET /generate-font-pro/{job_id}` | `create_font` + `get_font` | = — both support `glyph_px` 8/12/16/24/32/64 (default 16); MCP docs specify a 10×8 row-major atlas for the 80-character glyph sequence and no space glyph. |
| `POST /create-ui-asset`, `GET /ui-assets`, `GET /ui-assets/{id}`, `DELETE /ui-assets/{id}` | `create_ui_asset`, `list_ui_assets`, `get_ui_asset`, `delete_ui_asset` | = |
| `POST /generate-ui-v2` (freeform UI; no `pieces`/`elements`) | — (MCP has no freeform UI generator) | none |
| `GET /balance` | `get_balance` | = |
| `GET /background-jobs/{job_id}` | per-resource `get_*` tools | different model |
| `DELETE /background-jobs/{job_id}` | `cancel_job` | = |

**Note on UI generation.** MCP `create_ui_asset` — structured `pieces`/`elements` with labeled sub-parts — has a full REST equivalent, `POST /create-ui-asset` (same `pieces`/`elements`; as of the 2026-09-08 snapshot MCP also exposes `style_image_base64` and `project_id`, so neither is REST-only any more); that is the `=` row above. REST's *other* UI endpoint, `POST /generate-ui-v2`, is a simpler freeform generator (text + optional `concept_image`, no `pieces`/`elements`) with **no** MCP counterpart — MCP exposes no freeform UI-image tool. Details: [`pixellab-ui-generation-surfaces-research.md`](pixellab-ui-generation-surfaces-research.md).

**Note on async retrieval and management rows.** Where a `=` row bundles MCP `get_*` / `list_*` helpers against a single REST `POST`, REST retrieval is via `GET /background-jobs/{job_id}` (the generic async poll) plus, where present, a dedicated GET such as `/tilesets/{id}`, `/isometric-tiles/{id}`, `/tiles-pro/{id}`, or `/characters/{id}`. So MCP `get_*` tools are never true gaps. As of the 2026-07-19 snapshot REST v2 also exposes the *list* routes for sidescroller tilesets (`GET /tilesets-sidescroller`) and tiles-pro (`GET /tiles-pro`), and *delete* routes for every tile/tileset family and for managed character animations — so these families now have full create/retrieve/list/delete parity on both surfaces. (Before 2026-07-19 the `list`/`delete` half was MCP-only.)

### Create Image (raw generation)

MCP's model-specific raw-image tools mirror REST's PixFlux, Pixen, Pro, and separate Pro Flash routes. Their generation controls provide functional parity, while MCP additionally accepts preferred URL forms for PixFlux init/color images and Pro reference/style images. REST retains a few route-specific extras such as `background_removal_task`, deprecated `negative_description`, and `enhance_prompt`. `POST /create-image-pixflux-background` still uses the same `CreateImagePixfluxRequest` as `/create-image-pixflux`, so one MCP tool covers both URLs. Pro Flash makes exactly one image rather than the older Pro route's size-dependent batch.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /create-image-pixen` | `create_image_pixen` + `get_image` | = |
| `POST /create-image-pixflux` | `create_image_pixflux` + `get_image` | = |
| `POST /create-image-pixflux-background` | `create_image_pixflux` + `get_image` — byte-identical request schema (`CreateImagePixfluxRequest`) to the row above | = |
| `POST /create-image-bitforge` (`coverage_percentage`, `skeleton_keypoints`/`skeleton_guidance_scale` pose guidance, `inpainting_image`/`mask_image`, `style_image`/`style_strength`) | — no MCP tool combines any of BitForge's unique controls | none |
| `POST /generate-image-v2` (Pro) | `create_image_pro` + `get_image` | = — both expose exact palette and per-image color-cap controls under surface-specific names; REST additionally documents beta `smart` and the size-based output-count ladder. |
| `POST /create-image-pro-flash` (one image, native size) | `create_image_pro_flash` + raw-image job retrieval | =, core workflow |
| `GET /pro-flash/capabilities` (supported native sizes/controls) | `get_pro_flash_capabilities` | =, core workflow |
| `POST /generate-with-style-v2` (Pro, style ref) | `create_image_pro` accepts one style image (URL or base64) plus `style_copy`; REST supports 1–4 `style_images` and optional `style_description`, and derives a square output size from the references | ◐ |

### Image Edit, Convert, Resize

**Re-audit correction:** MCP `edit_image` is the Pro workflow matching `EditImagesV2Request`: it accepts 1–16 edit targets plus optional reference mode, now through preferred URLs or inline base64. Base `EditImageRequest` is text-only and has `color_image`/`text_guidance_scale`, so it remains only partially covered. As of 2026-09-25, `image-to-text` is another REST-only image operation; the Pro converter, resize, and remove-background also remain REST-only.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /edit-image` (base; single `image`, text-only, has `color_image`/`text_guidance_scale`) | `edit_image` can perform a single-image, text-only edit as a subset of its range, but is fundamentally the Pro/batch/reference-mode tool, not a dedicated base-tier match | ◐ |
| `POST /edit-images-v2` (Pro; `edit_images` list of 1-16, `method`: text or reference) | `edit_image` — matches the list-of-images shape and the text-vs-reference mode switch; MCP's own docstring tags it "(pro)" | = |
| `POST /edit-image-pro-flash` (one image, unchanged native canvas) | `edit_image_pro_flash` — MCP additionally accepts an image URL or owned `source_image_id`; REST requires encoded `image` | =, core workflow |
| `POST /edit-image-pixen` (Pixen tier; 1 generation, source ≤256px/side, target area ≤256x256) | `edit_image_pixen` + `get_image` — but the **default diverges**: REST defaults `no_background: true`, while MCP leaves it unset and follows the input (a transparent input stays transparent, an opaque one stays opaque) | = |
| `POST /image-to-pixelart` | `image_to_pixelart` + `get_image` — MCP `faithful` is REST `fixer`, `output_width`/`output_height` are REST `output_size`, and `init_image_strength`/`text_guidance_scale`/`seed` match | = |
| `POST /image-to-text` (PixelLab prompt from image) | — no MCP image-to-text tool | none |
| `POST /image-to-pixelart-pro` (older Pro; no output-size field, native scale auto-detected) | `image_to_pixelart_pro_flash` performs the same native-scale conversion through the separate Pro Flash model/tier | ◐ |
| `POST /image-to-pixelart-pro-flash` (6 generations; detects native scale/output size) | `image_to_pixelart_pro_flash` + `get_image` | =, core workflow |
| `POST /normal-map` (sprite PNG or horizontal animation strip; `lite` 0.1 or `pro` 0.5 generation when delivered) | `create_normal_map` + `get_image` — MCP also accepts PixelLab asset references and image URLs | = |
| `POST /resize` | — | none |
| `POST /remove-background` | generation-time `no_background` only, not post-hoc removal | none |

### Inpaint

**Re-audit correction:** the prior snapshot had the base/Pro assignment backwards here too. MCP `inpaint_image` has a `crop_to_mask` field ("Confine generated content to the mask boundary for clean edges") — that field exists **only** on `InpaintV3Request` (`"Whether to crop generated content to mask boundary (ensures clean edges)"`, worded almost identically). Base `InpaintRequest` has no `crop_to_mask` at all, and instead carries a full set of PixFlux-style weak-guidance generation controls (`direction`, `isometric`, `shading`, `outline`, `detail`, `text_guidance_scale`, `init_image`, `color_image`, `negative_description`, `extra_guidance_scale`, `oblique_projection`) that `inpaint_image` does not expose. `inpaint_image`'s rectangular `mask_x/y/width/height` shorthand doesn't map to a live REST field either way — `InpaintV3Request`'s own `bounding_box` is explicitly marked `"(deprecated)"` in its description, so MCP likely builds a full `mask_image` internally rather than calling a deprecated field. Net: `inpaint-v3` is the full `=` match; base `inpaint` drops to ◐.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /inpaint` (base; no `crop_to_mask`, has `direction`/`isometric`/`shading`/`outline`/`detail`/`text_guidance_scale`/`init_image`/`color_image`) | `inpaint_image` covers the core mask-regenerate job but lacks all of base's extra weak-guidance controls, and is fundamentally the Pro-shaped tool, not a dedicated base-tier match | ◐ |
| `POST /inpaint-v3` (Pro; `crop_to_mask`, `bounding_box`/`context_image` both marked deprecated) | `inpaint_image` — matches on `crop_to_mask` and the white=generate/black=preserve mask convention | = |
| `POST /inpaint-image-pro-flash` (white/black same-size mask; claims exact unmasked RGBA) | `inpaint_image_pro_flash` — MCP adds source/mask URLs, an owned source ID, and rectangular-mask shorthand; REST requires encoded source and mask | =, core workflow; exact-mask claim untested |

### Cleanup

New in the 2026-09-08 refresh. All three are cheap (MCP documents 0.1 generations each). `correct-pixelart` and `reduce-colors` take one or more same-size frames, so an animation or a character's directions stay consistent with each other; `unzoom` takes a single image. REST returns the corrected images synchronously; MCP queues a job retrieved with `get_image`.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /correct-pixelart` (`images[]`, `strength` 0.0–1.0 default 0.1; max area 1024x1024; alpha preserved; does not resize) | `correct_pixelart` (`images_base64`/`image_urls`, `strength`) | = |
| `POST /reduce-colors` (`images[]`, `num_colors` 2–256 **xor** `palette_image`, `dithering` `none`/`2x2`/`4x4`/`8x8`, `dithering_strength` 0–10; 512x512 total pixel budget across frames; returns the palette as a 1px strip plus `n_colors`) | `reduce_colors` (`images_base64`/`image_urls`, `num_colors`, `palette_image_base64`/`palette_image_url`, `dithering`, `dithering_strength`) | = |
| `POST /unzoom` (`image`, `quantize` `-1` keep all / `0` auto / `2`–`256`; min 256x256, max area 2048x2048; **result is opaque** — transparency is composited onto white; returns `original_size`, `unzoomed_size`, `zoom_factor_detected`) | `unzoom_image` (`image_base64`/`image_url`, `quantize`) | = |

`/unzoom` is not merely a utility: the API description now instructs callers to run user-supplied artwork through it **before** sending it to any endpoint that takes a reference or style image, because upscaled pixel art (every art pixel a block of screen pixels) is the most common cause of poor output.

### Raw Animation, Rotation, Skeleton

MCP `animate_image`, `animate_image_pixminimax`, `animate_with_skeleton_v3`, and `transfer_outfit` are standalone raw-animation tools; the first two take frame URLs/base64, Skeleton v3 takes a reference image and keypoint sequence, and outfit transfer takes an animation frame list plus a same-character reference image. They match REST `animate-with-text-v3`, `animate-pixminimax`, `animate-with-skeleton-v3`, and `transfer-outfit-v2` respectively. REST retains route-specific `drift_threshold`, the older raw-skeleton endpoints, and other exact controls. Managed animation remains a separate full-parity family.

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /animate-with-text` (base; `reference_image`+`action`) | `animate_*(action_description)` (modern `mode="v3"`), managed | ◐ |
| `POST /animate-with-text-v2` (Pro; `reference_image`+`action`; optional shared-frame `target_palette`) | `animate_*(action_description)`; no matching Pro/v2 mode is documented in MCP, `animate_character` has no hex-palette field, and `animate_object` lists one without a mode limit while REST documents it only for `mode="pro"`; managed | ◐ |
| `POST /animate-with-text-v3` (new; `first_frame`+optional `last_frame`+`action`) | `animate_image` — no managed asset needed; functionally equivalent, but REST additionally exposes `drift_threshold` and `enhance_prompt`, while MCP accepts frame URLs | = |
| `POST /animate-pixminimax` (Beta; `first_frame`+optional `last_frame`+`description`) | `animate_image_pixminimax` — no managed asset needed; both expose motion enhancement plus caption fields for subject, pose, view, and facing, MCP adds preferred frame URLs, and REST additionally exposes `drift_threshold` | = |
| `POST /animate-with-skeleton-v3` (Beta; reference image + 3–15 keypoint frames) | `animate_with_skeleton_v3` — raw keypoint sequence, max 256×256; REST additionally exposes `drift_threshold`; MCP retrieves output with `get_image` | = core workflow |
| `POST /interpolation-v2` (Pro; *required* `start_image`+`end_image`) | `animate_image(first_frame_base64, last_frame_base64)` reaches the same start+end capability — but that `last_frame_base64` is `animate-with-text-v3`'s own optional `last_frame`, so this is the v3 model doing interpolation, not the Pro `interpolation-v2` model | ◐ |
| `POST /generate-8-rotations-v2` (Pro; rotate/style/concept methods) | `create_character(mode="v3", reference_image_url/base64)` rotates the exact character sprite into managed directions; `create_8_direction_object` covers 8-direction object creation but does not expose REST's method selector | ◐ |
| `POST /generate-8-rotations-v3` | `create_character(mode="v3", reference_image_url/base64)` rotates the exact character sprite, but persists it as a managed character; MCP has no matching raw-image result workflow | ◐ |
| `POST /edit-animation-v2` (Pro; same edit across all frames) | `edit_image` applies the same text edit consistently to a list of images/frames; it is a broader Pro image-edit tool, not the dedicated animation endpoint | ◐ |
| `POST /transfer-outfit-v2` (Pro) | `transfer_outfit` — reskins two or more animation frames with a same-character outfit reference; both are composited-frame workflows | = |
| `POST /animate-with-skeleton` (`skeleton_keypoints`, legacy three-frame shape) | — no equivalent MCP tool; Skeleton v3 uses a different request contract | none |
| `POST /estimate-skeleton` | — | none |
| `POST /rotate` (single arbitrary rotation) | — | none |

### Animated VFX

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /vfx` (description-driven effects artist, `lite`/`pro`; optional sprite; `effect_id` changes save over a saved effect) | `vfx_workbench` — same saved-effect family (GIF, spritesheet PNG/JSON, game-pack ZIP, reopen by effect ID), but the agent composes it with commands | ◐ |

### Prompt Enhancement

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `POST /enhance-pixen-prompt` | — (`search_help` is docs Q&A, not a rewriter) | none |
| `POST /enhance-character-v3-prompt` | — | none |
| `POST /enhance-animation-v3-prompt` (`engine=v3` or `engine=pixminimax`) | — | none |

### Infrastructure (non-asset)

| REST v2 | MCP functional counterpart | Parity |
|---|---|---|
| `GET /background-jobs/{job_id}` | per-resource `get_*` polling | different model |
| `GET /llms.txt` | `pixellab://docs/*` resources | different form |
| `GET /pro-flash/cost` | `get_pro_flash_capabilities` documents a free exact-size price split; no separate MCP cost-estimator tool | same price-check purpose via capabilities, non-asset |
| `POST /uploads` | — no matching MCP tool; returns a temporary `ref` accepted by documented image-URL fields | none, non-asset; no generation or charge |
| `POST /uploads/{ticket}` | `get_upload_url` supplies the 15-minute, user-bound upload destination | =, non-asset upload workflow; no generation |

The MCP docs also provide direct top-down tileset downloads at `/mcp/tilesets/{id}/image` and `/mcp/tilesets/{id}/metadata`. These are not REST v2 routes or MCP tools and do not affect the route/tool parity counts; the UUID acts as the access key.

## REST v2 Operations Without a Full MCP Match

This is the core deliverable. These REST v2 operations lack full MCP parity. Rows marked ◐ have a narrower or broader MCP workflow with material differences; rows marked none have no documented MCP overlap. Route to REST v2 when its unmatched controls or workflow are needed.

### 1. Raw image generation (3) — BitForge and freeform UI have no MCP overlap; multi-image style generation has narrower MCP support

MCP briefly shipped one generic `create_image` tool on 2026-07-26, then split it the same day (21:03 follow-up) into `create_image_pixflux`, `create_image_pixen`, and `create_image_pro`, each needing no managed asset and matching its REST counterpart field-for-field — closing four of the seven rows below outright (a re-audit found the fourth: `create-image-pixflux-background` uses the byte-identical `CreateImagePixfluxRequest` schema, confirmed from the raw OpenAPI path definitions, not just a same-named coincidence):

- `POST /create-image-pixen` — = full parity: `create_image_pixen` + `get_image`
- `POST /create-image-pixflux` — = full parity: `create_image_pixflux` + `get_image`
- `POST /create-image-pixflux-background` — = full parity: same tool, same schema (`CreateImagePixfluxRequest`) — this is a second URL for the identical operation, not a distinct model
- `POST /create-image-bitforge` — none: no MCP tool has `coverage_percentage` (BitForge's one unique control), `skeleton_keypoints`/`skeleton_guidance_scale` pose guidance, or its `inpainting_image`/`mask_image`/`style_image`/`style_strength` combination
- `POST /generate-image-v2` (Pro) — = functional parity: `create_image_pro` + `get_image`; MCP also accepts reference/style URLs
- `POST /generate-with-style-v2` (Pro, style reference) — ◐ partial: MCP `create_image_pro` accepts one style image with `style_copy`; REST accepts 1–4 `style_images` and optional `style_description`, and derives a square output size from the references
- `POST /generate-ui-v2` (freeform UI image; no `pieces`/`elements`) — none: MCP's only UI tool, `create_ui_asset`, is a structured panel builder (its REST twin is `create-ui-asset`), not a freeform generator, and lacks `concept_image`; MCP has no `generate-ui-v2` equivalent

### 2. Image edit / convert / resize / prompt description (5) — MCP's Pro edit tool is edit-images-v2, not base edit-image

**Re-audit correction:** MCP `edit_image` is tagged **"(pro)"** in its own description and takes a *list* of images plus an optional reference-image mode switch — that shape matches `EditImagesV2Request` (`edit_images` list of 1-16 + `method`: text/reference + `reference_image`), not base `EditImageRequest` (single `image`, text-only, has `color_image`/`text_guidance_scale` that `edit_image` lacks). So `edit-images-v2` is the full `=` match; base `edit-image` is ◐ (a scoped subset of the broader Pro tool). Still REST-only or partial:

- `POST /edit-image` (base) — ◐ partial: `edit_image` can perform a single-image, text-only edit as a subset of its range, but is the Pro/batch tool, not a dedicated base-tier match. Note this is *not* the cheap MCP edit path either — `edit_image_pixen` (2026-09-08, 1 generation) is, and it matches `edit-image-pixen`, a different endpoint again
- `POST /image-to-pixelart-pro` (older Pro) — ◐ partial: MCP `image_to_pixelart_pro_flash` performs the same automatic native-scale conversion, but uses the separate Pro Flash model/tier
- `POST /image-to-text` — returns a PixelLab-ready text description from an image; no MCP tool is documented
- `POST /resize`
- `POST /remove-background`

Note: MCP `create_map_object` may accept `background_image` / `inpainting` parameters. Those are map-object generation controls, not generic replacements for `edit-image` or `inpaint`.

### 3. Inpaint (1) — MCP's inpaint tool is Pro-tier (inpaint-v3), not base inpaint

**Re-audit correction:** MCP `inpaint_image` has a `crop_to_mask` field that exists **only** on `InpaintV3Request` — base `InpaintRequest` has no such field and instead carries PixFlux-style weak-guidance controls (`direction`, `isometric`, `shading`, `outline`, `detail`, `text_guidance_scale`, `init_image`, `color_image`) that `inpaint_image` doesn't expose. So `inpaint-v3` is the full `=` match; base `inpaint` is ◐. Still open:

- `POST /inpaint` (base) — ◐ partial: `inpaint_image` covers the core mask-regenerate job but lacks base's extra weak-guidance generation controls, and is fundamentally the Pro-shaped tool, not a dedicated base-tier match

### 4. Raw animation, rotation, skeleton (9) — MCP now has standalone raw-animation and outfit-transfer tools

MCP `animate_image` animates an arbitrary supplied image directly from frame URLs or inline base64, closing the core `animate-with-text-v3` gap and partially covering interpolation at v3 tier. MCP `edit_image` also applies one edit consistently across a list of frames, partially covering `edit-animation-v2`. MCP `transfer_outfit` now covers the documented animation outfit-transfer workflow. MCP `animate_character` / `animate_object` separately require managed assets. Fully REST-only: legacy skeleton estimation/animation and single-image rotate.

- `POST /animate-with-text` (base/legacy; `reference_image`+`action`) — ◐ partial: capability covered by MCP `animate_*` `action_description` (modern `mode="v3"`), managed asset only — `reference_image`'s subject/style role has no match on raw `animate_image` either
- `POST /animate-with-text-v2` (Pro; `reference_image`+`action`) — ◐ partial: same as above, and MCP documents no matching Pro/v2 mode, so the version match is unconfirmed; managed asset only
- `POST /interpolation-v2` (Pro; *required* `start_image`+`end_image`) — ◐ partial: MCP `animate_image(first_frame_base64, last_frame_base64)` covers the capability with no managed asset needed, but `last_frame_base64` is `animate-with-text-v3`'s own optional `last_frame` field — so it is the v3 model interpolating, not the Pro `interpolation-v2` model; `animate_*(mode="v3", custom_start_frame_base64, end_frame_base64)` covers the managed-asset case
- `POST /generate-8-rotations-v2` (Pro) — ◐ partial: MCP `create_character(mode="v3", reference_image_url/base64)` rotates an exact character sprite into managed directions; `create_8_direction_object` creates eight object views but does not expose REST's `method` selector
- `POST /generate-8-rotations-v3` — ◐ partial: MCP v3 rotates the exact character sprite, but stores the result as a managed character; it has no matching raw-image result workflow
- `POST /edit-animation-v2` (Pro) — ◐ partial: MCP `edit_image` applies the same text edit consistently across a list of frames, but does not expose REST's dedicated animation endpoint or its shared `target_palette` control
- `POST /animate-with-skeleton` (`skeleton_keypoints`, legacy three-frame shape) — fully REST-only; MCP Skeleton v3 uses a different request contract
- `POST /estimate-skeleton` — fully REST-only
- `POST /rotate` (single arbitrary rotation) — fully REST-only

There is no public raw *4-rotation batch* route: the batch rotation routes are 8-direction only. The *managed object* animation endpoint `/objects/{id}/animations` is a full `=` match to MCP `animate_object`. Managed character routes share template, Skeleton v3, v3, and PixMiniMax modes but retain REST-only `pro`, so those partial differences are listed under managed-character route differences above. `animate-with-text-v3`, raw `animate-pixminimax`, and Skeleton v3 are full `=` matches via `animate_image`, `animate_image_pixminimax`, and `animate_with_skeleton_v3`; they do not appear in the raw-animation gap list.

### 5. Prompt enhancement (3) — no MCP prompt-helper tools

MCP exposes `search_help` for docs Q&A, which is not a prompt rewriter:

- `POST /enhance-pixen-prompt`
- `POST /enhance-character-v3-prompt`
- `POST /enhance-animation-v3-prompt`

### 6. Managed-asset export (3) — MCP has create/get/list/delete/tags but no packaged export

MCP covers the asset lifecycle except packaged exports:

- `GET /characters/{id}/zip` (full-bundle ZIP export) — ◐ partial: MCP `get_character` returns a download link, but no documented full-bundle ZIP export
- `GET /characters/{id}/spritesheet` (2026-09-08) — none: a ZIP holding one uniform-grid sheet PNG (row 0 rotations, then one row per animation-direction, every cell the size of the largest frame, frames centred and never rescaled) plus a layout JSON. Unauthenticated — the random character id is the access key. Use `/zip` instead for individual frame PNGs or every state of a character group
- `GET /objects/{id}/spritesheet` (2026-09-08) — none: the object twin of the row above; this one does require a bearer token and only exports objects you created

(The `PATCH /characters/{id}/tags` and `PATCH /objects/{id}/tags` set-tags routes were listed here before 2026-07-19; MCP now covers them with `update_character_tags` / `update_object_tags`.)

### 7. Talking portraits (1) — MCP lip sync is managed-character only

- `POST /lip-sync` — ◐ partial: MCP `get_lip_sync` returns the same plan for a character with stored visemes, but REST can also produce a stateless plan from `viseme_count` without a managed character. Portrait attachment, vocal animation create/get, and talking GIF rendering have full MCP counterparts.

### 8. Managed-character route differences (3)

- `POST /create-character-pro` — ◐ partial: MCP `create_character(mode="pro")` supports concept images; REST alone documents a Pro-route `method` selector and `style_description`. MCP's exact-sprite rotation is on its separate v3 workflow.
- `POST /animate-character` and `POST /characters/animations` — ◐ partial by mode: template, Skeleton v3, v3, and PixMiniMax are exposed on both surfaces, but REST additionally supports legacy managed `mode="pro"` and `target_palette`, which current MCP `animate_character` does not.

### 9. Animated VFX (1)

- `POST /vfx` — ◐ partial: MCP `vfx_workbench` makes and saves the same kind of animated effect, but it is agent-authored; no MCP tool runs PixelLab's description-driven effects artist. PixelLab's REST description itself recommends the MCP workbench for agents.

### Not counted as asset gaps

- `GET /background-jobs/{job_id}` — REST's generic async poll. MCP deliberately uses per-resource `get_*` tools instead, so this is a different async model, not a missing capability.
- `GET /llms.txt` — the docs index itself, not an asset operation.
- `GET /pro-flash/cost` — REST's provisional operation/size/direction estimate. MCP documents the same price-check purpose through its existing capability lookup, without a separate tool; actual charged usage belongs to the completed job.

**Total: 29 public REST v2 operations without a full, dedicated MCP match** (3 image gen + 5 edit/convert/description + 1 inpaint + 9 raw animation/rotation + 3 managed-character differences + 3 prompt enhance + 3 managed-asset export + 1 talking-portrait route + 1 animated VFX route). Sixteen have partial overlap: `create-character-pro`, `generate-with-style-v2`, base `edit-image`, `image-to-pixelart-pro`, base `inpaint`, `animate-with-text`, `animate-with-text-v2`, `interpolation-v2`, `generate-8-rotations-v2`, `generate-8-rotations-v3`, `edit-animation-v2`, `characters/{id}/zip`, stateless `lip-sync`, both managed character-animation endpoints' REST `pro` mode, and `vfx`.

## MCP Tools With No REST v2 Counterpart

The mirror of the gap list above: MCP tools without a documented public REST v2 counterpart. Of the 118 MCP tools in the snapshot, 40 have no documented REST v2 counterpart: 37 map/platform tools, two gallery/asset-save tools, and PixelArt Workbench. The 2026-10-19 refresh added MCP-only `place_map_tiles`, while `vfx_workbench` now has the partial REST counterpart `POST /vfx` and leaves this list.

### Maps, platform, agent, sandbox, chat (37) — genuinely MCP-only

No public REST v2 art API covers these; they exist only as MCP tools. Every platform tool except `get_balance` (which maps to `GET /balance`) is here. There is no REST fallback to offer — if these tools are not visible, the capability is unavailable.

- **Maps (new in the 2026-09-08 refresh; `place_map_tiles` added 2026-10-19):** `create_map`, `delete_map`, `list_maps`, `get_map`, `edit_map`, `view_map`, `place_map_tiles`, `place_map_object`, `list_map_objects`, `move_map_object`, `remove_map_object`
- **Projects:** `list_projects`, `add_to_project` (accepts characters, objects, tilesets, maps, gallery images, and saved VFX effect IDs in game or folder projects), `remove_from_project`
- **Chat (game-building agent):** `chat_list_conversations`, `chat_get_messages`, `chat_send_message`
- **Sandbox (code execution + deploy):** `sandbox_create_session`, `sandbox_destroy_session`, `sandbox_bash`, `sandbox_run`, `sandbox_read`, `sandbox_read_image`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`, `sandbox_deploy_worker`, `sandbox_undeploy`, `sandbox_playtest`
- **Deployed agents:** `agent_list`, `agent_inspect`, `agent_talk`
- **Job control:** `list_jobs`, `wait_for_jobs` — REST now matches cancellation with `DELETE /background-jobs/{job_id}`, but still has no active-job list or all-jobs wait
- **MCP meta:** `search_help` (docs Q&A), `agent_feedback`, `search_knowledge` (Phaser/game-dev knowledge base)

**Maps are now a real public surface.** Before the 2026-09-08 refresh no public map CRUD was documented anywhere, and map work meant the website Map Workshop. MCP now creates a map from a top-down tileset (`create_map`, which also attaches every connected tileset sharing that tile size and base tile), paints terrain with `edit_map` `path`/`rect` ops over negative-capable cell coordinates (with `dry_run` to preview without saving), reads it back as an ASCII grid (`get_map`) or a rendered image (`view_map`), and places, moves, lists, or removes objects and characters on it. Since 2026-10-19, `create_map` can instead start a tile map from a tiles-pro, path, or building tile group (`tile_group_id`), and `place_map_tiles` places, stacks (levels 0–63), or erases that group's tiles on tile layers, adds further groups, and supports `dry_run`; erasing at a level also removes everything stacked above it. The latest MCP docs add exact world-pixel placement with `foot` or `top_left` anchors and atomic multi-placement batches; moves can set a new layer without changing the stored position. REST v2 still has no map CRUD or placement routes.

Handle these per [`mcp-platform-tools.md`](../../skills/pixellab-pip/references/mcp-platform-tools.md) — most are account reads or state-changing actions that need explicit approval.

### Formerly MCP-only, now on REST too (as of 2026-07-19)

The 2026-07-19 snapshot added REST routes for the `delete` / `list` lifecycle helpers this section previously listed as MCP-only, so they are no longer gaps: `delete_topdown_tileset` (`DELETE /tilesets/{id}`), `delete_sidescroller_tileset` (`DELETE /tilesets-sidescroller/{id}`), `delete_isometric_tile` (`DELETE /isometric-tiles/{id}`), `delete_tiles_pro` (`DELETE /tiles-pro/{id}`), `delete_animation` (`DELETE /characters/{id}/animations`), `list_sidescroller_tilesets` (`GET /tilesets-sidescroller`), `list_tiles_pro` (`GET /tiles-pro`).

### Not counted as MCP-only

- Per-resource `get_*` tools map to a dedicated REST GET where one exists — `GET /generate-font-pro/{job_id}` (`get_font`), `GET /map-objects/{id}` (`get_map_object`), `GET /portrait-character-pro/{job_id}` (`get_portrait_character`), `GET /tilesets-sidescroller/{id}` (`get_sidescroller_tileset`) — and otherwise to the generic `GET /background-jobs/{job_id}` async poll. Either way they are not gaps.
- `pixellab://docs/...` resources (Godot/Unity/Python/Wang/sidescroller/isometric/overview integration guides) are MCP-only, but they are documentation, not an API surface.

### Pixel-art command workflow (1) — MCP-only

`pixelart_workbench` is the model-authored pixel-art command tool. It accepts PixelLab IDs and supported image references, not local paths, and has no public REST route. The 0.4.125 announcement reports lower token use from PixelLab's testing; that estimate was not independently measured here. For the accepted input forms and live help contract, see the [PixelArt Workbench reference](../../skills/pixellab-pip/references/pixelart-workbench.md).

### Gallery and asset save (2) — MCP-only

`list_images` reads the Creator gallery and `save_to_asset` writes a generated or edited image into a character, object, animation direction, gallery entry, or an existing top-down or sidescroller tileset. Tileset saves replace the full sheet while keeping its ID and tile layout; no public REST v2 endpoint documents these operations. `save_to_asset` can replace existing remote content, so apply SKILL.md's explicit destructive-action gate before using it on an existing target.

**Total: 40 MCP tools without a documented REST v2 counterpart** — 37 in map/platform layers, two gallery/asset-save tools, and one PixelArt Workbench tool. Version 0.4.125 added `remove_from_project`, `wait_for_jobs`, and `pixelart_workbench`; the 2026-10-03 refresh added `list_images` and `save_to_asset`; the 2026-10-11 refresh added `vfx_workbench`, which left this list when REST `POST /vfx` appeared on 2026-10-19 (partial parity; see Animated VFX above); the same refresh added `place_map_tiles`. The new Skeleton v3 tool and `transfer_outfit` have REST counterparts and are counted as parity.

## Routing Implications

These follow from the gaps above and are already encoded in SKILL.md's Intent Router and Surface Rules — this section states *why*, not new rules:

- Category 1's BitForge/freeform UI gaps and partial multi-image style route, category 2's base `edit-image` (◐, not a dedicated match — route there when the extra `color_image`/`text_guidance_scale` controls matter, or when `edit_image_pixen` is too small and Pro-tier `edit_image` overreaches), its partial older Pro converter (`image-to-pixelart-pro`; MCP Pro Flash performs the same conversion on a different tier), and the remaining `resize`/`remove-background` gaps, category 3's base `inpaint` (◐, same reasoning — its weak-guidance controls aren't on `inpaint_image`), and category 5 are why the Intent Router still sends those specific operations to REST v2 even in an MCP-enabled agent.
- Category 4 no longer means a user asking to "animate this sprite I attached" is REST-only — MCP `animate_image`, `animate_image_pixminimax`, `animate_with_skeleton_v3`, and `transfer_outfit` animate or transform raw supplied frames directly. `edit_image` also applies one edit consistently across frame lists, with REST retaining the dedicated animation endpoint and its `target_palette` control. Legacy skeleton estimation/animation and single-image rotate remain REST-only.
- Managed asset types (character, object, tileset, tile, font, UI asset, map object) are the overlap zone: prefer MCP when its tools are visible, fall back to the matching REST endpoint otherwise. Raw-image generate/edit/inpaint/animate are now a second overlap zone: MCP covers PixFlux, Pixen, and Pro-tier generate/edit/inpaint/animate; REST remains necessary for BitForge, multi-image style controls, base (non-Pro) edit/inpaint controls, and the older Pro image-to-pixel-art tier when its model matters.
- The 2026-09-08 Cleanup family (`correct-pixelart`, `reduce-colors`, `unzoom`) and `image-to-pixelart` are a third overlap zone with full parity both ways, so an MCP-first agent no longer has to fall back to REST — or to a labeled local fallback — for palette reduction, unzooming, or pixel-art clean-up. Maps, gallery browsing/save-back, and active-job list/all-job wait are the reverse case: MCP-only, with no REST route to offer if the tools are not visible; job cancellation itself is now shared.
- Pro Flash adds a fourth overlap zone for one-image creation, character/object rotations, editing, masked editing, and image-to-pixel-art conversion. It is not a new default: prices are provisional, no quality test was run, and the exact-mask promise has not been verified. Check native dimensions and the price split with MCP `get_pro_flash_capabilities`, or REST capabilities plus `/pro-flash/cost`, before seeking approval; use completed-job usage as the charge.

## Caveats

- Snapshot-bound: the MCP inventory and REST index/OpenAPI were refreshed on 2026-10-29 (UTC). Counts cover 102 REST path templates (113 operations), 275 schema components, and 118 MCP tools; field descriptions and behavior can change without affecting these counts. Both surfaces can drift; the doc-watch cache workflow ([`pixellab-doc-watch-cache.md`](pixellab-doc-watch-cache.md)) is how drift is detected.
- MCP↔REST are not guaranteed pixel-identical for the same prompt/seed even where parity is `=`; treat them as one workflow family with overlapping controls, not field-for-field twins. REST generally exposes the fuller documented schema, but Pro Flash MCP adds URL/source-ID inputs and a capability-based price check, while REST has a dedicated cost-estimator route. Pro Flash's image provider explicitly does not promise deterministic output from a recorded seed.
- Re-audit correction (2026-10-08): the refreshed MCP `create_character` schema now supports v3 reference images for quadrupeds when `body_type="quadruped"` and the matching `template` are supplied, closing the former REST/MCP reference gap. MCP v3 without a reference image is now documented as humanoid-only; quadruped text creation remains available in standard and Pro modes. REST supports matching quadruped `template_id` references. `create-character-pro` is partial: both surfaces accept concept images, while REST retains the Pro-route `method` selector and `style_description` controls that MCP lacks; MCP's exact-sprite rotation is on its separate v3 workflow. Managed character animation also has a mode-level gap: REST retains legacy `mode="pro"`, while current MCP `animate_character` offers template, Skeleton v3, v3, and PixMiniMax.
- This spike compares only public REST v2 and public MCP. Website/Map Workshop, Pixelorama/editor, Aseprite-extension, and legacy v1 routes are out of scope here; see [User-Facing Term To Backend Mapping](pixellab-user-facing-term-backend-mapping.md) for those surfaces.
- Methodology note (2026-07-26 re-audit): base-vs-Pro tier assignments in this doc are now checked by diffing full REST request-schema field lists (property names, required lists, and descriptions) against each MCP tool's documented parameters and its own prose tags (e.g. a tool's description literally saying "(pro)"), not by matching on name similarity alone. Two families (`edit-image`/`edit-images-v2`, `inpaint`/`inpaint-v3`) had the base/Pro assignment backwards in an earlier pass specifically because the base-tier endpoint's name is the more obvious lexical match to the MCP tool's name, even though its field shape didn't match. Treat any future "obviously-named" match in this doc as unconfirmed until the schema fields are actually compared.
