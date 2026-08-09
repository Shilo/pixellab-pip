# PixelLab Inline Negative Prompting Current-Model Test Plan

Status: Stage A executed 2026-08-08; 76 calls and 124 candidates complete, scored, and
adjudicated.

Last reviewed: 2026-08-08.

Research basis: `../pixellab/pixellab-inline-negative-prompting-best-practices.md`.

Results: `../pixellab/pixellab-inline-negative-prompting-current-model-results.md`.

Historical dedicated-field study:
`../pixellab/pixellab-negative-prompting-confirmation-results.md`.

## Direction Change

The primary question is whether text telling the image model what not to generate helps
when that text is inside the complete user-facing `description`. A separate
`negative_description` parameter is neither required by this definition nor relevant to
the two primary routes.

The primary strata are:

1. Pixen / v3/new through REST `POST /v2/create-image-pixen`.
2. Create Image Pro / v2 through REST `POST /v2/generate-image-v2`.

BitForge and PixFlux are legacy evidence and receive zero weight in the current-model
result. REST holds the public surface fixed and captures exact request bytes. Pixen
`enhance_prompt` is explicitly `false`; no reference or style input is supplied.

## What The Experiment Can Attribute

The treatment is the deployed stack, not an abstract property of the words alone:

```text
inline wording × route/model × model prior × prompt parsing or rewriting × seed
× task × service build
```

Any hidden model selection, system prompt, prompt router, safety conditioning, or server
rewrite remains inseparable from the route result. Pixen and Pro are therefore analyzed
separately. A difference between them is a stack interaction, not proof of one hidden
component.

## Frozen Stage A

### Calls, images, and estimated usage

| Stratum | Core calls | Induction calls | Total calls | Images per 96×96 call | Expected images | Estimated usage |
|---|---:|---:|---:|---:|---:|---:|
| Pixen | 42 | 18 | **60** | 1 | 60 | ~60 generations |
| Create Image Pro | 12 | 4 | **16** | 4 | 64 | ~320–640 generations |
| **Total** | **54** | **22** | **76** | | **124** | **~380–700 generations** |

The Pro range uses the documented 20–40 generation category because the endpoint does
not publish a single fixed unit price. Returned usage and the before/after balance are
authoritative. Every Pro image is retained and scored, but the paid call is the
statistical cluster; four siblings are not four independent replications. Pro is an
explicitly cost-minimized calibration stratum: it can identify large counterexamples and
rank strategies, but it cannot establish a narrow endpoint-wide equivalence interval.

### Fixed inputs

- `image_size: {"width": 96, "height": 96}`
- registered seed in every request
- `no_background: true` for count, text, and induction; `false` for projection
- Pixen only: `enhance_prompt: false`
- no optional view, direction, outline, detail, style, or reference inputs
- deterministic queue shuffle seed: `20260811`

Seed registry:

| Block | Seed | Core | Induction |
|---|---:|---|---|
| `S1` | `632847119` | Pixen + Pro | Pixen + Pro |
| `S2` | `1948203657` | Pixen + Pro | Pixen only |
| `S3` | `947251603` | Pixen only | Pixen only |
| `S4` | `1558074219` | — | Pixen only |

The same numbers are bookkeeping across routes; they are not assumed to identify the
same latent state in different models.

## Core Efficacy Matrix

Each family uses four arms per seed/call block:

| Arm | Role | Causal interpretation |
|---|---|---|
| `B0` | neutral base | reference failure rate |
| `C1` | one concise inline exclusion | primary negative-wording treatment |
| `L1` | long exclusion and defect catalog | long-list dilution/harm treatment |
| `P1` | positive-only desired-state rewrite | strategy comparator, not a negative-wording ablation |

`C1` balances three common inline grammars over seed blocks: `No …`, `Without …`, and
`Avoid …`. The primary concise estimate averages them; syntax-specific results are
secondary. `L1` is deliberately a compound intervention and is used only to test the
real-world practice of broad negative boilerplate.

Pixen runs `3 families × 3 blocks × 4 arms = 36` core calls, plus an exact,
time-separated `B0` and `C1` repeat at `S1` for each family: **42 calls**.

Pro deliberately spends only **12 core calls** on the two cheapest high-information
families (`CNT`, `TXT`): `B0` and `C1` at `S1` and `S2` (eight calls), then `L1` and `P1`
at `S1` (four calls). Thus its primary contrast has two independent paid call blocks per
family, while the long-list and positive strategies remain calibration-only. Pro does not
run `PRJ` in Stage A. The `Avoid …` syntax at `S3` is therefore estimated on Pixen only.

