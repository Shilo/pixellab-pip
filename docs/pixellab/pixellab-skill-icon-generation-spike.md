# PixelLab Skill Icon Generation Spike

Last reviewed: 2026-06-29.

Purpose: capture live-generation findings for fantasy RPG skill icon and item icon requests so `pixellab-pip` can route future "skill icon", "ability icon", "spell icon", "action bar icon", and similar requests with better defaults.

This spike is based on live PixelLab generations and human visual review. The current human-ranked winner remains REST v2 `POST /generate-image-v2` ("Create S-XL image (Pro)") for complete 8x8 finished skill icon sheets. Two `generate-image-v2` prompt variants are close co-winners for different reasons: the original strict-grid prompt has the most authentic RPG hotbar/icon-sheet punch, while the later rich-background prompt reduces some border pressure and improves explicit background guidance.

## Target Asset Definition

A finished skill icon sheet means:

- A structured grid, usually 8x8 for 64 icons.
- Each icon is exactly one 32x32 cell when the user asks for 32px icons.
- For plural or complete skill-icon requests, `32x32 icons` means per-icon cell size, not a 32x32 output canvas. For 64 icons, generate one 256x256 sheet with an 8x8 grid, then crop or split locally only if separate files are needed.
- Full colorful illustrated background in every cell.
- A large, readable central pictorial symbol.
- No text, labels, letters, numbers, fake writing, runes, or glyph-like marks.
- No transparency.
- No borders, frames, UI slots, rounded corners, gutters, or decorative dividers unless the user explicitly asks for them.

The last point is important: downstream users can add borders in their game UI. PixelLab should produce clean borderless art by default.

## Current Recommendation

Use REST v2 `POST /generate-image-v2` first when the user asks for a complete finished skill icon sheet, especially an 8x8 or 64-icon sheet.

Do not describe this route as Pixen or Pixen-style. Pixen is the separate REST `create-image-pixen` route evaluated below, and it is not the default for finished skill icon sheets.

Why:

- It produced the strongest human-rated result in this spike.
- It produced the two best human-rated outputs, for different aesthetic tradeoffs.
- It generated the full 8x8 sheet in one call.
- It created full colorful backgrounds.
- The foreground symbols were extremely clear and readable.
- It produced a consistent set with useful symbol variety.
- It returned an exact 256x256 opaque image for an 8x8 sheet of 32px cells.

Known downside:

- It tends to add a visible 1px dark border/card-slot treatment around each icon even when instructed not to. Future prompts should emphasize "borderless art only", "no black outline around cell edges", "no separating cell lines", and "background continues to cell edges".
- The likely cause is training-prior vocabulary: `skill icons`, `game UI`, `strict grid`, `cell`, and `spritesheet` often imply action-bar slots. However, `game UI` and strict sheet language also help create the authentic, high-contrast RPG icon look. Treat this as a tradeoff, not a simple ban.

Current ranking:

| Rank | Route | Result |
|---:|---|---|
| 1A | REST `generate-image-v2`, rich-background prompt | Best match to the stated no-border/no-frame constraints; richer explicit background direction and slightly softer border behavior, but less of the classic hotbar punch. |
| 1B | REST `generate-image-v2`, original strict-grid prompt | Best authentic RPG icon-sheet feel, punchy colors, and strong symbol clarity, but the most obvious visible dark slot/card edge. |
| 2 | REST `generate-ui-v2` | Right general idea and colors, but too noisy/downscaled, lower 32px clarity, rounded/background-slot feel, and some text-like noise. |
| 3 | MCP `create_ui_asset` with 64 pieces | Clean structure and semantic labels, but poor consistency for pure icons because it strongly creates framed UI buttons/slots. |
| Fallback | MCP `create_tiles_pro` plus optional sheet edit | Interesting for 4x4 tile-like icon batches, but not the best route for finished 8x8 skill icon sheets. |

