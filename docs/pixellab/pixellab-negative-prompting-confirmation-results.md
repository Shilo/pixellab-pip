# PixelLab Negative Prompting Phase 1 Confirmation Results

Executed: 2026-08-08.

Status: complete; 46-call confirmation and 106-call static study fully preserved.

Companions:

- Research spike: `pixellab-negative-prompting-research-spike.md`
- Controlled plan: `../plans/pixellab-negative-prompting-controlled-test-plan.md`
- Phase 0 results: `pixellab-negative-prompting-calibration-results.md`
- Phase 0B results: `pixellab-negative-prompting-phase0b-results.md`

## Verdict

The completed confirmation found **no case where a dedicated negative field helped the
named target**. Across 32 same-endpoint, same-positive-description, same-seed paired
negative arms:

| Paired classification | Count | Share |
|---|---:|---:|
| Helpful | 0 | 0.0% |
| No observed effect | 25 | 78.1% |
| Worse | 1 | 3.1% |
| Adverse signal | 2 | 6.3% |
| Inconclusive because of ambiguity | 4 | 12.5% |

This result supports the operational default **do not automatically add negative
prompting**. Prefer positive structural wording and real route controls, and use a concise
negative only on a route that exposes the field when there is a specific, testable reason.

The study does **not** support the stronger claim that every negative prompt makes every
image worse. Most tested pairs had no observed semantic effect, and only one crossed the
pre-registered material-quality harm threshold. The precise conclusion is: no confirmed
benefit, frequent no observed effect, and a small number of adverse observations in the
tested static endpoint-family stacks.

## Attribution Boundary: The Treatment Is Route-Conditional

This experiment does not isolate an abstract, model-independent property called
“negative prompting.” It estimates the effect of adding PixelLab's public
`negative_description` field **through a particular deployed endpoint stack**. The
observable treatment includes its interaction with:

- the endpoint's selected model or model family;
- model priors for the subject and composition;
- PixelLab routing and version selection;
- prompt parsing, tokenization, field weighting, and any server-side prompt transformation;
- any undisclosed system instruction, safety conditioning, or quality wrapper, if present;
- the public request controls, seed behavior, and output/post-processing path; and
- the service build active on the execution date.

The public API does not expose those internal components, so the study cannot separate
“the negative field itself” from how PixFlux or BitForge consumed it. Same-endpoint,
same-seed pairing controls the visible request and keeps the deployed stack approximately
fixed within a block; it does not remove hidden routing or establish that another model
would interpret the field the same way.

Accordingly, every result should be read as an interaction:

```text
observed effect = negative wording × endpoint/model stack × task × seed × service build
```

“No observed benefit on this stack” is valid. “Negative prompting is intrinsically
unhelpful” is not established. Conversely, hidden routing is a plausible moderator, not a
post-hoc explanation that turns zero observed wins into evidence of benefit.

## Tested And Untested Model/Route Families

| Public workflow | Separate negative channel in current public schema | Controlled here? | What can be concluded |
|---|---|---|---|
| REST v2 `create-image-bitforge` | Yes | Yes | Dedicated-field result for the deployed BitForge stack and tested tasks. |
| REST v2 `create-image-pixflux` | Yes, documented as deprecated | Yes | Dedicated-field result for the deployed PixFlux stack and tested tasks. |
| Pixen: REST `create-image-pixen` / MCP `create_image_pixen` | No | No | Requires a separate inline-negation study; this result does not transfer. |
| Create Image Pro: REST `generate-image-v2` / MCP `create_image_pro` | No | No | Requires a separate inline-negation study, analyzed at the call level because one Pro call may return multiple correlated candidates. |
| Character `v3`/`new` and Character Pro | No separate negative field | No | Workflow-specific inline wording only; not covered by static BitForge/PixFlux results. |
| Modern animation `animate-with-text-v3` / MCP `animate_image` | No | No | Requires a temporal inline-action study with fixed frame anchors. |
| Pro/v3 inpaint `inpaint-v3` / MCP `inpaint_image` | No | No | Requires fixed source/mask inline-description testing. |
| Base inpaint and legacy `animate-with-text` | Yes | No | Dedicated-field behavior remains untested on these older/base workflows. |

