# PixelLab MCP New-Tools Verification — Plan

Status: plan only, not yet executed. Companion: `../pixellab/pixellab-mcp-vs-rest-route-parity.md`
(the schema-verified parity source every comparison below is drawn from) and
`../pixellab/pixellab-doc-watch-cache.md` (the refresh mechanism that surfaced these tools).

## Goal

Verify that every MCP tool added across the last 3 doc-watch refreshes that detected `mcp_docs`
changes (`2026-07-19`, `2026-07-26T19:55Z`, `2026-07-26T21:03Z`) actually works: callable with valid
inputs, rejects invalid inputs sanely, returns the documented output shape, and — for every tool with
a documented REST counterpart — produces output **equivalent or better** than calling that REST
endpoint directly. This is a functional/regression check, not a prompt-quality or art-direction
review.

## Scope — the 11 net-new tools

Derived from `.local/pixellab-doc-watch/reports/20260719T222026Z.md`,
`20260726T195547Z.md`, and `20260726T210346Z.md` (`create_image` was added in the second refresh and
replaced by the third — it is not tested separately since it no longer exists).

| Tool | Added | REST counterpart | Parity tier | Cost class |
|---|---|---|---|---|
| `update_character_tags` | 07-19 | `PATCH /characters/{id}/tags` | `=` | free, sync |
| `update_object_tags` | 07-19 | `PATCH /objects/{id}/tags` | `=` | free, sync |
| `create_image_pixflux` | 07-26 21:03 | `POST /create-image-pixflux` (+ `-background`, byte-identical schema) | `=` | 1 generation |
| `create_image_pixen` | 07-26 21:03 | `POST /create-image-pixen` | `=` | 1 generation |
| `create_image_pro` | 07-26 21:03 | `POST /generate-image-v2` | `=` | 20-40 generations |
| `edit_image` | 07-26 19:55 | `POST /edit-images-v2` (Pro tier — **not** base `/edit-image`, which is only ◐) | `=` | Pro-tier, cost varies by size/frame-count |
| `inpaint_image` | 07-26 19:55 | `POST /inpaint-v3` (Pro tier — **not** base `/inpaint`, which is only ◐) | `=` | Pro-tier |
| `animate_image` | 07-26 19:55 | `POST /animate-with-text-v3` | `=` (◐ vs Pro `interpolation-v2`, expected — different model tier) | scales with `width×height×frame_count` |
| `create_path_tiles` | 07-26 19:55 | `POST /create-tiles-pro` (`tile_feature: "roads"`) | `=` | Pro tile cost |
| `create_building_kit` | 07-26 19:55 | `POST /create-tiles-pro` (`tile_feature: "building"`) | `=` | Pro tile cost |
| `get_image` | 07-26 19:55 | n/a (getter only) | — | free |

`get_image` is the shared getter for the six raw-image tools above (`create_image_pixflux/pixen/pro`,
`edit_image`, `inpaint_image`, `animate_image`) — it is exercised by every live test in that group
rather than tested in isolation, plus one dedicated error-path check.

## Methodology — two tiers per tool

- **Smoke test**: call is accepted (no 422/validation error) with a minimal/cheapest-legal payload,
  response has the documented shape (`job_id`/`character_id`/etc., correct field types). For the two
  free/sync tag tools, smoke and live are the same call. For paid tools, a smoke test still spends the
  tool's minimum cost — there is no zero-cost way to confirm a generation tool accepts a call, so smoke
  tests use the cheapest legal size/config for that tool.
- **Live test**: a realistic, larger call, polled to completion via the documented getter, with the
  actual output inspected (dimensions, format, transparency, frame count — whatever the tool promises)
  against the request.
- **Equivalence check** (only for tools with a REST counterpart): call the MCP tool and the REST
  endpoint with matching content and the same `seed`, then compare output shape (dimensions, frame
  count, format) and — visually — that both are plausible renders of the same prompt. Exact
  pixel-identical output is **not** the bar (generation is not guaranteed deterministic across
  surfaces even at the same seed, per `docs/pixellab/pixellab-mcp-vs-rest-route-parity.md`); shape
  fidelity and comparable visual quality are.
- **Error-path test**: 1-2 deliberately invalid calls per tool (bad id, out-of-range field, malformed
  mask) to confirm the tool fails with a clear, documented error rather than hanging, silently
  succeeding, or returning a malformed response.

## Prerequisites

- MCP tools visible and connected (`ToolSearch select:mcp__pixellab__<name>` for each tool in scope,
  confirm schema loads).
