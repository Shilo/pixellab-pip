# PixelLab Negative Prompting Controlled Test Plan

Status: Phase 0, Phase 0B, and Phase 1 executed 2026-08-08; 106-call static study complete.

Scope: historical dedicated-field study on BitForge and deprecated PixFlux. It is not the
primary current-model plan and receives zero weight in Pixen/v3/new or Create Image Pro/v2
conclusions. See `pixellab-inline-negative-prompting-current-model-test-plan.md`.

Last reviewed: 2026-08-08.

Companion research: `../pixellab/pixellab-negative-prompting-research-spike.md`.

Phase 0 results: `../pixellab/pixellab-negative-prompting-calibration-results.md`.

Phase 0B results: `../pixellab/pixellab-negative-prompting-phase0b-results.md`.

Phase 1 results: `../pixellab/pixellab-negative-prompting-confirmation-results.md`.

The 180-call symmetric Phase 1 matrix is obsolete. Phase 0B found only one informative
replacement family, and the initial calibration already contained one informative PixFlux
family. The revised confirmation below tests those endpoint-specific pairs only. Both
executed calibration matrices and results remain immutable.

## Decision This Plan Must Support

Determine, per tested PixelLab endpoint, whether a dedicated
`negative_description` field:

1. reduces a named, visually scoreable failure;
2. has no practically meaningful effect;
3. makes the named failure or general image quality worse; or
4. cannot be classified with the collected evidence.

This plan does not seek a universal law for every model, prompt, or future PixelLab
build. A conclusion is valid only for the endpoint, schema date, prompt families, and
seed range tested. Static-image results must not be generalized to animation, inpaint,
Pixen, or Create Image Pro without their own study.

## Causal Unit And Routing Bias

The causal unit is not “negative prompting” detached from a model. It is the intervention
as interpreted by one deployed PixelLab workflow stack. Model priors, endpoint selection,
MCP/REST routing, prompt parsing, field weighting, prompt enhancement, any server-side or
system instruction that may exist, safety conditioning, and post-processing can all
moderate the observed effect.

The public interfaces do not reveal enough internals to factor those components apart.
Every analysis must therefore record and stratify by:

- public surface and operation (`MCP tool` or exact REST path);
- documented model/mode/workflow label, without inventing a provider identity;
- schema snapshot date and a hash of the exact public schema used;
- prompt-enhancement state and every visible request field;
- execution window, so silent service-build drift is at least bounded;
- task family and seed; and
- output candidate clustering, especially for Pro calls returning many related images.

Never pool estimates across route strata first. Report the route/task result, then compare
strata as an interaction analysis. If MCP and REST expose different fields, they are not a
clean surface-only ablation. Hidden routing remains a limitation even when all public
inputs match.

## Why Live Testing Was Required

Before this study, the repository and generation archive contained no same-endpoint,
same-seed, same-positive-description pair where only `negative_description` changes.
Historical outputs cannot identify causation. Current public documentation also does not publish
controlled efficacy evidence. The only way to resolve the dispute is a pre-registered
paired study that preserves every request and does not discard failures. The completed
study now supplies that record.

## Current Public Contract Frozen For This Study

The live REST v2 OpenAPI schema was re-read on 2026-08-08 before freezing this plan and
again after completion when checking current-model coverage.

| Endpoint | Dedicated field | Status | Study role |
|---|---|---|---|
| `POST /v2/create-image-pixflux` | `negative_description` | Exposed but described as `(Deprecated)` | Test whether the field is accepted and behaviorally active despite deprecation. |
| `POST /v2/create-image-bitforge` | `negative_description` | Exposed and described as text to avoid | Test the currently documented implementation. |

Both routes accept the common fields used here: `description`, `image_size`,
`text_guidance_scale`, `no_background`, and `seed`. The study omits endpoint-specific
controls so the paired field comparison changes only `negative_description`.

No current public MCP image tool exposes this field. Pixen and Create Image Pro are not
surrogate tests for it and are intentionally excluded from the dedicated-field phase.
Current `create-image-pixen`, `generate-image-v2` (Create Image Pro),
`create-character-v3`, `create-character-pro`, `animate-with-text-v3`, and `inpaint-v3`
schemas also expose no separate negative field. They remain untested inline-wording
strata, not missing replicas of the dedicated-field phase.

## Pre-Registered Hypotheses

- `H1 — concise benefit`: `N1` has fewer target failures than `B0` without a material
  loss in blinded quality.
