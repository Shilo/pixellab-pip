# Preset Template And Raw Skeleton Animations

Read this for PixelLab requests involving skeletons, preset animations, template animations, built-in character animations, or named motions such as `walking-8-frames`, `breathing-idle`, `jumping-1`, `running-6-frames`, or "make the website's walk template".

Current focus: preset/template animations for managed characters plus a streamlined REST-first auto-rig/keypoint pipeline for estimating, exporting, and animating raw skeleton data. Custom skeleton authoring beyond estimated/exported keypoints is still future-facing; route keypoint work carefully to documented REST skeleton endpoints, and do not automate private website or Aseprite extension internals.

## Core Distinction

There are two different animation families:

| User intent | Meaning | Route |
|---|---|---|
| Preset/template/built-in animation | Animate an existing managed character using a named motion template such as `walking-8-frames`, `breathing-idle`, or `jumping-1`. PixelLab generates frames for that character and direction. | Prefer MCP `animate_character`; fallback REST v2 `/characters/animations`. |
| Raw/custom skeleton animation | Generate frames from explicit skeleton keypoints, a reference image, optional masks/init images, and camera settings. | REST v2 `/animate-with-skeleton` and `/estimate-skeleton`. |

Do not call website/Aseprite private routes such as `/generate-animation/background` or extension suffixes such as `generate-animation`. They may reveal first-party behavior but are not stable public automation contracts.

## Default Route

For managed preset/template animations:

1. If PixelLab MCP tools are visible, use MCP first.
2. If MCP is unavailable or fails for a non-content reason and a PixelLab bearer token is configured, fall back to REST v2.
3. If the user explicitly asks for API/code/batch integration, use REST v2 directly.
4. If neither MCP nor REST auth is configured, stop before spending credits and route to setup; do not ask the user to paste secrets into chat.

This priority holds even when a REST/API secret exists. MCP remains the preferred agent workflow for managed character assets because it carries managed IDs, polling, downloads, and resource helpers. REST v2 is more feature-rich for exact schemas, raw skeleton keypoints, and advanced character-animation controls.

If the user explicitly requested MCP, do not silently fall back to REST. Report that MCP tools are unavailable and ask before using REST v2.

## MCP vs REST v2 Capability

MCP `animate_character` is fully suitable for normal managed-character template animation work when the visible runtime schema exposes the needed fields: template mode, v3 custom mode, explicit directions, and `frame_count` for v3. When the visible MCP schema exposes pro mode with cost confirmation, it can also route pro animation. Use MCP first when the tools are visible, but inspect the visible MCP schema before relying on fields such as `mode`, `frame_count`, `pro`, `confirm_cost`, cost reporting, or any future raw-skeleton support.

It is not a complete field-for-field replacement for REST v2 `/characters/animations` or `/animate-character`. The REST request schema currently exposes additional exact-control fields such as `description`, `text_guidance_scale`, `outline`, `shading`, `detail`, `isometric`, `color_image`, `force_colors`, `seed`, and inline `enhance_prompt` for v3 mode. Use REST v2 when those fields matter, when writing integration code, or when validating exact API behavior.

## Managed Preset Animation With MCP

Use this when the user has or wants a managed character.

Typical flow:

1. `get_character(character_id)` to confirm status, template/body type, directions, size, existing animations, and downloadable assets.
2. Choose `template_animation_id` from the character template family.
3. Call `animate_character` with explicit `directions` unless the user asked for all directions.
4. Poll with `get_character` or the returned job IDs, depending on visible MCP tool behavior.
5. Download frames/ZIP only after completion if local files are needed.

Live MCP smoke on 2026-06-30 showed template calls completing for humanoid `walking-8-frames` and `breathing-idle`, plus quadruped `walk-8-frames` and another built-in activity template. In that smoke, MCP did not expose usage/cost, and `animation_name` did not override the stored canonical template label returned by `get_character`. Verify by canonical `template_animation_id`, direction, and frame count rather than by a custom display name alone.

MCP call shape:

```python
animate_character(
    character_id="...",
    template_animation_id="walking-8-frames",
    animation_name="walk",
    directions=["south"],
    mode="template",
)
```

For a reference image or GIF frame that must become a managed humanoid character first, use REST v2 `create-character-v3` with required `description`, `reference_image`, `template_id="mannequin"`, and the appropriate `view`/`no_background` fields, then use the returned `character_id` with MCP `animate_character` after the character completes. Live testing on 2026-06-30 confirmed this path for a horse-headed biped: REST v2 created a managed mannequin-family character from a source GIF frame, and MCP `animate_character` completed `walking-8-frames` for `south`, `east`, `north`, and `west` with 8 frames per direction.

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
    directions=["south", "east", "north", "west"],
    mode="template",
)
```

Default direction behavior:

- If the user asks for "a walk animation" on an existing multi-direction character and does not specify direction, default to `south` for one preview candidate.
- Animate all directions only when the user asks for all directions, a complete direction set, or approves the additional cost.
- Template mode may default to all directions in REST, but the skill should still be explicit to avoid accidental multi-direction spend.

Direction names:

```text
4 directions: south, west, east, north
8 directions: south, south-east, east, north-east, north, north-west, west, south-west
```

Direction order is not semantically meaningful for requests; prefer the directions returned by `get_character` when available.

## Managed Preset Animation With REST v2

Use REST v2 when MCP is not visible, when exact schema control is needed, or when the user asks for API integration.

Endpoint:

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

Important fields:

| Field | Guidance |
|---|---|
| `character_id` | Required. Managed character must belong to the authenticated user. |
| `mode` | Use `template` for preset animation ids. Providing `template_animation_id` may auto-detect template mode, but be explicit. |
| `template_animation_id` | Exact preset id. Do not pass display labels. |
| `directions` | Be explicit to avoid accidental all-direction generation. |
| `frame_count` | Only for `mode="v3"` custom text animation. Ignored by preset template mode. |
| `action_description` | Required for custom v3/pro. Optional in template mode; use only for light customization when appropriate. |
| `enhance_prompt` | Only for v3 custom mode; do not set it for template/pro. |

### Template Rendering And Tuning

Managed template animation is skeleton-guided generation, not a simple layer composite of prebuilt arms/legs over the original frame. The template supplies motion/pose guidance, while PixelLab re-renders frames for the managed character and direction. This can preserve the character and move the limbs correctly while still introducing generation artifacts such as heavier shadows on legs, palette drift, or rigid/robotic body motion.

Use these public controls when a preset walk/idle/jump is close but needs style correction:

| Control | Use |
|---|---|
| `action_description` | Lightly bias the template, such as "relaxed natural walk with slight shoulder sway" or "keep flat shading and avoid heavy shadows on the legs". |
| `text_guidance_scale` | Controls how strongly template mode follows `action_description`; try moderate values first because very high values can distort identity. |
| `shading` | Main public knob for heavy shadow artifacts. Try values such as `flat shading`, `minimal shading`, or the character's original shading style. |
| `detail` | Lower detail can reduce noisy limb pixels or over-rendered joints. |
| `outline` | Reassert the original outline style when limbs become too thick, broken, or overdrawn. |
| `color_image` + `force_colors` | Constrain palette when template frames introduce extra dark tones or unwanted colors. |
| `seed` | Try a small number of reproducible candidates; template outputs can vary. |

Preset template mode does not expose direct controls for 3D depth maps, per-bone easing, stride curves, secondary motion, limb IK, `bone_scaling`, shadow strength, or skeleton keypoint edits. `frame_count` also does not tune preset motion; choose a different template id such as `walking-4-frames`, `walking-6-frames`, or `walking-8-frames`.

If the issue is mainly rendering style, retry template mode with conservative style controls. If the issue is the gait itself, such as a robotic walk, stiff torso, missing weight shift, or bad limb timing, use v3/pro custom animation or raw skeleton/Aseprite keypoint authoring instead of expecting preset mode to behave like a full animation rig editor.

Polling:

```text
POST response -> background_job_ids[]
poll each GET /v2/background-jobs/{job_id}
when completed -> use last_response animation metadata or GET character/ZIP
```

## Raw Skeleton Keypoint Routes

Use these only for explicit custom skeleton/keypoint workflows, not ordinary built-in walk/idle requests.

Endpoints:

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

Current MCP does not expose standalone raw-skeleton tools equivalent to Aseprite's "Estimate skeleton", "Edit skeleton", "Export skeleton for API", or "Animate with skeleton (new)" editor flow. MCP `create_character` / `animate_character` are managed-character tools; they can use template animations and stored character skeleton metadata internally, but they do not accept arbitrary keypoint arrays. Use REST v2 for raw skeleton estimation/animation unless the visible MCP schema explicitly exposes `estimate_skeleton`, `animate_with_skeleton`, `skeleton_keypoints`, or equivalent keypoint fields in the current runtime.

## Auto-Rig Skeleton Pipeline

Use this route when the user says "auto rig", "estimate skeleton", "rig this humanoid sprite", "export skeleton for API", "animate with this skeleton", or asks for an automatic skeleton pipeline from a simple humanoid prompt.

Today, the streamlined programmatic route is REST-first:

```text
source image or generated reference frame
  -> REST estimate-skeleton
  -> save/export keypoint JSON
  -> optional local/Aseprite keypoint editing or template keypoint authoring
  -> REST animate-with-skeleton or create-image-bitforge
