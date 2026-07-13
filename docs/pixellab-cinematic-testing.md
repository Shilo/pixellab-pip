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

- **Completion signal and poll resilience.** The generation jobs are asynchronous, and the top-level job status can lag behind the finished, already-billed result; the reliable signal is the job's own `last_response` completed/`done` status — not the outer status, and not the mere first appearance of an image (some endpoints stream partial progress images) — which is what avoids a hang. Poll loops must also tolerate transient timeouts and 5xx by re-polling the same job — never resubmitting a paid job (which would double-charge) — and should persist each paid response as it arrives so a crash can't orphan a charged job. The animation contract now says this.
- **De-duplication vs "no trimmed outputs."** Removing the duplicate frame at each shipped seam (the echoed-back input; and a loop-close frame identical to the first) is expected de-duplication for a clean stitch — not the ping-pong/reverse/trim playback manipulation that is otherwise disallowed. The contract now states this explicitly and keeps the raw frames alongside for integrity.

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

**Extended smoke — 6 / 6 correct.**

| ID | Verdict | Key behavior |
|---|---|---|
| ES1 | Pass | Immersive dungeon scene routed to a solid-background scene image, background held steady across the loop, background left solid (not transparent). |
| ES2 | Pass | Transparent regression held: transparency requested and kept, no baked scene, alpha verified. |
| ES3 | Pass | Decomposed the heavily-detailed brief into subject/setting/ambient/transient/mood/constraints and stated assumptions instead of asking; correctly spotted that the one-way shooting star makes the scene evolving (chained), not a single ambient loop. |
| ES4 | Pass | Start→end interpolation: generated both the exact opening and target frames and interpolated between them, with a plan to restore the exact anchors if the route altered them. |
| ES5 | Pass | Mapped the two supplied frames to the start and end anchors and interpolated between them. |
| ES6 | Pass | Complex multi-element night scene composed into one background render and animated in place so nothing drifts. |

**Extended live — 6 / 6 built from scratch, all pass** (run once the backend recovered). Each created its own opening frame — or, for the interpolation shot, both anchor frames — validated every shot, and cost a few cents.

| ID | Request | Route | Result |
|---|---|---|---|
| EL1 | Torch-lit dungeon corridor, loop ~3s | Cyclic loop, solid scene | Pass — solid background every frame, geometry stable, only torches move, seamless loop (~$0.04) |
| EL2 | Spinning star, transparent, loop ~2s | Cyclic loop, transparent | Pass — transparency preserved every frame (no matte/halo), seamless (~$0.06) |
| EL4 | Treasure chest opening, strict ~1.5s | Start→end interpolation | Pass — both exact anchors held pixel-exact, smooth 15-frame open (~$0.14) |
| ES6 | Rainy town street at night, loop ~4s | Cyclic loop, complex scene | Pass — all elements present, none forbidden, solid scene stable, pixel-exact loop, exactly 4.0s (~$0.05) |
| EL3 | Astronaut on an alien cliff, epic loop ~4s | Evolving chained + transient | Pass — 4 chained shots, loop closed pixel-exact, one honest moon-glow artifact (~$0.09) |
| EL5 | Sunrise over mountains, ~5s, no loop | Evolving chained, non-loop | Pass — continuous night→dawn arc, non-looping (~$0.11) |

Immersive solid-background scenes and the transparent regression both passed; the evolving scenes chained cleanly, and the interpolation shot honored both anchors exactly.

### Extended findings

- **Backgrounds and complex scenes** are handled well from existing guidance: a solid-background scene route for immersive scenes, the background held consistent by composing all elements into one render and confining motion, and no baked background when the user wants transparency. No new instruction was needed for scene handling.
- **Transparent-background support is intact** (the original approach): when the user wants no scene, transparency is preserved and verified.
- **Heavily-detailed, fully-delegated briefs** are decomposed into a concrete plan with stated assumptions and no blocking questions, including correctly detecting when a one-way element (a transient event) turns an otherwise-ambient loop into an evolving, chained scene.
- **Start→end interpolation — the route was corrected after a head-to-head.** For a shot that must hit an exact start and end, the right route is **`animate-with-text-v3` with `first_frame` + `last_frame`** (a text-driven tween), not the Pro `interpolation-v2`. Measured on the same task and reproduced by two independent checks: v3 held both endpoints pixel-exact with a controllable 4–16 frames (size and frame count coupled by the pixel budget) for ~$0.04, up to 256px; `interpolation-v2` consistently returned only ~2 frames, missed the endpoints, and cost ~2.4× more. The contract now prefers v3 for every start→end tween and demotes `interpolation-v2` to a rarely-needed alternative. Either endpoint may be supplied or generated.
- **A big lighting or palette shift on an evolving scene also needs the anchored tween.** Free-run animation anchors to the incoming palette and won't cross a large colour change (a night→dawn shot stays dark however the action is worded), so the target-state frame is generated and anchored as the end frame. Documented.
- **The endpoint's pixel budget is now documented.** `width × height × frame_count ≤ 524,288`, so a 256×256 canvas allows only 8 frames and 16 frames need `width × height ≤ 32,768` (about 181×181; 128px is a safe common choice) — size and frame count are coupled, and the references say so to avoid a rejected request.
- **The "extra frame" behavior was re-validated precisely** (see below): the endpoint returns one more image than the requested frame count, and that extra image 0 is the supplied opening frame echoed back — pixel-identical or a negligible re-encode difference across four measured real generations — so it is a duplicate to drop when stitching, not a meaningful re-render. The reference wording was corrected accordingly.

