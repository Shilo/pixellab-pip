# Preset Skeleton And Template Animations

Read this for PixelLab requests involving skeletons, preset animations, template animations, built-in character animations, or named motions such as `walk-8-frames`, `walking-8-frames`, `idle`, `jump`, `bark`, `running-6-frames`, or "make the website's walk template".

Current focus: preset/template skeleton animations for managed characters. Custom skeleton authoring is future-facing; route custom keypoint work carefully to documented REST skeleton endpoints, and do not automate private website or Aseprite extension internals.

## Core Distinction

There are two different animation families:

| User intent | Meaning | Route |
|---|---|---|
| Preset/template/built-in animation | Animate an existing managed character using a named motion template such as `walk-8-frames`, `idle`, or `bark`. PixelLab generates frames for that character and direction. | Prefer MCP `animate_character`; fallback REST v2 `/characters/animations`. |
| Raw/custom skeleton animation | Generate frames from explicit skeleton keypoints, a reference image, optional masks/init images, and camera settings. | REST v2 `/animate-with-skeleton` and `/estimate-skeleton`. |

Do not call website/Aseprite private routes such as `/generate-animation/background` or extension suffixes such as `generate-animation`. They may reveal first-party behavior but are not stable public automation contracts.

## Default Route

For managed preset/template animations:

1. If PixelLab MCP tools are visible, use MCP first.
2. If MCP is unavailable or fails for a non-content reason and a PixelLab bearer token is configured, fall back to REST v2.
3. If the user explicitly asks for API/code/batch integration, use REST v2 directly.
4. If neither MCP nor REST auth is configured, stop before spending credits and route to setup; do not ask the user to paste secrets into chat.

This priority holds even when a REST/API secret exists. MCP remains the preferred agent workflow for managed character assets because it carries managed IDs, polling, downloads, and resource helpers. REST v2 is more feature-rich for exact schemas and raw skeleton keypoints.

If the user explicitly requested MCP, do not silently fall back to REST. Report that MCP tools are unavailable and ask before using REST v2.

## Managed Preset Animation With MCP

Use this when the user has or wants a managed character.

Typical flow:

1. `get_character(character_id)` to confirm status, template/body type, directions, size, existing animations, and downloadable assets.
2. Choose `template_animation_id` from the character template family.
3. Call `animate_character` with explicit `directions` unless the user asked for all directions.
4. Poll with `get_character` or the returned job IDs, depending on visible MCP tool behavior.
5. Download frames/ZIP only after completion if local files are needed.

MCP call shape:

```python
animate_character(
    character_id="...",
    template_animation_id="walk-8-frames",
    animation_name="walk",
    directions=["south"],
    mode="template",
)
```

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
  "character_id": "ab3dd5a1-a78e-46d2-b297-112d05cb3aaf",
  "mode": "template",
  "template_animation_id": "walk-8-frames",
  "animation_name": "walk",
  "directions": ["south", "east", "north", "west"]
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
bear
cat
dog
horse
lion
```

MCP `create_character` uses `body_type="quadruped"` plus `template` for animal families. Humanoid/mannequin characters may use `body_type="humanoid"` and available proportions/template controls in the visible MCP schema.

If a character already exists, prefer its stored `template_id` from `get_character` or REST `GET /characters/{character_id}` over guessing from the prompt.

## Preset Animation IDs

Use exact ids. Do not send labels such as "Walk (8 frames)". This catalog was last verified against the website Add Animation bundle on 2026-06-30. Official REST docs expose the `template_animation_id` field but do not provide a stable public enum endpoint; refresh visible MCP tool docs or official docs before claiming "all available animations" or building long-lived integrations.

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

If a user asks for a label that maps cleanly to one id, choose it. Examples:

| User says | Use id |
|---|---|
| "dog walk 8 frames" | `walk-8-frames` |
| "dog fast walk" | `fast-walk` |
| "humanoid walk 8 frames" | `walking-8-frames` |
| "fight idle" | `fight-stance-idle-8-frames` |
| "bark" | `bark` |

If the requested animation exists for one template family but not another, say so and offer the closest same-family option. Do not silently substitute `walking-8-frames` for a quadruped `walk-8-frames` or vice versa.

## Frame Count And Ordering Rules

- Preset template mode owns its frame count through the selected template id. Do not set `frame_count` expecting it to override `walk-8-frames`.
- V3 custom mode owns frame count through `frame_count` 4-16, even only, default 8.
- Preserve returned frame order.
- Do not locally duplicate, trim, interpolate, reverse, or ping-pong frames unless the user explicitly asks for that packaging.
- Report the actual frame count returned if it differs from the id or expectation.

## Prompting And Descriptions

For template mode, keep `action_description` light or omit it. The template id carries the motion. Use `animation_name` for clear organization.

Good:

```json
{
  "template_animation_id": "walk-8-frames",
  "animation_name": "walk",
  "directions": ["south"]
}
```

Only add `action_description` when the user asks for a variant and the route supports it:

```json
{
  "template_animation_id": "walk-8-frames",
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
