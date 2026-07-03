# PixelLab 1-Bit Tileset Prompt Testing

Last reviewed: 2026-07-03.

These notes summarize local simulator and live MCP checks for strict black-and-white top-down and sidescroller tilesets. They are maintainer notes for designing future tests; the agent-facing routing contract remains in `skills/pixellab-pip/references/tilesets.md`.

## Goal

Use `dev-tools/pixellab_mcp_tileset_sim.py` to cheaply prototype MCP-shaped tileset requests before spending PixelLab generations, especially for 1-bit tilesets with solid black masses and white boundary pixels.

The primary success criterion is PixelLab-generated shape. Palette snapping is acceptable only as a post-process on an otherwise good PixelLab output. The simulator should therefore be used to learn how descriptions and structured inputs target silhouette, tile topology, boundary placement, top-surface placement, and compact export layout. It should not be used to decide whether live PixelLab will return exact `#000000` and `#FFFFFF`.

The simulator is useful for request shape, compact layout size, DualGrid packing, and rough layer targeting. It is not yet a PixelLab model predictor for final shape quality.

## Current State

Top-down has a workable recipe. `topdown-cave-rim-ref-a` shows that a black lower terrain, black upper terrain, `transition_size: 0.5`, and a compact `transition_reference_image` can put lighter pixels on the correct cave/wall boundary. The raw output is not exact black/white, but threshold clamping preserves the intended rim. `topdown-b-cave-rim-production-ref` is a stronger production branch with true near-white raw pixels and a more readable ledge, but the clamp becomes thicker and more cap-like than the older sparse rim.

Sidescroller does not yet have the exact sparse-rim ideal. The live tests suggest this behavior:

- `lower_description` controls the dark platform body.
- `transition_size: 0.0` can produce a clean dark silhouette, but it suppresses bright white rim requests.
- `transition_description` is where bright top/edge pixels appear, but PixelLab tends to turn them into a cap/surface material.
- `base_tile_id` chaining from a clean dark body preserved darkness but did not add a bright rim.

Current sidescroller options are therefore two imperfect branches: `side-c-broken-rim-05` for sparse rim placement, or `side-k-featureless-silhouette-capstones-05` for a more polished bright-cap platform after local clamp. `side-n-serrated-cap-no-blue-05` showed that adding stricter `no blue/no purple` drift wording can erase the usable white cap entirely, so do not use negative color-drift wording as the next automatic fix.

The unresolved sidescroller gap is full connected-shape outlining. Top-down tests can place white pixels on the wall/floor contour because `transition_description` maps to a terrain boundary. Sidescroller tests have not shown an equivalent control: the same kind of white-edge request maps to top caps, ledge highlights, or localized surface material instead of a consistent outline around the whole platform tileset shape.

## Corpus Findings

A replay audit scanned the local generation corpus for MCP-shaped tileset inputs and live-looking PNGs.

- Replayed compact candidates with live PNGs: `137`.
- Successful simulator replays: `126`.
- Matching live/sim output dimensions among successful replays: `126`.
- Deliberate simulator refusals: `11`, all replayed expanded top-down `transition_size: 1.0` cases.
- Strict black-and-white live outputs among successful replays: `22`.
- Strict black-and-white simulator outputs among successful replays: `49`.

The main conclusion is that the simulator is accurate enough for compact layout and request validation, but not yet accurate enough to choose final prompts by itself. Live PixelLab often adds near-black, dark purple, gray, cream, or off-white palette drift even when prompts say `1-bit`, `pure black`, `pure white`, and `no gray`; that palette drift is repairable. The harder unsolved problem is predicting whether PixelLab will place the white shape information in the right place: exposed rims, top ledges, wall boundaries, corners, and tile seams. Separate corpus review also found observed top-down Pro expansion at `transition_size: 0.5`, so compact prompt tests should prefer standard mode.

## Live 1-Bit MCP Tests

