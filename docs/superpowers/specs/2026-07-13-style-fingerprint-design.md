# Style Fingerprint — Design

**Date:** 2026-07-13 · **Status:** design, awaiting review · **Depends on:** the completed image-model benchmark (`docs/pixellab-image-model-benchmark-results.md`) and its outputs in the git-ignored `pixellab-pip-generations/model-benchmark-20260713/`.

## Problem

The benchmark ranked models by **quality + intent-fit**, but the reviewer noted that ranking conflates preference, intent, and style, and does not answer *"what is each model natively biased toward, style-wise."* A model can lose the quality ranking yet be the only one that natively produces a given look (e.g. top-down flat pixel art). We want a systematic **style fingerprint** per model.

## Goal

From the **existing** 124 outputs (no new generations), produce a per-model style fingerprint, then confirm-or-correct the model-profile statements already written in the benchmark results doc.

## Non-goals

- No new generations, no credits spent.
- Not a re-ranking; style is descriptive, tagged not ranked.
- Not a capability test (we are not prompting each model for each style on demand).

## Tags (three parent axes, kept minimal)

**Neutral** descriptors (what the style *is*) plus **cons** (what went *wrong*) — no descriptive view/frame axes, so the result maps straight onto a pros/cons fingerprint. Each tagged output gets:
- **Style** (toggle each, neutral — no judgement): `in-game` · `detailed` · `stylized/painterly` · `flat/simple`.
- **Cons** (toggle each, shown red — failure modes): `bad-direction` (facing/orientation wrong for the prompt) · `bad-crop / over-zoom` (zoomed/cut off when the whole subject/scene was wanted — includes a parallax band gone opaque) · `bad-high-detail` (over-detailed/busy for the context) · `bad-low-quality / muddy` · `bad-follow-instructions` (ignored the prompt — missing or wrong content). A good output has no cons.

(Iterated from earlier View+Frame+Style drafts: the descriptive **View** and **Frame** axes were dropped by the reviewer's choice for a pure pros/cons shape — orientation problems now surface only as `bad-direction`, framing/opacity problems only as `bad-crop`. Tradeoff, accepted: the fingerprint states no positive default-view bias, only flags wrong views.)

## Scope

Seed 7 only — the 16 blind grids for seed 7, ~58 model-cells, covering all 4 models across all 7 categories once. (Full both-seed set and a curated subset were considered; one seed is the effort/coverage balance since style is fairly consistent per model.) C7 (style-set) is excluded from tagging — it is a capability pair, and Pro/BitForge style is captured in the other categories.

## Method

1. **Tagging surface:** extend the existing blind gallery into a `style_tag.html` page — identities still hidden and shuffled per grid; each cell exposes the Style + Cons togglers and a "copy tags" export. Self-contained, git-ignored, same as the review galleries.
2. **Agent pre-tags, reviewer edits** (chosen for low reviewer effort):
   - **Agent tags all 58 cells first**, blind, from the pixels — deliberately *not* from the model-profile conclusions already written — saved to `style_tags_agent.txt`.
   - The page **pre-loads the agent tags**; the **reviewer edits** any cell they'd tag differently, then exports.
3. **Reconcile:** compare tags cell-by-cell; **aggregate per model** into a Style + Cons fingerprint. Because the reviewer edits from the agent's tags (not independent), the higher-signal data is the reviewer's **overrides** — where they changed a tag — not raw agreement. Flag those for discussion.
4. **Honesty guardrail:** every output's `*.blueprint.json` records the exact prompt + any controls. Where Pixen ran with `view`/`detail`/`direction` set (subject categories C1–C3), tags are marked **control-applied**; *true default bias* is read mainly from the default cases (Pixen C4/C5/C6; all PixFlux/Pro/BitForge everywhere).

## Deliverable

A **Style fingerprint** doc — a new sibling `docs/pixellab-image-model-style-fingerprint.md` (keeps the already-large results doc focused; cross-linked from it) — with:
- A per-model table: dominant **Style** tags (the pros) + **Cons** frequency (the failure modes) + a confidence note.
- A short reconciliation: which existing model-profile statements the tags **confirm**, and which they **contradict** (with fixes applied to the profile docs).
- Raw tags kept in the git-ignored run folder (`style_tags_user.*`, `style_tags_agent.*`).

## Confidence & caveats

- **Anchoring (not independent)** — the reviewer edits from the agent's pre-filled tags, not from a blank slate, so raw tag agreement is inflated. The meaningful signal is the reviewer's **overrides**; agreement alone is weak confirmation. (Chosen deliberately to cut reviewer effort.)
- **Blindness is weaker than the ranking pass** — the reviewer has strong priors after extensive discussion; identities are still hidden but this is not pristine.
- **Small n** — seed 7 only, ~1–2 samples per model per category; a fingerprint is directional, not decisive.
- **Partial contamination** — Pixen's subject categories carried controls; handled via the control-applied annotation above.

## Validation

Deliverable edits to tracked docs must pass `python dev-tools/qa.py` and `python -m pytest tests/test_helpers.py`. Agent-facing files (`SKILL.md`, `references/*`) stay YAGNI — style-fingerprint prose lives in `docs/`; only a routing-relevant, non-duplicative nugget may reach an agent-facing file, and only if it changes behavior.
