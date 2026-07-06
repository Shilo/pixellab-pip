# Preset Template And Raw Skeleton Animations

Read this for PixelLab requests involving skeletons, preset/template/built-in character animations, or named motions such as `walking-8-frames`, `breathing-idle`, `jumping-1`, `running-6-frames`, or "make the website's walk template".

SKILL.md holds the global rules this file does not restate: MCP-first routing with the not-configured / explicit-MCP fallback contract, the south-first direction default and ask-before-all-directions cost gate, frame-order preservation, and the ban on undocumented website / Aseprite-extension endpoints.

Two families: managed preset/template animation on an existing character, and raw skeleton/keypoint animation. Custom skeleton authoring beyond estimated/exported keypoints is future-facing; route keypoint work to the documented REST endpoints below.

## Core Distinction

| User intent | Meaning | Route |
|---|---|---|
| Preset/template/built-in animation | Animate an existing managed character using a named motion template such as `walking-8-frames`, `breathing-idle`, or `jumping-1`. PixelLab generates frames for that character and direction. | Prefer MCP `animate_character`; fallback REST v2 `/characters/animations`. |
| Raw/custom skeleton animation | Generate frames from explicit skeleton keypoints, a reference image, optional masks/init images, and camera settings. | REST v2 `/animate-with-skeleton` and `/estimate-skeleton`. |

## MCP vs REST v2 Field Coverage

MCP `animate_character` handles normal managed-character template work when its visible schema exposes template mode, v3 custom mode, explicit `directions`, and `frame_count` (v3). When the visible schema exposes pro mode with cost confirmation, it can route pro animation. Inspect the visible schema before relying on `mode`, `frame_count`, `custom_start_frame`, `end_frame`, `keep_first_frame`, `pro`, `confirm_cost`, cost reporting, or any raw-skeleton support.

It is not field-for-field equivalent to REST `/characters/animations`. REST exposes extra exact-control fields: `description`, `text_guidance_scale`, `outline`, `shading`, `detail`, `isometric`, `color_image`, `force_colors`, `seed`, v3-only `custom_start_frame`/`end_frame`, and inline `enhance_prompt` (v3 mode). Use REST when those fields matter, for integration code, or to validate exact API behavior.

## Managed Preset Animation (MCP)

Flow for an existing or wanted managed character:

1. `get_character(character_id)` to confirm status, template/body type, directions, size, existing animations, and downloadable assets.
2. Choose `template_animation_id` from the character's template family (catalog below).
3. `animate_character` with explicit `directions`.
4. Poll with `get_character` or the returned job IDs, per visible MCP tool behavior.
5. Download frames/ZIP only after completion if local files are needed.

Verify by canonical `template_animation_id`, direction, and frame count, not by a custom display name: MCP smoke (2026-06-30) showed `animation_name` did not override the stored canonical template label returned by `get_character`, and MCP exposed no usage/cost.

```python
animate_character(
    character_id="...",
    template_animation_id="walking-8-frames",
    animation_name="walk",
    directions=["south"],
    mode="template",
)
```

To turn a reference image or GIF frame into a managed character first, use REST `create-character-v3` with required `description`, `reference_image`, `template_id="mannequin"`, and the appropriate `view`/`no_background`, then animate the returned `character_id` with MCP once the character completes (verified for a horse-headed biped from a source GIF frame).

For a newly created quadruped:

```python
create_character(
    description="small black outline companion animal",
    body_type="quadruped",
    template="dog",
    n_directions=4,
    size=92,
)

animate_character(
    character_id="returned-character-id",
    template_animation_id="walk-8-frames",
    directions=["south"],
    mode="template",
)
```

Direction names:

```text
4 directions: south, west, east, north
8 directions: south, south-east, east, north-east, north, north-west, west, south-west
```

Prefer the directions returned by `get_character`; direction order is not semantically meaningful for requests.

## Managed Preset Animation (REST v2)

Use REST when MCP is not visible, exact schema control is needed, or the user asks for API integration.

