# PixelLab 360° Rotation Spike — minimal-prompt turntable via v3 interpolation

Research question: **what is the shortest `action` phrase that makes `animate-with-text-v3`
produce a clean, seamless, constant-speed 360° turntable** of a front-facing character,
with a stiff body (no walk/idle physics), consistent colors, and consistent shape?

The endgame is a phrase so minimal it generalises to any character (then the character
description is appended). This spike isolates the phrase only; character wording is added
later once a winner is found.

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
