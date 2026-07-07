# PixelLab Paperdolling Research Spike

Generated: 2026-07-04.

Scope: research a complete paperdolling system layered on top of PixelLab for RPG-style equipment, especially weapons that animate with a character and can be layered in a game engine. This is human/developer-facing research, not the canonical agent contract. Durable routing rules should be promoted into `skills/pixellab-pip/references/paperdolling.md` only after the wrapper design is implemented or proven.

## Executive Summary

PixelLab can generate the base character, animate the character, edit a character image, inpaint selected regions, edit short animation frame sets, transfer outfits to animation frames, estimate skeleton keypoints, and animate from skeleton keypoints. Current public REST/MCP surfaces do not expose semantic paperdoll layers, editor-native layer objects, isolated changed-part outputs, or a first-class "equipment layer" endpoint.

That makes paperdolling a wrapper system rather than a single PixelLab call:

```text
base character frames
  -> PixelLab same-canvas equipment composite
  -> local layer extraction and QA
  -> manifest + transparent equipment layer frames
  -> composited previews + engine import package
```

The most promising near-term route is a Python-assisted "client-extracted layer" workflow. PixelLab creates a same-canvas composite by adding a weapon, armor, clothing, hair, or accessory to the base character. The wrapper then compares the composite against the unchanged base frame(s), extracts changed pixels into transparent layer images, verifies that the base body did not drift, and produces a package with previews, manifests, and failure diagnostics.

The common two-PixelLab-call workflow of "add equipment, then ask AI to remove the character" can work as a manual fallback, but it spends an extra Pro edit, introduces another generative failure point, and can hallucinate missing or occluded equipment pixels. The wrapper should prefer one edit plus local extraction when QA passes; fall back to a second edit, a mask/inpaint route, or editor cleanup only when extraction fails.

Skeletons are useful, but not a silver bullet. PixelLab `estimate-skeleton` returns keypoints, and `animate-with-skeleton` can generate frames from a keypoint sequence. Neither returns equipment-only layers. For paperdolling, skeleton data is best treated as anchoring metadata, hardpoint validation, and future authoring support, not as the primary layer extraction mechanism.

## Spike Questions

| Question | Finding | Verdict |
|---|---|---|
| Can PixelLab public APIs create native reusable equipment layers? | No public REST/MCP field currently returns semantic layers or isolated changed pixels. Editor surfaces can have layer-oriented output methods, but those are not REST/MCP contracts. | Not available as a native API feature |
| Can a wrapper reduce the two-edit workflow to one edit? | Yes, for same-canvas opaque or mostly opaque equipment when the base pixels are preserved enough for alpha-aware differencing. | Promising |
| Can this scale to animated weapons? | Yes, if every base/composite frame shares the same canvas, frame order, pivot, and direction, and if temporal QA rejects jitter/drift. | Promising but high risk |
| Can skeleton data anchor equipment to hand bones? | Partially. Skeleton/keypoint data can define hardpoints and validate expected regions, but PixelLab does not expose a deterministic weapon attachment renderer. | Useful metadata, not complete solution |
| Should this become a standalone app later? | Likely, if visual QA, masks, layer ordering, and manual correction become central to the workflow. A Python prototype can de-risk the deterministic parts first. | Future direction |

## Current PixelLab Capability Boundary

| Capability | Public surface | Output | Paperdoll implication |
|---|---|---|---|
| Managed base character | MCP `create_character`; REST `create-character-v3`, `create-character-with-4-directions`, `create-character-with-8-directions`, `create-character-pro` | Managed character rotations and downloadable assets | Good source for standardized base frames. |
| Managed dressed state | MCP `create_character_state`; REST `create-character-state` | New managed character variant across rotations | Useful for dressed previews, not reusable isolated layers. |
| Managed character animation | MCP `animate_character`; REST `characters/animations` / `animate-character` | Managed animation frames by direction | Good for base animation; template output may still introduce style drift. |
| Single image edit | REST `edit-image` | One edited composite image | Best low-complexity base for single-frame layer extraction. |
| Pro/multi image edit | REST `edit-images-v2` | One or more edited composite images | Useful for small batches or consistent edits, still composite-only. |
| Inpaint | REST `inpaint` / `inpaint-v3`; website/editor Inpaint | Edited/inpainted composite image | Better when a mask can restrict the weapon/body region. |
| Edit animation | REST `edit-animation-v2` | Edited/composited frames | Useful for adding equipment to 2-16 frames, then extracting per-frame layers. |
| Transfer outfit | REST `transfer-outfit-v2` | Outfit-transferred/composited frames | Good for clothing/armor reskins, but not equipment layers. |
| Estimate skeleton | REST `estimate-skeleton` | Keypoints with labels and z-index-like data | Useful to infer hardpoints and body regions. |
| Animate with skeleton | REST `animate-with-skeleton` | Generated animation frames | Useful for raw skeleton generation, not layer isolation. |
| Aseprite extension changes-only layer | Visible editor/private extension workflow | Editor layer when verified | Useful manual/editor workflow and design reference, not a public REST/MCP contract. |

Important official-doc nuance:

- `edit-image`, `edit-images-v2`, `inpaint-v3`, `edit-animation-v2`, and `transfer-outfit-v2` are documented as returning edited images or frames, not native layer files.
- MCP docs currently list managed character/state/animation tools, object/tile/UI helpers, and related utilities, but not generic image-edit or inpaint equivalents.
- `animate-with-skeleton` defaults are side/east in the public schema; RPG paperdoll workflows should set `view` and `direction` explicitly.

## Aseprite Changes-Only Layer Findings

PixelLab's Aseprite extension is the closest existing product behavior to the desired paperdoll workflow. The public docs describe an output method named `New layer with changes`, and the installed extension exposes the same option alongside `New layer`, `Modify current layer, only changes`, `Modify current layer`, and `New frame`.

The important finding is that the extension does not look like a simple local image-diff script. As inspected in the locally installed extension on 2026-07-04:

- The editor dialog exposes `output_method` as a user-selectable field.
- The edit-image flow keeps `output_method` in request state, captures the edit image from the current sprite/frame/selection, encodes it as RGBA bytes, and sends the request to an extension/private operation path.
- The request builder copies request data and encodes images; it does not appear to strip `output_method`.
- The generation-preparation path treats both `New layer with changes` and `New layer` as requests to target a dedicated PixelLab generation layer instead of only a new frame.
- The placement path creates or replaces Aseprite cels from returned image bytes. It handles selection placement and full-canvas placement, but no local per-pixel subtraction of base-vs-result was found there.
- The websocket/result path receives returned image bytes and places them into cels. It special-cases discard behavior for `New layer with changes`, but no local changes-only extraction was found in the placement path.

That suggests a split responsibility:

```text
Aseprite UI/Lua
  captures source image and output_method
  prepares target frame/layer/cel
  sends request to extension/private backend
  places returned image bytes into a dedicated PixelLab generation layer

PixelLab extension/private backend
  likely interprets output_method
  likely decides whether result bytes are full output or changes-only output
```

This is an inference from the installed Lua code plus the public option docs, not an official public API guarantee. The public REST v2 OpenAPI schemas inspected for `edit-image`, `edit-images-v2`, `edit-animation-v2`, and `inpaint-v3` do not expose `output_method`. The portable wrapper should therefore not send `output_method` to public REST and should not call the Aseprite extension's private operation URLs.

### Can This Work Outside Aseprite?

Yes, but not by directly asking public REST for `New layer with changes`.

The portable equivalent is:

```text
base PNG(s)
  -> public PixelLab edit/inpaint/edit-animation route
  -> returned composite PNG(s)
  -> local Aseprite-parity changes-only extractor
  -> transparent equipment layer PNG(s)
  -> optional .aseprite workspace assembly
```

Aseprite itself can still be useful outside the visible extension workflow. Its documented Lua API can open/save sprites, create layers/cels, draw images, clear image regions, iterate pixels, and package the result into an `.aseprite` workspace. That means a future tool can create an Aseprite verification file with:

- locked or clearly named base layer,
- PixelLab composite layer,
- extracted `weapon_front` / `weapon_back` candidate layers,
- mask/diff heatmap QA layers,
- frame tags matching the manifest.

That workspace assembly should use Aseprite's documented CLI/Lua API, not the PixelLab extension internals.

### Aseprite-Inspired Routes

| Route | How it works | Public/portable? | Paperdoll role |
|---|---|---:|---|
| Aseprite extension `New layer with changes` | Artist runs PixelLab in Aseprite; extension/private backend returns pixels that the extension places in a dedicated generation layer. | No, visible/editor workflow only | Best manual/editor reference behavior. |
| Public REST plus local extraction | Agent calls documented PixelLab edit route, then Python compares base and composite and copies changed pixels into a transparent PNG. | Yes | Default portable paperdoll route. |
| Public REST plus Aseprite CLI assembly | Same as local extraction, then a Lua script builds a layered `.aseprite` file for artist QA. | Yes, if using documented Aseprite APIs | Good bridge between agent automation and artist editing. |
| Extension-private operation replay | Send `output_method` to the extension operation URL outside Aseprite. | No | Do not build the skill or wrapper around this. |
| `Modify current layer, only changes` | Extension writes changes into the selected layer. | Editor-only and destructive | Avoid as an automated default; useful only when an artist intentionally works in-place. |

### Implementation Consequences

The system plan should use the Aseprite extension as a behavioral benchmark, not a dependency:

- Recreate the output artifact, not the private protocol.
- Treat exact pixel equality as a fast path, then use tolerant alpha-aware extraction for small PixelLab redraw artifacts.
- Add drift detection before extraction so body redraws do not turn into false equipment pixels.
- Export a transparent layer PNG and a visual preview first; add `.aseprite` workspace assembly as an optional packaging step.
- Once the extractor is proven, promote only the durable route into `skills/pixellab-pip/references/paperdolling.md`: "Aseprite-parity client-extracted layer" from public composites.

## Traditional Paperdolling Patterns

Classic sprite paperdolling is a deterministic asset alignment problem.

The robust pattern is:

```text
one base animation contract
  same canvas/cell size
  same frame count
  same frame order
  same origin/pivot
  same direction names/order
  one or more transparent equipment layers
  manifest that defines slots, draw order, hardpoints, and compatibility
```

Useful design lessons:

- Frame-aligned equipment sheets are the baseline for pixel-art RPGs. Each item layer must match the character's animation grid exactly.
- Layer order is not just "equipment over body." Real systems need slots such as `weapon_back`, `shield_back`, `body`, `clothes`, `arms`, `weapon_front`, `shield_front`, `hair_front`, `hat`, and `vfx`.
- Top-down characters need front/back or direction-specific occlusion. A sword may be behind the torso in one frame and in front of the hand in another.
- Held weapons benefit from per-frame hardpoints: `hand_r`, `hand_l`, `weapon_tip`, `muzzle`, `shield_center`, plus optional angle and scale.
- Runtime systems should drive all layers from one animation clock. Independent sprite timers drift.
- Engine sorting must treat the whole character as one world object, while child layer order handles the body/equipment stack.
- Atlas trimming can introduce jitter unless pivots and source rectangles are preserved or explicitly declared.

Engine implications:

- Godot can use a root `Node2D` with synchronized layered `AnimatedSprite2D`/`Sprite2D` children. `Skeleton2D`/`Bone2D` helps with cutout rigs and IK, but is heavier than frame-aligned sprite layers.
- Unity's Sprite Library/Sprite Resolver workflow is a native route for swapping categorized sprites. For multi-part characters, Sorting Groups keep the character sorting as a unit while child renderers handle internal order.
- Phaser/Pixi workflows commonly use containers/layers and one animation state that advances every child layer together.
- Spine-style systems formalize the bone/slot/attachment/skin/draw-order model. This is conceptually useful even when Pip outputs simple PNG layers and manifests.

## AI-Assisted Paperdolling Patterns

AI paperdolling does not yet have one stable industry-standard workflow. The emerging pattern is a stack of partial controls: a base/reference image for identity, masks for edit locality, pose or video guidance for motion, style/reference controls for consistency, and manual or automated QA to catch drift. Most AI sprite workflows produce composited spritesheets, not reusable layer sheets.