```text
POST https://api.pixellab.ai/v2/characters/animations
GET  https://api.pixellab.ai/v2/background-jobs/{job_id}
GET  https://api.pixellab.ai/v2/characters/{character_id}
GET  https://api.pixellab.ai/v2/characters/{character_id}/zip
```

Request shape:

```json
{
  "character_id": "managed-humanoid-character-id",
  "mode": "template",
  "template_animation_id": "walking-8-frames",
  "animation_name": "walk",
  "directions": ["south"]
}
```

| Field | Guidance |
|---|---|
| `character_id` | Required. Managed character must belong to the authenticated user. |
| `mode` | Use `template` for preset animation ids. Providing `template_animation_id` may auto-detect template mode, but be explicit. |
| `template_animation_id` | Exact preset id. Do not pass display labels. |
| `directions` | Be explicit to avoid accidental all-direction generation. |
| `frame_count` | Only for `mode="v3"` custom text animation. Ignored by preset template mode; do not set it expecting it to override `walking-8-frames`. |
| `custom_start_frame` | Optional v3-only starting pose. Requires exactly one direction, uses the character's stored direction frame when omitted, incompatible with template/pro mode. |
| `end_frame` | Optional v3-only target pose for interpolation. Dimensions must match the start frame, requires exactly one direction, incompatible with template/pro mode. |
| `keep_first_frame` | v3-only, default `true`. Controls whether the reference frame is stored as frame 0 (see Frame Count). Incompatible with template/pro mode. |
| `action_description` | Required for custom v3/pro. Optional in template mode; use only for light customization. |
| `enhance_prompt` | Only for v3 custom mode; do not set it for template/pro. |

Polling:

```text
POST response -> background_job_ids[]
poll each GET /v2/background-jobs/{job_id}
when completed -> use last_response animation metadata or GET character/ZIP
```

## Template Rendering And Tuning

Managed template animation is skeleton-guided re-rendering, not a layer composite of prebuilt arms/legs over the original frame. The template supplies motion/pose guidance while PixelLab re-renders frames for the character and direction. It can preserve the character and move limbs correctly yet still introduce artifacts such as heavier leg shadows, palette drift, or rigid/robotic motion.

Public controls when a preset walk/idle/jump is close but needs style correction:

| Control | Use |
|---|---|
| `action_description` | Lightly bias the template, e.g. "relaxed natural walk with slight shoulder sway" or "keep flat shading, avoid heavy leg shadows". |
| `text_guidance_scale` | How strongly template mode follows `action_description`; try moderate values first, very high can distort identity. |
| `shading` | Main knob for heavy shadow artifacts. Try `flat shading`, `minimal shading`, or the character's original shading. |
| `detail` | Lower detail can reduce noisy limb pixels or over-rendered joints. |
| `outline` | Reassert the original outline when limbs become too thick, broken, or overdrawn. |
| `color_image` + `force_colors` | Constrain palette when template frames introduce extra dark tones. |
| `seed` | Try a small number of reproducible candidates; template outputs vary. |

Template mode does not expose direct controls for 3D depth maps, per-bone easing, stride curves, secondary motion, limb IK, `bone_scaling`, shadow strength, or keypoint edits, and `frame_count` does not tune preset motion; choose a different template id such as `walking-4-frames`/`walking-6-frames`/`walking-8-frames`. If the rendering style is the problem, retry template mode with conservative style controls. If the gait itself is wrong (robotic walk, stiff torso, missing weight shift, bad limb timing), use v3/pro custom animation or raw skeleton/Aseprite keypoint authoring instead of expecting preset mode to behave like a full rig editor.

For template mode keep `action_description` light or omit it; the template id carries the motion. Use `animation_name` for organization. Do not use prompt enhancement for template mode.

```json
{
  "template_animation_id": "walking-8-frames",
  "animation_name": "walk",
  "directions": ["south"]
}
```

Only add `action_description` for a variant the route supports:

