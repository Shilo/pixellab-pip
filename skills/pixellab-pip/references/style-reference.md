# Style Reference Generation

Read this for MCP `create_image_pro` style-image input, REST `generate-with-style-v2`, website/Aseprite "Create image from style reference (pro)", or any request where a supplied image should define visual style, pixel size, palette, rendering, or sheet layout without preserving the exact subject identity.

## REST `generate-with-style-v2` Size Handling

For REST `POST /generate-with-style-v2`, do not send `image_size`. The current schema retains it only as an optional deprecated property marked as removed; it is not a supported output-size control. The endpoint always derives a square output from the supplied style images:

- Inspect all style images and use the largest dimension across them as the effective output size, bounded to `16`–`512` pixels.
- Non-square style images are centered on the square output canvas. Do not scale, stretch, crop, or redraw them to choose a different output size.
- If the desired asset occupies a non-square region inside the square output, state that usable region in the prompt and require the remaining area to stay transparent.
- If the user asks for an output size that differs from the style images, this endpoint cannot honor an independent size; preserve the supplied references and choose a route with an explicit size control, or ask for replacement references at the desired scale.

For website/Aseprite workflows, or a local preparation task that explicitly requires a square style image, pad a copy of each non-square reference to its native largest dimension with transparent pixels and keep the original pixels centered. This local preparation rule does not create a REST `image_size` field.

## Reference Count And Batch Size

Do not maximize the number of generated subjects by enlarging the canvas. For style fidelity, preserve the style reference's scale first.

For `generate-with-style-v2`, output count is tied to the deduced square size buckets in the public docs:

- `16-42`: 64 images
- `43-85`: 16 images
- `86-170`: 4 images
- `171-512`: 1 image

When the style reference's target size yields one image, generate one output asset, or one requested sheet/atlas, per request unless the user explicitly accepts a packed multi-asset atlas. A packed atlas competes with scale, layout, and style fidelity.

## Prompting

The prompt should preserve observed style facts from the reference without introducing conflicting generic style labels. Inspect the style image before writing the prompt and describe what is visible: subject proportions or form factor, pose/view when relevant, silhouette shape, bounds inside each cell or canvas region, palette, outline treatment, texture/material cues, and shading.

For sheet references, include exact structural facts: canvas footprint, cell size, row/column meaning, subject bounds inside each cell, perspective, and transparent padding.

Never add inferred style labels such as `chibi`, `super-deformed`, `RPG Maker`, `front-facing`, `large readable sprite`, or `panel` just because the image is small pixel art. Use those words only when the user says them or the reference visibly supports them. If the reference shows realistic or elongated proportions in a tiny sprite, say that instead.

State when the supplied image is only a style/layout reference and not a subject/identity reference. If the user says not to recreate the reference subject, include a concise negative subject constraint in `description`.

For managed 8-direction assets, MCP `create_character(mode="pro", style_character_id=...)` / REST `create-character-pro.style_character_id` and MCP `create_8_direction_object(style_object_id=...)` / REST `create-8-direction-object.style_object_id` can reuse an existing completed character or object as the style source. The requested output size must fit the visible reference sprite. Character style-ID mode is incompatible with `rotate_character`; object style-ID mode uses the styled object's south view as the center reference unless an explicit reference/style image overrides it.

## Verification

After generation, verify:

- REST output dimensions equal the square size deduced from the style images, not a separately requested `image_size`.
- Transparency was preserved in unused padded areas.
- Visible content remains at the reference-relative footprint and scale.
- For sheet outputs, rows, columns, and cell occupancy match the requested structure.
- Requested palette, outline, detail, and shading visibly match the reference; accepted options alone
  do not prove adherence.
- The generated subject does not copy a style-only reference subject when the user prohibited it.

## Hard projection or orientation requirements

When a view or facing direction is a hard requirement, preserve the user's subject and category.
Use the shortest useful description that names the requested subject and required view or
orientation; do not substitute a familiar category or add unrequested details.

If text-only output misses the requirement, use a neutral guide that visibly demonstrates the
required view, facing cue, and framing. With MCP, pass it as `style_image_url` or
`style_image_base64`; with REST, use `generate-image-v2` for a `style_image` or
`generate-with-style-v2` for `style_images`. A guide can preserve the structural cue while
pulling output toward its own geometry, so do not use a distinctive generated asset as a guide
when novel geometry matters.

Verify the hard requirement before judging style: requested subject/category; requested
view/orientation and its defining cues (for example, a building's front facade and entrance on the
requested side); one whole centered asset with expected size/transparency; no clear text or
watermark; and no unwanted copy of a style-only reference. Change route after a structural failure
instead of repeatedly adding prompt exclusions.

Keep guides role-specific when their visual cues could bias a different asset class. Do not reuse an
architecture-specific building guide for characters; use a character-appropriate guide when a
character's view or pose needs anchoring.