Recurring AI workflows:

| Workflow | Shape | Strengths | Weaknesses | Paperdoll label |
|---|---|---|---|---|
| Reference-image to spritesheet | Upload or generate one character reference, then generate a full spritesheet or animation from it. | Fast route from concept to animation; many current tools expose this flow. | Output is a full character animation, not separate equipment/body layers; frame consistency still needs QA. | Composite animation |
| First-frame video to spritesheet | Generate a video from a character frame, extract key poses, then arrange frames into a sheet. | Good for motion exploration and hard-to-prompt actions. | Video frames can drift, blur, change scale, and lose pixel precision; layers are baked. | Composite animation source |
| Masked inpaint/edit | Draw or compute a mask around the hand/head/torso, then ask AI to add or modify only that region. | Better base preservation than unconstrained text edits; natural fit for weapons/hats/outfits. | Returns edited composites unless the editor has a verified changes-only layer mode. | Composite, extractable if QA passes |
| Asset combiner / bake-in | Place a generated weapon/item on one frame, send that combined frame into an animation/spritesheet model. | Practical way to make a sword/shield move with the character. | Bakes the item into every generated frame; not reusable across bodies without extraction or redrawing. | Baked equipment animation |
| Two-pass add/remove | AI adds the equipment to the character, then AI removes the character from the result. | Common workaround when no layer output exists; can be easy for helmets or simple props. | Extra cost and second hallucination step; may delete item pixels or leave body fragments. | AI-extracted layer candidate, high QA risk |
| Pose/control guided diffusion | Use pose, edge, depth, lineart, or skeleton controls plus a reference/style image. | Stronger spatial consistency than prompt-only generation; useful for multi-pose sheets. | Requires control inputs and model/tooling support; still produces composites unless paired with masks/layers. | Composite or generation control |
| Image-prompt/style adapter | Use a reference image or adapter to preserve identity/style across generated frames. | Helps maintain character/equipment identity when varying pose. | Identity/style preservation is soft, not a layer guarantee. | Consistency control |
| Custom model / style training | Train or tune on a game's sprites, body types, or equipment set. | Strong project-level consistency when enough data exists. | Heavy setup and still needs frame/layer contracts; may overfit. | Consistency control |
| Per-frame regenerate and cleanup | Regenerate only bad frames; erase or fix frame-level artifacts in an editor. | Matches how current AI sprite tools expose practical QA. | Human/editor loop; can break layer reuse unless changes are tracked. | QA/remediation workflow |

AI production guidance:

- Treat AI as an accelerant for drawing fitted composites, not as proof that a reusable layer exists.
- Prefer mask-first edits for paperdolling because uncontrolled image edits often redraw body pixels.
- Prefer one source base frame/animation contract and make every AI edit target that unchanged base, not the previous edited result.
- Use explicit reference controls when the tool supports them: base image, style image, pose/skeleton/keypoint image, palette/color image, seed, and frame count.
- Keep "baked equipment animation" and "reusable equipment layer" as separate product outputs. Both are useful, but they solve different user needs.
- Expect AI workflows to need curation: candidate selection, per-frame rejection, in-engine preview, and provenance tracking.

## PixelLab-Specific User Workflow Today

The user-described workflow is consistent with general AI pixel-art practice:

1. Create and animate the base character.
2. Edit the base image/frame to add the equipment.
3. Edit again to remove the character.
4. Save the remaining equipment image.
5. Layer that equipment in the game engine.

Public discussion around AI sprite sheets shows the same workaround: generate the character with equipment, then use a second prompt to remove the character and keep the fitted item. PixelLab's own Inpaint docs present adding a weapon to a character and changing outfits as intended edit use cases, but the public docs describe edited images, not reusable layer outputs.

The second "remove character" edit has three problems:

- It costs another generation/edit call.
- It asks the model to reconstruct a hidden semantic layer rather than merely preserve a known composite.
- It can delete legitimate equipment pixels, hallucinate occluded equipment, or leave body fragments.

The proposed wrapper should keep that workflow as a fallback, but the primary route should be:

```text
base frame + edit prompt -> equipment composite -> alpha-aware difference extraction -> QA -> transparent layer
```

The broader AI ecosystem also suggests two important additions to the PixelLab wrapper:

- A "baked animation" route should be offered honestly when the user only needs a character holding a weapon in a finished spritesheet.
- A "reusable paperdoll layer" route should remain stricter: same-canvas edit, extraction, manifest, and QA before layer claims.

## Candidate Approaches

