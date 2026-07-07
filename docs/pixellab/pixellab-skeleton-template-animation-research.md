# PixelLab Skeleton And Template Animation Research

Generated: 2026-06-30.

Scope: developer-facing research on PixelLab preset skeleton/template character animations and the REST-first auto-rig/keypoint pipeline for estimating, exporting, and animating skeleton data. This document focuses on observed website behavior, public REST v2/MCP equivalents, and the Aseprite extension's local skeleton/template evidence. It does not cover a full custom skeleton authoring UI beyond the current estimate/export/animate surfaces.

## Executive Summary

PixelLab has two related but distinct animation concepts:

| Concept | Meaning | Best supported automation surface |
| --- | --- | --- |
| Managed template animation | Animate an existing managed character by applying a named preset motion template such as `walk-8-frames`, `idle`, or `bark`. The output frames are generated per character and per direction. | MCP `animate_character`; REST v2 `POST /characters/animations` or `POST /animate-character`. |
| Raw skeleton animation | Generate an animation from supplied skeleton keypoints, reference image, optional init/inpaint/mask images, and camera settings. | REST v2 `POST /animate-with-skeleton`. |

The built-in website Add Animation buttons for a created character are managed template animations, not a public "download pre-generated walk sprites" feature. The selected template animation id is used as a motion guide, while the character's existing rotation image is used as the identity/style/first-frame anchor.

PixelLab now recommends **Animate with text (new)** — REST `POST /v2/animate-with-text-v3` — over the skeleton-based routes, covering both the managed preset/template animations (`walking-8-frames`, `idle`, etc.) and raw skeleton keypoints. Per the PixelLab team, the skeleton model is an older model; text animation is simpler and generally produces better results. Reach for the template or raw-skeleton routes when you specifically want a named preset motion, need to own/export/edit keypoints, or have another specific reason.

For the website example:

```text
Template: dog
Selected option: Walk (8 frames)
Template animation id: walk-8-frames
Character size: 92x92
Directions: 4 cardinal directions in the observed UI
```

The closest supported programmatic equivalent is:

```text
MCP:  animate_character(character_id, template_animation_id="walk-8-frames", mode="template")
REST: POST /v2/characters/animations with mode="template" and template_animation_id="walk-8-frames"
```

## Evidence Sources

Official/public sources checked:

- `https://api.pixellab.ai/v2/llms.txt`
- `https://api.pixellab.ai/v2/openapi.json`
- `https://api.pixellab.ai/mcp/docs`
- `https://www.pixellab.ai/docs/tools/animate-with-text-new`
- `https://www.pixellab.ai/docs/tools/animate-with-text-pro`
- `https://www.pixellab.ai/docs/tools/animate-with-skeleton`
- `https://www.pixellab.ai/docs/tools/create-animations-automatic`

First-party UI/editor observations:

- Website Add Animation UI, observed 2026-06-30.
- Installed Aseprite extension UI labels and behavior, observed 2026-06-30.

Per the docs publication rules, local extension sources are used only as uncited terminology and behavior evidence. This document intentionally avoids local file paths, source filenames, source snippets, credentials, and automation instructions for undocumented first-party routes.

## Website Add Animation Behavior

The website Add Animation page is a client-rendered first-party flow. Observation of that flow shows the important behavior:

1. The page fetches the managed character using the signed-in website session.
2. The loaded character object includes `template_id`, `rotation_urls`, `size`, `view`, `style_settings`, `bone_scaling`, `guidance`, `ai_freedom`, and existing `animations`.
3. Built-in animation options are selected from a template-specific list keyed by the character template id.
4. When a built-in option is submitted, the website uses an undocumented first-party background job route.
5. The website polls that first-party job until frames are ready.

The first-party website request is not the recommended automation contract. Treat this as observed first-party behavior only: it wraps a nested generation request that includes the managed character id, the selected `template_animation_id`, template-family information, the selected animation id, and the existing direction frame as an identity/style/first-frame anchor.

Important interpretation:

- `template_id` identifies the character/motion family, such as `dog`, `cat`, `horse`, `lion`, `bear`, or `mannequin`.
- `template_animation_id` identifies the preset motion, such as `walk-8-frames`.
- `extra_frozen_first_frame` and calibration image anchor the generated output to the existing character direction.
- The returned animation is generated output. The preset is not merely a static pre-rendered spritesheet being copied into the user's account.

### Managed Template Rendering Artifacts

A 2026-06-30 live humanoid horse `walking-8-frames` north test showed an important behavior boundary: the preset moved arms and legs according to the humanoid walk, but the generated frames gained consistently heavy dark leg shadows and a rigid, upright gait. Frame inspection showed the dark-pixel share stayed high across all eight frames, which indicates a persistent generation/style interpretation rather than a single bad frame.

The practical model is skeleton-guided frame generation, not a clean composite of prebuilt limb sprites over an unchanged character. PixelLab uses the managed character, stored body/template family, selected `template_animation_id`, direction frame, and style settings to generate new frames. Because the frames are generated, template mode can re-interpret shading, contrast, joint detail, and body stiffness even when the skeleton motion itself is correct.

