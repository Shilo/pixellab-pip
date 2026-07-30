# RPG Maker map-character sheet formats

Research checked July 30, 2026. This document covers the closely related alpha-capable PC charset formats used by the blueprint. It separates engine requirements from familiar RTP defaults. A size labeled **flexible** is computed from the imported image; the listed conventional size is a practical blueprint default, not an engine limit.

## Verified format matrix

| Version | Engine size rule and blueprint cell | Single-character output | Rows, top to bottom | Columns, left to right | Engine playback |
|---|---|---|---|---|---|
| RPG Maker XP | Engine-derived/flexible; blueprint uses the official 128×192 example's **32×48** cells | 128×192 PNG; one character; 4 columns × 4 rows | Down, Left, Right, Up | Walk patterns 1, 2, 3, 4; no inserted center-standing column | 1→2→3→4→1… |
| RPG Maker VX | Engine-derived/flexible; blueprint uses the conventional **32×32** character grid | `$rpg-maker-character.png`, 96×128; 3 columns × 4 rows | Down, Left, Right, Up | Movement pose A, standing pose, opposing movement pose B | 2→1→2→3→2… |
| RPG Maker VX Ace | Engine-derived/flexible; blueprint uses the native-era **32×32** character grid | `$rpg-maker-character.png`, 96×128; 3 columns × 4 rows | Down, Left, Right, Up | Movement pose A, standing pose, opposing movement pose B | 2→1→2→3→2… |
| RPG Maker MV | Engine-derived/flexible; **48×48 is documented as normal** | `$rpg-maker-character.png`, 144×192; 3 columns × 4 rows | Down, Left, Right, Up | Movement pose A, standing pose, opposing movement pose B | 2→1→2→3→2… |
| RPG Maker MZ | Engine-derived/flexible; **48×48 is documented as normal** | `$rpg-maker-character.png`, 144×192; 3 columns × 4 rows | Down, Left, Right, Up | Movement pose A, standing pose, opposing movement pose B | 2→1→2→3→2… |

## Blueprint decisions

- The exposed variables are `RPG Maker version` (default **MZ**) and `character` (default **adult male human chibi base character with non-explicit doll-like anatomy and no clothing or equipment**).
- PixelLab creates four cardinal rotations first. A user checkpoint then offers **Continue animating**, **Regenerate character**, or **Stop here**. Regeneration is an additional paid creation and therefore gets its own cost gate; continuing uses the already-approved animation jobs.
- PixelLab generates a 48px master because MZ is the default and MV/MZ normally use 48×48 cells. Packaging crops only fully transparent margins and downscales when a 32px profile requires it; it never upscales or repaints.
- PixelLab directions map explicitly to engine rows: south→Down row 1, west→Left row 2, east→Right row 3, north→Up row 4.
- XP retains the four returned walk frames in columns 1–4. For the three-frame engines, column 2 is the reviewed static rotation/standing pose and columns 1 and 3 are a visually verified pair of opposing stride poses kept in chronological order.
- XP packaging must verify the returned four-frame animation remains a clean loop across the 4→1 seam. PixelLab documents the frame count but not the gait phase assigned to each returned index.
- Normalization uses a shared crop, one global nearest-neighbor scale, a stable horizontal center, and a common foot baseline; fitting each frame independently would introduce visible jitter.
- Version selection controls the target canvas, cell convention, frame selection, and filename. Resizing uses nearest-neighbor sampling, preserves aspect ratio, and pads rather than repainting.
- VX through MZ receive the `$` single-character form because it is smaller and unambiguous. `!` is not added because a normal walking character should keep the engine's usual vertical offset and bush behavior.

## Scope

The executable blueprint covers RPG Maker XP, VX, VX Ace, MV, and MZ. RPG Maker 95, 2000, 2003, Unite, and console editions are outside this deliberately narrow workflow.

## Sources

- [RPG Maker XP material standards](https://rpgmakerofficial.com/product/products/rpgxp/material/index.html)
- [RPG Maker XP help: material specifications](https://www.rpg-maker.fr/dl/monos/aide/xp/source/rpgxp/material.html)
- [RPG Maker VX material standards](https://rpgmakerofficial.com/product/products/rpgvx/material/index.html)
- [RPG Maker VX Ace help: resource standards](https://www.rpgmaker.fixato.org/Manual/RPGVXAce/rpgvxace/6100_resource.html)
- [RPG Maker MV feature comparison: VX Ace 32×32 to MV 48×48](https://rpgmakerofficial.com/product/mv/new_function/02.html)
- [RPG Maker MV help: asset standards](https://rpgmakerofficial.com/product/MV_Help/page/01_11_01.html)
- [RPG Maker MZ help: asset standards](https://rpgmakerofficial.com/product/MZ_help-en/01_11_01.html)
- [Official charset structure and playback guide](https://www.rpgmakerweb.com/blog/charsets-structure-and-avoiding-traps)