| Approach | How it works | Strengths | Weaknesses | Best use |
|---|---|---|---|---|
| Reference-to-spritesheet AI | Use a base/reference character image and generate a new animation or sheet with the equipment described. | Fast and common across current AI sprite tools. | Produces baked composites, not equipment layers; consistency varies. | Prototyping dressed/armed characters quickly. |
| Video/key-pose workflow | Generate first-frame-guided video, extract key animation poses, then build a spritesheet. | Good for motion discovery and attack/gesture animation. | Poor layer reuse; pixel drift/blur risk; requires keyframe curation. | Motion ideation, not layer assets. |
| Asset combiner bake-in | Generate or import an item, visually place it on a character frame, then animate the combined image. | Practical for weapons/shields that must move with the body. | Reusable layer is lost unless later extracted; occlusion is baked. | Composite equipment animations. |
| Two-edit remove-character | PixelLab adds equipment, then PixelLab removes the character from the composite. | Simple mental model; can recover hidden item areas sometimes. | Extra cost; second generative failure; not deterministic; can leave fragments. | Manual fallback when diff extraction cannot isolate the item. |
| Same-canvas diff extraction | PixelLab adds one equipment item to the unchanged base, then local code copies changed pixels into a transparent layer. | One paid edit; deterministic extraction; easy QA; preserves PixelLab/user pixels only. | Fails if the body is redrawn, shifted, recolored, or if equipment color matches body too closely. | Default API layer-image workflow. |
| Masked inpaint plus diff | User/agent supplies a mask around the hand/head/torso, PixelLab edits only that area, then local extraction runs inside/near the mask. | Reduces unrelated redraws; better for tight placement. | Requires mask authoring and mask QA; output is still a composite. | High-value weapons, helmets, shields, and body-region edits. |
| Pose/reference-controlled edit | Use pose, skeleton, edge, style, or image-reference controls when the chosen AI route supports them. | Better placement and identity consistency than prompt-only edits. | Control quality depends on the model/tool; still composite-only without extraction. | Advanced retry strategy and future hardpoint workflows. |
| Edit-animation plus diff | PixelLab edits 2-16 animation frames consistently, then extraction runs frame-by-frame with temporal QA. | One route can handle a short animation segment. | Composite-only; frame drift and temporal jitter are high risk. | Animated weapon/outfit layer prototypes. |
| Transfer outfit plus diff | PixelLab applies a reference outfit to frames; extraction isolates changed pixels. | Good for clothing/armor style transfer over animation. | Less suited to held weapons; still composite-only. | Outfit/armor variants, not weapon-specific first choice. |
| Managed state/animation diff | Create a dressed managed character/state and compare to base managed character frames. | Can cover rotations and managed character flows. | Managed variants may not align pixel-perfectly; diff may capture whole body drift. | Dressed previews, maybe future batch experiments. |
| Skeleton/hardpoint anchoring | Estimate skeleton/keypoints and derive per-frame hand/attachment anchors for placement and QA. | Adds data needed by engines; can validate region and expected movement. | Does not generate equipment-only layers; needs keypoint sequence for animation. | Future hardpoint manifest and engine exporters. |
| Aseprite changes-only layer | Visible editor workflow writes only changed pixels to a layer, then agent verifies/export packages it. | Closest to native editor paperdolling. | Not headless; not stable REST/MCP; requires visible editor participation. | Artists already working in Aseprite. |

## Recommended System Shape

Name the output a "paperdoll package" rather than just a layer.

Minimum package:

```text
paperdoll-pack/
  base/
    idle/south/frame-000.png
  layers/
    weapon_iron_sword/front/idle/south/frame-000.png
    weapon_iron_sword/back/idle/south/frame-000.png
  composites/
    idle/south/frame-000.png
  previews/
    contact-sheet.png
    blink.gif
    mask-overlay.png
  qa/
    diff-heatmap.png
    report.json
  paperdoll.json
```

The manifest is the real contract. It should carry:

- Character identity and source route.
- Canvas size, frame size, origin, pivot, FPS, directions, animations, and frame order.
- Layer names, slot names, layer order, and whether a layer is front/back split.
- Equipment prompt and PixelLab route used.
- Input images/job IDs/asset IDs where safe and useful.
- Extraction thresholds and QA verdicts.
- Per-frame hardpoints when available.
- Engine export hints.

## Extraction Algorithm

Use local code to copy pixels from PixelLab/user outputs only. Do not draw, repaint, synthesize, or "fix" art locally unless explicitly labeled as non-PixelLab fallback.

Recommended stack:

- Pillow + NumPy for RGBA IO, alpha compositing, transparent PNGs, and simple previews.
- OpenCV for absolute difference, thresholding, morphology, connected components, and optional drift checks.
- scikit-image for SSIM, phase correlation, region properties, morphology helpers, and optional perceptual color difference.
- imageio for frame sequence IO if Pillow alone becomes awkward.

Algorithm:

1. Normalize inputs.
   - Load base `B_i` and composite `C_i` as same-size RGBA arrays.
   - Require same canvas, frame count, frame order, origin, and transparency mode.
   - Ignore transparent RGB for comparison, but preserve original alpha.
2. Detect drift before extraction.
   - Compare alpha masks and premultiplied luma.
   - Accept no shift, or integer translation only when it is clearly import/padding drift and can be corrected without resampling.
   - Fail on subpixel shift, rotation, scale, moved limbs, or inconsistent body silhouette.
3. Compute alpha-aware difference.
   - Premultiply RGB by alpha before differencing.
   - Seed the mask from high-confidence RGB/alpha differences.
   - Grow into lower-confidence neighboring differences so outlines do not break.
4. Apply conservative cleanup.
   - Use a small 3x3 close/open only to bridge cracks or remove isolated specks.
   - Label connected components.
   - Keep components that overlap the expected body/equipment region and have plausible area.
   - Allow multiple components for boots, gloves, eyes, or split weapon glints.
5. Construct the layer by copying pixels from the PixelLab composite.
   - `layer[mask] = composite[mask]`
   - Everywhere else remains transparent.
6. Verify round trip.
   - Composite `base + layer`.
   - Ensure outside-mask pixels still match the base.
   - Ensure the recomposed image matches the PixelLab composite within configured tolerance.
7. For animation, run temporal QA.
   - Check layer area, bounding box, centroid, component count, palette, and adjacent-frame mask overlap.
   - Fail on jitter, popping, one-frame disappearances, body drift, or unexplained palette shifts.
8. Generate previews.
   - Transparent layer files.
   - Final composites.
   - Contact sheet.
   - Blink/toggle GIF.
   - Diff heatmap and mask overlay for inspection.
   - Checkerboard previews only as clearly labeled QA artifacts, never final assets.

Default thresholds should be conservative and tunable per project. A useful starting point for pixel art is high-confidence max-channel RGB delta around 18, alpha delta around 16, low-confidence grow threshold around 6, and component filters based on expected region/area rather than global magic numbers.

## QA And Rejection Criteria

Reject or require manual/editor cleanup when:

- Canvas size, frame count, frame order, direction, or origin differs.
- The base body, face, hands, or limbs are moved or redrawn.
- The whole sprite changes palette or shading.
- Changed area is too large for the requested equipment.
- The extracted component includes duplicated body parts, full-body silhouettes, loose unregistered items, background, or edge artifacts.
- Equipment pixels are hidden behind the body and cannot be reconstructed from the visible composite.
- Equipment color is too close to base body/clothing colors to isolate safely.
- Semi-transparent VFX need physically correct alpha reconstruction from only a flattened composite. This is underdetermined; use editor layers, masks, or composite-only labeling.
- Animation layers flicker, jump, disappear, or change component count unexpectedly.

Successful extraction must prove:

- Same dimensions and transparent RGBA output.
- Layer alpha is zero outside accepted changed pixels.
- Nontransparent bounds overlap the intended body region or hardpoint.
- Base plus layer visually reads as one coherent character.
- Base plus layer matches the PixelLab composite enough for QA.
- No local drawing or repainting was used.

## Skeleton And Hardpoint Role

Skeleton routes should be a second-stage enhancement:

```text
base frame(s)
  -> estimate-skeleton
  -> normalize keypoints
  -> infer hand/head/torso/weapon hardpoints
  -> use hardpoints for prompt wording, region masks, QA bounds, and game-engine manifest
```

Use skeletons for:

- Hand/weapon anchor suggestions.
- Direction-specific prompt text.
- Expected body-region bounding boxes for extraction.
- Per-frame hardpoints exported to the game engine.
- Future keypoint authoring workflows.

Do not treat skeletons as:

- A deterministic equipment compositor.
- A way to recover occluded weapon pixels.
- A replacement for layer extraction QA.
- A complete animation source from one estimated pose. `estimate-skeleton` estimates one pose; real skeleton animation needs a keypoint sequence.

## Future Application Direction

A complete product likely wants an app because paperdolling is visual:

- Side-by-side base/composite/layer preview.
- Blink comparison.
- Per-frame timeline.
- Mask editor.
- Component accept/reject UI.
- Layer order and front/back split editor.
- Hardpoint editor.
- Engine export presets.
- Retry prompt builder with failed-QA diagnostics.

The Python prototype should intentionally stop short of being a full editor. Its job is to prove the deterministic extraction, manifest, preview, and QA contracts.

## Recommended Next Experiments

1. Single-frame sword extraction.
   - Base: one transparent south-facing RPG character frame.
   - PixelLab route: `edit-image` or `edit-images-v2` adding a sword to the hand.
   - Verify: extracted layer, round-trip composite, failure report if body changed.
2. Masked weapon extraction.
   - Add a hand/weapon region mask and compare against unmasked edit.
   - Verify lower unrelated redraw rate.
3. Eight-frame walk weapon extraction.
   - Base: PixelLab-managed walk animation frames.
   - PixelLab route: `edit-animation-v2` with "add the same sword to the right hand".
   - Verify temporal bbox/centroid stability and frame order.
4. Skeleton-assisted hardpoints.
   - Run `estimate-skeleton` on base frames.
   - Derive `hand_r`/`hand_l` anchors.
   - Use anchors to validate expected weapon region and export manifest hardpoints.
5. Front/back weapon split.
   - Test whether extracted weapon pixels can be split into `weapon_back` and `weapon_front` by overlap against body alpha and/or manual masks.
   - Determine whether automatic split is safe or needs editor confirmation.
6. AI baked-animation comparison.
   - Compare reference-to-spritesheet, first-frame video-to-sheet, and asset-combiner routes against the reusable-layer route.
   - Verify which outputs are useful composites and which, if any, survive extraction into reusable layers.
7. Mask-first versus prompt-only AI edit.
   - Generate the same weapon with and without a mask.
   - Measure unrelated base redraw rate, extraction success, and temporal stability.

## PixelLab AI Skill Paperdolling Approach (Reference)

Reviewed 2026-07-05 against the unofficial PixelLab AI Skill v1.5.5 (full download at the sibling `pixellab-ai-skill/` folder). This is prior art, recorded to map their choices onto this spike's model. It neither endorses nor ranks the projects.

### How their skill approaches layered characters

Their layering surface is mostly Markdown guidance plus one bundled recipe and one file-checker command. It does not do local pixel extraction.

- Modular outfit pipeline (`references/sprite-animation-layering.md`, `references/prompt-cheatsheet.md` "Layered Sprite Animation"): generate a neutral base body, build the base animation first, then `transfer-outfit-v2` a reference outfit onto the exact base frames to get a merged dressed animation, then `edit-animation-v2` with a prompt to "remove the character body and skin pixels, leave only the outfit layer." The outfit-only result is a second generative output, checked by compositing the same frame index back over the base body. This is exactly the two-pass add/remove path this spike flags under "Candidate Approaches" and "PixelLab-Specific User Workflow Today" as higher-risk: an extra paid edit that must reconstruct a hidden semantic layer and can delete or hallucinate pixels.
- Frame-grid contract: they write down the same-canvas/frame-count/frame-order/pivot/transparent-background contract before generating layers, plus stable frame names (`hero/base/walk_south_00.png`, `hero/weapons/sword/...`). This matches this spike's "Traditional Paperdolling Patterns" base-animation contract.
- State-first animation: pose a `create-character-state` first, then animate from that state so motion starts from a useful pose; small inpaint cleanups for face/hands/weapon jitter.
- Equipment/held weapons: sketch-and-inpaint only — duplicate the best base frame, sketch the item at the target size/position/color, mask the item plus the gripping hand/arm, then inpaint or edit-animation to propagate. This is Markdown guidance (`references/community-discord-workflows.md` "Weapons And Held Equipment"), not a tool. They advise separate layers only when gameplay needs runtime swaps/tinting/VFX, and baking the item into the outfit otherwise.
- `modular-rpg-character` recipe (`recipes/modular-rpg-character.json`): a dry-run manifest template with a `sprite_contract` (canvas, pivot, direction order, frames-per-direction, layer list, background), a `qa` note list ("base body is the timing source", "every layer preserves frame count/order/canvas/pivot", "outfit-only layers must not include body or skin pixels", "composite at least one base frame plus each layer"), and four chained assets with `depends_on` and `seed_offset` values: `create-character-v3` base → `animate-with-text-v3` walk → `transfer-outfit-v2` guard outfit → `edit-animation-v2` outfit-only cleanup. Payloads carry `REPLACE_WITH_BASE64_*` placeholders resolved by their manifest runner.
- `validate-sprites` checker (`scripts/pixellab_workflow.py`, `validate_sprite_layers`): a file-level validator over already-exported layer folders. Given `--root`, `--layers` (comma-separated, reference layer first), `--frame-glob`, and optional `--expected-size`, it globs each layer folder for frames, and reports: layers with no matching frames; per-frame PNG size mismatches; and — using the first layer as the reference set — missing frames, extra frames, and frame-order differences per other layer. It returns `ok`, per-layer `frame_counts`, and an `issues` list. Size is read from the 24-byte PNG IHDR header only; it does not read pixels, so it cannot confirm body/skin was actually removed or that a layer is non-blank/transparent (their separate `inspect-assets --require-nonblank` checks blankness). It validates layer files; it does not produce them.
- Skeleton: they bundle `examples/estimate-skeleton.json` (just an image) and `examples/animate-with-skeleton.json` (keypoint list, `view: side`/`direction: east` defaults) as endpoint example payloads. There is no paperdoll wiring, hardpoint derivation, or hardpoint manifest around them.

