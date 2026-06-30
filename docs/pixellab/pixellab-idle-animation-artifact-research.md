# PixelLab Idle Animation Artifact Research

Last reviewed: 2026-06-29.

Purpose: record live-generation findings from attempts to create a clean 9-frame idle loop from a small transparent pixel-art character frame using PixelLab REST v2 `animate-with-text-v3`.

This note intentionally does not link to any generated candidate files. The generation outputs were disposable test artifacts and may be deleted. The useful artifact is the routing lesson: low-motion character animation can produce external effect marks, especially when `last_frame` is supplied.

## Scope

Test subject:

- A 128x128 transparent pixel-art goblin character frame.
- A second 128x128 transparent variant with the visible white teeth removed.
- The user wanted 8 generated frames plus the original first frame, for 9 total frames.

Test route:

- REST v2 `POST /animate-with-text-v3`.
- `first_frame` was always the supplied character image.
- `frame_count` was `8`.
- `no_background` was `true`.
- `enhance_prompt` was `false`.
- `seed` was `0`, which the current schema describes as random seed behavior rather than deterministic replay.

Additional frame-count finding:

- The endpoint rejects odd `frame_count` values. A request for `frame_count: 7` failed validation; `frame_count: 6` is the nearest valid shorter setting and returns 7 total images including the initial frame.

Two route modes were compared:

- First and last frame supplied: equivalent to the product behavior the user described as "interpolate (new)".
- First frame only: equivalent to the product behavior the user described as "animate with text (new)".

## Summary Verdict

The strongest finding is that supplying `last_frame` for a low-motion idle loop strongly correlated with external artifact marks in the middle frames.

When `first_frame` and `last_frame` were both set to the same still pose, PixelLab reliably returned exact endpoint frames, but the in-between frames often contained non-character marks such as puffs, arcs, question-mark-like symbols, swirls, or motion streaks. The marks changed color and shape across prompts and seeds, but the failure pattern remained.

Removing the character's white teeth did not solve the issue. It changed the artifact style, which weakens the theory that the model was simply interpreting the teeth as smoke. The more likely cause is interaction between low-motion prompts and the interpolation path itself.

First-frame-only generation avoided the external puff/arc artifacts in the tested runs, but it did not close the loop and over-animated the character into visible arm or club gestures. This suggests `last_frame` helps loop closure but can induce external "motion explanation" artifacts, while omitting `last_frame` reduces those artifacts but gives the model too much freedom to drift.

Current synthesis from the test series:

- Changing frame count did not solve the idle artifact problem. Odd `frame_count` values are rejected, and the nearest shorter valid setting still produced detached white pixels and failed to close cleanly.
- Changing the last frame slightly did not solve the problem. A non-identical last-frame anchor still produced large detached splash/arc artifacts during a low-motion idle request.
- Some interpolated outputs showed late-frame visual instability, including color or palette shifts near the final generated frame before the anchored endpoint.
- The strongest positive lever was not frame count or anchor similarity; it was action clarity. When the `action` described a more expressive character motion, such as a friendly hand wave, the model had enough internal body movement to animate and avoided the detached idle artifacts in the observed run.

## Follow-up: Walk Loops From A Single Idle Pose

A later sprite-sheet test extended this finding from subtle idle loops to walk-cycle generation. The test subject was a transparent 128x128 south-facing futuristic humanoid/robot frame extracted from a multi-direction sprite sheet. The first frame was visually correct as a standing character identity anchor, but it was not a walk contact pose with one foot clearly forward.

The requested result was a natural, seamless south-facing walk cycle with no background. Several prompt and route variants were tried, including short prompts, detailed biomechanical prompts, prompts with negative constraints, prompts without negative constraints, first-frame-only input, identical first/last-frame interpolation, 4-frame-count / 5-total-frame attempts, 8-frame attempts, and a 16-frame attempt using the same seed as an earlier run.

Result summary: none of those variants produced a consistent, natural, production-ready walk loop from the single idle stance. The repeated failure mode was not just weak prompting. The model tended to preserve or elaborate the idle stance, open or change the mouth/face, create talk-like motion, add smoke/poof-like artifacts, exaggerate arm swings, or move the body in ways that did not read as clean alternating foot contacts.

Observed `animate-with-text-v3` behavior:

- Identical first/last-frame interpolation from the idle stance could satisfy endpoint pressure while still failing the walk. The output often looked like an idle/talking loop or contained non-walk artifacts rather than a natural stride.
- First-frame-only generation avoided the duplicate endpoint constraint, but it did not reliably close the loop even when the prompt explicitly requested a seamless walk cycle.
- In the observed v3 calls, `frame_count: 4`, `frame_count: 8`, and `frame_count: 16` returned 5, 9, and 17 images respectively, apparently including the supplied anchor frame(s). This should be treated as observed return behavior for those tests, not as a reason to trim or reorder frames without verification.
- Reusing a previous seed helped make comparisons fair, but it did not turn the idle anchor into a reliable walk cycle.
- Increasing frame count smoothed some transitions but did not solve the underlying motion problem. A longer output still lacked convincing walk mechanics when the only pose anchor was the idle stance.

