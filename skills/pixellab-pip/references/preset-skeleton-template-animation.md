# Preset Template And Raw Skeleton Animations

Read this for PixelLab character animation requests that use a preset/template/built-in motion or a custom skeleton. Exact preset ids are cataloged below.

SKILL.md holds the global rules this file does not restate: MCP-first routing with the not-configured / explicit-MCP fallback contract, the south-first direction default and ask-before-all-directions cost gate, frame-order preservation, and the ban on undocumented website / Aseprite-extension endpoints.

The workflows are managed preset/template animation, managed Skeleton v3 (preset or custom motion), raw Skeleton v3 keypoint animation, and the legacy raw skeleton endpoint. Use Skeleton v3 for an explicit new skeleton workflow; keep the legacy route only when its exact REST payload is required.

Engine selection is canonical in `animation.md` → Route Choice. Read this after selecting a template or skeleton workflow. The refreshed REST and MCP descriptions no longer state a Tier 1 gate, but availability and billing still come from the live surface.

## Table of Contents

- [Core Distinction](#core-distinction)
- [MCP vs REST v2 Field Coverage](#mcp-vs-rest-v2-field-coverage)
- [Managed Preset Animation (MCP)](#managed-preset-animation-mcp)
- [Managed Preset Animation (REST v2)](#managed-preset-animation-rest-v2)
- [Template Rendering And Tuning](#template-rendering-and-tuning)
- [Skeleton v3 Keypoint Animation](#skeleton-v3-keypoint-animation)
- [Skeleton v3 Custom Motion (Managed)](#skeleton-v3-custom-motion-managed)
- [Skeleton Estimation And Legacy Raw Animation](#skeleton-estimation-and-legacy-raw-animation)
- [Auto-Rig Skeleton Pipeline](#auto-rig-skeleton-pipeline)
- [Aseprite Boundary](#aseprite-boundary)
- [Preset Template Families](#preset-template-families)
- [Preset Animation IDs](#preset-animation-ids)
- [Frame Count](#frame-count)
- [Verification](#verification)

## Core Distinction

| User intent | Meaning | Route |
|---|---|---|
| Preset/template/built-in animation | Animate an existing managed character using a named motion template such as `walking-8-frames`, `breathing-idle`, or `jumping-1`. PixelLab generates frames for that character and direction. | Prefer MCP `animate_character`; fallback REST v2 `/characters/animations`. |
| Raw Skeleton v3 animation | Generate 3–15 frames from a reference image and a per-frame sequence of 18-joint keypoints. | MCP `animate_with_skeleton_v3` or REST `/animate-with-skeleton-v3`. |
| Managed Skeleton v3 animation | Custom humanoid motion, an MCP `move` from the documented quadruped lists, or an explicitly requested named preset. | MCP `animate_character(mode="skeleton-v3")`; without a template, MCP takes humanoid written poses or a tool-described move, while REST generates motion from action text. `poses`/`scale` are the humanoid path. For a requested preset add `template_animation_id`. See Skeleton v3 Custom Motion (Managed). |
| Legacy raw skeleton animation | Generate from the older three-frame skeleton payload with a reference image and optional masks/init images. | REST v2 `/animate-with-skeleton`. |

REST `/estimate-skeleton` estimates keypoints for one pose and remains a shared helper in the auto-rig pipeline; it is not a legacy animation route.

## MCP vs REST v2 Field Coverage

The current public MCP `animate_character` schema exposes `template`, `skeleton-v3`, `v3`, and `pixminimax` modes; it does not expose managed `pro`. It includes `template_animation_id`, `directions`, mode-specific `frame_count`, template-only `ai_freedom`, custom start/end frame base64/URL fields for v3 and PixMiniMax, `keep_first_frame`, `animation_group_id`, and PixMiniMax-only `subject_description`/`initial_pose`. For custom Skeleton v3 it also exposes `poses`, `scale`, and `move`, which REST does not expose. It does not expose REST's inline `enhance_prompt`. Connected client schemas may lag; check the visible mode before calling managed Skeleton v3 or PixMiniMax. Separate MCP `animate_with_skeleton_v3` accepts a raw reference image and keypoint sequence; it does not expose REST `/estimate-skeleton`.

It is not field-for-field equivalent to REST `/characters/animations`. REST additionally exposes `description`, `text_guidance_scale`, `outline`, `shading`, `detail`, `isometric`, `color_image`, `force_colors`, `target_palette` (pro, Skeleton v3, v3, and PixMiniMax modes), `seed`, and inline `enhance_prompt` (v3 mode); REST also retains managed `pro`. The REST `subject_description` and `initial_pose` fields are PixMiniMax-only; see `prompt-limits.md` for their surface-specific length contract. Use REST when those extra fields matter, for integration code, or to validate exact API behavior.

Template mode is nominally 1 generation per direction, but canvases over about 92px are billed per rendering batch. See `cost-routing.md` for the published batch sizes and check returned usage. MCP `animate_character`'s v3 mode also documents a canvas-area × frame-count budget that the REST managed-animation schema does not publish; see the `frame_count` field below.

## Managed Preset Animation (MCP)

Flow for an existing or wanted managed character:

1. `get_character(character_id)` to confirm status, template/body type, directions, size, existing animations, and downloadable assets.
2. Choose `template_animation_id` from the character's template family (catalog below).
3. `animate_character` with `character_id`, the chosen `template_animation_id`, explicit `directions`, and the `mode` selected under `animation.md` → Route Choice (`template` or `skeleton-v3`); optionally set `animation_name` as an organizational label.
4. Poll with `get_character` or the returned job IDs, per visible MCP tool behavior.
5. Download frames/ZIP only after completion if local files are needed.

Verify by canonical `template_animation_id`, direction, and frame count, not by a custom display name: MCP smoke (2026-06-30) showed `animation_name` did not override the stored canonical template label returned by `get_character`, and MCP exposed no usage/cost.

To turn a reference image or GIF frame into a managed character first, use MCP `create_character(mode="v3", description=..., reference_image_url=...)` — v3 is the only MCP mode that accepts a reference sprite; from scratch it outputs 8 directions, while a reference allows `n_directions` 4 or 8. Prefer the URL form over inline base64 (MCP clients truncate large inline base64). Choose text-only quadruped creation through SKILL.md's quadruped row rather than requiring a new reference. Reuse a supplied south-facing quadruped with matching `body_type="quadruped"` and `template` when v3 is selected; v3 from text is humanoid-only. With a v3 reference, set `n_directions` to 4 or 8 and pass a south-facing sprite as `reference_image_url`. Supply other views through `direction_images` to preserve them exactly and generate only missing directions. When the south-facing reference and `direction_images` cover every requested direction, PixelLab imports the supplied views for 0.25 generation total. Directions must match their labels and use the reference canvas size. If the MCP client cannot send an object for `direction_images`, send that same object JSON-encoded as a string. REST `create-character-v3` supports the corresponding quadruped reference with matching `template_id`. Then animate the returned `character_id` once the character completes. Fall back to REST when MCP is unavailable or REST's matching `template_id`, `no_background`, or `enhance_prompt` fields matter.

For a text-only quadruped when the user explicitly chooses Pro after cost disclosure:

```python
create_character(
    description="small black outline companion animal",
    mode="pro",
    body_type="quadruped",
    template="dog",
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

MCP `get_character` now documents a group ZIP download and a per-state spritesheet download; use the returned URL when either output fits. Use the REST `/zip` route above when its additional metadata is required; REST keypoints are documented only for template-based characters. See `job-lifecycle.md` for the MCP package differences.

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
| `mode` | `template`, `skeleton-v3`, `v3`, `pixminimax`, or REST-only legacy `pro`. Presets support `template` or `skeleton-v3`; use the mode selected under `animation.md` → Route Choice explicitly. Auto-detection selects template with a preset id, v3 otherwise. |
| `template_animation_id` | Exact preset id. Do not pass display labels. |
| `directions` | Be explicit to avoid accidental all-direction generation. |
| `frame_count` | v3: even 4–16; PixMiniMax: multiples of 4 from 4–40; default 8. MCP managed v3 additionally caps `width × height × frame_count` at `8 × 256 × 256` (256px canvas: at most 8 frames; 16 frames: up to about 180px). The REST managed schema does not publish that pixel budget. Custom Skeleton v3: 3–15; later directions reuse the group's count. Ignored by template, preset Skeleton v3, and pro; it does not override a preset's frame count. |
| `custom_start_frame` | Optional starting pose for v3 or PixMiniMax. Requires exactly one direction; max 256×256. Not available in template or Skeleton v3 mode; REST also rejects it in pro mode. |
| `end_frame` | Optional target pose for v3 or PixMiniMax interpolation. Dimensions must match the start frame, requires exactly one direction, and is not available in template or Skeleton v3 mode; REST also rejects it in pro mode. |
| `keep_first_frame` | v3 or PixMiniMax, default `true`. Controls whether the reference frame is stored as frame 0 (see Frame Count). Not available in template or Skeleton v3 mode; REST also rejects it in pro mode. |
| `action_description` | Optional in the MCP schema; provide it for custom motion. REST requires it when `template_animation_id` is omitted. In template mode, use it only for light customization. |
| `subject_description`, `initial_pose` | Optional PixMiniMax-only character and starting-pose captions; see `prompt-limits.md` for their surface-specific length contract. |
| `enhance_prompt` | REST only, valid for v3 custom mode; do not set it for template, PixMiniMax, pro, or Skeleton v3. |

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

Template mode does not expose direct controls for 3D depth maps, per-bone easing, stride curves, secondary motion, limb IK, `bone_scaling`, shadow strength, or keypoint edits, and `frame_count` does not tune preset motion; choose a different template id such as `walking-4-frames`/`walking-6-frames`/`walking-8-frames`. If the rendering style is the problem, propose a template retry with conservative style controls. If the gait itself is too rigid or robotic, offer free-form animation via `animation.md` → Route Choice; do not require another template attempt first. If the user wants to retain template motion, MCP `animate_character` exposes template-only `ai_freedom` (0–900, default 0 = rigid template following; higher lets the pose deviate more from the template skeleton). It does not tune Skeleton v3. Any extra paid attempt follows the existing retry approval rules.

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

## Skeleton v3 Keypoint Animation

Use this raw-image route with supplied or authored per-frame keypoints. It is a beta and requires 3–15 output-frame keypoint sets; each frame supplies the 18 named joints with normalized `x`/`y` coordinates from 0 to 1. The reference image and its `first_frame_keypoints` anchor the first pose, while `keypoints` contains the full ordered output sequence.

Use MCP `animate_with_skeleton_v3` when available, or REST `POST /v2/animate-with-skeleton-v3` for code and exact REST control. REST returns a background job; poll `GET /background-jobs/{job_id}`. MCP returns a job ID; retrieve the result with `get_image`. The result contains exactly `len(keypoints)` frames, in input order; it does not echo the reference frame.

The first pose is redrawn from the prompt and keypoints, so provide a close reference pose: a mismatch can affect the learned palette, background, and transparency. The input image is limited to 256×256. Supply each of the 18 named joints exactly once in `first_frame_keypoints` and every `keypoints` frame; their order is arbitrary. The joint labels are listed below; they are OpenPose COCO-18, so `ARM` is the wrist and `LEG` the ankle, and LEFT/RIGHT are the character's own sides (facing `east`, the RIGHT limbs are the near ones). Optional `z_index` accepts any integer as draw order (higher draws on top; default 0). Optional `depth` is 0–255 (about 128 is body center; higher is nearer); when omitted, the template's standing-pose depth for that direction is used. `description` is an appearance noun phrase (not pose, motion, style, or background); `action` is a short motion label because the keypoints carry the pose sequence. REST requires `direction`; `view` defaults to `low top-down` and `template_id` to `mannequin`, so set view/direction when the art needs a specific camera. Current cost examples are in `cost-routing.md`.

For managed motion follow the surface-specific section below; a requested preset instead adds `template_animation_id` to MCP `animate_character(mode="skeleton-v3")` or either REST managed-animation alias. Raw per-frame keypoints belong on `animate_with_skeleton_v3` or REST `/animate-with-skeleton-v3`.

## Skeleton v3 Custom Motion (Managed)

This beta workflow renders one shared 3D motion on an existing managed character, for one or several directions. Engine and custom-vs-preset selection are canonical in `animation.md` → Route Choice. Omit `template_animation_id`; managed pose objects are not raw COCO-18 `keypoints`. Use `frame_count` 3–15 (default 8). For humanoids, author one `poses` item per frame and optional per-pose `scale`; MCP `move` also supports the tool description's dedicated move lists for dog, cat, horse, bear, and lion templates. Use the body-specific names and controls for those quadruped moves; do not infer that `poses` or `scale` accepts quadruped bodies. Do not apply v3's even-only or PixMiniMax's multiple-of-four rule here.

- **MCP:** inspect the character with `get_character` and check that the connected `animate_character` schema exposes `poses`. For a new custom motion, call with `mode="skeleton-v3"`, the character id, `action_description`, the intended `frame_count` and explicit `directions`, but no `poses`, `scale`, `move`, or `animation_group_id`. This is the documented free instruction call; use its character measurements and pose units rather than guessing coordinate units, joint semantics, or reach. Then submit the agreed motion. The exposed pose fields are `frame`, `pelvis`, `hips`, `chest`, `lean`, `head`, `right_hand`, `left_hand`, `right_elbow`, `left_elbow`, `right_foot`, and `left_foot`. Optional `scale` with poses supplies one size per frame (1 = rest size). Alternatively, `move` lays out a named motion; use the connected `animate_character` tool description for allowed move names and controls, including the body-specific move lists. A pose can position a hand for a held prop, but there is no prop field and the tool does not draw the prop. The submission queues paid jobs; the free instruction response is not a completed animation.
- **REST:** current `CreateCharacterAnimationRequest` has no `poses`, `scale`, or `move` and rejects extra properties. Send `mode="skeleton-v3"`, `action_description`, `frame_count`, and explicit `directions` to `/animate-character` or `/characters/animations`; the server writes the shared motion from the action text (documented ~15 seconds before rendering jobs start). This is a generation request, not MCP's free instruction call. Do not silently substitute text-generated REST motion when the user requested exact written poses; offer raw keypoints or a client exposing the MCP fields.

To add directions to an existing custom Skeleton v3 group, reuse its `animation_group_id` and `animation_name`; the motion and frame count are reused, so do not resend `poses` or invent a different count. Pricing is in `cost-routing.md`.

Poll queued directions with `get_character` (REST: each returned `background_job_ids` entry via `GET /background-jobs/{job_id}`, then the character getter). Do not pass custom start/end images, `keep_first_frame`, template-only `ai_freedom`, or inline `enhance_prompt` for this mode. REST `target_palette` is supported for Skeleton v3; MCP `animate_character` has no equivalent palette field, so use REST for exact-palette managed Skeleton v3 animation. Shared motion does not promise pixel-identical frames, exact joint placement, perfect loops, or independently generated equipment layers that align.

Inspect every direction for grip continuity, missing or smeared held gear, limb occlusion and canvas growth. Coherent body motion or shared poses do not prove correct gear or handedness. A hand crossing the screen center during a cross-body swing is not by itself a hand switch.

## Skeleton Estimation And Legacy Raw Animation

REST `estimate-skeleton` remains useful for estimating one starting pose in an auto-rig pipeline; it does not create a full motion sequence. Use the legacy animation route only when the user needs its exact three-frame payload or optional legacy fields. New custom 3–15-frame pose sequences belong on Skeleton v3.

```text
POST /v2/estimate-skeleton
POST /v2/animate-with-skeleton
```

`estimate-skeleton` takes a character image (body `{"image": {...}}`, any size up to 256×256) and returns one pose's keypoints, with `x`/`y` as 0–1 fractions of the image you sent, ready for Skeleton v3 `keypoints`/`first_frame_keypoints`. It costs 0.1 generation; a fully transparent image is refused with 422 before any charge. `animate-with-skeleton` accepts fields such as:

```text
image_size
reference_image
skeleton_keypoints  (exactly 3 frames)
view
direction
guidance_scale
init_images
inpainting_images
mask_images
color_image
seed
```

MCP `animate_with_skeleton_v3` accepts raw keypoints for Skeleton v3, but there is no MCP equivalent of REST `estimate-skeleton` or the legacy `/animate-with-skeleton` payload. Use REST for estimation or the legacy route; do not treat the new animation tool as field-for-field support for the legacy route.

## Auto-Rig Skeleton Pipeline

Use this workflow for "auto rig", "estimate skeleton", "rig this sprite", "export skeleton for API", "animate with this skeleton", "my keypoints", "pose JSON", or a skeleton pipeline from a simple humanoid prompt. Estimation remains REST-first; use Skeleton v3 for per-frame animation when the full pose sequence is available:

```text
source image or generated reference frame
  -> REST estimate-skeleton
  -> save/export keypoint JSON
  -> author or edit a 3–15-frame pose sequence
  -> MCP animate_with_skeleton_v3 or REST animate-with-skeleton-v3
```

Raw skeleton animation is the right route when the user wants to own, export, edit, or reuse the keypoints; managed template animation is still right for built-in managed motions.

| User starts with | Best route |
|---|---|
| Existing sprite/image | Use it as the `estimate-skeleton` input and as the Skeleton v3 `first_frame`; author the remaining per-frame keypoints before animation. |
| Aseprite-authored skeleton | Export from Aseprite, map joints to the live Skeleton v3 schema, and supply a full 3–15-frame sequence; use the conversion below only for the legacy REST endpoint. |
| Prompt only ("humanoid knight") | Create or ask for a base reference frame first; prefer a PixelLab-generated humanoid/mannequin frame, then estimate keypoints from it. |
| Existing managed character id | Preset motions: MCP/REST managed template animation. Managed Skeleton v3 can use a preset or custom motion as described above. Fetch a frame and author raw per-frame keypoints when the user needs raw sequence ownership. |

For simple humanoid prompts default the body plan to humanoid/mannequin (MCP `create_character(body_type="humanoid")` or REST `create-character-v3` with `template_id="mannequin"`).

Legacy REST `/animate-with-skeleton` steps:

1. Estimate or author keypoints. REST `POST /v2/estimate-skeleton` for a sprite/image; Aseprite "Export skeleton for API" writes normalized `pose_keypoints`. Local tooling may edit/validate JSON keypoints client-side (not a PixelLab API call).
2. Convert exported keypoints to the target REST field: Aseprite `{ "pose_keypoints": [[...], ...] }` -> REST animation `skeleton_keypoints: [[...], ...]`; REST single-image BitForge `skeleton_keypoints: [...]`.
3. Call `POST /v2/animate-with-skeleton` with `image_size`, `reference_image`, `skeleton_keypoints`, and explicit `view`/`direction`.
4. Add `init_images`, `inpainting_images`, `mask_images`, or `color_image` when the user supplied those roles or the route requires them.

`estimate-skeleton` returns a skeleton for one pose; it does not invent a walk/run sequence. The legacy `animate-with-skeleton` requires exactly 3 keypoint frames (any other count returns 422). Skeleton v3 accepts 3–15 pose sets, but still requires the sequence; with only one estimated pose, author the remaining poses or use managed template animation or text animation if the user does not need keypoint control.

### View/Direction Trap And Defaults

- For a typical RPG/down-facing sprite, set `view="low top-down"` and `direction="south"` explicitly.
- For side-view/platformer sprites, set `view="side"` and `direction="east"` or `west`.
- Do not rely on `animate-with-skeleton` defaults: current OpenAPI defaults are `view="side"` and `direction="east"`, which are wrong for many RPG sprites. Do not infer defaults from website managed-character examples, which may use low top-down/south.
- Interpret human/person/player/NPC/robot/humanoid-monster and upright two-legged animals as humanoid/mannequin.
- Save a sidecar manifest with `body_plan`, `source_image`, `image_size`, `view`, `direction`, `estimated_keypoints`, and the payload-ready `skeleton_keypoints`.

Current schema requires `image_size` and `reference_image`; custom keypoint workflows also need explicit `skeleton_keypoints` or a prior `estimate-skeleton`. Endpoint prose lists common sizes `16`, `32`, `64`, `128`, `256` while schema may allow other 16-256 dimensions; refresh OpenAPI before exact production code for nonstandard sizes, and ask for missing image/keypoint roles before spending credits.

## Aseprite Boundary

Estimate skeleton maps to REST `POST /v2/estimate-skeleton`; Skeleton v3 animation maps to MCP `animate_with_skeleton_v3` or REST `POST /v2/animate-with-skeleton-v3`; the legacy route remains REST `POST /v2/animate-with-skeleton`. Pose-guided image generation maps to REST `create-image-bitforge` (`skeleton_keypoints`/`skeleton_guidance_scale`). Aseprite exports normalized `pose_keypoints`; map the joints and frames to the selected live schema rather than assuming the legacy `skeleton_keypoints` shape is interchangeable. Other Aseprite extension operations (edit skeleton, re-pose, insert template skeleton, private template-animation flow, and local skeleton JSON) remain editor-internal for public automation. Aseprite's local template catalog is older/smaller than the managed preset IDs below; do not assume every managed id such as `breathing-idle` or `jumping-1` exists there.

## Preset Template Families

Known managed template families, last verified against MCP docs, REST OpenAPI, and the website Add Animation bundle on 2026-06-30: `mannequin`, `dog`, `cat`, `horse`, `bear`, `lion`.

Use the right vocabulary for the surface:

| Surface | Field | Valid values | Notes |
|---|---|---|---|
| MCP `create_character` | `body_type` | `humanoid`, `quadruped` | Use `humanoid` for bipedal/mannequin body plans. Use `quadruped` only for four-legged animals. |
| MCP `create_character` | `template` | `bear`, `cat`, `dog`, `horse`, `lion` | Required only when `body_type="quadruped"`. Ignored for humanoid characters. |
| MCP `create_character` | `proportions` | JSON string, e.g. `proportions='{"type":"preset","name":"chibi"}'`; presets `default`, `chibi`, `cartoon`, `stylized`, `realistic_male`, `realistic_female`, `heroic`, or custom scale JSON | Humanoid standard-mode control, not a `body_type`. A bare preset name or prose is invalid. |
| MCP `create_character_pro_flash` | `template_id` | `mannequin`, `bear`, `cat`, `dog`, `horse`, `lion`, `custom` | For a body with no matching family, `custom` is accepted. Acceptance alone does not establish skeleton or preset-animation support; inspect the completed character's body/template metadata before choosing animation. |
| REST `create-character-pro` / `create-character-v3` | `template_id` | `mannequin`, `bear`, `cat`, `dog`, `horse`, `lion`, `custom` | `mannequin` is the bipedal/humanoid skeleton reconstruction template and the default in current OpenAPI. `humanoid` is **not** a template id — it fails with "Template not found". `custom` skips the skeleton for bodies that fit no template; it cannot use skeleton-based animation. |
| REST managed animation | `template_animation_id` | Exact animation ids from the character's family | Does not take `body_type`; the managed character already carries the body plan/template family. |
| Website Add Animation | `Template` | `mannequin`, `dog`, `cat`, `horse`, `bear`, `lion` | UI label for the managed character's animation family. |

Choose the template family by body plan and stance, not species. Map human/person/player/NPC/wizard/knight/robot/biped requests, and upright/two-footed animals (horse person, cat warrior, fox mage), to humanoid/mannequin unless managed metadata proves quadruped. Four-legged dog/cat/horse/bear/lion map to `quadruped` plus the matching `template`; a four-legged animal outside these five uses the closest template or ask. Treat "mannequin" and misspellings like "manniquin" as the humanoid plan. Gotcha: do not pass `template="mannequin"` to MCP `create_character` (`template` is quadruped-only there); REST uses `template_id="mannequin"`. If a character already exists, prefer its stored `template_id` from `get_character` / REST `GET /characters/{character_id}` over guessing from the prompt.

## Preset Animation IDs

Use exact ids. Do not send labels such as "Walk (8 frames)". The humanoid ids and frame counts below are verified against the refreshed public MCP guide; the quadruped lists retain the 2026-06-30 website catalog and should be checked with `get_character` for the selected template. Official REST docs expose the `template_animation_id` field but no stable public enum endpoint; refresh visible MCP tool docs or official docs before claiming "all available animations" or building long-lived integrations.

Ordered by likely request frequency, mannequin/humanoid first because most player, NPC, human, and biped requests map there.

### mannequin

| Template id | Frames |
|---|---|
| `walk` | 6 |
| `walk-1` | 6 |
| `walk-2` | 6 |
| `walking` | 6 |
| `walking-2` | 4 |
| `walking-3` | 6 |
| `walking-4` | 6 |
| `walking-5` | 4 |
| `walking-6` | 6 |
| `walking-7` | 6 |
| `walking-8` | 6 |
| `walking-9` | 6 |
| `walking-10` | 6 |
| `walking-4-frames` | 4 |
| `walking-6-frames` | 6 |
| `walking-8-frames` | 8 |
| `running-4-frames` | 4 |
| `running-6-frames` | 6 |
| `running-8-frames` | 8 |
| `running-slide` | 6 |
| `crouched-walking` | 6 |
| `crouching` | 5 |
| `sad-walk` | 8 |
| `scary-walk` | 8 |
| `breathing-idle` | 4 |
| `fight-stance-idle-8-frames` | 8 |
| `backflip` | 10 |
| `front-flip` | 6 |
| `getting-up` | 5 |
| `jumping-1` | 9 |
| `jumping-2` | 8 |
| `running-jump` | 8 |
| `two-footed-jump` | 7 |
| `cross-punch` | 6 |
| `lead-jab` | 3 |
| `surprise-uppercut` | 7 |
| `hurricane-kick` | 4 |
| `roundhouse-kick` | 7 |
| `high-kick` | 7 |
| `flying-kick` | 6 |
| `leg-sweep` | 7 |
| `fireball` | 6 |
| `taking-punch` | 6 |
| `falling-back-death` | 7 |
| `drinking` | 6 |
| `picking-up` | 5 |
| `pull-heavy-object` | 6 |
| `pushing` | 6 |
| `throw-object` | 7 |

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

After a preset motion has been selected, use these label mappings and exact-id passthroughs:

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
| Humanoid hurt, recoil, stagger, hit | `taking-punch` |
| Humanoid death / recovery | `falling-back-death` / `getting-up` as separately requested clips |
| Humanoid dash, dodge, sprint | Offer `running-slide` or `running-jump` when that motion fits |
| Humanoid cast, spell, magic | `fireball` when that motion fits |

Do not invent ids such as `hurt`, `dashing`, `casting`, `backstep-dodge`, `shooting`, or `staff-spin-attack`: MCP says they are rejected before queueing. If no preset fits, offer custom action text via `animation.md` → Route Choice instead. If an animation exists for one template family but not another, say so and offer the closest same-family option. Do not silently substitute `walking-8-frames` for a quadruped `walk-8-frames` or vice versa.

## Frame Count

- The humanoid table gives the exact output count in template mode and the pose count in preset managed Skeleton v3. Custom managed Skeleton v3 uses 3–15 frames instead. Use those pose counts with the pricing schedule in `cost-routing.md`.
- Preset template mode owns its frame count through the selected template id; do not set `frame_count` expecting it to override `walking-8-frames`.
- V3 custom mode uses `frame_count` 4–16, even only, default 8. Managed PixMiniMax mode uses multiples of 4 from 4–40, default 8. Both store the reference frame as frame 0 unless `keep_first_frame=false`; details in `animation.md`.
- Report the actual returned frame count if it differs from the id or expectation.

## Verification

Before reporting success, confirm: the selected mode and preset id or custom motion were used; the requested vs actually completed direction set; the returned frame count and dimensions. Managed animation can expand the source canvas; report a fixed-size mismatch rather than assuming source dimensions were retained. If exporting through Aseprite, verify tag/frame count/order and that the original frames were not rewritten.

Refresh official docs/OpenAPI/MCP docs before exact code claims when a template id is not here, the visible MCP schema differs, the user asks for all current animations, pricing/frame limits matter, or custom skeleton/keypoint support is requested.
