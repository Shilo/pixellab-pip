# Pro Flash

Read this for an explicit PixelLab Pro Flash request or when comparing it with another PixelLab route. Pro Flash is a separate beta family, not `create_image_pro`, `create_character(mode="pro")`, `edit_image`, or `inpaint_image`. REST describes its image-to-pixel-art operation as the same conversion as older Pro at lower cost and higher speed, but visual quality has not been independently tested. Other operations are operation-specific; do not assume the family is faster or better, or replace a benchmark-backed default based on its name alone.

| Goal | MCP when visible | REST v2 |
|---|---|---|
| One image | `create_image_pro_flash` | `POST /create-image-pro-flash` |
| Eight-direction character | `create_character_pro_flash` | `POST /create-character-pro-flash` |
| One- or eight-direction object | `create_object_pro_flash` | `POST /create-object-pro-flash` |
| One-image edit | `edit_image_pro_flash` | `POST /edit-image-pro-flash` |
| Masked edit | `inpaint_image_pro_flash` | `POST /inpaint-image-pro-flash` |
| Image to pixel art | `image_to_pixelart_pro_flash` | `POST /image-to-pixelart-pro-flash` |

For image-to-pixel-art Pro Flash, MCP accepts image URL/base64 or an owned source-image ID; REST requires encoded `image` and constrains optional `description` to 1–2000 characters. The MCP docs list `description` as `Optional[str]` without a length bound. Both document `seed` defaulting to 0, and `project_id` may be supplied. It costs 6 generations per image, detects native pixel scale/output size, has no output-size choice or cost-estimator operation, scales inputs down when the longest side exceeds 2048px, and saves completed output to the gallery as `source_image_id`. The result has not been quality-tested here.

Before planning a paid creation/edit call, check `get_pro_flash_capabilities(operation=..., width=..., height=..., n_directions=...)` (MCP) for supported native dimensions and a free operation-specific price split; REST has `GET /pro-flash/capabilities` and the separate provisional `GET /pro-flash/cost?operation=...&width=...&height=...&n_directions=...`. The current MCP guide documents this per-image ladder for creation, edit, and inpaint:

| Longest canvas side | Generations |
|---|---|
| Up to 96px | 5 |
| 100–208px | 6 |
| 212–256px | 9 |

For edit/inpaint, price the source canvas, not the mask. Character and eight-direction object creation add a separately billed rotation stage: total 6 at 48px, 17 at 256px (9 image + 8 rotations). Intermediate rotation steps are uneven; request the exact split rather than interpolating. A one-direction object costs only the image stage. Wait for a source-image job to complete before reuse; an owned `source_image_id` or supplied first frame avoids the image charge, but eight rotations still cost 1 at 48px or 8 at 256px. One-direction reuse is free.

REST OpenAPI still describes a provisional five-generation first image, and the older release notes advertised 4–6; neither is a safe ceiling for the MCP ladder. Quotes are provisional and no parameter caps the charge. Include both stages when applicable in approval and report completed-job usage. Keep these creation/edit prices separate from the converter's fixed six-generation price.

Creation supports preset native sizes `16x16` (experimental), `24x24`, `32x32`, `32x48`, `48x48`, `64x64`, `96x64`, `96x96`, and `128x128`; REST also documents custom 16–256-pixel dimensions in multiples of four as Beta. MCP image creation defaults to `64x64`, while REST requires `image_size`; text creation for characters/objects defaults to `64x64`. `create_image_pro_flash` makes exactly **one** image, unlike size-dependent Create Image Pro batches. It defaults to `no_background=true`, so explicitly set false for an opaque scene. A style image must fit without rescaling; use `style_options` only when the requested traits justify them.

Character Pro Flash always makes eight views; object Pro Flash supports one or eight. The first direction is `south`. For a chosen south-facing image, pass its owned `source_image_id` or a first-frame image, not both. MCP additionally accepts first-frame URLs; REST uses encoded `first_frame`. The MCP page's `n_directions` hint mentions 4 directions, but the parameter accepts only 8. For a text-only animal, pass the matching `template_id` (`bear`, `cat`, `dog`, `horse`, `lion`); MCP documents 6 generations at 64px.

Pro Flash edit keeps the source canvas size. REST takes one encoded `image`; MCP also offers `image_url` or an owned `source_image_id`. Reference-mode editing needs a reference that fits the source canvas. Set `no_background` explicitly when transparency matters: REST defaults it to `false`, while the MCP edit/inpaint signatures leave it unset. Inpaint requires the source and mask at the same supported native size: pure white RGB means regenerate, pure black RGB means preserve, regardless of mask alpha; an empty mask is rejected. MCP accepts a rectangle or mask image and has URL alternatives; REST requires `mask_image`. `context_image` requires its `bounding_box`. Select `output_method` deliberately: changes-only results are transparent outside the mask, while `Modify current layer` returns the composite. PixelLab claims unchanged pixels outside the mask for this route, but that claim is not live-verified here; inspect both regions before calling a strict-mask result final, and do not silently repair or retry a failure.

The Pro Flash image-creation schema says its `seed` is recorded but the provider does not promise deterministic output. Keep the user's seed if given; never promise identical reruns. Poll REST's returned `background_job_id` with `GET /background-jobs/{job_id}`. For MCP image jobs use the returned job ID with the available raw-image getter; for managed character/object results use `get_character`/`get_object`. Verify the downloaded image rather than treating a queued ID as completion.
