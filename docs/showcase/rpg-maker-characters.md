# RPG Maker Characters

Last reviewed: 2026-07-30.

<table>
  <tr>
    <td><img src="rpg-maker-characters/rpg-maker-mz-character.png" alt="RPG Maker MZ walk spritesheet, 144x192 with 48x48 cells"></td>
    <td><img src="rpg-maker-characters/rpg-maker-mz-character.gif" alt="RPG Maker MZ engine playback loop of all four directions"></td>
  </tr>
  <tr>
    <td><img src="rpg-maker-characters/rpg-maker-mv-character.png" alt="RPG Maker MV walk spritesheet, 144x192 with 48x48 cells"></td>
    <td><img src="rpg-maker-characters/rpg-maker-mv-character.gif" alt="RPG Maker MV engine playback loop of all four directions"></td>
  </tr>
  <tr>
    <td><img src="rpg-maker-characters/rpg-maker-vx-ace-character.png" alt="RPG Maker VX Ace walk spritesheet, 96x128 with 32x32 cells"></td>
    <td><img src="rpg-maker-characters/rpg-maker-vx-ace-character.gif" alt="RPG Maker VX Ace engine playback loop of all four directions"></td>
  </tr>
</table>

The same character brief — a red-haired swordsman in a black kimono with a single katana on his back — was run three times through the `rpg-maker-character` blueprint, once each for RPG Maker MZ, MV, and VX Ace. Each run produced a drop-in single-character walk sheet in that engine's own cell geometry, plus a looping playback GIF built from the finished sheet columns so the gait can be checked before the file ever reaches the editor.

The three runs are separate generations, not one sprite resized. MZ and MV share identical 48x48 export cells, and they are both shown here on purpose: the v3 character model interpreted the same words differently each time. The MZ figure is broader and more detailed — sharply spiked bright red hair, a drawn brow and nose, a visible scabbard — and fills more of its cell at 32x48 of the available 48x48. The MV figure is leaner and flatter-faced at 28x47, closer to a conventional chibi build, inside the same box. VX Ace ran at the smaller 32px character size and packs into 32x32 cells.

## Request

Every run invoked the shipped blueprint and supplied the RPG Maker version inline, so the recipe never had to stop and ask which engine to target.

### RPG Maker MZ Prompt

```text
@rpg-maker-character.blueprint.json mz, male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

### RPG Maker MV Prompt

```text
@rpg-maker-character.blueprint.json mv, male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

### RPG Maker VX Ace Prompt

