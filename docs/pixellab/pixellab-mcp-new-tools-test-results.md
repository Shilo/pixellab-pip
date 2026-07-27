# PixelLab MCP New-Tools Verification Results

Run date: 2026-07-27  
Run ID: `20260727T040152Z`  
Plan: `docs/plans/pixellab-mcp-new-tools-test-plan.md`

The live MCP connection exposed all 11 scoped tools, `PIXELLAB_SECRET` was present for REST calls,
and the downloaded OpenAPI document contained 74 paths. The full run consumed **1,063 generations**;
cash credits were unchanged. All recoverable artifacts are in the gitignored
`.local/mcp-tool-verification/20260727T040152Z/` folder: verified PNGs and tile ZIPs, REST
request/response records, fixtures, and inspection aids.

## PixelLab Developer Fix List

### High priority

- **MCP `inpaint_image` — mask correctness:** MCP and REST changed pixels outside the mask or left
  the masked region unchanged. `crop_to_mask` made no visible difference, and MCP silently accepted
  an out-of-bounds rectangle.
- **MCP `create_image_pixen` — validation and billing:** MCP accepted a 17px-wide request, then the
  job failed with an HTTP 500 server error. REST rejected it immediately with an HTTP 422 validation
  response. The repeat failure was refunded: the balance was unchanged immediately after failure and
  at the 60-second recheck.

### Medium priority

- **MCP `edit_image` — input transport:** a valid inline PNG was truncated at 40,020 base64
  characters. File-based REST avoided the problem; an MCP URL/file input would remove this
  client-size risk.
- **MCP `create_image_pro` — style controls:** style-copy and combined reference+style outputs did
  not visibly adopt the supplied gray-green palette.

### Low priority

- **MCP `get_image` / `get_tiles_pro` — status reporting:** jobs sometimes remained `processing` at
  95-100%. REST building remained `processing` for about 30 seconds after `last_response` contained
  the finished result.
- **MCP `create_building_kit` — naming:** the name and `layout` values do not clearly say that this
  generates architectural floor, wall, doorway, pillar, and stair tiles for constructing buildings.
- **MCP `create_building_kit` — intermittent failure:** the first `layout="grid"` job failed with
  only `Generation failed`; an exact reproduction later completed 58 valid tiles. The original
  failure's refund status cannot be reconstructed.
- **MCP `create_image_pixflux` — documented size limit:** 16×16 is rejected because the live minimum
  area is 1,024 pixels, despite the declared 16px per-axis minimum.

## Execution Completeness

All functional assertions in the test matrix are complete. The completion pass supplied the third PixFlux measurement, tested
reference-mode `edit_image` with `description` omitted, compared MCP and REST animation using literal
open/closed chest anchors, isolated the Pixen failure refund, and reproduced
`create_building_kit(layout="grid")` successfully. The reproduction cost 20 generations; the
balance changed by exactly that amount at completion and remained unchanged after 60 seconds. The original failed
job was not bracketed by snapshots, so its refund status cannot be reconstructed. Some early outputs
lack archived copies because their full job IDs were lost after live inspection; no functional
assertion remains open.

Timing is submission-to-first-observed terminal `completed` status. Because polling was intentionally
spaced, async values are upper bounds within one polling interval; generation queue time dominates.
“Steps” counts distinct agent tool calls or script executions from submission through a verified saved
result. REST bearer auth was supplied on every script invocation; MCP authenticated once when the
connection was established.

## Performance & Stability Summary