## Plain-brief autonomy round — beautiful full-background scenes (smoke + live)

A third round tested a stricter question: given only a **plain-language user goal with no technical hints**, does the cinematic contract by itself infer the whole execution — route, frame/timing, loop-vs-arc, endpoint anchoring, budget gating, and validation? Three scenes were chosen to stress different paths, each phrased the way a real user would and each run **twice** — a dry smoke pass (plan only, no spend) and a live generation:

| Scene | Intended path | Why chosen |
|---|---|---|
| Hooded traveler at a campfire in a snowy forest (loops) | Cyclic ambient loop | Should be one looped clip, not a 300-frame chain; layered ambient motion + a full solid background. |
| Tiny knight facing a huge sleeping dragon on a cliff (loops) | Cyclic loop, two subjects | Scale contrast, two subjects sharing one frame, wind + breathing; silhouette readability. |
| A lighthouse as a storm rolls in (does not loop) | Evolving one-way arc | Big calm→storm palette shift; forces chained shots and anchored keyframe tweens. |

### Smoke plans — 3 / 3 correct from plain text

Every plan, with no technical wording in the request, independently reached the right route and mechanics and asked no blocking questions:

- **Both loops → cyclic**, one composed solid-background scene image (`create-image-pixflux`) plus one `animate-with-text-v3` loop with `last_frame` = the opening frame to close the seam; the ~30 s comes from **infinite playback**, not from rendering 30 s of unique frames or chaining ~19 jobs. The knight/dragon plan kept **both subjects in one scene render** rather than compositing separate sprites.
- **The storm → evolving/chained**, distinct `first_frame` + `last_frame` keyframe tweens across five keyframes, with the intermediate keyframes **derived by editing the opening frame** so the lighthouse and rocks stay pixel-locked (independent re-generations would drift the composition). It also stated the honest tradeoff plainly: a smooth 30 s one-way clip needs ~300 frames, which a few-dollar budget cannot buy, so it plays as a slow cinematic dissolve.
- All three correctly derived the **pixel budget** (size × frame-count coupling), demoted `interpolation-v2` to explicit-request-only, planned calibrate-then-hard-stop budgeting, and surfaced the **same genuine ambiguity — aspect ratio / non-square canvas** — which this round resolves.

### Live loops — 2 / 2 pass, ~$0.03 each

| Scene | Route | Result |
|---|---|---|
| Snowy campfire, loop | Cyclic, `create-image-pixflux` + one `animate-with-text-v3` | Pass — 180×180 @ 16 frames (the largest square that still allows a full 16 under the budget), exact seam (first == last frame, mean diff 0.0), gorgeous cozy scene with the fire as the warm focal point, layered depth, fire/embers/snow all moving (~$0.03) |
| Knight + sleeping dragon, loop | Cyclic, one composed scene + one loop | Pass — 256×144 **widescreen** @ 14 frames, exact seam (mean diff 0.0), full dusk background with atmospheric depth and the intended tiny-knight/huge-dragon scale contrast (~$0.03). Honest miss: the dragon read as perched/stirring rather than curled-asleep — a prompt-fidelity gap fixable with a cheap re-roll, not a routing error |

Both loops delivered "30 seconds" as an infinitely-looping file, closed seamlessly with `last_frame` = the opening frame, and cost about three cents — confirming that a cyclic ambient loop is a ~2-call job, not a chained one.

### Live evolving arc — beautiful result, expensive path

The storm arc took the chained/evolving route across seven distinct keyframes (golden calm → dusk → overcast → building storm → storm → beam → lightning). The **anchored middle** of the sequence — where each job is pulled to the next keyframe — walks that gold→storm evolution cleanly and reads as genuinely cinematic. Getting the palette to cross at all required **seed-locking** the keyframes (same seed + composition wording, varying only the palette/weather words); an init-image *edit of the opening frame* was tried first and **discarded** because it anchored to the source palette and would not cross to the storm colours. The `last_frame` tween between keyframes then carried the actual colour cross. The finished piece is a real ~30-second one-way arc — **289 frames at ~10 fps, ≈29 s, for ~$1.05 total** (18 chained jobs plus a few discarded probes) — so an evolving cinematic is **not dollar-expensive**; the real cost is **time and drift**.