`v2`, `v3`, `new`, and `Pro` are workflow or tier labels, not one global model lineage.
In particular, REST `generate-image-v2` is the current Create Image Pro route despite
“v2” appearing in its endpoint name; it exposes no `negative_description` field.

## What Ran

Phase 1 used the two endpoint-family pairs retained by blinded calibration:

- PixFlux `CNT`: exactly two crossed swords, with extra swords/blades as the target
  failure.
- BitForge `TXT2`: a fantasy directional signpost, with pseudo-writing as the target
  failure.

For each retained pair, the combined dataset contains eight independent registered seeds
and three causal arms:

- `B0`: positive description with `negative_description` omitted;
- `N1`: same request plus the concise negative; and
- `N2`: same request plus the long negative.

Phase 1 generated seven new seed blocks per pair because one PixFlux seed already existed
from Phase 0 and one BitForge seed already existed from Phase 0B. It also generated two
exact baseline repeats per endpoint. All requests used 64×64 output,
`text_guidance_scale: 8`, `no_background: true`, and the frozen shuffled order.

| Operation | Calls | Reported generations | Errors | Retries |
|---|---:|---:|---:|---:|
| Phase 0 calibration | 30 | 30 | 0 | 0 |
| Phase 0B replacement calibration | 30 | 30 | 0 | 0 |
| Phase 1 confirmation | 46 | 46 | 0 | 0 |
| **Complete static study** | **106** | **106** | **0** | **0** |

## Review Independence

Two reviewers independently scored 46 opaque Phase 1 candidate IDs. They did not receive
the endpoint, family, arm, prompt, seed, request ID, or filename mapping. Target failure
and general visual quality were separate scores.

- Primary binary agreement before adjudication: 38/46 (82.6%).
- Reviewers agreed on all 23 PixFlux count candidates.
- All eight disagreements were BitForge text-severity judgments.
- A third blind reviewer adjudicated only those eight candidates.

Archived developer opinions and earlier manifest prose were not used as labels. The final
result is the adjudicated visual record, not a vote about what PixelLab is expected to do.

## PixFlux Count Result

The base prompt was `Crossed silver swords emblem centered in empty space.` The concise
field named extra/third/duplicate swords; the long field added more blade, object, text,
crop, blur, gradient, photorealism, and 3D-render exclusions.

| Arm | Clear target failures | Passes | Mean quality | Median paired quality change |
|---|---:|---:|---:|---:|
| `B0` baseline | 1/8 | 7/8 | 3.8125 | — |
| `N1` concise | 1/8 | 7/8 | 3.8125 | 0.0 |
| `N2` long | 1/8 | 7/8 | 3.8750 | 0.0 |

Every negative arm matched its same-seed baseline target outcome: 16 of 16 were classified
as no observed effect. The original Phase 0 seed omitted swords under `B0`, `N1`, and `N2`;
all seven new seeds rendered exactly two swords under all three arms. The initial failure
was therefore seed-specific, not a stable failure that the negative could rescue.

The exact repeats also show why pixel inequality is not semantic evidence. PixFlux
baseline repeats were not byte-identical, with normalized RGBA mean absolute differences
of 0.01565 and 0.01037, but their sword-count judgments stayed unchanged.

There were zero target discordances in eight paired seeds for either negative wording, so
McNemar's test has no discordant pairs to test. This is a direct observation of no target
change, not proof of equivalence: with only eight seeds, the two-sided exact 95% upper
bound for an unobserved per-seed discordance rate is about 36.9%.

The full adjudicated quality distribution and paired changes were:

