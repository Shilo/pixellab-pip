# Tilesets

Read this for terrain tilesets, platformer tilesets, isometric tiles, tile variants, or website Create Tileset Pro ambiguity.

"Tiles" is ambiguous. If unclear, ask whether the user wants:

- Terrain/autotile tileset.
- Platformer/sidescroller tileset.
- Individual tile variants such as hex, octagon, square, or isometric.
- One isometric tile/block.
- Packed texture sheet/image grid via Create Image Pro.
- Manual website Create Tileset Pro.

Capture tile size, route/view, terrain pair or platform body/surface descriptions, transition description/size, base tile IDs, style/reference/palette images, seed, and target engine/export convention when relevant.

## MCP Route Inputs

MCP `create_topdown_tileset` and `create_sidescroller_tileset` are sibling routes. Keep shared guidance shared, and separate route-specific instructions when a field means something different or only exists on one route.

Shared MCP controls currently visible on both routes:

- `tile_size`: tile dimensions; sidescroller supports 16 or 32, top-down supports 16 or 32 in `standard` mode and 64 in `pro` mode.
- `transition_size`: amount of transition/top layer; use route-specific meaning below.
- `detail`: `low detail`, `medium detail`, `highly detailed`.
- `shading`: `flat shading`, `basic shading`, `medium shading`, `detailed shading`, `highly detailed shading`.
- `outline`: `single color outline`, `selective outline`, `lineless`.
- `text_guidance_scale`, `tile_strength`, `tileset_adherence`, `tileset_adherence_freedom`, `seed`: generation controls.

Top-down MCP `create_topdown_tileset` route:

- Required terrain fields: `lower_description`, `upper_description`.
- Optional transition field: `transition_description`.
- Base tile fields for chaining: `lower_base_tile_id`, `upper_base_tile_id`.
- Route-only fields: `mode` (`standard` or `pro`) and `view` (`low top-down` or `high top-down`).
- Pro-only shape fields: `spread_x`, `slope_size`, `raggedness`.
- `transition_size` controls terrain blending/height behavior for top-down tiles; documented examples include 0.0, 0.25, 0.5, and 1.0.

Sidescroller MCP `create_sidescroller_tileset` route:

- Required platform body field: `lower_description`.
- Required platform surface/top field: `transition_description`.
- Base tile field for chaining: `base_tile_id`.
- No `upper_description`, `view`, `mode`, or Pro-only shape fields are exposed by the current MCP sidescroller tool.
- `transition_size` controls how much of the surface/top layer appears on the platform tile; documented examples include 0.0, 0.25, and 0.5.

## Human Label To API Mapping

Website, Aseprite extension, and MCP/REST labels sometimes differ. Map only non-obvious human-facing wording to the route's actual structured parameters before generating; do not duplicate schema fields whose names are already symmetric or directly inferable.

These labels are not symmetric with the MCP parameter names:

| Human UI wording | Applies to | MCP parameter | Notes |
|---|---|---|---|
| `Top tile description`, `Top Tile` | `create_sidescroller_tileset` | `transition_description` | Sidescroller MCP calls this the top decoration/surface layer. It is not the same as `transition_size`. |
| `Center tile description`, `Center Tile`, `platform center` | `create_sidescroller_tileset` | `lower_description` | Sidescroller MCP calls this the platform material/body. |
| `Target palette`, `palette`, `1-bit palette`, `Game Boy palette` | `create_topdown_tileset`, `create_sidescroller_tileset` | no current MCP parameter | If no palette/control image field is exposed by the chosen route, say palette is not enforced by MCP generation alone and plan an approved palette-control or palette-clamp route. |

No extra top-down human-label mapping is currently needed for schema-like labels such as lower, upper, or transition. Route top-down terrain wording to `create_topdown_tileset`; do not reuse sidescroller top/center label mapping unless the user explicitly asks for side-view/platformer tiles.

For an explicit Create Image Pro packed texture sheet or exact small-cell image grid, route to `create-image-pro.md`; do not reinterpret it as a Wang/autotile tileset just because the user says tiles.

Route top-down terrain/autotile wording to top-down tileset generation unless the user explicitly asks for platformer, sidescroller, side-view, or platform tiles. Phrases such as `upper`, `lower`, `inner`, `outer`, `floor`, `wall`, `transition`, `Wang`, `autotile`, or `terrain pair` describe top-down tileset structure when no side-view/platformer intent is present; do not reinterpret them as sidescroller center/top layers just because the words include floor or wall.

Before spending repeated generations on prompt wording, check the visible MCP schema or current REST schema for controllable generation parameters. For top-down and sidescroller tilesets, relevant controls may include:

- `text_guidance_scale`: increases or decreases text-description adherence.
- `tile_strength`: changes tile-pattern adherence.
- `tileset_adherence`: controls reference/texture image and tileset-structure adherence.
- `tileset_adherence_freedom`: controls structural flexibility; higher means more flexibility.
- `seed`: makes a promising setup reproducible when exposed.
- `lower_reference_image`, `upper_reference_image`, and `transition_reference_image`: REST controls for anchoring terrain or transition style.
- `color_image`: REST control for palette anchoring.
- Pro-only shape controls such as `spread_x`, `slope_size`, and `raggedness`.

