# Skill Icon Generation With generate-image-v2

Use this reference for PixelLab requests for skill icons, ability icons, spell icons, action-bar icons, or hotbar icons.

Prompts such as `generate 32px skill icon set`, `ability icons for this skill tree`, or `spell/action-bar icon sheet` classify as `create asset` + `skill_icon`. Read this reference before generating, including when the user also asks for no background, no border, or a theme tied to a skill tree.

## Default Route

Use REST v2 `POST /generate-image-v2` first for complete/backgrounded skill icon sheets.

If the user explicitly asks for cheap, low-cost, budget, or minimum credits, read `cost-routing.md` before spending credits. `generate-image-v2` is a Pro-family route and can be the best quality route for finished sheets, but a cheap request should get a lower-cost Pixen/`new` comparison, a smaller test, or an explicit cost/quality confirmation before a full Pro sheet.

Do not default to:

- Object generation
- `create-image-pixen`
- `create_tiles_pro`
- `generate-ui-v2`
- `create-ui-asset`

Use UI routes only when the user asks for the slot, button, panel, bar, container, or action-bar frame itself.

## Single Skill Icons

For a single skill, ability, spell, action-bar, or hotbar icon, prefer REST v2 `POST /generate-image-v2` when the user wants the highest-quality icon-art route or wants several candidates to choose from. At `32x32`, `generate-image-v2` may return a multi-candidate result because small output sizes produce batches; present those as candidates and select/package one only after visual review.

Use REST `create-image-pixen` only when the user explicitly values a cheap single-icon attempt, exact low-detail/outline/view controls, or fast iteration over candidate variety. Pixen can produce crisp symbols, but verify that the result still reads as a skill/ability icon rather than a simple inventory item, flat silhouette, rune-like mark, or unclear pictogram.

## Backgroundless / Transparent Icons

Complete/backgrounded skill icon sheets are the validated default. Transparent/backgroundless skill icons are a separate, less-validated request shape: when the user clearly asks for them, start with `generate-image-v2` plus `no_background: true` as a candidate, remove background and opacity prompt wording, and verify alpha, layout, borders, and 32px readability before calling it final.

If the user requests transparent icons or icons without backgrounds:

- Propose a single comparison test before a large batch when that would save credits.
- Use `no_background: true` when the user clearly wants a transparent result.
- Remove background, opacity, full-bleed painted-background, and canvas-size clauses from the prompt. Let `no_background` and `image_size` carry those controls.
- Verify the original PixelLab output for alpha, symbol clarity, grid sizing, per-cell size, and absence of unwanted borders/frames before calling the result final.
- If the original output has wrong symbol scale, a collapsed layout, border artifacts, text, poor readability, or backgrounds that are not safely separable from the icon art, report the failure against the original output. Do not silently repair those issues locally and claim success.

If `no_background: true` was sent but PixelLab returns an otherwise valid image with a background, read `background-removal.md` and apply safe background removal when it can preserve symbol/effect pixels and readability.

## Canvas Sizing

For plural or complete skill-icon sets, treat `32x32 icons` as the per-icon cell size, not the output canvas.

- `8x8` or `64` icons at `32x32` each means `image_size: { "width": 256, "height": 256 }`.
- `4x4` or `16` icons at `32x32` each means `image_size: { "width": 128, "height": 128 }`.
- A `32x32` `image_size` is only appropriate for one single icon.

Generate the sheet first, then verify the original PixelLab output against the requested cell size. If the user asked for `32px icons` and the original output contains 64px-ish symbols, a collapsed 2x2 layout, gutters that change the cell math, or a sheet that cannot divide into the requested 32px cells, report failure rather than resizing or reassembling it into a claimed final asset.

Crop or split locally only for inspection, packaging, or separate files when it preserves original pixels. Report those files as crops/splits of the original output, not as a repaired final sheet.

## Prompt Pattern

For complete sheets, preserve sheet language. Do not rewrite the request as separate standalone generated images unless the user explicitly asks for separate generated files.

Build a concise, content-focused description. Do not include generic operation language like `create this image` or `the final image should`. Avoid redundant metadata already supplied as JSON/tool parameters: do not say canvas size when `image_size` is set, and do not say transparent background when `no_background` is set. Use a single compact prompt string unless readability truly requires line breaks.

