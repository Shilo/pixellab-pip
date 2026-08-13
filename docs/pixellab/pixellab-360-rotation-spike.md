# PixelLab 360° Rotation Spike — minimal-prompt turntable via v3 interpolation

Research question: **what is the shortest `action` phrase that makes `animate-with-text-v3`
produce a clean, seamless, constant-speed 360° turntable** of a front-facing character,
with a stiff body (no walk/idle physics), consistent colors, and consistent shape?

The endgame is a phrase so minimal it generalises to any character (then the character
description is appended). This spike isolates the phrase only; character wording is added
later once a winner is found.

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
