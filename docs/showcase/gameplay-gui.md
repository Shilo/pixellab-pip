# Gameplay GUI

Last reviewed: 2026-06-25.

![Fantasy MMORPG GUI kit](gameplay-gui/gameplay-gui-fantasy-mmo-688x384.png)

This example shows prompt iteration for PixelLab Pip's REST v2 UI generator. The strongest result is the final fantasy MMORPG GUI sheet: a complete, highly usable transparent HUD kit with portrait frames, health and mana bars, action bars, bag slots, minimap frame, quest tracker, chat panel, parchment window, controls, icon frames, and currency buttons. Earlier iterations are kept below because they show why explicit component lists matter.

## Request

Initial:

```text
pip, create deep charcoal slate, framed by cool iron and ignited by sharp hits of heath-fire orange game UI at 344x192 resolution
```

Follow-up:

```text
create a new generation for full gameplay GUI:
- avatar
- health bar
- window
- various buttons
- other useful elements
```

Final follow-up:

```text
pip create a complete world of warcraft gui
```

## Best Example: Complete Fantasy MMORPG GUI

![Fantasy MMORPG GUI kit](gameplay-gui/gameplay-gui-fantasy-mmo-688x384.png)

This pass is the primary showcase example. Pip interpreted the named game as a broad high-fantasy MMORPG interface reference and routed the work to PixelLab REST v2 `generate-ui-v2`, while avoiding a direct copy of an existing game's protected interface.

Route: PixelLab REST v2 `generate-ui-v2`

Controls:

| Field | Value |
|---|---|
| Image size | `688x384` |
| Background | `no_background: true` |
| Seed | `250625` |
| Color palette | `dark iron, weathered stone, aged brass, leather brown, parchment tan, crimson health red, arcane blue, emerald green highlights` |
| Usage reported | `40` subscription generations |

Enhanced prompt sent as `description`:

```text
Complete original fantasy MMORPG pixel-art GUI kit, inspired by classic high-fantasy raid interfaces but not copying any existing game: ornate carved stone and dark iron frames with aged brass trim, glowing blue mana accents, red health accents, emerald quest accents, leather straps, small runic details, readable modular components arranged on one transparent sprite sheet. Include: player portrait frame, target portrait frame, health bar, mana bar, rage/energy resource bar, experience bar, action bar with twelve square spell slots, secondary action bar row, bag/inventory slot grid, minimap circular frame, quest tracker panel, parchment dialogue window, chat panel, tooltip frame, party member frames, raid-group compact frames, buff/debuff icon frames, menu buttons, checkboxes, sliders, tab headers, close buttons, gold/silver/copper currency icons, empty spell icon placeholders, decorative corners and separators. Clean game-ready UI assets, crisp 2D pixel art, consistent MMO HUD style, high contrast edges, no logos, no copyrighted symbols, no text labels, transparent background.
```

Request body:

```json
{
  "description": "Complete original fantasy MMORPG pixel-art GUI kit, inspired by classic high-fantasy raid interfaces but not copying any existing game: ornate carved stone and dark iron frames with aged brass trim, glowing blue mana accents, red health accents, emerald quest accents, leather straps, small runic details, readable modular components arranged on one transparent sprite sheet. Include: player portrait frame, target portrait frame, health bar, mana bar, rage/energy resource bar, experience bar, action bar with twelve square spell slots, secondary action bar row, bag/inventory slot grid, minimap circular frame, quest tracker panel, parchment dialogue window, chat panel, tooltip frame, party member frames, raid-group compact frames, buff/debuff icon frames, menu buttons, checkboxes, sliders, tab headers, close buttons, gold/silver/copper currency icons, empty spell icon placeholders, decorative corners and separators. Clean game-ready UI assets, crisp 2D pixel art, consistent MMO HUD style, high contrast edges, no logos, no copyrighted symbols, no text labels, transparent background.",
  "image_size": {
    "width": 688,
    "height": 384
  },
  "no_background": true,
  "color_palette": "dark iron, weathered stone, aged brass, leather brown, parchment tan, crimson health red, arcane blue, emerald green highlights",
  "seed": 250625
}
```

## Bad Example: Mood-Only Prompt

![First-pass charcoal heath-fire UI](gameplay-gui/gameplay-gui-mood-only-344x192.png)

This pass matched the desired palette and material mood, but it did not specify the gameplay elements that should appear. The output is a small UI sheet with a panel, a smaller frame, and a bar, rather than a full gameplay GUI kit.

Route: PixelLab REST v2 `generate-ui-v2`

Controls:

| Field | Value |
|---|---|
| Image size | `344x192` |
| Background | `no_background: true` |
| Color palette | `deep charcoal slate, cool iron gray, dark gunmetal, small sharp heath-fire orange glow accents` |
| Usage reported | `20` subscription generations |

Initial prompt:

```text
pip, create deep charcoal slate, framed by cool iron and ignited by sharp hits of heath-fire orange game UI at 344x192 resolution
```

Enhanced prompt sent as `description`:

```text
Pixel art game UI panel frame, 344x192 canvas, deep charcoal slate central panel, beveled cool iron border and corner brackets, sharp heath-fire orange glowing accents on rivets, notches, and thin trim lines, readable RPG HUD/menu frame, crisp hard pixel edges, high contrast, transparent outside the frame, no text, no characters, no background scene.
```

Request body:

```json
{
  "description": "Pixel art game UI panel frame, 344x192 canvas, deep charcoal slate central panel, beveled cool iron border and corner brackets, sharp heath-fire orange glowing accents on rivets, notches, and thin trim lines, readable RPG HUD/menu frame, crisp hard pixel edges, high contrast, transparent outside the frame, no text, no characters, no background scene.",
  "image_size": {
    "width": 344,
    "height": 192
  },
  "no_background": true,
  "color_palette": "deep charcoal slate, cool iron gray, dark gunmetal, small sharp heath-fire orange glow accents"
}
```

## Earlier Good Example: Component-Specific Prompt

![Gameplay GUI kit](gameplay-gui/gameplay-gui-component-specific-688x384.png)

Route: PixelLab REST v2 `generate-ui-v2`

Controls:

| Field | Value |
|---|---|
| Image size | `688x384` |
| Background | `no_background: true` |
| Color palette | `deep charcoal slate, cool iron gray, dark gunmetal, blackened steel, sharp heath-fire orange ember accents` |
| Usage reported | `40` subscription generations |

Initial prompt:

```text
create a new generation for full gameplay GUI:
- avatar
- health bar
- window
- various buttons
- other useful elements
```

Enhanced prompt sent as `description`:

```text
Complete pixel art gameplay GUI kit sheet on a 688x384 canvas, deep charcoal slate and cool iron fantasy interface with sharp heath-fire orange accent lights. Include a square avatar portrait frame, horizontal health bar, mana or stamina bar, large ornate window/dialogue panel, inventory slot frame, minimap frame, quest/objective panel, several reusable buttons in different sizes, icon button frames, tabs, dividers, corner brackets, scroll arrows, and small useful HUD elements. Cohesive RPG action game UI, crisp hard pixel edges, beveled iron trim, dark slate surfaces, bright orange ember highlights, organized as separate usable elements on transparent background, no readable text, no characters, no scene background.
```

Request body:

```json
{
  "description": "Complete pixel art gameplay GUI kit sheet on a 688x384 canvas, deep charcoal slate and cool iron fantasy interface with sharp heath-fire orange accent lights. Include a square avatar portrait frame, horizontal health bar, mana or stamina bar, large ornate window/dialogue panel, inventory slot frame, minimap frame, quest/objective panel, several reusable buttons in different sizes, icon button frames, tabs, dividers, corner brackets, scroll arrows, and small useful HUD elements. Cohesive RPG action game UI, crisp hard pixel edges, beveled iron trim, dark slate surfaces, bright orange ember highlights, organized as separate usable elements on transparent background, no readable text, no characters, no scene background.",
  "image_size": {
    "width": 688,
    "height": 384
  },
  "no_background": true,
  "color_palette": "deep charcoal slate, cool iron gray, dark gunmetal, blackened steel, sharp heath-fire orange ember accents"
}
```

## Outputs

| File | Purpose |
|---|---|
| [`gameplay-gui/gameplay-gui-fantasy-mmo-688x384.png`](gameplay-gui/gameplay-gui-fantasy-mmo-688x384.png) | Primary transparent fantasy MMORPG GUI kit sheet. |
| [`gameplay-gui/gameplay-gui-mood-only-344x192.png`](gameplay-gui/gameplay-gui-mood-only-344x192.png) | First-pass mood-focused UI sheet. Useful as a bad example for underspecified gameplay GUI requests. |
| [`gameplay-gui/gameplay-gui-component-specific-688x384.png`](gameplay-gui/gameplay-gui-component-specific-688x384.png) | Earlier transparent full gameplay GUI kit sheet. |

## Validation Notes

Final verification:

- PNG dimensions: `688x384px`.
- Pixel format: `Format32bppArgb`.
- Primary output has transparent background and separate GUI elements arranged as a reusable sheet.
- Primary output includes portrait frames, status bars, action bars, bag grid, minimap frame, quest tracker, chat panel, parchment panel, controls, icon frames, and currency buttons.
