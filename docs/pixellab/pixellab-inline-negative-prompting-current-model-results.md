# PixelLab Inline Negative Prompting — Current-Model Results

## New-tool results — 2026-09-29

**Practical answer: inline negative wording has no demonstrated general benefit on
PixMiniMax or the tested Pro Flash operations.** The controlled run completed 246
REST calls plus 12 MCP parity calls. Under the registered decision thresholds, the
54 negative-involving REST contrasts classify as **0% beneficial, 0% harmful, 0%
proven no-meaningful-effect, and 100% inconclusive**. That is an underpowered
evidence classification, not a claim that 100% had no effect.

The clearest observations point toward caution, not a new recommendation:

- PixMiniMax's no-sparks clause and its positive comparator both failed the
  registered flame constraint in all 3/3 core clips, as did baseline. Its prompt
  enhancer removed the exclusions from the returned prompt in all 3/3 negative
  cases.
- On one Pro Flash edit task, residual `OX7` lettering appeared in 2/3 baseline
  outputs and 3/3 when an unrelated `No red balloon in the upper-left sky`
  clause was added.
  Paired directions were 0/3 better, 1/3 worse, and 2/3 tied; this is a small,
  inconclusive adverse signal, not proof of harm.
- In the forbidden-object sentinel, the red balloon appeared in 0/12 baseline
  calls and 0/12 calls that said not to include it; positive controls produced
  it in 12/12. The negative wording did not induce it in this sample.

The tested REST and MCP schemas expose `description` but no explicit
`negative_prompt` field, so there is no dedicated-field generation result.
PixelLab's live Pro Flash capability metadata reported
`provider_model=gpt-image-2.5-flare`; the live MCP tool metadata labels
PixMiniMax as powered by MiniMax H3. These are PixelLab-reported labels, not an
independent backend audit, and provide no evidence that Pro Flash is secretly
MiniMax.

**Recommendation:** don't add negative boilerplate by default. Prefer a positive
description of the desired result; use a short exclusion only for a specific,
reproducible failure and inspect the output. For PixMiniMax, leave prompt
enhancement off when the exclusion must survive, or review its expanded prompt.

