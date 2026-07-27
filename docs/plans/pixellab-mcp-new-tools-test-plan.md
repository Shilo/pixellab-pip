# PixelLab MCP New-Tools Verification — Plan

Status: executed 2026-07-27. Results: `../pixellab/pixellab-mcp-new-tools-test-results.md`. Companion:
`../pixellab/pixellab-mcp-vs-rest-route-parity.md`
(the schema-verified parity source every comparison below is drawn from) and
`../pixellab/pixellab-doc-watch-cache.md` (the refresh mechanism that surfaced these tools).

## Goal

Verify that every MCP tool added across the last 3 doc-watch refreshes that detected `mcp_docs`
changes (`2026-07-19`, `2026-07-26T19:55Z`, `2026-07-26T21:03Z`) actually works: callable with valid
inputs, rejects invalid inputs sanely, returns the documented output shape, and — for every tool with
a documented REST counterpart — produces output **equivalent or better** than calling that REST
endpoint directly, **including on performance and stability**, not just output correctness (see
Performance & Stability Comparison below) — REST calls require the agent to author a script per call
plus a manual poll loop, while MCP tools are typed direct calls with a matching getter; this plan
makes that operational difference measurable rather than assumed. This is a functional/regression and
operational-overhead check, not a prompt-quality or art-direction review.

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
  fidelity and comparable visual quality are. Every equivalence check also captures the Performance &
  Stability metrics below for that pair.
- **Error-path test**: 1-2 deliberately invalid calls per tool (bad id, out-of-range field, malformed
  mask) to confirm the tool fails with a clear, documented error rather than hanging, silently
  succeeding, or returning a malformed response. If a paid request reaches a job and fails, record
  the balance before submission, at failure, and after a 60-second recheck; report the charge as
  refunded, not refunded, or still pending.

## Performance & Stability Comparison

The open question driving this section: REST requires the agent to author a script for every call (a
curl/python invocation with a hand-built auth header and JSON body), then run a separate manual poll
loop against `GET /background-jobs/{job_id}`. MCP tools are called directly with typed, schema-checked
arguments and their own matching `get_*` getter. **Both surfaces are still asynchronous — MCP does not
eliminate polling, it only removes the script-authoring and request-serialization step around each
call.** This section makes that difference measurable instead of asserting it.

Capture these per surface, for every REST-equivalence pair already in the per-tool matrix below (not
a separate round of calls — instrument the same calls the plan already makes):

1. **Steps to completion**: count of distinct agent actions (tool calls / script executions) from
   issuing the request to having a verified, saved output in hand. REST: authoring+running the submit
   script, then one action per poll, then a decode/save step. MCP: one tool call, then one action per
   `get_*` poll. Record the raw count on both sides for the same request — this is the concrete version
   of "REST requires the agent to create scripts and poll constantly."
2. **Wall-clock time to completion**: timestamp at submission and at the poll that first reports
   `completed`, for both surfaces, on the same request content. Report the two durations side by side,
   not just "MCP was faster/slower" — generation queue time can dominate and swamp any surface-level
   overhead, so call out when that's the case rather than over-crediting either surface.
3. **Poll count and status-lag**: how many polls each surface needed, and whether the status lagged the
   actual ready result on either surface — `references/job-lifecycle.md` documents this as a known REST
   behavior under load ("the top-level `status` can briefly lag the ready result"); check whether MCP's
   `get_*` tools show the same lag or report readiness more promptly.
4. **Failure/retry incidents**: any transient error, timeout, malformed response, or required retry on
   either surface during the run, with what caused it. This is the core stability signal — a surface
   that needs zero retries across the run is more stable than one that needed several, independent of
   whether either one is ever unavailable outright.
5. **Malformed-call rejection**: for a deliberately invalid payload (already planned as an error-path
   test for most tools), note whether MCP's schema validation rejects it client-side before any network
   call, versus REST where a hand-authored script can send a malformed request all the way to
   PixelLab's server before it's rejected. This is a real structural difference worth confirming
   empirically, not just asserting.