| Arm | Quality-score distribution | Paired quality-change distribution | Mean change and paired-bootstrap 95% interval |
|---|---|---|---|
| `B0` | 2.5×1, 3.5×1, 4.0×5, 4.5×1 | — | — |
| `N1` | 2.5×1, 3.5×1, 4.0×5, 4.5×1 | -0.5×1, 0×6, +0.5×1 | 0.0000 [-0.1875, +0.1875] |
| `N2` | 2.5×1, 3.5×1, 4.0×4, 4.5×2 | -0.5×1, 0×5, +0.5×2 | +0.0625 [-0.1250, +0.2500] |

The bootstrap intervals use one million paired resamples with fixed analysis seed
`20260810`. They summarize this empirical seed block; the exact discordance bound is the
more conservative statement about unseen target changes.

## BitForge Text Result

The base prompt was `Wooden fantasy directional signpost with three arrow-shaped boards
at a crossroads.` The concise field was `text, letters, words, numbers`; the long field
also named writing, labels, signatures, watermarks, typography, runes, glyphs, and slogans.

| Arm | Clear pseudo-writing | Ambiguous marks | Clear absence | Mean quality | Median paired quality change |
|---|---:|---:|---:|---:|---:|
| `B0` baseline | 5/8 | 3/8 | 0/8 | 3.9375 | — |
| `N1` concise | 6/8 | 2/8 | 0/8 | 3.8125 | 0.0 |
| `N2` long | 6/8 | 2/8 | 0/8 | 3.9375 | 0.0 |

No negative arm produced clear absence of pseudo-writing:

- nine pairs had the same clear target failure and stable quality;
- one concise-negative pair had the same failure but a one-point mean-quality loss and
  was classified worse;
- at seed block 5, both negative arms changed an ambiguous baseline into clear
  pseudo-writing, producing two adverse signals; and
- four seed/arm pairs remained ambiguous and therefore inconclusive.

Among seed pairs with non-ambiguous target scores on both sides, there were no beneficial
discordances. The ambiguity rate prevents a meaningful binary McNemar estimate over all
eight seeds. Treating ambiguous scores as either passes or failures would manufacture a
result in the favored direction, so the analysis leaves them missing as registered.

Five seeds per arm had non-ambiguous target scores on both sides; all five were
failure/failure pairs. The observed clear-pair failure-rate difference was 0 percentage
points, with no McNemar discordances. The two-sided exact 95% upper bound for an unobserved
discordance rate at `n=5` is about 52.2%. Across all eight seeds, allowing each ambiguous
score to be either pass or failure gives a partial-identification range of -25 to +37.5
percentage points for negative-minus-baseline failure rate. The target effect is therefore
formally inconclusive, not equivalent.

The full adjudicated quality distribution and paired changes were:

| Arm | Quality-score distribution | Paired quality-change distribution | Mean change and paired-bootstrap 95% interval |
|---|---|---|---|
| `B0` | 3.5×1, 4.0×7 | — | — |
| `N1` | 3.0×1, 3.5×1, 4.0×6 | -1.0×1, 0×7 | -0.1250 [-0.3750, 0.0000] |
| `N2` | 3.5×1, 4.0×7 | 0×8 | 0.0000 [0.0000, 0.0000] |

These are one-million-resample paired-bootstrap intervals with fixed seed `20260810`.
The degenerate `N2` interval means all eight observed quality differences were zero; it is
not evidence that unseen seeds must also have zero difference.

BitForge's two Phase 1 exact repeats were byte-identical to their baselines. Combined with
both calibrations, negative arms changed BitForge pixels far beyond repeat variation while
usually leaving the target outcome unchanged. The field is behaviorally active; that is
not the same as being useful.

## All 106 Static Attempts

The full dataset contains 52 calls with `negative_description`, 26 baseline controls, 12
positive structural rewrites, and 16 exact repeats. Applying the same conservative paired
rules to every negative call gives:

| Classification | All 52 negative-field attempts |
|---|---:|
| Helpful | 0 |
| No observed effect | 39 |
| Worse | 1 |
| Adverse signal | 2 |
| Inconclusive | 10 |

The 20 negative calls outside the retained confirmation pairs came from calibration
families whose baselines often passed or were ambiguous. They are included for completeness
but do not have the causal weight of the 32 retained confirmation comparisons.

