# PixelLab Negative Prompting Phase 0B Results

Executed: 2026-08-08.

Status: replacement-family calibration complete; endpoint-specific confirmation planned.

Companions:

- Initial calibration: `pixellab-negative-prompting-calibration-results.md`
- Research spike: `pixellab-negative-prompting-research-spike.md`
- Controlled plan: `../plans/pixellab-negative-prompting-controlled-test-plan.md`

## Result In One Sentence

BitForge's dedicated field again changed images beyond repeat variation but did not prevent
clear pseudo-writing in the only informative replacement family; PixFlux's three
replacement baselines did not clearly fail, so none can estimate negative-prompt benefit.

This is a result for the deployed PixFlux/BitForge endpoint stacks, not an intrinsic claim
about negative language. Model priors, routing, prompt-field weighting, and any hidden
server-side conditioning remain inseparable moderators. Pixen, Create Image Pro, and
v3/new workflows were not controlled in this phase.

## What Ran

- REST PixFlux and BitForge
- Replacement families: unwanted campsite subjects (`SUB`), signpost text (`TXT2`), and
  cottage projection (`PRJ`)
- Arms: baseline, concise negative, long negative, positive structural rewrite, and exact
  baseline repeat
- Seed `8382088`
- 64×64, `text_guidance_scale: 8`, `no_background: true`
- Thirty calls in the frozen shuffled order

The private run record is in
`pixellab-pip-generations/negative-prompt-study-phase0b-20260808/`.

## Operational Outcome

| Measure | Result |
|---|---:|
| Approved calls | 30 |
| Completed and validated PNGs | 30 |
| Charged generations reported by PixelLab | 30 |
| Rejections, retries, or unknown submissions | 0 |

## Blinded Review

Two independent reviewers scored opaque candidate IDs for visible person/animal shapes,
text-like marks, projection, quality, readability, and artifacts. A third blind reviewer
adjudicated four binary campsite disagreements and five ambiguous PixFlux signpost marks.

The campsite disagreements were real visual ambiguity: small central shapes could be read
as animals, flowers, foliage, or flame. The adjudicator found no clear person or animal.
PixFlux signpost marks were consistently ambiguous grain or ornament rather than clear
writing.

## Adjudicated Outcomes

### PixFlux

| Family | Baseline | Concise negative | Long negative | Positive rewrite | Repeat |
|---|---|---|---|---|---|
| `SUB` campsite subject | pass | pass | pass | pass | pass |
| `TXT2` signpost text | ambiguous | ambiguous | ambiguous | ambiguous pictograms | ambiguous |
| `PRJ` cottage projection | pass: front | pass: front | pass: front | pass: front | pass: front |

No PixFlux replacement baseline clearly failed. The families are therefore unsuitable for
confirming benefit, even though they still provide evidence that negatives caused no
obvious semantic regression in this seed.

### BitForge

| Family | Baseline | Concise negative | Long negative | Positive rewrite | Repeat |
|---|---|---|---|---|---|
| `SUB` campsite subject | ambiguous | ambiguous | ambiguous | pass | ambiguous |
| `TXT2` signpost text | **fail** | **fail** | **fail** | **fail** | **fail** |
| `PRJ` cottage projection | pass: front | pass: front | pass: front | pass: front | pass: front |

Every BitForge signpost contained clear repeated pseudo-writing. Neither the concise
`text, letters, words, numbers` field nor the longer catalog reduced the target failure.
The positive pictogram rewrite also failed, so this subject has a strong mark-filling prior
that none of the tested text strategies overcame.

## Repeat And Field-Activity Evidence

No Phase 0B exact repeat was byte-identical, but BitForge repeats were extremely close:

| BitForge family | Baseline-repeat RGBA difference | Concise-negative difference | Long-negative difference |
|---|---:|---:|---:|
| `SUB` | 0.0060 | 0.0900 | 0.1028 |
| `TXT2` | 0.0004 | 0.0701 | 0.0851 |
| `PRJ` | 0.0046 | 0.0578 | 0.0509 |

This independently repeats Phase 0's finding that BitForge's field is behaviorally active.
The output changes are much larger than baseline-repeat variation. Yet target outcomes did
not improve, demonstrating why “the field changes the image” must not be reported as “the
field helps.”

PixFlux negative-arm differences were generally within or near its larger repeat
variation, and no target outcome changed. The long campsite arm differed more than its
repeat numerically, but both images still contained no clear person or animal. This remains
consistent with no-op or weak semantic control on the tested PixFlux build.

## Quality

No negative arm produced a material endpoint-wide quality loss. The only 0.5-point
family-level drop was BitForge's concise projection arm; its projection still passed.
Positive rewrites lowered average quality in several Phase 0B families because the more
constrained compositions were visually plainer or more cluttered. This is another reason
to score target compliance and quality separately.

## Combined Phase 0 + Phase 0B Evidence

The two calibrations consumed 60 generations and provide two informative endpoint-family
pairs:

1. **PixFlux crossed-sword count:** baseline, concise negative, and long negative all
   failed to render swords; the positive structural rewrite succeeded.
2. **BitForge signpost text:** baseline, concise negative, long negative, and positive
   rewrite all contained pseudo-writing.

Across those informative pairs, negative prompting has produced **zero observed target
improvements**. It has also produced no material overall-quality harm. This is meaningful
directional evidence, but each pair currently has only one seed and cannot support a
stable endpoint rule.

## Decision

- Drop `SUB` and `PRJ` from confirmation.
- Do not force symmetric prompt families across endpoints.
- Confirm PixFlux only on the informative crossed-sword family from Phase 0.
- Confirm BitForge only on the informative signpost family from Phase 0B.
- Compare `B0`, `N1`, and `N2`; positive strategy is already documented but is not part of
  the dedicated-field causal estimate.
- Expand to eight total seeds per endpoint-family, with extra repeat controls.

The revised confirmation is 46 calls rather than the obsolete 180-call symmetric matrix.
It is cheaper and more informative.

## Current Verdict

The evidence still rejects both universal claims:

- There is no controlled evidence that negative prompting generally makes PixelLab worse.
- There is now repeated controlled evidence that a dedicated negative can change BitForge
  without improving the named failure.
- There is controlled one-seed evidence that PixFlux negatives did not rescue a failure
  that positive structural wording did rescue.

The appropriate label remains **endpoint-specific and inconclusive**, with a growing
negative result for efficacy rather than evidence of broad harm.
