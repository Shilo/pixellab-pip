# Tilesets

Read this for tilesets, isometric tiles, tile variants, and ambiguous tile requests.

## MCP Route Inputs

Multi-shape connectable terrain transition:

- Use MCP `create_tiles_pro` or REST `POST /create-tiles-pro` with `tile_feature="tileset"` only when the user explicitly requests a hex, isometric, or oblique connectable terrain transition, or explicitly requests tiles-pro tileset mode. Plain `create_tiles_pro` generates independent tile variations, not an autotiling tileset; never omit `tile_feature="tileset"` for a connectable-set request.
- Put the ordered terrain pair in `description`, such as `grass to water`; the first terrain is the main terrain and the second surrounds it.
- `tile_type` supports `square_topdown`, `isometric`, `hex`, `hex_pointy`, and `oblique` in tileset mode. Square top-down, isometric, and oblique return a 16-tile corner set; hex shapes return a 32-tile coastline set.
- Shape controls are `tile_size`, `tile_view_angle`, `tile_depth_ratio`, `tile_flat_top_px` (isometric), `oblique_lean` (oblique), and `outline_mode`. `create_tiles_pro` exposes no boundary-raggedness or raised-terrain-height fields; do not map those concepts to another tiles-pro control.
- `style_images` cannot be combined with `tile_feature="tileset"`. For square top-down requests, supplied per-terrain reference images and palette controls require REST `create-tileset`; the MCP top-down schema does not expose those inputs.
- Poll MCP `get_tiles_pro(tile_id)` or REST `GET /tiles-pro/{tile_id}` for completion and per-tile placement rules.

Shared MCP controls on the top-down and sidescroller routes (not `create_tiles_pro`):

- `tile_size`: tile dimensions; sidescroller supports 16 or 32, top-down supports 16 or 32 in `standard` mode and 64 in `pro` mode.
- `transition_size`: amount of transition/top layer; use route-specific meaning below.
- `detail`: `low detail`, `medium detail`, `highly detailed`.
- `shading`: `flat shading`, `basic shading`, `medium shading`, `detailed shading`, `highly detailed shading`.
- `outline`: `single color outline`, `selective outline`, `lineless`.
- `text_guidance_scale`, `tile_strength`, `tileset_adherence`, `tileset_adherence_freedom`: generation controls.

Top-down MCP `create_topdown_tileset` route:

- Required terrain fields: `lower_description`, `upper_description`.
- Optional transition field: `transition_description`.
- Base tile fields for chaining: `lower_base_tile_id`, `upper_base_tile_id`.
- Route-only fields: `mode` (`standard` or `pro`), `view` (`low top-down` or `high top-down`), and `shape_style` (`square` or `round`). Leave `shape_style` omitted unless the user explicitly requests one of those boundary geometries; it is a structured geometry control, not a prompt-style hint.
- Pro-only shape fields: `spread_x`, `slope_size`, `raggedness`.
- No `seed`: the MCP top-down route exposes none, so route reproducible top-down runs to REST `create-tileset`, which does.
- `transition_size` controls terrain blending/height behavior for top-down tiles. MCP documents it as a float and cites 0.0, 0.25, 0.5, and 1.0; with explicit `shape_style`, it is continuous from 0 to 1 and values above 0.5 use an extended 4x8 sheet. Verify the returned layout before treating it as a compact 4x4 atlas. REST-specific validation is stricter: without `shape_style`, it accepts only those four values; its `shape_style` description supports square 16px or 32px tiles.

Sidescroller MCP `create_sidescroller_tileset` route:

- Required platform body field: `lower_description`.
- Required platform surface/top field: `transition_description`.
- Base tile field for chaining: `base_tile_id` (REST `create-tileset-sidescroller` names it `lower_base_tile_id`).
- Route-only field: `seed`.
- No `upper_description`, `view`, `mode`, or Pro-only shape fields are exposed by the current MCP sidescroller tool.
- `transition_size` controls how much of the surface/top layer appears on the platform tile; documented examples include 0.0, 0.25, and 0.5.

Isometric MCP `create_isometric_tile` route:

- Required content field: `description`.
- Primary shape field: `tile_shape`; use `thin tile` for floor slabs, `thick tile` for raised platforms, and `block` for cubes, chunky objects, or full-height terrain blocks (default `block`) — same three values as REST, not shortened on MCP.
- Other common controls include `size`, `outline`, `shading`, `detail`, `text_guidance_scale`, and `seed`.
- REST `create-isometric-tile` uses different field *names* for the same ideas: `image_size`, `isometric_tile_size`, and `isometric_tile_shape`, with the identical values `thin tile`, `thick tile`, or `block`.

Path/road and building-kit MCP routes:

- `create_path_tiles` (18-config connectable path/road set) and `create_building_kit` (floor, connectable walls, doorways, pillar, stairs) are siblings of `create_tiles_pro`, not `create_topdown_tileset` — all three share `get_tiles_pro`/`list_tiles_pro`/`delete_tiles_pro`; there is no separate getter/lister/deleter for path tiles or a building kit.
- REST folds all three into `create-tiles-pro` via `tile_feature`: `"roads"` (path tiles), `"tileset"` (the connectable terrain transition `create_tiles_pro` itself can produce), or `"building"` (building kit, with the `building_*` fields).
- On REST isometric `create-tiles-pro` requests, `tile_flat_top_px` controls the top/bottom cap: `2` is classic and `4` is modern. It is ignored for non-isometric `tile_type` values.

## Human Label To API Mapping

Map only non-obvious request wording to structured parameters.

These labels are not symmetric with the MCP parameter names:

| Human UI wording | Applies to | MCP parameter | Notes |
|---|---|---|---|
| `Top tile description`, `Top Tile` | `create_sidescroller_tileset` | `transition_description` | Sidescroller MCP calls this the top decoration/surface layer. Not the same as `transition_size`. |
| `Center tile description`, `Center Tile`, `platform center` | `create_sidescroller_tileset` | `lower_description` | Sidescroller MCP calls this the platform material/body. |
| `Target palette`, `palette`, `1-bit palette`, `Game Boy palette` | `create_tiles_pro`, `create_topdown_tileset`, `create_sidescroller_tileset` | no current MCP parameter | If no palette/control image field is exposed, say palette is not enforced by MCP generation alone and plan an approved palette-control or palette-clamp route. |

Do not reinterpret `upper`, `lower`, `inner`, `outer`, `floor`, `wall`, `transition`, or `terrain pair` as sidescroller center/top layers without side-view intent. For an explicit Create Image Pro packed texture sheet or small-cell image grid, route to `create-image-pro.md`; do not treat it as an autotile tileset just because the user says tiles.

## Generation Controls

Treat structured API fields as controls, not prompt text. Change a control only when the user asked for it, the route requires it, a documented default must be supplied, or a verified failure mode calls for it; do not infer control values from descriptive words that can live safely in `lower_description`, `upper_description`, or `transition_description`. When the user asks for maximum/100%/forced text guidance, map that to the maximum valid `text_guidance_scale`; do not also change `transition_size`, `tile_strength`, `tileset_adherence`, or `tileset_adherence_freedom` unless requested or the failure mode calls for it.

Treat `outline`, `shading`, and `detail` as weak style controls, not deterministic placement controls: PixelLab docs say each "Weakly" controls its aspect, affecting taste, texture, color variation, and contour strength without guaranteeing exact edges, palette, or texture density. For placement or material changes, adjust terrain/transition descriptions and `transition_size` first.

Exception to the rule above: for any MCP or REST route that exposes `transition_size`, use `transition_size: 0.5` when the user requests or implies a transition but does not specify its size. Do not infer `transition_size: 1.0` from `wall`, `dithered`, `textured`, `black and white`, `max text guidance`, or similar wording.

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

## Fetching Results (top-down)

On the MCP route, poll `get_topdown_tileset(tileset_id)` — it returns status, tile data, download links, and base tile IDs directly, with no separate preview-vs-final split. On the REST route, fetch both result surfaces: poll `GET /background-jobs/{background_job_id}` for preview fields, then use `GET /tilesets/{tileset_id}` for the actual tile set, metadata, and generation parameters. The final user-facing tileset for a 16-tile result is the 4x4 sheet in the dual-grid (`15-tileset`) format, assembled from the tiles' `image` data in the exact order returned by the getter (`get_topdown_tileset` or `GET /tilesets/{tileset_id}`); name it plainly, such as `tileset.png` or `tileset-4x4.png`. A 25-tile result uses a 4x8 sheet in the same returned order; do not repack it as 4x4. Do not sort the tiles by `wang_N`, `original_position`, corner pattern, or any other inferred index, because those layouts can scramble the usable sheet. Decode the returned tile PNGs in memory for this sheet; do not save separate per-tile PNG files unless the user asks for individual tiles or a package.

The background job `last_response` may include full-sheet `image` and `quantized_image` fields; treat these as previews, not the final sheet. Save/show `image` as the primary preview (more likely to match the final tiles) and `quantized_image` as secondary. These fields may be base64 raw RGBA buffers rather than PNG, so decode and convert before writing PNGs. Public REST docs expose no tileset ZIP/export endpoint for Wang, dual-grid 15-tileset, or 3x3 formats; use the returned tile PNGs for local packaging only when the user asks.