Positive structural rewriting is also not universally successful. It fixed the initial
PixFlux crossed-sword failure, but did not eliminate BitForge signpost pseudo-writing and
had mixed quality effects in other calibration families. The practical lesson is to prefer
constructive structure as the default, then verify the actual output—not to treat any text
strategy as enforcement.

## What The Evidence Establishes

1. **No measured benefit on the tested stacks:** no dedicated negative arm removed a
   clear target failure without material quality loss in 32 retained confirmation pairs
   or 52 total negative attempts.
2. **PixFlux was semantically weak/no-op here:** concise and long negatives reproduced
   the same sword-count outcome as baseline at all eight seeds. Its public field is also
   documented as deprecated.
3. **BitForge processed the field but did not obey it reliably:** field-bearing requests
   changed pixels, yet never produced a sign with clear absence of pseudo-writing.
4. **Harm was possible but not universal:** one material quality loss and two adverse
   target signals occurred; most pairs were stable.
5. **Naming a forbidden concept did not reliably make it appear:** there is no support for
   the simplistic claim that the model always draws whatever appears in the negative
   description. The BitForge seed-5 results are an induction signal worth a dedicated
   neutral-noun probe, not proof of that mechanism.
6. **Endpoint support remains a hard boundary:** these results do not authorize inventing
   `negative_description` on Pixen, Pro, MCP, v3 animation, or Pro inpaint.

## Limits And Generalization

- Model choice, hidden routing, server-side prompt handling, and any undisclosed system
  conditioning are inseparable parts of the tested treatment. The results estimate the
  deployed route's behavior, not a route-free property of negative prompting.
- The confirmation has eight seeds but only one retained prompt family per endpoint. It
  can reject a large benefit for these tasks more confidently than it can establish a
  universal endpoint rule.
- Eight seeds cannot satisfy the pre-registered ±10-point practical-equivalence band.
  “No observed effect” is therefore an attempt-level label, not a formal endpoint-wide
  equivalence claim.
- The concise and long wordings cover two common negative styles, not every possible
  syntax, ordering, language, or weighting convention.
- PixFlux is deprecated, and service behavior can change. The results describe the tested
  public build on the execution date.
- Tiny 64×64 outputs make glyph-versus-texture judgments intrinsically difficult. The
  explicit ambiguous category and third adjudicator reduce, but cannot eliminate, that
  limitation.
- Static text-to-image findings do not transfer automatically to base inpaint, legacy
  animation, modern v3 inline action wording, Pixen inline exclusions, or Pro.
- No controlled call used Pixen, Create Image Pro, character v3/new, Character Pro,
  modern v3 animation, or Pro/v3 inpaint. Historical archive examples on some of those
  routes are uncontrolled and cannot fill that gap.

## Decision And Next Test

The current runtime recommendation is settled enough for normal routing:

- do not auto-populate negative prompts;
- use only a supported route field;
- prefer positive structure and structured controls;
- if a concise negative is deliberately used, treat it as probabilistic and inspect the
  result; and
- do not add generic quality-ban lists.

Further paid testing should answer a new, narrower question rather than repeat this same
eight-seed matrix. The highest-value next phase is a dedicated **induction probe** on
BitForge: compare a neutral baseline with unrelated, visually salient forbidden nouns at
registered seeds to test whether merely naming a noun raises its appearance rate. A
16-seed extension of the frozen confirmation is justified only if a formal endpoint-level
equivalence interval is required; it needs a new paid-call approval gate.

## Artifact Record

The Phase 1 run is preserved under the gitignored generation archive at
`pixellab-pip-generations/negative-prompt-study-phase1-20260808/`. It contains literal
requests, decoded PNGs, sanitized response records, run events, hashes, blind indexes,
both reviewer files, third-reviewer adjudication, final adjudication, automated metrics,
comparison sheets, manifest, and analysis.

The private local HTML audit embeds all 106 exact PNG byte streams and every persisted
request/response/score record. It remains in gitignored local storage and is not a
repository deliverable.
