# PixelLab Top-Down Tileset Transition Findings

Last reviewed: 2026-07-01.

This note records live-generation findings for PixelLab top-down Wang/autotile tilesets when using the hosted MCP `create_topdown_tileset` tool for grid-based graybox prototyping assets.

## Summary

For compact top-down prototype tilesets, `transition_size` is not only a visual control. It can also change the exported atlas layout and tile count. These findings apply primarily to Standard mode unless a Pro-mode caveat is called out.

- `transition_size: 0.0` produces the compact 16-tile `tileset15_4x4` layout, but can look flat unless the prompt strongly describes height, bevels, contrast, and boundary treatment.
- `transition_size: 0.25` also produces the compact 16-tile `tileset15_4x4` layout. It can produce clean, readable colored outlines, but live graybox tests showed risks where the top/floor tile lost visible grid detail and the lower and upper terrain colors became too similar.
- `transition_size: 0.5` produces the compact 16-tile `tileset15_4x4` layout. In live graybox tests, this was the strongest compact candidate overall because it kept the required atlas size while giving better wall depth and separation than `0.25`.
- `transition_size: 1.0` produced a richer visual result in one test, but expanded the output to a larger `tileset15_4x8` atlas with 25 populated tiles in live tests. It also produced stretched or poor-looking candidates in later tests. Do not assume it will preserve a strict 4x4 atlas.

## Standard vs Pro Mode

Standard mode was the better fit for the tested graybox prototype goal. A batch of Standard `32x32` generations with `transition_size: 0.5` consistently downloaded as compact `128x128` 4x4 atlases, and one Standard `0.5` candidate was the strongest result in live review.

Pro mode was not a good fit in the same live review. Even when the prompt explicitly requested full continuous grid lines at 16px spacing with no dashed or broken lines, the generated assets drifted toward rounded or block-mass shapes rather than crisp grid-based graybox Wang tiles. Pro `0.0` and `0.25` kept the compact `128x128` 4x4 atlas, but were still visually rejected for this prototype use case.

Pro `0.5` and `1.0` both showed the expanded-layout problem. The requested Pro `0.5` run returned metadata with `transition_size: 1.0` and downloaded as `128x256`, a 4x8 atlas with 25 populated tiles. The Pro `1.0` run also downloaded as `128x256`. Treat Pro transition values at and above `0.5` as unsafe for strict 16-tile 4x4 graybox exports until this behavior changes.

Pro mode was also materially more expensive in the live test. Four accepted Pro generations consumed 80 subscription generations, while a ten-generation Standard `0.5` batch consumed 40 subscription generations. Record this as observed run cost, not a permanent pricing guarantee.

## Accepted Values

The MCP tool currently validates `transition_size` as one of:

- `0.0`
- `0.25`
- `0.5`
- `1.0`

Attempts to use values such as `0.75` or `0.99` were rejected by request validation before generation. Agents should not suggest near-`1.0` fractional values as a workaround for the full-transition atlas expansion unless current public PixelLab docs or tool validation change.

## Graybox Prompt Findings

The most useful graybox prompts described separate visual roles for the terrains:

- Lower terrain: dark charcoal or navy blueprint floor, visible construction grid, sparse markers, and clear walkable base.
- Upper terrain: raised slate-blue wall or platform blocks, lighter than the floor, beveled square edges, cyan edge highlights, and collision-readable geometry.
- Transition: grid-aligned seams, thin cyan construction lines, yellow or magenta measurement ticks, clean corner joins, subtle height cues, and no organic terrain blending.

Prompts that over-emphasized outlines, darkness, or contrast could make the output read as a single island or void shape instead of distinct raised blockout tiles. Prompts that under-specified contrast could make floor and wall tiles look too similar.

## One-Bit And Dithering Findings

Prompt-only attempts were not able to force strict 1-bit black-and-white output or a dithered wall transition in hosted MCP Standard top-down tilesets.

A ten-generation Standard batch used:

- `tile_size: 16x16`
- `view: high top-down`
- `transition_size: 0.5`
- `outline: lineless`
- `shading: flat shading`
- `detail: low detail`
- `text_guidance_scale: 20`
- no `color_image`
- no lower, upper, or transition reference images
- default `tile_strength`, `tileset_adherence`, and `tileset_adherence_freedom`

The ten text variants tried concise and explicit phrases such as `1-bit`, `pure black`, `pure monochrome`, `no gray`, `black and white`, `dithered wall`, `dithered wall face`, `dithered vertical wall surface`, `dither wall band`, `checker black white wall surface`, `pixel noise`, `white pixels on black`, and `stippled wall surface`.

