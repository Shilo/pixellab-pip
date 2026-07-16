# PixelLab 16px Item Sprite Generation Spike

Last reviewed: 2026-07-15.

Purpose: capture current findings about generating strict `16x16` sprites with PixelLab, especially the difference between successful full-cell tile atlases and less reliable non-tile inventory item sprites. This is a research spike for prompt design, route selection, and verification. It is not a canonical agent instruction contract.

## Current Recommendation

Use different expectations for tiles, `32x32` item icons, and strict `16x16` item sprites:

| Target | Current confidence | Recommended route |
|---|---:|---|
| Full-cell `16x16` terrain or block textures | Higher | Text-only `POST /v2/generate-image-v2` with opaque, edge-to-edge cell wording |
| Transparent `32x32` inventory item icons | Higher | Text-only `POST /v2/generate-image-v2` with centered single-object icon wording |
| Transparent or contained `16x16` non-tile item sprites | Low | Treat as experimental; use style-reference/editor workflows only with strict copy checks, or generate at `32x32` and downscale with clear reporting |
| Individual `16x16` icons, one simple subject per job (e.g. currency, coins) | Higher for coins; Medium for other subjects | `POST /v2/create-image-pixen`, one short single-subject prompt per job, with `low detail` + `single color black outline` + `side` view; see Pixen Single-Subject section |
| Full-bleed `16x16` icon set (art cropped by the cell edge, not a backdrop behind a smaller subject) | Low for silhouette-varied sets; Medium for one shared cell-filling shape varied by interior features | Fix one cell-filling shape, then `create-image-pixen` per icon (frames tightest, crops). **The `create-image-bitforge` + `coverage_percentage` option below was later probed and failed on both counts** — it did not deliver bleed and ranked worst on quality; see BitForge At 16x16. Not text-only `generate-image-v2`: it has no coverage or detail field. See Full-Bleed 16x16 Icon Sets section |

The main observed pattern is that PixelLab can produce useful `16x16` output when the requested asset is a full-cell tile texture. It has not yet been reliable for text-only prompts asking for many standalone `16x16` food or inventory items in one atlas. Those prompts tend to drift toward larger, more readable item-icon scale. Style-reference routes can anchor the grid more strongly, but they can also over-copy the supplied reference image. Reference-image routes may copy less than style-reference routes, but still need cell occupancy and copy checks.

## Evidence Summary

Relevant committed showcase examples:

- [`showcase/tiles/minecraft-inspired-generate-image-v2-16x16-atlas.png`](../showcase/tiles/minecraft-inspired-generate-image-v2-16x16-atlas.png)
- [`showcase/tiles/minecraft-inspired-generate-image-v2-16x16-atlas.blueprint.json`](../showcase/tiles/minecraft-inspired-generate-image-v2-16x16-atlas.blueprint.json)
- [`showcase/item-icons/fantasy-rpg-consumables-8x8-32px.png`](../showcase/item-icons/fantasy-rpg-consumables-8x8-32px.png)
- [`showcase/item-icons/fantasy-rpg-consumables-8x8-32px.blueprint.json`](../showcase/item-icons/fantasy-rpg-consumables-8x8-32px.blueprint.json)
- [`showcase/item-icons/candy-sweets-treats-8x8-32px.png`](../showcase/item-icons/candy-sweets-treats-8x8-32px.png)
- [`showcase/item-icons/candy-sweets-treats-glossy-8x8-32px.png`](../showcase/item-icons/candy-sweets-treats-glossy-8x8-32px.png)
- [`showcase/skill-icons/create-image-pro-rich-background-8x8-32px.png`](../showcase/skill-icons/create-image-pro-rich-background-8x8-32px.png)
- [`showcase/skill-icons/create-image-pro-fire-magic-sheet-8x8-32px.png`](../showcase/skill-icons/create-image-pro-fire-magic-sheet-8x8-32px.png)

Additional non-showcase local tests were run for `512x512` food and consumable atlases, including four prompt-comparison jobs. Those runs are summarized here because they exposed the failure mode, but the generated files are not treated as public documentation assets.

## Surface And Endpoint Notes

The tested text-only route was REST `POST /v2/generate-image-v2`, surfaced in product wording as Create Image Pro / Create S-XL image. PixelLab's public API catalog lists this route as supporting small canvas sizes and larger square canvases, with optional reference and style images. See [`resources.md`](../resources.md#official-pixellab) for the current official-documentation entry points.

The important distinction is between accepted image size and reliable semantic control. A route may accept a small canvas or a prompt that describes small cells without reliably producing standalone objects that stay inside those cells.

The Aseprite and website/editor surfaces should also be treated separately from REST. The PixelLab Aseprite plugin can run inside an open Aseprite document with existing frames, style references, layer targets, and plugin-specific options. That editor context may influence output behavior in ways that are not equivalent to a text-only REST request.

## Successful Pattern: Full-Cell 16px Tiles

The strongest `16x16` success is the Minecraft-inspired tile atlas in the showcase. It used `POST /v2/generate-image-v2` with a `256x256` canvas, `no_background: false`, and a prompt that described a `16` by `16` grid of `16x16` full-cell block textures.

Key prompt features:

- The output is a single packed atlas.
- Each cell occupies exactly one `16x16` pixel area.
- Cells touch edge-to-edge with no margins, gutters, spacing, guide lines, or drawn grid.
- Every cell is fully filled edge-to-edge, including corners.
- The subjects are block faces and material textures, not centered objects.
- The prompt bans scenery, UI, labels, icons, characters, tools, and cross-cell detail.

This worked better because a tile texture uses the entire square. There is no separate object silhouette, no transparent padding, and no need to preserve empty space around an item.

Known limitation: this should be considered a mechanically useful atlas, not proof of perfect semantic uniqueness. Hash-based verification found most cells unique, but visual review still matters for repeated material families.

## Successful Pattern: 32px Item Icons

The item-icon showcases are strongest at `32x32`. For example, the fantasy RPG consumables sheet uses a `256x256` canvas arranged as `8` columns by `8` rows, with each cell a readable centered `32x32` item.

Useful prompt features:

- `Complete 8 by 8 sheet of 64 unique ... inventory item icons`.
- `each cell a readable 32x32 item`.
- `centered single-object silhouettes`.
- `crisp hard edges`, `low visual noise`, and a consistent inventory style.
- `no_background: true`.
- Negative constraints for text, labels, UI slots, buttons, borders, terrain tiles, skill icons, decorative grids, and background props.

This pattern also worked for candy and dessert icons. The result is relevant to food requests because it shows PixelLab can make strong consumable and treat sheets when the requested cell size gives enough room for readable object silhouettes.

## Related Pattern: 32px Skill Icons

Skill-icon examples also succeed at `32x32`, but they are usually full-bleed opaque square art rather than transparent inventory objects. They behave more like small illustrations than isolated sprites.

This matters because there are two different kinds of packed sprite sheets:

- Full-bleed square art or textures can touch every edge of the cell.
- Transparent object sprites need both object pixels and empty padding inside the same cell.

The second target is much harder at `16x16`.

## Failed Pattern: Text-Only 16px Food Item Atlases

A text-only `512x512` food atlas test asked for `32` columns by `32` rows of `16x16` food and fruit inventory items, including magical berries, fruit variants, grapes, and related consumables.

Observed result:

- The output was visually useful as a food sheet.
- It did not behave as a true `32` by `32` atlas of contained `16x16` items.
- The first visible item already exceeded a single `16x16` cell.
- Visual scale was closer to a smaller grid of larger food icons.

The important verification lesson is that canvas size and crop-grid hashes are not enough. A `16x16` crop grid can produce many non-empty unique crops even when visible objects span multiple intended cells. The first occupied cell should be inspected against the intended `16x16` bounds before broader automated checks.

## Style-Reference Atlas Tests

Two `POST /v2/generate-with-style-v2` tests used a prepared `512x512` style image that was itself an exact `32` by `32` sheet of `16x16` fruit and food item cells. The goal was to see whether a complete style/layout reference could make PixelLab imitate the grid and item scale more faithfully than text alone.

The result was mixed and should be treated as a caution:

- The route preserved the `512x512` canvas and produced a mechanically full `32` by `32` alpha-occupied sheet.
- It anchored the `16x16` cell rhythm better than the earlier text-only `512x512` food prompts.
- It also copied too much from the supplied style image.

The first style-reference run used normal style-copy wording. It returned a completed `512x512` sheet where every `16x16` cell had alpha content. Compared with the supplied style image:

- `0` of `1024` cells were byte-identical.
- `37.64%` of all pixels were exactly identical.
- `874` of `1024` cells had the same alpha bounding box as the corresponding style-image cell.

This was not literally a pixel-perfect copy, but it was functionally too close: item order, silhouettes, and repeated row structure were strongly inherited from the style image. It should not be used as a new asset sheet.

A second style-reference run revised the prompt to say the supplied image was only a layout guide and explicitly banned copying its palette, detail level, outline style, shading technique, item identities, silhouettes, row patterns, or ordering. REST `generate-with-style-v2` does not currently expose public boolean fields matching the Aseprite plugin's style-option checkboxes, so these were prompt constraints rather than API controls.

Compared with the supplied style image, the second run changed more:

- `0` of `1024` cells were byte-identical.
- `34.79%` of all pixels were exactly identical.
- `726` of `1024` cells had the same alpha bounding box.
- The average per-cell difference was much higher than the first run.

This proved the layout-only wording can reduce direct copying, but the result still inherited too much structure and introduced off-target content such as symbol-like or music-note-like cells. It was less copied, but still not a clean, usable new fruit atlas.

### Style-Reference Finding

A complete finished atlas is too strong as a style image when the desired output is another atlas with different content. PixelLab may treat the style image as a reconstruction target, not just as cell-layout evidence. For public or production work, reject outputs that substantially preserve item identities, silhouettes, ordering, or row patterns from a style-only source. Even when the pixels differ, over-copying can make the result inappropriate to use.

If using a style-reference route for strict `16x16` items, prefer references that demonstrate scale without providing a full finished target sheet to copy. Better candidates may include:

- A small set of separate `16x16` example items.
- Sparse layout guides with only a few occupied cells.
- A neutral grid/layout reference that does not contain valuable finished source items.
- Aseprite editor workflows where style options can be disabled and the output can be reviewed before use.

However, even Aseprite/editor style-reference output must be checked for copying. Disabling style-copy options may reduce palette, detail, outline, and shading imitation, but it is not a guarantee that item identities and silhouettes will be novel.

### Manual Aseprite 256px Style-Reference Observation

A manual `256x256` Aseprite style-reference attempt with the style-copy options disabled appeared to improve novelty compared with the full-copy style-reference behavior. It randomized some items and created some unique-looking fruit/food sprites.

The result was still mixed: some items remained near-copies of the input set. This supports the current recommendation that disabling style options is useful as an experiment, but not sufficient as an acceptance criterion. Outputs from this route still need per-item copy review, especially when the input style images contain finished items rather than neutral layout examples.

## REST Reference-Image 256px Crop Test

A corrected `POST /v2/generate-image-v2` test used the Aseprite-style "Reference" role rather than a style reference. The input image was the bottom-right `256x256` crop of the prepared `512x512` fruit atlas, not a scaled-down version of the whole atlas. The request used:

```json
{
  "image_size": { "width": 256, "height": 256 },
  "no_background": true,
  "reference_images": [
    {
      "size": { "width": 256, "height": 256 },
      "usage_description": "Use only as a reference for a 256 by 256 sheet layout: tiny centered transparent inventory items in 16 by 16 cells. Do not copy item identities, palette, silhouettes, row order, or patterns."
    }
  ]
}
```

It did not use `style_image`, `style_images`, or `style_options`.

Observed result:

- Canvas size passed: `256x256`.
- The intended grid had `256` cells.
- `254` of `256` cells had alpha content, so the sheet was not complete.
- The first occupied cell's alpha bounding box stayed inside the first intended `16x16` cell.
- `0` of `256` cells were byte-identical to the reference crop.
- `34.20%` of pixels were exactly identical to the reference crop. Much of this can come from shared transparent/background pixels, so it is not by itself proof of copying.
- Only `3` of `256` cells had the same alpha bounding box as the corresponding reference cell.