Public template-mode tuning is limited to generation controls such as `action_description`, `text_guidance_scale`, `outline`, `shading`, `detail`, `color_image`, `force_colors`, `seed`, and explicit `directions`. These can help with style artifacts such as excessive shadows or palette drift, but they are soft controls rather than deterministic animation-rig parameters.

No public managed-template field currently exposes direct 3D depth maps, per-bone easing, stride curves, secondary motion, limb IK, shadow-strength controls, editable keyframes, or `bone_scaling` as an animation-generation input. When the gait itself is too robotic, use managed v3/pro custom animation or raw skeleton/Aseprite keypoint authoring rather than expecting `walking-8-frames` to be a full rig editor.

### Humanoid Horse Walk Template Batch Study

A focused 2026-06-30 batch tested the humanoid/mannequin `walking-8-frames` template on a horse-headed bipedal character. The test character was an upright humanoid horse with a horse head, arms, legs, and a relaxed idle stance. The character was intentionally treated as a humanoid/mannequin body plan rather than a quadruped horse, because the sprite walks on two feet and has arms.

The source setup used a single south/down-facing idle frame as the visual reference for managed character creation. The managed character was created with a mannequin/humanoid template family, low top-down RPG view, transparent background, and 92x92 output size. The animation tests then used the same managed character and the same south direction unless noted otherwise.

The purpose of the batch was not to find a final production animation. It was to isolate which public inputs affected three observed failure modes:

- Direction/head instability: some generated frames turned the head or upper body toward the back-facing/north pose even though the requested direction was south.
- Shading artifacts: the legs received hard, dark shadow bands that looked unnatural for the character style.
- Motion quality: arms and legs moved consistently, but the gait remained rigid and robotic, with limited organic weight transfer.

Manifest-style trial summary:

| Row | Route | Mode | Template id | Direction | Seed | Action text | Style fields | Returned frames | Observed result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | MCP `animate_character` after REST managed character creation | `template` | `walking-8-frames` | `south` | Not set | None | None | 8 | Severe direction/head flip in the final frames; some frames showed a back-facing head/body interpretation despite the south request. |
| 1 | REST `POST /v2/characters/animations` | `template` | `walking-8-frames` | `south` | Fixed seed | None | None | 8 | Head stayed south/front-facing. Motion remained stiff and leg shading remained high-contrast. This suggests the row 0 flip was generation variance rather than a wrong direction request. |
| 2 | REST `POST /v2/characters/animations` | `template` | `walking-8-frames` | `south` | Same fixed seed | None | `shading="flat shading"` | 8 | Head/back flip returned in some frames. Hard leg shadows were not reliably fixed. For this character, `shading="flat shading"` by itself was not a stable correction. |
| 3 | REST `POST /v2/characters/animations` | `template` | `walking-8-frames` | `south` | Same fixed seed | Direction-lock wording only | None | 8 | Head stayed south/front-facing. Arm and leg cycling remained consistent but still rigid. |
| 4 | REST `POST /v2/characters/animations` | `template` | `walking-8-frames` | `south` | Same fixed seed | Direction-lock wording plus shadow/naturalness wording | None | 8 | Similar to row 3. The additional wording about shoulder sway, weight shift, flat colors, and avoiding heavy shadows did not materially improve gait quality. |
| 5 | REST `POST /v2/characters/animations` | `v3` | None | `south` | Same fixed seed | Custom natural walk wording | `frame_count=8` | 9 | Head stayed stable and dark pixels were lower, but output returned nine images and the pose read more like arms-spread stepping than a clean walk. |

The exact user-facing visual description used when creating the managed character was:

```text
a horse-headed humanoid character standing in a relaxed idle pose, bipedal upright body, RPG pixel art, transparent background
```

Rows 0, 1, and 2 did not provide animation action text. They relied on the template id and the managed character's stored description/settings. Rows 3 and 4 tested whether template mode would follow additional action text while still using the preset motion. Row 5 tested non-template v3 custom animation as a control.

Row 3 action text:

```text
A front-facing south/down-facing walking cycle. Keep the horse head, face, chest, and belly facing the camera in every frame; do not turn around or show the back of the head. Natural relaxed arm swing and subtle weight shift.
```

Row 4 action text:

```text
A front-facing south/down-facing walking cycle. Keep the horse head, face, chest, and belly facing the camera in every frame; do not turn around or show the back of the head. Natural relaxed arm swing, subtle shoulder sway, and gentle weight shift. Keep flat colors and avoid heavy dark leg shadows.
```

Row 5 v3 control action text:

```text
A front-facing south/down-facing natural relaxed walk cycle. The horse head, face, chest, and belly stay facing the camera every frame. Subtle shoulder sway, gentle weight shift, relaxed arm swing, soft flat colors, no heavy dark leg shadows.
```

Quantitative inspection supported the visual reading. The original MCP-default output had a high opaque-pixel count and a high dark-pixel share. Template rows 1-4 had similar dimensions and frame counts, but rows 3 and 4 were the most stable for head direction. The `flat shading` row did not reduce dark-pixel share reliably and reintroduced orientation instability. The v3 row reduced the average dark-pixel share but did not preserve the requested eight-frame count and did not produce a better walk cycle.