Other route observations:

- `animate-with-text-v2` / Pro-style raw text animation was not heavily tested enough to call it a reliable fallback. The lower-frame behavior can create larger, more drastic pose changes, and any 8-frame beta availability should be verified against the current public MCP/API surface before recommending it.
- Skeleton or template routes provided more explicit limb cycling, but observed outputs could read as stiff, robotic, or uncanny. Hard generated shadows on arms and legs made some tests look worse. Shadow/style controls can reduce that symptom, but they do not by themselves create natural weight transfer.

Practical conclusion: these findings do not show any currently proven fully automatic route that reliably turns a single idle stance into a natural seamless walk loop. For walk cycles, the key missing input is usually a real motion pose, not a longer prompt. A duplicate idle first/last frame is a weak animation constraint for locomotion because the model has to invent all contact, passing, weight-shift, and recovery poses while also returning to the same planted stance.

Routing consequence:

- Prefer a real walk contact or opposite-contact frame as `last_frame` instead of reusing the idle frame.
- If the user only has an idle frame, warn that raw interpolation and first-frame-only v3 both need visual inspection and may fail regardless of prompt length, negative prompting, or frame count.
- Do not keep spending retries on prompt wording alone when the source pose remains a neutral idle.
- Generate one direction first, preserve all returned frames, and verify foot contacts, mouth/face stability, body scale, detached artifacts, shadows, and loop closure before expanding to a full directional sheet.
- When natural locomotion matters, consider a managed/template walk only as a rough draft, or route to explicit pose authoring, skeleton/keypoint editing, Aseprite/Pixelorama cleanup, or another manual animation workflow.

## Observed Prompt Behavior

The following prompt families were tested with first and last frame supplied. All returned technically looped endpoint frames, but all produced external artifacts in the middle frames:

| Prompt family | Observed behavior |
|---|---|
| `idle` | Produced external arcs or symbols around the character. |
| Breathing-style prompts | Produced white puff/smoke-like marks above the head. |
| `looping neutral stance` | Produced external white arcs. |
| `stand` / `stand still` | Produced white or cyan motion/effect strokes. |
| `Standing pose, slow one-pixel bob.` | Produced puff-cloud artifacts. |
| `Subtle weight shift between planted feet.` | Produced colored or white motion/effect arcs across rerolls. |
| `Small torso dip and return.` | Produced white arc/cloud shapes. |
| Image-grounded idle loop with a slightly different generated last frame | Returned exact start and end anchors, but produced large detached white splash/arc marks in the middle frames. |
| Concrete hand-wave action with the same slightly different anchors | Returned exact start and end anchors and produced a readable raised-hand wave without the detached puff/splash artifacts seen in idle tests. |
| Negative-prompt append variants | Did not reliably help; mentioning puffs, smoke, or white pixels may have kept those concepts active in the prompt. |

The following variants were tested first-frame-only:

| Prompt | Observed behavior |
|---|---|
| `idle` | No external puff/arcs, but the character raised the arm/club and did not loop back to the source pose. |
| `idle loop` | No external puff/arcs, but the character raised the arm/club into a clear gesture and did not loop back to the source pose. |
| Image-grounded `idle loop` wording | No external puff/arcs and much less gesture drift than bare `idle loop`, but the last frame still was not pixel-identical to the source pose. |
| Image-grounded `idle loop` wording with 7 total frames | API rejected `frame_count: 7`; using the nearest valid shorter setting, `frame_count: 6`, returned 7 total images but reintroduced detached white pixels above the head and did not close the loop. |
| `slow blink` | No external puff/arcs, but the character drifted into larger arm/club gestures and did not loop back to the source pose. |

## Teeth Hypothesis

The user created a no-teeth variant to test whether the source image's small white mouth pixels were being interpreted as smoke, breath, or an effect seed.

Findings:

- The no-teeth source did not eliminate external artifacts when `last_frame` was supplied.
- With `idle`, the artifact changed into tan question-mark-like marks.
- With `stand still`, the artifact changed into pale motion/effect blobs.
- Therefore, the teeth may affect the visual vocabulary of artifacts, but they are unlikely to be the root cause.

Probable conclusion: the endpoint/model is adding external visual marks to communicate subtle or ambiguous motion, and the exact source pixels influence the artifact style only secondarily.

## Probable Cause

The most likely cause is the combination of:

1. Low-amplitude animation request.
2. Identical or near-identical `first_frame` and `last_frame`.
3. A prompt that asks for motion but provides no large body action.

That combination creates a constrained interpolation problem: the model must produce visible middle-frame change while returning exactly to the starting pose. In the observed runs, it often satisfied that pressure by adding detached visual marks around the character rather than only moving the character's body pixels.

This explains why:

- The endpoints looped cleanly when `last_frame` was supplied.
- The artifacts appeared mostly in middle frames.
- Prompt-only fixes did not reliably work.
- First-frame-only runs removed the external marks but drifted into larger body gestures and did not close the loop.
- Concise, image-grounded first-frame-only wording reduced drift compared with a bare `idle loop` prompt, but still did not produce a true closed loop.
- Using a slightly different last frame, rather than an identical last frame, did not remove the artifacts; in one test it produced larger detached white splash marks.
- A larger, concrete character action such as a friendly hand wave gave the model enough internal body motion and avoided the detached marks in one test.
- Late generated frames can also show palette or color instability, so endpoint equality alone is not enough to judge a loop.

## Practical Routing Guidance

For PixelLab Pip, do not assume `animate-with-text-v3` plus a matching `last_frame` is safe for tiny idle loops.

Use `last_frame` when:

- The user needs interpolation between two distinct poses.
- The motion is large enough that the model has clear internal character movement to generate.
- External motion marks are acceptable or can be inspected and rejected.

Avoid or treat `last_frame` as high-risk when:

- The first and last frame are identical.
- The requested action is idle, stand, neutral stance, breathing, subtle bobbing, weight shift, or another low-motion loop.
- The user requires no external effects, marks, symbols, trails, particles, or artifacts.

For clean idle loops, prefer one of these workflows:

1. Generate first-frame-only candidates and inspect for body drift.
2. Use only the earliest clean frames before any gesture grows too large, then assemble a local ping-pong loop from those frames.
3. Prefer concise image-grounded first-frame-only wording over bare labels such as `idle` or `idle loop` when testing for low-drift candidates.
4. If an interpolation candidate is otherwise good, remove only disconnected external artifact pixels with a conservative alpha/component cleanup pass.
5. Verify every frame visually and with a contact sheet before reporting success.

Do not spend many retries on these as primary fixes for subtle idle artifacts:

- Changing only the frame count.
- Changing only the last frame by a tiny amount.
- Relying on exact first/last endpoint matches.

For non-idle character animations, prefer expressive actions with visible body mechanics. A wave, attack, turn, jump, reach, or other concrete movement may perform better than trying to force barely visible idle motion through interpolation.

Local assembly and verification may include:

- GIF assembly with explicit disposal settings.
- Coalescing the GIF back into frames and comparing it to the source PNG sequence.
- Connected-component checks to detect detached pixels outside the main character/prop component.
- Conservative removal of detached generated pixels when the requested art remains entirely PixelLab/user-originated.

Do not call a PixelLab idle output final unless:

- Frame count is verified.
- Frame dimensions and transparency are verified.
- The preview GIF faithfully renders the PNG frames.
- The loop is inspected, not just assumed from matching endpoints.
- Middle frames contain no external marks or weird gestures.

## Prompting Lessons

Prompt-only mitigation was not enough in these tests.

Terms that appeared risky:

- `idle`
- `breathing`
- `stand`
- `stand still`
- `looping neutral stance`
- `weight shift`
- `one-pixel bob`
- `torso dip`

The issue was not that any single term always fails; it was that low-motion prompts with identical endpoints gave the model room to invent external motion indicators.

Negative prompts also did not reliably help. They can be useful for clear exclusions, but in this case long negative lists introduced artifact concepts such as puff, smoke, particles, trails, and white pixels into the prompt itself. In repeated tests, those concepts still appeared.

Future prompt experiments should avoid both broad animation labels and artifact vocabulary. Prefer concrete internal character actions that have visible motion without requiring external indicators, but expect first-frame-only outputs to need local loop assembly.

For animations that do not have to be subtle idles, prefer explicit expressive intent. Describe which limb moves, where it moves, and what pose it settles into. The successful wave test suggests the model behaves better when the requested action has a clear internal motion path.

Potential future tests:

- `eyes close then open`
- `head nod`
- `small hand twitch`
- `club hand relaxes`
- `one foot tap`

These are not guaranteed; they are simply more concrete than "idle" and less likely to require external motion marks.

## Skill Contract Implications

The skill should preserve this route distinction:

- `animate-with-text-v3` with `first_frame` only is not equivalent to `animate-with-text-v3` with both `first_frame` and `last_frame`.
- Supplying `last_frame` can improve loop closure but may create interpolation artifacts on low-motion prompts.
- If a user asks for a clean idle loop, Pip should warn internally that this route needs frame inspection and may require multiple candidates or local assembly.
- If the user explicitly prohibits artifacts, do not trust prompt constraints alone; verify frames.

Recommended answer/report wording after live attempts:

- Say whether `last_frame` was used.
- Say whether the endpoint returned exact endpoint matches.
- Say whether middle frames had external marks.
- Distinguish "technically loops" from "visually acceptable".

## Open Questions

- Whether a public PixelLab endpoint or mode exposes a stronger "no external effects" control for animation.
- Whether an official template-based idle animation on a managed character avoids these artifacts better than raw `animate-with-text-v3`.
- Whether smaller frame counts, different canvas padding, or pre-masked source images reduce artifact frequency.
- Whether a two-step route, such as first-frame-only generation followed by local ping-pong assembly, should become the default for tiny idle loops.
