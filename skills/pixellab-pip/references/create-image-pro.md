# Create Image Pro

Read this for explicit Create Image Pro wording, MCP `create_image_pro`/REST `generate-image-v2`, exact grid or sheet requests, small cell-size requests that are not already covered by `icon.md`, and exact hex palettes or color caps on any route.

Create Image Pro / MCP `create_image_pro` (+ `get_image`) / REST `generate-image-v2` is a general image-generation route. It can make attractive sprite sheets and texture sheets, but exact cell layout is prompt-guided rather than structurally guaranteed. A correct output canvas size is not proof that the image contains the requested cell grid. Style is prompt-guided too: there is no `detail`, `outline`, `shading`, `negative_description`, `color_image`, or `coverage_percentage` field; MCP accepts a preferred `style_image_url` or inline base64 plus `style_copy`, while REST has `style_image`+`style_options`. Route to `create_image_pixen`/`create-image-pixen`, `create_image_pixflux`/`create-image-pixflux`, or `create-image-bitforge` when another field must be enforced.

Prefer Pro when user instructions must be followed closely; it follows the user's description more closely than Pixen/v3/new, at higher cost and with a different character style.

MCP `create_image_pro` and REST `generate-image-v2` both remove the background by default (`no_background` defaults to `true`). Send `no_background: false` when the user wants an opaque, full-bleed image, scene, or sheet.

## Exact Palette Control

MCP uses `palette` (2–256 hex colors), optional `palette_name`, and `max_colors` (2–64 per image); REST uses `target_palette.colors`, optional `name`, `max_colors`, and beta `smart`. The palette colors constrain every result pixel; `max_colors` only caps the count. REST `smart` requires `colors`, is for single images, adds about 15–60 seconds, and is refused for animation; MCP documents no `smart` equivalent.

Routes with these fields:

- REST `target_palette`: `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `create-ui-asset`, `image-to-pixelart-pro`, the Pro Flash image/character/object creation and `image-to-pixelart-pro-flash` routes, `create-character-pro`, `create-character-with-8-directions` (`mode="pro"` only), `create-character-state`, `portrait-character-pro`, 1/8-direction object creation, object states, `create-tileset`/`tilesets` (`mode="pro"` only), `create-tiles-pro`, `generate-8-rotations-v2`, managed character animation (`pro`, `v3`, and `pixminimax` modes), object animation (`mode="pro"` only), `animate-with-text-v2`, `interpolation-v2`, `edit-animation-v2`, and `transfer-outfit-v2`.
- MCP `palette`/`palette_name`/`max_colors`: `create_image_pro`, the Pro Flash creation tools and `image_to_pixelart_pro_flash`, `create_character`, `create_character_state`, `create_portrait_character`, `create_1_direction_object`, `create_8_direction_object`, `create_object_state`, `animate_object`, `create_topdown_tileset`, `create_tiles_pro`, `create_path_tiles`, `create_building_kit`, `create_ui_asset`, and `transfer_outfit`. Apply the REST counterpart's mode limits. On `create_character`, REST documents palettes only for Pro; in v3 or standard mode, say enforcement is undocumented and check every visible output pixel against `colors` before claiming compliance.
- Every other route has no `palette`/`target_palette` field; do not send one. MCP `animate_character` lacks it, so use REST managed animation for a palette-constrained character animation.

For multiple directions or frames, give `colors`: a `max_colors` cap alone picks different colors per direction, and frame-based routes use one palette choice for all frames. Managed character animation and `animate-with-text-v2` put the source frame on the palette first; Pro Flash keeps a supplied `first_frame` or `source_image_id` unchanged; in outfit transfer the palette, not the reference, sets final colors. With REST `style_image`, set `style_options.color_palette: false` so the palette controls the colors; MCP `style_copy` already omits `color_palette` when a palette is given.

## Sub-32px Cell Requests

For exact grid/sheet/tile/icon/sprite requests with per-cell size below `32px`, treat Create Image Pro as prompt-sensitive rather than structurally guaranteed. Do not avoid it when the user asks for it; use prompt wording that makes the cell math, independence, and no-margin packing explicit, then verify the raw output honestly.

When the user explicitly asks for Create Image Pro with below-32px cells, do not push them to switch tools for that reason alone. Recommend a different route only when their real goal is a tile-specific asset (Wang/autotile terrain, isometric tiles, individual tile variants) or they need structural guarantees prompt-guided Create Image Pro cannot provide.

Use these alternatives only when they better match the user's actual intent:

- `create_tiles_pro` / REST `create-tiles-pro` for individual square, hex, octagon, or isometric tile variants, including small tile sizes.
- `create_topdown_tileset` / REST `create-tileset` for top-down Wang/autotile terrain transitions.
- `create_sidescroller_tileset` / REST `create-tileset-sidescroller` for platformer terrain.
- `create_isometric_tile` / REST `create-isometric-tile` for one isometric tile or block.

Do not call a Create Image Pro result a valid exact tile/icon/sprite grid based only on `image_size`. The output must pass visual cell-layout verification.

## Native-Size Multi-Output Batches

At small `image_size` values, `generate-image-v2` may return many same-prompt images. Native sizing enforces each returned file's dimensions; it does not assign a different requested concept to each output or guarantee semantic variety. Treat the results as candidates or variations unless the user explicitly requested a multi-asset set and delegated keeping all outputs; follow `reviewable-candidates.md` otherwise.

REST `generate-image-v2` documents the following output counts by maximum dimension:

- `16–32px`: 64; `33–35px`: 49; `36–41px`: 36; `42–50px`: 25.
- `51–64px`: 16; `65–84px`: 9; `85px`: 16; `86–170px`: 4; above `170px`: 1.

The MCP tool describes several candidates but does not publish these exact bands; inspect the returned results instead of assuming the REST counts. REST `generate-with-style-v2` uses the same count ladder through `170px` and returns one image from `171–512px`; its output size is still derived from the style images (see `style-reference.md`).

Variety requests (route-specific refinement of SKILL.md's "produce one candidate first"): when the user asks for a set, variety, or several `unique` small assets, run exactly one call. `generate-image-v2` at small sizes often returns dozens of distinct candidates from a single generation. Expand to further paid calls only when the first result's candidates are too few or too similar and the user approves the extra scope — or when the user explicitly approved a multi-call plan upfront per SKILL.md's batch-approval rule.

Prepare the description according to the requested set:

- One narrow composition such as `a health potion` yields variations of that composition, not variety—`unique` alone does not prevent near-identical motifs. For a varied set, name independent design axes such as silhouette, subject, material, palette, and detail, or say which dominant compositions must not repeat. Split into disjoint thematic calls only after one call's candidates prove too similar and the user approves.
- Do not assume a long catalog maps one-to-one onto returned images. Prefer smaller disjoint concept batches when coverage matters. If a named list is necessary, put `Unlabeled pictorial assets only; the names are semantic guidance and must never appear as visible text` before the list, then retain an applicable no-text clause after it. Long named catalogs can trigger captions or label-like marks even when `no text` appears only at the end.
- Make gameplay view explicit whenever it changes usability. For example, a top-down ground effect needs `top-down orthographic view looking straight down`, radial ground-plane debris, and negatives for horizon, side profile, ground baseline, or a vertical rising plume. Words such as `ground impact` or `plume rising` do not imply top-down view.

Before accepting or assembling a requested set, visually review every result for readable text or text-like marks, dominant-motif repetition, requested view, and recognizable subject differences. Exact pixel hashes prove only byte-level difference. Fail text-contaminated or wrong-view results rather than removing labels or rotating/repainting them locally; report when a batch contains variations instead of distinct concepts.

## Packed Sheet Prompt Recipe

Seams appear below roughly `26px` cells: one `256x256` request for a `16x16` grid of `16x16` cells showed visible seams around `25-26px` intervals despite the correct canvas size. Canvas math is not content layout — `image_size` sets only final dimensions, and `generate-image-v2` does not enforce cell boundaries. `grid`, `atlas`, `texture sheet`, and material lists tend to bleed continuous rows or multi-cell textures across cells; `contact sheet`/`separate thumbnails` improve independence but add gutters; asking PixelLab to draw guide lines bakes them into the asset.

Best observed prompt pattern for no-margin packed sheets:

- Frame the image as `256 packed independent block face texture files`, not a drawn grid or contact sheet.
- Say the image is `16 columns by 16 rows`, with each file occupying exactly one `16 by 16 pixel cell`.
- Say cells touch `edge-to-edge` with `zero pixels between cells`.
- Forbid `margins`, `gutters`, `padding`, `spacing`, `separator pixels`, `blank pixels`, `outlines`, `frames`, `guide lines`, and `drawn grid`.
- Say each cell is filled completely `edge-to-edge`, including edge and corner pixels.
- Forbid any detail continuing into neighboring cells: planks, grass edges, dirt or stone grain, ore veins, highlights, shadows, color bands, shapes, objects, horizontal/vertical strips, terrain rows, connected scenes, and wide textures.

## Verification

For exact grid outputs from Create Image Pro:

- Verify the original PixelLab output against both canvas size and visual cell layout.
- Check that visible boundaries, object centers, or tile extents actually follow the requested per-cell grid.
- For explicit cell sizes, derive the expected grid from the canvas and cell dimensions. Always inspect the first visible asset against its intended cell before accepting the result; fail if its type, scale, containment, or the observed grid differs from the request.
- Use local crop/split or boundary-measurement tools only for inspection or packaging, preserving original pixels. Do not add inspection grids to final assets, and do not ask PixelLab to draw inspection grids.
- If the original output has the right canvas size but the visible content uses a different grid, report the mismatch and do not present crops as repaired final assets.
- For sheets with cells below `32px`, use human visual review plus content-level measurement when possible.
