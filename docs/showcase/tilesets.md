# Tilesets

Last reviewed: 2026-07-02.

<table>
  <tr>
    <td colspan="2" align="center"><img src="tilesets/one-bit-16px-top-down-tilesets.png" alt="one-bit 16px top-down tilesets example"></td>
  </tr>
  <tr>
    <td><img src="tilesets/one-bit-black-green-topdown-tileset.png" alt="1-bit black and gameplay-green top-down tileset showcase"></td>
    <td><img src="tilesets/one-bit-black-gameboy-green-sidescroller-tileset.png" alt="1-bit black and Game Boy green sidescroller tileset showcase"></td>
  </tr>
</table>

PixelLab Pip can route top-down terrain/autotile and sidescroller/platformer requests through PixelLab's managed tileset tooling, then preserve accepted PixelLab structure while documenting any local palette work separately. The showcased top-down asset pairs the accepted strict black-and-white copy with the requested gameplay-green copy in one side-by-side composition. The showcased sidescroller pair demonstrates the same preservation-and-palette-clamp workflow for a compact platformer tileset.

## Contents

- [Primary Example: 1-Bit Black And Green Top-Down Tileset](#primary-example-1-bit-black-and-green-top-down-tileset)
- [Sidescroller Example: 1-Bit Black And Game Boy Green Platform Tileset](#sidescroller-example-1-bit-black-and-game-boy-green-platform-tileset)
- [Findings](#findings)
- [Showcase Assets](#showcase-assets)
- [Validation Notes](#validation-notes)

## Primary Example: 1-Bit Black And Green Top-Down Tileset

![1-bit black and gameplay-green top-down tileset showcase](tilesets/one-bit-black-green-topdown-tileset.png)

Original prompt:

```text
/pixellab-pip create 1-bit tileset with black upper, black lower, and black transition with horizontal white stripes. after done, create a copy with gameplay 1 bit green colors.
```

The 1-bit tileset example demonstrates a top-down Wang/autotile workflow with an important palette caveat. PixelLab generated the terrain-transition structure, but the raw PixelLab output contained near-black, cream, blue, and gray-ish colors rather than strict 1-bit black and white. The accepted final assets were local palette-clamped copies made from that PixelLab output: one exact black-and-white version and one exact gameplay-green recolor.

Source inputs: text-only request. No reference images, style images, masks, or palette images were supplied for the selected source generation.

Route: PixelLab MCP `create_topdown_tileset`.

Prompt preparation: agent-optimized from the user's 1-bit tileset request.

Local processing: the accepted black-and-white copy was palette-clamped to `#000000` and `#FFFFFF`; the gameplay-green copy was palette-clamped to `#0F380F` and `#9BBC0F`; the showcase image was locally assembled by placing those two accepted copies side by side at native size. No local shape edits or scaling were made.

Generation details:

| Field | Value |
|---|---|
| Output structure | Top-down Wang/autotile tileset |
| Source sheet | PixelLab MCP generated tileset |
| Source sheet size | `64x64` |
| Tile size | `16x16` |
| Final showcase image | `128x64`, native-size side-by-side composition |
| View | `high top-down` |
| Detail | `low detail` |
| Shading | `flat shading` |
| Outline | `lineless` |
| Transition size | `0.5` |
| Usage reported | Not exposed by MCP for the selected source generation |

MCP generation parameters:

```json
{
  "lower_description": "solid black 1-bit terrain, pure black fill, flat untextured surface, no gray tones",
  "upper_description": "solid black 1-bit terrain, pure black fill, flat untextured surface, no gray tones",
  "transition_description": "solid black transition bands with crisp horizontal pure white stripes, high contrast black and white only, no gray tones",
  "transition_size": 0.5,
  "detail": "low detail",
  "shading": "flat shading",
  "outline": "lineless",
  "mode": "standard",
  "tile_size": {
    "width": 16,
    "height": 16
  },
  "view": "high top-down",
  "text_guidance_scale": 12
}
```

Findings:

- The generated top-down tileset structure was usable for the requested compact black terrain transition.
- The raw PixelLab output did not natively pass strict 1-bit palette validation.
- Palette clamping produced exact two-color variants without changing tile shapes.
- The gameplay-green copy is a recolor of the accepted black-and-white copy, not a separate PixelLab generation.
- A later REST tileset attempt with a palette reference produced stricter black output but lost the visible stripe detail, so it was not selected for the showcase.

## Sidescroller Example: 1-Bit Black And Game Boy Green Platform Tileset

![1-bit black and Game Boy green sidescroller tileset showcase](tilesets/one-bit-black-gameboy-green-sidescroller-tileset.png)

Original prompt:

```text
/pixellab-pip create 1-bit sidescroller tileset with black center with white outline, and sparse white top. after done, create a copy with gameboy 1 bit green colors.
```

This example demonstrates a sidescroller/platformer workflow where the generated structure was accepted, but the raw PixelLab palette drifted away from strict 1-bit colors. The raw output contained 13 dark bluish-gray visible colors. The accepted final assets were local palette-clamped copies made from that PixelLab output: one exact black-and-white version and one exact Game Boy green recolor.

Source inputs: text-only request. No reference images, style images, masks, or palette images were supplied for the selected source generation.

Route: PixelLab MCP `create_sidescroller_tileset`.

Prompt preparation: agent-optimized from the user's sidescroller request.

Local processing: the accepted black-and-white copy was palette-clamped to `#000000` and `#FFFFFF`; the Game Boy green copy was palette-clamped to `#0F380F` and `#9BBC0F`; the showcase image was locally assembled by placing those two accepted copies side by side at native size, with the Game Boy green copy on the right. No local shape edits or scaling were made.

Generation details:

| Field | Value |
|---|---|
| Output structure | Sidescroller/platformer tileset |
| Source sheet | PixelLab MCP generated tileset |
| Source sheet size | `64x64` |
| Tile size | `16x16` |
| Tile count | `16` |
| Final showcase image | `128x64`, native-size side-by-side composition |
| View | Side-view platformer |
| Detail | `low detail` |
| Shading | `flat shading` |
| Outline | `single color outline` |
| Transition size | `0.25` |
| Usage observed | Balance moved from `440` to `437` generations remaining |

MCP generation parameters:

```json
{
  "lower_description": "strict 1-bit monochrome platform tile center: solid black terrain body, black fill in the middle, crisp white single-pixel outer outline, no gray, no anti-aliasing, simple high-contrast bitmap shapes",
  "transition_description": "sparse white pixels only along the top surface, minimal broken white dust or snow-like speckles, mostly black underneath, no gray, no anti-aliasing",
  "transition_size": 0.25,
  "detail": "low detail",
  "shading": "flat shading",
  "outline": "single color outline",
  "tile_size": {
    "width": 16,
    "height": 16
  }
}
```

Findings:

- The generated sidescroller tileset structure was usable for the requested black center, white outline, and sparse white top.
- The raw PixelLab output did not natively pass strict 1-bit palette validation.
- Palette clamping produced exact black-and-white and Game Boy green variants while preserving the generated PixelLab shapes.
- The Game Boy green copy is a recolor of the accepted black-and-white copy, not a separate PixelLab generation.
- This is a good example for documenting strict-palette verification because the raw art looked close but contained 13 visible colors.

## Findings

Top-down tileset generation is appropriate for terrain-transition requests that mention upper terrain, lower terrain, and transitions. For strict 1-bit palette requirements, current top-down generation should be verified against exact visible colors before being called final. Palette-constrained local derivatives should be documented separately from the raw PixelLab output.

Sidescroller tileset generation is appropriate for compact side-view platform requests with a lower platform material and a top transition layer. For strict 1-bit sidescroller requests, the same caveat applies: MCP prompt wording can produce a usable structure but may not enforce exact two-color output without verification and palette-clamped derivatives.

Prompt language that helped:

- `solid black 1-bit terrain` anchored both terrain sides.
- `horizontal pure white stripes` and `high contrast black and white only` helped push the transition toward readable stripe detail.
- `low detail`, `flat shading`, and `lineless` reduced extra rendering complexity.

Prompt language that remained soft:

- `1-bit`, `pure black`, and `no gray tones` did not fully constrain the raw PixelLab palette.
- The horizontal stripe request influenced the transition but did not produce perfectly uniform scanlines across every transition tile.

Practical notes from follow-up trials:

- Palette reference images can improve strict black-and-white output, but may reduce the transition texture that made the selected example readable. For this showcase, local palette clamping preserved the preferred PixelLab structure and texture better than selecting a palette-referenced generation.
- Transition reference images are most useful when authored in single-tile context, such as `16x16` for a `16x16` tileset. For `transition_size: 0.5`, the transition pattern belongs in the relevant half-tile band inside that tile context, not in a full `4x4` output-sheet-sized reference.
- Higher text guidance and stricter palette wording did not reliably improve the artistic result. Verification should check both structure readability and exact palette, because improving one can hurt the other.

## Showcase Assets

| Output | Stable showcase file |
|---|---|
| Black-and-white plus Game Boy green one-bit 16px top-down tilesets example | `docs/showcase/tilesets/one-bit-16px-top-down-tilesets.png` |
| Black-and-white plus gameplay-green tileset composition | `docs/showcase/tilesets/one-bit-black-green-topdown-tileset.png` |
| Black-and-white plus Game Boy green sidescroller tileset composition | `docs/showcase/tilesets/one-bit-black-gameboy-green-sidescroller-tileset.png` |

## Validation Notes

- The one-bit 16px top-down tilesets example is exactly `256x128`.
- The one-bit 16px top-down tilesets example contains only `#000000`, `#FFFFFF`, `#0F380F`, and `#9BBC0F` as visible colors.
- The one-bit 16px top-down tilesets example preserves the original black-and-white copy on the left and adds the Game Boy green copy on the right.
- The showcased composition is exactly `128x64`.
- The showcased composition contains only `#000000`, `#FFFFFF`, `#0F380F`, and `#9BBC0F` as visible colors.
- The black-and-white half uses only `#000000` and `#FFFFFF`.
- The gameplay-green half uses only `#0F380F` and `#9BBC0F`.
- The showcase composition preserves the accepted source copies at native `64x64` size.
- Local processing changed palette colors and assembled the two accepted copies into one showcase image.
- The sidescroller showcase composition is exactly `128x64`.
- The sidescroller showcase composition contains only `#000000`, `#FFFFFF`, `#0F380F`, and `#9BBC0F` as visible colors.
- The sidescroller black-and-white half uses only `#000000` and `#FFFFFF`.
- The sidescroller Game Boy green half uses only `#0F380F` and `#9BBC0F`.
- The sidescroller showcase composition preserves the accepted source copies at native `64x64` size.
