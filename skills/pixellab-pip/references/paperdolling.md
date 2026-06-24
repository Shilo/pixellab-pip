# Paperdolling

Read this for layered characters, outfit variants, equipment swaps, or animation-consistent paperdoll workflows.

Treat paperdolling as a composition workflow outside PixelLab, not a separate PixelLab feature. Use a layer-first workflow by default.

PixelLab can generate base sprites, edited states, outfit-transfer frames, masked inpaints, and standalone transparent objects. Public REST v2/MCP docs do not expose first-class layer creation, layer assignment, semantic layer extraction, or isolated changed-part outputs.

Ask or infer:

- Base character identity.
- Direction count.
- Sprite and canvas size.
- Animation list.
- Layers such as body, hair, outfit, armor, weapon, accessory, shadow, and VFX.
- Whether outputs must be isolated transparent layers or composited previews.
- Whether an existing composite may be edited lossily, or whether reusable isolated layers are required.

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
| Isolated equipment/object layer | Generate the item as an object first: MCP object tools or REST object/image routes. Use the character only as style/scale/reference. | Do not create the item on a character and subtract the character unless the user accepts lossy cleanup. |
| Dressed character preview/state | MCP `create_character_state` or REST character/edit routes. | Output is a character variant/composite, not a separate reusable layer. |
| Outfit/equipment across animation frames | REST `transfer-outfit-v2` or `edit-animation-v2`; MCP character animation only when working with managed character assets. | Preserve frame count/order and label output as composited animation frames. |
| Existing composite to isolated layer | Require an explicit mask or editor cleanup plan; use REST inpaint/edit only as a fallback. | PixelLab does not document semantic layer extraction, character subtraction, or occluded item reconstruction. |
| Website Try on | Use only as visible/manual website assistance when appropriate. | It returns one composited image and is experimental; it is not a layer pipeline. |

`inpaint-v3` requires `description`, `inpainting_image`, and `mask_image`; white mask areas are generated/replaced and black areas are preserved. Treat its output as a whole edited image, not a layer. `context_image` and `bounding_box` are deprecated in current OpenAPI.

`edit-images-v2` supports `edit_with_text` and `edit_with_reference` for 1-16 images depending on size. It can help keep related edits consistent, but it has no mask input and no layer or isolated-delta output.

`edit-animation-v2` and `transfer-outfit-v2` operate on 2-16 frames and return edited/composited frames, not equipment/body layers.

If layer fidelity matters, create and save each layer separately before compositing in Aseprite, Pixelorama, or local tooling.

Route MCP-managed characters through character/state/animation tools. Use REST v2 raw animation, edit-animation, interpolation, and outfit-transfer routes only when exact file-level control matters. Warn that text-only paperdolling drifts without a base frame, seed, or reference.
