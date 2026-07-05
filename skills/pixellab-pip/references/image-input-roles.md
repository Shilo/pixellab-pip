# Image Input Roles

Read this to classify image input roles when the user supplies attachments or file paths, or when an endpoint has `reference`, `style`, `concept`, `init`, `color`, mask, inpainting, or frame parameters.

Image input role is endpoint-specific. Do not map every supplied image to `reference_image`. Some inputs are references; others are edit targets, init/source images, masks, palettes, terrain style guides, or animation frame anchors. Classify the goal first, then pick the field.

When consistency matters, identify which input constrains identity, style, palette, source edit, or frames; if none is provided, note that results may vary across a batch.

When images are visible, inspect them and write task-relevant facts (subject, direction/view, pose, palette, style, materials, edit target) into the chosen natural-language parameter (`description`, `edit_description`, `action`, `style_description`), keeping observed facts separate from requested output changes.

## Goal Router

| User goal | Use this role | Meaning | Common fields/endpoints |
|---|---|---|---|
| "Use this as the subject" | Subject reference | The output should depict the same object, character, or subject, while text still guides details. | `reference_images` in `generate-image-v2`; `reference_image` in some character routes. |
| "Use this exact character" | Identity/character reference | Preserve the existing character identity and rotate, animate, or derive states from it. | `reference_image` in `create-character-v3`; `reference_image` with `method=rotate_character` in `create-character-pro`; `directions` in 4/8-direction character routes. |
| "Turn this portrait into a character" | Portrait conversion input | The supplied bust/face portrait is the source image to convert into a full-body character sprite. | `image` in `portrait-character-pro` with `direction=portrait_to_character`; MCP `create_portrait_character` when visible. |
| "Make a portrait from this character" | Character conversion input | The supplied full-body character sprite is the source image to convert into a bust portrait. | `image` in `portrait-character-pro` with `direction=character_to_portrait`; MCP `create_portrait_character` when visible. |
| "Make it look like this" | Style reference | Copy visual style, pixel size, palette feel, rendering, or tile shape, not the exact subject identity. | `style_image`, `style_images`, `reference_image` in `create-character-pro` style methods. |
| "Use this rough design" | Concept image | Use the image as a design idea or sketch; text can reinterpret it. | `concept_image` in `generate-ui-v2`; `concept_image` with `method=create_from_concept` in `create-character-pro`. |
| "Use this UI style" | UI style reference | Copy visual styling for a structured UI asset, not necessarily the layout. | `style_image` in `create-ui-asset`; if the user needs layout guidance instead, use `concept_image` in `generate-ui-v2` or shape `pieces`/`elements` in `create-ui-asset`. |
| "Start from this and transform it" | Init/source image | The supplied image is the starting state to modify, not merely inspiration. | `init_image` in PixFlux, BitForge, and map object routes. |
| "Edit/convert this image" | Target image | This is the image being edited, converted, resized, pixelated, or inpainted. | `image` in `edit-image`, `image-to-pixelart`, `image-to-pixelart-pro`; `edit_images` in `edit-images-v2`; `inpainting_image` for BitForge/inpaint targets; pair with `mask_image` only when the user supplies an edit-area mask. |
| "Add an effect/trail/aura to this sprite" | Target image | The supplied image is the canvas to preserve and augment. Add the requested VFX to the existing sprite/image rather than generating a separate object, unless the user explicitly asks for a reusable layer or isolated effect asset. | `image` in `edit-image`; `edit_images` in `edit-images-v2` for multi-image edits. |
| "Match these colors" | Palette reference | Extract or force colors from the supplied image/palette, not its subject. | `color_image`, `color_palette`. |
| "Animate from/to these frames" | Frame reference | The image is an animation boundary or motion anchor. | `first_frame`, `last_frame`, character south frame for animation prompt enhancement. |
| "Match this terrain/tile" | Terrain/tile style reference | Copy style/material/shape for a terrain layer, transition, or tile variant. | `lower_reference_image`, `upper_reference_image`, `transition_reference_image`, `style_images` in `create-tiles-pro`. |

## Endpoint Semantics

These are REST v2 routes unless current MCP docs or visible MCP tools expose a matching image-edit tool; do not route supplied-image edits to managed MCP tools just because MCP is configured. Only counter-intuitive or collision-prone fields are listed; where the field name plainly matches the role (`remove-background.image` = target, `resize.reference_image` = image to resize, `edit-image.image` = edit target), take it at face value.

- `create-character-v3`
  - `reference_image`: south-facing character to rotate into 8 directions (else generates from text); `outline` and `detail` are ignored when it is set.
- `create-character-pro` (image role depends on `method`)
  - `method=create_with_style`: `reference_image` is a style reference.
  - `method=create_from_concept`: `concept_image` seeds the design; `reference_image` adds style guidance.
  - `method=rotate_character`: `reference_image` is the existing character to rotate.
- 4/8-direction character routes
  - `directions`: per-direction reference images (provided used as-is, missing generated); bipedal templates require south if any are provided, quadrupeds require south and east.
- `portrait-character-pro`
  - `image` is the source to convert, not a style reference.
  - `direction=portrait_to_character`: source must be a bust portrait; output is a full-body sprite. Use `view` and `result_size` to control the sprite.
  - `direction=character_to_portrait`: source must be a full-body sprite; output is a bust portrait.
- `create-tiles-pro`
  - `style_images`: reference tiles. When provided, style tiles define style and dimensions; tile shape/size/view inputs are ignored.
- `edit-images-v2`
  - `edit_images`: targets to edit.
  - `reference_image`: used only with `method=edit_with_reference`, never with `method=edit_with_text`. No mask input or layer output is documented.
- `image-to-pixelart` / `image-to-pixelart-pro`
  - `image`: target to convert, not a style reference.
  - Treat "same size", "exact size", "exact resolution", and similar as a fixed output-size request; inspect the input dimensions when the size is implied.
  - No fixed size requested: prefer `image-to-pixelart-pro`. Fixed size within `image-to-pixelart` `output_size` limits: use normal `image-to-pixelart`.
  - Fixed size outside those limits: warn that Pro cannot guarantee exact dimensions before spending credits; if the user proceeds, use Pro, verify dimensions, then ask before PixelLab `resize` or local resize/pad/crop.

For animation frame anchors (`first_frame`, `last_frame`) and idle-loop risk, see `animation.md`.

## Clarify When Ambiguous

Infer roles from explicit wording for low-risk setup. Before a credit-spending call, ask one short question when a file could serve more than one role and the choice would change the endpoint, field, or output — never guess between identity, style, concept, edit target, mask, palette, and frame:

- "Should this image define the exact subject/character, only the style, or just the color palette?"
- "Is this the image to edit, or a reference for what the edit should look like?"
- "For this character image, should PixelLab rotate this exact character, use it as a style guide, or treat it as concept art?"
- "For this UI image, should it guide the layout/concept, visual style, or only the color palette?"
- "For animation, is this the first frame, last frame, or a style/reference image?"
