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

Each scenario was run by a separate assistant instance given only the plain-language request and the skill contract. Smoke instances were asked to plan and did not spend; live instances built the cinematic from scratch and self-validated. Scores use the rubric above (0/1/2 per dimension).

### Smoke results — 10 / 10 correct

Every scenario was routed and handled correctly, with no dimension failing. Highlights:

| ID | Request | Verdict | Key behavior |
|---|---|---|---|
| S1 | Campfire loop, no budget | Pass | Recognized a short flicker loop as a single clip (correctly de-escalated from a multi-shot cinematic) and kept it to a minimal, one-candidate-first flow. |
| S2 | 4s waterfall loop, from scratch, $2 | Pass | Multi-shot route; opening frame via a background image route; calibrate-on-first-job budgeting; loop closed by reusing the opening frame; 3 blocking questions. |
| S3 | "Cool looping animation", $3 | Pass | Flagged $3 as tight → single loop, not a chain; asked for scene/length/background before spending. |
| S4 | 1s wave, $1 | Pass | Correctly a single clip, not a cinematic; cheap route; asked which "wave". |
| S5 | 60s dragon, $0.20 | Pass | Told the user honestly that ~$0.20 cannot fund a full minute (~38 jobs), offered a short cut or a raised budget, hard-stop planned. |
| S6 | 5s cat-bats-ball loop, only two objects, facing camera, $3 | Pass | Two-layer object enforcement (transparent canvas + per-beat exclusions) and described the ball's own physics — never an off-screen actor. |
| S7 | Candle loop, 3s, in Spanish | Pass | Replied in Spanish, translated the generation text to English, routed and budget-gated correctly. |
| S8 | 5s spinning coin loop at 12 fps, $2 | Pass | Generated one full turn and looped it, set the frame delay for 12 fps, treated fps as a playback (assembly) choice. |
| S9 | 4s idle loop from a supplied frame, $2 | Pass | Used the supplied frame as the opening frame; anchored identity to its actual pixels; idle-artifact-aware loop. |
| S10 | 6s cinematic, no scene, $3 | Pass | Had duration and budget but correctly blocked on the missing scene before spending. |

Consistent across all ten: budgets were treated as required (asked when missing, hard-stopped as a cap) and never converted into invented dollar-per-generation prices; costs were to be calibrated on the first real job; the single-clip vs multi-shot boundary was judged correctly; from-scratch opening frames were routed sensibly (a scene/background route for scenes, a sprite route for small subjects); and no instance asked the user about frame counts, seeds, or timing.

### Live results — 6 built from scratch: 5 complete, 1 honest partial

All six created their own opening frame and validated every shot. Costs are the authoritative per-call figures; all were far under budget.

| ID | Request | Route chosen | Loop closes | Cost | Verdict |
|---|---|---|---|---|---|
| L1 | Campfire flicker loop, ~3s | One looped cycle | Yes (seam ≈ a normal flame step) | ~$0.04 | Pass |
| L2 | Fish passing a bubble, loop ~3s | One looped cycle | No — conveyor cut | ~$0.04 | Partial |
| L3 | Spinning gold coin loop, ~2.5s | One looped cycle | Yes (endpoints pixel-identical) | ~$0.07 | Pass |
| L4 | Seed sprouting into a flower, ~5s, no loop | Chained shots | n/a (one-way arc) | ~$0.17 | Pass |
| L5 | Robot waving at camera, loop ~3s | One looped cycle | Yes (seam smoother than an interior step) | ~$0.06 | Pass |
| L6 | Rain falling, loop ~3s | One looped cycle | Yes (seam within normal frame-to-frame range) | ~$0.05 | Pass |

- The periodic scenes (campfire, coin, robot wave, rain) each generated **one clean cycle and looped it at playback**, tuning the frame delay to the requested seconds — cheap and seamless. Loop closure was measured, not asserted: pixel-identical endpoints where a last-frame anchor was used, and within-normal seam distance where a self-closing field was used.
- The evolving scene (seed → flower) correctly **chained shots**, each continuing from the prior shot's frame, producing a smooth one-way growth arc with invisible seams.
- The one partial (fish + bubble) validated its constraints well — a connected-component check confirmed exactly the two objects with no third ever appearing — but the loop did not seam-close. The correct closure technique (reuse the opening frame as the target) was attempted three times and failed on the service side during a backend incident; rather than fake a loop (disallowed) the instance shipped an honest conveyor loop and reported "loops but does not seam-close" as a separate claim.
- Reporting quality was strong throughout: instances distinguished "technically loops" from "looks seamless", flagged concurrent-account balance movement as an overlapping observation instead of miscounting it as their own cost, refused to resubmit already-billed jobs, and offered honest quality caveats (e.g. subtle rain, calm-vs-lively flicker).

Note on conditions: the live suite ran many generations at once and coincided with a period of heavy service load, so some jobs hit transient infrastructure errors and a concurrency ceiling. Those are external to the workflow; the instances handled them correctly (retry the same job, never double-charge, validate before shipping).

## Findings and workflow improvements

Testing produced two rounds of concrete improvements to the cinematic contract, plus confirmation that the rest already works.

**Round 1 (from smoke tests) — the cyclic-loop shortcut.** Several instances independently reasoned that periodic motion (a flicker, spin, bob, sway, flow, rain, or breathing idle) needs only **one clean cycle looped at playback** — with the frame delay tuned to the requested duration — rather than a multi-job chain. This is cheaper and cleaner, and the boundary matters: chaining is for scenes that genuinely evolve. The contract now decides "cyclic vs evolving" up front, and defaults a sensible few-second length for an ambient loop given no duration. The live tests confirmed the rule works in both directions: the periodic scenes took the single-cycle path, and the growth arc took the chained path — each citing the rule.