Interpretation:

- Explicit `directions=["south"]` is necessary but not sufficient. The template renderer can still reinterpret individual frames if the prompt and random seed allow direction ambiguity.
- A fixed seed can remove a bad stochastic head flip in one run, but it should not be treated as a universal quality fix.
- Direction-lock `action_description` is the strongest observed mitigation for head flipping in south-facing humanoid template walks.
- Additional action wording about subtle shoulder sway, weight shift, and natural motion did not materially change the preset gait. The built-in template appears to dominate limb timing and body mechanics.
- `shading="flat shading"` is a soft style control, not a deterministic shadow-removal control. It may be appropriate to try when hard shadows are unacceptable, but this batch showed it can interact with generation variance and destabilize orientation.
- Preset template mode is useful for cheap, consistent arm/leg cycling and quick managed-character motion. It should not be presented as a reliable route for natural locomotion on characters where organic weight transfer, nuanced easing, or authored acting quality matters.

Recommended routing consequence:

- If the user asks for a cheap/simple managed walk, use template mode and include explicit direction-lock text when the character is front-facing or direction-sensitive.
- If the user asks for a natural, polished, or less robotic walk, warn that preset template mode is likely insufficient. Prefer raw animation routes such as `animate-with-text-*`, pro/custom managed animation when appropriate, or a custom skeleton/keypoint workflow.
- If the user specifically wants skeleton ownership, natural locomotion, or editable gait, use the raw skeleton pipeline: estimate or author keypoints, build a multi-frame keypoint sequence, then call `animate-with-skeleton`.
- Do not assume that adding naturalness language to a preset template will meaningfully alter the preset's gait mechanics. Treat it mainly as a style/orientation hint.

### Public API Boundary

The website and Aseprite extension expose useful evidence about PixelLab product behavior, but their private request shapes, session behavior, and editor operation channels are not public automation contracts. Use them only as terminology and behavior evidence. Programmatic integrations should use official REST v2 routes or MCP tools unless PixelLab publishes a first-party route in public docs.

## Public REST v2 Managed Character Animation

Current OpenAPI documents two managed character animation paths:

| Endpoint | Notes |
| --- | --- |
| `POST /v2/characters/animations` | Current documented managed character animation endpoint. The schema describes `template`, `v3`, and `pro` modes. |
| `POST /v2/animate-character` | Also documented with the same request schema. Older descriptive text remains here, but the schema is current. |

Both use `CreateCharacterAnimationRequest`.

Key request fields:

| Field | Role |
| --- | --- |
| `character_id` | Existing managed character id. Required. |
| `mode` | `template`, `v3`, or `pro`. Auto-detected as `template` when `template_animation_id` is provided; otherwise `v3`. |
| `template_animation_id` | Preset skeleton/template animation id. Required for template mode. |
| `action_description` | Required for custom `v3`/`pro`; optional customization/description in template mode. |
| `animation_name` | Name stored for this animation; defaults from action when omitted. |
| `directions` | Directions to animate. Template mode defaults to all available character directions. Custom mode defaults to south only. |
| `frame_count` | Only used in `v3` custom mode. Even integer 4-16, default 8. Ignored by template mode. |
| `outline`, `shading`, `detail` | Template-mode style overrides. Defaults to character settings. |
| `text_guidance_scale` | Template-mode prompt following strength. |
| `enhance_prompt` | Only valid for `mode="v3"`; not for template/pro. |

Secondary request fields include `description`, `color_image`, `force_colors`, `isometric`, and `seed`. These can matter for exact API integrations, especially when trying to reduce template-mode style drift, but they should not be confused with the primary preset contract: `character_id`, `mode="template"`, `template_animation_id`, and explicit `directions`.

Response:

```json
{
  "background_job_ids": ["job id per direction"],
  "directions": ["south", "east"],
  "status": "processing"
}
```

`CreateCharacterAnimationResponse` can also include `enhanced_prompt` and `enhance_usage`, but only when `enhance_prompt=true` is used in `mode="v3"`. Prompt enhancement is not valid for template/pro mode.

Poll with:

```text
GET /v2/background-jobs/{job_id}
```

Related managed character lifecycle routes:

```text
POST /v2/characters/animations
POST /v2/animate-character
GET /v2/background-jobs/{job_id}
GET /v2/characters
GET /v2/characters/{character_id}
GET /v2/characters/{character_id}/zip
PATCH /v2/characters/{character_id}/tags
DELETE /v2/characters/{character_id}
```

Template-mode cost is documented as lower than custom/pro in both REST descriptions and MCP docs. The public docs describe template mode as one generation per direction, while custom/pro is significantly more expensive.

### REST Example: Dog Walk 8 Frames

```bash
curl -X POST "https://api.pixellab.ai/v2/characters/animations" \
  -H "Authorization: Bearer $PIXELLAB_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "ab3dd5a1-a78e-46d2-b297-112d05cb3aaf",
    "mode": "template",
    "template_animation_id": "walk-8-frames",
    "animation_name": "walk",
    "directions": ["south", "east", "north", "west"]
  }'
```