Visual review found that this route did not behave like the earlier style-reference reconstruction. It did not preserve row order or most cell silhouettes directly. However, it still inherited the source category distribution strongly and failed completeness by leaving two empty cells. This makes it a more promising experiment than full-atlas style reference, but not a validated solution.

The key lesson is terminology-sensitive: Aseprite's "Reference" image role is not the same as a style-reference image. In REST terms, the closest public field is `reference_images`, not `style_image` or `style_images`. When testing this route, use a true `256x256` crop or source image at the intended output size; do not downscale a larger atlas, because downscaling changes the relationship between source cells and target cells.

## Fresh 256px Text-Only Atlas Test

A later text-only test reduced the request to a `256x256` canvas: `16` columns by `16` rows of `16x16` fruit and food item cells. It used `POST /v2/generate-image-v2`, `no_background: true`, no style image, and no user-supplied seed.

Observed result:

- Canvas size passed: `256x256`.
- The intended grid had `256` cells.
- All `256` cells had alpha content.
- The first occupied cell's alpha bounding box stayed inside the first intended `16x16` cell.
- Visually, the output was a better new atlas direction than the `512x512` style-reference attempts because it did not copy a supplied sheet.

This does not prove that text-only `16x16` item atlases are solved. The result still needs human review for exact per-cell containment, repeated semantics, and item uniqueness. It does suggest that smaller, less overloaded atlas requests may behave better than asking for `1024` unique food items at once.

## Four Prompt Comparison Runs

Four additional text-only runs tested whether the successful tile wording could be adapted to food items. All four used `POST /v2/generate-image-v2`, `image_size: 512x512`, `no_background: false`, and no user-supplied seed. `no_background: false` was intentional because it matched the full-cell tile strategy.

### 1. File Wording, Magical Berries

Prompt structure:

```text
A 1024-file packed atlas of original Minecraft mod food item texture files, arranged as 32 columns by 32 rows. Each file occupies exactly one 16 by 16 pixel cell inside a 512 by 512 image...
```

Result:

- Opaque output, as expected from `no_background: false`.
- Visually organized around larger fruit icons/textures.
- Failed true `32` by `32` layout of contained `16x16` food cells.
- `16x16` cropped hashes included many duplicates, and visual scale failed earlier than duplicate analysis.

### 2. File Wording, Consumables

Prompt structure matched the first run but used bread, toast, stews, cheeses, herbs, candy, drinks, and related consumables.

Result:

- Opaque output, as expected.
- Dense and readable food sheet.
- Still organized around larger icon cells rather than strict `16x16` food cells.
- Hash uniqueness was not sufficient to establish visual correctness.

### 3. Atlas Wording, Magical Berries

Prompt structure removed the potentially ambiguous `file` wording:

```text
A single 512 by 512 pixel atlas image containing 1024 independent Minecraft mod food item cells, arranged as 32 columns by 32 rows. Each cell occupies exactly one 16 by 16 pixel area inside the atlas...
```

Result:

- Opaque output, as expected.
- Removing `file` wording did not fix scale control.
- The output still read as larger fruit icons/textures rather than strict `16x16` cells.

### 4. Atlas Wording, Consumables

Prompt structure matched the third run but used broader consumable food and drink subjects.

Result:

- Opaque output, as expected.
- The clearest scale failure of the comparison set.
- Some objects read as larger `32px` or `64px`-scale food assets.
- Some content spanned multiple intended `16x16` cells.

### Comparison Finding

The word `file` was not the deciding factor. The successful tile showcase used `file` wording, but replacing it with `single atlas image` did not make food items obey strict `16x16` bounds.

The more likely deciding factor is subject type:

- Terrain/block textures can be represented as full-cell material patterns.
- Food objects activate item-icon composition, even when described as full-cell textures.

## Why Backgrounds Appeared

The four comparison runs used:

```json
{
  "no_background": false
}
```

That setting was chosen to mimic the successful tile atlas, where every cell is fully opaque. Backgrounds were expected in those comparison images. They were not evidence of a background-removal failure.

For transparent inventory icons, `no_background: true` remains the appropriate setting. However, the transparent food-atlas test also failed strict `16x16` scale, so transparency alone does not explain the issue.

## Working Hypotheses

### 1. 16px Tile Data And Product Priors Are Stronger

Minecraft-style `16x16` block textures are a common and coherent pixel-art target. A model can represent them as small full-cell patterns without preserving a separate object silhouette.

This explains why `16x16` terrain/block texture atlases are more promising than `16x16` item-object atlases.

### 2. Item Icon Priors Are Stronger At 32px

Standalone inventory objects are commonly represented at `32x32`, `48x48`, or `64x64`. At `16x16`, detailed subjects such as grapes, jars, sliced fruits, glowing berries, pies, and drinks become difficult to distinguish.

When asked for food items, PixelLab appears to prioritize recognizable item semantics over strict cell size. The result is larger, readable icons that can violate the requested bounds.

### 3. Transparent Objects Are Harder Than Full-Cell Textures

Tiles can fill every pixel. Transparent items need both object pixels and padding. A `16x16` transparent item may only have 8-14 useful pixels across after padding, which leaves very little room for grapes, caps, sparkles, jars, fruit slices, or clusters.

### 4. Food Labels May Trigger Icon Composition

Even prompts that say `texture` can contain object labels such as `berry`, `grape`, `jar`, `bottle`, `bread`, `cheese`, or `popsicle`. Those labels may activate item-icon composition more strongly than block-texture composition.

If the desired target is truly a `16x16` food-themed texture atlas rather than inventory objects, prompts may need to describe surfaces instead:

- `berry skin texture`
- `grape pulp texture`
- `jam surface`
- `fruit rind pattern`
- `seed cluster texture`
- `pie filling top`

That route may produce food-themed material cells, not recognizable pickup icons.

### 5. Style References May Anchor Pixel Scale Better Than Text

Image conditioning may provide concrete evidence of pixel density, object-to-canvas ratio, padding, and silhouette complexity. This may help override the larger item-icon prior.

A separate Aseprite plugin observation supports this hypothesis:

- Surface: `Create image from style reference (Pro)` inside Aseprite.
- Open document size: `128x128`.
- Style images shown in the plugin: `5/64`, with `64 frames` indicated.
- Prompt: `based upon the input set create a sheet of small food items, food, berries, places, jars, all at a 16x16 grid size`.
- Output method: `New layer`.
- `Remove background`: checked.
- `Advanced options`: unchecked.
- The plugin UI indicated that the tool costs `20-40 generations` and creates multiple frames.
- Reported behavior: the plugin prompted that the generated result would be padded to `16px`.

This is not equivalent to a REST text-only atlas request. The Aseprite flow includes document size, existing frames or style images, a layer target, background-removal state, and a multi-frame editor workflow. The phrase `16x16 grid size` may be interpreted together with that editor context.

## Workarounds

### Generate 32px Masters, Then Downscale

Use the validated `8x8` / `32px` item-icon prompt pattern, then downscale each item to `16x16`.

Pros:

- Best current visual quality.
- Uses a proven item-icon prompt structure.
- Good category control.

Cons:

- Local resizing changes pixels and must be reported as post-processing.
- It is not a native PixelLab `16x16` result.
- Downscaling may blur or alias unless handled carefully.

### Try Native Small Separate Images

Use `generate-image-v2` with a very small target canvas and a single simple item, rather than one large atlas containing many items.

Pros:

- Tests the small-canvas path directly.
- Avoids asking one image to contain hundreds of semantically distinct items.

Cons:

- Not yet proven for non-tile item sprites.
- May produce weak semantics at `16x16`.
- Requires strict visual bounds verification.

### Use Style Reference Pro With 16px References

Use Create image from style reference (Pro) with one or more `16x16` item references.

Pros:

- Best known route for salvageable `16px` non-tile items.
- References can anchor pixel density and silhouette bounds.
- Aseprite may provide useful editor context through document dimensions, frames, layers, and background-removal state.

Cons:

- More expensive than basic text-only generation.
- Not fully characterized in this repo.
- May return `17x17`, `32x32`, or padded output that still needs crop/pad handling.
- Requires careful reporting when local crop, pad, or sheet assembly is performed.
- May copy supplied reference items too closely, especially when the style image is a complete finished atlas.

Use this route only when copy review is part of the acceptance criteria. A style-reference output can pass size and cell checks while still being unusable because it reconstructs the reference image's item identities, silhouettes, row order, or distribution. In that case, reject it rather than treating it as a valid generated atlas.

### Use Reference Images For Layout/Concept, Not Style

REST `generate-image-v2` supports `reference_images`, which are closer to the Aseprite "Reference" role than `style_image` / `style_images`. This may be a better experimental route when the goal is to communicate atlas layout without asking PixelLab to copy palette, outline, shading, or detail level.

Pros:

- The corrected `256x256` crop test copied much less cell structure than the `512x512` style-reference tests.
- It can communicate the idea of tiny centered transparent inventory items in a packed atlas.
- It avoids the public `style_image` controls that explicitly copy style features.

Cons:

- It is still not a guarantee of novelty.
- It may inherit category distribution or visual habits from the reference.
- It may fail completeness, as one corrected `256x256` test produced `254` non-empty cells out of `256`.
- Inputs should be cropped to the intended output size, not downscaled from a larger atlas.

### Use Aseprite Style Reference With Options Disabled

The Aseprite plugin exposes style options such as copying palette, level of detail, outline style, and shading technique. When testing `16x16` non-tile item generation in Aseprite, disable these options if the goal is a new sheet rather than a close style clone.

Pros:

- The editor can provide document size, frame, layer, and background-removal context that REST text-only prompts do not have.
- Disabling style-copy options may reduce unwanted palette, outline, detail, and shading imitation.
- Aseprite's multi-frame workflow may be a better fit for many small items than one large REST atlas image.

Cons:

- Disabling style-copy options is not the same as guaranteeing novelty.
- Aseprite output can still copy source items or preserve source silhouettes and ordering, even in smaller `256x256` attempts where other cells are newly randomized.
- If a result substantially copies the input set, it is not appropriate to use as a new asset pack, even when it is technically generated by PixelLab.

### Produce Food-Themed Texture Tiles Instead Of Item Icons

If the game can accept full-cell food or material textures, use the tile prompt pattern and describe surfaces rather than objects.

Pros:

- Closest to the successful `16x16` tile pattern.
- Works naturally as a single atlas.

Cons:

- Does not produce transparent inventory icons.
- Cells may read as materials or surfaces rather than pickup items.
- Visual uniqueness still needs human review.

## Prompt Guidance

For true `16x16` full-cell textures:

- Use `single atlas image`, `16 columns by 16 rows`, and `each cell occupies exactly one 16 by 16 pixel area`.
- Use `full square`, `edge-to-edge`, and `including corners`.
- Prefer material/surface terms over object-icon terms.
- Use `no_background: false`.
- Ban connected rows, cross-cell highlights, cross-cell shadows, and detail continuing into neighboring cells.

For transparent item icons:

- Prefer `32x32` unless using the style-reference workaround.
- Use `Complete 8 by 8 sheet of 64 unique ... inventory item icons`.
- Use `clear centered object silhouettes`, `low visual noise`, and `no_background: true`.
- Avoid requesting hundreds of semantic object icons in one image.

For experimental `16px` non-tile items:

- Do not assume text-only `generate-image-v2` will contain each object inside a `16x16` cell.
- Try reference-image, style-reference, or Aseprite editor workflows when strict bounds matter, but reject outputs that copy the reference content too closely.
- Use reference images at the intended output size; crop a larger atlas to the relevant region rather than downscaling the whole atlas.
- Keep concepts simple: one berry, one grape, one seed, one bread bite.
- Avoid jars, bottles, pies, plates, clusters, and multi-part objects in the first test.
- Verify object bounds on the first generated item before broad crop/hash checks.
- Prefer smaller tests such as a `256x256` sheet of `256` cells before attempting a `512x512` sheet of `1024` unique items.

## Verification Guidance

For a `16x16` item atlas:

1. Confirm the image is the requested canvas size.
2. Overlay or inspect the intended `16x16` grid.
3. Check the first visible item against the first intended cell.
4. Confirm the item does not extend into neighboring cells.
5. Check a representative row and column.
6. Only after visual cell-scale passes, compute empty cells and duplicate hashes.

For full-cell opaque textures:

1. Confirm every cell is filled if that was requested.
2. Check visible cell boundaries and cross-cell continuity.
3. Use hash uniqueness for exact duplicates.
4. Use visual review for semantic duplicates and repeated material families.

For transparent item icons:

1. Check alpha.
2. Check object bounding boxes per cell.
3. Confirm each object is centered and contained.
4. Check duplicate hashes and semantic duplicates.

For reference-image, style-reference, or Aseprite outputs:

1. Compare the output to the supplied style/reference image, not just to the prompt.
2. Count exact same pixels when possible.
3. Compare per-cell alpha bounding boxes.
4. Review whether item identities, silhouettes, ordering, and row patterns were preserved.
5. Reject the result if it is effectively a reconstruction of the source, even when no cell is byte-identical.

## Recommended Next Experiments

1. Reproduce the Aseprite style-reference attempt with an open `128x128` document, several `16x16` food/item style frames, `Create image from style reference (Pro)`, `Output method: New layer`, and `Remove background` checked.
2. Use the observed prompt as the baseline: `based upon the input set create a sheet of small food items, food, berries, places, jars, all at a 16x16 grid size`.
3. Repeat with all style-copy options disabled when the UI exposes them, including both `128x128` and `256x256` documents.
4. Record whether the plugin prompts about padding to `16px`, whether output is generated as frames, layers, a sheet, or individual images, and whether any result is forced to `32x32`, `17x17`, or another size.
5. Compare output against the input set for copied items, copied silhouettes, copied ordering, and copied row structure; separate genuinely new cells from near-copy cells.
6. Run REST `generate-image-v2` with `reference_images` using cropped `256x256` references, not downscaled full atlases, to isolate whether the Aseprite Reference role maps better to public REST reference images.
7. Run the closest available non-Aseprite style-reference route with the same `16x16` references and prompt to isolate whether Aseprite editor context is the key variable.
8. Try text-only single-item `16x16` or `17x17` outputs for simple subjects such as blue berry, grape, raspberry, seed, bread bite, mushroom cap, cheese wedge, and candy.
9. Try more text-only `256x256` atlases of `256` item cells before scaling back up to `512x512` / `1024` cells.
10. Try a `256x256` atlas of 256 food surface textures, not object icons, using the tile prompt structure.
11. Compare all routes with the same item list and the same verification checklist.

## Pixen Single-Subject 16×16 Icons (Live Test 2026-07-11)

A separate live test evaluated `create-image-pixen` (the "Create Image S-XL (New)" tool) for individual `16x16` icons, one item per job. This is distinct from the atlas work above: `create-image-pixen` returns exactly **one image per call**, whereas `generate-image-v2` returns a native-size *batch* of many images at small sizes. So pixen is the route for "one icon per job," not for a one-shot multi-item sheet.

### Recipe That Worked

Ten fantasy MMORPG currency icons were generated, one per job, in parallel:

- One **short single-subject** `description` (e.g. `gold coin`) — never a multi-item list.
- `image_size` `16x16`, `no_background: true`, `detail: low detail`, `outline: single color black outline`, `view: side`, fixed `seed`.

Subjects: copper, silver, gold, platinum, bronze, electrum, and mithril coins; a coin stack; a gold ingot; a cut gem.

### Results And Quality

- All ten returned native `16x16` with clean alpha (35–47% opaque). **Transparency was honored** — the earlier 91%-opaque pixen result came from overloading a single `16x16` canvas with a 64-item list, not from the size or from `no_background`. Short single-subject prompts fix it.
- **Coins came out clean, readable, and color-differentiated**, reading as a coherent set — a good result for `16x16`. The coin stack and gold ingot also read well.
- The weaker outputs were subject/prompt problems, not size limits: `electrum coin` picked up a small face-like mark, and `cut blue gemstone` came out muddy (read more like a small figure than a gem). Reworded prompts (for example `faceted blue diamond, simple`) are the fix, not a different size.
- Cost was about **$0.008 per `16x16` icon**. The observed account concurrency cap was **8 simultaneous jobs** (Tier 2 during this test); two of ten returned HTTP `429` and were re-run sequentially.

### Confirmed Artifact: Hollow Coin Centers From Background Removal

Several coins came out as a gold **ring with a two-pixel transparent center hole** instead of a solid disc. This was diagnosed, not assumed:

- Regenerating the same `gold coin` with `no_background: false` returned a **fully opaque** coin whose center is a **dark near-black fill (RGB ≈ 56,58,64)** inside the gold rim.
- That dark center is the **same color as the background** pixen places behind the sprite. PixelLab's `no_background` removal is color-based, so it deletes the enclosed dark center along with the outer background, leaving the hole.
- A local **edge-flood** removal (flood from the image border, remove only background-colored pixels reachable from an edge, keep enclosed regions) applied to the opaque version restored a **solid disc with no hole** and clean transparency.

This matches the enclosed-background risk in [`background-removal.md`](../../skills/pixellab-pip/references/background-removal.md). It is a background-removal side effect, not a pixen rendering flaw and not a `16x16` limit.

### Practical Guidance

- For individual `16x16` icons, `create-image-pixen` with one short single-subject prompt is a viable, good-quality route, strongest for coins and currency.
- When an icon's interior is the same value as the generated background, prefer generating **opaque** (`no_background: false`) and removing the background **locally with an edge-connectivity method** that preserves enclosed fills, rather than relying on `no_background: true`. Steering the interior color away from the background with subject or palette wording also helps.
- Keep parallel batches at or below the account's concurrent-job cap.

Local run outputs (not committed showcase assets) are in the `pixellab-pip-generations/pixen-16x16-currency-set/` run folder: the ten icons, a native spritesheet, an inspection sheet, the with-background and edge-flood-repaired `gold coin` comparison, and a bundle blueprint. See [`pixellab-image-size-limits.md`](pixellab-image-size-limits.md) for the confirmed pixen `16x16` size floor.

