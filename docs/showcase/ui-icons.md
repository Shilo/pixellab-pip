# UI Icons

Last reviewed: 2026-07-15.

<table>
  <tr>
    <td align="center"><img src="ui-icons/animal-face-emoji-5x5-16px.png" alt="16px animal-face emoji sheet, 5 by 5"></td>
  </tr>
</table>

UI icons are the small pictorial marks a game shows outside the inventory grid: emojis, chat and social reactions, status and buff markers, map pins, and toolbar glyphs. This page covers those. Inventory, equipment, loot, and pickup icons live in [item-icons.md](item-icons.md); ability and hotbar icons live in [skill-icons.md](skill-icons.md); the panels, frames, and slots that contain icons live in [gameplay-gui.md](gameplay-gui.md).

The animal-face emoji set is the first showcased example and the page's smallest-canvas workflow: 25 individually generated `16x16` emojis, each quantized to 8 colors, assembled into one `80x80` sheet. It is also the clearest demonstration of the `16px` Pixen route, which is the only image route that generates at `16x16` at all.

## Contents

- [Primary Example: 16px Animal Face Emoji Set](#primary-example-16px-animal-face-emoji-set)
- [Findings](#findings)
- [Showcase Assets](#showcase-assets)
- [Validation Notes](#validation-notes)

## Primary Example: 16px Animal Face Emoji Set

![16px animal-face emoji sheet, 5 by 5](ui-icons/animal-face-emoji-5x5-16px.png)

Original prompt:

```text
/pixellab-pip pixen create 25 unique 16x16 animal-face emojis in one shared flat style. each a different animal with its own vivid palette. simple geometry, flat shading, few colors, hard edges, transparent background. quantize each image to 8 colors and than create sprite sheet.
```

The animal-face emoji set demonstrates `create-image-pixen` at the smallest canvas PixelLab accepts. Twenty-five animals — fox, cat, dog, panda, tiger, lion, bear, wolf, rabbit, frog, owl, penguin, koala, monkey, pig, cow, sheep, deer, raccoon, hedgehog, elephant, giraffe, zebra, whale, and chick — each carry their own vivid palette while sharing one flat, black-outlined style. Each emoji was then quantized to at most 8 colors, and the 25 results were assembled into a `5x5` sheet.

Source inputs: text-only request. No reference images, style images, masks, or palette images were supplied.

Route: PixelLab REST v2 `create-image-pixen`, one call per animal. Pixen returns a single image per call, so a 25-emoji set is 25 jobs rather than one sheet generation. That is the deliberate tradeoff at this size: the alternative — a `generate-image-v2` batch culled down to 25 — is unreliable for clean icons below `32px`.

Pixen is also the route that makes `16x16` possible. Its `image_size` accepts a per-axis minimum of `16` with both axes divisible by `4`, and `16x16` clears its `32x32` area floor. `create-image-pixflux` shares the same area wording but rejects `16x16` outright, and REST `create-character-v3` and `create-character-pro` floor at `32`. See [../pixellab/pixellab-image-size-limits.md](../pixellab/pixellab-image-size-limits.md).

Prompt preparation: agent-optimized. Each `description` names one animal and its own palette, then closes with a shared style clause — `flat shading, hard edges, simple geometry, few colors, thick chunky pixels` — so the 25 separate jobs land in one style. The per-image style controls Pixen exposes natively (`detail`, `outline`, `view`, `direction`) carry the rest of the intent, so the prompt does not restate it.

Generation details:

| Field | Value |
|---|---|
| Image size | `16x16` per generated emoji |
| Output structure | `Separate images` (25 native `16x16` PNGs, one per call) |
| Showcase sheet | `5x5`, `80x80`, assembled from the quantized `16x16` PNGs |
| Detail | `low detail` |
| Outline | `single color black outline` |
| View / direction | `side` / `south` |
| Background | `no_background: true` |
| Sent seeds | `101` through `125`, one per animal |
| Reported cost | `$0.1958` total across 25 calls (~`$0.008` each) |

Local processing: each of the 25 originals was quantized to at most 8 colors with Aseprite `ColorQuantization` (octree, source-derived per image), round-tripped back to RGB PNG copies, then tiled into the `80x80` sheet with zero gutters. Quantization reduced palettes and assembly arranged cells; neither repainted, resized, nor redrew any pixel. Every pixel is PixelLab-generated.

Blueprint — replayable route and request bodies ([`animal-face-emoji-5x5-16px.blueprint.json`](ui-icons/animal-face-emoji-5x5-16px.blueprint.json)). The 25 Pixen calls are identical except for `description` and `seed`; the first, the two weakest, and the last are shown, with the remaining 21 elided for readability:

```json
[
  {
    "_comment": "25 unique 16x16 animal-face emojis in one shared flat style, each with its own vivid palette. One Pixen job per animal (Pixen returns a single image per call), then each cell is quantized to 8 colors and the set is assembled into a 5x5 / 80x80 sheet. Pixen accepts 16x16 (per-axis min 16, divisible by 4); create-image-pixflux does not - it rejects 16x16 on a 32x32 area floor.",
    "_comment_prompt": "/pixellab-pip pixen create 25 unique 16x16 animal-face emojis in one shared flat style. each a different animal with its own vivid palette. simple geometry, flat shading, few colors, hard edges, transparent background. quantize each image to 8 colors and than create sprite sheet.",
    "_pixellab": {
      "api_base_url": "https://api.pixellab.ai",
      "auth": {
        "type": "bearer",
        "env": "PIXELLAB_SECRET",
        "required_before_calls": true
      },
      "paid_call_policy": "explicit_user_run_request_required",
      "output_directory": "pixellab-pip-generations/animal-face-emoji-16px",
      "output_collision_policy": "stop_if_exists"
    },
    "TASK": {
      "instruction": "Confirm the current user explicitly asked to run this blueprint and that a PixelLab bearer token is configured locally, then create the empty output directory. This blueprint makes 25 paid Pixen calls; stop and ask if either condition is unmet.",
      "verify": "Run authority and credential presence are confirmed and the output directory exists and is empty."
    }
  },
  {
    "_comment": "Fox.",
    "POST /v2/create-image-pixen": {
      "description": "fox face, bright orange fur, white muzzle and cheeks, black nose, pointed ears with black tips, flat shading, hard edges, simple geometry, few colors, thick chunky pixels",
      "image_size": { "width": 16, "height": 16 },
      "detail": "low detail",
      "outline": "single color black outline",
      "view": "side",
      "direction": "south",
      "no_background": true,
      "seed": 101
    }
  },
  {
    "_comment": "Tiger. Weakest cell of the original run - stripes read as noise at 16px; vary the seed if a cleaner take is needed.",
    "POST /v2/create-image-pixen": {
      "description": "tiger face, vivid orange fur, black stripes, white muzzle, yellow eyes, flat shading, hard edges, simple geometry, few colors, thick chunky pixels",
      "image_size": { "width": 16, "height": 16 },
      "detail": "low detail",
      "outline": "single color black outline",
      "view": "side",
      "direction": "south",
      "no_background": true,
      "seed": 105
    }
  },
  {
    "_comment": "Whale. Weakest cell of the original run alongside the tiger - came out whale-shaped with a tail stub rather than a pure face; vary the seed if a tighter head crop is needed.",
    "POST /v2/create-image-pixen": {
      "description": "whale face, bright blue skin, white underside, small round eye, wide smiling mouth, flat shading, hard edges, simple geometry, few colors, thick chunky pixels",
      "image_size": { "width": 16, "height": 16 },
      "detail": "low detail",
      "outline": "single color black outline",
      "view": "side",
      "direction": "south",
      "no_background": true,
      "seed": 124
    }
  },
  {
    "_comment": "Chick.",
    "POST /v2/create-image-pixen": {
      "description": "baby chick face, vivid yellow fluffy feathers, tiny orange beak, round black eyes, flat shading, hard edges, simple geometry, few colors, thick chunky pixels",
      "image_size": { "width": 16, "height": 16 },
      "detail": "low detail",
      "outline": "single color black outline",
      "view": "side",
      "direction": "south",
      "no_background": true,
      "seed": 125
    }
  },
  {
    "TASK": {
      "instruction": "Save the 25 returned images in call order as 01-fox.png through 25-chick.png, naming each file for the animal its call requested.",
      "outputs": ["01-fox.png", "…", "25-chick.png"],
      "verify": "25 files exist, each 16x16 with a transparent background."
    }
  },
  {
    "TASK": {
      "instruction": "Quantize each of the 25 images to at most 8 colors independently, deriving each animal's palette from its own source pixels so the vivid per-animal palettes stay distinct. Preserve transparency and every silhouette; do not dither, repaint, or resize. Write RGB PNG copies into quantized-8color/ under the same filenames, leaving the originals untouched. Aseprite's ColorQuantization plus an indexed round-trip back to RGB satisfies this; note that Aseprite reserves one of the 8 palette slots for the transparent index, so visible colors land at 7 or fewer.",
      "inputs": ["01-fox.png", "…", "25-chick.png"],
      "outputs": ["quantized-8color/01-fox.png", "…", "quantized-8color/25-chick.png"],
      "verify": "Each quantized file is 16x16, uses at most 8 distinct colors among pixels with nonzero alpha, keeps its transparent background, and the 25 originals are unchanged."
    }
  },
  {
    "TASK": {
      "instruction": "Assemble the 25 quantized images into one spritesheet as a 5-column by 5-row grid of 16x16 cells in filename order, left to right then top to bottom, with no spacing, padding, or background. Preserve every source pixel and transparency; do not resize or repaint.",
      "inputs": ["quantized-8color/01-fox.png", "…", "quantized-8color/25-chick.png"],
      "outputs": ["animal-face-emoji-5x5-16px.png"],
      "verify": "The sheet is 80x80, each dimension divides evenly by 16 into a 5x5 grid, every cell matches its source file pixel-for-pixel in order, and transparency is preserved."
    }
  },
  {
    "TASK": {
      "instruction": "Create a separate inspection aid from a copy of the sheet: upscale it with nearest-neighbour, flatten it onto a dark backdrop for legibility, and overlay a contrasting one-pixel grid line at every 16px cell boundary. Label it 'Inspection aid - expected grid overlay' wherever it is shown. Keep it out of the final deliverables and never bake the grid into the sheet itself.",
      "inputs": ["animal-face-emoji-5x5-16px.png"],
      "outputs": ["animal-face-emoji-5x5-16px-inspection-grid.png"],
      "verify": "The overlay copy exists with grid lines at every cell boundary and animal-face-emoji-5x5-16px.png is unchanged."
    }
  }
]
```

Findings:

- Strongest `16px` emoji result observed: 25 recognizable animals, each in its own palette, holding one flat outlined style across 25 independent jobs.
- The shared style clause is what unifies separately generated icons. Without a fixed closing clause and fixed `detail`/`outline`/`view`/`direction` values, 25 individual calls have nothing binding them into a set.
- Pixen's native `detail: low detail` and `outline: single color black outline` do the work a `generate-image-v2` guardrail prompt has to describe in words. At `16x16` this matters more than at `32px`, because there is no room for the detail Pro tends to add.
- Naming the animal's palette inside each `description` ("bright orange fur, white muzzle", "cool slate grey fur, white muzzle") produced vivid per-animal color without any palette image or `forced_palette`.
- Two of 25 cells show `16px` semantic drift rather than route failure: the tiger's stripes read as noise, and the whale came out whale-shaped with a tail stub rather than a face. Both are the known small-canvas quality question, not a limit problem — see [pixellab-16px-item-sprite-generation-spike.md](../pixellab/pixellab-16px-item-sprite-generation-spike.md).
- Quantizing to 8 colors changed no alpha. Pixen's `16x16` output was already binary-alpha with hard edges, so there was no antialiasing for quantization to destroy.
- Aseprite reserves one of the 8 palette slots for the transparent index, so a `maxColors=8` source-derived reduction on transparent art yields at most 7 visible colors. Ask for 9 if exactly 8 visible colors are required.

## Findings

REST `create-image-pixen` is the best route currently showcased for `16px` UI icons and emojis. It is the only image route that generates at `16x16`, and its native `detail`, `outline`, `view`, and `direction` controls hold a flat readable style at a size where `generate-image-v2` adds detail the canvas cannot carry.

One emoji per call is the cost shape to plan around. Pixen returns a single image per call, so a set of N emojis is N jobs — cheap individually (~`$0.008` at `16x16`) but worth approving as a batch before starting. In exchange, every icon gets its own prompt, its own palette, and its own seed, which is what makes a set of individually distinct emojis possible at all.

Prompt language that helped:

- Naming one subject per call keeps the tiny canvas on a single readable shape; `16x16` has no room for a second object.
- A fixed style clause repeated verbatim across every call is what makes independently generated icons read as one set.
- Naming each subject's palette inline produces vivid per-icon color without a palette image.
- Leaving flatness, outline, and view to Pixen's own fields, rather than describing them in the prompt, keeps the `description` on content.

Future UI-icon showcases should live on this page when they cover other non-inventory icon surfaces, including status and buff markers, chat and social reaction sets, map pins and markers, and toolbar or settings glyphs.

## Showcase Assets

| Output | Stable showcase file |
|---|---|
| 16px animal-face emoji sheet | `docs/showcase/ui-icons/animal-face-emoji-5x5-16px.png` |

## Validation Notes

- The emoji sheet is exactly `80x80` and divides exactly into a `5x5` grid of `16x16` cells. It is showcased at native size, so it renders small; the underlying icons are `16x16` by request.
- It was generated as `25` original native `16x16` PNGs, one per Pixen call, then quantized and tiled locally into the showcase sheet (zero gutters).
- Each of the 25 emojis uses `5` to `7` visible colors, within the requested 8-color limit.
- All `25` cropped `16x16` cells are pixel-hash-unique. Pixel-hash uniqueness does not prove semantic uniqueness; visual review confirmed 25 distinct animals.
- Every sheet cell is pixel-identical to its quantized source file, in order.
- The sheet has alpha transparency. Across all 25 cells there are `0` partial-alpha pixels both before and after quantization, so edges are hard by generation, not by local thresholding.
- Raw cells carried `43` to `124` colors before quantization.
- Two cells are weaker on art quality: `05-tiger` (stripes read as noise) and `24-whale` (whale-shaped with a tail stub rather than a face). Both are flagged in the blueprint.
- Local work was limited to per-image palette quantization and sheet assembly. No repainting, resizing, cleanup, or procedural visual fixes were applied to the showcased pixels.
