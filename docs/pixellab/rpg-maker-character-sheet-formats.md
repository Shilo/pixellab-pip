# RPG Maker map-character sheet formats

Character-size support and blueprint overrides rechecked October 20, 2026; the broader format matrix was originally checked July 30, 2026. This document covers the Windows RPG Maker map-character formats from RPG Maker 2000 through MZ plus RPG Maker Unite. It separates engine requirements from familiar RTP defaults. A size labeled **flexible** is computed from the imported image or configured in the editor; the listed conventional size is not an engine limit.

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

The recipe accepts three user choices:

- `RPG Maker version`, with no default. If the version was not supplied or confidently inferred from the current request and relevant context, the agent asks the user to choose XP, VX, VX Ace, MV, or MZ. This validated export-profile enum is not image-prompt text; it selects cell defaults plus the engine's sheet geometry, frame semantics, and filename rules.
- `character`, default **bald unisex chibi base character, plain skin-tone body**. The description stays intentionally minimal; v3 handles direction generation and visual treatment.
- Optional `size`. This is the size of one exported character frame/cell, including its transparent padding. A single positive integer such as `128` means `128x128`; `WxH` supplies rectangular dimensions. Both `x` and `×`, optional whitespace, and `px` units are accepted. Use a size supplied or confidently inferred from the request and relevant context; otherwise infer the version's conventional size. Malformed or unsupported values are reported rather than silently replaced with a default.

The recipe's first TASK states the sizing rules used to resolve cell width `CW` and height `CH` before preflight. These conventional sizes apply only when the request and context establish no other size:

| Resolved version | Default PixelLab `size` | Default export cell | Default output |
|---|---:|---:|---|
| XP | 48 | 32x48 | 4x4 = 128x192 |
| VX | 32 | 32x32 | 3x4 = 96x128 |
| VX Ace / VXAce | 32 | 32x32 | 3x4 = 96x128 |
| MV | 48 | 48x48 | 3x4 = 144x192 |
| MZ | 48 | 48x48 | 3x4 = 144x192 |

The official XP and VX material standards explicitly allow arbitrary character sizes; the VX Ace product page confirms that VX graphic formats carry over unchanged. The MV and MZ manuals call 48x48 the normal size while allowing it to change freely. The official charset guide also confirms that cells may be rectangular. These are image-slicing rules, not requirements to match the map tile size.

Version continues to control column count, playback, standing-frame treatment, and filename when size changes. XP exports `4*CW` by `4*CH`; VX through MZ export `3*CW` by `4*CH` and retain the `$` prefix. For example:

| Request settings | Export cell | PixelLab `size` | Sheet |
|---|---:|---:|---:|
| `MZ, size 128` or `MZ, size 128x128` | 128x128 | 128 | 384x512 |
| `MZ, size 64x128` | 64x128 | 128 | 192x512 |
| `XP, size 128` | 128x128 | 128 | 512x512 |

The blueprint uses ordinary placeholders and the existing contextual inference step, with no conditional default or `map:` modifier. Its TASK rules determine `{{character generation size in pixels}}` as the numeric value `max(32, CW, CH)` and `{{character sheet filename}}` from the version before preflight. These are inferred tool/output values, not extra questions for the user. The lower bound comes from the current v3 from-scratch generator, not the RPG Maker engine: smaller export cells use a 32px source and the existing shared downscale. The route currently supports a generation size up to 256px; a requested cell with a greater dimension stops before spending and is reported as a PixelLab route limit. The recipe does not silently clamp the request or switch routes. An unqualified `size` always means one cell; an explicitly requested whole-sheet size must not be mistaken for that cell size.

Neither version nor size options are interpolated into `create_character.description`. That field is exactly the resolved `character` wording after request framing and these options are removed; engine-specific knowledge remains in deterministic packaging TASKs.

## PixelLab source canvas versus RPG Maker cell size

PixelLab's MCP `create_character.size` is a source-generation control, separate from the exact RPG Maker export cell. The current MCP docs distinguish modes: standard mode adds roughly 40% canvas space; v3 from scratch sends the requested square size to the sprite generator, while reference-mode size is advisory. The REST v3 schema documents a 32-256px from-scratch range. Returned dimensions still need to be inspected, and animation may use a larger canvas.