Four live MCP tests were run from simulator-matched JSON:

| Test | Tool | Result |
|---|---|---|
| `side-cave-rim` | `create_sidescroller_tileset` | Compact `64x64`; good chunky cave-platform shape; `7` visible colors; not strict 1-bit. |
| `side-clean-blocks` | `create_sidescroller_tileset` | Compact `64x64`; readable platform blocks; `8` visible colors; strongest purple/gray drift. |
| `top-wall-outline` | `create_topdown_tileset` | Compact `64x64`; best wall-boundary structure; `17` visible colors; not strict 1-bit. |
| `top-arduboy-wall` | `create_topdown_tileset` | Compact `64x64`; readable room-wall structure; `23` visible colors; not strict 1-bit. |

The best structural prompt was the plain top-down wall outline request:

```json
{
  "lower_description": "1-bit pure black floor void, flat solid black fill, no gray",
  "upper_description": "1-bit pure black wall mass, flat solid black fill, no gray",
  "transition_description": "pure white one-pixel contour outline around wall boundary, crisp orthogonal 1-bit edge pixels, no gray",
  "transition_size": 0.5,
  "detail": "low detail",
  "shading": "flat shading",
  "outline": "lineless",
  "mode": "standard",
  "view": "high top-down",
  "tile_size": {
    "width": 16,
    "height": 16
  },
  "text_guidance_scale": 12
}
```

## Prompt Guidance

## Live Prompt Ladder Findings

A small simulator-to-live ladder tested one top-down candidate and one sidescroller candidate after local deterministic and DeepSeek simulator review.

Top-down request:

- `lower_description`: black floor void.
- `upper_description`: black wall mass.
- `transition_description`: one-pixel pure white rim pixels on the wall/floor boundary.
- `transition_size: 0.5`.

Live result: compact `64x64`; placement mostly passed. PixelLab placed the brighter pixels on the wall/floor contour, matching the intended boundary/rim class. Palette failed strict 1-bit: highlights drifted to dark yellow/brown rather than white.

Sidescroller request:

- `lower_description`: solid black horizontally tileable platform center body with no seam highlights.
- `transition_description`: pure white broken rim pixels only on exposed top surface and outside end-cap edges.
- `transition_size: 0.25`.

Live result: compact `64x64`; placement partially passed. PixelLab placed brighter pixels mostly along top/ledge runs and kept much of the body dark. Palette failed strict 1-bit: highlights drifted to blue/cyan/purple rather than white, and the rim was subtle.

The same sidescroller wording was then tested with `transition_size: 0.5`. The larger transition produced a stronger top/rim accent mask than `0.25` and better emphasized exposed top/vertical edge runs, but it also increased opaque coverage, color count, and blue/purple texture drift. This suggests `transition_size` is a real coverage control for sidescroller top/rim placement, but not a palette-control or clean-1-bit control.

Observed conclusion: prompt-only MCP wording is useful for steering the semantic placement of light accents into `transition_description`, but it is not enough to enforce exact black/white palette. For production 1-bit work, continue to prioritize shape and placement in MCP tests, then use REST palette/reference controls or an explicitly labeled palette-clamped derivative after the PixelLab-generated shape is approved.

## REST Control Findings

Three REST top-down checks tested the same black floor, black wall, and white contour prompt with locally authored control images.

| Test | Controls | Result |
|---|---|---|
| `topdown-color-transition-ref-a` | Mostly black `64x64` `color_image` with small white swatches, plus `16x16` `transition_reference_image` | Completed, but collapsed to pure black. Strict 1-bit passed only because all white contour information disappeared. |
| `topdown-color-transition-ref-b-balanced` | Balanced black/white checker `64x64` `color_image`, plus stronger `16x16` `transition_reference_image` | Completed, but still collapsed to pure black. |
| `topdown-transition-ref-c-no-color-image` | Stronger `16x16` `transition_reference_image`, no `color_image` | Completed with visible near-white contour pixels on the wall/floor boundary. Palette was not strict black/white, but placement was useful. |

