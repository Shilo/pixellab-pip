# Paperdolling

Read this for layered characters, outfit variants, equipment swaps, or animation-consistent paperdoll workflows.

SKILL.md holds the global asset-integrity and no-baked-background rules; this file does not restate them. Paperdoll-specific allowance: local tools may compose, align, mask, resize, crop, diff, and extract changed pixels into transparent layer images, and verify them, but visible body/layer pixels must come from PixelLab or the user (no local drawing or repainting without an approved, labeled non-PixelLab fallback).

Treat paperdolling as a character-anchored edit workflow. Fitted hair, facial features, horns, wearables, armor, held gear, footwear, VFX, or similar body-region additions stay anchored to the base character image as edits on the base frame; do not route them as standalone objects unless the user explicitly wants a separate unattached prop.

Public REST v2/MCP docs do not expose editor-native layer objects or semantic equipment extraction. Pro Flash inpainting can return mask-scoped changes-only images (see Route Contract); this does not identify equipment or recover hidden parts. The Aseprite extension may also expose editor-local changes-only layer import; verify its exported pixels rather than treating it as a REST/MCP layer-creation contract.

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
| Fitted paperdoll edit from code/API | Prefer MCP `edit_image` on the base image (image URLs preferred; transport details in `image-input-roles.md`); fall back to REST `edit-images-v2` or base `edit-image` when its cheaper tier/extra controls matter. Treat the result as an edited composite first. | These edit routes output composites and do not expose `output_method`; the separate Pro Flash masked route below has its own output controls. |
| Separate transparent layer images plus final composite, without Aseprite | Per addition, create a same-canvas edited composite from the unchanged base with a prompt to add only that feature and preserve every other base pixel. Locally diff against the base, copy changed pixels into a transparent PNG, then compose base plus accepted layers into the final PNG. Deliver at least `base`, one transparent image per layer, and the final composite. | Image-file paperdolling, not editor-native layer creation. See verification checklist before calling any PNG a reusable layer. |
| Masked fitted layer attempt | Prefer the visible editor image-edit workflow with a body-region selection and changes-only layer output. For public API fallback, follow the exact-mask rule in `image-input-roles.md`. | Inpainting returns an edited image, not semantic layer extraction. Verified editor changes-only output is the better layer path. |
| Explicitly chosen Pro Flash masked changes-only output | Read `pro-flash.md`; use MCP `inpaint_image_pro_flash` or REST `inpaint-image-pro-flash` with `output_method="New layer with changes"`. Review the returned image directly over the unchanged base, without diff-extracting it as a composite. | Transparent outside the mask does not mean equipment-only inside it. This is an unbenchmarked opt-in, not a replacement for the default edit route or the existing exact-mask warning. |
| Standalone prop/accessory sprite | MCP object tools or REST object/image routes only when the user wants a separate reusable prop that need not fit the current body pose. | Do not use object generation for fitted hair, clothes, hats, eyes, or accessories on an existing character; it produces unregistered loose parts. |
| Dressed character preview/state | MCP `create_character_state`, REST character/edit routes, or editor image-edit with normal composite output. When the addition needs room beyond the source character's tight canvas (a weapon, wings), pass MCP `override_width`/`override_height` (REST `override_frame_size`) — multiples of 4, no smaller than the source, up to 256 — or it is clipped. | Output is a character variant/composite, not a separate reusable layer unless generated with a changes-only layer mode or extracted and verified from a same-canvas edit. |
| Outfit/equipment across animation frames | MCP `transfer_outfit` when visible, otherwise REST `transfer-outfit-v2`; use `edit-animation-v2` for arbitrary frame edits. | Preserve frame count/order; label output as composited animation frames. |
| Existing composite to isolated layer | Require an explicit mask or editor cleanup plan; follow `image-input-roles.md` before any public API fallback. | PixelLab does not document semantic layer extraction, character subtraction, or occluded-addition reconstruction. |
| Website Try on | Visible/manual website assistance only. | Returns one composited image and is experimental; not a layer pipeline. |

## Workflow

Both output modes share these steps and branch only at output:

1. Confirm the output shape with the user (above) before claiming layers.
2. Obtain the base character image/frame and keep it unchanged for every addition edit.
3. Run each requested layer as a separate existing-image edit against the original base (not the previous edited result), so layers stay independent. Prompt each edit as a single body-region addition using the Prompt Fields above.
4. Produce the layer per the chosen output mode:
   - **Separate transparent image files (no editor):** when PixelLab returns a composite, save it and extract a candidate overlay with the helper below. For an explicitly selected changes-only route, retain the returned candidate directly; do not run it through composite extraction. Keep its exact pixels; do not threshold away body drift, clip unrelated changes, recolour, or harden alpha to make extraction appear to pass. Any accepted cleanup is a separate derivative under `finishing.md`.
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
- For a layer extracted from a composite, alpha-compositing it over the unchanged base reproduces that composite. Erasure or reduced alpha over existing body pixels cannot be represented by simply copying the edited pixels into an ordinary overlay; reject that extraction instead of filling the gap or claiming a faithful layer. Direct API/editor changes-only candidates still need the other visual checks; compare a composite counterpart if already available, without generating another solely for this check.
- (Editor) unchanged frame count/order when relevant; no loose unregistered parts.

Do not call an extracted PNG or editor layer a reusable layer until it passes these. Reject and retry on a duplicated body, moved limbs, redraw, background change, or loose unregistered parts.

## Exact Pixel Extraction

The optional helper implements composite extraction and layer composition. From the generation's folder, replace `<skill-dir>` with the installed skill's absolute directory:

```bash
python "<skill-dir>/assets/paperdoll.py" extract base.png edit.png --out extracted
python "<skill-dir>/assets/paperdoll.py" compose base.png extracted/layer.png --out composed
```

`extract` accepts optional `--region LEFT TOP RIGHT BOTTOM`, with exclusive right/bottom edges; it rejects outside changes instead of clipping them. Pass one registered, same-canvas still-image pair at a time; it writes `layer.png` and `derivative.json` after exact visible alpha-over comparison passes. `compose` accepts one or more layer paths after the base, stacked in the supplied bottom-to-top order; it writes `composite.png` and a record. Both require a fresh destination. Dependency/skip handling and equivalent host tooling are covered by `local-asset-assembly.md`; apply the same extraction checks when using a host alternative.

Exit 0 means the operation ran; records remain `needs_visual_review`. Exit 1 means refusal or failure, not an accepted layer; exit 3 is the dependency skip described in `local-asset-assembly.md`. Exact recomposition does not distinguish equipment from a redrawn body: inspect every candidate against the checklist above. A state or separately generated animation may redraw the base even with the same named motion. Require pose-matched base/edited frames for each animation frame; do not assume paired template or Skeleton v3 jobs align. Splitting a composite by body overlap cannot recover an addition hidden behind the body; obtain the missing back layer separately or deliver a verified composite.

## Example Prompt (hair)

```text
Edit this south-facing 92x92 chibi humanoid creature sprite. Add only short spiky teal hair attached to the top/front of the head, following the head perspective and centered above the forehead. Keep every existing body, face, limb, outline, pose, canvas pixel, and transparent background unchanged except where the hair naturally covers the scalp. Do not redraw the character, do not move any body parts, do not add a second head, and do not create loose detached hair pieces.
```

Clothing, multi-part outfits, and hats follow the same pattern: one prompt listing each piece and its body region (cap on head with front brim, jacket over torso/arms, shorts at the waist, boots on both feet), matching the existing outline/shading/palette/camera, preserving all other base pixels and the exact canvas/background.

## API Facts

- MCP `inpaint_image` is the MCP-first equivalent of `inpaint-v3` (both Pro; both carry `crop_to_mask`), taking a preferred `image_url` or alternative `image_base64`, plus `description` and a rectangular mask or preferred `mask_image_url` / alternative `mask_image_base64`. REST `inpaint-v3` is documented as Pro (cost signal per SKILL.md Model And Mode Terms), requires `description`, `inpainting_image`, and `mask_image`; white mask areas are generated/replaced, black areas preserved. Output is a whole edited image, not a layer. `context_image` and `bounding_box` are deprecated in current OpenAPI.
- MCP `edit_image` is the MCP-first equivalent of `edit-images-v2` (Pro); prefer its URL inputs and follow `image-input-roles.md`. Treat output as an edited image/composite unless a transparent layer is extracted and verified, or a changes-only editor layer is verified.
- `edit-animation-v2` and `transfer-outfit-v2` operate on 2-16 frames and return edited/composited frames, not equipment/body layers.
- Route MCP-managed characters through character/state/animation tools; select the managed or raw animation engine via `animation.md` → Route Choice, with preferred URL or alternative inline frame inputs. Use MCP `transfer_outfit` when visible, otherwise REST `transfer-outfit-v2`; use REST `edit-animation-v2` or the selected REST raw animation route only when exact file-level control matters. Warn that text-only paperdolling drifts without a base frame, seed, or reference.
