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
- Background: outputs came back **opaque with a uniform mauve background** (no `remove_background`
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
3. **`generate-8-rotations` alone** if 8 discrete directions (no smooth in-betweens) is acceptable.

The `360-scoresheet.html` still lets you manually confirm the negative result per-phrase.
