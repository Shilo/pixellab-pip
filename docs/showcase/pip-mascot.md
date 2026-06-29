# Pip Mascot

Last reviewed: 2026-06-25.

![Pip mascot idle animation](pip/pip.gif)

Pip is a compact honey-tan pixel pup mascot with a cyan collar and a friendly loopable idle animation. PixelLab Pip turned a mascot brief into PixelLab-ready character and animation prompts, routed the work through PixelLab MCP, and recorded the resulting assets for reuse.

## Request

### Character Prompt

```text
pip create a 64px character based on .pip-mascot.md
```

### Idle Animation Prompt (Follow-up)

```text
it should be happy and also loopable, so dont do stuff like a short smile, must be a repeated smile or tongue out, stuff like that
```

## Best Example: Pip Mascot Idle Animation

![Pip mascot idle animation](pip/pip.gif)

The final showcase asset is a south-facing happy pant idle loop assembled from the generated PixelLab character animation frames.

## Brief Summary

The mascot direction was a tiny rounded corgi-inspired scout puppy with honey-tan fur, cream muzzle/chest/belly/paws, oversized floppy ears, simple dark eyes, a cyan collar, and a small route-node/API-style tag. Pip condensed that direction into the generation-ready PixelLab prompt below.

## Character Generation

Route: PixelLab MCP `create_character`

Generation details:

| Field | Value |
|---|---|
| Mode | `standard` |
| Body type | `quadruped` |
| Template | `dog` |
| Size | `64` target character size |
| View | `side` |
| Directions | `4` |
| Detail | `medium detail` |
| Shading | `flat shading` |
| Outline | `single color black outline` |
| Text guidance scale | `8.5` |

Prompt sent as `description`:

```text
Adorable tiny corgi-inspired scout puppy mascot named Pip for a PixelLab workflow assistant. Rounded compact body, short little legs, oversized floppy ears, warm honey-tan fur with cream muzzle, chest, belly, and paws, big simple curious dark eyes, cheerful helpful expression. Bright cyan-blue collar with a tiny connected-node route tag or API graph tag. Clean game-ready pixel art, chunky readable shapes, crisp single-color outline, limited warm palette with cyan accent, transparent background. Friendly alert sitting pose with one paw raised where possible; puppy first, subtle tool-routing assistant second. No text, no logos, no gradients, no blur, no complex props.
```

Generation result:

- PixelLab returned four rotations: south, east, north, and west.
- The generated rotation canvases were `92x92px` with transparency. PixelLab uses a larger canvas than the requested character size to leave animation room.

## Idle Animation

Selected concept:

```text
Tongue-Out Happy Pant
```

Route: PixelLab MCP `animate_character`

Generation details:

| Field | Value |
|---|---|
| Animation name | `happy-pant-idle` |
| Mode | `v3` |
| Direction | `south` |
| Frame count requested | `8` |
| Frames returned | `9` including reference frame |

Prompt sent as `action_description`:

```text
loopable happy idle: Pip stays sitting facing forward with a constant cheerful tongue-out smile, gently panting in place, soft subtle body bounce, floppy ears bobbing slightly, friendly happy expression held throughout the whole seamless loop
```

## Local Assembly Notes

The GIF preview was assembled in Aseprite from the single-frame PNGs, with the first frame duration adjusted for the idle loop.

## Outputs

| File | Purpose |
|---|---|
| [`pip/pip.gif`](pip/pip.gif) | Primary south-facing happy pant idle loop. |
| [`pip/pip.png`](pip/pip.png) | Static south-facing Pip sprite. |

The showcase image files are display-ready `34x54px` versions derived from the generated PixelLab character and animation frames.

## Validation Notes

Final verification:

- GIF dimensions: `34x54px`.
- GIF frames: `9`.
- GIF pixel format: `Format32bppArgb`.
- Static PNG dimensions: `34x54px`.
- Static PNG pixel format: `Format32bppArgb`.
