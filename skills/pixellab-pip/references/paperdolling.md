# Paperdolling

Read this for layered characters, outfit variants, equipment swaps, or animation-consistent paperdoll workflows.

Treat paperdolling as a character-anchored edit workflow first, then a composition workflow. Requests for fitted hair, facial features, horns, wearables, accessories, armor, held gear, footwear, VFX, or similar body-region additions should stay anchored to the base character image instead of being routed as standalone objects.

PixelLab can generate base sprites, edited states, outfit-transfer frames, masked inpaints, image edits, and standalone transparent objects. Public REST v2/MCP docs do not expose first-class editor layer creation, layer assignment, semantic layer extraction, or isolated changed-part outputs. Some editor integrations, including the Aseprite extension, may expose editor-local changes-only layer import behavior. Treat that as an editor-specific capability, not a REST/MCP contract, and accept the result only after visual/export verification proves it is actually changes-only.

Paperdoll rule: visible body/layer pixels must come from PixelLab or the user. Local tools may compose, align, package, import/export, mask, resize, crop, compute differences, extract changed pixels into transparent images, and verify layers, but must not draw or repaint them unless the user explicitly requests or approves a labeled non-PixelLab fallback.

Ask or infer:

- Base character identity.
- Direction count.
- Current character direction for each edit, such as south/down-facing, east/right-facing, north/up-facing, west/left-facing, or diagonal.
- Sprite and canvas size.
- Animation list.
- Layers such as body, hair, outfit, armor, weapon, accessory, shadow, and VFX.
- For every requested visual addition: identity, intended body region, position, facing/rotation, attachment/occlusion rule, and whether it should appear in front of or behind the base body.
- Whether outputs must be separate transparent layer image files, editor-native layers, composited previews, or both.
- Whether an existing composite may be edited lossily, or whether reusable isolated layers are required.

When the user asks for layers but does not name an editor or output format, ask them to choose between:

- Separate transparent image layer files plus a final composited image.
- An Aseprite/editor layer workflow where each layer contains only the newly added pixels.

If the user declines to choose an output shape, do not claim separate layers. Pick the best character-anchored composite route or ask again when layer files are required. Use verified editor changes-only layers only when the user is already working in that editor or accepts visible editor guidance. Use the API layer-image workflow only when the user requests or accepts separate transparent image layer files plus a final composite. Do not choose standalone object generation as the fallback for fitted body additions.

Preserve:

- Canvas size.
- Frame count.
- Frame order.
- Direction names/order.
- Origin/pivot.
- Transparency/background.
- Palette/style reference where consistency matters.

For reusable sets, confirm the base character and frame-grid contract before variants. Inspect outputs against the preservation list above before describing them as reusable layers.

## Route Contract

| Goal | Route | Warning |
|---|---|---|
| Fitted isolated paperdoll layer in Aseprite | Use the visible Aseprite extension image-edit workflow on the base character frame. When the installed extension exposes a new-layer changes-only `output_method`, request that mode for isolated layers. Prompt with the character identity, current direction, requested addition, target body region, exact placement, rotation/facing, scale, occlusion, and preservation rules. | This is an editor-surface workflow, not a stable headless API. Do not automate extension internals or call private operation URLs. If the agent cannot operate the visible extension with user participation or inspect exported layers, it must not claim it created fitted changes-only layers; it can guide the user, use public REST for composites, or package already verified exported layers afterward. |
| Fitted paperdoll edit from code/API | Use a documented REST v2 image-edit endpoint on the base image when a public API route is required; check current docs/schema before naming the exact endpoint. Use a detailed character-anchored edit prompt and same canvas size. Treat the API result as an edited composite first. | Public REST image-edit endpoints are not Aseprite layer workflows. Public REST docs describe image editing outputs, not editor `output_method` layer modes. |
| Separate transparent layer images plus final composite, without Aseprite | For each requested addition, create a same-canvas edited composite from the unchanged base image, with a prompt that asks PixelLab to add only that feature/body-region addition and preserve every other base pixel. Locally compare the edited composite to the base, copy changed pixels into a transparent PNG layer image, then compose base plus accepted layer images into the final PNG. Deliver at least `base`, one transparent image per requested layer, each intermediate edited composite if useful for QA, and the final composite. | This is image-file paperdolling, not editor-native layer creation. Reject and retry if the extracted layer contains a duplicated body, large unrelated redraws, moved limbs, background changes, or loose unregistered parts. Do not call the extracted PNG a reusable layer until it passes transparency, bounds, canvas-size, and composite QA. |
| Masked fitted layer attempt | Use the visible editor image-edit workflow with a body-region selection and changes-only layer output mode when available, or REST `inpaint-v3` only when the user supplies or approves a mask for the body region to edit. | Inpainting returns an edited image, not semantic layer extraction. Editor-local changes-only output is the better layer path when available and verified. |
| Standalone prop/accessory sprite | Use MCP object tools or REST object/image routes only when the user asks for a separate reusable prop/accessory sprite that does not need to be fitted to the current body pose. | Do not use standalone object generation for fitted hair, clothes, hats, eyes, or accessories on an existing character; it commonly produces unregistered loose parts. |
| Dressed character preview/state | MCP `create_character_state`, REST character/edit routes, or editor image-edit workflow with normal composite output. | Output is a character variant/composite, not a separate reusable layer unless generated with a changes-only layer mode, or extracted into a transparent layer image from a verified same-canvas edit. |
| Outfit/equipment across animation frames | REST `transfer-outfit-v2` or `edit-animation-v2`; MCP character animation only when working with managed character assets. | Preserve frame count/order and label output as composited animation frames. |
| Existing composite to isolated layer | Require an explicit mask or editor cleanup plan; use REST inpaint/edit only as a fallback. | PixelLab does not document semantic layer extraction, character subtraction, or occluded addition reconstruction. |
| Website Try on | Use only as visible/manual website assistance when appropriate. | It returns one composited image and is experimental; it is not a layer pipeline. |