### Map onto this spike's model

- Already covered here: the frame-grid contract (see "Traditional Paperdolling Patterns"), `transfer-outfit-v2` / `edit-animation-v2` as composite routes (see "Current PixelLab Capability Boundary" and "Candidate Approaches"), state-first animation, and the honest split between baked composites and reusable layers (see "AI-Assisted Paperdolling Patterns"). Their "remove the body" second edit is this spike's "Two-pass add/remove" candidate, already labeled high-QA-risk and recommended only as a fallback.
- Genuinely useful concrete artifacts to consider adopting: (1) the `validate-sprites` file-level checker is a small, deterministic subset of the QA in "QA And Rejection Criteria" — specifically the input-contract checks (same frame set, same order, same size across layers), runnable on already-separated PNGs; and (2) the recipe's explicit `sprite_contract` and `qa` fields are a compact, machine-readable shape for the manifest sketched in "Recommended System Shape."
- Where this spike goes further: local alpha-aware diff extraction from a single same-canvas edit (see "Extraction Algorithm"), drift detection before extraction, temporal QA for animation, round-trip verification (`base + layer` matches the composite), skeleton-derived hardpoints as metadata (see "Skeleton And Hardpoint Role"), and engine exporters. None of these exist in their skill.

### What their skill does not do

- No local pixel diff-extraction of a changed-part layer from an unchanged base; the isolated layer, when produced, comes from a second PixelLab generative edit.
- No drift detection, no temporal QA, and no round-trip `base + layer` verification.
- No reusable-vs-composite honesty labels beyond the recipe's prose `qa` notes.
- No skeleton hardpoint manifest or hardpoint-bounded extraction.

## Reference Implementation: lysle.net Skeleton Tool

Reviewed 2026-07-07 against a working browser-based PixelLab skeleton editor ("Lysle.net Skeleton Tool", `https://lysle.net/satoshi/skeleton`), mirrored and source-audited locally. It is prior art for the skeleton/keypoint half of this system: it auto-rigs, hand-edits, and animates skeleton keypoints across a 4-direction grid of frames, calling PixelLab for generation. Recorded for the concrete keypoint evidence; it neither endorses nor ranks projects.

Concrete, verifiable findings:

- **Keypoint schema.** Each keypoint is `{ x, y, label, z_index }` — `x,y` normalized 0..1 within the frame (multiply by canvas size for pixels), `z_index` an integer draw-order/depth hint. `estimate-skeleton` responses are assigned straight into this model, so it is the shape the tool consumes from the API. This corroborates the Capability Boundary table's "keypoints with labels and z-index-like data": `z_index` is a real per-keypoint field, usable for front/back occlusion ordering (`weapon_back`/`weapon_front`) and for the plan's hardpoint metadata.
- **Label vocabulary (18, COCO-style):** NOSE, LEFT/RIGHT EYE, LEFT/RIGHT EAR, NECK, LEFT/RIGHT SHOULDER, LEFT/RIGHT ELBOW, LEFT/RIGHT ARM, LEFT/RIGHT HIP, LEFT/RIGHT KNEE, LEFT/RIGHT LEG. Naming quirk to note: **"ARM" is the wrist/hand end** and **"LEG" is the ankle/foot end** (elbow/knee are the mid-joints). This turns the plan's abstract "map labels to hand/head/torso/feet anchors" (Phase 5) into a concrete mapping.
- **Keypoint-anchored attachments as prior art.** The tool pins decorative sprites to named keypoints so they track that point across frames/directions — a working reference for the plan's "preview weapon alignment" / hardpoint-anchored placement idea. But those attachments are **cosmetic client-side SVG overlays, never baked into or returned by PixelLab.** So even a dedicated skeleton tool confirms PixelLab exposes no native equipment-layer output, reinforcing this spike's core boundary finding rather than challenging it.
- **Client-side estimate→edit→animate authoring** runs entirely in the browser with keypoints as portable JSON — a concrete reference for the Phase 7 "visual app / keypoint authoring" direction.

Caveats / what it does not prove:

- Its **generation** calls are proxied through the author's own backend (`lysle.net/.../api/generate-from-skeleton` and `/generate-from-rotation`) with the API key in the request body, returning a normalized `{ success, image, retryable, message }` envelope. So the tool does **not** reveal PixelLab's real `animate-with-skeleton` request/response schema — that hop is server-side. Only `estimate-skeleton` and `balance` are called directly (`api.pixellab.ai/v1/...`, `Bearer`). Treat the observed generation payload as the wrapper's shape, not PixelLab's.
- Observed against PixelLab **v1** (`/v1/estimate-skeleton`); confirm the label set and shape against the current v2 OpenAPI before hardcoding anchor logic.

## External Paperdolling Survey Cross-Check (ChatGPT Deep Research)

Reviewed 2026-07-05 against an external "Deep Research" survey of sprite-frame paperdolling for pixel-art RPGs (Aseprite, TexturePacker, Tiled, Spine/Spriter, atlas packing, palette discipline, diffusion-based AI methods, and AI copyright/licensing). It is a general, engine-agnostic survey of the whole problem space, not a PixelLab-specific design. Recorded here to separate what independently validates this spike from what is genuinely new and what does not apply to a hosted-PixelLab wrapper.

Independent validation (already covered here): the base-animation frame contract (same canvas, frame count, frame order, pivot, direction), the semantic slot and z-order stack (`weapon_back … body … weapon_front … hair_front … fx`), front/back occlusion splits, per-frame hardpoints (`hand_r`, `weapon_tip`), one animation clock driving all layers, treating the character as one engine world object with child layer order, pivot/source-rectangle preservation to avoid trim jitter, and the split between baked composites and reusable layers. The survey reaches the same conclusions from the general-tooling side. Useful corroboration; it adds no new routing rule.