Use `create_tiles_pro` as an experimental alternative when the user wants a tile-like set or when Pro image generation keeps failing semantic style, but do not treat it as the default for finished skill icon sheets yet.

## Prompting Rules Learned

Use these phrases for skill icon prompts:

- `Pictorial symbols only`
- `Use clear centered pictures and silhouettes`
- `Do not use runes or glyphs`
- `No text-like marks`
- `No letters, no words, no numbers, no labels, no captions, no handwriting, no decorative script, no fake writing, no alphabet-like shapes`
- `Every pixel must be painted`
- `Fully opaque`
- `No transparent pixels, no alpha, no blank corners, no padding`
- `No borders, no frames, no UI slots, no rounded corners, no gutters, no decorative dividers`
- `No black outline around each cell`
- `No separating lines between icons`
- `Invisible grid only`
- `Do not draw separator lines, seams, perimeter strokes, boxes, card edges, icon slots, frames, borders, or outlines around square areas`
- `Background artwork must reach all four edges and all four corners and touch neighboring artwork directly`

Avoid positive or unqualified mentions of these phrases unless the user explicitly wants them:

- `rune`
- `glyph`
- `sigil`
- `spellbook labels`
- `numbered icon labels`
- `UI slot`
- `button`
- `frame`
- `border`
- `card`

Use with caution:

- `game UI` gives desirable authentic icon-sheet punch, but can increase slot/card-edge behavior.
- `spritesheet`, `strict grid`, and `cell` improve alignment and classic sheet feel, but can increase visible per-cell borders.
- `Borderless spritesheet mosaic` can reduce hard grid/card behavior, but it flattened backgrounds in the trial; treat it as experimental rather than a default phrase.
- `Each generated image is one standalone square icon`, `one icon per image`, or `no overlapping multiple icons in one image` should be used only when the user explicitly wants separate generated files. For complete sheets, this wording can push the model toward isolated symbols on flat/simple backgrounds instead of a cohesive rich 8x8 sheet.

Even negative mentions of `rune`, `glyph`, and `sigil` helped only when paired with "do not use"; positive use of those words can drift into text-like marks.

When the user asks for backgrounded icons, preserve or add the rich-background language from the winning prompt: `rich full-bleed illustrated miniature background`, `luminous gradients`, `painterly pixel texture`, `depth`, `magical light`, `atmospheric color variation`, and `not flat solid color`.

## Route Findings

### REST `POST /generate-image-v2`

Observed as "Create S-XL image (Pro)" / generic Pro image generation.

Tested parameters:

- Endpoint: REST v2 `POST /generate-image-v2`
- `image_size`: `{ "width": 256, "height": 256 }`
- `no_background`: `false`
- Best human-ranked seed so far: `24062805`
- Rich-background near-best seed: `24062808`
- Border-reduction trial seed: `24062806`

Best use:

- Complete 8x8 skill icon spritesheets.
- Finished action-bar icon sets.
- Skill icons where readability and colorful backgrounds matter more than exact per-icon semantic uniqueness.

Canvas sizing:

- For 32px cells, compute the output canvas from the requested grid, not from the cell size.
- `8x8` or `64` icons at `32x32` each means `image_size: { "width": 256, "height": 256 }`.
- A `32x32` `image_size` is only appropriate for one single icon, not a complete set.
- Do not prompt complete sheets as standalone per-image icons unless the requested deliverable is separate files; generate the sheet first, then crop locally if separate PNGs are needed.

Pros:

- Best human-ranked route so far.
- Produced two closely ranked top outputs with different strengths.
- Clear, readable symbols.
- Full colorful backgrounds.
- Strong consistency across the sheet.
- Good mixture of skills and item-like symbols.
- Can produce an exact `256x256` sheet for 64 `32x32` cells.
- Produced fully opaque output in the winning run.

Cons:

- Tends to add a visible 1px dark border or card edge around cells.
- Repeats visual categories in practice; shields and arrows/bows dominated the seed-24062805 output, with weapons, potions, portals, and elemental effects also clustering.
- Can still hallucinate text if the prompt does not strongly ban all text-like marks.
- Single-shot sheets can obey the overall grid while not perfectly matching every requested individual skill concept.

#### Top Candidate 1B: Original Strict-Grid Prompt

Human read:

- Best for authentic RPG hotbar/icon-sheet feel.
- Appealing punchy colors and strong contrast.
- Very clear symbols and consistent icon language.
- Weakness: visible dark card/slot edge around each icon, likely because `spritesheet`, `strict grid`, `cell`, and `game UI skill icons` activate real game-icon-slot priors.

Input:

```json
{
  "endpoint": "POST https://api.pixellab.ai/v2/generate-image-v2",
  "body": {
    "description": "A complete 8 by 8 spritesheet of 64 unique fantasy RPG ability icons. Exact canvas 256x256 pixels. Strict grid: 8 columns, 8 rows, each cell exactly 32x32 pixels, no spacing, no overlap, no cropped cells. Pixel art game UI skill icons, cohesive high fantasy theme, readable at 32px.\n\nEach cell is a finished opaque square icon with a full-bleed illustrated fantasy background touching all four edges and all four corners. Every pixel must be painted. No transparent pixels, no alpha, no blank corners, no padding.\n\nPictorial symbols only. Use clear centered pictures and silhouettes: flames, ice shards, lightning bolts, shields, hands, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, weapons, masks, potions, celestial beams, aura effects. Do not use runes or glyphs. No text-like marks. No letters, no words, no numbers, no labels, no captions, no handwriting, no decorative script, no fake writing, no alphabet-like shapes.\n\nUnique varied abilities: elemental magic, weapon attacks, healing, protection, stealth, curses, nature magic, summoning, movement, utility, crafting, survival, resurrection, treasure sense. No terrain tiles, no map tiles, no inventory item sheet. No borders, no frames, no UI slots, no rounded corners, no decorative dividers, no watermark. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.",
    "image_size": {
      "width": 256,
      "height": 256
    },
    "no_background": false,
    "seed": 24062805
  }
}
```

Verification:

- Stable showcase copy: `docs/showcase/skill-icons/create-image-pro-original-strict-grid-8x8-32px.png`
- Dimensions: `256x256`
- Alpha: fully opaque. Report alpha as `alpha_min=255`, `alpha_max=255` when using 8-bit alpha, or explicitly say `normalized alpha=1.0` if using normalized tooling.
- Cropped cell hashes: 64 pixel-hash-unique cells. This proves non-identical pixel data, not semantic uniqueness.
- Usage: 20 generations
- Main issue: visible black border/card edge around each icon cell.

#### Top Candidate 1A: Rich-Background Reduced-Slot Prompt

Human read:

- Best match to the stated no-border/no-frame constraints among the top outputs.
- Better explicit background direction: luminous gradients, painterly pixel texture, depth, magical light, atmospheric color variation, not flat solid color.
- Slightly less hard-framed than the original strict-grid winner.
- Weakness: softened some of the classic installed-in-an-RPG-hotbar punch from the original.

Key prompt differences from 1B:

- Replaced `spritesheet`, `Strict grid`, and `each cell` with softer `sheet`, `icon`, and `square` wording.
- Kept `skill icons` and `game UI`, because those improve the target vibe.
- Separated `Pixel art` from the `game UI` phrase.
- Added explicit high-quality background language.
- Added more direct anti-border language: `black outlines around icon square edges` and `separating lines`.
- Expanded ability categories, including `mind`, `time`, `gravity`, `poison`, `holy`, `shadow`, `blood`, `mana`, `rage`, and utility skills.

Input:

```json
{
  "endpoint": "POST https://api.pixellab.ai/v2/generate-image-v2",
  "body": {
    "description": "A complete 8 by 8 sheet of 64 unique fantasy RPG skill icons for game UI. Exact canvas 256x256 pixels. 8 columns and 8 rows, each icon exactly one 32x32 square, perfectly aligned, edge-to-edge, no spacing, no overlap, no cropped icons. Pixel art, cohesive high fantasy theme, readable at 32x32.\n\nEach icon is a finished opaque square with a rich full-bleed illustrated miniature background behind the skill symbol. Backgrounds should be high quality: luminous gradients, painterly pixel texture, depth, magical light, atmospheric color variation, not flat solid color. Background art touches all four edges and corners. Every pixel painted; no transparent pixels, no alpha, no blank corners, no padding.\n\nPictorial symbols only. Use clear centered pictures and silhouettes: flames, ice shards, lightning bolts, shields, hands, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, weapons, masks, potions, celestial beams, aura effects. Do not use runes or glyphs. No text-like marks, letters, words, numbers, labels, captions, handwriting, decorative script, fake writing, or alphabet-like shapes.\n\nUnique varied abilities: elemental magic, weapon attacks, healing, protection, stealth, curses, nature magic, summoning, movement, utility, crafting, survival, resurrection, treasure sense, mind, time, gravity, poison, holy, shadow, blood, mana, rage, tracking, alchemy, lockpicking, leadership, taunt, cleanse, traps, phoenix, dragon breath. No terrain tiles, map tiles, or inventory item sheet. No borders, frames, UI slots, rounded corners, dividers, watermark, black outlines around icon square edges, or separating lines. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.",
    "image_size": {
      "width": 256,
      "height": 256
    },
    "no_background": false,
    "seed": 24062808
  }
}
```

Verification:

- Stable showcase copy: `docs/showcase/skill-icons/create-image-pro-rich-background-8x8-32px.png`
- Dimensions: `256x256`
- Alpha: `alpha_min=255`, `alpha_max=255`, `transparent_pixels=0`
- Cropped cell hashes: 64 pixel-hash-unique cells; semantic uniqueness still needs visual review.
- Usage: 20 generations
- Visual result: recovered richer background/gradient quality compared with the over-optimized borderless mosaic prompt, while avoiding the hardest slot-card grid of the original strict-grid output.

#### Themed Follow-up: Fire Magic Complete Sheet

Human read:

- The complete-sheet fire-magic run was a major improvement over a previous standalone 32x32 batch.
- The previous standalone batch used `image_size: { "width": 32, "height": 32 }` and "one standalone square icon" wording. It produced crisp symbols, but several icons felt like simple silhouettes, item symbols, or rune-like marks on sparse or flat backgrounds.
- The new run used one complete `256x256` 8x8 sheet and described each icon as one `32x32` square inside that sheet. It produced a more cohesive painted game-skill-sheet look with richer backgrounds.
- The strongest composition phrases were `rich full-bleed illustrated miniature background`, `background artwork touches neighboring artwork directly`, and `Invisible grid only`.
- The dense fire-specific ability list improved variety without abandoning the single-theme request.

Input:

```json
{
  "endpoint": "POST https://api.pixellab.ai/v2/generate-image-v2",
  "body": {
    "description": "A complete 8 by 8 sheet of 64 unique fantasy RPG fire magic skill icons. Exact canvas 256x256 pixels. 8 columns and 8 rows, each icon exactly one 32x32 square, perfectly aligned edge-to-edge, no spacing, no overlap, no cropped icons. Pixel art, consistent fire magic theme, readable at 32x32.\n\nEach icon is a finished Fully opaque square with a rich full-bleed illustrated miniature background behind the skill symbol. Backgrounds: luminous gradients, painterly pixel texture, depth, magical light, atmospheric color variation, not flat solid color. Background artwork touches neighboring artwork directly and touches all four edges and corners. Every pixel painted. No transparent pixels, no alpha, no blank corners, no padding.\n\nPictorial symbols only. Use clear centered pictures and silhouettes. Make all 64 abilities unique, including fireball, flame shield, meteor, phoenix wing, lava wave, burning sword, ember trap, dragon breath, volcano, scorch beam, flame pillar, ash storm, magma armor, solar flare, fire nova, blazing arrow, molten chains, salamander spirit, ignite spark, wildfire, cinder cloak, fire crown, burning skull, furnace heart, flame whip, lava hammer, sun spear, ember eye, fire portal, forge anvil, magma fist, volcanic shield, flame serpent, obsidian shard, ember rain, brazier, lava skull, firestorm spiral, pyromancer hand, flame bow, cinder bomb, smoke vortex, phoenix egg, ember wings, searing chain, heat blade, molten gauntlet, solar disk, volcanic plume.\n\nDo not use runes or glyphs. No text-like marks, letters, words, numbers, labels, captions, handwriting, decorative script, fake writing, or alphabet-like shapes. No terrain tiles, map tiles, inventory item sheet, UI slots, buttons, borders, frames, rounded corners, corner radius, dividers, watermark, decorations, black outlines around icon square edges, or separating lines. Invisible grid only. Palette: ember orange, molten gold, crimson red, charcoal smoke, blackened obsidian, hot white highlights.",
    "image_size": {
      "width": 256,
      "height": 256
    },
    "no_background": false,
    "seed": 20260629
  }
}
```

Verification:

- Stable showcase copy: `docs/showcase/skill-icons/create-image-pro-fire-magic-sheet-8x8-32px.png`
- Dimensions: `256x256`
- Alpha: `alpha_min=255`, `alpha_max=255`, `transparent_pixels=0`
- Usage: 20 generations
- Reported cost: `$0.095`
- Prompt length: 1994 characters, just under the observed `generate-image-v2.description` limit.

Lesson:

- For themed complete sets such as fire magic, keep the full-sheet route and only adapt the theme, palette, and ability list.
- Do not route to separate standalone 32x32 generations unless the user explicitly wants independently generated files.
- A dense list of concise themed ability names can improve variety, but it must be balanced against the `generate-image-v2` prompt-length limit.

Border-reduction trial:

```json
{
  "endpoint": "POST https://api.pixellab.ai/v2/generate-image-v2",
  "body": {
    "description": "Complete borderless 8x8 pixel-art spritesheet mosaic of 64 unique fantasy RPG ability pictograms. Exact canvas 256x256. Invisible grid only: 8 columns, 8 rows, each adjacent square area exactly 32x32, packed edge-to-edge, no spacing, no gaps, no overlap, no cropped art.\n\nEach 32x32 area is a full-bleed opaque miniature fantasy painting with a large clear centered ability symbol. The painted background must reach all four edges and all four corners and touch neighboring artwork directly. Do not draw the grid. Do not draw separator lines, seams, perimeter strokes, boxes, card edges, icon slots, frames, borders, outlines around square areas, or dark edge pixels along the 32x32 boundaries. Square fully painted corners, never rounded.\n\nPictorial symbols only: flames, ice, lightning, shields, hands, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, weapons, masks, potions, beams, aura effects, waves, stones, vines, eyes, chains, hearts, crowns, hammers, hooks, moons, suns. Large readable symbols, integrated into the background, not enclosed in UI.\n\nNo text, letters, words, numbers, labels, captions, handwriting, decorative script, fake writing, runes, glyphs, alphabet-like marks, watermark, transparent pixels, alpha, blank pixels. Varied abilities: elements, healing, protection, stealth, curses, nature, summoning, movement, crafting, survival, resurrection, treasure sense, weapon attacks, mind, time, gravity, poison, holy, shadow, blood, mana, rage, tracking, mining, fishing, cooking, alchemy, lockpicking, leadership, taunt, cleanse, traps, phoenix, dragon breath. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.",
    "image_size": {
      "width": 256,
      "height": 256
    },
    "no_background": false,
    "seed": 24062806
  }
}
```