- `H2 — concise harm`: `N1` has more target failures or materially lower quality than
  `B0`.
- `H3 — long-negative harm`: `N2` performs worse than `N1` on target compliance,
  quality, or both.
- `H4 — positive structure`: `P1` performs at least as well as the best negative arm.
- `H5 — PixFlux no-op`: PixFlux `N1` and `N2` are behaviorally indistinguishable from
  `B0`, after same-request repeat variability is measured.

`N1` versus `B0` is the causal field ablation. `N2` versus `B0` tests broad negative
lists. `P1` is a strategy comparison, not a one-variable causal ablation.

## Fixed Arms

| Arm | Positive description | `negative_description` |
|---|---|---|
| `B0` | Base prompt | Omitted |
| `N1` | Byte-identical to `B0` | Concise target exclusion |
| `N2` | Byte-identical to `B0` | Long target-plus-defect list |
| `P1` | Constructive positive rewrite | Omitted |
| `R0` | Byte-identical request body to `B0` | Omitted |

`R0` is a second submission of the exact `B0` body. Request identifiers and timestamps
are metadata outside the body and may differ.

## Frozen Prompt Registry

Punctuation and spelling below are literal. Do not enhance, translate, reorder, or add
boilerplate after seeing an output. Any wording change creates a new protocol version.

### `CNT` — object count

Target: exactly two whole swords and no third or duplicated weapon.

- Base (`B0`, `N1`, `N2`, `R0`): `Crossed silver swords emblem centered in empty space.`
- Concise negative (`N1`): `extra swords, third sword, duplicate swords`
- Long negative (`N2`): `extra swords, third sword, duplicate swords, extra blades, floating weapons, shields, banners, text, watermark, cropped objects, blur, gradients, photorealism, 3D render`
- Positive rewrite (`P1`): `Exactly two whole silver swords crossing once in an X, both fully visible, centered with clear empty space on all sides.`

### `TXT` — text contamination

Target: a pictorial shop sign with no letter-like or number-like marks. The intended
potion-bottle pictogram is not text.

- Base (`B0`, `N1`, `N2`, `R0`): `Wooden fantasy potion-shop sign centered in empty space.`
- Concise negative (`N1`): `text, letters, words, numbers`
- Long negative (`N2`): `text, letters, words, numbers, writing, labels, logos, signatures, watermarks, typography, runes, glyphs, slogans`
- Positive rewrite (`P1`): `Wooden fantasy shop sign with one centered red potion-bottle pictogram as the entire face design, a simple carved border, and a clear silhouette.`

### `STY` — render style

Target: limited-color hard-edged pixel art, without smooth, photographic, or 3D-render
traits.

- Base (`B0`, `N1`, `N2`, `R0`): `Small blue ceramic potion bottle centered in empty space.`
- Concise negative (`N1`): `glossy, photorealistic, 3D render, smooth gradients`
- Long negative (`N2`): `glossy, reflective, photorealistic, 3D render, smooth gradients, cinematic lighting, depth of field, bokeh, antialiasing, blur, plastic, subsurface scattering, painterly brushwork`
- Positive rewrite (`P1`): `Small blue potion bottle using exactly three opaque colors: a dark navy outline, a medium-blue fill, and a pale-blue highlight, with hard stair-step pixel edges, centered in empty space.`

## Fixed Request Body

Every request uses:

```json
{
  "description": "<literal prompt from the registry>",
  "image_size": { "width": 64, "height": 64 },
  "text_guidance_scale": 8,
  "no_background": true,
  "seed": 1178348305
}
```

`N1` and `N2` add their literal `negative_description`. `B0`, `P1`, and `R0` omit the
property rather than sending an empty string. All other optional fields are omitted.

## Fixed Seed Registry

Eight unique positive 31-bit seeds were generated once with a cryptographic random
number generator and frozen before any output was produced:

| Block | Seed | Use |
|---:|---:|---|
| 1 | `1178348305` | Calibration pilot and first repeat block |
| 2 | `8382088` | Confirmation |
| 3 | `1505276381` | Confirmation |
| 4 | `1344908665` | Confirmation |
| 5 | `1824521337` | Confirmation |
| 6 | `338955590` | Confirmation |
| 7 | `1696822838` | Confirmation |
| 8 | `1156405294` | Confirmation |

## Phase 0 — Calibration Pilot

### Purpose