```text
@rpg-maker-character.blueprint.json vx ace, male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

## Prompt Preparation

The blueprint splits each request into two independent values before any paid call runs.

The RPG Maker version is resolved case-insensitively, an optional `RPG Maker` prefix is stripped, `VXAce` normalizes to `VX Ace`, and only XP, VX, VX Ace, MV, and MZ are accepted. The version never reaches PixelLab; it only selects the request size and the export geometry. Because all three prompts named a version, none of the runs hit the blueprint's "ask the user once" branch.

The character wording keeps only the words the user wrote. Request framing and the version phrase are removed, and nothing is added — no style, age, anatomy, clothing, or equipment enhancement. Since the three prompts differ only in the version phrase, all three resolve to the identical `description`, as the three blueprints record:

```text
male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back
```

Identical input wording does not mean identical output. `v3` is unseeded, so the three sheets are independent draws from the same sentence, which is exactly why MZ and MV look like different characters despite sharing both the description and the export profile.

## Character Generation

Route: PixelLab MCP `create_character`

| Field | MZ | MV | VX Ace |
|---|---|---|---|
| Mode | `v3` | `v3` | `v3` |
| Body type | `humanoid` | `humanoid` | `humanoid` |
| Size | `48` | `48` | `32` |
| View | `low top-down` | `low top-down` | `low top-down` |
| Detail | `high detail` | `high detail` | `high detail` |
| Returned canvas (this run) | `92x92px` | `92x92px` | `64x64px` |

Size is derived from the version alone (`XP` and `MV`/`MZ` map to `48`, `VX` and `VX Ace` map to `32`), so the recipe never asks for a technical pixel value.

`create_character.size` is character size, not canvas size. PixelLab pads the canvas to leave animation room — the MCP docs describe roughly 40% larger and give 48px character → about 68px canvas as their example — but the actual returned dimension is not a stable contract. A `48` request came back on `92x92` in both runs here, while separate `v3` requests at the same size have returned `84x84`, and a standard-mode 48px request has returned `68x68`. Treat the canvas as run evidence, never as a replay requirement: packaging reads nonzero-alpha content bounds and discards the padding, so a different canvas produces the same sheet.

`v3` always returns eight rotations. Directions are mapped only from explicit trimmed, case-insensitive direction labels — never from array or response order — and this four-direction recipe keeps south, west, east, and north while ignoring the four labeled diagonals. All three runs were approved from their first candidate; no regeneration was needed.

## Walk Animation

Route: PixelLab MCP `animate_character`

| Field | Value |
|---|---|
| Mode | `template` |
| Template animation | `walking-4-frames` |
| Directions | `south`, `west`, `east`, `north` |
| AI freedom | `0` |

Template mode at `ai_freedom: 0` follows the skeleton pose rigidly, which is what keeps four separately generated directions on a shared gait. Each direction returns four frames, saved unchanged and in returned order.

## Engine Packaging

For VX through MZ, a single-character sheet is three columns wide and four rows tall. Rows are fixed as Down, Left, Right, Up (south, west, east, north) and columns run movement, standing, movement, so the engine plays column 2 → 1 → 2 → 3. XP is the exception and is covered under Engine Coverage below.

| Profile | MZ | MV | VX Ace |
|---|---|---|---|
| Cell | `48x48` | `48x48` | `32x32` |
| Sheet | `144x192` | `144x192` | `96x128` |
| Grid | `3x4` | `3x4` | `3x4` |
| Filename prefix | `$` | `$` | `$` |

None of these cell sizes is an engine limit. XP through MZ derive cell size from the imported image, so 48x48 is what RPG Maker MV and MZ document as normal and 32x32 is the VX and VX Ace convention — not a hard requirement. The blueprint pins them anyway so that a replay lands on the size the engine's own RTP art and default character scaling assume.

The three columns come from two different PixelLab calls, which is easy to miss. Column 2, the standing pose, is the reviewed static rotation produced by `create_character` — it is not an animation frame and never was. Only columns 1 and 3 come from `animate_character`.

That split is why frames get discarded. `walking-4-frames` returns four frames per direction, the layout has room for two of them, and the other two are dropped. The sheet is therefore two kept walk frames plus one static rotation, not three of the four generated frames. XP is the only supported engine that uses all four, because its 4-column layout has no standing pose to fill.

Which two survive is not arbitrary. `walking-4-frames` assigns a stable pose to each returned index: frames `01` and `03` are neutral, legs-together standing poses, and frames `02` and `04` are the two opposing stride extremes. All three runs here selected `02` and `04` and dropped `01` and `03` in every direction, and a sweep of all 14 local runs of this blueprint that reached the animation step — 56 direction-rows across character sizes 32 and 48 — found the same mapping every time. The template's own structure is already movement / neutral / movement, which is exactly the layout these engines want, so the discarded frames cost no gait information.

The evidence for that mapping is visual rather than numeric, and deliberately so. Five candidate pixel metrics were tested against all 56 rows — foot-region width, sprite height, foot-centroid displacement, interior leg gap, and pairwise frame difference — and every one of them inverts on some rows, the best still at roughly a 7% error rate. Rendered contact sheets of all fourteen runs settle it without ambiguity where the metrics cannot.

On the strength of that sweep the blueprint now pins the selection: column 1 takes frame `02` and column 3 takes frame `04`, with no per-run judgement call, so a replay is reproducible rather than dependent on an agent's reading of a contact sheet. The check survives as a guard rather than as the selection mechanism — PixelLab documents the template's frame count but not its phase-index mapping, so if a future template shifts its phases the packaging step stops and reports instead of silently shipping two near-identical standing poses. Details of the sweep, including which metrics fail to discriminate, are in [RPG Maker map-character sheet formats](../pixellab/rpg-maker-character-sheet-formats.md).

Poses are normalized only after selection. Each delivered pose is cropped to its `alpha > 0` bounds, the cropped poses in a row are aligned to one bottom-center origin, and a single nearest-neighbor scale of `min(1, cell / maxW, cell / maxH)` is applied across every delivered pose so the rows stay consistent with each other. In all three runs the largest row union fit inside the cell (`32x48` for MZ, `28x47` for MV, `21x31` for VX Ace), so the scale resolved to `1.0` and no pixels were resampled at all.

The `$` prefix is what tells RPG Maker a sheet holds one character. Without it, VX through MZ read the file as eight characters in a 12x8 cell grid, and a 3x4 sheet imported under a plain name will be sliced into the wrong poses rather than rejected. The showcase copies here drop the prefix so the filenames stay portable across shells and web paths; rename a sheet to `$name.png` before importing it. The destination differs by engine generation: MV and MZ read map characters from `img/characters`, while VX and VX Ace use `Graphics/Characters`.

The other RPG Maker filename flag, `!`, is deliberately not used. It suppresses the engine's usual upward display offset — 4 pixels on VX and VX Ace, 6 on MV and MZ — along with bush translucency, which is what you want for a door or a chest that should sit flush with the tile it occupies. A walking character should keep both behaviors, so these sheets ship without it. If a sprite looks like it is floating slightly above the tile grid, that offset is the expected engine behavior and not a packaging error.

## Engine Coverage

The blueprint targets five engines: XP, VX, VX Ace, MV, and MZ. Three are showcased here; the two that are not still replay from the same recipe.

VX is identical to the showcased VX Ace profile — 32x32 cells, 96x128, same `$` rules and same 2 → 1 → 2 → 3 playback.

XP is the one supported engine that packages differently. It is a **4x4** sheet of **32x48** cells at 128x192, it keeps all four returned walk frames in columns 1 through 4, playback runs 1 → 2 → 3 → 4 → 1, and it does **not** take a `$` prefix. Because XP has no standing column, the static rotation is unused and the loop has to close cleanly across the 4 → 1 seam, which the blueprint inspects explicitly.

RPG Maker 2000, 2003, and Unite are out of scope by design rather than oversight. 2000 and 2003 use fixed 24x32 cells in 8-bit indexed CharSets that ignore alpha entirely and order rows Up, Right, Down, Left, so they would need palette conversion and a different row mapping. Unite abandons the single-sheet model altogether: each direction is its own horizontal animation file with a 1-pixel transparent border, 2 transparent pixels between frames, and per-direction import metadata registered in Resource Manager. Neither can be reached by changing cell size or row order on this atlas.

The full format matrix, including the engines this showcase does not cover, is in [RPG Maker map-character sheet formats](../pixellab/rpg-maker-character-sheet-formats.md).

## Blueprints

Three replayable blueprints, one per engine:

- [`rpg-maker-mz-character.blueprint.json`](rpg-maker-characters/rpg-maker-mz-character.blueprint.json)
- [`rpg-maker-mv-character.blueprint.json`](rpg-maker-characters/rpg-maker-mv-character.blueprint.json)
- [`rpg-maker-vx-ace-character.blueprint.json`](rpg-maker-characters/rpg-maker-vx-ace-character.blueprint.json)

Each is the shipped `rpg-maker-character` recipe with the version pinned, so the version-selection prompt and the other engines' packaging branches are already resolved away. The three files differ only in the pinned version name, the `create_character` size, and the cell and sheet geometry in the packaging step. Blueprint excerpt — the two PixelLab calls from the MZ file, which the complete workflow surrounds with review, approval, inspection, and assembly `TASK` steps:

```json
[
  {
    "MCP create_character": {
      "body_type": "humanoid",
      "description": "male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back",
      "detail": "high detail",
      "mode": "v3",
      "size": 48,
      "view": "low top-down"
    }
  },
  {
    "MCP animate_character": {
      "character_id": "<id returned by create_character for the approved candidate>",
      "mode": "template",
      "template_animation_id": "walking-4-frames",
      "animation_name": "four-direction walk",
      "directions": ["south", "west", "east", "north"],
      "ai_freedom": 0
    }
  }
]
```

## Reproducibility Controls

| Control | Setting |
|---|---|
| Character mode | `v3`, eight rotations, four kept |
| Character size | `48` for MZ and MV, `32` for VX Ace |
| View | `low top-down` |
| Detail | `high detail` |
| Animation | `walking-4-frames` template, `ai_freedom: 0` |
| Frames per direction | `4` |
| Transparency | preserved end to end; sheets and GIFs are transparent |
| File format | PNG, which MV and MZ require and VX Ace supports with alpha |
| Scaling | nearest-neighbor only, and unused in all three runs |
| GIF timing | 12 centiseconds per frame, infinite loop, explicit disposal |

No seed was sent, so the three characters are independent draws rather than variations of one seeded result.

## Local Processing

Sheet assembly, playback GIF encoding, and the inspection grid are local steps recorded as `TASK` entries in each blueprint; PixelLab returns individual frames, not engine sheets.

The playback GIF is cut from the finished sheet, not from the raw frames. Each GIF frame is one unscaled full-height sheet column — 48 or 32 pixels wide by the full sheet height — carrying all four direction cells stacked Down/Left/Right/Up, played in engine order 2 → 1 → 2 → 3. Building it this way means the GIF cannot drift from the PNG: it is the same pixels, re-ordered.

Each run also writes an inspection grid beside the sheet, an unscaled copy at identical pixel dimensions with contrasting one-pixel lines drawn only on interior cell boundaries. It is a review aid for confirming that every pose sits inside its cell on a shared baseline; the delivered sheet is never modified.

## Validation

- Sheet dimensions match each engine profile exactly: `144x192` with `48x48` cells for MZ and MV, `96x128` with `32x32` cells for VX Ace.
- All twelve cells in each sheet are occupied; no empty pose passed through.
- Every source column uses strictly binary alpha (`0` or `255`) and stays within the GIF palette limit (118, 80, and 67 opaque colors), so each playback GIF is genuinely pixel-exact rather than a visual approximation. All four coalesced frames of all three GIFs compare identically to their source sheet columns, with zero mismatched pixels.
- GIF timing decodes as 12 centiseconds per frame with infinite looping in all three files.
- Every walk frame was inspected against the approved rotations before packaging. The MV run failed that gate on the first attempt: the north walk dropped the katana in three of its four frames, which cannot be directional occlusion since a back-mounted sword is most visible from behind. Packaging stopped, the north direction alone was deleted and regenerated with the same template call, and the replacement frames carry the sword throughout. The other three directions were untouched. The blueprint forbids repairing frames by hand or packaging a failed animation, so the sheet on this page is the post-retry result.
- Wording mismatches were reported rather than papered over, and they differ per run because the three characters are independent draws. "Spiky red hair" landed cleanly in MZ, which has sharp distinct spikes; MV read it as tousled and rounded, and VX Ace sits between the two with a soft spiked fringe. "Brown eyes" did not survive anywhere. MZ renders a legible eye, but it is pale grey rather than brown, so that run contradicts the description rather than merely failing to show it. MV's eye is a dark cluster too small to assign a hue, and VX Ace's is a single light highlight pixel. Anyone reproducing this should expect eye color below roughly 48px to be either unrenderable or unreliable, not simply invisible.

## Showcase Assets

| Asset | Path |
|---|---|
| MZ sheet | `docs/showcase/rpg-maker-characters/rpg-maker-mz-character.png` |
| MZ playback | `docs/showcase/rpg-maker-characters/rpg-maker-mz-character.gif` |
| MV sheet | `docs/showcase/rpg-maker-characters/rpg-maker-mv-character.png` |
| MV playback | `docs/showcase/rpg-maker-characters/rpg-maker-mv-character.gif` |
| VX Ace sheet | `docs/showcase/rpg-maker-characters/rpg-maker-vx-ace-character.png` |
| VX Ace playback | `docs/showcase/rpg-maker-characters/rpg-maker-vx-ace-character.gif` |
| Blueprints | `docs/showcase/rpg-maker-characters/*.blueprint.json` |
