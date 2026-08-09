# PixelLab Negative Prompting Calibration Results

Executed: 2026-08-08.

Status: Phase 0 complete; confirmation not yet authorized.

Companions:

- Research and historical evidence: `pixellab-negative-prompting-research-spike.md`
- Frozen protocol: `../plans/pixellab-negative-prompting-controlled-test-plan.md`

## Result In One Sentence

The one-seed calibration shows that BitForge's dedicated negative field is behaviorally
active, while PixFlux's deprecated field produced no visible target change beyond ordinary
repeat variation; neither endpoint yet shows controlled evidence that negatives are
generally beneficial or materially harmful.

## What Ran

- REST `POST /v2/create-image-pixflux`
- REST `POST /v2/create-image-bitforge`
- Three prompt families: crossed-sword count, sign text contamination, and flat-render
  style
- Four comparison arms: baseline (`B0`), concise negative (`N1`), long negative (`N2`),
  and positive structural rewrite (`P1`)
- One exact baseline repeat (`R0`) per endpoint/family
- One fixed seed: `1178348305`
- Fixed 64×64 canvas, `text_guidance_scale: 8`, and `no_background: true`
- Thirty calls in a frozen shuffled order

All request bodies were persisted before submission. Every returned image was decoded,
PNG-signature checked, dimension checked, hashed, and saved before the call was marked
complete. The complete private run record is in
`pixellab-pip-generations/negative-prompt-study-20260808/`.

## Operational Outcome

| Measure | Result |
|---|---:|
| Approved calls | 30 |
| Completed images | 30 |
| Charged generations reported by PixelLab | 30 |
| Rejected payloads | 0 |
| Retries | 0 |
| Unknown or quarantined submissions | 0 |
| Output size failures | 0 |

This confirms that both documented REST fields were accepted on the tested build. It does
not by itself establish visual efficacy.

## Review Method

Two independent reviewers scored opaque candidate filenames without seeing endpoint,
prompt family, arm, seed, request, or the other reviewer's scores. They recorded object
counts, text-like marks, render-style failure, quality, readability, composition, and
artifacts. Their binary target judgments agreed on all 30 candidates.

A third blind adjudicator reviewed three sign images where marks were rated absent by one
reviewer and ambiguous by the other. All three were adjudicated as decorative or glyph-like
but not clearly readable text.

The sword rubric exposed one calibration defect: both reviewers used
`extra_or_fused_blade: true` for the ordinary overlap where two swords cross. Final sword
compliance therefore uses their agreed sword-object count and neutral observations. A
normal crossing is allowed; missing swords or a third blade is a failure.

## Adjudicated Target Outcomes

`pass` means target severity 0, `ambiguous` means severity 1 and is excluded from the
binary analysis, and `fail` means severity 2-3.

### PixFlux

| Family | `B0` | `N1` concise | `N2` long | `P1` positive | `R0` repeat |
|---|---|---|---|---|---|
| Crossed-sword count | fail: no recognizable swords | fail: no recognizable swords | fail: no recognizable swords | pass: two swords | fail: no recognizable swords |
| Text contamination | pass: blank sign | pass: blank sign | pass: blank sign | pass: pictorial framed bottle | pass: blank sign |
| Flat render style | pass | pass | pass | pass | pass |

PixFlux's concise and long negative arms had the same semantic target result as baseline
in every family. The count prompt is the only efficacy-informative family: both negative
arms failed exactly as baseline did, while the constructive positive rewrite produced two
recognizable swords.

### BitForge

| Family | `B0` | `N1` concise | `N2` long | `P1` positive | `R0` repeat |
|---|---|---|---|---|---|
| Crossed-sword count | pass | pass | pass | pass | pass |
| Text contamination | pass | ambiguous glyph-like emblem | ambiguous glyph-like emblem | ambiguous decorative marks | pass |
| Flat render style | pass | pass | pass | pass | pass |

All BitForge baselines already avoided the primary failure. This makes the seed useful for
detecting field activity and possible regressions, but not negative-prompt benefit. The two
negative sign arms shifted from the baseline's framed potion design to purple bottles with
glyph-like emblems. The marks were not readable text, so this is a possible concept-priming
regression rather than a primary failure.

## Same-Seed Reproducibility

Exact request repeats were not universally deterministic:

| Endpoint | Count `B0=R0` | Text `B0=R0` | Style `B0=R0` |
|---|---:|---:|---:|
| PixFlux | no | no | no |
| BitForge | yes | no | yes |

