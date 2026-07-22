# Visual Effects

Last reviewed: 2026-07-22.

<table>
  <tr>
    <td><img src="visual-effects/fantasy-aura-effects.gif" alt="Sixteen separately animated fantasy aura effects"></td>
    <td><img src="visual-effects/fantasy-aura-effects.png" alt="Sixteen fantasy aura source sprites"></td>
  </tr>
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

The aura library adds sixteen transparent 64px effects—energy, elemental, magical, and material themes—animated independently and synchronized into one 4x4 GIF.

## Contents

- [Fantasy Aura Effects](#fantasy-aura-effects)
- [Spark Explosion](#spark-explosion)
- [Void Implosion](#void-implosion)
- [Fire Explosion](#fire-explosion)
- [Toxic Explosion](#toxic-explosion)
- [Workflow](#workflow)
- [Findings](#findings)
- [Showcase Assets](#showcase-assets)
- [Validation Notes](#validation-notes)

## Fantasy Aura Effects

<table>
  <tr>
    <td><img src="visual-effects/fantasy-aura-effects.gif" alt="Sixteen separately animated fantasy aura effects"></td>
    <td><img src="visual-effects/fantasy-aura-effects.png" alt="Sixteen fantasy aura source sprites"></td>
  </tr>
</table>

Sixteen transparent 64px fantasy auras share one silhouette while using distinct elemental palettes and motion.

### Request

```text
/pixellab-pip create aura blueprint with energy, fire, water, ice, lightning, wind, nature, poison, darkness, holy, arcane, blood, bone, ghost, smoke, sand
```

Follow-up intent: animate every aura separately in the same array order, then combine all effects into one GIF.

Source inputs: text only. The static description treated the comma-separated theme list as one request and asked for a fully contained symmetrical aura with vertical power spikes and a bottom energy ring.

Route: REST v2 `generate-image-v2` for the source candidates, then sixteen REST v2 `animate-with-text-v3` calls—one per theme.

Prompt preparation: the sixteen returned candidates were assigned in array order. Each animation action named its corresponding theme and described material-specific motion: fire licks upward, water circulates, lightning crackles, wind spirals, nature sways, poison bubbles, holy light radiates, smoke billows, and sand grains spiral.

Local processing: PixelLab produced every visible aura frame. Local assembly copied the returned PNGs, assembled each animation horizontally for verification, arranged matching frame indices into 4x4 combined frames, and encoded the final GIF. The GIF preserves transparency and theme positions; its 256-color-per-frame format introduces normal palette quantization, while the source PNGs remain lossless.

Generation details:

| Field | Value |
|---|---|
| Source route | REST v2 `generate-image-v2` |
| Animation route | REST v2 `animate-with-text-v3` |
| Source size | `64x64` per aura |
| Source output | 16 candidates assembled as a 4x4 `256x256` sheet |
| Animation jobs | 16, one per theme |
| Frames | `8` requested; 9 returned including frame 0 |
| Background | `no_background: true` |
| Prompt enhancement | Disabled for animation |
| Seed | Omitted from requests |
| Final GIF | `256x256`, 9 frames, 100 ms per frame, loops forever |

Blueprint excerpt (truncated) — the [complete replayable workflow](visual-effects/fantasy-aura-effects.blueprint.json) records all sixteen successful theme-specific animation calls and assembly tasks:

```json
[
  {
    "POST /v2/generate-image-v2": {
      "description": "fully contained symmetrical energy, fire, water, ice, lightning, wind, nature, poison, darkness, holy, arcane, blood, bone, ghost, smoke, sand aura with vertical power spikes and a bottom energy ring",
      "image_size": {
        "width": 64,
        "height": 64
      },
      "no_background": true
    }
  },
  {
    "_comment": "Representative animation step; the complete blueprint repeats this shape once per theme in array order.",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "01/source.png",
      "action": "energy aura surges in rhythmic concentric pulses while its vertical power spikes breathe brighter and dimmer in place",
      "frame_count": 8,
      "no_background": true,
      "enhance_prompt": false
    }
  },
  {
    "TASK": {
      "instruction": "Assemble matching frame indices from all sixteen completed theme animations into transparent 4x4 frames, then encode the nine combined frames as fantasy-aura-effects.gif at 100 milliseconds per frame, looping forever with disposal Previous.",
      "outputs": [
        "fantasy-aura-effects.gif"
      ],
      "verify": "The GIF is 256x256 with nine ordered frames, preserves transparency and theme-array positions, and changes returned frame content only through GIF palette encoding."
    }
  }
]
```
Findings:

- Separate animation calls produce meaningfully different motion instead of applying one shared pulse to the whole atlas.
- Naming the exact theme in every `action` keeps motion aligned with the array order.
- The combined GIF reads as a coordinated effect library while every aura remains in its original 4x4 position.
- Small 64px Animate with Text V3 jobs cost one generation each in this run; pricing and accounting may change.


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

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet. The GIF keeps returned animation frames 1-6 and 9 in order, omits frames 7-8, and appends one fully transparent end frame.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames | `8` |

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
      "verify": "spark-explosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell's alpha channel and visible RGB pixels are pixel-identical to its corresponding returned image."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 returned frames (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "spark-explosion.png",
      "action": "bright spark flash pop explosions viewed top-down orthographic looking straight down, small radial burst of yellow and white sparks and glinting star-shaped flash on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use returned animation frames 1 through 6 and frame 9 in that order, omit frames 7 and 8, then append one fully transparent 256x256 frame. Assemble those eight frames as a transparent GIF at 0.12 seconds per frame without resizing or repainting returned frame content.",
      "outputs": ["spark-explosion.gif"],
      "verify": "spark-explosion.gif is exactly 256x256 with eight 0.12-second frames: returned frames 1-6 and 9 remain in order, followed by one fully transparent frame; returned frame content changes only through GIF palette encoding."
    }
  }
]
```

Findings:

- Reads as a crisp top-down radial spark burst with a clear yellow-white center and star-shaped glint.
- The strongest of the four explosion effects.

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

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet. The GIF keeps returned animation frames 1-6 in order, omits frames 7-9, and appends one fully transparent end frame.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames | `7` |

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
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 returned frames (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "void-implosion.png",
      "action": "dark void magic implosions viewed top-down orthographic looking straight down, radial burst of purple and violet arcane energy with black core, swirling shadow tendrils and magic sparks on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use returned animation frames 1 through 6 in order, omit frames 7 through 9, then append one fully transparent 256x256 frame. Assemble those seven frames as a transparent GIF at 0.12 seconds per frame without resizing or repainting returned frame content.",
      "outputs": ["void-implosion.gif"],
      "verify": "void-implosion.gif is exactly 256x256 with seven 0.12-second frames: returned frames 1-6 remain in order, followed by one fully transparent frame; returned frame content changes only through GIF palette encoding."
    }
  }
]
```

Findings:

- Reads as a top-down arcane implosion with a dark core and swirling violet tendrils.
- The assembled GIF keeps returned frames 1-6 and ends on a fully transparent frame.

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

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet. The GIF keeps returned animation frames 1-7 and 9 in order, omits frame 8, and appends one fully transparent end frame.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames | `9` |

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
      "verify": "fire-explosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell's alpha channel and visible RGB pixels are pixel-identical to its corresponding returned image."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 returned frames (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "fire-explosion.png",
      "action": "fiery explosion blasts viewed top-down orthographic looking straight down, radial burst of orange and red flames with bright yellow-white core, smoke and ember debris spreading outward on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use returned animation frames 1 through 7 and frame 9 in that order, omit frame 8, then append one fully transparent 256x256 frame. Assemble those nine frames as a transparent GIF at 0.12 seconds per frame without resizing or repainting returned frame content.",
      "outputs": ["fire-explosion.gif"],
      "verify": "fire-explosion.gif is exactly 256x256 with nine 0.12-second frames: returned frames 1-7 and 9 remain in order, followed by one fully transparent frame; returned frame content changes only through GIF palette encoding."
    }
  }
]
```

Findings:

- Reads as a top-down fire blast with an orange-and-red flame ring and a bright yellow-white core.
- Background removal did not fully clear, leaving some residual background pixels
- The assembled GIF keeps returned frames 1-7 and 9, then ends on a fully transparent frame.

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

Local processing: the 64 native-size candidates were manually compiled into an 8x8 spritesheet. The GIF keeps all nine returned animation frames in order and appends one fully transparent end frame.

Generation details:

| Field | Value |
|---|---|
| Source sprite size | `32x32` |
| Source output | 64 candidates, tiled into an 8x8 `256x256` spritesheet |
| Animation reference | source spritesheet as `first_frame` |
| Frame count requested | `8` (9 including reference frame 0) |
| Background | `no_background` for both steps |
| GIF size | `256x256` |
| GIF frames | `10` |

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
      "verify": "toxic-explosion.png is exactly 256x256 with sixty-four 32x32 cells; every cell's alpha channel and visible RGB pixels are pixel-identical to its corresponding returned image."
    }
  },
  {
    "_comment": "Animate with Text (new) using the spritesheet as first_frame reference, pluralized action, 8 frames producing 9 returned frames (frame 0 + 8 generated).",
    "POST /v2/animate-with-text-v3": {
      "first_frame": "toxic-explosion.png",
      "action": "toxic acid explosions viewed top-down orthographic looking straight down, radial burst of green and lime slime splatter with bubbling ooze, corrosive droplets and vapor spreading outward on the ground plane, circular symmetrical blast",
      "frame_count": 8,
      "no_background": true
    }
  },
  {
    "TASK": {
      "instruction": "Use all nine returned animation frames in order, then append one fully transparent 256x256 frame. Assemble those ten frames as a transparent GIF at 0.12 seconds per frame without resizing or repainting returned frame content.",
      "outputs": ["toxic-explosion.gif"],
      "verify": "toxic-explosion.gif is exactly 256x256 with ten 0.12-second frames: all nine returned frames remain in order, followed by one fully transparent frame; returned frame content changes only through GIF palette encoding."
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

The `first_frame` field is where the website's Animate with Text (new) reference-image slot maps; the endpoint has no separate reference-image field. Manually compiling the candidate spritesheet, selecting returned frames, appending a transparent end frame, and encoding the GIF were local post-processing steps recorded as `TASK` steps in each blueprint.

## Findings

- One 32px `generate-image-v2` call already satisfies a variety request: the 64 returned candidates were distinct enough to seed unique per-theme explosions without additional calls.
- Forcing `top-down orthographic view looking straight down` plus radial ground-plane wording was necessary; without it the model tends to render side-view blasts with a horizon.
- Using the candidate spritesheet as the animation `first_frame` produced lively, dense effect motion that reads as a top-down explosion.
- Frame counts vary because each GIF keeps an explicitly recorded subset of returned frames in order and appends one fully transparent end frame; the PixelLab request still records `frame_count: 8`.

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
| Fantasy aura animation | `docs/showcase/visual-effects/fantasy-aura-effects.gif` |
| Fantasy aura source sheet | `docs/showcase/visual-effects/fantasy-aura-effects.png` |
| Fantasy aura blueprint | `docs/showcase/visual-effects/fantasy-aura-effects.blueprint.json` |

## Validation Notes

- All four animation GIFs are `256x256` with transparency.
- Spark explosion GIF: `8` frames.
- Void implosion GIF: `7` frames.
- Fire explosion GIF: `9` frames.
- Toxic explosion GIF: `10` frames.
- Fantasy aura GIF: `9` transparent `256x256` frames at 100 ms each, looping forever with disposal `Previous`.
- Fantasy aura source sheet: `256x256`, arranged as a 4x4 grid of sixteen `64x64` cells in theme-array order.
- GIF frame counts include the supplied reference frame and the locally appended fully transparent end frame; spark, void, and fire also omit the returned frames named in their `TASK` steps.
- Each source spritesheet is `256x256`, an 8x8 grid of `32x32` candidate cells with transparency.
- All 144 lossless aura PNG cells matched their generated source frames pixel-for-pixel before GIF palette encoding.
