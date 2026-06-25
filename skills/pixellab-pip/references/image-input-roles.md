# Image Input Roles

Read this to classify image input roles when the user supplies attachments or file paths, or when an endpoint has `reference`, `style`, `concept`, `init`, `color`, `character`, mask, inpainting, or frame image parameters.

Image input role is endpoint-specific. Do not map every supplied image to `reference_image`. Some PixelLab image inputs are references, but others are edit targets, init/source images, masks, palettes, terrain style guides, or animation frame anchors. Classify the user's goal first, then pick the endpoint field.

When consistency matters, identify which input constrains identity, style, palette, source edit, or animation frames. If no anchor is provided, note that results may vary across a batch.

When images are visible to the agent, inspect them and write task-relevant facts into the selected natural-language parameter, such as `description`, `edit_description`, `action`, `action_description`, or `style_description`: subject, direction/view, pose, palette, style, materials, edit target, and intended output. Keep observed input facts separate from requested output changes. If the user says not to enhance, preserve their wording except for required endpoint formatting.

## Goal Router

| User goal | Use this role | Meaning | Common fields/endpoints |
|---|---|---|---|
| "Use this as the subject" | Subject reference | The output should depict the same object, character, or subject, while text still guides details. | `reference_images` in `generate-image-v2`; `reference_image` in some character routes. |
| "Use this exact character" | Identity/character reference | Preserve the existing character identity and rotate, animate, or derive states from it. | `reference_image` in `create-character-v3`; `reference_image` with `method=rotate_character` in `create-character-pro`; `directions` in 4/8-direction character routes. |
| "Make it look like this" | Style reference | Copy visual style, pixel size, palette feel, rendering, or tile shape, not the exact subject identity. | `style_image`, `style_images`, `reference_image` in `create-character-pro` style methods. |
| "Use this rough design" | Concept image | Use the image as a design idea or sketch; text can reinterpret it. | `concept_image` in `generate-ui-v2`; `concept_image` with `method=create_from_concept` in `create-character-pro`. |
| "Start from this and transform it" | Init/source image | The supplied image is the starting state to modify, not merely inspiration. | `init_image` in PixFlux, BitForge, and map object routes. |
| "Edit/convert this image" | Target image | This is the image being edited, converted, resized, pixelated, or inpainted. | `image` in `edit-image`, `image-to-pixelart`, `image-to-pixelart-pro`; `edit_images` in `edit-images-v2`; `inpainting_image` for BitForge/inpaint targets; pair with `mask_image` only when the user supplies an edit-area mask. |
| "Add an effect/trail/aura to this sprite" | Target image | The supplied image is the canvas to preserve and augment. Add the requested VFX to the existing sprite/image rather than generating a separate object, unless the user explicitly asks for a reusable layer or isolated effect asset. | `image` in `edit-image`; `edit_images` in `edit-images-v2` for multi-image edits. |
| "Match these colors" | Palette reference | Extract or force colors from the supplied image/palette, not its subject. | `color_image`, `color_palette`. |
| "Animate from/to these frames" | Frame reference | The image is an animation boundary or motion anchor. | `first_frame`, `last_frame`, character south frame for animation prompt enhancement. |
| "Match this terrain/tile" | Terrain/tile style reference | Copy style/material/shape for a terrain layer, transition, or tile variant. | `lower_reference_image`, `upper_reference_image`, `transition_reference_image`, `style_images` in `create-tiles-pro`. |

## Endpoint Semantics

These image-editing and image-conversion routes are REST v2 routes unless current MCP docs or visible MCP tools expose a matching image-edit tool. Do not route supplied-image edits to managed MCP object/character tools just because MCP is configured.

- `generate-image-v2`
  - `reference_images`: subject guidance, up to 4 images.
  - `style_image`: style and pixel-size reference.
  - `style_options`: what to copy from the style image.
- `generate-with-style-v2`
  - `style_images`: 1-4 style reference images.
  - Use when style matching is the point, not subject preservation.
- `create-image-pixflux`
  - `init_image`: initial image to start from.
  - `color_image`: forced palette image.