```

Do not route raw skeleton data through MCP unless the visible MCP tool schema accepts keypoint data. Current MCP template animation is still the right route for built-in managed motions such as humanoid `walking-8-frames`; raw skeleton animation is the right route when the user wants to own, export, edit, or reuse the skeleton keypoints.

### Input Cases

| User starts with | Best route |
|---|---|
| Existing sprite/image | Use it as the `estimate-skeleton` input image and as `reference_image` for later `animate-with-skeleton` unless the user supplies a separate reference. |
| Aseprite-authored skeleton | Export from Aseprite, convert `pose_keypoints` to REST `skeleton_keypoints`, then call REST. |
| Prompt only, such as "humanoid knight" | First create or ask for a base reference frame. Prefer a PixelLab-generated humanoid/mannequin frame if the user wants PixelLab to create the character; then estimate/export keypoints from that image. |
| Existing managed character id | For preset motions, use MCP/REST managed template animation. For raw skeleton ownership, fetch/download a direction frame, estimate/export keypoints, then use REST raw skeleton routes. |

For simple humanoid prompts, default the body plan to humanoid/mannequin. If creating a managed reference character first, use MCP `create_character(body_type="humanoid")` or REST `create-character-v3` with `template_id="mannequin"`. If creating only a raw single-frame reference, use an appropriate REST image/character route and then estimate keypoints from the returned image.

### Programmatic Steps

1. Estimate or author keypoints.
   - REST: `POST /v2/estimate-skeleton` for a sprite/image.
   - Aseprite: "Estimate skeleton" creates local editable pose data; "Export skeleton for API" writes normalized keypoints as `pose_keypoints`.
   - Local agent tooling may edit/validate JSON keypoints, but that is client-side, not a PixelLab API call.
2. Convert exported keypoints to the target REST field.
   - Aseprite export shape: `{ "pose_keypoints": [[...], ...] }`.
   - REST animation field: `skeleton_keypoints: [[...], ...]`.
   - REST single-image BitForge field: `skeleton_keypoints: [...]`.
3. Call `POST /v2/animate-with-skeleton` with `image_size`, `reference_image`, `skeleton_keypoints`, and explicit `view` / `direction`.
4. Add `init_images`, `inpainting_images`, `mask_images`, or `color_image` when the user supplied those roles, the route requires them, or the user asks to match Aseprite's richer "Animate with skeleton (new)" behavior. Aseprite's editor flow can build freeze/inpaint masks and extra per-frame context locally; the minimal REST recipe is the public route, not wire-equivalent output parity.

Important: `estimate-skeleton` returns a skeleton for an image pose; it does not invent a full walk/run sequence by itself. For a real skeleton animation, `animate-with-skeleton` needs a keypoint sequence. If the user provides only one estimated pose and asks for motion, choose one of these:

- Ask for or create additional keypoint poses.
- Use an Aseprite visible editor workflow to insert/author local skeleton templates, then export the sequence.
- Use managed template animation instead when they actually want a built-in walk/idle/jump.
- Use REST custom text animation when they want motion but do not need skeleton ownership/export.

### Defaults For Humanoid Auto-Rigging

- Interpret "human", "person", "player", "NPC", "robot", "humanoid monster", and upright two-legged animal characters as humanoid/mannequin.
- For a typical RPG/down-facing sprite, set `view="low top-down"` and `direction="south"` explicitly when calling `animate-with-skeleton`.
- For side-view/platformer sprites, set `view="side"` and `direction="east"` or `west` based on the sprite.
- Do not rely on `animate-with-skeleton` defaults; OpenAPI defaults are `view="side"` and `direction="east"`, which are wrong for many RPG sprites.
- Save a sidecar manifest with `body_plan`, `source_image`, `image_size`, `view`, `direction`, `estimated_keypoints`, and the REST payload-ready `skeleton_keypoints`.

Current OpenAPI defaults raw `animate-with-skeleton` to `view="side"` and `direction="east"`. Do not infer raw skeleton defaults from website managed-character examples, which may use low top-down/south or another stored character view/direction. Endpoint prose lists common supported sizes `16`, `32`, `64`, `128`, and `256`, while schema behavior can allow other 16-256 dimensions; verify current OpenAPI before writing exact production code for nonstandard sizes.

Before exact calls, refresh OpenAPI. Current schema requires `image_size` and `reference_image`; custom keypoint workflows also need explicit `skeleton_keypoints` or a prior `estimate-skeleton` step. Ask for missing image/keypoint roles before spending credits.

If the user says "estimate skeleton", "auto rig this sprite", "custom skeleton", "my keypoints", "pose JSON", "export skeleton", or "animate with this skeleton", route to REST raw skeleton primitives or Aseprite visible editor workflow depending on whether they want programmatic generation or interactive editing. Ask for or infer the required image/keypoint roles before spending credits. If the user simply says "skeleton walk template" or "preset skeleton animation", use managed template animation instead.

## Aseprite Boundary

For Aseprite requests:

```text
PixelLab MCP or REST v2 generation
  -> verified local frames/ZIP
  -> Aseprite CLI/Lua import/export/tagging
