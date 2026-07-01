# Create Image Pro

Read this for explicit Create Image Pro wording, REST `generate-image-v2`, exact grid or sheet requests, and small cell-size requests that are not already covered by `skill-icons.md` or `item-icons.md`.

Create Image Pro / REST `generate-image-v2` is a general image-generation route. It can make attractive sprite sheets and texture sheets, but exact cell layout is prompt-guided rather than structurally guaranteed. A correct output canvas size is not proof that the image contains the requested cell grid.

## Sub-32px Cell Requests

For exact grid, sheet, tile, icon, or sprite requests where the requested per-cell size is below `32px`, treat Create Image Pro as prompt-sensitive rather than structurally guaranteed. Do not avoid Create Image Pro by default when the user asks for it; use prompt wording that makes the intended cell math, independence, and no-margin packing explicit, then verify the raw output honestly.

When the user explicitly asks for Create Image Pro and a below-32px cell size, do not ask them to switch tools solely because the cells are below `32px`. Recommend a different route only when their actual goal is a tile-specific asset such as Wang/autotile terrain, isometric tiles, or individual tile variants, or when they require structural guarantees that prompt-guided Create Image Pro cannot provide. For packed sheet requests, proceed with the best prompt pattern below and verify the result before calling it valid.

Use these alternatives only when they better match the user's actual intent:

- `create_tiles_pro` / REST `create-tiles-pro` for individual square, hex, octagon, or isometric tile variants, including small tile sizes.
- `create_topdown_tileset` / REST `create-tileset` for top-down Wang/autotile terrain transitions.
- `create_sidescroller_tileset` / REST `create-tileset-sidescroller` for platformer terrain.
- `create_isometric_tile` / REST `create-isometric-tile` for one isometric tile or block.

Do not call a Create Image Pro result a valid exact tile/icon/sprite grid based only on `image_size`. The output must pass visual cell-layout verification.

## 16px Minecraft Sheet Prompt Lessons

A request for a `256x256` Create Image Pro sheet with a `16 by 16` grid of `16x16` Minecraft-style tiles can produce an attractive texture sheet, but not a true 16px tile grid. The PNG may be `256x256`, so it can be mechanically sliced into 16px cells, while the visible content still spans cells. In one observed failure, visual seams appeared around `25-26px` intervals despite the correct canvas size.

The failure came from confusing canvas math with content layout. `image_size: { "width": 256, "height": 256 }` controlled only the final image dimensions; the prompt asked for 16px cells, but `generate-image-v2` did not enforce cell boundaries.

Observed prompt failures:

- `grid`, `atlas`, `texture sheet`, and generic material lists can produce continuous rows, long planks, terrain bands, or multi-cell textures.
- `contact sheet` and `separate thumbnails` can improve cell independence, but may introduce visible gutters, borders, or spacing.
- Asking PixelLab to draw guide lines or a visible grid bakes those lines into the generated asset. Do not do this for final tiles.

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
- Use local crop/split or boundary-measurement tools only for inspection or packaging, preserving original pixels. Do not add inspection grids to final assets, and do not ask PixelLab to draw inspection grids.
- If the original output has the right canvas size but the visible content uses a different grid, report the mismatch and do not present crops as repaired final assets.
- For sheets with cells below `32px`, use human visual review plus content-level measurement when possible.