Observed conclusion: for black-on-black 1-bit top-down terrain, `color_image` can suppress the desired white transition instead of merely constraining the palette. `transition_reference_image` is currently the better first REST control for edge placement. Add `color_image` only as a separate follow-up test after confirming it does not erase the transition, or palette-clamp a shape-approved PixelLab output as labeled local processing.

Three REST sidescroller checks then tested a black platform body with white top/end-cap pixels.

| Test | Controls | Result |
|---|---|---|
| `side-transition-ref-a-no-color-image` | `16x16` top/surface `transition_reference_image`, `transition_size: 0.25`, no `color_image` | Completed with good transparent platform topology, but PixelLab remapped the intended white rim into dark blue/purple; no bright or whiteish pixels. |
| `side-transition-ref-b-strong-top-no-color-image` | Stronger white top reference, `transition_size: 0.5`, no `color_image` | Completed with more top/surface coverage, but still no bright or whiteish pixels; white was remapped into dark teal/blue. |
| `side-color-transition-ref-c-balanced` | Stronger top reference plus balanced black/white `64x64` `color_image` | Completed as strict black/transparent, but the white top layer disappeared. |

Observed conclusion: sidescroller REST controls currently preserve platform topology better than prompt-only testing, but they still do not force a white top rim. `transition_reference_image` can influence where the top layer belongs, while `color_image` again risks erasing the requested white transition. For sidescroller 1-bit work, keep using reference-free or reference-only live tests for shape, then palette-clamp only after the edge/top placement is acceptable.

## Palette Clamp Findings

A local black/white threshold study tested whether the raw PixelLab outputs contain enough luminance separation to become usable strict 1-bit assets after palette snapping. These outputs are labeled local derivatives, not raw PixelLab generations.

| Source | Clamp result |
|---|---|
| REST top-down `transition_reference_image` only | Strong candidate. Near-white contours survive strict clamping across high thresholds, so the top-down pipeline is close: shape with `transition_reference_image`, then clamp after approval. |
| REST top-down cave-rim `transition_reference_image` only | Strongest current top-down clamp target. Raw output has no true white, but the lighter contour is placed on the wall/floor boundary and clamps cleanly at threshold 96 with dark interiors preserved. |
| REST sidescroller `transition_reference_image` only | Weak candidate. Top-layer information exists, but it is dark blue/teal; low thresholds reveal too much body texture, while high thresholds lose the rim. |
| REST sidescroller `lower_reference_image` + `transition_reference_image`, no `color_image` | Not a candidate. `side-i-ref-lower-transition-no-color-05` over-anchored the structure into flat gray horizontal slabs; clampable light pixels became broad mid-band strips rather than sparse top/end ledge chips. |
| REST sidescroller `color_image` + reference | Not recoverable. The output is black/transparent with no white rim to recover. |
| Prompt-only MCP sidescroller `transition_size: 0.5` | Best current sidescroller clamp candidate. It has brighter top/end-cap accents than REST sidescroller reference runs, and high thresholds preserve a cleaner ledge line. |

Current selected clamp previews live under `pixellab-pip-generations/1bit-palette-clamp-study-20260703/selected-candidates/`.

A follow-up REST sidescroller prompt-only test, `side-prompt-d-high-contrast-no-controls`, tried to ask directly for high-contrast bright white top/end-cap pixels, darker interiors, and no controls. It did not improve the situation: the raw output contained no bright or whiteish pixels, shifted accents into purple midtones, and produced more interior texture. Threshold clamps only recovered white at low/mid thresholds where body noise also becomes white. This did not beat the earlier MCP `transition_size: 0.5` candidate.

