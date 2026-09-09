# PixelLab Tibia High-Oblique Item Perspective MVP Research Spike

Last reviewed: 2026-09-08.

Purpose: document the controlled PixelLab experiments used to generate 32x32
transparent treasure-chest inventory sprites in a steep, side-turned Tibia-style
perspective, and preserve the shortest reusable request that produced the most
consistent result.

## Executive finding

For a new material or trim variant, the most reliable route found was MCP
`create_image_pro` with:

- one accepted 32x32 sprite that already has the desired camera supplied as
  `style_image_base64`;
- two additional native-size square style references supplied in
  `reference_images`;
- `width: 32`, `height: 32`, `no_background: true`;
- `style_copy: ["color_palette", "outline", "detail", "shading"]`;
- a short prompt that describes the plane relationship positively and excludes
  the common top-down and isometric substitutions.

The final Pro round produced the best new designs. Its selected wooden, iron-bound,
and ornate outputs are preserved in the [chronological R9 run folder (archive suffix r8)](../../pixellab-pip-generations/treasure-chests-tibia-pro-style-lock-r8-20260908/)
and its request history is in the [chronological R9 blueprint](../../pixellab-pip-generations/treasure-chests-tibia-pro-style-lock-r8-20260908/treasure-chests-tibia-pro-style-lock-r8-20260908.blueprint.json).

This is an empirical routing result, not a claim that PixelLab exposes a
mathematically named Tibia camera. In this spike, “Tibia perspective” means a
very high-oblique inventory view with a dominant near-facing plane and a narrow
side plane receding down-right.

## Target and acceptance rule

The target was one centered treasure chest on an exact 32x32 transparent canvas.
The required camera cues were:

- the near-facing plane is tall and visually dominant;
- the side plane is narrow, deep, and recedes down-right;
- only a thin lid edge is visible;
- the latch is placed on the near-facing plane;
- the image reads as a side-turned inventory sprite rather than a roof or box
  viewed from above.

Reject an output when it is top-down, bird's-eye, roof-dominant, conventional
three-quarter, isometric, front-only, ground-based, shadowed, or otherwise loses
the near-plane/side-plane relationship. Dimensions and transparency are
necessary but are not enough to pass the camera test.

All returned alternatives were retained and reviewed. The final R9 review found
64/64 exact alpha-mask matches to the R6 wooden anchor, 27/64 exact matches for
the iron group, and no exact mask matches for the ornate group. The ornate group
still contained visually clear high-oblique results; the selected frame was the
strongest visual match rather than a mask-identical copy. Every R9 output was
32x32 RGBA with no partial alpha.

## Controlled attempt history

Run labels in this table are chronological (R1 through R9); an archive folder's
working suffix can differ from its chronological run number.

Each paid batch had a blueprint and review record. The shared ledger reserved
480 of the 1,000 Generation Unit cap; no new paid generation was made while
writing this spike.

| Run | Route and reference strategy | Returned output | Finding and decision |
| --- | --- | ---: | --- |
| R1 | Pro with one supplied style image per material and three distinct MVP prompts | 192 alternatives | Mixed top-down, conventional three-quarter, and side variations. Text alone did not stabilize the camera. Rejected. |
| R2 | Pro with multiple labeled references and prompts centered on front dominance, thin lid, or latch placement | 192 alternatives | Labels and role descriptions did not reliably impose the projection. Rejected. |
| R3 | Pro with all supplied styles plus a rotating brown/silver style anchor | 192 alternatives | More style context improved palette direction but not the camera. Rejected. |
| R4 | Pro with a neutral high-oblique geometry guide, all supplied styles, and a rotating direct style anchor | 192 alternatives | The guide was ignored or converted into generic box geometry. Rejected. |
| R5 | Pro with a packed style strip and a neutral guide | 192 alternatives | Native-scale context was useful for palette and pixel language, but the camera remained unstable. Rejected. |
| R6 | `edit_image` with one geometry-preserving source and a separate appearance reference for each material | 3 edited sprites | Exact geometry lock: all three alpha masks matched their source. Best route when preserving the camera is more important than generating new geometry. |
| R7 | Pro with the R6 outputs as style anchors, all three original styles, and longer locked-camera wording | 192 alternatives | The near plane improved, but many outputs still showed a broad roof/top face. Rejected as a dependable Pro recipe. |
| R8 | Pro with a labeled camera anchor in `reference_images`, the R6 wooden anchor, and all original styles | 192 alternatives | Descriptive reference roles did not act as a hard geometric lock. Conventional three-quarter outputs remained. Rejected. |
| R9 | Pro with a material-specific R6 anchor in `style_image_base64`, two native 32x32 style references, and the concise style-lock prompt | 192 alternatives | Best new-generation round. Wooden, iron-bound, and ornate selections all visibly retained the steep side-turned camera. Recommended. |

