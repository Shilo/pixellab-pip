# Style Reference Generation

Read this for `generate-with-style-v2`, website/Aseprite "Create image from style reference (pro)", or any request where a supplied image should define visual style, pixel size, palette, rendering, or sheet layout without preserving the exact subject identity.

## Aseprite-Equivalent Size Handling

When the user supplies style image(s) and does not explicitly request a different output size, derive the request size from the style reference rather than choosing a larger canvas for batching or convenience.

Prepare style-reference requests this way:
- Inspect all style images and find the largest referenced width and height.
- Set `target_size` to `max(largest_width, largest_height)`, clamped to the endpoint's allowed range.
- Use a square `image_size` of `target_size x target_size`.
- If a style image is non-square, pad it to `target_size x target_size` with transparent pixels and keep the original pixels centered. Do not scale, stretch, crop, or redraw the style image.
- If the desired asset occupies a non-square region inside the square canvas, state that usable region in the prompt and require the remaining area to stay transparent.
- Use a larger square only when the user asks for a larger output, the supplied references require it, or the requested content cannot fit at the reference-relative size and the user approves that tradeoff.

## Reference Count And Batch Size

Do not maximize the number of generated subjects by enlarging the canvas. For style fidelity, preserve the style reference's scale first.

For `generate-with-style-v2`, output count is tied to square size buckets in the public docs:

- `16-32`: 64 images
- `33-64`: 16 images
- `65-128`: 4 images
- `129-512`: 1 image

When the style reference's target size yields one image, generate one output asset, or one requested sheet/atlas, per request unless the user explicitly accepts a packed multi-asset atlas. A packed atlas competes with scale, layout, and style fidelity.

## Prompting

The prompt should preserve observed style facts from the reference without introducing conflicting generic style labels. Inspect the style image before writing the prompt and describe what is visible: subject proportions or form factor, pose/view when relevant, silhouette shape, bounds inside each cell or canvas region, palette, outline treatment, texture/material cues, and shading.

For sheet references, include exact structural facts: canvas footprint, cell size, row/column meaning, subject bounds inside each cell, perspective, and transparent padding.

Never add inferred style labels such as `chibi`, `super-deformed`, `RPG Maker`, `front-facing`, `large readable sprite`, or `panel` just because the image is small pixel art. Use those words only when the user says them or the reference visibly supports them. If the reference shows realistic or elongated proportions in a tiny sprite, say that instead.

State when the supplied image is only a style/layout reference and not a subject/identity reference. If the user says not to recreate the reference subject, include a concise negative subject constraint in `description`.

## Verification

After generation, verify:

- Output dimensions equal the square `image_size`.
- Transparency was preserved in unused padded areas.
- Visible content remains at the reference-relative footprint and scale.
- For sheet outputs, rows, columns, and cell occupancy match the requested structure.
- The generated subject does not copy a style-only reference subject when the user prohibited it.