PixFlux baseline-to-repeat normalized RGBA differences were small but nonzero:

- count `0.0035`;
- text `0.0143`; and
- style `0.0058`.

Its concise-negative differences were `0.0024`, `0.0135`, and `0.0040`, respectively—no
larger than ordinary repeat variation. Long-negative differences were also close at
`0.0039`, `0.0185`, and `0.0054`. Combined with the identical semantic outcomes, this is
calibration evidence that PixFlux's deprecated field was a no-op or very weak for these
requests. One seed cannot prove practical equivalence.

BitForge behaved differently:

- count and style repeats were pixel-identical, while concise-negative differences were
  `0.0335` and `0.0168`;
- long-negative differences were `0.0406` and `0.0171`; and
- text repeat difference was only `0.0052`, versus `0.1863` for concise negative and
  `0.1692` for long negative.

The field therefore changed BitForge output well beyond its observed repeat variation.
That establishes behavioral activity for the tested build, not benefit.

## Quality Outcome

Mean quality is the average of the two blind 1-5 ratings, then averaged across the three
families.

| Endpoint | `B0` | `N1` | `N2` | `P1` |
|---|---:|---:|---:|---:|
| PixFlux | 3.17 | 3.17 | 3.17 | 3.17 |
| BitForge | 4.33 | 4.33 | 4.17 | 4.00 |

No negative arm reaches the pre-registered material-harm threshold. BitForge's long count
negative scored 0.5 lower than its baseline pair, but the endpoint-wide long-negative
change was only -0.17. This is a lead for replication, not evidence of broad quality harm.

## What The Pilot Establishes

1. **BitForge's dedicated field is not a no-op.** Same-seed negative arms changed output
   beyond exact-repeat variation.
2. **Field activity is not benefit.** BitForge baselines already passed, so the run cannot
   estimate how many failures the field prevents.
3. **PixFlux showed no semantic benefit or harm.** Its negative-arm variation was similar
   to repeat variation, consistent with a deprecated no-op or weak control.
4. **Positive structure won the only informative failure.** PixFlux failed to render
   swords under baseline, concise negative, long negative, and repeat; the positive
   `exactly two ... crossing once in an X` rewrite succeeded.
5. **No clear “negative summoned exactly what it named” case occurred.** BitForge text
   negatives did produce ambiguous glyph-like emblems, which is suggestive but below the
   primary readable-text threshold.
6. **No material overall-quality harm was observed.** Long negatives also produced no
   benefit in this sample.

## What It Does Not Establish

- that PixFlux's field is always ignored;
- that BitForge negatives usually improve or worsen outputs;
- that long negative lists are harmless;
- that inline negation behaves like a separate field;
- that results generalize to other seeds, prompts, sizes, controls, animation, inpaint,
  Pixen, Pro, or future model builds; or
- practical equivalence from a one-seed sample.

The correct Phase 0 verdict is **inconclusive on good-versus-bad**, with strong evidence
that endpoint behavior differs.

## Required Protocol Revision

The frozen plan says not to purchase confirmation data for a family whose baseline never
fails. Two families now need replacement or harder calibration:

- The text baseline produced no clear text on either endpoint.
- The style baseline produced flat pixel art on both endpoints without any negative.
- The sword baseline is informative for PixFlux but too easy for BitForge.

The exact 30-call Phase 0B replacement protocol is now frozen in the controlled test
plan. Before the 180-call confirmation:

1. retain crossed-sword count for PixFlux;
2. introduce a stronger but non-contradictory BitForge count/duplication family;
3. test a directional signpost with a stronger natural text prior;
4. replace the uninformative render-style family with unwanted-subject and hard-projection
   priors;
5. run the separately approved Phase 0B calibration on only those replacements; and
6. freeze the endpoint-specific successful family set before expanding seeds.

Do not spend the planned 180 confirmation generations on the current text/style families.
That would increase sample size without increasing information.

## Runtime Consequence

The existing conservative runtime rule remains correct:

- inspect live route support;
- prefer positive structural wording and real controls;
- use a concise dedicated negative only where the selected schema exposes it;
- do not invent the field on Pixen, Pro, MCP, or modern v3 routes; and
- treat every exclusion as probabilistic and visually verify the output.

The pilot does not justify promoting “negative prompting is good,” “negative prompting is
bad,” or “negative prompting is harmless” into the runtime contract.