For an 8-direction character:

```json
[
  "south",
  "south-east",
  "east",
  "north-east",
  "north",
  "north-west",
  "west",
  "south-west"
]
```

## MCP Managed Character Animation

The MCP docs describe managed asset workflows as the preferred agent surface when MCP tools are visible:

```python
create_character(description="wizard", n_directions=8)
animate_character(character_id, "walk")
animate_character(character_id, "idle")
```

Relevant tools:

| MCP tool | Role |
| --- | --- |
| `create_character` | Creates managed humanoid or quadruped characters. |
| `animate_character` | Queues managed character animation jobs. |
| `get_character` | Polls/reads character status, rotation URLs, animations, and download link. |
| `delete_animation` | Deletes character animations by type/direction. |
| `get_balance` | Checks available account balance/credits. |

`animate_character` parameters documented in MCP:

| Parameter | Notes |
| --- | --- |
| `character_id` | Existing character id. |
| `template_animation_id` | Preset animation id such as `walk-8-frames`; optional for custom mode. |
| `action_description` | Custom motion text; optional in template mode. |
| `animation_name` | Stored name. |
| `directions` | Requested directions. |
| `mode` | `template`, `v3`, or `pro` when exposed by the tool. |
| `frame_count` | Default 8; relevant for v3 custom animations. |
| `confirm_cost` | Cost confirmation gate in MCP. |

Recommended MCP flow for preset skeleton/template animations:

1. Use `get_character(character_id)` to confirm template id, directions, size, and current animations.
2. Pick a template animation id compatible with the character template/body type.
3. Use `animate_character` with `template_animation_id` and explicit `directions`.
4. Poll with `get_character` until the new animation appears, or use any returned job ids if the client exposes them.
5. Download the character ZIP or frame URLs from the managed character details.

## MCP vs REST Feature-Richness

For managed preset template animations, MCP and REST v2 expose essentially the same core capability:

| Requirement | MCP | REST v2 |
| --- | --- | --- |
| Create managed characters | Yes, simpler agent-facing schema. | Yes, fuller exact schemas across multiple endpoints. |
| Animate existing character with preset id | Yes, `animate_character`. | Yes, `POST /characters/animations` / `POST /animate-character`. |
| Select directions | Yes. | Yes. |
| Select mode `template` / `v3` / `pro` | Yes in current docs/tool metadata. | Yes in OpenAPI schema. |
| Exact schema introspection | Limited to MCP tool schema/docs visible in client. | Strong, via OpenAPI. |
| Managed polling/download helpers | Strong, through `get_character`. | Available via background jobs and character endpoints. |
| Raw skeleton keypoints | Not documented as a current MCP managed tool. | Yes, `POST /animate-with-skeleton` and `POST /estimate-skeleton`. |

Recommendation:

- For agents with visible PixelLab MCP tools, use MCP first for managed preset character animations because it is the intended managed-agent workflow and handles IDs, polling, and character resources naturally.
- Fall back to REST v2 when MCP is unavailable, when exact request schema control is needed, or when the task needs raw skeleton keypoints.
- Do not call undocumented website/editor operation routes from automation unless PixelLab publishes them in REST v2 or MCP docs later.

## Aseprite Extension Findings

The installed Aseprite extension contains both private editor workflows and useful local evidence about skeleton/template concepts.

Observed extension capabilities:

| Capability | Role |
| --- | --- |
| Template animation flow | Local editor workflow for applying a named skeleton/template motion to a reference frame. |
| Local template catalog | Editor-side catalog of classic/realistic body templates, display names, and frame counts. |
| New skeleton animation flow | Editor workflow for generating frames from authored or estimated skeleton keypoints. |
| Older pose animation flow | Editor workflow for template skeleton setup, animation-to-animation skeleton setup, and pose-guided generation. |
| Skeleton setup dialog | UI for template skeleton insertion, rescaling, export, and animation-to-animation tabs. |
| Skeleton export | Exports normalized pose/skeleton keypoint JSON for API use. |
| Pose editing | Estimates, stores, overlays, and edits skeleton keypoints inside Aseprite. |

### Aseprite Skeleton Feature Parity

The Aseprite extension exposes a richer interactive skeleton editor than MCP or public REST because it combines PixelLab calls with local Aseprite state. The important split is:

| Aseprite feature | What the extension does | Public MCP equivalent | Public REST v2 equivalent | Automation guidance |
| --- | --- | --- | --- | --- |
| Estimate skeleton | Sends one or more sprite frames through the editor's private estimation channel, receives normalized keypoints, maps them back onto the canvas, repairs duplicates, and writes them into local pose data. | None documented as a standalone MCP tool. | `POST /v2/estimate-skeleton` returns `keypoints` for an image. | Use REST for programmatic estimation. Use Aseprite only when the user wants interactive overlay/editing in the editor. |
| Edit skeleton | Toggles an Aseprite editing mode over a local pose layer, lets the user move keypoints, redraws the skeleton overlay, and persists points in cel/layer properties. | None. | No edit endpoint; editing is client-side manipulation of `Point[]`/keypoint JSON before another call. | Implement local JSON/keypoint editing in our tooling if needed; do not call extension internals. |
| Replace/insert template skeleton | Loads a local skeleton reference and inserts it into the current Aseprite frame. | Managed template animations exist via `animate_character`, but not raw local keypoint insertion. | No public catalog endpoint for these local Aseprite skeletons. `animate-with-skeleton` can consume keypoints once prepared. | Treat local references as editor assets/research, not public template ids. |
| Export skeleton for API | Exports selected/all frame keypoints as normalized JSON shaped as `{ "pose_keypoints": [[...], ...] }`. | None. | `animate-with-skeleton` expects nested keypoint arrays under `skeleton_keypoints`; `create-image-bitforge` accepts a single keypoint array. | Convert/exported `pose_keypoints` to REST `skeleton_keypoints` when building custom skeleton animation. |
| Template animation for an Aseprite character | Applies a local template animation catalog to a sprite/template name through a private editor generation route. | Managed `animate_character` exists, but it uses public managed character ids and `template_animation_id`, not Aseprite `template_name` values. | No public endpoint for Aseprite's local template-name catalog. Use managed character animation when the target is a PixelLab managed character, or export keypoints and use `animate-with-skeleton` for raw skeleton ownership. | Treat as a separate private Aseprite flow. Do not map its local `template_name` values to public `template_id` or MCP `body_type`. |
| Animate with skeleton (new) | Builds keypoint arrays per frame, derives depth from bundled 3D reference skeletons, builds inpainting/freeze masks, injects a reference image, then uses a private editor generation route. | None for raw skeleton keypoints. | `POST /v2/animate-with-skeleton` is the public route for reference image plus skeleton keypoints, init images, inpainting images, masks, view, direction, and guidance. | Use REST for equivalent generation; local Aseprite mask/depth prep is extra editor logic we may need to reproduce if exact behavior matters. |
| Re-pose (skeleton) | Uses a reference frame skeleton and a target frame skeleton with pose/reference/init/inpainting images, then uses a private editor generation route. | `create_character_state` can make a managed character state, but it is not raw keypoint reposing. | No direct public `re-pose` endpoint documented. Approximate with `animate-with-skeleton`, `edit-animation-v2`, image edit, or managed state depending on the requested output. | Treat exact Aseprite re-pose as editor-only unless PixelLab publishes a public route. |
| Pose-guided style generation | Sends pose keypoints with a style/image request. | None documented. | `create-image-bitforge` has `skeleton_keypoints` and `skeleton_guidance_scale`; some image/edit routes have init/reference controls. | Use public skeleton-guided image generation only where OpenAPI exposes keypoint fields. |
| Local skeleton preview/3D controls | Projects bundled 3D skeletons into 2D, supports direction/tilt controls, and previews overlays. | None. | None as a hosted endpoint. | Local/editor functionality only. |

Current public MCP does not expose `estimate_skeleton`, `animate_with_skeleton`, `edit_skeleton`, `export_skeleton`, or local skeleton-template insertion tools. It does expose managed character workflows that already store skeleton/template metadata internally: `create_character`, `animate_character`, `create_character_state`, `get_character`, and `delete_animation`.

Current public REST v2 exposes these skeleton-related primitives:

| REST route/schema | Public role |
| --- | --- |
| `POST /v2/estimate-skeleton` | Estimate keypoints from an image. OpenAPI response is `keypoints: Keypoint[]`. |
| `POST /v2/animate-with-skeleton` | Generate animation frames from `reference_image`, `image_size`, nested `skeleton_keypoints`, optional `init_images`, `inpainting_images`, `mask_images`, `color_image`, `view`, `direction`, and `guidance_scale`. |
| `POST /v2/create-image-bitforge` | Skeleton-guided single-image generation via `skeleton_keypoints` and `skeleton_guidance_scale`. |
| `GET /v2/characters/{character_id}` | Managed character details can include `skeletons`, but this is returned metadata, not an edit surface. |
| `POST /v2/characters/animations` / `POST /v2/animate-character` | Managed preset/template/custom/pro character animation. Uses `template_animation_id` for presets, not raw keypoints. |

The practical conclusion: Aseprite has a real interactive rigging/pose-authoring workflow. Public REST has the core estimation and generation primitives. MCP currently has the managed-character/template workflow, but not the raw rigging/editor primitives.

The installed extension exposes local skeleton reference families labeled `bipedal realistic`, `bipedal semi-chibi`, and `quadrupedal tiny`. It also exposes local walk references for those families. The local keypoint data uses labeled body points such as neck, face, shoulder, hip, and knee points. That supports the conclusion that PixelLab preset animation is skeleton/keypoint-guided under the hood. However, the extension's private editor channels are not stable public REST contracts.

## Proposed Auto-Rig Skeleton Pipeline

The useful product abstraction for Pip is an "auto-rig skeleton pipeline": accept a simple user intent, produce or use a reference sprite, estimate keypoints, save those keypoints as reusable API data, and then route to the public generation path that actually accepts skeleton data.

