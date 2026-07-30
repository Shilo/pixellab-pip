# RPG Maker map-character sheet formats

Research checked July 30, 2026. This document covers the Windows RPG Maker map-character formats from RPG Maker 2000 through MZ plus RPG Maker Unite. It separates engine requirements from familiar RTP defaults. A size labeled **flexible** is computed from the imported image or configured in the editor; the listed conventional size is not an engine limit.

## Verified format matrix

| Version | Cell and file geometry | Direction layout | Animation layout | Image-format notes |
|---|---|---|---|---|
| RPG Maker 2000 | Fixed **24x32** cells. A standard CharSet is **288x256**, containing 8 characters in a 4x2 character grid; the engine can also open a **72x128** single-character 3x4 sheet or a **24x32** non-animated character. | Within each character: **Up, Right, Down, Left** from top to bottom. | 3 columns; the center column is standing, flanked by the two step poses. | BMP or PNG must be 8-bit indexed with exactly 256 palette entries. Alpha/transparency chunks are ignored by the engine. |
| RPG Maker 2003 | Same map CharSet format as 2000: fixed **24x32** cells; **288x256** for 8 characters, **72x128** for one animated character, or **24x32** for one non-animated character. | **Up, Right, Down, Left** from top to bottom. | 3 columns; the center column is standing, flanked by the two step poses. | Same 8-bit indexed BMP/PNG restriction; alpha/transparency chunks are ignored. RPG Maker 2003 has additional battle-character formats, but those are not map CharSets. |
| RPG Maker XP | Engine-derived/flexible; this workflow's conventional value is the official **128x192** example's **32x48** cells. One character per file, **4 columns x 4 rows**. | **Down, Left, Right, Up** from top to bottom. | Columns are walk patterns **1, 2, 3, 4**; engine playback is **1→2→3→4→1…**. | PNG supports 32-bit color and alpha; JPG is also accepted but is unsuitable for transparent sprites. |
| RPG Maker VX | Engine-derived/flexible; conventional **32x32** cells. A `$` filename is one character in a **3x4** sheet; without `$`, a file contains 8 characters and is **12 cells x 8 cells**. | **Down, Left, Right, Up** from top to bottom. | Movement pose A, standing pose, opposing movement pose B; playback is **2→1→2→3→2…**. | PNG, JPG, or BMP; PNG supports alpha. `$` selects the single-character layout. `!` disables the normal 4-pixel upward display offset and bush translucency. |
| RPG Maker VX Ace | Same flexible geometry and 3x4/12x8 layouts as VX; conventional **32x32** cells. | **Down, Left, Right, Up** from top to bottom. | Movement pose A, standing pose, opposing movement pose B; playback is **2→1→2→3→2…**. | PNG or JPG; PNG supports alpha. `$` selects one character. `!` disables the normal 4-pixel upward display offset and bush translucency. |
| RPG Maker MV | Engine-derived/flexible; **48x48 is documented as normal**. A `$` filename is one character in a **3x4** sheet; without `$`, a file contains 8 characters and is **12 cells x 8 cells**. | **Down, Left, Right, Up** from top to bottom. | Movement pose A, standing pose, opposing movement pose B; playback is **2→1→2→3→2…**. | PNG. `$` selects one character. `!` disables the normal 6-pixel upward display offset and bush translucency. |
| RPG Maker MZ | Same flexible geometry as MV; **48x48 is documented as normal**. A `$` filename is one character in a **3x4** sheet; without `$`, a file contains 8 characters and is **12 cells x 8 cells**. | **Down, Left, Right, Up** from top to bottom. | Movement pose A, standing pose, opposing movement pose B; playback is **2→1→2→3→2…**. | PNG. `$` selects one character. `!` disables the normal 6-pixel upward display offset and bush translucency. |
| RPG Maker Unite | Flexible frame size configured in Resource Manager. Each direction is a **separate horizontal animation file**, not a row in one 3x4 or 4x4 charset. Frames require a 1-pixel transparent outer border and 2 transparent pixels between adjacent frames. The official 98x146 sample has a 96x144 visible region; it is an example, not a fixed cell size. | Four separately registered files: Facing Down, Facing Left, Facing Right, and Facing Up. Recommended names use `name_down_N.png`, `name_left_N.png`, `name_right_N.png`, and `name_up_N.png`. | Frame count is configurable per direction, may differ between directions, and is encoded horizontally. Resource Manager separately records frame size, frame count, and playback speed. | PNG. This is a materially different import model from XP–MZ and cannot be represented by merely changing the cell size or row order of the same atlas. |

## Blueprint scope and variables

The executable blueprint deliberately supports **XP, VX, VX Ace, MV, and MZ only**. RPG Maker 2000/2003 remain research-only because their fixed 24x32 indexed-palette CharSet pipeline would add palette conversion and different direction ordering for an exceptionally unlikely target. Unite remains research-only because it requires four separate direction files, explicit gutters, and per-direction import metadata rather than the single-sheet deliverable shared by XP–MZ.

The blueprint exposes three variables:

- `RPG Maker version`, default **MZ**. This is a validated export-profile enum, not image-prompt text. It selects cell defaults plus the engine's sheet geometry, frame semantics, and filename rules.
- `character`, default **adult male human chibi base character with non-explicit doll-like anatomy and no clothing or equipment**.
- `character cell size`, default **engine conventional**. An override accepts one positive integer for a square cell or `WIDTHxHEIGHT` for a rectangular cell. This controls export geometry only; it does not change PixelLab's generated subject size.