- `create-image-bitforge`
  - `init_image`: starting image.
  - `style_image`: style transfer reference.
  - `inpainting_image`: image being inpainted.
  - `mask_image`: black/white mask where white marks the edit area.
  - `color_image`: forced palette image.
- `generate-ui-v2`
  - `concept_image`: optional UI design/layout guide.
  - `color_palette`: text color palette guidance.
  - If the user asks to use an image as UI "style", clarify whether it should guide layout/concept or only palette, because no generic UI `style_image` field was documented.
- `create-character-v3`
  - `reference_image`: south-facing character image to rotate into 8 directions. If omitted, PixelLab first generates from text.
  - `outline` and `detail` are ignored when `reference_image` is provided.
- `create-character-pro`
  - `method=create_with_style`: `reference_image` is a style reference.
  - `method=create_from_concept`: `concept_image` seeds the design; `reference_image` adds style guidance.
  - `method=rotate_character`: `reference_image` is the existing character to rotate.
- 4/8-direction character routes
  - `directions`: direction-specific reference images. Provided directions are used as-is; missing directions are generated.
  - Bipedal templates require south if any are provided. Quadrupeds require south and east.
- `create-tileset`
  - `lower_reference_image`, `upper_reference_image`, `transition_reference_image`: style references for terrain layers/transition.
  - `color_image`: palette reference.
- `create-tiles-pro`
  - `style_images`: reference tiles. When provided, style tiles define style and dimensions; tile shape/size/view inputs are ignored.
- `edit-image`
  - `image`: target image to edit.
  - `color_image`: style/color guide.
  - Use for additive sprite effects such as motion streaks, slashes, dust, aura, impact arcs, and wind trails when the user supplies the sprite to modify.
  - Output is a whole edited image. If the user needs an isolated reusable effect layer, ask before choosing separate object/image generation or post-processing extraction.
- `edit-images-v2`
  - `edit_images`: targets to edit.
  - `method`: `edit_with_text` or `edit_with_reference`.
  - `reference_image`: required only for `method=edit_with_reference`.
  - No mask input or layer output was documented.
- `image-to-pixelart` / `image-to-pixelart-pro`
  - `image`: target image to convert, not a style reference.
  - Treat "same size", "exact size", "exact resolution", and similar wording as a fixed output-size request; inspect the input image dimensions when the size is implied.
  - If no fixed output size is requested, prefer `image-to-pixelart-pro`.
  - If fixed output size is requested and fits current `image-to-pixelart` `output_size` limits, use normal `image-to-pixelart`.
  - If requested size is outside current `output_size` limits, warn that Pro cannot guarantee exact dimensions before spending credits. If the user proceeds, use Pro, verify dimensions, then ask before PixelLab `resize` or local nearest-neighbor/canvas resize/pad/crop.
- `resize`
  - `image`: target image to resize.
  - Use for PixelLab resizing only after checking current size limits and output behavior. For simple nearest-neighbor canvas padding/cropping, local tooling may be safer after user approval.
- `remove-background`
  - `image`: target image whose background should be removed.
  - Use for transparent-background extraction when the user wants PixelLab's public REST route, not MCP.
- `animate-with-text-v3`
  - `first_frame`: required starting frame.
  - `last_frame`: optional ending frame for interpolation/guidance.
- `inpaint-v3`
  - `inpainting_image`: target image to edit.
  - `mask_image`: white marks pixels to generate/replace; black preserves pixels.
  - `context_image` and `bounding_box` are deprecated in current OpenAPI.
  - Output is a whole edited image, not an isolated layer.
- `map-objects`
  - `init_image`: starting image to transform.
  - `background_image`: background/map image for style matching when using inpainting.
  - `color_image`: forced palette image.

## Clarify When Ambiguous

Ask one short question when the same file could be more than one role:

- "Should this image define the exact subject/character, only the style, or just the color palette?"
- "Is this the image to edit, or a reference for what the edit should look like?"
- "For this character image, should PixelLab rotate this exact character, use it as a style guide, or treat it as concept art?"
- "For animation, is this the first frame, last frame, or a style/reference image?"

Never guess between identity, style, concept, edit target, palette, and frame roles when credit-spending generation depends on it.
