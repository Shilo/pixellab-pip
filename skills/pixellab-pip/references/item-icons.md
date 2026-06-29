# Item Icon Generation With generate-image-v2

Use this reference for PixelLab requests for inventory item icons, equipment icons, loot icons, pickup icons, consumable icons, transparent RPG item sheets, or complete item-icon sets.

Prompts such as `32px inventory item set`, `RPG equipment icons`, `loot icon sheet`, `pickup icons`, or `all common RPG inventory items` classify as `create asset` + `item_icon`. Read this reference before generating, including when the user asks for transparent background, no border, no frame, or individual split PNGs.

## Default Route

Use REST v2 `POST /generate-image-v2` first for complete item-icon sheets.

Do not default to:

- MCP `create_1_direction_object`
- REST `create-1-direction-object`
- `create-image-pixen`
- `create_tiles_pro`
- `generate-ui-v2`
- `create-ui-asset`

Object routes are for standalone props and managed objects, not icon sheets. In testing, `create_1_direction_object` produced noisy/downscaled-looking icons, broken or inconsistent contours, incomplete outlines, artifacts, and weak 32px clarity. Avoid it whenever the user requests icons, icon sheets, inventory items for UI, or consistent game inventory artwork, even when the icon subject is a weapon, shield, potion, pickup, or prop.

Use UI routes only when the user asks for the slot, button, panel, inventory frame, item-card background, or container UI itself.

## Single Item Icons

For a single transparent inventory item icon, still avoid object generation. Prefer REST v2 `POST /generate-image-v2` when the user wants the highest-quality icon-art route or wants several candidates to choose from. At `32x32`, current `generate-image-v2` behavior may return a multi-candidate result because small output sizes produce batches; present those as candidates and select/package one only after visual review.

Use REST `create-image-pixen` only when the user explicitly values a cheap single-image attempt, exact low-detail/outline/view controls, or fast iteration over candidate variety. Pixen can produce clean contours, but verify semantic recognizability carefully.

## Transparent Icons

Inventory item icons usually need transparent backgrounds. Use `generate-image-v2` with `no_background: true` for the first real candidate.

`create-image-pixen` can be useful as a single comparison test because it exposes `detail`, `outline`, and `view`, but do not treat it as the default sheet route. In testing, Pixen had clearer contours than object generation but produced random-looking or semantically unclear items, duplicated concepts, excessive micro-colors, and sheet-layout drift where multiple shapes occupied the space of two 32px slots.

If the user asks for a large batch and credits matter, propose a single comparison test before running multiple expensive Pro candidates. If the user clearly asks to proceed, run the best Pro route and verify honestly.

## Canvas Sizing

For plural or complete item-icon sets, treat `32x32 icons` as the per-item cell size, not the output canvas.

- `8x8` or `64` icons at `32x32` each means `image_size: { "width": 256, "height": 256 }`.
- `4x4` or `16` icons at `32x32` each means `image_size: { "width": 128, "height": 128 }`.
- A `32x32` `image_size` is only appropriate for one single item icon.

Generate the sheet first, then verify the original PixelLab output against the requested cell size. Crop or split locally only for inspection, packaging, or separate files when it preserves original pixels. Report those files as crops/splits of the original output, not as repaired art.

## Prompt Pattern

For complete sheets, preserve sheet language. Do not rewrite the request as separate standalone generated images unless the user explicitly asks for separate generated files.

Build a concise, content-focused description. Avoid redundant metadata already supplied as JSON/tool parameters: do not say canvas size when `image_size` is set, and do not say transparent background when `no_background` is set. Use a single compact prompt string unless readability truly requires line breaks.

Use this transparent-sheet pattern as a starting point:

```text
Complete 8 by 8 sheet of 64 unique fantasy RPG inventory item icons, 8 columns and 8 rows, each cell a readable 32x32 item, perfectly aligned with no spacing, overlap, cropped items, dividers, or drawn grid. Pixel art with clear centered object silhouettes, crisp hard edges, low visual noise, limited palette, consistent high-fantasy inventory style. Include varied common RPG inventory categories: melee weapons, ranged weapons, shields, armor, helmets, boots, gloves, jewelry, potions, scrolls, books, maps, food, coins, gems, ores, wood, herbs, monster parts, bottles, light sources, tools, keys, chests, bags, bedrolls, bombs, arrows, elemental items, holy items, and cursed charms. No text, letters, words, numbers, labels, captions, handwriting, fake writing, runes, glyphs, UI slots, buttons, borders, frames, rounded corners, watermark, terrain tiles, map tiles, skill icons, or decorative grid lines.
```

Prefer category coverage for the first candidate. A long exact 64-item list can over-constrain the model and may produce noisier/downscaled-looking results, mixels, jagged linework, or worse pixel clarity even on the same `generate-image-v2` endpoint. If exact coverage is required, use a concise item list in a follow-up candidate and compare visually against the category-based candidate before calling it final.

Some mild stair-stepping or jagged diagonal linework may appear even in the best `generate-image-v2` item-icon candidates. Treat it as a failure only when it harms 32px readability, makes the object shape unclear, or produces noisy/mixed-resolution pixels. Do not reject an otherwise strong candidate for normal pixel-art diagonal stepping.

Do not over-prompt outline-specific instructions unless the user asks for a particular outline style. The route should naturally produce consistent readable contours. If the output has spotty, broken, incomplete, or inconsistent item contours, treat it as a failed candidate during visual review.

Text should appear in icons only when the user explicitly requests text. By default, item icons should use recognizable object silhouettes, not labels, numbers, fake writing, or UI captions.

## Request Body

Use this shape for the default route:

```json
{
  "description": "<optimized complete-sheet prompt>",
  "image_size": {
    "width": 256,
    "height": 256
  },
  "no_background": true
}
```

Use a seed only when reproducibility or comparison is useful.

Keep `generate-image-v2.description` within the documented character limit. If an exact item list makes the prompt too long or harms visual quality, prefer category coverage for the first candidate and handle exact coverage through a follow-up comparison.

## Verification

Verify before calling the output final:

- Original PixelLab output dimensions match the requested sheet size.
- Original PixelLab output divides exactly into requested cell dimensions.
- `32px icons` are evaluated as 32px per icon/cell, not as the whole sheet size.
- Items fit the requested cell scale; collapsed layouts, multi-object clusters occupying the wrong number of cells, gutters that change cell math, or 64px-ish symbols fail a 32px item-icon-set request.
- Alpha is transparent/backgroundless when `no_background: true` was requested.
- Cropped cells are pixel-hash-unique when uniqueness is required; this does not prove semantic uniqueness.
- Human visual check confirms recognizable RPG item semantics, not just abstract or random shapes.
- Human visual check confirms semantic variety across common inventory categories.
- Human visual check finds no text-like marks unless the user explicitly requested text.
- Human visual check finds no borders, frames, gutters, rounded corners, slot styling, drawn grid, or checkerboard baked into the PixelLab output.
- Human visual check confirms crisp readable pixel art, not noisy/downscaled-looking shapes, mixels, smeared detail, jagged/stair-stepped linework that harms readability, or broken/inconsistent contours.
- Any local crops, splits, previews, checkerboards, or format conversions preserve original pixels and are labeled as derivatives of the original PixelLab output.

Metadata is not enough. A sheet can have the correct dimensions, binary alpha, and unique cells while still failing as pixel art because the objects are semantically unclear, too noisy, badly aligned, or visually downscaled.

If the original PixelLab output fails required size, layout, alpha, border, text, semantic-recognizability, or readability checks, report it as a failed candidate and ask how to proceed. Do not resize, reassemble, remove backgrounds, quantize, clean outlines, or otherwise post-process it into a claimed final asset unless the user explicitly approves that repair path.