Full methods, limits, route coverage, and results: [new-tool study report](pixellab-inline-negative-prompting-new-tool-results.md).
The model-by-model capability table, including earlier Pixen and Create Image Pro results, is in [inline results by route](pixellab-inline-negative-prompting-best-practices.md#pixellab-inline-results-by-route).

---

## Historical prior study — 2026-08-08

Executed: 2026-08-08.

Status: Stage A generation complete; 76 paid REST calls, 124 candidates, and blinded
machine-vision dual review with adjudication. Independent human visual validation is
pending.

Companions:

- Best-practice research: `pixellab-inline-negative-prompting-best-practices.md`
- Frozen plan: `../plans/pixellab-inline-negative-prompting-current-model-test-plan.md`
- Historical dedicated-field result: `pixellab-negative-prompting-confirmation-results.md`

## Verdict

### At a glance

Across 33 inline-negative treatment calls—16 concise exclusions (`C1`), 11 long lists
(`L1`), and 6 forbidden-noun probes (`I1`)—the blinded call-level classifications were:

| Outcome | Calls | Share |
|---|---:|---:|
| Helpful | 3 | 9.1% |
| Worse | 8 | 24.2% |
| No observed effect | 19 | 57.6% |
| Inconclusive | 3 | 9.1% |

For concise exclusions alone, 3/16 calls helped, 2/16 worsened, 10/16 had no observed
effect, and 1/16 was inconclusive. All three helpful calls were on Pro; both concise-call
regressions were on Pixen. Pro's pseudo-text failures fell from 7/8 baseline candidates to
1/8 with concise exclusions across two paid calls. On Pixen, `No red balloon.` produced a
red balloon in all four registered seeds and the exact repeat, while the neutral and
matched-negative controls produced none.

These are descriptive shares of this small, mixed task set, not probabilities for arbitrary
prompts. “No observed effect” is not a formal equivalence finding; Pro siblings are counted
within their paid call, and independent human visual validation is still pending.

**Practical result:** concise inline exclusions can help on a specific Pro pseudo-text
failure, but there is no broad benefit; most calls showed no change, and naming a forbidden
object can backfire on Pixen. Use exclusions only for a specific, testable issue, and prefer
describing the desired visible state when an absent object might become salient.

Neither blanket claim survived current-model testing:

- Negative prompting is **not generally bad**. On Create Image Pro/v2, concise inline
  exclusions reduced pseudo-text failures from 7/8 baseline candidates to 1/8 across two
  independent paid call blocks.
- Negative prompting is **not harmless or reliably beneficial**. On Pixen/v3/new, `No
  red balloon.` generated a visible red balloon in 4/4 registered seeds and again in the
  exact repeat, while 0/4 neutral baselines and 0/4 matched `No black cat.` controls
  contained a red balloon.
- Many effects were **task-dependent no-ops**. Pixen text exclusions had no observable
  benefit because every tested baseline already passed. Pixen projection exclusions did
  not overcome its view prior; all 9 concise/long negative calls still failed.
- Positive structural wording remains a distinct strategy, not proof that negatives are
  bad. It fixed Pixen projection in all 3 seeds where baseline, concise, and long-negative
  arms all failed.

The operational answer is conditional: use a short, targeted inline exclusion when the
selected route and failure mode have evidence it can help; describe the desired visible
state when naming an otherwise absent object risks introducing it. Do not attach broad
negative boilerplate automatically.

## Execution And Cost

| Route | Calls | Returned images | Returned usage |
|---|---:|---:|---:|
| Pixen/v3/new, `create-image-pixen` | 60 | 60 | 60 generations |
| Create Image Pro/v2, `generate-image-v2` | 16 | 64 | 320 generations |
| **Total** | **76** | **124** | **380 generations** |

The subscription balance decreased by 382 generations during the run. Per-response usage
sums to 380; the two-generation discrepancy cannot be attributed from these records and
could reflect concurrent account activity or accounting timing. It is preserved rather
than forced to match.

Every request used REST v2 at 96×96 with a registered seed. Pixen prompt enhancement was
explicitly false. Raw request bytes, submit responses, Pro terminal responses, all PNGs,
hashes, usage, and balance snapshots are preserved under the gitignored run directory
`pixellab-pip-generations/negative-prompt-study-current-models-20260808/`.

The personal all-attempt audit is
`.local/pixellab-inline-negative-prompting-current-model-all-attempts.html`. It embeds all
124 images and lists every call, endpoint, description, input, raw-file link, blinded
score, and helpful/no-op/worse/inconclusive classification. It is intentionally not part
of the repository.

The separate personal human-review workbook is
`.local/pixellab-inline-negative-prompting-human-review.html`. It presents every exact
request and all 124 outputs, keeps the machine conclusions hidden by default, and lets a
human reviewer score each output plus classify each negative-treatment call as good
influence, no-op, bad influence, or inconclusive. Decisions autosave locally and can be
exported/imported as JSON. Human scores have not yet been incorporated into the verdicts
below.

## Review Integrity And Limitation

Two AI reviewers independently scored opaque candidate IDs with route, arm, seed, repeat,
and Pro sibling membership hidden. Primary-outcome agreement was 87.1%. A third AI
reviewer, also blinded, adjudicated the 17 candidates with any primary or
induction-presence disagreement. Pro candidates were all scored and reduced to paid-call
clusters; none was selected as a “best” result.

This controls treatment anchoring but not shared machine-vision failure modes. The current
visual labels and derived good/no-op/bad classifications are therefore provisional until
the independent human workbook is completed and reconciled. Literal request, response,
usage, hash, and API-validity facts do not depend on visual judgment.

## Core Results

### Pixen/v3/new

| Family | Baseline | Concise inline exclusion | Long negative | Positive rewrite | Interpretation |
|---|---:|---:|---:|---:|---|
| Count | 0/3 clear failures, 1/3 ambiguous | 1/3 failures | 1/3 failures | 0/3 failures | One concise and one long arm regressed at `S1`; the exact `B0` pass and `C1` failure both repeated. Other blocks were no-op/inconclusive. |
| Pseudo-text | 0/3 failures | 0/3 | 0/3 | 0/3 | Ceiling: every strategy passed, so negatives were no-op rather than demonstrated benefit. |
| Projection | 3/3 failures | 3/3 | 3/3 | 0/3 | Negative wording did not overcome the model/route view prior; explicit front-elevation structure did. |

The count regression is not universal Pixen induction evidence by itself. It is useful
because it repeated byte-for-byte at `S1`; the separate noun sentinel supplies the direct
induction test.

### Create Image Pro/v2

| Family | Baseline candidates failed | Concise candidates failed | Result |
|---|---:|---:|---|
| Count | 1/8 | 0/8 | One block no-op; one improved from 1/4 to 0/4. Small favorable signal, not a stable endpoint rate. |
| Pseudo-text | 7/8 | 1/8 | Both paid blocks improved: 4/4→0/4 and 3/4→1/4. Strong calibration benefit with similar mean quality. |

The one Pro long text call had 0/4 clear failures but 1/4 ambiguous and therefore remains
inconclusive. The positive pictogram rewrite passed 4/4; it is a useful strategy result,
not a causal estimate of negative wording.

## Direct Forbidden-Noun Induction

| Route | Neutral `B0` red balloons | `No red balloon` | Matched `No black cat` | Positive capability |
|---|---:|---:|---:|---:|
| Pixen | 0/4 | **4/4**, plus repeat 1/1 | 0/4 | 4/4 |
| Pro | 0/4 candidates | 0/4 | 0/4 | 3/4 present, 1/4 ambiguous |

This is a route interaction, not an abstract lexical law. The Pixen result satisfies the
registered large-signal rule and survives an exact time-separated repeat. Pro showed a
no-op under the cost-minimized one-call sentinel. A general mechanism claim would still
require a second preregistered noun and context.

## What Changes In Practice

1. Inline exclusions are legitimate negative prompting even without a dedicated field.
2. On Pro, concise task-specific exclusions are worth trying for visible pseudo-text; the
   current count evidence is promising but small.
3. On Pixen, do not name an otherwise absent object solely to prohibit it. Describe the
   intended empty/replacement state instead.
4. On Pixen projection/view problems, use positive structural wording or a route/control
   change; repeating negative view terms did not help here.
5. Keep long generic negative catalogs separate from targeted constraints. This run found
   no reliable advantage over concise wording.
6. Treat prompt wording, route, model prior, prompt processor, task, and service build as
   one deployed treatment. The public data cannot assign the effect to a hidden system
   prompt or model component.

## Limits And Next Test

- Pixen has three independent core seeds; Pro intentionally has only two primary call
  blocks per family to control cost.
- Pro's four siblings per call are correlated and were never treated as four independent
  calls.
- The count and projection families are small. “No meaningful effect” was not established
  with a narrow equivalence interval.
- Exact seeds may not identify the same latent state across routes.
- The service build and hidden routing stack can change.

The 40 Pro calls removed for cost are listed as a TODO in
`pixellab-negative-prompting-research-spike.md`. Do not run them wholesale. The next
highest-value test is a small second-noun Pixen induction replication; add Pro calls only
for a decision-changing signal, one matched block at a time and under a new paid-call
gate.