| Tool | MCP steps-to-completion | REST steps-to-completion | MCP time (median if repeated) | REST time (median if repeated) | Failure/retry incidents | Malformed call rejected client-side by MCP? | MCP base64 truncation risk observed? |
|---|---:|---:|---:|---:|---|---|---|
| `update_character_tags` | 1 | 1 | 0.899 s (n=3) | 0.717 s (n=3) | None | No; 21 tags returned a tool error envelope | N/A |
| `update_object_tags` | 1 | 1 | 0.817 s (n=3) | 0.737 s (n=3) | None | No; 21 tags returned a tool error envelope | N/A |
| `create_image_pixflux` | 4 | 2 | ~30 s (n=3) | 20.691 s (n=3) | First variance orchestration lost its job handle; replacement completed without retrying that job | Yes for declared width bounds | No; a 400×400, 37,916-character input arrived intact |
| `create_image_pixen` | 3 | 2 | ~49 s (n=3) | 40.123 s (n=3) | 17×20 MCP job failed with HTTP 500; REST returned HTTP 422; isolated repeat caused no net charge | No | N/A |
| `create_image_pro` | 5 | 5 | ~91 s | ~92 s | No retry; style-copy fidelity misses recorded | No; the five-reference JSON is validated inside the tool | N/A |
| `edit_image` | 5 | 4 | ~91 s | ~62 s | Large inline PNG truncated; description-free reference mode passed; no billing discrepancy after reconciliation | Yes for 513px dimensions; no for frame-count rule | **Yes** |
| `inpaint_image` | 4 | 4 | ~61 s | ~62 s | Both surfaces completed but violated mask semantics; out-of-bounds MCP rectangle was charged and silently accepted | No | No; compact 512×512 image plus mask arrived intact |
| `animate_image` | 4 | 5 | ~62 s (literal tween) | ~93 s (literal tween) | No generation failure; MCP again lagged at high progress before completion | No; odd/pixel-budget rules return tool error envelopes | No; 256×256 boundary input arrived intact |
| `create_path_tiles` | 6 | 4 | ~106 s | ~62 s | No retry; initial MCP ETA was ~459 s | No | N/A |
| `create_building_kit` | 9 | 8 | ~211 s | ~151 s | First explicit `grid` job failed generically; exact reproduction completed 58 tiles and cost 20 generations; REST result was ready about 30 s before top-level status became `completed` | Yes for `wall_tiles=4`; no for projection-specific size | N/A |
| `get_image` | 1 per poll | 1 per poll | 0.8-1.1 s per read | 0.7-2.7 s per read | MCP showed 95%/100% status lag; REST building showed `message_done` while top-level remained `processing` | No | N/A |

The cheap PixFlux and Pixen REST routes return their image synchronously, so the broad premise that
REST always requires manual job polling does not hold for those two endpoints. For async routes,
both surfaces required polling. REST building status lagged a ready `last_response` for roughly 30
seconds; MCP getters also lagged at 95% and once reported `processing 100%` before completion.

## `update_character_tags`

- Smoke/live — **PASS**: `qa-smoke` replaced the fixture’s tags and was echoed.
- Coverage: empty list — **PASS**: the clear response was followed by a tag-filtered list returning
  zero characters; the equivalence tags were then restored.
- Coverage: 21 tags — **PASS**: clear max-20 validation error.
- Coverage: trim and case-insensitive dedupe — **PASS**: `" QA-Tag "`, `"qa-tag"`, and `"Mixed"`
  normalized to `QA-Tag, Mixed`.
- Error: nonexistent UUID — **PASS**: clear `Character not found` error.
- REST equivalence — **Equivalent**: all three repeated MCP/REST pairs returned the same tag set.
  REST was slightly faster in this sample, but both were one synchronous request.

## `update_object_tags`

- Smoke/live — **PASS**: `qa-smoke` replaced the fixture’s tags and was echoed.
- Coverage: empty list — **PASS**: the clear response was followed by a tag-filtered list returning
  zero objects; the equivalence tags were then restored.
- Coverage: 21 tags — **PASS**: clear max-20 validation error.
- Coverage: trim and case-insensitive dedupe — **PASS**: normalized to `QA-Tag, Mixed`.
- Error: nonexistent UUID — **PASS**: clear `Object not found` error.
- REST equivalence — **Equivalent**: all three repeated pairs returned identical tag sets.
- Cost finding: the prerequisite `create_1_direction_object(size=32)` fixture cost 20 generations
  and returned a review pack, not the plan’s former ~1-generation single candidate. This was a
  test-plan documentation mismatch and the plan was corrected.

## `create_image_pixflux`

- Smoke — **PASS**: 32×32 transparent PNG.
- Live text-to-image — **PASS**: 64×64 transparent dragon PNG.
- Live img2img — **PASS**: `init_image_strength=150` was accepted and completed.
- Coverage: forced palette — **PASS**.
- Coverage: isometric — **PASS**.
- Coverage: north and west direction spot checks — **PASS**.
- Coverage: 16×16 original-plan minimum — **FAIL**: live service rejected 256 total pixels with
  `minimum is 32x32 = 1024px`. This was a plan documentation mismatch; the plan now treats 32×32 as
  the smallest legal square and 16×16 as a rejection probe.
- Coverage: 400×400 maximum — **PASS**.
- Error: width 15 and 401 — **PASS**: declared bounds were rejected client-side.
- REST equivalence — **MCP worse operationally**: output dimensions/background behavior matched,
  but REST returned the PNG synchronously in one request while MCP needed a job plus getter. One
  MCP handle was orphaned by the local orchestration timeout; it was not resubmitted or double-charged.
