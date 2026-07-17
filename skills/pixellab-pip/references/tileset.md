# Tilesets

Read this for terrain tilesets, platformer tilesets, isometric tiles, tile variants, or website Create Tileset Pro ambiguity. SKILL.md holds the model/mode label semantics this file does not restate (including that website Create Tileset Pro is not the public `create-tiles-pro` flow, and that Gemini wording is stale).

"Tiles" is ambiguous. If unclear, ask whether the user wants:

- Terrain/autotile tileset.
- Platformer/sidescroller tileset.
- Individual tile variants such as hex, octagon, square, or isometric.
- One isometric tile/block.
- Packed texture sheet/image grid via Create Image Pro.
- Manual website Create Tileset Pro.

Capture tile size, route/view, terrain pair or platform body/surface descriptions, transition description/size, base tile IDs, style/reference/palette images, and target engine/export convention when relevant.

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

Isometric MCP `create_isometric_tile` route:

- Required content field: `description`.
- Primary shape field: `tile_shape`; use `thin` for floor slabs, `thick` for raised platforms, and `block` for cubes, chunky objects, or full-height terrain blocks.
- Other common controls include `size`, `outline`, `shading`, `detail`, `text_guidance_scale`, and `seed`.
- REST `create-isometric-tile` uses different field names for the same ideas: `image_size`, `isometric_tile_size`, and `isometric_tile_shape` with values `thin tile`, `thick tile`, or `block`.

## Human Label To API Mapping

Website, Aseprite, and MCP/REST labels sometimes differ. Map only non-obvious human-facing wording to the route's structured parameters before generating; do not duplicate fields whose names are already symmetric or directly inferable.

These labels are not symmetric with the MCP parameter names:

| Human UI wording | Applies to | MCP parameter | Notes |
|---|---|---|---|
| `Top tile description`, `Top Tile` | `create_sidescroller_tileset` | `transition_description` | Sidescroller MCP calls this the top decoration/surface layer. Not the same as `transition_size`. |
| `Center tile description`, `Center Tile`, `platform center` | `create_sidescroller_tileset` | `lower_description` | Sidescroller MCP calls this the platform material/body. |
| `thin floor`, `floor slab`, `flat tile` | `create_isometric_tile` | `tile_shape: "thin"` | REST uses `isometric_tile_shape: "thin tile"`. |
| `thick platform`, `raised platform` | `create_isometric_tile` | `tile_shape: "thick"` | REST uses `isometric_tile_shape: "thick tile"`. |
| `block`, `cube`, `full-height tile` | `create_isometric_tile` | `tile_shape: "block"` | Same value on REST `isometric_tile_shape`. |
| `Target palette`, `palette`, `1-bit palette`, `Game Boy palette` | `create_topdown_tileset`, `create_sidescroller_tileset` | no current MCP parameter | If no palette/control image field is exposed, say palette is not enforced by MCP generation alone and plan an approved palette-control or palette-clamp route. |

Route top-down terrain/autotile wording to `create_topdown_tileset` unless the user explicitly asks for platformer/sidescroller/side-view tiles. Phrases such as `upper`, `lower`, `inner`, `outer`, `floor`, `wall`, `transition`, `Wang`, `autotile`, or `terrain pair` describe top-down structure absent side-view intent; do not reinterpret them as sidescroller center/top layers just because the words include floor or wall. For an explicit Create Image Pro packed texture sheet or small-cell image grid, route to `create-image-pro.md`; do not treat it as a Wang/autotile tileset just because the user says tiles.

## Generation Controls

Treat structured API fields as controls, not prompt text. Change a control only when the user asked for it, the route requires it, a documented default must be supplied, or a verified failure mode calls for it; do not infer control values from descriptive words that can live safely in `lower_description`, `upper_description`, or `transition_description`. When the user asks for maximum/100%/forced text guidance, map that to the maximum valid `text_guidance_scale`; do not also change `transition_size`, `tile_strength`, `tileset_adherence`, or `tileset_adherence_freedom` unless requested or the failure mode calls for it.

Treat `outline`, `shading`, and `detail` as weak style controls, not deterministic placement controls: PixelLab docs say each "Weakly" controls its aspect, affecting taste, texture, color variation, and contour strength without guaranteeing exact edges, palette, or texture density. For placement or material changes, adjust terrain/transition descriptions and `transition_size` first.

