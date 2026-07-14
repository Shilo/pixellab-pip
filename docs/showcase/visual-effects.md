# Visual Effects

Last reviewed: 2026-07-10.

<table>
  <tr>
    <td><img src="visual-effects/spark-explosion.gif" alt="Top-down spark flash explosion animation"></td>
    <td><img src="visual-effects/void-implosion.gif" alt="Top-down void magic implosion animation"></td>
  </tr>
  <tr>
    <td><img src="visual-effects/fire-explosion.gif" alt="Top-down fiery explosion animation"></td>
    <td><img src="visual-effects/toxic-explosion.gif" alt="Top-down toxic acid explosion animation"></td>
  </tr>
</table>

PixelLab Pip turned a single request for a variety of unique top-down explosions into a two-step workflow per effect: generate a 32px source sprite, then animate it. The user asked for 32px explosion visual effects that were all unique and top-down. A single Create Image Pro call at 32px returned 64 distinct candidate variations, which were manually compiled into an 8x8 spritesheet. That spritesheet was then used as the reference frame for an Animate with Text (new) pass, producing a looping explosion animation for each theme.

## Contents

- [Spark Explosion](#spark-explosion)
- [Void Implosion](#void-implosion)
- [Fire Explosion](#fire-explosion)
- [Toxic Explosion](#toxic-explosion)
- [Workflow](#workflow)
- [Findings](#findings)
- [Showcase Assets](#showcase-assets)
- [Validation Notes](#validation-notes)

## Request

```text
/pixellab-pip create 32px explosion visual effects. must be a variety of top down explosions that are all unique.
```

## Spark Explosion

<table>
  <tr>
    <td><img src="visual-effects/spark-explosion.gif" alt="Top-down spark flash explosion animation"></td>
    <td><img src="visual-effects/spark-explosion.png" alt="Spark explosion source spritesheet"></td>
  </tr>
</table>

Request intent: a small, bright yellow and white spark flash with a star-shaped glint, viewed straight down.

Source inputs: text-only request for the source sprite. The animation step used the locally assembled 32px spritesheet as its reference frame.

Route: REST v2 `generate-image-v2` (Create Image Pro) for the source sprite, then REST v2 `animate-with-text-v3` (Animate with Text (new)) for the animation.

Prompt preparation: the description named a small radial burst of yellow and white sparks and a glinting star-shaped flash, keeping the top-down orthographic and radial ground-plane wording. The animation `action` pluralized the subject to `explosions`.

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet; the returned animation frames were assembled into a transparent GIF, then hand-polished by reordering frames and deleting redundant ones.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames after polish | `8` |

Blueprint — replayable route and request body ([`spark-explosion.blueprint.json`](visual-effects/spark-explosion.blueprint.json)):

```json
[
  {
    "_comment": "One generate-image-v2 call at 32x32 returns 64 unique top-down candidate variations; they were tiled locally into an 8x8 spritesheet (spark-explosion.png) used as the animation reference frame.",
    "_comment_prompt": "/pixellab-pip create 32px explosion visual effects. must be a variety of top down explosions that are all unique.",
    "POST /v2/generate-image-v2": {
      "description": "bright spark flash pop explosion viewed top-down orthographic looking straight down, small radial burst of yellow and white sparks and glinting star-shaped flash on the ground plane, circular symmetrical blast",
      "image_size": {
        "width": 32,
        "height": 32
      },
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use all 64 images returned by the immediately preceding PixelLab call in returned order. Arrange them row-major into an 8 by 8 spritesheet with no margins, spacing, resizing, repainting, or quantization.",
      "outputs": ["spark-explosion.png"],
      "verify": "spark-explosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell is pixel-identical to its corresponding returned image and transparency is preserved."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 total (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "spark-explosion.png",
      "action": "bright spark flash pop explosions viewed top-down orthographic looking straight down, small radial burst of yellow and white sparks and glinting star-shaped flash on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use the nine animation frames returned by the immediately preceding PixelLab call. Reorder the whole frames by visual progression into the strongest top-down spark loop, remove one redundant near-duplicate, and assemble a transparent 256x256 GIF at 0.12 seconds per frame. Do not resize or repaint frame content.",
      "outputs": ["spark-explosion.gif"],
      "verify": "spark-explosion.gif is exactly 256x256 with eight 0.12-second frames, uses only returned frame content apart from GIF palette encoding, and preserves transparency."
    }
  }
]
```

Findings:

- Reads as a crisp top-down radial spark burst with a clear yellow-white center and star-shaped glint.
- The strongest of the four effects; used as the page and README gallery thumbnail.

## Void Implosion

<table>
  <tr>
    <td><img src="visual-effects/void-implosion.gif" alt="Top-down void magic implosion animation"></td>
    <td><img src="visual-effects/void-implosion.png" alt="Void implosion source spritesheet"></td>
  </tr>
</table>

Request intent: a purple and violet arcane implosion with a black core and swirling shadow tendrils, viewed straight down.

Source inputs: text-only request for the source sprite. The animation step used the locally assembled 32px spritesheet as its reference frame.

Route: REST v2 `generate-image-v2` (Create Image Pro) for the source sprite, then REST v2 `animate-with-text-v3` (Animate with Text (new)) for the animation.

Prompt preparation: the description named purple and violet arcane energy, a black core, and swirling shadow tendrils, keeping the top-down orthographic and radial ground-plane wording. The animation `action` pluralized the subject to `implosions`.

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet; the returned animation frames were assembled into a transparent GIF, then hand-polished by reordering frames and deleting redundant ones.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames after polish | `7` |

Blueprint — replayable route and request body ([`void-implosion.blueprint.json`](visual-effects/void-implosion.blueprint.json)):

```json
[
  {
    "_comment": "One generate-image-v2 call at 32x32 returns 64 unique top-down candidate variations; they were tiled locally into an 8x8 spritesheet (void-implosion.png) used as the animation reference frame.",
    "_comment_prompt": "/pixellab-pip create 32px explosion visual effects. must be a variety of top down explosions that are all unique.",
    "POST /v2/generate-image-v2": {
      "description": "dark void magic implosion viewed top-down orthographic looking straight down, radial burst of purple and violet arcane energy with black core, swirling shadow tendrils and magic sparks on the ground plane, circular symmetrical blast",
      "image_size": {
        "width": 32,
        "height": 32
      },
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use all 64 images returned by the immediately preceding PixelLab call in returned order. Arrange them row-major into an 8 by 8 spritesheet with no margins, spacing, resizing, repainting, or quantization.",
      "outputs": ["void-implosion.png"],
      "verify": "void-implosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell is pixel-identical to its corresponding returned image and transparency is preserved."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 total (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "void-implosion.png",
      "action": "dark void magic implosions viewed top-down orthographic looking straight down, radial burst of purple and violet arcane energy with black core, swirling shadow tendrils and magic sparks on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use the nine animation frames returned by the immediately preceding PixelLab call. Reorder the whole frames by visual progression into the strongest top-down implosion loop, remove two redundant near-duplicates, and assemble a transparent 256x256 GIF at 0.12 seconds per frame. Do not resize or repaint frame content.",
      "outputs": ["void-implosion.gif"],
      "verify": "void-implosion.gif is exactly 256x256 with seven 0.12-second frames, uses only returned frame content apart from GIF palette encoding, and preserves transparency."
    }
  }
]
```

Findings:

- Reads as a top-down arcane implosion with a dark core and swirling violet tendrils.
- Polishing trimmed it to 7 frames after removing redundant near-duplicate frames.

## Fire Explosion

<table>
  <tr>
    <td><img src="visual-effects/fire-explosion.gif" alt="Top-down fiery explosion animation"></td>
    <td><img src="visual-effects/fire-explosion.png" alt="Fire explosion source spritesheet"></td>
  </tr>
</table>

Request intent: a fiery orange and red explosion with a bright yellow-white core, viewed straight down.

Source inputs: text-only request for the source sprite. The animation step used the locally assembled 32px spritesheet as its reference frame.

Route: REST v2 `generate-image-v2` (Create Image Pro) for the source sprite, then REST v2 `animate-with-text-v3` (Animate with Text (new)) for the animation.

Prompt preparation: the shared request named the visual result — orange and red flames, bright yellow-white core, smoke and ember debris — and forced a top-down orthographic view with radial ground-plane spread so the effect reads as a ground impact rather than a side-view blast. The animation `action` reused the sprite description with the subject pluralized to `explosions`.

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet; the returned animation frames were assembled into a transparent GIF, then hand-polished by reordering frames and deleting redundant ones.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames after polish | `9` |

Blueprint — replayable route and request body ([`fire-explosion.blueprint.json`](visual-effects/fire-explosion.blueprint.json)):

```json
[
  {
    "_comment": "One generate-image-v2 call at 32x32 returns 64 unique top-down candidate variations; they were tiled locally into an 8x8 spritesheet (fire-explosion.png) used as the animation reference frame.",
    "_comment_prompt": "/pixellab-pip create 32px explosion visual effects. must be a variety of top down explosions that are all unique.",
    "POST /v2/generate-image-v2": {
      "description": "fiery explosion blast viewed top-down orthographic looking straight down, radial burst of orange and red flames with bright yellow-white core, smoke and ember debris spreading outward on the ground plane, circular symmetrical blast",
      "image_size": {
        "width": 32,
        "height": 32
      },
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use all 64 images returned by the immediately preceding PixelLab call in returned order. Arrange them row-major into an 8 by 8 spritesheet with no margins, spacing, resizing, repainting, or quantization.",
      "outputs": ["fire-explosion.png"],
      "verify": "fire-explosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell is pixel-identical to its corresponding returned image and transparency is preserved."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 total (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "fire-explosion.png",
      "action": "fiery explosion blasts viewed top-down orthographic looking straight down, radial burst of orange and red flames with bright yellow-white core, smoke and ember debris spreading outward on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use all nine animation frames returned by the immediately preceding PixelLab call. Reorder the whole frames by visual progression into the strongest top-down fire-blast loop, retaining all nine, and assemble a transparent 256x256 GIF at 0.12 seconds per frame. Do not resize or repaint frame content.",
      "outputs": ["fire-explosion.gif"],
      "verify": "fire-explosion.gif is exactly 256x256 with nine 0.12-second frames, uses only returned frame content apart from GIF palette encoding, and preserves available transparency including any residual background pixels."
    }
  }
]
```

Findings:

- Reads as a top-down fire blast with an orange-and-red flame ring and a bright yellow-white core.
- Background removal did not fully clear, leaving some residual background pixels
- Retained all 9 frames after polishing; only frame order was adjusted.

## Toxic Explosion

<table>
  <tr>
    <td><img src="visual-effects/toxic-explosion.gif" alt="Top-down toxic acid explosion animation"></td>
    <td><img src="visual-effects/toxic-explosion.png" alt="Toxic explosion source spritesheet"></td>
  </tr>
</table>

Request intent: a green and lime acid burst with bubbling ooze and corrosive vapor, viewed straight down.

Source inputs: text-only request for the source sprite. The animation step used the locally assembled 32px spritesheet as its reference frame.

Route: REST v2 `generate-image-v2` (Create Image Pro) for the source sprite, then REST v2 `animate-with-text-v3` (Animate with Text (new)) for the animation.

Prompt preparation: the description named green and lime slime splatter, bubbling ooze, and corrosive droplets and vapor, with the same top-down orthographic and radial ground-plane wording. The animation `action` pluralized the subject to `explosions`.

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet; the returned animation frames were assembled into a transparent GIF, then hand-polished by reordering frames and deleting redundant ones.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames after polish | `10` |

Blueprint — replayable route and request body ([`toxic-explosion.blueprint.json`](visual-effects/toxic-explosion.blueprint.json)):

```json
[
  {
    "_comment": "One generate-image-v2 call at 32x32 returns 64 unique top-down candidate variations; they were tiled locally into an 8x8 spritesheet (toxic-explosion.png) used as the animation reference frame.",
    "_comment_prompt": "/pixellab-pip create 32px explosion visual effects. must be a variety of top down explosions that are all unique.",
    "POST /v2/generate-image-v2": {
      "description": "toxic acid explosion viewed top-down orthographic looking straight down, radial burst of green and lime slime splatter with bubbling ooze, corrosive droplets and vapor spreading outward on the ground plane, circular symmetrical blast",
      "image_size": {
        "width": 32,
        "height": 32
      },
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use all 64 images returned by the immediately preceding PixelLab call in returned order. Arrange them row-major into an 8 by 8 spritesheet with no margins, spacing, resizing, repainting, or quantization.",
      "outputs": ["toxic-explosion.png"],
      "verify": "toxic-explosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell is pixel-identical to its corresponding returned image and transparency is preserved."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 total (frame 0 + 8 generated). The historical 10-frame GIF used hand polishing whose exact repeat/order is not recoverable, so that local step is intentionally not encoded.",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "toxic-explosion.png",
      "action": "toxic acid explosions viewed top-down orthographic looking straight down, radial burst of green and lime slime splatter with bubbling ooze, corrosive droplets and vapor spreading outward on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  }
]
```

Findings:

- Reads as a clean top-down acid burst with green and lime ooze spreading outward.
- A solid, usable top-down splatter with a clean transparent background.

## Workflow

Each effect used the same two PixelLab calls:

1. `generate-image-v2` at `32x32` with `no_background`. At small sizes this route returns many distinct candidate variations from one generation, so a single call produced the full variety of unique explosions rather than one narrow composition.
2. `animate-with-text-v3` with the 8x8 candidate spritesheet as `first_frame` and `frame_count` of 8. Passing the spritesheet as the reference frame gave the animation dense pixel motion to work from, and pluralizing the subject in `action` matched the multi-blast reference.

The `first_frame` field is where the website's Animate with Text (new) reference-image slot maps; the endpoint has no separate reference-image field. Manually compiling the candidate spritesheet, assembling the GIF, and per-frame polish — reordering frames and deleting redundant ones — were local post-processing steps and are not blueprint calls.

## Findings

- One 32px `generate-image-v2` call already satisfies a variety request: the 64 returned candidates were distinct enough to seed unique per-theme explosions without additional calls.
- Forcing `top-down orthographic view looking straight down` plus radial ground-plane wording was necessary; without it the model tends to render side-view blasts with a horizon.
- Using the candidate spritesheet as the animation `first_frame` produced lively, dense effect motion that reads as a top-down explosion.
- Frame counts vary between effects because each GIF was hand-polished after generation — frames reordered and redundant ones deleted; the blueprint records the original `frame_count` of 8.

## Showcase Assets

| Output | Stable showcase file |
|---|---|
| Spark explosion animation | `docs/showcase/visual-effects/spark-explosion.gif` |
| Spark explosion source spritesheet | `docs/showcase/visual-effects/spark-explosion.png` |
| Void implosion animation | `docs/showcase/visual-effects/void-implosion.gif` |
| Void implosion source spritesheet | `docs/showcase/visual-effects/void-implosion.png` |
| Fire explosion animation | `docs/showcase/visual-effects/fire-explosion.gif` |
| Fire explosion source spritesheet | `docs/showcase/visual-effects/fire-explosion.png` |
| Toxic explosion animation | `docs/showcase/visual-effects/toxic-explosion.gif` |
| Toxic explosion source spritesheet | `docs/showcase/visual-effects/toxic-explosion.png` |

## Validation Notes

- All four animation GIFs are `256x256` with transparency.
- Spark explosion GIF: `8` frames.
- Void implosion GIF: `7` frames.
- Fire explosion GIF: `9` frames.
- Toxic explosion GIF: `10` frames.
- Frame counts differ from the requested `frame_count` of 8 because each GIF was hand-polished after generation — frames reordered and redundant ones deleted.
- Each source spritesheet is `256x256`, an 8x8 grid of `32x32` candidate cells with transparency.
