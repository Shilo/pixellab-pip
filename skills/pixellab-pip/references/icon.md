# Icon And Icon Sheet Generation

Use this reference for skill/ability/spell/action-bar/hotbar icons and for inventory item/equipment/loot/pickup/consumable icons, single or sheets, including transparent, no-border, and split-PNG requests.

## Route

### Size Routing (Decide First)

- **Single `16px` icon (one `16x16` image, one item) → `create-image-pixen` (the "new" / Pixen model). Required for a clean 16px icon.** At `16px`, `generate-image-v2` (Pro) gives inconsistent outlines (~62% edge coverage), baked shadows, and orphan pixels — unreliable for a clean single icon. Pixen's `detail`/`outline` controls give consistent outlines and readable shapes. Recipe: `detail: low detail`, `outline: single color black outline`, `view` to suit the subject, `no_background: true`; Pixen returns one image per call, so one item per job. Optional polish: clamp the palette to ~16–32 colors (see `aseprite-cli.md`) — Pixen otherwise ships many shades.
- **`16px` sheet or large varied set →** either Pixen one-item-per-job then assemble locally (clean, but N paid jobs — get batch approval per SKILL.md), or a guardrailed Pro `generate-image-v2` batch (one job returns ~64 native `16px` candidates) then cull the muddy ones. State the tradeoff and let the user choose; a Pro `16px` batch is variety-to-cull, not clean-per-icon.
- **17–31px:** untested here; lean on Pixen's `detail`/`outline` controls toward 16px and validate a small Pro test toward 32px before trusting a sheet.
- **`32px+` icons → `generate-image-v2` (Pro)**, per the guidance below. Guardrail the prompt (bold single-color black outline, low detail, limited palette, no gradients / noise / stray pixels); Pro is strongest at `32px+`.

**Confirmation:** because `16px` overrides the Pro-first default, confirm the route with the user before generating a `16px` icon via Pixen — unless the user explicitly named the new/Pixen model, then proceed. This confirms the route only; cost-routing and batch-approval rules still apply.

For `32px+` icons, use REST v2 `POST /generate-image-v2` first for icon sheets and for single icons when quality or candidate variety matters. It is a Pro-family route: on a cheap/budget request, read `cost-routing.md` first and offer a lower-cost Pixen comparison or a smaller test before a full Pro sheet.

Do not default to object generation (`create_1_direction_object` / `create-1-direction-object`), `create_tiles_pro`, `generate-ui-v2`, or `create-ui-asset` for icons. Object routes produced noisy/downscaled-looking icons with broken contours and weak 32px clarity in testing — avoid them for any icon request, even when the subject is a weapon, potion, or prop. Use UI routes only when the user asks for the slot, button, panel, frame, or container UI itself. (`create-image-pixen` is governed by Size Routing above, not this avoid-list: it is required at `16px` and optional otherwise.)

At `32px+`, use `create-image-pixen` when the user explicitly values a cheap attempt, exact `detail`/`outline`/`view` controls, or fast iteration over candidate variety (at `16px` it is required — see Size Routing). Verify Pixen results read as the requested icon type; in testing it gave clean contours but, on multi-item sheets, semantically unclear or duplicated items and sheet-layout drift.

Background defaults differ by icon type:

- Skill/ability icons: backgrounded sheets (`no_background: false`) are the validated default — rich full-bleed painted cells. Transparent skill icons are a less-validated shape; use `no_background: true` only when clearly requested.
- Item/inventory icons: transparent (`no_background: true`) is the default — inventory icons usually need alpha.

If `no_background: true` was sent but the output kept a background, read `background-removal.md` and apply safe removal when it preserves the art.

## Canvas Sizing

For plural or complete sets, `32x32 icons` is the per-icon cell size, not the canvas:

- `8x8` / 64 icons at 32px each → `image_size: { "width": 256, "height": 256 }`.
- `4x4` / 16 icons at 32px each → `image_size: { "width": 128, "height": 128 }`.
- A `32x32` `image_size` fits only a single icon. At small sizes `generate-image-v2` may return a multi-candidate batch; read `create-image-pro.md` for native-size diversity, no-label, and view guidance, then present candidates and select after visual review.

Generate the sheet first, then verify the original output against the requested cell size. If symbols come out 64px-ish, the layout collapses, or gutters break the cell math, report a failed candidate — do not resize or reassemble it into a claimed final.

## Prompt Pattern

Preserve sheet language for complete sheets; do not rewrite the request as separate standalone images unless the user asks for separate generated files. Follow SKILL.md Text Preparation: content only, no operation language, no canvas size or transparency wording already carried by `image_size`/`no_background`.

Backgrounded skill-icon sheet starting point:

```text
Complete 8 by 8 sheet of 64 unique fantasy RPG skill icons for game UI, 8 columns and 8 rows, each cell a readable 32x32 icon, perfectly aligned edge-to-edge with no spacing, overlap, cropped icons, dividers, or drawn grid. Rich full-bleed illustrated miniature backgrounds behind clear centered pictorial symbols: flames, ice shards, lightning bolts, shields, daggers, arrows, skulls, leaves, spirits, portals, stars, wings, claws, masks, potions, celestial beams, and aura effects. No text, letters, words, numbers, labels, captions, handwriting, fake writing, runes, glyphs, or alphabet-like shapes. Varied abilities across elemental magic, weapon attacks, healing, protection, stealth, curses, nature, summoning, movement, utility, poison, holy, shadow, and dragon breath. No terrain tiles, inventory sheet, borders, frames, UI slots, rounded corners, watermark, or separating lines. Palette: sapphire blue, ember orange, moonlit violet, emerald green, gold highlights.
```

Transparent item-icon sheet starting point:

```text
Complete 8 by 8 sheet of 64 unique fantasy RPG inventory item icons, 8 columns and 8 rows, each cell a readable 32x32 item, perfectly aligned with no spacing, overlap, cropped items, dividers, or drawn grid. Pixel art with clear centered object silhouettes, crisp hard edges, low visual noise, limited palette, consistent high-fantasy inventory style. Include varied common RPG inventory categories: melee weapons, ranged weapons, shields, armor, helmets, jewelry, potions, scrolls, books, food, coins, gems, ores, herbs, monster parts, tools, keys, chests, bags, bombs, and arrows. No text, letters, words, numbers, labels, captions, fake writing, runes, glyphs, UI slots, buttons, borders, frames, rounded corners, watermark, terrain tiles, or decorative grid lines.
```

Adapt theme, subject list, and palette; keep the sheet-layout, per-cell-size, no-text, and no-border clauses. A validated fire-magic skill sheet used a 1994-character description at 256x256 — themed sets still work better as one cohesive sheet than as separate 32x32 generations.

Anchors for known failure modes (use only the ones that apply): `Pictorial symbols only`; `rich full-bleed illustrated miniature background` / `Fully opaque, every pixel painted` (backgrounded only); `No borders, frames, UI slots, rounded corners, dividers, watermark`; `No black outlines around icon square edges`.

Avoid positive mentions of `rune`, `glyph`, `sigil`, `spellbook labels`, `UI slot`, `button`, `frame`, `border`, or `card` unless requested — they create text-like marks or slot styling. Use them only in negative clauses. For sheets, avoid `one icon per image` / `standalone icon` phrasing — it pushes isolated symbols on flat backgrounds.

Item-icon specifics:

- Prefer category coverage over an exact 64-item list for the first candidate; long exact lists over-constrain and produce noisier results. If exact coverage is required, run it as a follow-up candidate and compare.
- Do not over-prompt outline instructions unless the user asks for a specific outline style; spotty or broken contours are a failed candidate, not a prompt-patch target.

## Request Body

```json
{
  "description": "<optimized complete-sheet prompt>",
  "image_size": { "width": 256, "height": 256 },
  "no_background": false
}
```

Set `no_background: true` for item icons and requested-transparent skill icons. When the endpoint exposes `seed` and the user did not provide one, send an agent-chosen non-zero seed and record it per `usage-reporting.md`.

## Verification

Internal pre-final checks (report only the constraints the user named, per `usage-reporting.md`):

- Output dimensions match the requested sheet size and divide exactly into the requested cells; `32px icons` means 32px per cell.
- Symbols/items fit the cell scale — no 64px-ish symbols, collapsed layouts, multi-object clusters in one cell, or gutters that change cell math.
- For explicit cell-size sheet requests, check the first visible icon/item against its intended cell before trusting automated crops: the visible object must fit inside that cell's pixel bounds without crossing into adjacent cells. If the first item is already larger than the requested cell, the sheet fails even if the canvas size and crop hashes look plausible.
- Alpha matches the request: fully opaque for backgrounded sheets, clean transparency for `no_background: true` (after `background-removal.md` verification if removal was applied).
- No text-like marks, borders, frames, gutters, rounded corners, or slot styling unless requested. Metadata is not enough — a 1px opaque edge or a semantically unclear item passes structural checks while failing the art request; a human visual check is required for variety, readability at 32px, and recognizable semantics. For a request for unique items, inspect every cell for recognizable semantic duplication or an indistinguishable variant; do not report semantic uniqueness from pixel hashes alone.
- Item icons: crisp readable pixel art without mixels or smeared detail. Normal stair-stepped diagonals are fine; treat stepping as failure only when it harms 32px readability or shape clarity.
- Cropped cells pixel-hash-unique when uniqueness is required (does not prove semantic uniqueness).

On failure, report the failed candidate and ask how to proceed per SKILL.md Asset Integrity; safe background removal after `no_background: true` is the only default repair.