## API Layer-Image Paperdoll Workflow

Use this workflow when the user wants separate image files for paperdoll layers and a final composited image, but is not using Aseprite or another editor with verified changes-only layer output.

1. If the user asks for layers without naming an editor or file format, ask them to choose between separate transparent PNG layer images plus a final composited PNG, or an Aseprite/editor layer workflow where each layer contains only the newly added pixels. Proceed with this workflow only when the image-file artifact shape is requested or accepted.
2. Generate or obtain the base character image first. Save it as the base layer image and keep it unchanged for every subsequent addition edit.
3. For each requested layer, run a separate existing-image edit against the original base image, not against the previous edited result. This keeps each extracted layer independent.
4. Prompt each edit as a single body-region addition. Include:
   - Character identity and silhouette: species/body type, colors, scale, and style.
   - Direction: south/down-facing, east/right-facing, north/up-facing, west/left-facing, or diagonal.
   - Target addition: hair, hat, shirt, boots, eyes, armor, held gear, VFX, etc.
   - Body part and side: top/front of head, torso, left hand, both feet, right hip, behind back, etc.
   - Placement and geometry: centered, tilted, wrapped around limb, follows perspective, in front of or behind body.
   - Preservation: keep every base pixel unchanged except where the addition naturally occludes it; keep exact canvas size and transparent background.
5. Save the PixelLab edited result as an intermediate composite for that layer.
6. Locally create a transparent layer image by comparing the intermediate composite to the base image and copying only changed pixels from the PixelLab result. Use conservative alpha/difference thresholds that preserve the addition while avoiding noisy unchanged pixels.
7. Verify the extracted layer image before accepting it:
   - Same canvas size as the base.
   - Transparent outside the addition.
   - Nontransparent bounds overlap the intended body region.
   - No full-body duplicate, moved limbs, face/body redraw, background, or unrelated changed pixels.
   - The base plus the layer reads as one coherent character.
8. Repeat per layer. Then compose the final image from the base plus the accepted transparent layer images in the requested order, such as base, hair, clothing, hat, accessories, VFX.
9. If extraction fails, do not patch the art manually. Retry with a smaller body-region prompt, an approved mask/inpaint route, or an editor workflow. If the user accepts composite-only output, label it as composite-only and skip layer claims.

Example hair prompt for API layer-image extraction:

```text
Edit this south-facing 92x92 chibi humanoid creature sprite. Add only short spiky teal hair attached to the top/front of the head, following the head perspective and centered above the forehead. Keep every existing body, face, limb, outline, pose, canvas pixel, and transparent background unchanged except where the hair naturally covers the scalp. Do not redraw the character, do not move any body parts, do not add a second head, and do not create loose detached hair pieces.
```

Example clothing-and-hat prompt for API layer-image extraction:

```text
Edit this south-facing 92x92 chibi humanoid creature sprite. Add only a fitted red jacket, dark shorts, small boots, and a soft rounded cap as one clothing paperdoll addition. Place the cap on top of the head with a front brim, the jacket over the torso and arms, shorts at the waist, and boots on both feet. Match the existing pixel-art outline, shading, palette weight, and camera angle. Keep every base character pixel unchanged except where clothing naturally covers it. Keep exact canvas size and transparent background. Do not redraw the character and do not generate loose unregistered parts.
```