Recommended current implementation:

```text
source sprite/reference frame
  -> REST /estimate-skeleton
  -> normalize/save keypoints and metadata
  -> optional keypoint editing or sequence authoring
  -> REST /animate-with-skeleton for animation frames
  -> optional Aseprite import/export/tagging after generation
```

Current route choice:

| Step | Preferred surface now | Reason |
| --- | --- | --- |
| Create a prompt-only humanoid reference | MCP `create_character` or REST `create-character-v3` when a managed character is useful; REST image/character route when only a raw reference frame is needed | The skeleton estimator requires an image. Simple humanoid prompts need a reference frame before raw keypoint work can begin. |
| Auto-rig an existing sprite | REST `POST /v2/estimate-skeleton` | Public route that returns keypoints from an image. |
| Store/export the rig | Local sidecar JSON and optional Aseprite export/import | Editing/export is client-side data handling, not a hosted MCP/API edit endpoint. |
| Animate from skeleton data | REST `POST /v2/animate-with-skeleton` | Public route that accepts nested `skeleton_keypoints`. |
| Create a single skeleton-guided image | REST `POST /v2/create-image-bitforge` | Public route that accepts one keypoint array plus `skeleton_guidance_scale`. |
| Built-in walk/idle/jump on managed character | MCP `animate_character` or REST managed character animation | Prefer this when the user wants a managed preset, not raw keypoint ownership. |

MCP priority should be conditional:

- Use MCP first for managed character creation and managed preset animation.
- Use REST first for raw skeleton keypoints today, because current public MCP tools do not accept or estimate skeleton keypoint arrays.
- If a future MCP tool visibly exposes `estimate_skeleton`, `animate_with_skeleton`, or `skeleton_keypoints`, prefer it only for the matching raw-skeleton step and keep the same keypoint/export semantics.
- Inspect the visible MCP runtime schema before depending on mode-specific fields, cost confirmation fields, or the absence/presence of raw-skeleton tools.

Important limitation: `estimate-skeleton` auto-rigs one supplied pose. It does not automatically create a full walk/run skeleton sequence. To animate with skeleton data, the pipeline needs multiple keypoint frames or another authored motion source. For a single estimated pose plus a generic "walk" request, Pip should either route to managed template animation, ask for/generate additional skeleton poses, use an Aseprite-visible authoring/export workflow, or use REST custom text animation when skeleton ownership is not required.

Humanoid defaults:

- Map human/person/player/NPC/robot/humanoid monster/upright two-legged animal prompts to humanoid/mannequin.
- For down-facing RPG sprites, default the raw skeleton animation call to `view="low top-down"` and `direction="south"` rather than relying on REST defaults.
- For side-view sprites, use `view="side"` and the visible facing direction.
- Persist a sidecar manifest with body plan, source image, image size, view, direction, estimated keypoints, payload-ready skeleton keypoints, route used, and timestamp.

## Template Character Families

Public MCP docs expose these high-level managed character template families:

| Family | Use |
| --- | --- |
| `mannequin` | Humanoid/mannequin-style preset animation family. |
| `bear` | Quadruped animal family. |
| `cat` | Quadruped animal family. |
| `dog` | Quadruped animal family. |
| `horse` | Quadruped animal family. |
| `lion` | Quadruped animal family. |

The website Add Animation UI currently keys available animation lists by:

```text
mannequin
bear
cat
dog
horse
lion
```

The Aseprite extension also has older/classic and realistic local editor template labels across bipedal, quadrupedal, winged, floating, amorphous, and humanoid categories. Treat the website/MCP public families as the stable current managed-character route. Treat Aseprite-only labels as local editor/template evidence unless they appear in current REST/MCP docs for the surface being automated.

## Website Preset Animation IDs

The current website Add Animation bundle exposes the following template-specific animation ids.

### `dog`

| Category | Group | IDs |
| --- | --- | --- |
| Movement | Walking | `walk-4-frames`, `walk-6-frames`, `walk-8-frames`, `fast-walk` |
| Movement | Running | `running-4-frames`, `running-6-frames`, `running-8-frames` |
| Movement | none | `sneaking` |
| Idle | none | `idle` |
| Activities | none | `bark` |

### `cat`

| Category | Group | IDs |
| --- | --- | --- |
| Movement | Walking | `walk-4-frames`, `walk-6-frames`, `walk-8-frames` |
| Movement | Running | `running-4-frames`, `running-6-frames`, `running-8-frames`, `slow-run` |
| Movement | none | `jump` |
| Idle | none | `idle`, `seated-on-belly-idle` |
| Transitions | none | `sitting`, `sitting-on-belly`, `standing`, `standing-from-belly` |
| Activities | none | `drinking`, `eating`, `licking`, `yawning` |
| Emotions | none | `angry` |

### `bear`