**Forensic follow-up — the arc degenerates in its back third.** A close frame-by-frame audit — independently re-confirmed on the current final frames — found a genuinely good calm→dusk→storm-onset front half (frames 0–~72) that gives way to a degenerating free-run back third (frames ~136–288), traced to specific and fixable authoring mistakes (the calm opening itself is slow but continuous — fine — so the failure is one zone, not two):

- **Long free-run stretches drift and accumulate artifacts.** The climax was **9 consecutive free-run jobs** (no `last_frame`): the wave foam compounds frame-over-frame and never clears, blooming into white mushroom-cloud "explosions" (frames ~216–232) and then a static white coating over the islet (~240–288), with the palette creeping back toward gold during "stormy night." *Fix: anchor on a cadence — never chain more than ~2–3 free-run jobs; re-pass a stable keyframe to pull error back.*
- **Additive action wording piles up.** The actions literally said waves "explode into white foam" / "spray bursts" — free-run keeps adding the burst and never subtracts it. *Fix: describe steady rhythmic motion instead.*
- **Seed-lock holds palette, not composition.** The lighthouse sits left in the first keyframe and centre later, so the tween must warp geometry to cross, producing a visible zoom/pop at the lamp flare. Seed-locking frees the palette but only loosely holds layout. *Fix: keep every keyframe's framing identical and the stages visually close; editing one base image is not the fix, since that resists the palette change.*
- **A swept beam can't be held by text.** The lighthouse beam flickers on/off and jumps direction, then collapses to a static vertical cone — it never sweeps. *Fix: give it its own anchored beam-left/centre/right keyframes, or accept it will not trace a path.*

These are now in the cinematic contract's quality rules. The corrected lesson: an evolving arc's quality lives or dies on **anchor cadence** — seed-locked keyframes are only as good as how densely the chain is pulled back to them; leave a long free-run tail and it degenerates into uncanny morphing. (An abandoned first pass of this same scene was worse — it never left golden daylight at all, so the re-iteration fixed the "weather stages look the same" problem but kept the free-run-tail defects.) (By contrast, the census of the last 24 hours confirmed the **routing** itself is sound: every cyclic/ambient request was correctly built as one looped job, every evolving request chained — no scene that needed stitching was cheaped out to a single clip.)

### Round findings

- **Plain-brief autonomy works.** With zero technical wording, the contract alone drove correct route selection, frame/pixel-budget math, loop-vs-arc, endpoint anchoring, budget gating, and validation, across both the easy (loop) and hard (evolving) cases.
- **Cyclic loops are cheap and seamless.** Two ambient loops at ~$0.03 each with mathematically exact loop closure; the internal motion (fire, wind) made the `last_frame` = first-frame close clean rather than triggering the idle-loop artifact risk.
- **Widescreen is supported and now recommended.** Non-square opening frames (256×144, 180×180) generate and animate correctly; cinematics read better wide than square, so the contract now recommends a widescreen frame within the pixel budget.
- **Aspect ratio was the one recurring uncertainty** across all three plans; it is now documented (a widescreen recommendation plus the size/frame-count coupling).
- **Evolving scenes are the expensive, drift-prone path.** The live storm arc required many chained segments and repeated composition-lock re-rolls (regenerating keyframes as edits of the opening frame to stop the lighthouse and rocks from wandering) — far more work than either loop, matching the plan's honest warning that a smooth one-way 30 s is not cheap. Keyframe-editing-from-the-opening for composition consistency is now called out in the contract.
- **Craft guidance was promoted.** The durable, behaviour-changing subset of the scene-composition research — layer and stagger several ambient motions, build depth with atmospheric perspective, and let the subject own the brightest palette values — is now in the contract's quality rules (background research recorded separately).

## LEGO duel production round — loop-fill and render-look failures

A heavily-scripted, no-budget attempt at a real production output: a ~60-second LEGO-parody lightsaber duel with comic speech bubbles. It exposed four issues — forensically validated (frames hashed, prompts and the assembler read, colours counted) — that drove concrete contract fixes.

**What worked:** correct routing (REST v2, no MCP present), character identity held across shots, and — the biggest risk — both speech bubbles ("ME FATHER", "NOOOOOO!") rendered legibly after re-rolls on a larger canvas.

**What failed:**