Verify request acceptance, response capture, blinding, rubric usability, target failure
frequency, and same-request reproducibility before purchasing a larger sample. The pilot
is allowed to conclude that a prompt family is uninformative; it is not powered to
declare broad benefit, harm, or equivalence.

### Exact call count

- 2 endpoints × 3 prompt families × 4 comparison arms = 24 calls.
- One `R0` repeat for each endpoint/family baseline = 6 calls.
- Total: **30 paid calls**, expected to consume about **30 generations** based on the
  current non-Pro route tier and historical usage records. Preserve the returned usage
  object because actual billing is authoritative.

### Frozen dispatch order

This order was shuffled before generation with deterministic shuffle seed `20260808`.
Do not regroup calls by arm during execution.

| Order | Request ID | Endpoint | Family | Arm |
|---:|---|---|---|---|
| 1 | `BF-STY-N1` | BitForge | `STY` | `N1` |
| 2 | `PF-STY-B0` | PixFlux | `STY` | `B0` |
| 3 | `PF-CNT-N2` | PixFlux | `CNT` | `N2` |
| 4 | `BF-TXT-P1` | BitForge | `TXT` | `P1` |
| 5 | `BF-CNT-P1` | BitForge | `CNT` | `P1` |
| 6 | `PF-CNT-P1` | PixFlux | `CNT` | `P1` |
| 7 | `PF-TXT-P1` | PixFlux | `TXT` | `P1` |
| 8 | `BF-TXT-R0` | BitForge | `TXT` | `R0` |
| 9 | `PF-TXT-B0` | PixFlux | `TXT` | `B0` |
| 10 | `BF-STY-R0` | BitForge | `STY` | `R0` |
| 11 | `BF-STY-P1` | BitForge | `STY` | `P1` |
| 12 | `PF-TXT-R0` | PixFlux | `TXT` | `R0` |
| 13 | `PF-STY-P1` | PixFlux | `STY` | `P1` |
| 14 | `PF-STY-N2` | PixFlux | `STY` | `N2` |
| 15 | `BF-CNT-N1` | BitForge | `CNT` | `N1` |
| 16 | `BF-TXT-N2` | BitForge | `TXT` | `N2` |
| 17 | `PF-STY-R0` | PixFlux | `STY` | `R0` |
| 18 | `BF-STY-N2` | BitForge | `STY` | `N2` |
| 19 | `PF-TXT-N1` | PixFlux | `TXT` | `N1` |
| 20 | `BF-CNT-B0` | BitForge | `CNT` | `B0` |
| 21 | `PF-TXT-N2` | PixFlux | `TXT` | `N2` |
| 22 | `PF-CNT-B0` | PixFlux | `CNT` | `B0` |
| 23 | `PF-CNT-R0` | PixFlux | `CNT` | `R0` |
| 24 | `BF-CNT-R0` | BitForge | `CNT` | `R0` |
| 25 | `BF-TXT-N1` | BitForge | `TXT` | `N1` |
| 26 | `PF-STY-N1` | PixFlux | `STY` | `N1` |
| 27 | `BF-STY-B0` | BitForge | `STY` | `B0` |
| 28 | `PF-CNT-N1` | PixFlux | `CNT` | `N1` |
| 29 | `BF-CNT-N2` | BitForge | `CNT` | `N2` |
| 30 | `BF-TXT-B0` | BitForge | `TXT` | `B0` |

### Pilot acceptance and stopping rules

Stop the pilot immediately if any of these occurs:

- authentication fails;
- a route rejects the documented payload shape;
- an endpoint reports an unexpected charge above 1 generation per image;
- three consecutive transient server failures occur after bounded backoff; or
- saved image bytes, request records, or usage records cannot be verified.

Do not silently retry a request after an uncertain timeout. Mark it `submission-unknown`
so a retry cannot double-charge or create an untracked duplicate.

After all accepted calls are captured:

- If `B0` never exhibits the target failure for a family on either endpoint, that family
  is non-informative for efficacy. Replace it only in a new protocol revision and rerun
  calibration; do not tune it inside this dataset.
- If reviewers cannot apply the target rubric consistently, revise the rubric in a new
  protocol version before confirmation.
- If PixFlux rejects the deprecated field, record a schema/implementation defect and do
  not resubmit alternate negative syntax.
- If the field-bearing image bytes are identical to baseline while `B0` and `R0` are also
  identical, treat this only as pilot evidence of a no-op; confirmation is still required
  for a durable rule.

## Phase 0B — Replacement-Family Calibration