Treat structured API fields as controls, not prompt text. Set or change controls only when the user explicitly requested that control, the route requires it, a documented default must be supplied by a helper, or a verified failure mode specifically calls for that control. Do not infer control values from descriptive words when those words can live safely in `lower_description`, `upper_description`, or `transition_description`.

When the user asks for maximum, 100%, or forced text guidance, map that request to the maximum valid `text_guidance_scale` exposed by the chosen tool or schema. Do not also change `transition_size`, `tile_strength`, `tileset_adherence`, or `tileset_adherence_freedom` unless the user requested those controls or the failure mode specifically calls for them.

For any MCP or REST tileset route that exposes `transition_size`, use `transition_size: 0.5` when the user requests or implies a transition but does not specify its size. Do not infer `transition_size: 1.0` from `wall`, `dithered`, `textured`, `black and white`, `max text guidance`, or similar prompt wording.

Tileset generators do not reliably enforce strict 1-bit black-and-white output from text alone, even with high `text_guidance_scale`. Treat `1-bit`, `black-and-white only`, `no gray`, and named exact palettes as palette requirements unless the user explicitly accepts approximation. If the chosen route exposes a palette/control image parameter, use or ask for that route-specific control. If the chosen route does not expose palette control, state that limitation before generation, or deliver an honestly labeled palette-clamped derivative after saving the untouched PixelLab original.

When the user requests a 1-bit tileset and the chosen tileset route exposes style controls, default any unspecified style controls to `detail: low detail`, `shading: flat shading`, and `outline: lineless`. Preserve explicit user-supplied values for those controls.

For REST top-down tilesets, treat `lower_reference_image`, `upper_reference_image`, and `transition_reference_image` as stronger composition/style controls than `color_image`. Do not author or add terrain/transition reference images just because the user asks for a material, texture, dither, wall, or floor. Use reference-image fields when the user supplies a reference, explicitly asks for a reference/control image, or approves a retry after the previous attempt misses the desired placement or material read. When using `transition_reference_image`, treat it as a style reference rather than an exact mask or stamp. Keep `text_guidance_scale` at the default unless the user's text description is more important than matching the reference image; high text guidance can make text/model priors compete with the reference and may worsen palette drift.

When authoring a local terrain or transition reference image for a top-down tileset, keep it in single-tile context: use the requested `tile_size` unless the user supplied a different reference size. For example, a 16x16 tileset should use a 16x16 transition reference; with `transition_size: 0.5`, place the transition pattern in the relevant 8-pixel band inside that 16x16 context. Do not scale terrain/transition references to the full 4x4 output sheet size. The 64x64 sizing caveat below applies to `color_image`, not to terrain or transition reference images.

When `color_image` is explicitly requested or approved for top-down REST tilesets, prepare it as a 64x64 palette reference unless current route behavior proves another size works. The request validator may accept a smaller PNG but the background job can fail later with an internal `Expected image of size 64x64` error. If a tileset job fails with that size expectation and the palette image was smaller or unknown, retry once with a 64x64 `color_image` when the user's budget/attempt count allows; report the mismatch as a PixelLab validation/background-job caveat.

`color_image` constrains the palette, not where colors or texture appear inside each Wang tile. If the user needs texture on a pure terrain tile, put the texture placement in that terrain's description, not only in the transition description. Reference images can force placement more strongly, but use them only under the reference-image conditions above.

For REST top-down tilesets, fetch both result surfaces after generation completes: poll `GET /background-jobs/{background_job_id}` for preview fields, then use `GET /tilesets/{tileset_id}` for the actual tile set, metadata, and generation parameters. The final user-facing tileset for a 16-tile result is the dual-grid 15-tileset 4x4 sheet assembled from `tileset.tiles[].image` in the exact order returned by `GET /tilesets/{tileset_id}`; name it plainly, such as `tileset.png` or `tileset-4x4.png`. Do not sort the tiles by `wang_N`, `original_position`, corner pattern, or any other inferred index because those layouts can scramble the usable 16-tile sheet. Decode the returned tile PNGs in memory for this sheet, but do not save separate per-tile PNG files unless the user asks for individual tiles or a package.

The background job `last_response` may include full-sheet fields such as `image` and `quantized_image`; treat these as previews/showcase images, not the final tileset sheet. Save and show `image` as the primary preview when present, because it is more likely to visually match the final tile images. Save `quantized_image` as a secondary preview when present. These background-job fields may be base64 raw RGBA buffers rather than PNG payloads, so decode and convert them before writing PNG files. Current public REST docs do not expose a tileset ZIP/export endpoint for website formats such as Wang, dual-grid 15-tileset, or 3x3; use the returned tile PNGs for local packaging only when the user asks for that format.

If PixelLab produces a useful tileset whose colors still need exact indexed-palette cleanup, read `aseprite-cli.md` for the palette-clamp route. Report the untouched PixelLab original separately from any Aseprite/local palette-clamped derivative, and do not imply the derivative is the raw PixelLab result.

Do not equate website Create Tileset Pro with public `create-tiles-pro`. Treat older Gemini wording as stale/low-confidence unless current official website docs reintroduce it.
