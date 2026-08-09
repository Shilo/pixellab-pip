# PixelLab Negative Prompting Research Spike

Last reviewed: 2026-08-08.

Purpose: determine what the repository, current public PixelLab documentation, and the
local generation archive actually establish about negative prompting. This is a research
record and test plan, not a canonical runtime contract. Promote a conclusion into
`skills/pixellab-pip/SKILL.md` or a runtime reference only after route-specific controlled
tests support it.

## Executive Verdict

The completed evidence does **not** support either universal claim:

- "Negative prompting makes PixelLab outputs worse."
- "Negative prompting helps PixelLab, or is harmless when it does not help."

The defensible conclusion is narrower:

1. A separate `negative_description` field is route-specific. Current public REST v2
   exposes it on selected older/base workflows, labels the PixFlux field deprecated, and
   exposes no negative field on Pixen, Create Image Pro, modern v3 animation, Pro inpaint,
   or any current public MCP tool.
2. Inline exclusion wording such as `no text` is a different intervention from a separate
   negative field. The archive contains both apparent successes and apparent backfires.
3. The pre-study archive contains no controlled same-route, same-seed,
   same-positive-description comparison where only `negative_description` changes.
   Historical outputs cannot establish causality, but the later 106-call controlled study
   now supplies 52 such negative-field attempts.
4. The strongest current engineering default is positive structural wording plus real
   route controls. A short targeted exclusion can be a probabilistic guardrail, but it is
   not enforcement and should not be used to rescue a route-level failure.
5. The question must be answered per endpoint/model stack, surface, service build, and use
   case. Pooling PixFlux, BitForge, Pixen, Pro, inpaint, and animation into one “PixelLab
   negative prompting” verdict would hide materially different schemas, model priors,
   routing, and prompt-processing behavior.
6. The completed 106-call static study found zero helpful negative arms. In the retained
   32-pair confirmation, 25 had no observed effect, one was worse, two produced adverse
   signals, and four were ambiguous. BitForge's field is behaviorally active but did not
   prevent the named failure; PixFlux's deprecated field was semantically weak/no-op on
   the tested task. See `pixellab-negative-prompting-confirmation-results.md`.

This challenges both the developers' reported blanket warning and the opposite intuition
that negatives are helpful or necessarily harmless. The data support not adding negatives
by default because no benefit was measured—not because every negative made every image
worse. No controlled call used Pixen, Create Image Pro, character v3/new, modern v3
animation, or Pro/v3 inpaint.

## Terms Kept Separate

| Term | Meaning in this spike | Why it matters |
|---|---|---|
| Separate negative field | Text sent in the documented REST `negative_description` property. | It may be processed separately by the route, and many routes reject or omit it. |
| Inline negation | `no`, `not`, `without`, `avoid`, or similar wording inside `description` or `action`. | The words enter the main positive text channel and may behave differently from a dedicated negative field. |
| Positive structural constraint | A description of the allowed composition, palette, count, geometry, or occupancy without naming the unwanted concept. | It supplies a constructive target rather than only an exclusion. |
| Structured control | A real field such as `outline`, `detail`, `shading`, `view`, `no_background`, `color_image`, mask, or reference image. | It may target a failure mode more directly than prompt wording. |
| No-op | The negative intervention produces no meaningful change beyond normal same-request variation. | Pixel identity alone is insufficient unless same-request reproducibility is first measured. |
| Backfire | The forbidden feature becomes more frequent, more salient, or quality drops after the negative intervention. | A single changed-seed anecdote is suggestive, not proof. |

## Causal Scope And Hidden-Stack Confounding

“Negative prompting” is not one treatment independent of the system that receives it.
For the controlled study, the actual treatment is adding `negative_description` to a
specific public request while the rest of that endpoint's visible payload stays fixed.
The observed response is jointly determined by the wording and the deployed stack:

```text
negative wording × endpoint/model family × model priors × routing × prompt processing
× task × seed × service build
```

PixelLab does not publicly expose internal model identifiers for every call, field-weight
implementation, hidden routing decisions, or any server-side/system prompt layer that may
exist. Those components cannot be experimentally removed from black-box API testing.
Same-endpoint, same-seed pairs reduce visible request confounding and short randomized run
windows reduce time drift; neither identifies a model-independent “pure” negative-prompt
effect.