Status: executed 2026-08-08; 30/30 calls completed with 30 reported generations, zero
errors, and zero retries.

Phase 0 found that the original text and style baselines never clearly failed on either
endpoint. The BitForge sword baseline also passed. The then-proposed symmetric 180-call
confirmation was withheld until replacement families demonstrated a usable baseline
failure rate; Phase 0B retained only BitForge `TXT2`, enabling the smaller executed Phase
1 matrix.

Phase 0B tests three stronger natural priors without putting a literal contradiction in
the positive description. It uses seed block 2 (`8382088`) and the same common 64×64,
`text_guidance_scale: 8`, `no_background: true` payload. `B0`, `P1`, and `R0` omit
`negative_description`; `N1` and `N2` add it. `R0` is byte-identical to `B0`.

### `SUB` — unwanted subject

Target: an unoccupied scene with no visible person or animal.

- Base (`B0`, `N1`, `N2`, `R0`): `Moonlit forest campsite with a small campfire centered between dark pine trees.`
- Concise negative (`N1`): `people, characters, animals`
- Long negative (`N2`): `people, characters, animals, travelers, campers, human silhouettes, faces, hands, birds, wolves, deer, horses, text, watermark, blur, cropped objects`
- Positive rewrite (`P1`): `Empty moonlit forest clearing centered on one unattended campfire between dark pine trees.`

### `TXT2` — stronger text prior

Target: three pictorial arrow boards without letter-like or number-like marks.

- Base (`B0`, `N1`, `N2`, `R0`): `Wooden fantasy directional signpost with three arrow-shaped boards at a crossroads.`
- Concise negative (`N1`): `text, letters, words, numbers`
- Long negative (`N2`): `text, letters, words, numbers, writing, labels, signatures, watermarks, typography, runes, glyphs, slogans`
- Positive rewrite (`P1`): `Wooden fantasy directional signpost with three arrow-shaped boards: one red sword pictogram, one blue potion pictogram, and one green tree pictogram, with each pictogram centered on its board.`

### `PRJ` — projection prior

Target: a straight front elevation with no visible side wall or diagonal depth.

- Base (`B0`, `N1`, `N2`, `R0`): `Small wooden cottage with a red door and two windows, full building visible.`
- Concise negative (`N1`): `isometric view, three-quarter view, visible side wall, diagonal perspective`
- Long negative (`N2`): `isometric view, three-quarter view, visible side wall, diagonal perspective, aerial view, top-down view, tilted camera, vanishing point, corner-facing building, rear view, cropped building`
- Positive rewrite (`P1`): `Straight front elevation of one small wooden cottage, facade parallel to the screen, one centered red door and two front windows, full rectangular building visible.`

### Phase 0B call count and order

- 2 endpoints × 3 replacement families × 4 comparison arms = 24 calls.
- One exact repeat for every endpoint/family = 6 calls.
- Total: **30 paid calls**, expected about **30 generations**.
- Phase 0 approval does not authorize these calls.

The order below was frozen with deterministic shuffle seed `20260809`:

| Order | Request ID | Endpoint | Family | Arm |
|---:|---|---|---|---|
| 1 | `PF-TXT2-N2` | PixFlux | `TXT2` | `N2` |
| 2 | `BF-SUB-N2` | BitForge | `SUB` | `N2` |
| 3 | `BF-SUB-P1` | BitForge | `SUB` | `P1` |
| 4 | `PF-TXT2-R0` | PixFlux | `TXT2` | `R0` |
| 5 | `PF-SUB-N1` | PixFlux | `SUB` | `N1` |
| 6 | `BF-TXT2-P1` | BitForge | `TXT2` | `P1` |
| 7 | `PF-PRJ-B0` | PixFlux | `PRJ` | `B0` |
| 8 | `PF-SUB-R0` | PixFlux | `SUB` | `R0` |
| 9 | `PF-PRJ-P1` | PixFlux | `PRJ` | `P1` |
| 10 | `BF-PRJ-N1` | BitForge | `PRJ` | `N1` |
| 11 | `PF-TXT2-P1` | PixFlux | `TXT2` | `P1` |
| 12 | `PF-PRJ-R0` | PixFlux | `PRJ` | `R0` |
| 13 | `BF-PRJ-R0` | BitForge | `PRJ` | `R0` |
| 14 | `BF-TXT2-N2` | BitForge | `TXT2` | `N2` |
| 15 | `PF-TXT2-B0` | PixFlux | `TXT2` | `B0` |
| 16 | `BF-TXT2-N1` | BitForge | `TXT2` | `N1` |
| 17 | `BF-PRJ-P1` | BitForge | `PRJ` | `P1` |
| 18 | `BF-TXT2-B0` | BitForge | `TXT2` | `B0` |
| 19 | `BF-SUB-R0` | BitForge | `SUB` | `R0` |
| 20 | `PF-PRJ-N1` | PixFlux | `PRJ` | `N1` |
| 21 | `PF-TXT2-N1` | PixFlux | `TXT2` | `N1` |
| 22 | `BF-PRJ-B0` | BitForge | `PRJ` | `B0` |
| 23 | `BF-SUB-N1` | BitForge | `SUB` | `N1` |
| 24 | `BF-TXT2-R0` | BitForge | `TXT2` | `R0` |
| 25 | `BF-SUB-B0` | BitForge | `SUB` | `B0` |
| 26 | `PF-SUB-P1` | PixFlux | `SUB` | `P1` |
| 27 | `PF-SUB-B0` | PixFlux | `SUB` | `B0` |
| 28 | `PF-PRJ-N2` | PixFlux | `PRJ` | `N2` |
| 29 | `BF-PRJ-N2` | BitForge | `PRJ` | `N2` |
| 30 | `PF-SUB-N2` | PixFlux | `SUB` | `N2` |

