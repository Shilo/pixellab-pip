# Tilesets

Read this for terrain tilesets, platformer tilesets, isometric tiles, tile variants, or website Create Tileset Pro ambiguity.

"Tiles" is ambiguous. If unclear, ask whether the user wants:

- Terrain/autotile tileset.
- Platformer/sidescroller tileset.
- Individual tile variants such as hex, octagon, square, or isometric.
- One isometric tile/block.
- Manual website Create Tileset Pro.

Capture tile size, view, terrain pair or tile list, transition description, base tile IDs, style/reference/palette images, seed, and target engine/export convention when relevant.

Route top-down terrain/autotile wording to top-down tileset generation unless the user explicitly asks for platformer, sidescroller, side-view, or platform tiles. Phrases such as `upper`, `lower`, `inner`, `outer`, `floor`, `wall`, `transition`, `Wang`, `autotile`, or `terrain pair` describe top-down tileset structure when no side-view/platformer intent is present; do not reinterpret them as sidescroller center/top layers just because the words include floor or wall.

Before spending repeated generations on prompt wording, check the visible MCP schema or current REST schema for controllable generation parameters. For top-down and sidescroller tilesets, relevant controls may include:

- `text_guidance_scale`: increases or decreases text-description adherence.
- `tile_strength`: changes tile-pattern adherence.
- `tileset_adherence`: controls reference/texture image and tileset-structure adherence.
- `tileset_adherence_freedom`: controls structural flexibility; higher means more flexibility.
- `seed`: makes a promising setup reproducible when exposed.
- `lower_reference_image`, `upper_reference_image`, and `transition_reference_image`: REST controls for anchoring terrain or transition style.
- `color_image`: REST control for palette anchoring; for top-down REST tilesets, prepare it as a 64x64 palette reference unless current docs or route behavior prove another size is accepted.
- Pro-only shape controls such as `spread_x`, `slope_size`, and `raggedness`.

If the desired result depends on a strict palette, prefer REST tileset generation when it exposes `color_image` and the visible MCP tool does not. Use prompt-only MCP retries only after checking that the needed palette controls are unavailable in the current surface.

The Standard top-down generator does not reliably enforce strict 1-bit black-and-white output from text alone, even with high `text_guidance_scale`. Treat `1-bit`, `no gray`, and similar wording as soft hints unless a palette control or approved post-processing route is also used.

For REST top-down tilesets, treat `lower_reference_image`, `upper_reference_image`, and `transition_reference_image` as stronger composition/style controls than `color_image`. Do not author or add terrain/transition reference images just because the user asks for a material, texture, dither, wall, or floor. Use reference-image fields when the user supplies a reference, explicitly asks for a reference/control image, or approves a retry after a prompt-plus-palette attempt misses the desired placement or material read. When using `transition_reference_image`, treat it as a style reference rather than an exact mask or stamp. Keep `text_guidance_scale` at the default unless the user's text description is more important than matching the reference image; high text guidance can make text/model priors compete with the reference and may worsen palette drift.

Use REST `color_image` when the user clearly wants a fixed palette, such as an explicit color list, `1-bit`, `black and white`, or a supplied palette image. For top-down REST tilesets, the request validator may accept a smaller PNG but the background job can fail later with an internal `Expected image of size 64x64` error. Avoid that process trap by sending a 64x64 palette reference image for `color_image` unless current route behavior proves a different size works. If a tileset job fails with that size expectation and the palette image was smaller or unknown, retry once with a 64x64 `color_image` when the user's budget/attempt count allows; report the mismatch as a PixelLab validation/background-job caveat.

If PixelLab produces a useful tileset whose colors still need exact indexed-palette cleanup, read `aseprite-cli.md` for the palette-clamp route. Report the untouched PixelLab original separately from any Aseprite/local palette-clamped derivative, and do not imply the derivative is the raw PixelLab result.

Do not equate website Create Tileset Pro with public `create-tiles-pro`. Treat older Gemini wording as stale/low-confidence unless current official website docs reintroduce it.
