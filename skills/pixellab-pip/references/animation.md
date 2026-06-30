# Animation

Read this for raw animation, managed character/object animation, interpolation, skeleton animation, outfit transfer, rotation, frame anchors, or animation preview verification.

## Route Choice

Use MCP `animate_character` or `animate_object` for managed MCP assets. For direct files, exact REST schemas, skeletons, interpolation, outfit transfer, raw frame editing, or rotation, use REST v2 routes such as `animate-with-text-v3`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, or `generate-8-rotations-v2/v3`.

For existing multi-direction MCP characters, default an unspecified first animation direction to `south` for one preview candidate. Animate all directions only when the user asks for all directions, a complete direction set, or approves the larger batch.

## Frame Roles

Classify supplied images before spending credits:

- `first_frame`: starting image for raw animation.
- `last_frame`: ending/interpolation anchor, not a generic style reference.
- Character/object asset ID: managed animation target.
- Outfit/source/reference frames: route-specific identity or style input.

Infer low-risk frame roles from explicit wording. Ask when role uncertainty would change the endpoint, field, or output semantics, such as style reference vs edit target vs first frame vs last frame vs outfit reference.

## Idle Loop Risk

Do not assume `animate-with-text-v3` with an identical or near-identical `last_frame` is safe for tiny or low-motion idle loops. The endpoint frames can still match while middle frames add detached puffs, arcs, symbols, trails, or other external marks.

Use `last_frame` when the user needs interpolation between distinct poses, the action has clear internal body motion, or external motion marks are acceptable and will be inspected.

Treat `last_frame` as high-risk when:

- The first and last frames are identical or nearly identical.
- The prompt is idle, stand, breathing, subtle bob, weight shift, neutral stance, or another low-motion loop.
- The user requires no effects, particles, marks, symbols, trails, or artifacts.

For clean idle loops, prefer one candidate first. Use first-frame-only generation with careful prompt wording unless the user provides or asks for a last-frame anchor. If the user supplies an identical or near-identical `last_frame`, explain the artifact risk and ask whether to use it or try first-frame-only instead. Preserve the endpoint's returned frame order when assembling previews or spritesheets; do not create local ping-pong, reversed, duplicated, trimmed, or otherwise reordered outputs unless the user explicitly asks for that playback style. Do not spend retries changing only frame count or tiny last-frame differences unless the user asks for that specific experiment.

When the user does not specify `frame_count`, use the endpoint default or documented animation/template default. For REST `animate-with-text-v3`, current OpenAPI documents `frame_count` as 4-16 with default 8; refresh the schema before choosing a non-default value when exact current behavior matters.

## Walk Loops From Idle Stances

Treat natural walk loops generated from a single idle or neutral stance frame as high risk. Observed attempts failed across short and long prompts, negative prompting, no negative prompting, first-frame-only input, identical first/last-frame anchors, and 4-, 8-, and 16-frame requests. Common failures included idle collapse, mouth/talking motion, exaggerated arm movement, weak foot contacts, stiff skeleton/template motion, and hard limb shadows. Breathing/wind/smoke/spark-like artifacts near the head appear connected to inferred breathing behavior when the model interprets the request as idle-like motion.

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

`transfer-outfit-v2` and `edit-animation-v2` return edited/composited frames, not reusable paperdoll layers. Preserve frame count, order, size, direction labels, and transparency. If source and target frame counts, dimensions, or direction sets differ, ask how to align them before spending credits.

For paperdoll or layer requests, read `paperdolling.md` before using animation edit or outfit transfer.