| Category | Group | IDs |
| --- | --- | --- |
| Movement | Walking | `walk-4-frames`, `walk-6-frames`, `walk-8-frames` |
| Movement | Running | `running-4-frames`, `running-6-frames`, `running-8-frames` |
| Movement | none | `jump`, `stand-on-hind-legs` |
| Combat | none | `attack-left`, `attack-right`, `jump-attack` |
| Idle | none | `idle-long`, `idle-resting`, `idle-sitting` |
| Activities | none | `drinking`, `eating` |
| Sleeping | none | `going-to-sleep`, `waking-getting-up` |
| Transitions | none | `sitting-down`, `standing-up` |
| Emotions | none | `angry` |

### `horse`

| Category | Group | IDs |
| --- | --- | --- |
| Movement | Walking | `walk-4-frames`, `walk-6-frames`, `walk-8-frames`, `walk-turn-left`, `walk-turn-right` |
| Movement | Running | `running-4-frames`, `running-6-frames`, `running-8-frames`, `running-turn-left`, `running-turn-right`, `running-headbutt` |
| Movement | none | `swimming` |
| Combat | none | `attack`, `attack-back`, `hit-left`, `hit-right`, `dying` |
| Idle | none | `idle-shaking-head`, `rest-idle` |
| Eating | none | `eat-start`, `eating`, `eat-end` |
| Sleeping | none | `start-sleep`, `sleep-cycle`, `rest-cycle`, `wake-up` |
| Transitions | none | `lie-down`, `stand-up` |

### `lion`

| Category | Group | IDs |
| --- | --- | --- |
| Movement | Walking | `walk-4-frames`, `walk-6-frames`, `walk-8-frames` |
| Movement | Running | `running-4-frames`, `running-6-frames`, `running-8-frames` |
| Movement | none | `jump` |
| Combat | none | `attack`, `jump-attack` |
| Idle | none | `idle`, `idle-sitting` |
| Activities | none | `drinking`, `eating` |
| Transitions | none | `sitting`, `standing` |

### `mannequin`

| Category | Group | IDs |
| --- | --- | --- |
| Movement | Walking | `walk`, `walk-1`, `walk-2`, `walking`, `walking-2`, `walking-3`, `walking-4`, `walking-5`, `walking-6`, `walking-7`, `walking-8`, `walking-9`, `walking-10`, `walking-4-frames`, `walking-6-frames`, `walking-8-frames`, `crouched-walking`, `sad-walk`, `scary-walk` |
| Movement | Running | `running-4-frames`, `running-6-frames`, `running-8-frames`, `running-slide` |
| Movement | Idle | `breathing-idle`, `fight-stance-idle-8-frames` |
| Movement | Jumping | `jumping-1`, `jumping-2`, `running-jump`, `two-footed-jump` |
| Movement | none | `crouching`, `backflip`, `front-flip`, `getting-up` |
| Combat | Punching | `cross-punch`, `lead-jab`, `surprise-uppercut` |
| Combat | Kicking | `hurricane-kick`, `roundhouse-kick`, `high-kick`, `flying-kick`, `leg-sweep` |
| Combat | Reactions | `taking-punch`, `falling-back-death` |
| Combat | none | `fireball` |
| Interactions | none | `drinking`, `picking-up`, `pull-heavy-object`, `pushing`, `throw-object` |

Notes:

- The website also appends custom choices to every template list: `custom-v3` and `custom`.
- Quadruped walk ids use `walk-*`; mannequin walk ids include both older variants such as `walk-1` and explicit frame-count ids such as `walking-8-frames`.
- Use the exact id value, not the display label.

## Frame Count Semantics

Frame count behavior depends on route/mode:

| Route/mode | Frame count behavior |
| --- | --- |
| Managed `template` mode | Determined by `template_animation_id`; `frame_count` is not the control surface. |
| Managed `v3` mode | `frame_count` is even 4-16, default 8. |
| Managed `pro` mode | Custom/pro route; higher cost. Direction generation may use completed sides as reference. |
| `animate-with-text-v3` | Raw first-frame animation, even 4-16, default 8, pixel budget `width * height * frame_count <= 524288`. |
| `animate-with-text-v2` | Pro/raw route; frame count depends on size bands in docs/tool behavior. |
| `animate-with-skeleton` | Raw skeleton-keypoint route; OpenAPI example and descriptions emphasize skeleton keypoints rather than preset ids. |

The website preview logic accounts for `requested_frame_count`, `generation_model`, and odd/even reductions for v3 outputs. Do not infer template frame count by post-processing the returned frame array into a different length.

## Raw Skeleton API

Public REST v2 exposes:

```text
POST /v2/estimate-skeleton
POST /v2/animate-with-skeleton
```

`estimate-skeleton` takes a character image and returns keypoints. `animate-with-skeleton` accepts:

| Field | Role |
| --- | --- |
| `image_size` | Required output size. |
| `reference_image` | Required reference image. |
| `skeleton_keypoints` | Array of keypoint arrays. |
| `view` | Camera view. |
| `direction` | Subject direction. |
| `guidance_scale` | How closely to follow the reference and skeleton. |
| `init_images` | Optional initial images. |
| `inpainting_images` | Optional skeleton-connected inpainting/reference frames. |
| `mask_images` | Optional masks. |
| `color_image`, `seed` | Palette/seed controls. |

