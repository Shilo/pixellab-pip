# PixelLab 360° Rotation Spike — minimal-prompt turntable via v3 interpolation

Research question: **what is the shortest `action` phrase that makes `animate-with-text-v3`
produce a clean, seamless, constant-speed 360° turntable** of a front-facing character,
with a stiff body (no walk/idle physics), consistent colors, and consistent shape?

The endgame is a phrase so minimal it generalises to any character (then the character
description is appended). This spike isolates the phrase only; character wording is added
later once a winner is found.

---

## TL;DR — conclusions and the prompts to use

**A prompt CAN rotate a subject 360° from a single frame** (overturning this spike's original negative
conclusion, which only held for *minimal keyword* prompts). The lever is an explicit **trajectory prompt**,
not a magic keyword, and not the character description.

**① General MVP prompt — 360° from one frame** (`animate-with-text-v3`, `frame_count` 16, no seed,
`enhance_prompt` false; ~75% per run in config B, ~60% config A — regenerate 2–3× and keep the run that
closes the loop; swap "subject" for the subject's name to generalise):
> "Turntable: rotate the view around the still subject - front, three-quarter, side, back, full back,
> opposite side, back to the front. Subject stays in the same pose."

**② Constant-speed variant** (removes the end-slowdown; use **config A** = `first_frame` only, no
`last_frame`; `no_background: true`):
> "Turntable: the view orbits the motionless subject by an equal angle each frame, distributing the full
> 360 turn evenly - front 0, 45, 90 right side, 135, full 180 back view, 225, 270 left side, 315, back to
> front. Constant angular speed, no acceleration or deceleration. Subject stays in the same pose."

**③ Best all-in-one — 360° rotation + maximum stillness + subject identity (RECOMMENDED DEFAULT).** One
`action` gives a full turn, a rigid figurine-still subject, and (via the description) consistent invented
side/back views. Template — the two variables are `<OBJECT>` (the framing noun, repeated verbatim) and
`<subject_description>` (the subject; put any back-view detail inside it):
> "Turntable: rotate the view around a solid **`<OBJECT>`** depicting **`<subject_description>`** - front,
> three-quarter, side, back, full back, opposite side, back to the front. The **`<OBJECT>`** itself never
> moves; only the viewing angle changes."

Current leader: **`<OBJECT>` = "figurine"** (Batch 4I: 10/10 full rotation with a *minimal* description; round-2
tied figurine = toy figure = display model, and figurine leads the simplified round — user scoring pending).
**Keep `<subject_description>` minimal** — a long description degraded rotation (Batch 4H/4I). Example filled:
> "Turntable: rotate the view around a solid figurine depicting a frog on top of a turkey - front,
> three-quarter, side, back, full back, opposite side, back to the front. The figurine itself never moves;
> only the viewing angle changes."

Design rules (all reviewer-agreed): use **`depicting`** to demote the description's verbs to a *depiction*
(stops the model animating it); **one `<OBJECT>` variable, repeated verbatim**; **`solid` once** (not
repeated — protects held props); **no punctuation tricks** to demote the description (quotes/parens/brackets
backfire in caption-trained models); **avoid material/effect words** ("stone", "bronze", "ice/frozen") — they
add texture shimmer / VFX. **The object noun also *triggers* the rotation** — a plain description with no
object noun rotated only 1/5 (Batch 4F control).

**The three essential ingredients** (present in every winner, absent in every failure — wording beats length):
1. frame it as **the view/camera rotating around the subject**, not the subject moving;
2. the word **"turntable"** (+ "still / motionless / same pose") to suppress physics;
3. an **explicit view sequence that names the return**: front → ¾ → side → back → opposite side → **back to front**.

**Config choice:**
- **Config B** (frame as both `first_frame` and `last_frame`): best completion (~75%) and a seamless loop,
  but decelerates into the fixed end frame.
- **Config A** (start frame only): ~60% completion, no forced loop seam, but **even angular speed** (no
  end-slowdown). Pick B for a looping GIF, A for an evenly-spaced sprite sheet.

**Mandatory setup notes:**
- **`no_background: true` on a transparent input** — otherwise `animate-with-text-v3` repaints the subject
  (proven in `no-background-3way-20260813/`). Also yields a transparent output.
- **No seed** (seedless is per-draw random; a fixed seed dampened rotation strength in early batches).
- **Reliability ceiling ~75%** — regenerate 2–3× and keep the best draw.

**Alternative (endpoint-driven, not prompt-based):** `generate-8-rotations-v3` produces 8 clean directional
views with no prompt; interpolating between consecutive anchors gives a smooth, subject-agnostic 360 and a
16-direction sheet (Batches 2B–3). Use this when you want guaranteed rigid rotation and don't need the
single-frame/prompt-only path.

---

## Scope correction (2026-07-21, from user) — read before trusting the batches below

The user tightened the goal and flagged two methodology problems. These override earlier framing:

1. **Fixed seed was a confound.** Batches 1–3E all used `seed: 726361` (to hold composition
   constant across phrases). But a single fixed random draw can itself be a non-rotating one, so a
   negative result does not prove "no phrase rotates" — only "not with this seed." **All repeat
   tests must send NO seed** (PixelLab randomises), and each phrase should be sampled across
   several seedless runs. For identical-anchor config the zero-motion is likely geometric, but it
   is retested seedless anyway to be sure.

2. **Only a single south frame is a valid input.** The goal is an MVP **prompt** that rotates from
   one south frame — used *either* as start-only *or* as start+end (both = the same south frame).
   Multiple jobs are allowed, but **every job's input images must be only that original south
   frame** — nothing derived. This makes several earlier batches **out of scope** for the MVP-prompt
   question (still valid as background, but not answers to it):
   - **Batch 2B `generate-8-rotations-v3` and `/rotate`** — these ARE the rotation primitives we are
     trying to *replicate*, not use.
   - **Batch 3 (interpolate adjacent anchors)** — the rotation comes from two *distinct* directional
     frames as first/last, i.e. it is driven by the visual endpoints, not the prompt, and those
     anchors came from `generate-8-rotations-v3`. Invalid as a prompt test.
   - **Batch 3D generalization** — uses freshly *generated* subjects (not the one south frame).
   - **Batch 3E chain** — clip 2's input is clip 1's back frame (a derived input).

Valid configurations for the MVP-prompt search (tool = `animate-with-text-v3`, v3, **no seed**):
   - **Config A — start-only:** `first_frame` = south, no `last_frame`.
   - **Config B — start+end:** `first_frame` = south, `last_frame` = the same south frame.

Success test for a "real 360" (not a morph): the one-sided red mask/horn x-centroid must sweep to
the **opposite** side (~±20 px) **and return to the front** (last-frame x back to ~+8), as the true
`generate-8-rotations` loop does (start +8 → min −18 → last +10). A run that crosses to the back but
**ends** at the back (last x ≈ −12) is a **180° turn, not a 360** — the one-sided mask is on the far
side at 180° too, so "crossed to the far side" alone is not sufficient; the trajectory must come back.

## Batch 4A — seedless repeat (2026-07-21): does removing the seed unlock a 360?

Approved seedless rerun. 22 phrases × 2 valid single-south-frame configs (A start-only, B start+end),
**no seed**, `animate-with-text-v3`, `frame_count` 16. Artifacts: `4A_seedless/`, `seedless_scores.json`.

Results (44 runs, verdict = red-mask trajectory):

| verdict | count | |
|---|---|---|
| PASS (true 360) | **0** | no run crossed to the back **and** returned to front |
| HALF-180 | 2 | config A `turning around`, `turn all the way around` — clean ~180° to a back view |
| PARTIAL | 5 | mostly config-A turn-family (partial/wobble) |
| FAIL | 37 | frozen/minimal |

Config A: 2 HALF-180, 4 PARTIAL, 16 FAIL. Config B: 21 FAIL + 1 marginal — identical anchors stay
frozen regardless of seed, confirming the zero-motion is geometric, not a seed artifact.

**Was the seed the blocker? Two-part answer:**
- **Motion magnitude — yes, the seed dampened it.** Seedless `turning around` (config A) reached the
  back cleanly: motion 0.054, x-sweep +9.5 → −13.0. The *seeded* equivalent (Batch 2A) was far weaker
  (motion 0.016, turn_signal 0). So the fixed seed was suppressing rotation strength — the earlier
  seeded batches understated what the prompt could do.
- **The 360 itself — no.** Even seedless, every run caps at ~180° (front→back); none return to front.
  Trajectory of the best run, A_17 `turning around`:
  `+8 +8 +9 +9 +9 … +9 +2 −1 −8 −12 −13 −13` → holds front, then snaps to back and **stays** (180°,
  back-loaded speed). "turn around" = "face the opposite way" = 180°, and a single 16-frame clip from
  one frame has no anchor to rotate back to.

**Verdict:** a single south frame + prompt cannot produce a true 360 on `animate-with-text-v3`,
seeded or seedless. Config A → 180° ceiling; config B → geometric freeze. The seed affected turn
*strength*, not the *360 ceiling*.

> ⚠️ **Corrected by Batch 4B.** This verdict only holds for *minimal* prompts. With a verbose
> trajectory prompt, **config B does reach a full 360** — the "geometric freeze" applies to short
> prompts, not to a prompt that describes the whole rotation path. The 180°/freeze ceiling was a
> prompt-content limitation, not a hard limit of the endpoint.

Open single-frame idea not yet tried (still obeys "input = only the south frame"): run TWO config-A
jobs from the same south frame with opposite turn directions (e.g. `turn around clockwise` vs
`turn around counter-clockwise`), then compose clipA(front→back) + reverse(clipB)(back→front) into a
360. Requires (a) the model to honour turn direction and (b) both to reach a matching back view;
frame-reversal is a playback manipulation to flag before shipping.

## Batch 4B — MAJOR CORRECTION: a verbose prompt DOES give a true 360 from one frame (config B)

The earlier "no single-frame prompt can rotate" conclusion was **wrong — it only tested *minimal*
prompts.** The user produced a full 360 in Aseprite ("interpolate new" = `animate-with-text-v3`) from
a single frame used as **both start and end**, with a long trajectory-describing prompt. Reproduced
here through the REST API. Artifacts: `pixellab-pip-generations/frog-turkey-360-20260721/`.

Setup: user's `frog-turkey-input-128px.png` as `first_frame` **and** `last_frame` (config B),
`animate-with-text-v3`, `frame_count` 16, **no seed**. Metric: green-frog visibility (front = high,
back ≈ 0); FULL-360 = drops to back **and** recovers to front.

> Reference-file correction (2026-07-21): the user's true Aseprite success is `USER-aseprite-success.gif`
> (green 468 → 0 → **436**, a clean full return to front — with an end frame). An earlier file used as
> the reference, `USER-aseprite-startonly-flawed.gif` (green 468 → 2 → **124**), was a **start-only**
> attempt that only partially returns — flawed, not a full 360. The two exports independently confirm the
> config split: **with an end frame → clean 360; start-only → partial.** Conclusions are unchanged (the
> API reproductions were scored independently and are genuine FULL-360s); only the displayed reference gif
> was swapped to the correct one.

The winning prompt (774 chars, verbatim):
> "The frog riding the turkey remains completely motionless in the same pose while the sprite view
> rotates around them in a full turnaround. Treat this like a character turnaround sheet animated in
> sequence: show the frog-and-turkey pair progressively from the current front-facing angle, to
> three-quarter view, to side view, to back three-quarter view, to full back view, then around the
> opposite side and back to the starting angle. The frog stays seated on the turkey the entire time,
> and both the frog and the turkey keep the same pose, posture, and relative position. Do not animate
> walking, flapping, bouncing, swaying, or extra movement. The only motion should be the viewing angle
> changing smoothly around the frog riding the turkey, like a turntable character showcase."

Results (25 runs, config B, seedless):
- **Verbose prompt: 3/3 FULL-360** (green 223 → 0 → 223) — a clean, complete turntable, reproducible.
- **All 22 MVP prompts: FAIL** (green barely dips) except "turning around" = one PARTIAL. The minimal
  phrases that failed in every earlier batch fail here too.

Corrected conclusions:
1. **Config B (start == end == one frame) is NOT geometrically frozen.** It is frozen only for minimal
   prompts. A prompt that explicitly narrates the whole path (front → ¾ → side → back → opposite side
   → back to start) drives a full 360 even with identical anchors. The identical end frame is what
   *closes the loop*; the prompt supplies the trajectory.
2. **Aseprite was not the factor** — the public REST endpoint reproduces the 360 identically.
3. **Seed was not the factor** either (seedless here; 3/3).
4. **The factor is prompt content:** an explicit multi-view turntable description with a return-to-start
   clause, framed as *the view/camera* rotating around a *motionless* subject.

This overturns the headline "there is no MVP prompt". There IS — it is just not *minimal-keyword*; it
is a *structured trajectory* prompt. Batch 4C searches for the shortest such prompt that still works.

## Batch 4C — smallest working prompt (config B, frog, seedless, success = green-frog FULL-360 rate)

Seedless output is random per run, so candidates are scored by **success rate** over multiple runs,
not a single binary. Artifacts: `ladder_scores.json`, `ladder2_scores.json`, `refine_jobs.json`,
`refine2/`.

Reliability vs length (4 runs each unless noted):

| prompt (abbrev) | chars | FULL-360 rate |
|---|---|---|
| user's original | 774 | reliable (3/3 in Batch 4B) |
| C344 (full sequence + framing) | 344 | 75% |
| **T164 "Turntable: rotate the view around the still subject - front, ¾, side, back, full back, opposite side, back to the front. Subject stays in the same pose."** | **164** | **6/8 ≈ 75%** (confirmed) |
| T150 (drop "full back") | 153 | 2/3 ≈ 67% |
| T130 (drop the pose clause) | 132 | 2/3 ≈ 67% |
| C171 (turntable + sequence) | 171 | 50% |
| T113 (minimal sequence) | 113 | 1/3 ≈ 33% |
| C210 ("the camera orbits all the way around it…") | 210 | 0% |
| C124 / C102 / C063 | ≤124 | 0–25% |

**Winner: T164 (164 chars, ~75%)** — as reliable as the user's original 774-char prompt at ~1/5 the
length. It compresses to ~130 chars at ~67% (drop "Subject stays in the same pose" or "full back");
below ~130 chars reliability falls off (T113 33%).

Findings:
- **Wording beats length.** C210 (longer) fails where C171/T164 (shorter) succeed — it drops the
  "turntable" framing and the tight view sequence.
- **The essential ingredients** (present in every winner, absent in every failure):
  1. frame it as *the view/camera rotating around the subject* (not the subject moving);
  2. the word *turntable* (and/or "motionless / same pose") to suppress physics;
  3. an *explicit view sequence that names the return*: front → ¾ → side → back → opposite side →
     **back to the front**. Compressing or dropping this sequence is what breaks it.
- **Reliability has a ceiling.** Even the best prompts are ~75% over 8 runs, never a guaranteed
  100% — seedless generation sometimes stops short of closing the loop. Practical use: pick the
  prompt, generate 2–3 times, keep the run that closes.

**MVP prompt (single frame → 360, config B, no seed) — final:**
> "Turntable: rotate the view around the still subject - front, three-quarter, side, back, full back,
> opposite side, back to the front. Subject stays in the same pose."

164 chars, ~75% per run. Substitute the subject's own name for "subject" and this generalises. Use
the frame as both `first_frame` and `last_frame`, `frame_count` 16, no seed; regenerate 2–3× and keep
the run that closes the loop.

**Start-only works too (config A).** Re-testing T164 with `first_frame` only (no `last_frame`) scored
**3/5 ≈ 60%** FULL-360 — vs 6/8 ≈ 75% for config B. So the end frame *helps* reliability but is **not
required**: a prompt that names the return ("back to the front") drives the loop closure on its own.
The user's earlier flawed start-only Aseprite export was one unlucky draw, not a config-A ceiling.

Reproduction request (config B — the frame is used as BOTH anchors):
```
POST /v2/animate-with-text-v3
{
  "first_frame":    { "type": "base64", "base64": "<subject front frame>", "format": "png" },
  "last_frame":     { "type": "base64", "base64": "<the SAME frame>",      "format": "png" },
  "action":         "Turntable: rotate the view around the still subject - front, three-quarter, side, back, full back, opposite side, back to the front. Subject stays in the same pose.",
  "frame_count":    16,
  "enhance_prompt": false
}
```
(no `seed`.) The investigation also used two bare configs — Config A = start-only (omit `last_frame`),
Config B = start+end (both anchors the same frame). Only config B + a trajectory prompt yields a true
360; config A tops out at ~180°.

### Why it works — it is context, not character count

The user's challenge is correct: **length is a proxy, the real driver is context.** The evidence in
this spike says length is not causal — C210 (210 chars) scores 0%, while T130 (132 chars) scores 67%.
A longer prompt lost to a shorter one because it dropped the right context.

What actually matters is *which information the prompt supplies to the interpolator*:

- `animate-with-text-v3` interpolates between `first_frame` and `last_frame`, steered by `action`. With
  config B the two anchors are identical, so the unguided default is the shortest path = **no motion**.
- A minimal prompt ("360", "turntable", "spin") is a **label**, not a path. The model has no per-frame
  target, so it stays put or wobbles. It cannot expand a one-word label into 16 intermediate poses.
- The winning prompt supplies three pieces of context the label lacks:
  1. **a frame of reference** — *the view/camera* rotates, the subject is *still* → the model animates
     the camera, not the character's limbs (kills physics);
  2. **explicit intermediate keyframes in words** — front → ¾ → side → back → opposite side → front.
     This is effectively text-keyframing: it tells the interpolator *where to be at each stage*;
  3. **an explicit return** — needed because start == end, so the loop must go all the way around.
- Remove any one of these and it fails, regardless of length. "turntable character showcase" alone
  (35 chars) fails — no keyframes. C210 fails at 210 chars — it says "orbit all the way around" but never
  *enumerates the views* and drops the word "turntable".

Why length still *correlates* with success: the required context — especially the enumerated view
sequence — simply takes a minimum number of words to state. Below ~130 chars you physically cannot fit
"camera rotates around a still subject + the full front→…→back→…→front sequence", so short prompts fail
by **omission**, not by being short. The ~130-char floor is "the fewest characters that still carry all
three ingredients", not a length threshold the model reacts to. Pack the ingredients denser and a short
prompt works; pad a prompt with the wrong words and a long one fails.

## Batch 4D — constant-speed investigation (2026-08-13): the turn slows near the end

New question from the user: the winning turntables (T164 / the 774-char prompt) **decelerate near the
end** — the rotation should be a constant angular speed between every frame. This batch isolates what
controls per-frame speed. Artifacts: `frog-turkey-360-20260721/constant-speed-20260813/` (round 1 =
folder root; rounds 2–4 = `nobg-true/`), `report.json`…`report4.json`.

**Fidelity prerequisite — `no_background: true` is mandatory here.** The frog input is transparent, and
on a transparent input `animate-with-text-v3` with `no_background` unset/`false` **repaints the subject**
(the turkey wattle turns white) — proven in `no-background-3way-20260813/`. Round 1 omitted it (so those
frames are compromised for fidelity); rounds 2–4 all send `no_background: true`, which both preserves the
subject (front wattle-red = 1473 on every run) and returns a genuinely transparent background. The
wattle-red dropping to ~870–1014 on the *completing* runs is the head genuinely turning away, not
corruption — the under-rotating runs keep red ~1430 because they never present the back.

**Metrics.** Per-frame motion = mean abs pixel diff to the previous frame. `cov` = its coefficient of
variation (lower = more constant). `tail/head` = mean(last 4 diffs) ÷ mean(first 4 diffs): **<1 = slows
at the end** (the reported problem), **>1 = speeds up at the end**, **≈1 = even**. `full360` = green-frog
drops to the back (≤30% of front) **and** recovers (≥60%). Caveat: pixel-diff is not pure *angular*
speed — the side↔back transition inherently changes more pixels per degree than the near-front views, so
`cov` never reaches 0 for a genuine turn; `tail/head` is the cleaner read on the specific end-slowdown.

Wordings tested:
- **S2 (degree waypoints):** "…orbits the motionless subject by an equal angle each frame, distributing
  the full 360 turn evenly - front 0, 45, 90 side, 135, 180 back, 225, 270 opposite side, 315, back to
  front. Constant angular speed, no acceleration or deceleration. Subject stays in the same pose."
  (**S2b** = same with "full 180 back view" + left/right side labels.)
- **S3 (velocity prose):** "Turntable spinning at constant angular velocity … the same fixed number of
  degrees every single frame …" — no enumerated waypoints.
- **M1 (proven T164 view-sequence + even clause):** "Turntable: rotate the view around the still subject
  by the same angle in every frame, an even constant speed all the way around - front, three-quarter,
  side, back, full back, opposite side, back to the front. Subject stays in the same pose."

### Results by round

| round | config | wording | full-360 | cov (↓ even) | tail/head (≈1 even) |
|---|---|---|---|---|---|
| 1 | B (no nobg) | S2 degrees | near-miss | **0.216** | **1.013** |
| 1 | B (no nobg) | S3 velocity prose | ✓ | 0.633 | 0.768 (slows) |
| 1 | B (no nobg) | S1 T164+"no easing" | ✗ | 0.609 | 0.613 (slows worst) |
| 2–3 | B, nobg:true | S2 / S2b degrees | **1/6** | ~0.17–0.36 | even *when* it lands |
| 3 | B, nobg:true | M1 views+even | **2/2** | ~0.32 | 1.471 / 0.653 (inconsistent) |
| 4 | **A**, nobg:true | **S2b degrees** | **2/2** | **0.21 / 0.24** | 1.47 / 1.59 (mild speed-up) |
| 4 | A, nobg:true | M1 views | 0/2 (under-rotates) | 0.10 / 0.15 | ~1.0–1.3 |

### What controls per-frame speed

1. **Enumerating evenly-spaced *degree* waypoints (S2/S2b) flattens the speed;** prose like "constant
   angular velocity" (S3) does not — S3 rotates fully but rushes the back and eases the ends (0.768).
   The model needs the even *keyframe targets*, not an adjective.
2. **The end-slowdown tracks config B's fixed `last_frame` — observed, mechanism inferred.** Every
   config-B full-360 decelerates at the end (last 2–3 per-frame diffs taper, e.g. config-B S2b_r2 ends
   `…9.72, 7.5, 4.63`; tail/head ~0.6–0.9), and **config A does not** (config-A S2b ends `…15.08, 15.94`;
   tail/head ~1.0–1.6). That config split is the hard evidence. The *reason* is an inference, not proven:
   the most parsimonious explanation is that a fixed identical end anchor is a boundary condition the
   trajectory must converge onto, so it slows as it arrives — the same way any interpolation settles onto a
   fixed endpoint. **This is not a claim about PixelLab's internal pipeline or any deliberate "ease-out"** —
   we have no visibility into their algorithm and cannot say they intentionally decelerate. All we can state
   is the empirical config-dependent behavior and remove the anchor (config A) to avoid it.
3. **Completion vs config flips with wording:**
   - **Config B:** view-sequence (M1) completes reliably (2/2) but times unevenly; degree-waypoints
     (S2/S2b) under-commit to the turn (1/6).
   - **Config A:** degree-waypoints (S2b) complete reliably (2/2) *and* give the lowest `cov` of any
     genuine full-360 (0.21–0.24); view-sequence (M1) under-rotates to ~½ (0/2).
4. **Residual:** config A + S2b trades the *slowdown* for a mild *speed-up* at the very end
   (tail/head ~1.5), but overall variation (`cov`) is the best measured and there is no dead, decelerating
   tail — far less objectionable perceptually.

### Recommendation (constant-speed 360)

Pick by what you need — you cannot get both a pixel-perfect seamless loop **and** perfectly flat speed
from a single 16-frame `animate-with-text-v3` clip:

- **Evenest angular speed (sprite sheet / turntable):** **config A** (`first_frame` only, **no**
  `last_frame`) + the **degree-waypoint prompt (S2b)** + `no_background: true`. Best `cov`, no
  end-slowdown, reliable completion. Trade-off: the final frame lands *near* front but not pixel-identical,
  so a perfect loop seam isn't guaranteed (fine for an evenly-spaced sheet).
- **Seamless loop (looping GIF):** config B (frame as both anchors) + a trajectory prompt; accept the
  mild ease-into-the-anchor at the end, and regenerate 2–3× keeping the evenest closing draw.
- Either way: `no_background: true`, `frame_count` 16, no seed, `enhance_prompt` false; regenerate 2–3×
  (seedless completion is ~per-draw, not guaranteed) and keep the run whose playback reads as even.

**Constant-speed prompt (S2b) — verbatim:**
> "Turntable: the view orbits the motionless subject by an equal angle each frame, distributing the full
> 360 turn evenly - front 0, 45, 90 right side, 135, full 180 back view, 225, 270 left side, 315, back to
> front. Constant angular speed, no acceleration or deceleration. Subject stays in the same pose."

## Batch 4E — maximum stillness: make the subject a rigid "figurine" (2026-08-13)

New goal from the user: not speed, but **stillness** — the subject should rotate like a statue/figurine
with little-to-no movement in face, limbs, mouth, or weapons. Technique tested: keep the MVP turntable
prompt but **positively frame the subject as a rigid object** (statue, figurine, inanimate, …) so the model
never tries to animate it — positive prompting only, no "do not move" negatives. Artifacts:
`frog-turkey-360-20260721/stillness-20260813/` (round 1, all 10) and `stillness-20260813/confirm/`
(top-3 + control × 3). Base = T164 turntable + "back to the front"; only the subject noun + a one-sentence
object clause vary. config B, `no_background: true`, seedless, `frame_count` 16.

**Metric.** `area_jerk` = std of the second difference of the per-frame silhouette area (opaque-pixel count),
normalised — a proxy for high-frequency flail (flapping wings, shifting limbs) on top of the smooth
rotation. Lower = stiller. Backed by **visual montage inspection** (every-other-frame strips) because a pure
metric can't fully separate wanted rotation from unwanted deformation.

Round 1 (10 framings, 1 run each) then a 3-run confirmation of the leaders:

| framing (positive object clause) | full-360 | mean area_jerk (↓ stiller) | verdict |
|---|---|---|---|
| **"figurine"** — *solid molded figurine on a rotating display stand, completely rigid* | **3/3** | **0.044** | **winner — ~2.4× stiller than control** |
| "inanimate subject" — *completely inanimate frozen object, one fixed pose* | 2/3 | 0.081 | mediocre — the lone early run (0.048) was luck; the 3-run mean is worse than "collectible" |
| "collectible figure" — *solid collectible display figure on a spinning base* | 3/3 | 0.066 | beats control |
| "bronze sculpture" / "resin model" | 1/1 | 0.043 / 0.061 | moderate (single runs) |
| control (plain T164, "still subject") | 3/3 | 0.106 | most flail (turkey tail/plumage flares) |
| "action figure" | 1/1 | 0.077 | ≈ control |
| **"stone statue"** | 1/1 | 0.094 | **worse than control** — material shimmer |
| **"ice sculpture / frozen"** | 1/1 | 0.160 | **worst — adds literal blue ice-swirl VFX** |
| "statue figurine" (COMBO, many stillness words) | ✗ under-rotated | — | too many constraints suppressed the turn |

Findings:
1. **Positive object-framing works — but only the right word, and "figurine" specifically wins.** Framing
   the subject as a *figurine* (best) or *collectible* roughly halves the unwanted movement vs the plain MVP,
   with no negative prompting. Notably **"inanimate" is not it** — over 3 runs it fell to 2/3 completion and
   only average stillness (0.081); its one strong early run was luck. Don't assume the most literal word wins;
   "figurine" (a *manufactured object on a stand*) beat every other framing on both completion and stillness.
   Visual check confirms the winner: the frog stays seated, sword + shield held constant, and the turkey's
   feet/wings/tail locked, where the control's turkey tail visibly flares and shifts.
2. **Material/effect words backfire.** "ice sculpture / frozen" makes the model render *ice effects* (blue
   swirls animating around the subject) — the opposite of still. "stone statue" adds texture shimmer. So the
   trick is to imply *a manufactured rigid object*, not a material with its own visual connotations.
3. **Don't over-stack.** Piling many stillness clauses (COMBO) suppressed the rotation itself
   (under-rotated). One clean object clause is enough.
4. **Best is a single positive clause: "figurine".** Winner prompt (3/3 full-360, stillest):
   > "Turntable: rotate the view around the figurine - front, three-quarter, side, back, full back, opposite
   > side, back to the front. It is a solid molded figurine on a rotating display stand, completely rigid,
   > holding one fixed pose."

   Generalise by naming the subject: "…around the <subject> figurine - … It is a solid molded
   figurine on a rotating display stand, completely rigid, holding one fixed pose." Still ~75% completion
   (regenerate 2–3×), and it composes with the config choice from Batch 4D (config B for a seamless loop).

### 4E follow-up (2026-08-13) — LOW SAMPLE, not a conclusion; larger round planned

**Caveat (read first).** Batch 4E is **1 run per term** (round 1) plus ≤3 for the four confirmed terms —
far too low to conclude; seedless RNG dominates at this scale. "Figurine wins" is a **lead, not a verdict.**
A 10-run-per-keyword round is required before declaring a best keyword.

**Interactive scoresheet:** `.local/stillness-scoresheet.html` — every output frame of every run, per keyword,
with manual 1–5 scoring on three axes (**360 rotation / stillness / stays-itself**) and a live leaderboard.
**Human visual scoring is weighted above the auto-metrics** — a person spots identity morphs, weapon
duplication, and texture artifacts that the silhouette-jerk proxy cannot. The "stays-itself" axis explicitly
does **not** penalize guessed side/back views (a missing-description side-effect, not an identity failure).

**Keyword triage for the 10-run round (user's calls, validated):**

| keyword | decision | reason |
|---|---|---|
| COLLECTIBLE | keep | clean object framing, low flail |
| FIGURINE | keep | current lead |
| STATUE | keep | retest — material wording softened to "a solid statue" (drop "stone/carved" that caused shimmer) |
| ACTIONFIGURE | keep | plausible, retest |
| INANIMATE | keep | retest — early lift (0.048) was luck; fell to 2/3 on confirm |
| control (plain) | drop* | baseline only, no explicit framing |
| SCULPTURE (bronze) | drop | material word → shine/detail artifacts |
| RESIN3D | drop | niche jargon, weak model prior |
| COMBO (stacked) | drop | double descriptions → under-rotated |
| FROZEN (ice) | drop | adds literal blue ice-swirl VFX |

*Pushback kept on record: a **description-only control** (subject described + rigid clause, no object noun)
belongs in the round, to separate "the object word helped" from "the description helped." Pending user call.

**Round-1 human scores (recovered 2026-08-14; weighted above the auto metrics).** The user scored the 10
round-1 arms by eye (absolute quality on 1 run each — a *different* rule from round 2's per-output pass count).
Full scores (each 1–5; stored at `.local/round1-human-scores.json`, seeded into the scoresheet):

| arm | rotation | stillness | stays-itself | total | user's note (condensed) |
|---|---|---|---|---|---|
| COLLECTIBLE | 5 | 3 | 4 | **12** | all rotate; **bounce at the end**; equipment persistent — best rotation |
| FIGURINE | 3 | 5 | 3 | **11** | failed 1/4 to rotate; very still (some eye-blink); equipment stretches/switches hands — **best stillness** |
| STATUE | 3 | 4 | 4 | **11** | few tests; rotated fine, stiff, stays itself — retest |
| COMBO | 4 | 4 | 3 | **11** | fully rotates but **double-sided** for no reason; bounces — retest |
| ACTIONFIGURE | 3 | 4 | 3 | **10** | only 1 test; stiff — retest |
| RESIN3D | 1 | 4 | 4 | **9** | doesn't fully rotate; niche word — not worth retesting |
| INANIMATE | 1 | 3 | 4 | **8** | **none rotated**; low stillness; spontaneous details |
| FROZEN | 2 | 4 | 2 | **8** | ice particle FX; not a full rotation; bouncing — drop |
| control (B0) | 2 | 2 | 2 | **6** | failed 1/4 to rotate; constant micro-movement; morphs shield/feathers |
| SCULPTURE | 1 | 3 | 2 | **6** | doesn't fully rotate; morphs + bounces — drop |

Key human corrections to the auto read:
- **INANIMATE did NOT rotate** in any round-1 run per the human — the auto metric over-counted "full-360"
  from the green dip; human rotation = 1. (The round-2 template later *did* get inanimate rotating 4/5, so the
  description + object framing fixed what round-1 could not.)
- **FIGURINE = best stillness** (5/5) but failed to rotate 1/4 and showed minor eye-blink; held equipment
  sometimes **stretches or switches hands** — an identity issue the round-2 `<subject_description>` targets.
- **COLLECTIBLE = best rotation** (all rotated) but has a **"bounce at the end"** — this is the config-B
  end-anchor ease from Batch 4D, seen here by eye. The bounce and hand-switching recur across arms.

**Self-challenge — where my metrics disagreed with the human, the human is right.** The user's scores expose
concrete failures in my auto proxies, and they override my earlier auto-based claims:
- **The `full-360` flag over-counts rotation.** It fires whenever the frog is occluded — which also happens on
  a *partial* turn or a *morph*, not only a true 360. INANIMATE: my auto called it 2/3; the human saw **0/5
  actually rotate**. So statements like "figurine wins on flail, 3/3" earlier in Batch 4E are **auto-only and
  not trustworthy on their own** — read them as rough triage, not verdicts.
- **The `area_jerk` "flail" metric is not a stillness measure.** It conflates legitimate rotation area-change
  with unwanted motion, which is why it ranked figurine *worst* in Batch 4F while the eye ranked it
  *cleanest*, and why it disagrees with the human's "figurine = best stillness."
- **Neither proxy sees what the human sees:** eye-blinks, held-equipment switching hands / stretching, the
  config-B end-bounce, or double-sided morphs. These decide the result and only a person catches them.
- **My Batch 4F ranking is provisional** until the user scores round 2 in the scoresheet; where their pips
  disagree with mine, theirs win.
- **Control nuance:** the plain round-1 control (T164, no description) rotated 3/4, but the round-2 control
  (full description + "held completely rigid", still no object noun) rotated only 1/5 — so "held rigid" can
  *over-suppress* the turn, and the object noun is what compensates. Reinforces that the object noun is
  load-bearing for the rotation, not just stillness.

**Subject description added — the `<subject_description>` variable.** Earlier batches described no subject, so

**Subject description added — the `<subject_description>` variable.** Earlier batches described no subject, so
the model guessed side/back views. The next round adds a concise description. **Placement (challenged, chosen):
bind the description to the object noun, inline, right after the rotation framing** —
`rotate the view around a <object> of <subject_description> - <sequence>…`. Rationale: lead with the turntable
framing (Batch 4C shows it is load-bearing); binding "`<object>` of `<subject>`" makes the model treat the
described subject *as* the rigid object it rotates (identity + stillness fused in one noun phrase); keep the
view sequence in its proven slot; put rigidity + a short back-hint at the tail. Rejected: description at the
very front (dilutes the rotation trigger) and description-only-at-the-tail (weak influence on the invented
intermediate frames).

**Back-view hint (user idea — validated, with caution).** Describing the back constrains invented details
(prevents a face on the back, duplicated weapons). Risk is length/dilution (over-stacking hurt COMBO), so it
is kept **short and held constant across all five** so it does not confound the keyword comparison.

**Proposed template (pending approval) — only `<OBJECT>` varies:**
> Turntable: rotate the view around <OBJECT> of a frog sitting on top of a turkey, holding a sword in its
> right hand and a shield in its left hand - front, three-quarter, side, back, full back, opposite side, back
> to the front. It stays completely rigid in one fixed pose; only the viewing angle changes. From behind, only
> the backs of the frog and turkey and the turkey's tail feathers are visible.

`<OBJECT>` ∈ {a solid collectible display figure, a solid molded figurine, a solid statue, a hard plastic
action figure, a completely inanimate figure}. Round: 5 keywords × 10 seedless runs, config B,
`no_background: true`, `frame_count` 16; then re-score in the scoresheet (human-weighted) and decide.

## Batch 4F — final stillness round with a subject-description template (2026-08-14)

Built on a **3-way design review** (Claude + a subagent + Codex `gpt-5.6-sol`) that converged on a single
blueprint before any jobs ran. Artifacts: `frog-turkey-360-20260721/stillness-round2-20260814/`,
`.local/stillness-templates.md` (the blueprint + all arms), `.local/stillness-scoresheet.html` (every frame,
human scoring).

**Template (two variables):**
> Turntable: rotate the view around a solid `<OBJECT>` depicting `<subject_description>` - front,
> three-quarter, side, back, full back, opposite side, back to the front. The `<OBJECT>` itself never moves;
> only the viewing angle changes.

Agreed design decisions (each challenged by all three reviewers):
- **`depicting`** recasts the description's verbs ("sitting/holding") as a *depiction* so the model rotates an
  object instead of animating a live scene — the key fix for "will it animate the subject?".
- **One `<OBJECT>` variable, repeated verbatim** ("a solid figurine … The figurine itself never moves") —
  exact repetition is the strongest coreference signal; repeating a referring expression is *not* the
  over-stacking failure (that is stacking multiple distinct motion-negations).
- **`solid` appears once** (not repeated) — the noun already carries coreference; repeating "solid" risked a
  fused/monolithic look that blurs held props (the sword/shield).
- **No formatting to demote the description** — quotes/parens/brackets/colon all backfire in a caption-trained
  model (`()` reads as an *attention boost*, `[]` as metadata syntax, `""` as literal/caption); `depicting`
  is the real mechanism, and the slot is user-filled so baked punctuation is a maintenance trap.
- **Back-view detail lives inside `<subject_description>`** (safe: the sequence's leading "front" re-anchors).

Round: 6 arms × 5 seedless runs (config B, `no_background: true`, `frame_count` 16). `<subject_description>` =
"a frog sitting on top of a turkey, holding a sword in its right hand and a shield in its left hand; from
behind, only their backs and the turkey's tail feathers show".

**Human scores (authoritative — user, per-output pass count out of 5).** Each axis = how many of the 5
outputs passed. Round 2 is the source of truth:

| rank | `<OBJECT>` | rotation | stillness | stays-itself | total | verdict |
|---|---|---|---|---|---|---|
| 1= | **figurine** | 4 | 4 | 3 | **11** | three-way tie — finalist |
| 1= | **toy figure** | 4 | 4 | 3 | **11** | three-way tie — finalist |
| 1= | **display model** | 4 | 4 | 3 | **11** | three-way tie — finalist |
| 4 | statue | 2 | 4 | 2 | 8 | **out** — rotation 2/5, stays-itself 2/5 |
| 5 | inanimate object | 2 | 2 | 3 | 7 | **out** |
| 6 | control (no object noun) | 1 | 2 | 2 | 5 | **out** — baseline |

**Reconciliation — my AI provisional was wrong in key places.** I had ranked figurine a clear #1 (5/4/5) and
put statue and inanimate at 12 each. The human read is a **three-way tie at 11** (figurine = toy figure =
display model), with **statue (8) and inanimate (7) clearly out** — I over-rated their rotation (the same
full-360 over-counting) and their stays-itself. All three finalists score stays-itself **3/5** — i.e. ~2 of 5
outputs fail identity, almost entirely the **white smoke/particle artifacts**, which hit the three about
equally (consistent with the artifact being RNG/model-inherent, not arm-specific). My visual claim that "toy
flaps most" did **not** translate to a worse human score — toy tied for the top.

Findings:
1. **The object noun triggers the rotation, not just the stillness.** The control — same description + "held
   completely rigid" but **no object noun** — rotated only **1/5** (it holds front-facing and never turns).
   Every object-framed arm rotated 4–5/5. So "a solid figurine/statue/… depicting X" does double duty: it is
   the *stillness* cue **and** the *turntable-object* cue that makes the model orbit it. This is a new,
   important result — the object framing is load-bearing for the turn itself.
2. **No single winner — a three-way tie.** figurine, toy figure, and display model all score 11 (rotation
   4/5, stillness 4/5, stays-itself 3/5). statue and inanimate fall a tier below. A **tie-breaker round
   (Batch 4G)** runs just the three finalists to separate them.
3. **The auto flail metric is unreliable when completion varies** — it scored figurine *worst* because it
   penalizes the large area-change of a *full* rotation. Human judgment is the arbiter for stillness/identity.
4. **The white-smoke/particle artifact is the dominant failure and appears arm-independent** — it costs every
   finalist ~2/5 on stays-itself. My earlier visual impression that "toy flaps most" did **not** hold up in the
   per-output human scoring (toy tied for the top). Material/effect words remain off the table regardless; the
   likely real fix for the smoke is a `negative_description`, not more positive wording.
5. **Low sample (5 runs/arm)** — figurine's #1 is solid (5/5 + cleanest), but the mid-pack ranking is
   provisional; a larger round would firm it up if needed.

**Human scoring rule for round 2 (authoritative — this differs from round 1).** Each axis score `X/5` = the
number of the 5 outputs that **passed** that axis (close-enough counts as a pass; a clear failure does not
add to the count). It is *not* an absolute quality rating — "stillness 4/5" means 4 of 5 were passable, not
that 4 were perfect. This applies to all three axes. **Round 2 is the source of truth for the MVP prompt;
round 1 (absolute quality on 1 run each) is only suggestive guidance.** The user also counts the **spontaneous
white "smoke"/particle artifacts** (which I earlier called wing-flaps) as a **stays-itself failure**, even
though they are likely erasable by hand — so they lower "stays-itself", not just "stillness". These artifacts
appear across most arms, so they read as largely RNG/model-inherent on this subject rather than arm-specific;
the tie-breaker round (below) measures which arm minimizes them most consistently.

## Batch 4G — tie-breaker of the three finalists (2026-08-14)

The round-2 human scores tied **figurine = toy figure = display model** at 11. Tie-breaker: those three plus
**statue** (kept as a full contender since its runs were already generated), 5 seedless runs each, same final
template with the **updated back-view** ("from behind, only the turkey's back and tail feathers show").
Artifacts: `frog-turkey-360-20260721/stillness-tiebreak-20260814/`.

**Human scores (authoritative) — HEAVY REGRESSION.** Every arm rotated only **1/5** (vs 4/5 in round 2):

| `<OBJECT>` | rotation | stillness | stays-itself | total |
|---|---|---|---|---|
| display model | 1/5 | 3/5 | 2/5 | 6 |
| figurine | 1/5 | 4/5 | 1/5 | 6 |
| toy figure | 1/5 | 2/5 | 0/5 | 3 |
| statue | 1/5 | 0/5 | 0/5 | 1 |

Auto `full-360` **agrees the regression is real** (not a scoring artifact): figurine 2/5, display 1/5, statue
1/5, toy 0/5 — versus round-2 auto of 4–5/5. User's verdict: **this round was a failure**; the arm that beat
control did so only on stillness, which is not success.

**Regression investigation (non-destructive first):**
- **Not a seed** — all three rounds are seedless (verified in the run scripts). Ruled out.
- **The ONLY generation difference round-2 → round-3 was the back-view wording:** R2 "…from behind, only *their
  backs and* the turkey's tail feathers show" vs R3 "…from behind, only *the turkey's back and* tail feathers
  show". Input image, config B, `no_background:true`, seedless, 16f, and the rest of the prompt are identical.
- So the cause is **either that wording tweak or a same-day PixelLab backend/temporal shift** — non-destructive
  analysis cannot separate them. A further hypothesis: the subject **description itself** (added in round 2)
  degrades rotation and adds the white smoke (round 1, which had no description, is recalled as cleaner).
  **Batch 4H** resolves all of this by controlled re-run.
- **Correlated axes (user):** when rotation fails, stillness/stays-itself drop too — a failed turn means the
  model morphs / adds artifacts instead of rotating cleanly. **Rotation is the linchpin;** fix it first.

## Batch 4H — rotation-regression diagnostic (2026-08-14)

Controlled re-run to find the cause. All figurine, config B, seedless, 16f, 5 runs each; **one variable per
arm.** Artifacts: `frog-turkey-360-20260721/diag-20260814/`.

| arm | what it isolates |
|---|---|
| **A_round2exact** | the EXACT round-2 prompt (back-view "their backs…") — does round 2 rotate **again today**? Separates *wording* from a *same-day backend/temporal shift*. |
| **B_round3exact** | the EXACT round-3 prompt — confirms the current regressed state. |
| **C_nodesc** | round-1 style: NO subject description, NO back-view — does the **description** degrade rotation / add smoke? |
| **D_bg_nobgfalse** | round-2 prompt but the input has an **opaque grey background** and `no_background:false` — the user's smoke hypothesis. |
| **E_strongrot** | round-2 prompt **+ "The camera makes one complete 360-degree orbit"** — does a stronger *view-orbit* cue help? |

**Results (auto full-360):** A_round2exact **5/5**, B_round3exact **3/5**, C_nodesc **5/5**, D_bg_nobgfalse
**5/5**, E_strongrot **5/5**. Visual: all arms rotate cleanly; the white feather/sparkle artifacts persist in
**every** arm (A, C, D alike).

**Verdicts:**
- **Rotation regression = RNG + a mildly-worse back-view wording, NOT a systematic break.** The exact round-2
  prompt (A) rotates **5/5 again today** → backend/temporal shift ruled out; the seed was already ruled out.
  The round-3 wording (B) scores 3/5 vs A's 5/5 → the tweak ("only the turkey's back and tail feathers show")
  is genuinely a bit worse, but B's 3/5-now vs the tie-breaker's ~1/5 shows the catastrophic 1/5 was largely an
  **unlucky RNG cluster** on 5 seedless samples. **Fix: revert to the round-2 back-view wording** (or drop the
  back-view — C, with no description at all, also rotates 5/5), and **use more runs** so a bad RNG cluster
  can't masquerade as a regression.
- **The description does NOT degrade rotation** — C (no description) = 5/5, same as A.
- **The white smoke is INHERENT, not prompt- or config-caused.** It appears in every arm regardless of the
  description (C has it), the wording, or `no_background` (D — opaque bg + `no_background:false` — still has
  it). It is the model animating the **turkey's wing/tail feathers** (plus occasional sparkle VFX) as it turns.
  This **disproves both** user hypotheses ("the description causes the smoke" and "an opaque background +
  `no_background:false` fixes it"). The remaining untested lever is a **`negative_description`** targeting
  feathers/particles/sparkles; otherwise the artifacts are erasable in post.

## Batch 4I — simplified description restores rotation (2026-08-14)

Following Batch 4H (the full description + back-view was the mildly-worse bit for rotation), the
`<subject_description>` was cut to just **"a frog on top of a turkey"** (no equipment, no back-view) and the
three finalists (statue dropped — a tier below per round 2) were re-run at **10 runs each** to beat RNG.
Artifacts: `frog-turkey-360-20260721/simple-desc-20260814/`.

Results (auto full-360, 10 runs each):

| `<OBJECT>` | full-360 |
|---|---|
| **figurine** | **10/10** |
| toy figure | 9/10 |
| display model | 8/10 |

- **Rotation is restored and improved** — vs the tie-breaker's 0–2/5 and round 2's 4–5/5. This **confirms the
  user's hypothesis**: the richer description ("…holding a sword…; from behind, only…") was causing context
  confusion that degraded rotation. Leaner description = more reliable turn.
- **figurine leads at 10/10** (visually confirmed — every run does a clean full turn).
- **The white smoke is unchanged** — the turkey's feather/sparkle artifacts persist across the simplified runs,
  exactly as Batch 4H found (inherent to the subject, not the description). Still the open item; lever remains a
  `negative_description` or post-erase.

Current best prompt (rotation-optimised) — swap the object noun to test, `<subject_description>` kept minimal:
> "Turntable: rotate the view around a solid figurine depicting a frog on top of a turkey - front,
> three-quarter, side, back, full back, opposite side, back to the front. The figurine itself never moves;
> only the viewing angle changes."

## Fixed setup (all tests identical — only the `action` phrase varies)

| Parameter | Value | Why |
|---|---|---|
| Route | REST v2 `animate-with-text-v3` | v3 + start→end interpolation on a raw file |
| `first_frame` | `chibi-oni-front-frame0-128px.png` (south) | the pixel-perfect front sprite (NOT the concept) |
| `last_frame` | same south frame | forces a full turn *back* to south = seamless loop |
| `frame_count` | 16 | max (v3 caps at 16, must be even) |
| size | 128×128 native | budget 128·128·16 = 262 144 ≤ 524 288 ✓ |
| `seed` | one shared random int (seed-lock) | isolates the phrase variable across all calls |
| `negative_description` | empty (batch 1) | test the raw phrase; anti-physics negatives are batch 2 |
| `enhance_prompt` | false | test the literal minimal phrase, not an enhanced rewrite |

Returned images: **17** (image 0 = echoed south `first_frame`; frames 1–16 generated;
frame 16 = `last_frame` south). Frame 0 and frame 16 are both south → loop anchors.

Key unknown this spike answers: with `first_frame == last_frame == south`, does the phrase
push a genuine **full turn** through east/north/west, or does the model take the zero-motion
"already there" interpretation and idle? That is exactly what each phrase is scored on.

## Batch 1 — minimal `action` phrases to test

Pure minimal phrases (the core research), plus a couple of explicit-path controls to help
interpret results.

| # | `action` phrase | class |
|---|---|---|
| 01 | `360` | ultra-minimal |
| 02 | `360 degrees` | ultra-minimal |
| 03 | `360 degree rotation` | minimal |
| 04 | `rotate 360 degrees` | minimal |
| 05 | `turnaround` | single word |
| 06 | `turntable` | single word |
| 07 | `character turntable` | minimal |
| 08 | `full rotation` | minimal |
| 09 | `full turn` | minimal |
| 10 | `spinning` | single word |
| 11 | `spin` | single word |
| 12 | `spinning in place` | minimal |
| 13 | `rotate` | single word |
| 14 | `rotate in place` | minimal |
| 15 | `turning around` | minimal |
| 16 | `rotate clockwise` | minimal + direction |
| 17 | `pirouette` | single word |
| 18 | `turning to face away then back to the front` | explicit-path control |
| 19 | `turnabout` | single word |

Batch 2 (only after batch 1 identifies phrases that turn): re-run the top phrases with a
constant anti-physics `negative_description` (e.g. `walking, moving arms, moving legs,
hair movement, blinking, bouncing, breathing`) and/or `rotate counterclockwise` to confirm
stiffness and direction control. Not run until batch 1 results are in.

## Scoring

### Auto pre-score (rough ranking only — not the verdict)
Computed from the 17 returned frames:
- **loop_closure** — similarity of frame 0 vs frame 16 (both should be south).
- **motion_amount** — mean inter-frame pixel diff. Too low ⇒ idle/no turn; very high ⇒ chaotic.
- **turn_signal** — sweep of the red oni-mask pixel count across frames. A real turntable
  makes the one-sided mask move and occlude when back-facing; a flat idle does not.
- **palette_stability** — colour-histogram drift across frames (proxy for consistent colours).

### Manual score (the real verdict — HTML scoresheet)
Human 1–5 per criterion, per animation:
1. **Completes a 360** — genuine full turn through all sides back to front.
2. **Smooth & seamless** — no jump at the loop, no popping frames.
3. **Constant speed** — even angular step per frame.
4. **Consistent colours** — face, horns, mask, clothing hold their colours.
5. **Consistent shape** — chibi proportions, horns, mask, outfit preserved.
6. **Stiff / no physics** — no walking legs, flailing arms, hair/cloth sim, or blinking.

## Notes / risks
- Cost: each animation = 4 subscription generations (~$0.042 if paid). Batch 1 (18) = 72 gen.
- 16-direction ambition (>8): out of scope for batch 1; first prove a clean single 360.
- The >64px caveat (first==last south for interpolation) applies here (128px) and is the
  intended behaviour, not a problem — it is what closes the loop.

## Results — Batch 1 (2026-07-21, seed 726361, 19/19 completed, 76 generations)

Artifacts: `pixellab-pip-generations/chibi-oni-360-rotation-20260721/` — per-phrase GIFs +
spritesheets, `360-compare-grid.png` (frames 0/4/8/12/16 for all 19), `auto_scores.json`,
`360-scoresheet.html` (manual scoresheet).

**Verdict: no phrase produced a rotation. The method itself is the blocker.**

With `first_frame == last_frame == south`, `animate-with-text-v3` interpolates the shortest
path between two *identical* poses → the zero-motion geodesic. Every one of the 19 phrases
returned a near-static south-facing sprite. The red one-sided oni mask never leaves its side
in any frame; `turn_signal` (silhouette-asymmetry variance) = **0.000 for all 19**.

| Phrase class | example | mean inter-frame motion | what actually happened |
|---|---|---|---|
| minimal / single-word | `360`, `spin`, `rotate`, `turntable`, `pirouette` | ~0.005 (frozen) | essentially no movement |
| path-narrating | `turning around`, `turnabout`, `turning to face away then back` | 0.016–0.024 | slightly more animation, but it is **head-dip + blinking + a hand particle artifact**, still no turn |

Key reads:
- More descriptive phrasing buys more *motion*, not *rotation* — and that extra motion is the
  forbidden kind (blinking, head bob, detached puffs near the hand — the `last_frame` artifact
  risk in `../../skills/pixellab-pip/references/animation.md`).
- `loop_closure` = 1.0 and `palette_stability` ≈ 0.99 everywhere — trivially true because the
  frames barely change; not evidence of a good turntable.
- Background: outputs came back **opaque with a uniform mauve background** (no `no_background`
  set). Uniform, so it does not affect the comparison; a winner would get a transparent re-run.

**So the minimal-phrase question is moot for this exact configuration** — the identical-anchor
interpolation cannot rotate, so there is no phrase to find. The character-description step is
not the missing piece either.

## Recommended next spike (needs approval — new credits)

To actually get a smooth, constant-speed, stiff 360, the endpoints must differ so interpolation
has somewhere to go. Options, cheap→robust:

1. **First-frame-only** (drop `last_frame`) + a rotation phrase. Cheap probe (a handful of the
   above phrases). Risk: open turn that will not cleanly loop back to south, speed not guaranteed
   even. Good for a quick "does removing the anchor unlock any turn?" signal.
2. **Anchor-stitch (recommended for the real goal).** Generate distinct directional anchors with
   PixelLab's rotation tools (`generate-8-rotations-v2/v3`, or `rotate` to specific angles), then
   run short interpolations between *consecutive* views (S→E, E→N, N→W, W→S — 4 frames each) and
   stitch into one 16-frame loop. Distinct endpoints force real turning; equal per-segment frame
   counts give constant speed; ending on S closes the loop. This also directly serves the
   16-direction ambition (interpolate between 8 anchors → 16 in-betweens).
3. **`generate-8-rotations-v2`/`-v3` alone** if 8 discrete directions (no smooth in-betweens) is acceptable.

The `360-scoresheet.html` still lets you manually confirm the negative result per-phrase.

## Results — Batch 2 (2026-07-21, seed 726361): first-frame-only probe + 8-rotations

Two experiments against the Batch 1 negative. Artifacts: `batch2-2A-firstframeonly-grid.png`,
`2B_generate-8-rotations/`, `batch2_jobs.json`.

### 2A — first-frame-only (dropped `last_frame`), same 6 top phrases
Removing the identical-anchor trap **unlocked motion** (inter-frame 0.034–0.057 vs Batch 1's
0.005), and for the *turn-verb* phrases, **real partial rotation**:

| phrase | inter-frame motion | visual result |
|---|---|---|
| `turnaround` | 0.034 | **turns ~180° to a back view** by frame 16 (hair back, no face, mask gone) |
| `turning around` | 0.041 | **turns ~180° to back** by frame 16 — same as turnaround |
| `rotate clockwise` | 0.049 | mostly front; slight sway, no clear turn |
| `360 degree rotation` | 0.034 | mostly front; mask fades but stays front |
| `turntable` | 0.057 | mostly front; highest wobble but no turn |
| `spinning` | 0.044 | **hand particle artifact**, stays front — "spin" reads as an effect |

Takeaways:
- The verb matters more than any noun: **"turn around" rotates; "360 / turntable / spin / rotate"
  do not.** "spin" actively harms (adds an effect artifact).
- Even the winner only reaches ~180° (front→back) in 16 frames and does **not** return to front,
  so it is not a seamless 360, and back-half frames carry mild physics/artifact risk.
- `turn_signal` reads 0 for all because front and back are both mirror-symmetric; only side
  profiles spike it — so the metric under-reports these front→back turns. Trust the grid.

### 2B — `generate-8-rotations-v3` (descriptionless) — **the breakthrough**
One call on the south frame returned **8 clean directional views forming a genuine, complete,
identity-consistent 360 turntable.** The one-sided oni mask correctly sweeps around the head
and occludes on the back views; horns, white hair, red/black/white outfit, colours, and chibi
proportions all hold. Each view is a rigid rotated pose — **no subject movement** (no walk,
no blink, no hair sim). This is exactly the "stiff rotation, no physics" the goal asks for.

**Conclusion so far:** the clean 360 does **not** come from an `animate-with-text-v3` action
phrase at all — it comes from `generate-8-rotations-v3`. The "MVP description" for rotation
is effectively **none**: the dedicated rotation endpoint is the correct, subject-agnostic tool.
The remaining question — how to make it *smooth* (more than 8 frames) and how minimal the
per-tween action can be — moves to Batch 3.

## Batch 3 (in progress) — smooth the 8 anchors into a many-frame 360

Interpolate between *consecutive* 8-rotation anchors (endpoints now differ, so interpolation
has somewhere to go) with the most minimal action that yields clean rigid in-betweens. Test a
few minimal tween actions on one adjacent pair, pick the winner, then stitch all 8 segments
into one constant-speed loop that closes on south.

## Results — Batch 3 (2026-07-21, seed 726361): interpolate the anchors into a smooth 360

### 3-i — tween action test (anchor S→SE, `frame_count`=4)
`turn`, `rotate`, `turning` all interpolate the 45° step cleanly and rigidly (identity held, no
physics). Empty action is rejected (`min_length` 1). Then the decisive control:
**`x` (nonsense) and `jump` (contradictory) produced the *same* clean rotation as `turn`.**

> **With two distinct rotation anchors as `first_frame`/`last_frame`, the interpolation is
> geometrically constrained by the endpoints and the `action` text is inert.** "jump" did not
> add a jump. The field is a required non-empty string, but its content does not affect the
> result. Evidence: `tween_action_matters.png` (rows turn / x / jump are indistinguishable).

### 3-ii — stitched 360 (`2C_smooth360_turn.gif`, `_sheet.png`)
8 segments (each consecutive anchor pair, incl. wrap 7→0), `animate-with-text-v3`, `action="turn"`,
`frame_count`=4, seed-locked; keep each segment's anchor + 3 in-betweens → **32-frame loop**.

- Genuine continuous 360: front → right → back (hair back, no face, mask hidden) → left → front.
- Identity consistent throughout (horns, one-sided mask sweeps correctly, hair, outfit, colours,
  chibi proportions). No walking / arms / blink / hair-sim — rigid rotation.
- **Constant speed:** per-step motion mean 0.056, std 0.011 (even; no jumps).
- **Loop closes:** seam frame 31→0 = 0.052 ≈ mean step 0.056 — no visible jump at the loop.
- Caveat: anchors (and thus the loop) carry `generate-8-rotations-v3`'s flat **grey background**
  (opaque). Uniform → keyable; a transparent asset needs `remove-background` per frame or a
  careful key. Not part of the rotation question.

---

## FINAL ANSWER — the MVP for a clean rigid 360 (any subject)

> ⚠️ **Superseded by Batch 4B (below).** This section concluded no single-frame prompt can rotate —
> that was true only for *minimal* prompts. A verbose trajectory prompt DOES give a true 360 from one
> frame in config B. The `generate-8-rotations`-based recipe here is still valid, but it is no longer
> the *only* path. Read Batch 4B/4C for the corrected answer.

**There is no "magic description."** `animate-with-text-v3` driven by an action phrase cannot make
a subject rotate: identical anchors → zero motion (Batch 1); first-frame-only → only the *turn*
verbs reach ~180° with artifacts (Batch 2A). The rotation must come from **distinct directional
endpoints**, not text.

**Subject-agnostic recipe (no character description needed for rotation):**
1. `POST /v2/generate-8-rotations-v3` with the front sprite as `first_frame` → 8 identity-consistent
   directional anchors (descriptionless; this is where rotation actually comes from).
2. For each consecutive anchor pair (0→1 … 7→0), `POST /v2/animate-with-text-v3` with
   `first_frame`=A_i, `last_frame`=A_{i+1}, **`action` = any non-empty string** (`"turn"` for
   readability; content is inert), `frame_count`=4, a shared `seed`, `enhance_prompt`=false.
3. Stitch: for each segment keep the anchor + `frame_count`−1 in-betweens (drop the echoed frame 0
   and the trailing duplicate anchor) → a constant-speed 360 loop that closes on south.

Notes:
- Constant speed = equal `frame_count` per 45° segment. More frames/segment = smoother.
- **16 directions** fall straight out of this: 8 anchors + 1 in-between each = 16 evenly-spaced views.
- The only "minimal description" that survives is a **1-character placeholder** in the tween's
  required `action` — proof that the description is not the lever; the endpoints are.
- To keep the subject perfectly rigid, do not add motion verbs to the tween (they are inert here
  anyway) and never give `animate-with-text-v3` an idle/loop action expecting a turn.

## Generalization — the recipe is subject-agnostic (Batch 3D)

Ran step 1 (`generate-8-rotations-v3`) on two subjects deliberately unlike the chibi, generated
fresh via `create-image-pixflux` (128×128, `no_background`). Artifacts:
`3D_generalization/` (`knight_front.png`, `fox_front.png`, `*_8rot/`, `generalization_8rot_montage.png`).

| subject | type | result |
|---|---|---|
| silver-armor knight w/ sword + cape | hard-surface humanoid, asymmetric held item | clean coherent 360; sword & cape rotate correctly; proper cape-covered back view; armor consistent |
| sitting orange fox | non-humanoid quadruped | clean coherent 360; tail/ears/markings consistent front→side→back→front |

So identity + rotation quality hold across an anime chibi, an armored humanoid with a held weapon
and cape, and a sitting animal — with **no description tuning**. `generate-8-rotations-v3` is the
subject-agnostic rotation primitive; the MVP recipe above is not chibi-specific. (Both also return
a flat grey background, same keyable caveat.)

## Deliverables produced (chibi-oni)

- `2C_smooth360_turn.gif` / `_sheet.png` — 32-frame smooth 360 loop (grey bg, as returned).
- `2C_smooth360_transparent.gif` / `2C_smooth360_transparent_sheet.png` — same loop, background
  removed per frame via `remove-background` (clean key, no halo).
- `2E_16direction_transparent_sheet.png` — **16-direction character sheet** (every other loop
  frame = 22.5° spacing), transparent — the stated end goal.
- `2B_generate-8-rotations/` + `2B_8rotations_montage.png` — the 8 anchors.
- `3D_generalization/` — knight + fox generalization proof.
- `smooth-360-pipeline.blueprint.json` — the reproducible recipe.

Background removal is PixelLab `remove-background` (no locally authored pixels); the grid
composite over a checkerboard is an inspection aid only, not a shipped asset.

## Batch 3E — challenging the spike: can *description alone* give a true 360?

Adversarial follow-up to the most promising lead (2A "turnaround" reaching ~180°) and to close
gaps the earlier batches left. Artifacts: `3E_description_360/`, `3E_chain_full_montage.png`,
`3E_chain_description360.gif`.

### The `/rotate` endpoint — does it beat 8-rotations for granularity? No.
`POST /rotate` (`from_image`/`from_view`/`from_direction` → `to_view`/`to_direction`, single view
out) only supports the **same 8 compass directions**. It gives per-direction control but **not**
finer-than-8 native granularity, so it is not a shortcut to 16 directions; interpolation remains
the path to >8.

### Single-clip "stronger phrase" attempts (first-frame-only, 16f)
`turn all the way around` reaches ~180° (back), same as `turnaround`. `spin around once` and
`360 degree spin all the way around` stay front (spin adds artifacts). `rotate a full circle back
to the front` stays front — "back to the front" cancels the turn. **The model reads "turn around"
as "face the opposite way" (=180°) and caps there;** no single 16-frame clip reaches 360.

### The chain — front→back (`turn all the way around`) then back→front (`continue turning to face front`)
Both halves complete (front→back→front, returns to the start pose, technically loops). Clip-2
phrasing **does** matter here (`continue turning to face front` lands a cleaner front than
`turn around`) — so the earlier "action is inert" claim holds only for small distinct-anchor gaps,
**not** across a 180° ambiguous gap where the action steers the endpoint. That over-claim is now
scoped.

**But it is not a true 360 — proven by the red mask/horn x-centroid** (a one-sided feature must
sweep to the *opposite* side in a real turn):

| sequence | red-X sweep | crosses to far side? | what it actually is |
|---|---|---|---|
| real `generate-8-rotations` loop (2C) | +10.6 → **−17.6** → +10.3 (28 px) | **yes** | genuine 360 rotation |
| pure-description chain (3E) | −0.1 → +8.2 (8 px) | **no** | front→back→front **morph** ("look behind"), plus uneven speed and softer identity |

So the chain *looks* like it turns but the character never presents its true opposite side — the
animate model morphs the front into a back and back again rather than rotating through the profiles.

### Verdict on "is there promise for description-driven 360": **no.**
Every description path tops out at a 180° morph. A **true** 360 (features sweeping fully to the far
side, constant speed, crisp profiles, consistent identity) comes **only** from
`generate-8-rotations-v3` anchors. This strengthens, not weakens, the MVP conclusion: the rotation
primitive is the endpoint, and no prompt wording substitutes for it. Remaining upside is polish on
that winning pipeline (more interpolation frames per segment; try `interpolation-v2`; `generate-8-
rotations-v2` `view` for top-down/side games), not a new description trick.
