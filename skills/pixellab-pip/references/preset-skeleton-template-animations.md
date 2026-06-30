# Preset Template And Raw Skeleton Animations

Read this for PixelLab requests involving skeletons, preset animations, template animations, built-in character animations, or named motions such as `walking-8-frames`, `breathing-idle`, `jumping-1`, `running-6-frames`, or "make the website's walk template".

Current focus: preset/template animations for managed characters, plus boundary guidance for raw skeleton/keypoint routes. Custom skeleton authoring is future-facing; route custom keypoint work carefully to documented REST skeleton endpoints, and do not automate private website or Aseprite extension internals.

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

MCP `animate_character` is fully suitable for normal managed-character template animation work: template mode, v3 custom mode, explicit directions, and `frame_count` for v3. When the visible MCP schema exposes pro mode with cost confirmation, it can also route pro animation. Use MCP first when the tools are visible.

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

Current OpenAPI defaults raw `animate-with-skeleton` to `view="side"` and `direction="east"`. Do not infer raw skeleton defaults from website managed-character examples, which may use low top-down/south or another stored character view/direction. Endpoint prose lists common supported sizes `16`, `32`, `64`, `128`, and `256`, while schema behavior can allow other 16-256 dimensions; verify current OpenAPI before writing exact production code for nonstandard sizes.

Before exact calls, refresh OpenAPI. Current schema requires `image_size` and `reference_image`; custom keypoint workflows also need explicit `skeleton_keypoints` or a prior `estimate-skeleton` step. Ask for missing image/keypoint roles before spending credits.

If the user says "custom skeleton", "my keypoints", "pose JSON", "export skeleton", or "animate with this skeleton", ask for or infer the required image/keypoint roles before spending credits. If the user simply says "skeleton walk template" or "preset skeleton animation", use managed template animation instead.

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
- Inspecting local skeleton reference files for research only.

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
| Human, person, player, NPC, wizard, knight, robot, humanoid monster | `body_type="humanoid"` | `template_id="mannequin"` | `bipedal-realistic` unless chibi/tiny farming-RPG style is requested |
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
  "action_description": "a steady cheerful walk with a slight head bob"
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