## Full-Bleed 16x16 Icon Sets (Live Test 2026-07-15)

Two `16x16` native-batch runs on `POST /v2/generate-image-v2` (one call each, 64 images, $0.095 each) were rejected by the requester as noisy, unreadable, and not full size: `ui-icons-questboard` (64 fantasy UI icons, `no_background: true`) and `cute-animal-emojis-16px` (64 cute animal emoji faces, `no_background: false`). Both are local run folders, not showcase assets. A comparison set of round yellow smiley emojis generated on the same endpoint at the same size was accepted as crisp and readable, which is what makes the pair diagnostic: the endpoint is not the whole story.

Measured across the 64 cells of each run:

| Measure | Questboard | Animal emojis | Reference for clean `16x16` |
|---|---:|---:|---|
| Unique colors per cell (median) | 19 | 19 | ~4-12 |
| Subject longest side within the 16px cell (median) | 14px | 14px | 16px for full-bleed |
| Cells whose art reaches the cell edge | 0/64 | 9/64 | 64/64 for full-bleed |

A subject 14px across in a 16px cell spends about 40% of the available area on margin, which at this size is the difference between readable and muddy.

### Why They Failed

Four causes, in rough order of leverage. The first is route selection; the rest are request design.

1. **The route had no field for anything being asked for.** Both prompts specified `flat`, `no gradients`, `limited palette`, and `bold single-color black outline`. `generate-image-v2` has no `detail`, `outline`, `shading`, `color_image`, or `coverage_percentage` field, so every one of those was unenforceable text and all four were ignored — hence 19 colors per cell. This is the mechanism behind the existing "Pro is unreliable for a clean icon below `32px`" guidance, and it is why the fix is a route with the fields rather than more prompt wording. Recorded canonically in [`create-image-pro.md`](../../skills/pixellab-pip/references/create-image-pro.md).
2. **`full-bleed` was read as backdrop rather than crop.** The animal run sent `no_background: false` and wrote `every pixel is painted, including all four corners and all four edges`. A painted backdrop with a small creature on it satisfies that literally, and that is what came back. The background was requested, not a model failure. The requester meant the art itself should reach the edges. Two readings, opposite settings; `cropped` is the term that cannot be misread.
3. **Silhouette variety and bleed competed.** The animal run asked for 22 species each with `a distinct ear or horn silhouette` *and* edge-to-edge fill. A silhouette reads only against negative space, so outline-varied sets and full-bleed are mutually exclusive as the same design axis; the model resolves the conflict with margin or a backdrop. This is not a hard geometric impossibility — a cropped close-up fox face is full-bleed — but it does mean variety must move to interior features (color, markings, eyes, expression) once bleed is required. The questboard run is the sharper case: a key or feather has no cell-filling form at all, and its prompt additionally said `each a single centered emblem`, which explicitly requests the margin. Avoid `centered` in any full-bleed prompt.
4. **Prior strength at the target size.** The accepted smiley set had the advantages the failed sets lacked: one fixed round head that inscribes a square naturally, variety carried entirely by interior features, a palette stated as construction (`flat yellow fill with one darker yellow shade`, near-black features — roughly five colors) rather than as a list of ten hues, and a subject that genuinely exists at `16px` in the wild via emoji fonts, favicons, and UI icons. There is no comparable `16px` corpus of full-bleed animal portraits or fantasy props. This reinforces hypotheses 1 and 3 above: shape simplicity and native-size priors, not transparency, drive the result.

### Guidance

- Decide bleed vs backdrop with the requester before generating; do not infer it from the word `full-bleed`.
- For a varied full-bleed set, fix one shared cell-filling shape and vary interior features. Do not vary the silhouette.
- State the palette as construction (`one flat fill plus one shade`), not as a list of hues. A ten-hue list plus per-subject schemes is what produced 19 colors per cell.
- Route by field, not by candidate count: `create-image-pixen` for `detail`/`outline`, `create-image-bitforge` for `coverage_percentage`. The `generate-image-v2` batch is attractive at ~$0.095 for 64 candidates, but 64 pixen jobs at ~$0.008 each is ~$0.51 and is the route that has the controls. **Superseded for bitforge:** a later probe found `coverage_percentage: 100` neither produced bleed nor acceptable art at `16px` — having the field is not the same as the field working. See BitForge At 16x16.
- Do not use `forced_palette`. It does not exist in the v2 schema; the field is `color_image`, and these request schemas set `additionalProperties: false`, so an unknown field is a hard `422`.

## BitForge At 16x16: The Mid-Grey Mechanism (Live Test 2026-07-15)

Follow-up to the full-bleed animal-emoji rejection above. **Context: BitForge is already the measured worst model across the board** — it placed last or near-last in every category of the [model benchmark](../pixellab-image-model-benchmark-results.md), which recommends it *only* for its unique controls (`init_image`, `mask_image`, `color_image`, `coverage_percentage`, `style_image`) and never as a quality pick. This section does not re-discover that; it explains **why** it fails specifically at `16px`, and finds that even its `coverage_percentage` justification does not hold at this size.

Six single-fox `16x16` probes, seed `715642`, `no_background: true`, `detail: low detail`, `outline: lineless`, `view: side`; the requester ranked them without seeing the metrics. **The ranking maps 1:1 to route** — all four pixen probes beat both bitforge probes.

| Rank | Route | Extra fields | Muddy mid-grey |
|---:|---|---|---:|
| 1-4 | `create-image-pixen` | none | **0%** |
| 5 | `create-image-bitforge` | `shading: flat shading` + anti-shading `negative_description` | **16%** |
| 6 | `create-image-bitforge` | same + `coverage_percentage: 100` | **13%** |