Retain a replacement family for confirmation only if at least one endpoint's `B0` or
`R0` clearly exhibits its target failure and blind reviewers can apply the rubric. A
family may be retained for one endpoint and rejected for the other; confirmation does not
need a falsely symmetric family set.

## Blinded Scoring Protocol

Generate the blinded index only after all images in a phase are saved. Reviewers receive
opaque candidate IDs and shuffled images, with endpoint, family, arm, prompt, seed, and
filename concealed. Reviewers must score independently before adjudication. Do not use
PixelLab employee opinions or archived manifest judgments as labels.

Use two independent blinded reviewers, with a third reviewer adjudicating only disputed
primary outcomes. Triangulate visual judgments with deterministic measurements; no one
human or model review is treated as unquestionable ground truth.

### Primary outcome

Target-failure severity:

| Score | Meaning |
|---:|---|
| 0 | Clearly absent |
| 1 | Ambiguous or too unclear to decide |
| 2 | Clearly present |
| 3 | Present and visually dominant |

The binary primary outcome is `failure = true` for scores 2-3. Score 1 remains missing
for the primary analysis and is reported separately; it must not be forced into the arm's
favored category.

Family-specific anchors:

- `CNT`: failure means other than exactly two whole sword objects, including a third,
  detached duplicate, or fused extra blade.
- `TXT`: failure means an independent visual reviewer sees letter-like, number-like,
  word-like, rune-like, or watermark-like marks. The single intended bottle pictogram is
  exempt.
- `STY`: failure means smooth gradient rendering, photographic material response, or
  clearly 3D-rendered volume dominates over hard limited-color pixel construction.

### Secondary outcomes

Score each from 1 (worst) to 5 (best):

- overall visual quality;
- compliance with the intended object/composition;
- silhouette/readability at native 64×64 size; and
- artifact freedom.

Also record a short defect tag list. For `TXT`, OCR is a secondary flag only because OCR
at 64×64 can miss invented glyphs. For `STY`, record opaque unique-color count, alpha
coverage, and a gradient/edge-softness metric. Automated metrics support but do not
replace blinded visual scoring.

## Phase 1 — Confirmatory Static Study

Status: executed exactly as frozen; 46/46 calls completed with 46 reported generations,
zero errors, and zero retries.

The calibrations retain one informative family per endpoint:

- PixFlux `CNT`, using the original crossed-swords prompt and its concise/long negatives.
  Seed block 1 already exists; run blocks 2-8.
- BitForge `TXT2`, using the replacement directional-signpost prompt and its
  concise/long text negatives. Seed block 2 already exists; run blocks 1 and 3-8.

Confirmation isolates the dedicated-field estimate and therefore uses `B0`, `N1`, and
`N2`, not `P1`. Positive strategy remains a documented secondary result from calibration.

- 2 endpoint-family pairs × 7 new seeds × 3 arms = **42 calls**.
- Add two exact baseline repeats per endpoint-family = **4 calls**.
- Phase 1 total: **46 calls**, expected about **46 generations**.
- Combined Phase 0 + Phase 0B + Phase 1: **106 calls/generations**.