```json
{
  "template_animation_id": "walking-8-frames",
  "action_description": "a steady cheerful walk with a slight head bob",
  "text_guidance_scale": 6,
  "shading": "flat shading",
  "detail": "low detail",
  "outline": "single color black outline"
}
```

## Raw Skeleton Keypoint Routes

Use these only for explicit custom skeleton/keypoint workflows, not ordinary built-in walk/idle requests.

```text
POST /v2/estimate-skeleton
POST /v2/animate-with-skeleton
```

`estimate-skeleton` takes a character image and returns keypoints. `animate-with-skeleton` accepts fields such as:

```text
image_size
reference_image
skeleton_keypoints
view
direction
guidance_scale
init_images
inpainting_images
mask_images
color_image
seed
```

MCP `create_character` / `animate_character` are managed-character tools: they use template animations and stored skeleton metadata internally but do not accept arbitrary keypoint arrays. Use REST for raw skeleton estimation/animation unless the visible MCP schema explicitly exposes `estimate_skeleton`, `animate_with_skeleton`, `skeleton_keypoints`, or equivalent keypoint fields.

## Auto-Rig Skeleton Pipeline

Use this route for "auto rig", "estimate skeleton", "rig this sprite", "export skeleton for API", "animate with this skeleton", "my keypoints", "pose JSON", or a skeleton pipeline from a simple humanoid prompt. It is REST-first:

```text
source image or generated reference frame
  -> REST estimate-skeleton
  -> save/export keypoint JSON
  -> optional local/Aseprite keypoint editing
  -> REST animate-with-skeleton or create-image-bitforge
```

Raw skeleton animation is the right route when the user wants to own, export, edit, or reuse the keypoints; managed template animation is still right for built-in managed motions.

| User starts with | Best route |
|---|---|
| Existing sprite/image | Use it as the `estimate-skeleton` input and as `reference_image` for later `animate-with-skeleton` unless the user supplies a separate reference. |
| Aseprite-authored skeleton | Export from Aseprite, convert `pose_keypoints` to REST `skeleton_keypoints`, then call REST. |
| Prompt only ("humanoid knight") | Create or ask for a base reference frame first; prefer a PixelLab-generated humanoid/mannequin frame, then estimate keypoints from it. |
| Existing managed character id | Preset motions: MCP/REST managed template animation. Raw skeleton ownership: fetch a direction frame, estimate/export keypoints, then REST raw skeleton routes. |

For simple humanoid prompts default the body plan to humanoid/mannequin (MCP `create_character(body_type="humanoid")` or REST `create-character-v3` with `template_id="mannequin"`).

Programmatic steps:

1. Estimate or author keypoints. REST `POST /v2/estimate-skeleton` for a sprite/image; Aseprite "Export skeleton for API" writes normalized `pose_keypoints`. Local tooling may edit/validate JSON keypoints client-side (not a PixelLab API call).
2. Convert exported keypoints to the target REST field: Aseprite `{ "pose_keypoints": [[...], ...] }` -> REST animation `skeleton_keypoints: [[...], ...]`; REST single-image BitForge `skeleton_keypoints: [...]`.
3. Call `POST /v2/animate-with-skeleton` with `image_size`, `reference_image`, `skeleton_keypoints`, and explicit `view`/`direction`.
4. Add `init_images`, `inpainting_images`, `mask_images`, or `color_image` when the user supplied those roles or the route requires them.

`estimate-skeleton` returns a skeleton for one pose; it does not invent a walk/run sequence. `animate-with-skeleton` needs a keypoint sequence, so with only one estimated pose either ask for/create more poses, author a sequence in Aseprite, use managed template animation (built-in walk/idle/jump), or use REST custom text animation (motion without skeleton ownership).

### View/Direction Trap And Defaults