Border-reduction trial verification:

- Stable showcase copy: `docs/showcase/skill-icons/create-image-pro-borderless-mosaic-8x8-32px.png`
- Dimensions: `256x256`
- Alpha: `alpha_min=255`, `alpha_max=255`, `transparent_pixels=0`
- Cropped cell hashes: 64 pixel-hash-unique cells; semantic uniqueness still needs visual review.
- Usage: 20 generations
- Visual result: reduced the obvious 1px card-grid border compared with the previous winning run, but many symbols still use dark pixel outlines and boundary-edge pixels remain darker than the sheet average. Treat this as an improvement, not a solved no-border guarantee.

### REST `POST /create-image-pixen`

Best use:

- Fast one-shot experiments for full icon sheets.
- Cases where the user wants a simpler, flatter icon style.

Tested parameters:

- Endpoint: REST v2 `POST /create-image-pixen`
- Target: one-shot 8x8, `256x256`, 64 fantasy skill icons.

Pros:

- Understood "skill icons" better than object generation.
- Produced clear central foregrounds.
- Produced unique backgrounds.
- One-call 8x8 sheet generation.

Cons:

- Added gutters/spacing.
- Added rounded dark cell shapes and implied borders.
- Foreground symbols were effectively smaller than the requested 32px cell, closer to roughly 26px.
- Backgrounds were simpler than desired.
- Less strong than `generate-image-v2` for the finished fantasy skill icon target.

### MCP `create_tiles_pro`

Best use:

- Experimental route for skill icon-like tile cells.
- Possible fallback when the user wants 16-icon batches or tile-like ability icons.
- Style exploration before a final Pro image generation prompt.

Tested parameters:

- Tool: MCP `create_tiles_pro`
- `tile_type`: `square_topdown`
- `tile_view`: `top-down`
- `tile_size`: `32`
- `outline_mode`: `segmentation`

Pros:

- Produced outputs that looked much more like actual skill icons than object generation.
- Strong icon-read at 32px after prompt optimization.
- Good high-fantasy backgrounds.
- `tile_size=32` produced exact 32x32 source tiles.
- The "pictorial symbols only" prompt reduced text-like artifacts.

Cons:

- At `tile_size=32`, one generation produced 16 variations, not 64. A full 8x8 sheet requires four jobs and local assembly.
- It is still tile-system prompted; output can inherit tile/cutout behavior.
- Raw outputs often contain transparent pixels/corners despite "no transparency" wording.
- Numbered per-tile prompts and `rune`/`glyph` language can create text-like marks.
- A full-sheet REST `edit-images-v2` pass was observed to fix opacity in one 4x4 source sheet, but verify afterward; it costs another generation batch and may not improve art quality.

Best prompt additions:

- `Pictorial symbols only`
- `Do not use runes or glyphs`
- `Every pixel must be painted`
- `Background must fill the entire 32x32 square and touch all four edges and all four corners`

### REST `POST /edit-images-v2`

Best use:

- Sheet-level cleanup after a promising generation.
- Filling transparency after `create_tiles_pro` or another route, when the source art is already good.
- Preserving a grid while fixing opacity/background fill.

Pros:

- One full-sheet pass fixed alpha in the 4x4 tiles-pro trial.
- Cheaper operationally than editing each tile independently.
- Can preserve the overall icon look while making the sheet fully opaque.

Cons:

- Does not reliably fix underlying semantic problems such as scene-heavy icons.
- Can inherit weak foreground readability from the source image.
- Can subtly alter pixels; use only when the source art is already close.

Recommendation:

- Use sheet-level edit, not per-tile edit, when the sheet is already visually good but has opacity/background issues. Treat this as observed cleanup, not a reliable rescue path; always verify opacity and visual quality afterward.