### `CNT` — object-count duplication

Primary failure: anything other than exactly two whole sword objects, including an extra
or fused blade.

| Arm/block | Exact `description` |
|---|---|
| `B0` | `Crossed silver swords emblem centered in empty space.` |
| `C1/S1` | `Crossed silver swords emblem centered in empty space. No third sword or extra blade.` |
| `C1/S2` | `Crossed silver swords emblem centered in empty space. Without any third sword or extra blade.` |
| `C1/S3` | `Crossed silver swords emblem centered in empty space. Avoid duplicate swords and extra blades.` |
| `L1` | `Crossed silver swords emblem centered in empty space. Do not include a third sword, duplicate weapons, extra blades, shields, banners, text, watermark, cropped objects, blur, gradients, photorealism, or 3D rendering.` |
| `P1` | `Exactly two whole silver swords crossing once in an X, both fully visible, centered with clear empty space on all sides.` |

### `TXT` — pseudo-writing contamination

Primary failure: clearly repeated letter-, number-, word-, rune-, glyph-, label-, logo-,
signature-, or watermark-like marks. Natural wood texture is not failure.

| Arm/block | Exact `description` |
|---|---|
| `B0` | `Wooden fantasy directional signpost with three arrow-shaped boards at a crossroads.` |
| `C1/S1` | `Wooden fantasy directional signpost with three arrow-shaped boards at a crossroads. No text, letters, words, or numbers.` |
| `C1/S2` | `Wooden fantasy directional signpost with three arrow-shaped boards at a crossroads. Without text, letters, words, or numbers.` |
| `C1/S3` | `Wooden fantasy directional signpost with three arrow-shaped boards at a crossroads. Avoid writing, labels, and number-like marks.` |
| `L1` | `Wooden fantasy directional signpost with three arrow-shaped boards at a crossroads. Do not include text, letters, words, numbers, writing, labels, logos, signatures, watermarks, typography, runes, glyphs, slogans, blur, gradients, photorealism, or 3D rendering.` |
| `P1` | `Wooden fantasy directional signpost with three arrow-shaped boards; each board carries one centered pictogram: a red sword, a blue potion, and a green tree.` |

### `PRJ` — projection and view prior

Primary failure: any clearly visible side wall or diagonal/isometric depth rather than a
straight front elevation.

| Arm/block | Exact `description` |
|---|---|
| `B0` | `Small wooden cottage with a red door and two windows, full building visible.` |
| `C1/S1` | `Small wooden cottage with a red door and two windows, full building visible. No visible side wall or diagonal perspective.` |
| `C1/S2` | `Small wooden cottage with a red door and two windows, full building visible. Without a visible side wall or diagonal perspective.` |
| `C1/S3` | `Small wooden cottage with a red door and two windows, full building visible. Avoid isometric, three-quarter, and corner-facing views.` |
| `L1` | `Small wooden cottage with a red door and two windows, full building visible. Do not use an isometric view, three-quarter view, visible side wall, diagonal perspective, aerial view, top-down view, tilted camera, vanishing point, corner-facing building, rear view, or cropped building.` |
| `P1` | `Straight front elevation of one small wooden cottage, facade parallel to the screen, one centered red door and two front windows, full rectangular building visible.` |

## Direct Induction Sentinel

The efficacy matrix cannot establish that a named forbidden concept was induced merely
because its target outcome worsened. A separate noun-swap sentinel tests that mechanism.

| Arm | Exact `description` | Role |
|---|---|---|
| `B0` | `Quiet stone courtyard with an empty wooden bench and two potted ferns.` | no forbidden noun |
| `I1` | `Quiet stone courtyard with an empty wooden bench and two potted ferns. No red balloon.` | names the primary absent target |
| `Q1` | `Quiet stone courtyard with an empty wooden bench and two potted ferns. No black cat.` | matched negative syntax naming another target |
| `Pcap` | `Quiet stone courtyard with a wooden bench, two potted ferns, and one red balloon tied to the center of the bench.` | verifies the route can depict the target |

Primary outcome: visible red-balloon appearance. Black-cat appearance is secondary.
Pixen runs four seed blocks × four arms plus exact `S1/B0` and `S1/I1` repeats: **18
calls**. Pro runs one `S1` call for each arm: **4 calls**. Its induction result is a
sentinel, not a stable rate.

