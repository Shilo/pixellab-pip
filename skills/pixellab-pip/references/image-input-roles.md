# Image Input Roles

Read this to classify image input roles when the user supplies attachments or file paths, or when an endpoint has `reference`, `style`, `concept`, `init`, `color`, mask, inpainting, or frame parameters.

Image input role is endpoint-specific. Do not map every supplied image to `reference_image`. Some inputs are references; others are edit targets, init/source images, masks, palettes, terrain style guides, or animation frame anchors. Classify the goal first, then pick the field.

When consistency matters, identify which input constrains identity, style, palette, source edit, or frames; if none is provided, note that results may vary across a batch.

When images are visible, inspect them and write task-relevant facts into the chosen natural-language parameter (`description`, `edit_description`, `action`, `style_description`), keeping observed facts separate from requested output changes.

For style-reference generation, also read `style-reference.md`.

## MCP Inline Image Transport

Large base64-only MCP inputs can be truncated by the client. When exact pixels matter and no URL field
exists, use the equivalent REST route; never silently shrink or quantize a user image.

## Goal Router

| User goal | Use this role | Meaning | Common fields/endpoints |
|---|---|---|---|
| "Use this as the subject" | Subject reference | The output should depict the same object, character, or subject, while text still guides details. | `reference_images` in MCP `create_image_pro` / REST `generate-image-v2` (up to 4 labelled entries on both — MCP entries accept a preferred `url` or inline base64 plus a `usage` note; REST uses an array with `usage_description`); `reference_image` in some character routes. |
| "Use this exact character" | Identity/character reference | Preserve the existing character identity and rotate, animate, or derive states from it. | MCP `create_character(mode="v3", reference_image_url=...)` (prefer the URL form — MCP clients truncate large inline base64) / REST `create-character-v3.reference_image`; `reference_image` with `method=rotate_character` in `create-character-pro` (REST-only — MCP `mode="pro"` rejects `reference_image_base64`); `directions` in 4/8-direction character routes (REST-only per-direction references — MCP `create_character` has only `n_directions`, no per-direction images). |
| "Turn this portrait into a character" | Portrait conversion input | The supplied bust/face portrait is the source image to convert into a full-body character sprite. | `image` in `portrait-character-pro` with `direction=portrait_to_character`; MCP `create_portrait_character` when visible. |
| "Make a portrait from this character" | Character conversion input | The supplied full-body character sprite is the source image to convert into a bust portrait. | `image` in `portrait-character-pro` with `direction=character_to_portrait`; MCP `create_portrait_character` when visible. |
| "Make this portrait talk" | Vocal portrait input | Generate mouth shapes from a portrait, either statelessly or stored on a managed character. | Raw portrait `portrait` in REST `vocal-animation` / `image` in MCP `create_vocal_animation`, or attach it first with `POST /characters/{id}/portrait` / `set_character_portrait`. |
| "Make it look like this" | Style reference | Copy visual style, pixel size, palette feel, rendering, or tile shape, not the exact subject identity. | MCP `create_image_pro.style_image_url` (preferred) or `style_image_base64`, plus `style_copy`; REST `generate-image-v2.style_image`+`style_options`; `style_images`; `reference_image` in `create-character-pro` style methods; managed `style_character_id` / `style_object_id` when a completed 8-direction asset should supply style and scale. |
| "Use this rough design" | Concept image | Use the image as a design idea or sketch; text can reinterpret it. | `concept_image` in `generate-ui-v2`; `concept_image` with `method=create_from_concept` in `create-character-pro`. |
| "Use this UI style" | UI style reference | Copy visual styling for a structured UI asset, not necessarily the layout. | `style_image` in `create-ui-asset`; if the user needs layout guidance instead, use `concept_image` in `generate-ui-v2` or shape `pieces`/`elements` in `create-ui-asset`. |
| "Start from this and transform it" | Init/source image | The supplied image is the starting state to modify, not merely inspiration. | MCP `create_image_pixflux.init_image_url` (preferred) or `init_image_base64`, plus `init_image_strength`; REST `init_image` in `create-image-pixflux`; REST-only `init_image` in BitForge and map-object routes (MCP `create_map_object` uses `background_image`+`inpainting` instead, not an init image). |
| "Edit/convert this image" | Target image | This is the image being edited, converted, resized, pixelated, or inpainted. | `image` in `edit-image`, `image-to-pixelart`, `image-to-pixelart-pro`; `edit_images` in `edit-images-v2`; `inpainting_image` for BitForge/inpaint targets; pair with `mask_image` only when the user supplies an edit-area mask. MCP prefers `image_urls` / `reference_image_url` in `edit_image` and `image_url` / `mask_image_url` in `inpaint_image`; the corresponding base64 fields remain alternatives. |
| "Add an effect/trail/aura to this sprite" | Target image | The supplied image is the canvas to preserve and augment. Add the requested VFX to the existing sprite/image rather than generating a separate object, unless the user explicitly asks for a reusable layer or isolated effect asset. | `image` in `edit-image`; `edit_images` in `edit-images-v2` for multi-image edits; MCP `edit_image.image_urls` (preferred) or `images_base64`. |
| "Match these colors" | Palette reference | Extract or force colors from the supplied image/palette, not its subject. | `color_image`, `color_palette`; MCP `create_image_pixflux.color_image_url` (preferred) or `color_image_base64`. |
| "Animate from/to these frames" | Frame reference | The image is an animation boundary or motion anchor. | `first_frame`, `last_frame`, character south frame for animation prompt enhancement. MCP prefers `first_frame_url`/`last_frame_url`; inline base64 remains available. |
| "Match this terrain/tile" | Terrain/tile style reference | Copy style/material/shape for a terrain layer, transition, or tile variant. | `style_images` in MCP `create_tiles_pro` / REST `create-tiles-pro` (also `style_images` on `create_1_direction_object`, `style_image_base64` on `create_8_direction_object`); `lower_reference_image`, `upper_reference_image`, `transition_reference_image` are REST-only tileset fields — MCP tileset tools take only `lower_base_tile_id`/`upper_base_tile_id`. |

## Endpoint Semantics

These are REST v2 routes; MCP `edit_image`/`inpaint_image`/`animate_image` cover the same edit/inpaint/animate roles directly (fields noted above) and need no managed asset — do not route supplied-image edits to *managed* MCP tools (`create_*_state`) just because MCP is configured; those regenerate a managed asset, not an in-place edit. Only counter-intuitive or collision-prone fields are listed; where the field name plainly matches the role (`remove-background.image` = target, `resize.reference_image` = image to resize, `edit-image.image` = edit target), take it at face value.

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

Exact-mask edits: avoid MCP `inpaint_image` and REST `inpaint-v3` until fixed; live tests changed
pixels outside the mask or ignored the masked region. For other inpainting, verify both regions and
report failures without retrying or repairing silently.

## Clarify When Ambiguous

Infer roles from explicit wording for low-risk setup. Before a credit-spending call, ask one short question when a file could serve more than one role and the choice would change the endpoint, field, or output — never guess between identity, style, concept, edit target, mask, palette, and frame:

- "Should this image define the exact subject/character, only the style, or just the color palette?"
- "Is this the image to edit, or a reference for what the edit should look like?"
- "For this character image, should PixelLab rotate this exact character, use it as a style guide, or treat it as concept art?"
- "For this UI image, should it guide the layout/concept, visual style, or only the color palette?"
- "For animation, is this the first frame, last frame, or a style/reference image?"