### MCP `create_1_direction_object`

Best use:

- Standalone transparent item/object icons.
- Pickups, props, inventory items, weapons, materials, furniture, and other object-like assets.

Tested parameters:

- Tool: MCP `create_1_direction_object`
- `size`: `32`
- `view`: `sidescroller`
- `item_descriptions`: 64 unique fantasy skill/icon descriptions.

Pros:

- Strong for isolated objects and item-like foregrounds.
- Good symbol silhouettes when the target can be treated as an object.
- Can produce many candidates in a review pack.

Cons for skill icon sheets:

- Object-first behavior, not GUI/skill-icon behavior.
- Produces item/object-like assets rather than finished action-bar icons.
- Tends toward transparent backgrounds unless heavily prompted otherwise.
- Background-heavy prompting overcorrected into scene-based miniatures with weak skill readability.

Recommendation:

- Do not default to this for finished skill icons.
- Use it when the user asks for transparent item icons, pickup icons, or object sprites.

### REST `POST /create-image-pixflux`, `POST /create-image-bitforge`, `POST /generate-with-style-v2`

Status:

- Not evaluated in this spike for finished skill icon sheets.

Possible future use:

- Style reference workflows if the user provides a preferred icon sheet.
- Alternative image models if `generate-image-v2` keeps adding borders.

### REST `POST /generate-ui-v2`

Status:

- Evaluated once for finished 8x8 skill icon sheets.

Tested parameters:

- Endpoint: REST v2 `POST /generate-ui-v2`
- `image_size`: `{ "width": 256, "height": 256 }`
- `no_background`: `false`
- `seed`: `24062810`
- `color_palette`: `sapphire blue, ember orange, moonlit violet, emerald green, gold`
- Prompt: same rich-background hybrid skill-icon prompt used for the latest `generate-image-v2` comparison.

Observed result:

- No stable showcase asset retained; findings are recorded from visual review and verification metadata only.
- Dimensions: `256x256`
- Alpha: `alpha_min=255`, `alpha_max=255`, `transparent_pixels=0`
- Cropped cell hashes: 64 pixel-hash-unique cells; semantic uniqueness still needs visual review.

Pros:

- Right general idea and colors.
- Strong "actual game icon sheet" feel at a glance.
- Rich color and high visual density.
- Good symbol variety.
- Boundary-edge luminance was close to sheet average in the test, suggesting it did not rely on one uniform dark grid line as heavily as some prior attempts.

Cons:

- Lacked 32px clarity; the image looked too noisy and downscaled.
- Backgrounds appeared to have rounded/button-like corners or border-radius behavior.
- Still produced small slot-border/card-edge behavior around many icons.
- Some tiny text-like or glyph-like noise appeared.
- Tended toward many small detailed icons, which can hurt clarity at 32px compared with the best `generate-image-v2` runs.

Recommendation:

- Keep as an experimental runner-up when the user wants authentic game UI icon-sheet feel.
- Do not default to it for strict no-border/no-text skill icon sheets until prompt wording is improved.

### REST `POST /create-ui-asset` and MCP `create_ui_asset`

Status:

- MCP `create_ui_asset` evaluated once for finished 8x8 skill icon sheets using 64 square `pieces` with skill labels.

Tested parameters:

- Tool: MCP `create_ui_asset`
- `width`: `256`
- `height`: `256`
- `no_background`: `false`
- `seed`: `24062809`
- `pieces`: 64 `rounded_rect` regions, each `64x64` in the virtual 512x512 editor grid, mapping to 32x32 output regions.
- `radius`: `0` on every piece.
- `label`: one skill concept per piece, such as `fireball`, `ice shards`, `lightning bolt`, `holy heal`, `shield wall`, and so on.

Observed result:

- No stable showcase asset retained; findings are recorded from visual review and verification metadata only.
- UI asset ID: `81bf98ef-4309-4c38-90a3-d39fb8d6ade3`
- Dimensions: `256x256`
- Alpha: `alpha_min=255`, `alpha_max=255`, `transparent_pixels=0`
- Cropped cell hashes: 64 pixel-hash-unique cells; semantic uniqueness still needs visual review.

Pros:

- Followed the 8x8 structure very cleanly.
- Per-piece labels improved semantic targeting compared with generic prompts.
- Symbols were readable and distinct.

Cons:

- Had poor visual consistency as a finished icon-art sheet.
- Produced weird unified borders and frames across the sheet.
- Strongly pushed the result toward framed icon buttons/slots, even with radius `0` and explicit no-border wording.
- Result felt more like a UI action-bar asset than pure borderless skill-icon art.
- Piece labels are useful as metadata, but may increase text/glyph risk unless the prompt says labels must not be drawn.

Recommendation:

- Use for action-bar slots, icon buttons, UI containers, or when per-icon label control matters more than pure borderless art.
- Do not default to MCP `create_ui_asset` for strict borderless skill icon sheets.

## Item Icon Guidance

"Item icon" is ambiguous:

- If the user wants transparent inventory objects or pickups, use MCP `create_1_direction_object` or REST object/image routes.
- If the user wants finished action-bar item icons with colorful square backgrounds, use the same skill-icon guidance as above and prefer REST `generate-image-v2`.
- If the user wants both item and skill icons in one sheet, `generate-image-v2` handled mixed symbols well in the winning run.

## Suggested `SKILL.md` Routing Update

Future `SKILL.md` guidance should distinguish:

- `skill icon`, `ability icon`, `spell icon`, `action-bar icon`, `hotbar icon`: finished UI icon art, default to REST `generate-image-v2` for complete sheets.
- `item icon` with transparent/backgroundless wording: object/icon asset, likely object route.
- `item icon` with action-bar/UI/backgrounded wording: finished icon art, default to REST `generate-image-v2`.

Draft routing rule:

> For finished skill/ability/spell/action-bar icon sheets, prefer REST `generate-image-v2` over object generation, Pixen, and tiles-pro. Use strict prompt wording for pictorial symbols only, no text-like marks, fully opaque painted cells, and no borders/frames/UI slots. Verify dimensions, alpha, grid structure, visual text artifacts, and cell-edge borders before calling the output final. Use `create_tiles_pro` only as an experimental/fallback style route, and use sheet-level `edit-images-v2` only for opacity/background cleanup on an already-good sheet.

Avoid routing finished skill icon sheets to UI routes merely because the user says `action bar` or `hotbar`; use UI routes only when the user asks for the slot/button/container itself.

## Verification Checklist

Always verify:

- Output dimensions match the requested sheet size.
- Sheet divides exactly into requested cell dimensions.
- Alpha is fully opaque when the user requests backgrounded/no transparency.
- Cropped cells are unique by hash when uniqueness is required; this checks pixel uniqueness only.
- Human visual check for semantic uniqueness when each icon must represent a distinct skill concept.
- Human visual check for text-like marks.
- Human visual check for borders, frames, gutters, rounded corners, or slot styling.
- Human visual check that central symbols are readable at 32px.

For border detection, metadata is not enough. A 1px black border can be fully opaque and structurally valid while still violating the user's art requirement.

## Open Questions

- Can prompt wording eliminate the 1px border in `generate-image-v2`, or is it a model habit for icon sheets?
- Can REST `generate-ui-v2` be prompt-optimized to remove slot-border and text-like artifacts while preserving its authentic game-icon feel?
- Can `create-ui-asset` or MCP `create_ui_asset` be coerced into borderless icon-art sheets after a first test showed strong framed icon-button behavior?
- Does `generate-with-style-v2` using the current winner as style reference preserve clarity while removing borders?
- For production 64-icon sheets, is it better to generate one full sheet, four 4x4 sheets, or individual icons when exact per-icon semantics matter?
