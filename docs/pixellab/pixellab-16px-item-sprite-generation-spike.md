# PixelLab 16px Item Sprite Generation Spike

Last reviewed: 2026-07-09.

Purpose: capture current findings about generating strict `16x16` sprites with PixelLab, especially the difference between successful full-cell tile atlases and less reliable non-tile inventory item sprites. This is a research spike for prompt design, route selection, and verification. It is not a canonical agent instruction contract.

## Current Recommendation

Use different expectations for tiles, `32x32` item icons, and strict `16x16` item sprites:

| Target | Current confidence | Recommended route |
|---|---:|---|
| Full-cell `16x16` terrain or block textures | Higher | Text-only `POST /v2/generate-image-v2` with opaque, edge-to-edge cell wording |
| Transparent `32x32` inventory item icons | Higher | Text-only `POST /v2/generate-image-v2` with centered single-object icon wording |
| Transparent or contained `16x16` non-tile item sprites | Low | Treat as experimental; prefer style-reference workflows or generate at `32x32` and downscale with clear reporting |

The main observed pattern is that PixelLab can produce useful `16x16` output when the requested asset is a full-cell tile texture. It has not yet been reliable for text-only prompts asking for many standalone `16x16` food or inventory items in one atlas. Those prompts tend to drift toward larger, more readable item-icon scale.

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
- Try style reference first when strict bounds matter.
- Keep concepts simple: one berry, one grape, one seed, one bread bite.
- Avoid jars, bottles, pies, plates, clusters, and multi-part objects in the first test.
- Verify object bounds on the first generated item before broad crop/hash checks.

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

## Recommended Next Experiments

1. Reproduce the Aseprite style-reference attempt with an open `128x128` document, several `16x16` food/item style frames, `Create image from style reference (Pro)`, `Output method: New layer`, and `Remove background` checked.
2. Use the observed prompt as the baseline: `based upon the input set create a sheet of small food items, food, berries, places, jars, all at a 16x16 grid size`.
3. Record whether the plugin prompts about padding to `16px`, whether output is generated as frames, layers, a sheet, or individual images, and whether any result is forced to `32x32`, `17x17`, or another size.
4. Run the closest available non-Aseprite style-reference route with the same `16x16` references and prompt to isolate whether Aseprite editor context is the key variable.
5. Try text-only single-item `16x16` or `17x17` outputs for simple subjects such as blue berry, grape, raspberry, seed, bread bite, mushroom cap, cheese wedge, and candy.
6. Try a `256x256` atlas of 256 food surface textures, not object icons, using the tile prompt structure.
7. Compare all routes with the same item list and the same verification checklist.

## Bottom Line

PixelLab appears capable of `16x16` pixel density, but subject type and surface context matter. Text-only `generate-image-v2` is promising for `16x16` full-cell tiles and reliable for `32x32` item-icon sheets. Strict `16x16` non-tile item sprites should remain experimental until style-reference or native-small-image workflows are reproduced and verified.
