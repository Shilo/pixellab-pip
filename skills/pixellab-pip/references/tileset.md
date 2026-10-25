# Tilesets

Read this for tilesets, isometric tiles, tile variants, and ambiguous tile requests.

## Contents

- [MCP Route Inputs](#mcp-route-inputs)
- [Human Label To API Mapping](#human-label-to-api-mapping)
- [Generation Controls](#generation-controls)
- [Strict 1-bit / Exact Palette Work](#strict-1-bit--exact-palette-work)
- [Fetching Results (top-down)](#fetching-results-top-down)
- [Autotile Preview (top-down)](#autotile-preview-top-down)
- [Chaining Terrains (top-down)](#chaining-terrains-top-down)
- [Ground Textures And Loose Variants](#ground-textures-and-loose-variants)

## MCP Route Inputs

Multi-shape connectable terrain transition:

- Use MCP `create_tiles_pro` or REST `POST /create-tiles-pro` with `tile_feature="tileset"` only when the user explicitly requests a hex, isometric, or oblique connectable terrain transition, or explicitly requests tiles-pro tileset mode. Plain `create_tiles_pro` generates independent tile variations, not an autotiling tileset; never omit `tile_feature="tileset"` for a connectable-set request.
- Put the ordered terrain pair in `description`, such as `grass to water`; the first terrain is the main terrain and the second surrounds it.
- `tile_type` supports `square_topdown`, `isometric`, `hex`, `hex_pointy`, and `oblique` in tileset mode. Square top-down, isometric, and oblique return a 16-tile corner set; hex shapes return a 32-tile coastline set.
- Shape controls are `tile_size` (connectable sets have tighter per-shape ranges than plain variants, and square top-down roads are exactly 32), `tile_view_angle`, `tile_depth_ratio`, `tile_flat_top_px` (isometric), `oblique_lean` (oblique), and `outline_mode`. `create_tiles_pro` exposes no boundary-raggedness or raised-terrain-height fields; do not map those concepts to another tiles-pro control.
- `style_images` cannot be combined with `tile_feature="tileset"`. For square top-down requests, supplied per-terrain reference images require REST `create-tileset`; the MCP top-down schema does not expose them. Hex palette fields exist on both surfaces; see `create-image-pro.md` for their mode limits.
- Poll MCP `get_tiles_pro(tile_id)` or REST `GET /tiles-pro/{tile_id}` for completion and per-tile placement rules. Interpret `edge/4` bits as N/E/S/W continuation; `edge/6` bits as the six hex edges counter-clockwise from vertex 0, where set means the other terrain lies beyond; and `corner/4` as `NW<<3 | NE<<2 | SW<<1 | SE`, where set means the first terrain occupies that corner.

Shared MCP controls on the top-down and sidescroller routes (not `create_tiles_pro`):

- `tile_size`: tile dimensions; sidescroller supports 16 or 32, top-down supports 16 or 32 in `standard` mode and 64 in `pro` mode.
- `transition_size`: amount of transition/top layer; use route-specific meaning below.
- `detail`: `low detail`, `medium detail`, `highly detailed`.
- `shading`: `flat shading`, `basic shading`, `medium shading`, `detailed shading`, `highly detailed shading`.
- `mode`: `standard` (default; runs on Pixen, cheap and fast) or `pro` (the richest painted tiles; use it when the look matters and its higher cost is approved — prices in `cost-routing.md`).
- `enhance` (default `true`, standard mode only; Pro ignores it) rewrites the descriptions and picks matching base colours before generation, and the stored tileset keeps the rewritten text, so a chained tileset reuses it. Set `enhance: false` when the user's exact wording must reach the model, and report which was used.
- No-effect fields: the MCP docs say `outline`, `text_guidance_scale`, `tile_strength`, `tileset_adherence`, and `tileset_adherence_freedom` have no effect on either route (standard runs on Pixen and Pro ignores them), and top-down `spread_x`/`slope_size` have none either; the REST top-down schema agrees. Omit them rather than tuning them. Only the REST sidescroller schema still describes them as controls.

Top-down MCP `create_topdown_tileset` route:

- Required terrain fields: `lower_description`, `upper_description`.
- Optional transition field: `transition_description`.
- Base tile fields for chaining: `lower_base_tile_id`, `upper_base_tile_id`.
- Route-only fields: `view` (`low top-down` or `high top-down`) and `shape_style` (`square` or `round`). Only Pro honours `view`; standard always draws high top-down, so offer Pro, with its cost, when the tileset must match the characters' view (`create_character` defaults to low top-down). `shape_style` is `mode="standard"` only — sending it with `mode="pro"` is rejected — and standard draws `round` borders when it is omitted. Leave it omitted unless the user explicitly requests square or round geometry; it is a structured geometry control, not a prompt-style hint.
- Pro mode is a richer painted tileset workflow for 16/32/64px tiles. Its border controls are `raggedness`, `roundness`, `boundary_amplitude`/`boundary_seed`, `step_slope`, and `connect_diagonals`; use them only when the user asks for that geometry. `raggedness` defaults to 0 and ranges from 0 (smooth) to 1 (rough); tall sets (`transition_size > 0.4`) are half as rough. `roundness` defaults to 0.85 in Pro (0.6 on standard): 0 is square, 1 is round, and 2 cuts corners at 45 degrees; values above 1 require Pro. `boundary_amplitude` defaults to 0 and ranges to 0.3; it works in Pro at any `transition_size`, or on standard only up to `transition_size: 0.5`. The seed defaults to 0 and repeats the same boundary meander. `step_slope` ranges to 2 but is only valid in Pro at `transition_size: 0.25`; 0 is a cliff and 2 is the gentlest slope. `connect_diagonals` is Pro-only and defaults to false. See the endpoint schema when exact validation matters.
- No `seed`: the MCP top-down route exposes none, so route reproducible top-down runs to REST `create-tileset`, which does.
- `transition_size` is how far the upper terrain rises, not a blend width: 0 is flat ground, 0.25 a low raised bank, 0.5 low walls, and 1.0 walls a full tile tall. Standard takes any value from 0 to 1; above 0.5 it makes 25 tiles in a 4x8 sheet and needs 16px tiles. Pro uses only 0, 0.25, 0.5, or 1.0 (MCP snaps to the nearest; REST accepts only those) and makes 25 tiles from 0.5. Check the requested atlas size and verify the returned layout before treating it as compact 4x4.

Sidescroller MCP `create_sidescroller_tileset` route:

- Required platform body field: `lower_description`.
- Required platform surface/top field: `transition_description`.
- Base tile field for chaining: `base_tile_id` (REST `create-tileset-sidescroller` names it `lower_base_tile_id`). MCP documents it as `mode="pro"` only: the platform body is reused, so repeat the same body in `lower_description` and describe only the new top in `transition_description`.
- Route-only field: `seed`. `mode` and `enhance` are MCP-only here; the REST sidescroller schema has neither, so a Pro sidescroller or `enhance: false` needs MCP.
- `transition_size` controls how much of the surface/top layer appears on the platform tile; MCP snaps it to the nearest of 0.0, 0.25, and 0.5.

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
| `Target palette`, `palette`, `1-bit palette`, `Game Boy palette` | `create_tiles_pro`, `create_topdown_tileset`, `create_sidescroller_tileset` | `palette`/`palette_name`/`max_colors` on `create_tiles_pro` and `create_topdown_tileset` (see `create-image-pro.md` for mode limits); none on `create_sidescroller_tileset` | For sidescroller, say palette is not enforced by MCP generation alone and plan an approved palette-control or palette-clamp route. |

Do not reinterpret `upper`, `lower`, `inner`, `outer`, `floor`, `wall`, `transition`, or `terrain pair` as sidescroller center/top layers without side-view intent. For an explicit Create Image Pro packed texture sheet or small-cell image grid, route to `create-image-pro.md`; do not treat it as an autotile tileset just because the user says tiles.

## Generation Controls

Treat structured API fields as controls, not prompt text. Change a control only when the user asked for it, the route requires it, a documented default must be supplied, or a verified failure mode calls for it; do not infer control values from descriptive words that can live safely in `lower_description`, `upper_description`, or `transition_description`. When the user asks for maximum/100%/forced text guidance, map that to the maximum valid `text_guidance_scale` only on REST sidescroller; elsewhere say the field has no effect (see the no-effect fields above) and sharpen the descriptions instead. Do not also change `transition_size` or other controls unless requested or the failure mode calls for it.

Treat `shading` and `detail` (plus `outline` on REST sidescroller) as weak style controls, not deterministic placement controls: PixelLab docs say each "Weakly" controls its aspect, affecting taste, texture, color variation, and contour strength without guaranteeing exact edges, palette, or texture density. For placement or material changes, adjust terrain/transition descriptions and `transition_size` first.

Exception to the rule above: on sidescroller tilesets, use `transition_size: 0.5` when the user requests or implies a transition but does not specify its size. On top-down tilesets it is upper-terrain height in both modes; choose it from the user's height intent, use 0.25 (a low bank; at 0 no transition strip is drawn) when a transition is implied without a height, and warn when the value produces 25 tiles. Do not infer `transition_size: 1.0` from `wall`, `dithered`, `textured`, `black and white`, `max text guidance`, or similar wording.

For REST top-down tilesets, use `lower_reference_image` and `upper_reference_image` in Pro when the user wants the shared terrain to match a tile in an existing tileset exactly; they are base-tile matching references in this mode. `transition_reference_image` remains a style reference, not a mask or stamp. Do not add references just because the user names a material, texture, wall, or floor; use them when supplied, requested, or approved for a retry. Author a local reference in single-tile context at the requested `tile_size` — a 16x16 tileset uses a 16x16 reference, and at `transition_size: 0.5` place the pattern in the 8-pixel band, not scaled to the full 4x4 sheet.

On REST top-down tilesets `color_image` now has no effect: standard picks its own colours, and Pro takes hex colours through `target_palette` (MCP `palette`; see `create-image-pro.md`). On REST sidescroller, `color_image` constrains the palette, not where colors or texture appear inside each tile; put texture placement in the descriptions. When it is requested or approved there, prepare it as 64x64 unless current behavior proves another size works: in an earlier top-down validation the validator accepted a smaller PNG but the background job later failed with an internal `Expected image of size 64x64` error. On that failure with a smaller/unknown palette image, retry once with a 64x64 `color_image` when budget allows, and report it as a PixelLab validation/background-job caveat. This 64x64 rule applies to `color_image`, not terrain/transition reference images.

## Strict 1-bit / Exact Palette Work

Tileset generators do not reliably enforce strict 1-bit black-and-white output from text alone. Treat `1-bit`, `black-and-white only`, `no gray`, and named exact palettes as palette requirements unless the user explicitly accepts approximation.

- Prioritize PixelLab-generated shape over raw palette: palette clamping can make a good shape exact black/white but cannot fix a wrong silhouette, exposed edge, center-tile seam, or misplaced transition without locally altering the art.
- Prefer standard mode over Pro for strict 1-bit top-down wall/floor tests: Pro makes tall walls and 25 tiles from `transition_size: 0.5`, while standard stays a compact 16-tile set up to 0.5.
- When a 1-bit tileset is requested, default any unspecified style controls that the route's schema says take effect to `detail: low detail`, `shading: flat shading`, and `outline: lineless`; preserve explicit user-supplied values.
- Standard top-down has no documented palette enforcement; the documented exact-palette top-down route is Pro with `palette` (REST `target_palette`, Pro-only), so offer it with its cost when an exact palette is required.
- If the route exposes a palette/control image field, use or ask for it. Otherwise state the limitation before generating, or deliver an honestly labeled palette-clamped derivative via `aseprite-cli.md` after saving the untouched original; report the original separately and do not imply the derivative is the raw PixelLab result.
- On REST sidescroller, do not treat a black/white `color_image` as the default 1-bit fix: in earlier tests it erased the white top rim. Verify raw PixelLab shape first, then palette-clamp for exact black/white derivatives.
- Top-down terrain transitions are more reliable than sidescroller generation for full connected-shape white outlines. Do not burn repeated sidescroller prompt-only attempts on that outline goal without a new control route or user-approved post-process.
- For exact niche constraints (strict palettes, monochrome, single-pixel rims, whole-shape sidescroller outlines), run a small proof test before batching. On a miss, suggest post-processing, reference/control routes, another PixelLab image route, or human-authored assets.

## Fetching Results (top-down)

On the MCP route, poll `get_topdown_tileset(tileset_id)` — it returns status, tile data, download links, and base tile IDs directly, with no separate preview-vs-final split. On the REST route, fetch both result surfaces: poll `GET /background-jobs/{background_job_id}` for preview fields, then use `GET /tilesets/{tileset_id}` for the actual tile set, metadata, and generation parameters. The final user-facing tileset for a 16-tile result is the 4x4 sheet in the dual-grid (`15-tileset`) format, assembled from the tiles' `image` data in the exact order returned by the getter (`get_topdown_tileset` or `GET /tilesets/{tileset_id}`); name it plainly, such as `tileset.png` or `tileset-4x4.png`. A 25-tile result uses a 4x8 sheet in the same returned order; do not repack it as 4x4. Do not sort the tiles by `wang_N`, `original_position`, corner pattern, or any other inferred index, because those layouts can scramble the usable sheet. Decode the returned tile PNGs in memory for this sheet; do not save separate per-tile PNG files unless the user asks for individual tiles or a package.

The background job `last_response` may include full-sheet `image` and `quantized_image` fields; treat these as previews, not the final sheet. Save/show `image` as the primary preview (more likely to match the final tiles) and `quantized_image` as secondary. These fields may be base64 raw RGBA buffers rather than PNG, so decode and convert before writing PNGs. Public REST docs expose no tileset ZIP/export endpoint for Wang, dual-grid 15-tileset, or 3x3 formats; use the returned tile PNGs for local packaging only when the user asks.

The detailed `get_topdown_tileset` section of the public MCP guide documents direct downloads for a completed top-down tileset, despite the guide's opening overview saying character downloads are the only direct HTTP endpoints: `GET /mcp/tilesets/{id}/image` returns the sheet (add `?inline=true` to return bytes instead of a CDN redirect), and `GET /mcp/tilesets/{id}/metadata` returns tile metadata including `bounding_box`, `corners`, and `pattern_4x4`. These are MCP-documented HTTP helpers, not REST v2 endpoints. They require no authentication; the UUID is the access key, so keep it private. While generation is pending, either route returns 423 with `Retry-After`.

## Autotile Preview (top-down)

When a seam/test-map preview is requested or needed for an observed problem on a 16-tile top-down set, save the `/mcp/tilesets/{id}/image` sheet and its `/metadata` JSON side by side as `<sheet>.png` + `<sheet>.json`, then run `python "<skill-dir>/assets/tileset_preview.py" map.png <sheet>.png [<next-sheet>.png ...]` (a chain in order, e.g. sea>beach then beach>grass). It paints a random autotiled map and `map_tiles.png` with each tile's corners; check seams and the diagonal tiles `0110`/`1001`, which a random map rarely shows. It rejects 25-tile sets. Exit 3 with a `skipped` status means Pillow or numpy is missing: report the preview as not run. A broken or thin bank on `0110`/`1001` is a finding, not retry authority; propose a new paid run of that set with another `boundary_seed`, or `connect_diagonals: true` when the game wants the two corners joined. For 25-tile cliff sets and Godot import, read PixelLab's MCP resource `pixellab://docs/godot/wang-tilesets`.

## Chaining Terrains (top-down)

A chain such as `sea > beach > grass` is one tileset per touching pair, in order; terrains that never touch need no set. Submit the first set; the submit returns its base tile ids. When it has finished, submit the next with `lower_base_tile_id` = the previous set's **upper** base tile id and `lower_description` repeating that terrain's words exactly, so the shared terrain matches on both sides. Report the base tile ids; extending the chain later needs them. One optional measured Pro-pair configuration at 32 px (not defaults): `transition_size: 0.25`, `boundary_amplitude: 0.15` (a natural meandering edge), `step_slope: 1` (a soft earthy bank; 0 is a cliff). Each terrain is one material plus one detail, with no objects or characters (they repeat on every tile).

## Ground Textures And Loose Variants

- A seamless ground texture that is not an autotile set: MCP `create_image_pixflux` with `view: "high top-down"`, `color_image_url` = the region's background for its palette, and `seamless tileable top-down ground texture ... even lighting, no objects`. Calm a noisy or streaky texture with `init_image_url` = the previous result at `init_image_strength` 40-90 (it is how much of the input is kept; this low keeps only the composition) and `flat even texture, no streaks`.
- Independent ground variants with `create_tiles_pro` (no `tile_feature`): a numbered list in `description`, `1). dark cracked basalt ground 2). basalt with thin glowing ember cracks ...`.
