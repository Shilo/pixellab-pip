# Skill Icon Generation With generate-image-v2

Use this reference for PixelLab requests for skill icons, ability icons, spell icons, action-bar icons, or hotbar icons.

## Default Route

Use REST v2 `POST /generate-image-v2` first for complete/backgrounded skill icon sheets.

Do not default to:

- Object generation
- `create-image-pixen`
- `create_tiles_pro`
- `generate-ui-v2`
- `create-ui-asset`

Use UI routes only when the user asks for the slot, button, panel, bar, container, or action-bar frame itself.

## Canvas Sizing

For plural or complete skill-icon sets, treat `32x32 icons` as the per-icon cell size, not the output canvas.

- `8x8` or `64` icons at `32x32` each means `image_size: { "width": 256, "height": 256 }`.
- `4x4` or `16` icons at `32x32` each means `image_size: { "width": 128, "height": 128 }`.
- A `32x32` `image_size` is only appropriate for one single icon.

Generate the sheet first, then crop or split locally only if separate PNG files are needed. Local splitting is allowed because it does not create or repaint requested art.

## Prompt Pattern

For complete sheets, preserve sheet language. Do not rewrite the request as separate standalone generated images unless the user explicitly asks for separate generated files.

Use this pattern:

```text
A complete 8 by 8 sheet of 64 unique fantasy RPG skill icons for game UI. Exact canvas 256x256 pixels. 8 columns and 8 rows, each icon exactly one 32x32 square, perfectly aligned, edge-to-edge, no spacing, no overlap, no cropped icons. Pixel art, cohesive high fantasy theme, readable at 32x32.

Each icon is a finished opaque square with a rich full-bleed illustrated miniature background behind the skill symbol. Backgrounds should be high quality: luminous gradients, painterly pixel texture, depth, magical light, atmospheric color variation, not flat solid color. Background art touches all four edges and corners, and touches neighboring artwork directly. Invisible grid only; do not draw the grid. Every pixel painted; no transparent pixels, no alpha, no blank corners, no padding.

Pictorial symbols only. Use clear centered pictures and silhouettes: flames, ice shards, lightning bolts, shields, hands, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, weapons, masks, potions, celestial beams, aura effects. Do not use runes or glyphs. No text-like marks, letters, words, numbers, labels, captions, handwriting, decorative script, fake writing, or alphabet-like shapes.

Unique varied abilities: elemental magic, weapon attacks, healing, protection, stealth, curses, nature magic, summoning, movement, utility, crafting, survival, resurrection, treasure sense, mind, time, gravity, poison, holy, shadow, blood, mana, rage, tracking, alchemy, lockpicking, leadership, taunt, cleanse, traps, phoenix, dragon breath. No terrain tiles, map tiles, or inventory item sheet. No borders, frames, UI slots, rounded corners, dividers, watermark, black outlines around icon square edges, or separating lines. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.
```

For themed sheets, adapt the ability list and palette but keep the sheet/canvas/background/text/border clauses.

## Required Keywords

Use these phrases when the user asks for backgrounded skill icons:

- `Pictorial symbols only`
- `Use clear centered pictures and silhouettes`
- `rich full-bleed illustrated miniature background`
- `luminous gradients`
- `painterly pixel texture`
- `depth`
- `magical light`
- `atmospheric color variation`
- `not flat solid color`
- `Every pixel painted`
- `Fully opaque`
- `No transparent pixels, no alpha, no blank corners, no padding`
- `No borders, frames, UI slots, rounded corners, dividers, watermark`
- `No black outlines around icon square edges`
- `No separating lines`
- `Invisible grid only`
- `Background artwork touches neighboring artwork directly`

## Avoid

Avoid positive or unqualified mentions of these terms unless the user explicitly wants them:

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

Use `Do not use runes or glyphs` only as a negative clause. Positive `rune`, `glyph`, or `sigil` concepts can create text-like marks.

Avoid these phrases for complete sheets unless the user explicitly asks for separate generated files:

- `Each generated image is one standalone square icon`
- `one icon per image`
- `no overlapping multiple icons in one image`
- `standalone icon`

Those phrases can push isolated symbols on flat/simple backgrounds instead of a cohesive rich sheet.

## Request Body

Use this shape for the winning route:

```json
{
  "description": "<optimized complete-sheet prompt>",
  "image_size": {
    "width": 256,
    "height": 256
  },
  "no_background": false
}
```

Use a seed only when reproducibility or comparison is useful.

## Verification

Verify before calling the output final:

- Dimensions match the requested sheet size.
- Sheet divides exactly into requested cell dimensions.
- Alpha is fully opaque when backgrounded/no transparency is requested.
- Cropped cells are pixel-hash-unique when uniqueness is required; this does not prove semantic uniqueness.
- Human visual check confirms semantic variety.
- Human visual check finds no text-like marks.
- Human visual check finds no borders, frames, gutters, rounded corners, or slot styling.
- Central symbols are readable at 32px.

Metadata is not enough for border detection. A 1px dark edge can be fully opaque and structurally valid while still violating the art request.
