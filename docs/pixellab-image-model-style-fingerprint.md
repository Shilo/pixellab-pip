# PixelLab Image-Model Style Fingerprint (validation)

**Date:** 2026-07-13 · **Purpose:** a light second pass that **validates** the model profiles from the [image-model benchmark](pixellab-image-model-benchmark-results.md) — it does **not** re-rank models or override those findings. Lower weight than the ranking round; treat it as confirmation, not new law.

**Method:** the existing seed-7 outputs (58 model-cells, all 4 models × 7 categories) were tagged blind on two dimensions — neutral **Style** (`in-game` / `detailed` / `stylized-painterly` / `flat-simple`) and red **Cons** (`bad-direction` / `bad-crop` / `bad-high-detail` / `bad-low-quality-muddy` / `bad-follow-instructions`). The agent pre-tagged; the reviewer edited from there. **Reviewer tags are weighted higher** (human visual judgement); the agent's tags are kept only for the diff. No new generations.

## Per-model fingerprint (reviewer tags)

Counts are cells carrying the tag / cells for that model (seed 7).

| Model | Dominant style (pros) | Cons (failure modes) | Reads as |
|---|---|---|---|
| **PixFlux** | stylized 9/16 · flat 8/16 · in-game 11/16 · **detailed just 4/16** | almost none (1 dir, 1 follow) | **low-detail, painterly / stylized / flat, and clean** — few failure modes |
| **Pixen** | **detailed 15/16** · in-game 11/16 · stylized 3 · **flat 0** | **bad-crop 4 · bad-high-detail 3** (+1 dir, 1 follow) | **the high-detail model** — and its detail bites back as crop / over-detail cons |
| **Pro** | in-game 13/16 · detailed 9/16 · flat 4 · stylized 2 | bad-crop 2 (else clean) | **clean, in-game, fairly detailed** — crops larger subjects occasionally |
| **BitForge** | in-game 6/10 · detailed 3 · flat 2 · stylized 2 | **bad-low-quality 6/10** · dir 2 · follow 2 | **the weakest render** — muddiness is its defining trait |

## Validation verdict — all four confirm their profile

- **PixFlux** — low-detail, painterly/stylized/flat, clean. ✅ Confirms "lower detail → painterly/stylized/abstract."
- **Pixen** — detailed on 15/16 cells (never flat), with crop + over-detail cons. ✅ Confirms the "high-detail default → crops/zooms, over-details" signature.
- **Pro** — clean, in-game, detailed, occasional crop of larger subjects. ✅ Confirms "high-fidelity, crops larger subjects."
- **BitForge** — muddiness dominates (6/10). ✅ Confirms "weakest on raw quality."

The reviewer's edits reinforced this: they removed the agent's over-applied `detailed` from **BitForge (7 cells)** and **PixFlux (5 cells)** — exactly right, since BitForge's texture is *muddy* and PixFlux's is *flat/stylized*, not "detailed." So the human correction moved the fingerprint **toward** the existing profiles.

## Notes & caveats

- **One nuance, not a conflict:** `in-game` is high across *all* models (Pro highest, 13/16). It is a broad trait, so it does not by itself distinguish models — the round-1 "Pixen in-game *scene* feel" is the narrower, scene-specific claim and still stands separately.
- **Weight:** lower than the ranking round. Anchoring (reviewer edited from agent pre-fill, not independent), small n (seed 7, ~1–2 samples/model/category), and a deliberately loose/quick reviewer pass all cap confidence. Directional confirmation only.
- **Instructions unchanged:** nothing here contradicts `SKILL.md`, the references, or the results doc, so no routing/instruction edits were made — this pass is validation, as intended.
- Raw tags: `pixellab-pip-generations/model-benchmark-20260713/style_tags_agent.txt` and `style_tags_user.txt` (git-ignored, local).