Every call keeps the applicable frozen description/negative text, 64×64 size,
`text_guidance_scale: 8`, and `no_background: true`. `R0` is byte-identical to its
same-seed `B0`. Phase 1 was separately approved before execution.

The order below was frozen with deterministic shuffle seed `20260810`:

| Order | Request ID | Order | Request ID |
|---:|---|---:|---|
| 1 | `PF-CNT-S6-N1` | 24 | `PF-CNT-S7-B0` |
| 2 | `BF-TXT2-S4-B0` | 25 | `PF-CNT-S8-B0` |
| 3 | `BF-TXT2-S5-B0` | 26 | `PF-CNT-S8-N1` |
| 4 | `BF-TXT2-S8-N2` | 27 | `PF-CNT-S7-N1` |
| 5 | `BF-TXT2-S8-B0` | 28 | `PF-CNT-S2-R0` |
| 6 | `PF-CNT-S2-N2` | 29 | `PF-CNT-S5-B0` |
| 7 | `BF-TXT2-S5-N2` | 30 | `PF-CNT-S2-N1` |
| 8 | `PF-CNT-S6-B0` | 31 | `BF-TXT2-S1-N2` |
| 9 | `PF-CNT-S3-N1` | 32 | `PF-CNT-S7-N2` |
| 10 | `PF-CNT-S3-N2` | 33 | `BF-TXT2-S1-N1` |
| 11 | `BF-TXT2-S7-N2` | 34 | `PF-CNT-S4-N1` |
| 12 | `PF-CNT-S5-N2` | 35 | `BF-TXT2-S6-N2` |
| 13 | `BF-TXT2-S4-R0` | 36 | `BF-TXT2-S8-N1` |
| 14 | `PF-CNT-S6-N2` | 37 | `PF-CNT-S4-B0` |
| 15 | `PF-CNT-S4-N2` | 38 | `BF-TXT2-S3-B0` |
| 16 | `BF-TXT2-S4-N2` | 39 | `BF-TXT2-S7-B0` |
| 17 | `BF-TXT2-S3-N1` | 40 | `BF-TXT2-S6-N1` |
| 18 | `BF-TXT2-S1-B0` | 41 | `BF-TXT2-S3-R0` |
| 19 | `BF-TXT2-S5-N1` | 42 | `BF-TXT2-S4-N1` |
| 20 | `PF-CNT-S5-N1` | 43 | `PF-CNT-S2-B0` |
| 21 | `BF-TXT2-S6-B0` | 44 | `PF-CNT-S3-R0` |
| 22 | `BF-TXT2-S3-N2` | 45 | `PF-CNT-S3-B0` |
| 23 | `BF-TXT2-S7-N1` | 46 | `PF-CNT-S8-N2` |

### Executed Result

The frozen order, bodies, seeds, and call count were preserved. Two independent blind
reviewers scored all 46 new candidates; a third blind reviewer adjudicated eight BitForge
text disagreements. Combining the retained calibration seeds with Phase 1 produced 32
paired negative-arm comparisons:

| Classification | Count |
|---|---:|
| Helpful | 0 |
| No observed effect | 25 |
| Worse | 1 |
| Adverse signal | 2 |
| Inconclusive | 4 |

PixFlux had no target-outcome discordances across either negative wording at eight seeds.
BitForge never produced a clear text-free signpost; one pair crossed the material-quality
harm threshold and two changed ambiguous baselines into clear failures. Full paired scores,
limitations, repeat metrics, and the runtime decision are in the Phase 1 results document.

Analyze each endpoint separately. The primary comparison is paired `N1` versus `B0` at
the same endpoint, family, and seed. Report the paired failure-rate difference, exact or
bootstrap 95% confidence interval, discordant-pair counts, and a paired test such as
McNemar's test. Analyze ordinal quality as paired data and publish its full distribution.
Report family-stratified results even when an endpoint-level summary is shown.

### Practical decision bands

For each endpoint:

- **Benefit:** the negative arm reduces primary failures by at least 20 percentage points,
  its uncertainty does not include zero, and median quality is not more than 0.5 points
  lower.
- **Harm:** primary failures increase by at least 20 percentage points, or median quality
  drops by at least 1 point with degradation in at least 25% of paired outputs.
- **No meaningful effect:** the 95% interval for the paired failure-rate difference lies
  wholly inside -10 to +10 percentage points and paired quality change lies wholly inside
  -0.5 to +0.5 points.
