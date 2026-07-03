# PixelLab 1-Bit Tileset Prompt Testing

Last reviewed: 2026-07-03.

These notes summarize local simulator and live MCP checks for strict black-and-white top-down and sidescroller tilesets. They are maintainer notes for designing future tests; the agent-facing routing contract remains in `skills/pixellab-pip/references/tilesets.md`.

## Goal

Use `dev-tools/pixellab_mcp_tileset_sim.py` to cheaply prototype MCP-shaped tileset requests before spending PixelLab generations, especially for 1-bit tilesets with solid black masses and white boundary pixels.

The primary success criterion is PixelLab-generated shape. Palette snapping is acceptable only as a post-process on an otherwise good PixelLab output. The simulator should therefore be used to learn how descriptions and structured inputs target silhouette, tile topology, boundary placement, top-surface placement, and compact export layout. It should not be used to decide whether live PixelLab will return exact `#000000` and `#FFFFFF`.

The simulator is useful for request shape, compact layout size, DualGrid packing, and rough layer targeting. It is not yet a PixelLab model predictor for final shape quality.

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
| REST sidescroller `transition_reference_image` only | Weak candidate. Top-layer information exists, but it is dark blue/teal; low thresholds reveal too much body texture, while high thresholds lose the rim. |
| REST sidescroller `color_image` + reference | Not recoverable. The output is black/transparent with no white rim to recover. |
| Prompt-only MCP sidescroller `transition_size: 0.5` | Best current sidescroller clamp candidate. It has brighter top/end-cap accents than REST sidescroller reference runs, and high thresholds preserve a cleaner ledge line. |

Current selected clamp previews live under `pixellab-pip-generations/1bit-palette-clamp-study-20260703/selected-candidates/`.

A follow-up REST sidescroller prompt-only test, `side-prompt-d-high-contrast-no-controls`, tried to ask directly for high-contrast bright white top/end-cap pixels, darker interiors, and no controls. It did not improve the situation: the raw output contained no bright or whiteish pixels, shifted accents into purple midtones, and produced more interior texture. Threshold clamps only recovered white at low/mid thresholds where body noise also becomes white. This did not beat the earlier MCP `transition_size: 0.5` candidate.

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