The complete chronological ledger is the [perspective history](../../pixellab-pip-generations/treasure-chests-tibia-perspective-history-20260908.md).
The budget record is the [1,000-unit budget ledger](../../pixellab-pip-generations/treasure-chests-tibia-perspective-budget-20260908.json).

## Findings

### 1. An accepted image is a stronger camera anchor than a label

The decisive change in R9 was using a previously accepted, material-specific
sprite as the direct `style_image_base64` image. That image already contained
the desired relationship between the near plane, thin lid edge, latch, and
receding side plane. The two additional style references supplied palette,
outline, shading, and native pixel-language context.

The experiments indicate that `reference_images` with descriptive `usage`
strings are useful contextual references but should not be treated as a hard
projection lock. A reference labeled “high-oblique geometry” can still be
interpreted as a generic box or a familiar three-quarter object.

### 2. Style-image and reference-image roles are different

Use `style_image_base64` when the supplied image should carry the composition
and camera as well as the visual language. Use `reference_images` for additional
style context, palette, detail, outline, or material cues. When a style-only
reference must not donate its subject geometry, do not promote it to the
style-image role.

R7 is an important boundary case: it also used R6 outputs as style images but
paired them with more references and longer wording. It improved some outputs
without making the camera dependable. R9's result should therefore be
reproduced as a complete recipe—accepted anchor, two square references, compact
structural wording, and material-specific design focus—not as a claim that one
field alone guarantees success.

### 3. Edit mode is the geometry-lock route

R6 used `edit_image` with the desired geometry as the source and a separate
appearance reference. The source silhouette and alpha mask were preserved
exactly for all three edited sprites. This is the correct fallback when a
precise camera must survive unchanged.

Edit mode has a different product goal from Pro generation: it is a reliable
way to redesign appearance around existing geometry, not the preferred way to
invent a novel chest silhouette. For new geometry, use the R9 Pro recipe and
review every returned alternative.

### 4. Short positive plane language outperformed prompt accumulation

The useful camera description is structural and compact:

> a dominant tall near-facing plane, a narrow deep side plane receding
> down-right, only a thin lid edge, and the latch on the near plane

Negative terms remain useful as a short guardrail, but repeatedly adding
synonyms did not compensate for a weak visual anchor. The prompt should name
the required plane relationship once, then list the small set of familiar
substitutions to reject.

### 5. Native square references are safer for a square output

The supplied 36x32 reference was not used in R9 because the target was an exact
32x32 square and the two 32x32 references already provided enough style
context. The non-square image may be usable when padded or when aspect ratio is
not strict, but it should not be silently stretched into a square camera
anchor.

### 6. Material-specific design focus helps preserve the camera

R9 changed one design axis at a time while keeping the camera fixed:

- wooden: redesign the wood;
- iron-bound: redesign the iron binding;
- ornate: redesign the ornate trim and metalwork.

This is more stable than asking the model to change material, category,
silhouette, camera, and scene context in one sentence.

## Universal MVP prompt

The following is the compact prompt template for this chest-family workflow.
The double-brace values are string variables. Replace the values, but keep the
camera sentence and its exclusions intact.

~~~text
Create one new {{asset_style}} {{asset_type}} inventory item on an exact {{canvas_size}} transparent canvas. Match the attached style image's exact {{view_label}}: a dominant tall near-facing plane, a narrow deep side plane receding down-right, only a thin lid edge, and the {{front_detail}} on the near plane. Keep this camera fixed and redesign only the {{design_focus}}. No visible top face, no top-down, no bird's-eye, no conventional 3/4, no isometric, no front-only, no ground, no shadow, no text, no frame, no extra objects.
~~~

Recommended substitutions:

| Variable | Example values |
| --- | --- |
| `{{asset_style}}` | `wooden`, `iron-bound`, `ornate` |
| `{{asset_type}}` | `treasure chest` |
| `{{canvas_size}}` | `32x32` |
| `{{view_label}}` | `very high-oblique Tibia side view` |
| `{{front_detail}}` | `latch` |
| `{{design_focus}}` | `wood`; `iron binding`; `ornate trim and metalwork` |

“Universal” here means reusable across chest materials, binding, and trim
variants. For another object category, replace the chest-specific `lid edge`
and `front_detail` wording with the equivalent edge and front-plane feature,
while retaining the explicit near-plane/side-plane camera description.

## Recommended MCP request shape

Resolve the prompt variables first, then send one Pro request per material
variant. The shape below is intentionally small and mirrors the successful R9
props:

~~~json
{
  "description": "<resolved universal MVP prompt>",
  "width": 32,
  "height": 32,
  "no_background": true,
  "style_copy": [
    "color_palette",
    "outline",
    "detail",
    "shading"
  ],
  "style_image_base64": "<accepted 32x32 camera-anchor PNG>",
  "reference_images": [
    {
      "base64": "<native 32x32 style reference 1>",
      "usage": "additional Tibia style reference: palette, crisp outline, shading, native pixel scale"
    },
    {
      "base64": "<native 32x32 style reference 2>",
      "usage": "additional Tibia style reference: palette, crisp outline, shading, native pixel scale"
    }
  ]
}
~~~

For the tested chest set, the style-image value was the accepted R6 output for
the same material, and the two reference-image values were the supplied native
32x32 styles. The supplied 36x32 style was omitted from the square R9 request.
Do not replace the accepted camera anchor with a text-only label or a
distinctive style-only subject unless copying its geometry is intended.

If exact geometry preservation is required, use the edit request shape instead:

~~~json
{
  "images_base64": [
    "<32x32 source sprite whose camera must be preserved>"
  ],
  "reference_image_base64": "<appearance or material reference>"
}
~~~

The Pro and edit props are documented in the [Create Image Pro reference](../../skills/pixellab-pip/references/create-image-pro.md)
and [style-reference routing reference](../../skills/pixellab-pip/references/style-reference.md).

## Verification checklist

Review every returned alternative before selecting a result:

1. Confirm exact `32x32` dimensions and RGBA transparency.
2. Confirm the background is empty and there is no ground, shadow, frame, or
   text.
3. Confirm the near-facing plane dominates the sprite.
4. Confirm the side plane is narrow, visibly deep, and recedes down-right.
5. Confirm only a thin lid edge is visible; reject a broad roof/top face.
6. Confirm the latch or equivalent front detail is on the near plane.
7. Reject top-down, bird's-eye, conventional three-quarter, isometric, and
   front-only interpretations.
8. Confirm the requested material or trim changed without changing the camera.
9. Preserve all alternatives and record the selected frame, reason, and
   request props in a blueprint.

The final R9 visual review is [available here](../../pixellab-pip-generations/treasure-chests-tibia-pro-style-lock-r8-20260908/review.md).
The selected-output preview and input comparison are [the selected preview](../../pixellab-pip-generations/treasure-chests-tibia-pro-style-lock-r8-20260908/selected-preview-contact-sheet.png)
and [the input comparison](../../pixellab-pip-generations/treasure-chests-tibia-pro-style-lock-r8-20260908/tibia-input-vs-selected-comparison.png).

## Reproducibility and artifact record

The generation archive keeps each batch, its blueprint, its review, and the
shared budget/history records. The flat export contains one tightly packed,
unlabeled sprite sheet and one same-stem blueprint for every batch attempt; its
index is [sprite-sheet-index.json](../../pixellab-pip-generations/treasure-chests-tibia-all-attempts-flat-20260908/sprite-sheet-index.json).

The R6 geometry-lock evidence is [the R6 review](../../pixellab-pip-generations/treasure-chests-tibia-edit-r5-20260908/review.md)
and [the R6 blueprint](../../pixellab-pip-generations/treasure-chests-tibia-edit-r5-20260908/treasure-chests-tibia-edit-r5-20260908.blueprint.json).
The rejected Pro comparisons are preserved in the [R5 review](../../pixellab-pip-generations/treasure-chests-tibia-style-strip-r4-20260908/review.md),
the [R7 review](../../pixellab-pip-generations/treasure-chests-tibia-pro-locked-r6-20260908/review.md),
and the [R8 review](../../pixellab-pip-generations/treasure-chests-tibia-pro-anchor-r7-20260908/review.md).

## Limitations and follow-up

- The result is a learned visual recipe, not a guaranteed projection constraint.
- Pro generation can still return mixed-quality alternatives; review remains
  mandatory.
- A style image that already contains the desired geometry can transfer that
  geometry. Use that deliberately; do not use it when the subject silhouette
  must be novel.
- The universal prompt is intentionally chest-family specific. Making it
  category-agnostic would remove the lid and latch anchors that improved this
  task.
- Future reruns should preserve the same request shape and compare against the
  R9 selected outputs before spending additional Generation Units.

## Related operational references

- [PixelLab style-reference routing](../../skills/pixellab-pip/references/style-reference.md)
- [Create Image Pro request contract](../../skills/pixellab-pip/references/create-image-pro.md)
- [Blueprint and history contract](../../skills/pixellab-pip/references/blueprint.md)
- [Reviewable alternatives contract](../../skills/pixellab-pip/references/reviewable-candidates.md)
- [Local asset assembly](../../skills/pixellab-pip/references/local-asset-assembly.md)
