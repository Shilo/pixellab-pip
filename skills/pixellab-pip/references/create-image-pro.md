# Create Image Pro

Read this for explicit Create Image Pro wording, REST `generate-image-v2`, exact grid or sheet requests, and small cell-size requests that are not already covered by `skill-icons.md` or `item-icons.md`.

Create Image Pro / REST `generate-image-v2` is a general image-generation route. It can make attractive sprite sheets and texture sheets, but exact cell layout is prompt-guided rather than structurally guaranteed. A correct output canvas size is not proof that the image contains the requested cell grid.

## Sub-32px Cell Requests

For exact grid, sheet, tile, icon, or sprite requests where the requested per-cell size is below `32px`, treat Create Image Pro as unreliable unless the user explicitly accepts it as an experimental texture-sheet route.

If the user explicitly asks for Create Image Pro and a below-32px cell size, do not immediately spend credits. Briefly explain that Create Image Pro can return the requested canvas size while the visual cells drift away from the requested pixel grid. Ask whether they want to switch to a tile-specific route instead.

Prefer these alternatives when they match the user's intent:

- `create_tiles_pro` / REST `create-tiles-pro` for individual square, hex, octagon, or isometric tile variants, including small tile sizes.
- `create_topdown_tileset` / REST `create-tileset` for top-down Wang/autotile terrain transitions.
- `create_sidescroller_tileset` / REST `create-tileset-sidescroller` for platformer terrain.
- `create_isometric_tile` / REST `create-isometric-tile` for one isometric tile or block.

If the user confirms they still want Create Image Pro, label the result as an experimental texture or preview sheet until verification passes. Do not call it a valid exact tile/icon/sprite grid based only on `image_size`.

## What Went Wrong In The 16px Minecraft Tile Attempt

A request for a `256x256` Create Image Pro sheet with a `16 by 16` grid of `16x16` Minecraft-style tiles produced an attractive texture sheet, but not a true 16px tile grid. The PNG was `256x256`, so it could be mechanically sliced into 16px cells, but measured visual seams were around `25-26px` intervals instead of `16px` intervals.

The failure came from confusing canvas math with content layout. `image_size: { "width": 256, "height": 256 }` controlled only the final image dimensions; the prompt asked for 16px cells, but `generate-image-v2` did not enforce cell boundaries.

## Verification

For exact grid outputs from Create Image Pro:

- Verify the original PixelLab output against both canvas size and visual cell layout.
- Check that visible boundaries, object centers, or tile extents actually follow the requested per-cell grid.
- Use local crop/split or boundary-measurement tools only for inspection or packaging, preserving original pixels.
- If the original output has the right canvas size but the visible content uses a different grid, report the mismatch and do not present crops as repaired final assets.
- For sheets with cells below `32px`, use human visual review plus content-level measurement when possible.
