# Style Reference Generation

Read this for `generate-with-style-v2`, website/Aseprite "Create image from style reference (pro)", or any request where a supplied image should define visual style, pixel size, palette, rendering, or sheet layout without preserving the exact subject identity.

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

## Hard top-down building projection

For a traditional screen-aligned south-facing building, use a neutral reference that visibly
demonstrates the projection, bottom/south front facade, and entrance. A locally authored generic
guide is an acceptable generation control when it is kept separate from final art. Do not use a
previously generated specific house as the style reference when the next request requires novel
geometry; the tested route preserved projection but converged on the reference-specific
architecture.

In the current controlled building test, the neutral reference held the projection even when
style_description was omitted. Start with the shortest useful description:

    a new traditional 2D town-house sprite with a south-facing entrance and different geometry.

Keep the structural review gate. This finding is specific to the tested building route and model
state; it does not make text-only Pixen/PixFlux generation reliable. Reliability is currently
bounded to town-house-like forms: shop and inn wording caused depth or signage failures in the
repeat suite even with explicit front-facade language, so use a category-specific test before
generalizing the route.

For this building route, reject any candidate that fails a hard gate: shallow screen-aligned
top-down projection; front facade and entrance on the south/bottom edge; one whole centered
building with the expected size, transparency, and no clear text or watermark; and, when new
geometry is requested, no distinctive copy of the style reference. Change route after a projection
failure instead of repeatedly adding prompt exclusions.

This control is building-specific. Do not reuse it for characters or create a combined
building/character guide: roof, front-facade, and entrance cues encode architecture and can bias
character silhouette or pose. Keep a character-specific reference separate, and create one only
when character testing demonstrates a need.