**Round 2 (from live tests) — robust async handling.** Building for real surfaced two fixes:

- **Completion signal and poll resilience.** The generation jobs are asynchronous, and the top-level job status can lag behind the finished, already-billed result; four separate instances found that keying completion on the presence of the returned images (rather than only the outer status) is what avoids a hang. Poll loops must also tolerate transient timeouts and 5xx by re-polling the same job — never resubmitting a paid job (which would double-charge) — and should persist each paid response as it arrives so a crash can't orphan a charged job. The animation contract now says this.
- **De-duplication vs "no trimmed outputs."** Removing the duplicate re-rendered frame at each shipped seam (and a loop-close frame identical to the first) is expected de-duplication for a clean stitch — not the ping-pong/reverse/trim playback manipulation that is otherwise disallowed. The contract now states this explicitly and keeps the raw frames alongside for integrity.

**What already worked (no change needed).** Route selection (single clip vs multi-shot, cyclic vs evolving), budget discipline (required, calibrated on real usage, hard-stopped, never invented in dollars), from-scratch opening-frame routing, loop closure by reusing the opening frame, per-shot validation with re-rolls, only-these-objects enforcement by describing object physics instead of off-screen actors, non-English handling, supplied-frame handling, and the standard deliverable set (looping GIF, spritesheet, individual frames, blueprint, manifest, plus a raw un-processed cut). One instance described the fit plainly: the cinematic and animation contracts "matched the live API behavior exactly."

**Overall.** Across the tested range — from scratch, cyclic loops, evolving arcs, natural loops that reuse the first frame as the last, multi-object scenes, camera-facing subjects, non-English requests, supplied frames, and budget edge cases — the workflow routed, planned, budgeted, generated, validated, and reported correctly. The one incomplete result was an external service failure during a loop-close attempt, handled honestly. With the two rounds of improvements applied, cinematic support covers the common user requests reliably.

## Extended testing — backgrounds, complex scenes, detailed direction, and start→end interpolation

The first round used transparent-subject scenes. A second round targets richer requests inspired by scene-driven pixel-art cinematics (full game-style backgrounds and short beats): immersive scenes with baked backgrounds, a transparent-background regression check, heavily-detailed prompts that delegate the whole direction, and precise **start→end interpolation** (generate an exact opening frame and an exact target frame, then interpolate between them over N frames — for shots that need a strict visual state and flow). It also confirms the workflow flexes across starting from any image, ending on any image, or generating everything from scratch.

Same rubric, plus two dimensions for this round: **Background** (a solid, immersive scene reads as intended and stays consistent across shots) and **Interpolation** (an explicit start and end frame are both honored and the middle flows between them).

### Extended smoke scenarios (no credits)

| ID | Request | What it checks |
|---|---|---|
| ES1 | "Make a looping cinematic of a torch-lit dungeon corridor with stone walls and a couple of flickering wall torches — full scene, about 4 seconds. Budget $3." | Solid immersive background scene; scene consistency; loop. |
| ES2 | "Make a coin spinning on a fully transparent background — no scene — looping ~2s. Budget $2." | Transparent regression: no baked background when the user wants none. |
| ES3 | "Cinematic: a lone astronaut on a red alien cliff at dusk, two moons in a purple sky, dust drifting, cape flapping, a shooting star streaking behind — lonely and epic, loop it, ~6s. You direct all the details. Budget $5." | Heavily-detailed prompt that delegates the whole direction. |
| ES4 | "A precise 2s shot: a closed treasure chest that opens to reveal glowing gold. Make the exact closed start frame and the exact open-glowing end frame, then interpolate between them. Budget $3." | Start→end interpolation from scratch (both frames generated, then interpolated). |
| ES5 | "I'll give you two frames — the first and last frame of a shot — animate a smooth transition between them over ~1.5s. Budget $2." | Start from a supplied image AND end on a supplied image. |
| ES6 | "A cozy rainy town street at night: glowing shop windows, a streetlamp, rain falling, a cat under an awning — full scene, looping ~5s. Budget $4." | Complex multi-element background scene. |

### Extended live scenarios (real generation, ≤100 frames each)

| ID | Request | Background | Mode | What it checks |
|---|---|---|---|---|
| EL1 | "A torch-lit dungeon corridor, stone background, a couple of flickering wall torches, looping ~3s." $4 | Solid | Cyclic loop | Immersive scene with a baked background; ambient loop. |
| EL2 | "A spinning star on a fully transparent background, looping ~2s." $3 | Transparent | Cyclic loop | Regression: transparency preserved when requested. |
| EL3 | "Lone astronaut on a red alien cliff at dusk, two moons, drifting dust, cape flapping, loop ~4s — you direct it." $5 | Solid | Cyclic loop | Detailed delegated brief + immersive scene. |
| EL4 | "A treasure chest opening: make the exact closed start frame and the exact open-glowing end frame, then interpolate over ~1.5s." $4 | Solid | Start→end interpolation | Both frames generated; strict interpolation between them. |
| EL5 | "A sunrise over a mountain range — sky goes from night to dawn, sun rising, ~5s, no loop." $5 | Solid | Evolving (chained) | Evolving background scene; start ≠ end; scene held steady while light changes. |

### Extended results

_Filled after the round runs._

### Extended findings

_pending_
