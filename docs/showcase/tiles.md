# Tiles

Last reviewed: 2026-07-01.

![Minecraft-inspired 16x16 tile atlas](tiles/minecraft-inspired-generate-image-v2-16x16-atlas.png)

![Minecraft mod 32px tile sheet](tiles/minecraft-mod-generate-image-v2-8x8-32px-sheet.png)

PixelLab Pip can showcase tile workflows from several surfaces: Create Image Pro texture sheets, `create_tiles_pro` tile variants, top-down Wang tilesets, sidescroller tilesets, and isometric tiles. The primary Create Image Pro example is a proper `256x256` atlas that mechanically slices into a `16x16` grid of `16x16` Minecraft-inspired tiles. It is useful as a first-pass atlas showcase, with one important caveat: strict uniqueness did not fully pass.

## Contents

- [Primary Example: Minecraft-Inspired 16x16 Atlas](#primary-example-minecraft-inspired-16x16-atlas)
- [Follow-Up Example: Minecraft Mod 32px Terrain Pack](#follow-up-example-minecraft-mod-32px-terrain-pack)
- [Findings](#findings)
- [Showcase Assets](#showcase-assets)
- [Validation Notes](#validation-notes)

## Primary Example: Minecraft-Inspired 16x16 Atlas

![Minecraft-inspired 16x16 tile atlas](tiles/minecraft-inspired-generate-image-v2-16x16-atlas.png)

Original prompt:

```text
/pixellab-pip create a grid of 16x16 minecraft-inspired tiles using image pro. every tile must be unique and textured.
```

The Minecraft-inspired atlas is the lead tile showcase because it is a valid `256x256` image that can be sliced into a `16x16` grid of `16x16` cells. It demonstrates that Create Image Pro can produce a mechanically correct atlas at Minecraft's native texture size. Verification found `251 / 256` exact-unique cells, so this is a strong first-pass atlas rather than a strict all-unique final pack.

Route: PixelLab REST v2 `generate-image-v2`, surfaced in product language as Create Image Pro.

Prompt preparation: agent-optimized from the user's Minecraft-style 16px atlas request.

Generation details:

| Field | Value |
|---|---|
| Image size | `256x256` |
| Atlas grid | `16x16` |
| Tile size | `16x16` |
| Background | `no_background: false` |
| Usage reported | `20` generations |
| Balance observation | `1448 -> 1428` generations |
| Exact-unique cells | `251 / 256` |

Request body:

```json
{
  "description": "A 256-file packed atlas of original voxel sandbox block-game terrain texture files, arranged as 16 columns by 16 rows. Each file occupies exactly one 16 by 16 pixel cell inside a 256 by 256 image. Cells touch edge-to-edge with zero pixels between cells. No margins, gutters, padding, spacing, separator pixels, blank pixels, outlines, frames, guide lines, or drawn grid. Every cell is completely filled edge-to-edge including corner pixels. Each of the 256 cells is unique, highly textured, and readable as a small square block face: stone, dirt, grass top, grass side, sand, gravel, clay, snow, ice, moss, bark, planks, leaves, ores, bricks, cobble, mud, lava rock, nether-like stone, fantasy minerals, farmland, hay, glass, wool, metal, decorative tiles, and rare variants. No large strips, connected terrain rows, scenery, UI, labels, text, icons, characters, tools, shadows spanning cells, highlights spanning cells, ore veins crossing cells, planks crossing cells, or texture detail continuing into neighboring cells. Crunchy 16-bit pixel-art texture, crisp square pixels, high material variety, original designs inspired by block-building survival games.",
  "image_size": {
    "width": 256,
    "height": 256
  },
  "no_background": false
}
```

Findings:

- The atlas passes canvas size and mechanical 16px slicing.
- The output is appropriate for a Minecraft-inspired `16x16` texture atlas showcase.
- Strict uniqueness did not fully pass: verification found `5` duplicate exact cells.
- Visual review found several repeated or similar material rows, so semantic uniqueness is weaker than the mechanical grid result.
- The best next strict-uniqueness route is to generate batches of native `16x16` Image Pro outputs, then assemble 256 PixelLab-origin tiles into one atlas.

## Follow-Up Example: Minecraft Mod 32px Terrain Pack

![Minecraft mod 32px tile sheet](tiles/minecraft-mod-generate-image-v2-8x8-32px-sheet.png)

Original prompt:

```text
pip create a grid of 32x32 tiles using create image pro. they must be various tiles for a minecraft mod
```

The Minecraft mod terrain pack demonstrates a cleaner uniqueness workflow at `32x32`: generate `64` original PixelLab images at native tile size, then locally arrange those original tiles into an exact `8x8` sheet. The assembled sheet is a stable showcase artifact with auditable 32px cell boundaries.

Route: PixelLab REST v2 `generate-image-v2`, surfaced in product language as Create Image Pro.

Prompt preparation: agent-optimized from the user's Minecraft tile-pack request.

Local processing: 64 original PixelLab `32x32` PNGs were arranged into an `8x8` sheet without repainting, resizing, quantization, or procedural visual fixes.

Generation details:

| Field | Value |
|---|---|
| Image size | `32x32` per generated tile |
| Tile count | `64` |
| Final sheet | `8x8`, `256x256` |
| Background | `no_background: false` |
| Seed | `1323610680` |
| Usage reported | `20` generations |
| Balance observation | `1564.25 -> 1544.25` generations |

Natural-language generation input:

```text
Varied Minecraft mod terrain block top-face textures, seamless 32x32 orthographic voxel-inspired tiles, no text/icons/borders/perspective.
```

Request settings:

```json
{
  "image_size": {
    "width": 32,
    "height": 32
  },
  "no_background": false,
  "seed": 1323610680
}
```

Findings:

- Generating original `32x32` tiles and assembling them locally produced a reliable sheet layout.
- The final spritesheet is exactly `256x256` and divides cleanly into `8x8` cells of `32x32`.
- Every tile was generated by PixelLab; local work only arranged original outputs into a sheet.
- The generated set is well suited to a Minecraft-inspired terrain pack because each source tile has the intended native size.
- This is still a texture-pack workflow, not a Wang/autotile terrain-transition workflow.

## Findings

Create Image Pro / REST `generate-image-v2` can produce mechanically valid atlas images when the whole atlas is generated at once, as shown by the `16x16` Minecraft-inspired atlas. Exact semantic uniqueness is still a separate verification step; a correct grid can contain repeated or visually similar cells.

For stricter uniqueness, generating tiles at native size and assembling PixelLab-origin outputs locally gives a clearer audit path. That approach worked well for the `32x32` terrain pack and is the recommended next pass for a fully unique `16x16` atlas, though it costs more generations.

Future tile showcases should live on this page when they cover different tile surfaces, including:

- Top-down Wang/autotile terrain from REST `create-tileset` or MCP `create_topdown_tileset`.
- Sidescroller/platformer terrain from REST `create-tileset-sidescroller` or MCP `create_sidescroller_tileset`.
- Individual tile variants from REST `create-tiles-pro` or MCP `create_tiles_pro`.
- Single isometric tiles from REST `create-isometric-tile` or MCP `create_isometric_tile`.

Prompt language that helped:

- `16 columns by 16 rows` and `each file occupies exactly one 16 by 16 pixel cell` anchored the atlas layout.
- `No margins, gutters, padding, spacing, separator pixels, blank pixels, outlines, frames, guide lines, or drawn grid` helped preserve mechanical slicing.
- Broad terrain-material lists improved coverage.
- `No large strips`, `no connected terrain rows`, and no cross-cell detail wording reduced but did not eliminate repeated or similar cells.

## Showcase Assets

| Output | Stable showcase file |
|---|---|
| Minecraft-inspired 16x16 atlas | `docs/showcase/tiles/minecraft-inspired-generate-image-v2-16x16-atlas.png` |
| Minecraft mod 32px terrain spritesheet | `docs/showcase/tiles/minecraft-mod-generate-image-v2-8x8-32px-sheet.png` |

## Validation Notes

- The 16px atlas is exactly `256x256`.
- The 16px atlas divides exactly into a `16x16` grid of `16x16` cells.
- The 16px atlas passed canvas size and mechanical slicing checks.
- The 16px atlas failed strict exact uniqueness with `251 / 256` unique cells.
- The 16px atlas has visible repeated or similar material rows.
- The 32px pack retained `64` generated tiles.
- Each generated 32px tile is exactly `32x32`.
- The assembled 32px sheet is exactly `256x256` and divides exactly into an `8x8` grid.
- All `64` 32px tiles have unique PNG hashes and full-square opaque coverage.
- No local repainting, resizing, quantization, cleanup, or procedural visual fixes were applied to the showcased tile pixels.
