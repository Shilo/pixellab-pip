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

Split into **neutral** descriptors (what the style *is*) and **cons** (what went *wrong*), so the result maps straight onto a pros/cons fingerprint. Each tagged output gets:
- **View** (pick 1, neutral): `front` · `side` · `top-down` · `three-quarter` · `n/a` (subjectless scene).
- **Style** (toggle each, neutral — no judgement): `in-game` · `detailed` · `stylized/painterly` · `flat/simple`.
- **Cons** (toggle each, shown red — failure modes): `unwanted-view` (orientation doesn't match the prompt) · `unwanted-crop` (zoomed/cut off when the whole subject/scene was wanted) · `unwanted-detail` (over-detailed/busy for the context) · `low-quality/muddy`. A good output has no cons.

(Earlier iterations used a `Frame` axis and a `low-quality` style tag; `Frame` is folded into `unwanted-crop` and `low-quality` moved to cons, so the neutral tags describe and the red tags flag problems. Parallax note: a dense **opaque** band (transparency lost) is tagged `unwanted-crop` — the model zoomed into the foliage until the see-through gaps disappeared — so no dedicated opacity con is needed.)

## Scope

Seed 7 only — the 16 blind grids for seed 7, ~58 model-cells, covering all 4 models across all 7 categories once. (Full both-seed set and a curated subset were considered; one seed is the effort/coverage balance since style is fairly consistent per model.) C7 (style-set) is excluded from tagging — it is a capability pair, and Pro/BitForge style is captured in the other categories.

## Method

1. **Tagging surface:** extend the existing blind gallery into a `style_tag.html` page — identities still hidden and shuffled per grid; each cell exposes the three tag pickers and a "copy tags" export (grid/cell → View, Frame, Style). Self-contained, git-ignored, same as the review galleries.
2. **Two independent raters:**
   - **User tags blind** via the page.
   - **Agent tags independently** by viewing each cell's image fresh from the pixels — deliberately *not* from the model-profile conclusions already written, so it is a genuine second rater, not an echo. Agent tags without consulting `mapping_hidden.json` first (blind), then un-blinds.
3. **Reconcile:** compare tags cell-by-cell; compute simple agreement; **aggregate per model** into a dominant View / Frame / Style fingerprint with an agreement note. Flag disagreements for discussion.
4. **Honesty guardrail:** every output's `*.blueprint.json` records the exact prompt + any controls. Where Pixen ran with `view`/`detail`/`direction` set (subject categories C1–C3), tags are marked **control-applied**; *true default bias* is read mainly from the default cases (Pixen C4/C5/C6; all PixFlux/Pro/BitForge everywhere).

## Deliverable

A **Style fingerprint** doc — a new sibling `docs/pixellab-image-model-style-fingerprint.md` (keeps the already-large results doc focused; cross-linked from it) — with:
- A per-model table: dominant **View**, **Frame**, **Style** tags + a confidence/agreement note.
- A short reconciliation: which existing model-profile statements the tags **confirm**, and which they **contradict** (with fixes applied to the profile docs).
- Raw tags kept in the git-ignored run folder (`style_tags_user.*`, `style_tags_agent.*`).

## Confidence & caveats

- **Blindness is weaker than the ranking pass** — the reviewer has strong priors after extensive discussion. Tagging blind still forces judging the pixels over the label, but is not pristine; stated honestly, not oversold.
- **Small n** — seed 7 only, ~1–2 samples per model per category; a fingerprint is directional, not decisive.
- **Partial contamination** — Pixen's subject categories carried controls; handled via the control-applied annotation above.
- **Style is partly prompt-driven** — our prompts rarely specified view/framing, so the view/frame a model *chose* is informative; where a prompt did imply a view, note it.

## Validation

Deliverable edits to tracked docs must pass `python dev-tools/qa.py` and `python -m pytest tests/test_helpers.py`. Agent-facing files (`SKILL.md`, `references/*`) stay YAGNI — style-fingerprint prose lives in `docs/`; only a routing-relevant, non-duplicative nugget may reach an agent-facing file, and only if it changes behavior.