- **The mechanism is desaturated mid-grey** (HSV `s < 0.28`, `0.3 < v < 0.85` — excludes cream highlights and the dark outline). Binary: 0% in every accepted probe, 13-16% in both rejected. Mid-grey is the color a shading ramp is made of, not the color of a part; at `16px` the eye stops segmenting parts and reads blur. **Quantizing to 8 colors did not redeem them** — it preserves the grey with fewer steps. This is a plausible mechanism for the benchmark's measured "BitForge weakest overall" at small sizes, though the benchmark's verdict stands on its own evidence and does not depend on this one.
- **The `shading` enum has no "off" rung:** `flat → basic → medium → detailed → highly detailed shading`. Setting `flat shading` selects the *least* shading, not none — it still requests a ramp. `create-image-pixen` exposes **no `shading` field at all**, which is why it renders flat by default. Do not reach for the field to *get* flat.
- **`coverage_percentage: 100` did not produce edge-to-edge** (117/256 opaque, 0/64 border pixels painted) *and* ranked worst. The Full-Bleed guidance above ("`create-image-bitforge` for `coverage_percentage`") did not hold at this size.
- **A closed named palette beat negations.** The top probe stated `three vivid flat colors only: bright orange, cream, dark brown` and never said "no shading". The 4th-ranked said `absolutely flat… no shading, no shadows, no highlights, no gradients, no dithering` and came out *more* shaded. Three named warm colors cannot build a ramp — the constraint is structural rather than a request.
- **Judge tiny art at 1×.** At 16× magnification the worst probe looks admirably flat (9 raw colors) and the best looks noisy (81). Four metrics — raw color count, orphan-color distance, region fragmentation, per-color coherence — each confirmed that inverted reading; a native-size strip settled it in one glance. Magnification flatters illegible art, and raw color count is not a flatness proxy.
- **Confidence: directional only.** One subject, one seed, n=1 per configuration, one reviewer. Route and grey% separate cleanly; the prompt-wording claims are confounded with route and are the weakest here.

Local run outputs (not showcase assets): `pixellab-pip-generations/flat-animal-emojis-16px/`.

## Pro (generate-image-v2) vs Pixen at 16×16 (Live Test 2026-07-11)

A follow-up compared the two image routes head-to-head at `16x16` for treasure items. The motivating puzzle: `generate-image-v2` (Pro) normally produces cleaner, higher-fidelity item art than pixen at `32px+`, yet an earlier `16x16` Pro attempt came out noisy with orphan pixels — the opposite of expectation.

### Setup

- **Pro:** one `POST /v2/generate-image-v2` job at `16x16`, `no_background: true`, seed, and an optimized single-centered-treasure prompt. Pro is **asynchronous** — it returns HTTP `202` + `background_job_id`; poll `GET /v2/background-jobs/{id}`. At `16x16` it returned a **native-size batch of 64 images** from the one prompt (usage `$0.095`, ≈`$0.0015`/image).
- **Pixen:** nine `POST /v2/create-image-pixen` jobs, one treasure item each, `16x16`, the proven recipe (`detail: low detail` + `outline: single color black outline` + `view: side` + `no_background`, ≈`$0.0084`/image). Pixen is **synchronous**, one image per call.
- Pro description (verbatim): `Fantasy RPG treasure loot icon, one centered treasure object per image, bold clean silhouette, highly readable at tiny size, crisp pixel art, limited palette, no orphan pixels, transparent background. Unlabeled pictorial assets only. Varied precious treasures across gold coins, gemstones, jeweled rings, crowns, goblets, chalices, pearls, amulets, treasure chests, golden idols, and relics. No text, letters, numbers, or labels.`
- Pixen items: `gold coin`, `red ruby gemstone`, `golden crown`, `jeweled gold ring`, `treasure chest`, `white pearl`, `golden goblet`, `cut diamond`, `golden amulet`.

### Root Cause: The Control Surface

`generate-image-v2` exposes only `description`, `image_size`, `seed`, `no_background`, `reference_images`, `style_image`, `style_options` — **no `detail`, `outline`, or `view` controls**. `create-image-pixen` exposes `detail`, `outline`, and `view`. That single difference explains the `16x16` quality gap: pixen can be forced to a flat, low-detail, hard-outlined style that suits `16px`; Pro always renders at its native detail level, which is tuned for `32px+`.

### Results

| Signal | Pixen (9) | Pro (64) |
|---|---:|---:|
| boundary that is dark outline | **93%** | 56% |
| avg orphan pixels | 0.00 | 0.20 |
| distinct colors per image | 61 | 28 |
| avg opaque | 35.6% | 44.4% |
| anti-aliased (partial-alpha) pixels | 0 | 0 |
| edges | hard single-color outline | soft, no enforced outline |
| text/caption artifacts | none | 2 frames became `$` / `2` marks |
| cost per image | `$0.0084` | `$0.0015` (batch of 64) |

- **Pixen** produced clean, bold-outlined, instantly readable icons with zero orphan pixels and a consistent style — the better route for clean, specific `16x16` icons.
- **Pro** produced far more variety and richer shading in one job, but at `16x16` the extra detail degraded into softer edges, muddier reads, some stray/orphan pixels, and two caption-contamination frames. Usable after culling, not clean out of the box.
- **It is containment, not color count.** Counter to a "more colors = more noise" intuition, pixen uses *more* than twice as many colors (61 vs 28) yet reads cleaner. Neither route anti-aliases (both have 0 partial-alpha pixels), so "soft" edges are *undefined* edges, not blur. The drivers are the border and the detail level: pixen's dark outline covers **93%** of each silhouette boundary vs Pro's **56%**, and its `low detail` flattening organizes those colors into a crisp shape; Pro leaves ~44% of its edges bordered only by the item's own color meeting transparency, plus occasional orphan pixels, so shapes lose definition at `16px`.

### Why Pro Looks Worse At 16px Than At 32px+

Pro's native detail level resolves cleanly when there are at least `32px` to spend on an item, which is why it is the higher-quality route for `32x32+` item icons (consistent with the `32x32` item-icon rows above). Crammed into `16x16`, that same detail becomes sub-pixel noise and orphan pixels, and there is no low-detail control to flatten it. The earlier failed `16x16` Pro sheet was likely also an unoptimized prompt; an optimized single-object, no-text prompt improved Pro's `16x16` output substantially but still could not match pixen's controlled cleanliness at that size.

### Guidance