Genuinely additive and accurate (worth carrying into the plan):

- Atlas packaging discipline, with concrete starting points: trim transparent borders only if source-size metadata is preserved so the runtime can reconstruct untrimmed placement; 1-2 px border padding to stop neighbor bleed; 1 px extrude to stop edge flicker; atlas rotation off unless the loader supports rotated regions; conservative atlas max size (2048, raise to 4096 only when the target is validated); duplicate-frame detection to save area. The jitter concept was already here; the parameters are new and belong in the Engine Export phase.
- Provenance and licensing is a real shipped-art concern this spike did not cover. The 2025 U.S. Copyright Office copyrightability report holds that AI output is protectable only where a human author contributes sufficient expression, not from prompts alone; Steam requires creators to disclose pre-generated and live-generated AI content; tool/model licenses (for example Adobe Firefly commercial terms, the Stability AI Community License revenue thresholds) attach their own conditions. For Pip the operative license is PixelLab's own terms of service, not these; the actionable rule is to keep a provenance log (route, prompt, seed, model, usage) and never assert copyright or licensing guarantees on the user's behalf.
- Standard atlas manifest field names (`sourceSize`, `spriteSourceSize`, pivot stored in untrimmed frame space) are worth mirroring in the export manifest for drop-in interop with Pixi/Phaser/TexturePacker-style loaders.
- Palette-class recolor (`skin`, `cloth_primary`, `metal`, `fx` as swappable classes) is a cheap variation axis in general paperdolling, but it manufactures new pixels locally and so is in tension with this system's pixel-provenance contract. Out of core scope unless recolor variants become an explicit product goal, and then only as a labeled user-approved transform.

Challenged / not adopted (poor fit for a hosted-PixelLab wrapper, or already positioned):

- The survey's AI depth assumes direct control of a raw diffusion pipeline: Diffusers img2img/inpaint, ControlNet conditioning, IP-Adapter, and LoRA/DreamBooth training. PixelLab is a hosted API that abstracts those controls behind its own routes; the wrapper cannot inject a ControlNet map or a project LoRA into a PixelLab call. This spike's AI-patterns table already captures what PixelLab-style tools actually expose, so the extra diffusion detail is background, not an actionable route.
- Skeletal authoring (Spine/Spriter runtime skins, AnimationState mix durations of ~0.1-0.6 s, cross-rig retargeting) is an engine-runtime/animation concern downstream of layer production, not the extraction wrapper's job. Already positioned as engine-side here.
- Post-generation pixelization/quantization (SD-πXL, cell-aware pixelization) is largely unnecessary because PixelLab output is already palette-native pixel art. The wrapper's palette job is drift detection across base and composite, not re-pixelizing a non-pixel model's output.
- GPU texture compression (KTX 2.0 / Basis Universal, ASTC/ETC2/BC) is a per-target engine concern downstream of the exporter; keep it out of the Python extraction/QA core and revisit only if a specific export target requires it.
- The survey does not address PixelLab's public-surface boundary, the same-canvas diff-extraction core, drift/temporal/round-trip QA, or the one-edit-plus-extraction versus two-pass remove-character cost tradeoff. This spike remains the authority on those; the survey complements it on downstream storage, packaging, and legal, it does not replace it.

## Source Notes

Official PixelLab:

- [REST `llms.txt`](https://api.pixellab.ai/v2/llms.txt)
- [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [Interactive REST docs](https://api.pixellab.ai/v2/docs)
- [MCP docs](https://api.pixellab.ai/mcp/docs)
- [General output method docs](https://www.pixellab.ai/docs/options/general)
- [Edit image (Pro) docs](https://www.pixellab.ai/docs/tools/edit-image-pro)
- [PixelLab Inpaint docs](https://www.pixellab.ai/docs/tools/inpaint)
- [PixelLab home page editing/rotation claims](https://www.pixellab.ai/)

Aseprite/editor findings:

- [Aseprite scripting API](https://www.aseprite.org/api/)
- [Aseprite Sprite API](https://www.aseprite.org/api/sprite)
- [Aseprite Image API](https://www.aseprite.org/api/image)
- [Aseprite layers docs](https://www.aseprite.org/docs/layers/)
- Local PixelLab Aseprite extension inspected on 2026-07-04. Findings are summarized without local machine paths, line references, source snippets, or extension filename citations.

AI sprite and diffusion workflow references:

- [Scenario spritesheet workflow](https://help.scenario.com/articles/9088582240-create-spritesheets-with-scenario)
- [Spritesheets.ai advanced editor and asset combiner](https://www.spritesheets.ai/tutorial/advanced-edits-and-playground)
- [Sprite Sheet Diffusion paper](https://arxiv.org/html/2412.03685v2)
- [ComfyUI inpainting workflow](https://docs.comfy.org/tutorials/basic/inpaint)
- [Hugging Face Diffusers inpainting guide](https://huggingface.co/docs/diffusers/en/using-diffusers/inpaint)
- [ControlNet paper](https://arxiv.org/abs/2302.05543)
- [IP-Adapter paper](https://arxiv.org/abs/2308.06721)

Traditional paperdoll and engine references:

- [Universal LPC Sprite Sheet Character Generator](https://github.com/liberatedpixelcup/Universal-LPC-Spritesheet-Character-Generator)
- [Liberated Pixel Cup style guide](https://lpc.opengameart.org/static/LPC-Style-Guide/build/styleguide.html)
- [Spine runtimes](https://en.esotericsoftware.com/spine-using-runtimes/)
- [Godot 2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html)
- [Godot `RemoteTransform2D`](https://docs.godotengine.org/en/stable/classes/class_remotetransform2d.html)
- [Unity Sprite Swap examples](https://docs.unity3d.com/Packages/com.unity.2d.animation%407.0/manual/ex-sprite-swap.html)
- [Phaser animations](https://docs.phaser.io/phaser/concepts/animations)
- [PixiJS containers](https://pixijs.com/8.x/guides/components/scene-objects/container)
- [PixiJS spritesheets](https://pixijs.com/7.x/guides/components/sprite-sheets)
- [Ascension paperdoll tutorial](https://www.ascensiongamedev.com/topic/1041-paperdoll-tutorial/)
- [RPG Maker visual equipment discussion](https://forums.rpgmakerweb.com/threads/trying-to-implement-a-paper-doll-composite-sprite-visual-equipment-system.182351/)
- [GameDev.net paperdoll discussion](https://gamedev.net/forums/topic/622607-2d-action-game-sprites-paper-doll-equipment-or-custom-characters-with-unchanging-appearance/)
- [AI sprite-sheet equipment discussion](https://www.reddit.com/r/aigamedev/comments/1t2r1nn/armor_and_weapon_generation_for_2d_pixel_sprite/)

Image-processing references:

- [Pillow ImageChops](https://pillow.readthedocs.io/en/latest/reference/ImageChops.html)
- [OpenCV array operations](https://docs.opencv.org/4.x/d2/de8/group__core__array.html)
- [OpenCV thresholding](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html)
- [OpenCV connected components](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html)
- [OpenCV morphology](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- [scikit-image structural similarity](https://scikit-image.org/docs/0.25.x/api/skimage.metrics.html)
- [scikit-image registration](https://scikit-image.org/docs/stable/api/skimage.registration.html)

External survey cross-check (added 2026-07-05; org-root references for the packaging and legal points carried into this spike):

- [U.S. Copyright Office AI initiative and copyrightability report](https://www.copyright.gov/ai/)
- [Stability AI Community License](https://stability.ai/community-license-agreement)
- [Adobe Firefly](https://www.adobe.com/products/firefly.html)
- [TexturePacker documentation](https://www.codeandweb.com/texturepacker/documentation)
- [Khronos KTX / Basis Universal](https://www.khronos.org/ktx/)

Paperdoll asset systems, generators, and tutorials (curated 2026-07-07; complements the "Traditional paperdoll and engine references" list above with modular layer-sheet assets and step-by-step walkthroughs):

LPC (open layered-sprite standard):

- [Universal LPC Spritesheet Character Generator — live app](https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/) — stack body/clothing/armor/weapon layers and export the sheet; the clearest working demo of paperdoll layering.
- [Universal LPC Spritesheet Character Generator — GitHub repo](https://github.com/liberatedpixelcup/Universal-LPC-Spritesheet-Character-Generator) — the actual CC-licensed layer PNGs plus z-index sheet definitions.
- [BenCreating/LPC-Spritesheet-Generator](https://github.com/BenCreating/LPC-Spritesheet-Generator) — actively maintained generator variant.
- [LPC Style Guide (frames, directions, timing)](https://lpc.opengameart.org/static/LPC-Style-Guide/build/styleguide.html) — the frame contract every LPC layer conforms to.
- [LPC Character Bases (OpenGameArt)](https://opengameart.org/content/lpc-character-bases) and [LPC Revised Character Basics](https://opengameart.org/content/lpc-revised-character-basics) — base bodies to layer onto.

Modular pixel-art layer-sheet asset systems:

**Quality exemplar — Seliel the Shaper's Mana Seed bases.** The reference standard for *both* halves of this problem: clean modular paperdoll layering **and** genuinely expressive character animation. SNES-inspired, 32px character centered in 64×64 cells, **100% hand-drawn (no AI)**, 150+ animations including expressive melee combat (overhand / forehand / backhand strikes), bow, evade, hit, and fall. Equipment is delivered as **frame-matched layer sheets** stacked over the base (technique #1 above) with shader-based color ramps — the fluidity comes from an animator hand-keying every frame, not from a rig or from AI. Treat these as the visual-quality benchmark that extracted/generated equipment layers should aim toward, not a technique this system can auto-reproduce.

- [Mana Seed "Character Base" by Seliel the Shaper](https://seliel-the-shaper.itch.io/character-base) — combat/action-RPG-oriented modular base: base body plus frame-matched clothing/hair/armor/weapon layer sheets.
- [Mana Seed "Farmer Sprite System" / Farmer Base (free sample; full ~$29.99)](https://seliel-the-shaper.itch.io/farmer-base) — the base behind the expressive attack animations in the willyxz paper-doll demo below; farming-sim body that also ships melee-strike and bow combat. Includes a layer customizer. Note Seliel's own caveat: it has combat animations but is not recommended as a dedicated action-RPG body.
- [Mana Seed Official collection](https://itch.io/c/398089/mana-seed-official) and [Mana Seed Compatible (third-party layers)](https://itch.io/c/1072771/mana-seed-compatible) — the matching equipment-layer ecosystem.
- [Memao Sprite Sheet Creator](https://sleeping-robot-games.itch.io/sprite-sheet-creator) — paper-doll customizer that exports sprite sheets.

RPG Maker paperdoll / visual-equipment discussions:

- [Implementing paper dolls (RPG Maker)](https://forums.rpgmakerweb.com/threads/implementing-paper-dolls.107148/)
- [Paperdolls… is it possible? (RPG Maker)](https://forums.rpgmakerweb.com/threads/paperdolls-is-it-possible.45622/)

Runtime implementations and video walkthroughs:

- [Paper Doll System for Unity (Mana Seed compatible)](https://willyxz.itch.io/paper-doll-for-farmer-base) and [Paper Doll for Unity by DirePixel](https://direpixel.itch.io/paper-doll-for-unity) — runtime layer-stacking implementations.
- [Video — Paper Doll for Unity: How to Use](https://www.youtube.com/watch?v=SjRCLN0t0Ww)
- [Video — Paper Doll Character Customizer (Unity, ScriptableObjects)](https://www.youtube.com/watch?v=B6gFcrBzhUE)
- [Video — Godot 2D Cutout Animation Setup](https://www.youtube.com/watch?v=tCrsscmdv9M) — the skeletal-rig alternative (contrast to frame-matched sheets).
- [Godot Forum — layering sprites / dress-up a character in 2D](https://forum.godotengine.org/t/how-to-layer-sprites-dress-up-a-character-in-2d/11898)