- For a typical RPG/down-facing sprite, set `view="low top-down"` and `direction="south"` explicitly.
- For side-view/platformer sprites, set `view="side"` and `direction="east"` or `west`.
- Do not rely on `animate-with-skeleton` defaults: current OpenAPI defaults are `view="side"` and `direction="east"`, which are wrong for many RPG sprites. Do not infer defaults from website managed-character examples, which may use low top-down/south.
- Interpret human/person/player/NPC/robot/humanoid-monster and upright two-legged animals as humanoid/mannequin.
- Save a sidecar manifest with `body_plan`, `source_image`, `image_size`, `view`, `direction`, `estimated_keypoints`, and the payload-ready `skeleton_keypoints`.

Current schema requires `image_size` and `reference_image`; custom keypoint workflows also need explicit `skeleton_keypoints` or a prior `estimate-skeleton`. Endpoint prose lists common sizes `16`, `32`, `64`, `128`, `256` while schema may allow other 16-256 dimensions; refresh OpenAPI before exact production code for nonstandard sizes, and ask for missing image/keypoint roles before spending credits.

## Aseprite Boundary

Estimate skeleton maps to REST `POST /v2/estimate-skeleton`; authoring/animating from keypoints maps to REST `POST /v2/animate-with-skeleton`; pose-guided image generation maps to REST `create-image-bitforge` (`skeleton_keypoints`/`skeleton_guidance_scale`). Aseprite exports normalized `pose_keypoints`; convert to REST `skeleton_keypoints`. Everything else in the Aseprite extension (edit skeleton, re-pose, insert template skeleton, its private template-animation flow and local skeleton JSON) is editor-internal and out of scope for public automation per SKILL.md. Aseprite's local template catalog is older/smaller than the managed preset IDs below; do not assume every managed id such as `breathing-idle` or `jumping-1` exists there.

## Preset Template Families

Known managed template families, last verified against MCP docs, REST OpenAPI, and the website Add Animation bundle on 2026-06-30: `mannequin`, `dog`, `cat`, `horse`, `bear`, `lion`.

Use the right vocabulary for the surface:

| Surface | Field | Valid values | Notes |
|---|---|---|---|
| MCP `create_character` | `body_type` | `humanoid`, `quadruped` | Use `humanoid` for bipedal/mannequin body plans. Use `quadruped` only for four-legged animals. |
| MCP `create_character` | `template` | `bear`, `cat`, `dog`, `horse`, `lion` | Required only when `body_type="quadruped"`. Ignored for humanoid characters. |
| MCP `create_character` | `proportions` | preset `default`, `chibi`, `cartoon`, `stylized`, `realistic_male`, `realistic_female`, `heroic`, or custom scale JSON | Humanoid only. This is how MCP expresses realistic/chibi humanoid proportions; it is not a separate `body_type`. |
| REST managed character create | `template_id` | `mannequin`, `bear`, `cat`, `dog`, `horse`, `lion` | `mannequin` is the bipedal/humanoid skeleton reconstruction template and the default in current OpenAPI. |
| REST managed animation | `template_animation_id` | Exact animation ids from the character's family | Does not take `body_type`; the managed character already carries the body plan/template family. |
| Website Add Animation | `Template` | `mannequin`, `dog`, `cat`, `horse`, `bear`, `lion` | UI label for the managed character's animation family. |

Choose the template family by body plan and stance, not species. Map human/person/player/NPC/wizard/knight/robot/biped requests, and upright/two-footed animals (horse person, cat warrior, fox mage), to humanoid/mannequin unless managed metadata proves quadruped. Four-legged dog/cat/horse/bear/lion map to `quadruped` plus the matching `template`; a four-legged animal outside these five uses the closest template or ask. Treat "mannequin" and misspellings like "manniquin" as the humanoid plan. Gotcha: do not pass `template="mannequin"` to MCP `create_character` (`template` is quadruped-only there); REST uses `template_id="mannequin"`. If a character already exists, prefer its stored `template_id` from `get_character` / REST `GET /characters/{character_id}` over guessing from the prompt.

## Preset Animation IDs

Use exact ids. Do not send labels such as "Walk (8 frames)". This catalog was last verified against the website Add Animation bundle on 2026-06-30. Official REST docs expose the `template_animation_id` field but no stable public enum endpoint; refresh visible MCP tool docs or official docs before claiming "all available animations" or building long-lived integrations.

