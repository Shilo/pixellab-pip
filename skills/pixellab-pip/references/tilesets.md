# Tilesets

Read this for terrain tilesets, platformer tilesets, isometric tiles, tile variants, or website Create Tileset Pro ambiguity.

"Tiles" is ambiguous. If unclear, ask whether the user wants:

- Terrain/autotile tileset.
- Platformer/sidescroller tileset.
- Individual tile variants such as hex, octagon, square, or isometric.
- One isometric tile/block.
- Packed texture sheet/image grid via Create Image Pro.
- Manual website Create Tileset Pro.

Capture tile size, view, terrain pair or tile list, transition description, base tile IDs, style/reference/palette images, seed, and target engine/export convention when relevant.

For an explicit Create Image Pro packed texture sheet or exact small-cell image grid, route to `create-image-pro.md`; do not reinterpret it as a Wang/autotile tileset just because the user says tiles.

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

Treat structured API fields as controls, not prompt text. Set or change controls only when the user explicitly requested that control, the route requires it, a documented default must be supplied by a helper, or a verified failure mode specifically calls for that control. Do not infer control values from descriptive words when those words can live safely in `lower_description`, `upper_description`, or `transition_description`.

When the user asks for maximum, 100%, or forced text guidance, map that request to the maximum valid `text_guidance_scale` exposed by the chosen tool or schema. Do not also change `transition_size`, `tile_strength`, `tileset_adherence`, or `tileset_adherence_freedom` unless the user requested those controls or the failure mode specifically calls for them.

For any MCP or REST tileset route that exposes `transition_size`, use `transition_size: 0.5` when the user requests or implies a transition but does not specify its size. Do not infer `transition_size: 1.0` from `wall`, `dithered`, `textured`, `black and white`, `max text guidance`, or similar prompt wording.

If the desired result depends on a strict palette, prefer REST tileset generation when it exposes `color_image` and the visible MCP tool does not. Use prompt-only MCP retries only after checking that the needed palette controls are unavailable in the current surface.

The Standard top-down generator does not reliably enforce strict 1-bit black-and-white output from text alone, even with high `text_guidance_scale`. Treat `1-bit`, `no gray`, and similar wording as soft hints unless a palette control or approved post-processing route is also used.

For REST top-down tilesets, treat `lower_reference_image`, `upper_reference_image`, and `transition_reference_image` as stronger composition/style controls than `color_image`. Do not author or add terrain/transition reference images just because the user asks for a material, texture, dither, wall, or floor. Use reference-image fields when the user supplies a reference, explicitly asks for a reference/control image, or approves a retry after a prompt-plus-palette attempt misses the desired placement or material read. When using `transition_reference_image`, treat it as a style reference rather than an exact mask or stamp. Keep `text_guidance_scale` at the default unless the user's text description is more important than matching the reference image; high text guidance can make text/model priors compete with the reference and may worsen palette drift.

Use REST `color_image` when the user clearly wants a fixed palette, such as an explicit color list, `1-bit`, `black and white`, or a supplied palette image. For top-down REST tilesets, the request validator may accept a smaller PNG but the background job can fail later with an internal `Expected image of size 64x64` error. Avoid that process trap by sending a 64x64 palette reference image for `color_image` unless current route behavior proves a different size works. If a tileset job fails with that size expectation and the palette image was smaller or unknown, retry once with a 64x64 `color_image` when the user's budget/attempt count allows; report the mismatch as a PixelLab validation/background-job caveat.

`color_image` constrains the palette, not where colors or texture appear inside each Wang tile. If the user needs texture on a pure terrain tile, put the texture placement in that terrain's description, not only in the transition description. Reference images can force placement more strongly, but use them only under the reference-image conditions above.

For REST top-down tilesets, fetch both result surfaces after generation completes: poll `GET /background-jobs/{background_job_id}` for preview fields, then use `GET /tilesets/{tileset_id}` for the actual tile set, metadata, and generation parameters. The final user-facing tileset for a 16-tile result is the dual-grid 15-tileset 4x4 sheet assembled from `tileset.tiles[].image` in the exact order returned by `GET /tilesets/{tileset_id}`; name it plainly, such as `tileset.png` or `tileset-4x4.png`. Do not sort the tiles by `wang_N`, `original_position`, corner pattern, or any other inferred index because those layouts can scramble the usable 16-tile sheet. Decode the returned tile PNGs in memory for this sheet, but do not save separate per-tile PNG files unless the user asks for individual tiles or a package.

The background job `last_response` may include full-sheet fields such as `image` and `quantized_image`; treat these as previews/showcase images, not the final tileset sheet. Save and show `image` as the primary preview when present, because it is more likely to visually match the final tile images. Save `quantized_image` as a secondary preview when present. These background-job fields may be base64 raw RGBA buffers rather than PNG payloads, so decode and convert them before writing PNG files. Current public REST docs do not expose a tileset ZIP/export endpoint for website formats such as Wang, dual-grid 15-tileset, or 3x3; use the returned tile PNGs for local packaging only when the user asks for that format.

If PixelLab produces a useful tileset whose colors still need exact indexed-palette cleanup, read `aseprite-cli.md` for the palette-clamp route. Report the untouched PixelLab original separately from any Aseprite/local palette-clamped derivative, and do not imply the derivative is the raw PixelLab result.

Do not equate website Create Tileset Pro with public `create-tiles-pro`. Treat older Gemini wording as stale/low-confidence unless current official website docs reintroduce it.