- `PIXELLAB_SECRET` configured for the REST-side equivalence calls (`references/credentials.md`).
- Two cheap fixture assets, created once and reused across the plan (not part of the 11 tools under
  test — just prerequisites for the tag tools, which need an existing `character_id`/`object_id`):
  - one `create_character(description="test dummy", mode="standard")` call (~1 generation) for
    `update_character_tags`.
  - one `create_1_direction_object(description="test cube", size=32)` call (~1 generation, single
    candidate since `size≤42`) for `update_object_tags`.
- Output folder: `.local/mcp-tool-verification/<run-id>/` (gitignored, throwaway QA artifacts — this
  is a functional check, not a user asset request, so it does not belong in
  `pixellab-pip-generations/` or get a blueprint/manifest per `SKILL.md`'s Asset Integrity section).
- Before any paid call, apply the normal cost-approval gate (`references/auto.md`): show the full
  predicted call list and total below, get approval once, then run smoke+live+equivalence+error tests
  per tool without re-asking per call.

## Cost budget (rough floor, smallest-legal configs; live/equivalence tests add more)

| Group | Generations (approx) |
|---|---|
| Fixtures (1 character + 1 object) | ~2 |
| `create_image_pixflux` smoke + live + REST equivalence | ~3 |
| `create_image_pixen` smoke + live + REST equivalence | ~3 |
| `create_image_pro` smoke + live + REST equivalence (20-40 each call) | ~60-120 |
| `edit_image` smoke + live + REST equivalence | ~3-6 |
| `inpaint_image` smoke + live + REST equivalence | ~3-6 |
| `animate_image` smoke + live + REST equivalence | ~6-12 |
| `create_path_tiles` smoke + live + REST equivalence | Pro tile cost ×2 |
| `create_building_kit` smoke + live + REST equivalence | Pro tile cost ×2 |
| `update_character_tags` / `update_object_tags` | 0 (free) |

`create_image_pro` dominates the budget — consider running its smoke test at the smallest legal
canvas (16×16) to keep even the "cheap" check inside the 64-candidate bucket, and treat its
REST-equivalence call as optional/skippable if budget is tight, since `generate-image-v2` parity is
already the most exhaustively re-verified row in the parity map.

## Per-tool test matrix

### `update_character_tags` / `update_object_tags`

- **Smoke = live** (free, synchronous, no polling): call with `tags: ["qa-smoke"]` on the fixture
  character/object. Assert the full replacement list comes back as sent.
- **Coverage**: empty list (`tags: []`) clears all tags — verify via a follow-up `get_character`/
  `get_object` (or `list_characters`/`list_objects` filter) that no tags remain; a 21-tag list (over
  the documented 20-max) — expect a validation error; a tag with leading/trailing whitespace and mixed
  case — expect it trimmed and case-insensitively deduped against an existing tag.
- **Error path**: a random non-existent UUID for `character_id`/`object_id` — expect a clear 404-class
  error, not a silent no-op.
- **REST equivalence**: `PATCH /characters/{id}/tags` / `PATCH /objects/{id}/tags` with the same tag
  list on the same fixture id; compare the returned tag set.

### `create_image_pixflux`

- **Smoke**: `description="red square", width=32, height=32, no_background=true` — 1 generation.
- **Live**: `description="cute dragon sprite", width=64, height=64, no_background=true`, plus a second
  call exercising `init_image_base64`+`init_image_strength=150` (img2img edit) on the first call's
  output. Verify output PNG dimensions match request, transparency present.
- **Coverage**: `color_image_base64` forced-palette path; `isometric=true`; each `direction` enum
  value at least once (spot check 2, not all 8); boundary sizes 16×16 (min) and 400×400 (max, total
  area ≤160,000 — pair with a smaller partner dimension to stay in bounds).
- **Error path**: `width=15` (below min) and `width=401` (above max) — expect validation errors, not
  silently clamped output.
- **REST equivalence**: `POST /create-image-pixflux` with identical `description`/size/`seed`; compare
  dimensions and background handling.

### `create_image_pixen`

- **Smoke**: `description="ornate iron key", width=32, height=32`.
- **Live**: `description="mossy stone wall", width=128, height=128, no_background=false`.
- **Coverage**: `no_background=true` for a sprite-style request; boundary sizes 16×16 (min) and
  512×512 (max total area).
- **Error path**: `width=17` on an odd-not-multiple concern — verify whether REST's `multipleOf: 4`
  constraint (present on `CreateImagePixenRequest`, absent from the MCP schema per the parity map) is
  actually enforced server-side even when MCP's own declared schema doesn't require it; if REST
  rejects 17 but MCP's tool accepts it, that's a real cross-surface behavior gap worth flagging even
  though the file `icon.md` already documents the schema-level asymmetry.
- **REST equivalence**: `POST /create-image-pixen` with identical `description`/size/`seed`.

### `create_image_pro`

- **Smoke**: `description="ornate iron key", width=16, height=16` (smallest legal canvas, stays in the
  64-candidate bucket, cost is per-call not per-candidate).
- **Live**: `description="knight in gold armor", width=128, height=128`, then a second call adding
  `reference_images` (1-2 labelled entries, e.g. the knight output plus a separate armor swatch) to
  verify multi-reference composition.
- **Coverage**: `style_image_base64`+`style_copy` (test with a 1-2 element subset of
  `color_palette`/`outline`/`detail`/`shading`, not all four, to confirm partial-copy actually
  narrows what's copied); confirm `style_image_base64` takes exactly **one** image, not an array —
  this is the tool's documented boundary against REST's separate `generate-with-style-v2` endpoint
  (required 1-4 blended `style_images` + free-text `style_description`), which has no MCP tool and is
  intentionally out of scope for this plan; combine `reference_images` (subject) with
  `style_image_base64` (style) in one call and confirm both apply independently — the output should
  match the reference's subject *and* the style image's look, since they are documented as separate
  mechanisms, not aliases of each other; aspect-gated max sizes — confirm 512×512 square accepted, and
  that an off-ladder combination like 688×512 is rejected per the documented aspect-gating (echoes the
  same gate already verified on `create_ui_asset`, but on a different tool — worth an independent
  check).
- **Error path**: 5 `reference_images` (over the documented max of 4) — expect a validation error.
- **REST equivalence**: `POST /generate-image-v2` with identical `description`/size/`seed`/
  `reference_images` (mapping MCP's `usage` label to REST's `usage_description` field per the parity
  map's confirmed field-name mismatch); compare candidate-count bucket and image dimensions.

### `edit_image`

- **Smoke**: `images_base64=[<32x32 png from create_image_pixflux smoke test>], description="add a red outline"`.
- **Live**: reference-mode call — `images_base64=[<source>], reference_image_base64=<a different
  style source>` — verify the tool actually switches modes (output reflects the reference's
  appearance, not just the text description) and that `description` becomes optional/refining as
  documented. Also test the multi-frame path: `images_base64` with 2-3 frames, confirm the same edit
  is applied consistently across all of them (this is the tool's core differentiator vs base
  `edit-image`, so it's the highest-value thing to verify).
- **Coverage**: frame-count-vs-size limit table (≤64px→16 frames, ≤80px→9, ≤128px→4, larger→1, one
  fewer in reference mode) — test at least the ≤64px/16-frame boundary and the >128px/1-frame boundary.
- **Error path**: 17 frames at ≤64px (over the 16-frame cap) — expect rejection; a >512×512 input
  image — expect rejection (documented max input size).
- **REST equivalence**: `POST /edit-images-v2` (not base `/edit-image` — confirmed non-match per the
  parity map) with the same `edit_images`/`method`/`description`; compare that both apply the edit
  consistently across the same input set.

### `inpaint_image`

- **Smoke**: rectangular mask — `image_base64=<source>, description="plain grass, no object",
  mask_x=8, mask_y=8, mask_width=8, mask_height=8` on a 32×32 source.
- **Live**: custom `mask_image_base64` path (white=regenerate/black=preserve) on a larger (e.g.
  128×128) source, confirm pixels outside the mask are byte-identical to the input and only the masked
  region changed. Also test `crop_to_mask=false` vs the `true` default and confirm the visible
  difference at the mask boundary.
- **Coverage**: mask fully covering the image (edge case — effectively a full regenerate); a
  rectangle mask specified with `mask_x+mask_width` exceeding the image bounds.
- **Error path**: the out-of-bounds mask rectangle above — expect a clear validation error, not a
  silently clamped/cropped mask; supplying both `mask_image_base64` and `mask_x/y/width/height`
  simultaneously — confirm documented precedence or rejection.
- **REST equivalence**: `POST /inpaint-v3` (not base `/inpaint`) with the same image, mask, and
  `description`; compare that both preserve the unmasked region pixel-for-pixel and that
  `crop_to_mask` behaves the same on both surfaces.

### `animate_image`

- **Smoke**: `first_frame_base64=<64x64 source>, action="idle breathing", frame_count=4` (cheapest
  legal: small frame, min frame count).
- **Live**: a start→end tween — `first_frame_base64=<open>, last_frame_base64=<closed>,
  action="chest lid closing", frame_count=6` — verify `get_image` returns `frame_count+1` images
  (frame 0 = echoed input), and that the last generated frame visually approaches the supplied
  `last_frame_base64`.
- **Coverage**: pixel-budget boundary — 256×256 frame at `frame_count=8` (budget exactly 524,288,
  should succeed) vs `frame_count=10` at the same size (budget exceeded, should reject); odd
  `frame_count` (e.g. 5) — expect rejection since the field is documented EVEN-only.
- **Error path**: a first frame larger than 256×256 — expect rejection; `last_frame_base64` with
  different dimensions than `first_frame_base64` — expect rejection (documented "same size" constraint).
- **REST equivalence**: `POST /animate-with-text-v3` with the same `first_frame`/`action`/
  `frame_count`/`seed` (and `last_frame` for the tween case); compare frame count returned and that
  frame 0 is the echoed input on both surfaces.

### `create_path_tiles`

- **Smoke**: `description="grass with a dirt road"` (all defaults — `tile_type=square_topdown`,
  `tile_size=32`).
- **Live**: `tile_type="isometric", tile_size=64, description="stone floor with a mosaic walkway"` —
  poll via `get_tiles_pro`, confirm 18 configs are returned (straights/corners/T-junctions/crossroads/
  dead-ends/plain ground) with edge-rule bitmasks present.
- **Coverage**: `outline_mode="segmentation"` vs default `"outline"`.
- **Error path**: `tile_size=48` with `tile_type="square_topdown"` (which the tool description says
  requires exactly 32) — expect rejection.
- **REST equivalence**: `POST /create-tiles-pro` with `tile_feature: "roads"` and matching
  `description`/`tile_type`/`tile_size`; compare returned tile count and edge-rule shape.

### `create_building_kit`

- **Smoke**: `wall_description="stone brick walls", floor_description="flagstone floor"` (all
  defaults — `tile_type=isometric`, `tile_size=32`, `wall_tiles=2`).
- **Live**: `tile_type="oblique", oblique_lean=0.5, wall_tiles=3, floor2_description="wooden roof
  shingles"` — poll via `get_tiles_pro`, confirm floor/walls/doorways/pillar/stairs pieces are all
  present and wall segments carry outline rules matching floor-area shape as documented.
- **Coverage**: `layout="grid"` vs `"materials"` (confirm the isometric-default/square_topdown-default
  behavior actually differs when explicitly overridden).
- **Error path**: `wall_tiles=4` (over the documented 1-3 max) — expect rejection; `tile_size=16` with
  `tile_type="isometric"` (which requires 32-96) — expect rejection.
- **REST equivalence**: `POST /create-tiles-pro` with `tile_feature: "building"` and the matching
  `building_*` fields; compare returned piece set.

### `get_image` (exercised throughout, plus one dedicated check)

- **Error path**: call with a fabricated/non-existent `job_id` — expect a clear not-found error, not
  a hang or an empty-success response.
- **Coverage note**: since every raw-image live test above polls `get_image`, confirm across those
  polls that the "processing" → "completed" status transition is observable (not just a single
  final read) at least once, and that the completed response includes both inline image data and the
  documented no-auth download URLs.

## Execution order

1. Free tag tests first (`update_character_tags`/`update_object_tags`) — zero cost, run immediately
   after the two fixture creations.
2. Cheapest paid tools next: `create_image_pixflux`, `create_image_pixen` (1 generation each).
3. `edit_image` and `inpaint_image`, using outputs from step 2 as source images.
4. `animate_image`, using an output from step 2 as the first frame.
5. `create_path_tiles` and `create_building_kit` (independent of the raw-image chain, can run in
   parallel with steps 2-4 if budget allows).
6. `create_image_pro` last — priciest per call, run only after the cheaper tools have confirmed the
   MCP connection and polling loop both work correctly, so a failure there is more likely to be
   `create_image_pro`-specific rather than an environment problem.
7. REST-equivalence calls interleaved immediately after each tool's live test, while the exact request
   parameters are still in hand — not batched at the end.

## Reporting

Write results as a companion file, `docs/pixellab/pixellab-mcp-new-tools-test-results.md`, structured
per tool: smoke PASS/FAIL, live PASS/FAIL, coverage cases PASS/FAIL (list each), error-path PASS/FAIL
(list each), REST-equivalence verdict (equivalent / MCP better / MCP worse, with the specific
difference named — e.g. cost, output fidelity, missing field). Any FAIL gets a note on whether it's a
PixelLab-side bug (report upstream) or a skill-documentation mismatch (fix `references/`/`SKILL.md`
and re-run the relevant `dev-tools/qa.py`). "Equivalent or better" is the pass bar per tool — a tool
that only partially matches its REST counterpart's documented capability (there are none in this
11-tool set per the parity map — all are `=`) would need that gap called out explicitly rather than
silently marked PASS.
