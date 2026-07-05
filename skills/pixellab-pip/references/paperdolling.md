# Paperdolling

Read this for layered characters, outfit variants, equipment swaps, or animation-consistent paperdoll workflows.

SKILL.md holds the global asset-integrity and no-baked-background rules; this file does not restate them. Paperdoll-specific allowance: local tools may compose, align, mask, resize, crop, diff, and extract changed pixels into transparent layer images, and verify them, but visible body/layer pixels must come from PixelLab or the user (no local drawing or repainting without an approved, labeled non-PixelLab fallback).

Treat paperdolling as a character-anchored edit workflow. Fitted hair, facial features, horns, wearables, armor, held gear, footwear, VFX, or similar body-region additions stay anchored to the base character image as edits on the base frame; do not route them as standalone objects unless the user explicitly wants a separate unattached prop.

Public REST v2/MCP docs do not expose first-class editor layer creation, layer assignment, semantic layer extraction, or isolated changed-part outputs. Some editor integrations (the Aseprite extension) may expose an editor-local changes-only layer import. Treat that as editor-specific, not a REST/MCP contract, and accept it only after visual/export verification proves it is actually changes-only.

Gather up front: base character identity, direction count, current direction per edit, sprite/canvas size, animation list, and the layer set (body, hair, outfit, armor, weapon, accessory, shadow, VFX). Ask whether outputs must be separate transparent layer image files, editor-native layers, composited previews, or both, and whether an existing composite may be edited lossily or reusable isolated layers are required.

When the user asks for layers but names no editor or format, offer two output shapes:

- Separate transparent image layer files plus a final composited image.
- An editor (Aseprite) workflow where each layer contains only the newly added pixels.

If the user declines to choose, do not claim separate layers: pick the best character-anchored composite route or ask again. Do not fall back to standalone object generation for fitted additions.

Preserve across every paperdoll edit: canvas size, frame count/order, direction names/order, origin/pivot, transparency, and palette/style where consistency matters. Inspect outputs against this list before calling them reusable layers.

## Prompt Fields (every fitted addition)

State these once per edit, in the edit prompt:

- Character identity and silhouette: species/body type, colors, scale, style.
- Direction: south/down-facing, east/right-facing, north/up-facing, west/left-facing, or diagonal.
- Target addition: hair, hat, shirt, boots, eyes, armor, held gear, VFX, etc.
- Target body region and side: top/front of head, torso, left hand, both feet, right hip, behind back, etc.
- Placement and geometry: centered, tilted, wrapped around a limb, follows perspective, in front of or behind the body.
- Preservation: keep every base pixel unchanged except where the addition naturally occludes it; keep exact canvas size and transparent background.

## Route Contract

| Goal | Route | Warning |
|---|---|---|
| Fitted isolated paperdoll layer in Aseprite | Use the visible Aseprite extension image-edit workflow on the base character frame. When the installed extension exposes a new-layer changes-only `output_method`, request that mode. Prompt with the fields above. | Editor-surface workflow, not a stable headless API. Do not automate extension internals or private operation URLs. If the agent cannot operate the visible extension with user participation or inspect exported layers, it must not claim it created fitted changes-only layers; guide the user, use public REST for composites, or package already-verified exported layers. |
| Fitted paperdoll edit from code/API | Use a documented REST v2 image-edit endpoint on the base image; check current docs/schema before naming the exact endpoint. Detailed character-anchored edit prompt, same canvas size. Treat the API result as an edited composite first. | Public REST image-edit endpoints are not editor layer workflows; they output edited images, not `output_method` layer modes. |
| Separate transparent layer images plus final composite, without Aseprite | Per addition, create a same-canvas edited composite from the unchanged base with a prompt to add only that feature and preserve every other base pixel. Locally diff against the base, copy changed pixels into a transparent PNG, then compose base plus accepted layers into the final PNG. Deliver at least `base`, one transparent image per layer, and the final composite. | Image-file paperdolling, not editor-native layer creation. See verification checklist before calling any PNG a reusable layer. |
| Masked fitted layer attempt | Visible editor image-edit workflow with a body-region selection and changes-only layer output when available, or REST `inpaint-v3` only when the user supplies or approves a mask for the body region. | Inpainting returns an edited image, not semantic layer extraction. Verified editor changes-only output is the better layer path. |
| Standalone prop/accessory sprite | MCP object tools or REST object/image routes only when the user wants a separate reusable prop that need not fit the current body pose. | Do not use object generation for fitted hair, clothes, hats, eyes, or accessories on an existing character; it produces unregistered loose parts. |
| Dressed character preview/state | MCP `create_character_state`, REST character/edit routes, or editor image-edit with normal composite output. | Output is a character variant/composite, not a separate reusable layer unless generated with a changes-only layer mode or extracted and verified from a same-canvas edit. |
| Outfit/equipment across animation frames | REST `transfer-outfit-v2` or `edit-animation-v2`; MCP character animation only for managed character assets. | Preserve frame count/order; label output as composited animation frames. |
| Existing composite to isolated layer | Require an explicit mask or editor cleanup plan; use REST inpaint/edit only as a fallback. | PixelLab does not document semantic layer extraction, character subtraction, or occluded-addition reconstruction. |
| Website Try on | Visible/manual website assistance only. | Returns one composited image and is experimental; not a layer pipeline. |

