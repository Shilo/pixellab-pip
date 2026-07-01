# Tilesets

Read this for terrain tilesets, platformer tilesets, isometric tiles, tile variants, or website Create Tileset Pro ambiguity.

"Tiles" is ambiguous. If unclear, ask whether the user wants:

- Terrain/autotile tileset.
- Platformer/sidescroller tileset.
- Individual tile variants such as hex, octagon, square, or isometric.
- One isometric tile/block.
- Manual website Create Tileset Pro.

Capture tile size, view, terrain pair or tile list, transition description, base tile IDs, style/reference/palette images, seed, and target engine/export convention when relevant.

Before spending repeated generations on prompt wording, check the visible MCP schema or current REST schema for controllable generation parameters. For top-down and sidescroller tilesets, relevant controls may include:

- `text_guidance_scale`: increases or decreases text-description adherence.
- `tile_strength`: changes tile-pattern adherence.
- `tileset_adherence`: controls reference/texture image and tileset-structure adherence.
- `tileset_adherence_freedom`: controls structural flexibility; higher means more flexibility.
- `seed`: makes a promising setup reproducible when exposed.
- `lower_reference_image`, `upper_reference_image`, and `transition_reference_image`: REST controls for anchoring terrain or transition style.
- `color_image`: REST control for palette anchoring.
- Pro-only shape controls such as `spread_x`, `slope_size`, and `raggedness`.

If the desired result depends on strict palette, dithering placement, or a specific wall/floor material split, prefer REST tileset generation when it exposes reference or palette image fields that the visible MCP tool does not. Use prompt-only MCP retries only after checking that the needed controls are unavailable in the current surface.

Live Standard top-down tests showed that even `text_guidance_scale: 20` did not force strict 1-bit black-and-white output or readable wall-surface dithering from text alone. Treat `1-bit`, `dithered`, `stippled`, `checker`, `no gray`, and similar wording as soft hints unless a palette/reference control or approved post-processing route is also used.

For REST top-down tileset reference-image tests, treat `transition_reference_image` as a style reference rather than an exact mask or stamp. If `tile_size` is 16 and `transition_size` is 0.5, a 16x16 reference remains valid, but a reference with an 8-pixel transition/wall band inside a 16x16 tile context may be a better next test than a bare 8x8 checker. Start with default `text_guidance_scale` when testing reference adherence; max text guidance can make text/model priors compete with the reference and may worsen palette drift.

Do not equate website Create Tileset Pro with public `create-tiles-pro`. Treat older Gemini wording as stale/low-confidence unless current official website docs reintroduce it.
