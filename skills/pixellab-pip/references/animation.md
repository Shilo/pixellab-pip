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

Managed v3 character and object animation (MCP `animate_character`/`animate_object` and the REST equivalents) stores the input reference frame as frame 0 by default, so `frame_count=8` stores and reports 9 frames. Set v3-only `keep_first_frame=false` (incompatible with template and pro modes) when the user needs exactly `frame_count` generated frames; otherwise expect and report the extra frame instead of treating it as a frame-count mismatch.

When the user does not specify `frame_count`, use the endpoint default or documented animation/template default. For REST `animate-with-text-v3`, current OpenAPI documents `frame_count` as 4-16, must be even, default 8; refresh the schema before choosing a non-default value when exact current behavior matters.

Raw `animate-with-text-v3` returns `frame_count`+1 images: image 0 is a re-render of the supplied `first_frame` (close but not pixel-identical), then the generated frames — so `frame_count=16` yields 17 images. Count and report accordingly; do not read the extra image as a frame-count mismatch. `first_frame` and `last_frame` are Base64Image objects (`{"type":"base64","base64":"…","format":"png"}`), not bare base64 strings. Because image 0 is a re-render, a from-scratch loop's true anchor is the first generated frame, not the pre-generation opening image.

## Async Polling

`animate-with-text-v3` (and the other generation endpoints) are async: `POST` returns a `background_job_id`; poll `GET /background-jobs/{job_id}`. Treat the job as done when `last_response` holds the images (its inner status is completed) — the top-level job `status` can lag behind the ready, already-billed result, so waiting only on it may hang. Make the poll loop tolerant of transient timeouts and 5xx: re-poll the same saved `background_job_id`, and never resubmit a paid job on a transient poll error — that double-charges (see `job-lifecycle.md`). Persist each paid response as it arrives so a poller crash cannot orphan a charged job.

## Duplicate-Filled Atlas Risk

`animate-with-text-v3` cannot turn a spritesheet of identical still cells into unique sequential phases from the prompt alone. It treats the whole atlas as one image and applies synchronized motion to every cell — with `first_frame` only or with identical `first_frame`/`last_frame` anchors — and wording like "every cell unique" does not override this.

If the user insists on animating a duplicate-filled atlas in place, `animate-with-text-v2` / Pro honors per-cell variation better but at lower pixel quality. Offer it as an optional paid candidate, not a quality upgrade; warn about palette and color drift; generate one candidate first and verify every cell.

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
- For atlas inputs, whether cells contain genuinely different animation phases rather than synchronized copies or superficial pixel noise.
- Preview GIF or spritesheet output faithfully represents the source frames.

Report whether the result technically loops and whether it is visually acceptable. These are different claims.

## Outfit And Edit Animation

`transfer-outfit-v2` and `edit-animation-v2` return composited frames, not reusable paperdoll layers. Preserve frame count, order, size, direction labels, and transparency; if source and target counts, dimensions, or direction sets differ, ask how to align them before spending credits.

For paperdoll or layer requests, read `paperdolling.md` before using animation edit or outfit transfer.