- **Clean, consistent, specific `16x16` icons → pixen** (`low detail` + `single color black outline`).
- **Cheap, large, varied `16x16` treasure/loot grab-bag → Pro batch, then cull** the muddy and text-contaminated frames; at ≈`$0.0015`/image it is far cheaper per icon and gives one-shot variety pixen cannot.
- **`32px+` item icons → Pro** (`generate-image-v2`); its detail resolves and it beats pixen on fidelity and clarity.
- Front-load `Unlabeled pictorial assets only` and forbid text in Pro batch prompts; even so, expect occasional caption-like frames to cull.

Local run outputs (not committed showcase assets) are in the `pixellab-pip-generations/pro-vs-pixen-16x16-treasure/` run folder: the 64-image Pro batch, the 9 pixen icons, inspection sheets, and clean native spritesheets.

### Guardrailed Pro Prompt And The 16-vs-32 Ladder (Live Test 2026-07-11)

A second test asked whether Pro's `16px` weakness is fixable by prompt guardrails, and how both routes scale from `16` to `32`. One Pro description with explicit `bold single-color black outline`, `low detail`, `flat fill`, `limited palette`, and `no gradients / noise / stray pixels` was run at `16x16` and `32x32` (64 images each); pixen ran the same four fantasy items (`iron sword`, `round wooden shield`, `red health potion`, `wooden wizard staff`) at each size. Seed `20260712`, `no_background: true` throughout.

| group | n | dark-outline coverage | orphans/img | colors/img | opaque% |
|---|---:|---:|---:|---:|---:|
| Pro 16 | 64 | 62% | 0.45 | 22 | 37% |
| Pro 32 | 64 | **96%** | 0.91 | 32 | 32% |
| Pixen 16 | 4 | 100% | 0.25 | 54 | 35% |
| Pixen 32 | 4 | 100% | 0.00 | 283 | 49% |

- **Guardrail wording measurably steers Pro.** Explicit outline / low-detail / limited-palette wording raised Pro's dark-outline coverage from the un-guardrailed `56%` (treasure test) to `62%` at `16px` and `96%` at `32px`. Pro has no `outline` control, but the prompt is a real lever — most effective at `32px`.
- **Pro is decisively a `32px+` tool.** Guardrailed Pro `32x32` was the best group overall: 64 varied, clean, strongly-outlined, game-ready fantasy icons in one job. Guardrailed Pro `16x16` improved clearly over the earlier un-guardrailed `16px` Pro but stayed softer/muddier (62% outline) — `16px` is simply too small for the model to place a consistent outline even when told to.
- **Orphan count is not the quality signal; outline coverage is.** Pro `32` had *more* orphan pixels than Pro `16` (0.91 vs 0.45) yet looks far cleaner, because the near-complete outline and larger, resolved shapes dominate perception.
- **Both routes gain quality from `16`→`32`.** Pixen stayed fully clean (100% outline, ~0 orphans) at both sizes and grew much richer at `32` (colors 54→283: gradient shading contained inside the outline). Pixen `16` is simple but perfectly readable.
- **Practical split, refined:** at `16px`, pixen is still the cleaner route (100% vs 62% outline), but a guardrailed Pro `16x16` batch is a viable cheap-variety source to cull. At `32px`, guardrailed Pro is the strongest route for varied item sets; pixen `32` is the choice when you need specific, controlled, guaranteed-clean icons.

Local run outputs in the `pixellab-pip-generations/fantasy-pro-vs-pixen-16-32/` run folder (Pro 16/32 batches of 64, pixen 16/32 sets of 4, inspection sheets).

### Assessment: Per-Size Verdict (2026-07-11)

Combining live results, metrics, and reviewer judgment — high-confidence conclusions only:

- **`16px` Pixen — the viable `16px` route.** Consistent outlines (100% coverage), readable, clean shapes. Effectively the only production route at `16px`. Recommended polish: clamp the palette to roughly 16–32 colors (it ships ~54); that reads as more authentic pixel art. This is a local post-process, not a generation control.
- **`16px` Pro — not viable for a clean single icon.** Inconsistent outline (62%), baked shadows, and orphan pixels; muddier than Pixen. Nuance: it is not *entirely* unreadable — some items read (swords, potions, keys) — and a guardrailed Pro `16px` batch is usable as a cheap variety source to cull, but it is unreliable for a clean, finished single `16px` icon.
- **`32px` Pixen — usable but over-shaded.** Consistent pixels and outline, but ~283 colors is far more than clean pixel art needs, so it looks over-shaded/painterly for `32px`. Nuance: it is still readable at native scale; the real problem is the color/shading load, not legibility. Clamping to ~16–32 colors is the fix — `detail: low detail` alone did not limit colors at `32px`.
- **`32px` Pro (guardrailed) — best of the four.** Clean, strongly-outlined (96%), varied, essentially production-ready with minor touch-ups. This is Pro's sweet spot.
- **Cross-cutting: palette discipline is the shared lever.** Both Pixen sizes carry more colors than clean pixel art wants; a local palette clamp to ~16–32 colors is the recommended polish, and neither route exposes a color-count generation control (color reduction is a local/editor step — see `../../skills/pixellab-pip/references/aseprite-cli.md`). A local MEDIANCUT clamp confirmed this: the `32px` wooden shield dropped 458→23 colors and the coins ~55→15, with shapes preserved — the over-shading flattens into clean pixel art.

## Bottom Line

PixelLab appears capable of `16x16` pixel density, but subject type and surface context matter. Text-only `generate-image-v2` is promising for `16x16` full-cell tiles and reliable for `32x32` item-icon sheets. Strict `16x16` non-tile item *atlases* remain experimental, but individual `16x16` icons from per-job `create-image-pixen` (one short single-subject prompt) are a good-quality route, strongest for coins and currency — see the Pixen Single-Subject section. At `16x16`, pixen also produces cleaner icons than `generate-image-v2` (Pro), which lacks `detail`/`outline` controls and renders at a `32px+`-tuned detail level; Pro regains the quality lead at `32px+`. See the Pro vs Pixen section.

The best current path is not one universal route. For strict `16x16` non-tile items, use smaller text-only tests, Aseprite/editor workflows, REST `reference_images`, or REST style-reference workflows only with explicit copy-detection. If the output copies the supplied reference/style items too closely, it should be rejected even if it passes canvas-size and cell-size checks.