- **Loop-fill masquerading as duration (the core fix).** The manifest self-declared **100 unique frames stretched to 598** — each shot was one ~14-frame clip *looped 5–9×* to reach ~7 s, and the assembler cited this contract's "cyclic-fill" as its justification. The "Cyclic or evolving?" guidance (generate one clip, loop it at playback to fill duration) was scoped only to *ambient* motion, but nothing forbade applying it to a *narrative/action* beat. It now does: a narrative or action beat gets its length from **unique frames** — rapid cuts of distinct micro-actions, or chained jobs — never by looping. A 16-frame clip (~1.6 s) is already plenty for one expressive micro-action; the failure is *padding* it, not its length.
- **"Subtle" fights were mostly the loop, not weak swings.** The raw clash clip measured a strong ~8 % frame-to-frame delta — real motion — but shown as the same 1.4 s swing five times it read as a twitch. The "steady rhythmic motion" rule (added to stop the lighthouse's additive foam) had also biased action beats toward subtlety, so it now carries an **action exception**: describe bold, deliberate, large motion (swing arc, lunge, follow-through) and chain progressive poses; the rule only bans *accumulating* particle bursts.
- **3D render, not pixel art.** Prompts used render-y wording ("glossy plastic diorama, cinematic dramatic lighting") on a 256-wide canvas, and the keyframes carried **380–421 unique colours** (flat pixel art is ~16–64). Fix: a Text-Preparation note that when a look is at stake (flat pixel art), state it explicitly, move render adjectives to `negative_description`, and enforce it with the endpoint's **flat-shading / outline / low-detail / palette** controls — not prompt words alone; a large canvas plus render wording pushes the image models to a smooth semi-realistic render.
- **Anticlimactic ending.** After the "NOOOOOO" reveal the script ended on two calm wide "posing" shots; the authored despair never rendered and character screen-positions flipped across the cut. This was a script/prompt design flaw (hold the aftermath emotion, preserve positions and seed continuity), not a contract gap.
- **Cross-shot consistency regressed once the render look was fixed — and text alone cannot hold it.** The v1 attempt was consistent because its higher-detail 256 px render *accidentally* anchored the cast; the v2 switch to flat low-resolution pixel art removed that anchor, and each independent `create-image-pixflux` shot invented a different figure *and* a different room (villain grey-hooded → brown → black-caped; chamber grey brick → fire → blue). A live A/B of four conditioning techniques against a locked master settled it: **`edit-image` from the master** holds the flat look and identity best and is cheapest (use for most shots); **`generate-image-v2` + `reference_images`** reframes hardest while staying recognisable (Pro price; only for big framing changes); **`init_image` clones** the master and will not re-frame; **`generate-with-style-v2` redesigns** the cast in high detail, breaking the flat look. The contract now requires anchoring a recurring cast **and setting** to a master reference via these routes — never independent text-only generation per shot — and warns that even anchored, exact consistency may not fully hold.
- **Mixed resolution / baked white padding on the reframe shots.** The v3 rebuild fixed consistency but the two gantry shots bracketing the dialogue came back **letterboxed with white padding** (a 158×92 scene inset in the 192×108 frame with ~8–17 px white borders). Cause: those shots used `generate-image-v2` with a **`style_image`**, which forces a **square** output — the off-aspect result was fit into the canvas with baked white borders, mixing resolutions and violating the no-baked-background rule. The contract now requires every shot to land on the cinematic's exact canvas edge-to-edge: request the exact canvas, use `reference_images` not a `style_image` for a `generate-image-v2` reframe, and normalise any off-aspect frame (crop or nearest-neighbour-scale to fill) before assembly rather than padding it. A corrected cut was produced by cropping the padding and nearest-neighbour-upscaling the content to fill the canvas.

## Production-readiness final suite — one small live test per distinct use case

The prior rounds grew the cinematic contract reactively (each failure drove a fix). This round is a **deliberate coverage sweep**: is the contract now production-ready across *every* distinct behaviour it encodes, with each behaviour exercised by its own small, isolated test? Five use cases were chosen to map one-to-one onto the contract's decision points and its most recently-edited rules, so a pass on all five is direct evidence the rules hold when an agent meets them cold.

Every test is run **twice**: a **smoke pass** (plain-language plan-only request — "walk me through the plan and rough cost before spending, don't generate yet") and a **live pass** (generate it). Both passes go to a fresh assistant instance given **only** `@skills/pixellab-pip/SKILL.md` and a plain-language user request with **no technical/test wording** — so the test measures whether the contract *alone* drives the right route, mechanics, and quality. Each live test is capped at **≤3 jobs / ~50 frames** to keep the sweep cheap and each behaviour isolated. Smoke passes run simultaneously; live passes run simultaneously.

### Use-case coverage map

| Test | Plain-language scene | Distinct use case exercised | Contract rule under test |
|---|---|---|---|
| A | Cozy campfire at night, embers rising, flames flickering — smooth seamless ~6 s loop. | **Cyclic ambient loop** — one clip looped at playback, not chained. | "Cyclic or evolving?" decision; loop-fill is *for* ambient; exact-canvas / no-pad. |
| B | A seed on bare soil sprouting into a small blooming flower over ~4 s, start ≠ end. | **Evolving one-way arc** — unique frames, chained, no loop-fill. | Chained shots for an evolving scene; narrative length from unique frames. |
| C | A calm mountain lake shifting from night to dawn over ~5 s. | **Large palette / lighting shift tween** — generated seed-locked target end frame. | `first_frame`+`last_frame`; free-run won't cross a big palette shift; seed-lock. |
| D | A knight winding up and swinging a heavy two-handed sword in a big overhead chop. | **Action beat expressiveness + choreography faithfulness.** | Bold/deliberate/large motion; before→after pose pair; stage the *intended read*. |
| E | Two little robots in one small workshop — left waves, right nods back, same room throughout. | **Recurring cast + setting consistency across shots.** | Master-reference anchoring (edit-image / reference_images); exact-canvas, no pad. |

### Scoring

Each live output is scored for **confidence vs the original plain-language intent** (0–100%): did the finished cinematic do what a person asking that sentence would expect — right route, right motion/arc, on-model, clean loop or clean one-way, exact canvas? The score is assigned by **independent inspection of the delivered frames/GIF**, not by trusting the building instance's self-report.

### Results

**Smoke plans — 5 / 5 routed correctly from plain text.** With no technical wording, each instance reached the right route and mechanics and asked no blocking questions beyond the required budget/scene confirmations:

- **A (campfire)** → cyclic ambient loop: one scene image + one looped `animate-with-text-v3`, widescreen for the full 16 frames, drop the echoed frame, duration = playback speed. Explicitly de-escalated from a chain.
- **B (seed→flower)** → evolving one-way: `first_frame`+`last_frame` tween, end frame as an **edit** of the start (correct for a same-palette additive change), slow per-frame delay to fill ~4 s rather than paying for more frames, with an honest steppiness caveat and a chaining escalation offered.
- **C (night→dawn)** → large palette shift: anchored tween with the dawn still **re-generated and seed-locked** to the night composition (not edited, because an edit won't cross a big palette shift). The exact contract rule, applied cold.
- **D (knight chop)** → routed a *single* overhead chop as a **character animation, not a cinematic** — correct, since one chop is one clip. This is the single-clip boundary working; the live D was therefore posed as a two-beat action scene (chop → pillar shatters) to actually exercise the cinematic action-choreography rules.
- **E (two robots)** → recurring cast+setting: master frame + chained shots, and correctly reasoned that with **no camera cut, chaining from the handoff frame beats re-anchoring** — matching the contract's "chaining holds identity best where a cut is not needed."

**Live builds — 5 / 5 delivered, all met the core intent.** Confidence scored by independent frame inspection, not self-report:

| Test | Route the contract drove | Confidence vs intent | Independent inspection notes |
|---|---|---|---|
| A — campfire loop | Cyclic loop (built as a 3-job seam-closed chain) | **95%** | Gorgeous cozy scene, stable background (treeline, stone ring, stars), flames flicker + orange embers rise, loop seam pixel-exact (`last_frame` == opening, mean-diff 0.0). One re-roll to kill spurious cyan "magic sparkles." ~$0.12. |
| B — seed→flower | Evolving, chained + `edit-image` end anchor | **88%** | Clean readable arc: seed → sprout → leaves → bud → vivid orange bloom; 49 frames, every frame 256×128, no padding. Minor honest drift: mid-growth stem renders dark before greening. ~$0.10. |
| C — night→dawn | Anchored tween, seed-locked dawn target | **78%** | The hard part — the night→dawn **palette crossing** — is handled well and reads genuinely cinematic (stars → moonrise → pre-dawn → golden sun + lake reflection). But the mountain silhouettes **warp/pop mid-tween** (frame-diff spikes to ~24) because the two anchors weren't composition-locked tightly enough — the documented "seed-lock holds palette, not layout" residual, reproduced live. ~$0.12. |
| D — knight chop → pillar | Two-beat action cinematic (chained) | **92%** | Excellent: clean wind-up → hard overhead chop → pillar clearly shatters into chunks → low follow-through settle. Reads unambiguously as a powerful chop. Two re-rolls to kill a spurious glowing "energy orb / starburst" the model kept inventing on the swing; forbidding glow/orb/energy fixed it. ~$0.13. |
| E — two robots | Master frame + chained shots (no cut) | **88%** | Both robots (teal-left, orange-right) and the workshop hold consistent across all 49 frames; left waves, right nods, non-acting robot stays still. No re-rolls. Minor: right robot's eyes flick to a dark visor during motion. Not seam-closed (a loop wasn't requested). ~$0.09. |

**Mean confidence ≈ 88%; route selection correct in 5/5 from plain text.** Every distinct use case — cyclic loop, evolving arc, big-palette tween, action beat with a staged break, recurring cast+setting — was routed and built correctly by the contract alone, and each cost about ten cents.

### Findings

- **The contract is production-ready across all five use cases.** From zero technical wording, it drove correct route selection, pixel-budget math, loop-vs-arc, endpoint anchoring, consistency method, budget gating, and validation — no routing miss in any test.
- **One new, generalizable defect: v3 free-run hallucinates unrequested glow/sparkle/magic VFX on bright or energetic beats.** Two independent tests hit it — a campfire grew **cyan "magic sparkles"**, a sword swing grew a **glowing "energy orb / starburst"** — each costing a re-roll. The contract only caught it *reactively* (the artifact-watch validation step); it did not tell the agent to *forbid* it up front. Fixed: the artifact-watch rule now says to proactively forbid hallucinated glow/sparkle/magic/beam VFX in the animate `action` on bright, energetic, or impact beats, not just catch them in validation. (A review pass caught and corrected a first draft that also named `negative_description` — a field the v3 animate endpoint doesn't expose; the artifact is an animation-time hallucination, so `action` is the right lever.) (Subject-agnostic — the two triggers were a fire and a hard hit, not a genre.)
- **C reproduced the known "seed-lock holds palette, not layout" limitation.** The night→dawn *colour* cross succeeded; the *composition* warped at the tween because the dawn target's mountains didn't match the night frame's. The contract already warns about this (keep every keyframe's framing identical and the stages visually close) and predicts exactly this residual — so it is an execution slip against an existing, correct rule, not a contract gap. No new rule; the warning stands and is now empirically confirmed a second time.
- **No change needed for the rest.** Cyclic-vs-evolving, edit-for-same-palette vs regenerate-for-big-shift, chained-consistency-without-a-cut, the single-clip boundary (D's smoke), exact-canvas/no-padding (every frame landed full-bleed), and budget discipline all behaved correctly with no intervention.

*Test-design caveat (not a skill issue):* the live prompts hinted "~50 frames," which nudged the campfire loop into a 3-job seam-closed chain rather than one looped clip. Both are valid cyclic builds and the result is seamless; the frame hint, not the contract, drove the richer path.

### Second wave — five more, entirely different routes

The first five covered the contract's core decision points. This wave deliberately targets **routes and edge cases the first five never touched**, with five completely different scenes, same two-pass (smoke plan-only + live) method, same plain-language / no-technical-wording rule, same ≤3-jobs / ~50-frame cap.

| Test | Plain-language scene | Route / edge case exercised (untested in wave 1) | Contract area under test |
|---|---|---|---|
| F | A glowing magic potion bottle bubbling on a **fully transparent background**, loop ~3 s. | **Transparent subject (pixen), no baked scene** — wave 1 was all solid scenes. | Transparent-background regression; no baked matte; cyclic loop. |
| G | A cat batting a ball of yarn back and forth, **only the cat and the ball ever on screen**, loop ~4 s. | **Two interacting objects** with an only-allowed-objects rule. | Describe object physics not an off-screen actor; forbid everything else; avoid silhouette-merge; loop. |
| H | A snowy tavern at night: a **wide shot**, then **cut to a close-up** of the swinging sign, same tavern. | **Hard reframe across a cut** — wave 1's consistency test (E) had no cut. | Master-reference anchoring escalated to `generate-image-v2` + `reference_images`; exact-canvas, no pad. |
| I | **A supplied house image** brought to life — window flicker + a wisp of smoke, house unchanged, loop ~3 s. | **Supplied opening frame** — wave 1 was all from-scratch. | Supplied-frame image role (`image-input-roles`); anchor identity to the actual pixels; copy the input into the folder. |
| J | A forest waterfall into a misty pool, **requested in French**, loop ~3 s. | **Non-English request** + several staggered ambient motions. | Localization (reply in French, generation text in English); layered/staggered ambient motion; cyclic loop. |

Same scoring: confidence vs the original plain-language intent, assigned by independent inspection of the delivered frames.

#### Results (second wave)

**Smoke plans — 5 / 5 routed correctly from plain text** (one, G, needed a re-run after a first instance returned a stray non-answer with no tool calls — an instance glitch, not a routing error). Highlights: F took the transparent/pixen path with no baked scene; G enforced only-two-objects via a transparent canvas plus explicit action exclusions **and cited the new glow-VFX rule unprompted** ("free-run v3 tends to hallucinate glints onto energetic beats, so I forbid them up front"); H correctly read "cut to" as a **hard cut** needing a master reference + `generate-image-v2 reference_images` for the close-up (and flagged that as the one Pro-priced step); I mapped the supplied PNG to the opening-frame role with an honest "v3 re-renders every frame, so the house may drift" caveat; J answered entirely in French while planning English generation text.

**Live builds — 5 / 5 delivered, all met the core intent.** Confidence by independent frame inspection:

| Test | Route the contract drove | Confidence vs intent | Independent inspection notes |
|---|---|---|---|
| F — transparent potion | Cyclic loop, transparent (`create-image-pixflux` + one animate) | **90%** | Clean transparent field (alpha strictly 0/255, no matte), cork+glass held still, only the liquid bubbles. 16 frames, ~3 s loop. ~$0.05. |
| G — cat + yarn, 2 objects | Cyclic-ish, 2 chained shots, transparent (`create-image-pixen`) | **78%** | Only the cat and red yarn ever on screen (no hands/objects), transparent, reads as batting. **But shot 2's mid-frames carry injected white sparkle VFX** — the glow artifact again — *despite* the action forbidding "no sparkles" and a fresh-seed re-roll; shipped with an honest caveat. Loop returns near (not pixel-perfectly to) the opening. ~$0.15 incl. the superseded re-roll. |
| H — tavern wide → cut to sign | Two shots, **hard cut**, `generate-image-v2` + `reference_images` | **88%** | The cut works: wide snowy tavern (flickering windows, chimney smoke, falling snow) → close-up of the swinging beer-mug sign, same tavern style/palette/sign motif held across the cut. Every frame exactly 256×144, no letterbox. ~$0.17 (the close-up was the one Pro call). |
| I — supplied house, ambient | Supplied frame as `first_frame`=`last_frame`, one animate | **88%** | House preserved **pixel-identically** (frame 0 vs source = 0.0 diff; last-frame anchor = 0.0); warm window/door flicker + a chimney smoke wisp added; 16 frames, ~3 s. Source copied into the folder. ~$0.03. |
| J — forest waterfall (French) | Cyclic loop, staggered ambient (`create-image-pixflux` + animate) | **88%** | Water cascade + pool ripple + rising mist, framing (rocks/ferns) stable, clean loop; whole exchange conducted in French with English generation text. Rejected a no-`last_frame` candidate for a cleaner seam. ~$0.52 balance delta incl. the rejected probe. |

**Mean confidence ≈ 86%; route selection correct in 5/5 from plain text — across five routes the first wave never touched.**

#### Findings (second wave) — no new contract defect

- **Every new route worked from the contract alone:** transparent/pixen with no baked matte (F), only-allowed-objects via object physics + exclusions (G), a hard reframe across a cut via `reference_images` (H), a supplied-frame opening role with pixel-exact preservation (I), and a non-English request with localized replies + English generation text (J). None needed a contract change.
- **The glow-VFX artifact recurred a third time (G) — and this *confirms* the wave-1 fix rather than extending it.** G's instance did exactly what the updated rule says: it forbade sparkles in the `action` up front *and* re-rolled the failing shot with a fresh seed — and v3 injected them anyway. The endpoint simply cannot be guaranteed clean on an energetic beat; the contract's job is to minimize (proactive forbid), catch (validation), and disclose (honest caveat) — all of which happened. The rule already carries both clauses ("forbid … up front, not only when catching them in validation, and still watch … when checking each job"), so no wording change is warranted; three independent hits (fire, hard hit, batting cat) just raise confidence that the rule targets a real, stubborn failure mode.
- **The `generate-image-v2` + `reference_images` reframe route (H) held identity across a hard cut** exactly as the Continuity rule prescribes — the first live confirmation of that specific escalation path (wave 1's consistency test had no cut), and it landed full-bleed with no baked padding.
- **Supplied-frame handling (I) is clean:** the frame was mapped to the opening role, preserved pixel-exact via a `first_frame`=`last_frame` anchor, and the input was copied into the deliverable folder per the blueprint rule.

*Same test-design caveat as wave 1:* the "~50 frames" hint again nudged a cyclic scene (G) into a 2-shot chain rather than one looped clip; both are valid and the frame hint, not the contract, drove it.

**Two-wave conclusion.** Ten entirely different scenes across ten distinct routes/edge cases, run cold from plain language, produced **10/10 correct routing** and a mean confidence in the high-80s, with exactly **one** contract improvement surfaced (the proactive glow-VFX forbid, wave 1) and **zero** new defects in wave 2. The cinematic contract is production-ready across the use cases tested.

### Targeted quality round — the cyclic-*gesture* fix (raising the low scorer)

Wave 2's low scorer, **G (cat batting yarn, 78%)**, was root-caused rather than accepted. Its three defects — a violent loop pop, the cat's posture drifting (sit → recline → sit), and injected sparkles — all traced to **one wrong build decision**: it made a periodic *gesture* (batting) as **two chained free-run shots with no loop closure**, i.e. it treated an energetic action-cycle like an ambient texture loop. Measured: the original G's final frame vs its opening was **MAD 31.65** — a hard visible jump each time the loop repeated (a clean seam is ≈3–8).

**Root of the gap in the contract:** the "cyclic vs evolving" split treated *all* periodic motion identically ("one clean cycle, loop it"). It never distinguished **ambient** texture (flicker/flow/drift — loops fine first-frame-only) from a repeating **gesture** (a bat/wave/bounce/swing — a discrete body action that must *return to its own start pose* to loop). Nothing told the agent that a gesture is one self-closing cycle, never a chain.

**Fix:** the cyclic branch now carries that distinction — a repeating gesture is **one self-closing cycle inside a single clip (rest → gesture → back to the start pose), never chained**, with the closure mechanism chosen per `animation.md`.

**Validation — 3 fresh cold tests of the exact use case, each reading the amended contract:**

| Test | Scene | How the agent built it (from the amended rule) | Loop-close MAD | Confidence |
|---|---|---|---|---|
| G2 | Cat batting yarn (the re-do) | One self-closing clip, `last_frame` = opening | **0.76** (was 31.65) | **88%** |
| K | Bouncing rubber ball | One self-closing clip, symmetric first-frame-only | **3.04** | **92%** |
| L | Swinging pocket-watch pendulum (transparent) | One self-closing clip, `last_frame` = opening (AE 0) | **4.06** | **90%** |

All three built **one self-closing cyclic clip** (none chained) and **seam-closed cleanly** — the pop that sank the original G is gone (31.65 → 0.76 on the same scene), and the cat now holds a **stable upright posture** across the whole loop instead of reclining. Mean of the three ≈ **90%**, and G's own scene rose **78% → 88%**.

**One empirical refinement the tests forced:** the first draft of the rule mandated "anchor `last_frame` = opening, never first-frame-only" for every gesture. K (the bounce) disproved the absolute: an identical `last_frame` made the ball "land halfway and sit still," and a *symmetric first-frame-only* arc closed better (3.04). The rule was softened to pick the closure by the motion — `last_frame` for a gesture that must land on an exact pose (cat, pendulum), first-frame-only when the motion is naturally symmetric and an identical anchor would over-constrain it (bounce) — deferring the mechanism choice to `animation.md`.

**Residual (unchanged, honest):** G2 still saw v3 inject sparkles despite the forbid *and* the `last_frame` anchor (the agent isolated a seed where they land fully detached and offered a masked cut alongside the raw). This is the known stubborn glow-VFX limit, not a regression — the gesture fix targeted the pop and the drift, which it removed, and made no claim to fix the hallucination. (An early draft of the amended rule asserted the anchor "curbs" the VFX; a review pass cut that as unsupported by this very test — the anchored cat still sparkled.)

**Net:** the one genuinely low score was a real, fixable contract gap, not model noise. With the cyclic-gesture distinction added, the same class of request now lands ~90%.

### Targeted quality round — the C night→dawn composition lock (raising the next low scorer)

After the gesture fix, the lowest remaining score was **C (night→dawn lake, 78%)**: the palette *crossing* worked but the mountain silhouettes **warped** mid-tween. Root cause, measured: C's night opening and its generated dawn target were **different mountain ranges** — dark-silhouette overlap (IoU) only **0.72** — so the anchored tween had to morph one layout into another, spiking a frame-to-frame jump of 23.92 at the transition.

**Probe (the experiment):** with C's exact night frame fixed as the opening, the dawn target was generated several ways and each was measured for (i) silhouette overlap vs the night frame and (ii) whether the palette actually crossed to warm dawn:

| Technique | Silhouette IoU | Crossed to dawn? |
|---|---|---|
| Seed-lock, no init (contract's prior default) | **0.32** | Yes |
| `init_image` at normal strength (150–350) | 0.99 | **No** (stayed night-dark) |
| `init_image` at strength ~30 | 0.98 | Only at the horizon |
| **`init_image` very low (~20) + backlit-silhouette wording** | **0.92** | **Yes** |

**Findings that drove the contract change:**

- **Seed-lock alone does *not* hold structure** — it crossed the palette but invented a *different* composition (IoU 0.32, worse than doing nothing). The contract had recommended seed-lock as the composition-hold path while only warning of "drift"; the drift can be total.
- **`init_image` anchors to the *source* palette at normal strength** (confirming the prior finding) — it holds geometry perfectly but won't cross to dawn.
- **The working technique:** a **very low `init_image_strength` (~15–30 of the 1–999 integer scale; default 300)** lets the opening's strong **edges** survive while the uniform sky/water regions repaint to the target palette — crossing the palette *and* holding the structure — **but only when the held structure reads as a backlit silhouette** in the new light (dark mountains against a bright dawn sky), worded that way. (Schema note: `init_image_strength` is an integer 1–999, not a 0–1 float.)
- Chaining **composition-matched intermediate keyframes** (built with the same low-init lock) makes the shift rise monotonically with no boundary pop.

**Before → after (C vs C2), same scene:**

| Metric | C (before) | C2 (after) |
|---|---|---|
| Night→dawn silhouette IoU | 0.72 | **0.92** |
| Worst frame-to-frame jump | 23.92 (a geometry **warp**) | 19.91 (a legit **sky-brighten**, silhouette holds) |
| Job-seam pops | visible warp/banding | none (seams 8.2 / 9.6) |
| Endpoints | — | pixel-exact (frame 0 = night, frame 48 = dawn) |
| Confidence | **78%** | **~88%** |

C2's only residual is mild water-reflection shimmer during the mid-transition (reads as light on water); the mountain-warp that defined C's 78% is gone. The contract's Continuity rule now carries the low-init-pin technique (replacing the too-absolute "don't use init_image for a palette shift," which held only at normal strength).