The defensible unit of inference is therefore the **tested endpoint/model stack on the
tested build and tasks**. A weak or adverse result can reflect how that stack weights the
field, a strong subject prior, a prompt parser, or their interaction. It must not be
rewritten as “negative language is intrinsically bad.” The same caution works in the other
direction: an attractive output cannot prove the negative caused it, and unobserved hidden
routing cannot be invoked to claim a benefit the output did not show.

## Sources And Method

The review used four evidence layers:

1. The full tracked repository and its Git history, including runtime rules, references,
   research notes, plans, tests, fixtures, blueprints, and showcase claims.
2. Current official PixelLab sources: the
   [REST v2 endpoint index](https://api.pixellab.ai/v2/llms.txt),
   [OpenAPI schema](https://api.pixellab.ai/v2/openapi.json),
   [REST reference](https://api.pixellab.ai/v2/redoc),
   [hosted MCP documentation](https://api.pixellab.ai/mcp/docs), human documentation,
   and the official SDK/MCP repositories linked by `llms.txt`.
3. An exhaustive structural and text inventory of `pixellab-pip-generations/`, followed
   by review of every logical output whose canonical blueprint contains
   `negative_description`.
4. Focused visual review of the useful near-pairs and failed outputs. Existing manifest
   judgments were treated as claims to verify, not ground truth by themselves.

The generation archive contained 23,691 files in 1,901 directories: 20,795 PNGs, 247
GIFs, 2,315 JSON files, 8 JSONL files, and 77 Markdown files. Fifteen structured records
were malformed or truncated; raw-text search supplemented the structural scan so those
records were not silently omitted. None of the malformed records contains a usable
separate-negative experiment.

## Current Official Contract

Current OpenAPI contains exactly four request schemas with `negative_description`, used
by five REST operations:

| REST operation | Field status | Public description |
|---|---|---|
| `POST /create-image-bitforge` | Optional string, default empty | Text describing what to avoid. |
| `POST /create-image-pixflux` | Optional string, default empty; description says deprecated | No current behavioral recommendation. |
| `POST /create-image-pixflux-background` | Same PixFlux request schema | Same deprecated field. |
| `POST /animate-with-text` | Optional string or null, default empty | Negative prompt guiding what not to generate. |
| `POST /inpaint` | Optional string, default empty | Text describing what to avoid. |

No one of these fields declares a public `minLength` or `maxLength`. That is absence of a
documented limit, not evidence of unlimited input.

The authoritative MCP documentation has no negative-prompt parameter. In particular:

- `create_image_pixflux` does not expose REST PixFlux's deprecated field.
- `create_image_pixen` and `create_image_pro` expose no negative field, matching their
  REST counterparts.
- MCP has no BitForge image-generation tool.
- MCP `animate_image` corresponds to modern frame-anchored v3 animation, not legacy
  `animate-with-text`; neither it nor REST `animate-with-text-v3` exposes the field.
- MCP `inpaint_image` corresponds to Pro/v3 inpaint, not base `inpaint`; neither it nor
  REST `inpaint-v3` exposes the field.

PixelLab's human [guidance options](https://www.pixellab.ai/docs/options/guidance) and
[character options](https://www.pixellab.ai/docs/options/character) pages say a negative
description can sometimes help steer away from content. This is the only explicit current
official recommendation found. It neither promises improvement nor says that negatives
are harmful. Several editor/tool pages still display a Negative description option,
including PixFlux, but editor UI presence does not override PixFlux's current public REST
deprecation marker or establish MCP parity.

Official SDKs retain the older four-workflow shape: BitForge, PixFlux, base animation,
and base inpaint. A JavaScript README example uses a PixFlux negative, but that example is
configured for v1 and is legacy evidence rather than a current v2 best practice.

No official current source was found that:

- recommends automatically populating negatives;
- recommends a standard negative list, weighting syntax, or comma format;
- says PixFlux's deprecated field is ignored;
- exposes the field on Pixen, Pro, v3 animation, Pro inpaint, or MCP; or
- shows a controlled efficacy test.

## Repository Findings

### Runtime contradiction

`SKILL.md` currently treats `negative_description` as a generic natural-language field and
unconditionally says to move render-like adjectives into it for flat pixel art. That rule
was added before later route-specific work documented that Pro, MCP, Pixen, and v3
animation do not expose the field, and that PixFlux's REST field is now described as
deprecated.

The route-specific references are more accurate than the global sentence:

- `references/create-image-pro.md` correctly says Pro has no negative field or structured
  detail/outline/shading controls.
- `references/official-pixellab-documentation.md` records negative prompting as a
  REST-only route-specific extra, not an MCP capability.
- `references/animation.md` correctly treats v3 exclusions as `action` wording and records
  that negative prompting did not solve idle-derived walk failures.
- `references/icon.md`, `references/create-image-pro.md`, `references/style-reference.md`,
  and `references/cinematic.md` use narrow inline exclusions on routes without a separate
  field.

The unconditional global instruction is therefore a schema/routing defect independent of
the unresolved quality question. A future runtime fix should never invent an unsupported
field.

### Historical evidence is mostly negative or mixed

The tracked research supplies several route-specific warnings:

- Idle animation append-negatives did not reliably prevent detached puffs, smoke, trails,
  or white pixels; some named concepts still appeared.
- Aura tests found same-seed inline `no central object or emblem` wording did not override
  the composition prior and may have kept those concepts salient. The study correctly
  stops short of claiming causation.
- One-bit tileset tests found stronger texture/color exclusions failed to remove texture;
  `no blue`/`no purple` also damaged the useful white cap in that run.
- Twenty-four top-down-house Pixen outputs failed the projection target across positive,
  anti-isometric, and no-negative prompts. Negation did not rescue the route-level prior.
- In tiny BitForge sprite tests, an anti-shading negative was present in outputs ranked
  below Pixen probes. A closed positive palette performed better than a long `no shading,
  no shadows, no highlights, no gradients, no dithering` description. That comparison is
  directional because request capture and route/configuration confounds prevent a clean
  ablation.
- Portrait framing improved with concise composition and scale anchors. A promoted prompt
  still uses three short inline exclusions and passed a cross-subject sample, which argues
  for positive-first and concise—not for never using negation.
- Cinematic v3 has one case where targeted inline exclusions removed an unwanted glow/orb
  on retry, and another where `no sparkles` failed. Both still require visual validation.

Successful icon and showcase prompts often contain inline text/border exclusions. Their
outputs prove those prompts can succeed; bundled positive structure and route changes mean
they do not prove the exclusions caused success. Human-facing prose should say the clauses
"were present in the successful prompt" unless an ablation isolates their effect.

No automated test currently checks route support for `negative_description`. Blueprint QA
validates shape and paths, not the live endpoint schema, so an unsupported field can pass
local QA.

## Generation Archive Findings

### Inventory

The archive contains 59 JSON-key occurrences across 33 files. Four are schema definitions
inside an archived OpenAPI snapshot, leaving 55 flow-data occurrences across 32 files and
19 generation directories.

Forty-four occurrences are canonical REST blueprint call bodies. Duplicate manifests and
request metadata account for the other 11. The canonical records represent 42 unique
logical request/output groups because two ES sweep pairs are byte-identical copies.

| Route | Blueprint calls | With `negative_description` | Without it |
|---|---:|---:|---:|
| `create-image-pixflux` | 60 | 33 | 27 |
| `create-image-pixflux-background` | 9 | 7 | 2 |
| `create-image-bitforge` | 7 | 4 | 3 |
| `animate-with-text-v3` | 170 | 0 | 170 |
| Route subtotal | 246 | 44 | 202 |

Across every generation/action call in archived blueprints, 919 call steps were found: 44
with a separate field and 875 without one. Of the 875 without the field, 231 contain
heuristically detected inline negation. These counts measure usage, not efficacy.

### Visual outcomes for all 42 unique field-bearing groups

- 37 show no obvious forbidden feature in the reviewed output.
- 2 fail the requested goal: both BitForge lake-dragon images lack a clear dragon despite
  negatives that name `missing dragon`, `tiny or hidden dragon`, or an unclear reflection.
- 3 are internally conflicted and cannot be scored cleanly: a robot prompt forbids faces
  and hands while positively requesting eye panels and arms, and two day-cycle prompts
  broadly forbid animals while positively requesting fireflies.

This is **not** a 37/42 success rate for negative prompting. The positive descriptions,
seeds, route controls, model priors, and negatives all changed together, and no matched
control establishes what would have happened without the field.

### There is no controlled pair

The exhaustive scan found:

- no same-route, same-seed, exact-same-positive-description group mixing field-present and
  field-absent calls; and
- no credible same-route/same-seed near-description pair where the negative intervention
  is isolated.

This is the central limitation of the historical corpus.

### Useful near-pairs

#### Rain opening frame: apparent benefit, heavily confounded

`rain-loop-20260712/00-opening-frame.png` used seed 71207 without a recorded negative and
looks like a central waterfall. The accepted `00-opening-frame-v2.png` used seed 42 with a
negative forbidding waterfalls, rivers, a central stream, and a splash pool, and shows
distributed rain.

The first positive prompt was not retained and the seed changed. The result is compatible
with a benefit, but it cannot attribute the improvement to `negative_description`.

#### Lake dragon: field did not enforce the exclusion

The initial and retry BitForge prompts positively demand a large unmistakable dragon and
negatively mention missing/hidden dragons. Both outputs fail to depict a clear dragon.
Same-prompt/same-seed PixFlux comparisons show a small dragon on retry, but endpoint,
canvas size, and controls differ. This proves the BitForge negative was not enforcement;
it does not prove that the negative caused the missing dragon.

#### Rain pond animation: strongest apparent backfire, but inline and changed-seed

Three `animate-with-text-v3` takes used the same opening image:

- Take 1, resolved seed 3964806125, had a glow-orb bloom.
- Take 2, resolved seed 2819547682, added inline `no sun, no moon, no glowing orb` wording
  and produced a large glowing sun disc.
- Take 3, resolved seed 2564500923, omitted both the effect nouns and their negation and
  was accepted without the bloom.

The visual contrast is strong evidence that inline negative wording **can** backfire. It
does not test a separate field, and changed seeds plus changed action wording prevent a
causal estimate.

### Unsupported-field evidence

Archived Pixen attempts provide hard transport evidence:

- A slime attempt with `negative_description` was rejected as `extra_forbidden`; dropping
  the field allowed the retry.
- Clay-flower-pot records make the same schema observation.
- Pro and v3 animation records correctly keep exclusions inline because their schemas
  expose no separate field.

This is conclusive about request validity, not visual quality.

## Current Recommendation

1. Inspect the selected live schema. Never create `negative_description` on a route that
   does not expose it.
2. Omit PixFlux's deprecated negative field by default. Use it only for an exact user value
   or an explicitly approved controlled experiment.
3. Prefer positive structural wording and dedicated controls. Examples: `exactly one whole
   apple centered in empty space`, a closed named palette, `outline`, `detail`, `view`,
   `no_background`, masks, and references.
4. When a supported negative field is justified, keep it short and tied to one material,
   visually testable failure mode.
5. On no-field routes, use only essential inline exclusions. Avoid long catalogs of every
   imaginable defect and do not repeat the same unwanted noun in positive and negative
   forms.
6. Treat exclusions as probabilistic. Verify the output and change route/control when the
   failure reflects a strong model prior, geometry problem, or missing input anchor.

These are now controlled-evidence-backed engineering defaults for the tested static
routes. They are not a claim that all negatives are harmful or that results transfer to
other routes.

## Live Phase 0 Calibration

The frozen 30-call calibration was executed on 2026-08-08. Full results and limitations
are recorded in `pixellab-negative-prompting-calibration-results.md`.

The calibration adds three controlled findings to the historical review:

1. BitForge's dedicated field is behaviorally active. Its negative arms changed same-seed
   outputs substantially more than exact baseline repeats, especially in the sign family.
2. PixFlux's deprecated field produced the same semantic target outcomes as baseline in
   all three families, and its pixel differences were comparable to repeat variation. This
   is evidence of no-op or weak behavior for the tested seed, not proof of equivalence.
3. The only baseline failure that could test efficacy was PixFlux's crossed-sword prompt.
   Concise and long negatives did not fix it; the constructive positive rewrite did.

No negative arm produced a material overall-quality loss under the pre-registered band.
BitForge's two text-negative images contained ambiguous glyph-like emblems while the
baseline did not, but blind adjudication found no clearly readable text. This is a
replication target, not a proven backfire.

The text and style baselines never clearly failed on either endpoint, so they are not
informative enough for confirmation. Per the frozen stopping rule, replace or harden those
families and recalibrate them before purchasing the larger seed matrix.

Phase 0B performed that replacement calibration. Its complete results are in
`pixellab-negative-prompting-phase0b-results.md`. The unwanted-subject and projection
baselines remained non-informative, but BitForge's stronger signpost prompt produced clear
pseudo-writing in baseline, concise-negative, long-negative, positive, and repeat arms.
The field again changed BitForge pixels well beyond repeat variation without improving the
named failure. The revised confirmation therefore uses only two endpoint-specific
informative pairs: PixFlux crossed-sword count and BitForge signpost text.

## Live Phase 1 Confirmation

The frozen 46-call confirmation was executed on 2026-08-08. Combined with the two
calibrations, the complete static study contains 106 successful calls, 106 validated PNGs,
zero errors, and zero retries. Full results are in
`pixellab-negative-prompting-confirmation-results.md`; private per-attempt audit artifacts
remain under gitignored local storage rather than tracked documentation.

Across the retained eight-seed endpoint-family pairs:

- PixFlux count: baseline, concise negative, and long negative had identical same-seed
  sword-count outcomes in every block. Sixteen of sixteen negative comparisons had no
  observed effect.
- BitForge signpost text: no baseline or negative arm produced clear absence of
  pseudo-writing. Of 16 negative comparisons, nine had no observed effect, one was worse
  on quality, two changed an ambiguous baseline into clear failure, and four remained
  ambiguous.
- Combined: zero helpful, 25 no observed effect, one worse, two adverse signals, and four
  inconclusive among 32 confirmation comparisons.

Eight seeds cannot prove formal endpoint-wide equivalence, and only one retained prompt
family was tested per endpoint. The result is nevertheless sufficient to reject automatic
negative insertion as a useful default for these routes: the study measured no benefit,
and BitForge supplied limited adverse counterexamples to the claim that negatives are
always harmless.

## Controlled Test Plan

The finite goal is not to prove a universal law across all possible prompts. It is to reach
route-specific conclusions with pre-registered prompts, seeds, scoring, and decision
thresholds, then state exactly where the conclusion generalizes.

### Design principles

- Change one intervention at a time.
- Seed-lock every comparison block, but include several independent seeds.
- First measure exact-request reproducibility; same-seed pixel equality is not assumed.
- Preserve every request and response before scoring.
- Randomize candidate order and blind reviewers to endpoint and condition.
- Score forbidden-feature absence and overall quality separately.
- Do not tune prompts after seeing outcomes. A new wording starts a new registered study.
- Analyze each endpoint separately before any pooled summary.

### Standard comparison arms

| Arm | Positive description | Separate field or inline wording | Question answered |
|---|---|---|---|
| `B0` baseline | Fixed base description | Empty/omitted negative | Normal failure rate. |
| `N1` concise negative | Identical to `B0` | One short targeted exclusion | Does a focused negative help or harm? |
| `N2` long negative | Identical to `B0` | Target plus a broad defect catalog | Does length dilute quality or prime concepts? |
| `P1` positive structure | Constructive rewrite describing the allowed result | No negative | Is a positive constraint better than negation? |
| `I1` induction probe | Identical neutral description | Salient unrelated forbidden noun | Can naming a concept make it appear? |
| `R0` exact repeat | Byte-identical to `B0` | Same as `B0` | How variable is an identical same-seed call? |

`P1` is a strategy comparison, not a causal ablation, because its positive text changes.
The causal field estimate is `N1` versus `B0`; `R0` determines whether pixel-difference
metrics are meaningful.

### Prompt families

Use at least these visually scoreable families:

1. **Count/duplication:** exactly one whole red apple; target extra or duplicate apples.
2. **Unwanted subject:** an unoccupied moonlit forest clearing; target a salient animal.
3. **Text contamination:** a pictorial shop sign or icon; target letters, words, numbers,
   and watermark-like marks; use OCR plus independent visual review.
4. **Style conflict:** flat limited-palette pixel art; target glossy/3D/photo styling; score
   edge hardness, palette/ramp behavior, and blinded style judgment.
5. **Background isolation:** one potion sprite; compare prompt exclusions against the real
   `no_background` control and alpha measurements.
6. **Composition/view:** a simple side-view subject; test whether negatives can counter a
   route prior versus a direct `view` control.

Exact prompts must be frozen in a request matrix before the first paid call. Avoid famous
characters, living artists, copyrighted style imitation, ambiguous categories, or pairs
where the positive and negative instructions literally conflict.

### Completed static dedicated-field study

The exact prompts, request bodies, random seeds, shuffled dispatch order, scoring rubric,
decision bands, and cost boundaries are frozen in
`../plans/pixellab-negative-prompting-controlled-test-plan.md`. That plan is the canonical
execution protocol; this spike retains the research rationale.

The executed design used a 30-call initial calibration, a 30-call replacement-family
calibration, and a 46-call endpoint-specific confirmation. Calibration stopped carrying
families whose baselines did not exhibit a scoreable failure. Confirmation then expanded
the retained PixFlux count and BitForge text pairs to eight total seeds with additional
repeat controls. The complete 106-call record is published rather than dropping the
uninformative or ugly outputs.

If formal practical equivalence becomes a requirement, the frozen confirmation may be
extended in pre-registered batches to 16 and at most 32 seeds. The eight-seed result does
not meet the ±10-point equivalence band. Any extension needs a new approval gate and must
report `inconclusive` if the maximum sample remains insufficient.

### Remaining study: inline negation on no-field image routes

Test Pixen separately with `B0`, an inline concise exclusion, an inline long exclusion,
and `P1`. Use the route's actual structured controls identically in every arm. This tests
main-channel concept priming, not `negative_description`.

Create Image Pro is a separate high-cost phase. Its native small-size batches can provide
many candidates per call, but a call is Pro-priced and candidates from one call are not
independent seeds. Use a small pre-registered number of calls only after the Pixen/static
studies justify the question.

### Remaining study: animation and inpaint

Do not generalize static-image results to animation or editing.

- For modern `animate-with-text-v3`, compare baseline `action`, concise inline exclusion,
  long inline exclusion, and positive internal-motion wording on the same anchors and
  seed blocks. Score every frame for forbidden artifacts, identity drift, and motion
  quality.
- Test legacy `animate-with-text` separately if its negative field remains relevant to
  supported routing.
- For base `inpaint`, reuse the exact same source and mask across arms. Score only pixels
  in and near the mask as well as whole-image collateral change.

### Scoring and analysis

Primary binary outcome: whether the named forbidden feature is visibly present.

Secondary outcomes:

- instruction compliance;
- subject identity and composition;
- overall visual quality on a fixed ordinal scale;
- text/OCR contamination;
- duplicate/object count;
- alpha/background integrity;
- palette, edge, or gradient metrics where they actually correspond to the task; and
- animation artifact count and frame coverage.

Use two independent blinded reviewers and adjudicate disagreements. Automated metrics are aids,
not substitutes for visual scoring. Analyze paired binary outcomes with a paired method
such as McNemar's test and report effect size with confidence intervals. Analyze ordinal
quality as paired data and report the distribution, not only an average.

Pre-register practical decision bands per endpoint:

- **Benefit:** materially fewer forbidden-feature failures with no material quality loss.
- **Harm:** more forbidden features, a material quality loss, or both.
- **No meaningful effect:** the confidence interval stays inside the predefined smallest
  effect of interest and quality is unchanged.
- **Inconclusive:** too much rerun variance, reviewer disagreement, or too few failures in
  the baseline.

Do not label a result no-op merely because one pair looks similar, and do not label it
harmful because one changed-seed output contains the named noun.

### Artifacts and reproducibility

Store a live study under a named generation folder, for example:

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
  automated-metrics.json
  analysis.json
  manifest.json
  negative-prompt-study.blueprint.json
```

Preserve literal requests, resolved seeds, usage, failures, and all candidates. The blinded
index must be generated before review and decoded only after scores are locked. Record
exact output hashes but do not treat hash differences as semantic differences.

## Cost And Execution Gate

The approved static study is complete: 106 live calls reported 106 generations, with no
errors or retries. That approval does not carry into a seed extension, induction probe,
Pixen, animation, inpaint, or Pro study. Each later phase can cost substantially more and
requires a new gate.

Before execution, apply Pip's cost-approval gate with:

- every exact prompt and negative value;
- endpoint, size, controls, and seed matrix;
- predicted calls and generations per phase;
- a balance snapshot when available; and
- an explicit stopping rule.

Approve and run phases sequentially. Do not silently roll a pilot approval into an
open-ended confirmatory or Pro batch.

## Promotion Criteria

Update the runtime contract only when a completed route-specific study provides:

1. preserved requests and outputs;
2. multiple independent seed blocks;
3. reproducibility controls;
4. blinded scores;
5. a practical effect estimate with uncertainty;
6. a clear statement of endpoint, schema version/date, prompt families, and limits; and
7. a result that changes an agent decision, action, safety boundary, or verification step.

Until then, keep this evidence in `docs/` and correct only the definite schema/routing
contradiction: never invent `negative_description` on a route that does not expose it.