Historical runs illustrate why source size must not become a returned-canvas guarantee: a standard-mode request at size 48 produced 68x68 RGBA direction PNGs, and separate v3 requests at size 48 produced 84x84 and 92x92 canvases. Those observations remain run evidence rather than replay requirements.

The blueprint uses the inferred numeric generation size, records each returned canvas only as run evidence, removes only fully transparent margins, and packages from nonzero-alpha content bounds into the resolved cell. Packaging bottom-centers the cropped poses, computes one global nearest-neighbor scale from the greatest cropped pose width and height across the delivered poses, never upscales, and adds only transparent padding to reach the exact RPG Maker cell. Rectangular cells use the same shared fit without stretching the character.

Larger size also affects paid usage. The default-size chain remains approximately six generations, but that is not a flat price for every cell size. The current v3 from-scratch formula is `1 + ceil(S*S*8/65536)` for source size `S`; template animations can use multiple billable batches per direction on larger canvases. Preflight therefore estimates creation and all four directional jobs using current tool descriptions or official MCP docs and shows the cell and sheet dimensions before approval. A regeneration is costed at the selected source size too.

## Other blueprint decisions

- PixelLab creates four cardinal rotations first. A user checkpoint then offers **Continue animating**, **Regenerate character**, or **Stop here**. Regeneration is an additional paid creation and therefore gets its own cost gate; continuing uses the already-approved animation jobs.
- PixelLab directions map explicitly to XP–MZ engine rows: south→Down row 1, west→Left row 2, east→Right row 3, north→Up row 4.
- XP retains the four returned walk frames in columns 1–4. For the three-frame engines, column 2 is the reviewed static rotation/standing pose and columns 1 and 3 are returned walk frames 02 and 04, pinned rather than rediscovered per run; see the phase-to-index mapping below.
- XP packaging verifies that the returned four-frame animation remains a clean loop across the 4→1 seam. Because returned frames 01 and 03 share the neutral phase, XP columns 1 and 3 legitimately resemble each other; the XP duplicate check targets a stalled gait between adjacent frames, not that similarity.
- Normalization uses a shared crop, one global nearest-neighbor scale, a stable horizontal center, and a common foot baseline; fitting each frame independently would introduce visible jitter.
- VX through MZ receive the `$` single-character form because it is smaller and unambiguous. `!` is not added because a normal walking character should keep the engine's usual vertical offset and bush behavior.

## `walking-4-frames` phase-to-index mapping

The `walking-4-frames` template assigns a **stable pose phase to each returned frame index**, verified across every local run of this blueprint that reached the animation step: 14 runs, 56 direction-rows, character sizes 32 and 48, many different characters. PixelLab documents the template's frame count but not this mapping, so it is an observed property of the current template, not a published contract.

The sample is mixed in `create_character` mode. Seven of the fourteen runs record `standard` and one records `v3`; the remaining six record no mode. That is worth stating because the blueprint now emits only `v3`. It does not undermine the mapping: frame phase is a property of the `animate_character` template call, and every manifest that records one records `walking-4-frames` with `ai_freedom: 0`.

| Returned index | Saved file | Pose |
|---|---|---|
| 0 | `01.png` | legs together, neutral standing |
| 1 | `02.png` | stride extreme A |
| 2 | `03.png` | legs together, neutral standing |
| 3 | `04.png` | stride extreme B, opposite leg |

The template therefore already matches the three-column RPG Maker layout one-to-one: **movement, standing, movement** corresponds to frames 2, (1 or 3), 4. The two discarded frames are the two neutral poses, which is why discarding them costs no gait information.

Visual confirmation is unambiguous in both view types. Side views show frames 1 and 3 with feet together and frames 2 and 4 mid-stride; front and back views show frames 1 and 3 square-stanced and frames 2 and 4 leaning with one leg crossing.

**The evidence is visual, and no cheap pixel metric reproduces it reliably.** Five were tried against all 56 rows and every one of them inverts on some rows:

| Metric | Result |
|---|---|
| Foot-region bounding-box width | No discrimination. Per-run averages 20.1 / 15.6 / 11.5 px for frames 1 and 3 against 20.6 / 17.2 / 11.9 for 2 and 4. |
| Sprite height | No discrimination. Differences 0–3 px; 22 of 56 rows tie outright. |
| Foot-centroid horizontal displacement | Too noisy. 50 of 56 rows separate the candidate pairs by under 1 px. |
| Interior leg gap between the feet | Strong in most side rows but not general. Inverts where a prop hangs between the legs — a katana scabbard cost one run its signal — and inverts by construction in front and back views, where a square stance leaves a gap that a stride closes by projection overlap. |
| Pairwise frame difference, `d(02,04) > d(01,03)` | Holds in 26 of 28 side rows and 27 of 28 front rows, but run-7 west inverts at a ratio of 0.92 and several rows sit within 5% of the boundary. |

An inversion rate around 7% on the best of these is far too high to serve as an automated guard, and a run that trips it is far more likely to be metric noise than an actual phase shift. The mapping itself is not in doubt — rendered side-view and front-view contact sheets of all fourteen runs show it without ambiguity — but establishing it took direct inspection, not a threshold.

That asymmetry is the reason the blueprint pins the indices instead of computing them. The three-column profiles take returned frame 02 for column 1 and 04 for column 3 and discard 01 and 03, so a replay reproduces the same sheet rather than re-deriving the pair. The remaining check is a qualitative guard, deliberately not a numeric one: it asks whether the two frames show opposite legs leading.

That guard has to tolerate being unable to answer. A five-profile test run found the legs completely hidden by a knee-length dress on one character and a floor-length cloak on another, so the check could not be performed at all — while a third character's high-contrast boots made it trivial at the same 32px size. Occlusion, not sprite size, is what decides legibility. The guard therefore records an inconclusive result and proceeds with the pinned mapping; only a clear reversal in both the west and east frames stops packaging, and it never substitutes another pair on its own.

## Sources

- [EasyRPG media-file format specifications for RPG Maker 2000/2003](https://wiki.easyrpg.org/development/rtp-replacement/media-file-format-specifications)
- [Makerpendium CharSet geometry, direction order, and standing column](https://makerpendium.de/wiki/CharSet)
- [RPG Maker XP material standards](https://rpgmakerofficial.com/product/products/rpgxp/material/index.html)
- [RPG Maker VX material standards](https://rpgmakerofficial.com/product/products/rpgvx/material/index.html)
- [RPG Maker VX Ace product page: unchanged VX graphic formats](https://rpgmakerofficial.com/product/products/rpgvxace/index/index.html)
- [RPG Maker VX Ace help: resource standards (archived)](https://web.archive.org/web/20250710042541/https://rpgmaker.fixato.org/Manual/RPGVXAce/rpgvxace/6100_resource.html)
- [RPG Maker MV feature comparison: VX Ace 32x32 to MV 48x48](https://rpgmakerofficial.com/product/mv/new_function/02.html)
- [RPG Maker MV help: asset standards](https://rpgmakerofficial.com/product/MV_Help/page/01_11_01.html)
- [RPG Maker MZ help: asset standards](https://rpgmakerofficial.com/product/MZ_help-en/01_11_01.html)
- [Official charset structure and playback guide](https://www.rpgmakerweb.com/blog/charsets-structure-and-avoiding-traps)
- [RPG Maker Unite character image-material standards](https://rpgmakerunite.com/en/article/15136543947417/)
- [RPG Maker Unite Resource Manager character settings](https://rpgmakerunite.com/en/article/9570339256473/)
- [RPG Maker Unite field-character file layout and naming](https://rpgmakerunite.com/en/learn/002_eng.html)
- [PixelLab MCP character-tool documentation](https://api.pixellab.ai/mcp/docs)
- [PixelLab REST v2 OpenAPI: CreateCharacterV3Request and V3OutputImageSize](https://api.pixellab.ai/v2/openapi.json)