- Large-inline check — **PASS** at 400×400/37,916 base64 characters; no corruption observed.
- Performance repeat — **PASS**: the replacement third MCP measurement completed at 64×64, closing
  the planned three-pair variance sample.

## `create_image_pixen`

- Smoke — **PASS**: 32×32 ornate key.
- Live — **PASS**: 128×128 opaque mossy wall.
- Coverage: transparent sprite — **PASS**.
- Coverage: 16×16 minimum — **PASS**.
- Coverage: 512×512 maximum — **PASS**.
- Error: width 17 — **FAIL**: MCP accepted the request, then the job failed with an HTTP 500 server
  error (`Height and width must be equal for small generations`). REST rejected the same payload
  with an HTTP 422 validation response because width must be a multiple of four. The isolated repeat
  caused no net charge: the balance was unchanged before submission, at failure, and after 60 seconds. This
  is a **PixelLab-side MCP validation bug**; refund behavior passed.
- REST equivalence — **MCP worse** for malformed dimensions; the three valid repeated pairs were
  functionally equivalent, but REST returned synchronously and rejected invalid dimensions earlier.

## `create_image_pro`

- Smoke — **PASS**: 16×16 produced the documented 64 candidates at 20 generations.
- Live 128×128 knight — **PASS**: four candidates.
- Live two labelled references — **PASS**: four candidates; the output visibly retained the knight
  subject and adopted material cues from the second reference.
- Coverage: one style image and partial `color_palette`/`outline` copy — **FAIL**: the request was
  accepted as the exact partial-copy shape, but candidates did not clearly adopt the supplied
  gray-green palette.
- Coverage: reference plus style in one call — **FAIL**: subject identity was retained, but the
  output stayed gold/brown rather than visibly adopting the supplied palette. This is a
  **PixelLab-side output-fidelity issue**, not a field-mapping mismatch.
- Coverage: style image is one string, not an array — **PASS**: live schema and call both confirm it.
- Coverage: 512×512 square — **PASS**: one candidate at 40 generations.
- Coverage/error: 688×512 off-ladder — **PASS**: rejected with live max 600×448 for that aspect.
- Error: five references — **PASS**: rejected at max four.
- REST equivalence — **Equivalent**: identical two-reference 128×128 request produced four
  candidates on both surfaces at 20 generations, with matching dimensions and field mapping
  (`usage` ↔ `usage_description`).

## `edit_image`

- Smoke — **PASS**: one 32×32 text edit completed.
- Live reference mode — **PASS**: response explicitly switched to `mode: reference` and returned
  two distinct 64×64 outputs.
- Coverage: reference mode with `description` omitted — **PASS**: the 32×32 output visibly adopted
  the supplied stone texture, confirming that the description is genuinely optional.
- Live multi-frame consistency path — **PASS**: two frames received the same reference edit.
- Coverage: 16 frames at ≤64px — **PASS**: all 16 returned.
- Coverage: one frame above 128px — **PASS**: compact 512×512 input returned one 512×512 output.
- Error: 17 frames at 32px — **PASS**: rejected at the 16-frame cap.
- Error: 513×513 — **PASS**: dimensions rejected client-side.
- REST equivalence — **MCP worse for transport, otherwise equivalent**: the matched two-frame text
  edit completed on both surfaces at 20 generations with two 32×32 outputs. An unquantized valid PNG
  was truncated to 40,020 base64 characters in the MCP client path; the file-based REST script has no
  analogous inline argument risk. A compact PNG at the same dimensions succeeded.
- Billing — **PASS**: six original MCP calls cost 140 generations (five at 20, one 512px call at 40)
  and the matched REST Pro call cost 20. The later completion pass added one 20-generation MCP edit
  and five one-generation calls. Together, 160 from the original edit matrix plus 25 from completion
  exactly explains the observed 185-generation balance change. The sparse snapshots cannot establish
  when individual charges became visible, so no billing-timing claim is made.

## `inpaint_image`

- Smoke rectangle — **FAIL**: the call completed, but the requested 8×8 region was unchanged while
  pixels outside it changed.
- Live custom mask — **FAIL**: both 512×512 outputs were byte-identical to the input, including the
  white mask region.
- Live `crop_to_mask=true` vs `false` — **FAIL**: outputs were byte-identical; no boundary difference.
- Coverage: full-image mask — **PASS**: output changed across the requested full area.
- Coverage/error: rectangle beyond image bounds — **FAIL**: `(28,28,8,8)` on 32×32 was accepted,
  charged, and completed instead of returning the planned clear validation error.