All ten outputs preserved the expected compact atlas size: each downloaded PNG was `64x64`, matching a 4x4 grid of `16x16` tiles. None produced strict 1-bit output. Unique RGB color counts ranged from 13 to 37, and every output contained non-black/non-white colors. Several outputs also introduced visible tint despite monochrome wording; one high-contrast silhouette prompt drifted strongly purple.

The strongest visual cluster came from prompts that kept both lower and upper terrain black or monochrome and described the transition as a white-on-black or black-and-white wall surface. Prompts that made the upper terrain white tended to brighten the whole terrain too much. However, even the strongest cluster did not place readable dithering on the wall surface.

Observed conclusion: `text_guidance_scale` is a soft prompt-following control, not a hard palette, dithering, or material-placement constraint. For strict palette or precise dithering-placement tests, prompt-only MCP generation should be treated as low-confidence. Prefer REST `color_image` for palette anchoring, REST reference-image fields for terrain or transition anchoring, or an explicitly approved local/editor post-process workflow when the user wants deterministic 1-bit indexed output or ordered dithering.

`color_image` is a REST-only palette reference image field for tileset generation. It should not be used when the experiment is specifically measuring text-only obedience, because it changes the test from prompt-following to palette anchoring.

### Transition Reference Image Test

A two-generation REST `POST /v2/tilesets` batch tested whether a small ordered-dither `transition_reference_image` could force wall-surface dithering. Both generations used the same concise prompts and settings:

- `lower_description: 1-bit black floor`
- `upper_description: 1-bit black wall`
- `transition_description: dithered black and white wall`
- `tile_size: 16x16`
- `mode: standard`
- `view: high top-down`
- `transition_size: 0.5`
- `outline: lineless`
- `shading: flat shading`
- `detail: low detail`
- `transition_reference_image`: a 16x16 black-and-white ordered dither checker

The first generation omitted `text_guidance_scale` and metadata confirmed the default value `8.0`. The second set `text_guidance_scale: 20.0`.

Both REST tileset objects contained 16 tiles at `16x16`, and the assembled canonical atlases were `64x64`. The default-guidance result was visually stronger: it was closer to black and white and picked up horizontal wall-band structure from the reference. The max-guidance result preserved more block/grid structure but drifted purple and had more colors. Neither copied the ordered dither pattern into the transition surface.

Observed conclusion: `transition_reference_image` can influence the transition style, but it is still a style/reference input, not an exact texture stamp or mask. Raising `text_guidance_scale` does not increase reference-image adherence; it can make text and model priors compete harder with the reference image. In this test, max text guidance worsened palette drift.

The 16x16 dither reference was a reasonable first test because the tileset tile size was 16x16 and REST does not document a separate required size for transition references. However, `transition_size: 0.5` means the visible wall/transition surface is roughly half-tile scale in many tiles. For future tests, prefer a 16x16 reference that includes tile context and an 8-pixel-high transition/wall band, rather than a pure full-tile checker. A bare 8x8 reference might match the half-tile idea, but it loses context and may be resized or interpreted only as generic texture.

## Routing Guidance

For a strict 4x4 graybox top-down tileset, start with:

- Standard mode
- `tile_size: 32x32`
- `transition_size: 0.5` first, with `0.25` as the next compact fallback
- `view: high top-down`
- low detail
- selective outline
- flat or basic shading

Avoid Pro mode for this specific graybox blockout workflow unless testing Pro-only controls such as corner-pair behavior, spread, slope, or raggedness. The live Pro tests cost more and did not improve visual quality for compact grid prototyping.

Use `transition_size: 1.0` only when the richer expanded transition set is acceptable. It may be visually preferable, but it should be treated as a different export layout rather than a compact 16-tile replacement.

Do not spend large prompt-only batches trying to force exact 1-bit palettes or transition-surface dithering. First decide whether the goal is text-obedience research or production control. For production control, move to REST palette/reference inputs or approved Aseprite/indexed-color processing instead of escalating prompt wording alone.

When testing `transition_reference_image`, keep `text_guidance_scale` at the default first. Increase it only when the text wording itself is more important than the reference style, because high text guidance does not mean high reference adherence.

## Verification

After generation, verify the downloaded PNG dimensions and metadata rather than relying on preview size:

- Compact `32x32` 4x4 output should download as `128x128`.
- Expanded `32x32` 4x8 output should download as `128x256`.
- Compact `16x16` 4x4 output should download as `64x64`.
- For strict palette claims, count unique RGB colors in the original downloaded PNG and verify the exact palette rather than relying on the prompt or preview.
- Check metadata fields such as `tile_size`, `tileset_data.total_tiles`, `tileset_data.spritesheet_grid`, and `tileset_data.spritesheet_layout`.
