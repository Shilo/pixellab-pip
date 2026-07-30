# RPG Maker map-character sheet formats

Research checked July 30, 2026. This document covers the closely related alpha-capable PC charset formats used by the blueprint. It separates engine requirements from familiar RTP defaults. A size labeled **flexible** is computed from the imported image; the listed conventional size is a practical blueprint default, not an engine limit.

## Verified format matrix

| Version | Character/cell size | Sheet format | Frames per walk cycle | Direction order | Other import behavior |
|---|---|---|---:|---|---|
| RPG Maker XP | **Flexible**; 32×48 is the common RTP convention | One character per image; 4 columns × 4 rows | 4 | Down, left, right, up | The engine divides the image into equal quarters horizontally and vertically. PNG supports full alpha. The documented cycle repeats 1→2→3→4→1. |
| RPG Maker VX | **Flexible**; 32×32 is the common convention | Normally eight characters arranged 4×2, each 3×4; `$` selects a one-character 3×4 sheet | 3 | Down, left, right, up | The middle column is standing and the runtime sequence returns through it: 2→1→2→3. Characters normally render four pixels above the tile; a leading `!` suppresses that shift and bush processing. |
| RPG Maker VX Ace | **Flexible**; 32×32 is the common convention | Same eight-character and `$` single-character layouts as VX | 3 | Down, left, right, up | Same center-standing sequence and four-pixel normal vertical shift as VX; `!` suppresses the shift and bush processing. PNG alpha is supported. |
| RPG Maker MV | **Flexible**; **48×48 is documented as normal** | Normally eight characters arranged 4×2, each 3×4; `$` selects a one-character 3×4 sheet | 3 | Down, left, right, up | The middle column is standing and playback returns through it. Characters normally render six pixels above the tile; `!` suppresses that shift and bush processing. Use PNG. |
| RPG Maker MZ | **Flexible**; **48×48 is documented as normal** | Same eight-character and `$` single-character layouts as MV | 3 | Down, left, right, up | Same center-standing sequence, six-pixel normal vertical shift, `$`, and `!` behavior as MV. MZ's selectable map tile size does not impose a different character cell size; character cells are still derived from the image grid. |

## Blueprint decisions

- The exposed variables are `RPG Maker version` (default **MZ**) and `character` (default **adult male human chibi base character with non-explicit doll-like anatomy and no clothing or equipment**).
- PixelLab creates four cardinal rotations first. A user checkpoint then offers **Continue animating**, **Regenerate character**, or **Stop here**. Regeneration is an additional paid creation and therefore gets its own cost gate; continuing uses the already-approved animation jobs.
- PixelLab's four-frame walk source is retained for XP. For the three-frame engines, packaging uses two opposing stride poses around the clean directional base/standing pose.
- Version selection controls the target canvas, cell convention, frame selection, and filename. Resizing uses nearest-neighbor sampling, preserves aspect ratio, and pads rather than repainting.
- VX through MZ receive the `$` single-character form because it is smaller and unambiguous. `!` is not added because a normal walking character should keep the engine's usual vertical offset and bush behavior.

## Scope

The executable blueprint covers RPG Maker XP, VX, VX Ace, MV, and MZ. RPG Maker 95, 2000, 2003, Unite, and console editions are outside this deliberately narrow workflow.

## Sources

- [RPG Maker XP material standards](https://rpgmakerofficial.com/product/products/rpgxp/material/index.html)
- [RPG Maker XP help: material specifications](https://www.rpg-maker.fr/dl/monos/aide/xp/source/rpgxp/material.html)
- [RPG Maker VX material standards](https://rpgmakerofficial.com/product/products/rpgvx/material/index.html)
- [RPG Maker VX Ace help: resource standards](https://www.rpgmaker.fixato.org/Manual/RPGVXAce/rpgvxace/6100_resource.html)
- [RPG Maker MV help: asset standards](https://rpgmakerofficial.com/product/MV_Help/page/01_11_01.html)
- [RPG Maker MZ help: asset standards](https://rpgmakerofficial.com/product/MZ_help-en/01_11_01.html)
- [Official charset structure and playback guide](https://www.rpgmakerweb.com/blog/charsets-structure-and-avoiding-traps)