A follow-up MCP sidescroller prompt-only test, `side-d-smooth-cap-05`, tried to remove texture language and ask for a smooth black silhouette with a crisp white cap. It also did not improve on `side-c-broken-rim-05`: the raw output became chunkier/noisier, and high-threshold clamps lost the clean broken ledge line. Keep `side-c-broken-rim-05` as the current sidescroller clamp baseline.

A follow-up MCP sidescroller prompt-only test, `side-e-white-crust-surface-05`, tried a structurally different branch: treat the white pixels as the sidescroller top/surface material rather than as an outline. This worked as a placement control, producing bright top material that clamps cleanly at threshold 96, but it overfilled into a continuous white cap/snow-platform read instead of sparse rim pixels. `side-f-white-chips-surface-025` then kept the same surface-material framing with `transition_size: 0.25` and separated-chip wording. That was a regression: all bright recoverable pixels disappeared. Keep `side-c-broken-rim-05` as the sparse-rim baseline; keep `side-e-white-crust-surface-05` only as a bright solid-cap branch.

`side-g-broken-ledge-highlight-05` attempted the next sparse-rim branch with `transition_size: 0.5`, no cap/crust/snow/surface-material wording, and a direct broken ledge highlight request. PixelLab failed the job with `unknown error` before producing an image, and balance did not change. `side-h-short-ledge-highlight-05` retried the same idea with shorter transition wording and also failed without a charge. Do not treat these as visual evidence, but stop this exact direct broken-ledge-highlight branch for now; use the known-working `side-c-broken-rim-05` wording family or REST/reference controls for the next sidescroller attempt.

`side-i-ref-lower-transition-no-color-05` tested the REST/reference route after the prompt-only ledge-highlight failures. It sent a black slab `lower_reference_image`, a sparse white top/end-chip `transition_reference_image`, and no `color_image`. The job completed, but the result showed that sidescroller reference images can over-anchor the platform into literal gray slab bands. The brightest pixels reached only luminance 128, landed mostly in the middle of the 16px tiles, and clamped into long horizontal strips rather than a professional 1-bit ledge. This makes lower+transition references a poor first fix for the sidescroller rim problem.

`side-j-chipped-capstones-05` returned to MCP prompt-only generation and kept the surface-material branch from `side-e`, but asked for sparse chipped capstones instead of a white crust. This restored true bright pixels and clamps cleanly, but PixelLab still interpreted the wording as a mostly continuous top cap with dangling teeth, and it reintroduced dark purple platform linework. Treat `capstone`/`chipped capstone` as a way to force bright top material, not as a sparse-rim control.

`side-k-featureless-silhouette-capstones-05` kept the chipped-top idea but strengthened the lower prompt with `featureless`, `pure black ink silhouette`, `no seams`, and `no internal linework`, plus `text_guidance_scale: 12`. PixelLab still drew purple block/platform texture in the body. This suggests the sidescroller body generator has a strong platform-material prior; stronger negative texture wording and higher text guidance do not reliably make a flat black interior.

`side-l-body-contour-transition0` moved the white contour request into `lower_description` and set `transition_size: 0.0`. This produced the cleanest dark platform silhouette so far, but PixelLab suppressed the requested white contour entirely: max luminance was only 26 and every clamp stayed black. This suggests sidescroller white edge/top pixels need the transition/top layer; `lower_description` can shape a dark body, but it is not reliable for bright rim placement when the transition layer is off. The useful follow-up is chaining from `side-l`'s `base_tile_id` and reintroducing a controlled transition.

`side-m-chained-silhouette-rim-05` used `side-l`'s clean-body `base_tile_id` and reintroduced a broken white rim through `transition_description` at `transition_size: 0.5`. Chaining preserved a dark body but did not combine the desired behaviors: max luminance was only 71, and no white rim survived normal clamp thresholds. For this 1-bit target, base-tile chaining is useful for continuity but is not currently a reliable way to add bright top/rim pixels to a clean body.