OpenAPI currently defaults raw `animate-with-skeleton` to `view="side"` and `direction="east"`. Website managed-character examples may use different values, such as low top-down/south, depending on the character and UI flow. Do not infer raw skeleton API defaults from website managed-character examples.

The endpoint prose lists supported sizes `16`, `32`, `64`, `128`, and `256`, while the schema allows integer width/height from 16 to 256. Verify current OpenAPI/schema behavior before writing exact production code for nonstandard dimensions.

This is the right public route for custom skeleton keypoints. It is not the same as selecting a managed preset animation id on a character. Future custom skeleton support should build on this route, plus explicit keypoint validation/export/import rules.

Current skill support should cover both managed preset animations and raw skeleton pipeline requests while keeping them separate:

```text
Managed preset: managed character id + template_animation_id + directions
Raw skeleton: reference image + estimated/exported skeleton_keypoints + view/direction
```

## Aseprite Workflow Boundary

Aseprite should be treated as a local editor/workspace surface after PixelLab generation, not as the primary automation contract for preset template animation.

The Aseprite extension includes local skeleton reference folders and a private template-animation catalog for editor workflows. These names are useful research evidence for pose/keypoint concepts, but they are not documented managed-character `template_animation_id` values and they do not cover every managed website preset id. Keep them separate from the public preset animation ID list unless PixelLab publishes them in REST v2 or MCP docs.

Recommended Aseprite workflow:

1. Use MCP or REST v2 to animate the managed character with `template_animation_id`.
2. Download the generated frames or character ZIP.
3. Use Aseprite CLI/Lua to create or update an `.aseprite` file, add frames, create a `walk` tag, and export spritesheets/GIFs.

Avoid:

- Calling private extension operation channels directly.
- Reusing extension secrets or browser session tokens.
- Driving the extension UI invisibly to spend credits.
- Treating local extension template JSONs as public API-stable contracts.

## Practical Routing Guidance

Use this decision tree:

```text
User wants built-in/preset walk/idle/jump/bark/etc. for an existing managed character
  -> Prefer MCP animate_character with template_animation_id.
  -> Fall back to REST v2 /characters/animations with mode="template".

User wants a new managed character and preset animations
  -> Prefer MCP create_character, then MCP animate_character.
  -> Fall back to REST v2 create-character-* then /characters/animations.

User wants exact skeleton keypoints, exported pose JSON, or custom skeletons
  -> REST v2 estimate-skeleton / animate-with-skeleton.
  -> Aseprite can export or organize keypoints, but do not automate private extension calls.

User wants "auto-rig this humanoid" from an image
  -> REST v2 estimate-skeleton.
  -> Save sidecar keypoint JSON and payload-ready skeleton_keypoints.
  -> Animate with REST animate-with-skeleton only when a keypoint sequence exists.

User wants "auto-rig this humanoid" from only a prompt
  -> Create or request a base reference frame first.
  -> Then estimate/export keypoints from that generated/reference frame.

User wants only to import/export/edit frames in Aseprite
  -> Generate with MCP/REST first, then use Aseprite CLI/Lua for workspace operations.
```

## Open Questions And Risks

1. Public docs do not expose a dedicated template catalog endpoint. The website bundle currently exposes the option lists, and MCP docs summarize template families, but official stability for every website option id should be treated as medium confidence.
2. `/v2/animate-character` prose contains an older frame-count note, while the current schema and `/v2/characters/animations` description say v3 custom mode supports even 4-16 frames. Prefer schema over stale prose.
3. The website first-party animation flow has richer internal fields such as calibration images and frozen first-frame anchors, but it is not a public automation contract.
4. Aseprite extension local skeleton references strongly imply skeleton-guided presets, but those files can be updated by the extension updater and are not public API guarantees.
5. `bone_scaling` appears in website character objects and UI constraints, but current public managed animation schema does not expose it as a direct animation-generation control. It should be treated as character metadata unless current docs later expose a stable field.
6. A single estimated skeleton pose is not a motion template. Pipeline UX must distinguish "rig this pose" from "author a skeleton animation sequence."

## Implementation Recommendations For `pixellab-pip`

1. Add a dedicated agent-facing reference for preset skeleton/template animation.
2. Trigger that reference on terms such as `skeleton`, `preset animation`, `template animation`, `built-in animation`, `walk template`, `idle template`, `bark`, and explicit template ids like `walk-8-frames`.
3. Prefer MCP for managed preset animations when MCP tools are visible.
4. Fall back to REST v2 only when MCP is unavailable, exact schema control is needed, or the user explicitly asks for API/code.
5. Add a streamlined auto-rig path for existing images: REST `estimate-skeleton`, sidecar manifest, optional keypoint editing/export, then REST `animate-with-skeleton` when a keypoint sequence exists.
6. Keep raw skeleton keypoint support separate from preset template animation. For now, route custom skeleton work to explanation/planning or REST `animate-with-skeleton`, not to hidden Aseprite/website internals.
7. Preserve template frame counts and returned frame order. Do not locally stretch, duplicate, trim, ping-pong, or reorder generated template frames unless the user explicitly asks for an alternate playback package.