Ordered by likely request frequency, mannequin/humanoid first because most player, NPC, human, and biped requests map there.

### mannequin

```text
walk
walk-1
walk-2
walking
walking-2
walking-3
walking-4
walking-5
walking-6
walking-7
walking-8
walking-9
walking-10
walking-4-frames
walking-6-frames
walking-8-frames
running-4-frames
running-6-frames
running-8-frames
running-slide
crouched-walking
crouching
sad-walk
scary-walk
breathing-idle
fight-stance-idle-8-frames
backflip
front-flip
getting-up
jumping-1
jumping-2
running-jump
two-footed-jump
cross-punch
lead-jab
surprise-uppercut
hurricane-kick
roundhouse-kick
high-kick
flying-kick
leg-sweep
fireball
taking-punch
falling-back-death
drinking
picking-up
pull-heavy-object
pushing
throw-object
```

### dog

```text
walk-4-frames
walk-6-frames
walk-8-frames
fast-walk
running-4-frames
running-6-frames
running-8-frames
sneaking
idle
bark
```

### cat

```text
walk-4-frames
walk-6-frames
walk-8-frames
running-4-frames
running-6-frames
running-8-frames
slow-run
jump
idle
seated-on-belly-idle
sitting
sitting-on-belly
standing
standing-from-belly
drinking
eating
licking
yawning
angry
```

### horse

```text
walk-4-frames
walk-6-frames
walk-8-frames
walk-turn-left
walk-turn-right
running-4-frames
running-6-frames
running-8-frames
running-turn-left
running-turn-right
running-headbutt
swimming
attack
attack-back
hit-left
hit-right
dying
idle-shaking-head
rest-idle
eat-start
eating
eat-end
start-sleep
sleep-cycle
rest-cycle
wake-up
lie-down
stand-up
```

### bear

```text
walk-4-frames
walk-6-frames
walk-8-frames
running-4-frames
running-6-frames
running-8-frames
jump
stand-on-hind-legs
attack-left
attack-right
jump-attack
idle-long
idle-resting
idle-sitting
drinking
eating
going-to-sleep
waking-getting-up
sitting-down
standing-up
angry
```

### lion

```text
walk-4-frames
walk-6-frames
walk-8-frames
running-4-frames
running-6-frames
running-8-frames
jump
attack
jump-attack
idle
idle-sitting
drinking
eating
sitting
standing
```

Common label mappings and exact-id passthroughs:

| User says | Use id |
|---|---|
| "human walk 8 frames" | `walking-8-frames` |
| "person idle" | `breathing-idle` |
| "wizard jump" | `jumping-1` or `jumping-2` |
| "bark" | `bark` |
| "dog walk 8 frames" | `walk-8-frames` |
| "dog fast walk" | `fast-walk` |
| "humanoid walk 8 frames" | `walking-8-frames` |
| "fight idle" | `fight-stance-idle-8-frames` |

If an animation exists for one template family but not another, say so and offer the closest same-family option. Do not silently substitute `walking-8-frames` for a quadruped `walk-8-frames` or vice versa.

## Frame Count

- Preset template mode owns its frame count through the selected template id; do not set `frame_count` expecting it to override `walking-8-frames`.
- V3 custom mode owns frame count through `frame_count` 4-16, even only, default 8. V3 also stores the reference frame as frame 0 (so `frame_count=8` stores 9 frames) unless `keep_first_frame=false`; details in `animation.md`.
- Report the actual returned frame count if it differs from the id or expectation.

## Verification

Before reporting success, confirm: the requested `template_animation_id` was used; the requested vs actually completed direction set; the returned frame count; dimensions match the character. If exporting through Aseprite, verify tag/frame count/order and that the original frames were not rewritten.

Refresh official docs/OpenAPI/MCP docs before exact code claims when a template id is not here, the visible MCP schema differs, the user asks for all current animations, pricing/frame limits matter, or custom skeleton/keypoint support is requested.