6. **Inline-base64 truncation risk (MCP-specific)**: several MCP tools (`create_character`'s
   `reference_image_base64`, and by extension the base64 image inputs on `create_image_pixflux`,
   `edit_image`, `inpaint_image`, `animate_image`) are already documented elsewhere in this skill as
   at risk of MCP-client truncation on large inline base64 ("MCP clients routinely truncate large
   inline base64"). For each of those tools' live tests, use one deliberately large input image
   (near the tool's own max dimensions) and confirm the tool either handles it intact or fails
   cleanly — a silently corrupted/truncated image accepted as if valid would be a real MCP-specific
   stability defect. REST has no equivalent risk for file-based script input, so this check has no
   REST-side counterpart to compare against — it is purely an MCP risk surface.
7. **Auth/session overhead (structural note, not a live measurement)**: REST requires the bearer token
   to be present in every individual script/call; MCP authenticates once at the client/connection
   level. Record this as a design-level stability factor in the final report (fewer places per call to
   mis-load, leak, or omit a token) rather than trying to time it.

**Repeat-count budget**: run steps 1-4 three times each for the free/cheap tools (`update_character_tags`/
`update_object_tags`, `create_image_pixflux`, `create_image_pixen`) to get a variance signal, not just
one data point. For the pricier tools (`edit_image`, `inpaint_image`, `animate_image`,
`create_path_tiles`, `create_building_kit`), run once — repeating three times would roughly triple
their already-nontrivial cost for a metric that matters less at that price point. `create_image_pro`
gets performance metrics only if its REST-equivalence call isn't skipped for cost (see Cost budget); if
skipped, say so explicitly in the report rather than silently omitting the row.

## Prerequisites

- MCP tools visible and connected (`ToolSearch select:mcp__pixellab__<name>` for each tool in scope,
  confirm schema loads).
- `PIXELLAB_SECRET` configured for the REST-side equivalence calls (`references/credentials.md`).
- Two cheap fixture assets, created once and reused across the plan (not part of the 11 tools under
  test — just prerequisites for the tag tools, which need an existing `character_id`/`object_id`):
  - one `create_character(description="test dummy", mode="standard")` call (~1 generation) for
    `update_character_tags`.
  - one `create_1_direction_object(description="test cube", size=32)` call (~20 generations; the
    live route returns a review pack even at this size) for `update_object_tags`.
- Output folder: `.local/mcp-tool-verification/<run-id>/` (gitignored, throwaway QA artifacts — this
  is a functional check, not a user asset request, so it does not belong in
  `pixellab-pip-generations/` or get a blueprint/manifest per `SKILL.md`'s Asset Integrity section).
- Before any paid call, apply the normal cost-approval gate (`references/auto.md`): show the full
  predicted call list and total below, get approval once, then run smoke+live+equivalence+error tests
  per tool without re-asking per call.

## Cost budget (full matrix estimate)

| Group | Generations (approx) |
|---|---|
| Fixtures (1 character + 1 object) | ~21 |
| `create_image_pixflux` smoke + live + REST-equivalence pair ×3 (performance repeat count) | ~8 |
| `create_image_pixen` smoke + live + REST-equivalence pair ×3 (performance repeat count) | ~8-10 |
| `create_image_pro` full smoke/live/coverage/REST matrix (20-40 each call) | ~160 |
| `edit_image` full smoke/live/coverage/REST matrix | ~180 observed across 7 MCP calls plus 1 REST Pro call |
| `inpaint_image` full smoke/live/coverage/REST matrix (20-40 each accepted call) | ~160 |
| `animate_image` full smoke/live/coverage/REST matrix | ~11 |
| `create_path_tiles` full smoke/live/coverage/REST matrix | ~80-160 |
| `create_building_kit` full smoke/live/coverage/REST matrix | ~100-200 |
| `update_character_tags` / `update_object_tags` | 0 (free) |

Budget roughly **1,000-1,100 generations** for the complete matrix, including accepted calls in cases
that were expected to reject. The completed 2026-07-27 verification run consumed 1,063 subscription
generations.
`create_image_pro`, edit/inpaint, and the tile kits dominate the budget — consider running Pro's smoke test at the smallest legal
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
  value at least once (spot check 2, not all 8); 32×32 (smallest legal square under the live
  1,024-pixel minimum-area check) and 400×400 (max, total area ≤160,000). Also send 16×16 and expect
  the live server to reject its 256-pixel area even though each side meets the declared 16px minimum.
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

Add one cross-tool **Performance & Stability Summary** table before the per-tool detail, columns:
tool | MCP steps-to-completion | REST steps-to-completion | MCP time (median if repeated) | REST time
(median if repeated) | failure/retry incidents (either surface) | malformed-call rejected client-side?
(MCP y/n) | base64-truncation risk observed? (y/n, MCP-only). Close the results file with one paragraph
answering the practical question this section exists to answer: for this tool family, does MCP's
typed-call-plus-getter pattern reduce agent-side operational overhead (fewer steps, fewer
script-authoring failure points) compared to REST's script-plus-manual-poll pattern, and does that
translate into measurably fewer incidents — separate from whether generation itself is faster, since
queue time is expected to dominate wall-clock and isn't a surface-level property.