Use this backgrounded-sheet pattern as a starting point:

```text
Complete 8 by 8 sheet of 64 unique fantasy RPG skill icons for game UI, 8 columns and 8 rows, each cell a readable 32x32 icon, perfectly aligned edge-to-edge with no spacing, overlap, cropped icons, dividers, or drawn grid. Rich full-bleed illustrated miniature backgrounds behind clear centered pictorial symbols: flames, ice shards, lightning bolts, shields, hands, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, weapons, masks, potions, celestial beams, and aura effects. No text, letters, words, numbers, labels, captions, handwriting, decorative script, fake writing, runes, glyphs, or alphabet-like shapes. Varied abilities across elemental magic, weapon attacks, healing, protection, stealth, curses, nature, summoning, movement, utility, crafting, survival, resurrection, treasure sense, mind, time, gravity, poison, holy, shadow, blood, mana, rage, tracking, alchemy, lockpicking, leadership, taunt, cleanse, traps, phoenix, and dragon breath. No terrain tiles, map tiles, inventory sheet, borders, frames, UI slots, rounded corners, watermark, black square-edge outlines, or separating lines. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.
```

For backgroundless sheets, adapt the same structure but remove background and opacity clauses. Keep the pictorial-symbol, no-text, no-border, sheet-layout, and per-cell-size clauses.

For themed sheets, adapt the theme phrase, ability list, and palette but keep the sheet layout, text, and border intent. Include background intent only when it is not already represented by structured fields such as `no_background`. Do not switch themed sets to standalone 32x32 generations just because every icon shares a theme; a complete `256x256` sheet with `8x8` 32px areas produced a better cohesive painted skill-sheet result than generating separate standalone 32x32 fire icons.

Use a dense, concise list of distinct themed abilities when variety matters. Keep the prompt under the `generate-image-v2.description` limit; a successful fire-magic sheet used a 1994-character description, `image_size: { "width": 256, "height": 256 }`, and `no_background: false`.

Text should appear in icons only when the user explicitly requests text. By default, skill icons should use pictorial symbols and silhouettes, not marks that could be read as words, letters, numbers, labels, fake writing, runes, glyphs, or UI captions.

## Prompt Anchors

Use these as optional anchors for backgrounded skill icons. Choose only phrases that materially support the user's request, the selected endpoint, or a known failure mode; do not paste the whole list into every prompt.

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

For backgroundless icons, use only the relevant content/layout/text/border anchors. Do not add background or opacity phrases that conflict with `no_background: true`.

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

For backgroundless attempts, set `no_background: true` and keep `description` focused on the sheet contents, cell layout, pictorial symbols, no text, and no borders. Do not repeat `transparent background` or canvas dimensions in the description when those are supplied by structured fields.

## Verification

Verify before calling the output final:

- Original PixelLab output dimensions match the requested sheet size.
- Original PixelLab output divides exactly into requested cell dimensions.
- `32px icons` are evaluated as 32px per icon/cell, not as the whole sheet size.
- Symbols fit the requested cell scale; 64px-ish symbols or collapsed 2x2-style layouts fail a 32px icon-set request.
- Alpha is fully opaque when backgrounded/no transparency is requested.
- Alpha is transparent/backgroundless when `no_background: true` was requested.
- If background removal was applied after a `no_background: true` request, it passed `background-removal.md` verification.
- Cropped cells are pixel-hash-unique when uniqueness is required; this does not prove semantic uniqueness.
- Human visual check confirms semantic variety.
- Human visual check finds no text-like marks unless the user explicitly requested text.
- Human visual check finds no borders, frames, gutters, rounded corners, or slot styling.
- Central symbols are readable at 32px.
- Any local crops, splits, previews, or format conversions preserve original pixels and are labeled as derivatives of the original PixelLab output.

Metadata is not enough for border detection. A 1px dark edge can be fully opaque and structurally valid while still violating the art request.

If the original PixelLab output fails required size, layout, border, text, or readability checks, report it as a failed candidate and ask how to proceed. Do not resize, reassemble, or otherwise post-process it into a claimed final asset unless the user explicitly approves that repair path. The only default exception is safe background removal after `no_background: true`, following `background-removal.md`.