For any MCP or REST route that exposes `transition_size`, use `transition_size: 0.5` when the user requests or implies a transition but does not specify its size. Do not infer `transition_size: 1.0` from `wall`, `dithered`, `textured`, `black and white`, `max text guidance`, or similar wording.

For REST top-down tilesets, `lower_reference_image`, `upper_reference_image`, and `transition_reference_image` are stronger composition/style controls than `color_image`. Do not add them just because the user names a material, texture, wall, or floor; use them when the user supplies a reference, asks for one, or approves a retry after a miss. Treat `transition_reference_image` as a style reference, not a mask or stamp; keep `text_guidance_scale` at default unless the text matters more than the reference (high text guidance competes with it and worsens palette drift). Author a local reference in single-tile context at the requested `tile_size` — a 16x16 tileset uses a 16x16 reference, and at `transition_size: 0.5` place the pattern in the 8-pixel band, not scaled to the full 4x4 sheet.

`color_image` constrains the palette, not where colors or texture appear inside each Wang tile; put texture placement in the terrain's description, not only the transition description. When `color_image` is requested or approved for top-down REST tilesets, prepare it as 64x64 unless current behavior proves another size works: the validator may accept a smaller PNG but the background job can fail later with an internal `Expected image of size 64x64` error. On that failure with a smaller/unknown palette image, retry once with a 64x64 `color_image` when budget allows, and report it as a PixelLab validation/background-job caveat. This 64x64 rule applies to `color_image`, not terrain/transition reference images.

## Strict 1-bit / Exact Palette Work

Tileset generators do not reliably enforce strict 1-bit black-and-white output from text alone, even at high `text_guidance_scale`. Treat `1-bit`, `black-and-white only`, `no gray`, and named exact palettes as palette requirements unless the user explicitly accepts approximation.

- Prioritize PixelLab-generated shape over raw palette: palette clamping can make a good shape exact black/white but cannot fix a wrong silhouette, exposed edge, center-tile seam, or misplaced transition without locally altering the art.
- Prefer standard mode over Pro for strict 1-bit top-down wall/floor tests: Pro outputs can expand at `transition_size: 0.5`, while standard mode is the safer compact 16-tile path.
- When a 1-bit tileset is requested and the route exposes style controls, default any unspecified ones to `detail: low detail`, `shading: flat shading`, and `outline: lineless`; preserve explicit user-supplied values.
- If the route exposes a palette/control image field, use or ask for it. Otherwise state the limitation before generating, or deliver an honestly labeled palette-clamped derivative via `aseprite-cli.md` after saving the untouched original; report the original separately and do not imply the derivative is the raw PixelLab result.
- Do not treat a black/white `color_image` as the default 1-bit fix: it can erase white transitions on black terrain. Verify raw PixelLab shape first, then palette-clamp for exact black/white derivatives.
- Top-down terrain transitions are more reliable than sidescroller generation for full connected-shape white outlines. Do not burn repeated sidescroller prompt-only attempts on that outline goal without a new control route or user-approved post-process.
- For exact niche constraints (strict palettes, monochrome, single-pixel rims, whole-shape sidescroller outlines), run a small proof test before batching. On a miss, suggest post-processing, reference/control routes, another PixelLab image route, or human-authored assets.

## Fetching Results (top-down REST)

After generation completes, fetch both result surfaces: poll `GET /background-jobs/{background_job_id}` for preview fields, then use `GET /tilesets/{tileset_id}` for the actual tile set, metadata, and generation parameters. The final user-facing tileset for a 16-tile result is the dual-grid 15-tileset 4x4 sheet assembled from `tileset.tiles[].image` in the exact order returned by `GET /tilesets/{tileset_id}`; name it plainly, such as `tileset.png` or `tileset-4x4.png`. Do not sort the tiles by `wang_N`, `original_position`, corner pattern, or any other inferred index, because those layouts can scramble the usable 16-tile sheet. Decode the returned tile PNGs in memory for this sheet; do not save separate per-tile PNG files unless the user asks for individual tiles or a package.

The background job `last_response` may include full-sheet `image` and `quantized_image` fields; treat these as previews, not the final sheet. Save/show `image` as the primary preview (more likely to match the final tiles) and `quantized_image` as secondary. These fields may be base64 raw RGBA buffers rather than PNG, so decode and convert before writing PNGs. Public REST docs expose no tileset ZIP/export endpoint for Wang, dual-grid 15-tileset, or 3x3 formats; use the returned tile PNGs for local packaging only when the user asks.
