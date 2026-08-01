# PixelLab S-XL / Pixen Full-Body Character Prompt Research Spike

Last reviewed: 2026-08-01.

Purpose: find the smallest description that reliably makes `Create image S-XL (new)` / Pixen produce a 64px, south/front-facing, low top-down, full-body idle character when the request leaves all other settings at their defaults. This is an observed prompt spike, not a guarantee about future model versions or every subject.

## Route and controlled request

The user-facing Aseprite label maps to Pixen: public REST `POST /v2/create-image-pixen`, MCP `create_image_pixen` followed by `get_image`, and an Aseprite/editor wrapper using Pixen terminology. The live sweep used MCP as requested.

Every accepted call used only this request shape:

```json
{
  "description": "<prompt>",
  "width": 64,
  "height": 64,
  "view": "low top-down",
  "direction": "south"
}
```

No `detail`, `outline`, `no_background`, `seed`, or `enhance_prompt` fields were sent. The MCP responses reported a non-transparent/default background. Public REST uses the documented `image_size` object instead of MCP's separate `width` and `height` arguments; the semantic settings are the same, not the literal JSON shape.

PixelLab's current camera documentation defines low top-down as approximately 20 degrees and south as facing the camera. It also warns that view and direction are weak controls. The requested “30 degree” wording was tested separately, but it is not the documented meaning of the low-top-down selector:

- [PixelLab camera options](https://www.pixellab.ai/docs/options/camera)
- [PixelLab API](https://www.pixellab.ai/pixellab-api)
- [PixelLab v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)

## Subject text constraint

The first sweep kept the user's exact character sentence first, including its final period:

```text
male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

The initial composition wording was appended after that sentence. The later follow-up deliberately tested the opposite order because the user requested the composition clause at the start; that comparison keeps the same exact subject sentence after the composition clause. The requested order takes precedence for each run.

## Incremental prompt plan

The sweep started at the bare subject and added one composition idea at a time. The full prompt for each row is the exact prefix above followed by the suffix.

| ID | Suffix tested | Purpose |
|---|---|---|
| B0 | *(none)* | Baseline subject-only prompt. |
| B1 | `full-body idle game character sprite.` | Add body coverage and neutral pose. |
| B2 | `full-body south-facing idle game character sprite.` | Add direction wording. |
| B3 | `full-body south-facing idle character sprite, low top-down view.` | Add camera wording. |
| B4 | `small centered full-body south-facing idle in-game character sprite, low top-down view.` | Add game-sprite framing and distance. |
| B5 | `full body visible with empty space around it, small centered south-facing idle game sprite, low top-down view.` | Test prior empty-space evidence. |
| R2 | `full-body south-facing idle game character sprite.` ×3 | Repeat the short direction candidate. |
| R4 | `small centered full-body front-facing south-facing idle in-game character sprite, low top-down view.` ×3 | Add explicit front-facing wording and repeat. |
| R5 | `one small centered full-body front-facing south-facing idle in-game character sprite with face and front of body visible, low top-down view.` ×3 | Stronger front-visibility fallback. |
| R6 | `one small centered full-body front-facing south-facing idle in-game character sprite, entire figure visible from head to feet, low top-down camera, no cropping.` ×3 | Stronger bounds/crop fallback. |
| R7 | `small centered full-body front-facing idle in-game character sprite, low top-down view.` ×3 | Remove `south-facing`. |
| R8 | `small centered full-body front-facing south-facing idle in-game character sprite, low top-down camera at approximately 30 degrees.` ×3 | Probe the requested 30-degree wording. |
| S1 | `full-body front-facing south-facing idle game character sprite, low top-down view.` ×3 | Remove `small` and `centered`. |
| S2 | `small centered full-body front-facing south-facing idle character sprite, low top-down view.` ×3 | Remove `in-game`. |
| T1 | `centered full-body front-facing south-facing idle in-game character sprite, low top-down view.` ×3 | Remove `small`. |
| T2 | `centered full-body front-facing south-facing idle game character sprite, low top-down view.` ×3 | Remove `small` and use shorter `game`. |
| T3 | `small full-body front-facing south-facing idle game character sprite, low top-down view.` ×3 | Replace `centered` with `small`. |

## Results

The first baseline was a cropped bust. The short south-only repeat was not stable: one of three outputs turned the character away. Removing the complete framing cue (`small` and `centered`) or removing `in-game` from the small-centered form caused rear-facing drift in the minimization checks. Keeping `small` allowed `centered` to be removed in the final T3 candidate. The useful threshold was explicit front-facing wording plus a small-character framing cue.

The earlier three-repeat score was too permissive. After the user's visual review, the only accepted original outputs in that sweep were `r5-visible-front-3.png` and `r4-centered-front-2.png`:

```text
male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back. one small centered full-body front-facing south-facing idle in-game character sprite with face and front of body visible, low top-down view.
```

The shorter accepted prompt was:

```text
male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back. small centered full-body front-facing south-facing idle in-game character sprite, low top-down view.
```

The other outputs should be treated as rejected for this task because they read as isometric, portrait-like, rear-facing, or action-like under the user's stricter visual review. The R8 30-degree wording did not solve that problem and is not used in the recommendation because the product's documented low-top-down selector is approximately 20 degrees, not an exact 30-degree mode.

The prompt is still a probabilistic improvement, not a formal guarantee. PixelLab's own documentation describes the camera and direction controls as weak, so every generated result needs a visual check.

## Follow-up: composition-first without `small`

The first controlled comparison moved the composition clause to the beginning of every description, removed `small`, and kept the same exact subject sentence afterward. It used five seedless MCP attempts per variant with the same 64×64, low-top-down, south request and no optional fields:

```text
full-body front-facing south-facing idle game character sprite, low top-down view. male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

and:

```text
full-body front-facing south-facing idle game character, low top-down view. male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

| Variant | Full body | Front/south readable | Neutral idle | Result |
|---|---:|---:|---:|---|
| No `small`, with `sprite` | Not promoted | Not promoted | Not promoted | The user's visual review rejected these outputs as isometric or portrait-like. |
| No `small`, no `sprite` | Not promoted | Not promoted | Not promoted | The user's visual review rejected these outputs as isometric or portrait-like. |

Conclusion: these short prompts did not work reliably. This was a useful negative result, but it did not prove that `small` is required; the missing piece was explicit framing and neutral-pose language.

```text
male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back. small centered full-body front-facing south-facing idle in-game character sprite, low top-down view.
```

This keeps the subject-first order used by the two accepted outputs. The longer composition-first wording was tested separately below.

## Final no-`small` MVP search

The next passes kept the user's required 64×64, `low top-down`, and `south` settings, omitted `no_background`, and tested several ways to replace the rejected `small` framing cue:

- `character only` was tested, but scenes still appeared often enough that it is not a reliable background-control instruction.
- `at approximately 20 degrees`, `not high top-down or isometric`, and `fills most of the frame` were tested as camera/framing cues. They improved individual images but were not as stable as the final wording.
- Subject-first variants with `fills most of the frame`, `narrow margins`, and `feet fully visible` produced a promising five-image run, but the composition-first version below was simpler and retained a consistent five-image result.

The current MVP is:

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet. male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

The final three-attempt MCP rerun with this exact description was visually checked. All three were full-body, readable front/south-facing, and neutral/idle. The images and job manifest are in `pixellab-pip-generations/s-xl-prompt-spike-20260731/final-no-background-64x64/`.

The practical pattern is: put the spatial contract first; say `sprite` to keep the game-asset interpretation; replace `small` with explicit full-body wording; use neutral-pose words to stabilize idle; and use `no_background: true` only when the final asset must be transparent.

### Exact `sprite` ablation

To isolate the word itself, a second five-attempt MCP run used the final MVP unchanged except for removing `sprite`:

```text
full-body front-facing south-facing idle game character, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet, narrow margins. male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

The same 64×64, low-top-down, south request was used, with `no_background` omitted. Attempts 1, 3, 4, and 5 were full-body, front-readable, and neutral; attempt 2 drifted toward a 3/4 view. Therefore `sprite` is not strictly necessary when the full framing contract is present, but it improved this small consistency sample from 4/5 to 5/5 and remains in the MVP. This is stronger evidence than the earlier short no-`sprite` batch, where only `without-sprite-4.png` was a near-pass and its camera was too high.

## Evidence from prior generations

The existing `pixellab-pip-generations/` corpus supported the following hypotheses before the live sweep:

- The 64×64 v4 rescue sweep found that explicit full-body language and margin/framing cues outperformed portrait-like wording. Its strongest prior compact candidate used `full body visible`, `small`, `centered`, and `idle` wording.
- The `create_character` run produced a consistent compact south-facing character sheet with the same subject concept, showing that the managed character route is structurally stronger than raw Pixen for repeated character identity/direction. This does not make it the same route as Create image S-XL (new).
- The live B5 empty-space probe returned a rear-facing character, likely because showing a katana attached to the back is compatible with showing the character's back. Empty-space wording is therefore not part of the MVP.

The retained live outputs and job manifest are under `pixellab-pip-generations/s-xl-prompt-spike-20260731/`. The follow-up comparisons are under its `no-small-prefix-sweep/`, `no-small-o2-mvp/`, `no-small-mvp-candidate/`, and `composition-first-mvp/` subfolders. They are ignored generation artifacts; no user or machine-specific paths are recorded here.

## API and Aseprite parity

Use the same exact description and the same semantic selectors in both surfaces:

- MCP: `description`, `width: 64`, `height: 64`, `view: "low top-down"`, `direction: "south"`.
- Public REST: the Pixen endpoint with the same description, `image_size: {"width": 64, "height": 64}`, `view`, and `direction`, omitting optional fields when defaults are requested.
- Aseprite: enter the exact description, select 64px, low top-down, and south, and leave the other controls at their defaults.

This makes the requested configuration semantically equivalent. It cannot make the pixels identical: Pixen generation is stochastic, the public REST and MCP argument schemas differ, and the Aseprite extension's internal request implementation is not a public contract. For deterministic production identity across frames, the managed `create_character` workflow or a reference-image workflow is a better follow-up than adding more camera adjectives to raw Pixen.

## Recommendation

Use the no-`small` MVP when canvas occupancy matters:

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet. male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

It is longer than the accepted `r4`/`r5` prompts because it replaces their implicit framing cue (`small`) with explicit full-body and pose anchors. If subject-first order is required, use the previously accepted `r5` prompt, accepting its smaller framing.

For a backgroundless result, add `no_background: true` to the request. Omitting it produced `transparent: False` in the MCP responses; prompt text such as `character only` did not reliably replace that flag.

### Route-selection caveat from the comparison work

This spike establishes the best prompt found for raw Pixen; it does not make Pixen the best model for every character request. In the focused comparison, Create Image Pro (`create_image_pro`/`generate-image-v2`) was the better observed route for a single static south-facing character candidate. Pro costs substantially more and produces a different, broader character style, so it should be selected only when orientation is more important than Pixen's cheaper, tighter style. Use managed Character Creator v3 when the deliverable needs persistent identity, eight directions, states, or animation.

Verify the full body first, then front/south orientation, then idle pose and low top-down framing. Do not judge hair, clothing, katana, color, or detail until the composition passes.

## Final controlled rerun: remove `narrow margins` and enable `no_background`

The user questioned whether `narrow margins` was necessary. It was added only as a canvas-occupancy cue; it was never intended to control direction, camera angle, or pose. A final three-attempt MCP rerun removed it and enabled the requested API flag:

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet. male with spiky red hair, brown eyes. wearing black kimono with only one katana attached to his back.
```

All three calls used the same settings and no other optional fields:

```json
{
  "width": 64,
  "height": 64,
  "view": "low top-down",
  "direction": "south",
  "no_background": true
}
```

| Attempt | MCP result | Visual finding |
|---|---|---|
| 1 | `64x64`, `transparent: True` | Full-body, neutral idle, and clearly front/south-readable. |
| 2 | `64x64`, `transparent: True` | Full-body, neutral idle, and front-readable, with more visual variation. |
| 3 | `64x64`, `transparent: True` | Full-body, neutral idle, and clearly front/south-readable. |

The three outputs contained no scene or floor background. `no_background: true` was therefore consistently effective in this small sample; prompt-only cues such as `character only` were not needed for this result. The low-top-down angle remained subtle, and the three images still varied in proportions and detail, so this is evidence that the shorter prompt can work—not a guarantee of deterministic direction.

Finding: `narrow margins` is not necessary to preserve full-body output and should be omitted from the MVP; it is not a direction or camera fix.

The saved images, comparison sheet, manifest, and replay blueprint are in the [final no-background 64x64 run](../../pixellab-pip-generations/s-xl-prompt-spike-20260731/final-no-background-64x64/comparison-spritesheet.png), with the [manifest](../../pixellab-pip-generations/s-xl-prompt-spike-20260731/final-no-background-64x64/final-no-background-64x64.manifest.json) and [blueprint](../../pixellab-pip-generations/s-xl-prompt-spike-20260731/final-no-background-64x64/final-no-background-64x64.blueprint.json).

## Investigation: Character Creator v3, humanoid conditioning, and Aseprite

The owner conversation supplied an important hypothesis: Character Creator v3 may use an internal humanoid switch or stronger system conditioning that is not present in Create Image S-XL (New). The owner described that behavior as a boolean that is unavailable to the caller. That is useful product-context evidence, but it is not itself a public API contract.

The local Aseprite extension and the current public v2 schema were audited to test the hypothesis.

### What the Aseprite extension proves

The Pixen route is `generate-pixen.lua` and sends to `generate-image-pixen`. Its default/request model contains `view`, `direction`, `no_background`, `outline`, and `detail`; it contains no `humanoid`, `body_type`, `template_id`, `system_prompt`, or equivalent character-mode field. The request builder serializes the model state, and the WebSocket transport sends the serialized JSON. Retained Pixen request-history entries independently show `view: "low top-down"`, `direction: "south"`, and `no_background: true` in the outbound payload.

The extension does contain other humanoid-related strings, but they belong to different workflows:

- `female-humanoid` and other humanoid names are template identifiers for template/rotation/animation tools.
- `character_type` belongs to the older complete-character/skeleton workflow.
- `humanoid_skeleton` is an internal pose/skeleton data structure.

None of those is attached to the Pixen `generate-image-pixen` request. Therefore the Aseprite settings are not a client-side no-op; the remaining failure is model/backend adherence or a route-level difference.

### What the public Character Creator contract proves

The current v2 API describes `create-character-v3` as a two-stage workflow: when no reference image is supplied, Pixen creates a south-facing sprite from the description, then v3 rotates it into eight directions. The request has `template_id` (default `mannequin` for bipedal subjects), `view`, `no_background`, and style fields, but no `humanoid` boolean, `direction`, or `system_prompt` field. The schema is closed with `additionalProperties: false`.

The public contracts therefore look like this:

| Route | Character conditioning | South/front control | Background default |
|---|---|---|---|
| `create_image_pixen` / Aseprite Pixen | No exposed humanoid mode | `view` and `direction`, documented as weak guidance | `no_background` defaults to `false` in public v2 |
| `create_character_v3` | Character route; `template_id: mannequin` for bipedal/humanoid subjects | South is the seed direction; v3 creates the other rotations | `no_background` defaults to `true` |

Sources: [PixelLab v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json), [Character Creator API docs](https://api.pixellab.ai/v2/docs), and [camera options](https://www.pixellab.ai/docs/options/camera).

The public prompt-enhancement contracts reinforce the route distinction: Pixen enhancement is documented to respect view, direction, and background settings; Character v3 enhancement is documented not to mention facing direction or background because v3 handles those structurally.

### Investigation conclusion

The humanoid hypothesis is directionally credible but the missing behavior is not recoverable by adding the word `humanoid` to a Pixen description. No authorized source exposed a hidden system prompt, and neither the installed extension nor the public schemas expose a switch that would activate one. The most defensible explanation is that Character Creator v3 has route-level character conditioning—possibly selected by its UI body-type state and `mannequin` template—while standalone Pixen remains a general image model with weak camera controls.

This changes the recommended engineering direction:

1. Keep the Pixen MVP prompt for standalone one-image generation, but treat south/front consistency as probabilistic and visually validate it.
2. For a game character that must be consistently humanoid and south-facing, use `create_character_v3`/Character Creator and take its south rotation, or provide a south-facing reference image. This is a different workflow, not a hidden Pixen option.
3. To make Aseprite and API behavior match Character Creator, Aseprite would need an explicit Character Creator v3 route or an authorized backend contract exposing that route. Injecting an undocumented `humanoid` or `system_prompt` key into Pixen would be unsupported and should not be implemented.

### Aseprite extension feasibility

Extending the extension is technically feasible, but it should be a separate Character Creator v3 integration rather than a new checkbox on `generate-pixen.lua`.

The current Character Creator page bundle shows a `humanoid` UI state and a `pixen_v3` generation mode. It passes a `templateId`, view, image size, outline, and detail into its character-generation hook. The same bundle also constructs a WebSocket URL from `api.pixellab.ai` for older template-rotation flows. This proves a shared host and overlapping transport infrastructure, not identical request contracts: the website's v3 path and the extension's Pixen path still use different payloads and output workflows.

The extension already has two nearby but non-equivalent routes:

- `generate-8-rotations.lua` sends a template reference such as `female-humanoid` to the legacy `generate-8-rotations` WebSocket route.
- `generate-8-rotations-v3.lua` requires an existing reference image and sends it to `animate-with-text-v3`; it is not the website's from-scratch Character Creator v3 flow.

A correct Aseprite implementation would therefore need to:

1. Add a new Character Creator v3 model and UI field that maps `Humanoid` to `template_id: "mannequin"` (or the exact authorized equivalent), rather than sending `humanoid: true` to Pixen.
2. Use the supported Character Creator v3 API/adapter (`create_character` with `mode="v3"`, or the documented `POST /v2/create-character-v3`) instead of depending on undocumented legacy WebSocket routes.
3. Handle the asynchronous character result and its eight directional outputs, then import the south rotation into the requested Aseprite frame or expose the full sheet.
4. Preserve the v3 defaults that matter: low top-down view, transparent background, and a south-facing seed.

This is a moderate feature, not a prompt tweak. The installed extension currently centralizes generation around WebSocket requests and does not contain a general REST client, so the transport/job polling and eight-frame import are the main implementation work. The public v2 schema documents the v3 route and its output/job contract; it does not expose the website's internal system prompt. ([PixelLab v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json), [API docs](https://api.pixellab.ai/v2/docs))

## Limits

- The subject-first test used three seedless repeats per candidate; the short composition-first comparison used five per variant; and the final MVP used five fresh repeats. None is an exhaustive statistical guarantee.
- No seed was supplied, so reruns can differ. The current user requirement also explicitly asked to leave seed/default options alone.
- Aseprite GUI output was not driven in this spike; its exact internal payload remains editor-only. The parity conclusion is a semantic contract, not a pixel-for-pixel comparison.
- At 64px, tiny details such as brown eyes may not be visually resolvable even when the description contains them.
