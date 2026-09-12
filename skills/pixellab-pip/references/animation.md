# Animation

Read this for raw animation, managed character/object animation, interpolation, skeleton animation, outfit transfer, rotation, frame anchors, or animation preview verification.

## Route Choice

Use MCP `animate_character`/`animate_object` for managed MCP assets. For a raw supplied image with no managed asset, use MCP `animate_image_pixminimax` only when the user explicitly requests PixMiniMax/MiniMax H3; otherwise use MCP `animate_image`. On REST, use `POST /animate-pixminimax` for that explicit model request, or `POST /animate-with-text-v3`/`interpolation-v2` otherwise. The v3 idle-loop, atlas, and pixel-budget risks below were characterized against the REST v3 endpoint; PixMiniMax has separate frame, cost, and prompt rules in the next section. For exact REST schemas, skeletons, outfit transfer, raw frame editing, or rotation, use the REST v2 routes (`animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `transfer-outfit-v2`, `rotate`). For 8 rotations from an image, MCP only partially covers it by regenerating rather than rotating the exact input — `create_8_direction_object(reference_image_base64=…)` for objects, `create_character(mode="v3", reference_image_base64=…)` for characters (identity transfer is unreliable on `create_8_direction_object` for humanoid subjects); use REST `generate-8-rotations-v2/v3` when the exact input pixels must be preserved.

Classify supplied frame images (first frame vs last frame vs style/edit reference vs managed asset ID) per the Goal Router in `image-input-roles.md`; ask before a credit-spending call when the role would change the endpoint, field, or output.

## PixMiniMax / MiniMax H3

PixelLab's public PixMiniMax operation is REST `POST /animate-pixminimax` and MCP `animate_image_pixminimax`. It is beta and requires Tier 1 or higher. The public wrapper accepts a motion-only `description` (limit in `prompt-limits.md`), a required `first_frame`, an optional same-size `last_frame`, `frame_count` 4–40 in multiples of four, an optional `seed`, `no_background`, `drift_threshold`, and `enhance_prompt`; the eight-way `direction` hint is valid only with enhancement. MCP exposes `enhance_prompt` and `direction` too, plus preferred URL frame inputs, but not REST's `drift_threshold`. The input canvas is capped at 256×256. It returns a background job; poll `GET /background-jobs/{job_id}` and expect `frame_count + 1` images, with the input frame intended at index 0.

Adapt MiniMax H3's official timeline-oriented prompting to PixelLab's smaller wrapper: start the motion on the first frame, name the action phases in order, describe the visible transition toward the result, and state “in place” when locomotion must not translate the subject. Preserve identity, palette, outline, scale, canvas placement, and transparency in positive wording. Keep the description concise and about motion, not appearance or audio. MiniMax's raw H3 prompt guides also cover audiovisual fields, reference labels, shots, and soundscape/music; those fields are not part of PixelLab's PixMiniMax schema and must not be copied into a PixelLab request.

Useful shape: `Start [subject] moving on the first frame. [phase 1], then [phase 2], then [result]. Keep the subject in place; preserve [identity anchors].` Use `enhance_prompt=true` when a short motion description needs model expansion and the extra ~0.05 generation is approved. Use `direction` with that enhancement when facing/attack direction matters; otherwise omit it and let the service infer from the image. For an end-state transition, supply a genuinely distinct `last_frame`; for a loop, matching anchors can over-constrain low-motion clips, so inspect the middle frames and endpoint rather than assuming the loop is clean.

## Idle Loop Risk

Do not assume `animate-with-text-v3` or PixMiniMax with an identical or near-identical `last_frame` is safe for tiny or low-motion idle loops. The endpoint frames can still match while middle frames add detached puffs, arcs, symbols, trails, or other external marks; verify the returned middle frames for each route.

Use `last_frame` when the user needs interpolation between distinct poses, the action has clear internal body motion, or external motion marks are acceptable and will be inspected.

For a strict tween between two distinct frames, use the selected raw-animation route with matching first/last-frame URL or base64 inputs: MCP `animate_image_pixminimax` for an explicit PixMiniMax request, otherwise `animate_image`; or REST `animate-pixminimax`/`animate-with-text-v3` with the matching `description`/`action` field. Use `interpolation-v2` (Pro; 128×128 cap; no frame-count control) only if the user explicitly asks for it — `animate_image` partially covers it at v3 tier.

For REST v3 color flicker, `drift_threshold` controls how often de-flicker correction runs: `0` corrects every frame; higher values correct only larger color drift. Omit it unless color drift is a stated or observed problem. REST `generate-8-rotations-v3.description` is an optional extra hint when the supplied frame alone does not convey the intended subject or styling.

Treat `last_frame` as high-risk when:

- The first and last frames are identical or nearly identical.
- The prompt is idle, stand, breathing, subtle bob, weight shift, neutral stance, or another low-motion loop.
- The user requires no effects, particles, marks, symbols, trails, or artifacts.

For clean idle loops, prefer one candidate first — first-frame-only generation with careful prompt wording — unless the user provides or asks for a last-frame anchor. If they supply a near-identical `last_frame`, explain the artifact risk and ask whether to use it or try first-frame-only. Do not spend retries on only frame-count or tiny last-frame changes unless the user asks for that experiment.

Exception: a 360° rotation turntable sends the one frame as both `first_frame` and `last_frame` with a rigid-object trajectory `action`, so the identical anchor closes the loop instead of freezing.

Managed character animation accepts v3-only frame anchors on both surfaces: MCP `animate_character` `custom_start_frame_base64`/`custom_start_frame_url` + `end_frame_base64`/`end_frame_url` (prefer the `_url` forms — MCP clients truncate large inline base64), or REST `/animate-character` / `/characters/animations` `custom_start_frame`/`end_frame`. Treat them like frame anchors: they require exactly one direction, are not compatible with template or pro mode, and the end frame enables interpolation toward a target pose. Use them only when the user asks for a custom start pose, target pose, or managed-character interpolation; otherwise let the character's stored direction frame be the start.

Managed v3 character and object animation (MCP `animate_character`/`animate_object` and the REST equivalents) stores the input reference frame as frame 0 by default, so `frame_count=8` stores and reports 9 frames. Set v3-only `keep_first_frame=false` (incompatible with template and pro modes) when the user needs exactly `frame_count` generated frames; otherwise expect and report the extra frame instead of treating it as a frame-count mismatch.

When appending to an existing managed animation group, pass its existing `animation_name` as well as `group_id`; PixelLab does not inherit the name from the group.

When the user does not specify `frame_count`, use the endpoint default or documented animation/template default. For REST `animate-with-text-v3`, current OpenAPI documents `frame_count` as 4-16, must be even, default 8, plus a **total pixel budget: `width × height × frame_count ≤ 524,288`**. Size and frame count are therefore coupled — a 256×256 canvas allows only 8 frames, and 16 frames need `width × height ≤ 32,768` (a square up to ~181×181; 128×128 is a safe common choice). Exceeding the budget is rejected; refresh the schema before choosing a non-default value when exact current behavior matters. MCP `animate_image` caps the first frame at 256×256 and requires the same even `frame_count` (4-16, default 8); its live tool schema states the identical pixel budget. PixMiniMax instead accepts 4-40 generated frames in multiples of four at any input size up to 256×256; do not apply v3's total-pixel-budget rule to it without current evidence.

Raw `animate-with-text-v3` and PixMiniMax return `frame_count`+1 images: image 0 is the supplied `first_frame` intended as frame 0, followed by the `frame_count` generated frames, so `frame_count=16` yields 17 images and PixMiniMax `frame_count=40` yields 41. Count and report accordingly; do not read the extra image as a frame-count mismatch. Verify the echo at the pixel and visible-content levels: v3 may normalize RGB values in transparent pixels, and small inputs can return a materially changed first image despite the documented echo convention. For chaining, image 0 counts as the handoff duplicate when it is pixel-exact, or when its size and alpha match and the only differences are RGB values stored in fully transparent pixels. A change to size, alpha, or any visible pixel is not a duplicate. Keep the raw frame and report any mismatch instead of silently replacing it; drop image 0 from the stitched playback only after this check. The first frame that has actually moved is image 1. `first_frame` and `last_frame` are Base64Image objects (`{"type":"base64","base64":"…","format":"png"}`), not bare base64 strings.

## Async Polling

`animate-with-text-v3`, PixMiniMax, and the other generation endpoints are async: `POST` returns a `background_job_id`; poll `GET /background-jobs/{job_id}` until the job `status` is `completed` (results at `last_response.images`) or `failed`. Two robustness notes from live runs: under heavy load the top-level `status` can briefly lag the ready result, so `last_response`'s own completed/`done` status is the earliest reliable signal — but do not treat the mere first appearance of an image as done, since some endpoints stream partial progress images. Prefer per-call `usage.generations` when present; if only `usage.usd` is exposed, report that as USD and do not convert it into generations without a documented formula. Make the poll loop tolerant of transient timeouts and 5xx: re-poll the same saved `background_job_id`, and never resubmit a paid job on a transient poll error — that double-charges (see `job-lifecycle.md`). Persist each paid response as it arrives so a poller crash cannot orphan a charged job.

## Atlas Animation Risk

`animate-with-text-v3` treats a spritesheet as one image rather than isolated cells. Prompt wording cannot reliably enforce cell boundaries or preserve each cell independently; motion may deform cells or cross between them. Animate one selected cell as the default. If the user explicitly approves animating several cells independently, use one job per cell and disclose the multi-job cost first.

If the user insists on animating an atlas in one job, explain that the result is experimental. `animate-with-text-v2` / Pro may honor per-cell variation better but at lower pixel quality; offer it as an optional paid candidate, not a quality upgrade, warn about palette and color drift, and verify every cell.

## Walk Loops From Idle Stances

Seamless walk loops generated from a single idle or neutral stance frame are high-risk:

- First-frame-only attempts can produce motion but did not reliably close the loop; identical first/last idle anchors add loop pressure but become constrained or unpredictable — varying prompt length, negative prompting, or frame count did not fix it — with palette shifts near the interpolation endpoint.
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
- For PixMiniMax, whether `enhanced_prompt` was returned and whether `direction` was used only with enhancement.
- Middle-frame visual quality, especially detached artifacts, palette shifts, body drift, or unexpected gestures.
- For atlas inputs, whether cells contain genuinely different animation phases rather than synchronized copies or superficial pixel noise.
- Preview GIF or spritesheet output faithfully represents the source frames.

Report whether the result technically loops and whether it is visually acceptable. These are different claims.

## Outfit And Edit Animation

`transfer-outfit-v2` and `edit-animation-v2` return composited frames, not reusable paperdoll layers. Preserve frame count, order, size, direction labels, and transparency; if source and target counts, dimensions, or direction sets differ, ask how to align them before spending credits.

For paperdoll or layer requests, read `paperdolling.md` before using animation edit or outfit transfer.
