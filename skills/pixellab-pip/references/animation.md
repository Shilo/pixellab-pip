# Animation

Read this for raw animation, managed character/object animation, interpolation, skeleton animation, outfit transfer, rotation, frame anchors, or animation preview verification.

## Route Choice

Use MCP `animate_character`/`animate_object` for managed MCP assets. For direct files, exact REST schemas, skeletons, interpolation, outfit transfer, raw frame editing, or rotation, use the REST v2 routes (`animate-with-text-v3`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, `generate-8-rotations-v2/v3`).

Classify supplied frame images (first frame vs last frame vs style/edit reference vs managed asset ID) per the Goal Router in `image-input-roles.md`; ask before a credit-spending call when the role would change the endpoint, field, or output.

## Idle Loop Risk

Do not assume `animate-with-text-v3` with an identical or near-identical `last_frame` is safe for tiny or low-motion idle loops. The endpoint frames can still match while middle frames add detached puffs, arcs, symbols, trails, or other external marks.

Use `last_frame` when the user needs interpolation between distinct poses, the action has clear internal body motion, or external motion marks are acceptable and will be inspected.

Treat `last_frame` as high-risk when:

- The first and last frames are identical or nearly identical.
- The prompt is idle, stand, breathing, subtle bob, weight shift, neutral stance, or another low-motion loop.
- The user requires no effects, particles, marks, symbols, trails, or artifacts.

For clean idle loops, prefer one candidate first — first-frame-only generation with careful prompt wording — unless the user provides or asks for a last-frame anchor. If they supply a near-identical `last_frame`, explain the artifact risk and ask whether to use it or try first-frame-only. Do not spend retries on only frame-count or tiny last-frame changes unless the user asks for that experiment.

For REST managed character animation, `/animate-character` and `/characters/animations` can accept v3-only `custom_start_frame` and `end_frame` fields. Treat them like frame anchors: they require exactly one direction, are not compatible with template or pro mode, and `end_frame` enables interpolation toward a target pose. Use them only when the user asks for a custom start pose, target pose, or managed-character interpolation; otherwise let the character's stored direction frame be the start.

When the user does not specify `frame_count`, use the endpoint default or documented animation/template default. For REST `animate-with-text-v3`, current OpenAPI documents `frame_count` as 4-16 with default 8; refresh the schema before choosing a non-default value when exact current behavior matters.

## Walk Loops From Idle Stances

Seamless walk loops generated from a single idle or neutral stance frame are high-risk:

- First-frame-only attempts can produce motion but did not reliably close the loop; identical first/last idle anchors add loop pressure but became constrained or unpredictable (across prompt lengths, with/without negative prompting, at 4/8/16 frames), with palette shifts near the interpolation endpoint.
- Prefer mid-walk start/end anchors over idle anchors — more reliable, but not a proven complete fix.
- Skeleton/template routes improve loopability and pose consistency but looked stiff, robotic, and prone to hard limb shadows.
- Common idle-derived failures: idle collapse, mouth/talking motion, exaggerated arms, weak foot contacts, and breathing/wind/smoke artifacts near the head (the model reads the request as idle-like motion).

If this route fails or the agent needs more detail, read `../../docs/pixellab/pixellab-idle-animation-artifact-research.md`.

## Verification

Before calling an animation final, verify:

- Frame count and frame order.
- Canvas dimensions and transparency.
- Whether `first_frame` and `last_frame` were used.
- Whether endpoint frames match when loop closure matters.
- Middle-frame visual quality, especially detached artifacts, palette shifts, body drift, or unexpected gestures.
- Preview GIF or spritesheet output faithfully represents the source frames.

Report whether the result technically loops and whether it is visually acceptable. These are different claims.

## Outfit And Edit Animation

`transfer-outfit-v2` and `edit-animation-v2` return composited frames, not reusable paperdoll layers. Preserve frame count, order, size, direction labels, and transparency; if source and target counts, dimensions, or direction sets differ, ask how to align them before spending credits.

For paperdoll or layer requests, read `paperdolling.md` before using animation edit or outfit transfer.