An induction signal requires `I1` to exceed both `B0` and `Q1` by at least 20 percentage
points, with `Pcap` succeeding in at least 75% of returned candidates. It is not called a
general mechanism unless replicated later with a second preregistered noun and context.

## Blinding And Scoring

After all Stage A calls finish, assign opaque randomized candidate IDs across route,
family, arm, seed, repeat, call cluster, and Pro candidate index. Reviewers do not see
metadata or Pro sibling membership. Score every candidate; never select a “best” Pro
image.

Primary outcome values are `pass`, `ambiguous`, and `fail`. Also score overall quality,
composition compliance, native-size readability, and artifact freedom from 1–5. Keep
these guardrails separate; do not collapse target success and quality into one arbitrary
score. Two independent reviews are required, with a third review only for primary-outcome
disagreements.

## Analysis And Weighting

- Pixen and Pro remain separate primary results.
- Each family has equal weight within a route.
- Each seed/call block has equal weight within a family.
- Each Pro call has one unit of weight; each sibling receives
  `1 / returned_candidate_count` inside that call.
- `C1-B0` is the sole primary efficacy contrast.
- `L1-B0` and `L1-C1` test broad-negative harm.
- `P1-C1` is a strategy comparison, not proof about negation alone.
- Exact repeats estimate deployed nondeterminism for both baseline and concise wording.
- Adjust the five tested route × family primary comparisons with Holm correction.
- BitForge and PixFlux have zero weight in every current-model estimate.

Use paired risk differences and paired bootstrap/randomization intervals for Pixen. For
Pro, first reduce candidates to call-level failure proportions and mean quality, then use
paired cluster bootstrap or permutation intervals. Never treat candidates as independent
`n`. Report ambiguity with lower/upper partial-identification bounds.

## Stage-A Decision Rules

Retain an endpoint-family pair for extension only when the target is scoreable, reviewer
agreement is at least 80%, ambiguity is at most 20%, and baseline failure is at least 20%
or a negative arm produces a plausible harm signal. Require `P1` composition compliance
of at least 75%; otherwise the route/family cannot express the intended control.

At a registered boundary:

- **Benefit:** at least a 20-point paired failure reduction for `C1-B0`, interval excludes
  zero, and the quality non-inferiority lower bound is above `-0.5`.
- **Harm:** at least a 20-point failure increase with interval above zero, or median
  quality falls by at least one point in at least 25% of blocks.
- **No meaningful effect:** the target interval lies wholly within ±10 points and quality
  within ±0.5.
- **Otherwise:** report inconclusive and extend once; do not tune inside captured data.

## Registered Extension Ceiling

Stage A is an exhaustive multi-mechanism Pixen calibration plus a deliberately small Pro
check, not a powered Pro endpoint-wide verdict. If retained Pixen pairs remain
inconclusive, add six blocks per family while preserving all prompts and controls. Add Pro
calls only when its small calibration shows an informative effect that needs confirmation,
one new matched block at a time. Freeze an exact extension manifest and obtain a separate
paid-call approval before any extension.

## Artifact Contract

Save under a new gitignored run directory:

```text
pixellab-pip-generations/negative-prompt-study-current-models-YYYYMMDD/
  protocol.md
  request-matrix.json
  requests.jsonl
  run-events.jsonl
  balance-before.json
  balance-after.json
  requests/
  responses/
  images/
  blinded-index.json
  scores-reviewer-a.jsonl
  scores-reviewer-b.jsonl
  adjudication.jsonl
  analysis.json
  manifest.json
  current-model-negative-prompt-study.blueprint.json
```

The resumable runner writes literal request bytes before submission, persists a Pro job
ID before polling, never resubmits uncertain or completed work, validates and hashes every
PNG, preserves every raw response, and stops on schema rejection, unexpected billing or
output count, uncertain submission state, or three consecutive transient failures.

The private self-contained HTML audit is generated in `.local/`. It must show every call,
endpoint, request body, description, route controls, raw request/response file, every
returned candidate, score, and final `helpful` / `no-op` / `worse` / `inconclusive`
classification. It is personal evidence and must never be added to the repository.

## Paid-Call Gate

This plan does not authorize generation by itself. Immediately before Stage A:

1. verify bearer authentication without revealing it;
2. generate and present all 76 exact request blocks and the ~380–700 generation
   range;
3. read PixelLab Pip's persistent `auto` setting exactly once;
4. capture a balance snapshot; and
5. if auto is off, wait for explicit approval covering this exact manifest.

Approval does not cover retries with uncertain charge state, prompt changes, route
substitution, enhancement, the registered extension, or an MCP bridge.