- Error: custom mask plus rectangle — **PASS**: rejected with “pass EITHER ... OR ... not both.”
- REST equivalence — **Equivalent but both buggy**: REST reproduced the same inverted/ineffective mask
  behavior. This is a **PixelLab-side shared implementation bug**; parity remains equal, but neither
  surface satisfies the documented white=regenerate/black=preserve contract.
- Large-inline check — **PASS**: compact 512×512 image plus custom mask arrived intact.

## `animate_image`

- Smoke — **PASS**: `frame_count=4` returned five images.
- Live start→end tween — **PASS**: six generated frames plus echoed frame 0; the final generated frame
  was materially closer to the supplied end frame than frame 0.
- Coverage: 256×256×8 exact pixel budget — **PASS**: nine images at eight generations.
- Coverage: 256×256×10 over budget — **PASS**: rejected.
- Coverage: odd frame count 5 — **PASS**: rejected.
- Error: 257×257 first frame — **PASS**: rejected.
- Error: mismatched last-frame dimensions — **PASS**: rejected.
- REST equivalence — **Equivalent**: both returned five images for the matched four-frame request;
  frame 0 was visibly pixel-identical to the input (only arbitrary RGB values under fully transparent
  pixels differed).
- REST last-frame equivalence — **Equivalent**: literal open/closed chest anchors produced seven
  64×64 images on both surfaces. Frame 0 matched the open anchor and frame 6 matched the closed anchor
  exactly; the inspected middle frames were visually equivalent.
- Large-inline check — **PASS**: exact 256×256 boundary input arrived intact.

## `create_path_tiles`

- Smoke — **PASS**: 18 square-topdown variations and edge rules returned.
- Live — **PASS**: 18 isometric 64px variations, including straight/corner/T/cross/dead-end/plain
  configurations and four-bit edge masks.
- Coverage: `outline` vs `segmentation` — **PASS**: both modes completed as separate sets.
- Error: square-topdown tile size 48 — **PASS**: clear exact-32 validation error.
- REST equivalence — **Equivalent**: both returned 18 stored tiles with the same edge-rule shape.
  MCP is structurally simpler because its getter returns final rules directly; REST required submit,
  background polling, then `GET /tiles-pro/{tile_id}`.

## `create_building_kit`

- Smoke — **PASS**: 58-piece isometric kit with floor, walls, doorways, pillar, stairs, and composed
  placement rules.
- Live — **PASS**: 56-piece 64px oblique kit with three-tile walls and the requested roof material.
- Coverage: explicit `layout=grid` — **PASS with an intermittent incident**: the first background job
  ended with only `Generation failed`; an exact reproduction completed 58 valid pieces. The
  reproduction cost 20 generations immediately and the balance was unchanged after 60 seconds.
- Coverage: explicit `layout=materials` — **PASS**: 56-piece set completed. The successful `grid`
  reproduction also confirmed the two layout paths produce different piece sets.
- Error: `wall_tiles=4` — **PASS**: client-side max-three rejection.
- Error: 16px isometric — **PASS**: clear 32-96 projection-specific rejection.
- REST equivalence — **Equivalent**: matching smoke request returned the same building roles and
  composed rule shape. REST exposed a ~30-second terminal-status lag after `message_done`; MCP
  separately exposed `processing 100%` before completion.

## `get_image`

- Coverage: processing→completed transition — **PASS**: observed repeatedly across raw-image jobs.
- Coverage: completed result — **PASS**: inline images were returned by the MCP result and no-auth
  download URLs saved valid PNGs.
- Error: fabricated job UUID — **PASS**: clear not-found error, no hang or empty success.
- REST comparison — **Equivalent getter capability**: both surfaces expose job progress and final
  result data. Both can lag; MCP showed 95%/100% progress lag, while REST building top-level status
  lagged a ready `last_response` by roughly 30 seconds.

## Verdict

MCP’s typed-call-plus-getter pattern reduces script-authoring and authentication overhead for the
async edit/inpaint/animation/tile/Pro family: requests are shorter, bearer headers are not rebuilt,
and final tile rules arrive through purpose-specific getters. It did **not** consistently reduce the
measured number of calls or wall-clock time: queue time dominated, MCP often required as many or more
polls, and synchronous REST PixFlux/Pixen were materially simpler. Incident counts were not lower on
MCP in this run—the Pixen validation gap caused a refunded HTTP 500 and large inline edit base64 was
truncated—while REST’s main surface-specific incident was terminal status lag. Pro edit billing
reconciled to the documented 20/40-generation size tiers. Practical conclusion: MCP lowers agent-side
authoring complexity for async jobs, but that advantage does not yet translate into uniformly fewer
operational steps or failures across this tool family.
