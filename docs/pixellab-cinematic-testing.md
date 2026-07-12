# PixelLab Cinematic Support — Test Plan & Results

Purpose: verify that the multi-shot cinematic workflow (short animated or seamlessly-looping scenes built by chaining animation jobs) is correct, complete, and streamlined for real user requests — including scenes built **from scratch** (no supplied frame) and **natural loops** where the last frame returns to the first. Testing runs in two tiers:

- **Smoke tests** — the request is posed in plain language and the assistant is asked to plan first; no credits are spent. These check routing, budget-gating, planning, and interaction quality.
- **Live tests** — the assistant builds the cinematic end to end and validates it. Each cinematic is capped at **100 frames** (≈10 seconds at 100 ms/frame).

Each test is written the way a person would actually ask, and points the assistant at the skill contract. Every result is scored on the rubric below. This document is a public record of coverage; it names no internal files.

## Scoring rubric

Each dimension scores **0 = fail, 1 = partial, 2 = pass**. Not every dimension applies to every test (marked n/a).

| Dimension | Pass means |
|---|---|
| Route | Recognized the request as a multi-shot / looping cinematic and used the cinematic contract (not a single one-off clip, unless the request truly is one). |
| Budget | Treated a user budget as required — asked for one if missing, and respected it as a hard cap. |
| Plan | Produced a documented beat-by-beat plan (one shot per beat) before spending. |
| First frame | For from-scratch scenes, chose a sound way to create the opening frame before animating. |
| Loop | For loop requests, anchored the end back to the start (first frame reused as the last) so it loops cleanly. |
| Validation | Checked every generated shot (frame count, size, transparency, motion, continuity) and re-rolled below confidence. |
| Constraints | Honored scene rules — only the allowed objects, facing, mood, background — and described object physics rather than off-screen actors. |
| Deliverables | Produced the standard set: a looping GIF, a spritesheet, the individual frames, plus a blueprint and manifest. |
| Streamlined | Asked the user nothing about mechanics (frame counts, seeds, chaining); kept friction minimal. |
| Quality (live) | The finished cinematic matches the request and plays/loops cleanly. |

## Smoke scenarios (no credits)

| ID | Request (as a person would ask) | What it checks |
|---|---|---|
| S1 | "Make a short seamlessly-looping animation of a glowing campfire." (no budget stated) | Budget is required — must ask before spending. |
| S2 | "Make a ~4-second seamlessly-looping pixel scene of a waterfall, from scratch. Budget $2." | From-scratch first frame, beat plan, loop anchoring, cost vs budget. |
| S3 | "Make me a cool looping animation. Budget $3." | Vague scene → ask a couple of scene questions, not mechanics. |
| S4 | "Make a 1-second looping wave. Budget $1." | Single short clip boundary → one animation job, not the multi-shot flow. |
| S5 | "Make a 60-second cinematic of a dragon flying. Budget $0.20." | Budget too small for the duration → say it can't fit; offer a shorter cut. |
| S6 | "Make a ~5s looping scene of a cat batting a ball toward the camera. Only the cat and the ball are ever on screen. Budget $3." | Only-allowed-objects, facing, physics-not-actors, loop, plan. |
| S7 | "Haz una animación en bucle de una vela encendida, 3 segundos. Presupuesto 2 dólares." | Non-English request → localize the scene, keep replies in Spanish, still route and budget-gate. |
| S8 | "Make a 5-second loop of a spinning coin at 12 fps. Budget $2." | Honors a named playback rate / adjusts the frame math; still budget-gates. |
| S9 | "Here's my hero sprite — make a ~4s idle loop from it. Budget $2." (frame supplied) | Uses the supplied frame as the opening frame (correct image role). |
| S10 | "Make me a 6-second cinematic. Budget $3." (no scene) | Duration only → ask what the scene should be. |

## Live scenarios (real generation, ≤100 frames each, from scratch)

| ID | Request | Loop | Frames cap | What it checks |
|---|---|---|---|---|
| L1 | "A small campfire flickering, seamlessly looping, about 3 seconds, from scratch. Budget $3." | yes | ≤100 | Ambient single-subject loop; first=last anchoring. |
| L2 | "A fish swimming past a rising bubble, looping ~3s. Budget $3." | yes | ≤100 | Two-object continuity in a loop. |
| L3 | "A gold coin spinning, seamlessly looping ~2.5s. Budget $3." | yes | ≤100 | Rotation loop; explicit first=last. |
| L4 | "A seed sprouting into a small flower, ~5s — doesn't need to loop. Budget $4." | no | ≤100 | Narrative micro-arc; start ≠ end. |
| L5 | "A little robot waving at the camera, seamlessly looping ~3s. Budget $3." | yes | ≤100 | Subject facing the camera; loop. |
| L6 | "Rain falling, seamlessly looping ~3s. Budget $3." | yes | ≤100 | Ambient particle-like motion loop. |

## Method notes

- From scratch means no starting image is provided (except S9/where noted): the assistant must first create an opening frame with an appropriate image route, then animate/interpolate from it.
- Natural loop means the opening frame is reused as the final target so the sequence returns to its start; the assistant should choose this rather than trying to hand-steer a long drift back.
- Every shot is validated before the next is built; failures are re-rolled, and re-rolls count against the budget.

## Results

_Filled after each tier runs._

### Smoke results

_pending_

### Live results

_pending_

## Findings and workflow improvements

_pending_