The current blueprint variable grammar resolves literal values; it does not need a dependent-expression extension. Its preflight `TASK` validates the version enum and maps it to primitive target dimensions when `character cell size` is `engine conventional`:

| Resolved version | `CW` | `CH` | Output formula |
|---|---:|---:|---|
| XP | 32 | 48 | `4*CW` by `4*CH` = 128x192 |
| VX | 32 | 32 | `3*CW` by `4*CH` = 96x128 |
| VX Ace / VXAce | 32 | 32 | `3*CW` by `4*CH` = 96x128 |
| MV | 48 | 48 | `3*CW` by `4*CH` = 144x192 |
| MZ | 48 | 48 | `3*CW` by `4*CH` = 144x192 |

An explicit cell-size override replaces `CW` and `CH` while retaining the selected engine's row count, column count, frame semantics, and filename rules. This is why version cannot collapse into size alone: XP and VX-family exports differ even when their conventional dimensions overlap. If the override is larger than the native subject bounds, the workflow adds transparent padding because it never upscales; requesting a larger generated subject is a separate override of PixelLab's generation `size`. Keeping the version mapping in the blueprint-specific TASK avoids adding a general-purpose expression language that every blueprint reader would then need to parse and validate.

The resolved version is never interpolated into `create_character.description`. PixelLab receives only visual guidance: the configurable character, four-direction top-down map-sprite readability, silhouette, identity, proportions, and pixel-art treatment. Engine-specific knowledge remains entirely in deterministic packaging TASKs.

## PixelLab source canvas versus RPG Maker cell size

PixelLab's MCP `create_character.size` is **character size**, not a guaranteed PNG canvas size. The current MCP documentation says the canvas is about 40% larger to leave room for animation and gives **48px character → about 68px canvas** as its example. A local decode of completed MCP artifacts confirmed that behavior: a standard-mode request with the default 48px character produced **68x68 RGBA** direction PNGs. Separate v3 requests at size 48 produced **84x84** and **92x92** canvases, demonstrating why an observed canvas dimension must not become a replay requirement.

The blueprint therefore keeps `create_character.size=48` as the MZ-optimized PixelLab master request, records the actual returned canvas only as run evidence, removes only fully transparent margins, and packages from nonzero-alpha content bounds into the independently resolved `CW` x `CH` target. It requires one consistent returned source canvas across the approved rotations and animation frames, computes one global nearest-neighbor scale from the maximum union width and maximum union height, never upscales, and adds only transparent padding to reach the exact RPG Maker cell. A larger PixelLab canvas is accepted; mismatched source dimensions stop packaging instead of silently producing a misaligned sheet.

## Other blueprint decisions

- PixelLab creates four cardinal rotations first. A user checkpoint then offers **Continue animating**, **Regenerate character**, or **Stop here**. Regeneration is an additional paid creation and therefore gets its own cost gate; continuing uses the already-approved animation jobs.
- PixelLab directions map explicitly to XP–MZ engine rows: south→Down row 1, west→Left row 2, east→Right row 3, north→Up row 4.
- XP retains the four returned walk frames in columns 1–4. For the three-frame engines, column 2 is the reviewed static rotation/standing pose and columns 1 and 3 are a visually verified pair of opposing stride poses kept in chronological order.
- XP packaging verifies that the returned four-frame animation remains a clean loop across the 4→1 seam. PixelLab documents the template frame count but not the gait phase assigned to each returned index.
- Normalization uses a shared crop, one global nearest-neighbor scale, a stable horizontal center, and a common foot baseline; fitting each frame independently would introduce visible jitter.
- VX through MZ receive the `$` single-character form because it is smaller and unambiguous. `!` is not added because a normal walking character should keep the engine's usual vertical offset and bush behavior.

## Sources

- [EasyRPG media-file format specifications for RPG Maker 2000/2003](https://wiki.easyrpg.org/development/rtp-replacement/media-file-format-specifications)
- [Makerpendium CharSet geometry, direction order, and standing column](https://makerpendium.de/wiki/CharSet)
- [RPG Maker XP material standards](https://rpgmakerofficial.com/product/products/rpgxp/material/index.html)
- [RPG Maker VX material standards](https://rpgmakerofficial.com/product/products/rpgvx/material/index.html)
- [RPG Maker VX Ace help: resource standards](https://www.rpgmaker.fixato.org/Manual/RPGVXAce/rpgvxace/6100_resource.html)
- [RPG Maker MV feature comparison: VX Ace 32x32 to MV 48x48](https://rpgmakerofficial.com/product/mv/new_function/02.html)
- [RPG Maker MV help: asset standards](https://rpgmakerofficial.com/product/MV_Help/page/01_11_01.html)
- [RPG Maker MZ help: asset standards](https://rpgmakerofficial.com/product/MZ_help-en/01_11_01.html)
- [Official charset structure and playback guide](https://www.rpgmakerweb.com/blog/charsets-structure-and-avoiding-traps)
- [RPG Maker Unite character image-material standards](https://rpgmakerunite.com/en/article/15136543947417/)
- [RPG Maker Unite Resource Manager character settings](https://rpgmakerunite.com/en/article/9570339256473/)
- [RPG Maker Unite field-character file layout and naming](https://rpgmakerunite.com/en/learn/002_eng.html)
- [PixelLab MCP character-tool documentation](https://api.pixellab.ai/mcp/docs)