## Aseprite Extension Paperdoll Workflow

Use this workflow when the user wants a layerable paperdoll result and is working in Aseprite or accepts visible editor guidance. This relies on editor integration behavior, not public REST/MCP layer semantics:

1. Put the base character frame on its own layer, with the correct direction/frame active.
2. Choose the extension's existing-image edit workflow rather than object/map-object generation.
3. If available, use the current selection to constrain the edit region around the body region. For example, select the head for hair/hat, torso for shirt/coat, hands for gloves, feet for boots, face for eyes, or weapon hand for held gear.
4. Click `Set image` after activating the correct base frame, layer, and optional selection. Verify the captured edit image is the current base/selection and not a stale frame or old selection.
5. Set the extension `output_method` to the new-layer changes-only mode when available. Treat this as a request to the extension, not a guarantee; accept the layer only after visual/export verification confirms it contains only the intended changed pixels. Use a current-layer changes-only mode only when the user explicitly wants to write changes into the active layer.
6. Use a detailed prompt that describes the existing character and the requested addition placement. Include:
   - Character identity and silhouette: species/body type, colors, scale, and style.
   - Direction: south/down-facing, east/right-facing, north/up-facing, west/left-facing, or diagonal.
   - Target visual addition: hair, hat, clothing, eyes, accessory, armor, held gear, etc.
   - Body part and side: on top of head, behind head, around neck, torso, left hand, right hip, both feet, etc.
   - Position and rotation: centered, tilted left, wraps behind ears, follows body perspective, front-facing brim, side-facing sleeve, etc.
   - Preservation: keep all existing character pixels unchanged except where the addition naturally occludes them; keep transparent background and exact canvas size.
7. After generation, inspect the layer by hiding/showing the base. The layer is successful only if it registers to the body in the same canvas and does not contain a duplicated/redrawn character.
8. Export the layer alone when possible and inspect transparency/nontransparent bounds. Verify exact canvas size, unchanged frame count/order when relevant, no full-body redraw, no duplicated character, and no unregistered loose parts.
9. Inspect the composite with base plus layer visible. The composite must read as one coherent character with the requested addition attached to the intended body region.
10. If the layer or composite fails any check, reject it and retry with tighter body-part selection, a stricter prompt, or a smaller edit region.

Example prompt:

```text
Edit this south-facing 92x92 chibi amphibian-dragon creature sprite. Add only a mint green leafy hair tuft as a paperdoll layer on the top/front of the head, following the head perspective and centered above the eyes. Keep the teal body, face, limbs, outline, pose, canvas size, and transparent background unchanged. Output only the changed hair pixels on the new layer; do not redraw the character, do not add a second head, and do not create separate loose parts.
```

For clothing plus a hat:

```text
Edit this south-facing 92x92 chibi amphibian-dragon creature sprite. Add only a fitted adventurer outfit and small rounded explorer hat as paperdoll changes: hat on top of the head with front brim, scarf around the neck, short tunic over the torso, belt at the waist, gloves on both hands, and boots on both feet. Match the existing pixel-art outline, shading, palette weight, and camera angle. Keep the base creature pixels unchanged except where the clothing naturally covers the body. Keep exact canvas size and transparent background. Output only the changed clothing and hat pixels on the new layer; do not redraw the creature and do not generate loose unregistered parts.
```

`inpaint-v3` requires `description`, `inpainting_image`, and `mask_image`; white mask areas are generated/replaced and black areas are preserved. Treat its output as a whole edited image, not a layer. `context_image` and `bounding_box` are deprecated in current OpenAPI.

`edit-images-v2` supports `edit_with_text` and `edit_with_reference` for 1-16 images depending on size. It can help keep related edits consistent, but public REST output should be treated as an edited image/composite unless a separate transparent layer image is extracted and verified, or a changes-only editor layer is verified from an editor workflow.

`edit-animation-v2` and `transfer-outfit-v2` operate on 2-16 frames and return edited/composited frames, not equipment/body layers.

If layer fidelity matters and the user is in Aseprite, prefer the visible editor image-edit workflow plus an extension changes-only layer output mode over generating standalone objects. After each changes-only edit produces a visually verified fitted layer, save or export that layer separately before packaging or compositing in Aseprite, Pixelorama, or local tooling.

Route MCP-managed characters through character/state/animation tools. Use REST v2 raw animation, edit-animation, interpolation, and outfit-transfer routes only when exact file-level control matters. Warn that text-only paperdolling drifts without a base frame, seed, or reference.
