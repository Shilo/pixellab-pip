# PixelLab 16px Chibi Character Generation Spike

Last reviewed: 2026-08-05.

Purpose: find the smallest reliable prompt and route for a clean, flat, low-detail
16px character with a cozy mobile-game chibi read. This spike starts from the
earlier local experiments in
[`chibi-soldier-16`](../../pixellab-pip-generations/chibi-soldier-16/) and
[`front-facing-dark-coat-16x16`](../../pixellab-pip-generations/front-facing-dark-coat-16x16/).
It is research, not a canonical runtime routing rule.

## Current recommendation

For this specific target—a native 16x16 character with a very large, simple
chibi head and a compact, flat body—start with Pro v2 and review its candidate
sweep. In the original comparison plus two later strict prompt rounds, Pro was
the only route that repeatedly approached the desired head-to-body silhouette
and the visually flat major color masses. Its 64 candidates make review and
selection part of the route, rather than a minor convenience.

Pixen remains a valid native-size one-shot route, but it is not the leading
route for this target. In the later side-by-side review it read narrower, less
chibi, and more detailed than the strongest Pro candidates. The earlier Pixen
recommendation came from comparing Pixen with Pro candidate 01 only; it should
not be treated as a general model ranking.

Neither text-only model met a literal low palette cap: even the stricter
five-color prompt produced 52–62 opaque colors per Pro candidate and 53 for
Pixen. Therefore Pro is the best raw generator for this silhouette and visual
flatness, not a direct substitute for an indexed four- or eight-color output.
Apply and label a palette-reduction pass when the palette limit itself is a
deliverable requirement.

If a single native 16x16 probe is more important than a candidate sweep, use
Pixen:

- MCP `create_image_pixen` when available; otherwise REST
  `POST /v2/create-image-pixen`.
- Use `16x16`, `detail: low detail`, `view: low top-down`,
  `direction: south`, `no_background: true`, and a single-color or selective
  outline.
- Keep the prompt short and structural. Say exactly what the head and clothing
  masses are, then explicitly ban props, extra characters, texture, gradients,
  dithering, highlights, and internal noise.
- Expect the result to be readable before it is truly palette-flat. The live
  Pixen output in this spike used 48 opaque colors despite the low-detail
  controls; quantization is the next experiment, not part of this result.

For the cleanest style when 24px output is acceptable, use managed
`create_character` in standard mode. It produced the cleanest flat color
clusters and consistent directional identity, but `size: 16` returned 24x24
rotation canvases. Do not crop or resize that output and call it native 16px.

Pro exposes no structured `detail`, `outline`, `shading`, or palette controls;
its prompt controls are soft and the raw files remain color-noisy. Do not
resize a larger output to make it appear native 16px, and do not describe a
quantized Pro result as raw model output.

Do not use BitForge as the default for this target. Its native 16x16 call
completed, but the result was a muddy blob even with `coverage_percentage`.
PixFlux is a poor strict-16px route: the live MCP rejected 16x16 and the
smallest accepted 32x32 test rendered a much larger, softer subject.

## Target-style research

Public store descriptions call Pickaxe King Island a relaxing pixel-graphics
tycoon/farming game with farming, mining, dungeons, the Fox Knight, monsters,
and a large costume collection. Public screenshot pages show small characters
that need to read quickly inside bright island, farm, and dungeon scenes. That
supports the following working interpretation of the requested visual target:

- cozy, game-like pixel clusters rather than illustration-level rendering;
- a clear outer silhouette and a few large clothing/color masses;
- cute, exaggerated proportions with a face that survives at tiny size;
- simple palette relationships and readable separation from the environment;
- character identity carried by hair shape, body color, and one clothing block,
  not by equipment or micro-detail.

This is a style description, not an attempt to reproduce a specific character.
The store and screenshot pages were used only for research. No store image,
web image, attached image, or prior generated sprite was supplied to any
PixelLab call in this spike.

Sources:

- [Google Play listing](https://play.google.com/store/apps/details?hl=en_US&id=com.rogueuniongames.pickaxekingisland)
- [Apple App Store listing](https://apps.apple.com/us/app/pickaxe-king-island/id6738040300)
- [Screenshot gallery and feature summary](https://mwm.ai/apps/pickaxe-king-island/6738040300)

## Proportion decision: two heads, not one and a half

For a 16px full-body game sprite, use approximately two heads tall:

| Part | Working budget |
|---|---:|
| Head and hair mass | 7–8px |
| Face detail | 1–2 eye pixels plus skin cluster |
| Torso and clothing | 5–6px |
| Feet / lower edge | 1–2px |

One-and-a-half heads makes the head about 9–10px tall and leaves too little
room for a readable torso, clothing break, and feet. It is useful for an
emote or portrait-like sprite, not for this full-body character target. The
two-head choice is an MVP construction heuristic, not a claim about the
game's source assets.

## Test matrix

All tests used one original fictional island worker prompt family. No image
input fields were sent: no `reference_images`, `style_image`, `init_image`,
`color_image`, `reference_image_base64`, or palette image.

| Route | Requested / observed size | Output | Cost shown by PixelLab | Result |
|---|---|---|---:|---|
| `create_character` standard | requested 16; observed 24x24 rotations | 4 directions | 1 generation | Cleanest flat style and strongest identity consistency; not native 16px |
| Pixen | 16x16 / 16x16 | 1 image | 1 generation | Best strict-size starting point; readable but still 48 opaque colors |
| Pro v2 | 16x16 / 16x16 | 64 candidates | 20 generations | Useful variation sweep; 52–62 colors per candidate and more face/edge noise |
| BitForge | 16x16 / 16x16 | 1 image | 1 generation | Coverage filled the canvas but the result was muddy and poorly separated |
| PixFlux | 16x16 rejected; 32x32 / 32x32 | 1 image | 1 generation | Smallest accepted canvas rendered a roughly 30px-tall subject; too soft/detailed |

### Strict flat-chibi retry, 2026-08-05

Two additional text-only rounds tested the same three native-size routes with
an aggressively constrained character: an approximately two-head-tall,
front-facing chibi; a 7–8px head; a compact tunic body; no hat, weapon, tool,
or accessory; flat regions; no texture, highlights, or dithering. The second
round also named an exact five-color palette. No reference, style, init, or
palette image was sent to any model.

| Route | Native size | Observed result | User review |
|---|---|---|---|
| Pro v2 | 16x16 | 64 candidates per round; 54–63 opaque colors in round one and 52–62 in round two | Best match: the only route to consistently approach the oversized, blocky chibi head and flat major masses. |
| Pixen | 16x16 | 1 candidate per round; 57 then 53 opaque colors | More detailed and narrower; did not approach the target head shape as closely as Pro. |
| BitForge | 16x16 | 1 candidate per round; 25 then 27 opaque colors | Still muddy or visually busy despite its lower raw color count; not competitive for this target. |

This reverses the earlier Pixen-first recommendation for this narrowly defined
style. The change is not a contradiction in native-size support: both Pro and
Pixen returned native 16x16 files. It reflects better like-for-like review,
including Pro's broader candidate sweep and a stricter prompt family. It is a
target-specific finding, not a claim that Pro is better for every 16px asset.

The observed opaque-color counts are diagnostic, not a quality score:

| Output | Opaque pixels | Opaque colors | Alpha bbox |
|---|---:|---:|---|
| Pixen 16x16 | 98 | 48 | (3,1)–(11,14) |
| Pro candidate 01 | 136 | 61 | (3,1)–(12,15) |
| BitForge 16x16 | 146 | 21 | (1,0)–(14,14) |
| PixFlux 32x32 | 320 | 43 | (9,1)–(24,30) |
| create_character south | 141 | 20 | (7,2)–(16,20) |

BitForge has fewer colors numerically than Pixen, but its color clusters are
less legible. The cleanest result is therefore not the result with the fewest
colors; silhouette and cluster separation still matter.

## Evidence files

The full live run is preserved in
[`16px-chibi-character-model-spike-2026-08-04`](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/).

- [Model comparison review sheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/model-comparison-review-contact-sheet.png)
- [8-color comparison review sheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/model-comparison-8-colors-review-contact-sheet.png)
- [4-color comparison review sheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/model-comparison-4-colors-review-contact-sheet.png)
- [Pixen 16x16 review preview](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pixen-16x16/pixen-16x16-review-preview.png)
- [Pixen 16x16 spritesheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pixen-16x16/pixen-16x16-spritesheet.png)
- [Pixen blueprint](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pixen-16x16/pixen-16x16.blueprint.json)
- [Pro 64-candidate review sheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pro-16x16/pro-16x16-review-contact-sheet.png)
- [Pro native 8x8 spritesheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pro-16x16/pro-16x16-spritesheet.png)
- [Pro blueprint](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pro-16x16/pro-16x16.blueprint.json)
- [BitForge review preview](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/bitforge-16x16/bitforge-16x16-review-preview.png)
- [BitForge blueprint](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/bitforge-16x16/bitforge-16x16.blueprint.json)
- [PixFlux 32x32 review preview](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pixflux-32x32/pixflux-32x32-review-preview.png)
- [PixFlux blueprint](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/pixflux-32x32/pixflux-32x32.blueprint.json)
- [create_character directional review sheet](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/create-character-size16/create-character-24px-review-contact-sheet.png)
- [create_character blueprint](../../pixellab-pip-generations/16px-chibi-character-model-spike-2026-08-04/create-character-size16/create-character-size16.blueprint.json)

The native spritesheets and directional sheet are local assemblies of
PixelLab output. Verification compared each native cell to its source image
pixel-for-pixel; review contact sheets and grid overlays are separate
inspection aids.

The lower row of each current three-column comparison sheet is the strict
flat-chibi retry: Pro candidate 05, Pixen, then BitForge. Each source is a
native 16x16 file displayed at the same 4x nearest-neighbor scale. The 8- and
4-color sheets are derived palette reductions, stored separately from their
raw sources.

## MVP prompt

This is the shortest tested prompt that still carries the important constraints.
Replace only the role, hair color, clothing color, and pants color.

~~~
Original fictional front-facing south-facing idle game character sprite:
a cheerful island worker with simple coral hair, a teal tunic, warm tan face
and tiny ochre trousers. Full body, centered, approximately two heads tall:
oversized head about half the 16px height, compact body. Head and clothes
only; tiny simple feet are okay. No hat, no weapon, no tool, no held item, no
backpack, no shield, no armor, no accessory, no scenery, no text, no shadow.
Native 16x16 sprite, clean chunky pixel clusters, hard 1-pixel edges, flat
solid color regions, 5 to 8 colors total, one simple face with at most two eye
pixels, no gradients, no dithering, no highlights, no texture, no internal
noise, transparent background.
~~~

Use these structured settings where the route exposes them:

~~~
{
  "detail": "low detail",
  "outline": "single color outline",
  "shading": "flat shading",
  "view": "low top-down",
  "direction": "south",
  "no_background": true,
  "width": 16,
  "height": 16
}
~~~

For `create_character`, use standard mode, four directions for a quick
comparison, `size: 16`, and the documented proportions preset
`{"type":"preset","name":"chibi"}`. Expect the observed 24x24 canvas behavior
until PixelLab exposes a smaller managed-character size.

For Pro, keep the same text but do not pretend that `flat`, `low detail`,
or `5 to 8 colors` are structured controls: Pro v2 exposes no matching
`detail`, `outline`, `shading`, or palette field. The prompt is the only
control in this comparison.

## What changed from the earlier work

The earlier soldier and dark-coat experiments were useful because they proved
that PixelLab can produce native 16px humanoid silhouettes. They also showed
the failure mode: prompt language such as “low detail” is not enough when the
subject description asks for equipment, costume motifs, or reference-driven
identity. The new MVP prompt removes every optional prop and reduces identity
to hair, face, one tunic mass, pants, and feet.

The strongest practical changes are:

1. Say `head and clothes only` before the negative list.
2. Ban weapons, hats, tools, armor, accessories, backpacks, scenery, text,
   shadows, texture, gradients, dithering, highlights, and internal noise.
3. Give the model a pixel budget: `5 to 8 colors total`, `one simple face`,
   `at most two eye pixels`, and `hard 1-pixel edges`.
4. Say `approximately two heads tall` instead of only saying `chibi`.
5. Use native canvas fields rather than relying on the word `small`.
6. Review the actual image. A correct 16x16 canvas does not prove a flat
   16px character, and a low color count does not prove clean clusters.

## Next experiment

Do not add more descriptive detail yet. The next controlled test should take
the selected Pro candidate and a Pixen control, then compare:

- no quantization;
- a hard 8-color reduction;
- a hard 6-color reduction;
- a manually chosen palette reduction with nearest-neighbor preservation.

Keep the source PNGs untouched and label reduced versions as derived
experiments. Four- and eight-color review previews now exist, but this remains
an open quality test: evaluate cluster cleanup and silhouette preservation,
not only the numerical palette count.