## Workflow

Both output modes share these steps and branch only at output:

1. Confirm the output shape with the user (above) before claiming layers.
2. Obtain the base character image/frame and keep it unchanged for every addition edit.
3. Run each requested layer as a separate existing-image edit against the original base (not the previous edited result), so layers stay independent. Prompt each edit as a single body-region addition using the Prompt Fields above.
4. Produce the layer per the chosen output mode:
   - **Separate transparent image files (no editor):** save the PixelLab edit as an intermediate composite, then locally diff it against the base and copy only changed pixels into a transparent PNG, using conservative alpha/difference thresholds that keep the addition and drop noisy unchanged pixels.
   - **Editor changes-only layer (Aseprite):** put the base frame on its own layer with the correct direction/frame active; use the extension's existing-image edit workflow (not object/map-object generation); optionally constrain with a body-region selection (head for hair/hat, torso for shirt, hands for gloves, feet for boots); click `Set image` and verify it captured the current base/selection, not a stale frame; set the extension `output_method` to the new-layer changes-only mode (treat as a request, not a guarantee); generate, then inspect by hiding/showing the base and export the layer alone.
5. Verify the layer against the checklist below before accepting it.
6. Repeat per layer, then compose the final image from base plus accepted layers in the requested order (base, hair, clothing, hat, accessories, VFX).
7. On failure, do not patch art manually: retry with a smaller body-region prompt, an approved mask/inpaint route, or an editor workflow. If the user accepts composite-only output, label it composite-only and drop layer claims.

## Extracted-Layer Verification

Accept a layer only if all hold:

- Same canvas size as the base.
- Transparent outside the addition; nontransparent bounds overlap the intended body region.
- No full-body duplicate, moved limbs, face/body redraw, background, or unrelated changed pixels.
- Base plus layer reads as one coherent character with the addition attached to the intended region.
- (Editor) unchanged frame count/order when relevant; no loose unregistered parts.

Do not call an extracted PNG or editor layer a reusable layer until it passes these. Reject and retry on a duplicated body, moved limbs, redraw, background change, or loose unregistered parts.

## Example Prompt (hair)

```text
Edit this south-facing 92x92 chibi humanoid creature sprite. Add only short spiky teal hair attached to the top/front of the head, following the head perspective and centered above the forehead. Keep every existing body, face, limb, outline, pose, canvas pixel, and transparent background unchanged except where the hair naturally covers the scalp. Do not redraw the character, do not move any body parts, do not add a second head, and do not create loose detached hair pieces.
```

Clothing, multi-part outfits, and hats follow the same pattern: one prompt listing each piece and its body region (cap on head with front brim, jacket over torso/arms, shorts at the waist, boots on both feet), matching the existing outline/shading/palette/camera, preserving all other base pixels and the exact canvas/background.

## API Facts

- `inpaint-v3` is documented as Pro (cost signal per SKILL.md Model And Mode Terms). It requires `description`, `inpainting_image`, and `mask_image`; white mask areas are generated/replaced, black areas preserved. Output is a whole edited image, not a layer. `context_image` and `bounding_box` are deprecated in current OpenAPI.
- `edit-images-v2` supports `edit_with_text` and `edit_with_reference` for 1-16 images (depending on size); treat output as an edited image/composite unless a transparent layer is extracted and verified, or a changes-only editor layer is verified.
- `edit-animation-v2` and `transfer-outfit-v2` operate on 2-16 frames and return edited/composited frames, not equipment/body layers.
- Route MCP-managed characters through character/state/animation tools; use REST raw animation, edit-animation, interpolation, and outfit-transfer only when exact file-level control matters. Warn that text-only paperdolling drifts without a base frame, seed, or reference.
