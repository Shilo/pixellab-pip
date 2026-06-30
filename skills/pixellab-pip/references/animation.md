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

Do not assume `animate-with-text-v3` with a matching `last_frame` is safe for tiny or low-motion idle loops. Identical or near-identical first/last frames can still match the endpoints while adding detached puffs, arcs, symbols, trails, or other external marks in middle frames.

Use `last_frame` when the user needs interpolation between distinct poses, the action has clear internal body motion, or external motion marks are acceptable and will be inspected.

Treat `last_frame` as high-risk when:

- The first and last frames are identical or nearly identical.
- The prompt is idle, stand, breathing, subtle bob, weight shift, neutral stance, or another low-motion loop.
- The user requires no effects, particles, marks, symbols, trails, or artifacts.

For clean idle loops, prefer one candidate first. Use first-frame-only generation with careful prompt wording unless the user provides or asks for a last-frame anchor. If the user supplies an identical or near-identical `last_frame`, explain the artifact risk and ask whether to use it or try first-frame-only instead. Preserve the endpoint's returned frame order when assembling previews or spritesheets; do not create local ping-pong, reversed, duplicated, trimmed, or otherwise reordered outputs unless the user explicitly asks for that playback style. Do not spend retries changing only frame count or tiny last-frame differences unless the user asks for that specific experiment.

When the user does not specify `frame_count`, use the endpoint default or documented animation/template default. For REST `animate-with-text-v3`, current OpenAPI documents `frame_count` as 4-16 with default 8; refresh the schema before choosing a non-default value when exact current behavior matters.

## Walk Loops From Idle Stances

Do not present any raw animation route as a reliable way to turn one idle or neutral stance frame into a natural seamless walk cycle.

Observed `animate-with-text-v3` walk-loop attempts from an idle south-facing character frame failed across short prompts, long prompts, negative prompting, no negative prompting, identical first/last anchors, first-frame-only input, and 4-, 8-, and 16-frame requests. The outputs repeatedly favored idle-like motion, mouth/open-face changes, exaggerated arm motion, pose drift, or non-walk movement instead of clear alternating foot contacts.

Treat this as a high-risk route when:

- The supplied first frame is a planted idle/neutral pose rather than a walk contact, passing pose, or opposite-contact pose.
- The user asks for a seamless walk cycle from an identical first and last frame.
- The task requires natural locomotion, credible weight transfer, stable face/body identity, and no artifacts.

Route-specific cautions:

- `animate-with-text-v3` with identical idle first/last frames may close the endpoints while collapsing toward idle, opening the mouth/face, adding smoke/poof-like artifacts, or inventing exaggerated limb motion.
- `animate-with-text-v3` with first frame only may generate motion, but it does not reliably loop back to the source pose even when the prompt explicitly asks for a seamless loop.
- `animate-with-text-v2` / Pro-style raw text animation is not yet validated as a reliable fallback for this case. Low-frame outputs can make larger pose jumps; treat any higher-frame beta support as current-schema-dependent and verify before recommending it.
- Skeleton or template routes can provide arm/leg cycling, but may look stiff or robotic and can generate hard shadows on limbs. Disabling or softening shadows can reduce one artifact class, but it does not guarantee natural gait.

For walk cycles, prefer a true walk-contact or opposite-contact `last_frame` over a duplicate idle frame. If only one idle frame exists, warn that prompt wording and frame-count changes alone have not produced consistent natural results in observed tests. Recommend one candidate for one direction first, or ask whether the user can provide/create a walk contact pose, use a managed/template walk as a rough draft, or finish the cycle in an editor workflow.

When testing a candidate, inspect for clear alternating left/right foot contacts, readable passing poses, no mouth/talking changes, no detached artifacts, no body-scale drift, no hard shadow reinterpretation, and credible loop closure before expanding to other directions.

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
