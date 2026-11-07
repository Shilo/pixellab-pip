# Icon And Icon Sheet Generation

Use this reference for skill/ability/spell/action-bar/hotbar icons, inventory item/equipment/loot/pickup/consumable icons, and emojis, single or sheets, including transparent, no-border, and split-PNG requests.

## Contents

- [Route](#route)
- [Canvas Sizing](#canvas-sizing)
- [Prompt Pattern](#prompt-pattern)
- [Matching An Existing Set](#matching-an-existing-set)
- [Request Body](#request-body)
- [Verification](#verification)

## Route

Route by the requested result, then size/style constraints:

- **One small icon:** ordinarily MCP `create_image_pixen` / REST `create-image-pixen` for one native-size result at 1 generation. Use requested outline/detail/view controls rather than forcing a black outline. PixFlux is another single-image option; Pro can fit a stronger style/reference or candidate-variety need, at higher call cost. Do not promise equal quality across models or choose a many-candidate call merely because the icon is 32px. Include route choice in the existing cost card, without a separate route-confirmation turn.
- **Named distinct icons:** preserve the exact requested subjects and count. Choose a sheet/batch or per-concept calls by required layout/controls and total call cost; explain the material tradeoff in the existing approval card. Verify every named item either way: allocating one call per name does not guarantee recognizable coverage, and a Pro candidate count is not a count of distinct requested concepts.
- **A sheet or exploratory variety:** MCP `create_image_pixen` / REST `create-image-pixen` can generate a one-call sheet; `create_image_pro` / `generate-image-v2` remains an option for style/references or candidate variety (`create-image-pro.md` covers its candidate counts and prompt-guided grid limits). For cells below 32px, prefer separately generated icons and approved local assembly when reliable cell boundaries matter. An explicit Pro sheet request may be attempted with its documented checks; no text prompt guarantees cell math. Keep generation-versus-assembly scope clear in the plan.

Do not default to object generation (`create_1_direction_object` / `create-1-direction-object`), `create_tiles_pro`, or UI tools for ordinary icons. Observed object-route icons had weak small-scale clarity; this is a scoped quality preference, not proof that those tools cannot make icons. A supported alternative must still deliver the requested size, subjects and readable art. Use UI routes for the slot, button, panel, frame, or container itself.

Background defaults differ by icon type:

- Skill/ability icons: backgrounded sheets (`no_background: false`) are the validated default — rich full-bleed painted cells. Transparent skill icons are a less-validated shape; use `no_background: true` only when clearly requested.
- Item/inventory icons: transparent (`no_background: true`) is the default — inventory icons usually need alpha.
- Emojis: transparent (`no_background: true`), like item icons.

If `no_background: true` was sent but the output kept a background, read `background-removal.md` and apply safe removal when it preserves the art.

## Canvas Sizing

For plural or complete sets, `32x32 icons` is the per-icon cell size, not the canvas:

- `8x8` / 64 icons at 32px each → `image_size: { "width": 256, "height": 256 }`.
- `4x4` / 16 icons at 32px each → `image_size: { "width": 128, "height": 128 }`.
- A `32x32` `image_size` fits only a single icon. At small sizes `generate-image-v2` may return a multi-candidate batch; read `create-image-pro.md` for native-size diversity, no-label, and view guidance, then present candidates and select after visual review.

For one-call sheet generation, verify the original sheet against the requested cell size. If symbols come out 64px-ish, the layout collapses, or gutters break the cell math, report a failed candidate — do not resize or reassemble it into a claimed final.

## Prompt Pattern

Preserve the requested final sheet. For one-call sheet generation, use sheet language; for approved per-concept generation and assembly, prompt each source as a standalone icon and deliver the assembled sheet. Follow SKILL.md Text Preparation: content only, no operation language, no canvas size or transparency wording already carried by `image_size`/`no_background`.

Backgrounded skill-icon sheet starting point:

```text
Complete 8 by 8 sheet of 64 unique fantasy RPG skill icons for game UI, 8 columns and 8 rows, each cell a readable 32x32 icon, perfectly aligned edge-to-edge with no spacing, overlap, cropped icons, dividers, or drawn grid. Rich full-bleed illustrated miniature backgrounds behind clear centered pictorial symbols: flames, ice shards, lightning bolts, shields, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, masks, potions, celestial beams, and aura effects. No text, letters, words, numbers, labels, captions, handwriting, fake writing, runes, glyphs, or alphabet-like shapes. Varied abilities across elemental magic, weapon attacks, healing, protection, stealth, curses, nature, summoning, movement, utility, poison, holy, shadow, and dragon breath. No terrain tiles, inventory sheet, borders, frames, UI slots, rounded corners, watermark, or separating lines. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.
```

Transparent item-icon sheet starting point:

```text
Complete 8 by 8 sheet of 64 unique fantasy RPG inventory item icons, 8 columns and 8 rows, each cell a readable 32x32 item, perfectly aligned with no spacing, overlap, cropped items, dividers, or drawn grid. Pixel art with clear centered object silhouettes, crisp hard edges, low visual noise, limited palette, consistent high-fantasy inventory style. Include varied common RPG inventory categories: melee weapons, ranged weapons, shields, armor, helmets, jewelry, potions, scrolls, books, food, coins, gems, ores, herbs, monster parts, tools, keys, chests, bags, bombs, and arrows. No text, letters, words, numbers, labels, captions, fake writing, runes, glyphs, UI slots, buttons, borders, frames, rounded corners, watermark, terrain tiles, or decorative grid lines.
```

For sheet prompts, adapt theme, subject list, and palette; keep the sheet-layout, per-cell-size, no-text, and no-border clauses.

For an action-focused ability, use one concrete visible pose instead of the `Pictorial symbols only` anchor when it communicates the mechanic better.

Anchors for known failure modes (use only the ones that apply): `Pictorial symbols only`; `rich full-bleed illustrated miniature background` / `Fully opaque, every pixel painted` (backgrounded only); `No borders, frames, UI slots, rounded corners, dividers, watermark`; `No black outlines around icon square edges`.

Avoid positive mentions of `rune`, `glyph`, `sigil`, `spellbook labels`, `UI slot`, `button`, `frame`, `border`, or `card` unless requested — they create text-like marks or slot styling. Use them only in negative clauses. For sheets, avoid `one icon per image` / `standalone icon` phrasing — it pushes isolated symbols on flat backgrounds.

Item-icon specifics:

- For exploratory variety, category coverage can avoid an overlong catalog. For a user-supplied exact list, retain every requested item from the first plan; do not replace it with categories or postpone missing subjects to an unapproved follow-up.
- Do not over-prompt outline instructions unless the user asks for a specific outline style; spotty or broken contours are a failed candidate, not a prompt-patch target.

## Matching An Existing Set

- Generate at the icon's final size. Drawing larger and downscaling came out muddy and speckled next to a native set.
- Pro with `style_image_url` = **one** icon of the set and `style_copy: ["outline", "detail", "shading"]` (no `color_palette`) keeps outline weight and shading while each icon keeps its own colours; the style icon's subject can be anything. A grid of icons as the style image makes Pro wrap candidates across cell corners.
- When Pro Flash was selected (`pro-flash.md`), a same-size icon as `style_image` worked well for one-icon jobs in the observed set. Several icons on one canvas came out cruder in that test; inspect the result rather than assuming a quality or cost advantage.
- Keep one colour family per class or school in a skill set; take the families from the project style (`project-style.md`).
- For requested rarity tiers, propose a supported edit of the approved base icon to retain its identity: `Same <item>, same shape, size and position, upgraded to a <tier> version: <changes>`. Use the selected route's image fields and verify continuity.
- A status or buff icon and the skill that applies it need different subjects, or the chip reads as the skill.
- Replacing a legacy set: list every meaning each old icon stood for first, reuse a fitting existing icon where one exists, and generate only the rest. When distinct meanings need distinct pictures, differentiate similar subjects (such as two open books); preserve intentional reuse.
- Icons the engine tints at runtime: `white and light grey only, greyscale, solid black outline`.
- Picking: show candidates at 3x on the UI's own background colour. Dark iron or black objects vanish on dark panels; upright, symmetric silhouettes read better than tilted ones; skip candidates with stray sparkle pixels in the corners.
- More failure anchors: `filling the frame` when the subject is small in the cell; say what an ambiguous silhouette must not be (`clearly a scythe, not a pickaxe`, `a lion-head shield, NOT a lion`) and name its direction (`pointing diagonally up-right`).

## Request Body

```json
{
  "description": "<optimized complete-sheet prompt>",
  "image_size": { "width": 256, "height": 256 },
  "no_background": false
}
```

MCP `create_image_pro`/`create_image_pixen` take flat `width`/`height` integers instead of a nested `image_size` object; same values, different shape.

Set `no_background: true` for item icons and requested-transparent skill icons.

## Verification

Internal pre-final checks (report only the constraints the user named, per `usage-reporting.md`):

- Output dimensions match the requested sheet size and divide exactly into the requested cells; `32px icons` means 32px per cell.
- Symbols/items fit the cell scale — no 64px-ish symbols, collapsed layouts, multi-object clusters in one cell, or gutters that change cell math.
- For explicit cell-size sheet requests, check the first visible icon/item against its intended cell before trusting automated crops: if the first item is already larger than the requested cell, the sheet fails even if the canvas size and crop hashes look plausible.
- Alpha matches the request: fully opaque for backgrounded sheets, clean transparency for `no_background: true` (after `background-removal.md` verification if removal was applied).
- No text-like marks, borders, frames, gutters, rounded corners, or slot styling unless requested. Metadata is not enough — a 1px opaque edge or a semantically unclear item passes structural checks while failing the art request; a human visual check is required for variety, readability at 32px, and recognizable semantics. For a request for unique items, inspect every cell for recognizable semantic duplication or an indistinguishable variant; do not report semantic uniqueness from pixel hashes alone.
- Item icons: crisp readable pixel art without mixels or smeared detail. Normal stair-stepped diagonals are fine; treat stepping as failure only when it harms 32px readability or shape clarity.
- Cropped cells pixel-hash-unique when uniqueness is required (does not prove semantic uniqueness).

On failure, report the failed candidate and ask how to proceed per SKILL.md Asset Integrity; safe background removal after `no_background: true` is the only default repair.