`side-n-serrated-cap-no-blue-05` tried to refine `side-k` by keeping the bright cap idea while explicitly banning blue shadows, purple blocks, bricks, planks, and internal linework. It regressed: max luminance was only 49, no near-white pixels survived, and threshold clamps stayed black. This suggests strong negative color/material wording can suppress the very bright transition material we need. Keep `side-k` as the cap branch; avoid spending another run on negative color-drift wording unless a new control variable is added.

A follow-up REST top-down reference-only test, `topdown-cave-rim-ref-a`, used a 16x16 broken-rim transition reference and cave-wall wording. It produced the best top-down 1-bit shape candidate so far: raw PixelLab colors remained dark gray/blue with no true white, but edge placement was correct and local clamps from threshold 32 through 96 preserved a readable white rim without flooding the interior. This reinforces the shape-first workflow: use PixelLab/reference controls for boundary placement, then palette-clamp only after the generated shape is accepted.

`topdown-b-cave-rim-production-ref` reused the same REST reference-only recipe with a denser broken-rim guide and production-facing cave wording. It produced true near-white pixels in the raw output and a high-contrast readable wall boundary. Compared with `topdown-cave-rim-ref-a`, it is stronger and more immediately visible, but the clamped result is thicker and more cap-like. Treat these as two valid top-down branches: sparse cave contour versus bolder ledge/cap.

For top-down wall tests, prefer:

- `mode: "standard"`.
- `transition_size: 0.5`.
- Black lower and upper descriptions when the desired result is a black wall/floor mass.
- A transition description that names white boundary pixels directly.
- `detail: "low detail"`, `shading: "flat shading"`, and `outline: "lineless"`.

For sidescroller ground tests, prefer:

- Solid black body in `lower_description`.
- White rim/top pixels in `transition_description`, not only in `outline`.
- `transition_size: 0.25` as the first test when subtle top accents are acceptable; try `0.5` when rim coverage is too sparse, accepting higher risk of color/texture drift.
- Avoid relying on `outline: "single color outline"` alone; it can encourage stylized gray/purple outlines.
- Do not spend repeated prompt-only attempts on a full connected-shape white outline unless a new control route is being tested; current evidence says the sidescroller route does not expose that contour concept cleanly.

## Shape-First Rubric

For 1-bit tests, grade outputs in this order:

1. Shape topology: the live PixelLab output must have usable terrain masses, not just correct colors.
2. Tileability: repeatable center/middle tiles should not introduce visible seam marks unless those marks are intended texture.
3. Boundary placement: white pixels should appear on exposed wall/platform/ledge boundaries rather than random interior noise.
4. Transition placement: top-down transition pixels should sit on lower/upper boundaries; sidescroller transition pixels should sit on the top surface or exposed rim.
5. Readability at native scale: the tile should read at `16x16` without scaled-preview smoothing.
6. Palette: exact two-color output is desirable but secondary, because palette clamping can fix color drift while preserving PixelLab's generated shape.

Future simulator improvements should target shape prediction before palette prediction. The most useful next step is a shape audit harness that extracts alpha/edge masks and white-pixel masks from live PixelLab outputs, compares them to simulator masks, and scores descriptions by shape behavior rather than exact RGB match.

## Simulator Limits

The simulator can cheaply check:

- Required MCP fields and allowed MCP fields.
- Tile size and compact export dimensions.
- Whether text targets the right layer: sidescroller body vs top layer, or top-down lower/upper/transition.
- Whether a prompt is likely to produce a compact `15-tileset`, `wang`, or `godot-3x3` output.

The simulator cannot check:

- Strict live palette adherence.
- PixelLab texture taste or exact model composition.
- Whether prompt wording will suppress gray, purple, cream, or off-white drift.
- REST-only palette/reference controls such as `color_image` or terrain reference images.
- Expanded top-down sheets.

For strict 1-bit deliverables, verify the raw PixelLab output separately and document any palette-clamped derivative as local processing.