```

Aseprite is appropriate for:

- Creating an `.aseprite` workspace from generated frames.
- Adding a `walk`, `idle`, `run`, or custom tag.
- Exporting a spritesheet, GIF, frame sequence, or metadata JSON.
- Estimating a skeleton onto an open sprite for interactive editing.
- Editing pose/keypoint overlays visually.
- Inserting local skeleton templates into frames for authoring.
- Exporting local skeleton keypoints for API use.
- Inspecting local skeleton reference files for research only.

Aseprite skeleton features observed in the installed extension:

| Feature | Closest public automation equivalent, not the same endpoint |
|---|---|
| Estimate skeleton | REST `POST /v2/estimate-skeleton`; no standalone MCP equivalent. |
| Edit skeleton | Client/editor-side keypoint editing; no PixelLab-hosted edit endpoint. |
| Export skeleton for API | Aseprite exports normalized `pose_keypoints`; convert to REST `skeleton_keypoints`. |
| Insert template skeleton | Local Aseprite reference JSON only; not public template ids. |
| Animations for character / template animation | Private Aseprite template-animation flow using local `template_name` / template catalog values; for public automation, use managed MCP/REST template animation on a character or REST raw skeleton routes after keypoints are exported. |
| Animate with skeleton (new) | REST `POST /v2/animate-with-skeleton`; no raw-skeleton MCP equivalent. |
| Re-pose (skeleton) | Exact Aseprite route is private/editor-only; approximate with REST skeleton/image-edit/managed-state routes based on requested output. |
| Pose-guided image generation | REST `create-image-bitforge` exposes `skeleton_keypoints` / `skeleton_guidance_scale`; otherwise treat as editor-only unless current OpenAPI shows a field. |

Aseprite uses private editor channels for these flows. The public routes above are functional equivalents for automation, not the same endpoints, auth context, or response shape. Aseprite's private template-animation catalog is also older/smaller than the managed website preset ID list below; do not assume every managed id, such as `breathing-idle` or `jumping-1`, exists in the local Aseprite template flow.

Do not:

- Call PixelLab Aseprite extension internals to spend credits.
- Use extension root operation suffixes as public REST endpoints.
- Read or expose extension secrets, request history credentials, or browser/session auth.
- Treat local extension skeleton JSON files as stable public template ids.

## Preset Template Families

Known managed template families, last verified against MCP docs, REST OpenAPI, and the website Add Animation bundle on 2026-06-30. Verify current tool/schema docs when exact availability matters:

```text
mannequin
dog
cat
horse
bear
lion
```

Use the right vocabulary for the surface:

| Surface | Field | Valid values | Notes |
|---|---|---|---|
| MCP `create_character` | `body_type` | `humanoid`, `quadruped` | Use `humanoid` for bipedal/mannequin body plans. Use `quadruped` only for four-legged animals. |
| MCP `create_character` | `template` | `bear`, `cat`, `dog`, `horse`, `lion` | Required only when `body_type="quadruped"`. Ignored for humanoid characters. |
| MCP `create_character` | `proportions` | preset `default`, `chibi`, `cartoon`, `stylized`, `realistic_male`, `realistic_female`, `heroic`, or custom scale JSON | Humanoid only. This is how MCP expresses realistic/chibi humanoid proportions; it is not a separate `body_type`. |
| REST managed character create | `template_id` | `mannequin`, `bear`, `cat`, `dog`, `horse`, `lion` | `mannequin` is the bipedal/humanoid skeleton reconstruction template and the default in current OpenAPI. |
| REST managed animation | `template_animation_id` | Exact animation ids from the character's family | Does not take `body_type`; the managed character already carries the body plan/template family. |
| Website Add Animation | `Template` | `mannequin`, `dog`, `cat`, `horse`, `bear`, `lion` | UI label for the managed character's animation family. |
| Aseprite automatic character animation | `character_type` | `bipedal-realistic`, `bipedal-semi-chibi`, `quadrupedal-tiny` | Local extension labels for its automatic complete-character flow. These are not MCP `body_type` values or public REST `template_id` values. |
| Aseprite local skeleton references | folder/type labels | `bipedal_realistic`, `bipedal_semi-chibi`, `quadrupedal_tiny`; UI labels `bipedal realistic`, `bipedal semi-chibi`, `quadrupedal tiny` | Research/import context only. Do not treat these local folders as stable public PixelLab template ids. |

MCP `create_character` uses `body_type="quadruped"` plus `template` for animals that stand and move on four legs. Humanoid/mannequin characters use `body_type="humanoid"` and humanoid proportion controls when available. Do not pass `template="mannequin"` to MCP `create_character`; `template` is quadruped-only there. REST v2 create routes use `template_id="mannequin"` for this humanoid/mannequin workflow.

Normalize user wording carefully:

- Treat "mannequin" and misspellings such as "manniquin" as the humanoid/mannequin body plan.
- For MCP, that means `body_type="humanoid"` and optional humanoid `proportions`; it does not mean `template="mannequin"`.
- For REST managed character creation, that means `template_id="mannequin"`.
- For Aseprite automatic complete-character flows, map humanoid/mannequin work to `bipedal-realistic` or `bipedal-semi-chibi` based on requested proportions/style.
- If a user says "bipedal chibi", prefer MCP `body_type="humanoid"` with chibi-like `proportions`, REST `template_id="mannequin"`, or Aseprite `bipedal-semi-chibi` depending on the surface.

Choose the template family by body plan and stance, not by species name alone. Map human/person/player/NPC/wizard/knight/robot/biped requests to the mannequin/humanoid animation family. Also map humanoid-stance animals or monsters, such as a horse person, cat warrior, fox mage, or any animal walking on two feet with arms, to mannequin/humanoid unless the existing managed character metadata proves it is quadruped.

If a character already exists, prefer its stored `template_id` from `get_character` or REST `GET /characters/{character_id}` over guessing from the prompt.

Default selection:

| User description | MCP create default | REST create default | Aseprite automatic default |
|---|---|---|---|
| Human, person, player, NPC, wizard, knight, robot, humanoid monster | `body_type="humanoid"` | `template_id="mannequin"` | `bipedal-realistic` unless chibi/tiny farming-RPG style is requested; override Aseprite's dialog default if it preselects `bipedal-semi-chibi` |
| Upright animal with arms or two-footed stance, such as a horse warrior or fox mage | `body_type="humanoid"` | `template_id="mannequin"` | `bipedal-realistic` or `bipedal-semi-chibi` by style |
| Small/chibi bipedal character | `body_type="humanoid"` plus chibi/cartoon proportions when available | `template_id="mannequin"` | `bipedal-semi-chibi` |
| Four-legged dog/cat/horse/bear/lion | `body_type="quadruped"` plus matching `template` | matching `template_id` | `quadrupedal-tiny` only for local Aseprite automatic animation |
| Four-legged animal outside the five managed quadruped families | `body_type="quadruped"` plus closest body-plan `template`, or ask if the stand-in changes output quality | closest `template_id`, or ask | `quadrupedal-tiny` only if using Aseprite's local automatic flow |

## Preset Animation IDs

Use exact ids. Do not send labels such as "Walk (8 frames)". This catalog was last verified against the website Add Animation bundle on 2026-06-30. Official REST docs expose the `template_animation_id` field but do not provide a stable public enum endpoint; refresh visible MCP tool docs or official docs before claiming "all available animations" or building long-lived integrations.

The sections are ordered by likely request frequency, with mannequin/humanoid first because most player, NPC, human, and biped requests map there.

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

If a user asks for a label that maps cleanly to one id, choose it. Common mappings and exact-id passthroughs:

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

If the requested animation exists for one template family but not another, say so and offer the closest same-family option. Do not silently substitute `walking-8-frames` for a quadruped `walk-8-frames` or vice versa.

## Frame Count And Ordering Rules

- Preset template mode owns its frame count through the selected template id. Do not set `frame_count` expecting it to override `walking-8-frames`.
- V3 custom mode owns frame count through `frame_count` 4-16, even only, default 8.
- Preserve returned frame order.
- Do not locally duplicate, trim, interpolate, reverse, or ping-pong frames unless the user explicitly asks for that packaging.
- Report the actual frame count returned if it differs from the id or expectation.

## Prompting And Descriptions

For template mode, keep `action_description` light or omit it. The template id carries the motion. Use `animation_name` for clear organization.

Good:

```json
{
  "template_animation_id": "walking-8-frames",
  "animation_name": "walk",
  "directions": ["south"]
}
```

Only add `action_description` when the user asks for a variant and the route supports it:

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

Do not use prompt enhancement for template mode. Use prompt enhancement only for v3 custom animation when appropriate and cost-approved.

## Verification

Before reporting success:

- Confirm requested `template_animation_id` was used.
- Confirm direction set and actual completed directions.
- Confirm returned frame count.
- Confirm dimensions match the character.
- Confirm transparent frames remain transparent when requested.
- If exporting through Aseprite, verify tag/frame count/order and that the original frames were not rewritten unexpectedly.

## When To Refresh Official Docs

Refresh official docs/OpenAPI/MCP docs before making exact code claims when:

- A template id is not in this reference.
- The visible MCP `animate_character` schema differs from this reference.
- The user asks for all available current animations.
- Pricing/cost or frame limits matter.
- Custom skeleton/keypoint support is requested.