- **Inconclusive:** none of the above, baseline failures are too rare, repeat variability is
  too high, or reviewer ambiguity exceeds 20%.

The bands are practical engineering thresholds, not claims about human perception in
every context.

Applied after execution, neither endpoint satisfies the formal benefit, harm, or
equivalence band. PixFlux has zero observed target discordances but eight seeds leave the
exact uncertainty wider than the ±10-point equivalence region. BitForge has target
ambiguity in three of eight baselines (37.5%), above the 20% rule. The endpoint-level
statistical declaration is therefore **inconclusive**, while the individual paired record
still contains zero helpful results, mostly no observed effects, one quality harm, and two
adverse signals. This distinction prevents “not formally equivalent” from being
misreported as benefit or harm.

## Sequential Extension For A No-Effect Claim

Eight seeds can detect a large effect but may not support equivalence. If Phase 1 is
inconclusive only because intervals are too wide, extend the same frozen matrix in batches
to 16 seeds and then at most 32 seeds. Recompute at the batch boundary; do not stop after
an especially favorable individual image.

Maximum dedicated-field confirmation size at 32 seeds:

- 2 endpoint-family pairs × 3 causal arms × 32 seeds = **192 calls**;
- plus the frozen repeat subset;
- approval and cost accounting are required before every extension batch.

If the maximum still cannot classify an endpoint, publish `inconclusive`. Do not convert
absence of proof into “negatives are harmless” or “negatives are harmful.”

## Later Route-Specific Studies

These phases answer different questions and require their own frozen addenda and paid-call
approval:

1. **Induction probe on dedicated-field routes:** compare a neutral baseline against an
   unrelated but visually salient forbidden noun to test whether naming the noun makes it
   appear. This is not mixed into the efficacy prompts.
2. **Pixen inline negation:** compare baseline, concise inline exclusion, long inline
   exclusion, and positive structure. This tests the main description channel, not a
   dedicated field.
3. **Create Image Pro inline negation:** a separate high-cost study; candidates returned by
   one call are not independent seeds.
4. **Base inpaint:** reuse one source and one mask within each seed block and compare only
   the documented base endpoint that exposes `negative_description`.
5. **Legacy animation:** test its separate field independently from modern v3 animation.
6. **Modern v3 animation:** compare inline action wording only; the route has no separate
   field.

Static-image conclusions must not be promoted to these routes before their own evidence
exists.

## Post-Confirmation Testing Roadmap

The 106-call study answered the immediate routing question: automatic negative insertion
has no demonstrated benefit. Further testing should now distinguish three narrower claims
rather than accumulate more unstructured examples.

### Priority 1 — BitForge forbidden-noun induction probe

Question: does placing an otherwise absent, visually salient object noun only in
`negative_description` increase that object's appearance rate?

Use two neutral prompt families with independently scoreable nouns, such as a red balloon
and a black cat. Freeze each neutral scene so the target object is neither implied nor
incompatible. For every family and seed, compare:

| Arm | Positive description | `negative_description` | Role |
|---|---|---|---|
| `B0` | Neutral frozen scene | omitted | Spontaneous target rate. |
| `I1` | Same as `B0` | Target noun only | Direct induction test. |
| `Q1` | Same as `B0` | `blur, watermark` | Field-present control that does not name the target. |
| `P1` | Same scene explicitly containing the target | omitted | Detectability/model-capability control; not part of the causal estimate. |

Start with four seeds: 2 families × 4 seeds × 4 arms = **32 calls**. Continue to 16 total
seeds only when both positive controls render the target in at least 75% of outputs and
baseline target appearance stays below 25%. The extension adds 2 × 12 × 4 = **96 calls**,
for a maximum of **128 calls**.

Primary analysis is paired `I1` versus both `B0` and `Q1`. Declare an induction signal
only if target appearance rises by at least 20 percentage points against both controls and
the paired interval excludes zero. Score general quality separately. A noun appearing in
one image is a counterexample to “this can never happen,” but is not enough to claim a
mechanism.

The exact nouns, positive descriptions, seeds, shuffled order, and expected cost must be
frozen in an addendum before approval. Do not reuse the signpost family: its pseudo-writing
prior makes noun induction hard to distinguish from ordinary generation behavior.

### Priority 2 — Formal equivalence extension, only if needed

If a formal PixFlux/BitForge no-effect interval is required, preserve the existing frozen
confirmation wordings and add seed blocks only at registered boundaries:

- 8→16 seeds: 2 endpoint-family pairs × 8 new seeds × 3 arms = **48 calls**, plus four
  time-separated baseline anchors = **52 calls**.
- 16→32 seeds: 2 pairs × 16 new seeds × 3 arms = **96 calls**, plus four anchors =
  **100 calls**.

Recompute only at each boundary. Stop when the paired target interval lies inside the
pre-registered ±10-point equivalence band and paired quality stays inside ±0.5, or at 32
seeds. This extension has lower practical priority than the induction probe because the
current default already follows from zero observed wins and limited adverse evidence.

### Priority 3 — Current Pixen inline-negation stratum

Pixen exposes no dedicated negative field. Use two scoreable families, eight seeds, and
four arms: baseline, concise inline exclusion, long inline catalog, and positive
structural rewrite. Keep REST `enhance_prompt: false`; otherwise prompt enhancement would
be an additional routing transformation. This is **64 calls**, with a four-call exact
repeat subset for **68 calls** total.

Run REST and MCP as separate strata if both surfaces matter. A smaller surface-interaction
pilot can use two families × four seeds × two wording arms (`B0`, concise inline) × two
surfaces = **32 calls**. Even with matched core fields and seeds, label any difference as a
surface/workflow interaction; public observation cannot identify which hidden router or
model component caused it.

### Priority 4 — Current Create Image Pro inline-negation stratum

REST `generate-image-v2` and MCP `create_image_pro` expose no dedicated negative field.
They therefore test inline wording, not `negative_description`. Start with two families ×
two registered call blocks × four arms = **16 Pro calls**: baseline, concise inline
exclusion, long inline catalog, and positive structural rewrite. Continue to eight total
blocks only if baseline failures and target scoring are informative, adding **48 calls**
for a maximum of **64 Pro calls**.

Pro may return many same-prompt candidates from one small-size call. Those candidates are
correlated and are not independent seeds: preserve every candidate, score all of them,
and use the paid call—not each image—as the statistical cluster. REST and MCP remain
separate route strata.

### Priority 5 — Operation-specific v3/new studies

`v3` and `new` do not name one universal current model. Character v3/new, Character Pro,
modern animation v3, and Pro/v3 inpaint are separate workflows and expose no dedicated
negative field. Test them only with an asset-specific question:

- character v3/new versus Character Pro: fixed character briefs, view, and reference
  state; analyze each route independently;
- animation v3: fixed first/last frame anchors and inline `action` wording; score every
  frame and temporal artifacts;
- Pro/v3 inpaint: fixed source, mask, crop, and context; score masked-region compliance
  and collateral change.

Do not combine their estimates under a single “v3” result. Base inpaint and legacy
animation, which do expose `negative_description`, require their own dedicated-field
studies.

### Approval boundary

None of this roadmap authorizes calls. Each phase must show the exact frozen request matrix
and predicted usage, then pass the PixelLab Pip paid-generation gate. Approval for one
phase does not authorize the next.

## Artifact And Execution Contract

Save the live study under:

```text
pixellab-pip-generations/negative-prompt-study-YYYYMMDD/
  protocol.md
  requests.jsonl
  responses/
  images/
  blinded-index.json
  scores-reviewer-a.jsonl
  scores-reviewer-b.jsonl
  adjudication.jsonl
  analysis.json
  manifest.json
  negative-prompt-study.blueprint.json
```

For every request, persist the literal request body before submission, then record HTTP
status, returned usage, image hash, dimensions, mode, alpha coverage, elapsed time, and
any error. Never store or print the bearer token. Validate every decoded PNG before
marking the call complete.

The execution runner must be resumable and append-only. A completed request ID is never
submitted again. An uncertain request remains quarantined until its charge/result status
is resolved manually.

## Cost Gate

No live generation is authorized by this document alone. Phase 0 and Phase 0B were each
approved and executed. Immediately before any later paid phase:

1. read Pip's persistent auto-generation preference exactly once;
2. verify the bearer token exists without revealing it;
3. show every exact paid call, its prompt, endpoint, seed, and predicted total;
4. if auto-generation is off, wait for explicit approval; and
5. do not infer approval from an earlier phase.

## Promotion Rule

Change the runtime recommendation only after a phase has preserved requests and outputs,
locked blinded scores, repeat controls, endpoint-specific effect estimates, and a declared
decision under the bands above. Report counterexamples and failed prompts alongside
successful ones. A developer statement, attractive anecdote, or single pair cannot
override the controlled evidence.
