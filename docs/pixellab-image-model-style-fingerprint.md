# PixelLab Image-Model Style Fingerprint (validation)

**Date:** 2026-07-13 · **Purpose:** a light second pass that **validates** the model profiles from the [image-model benchmark](pixellab-image-model-benchmark-results.md) — it does **not** re-rank models or override those findings. Lower weight than the ranking round; treat it as confirmation, not new law.

**Method:** the existing seed-7 outputs (58 model-cells — 16 each for PixFlux/Pixen/Pro, 10 for BitForge, which is excluded from the 256-wide runs) were tagged blind on two dimensions — neutral **Style** (`in-game` / `detailed` / `stylized-painterly` / `flat-simple`) and red **Cons** (`bad-direction` / `bad-crop` / `bad-high-detail` / `bad-low-quality-muddy` / `bad-follow-instructions`). The agent pre-tagged; the reviewer edited from there. **Reviewer tags are weighted higher** (human visual judgement); the agent's tags are kept only for the diff. No new generations.

## Per-model fingerprint (reviewer tags)

Counts are cells carrying the tag / cells for that model (seed 7).

| Model | Dominant style (pros) | Cons (failure modes) | Reads as |
|---|---|---|---|
| **PixFlux** | stylized 9/16 · flat 8/16 · in-game 11/16 · **detailed just 4/16** | almost none (1 dir, 1 follow) | **low-detail, painterly / stylized / flat, and clean** — few failure modes |
| **Pixen** | **detailed 15/16** · in-game 11/16 · stylized 3 · **flat 0** | **bad-crop 4 · bad-high-detail 3** (+1 dir, 1 follow) | **the high-detail model** — and its detail bites back as crop / over-detail cons |
| **Pro** | in-game 13/16 · detailed 9/16 · flat 4 · stylized 2 | bad-crop 2 · bad-follow 1 | **in-game, fairly detailed, low-con** — occasionally crops larger subjects (2 cells) |
| **BitForge** | in-game 6/10 · detailed 3 · flat 2 · stylized 2 | **bad-low-quality 6/10** · dir 2 · follow 2 · high-detail 1 | **the weakest render** — low-quality is its *distinctive* con (flagged on no other model) |

## Validation verdict — profiles hold, but evidence strength varies

- **Pixen — strongly confirmed.** detailed on 15/16 cells and flat on 0/16 (n=16), plus crop + over-detail cons. This is the one robust, hard-to-argue signal. ✅ Confirms "high-detail default → crops/zooms, over-details."
- **PixFlux — style confirmed; "clean" is only inferred.** Low-detail/painterly/flat is well-supported (detailed 4, stylized 9, flat 8). ✅ for that. But its near-zero cons imply "clean" only by *absence of tags on a loose pass* — that's weak, and "clean" wasn't in the original profile, so treat it as a hint, not a validated trait.
- **Pro — directional only.** in-game and "fairly detailed" (9/16) fit, but "crops larger subjects" rests on **2 cells** here; round 1's real evidence for that was the subject-fill metric, not this pass. ◑ Supports, doesn't prove.
- **BitForge — directional, distinctive.** low-quality flagged on 6/10 and on **no other model**, so muddiness is what *distinguishes* it (not what dominates its own tags — in-game ties at 6/10). ✅ for "weakest on raw quality," but n=10 + loose pass keep it directional.

The reviewer's edits removed the agent's over-applied `detailed` from **BitForge (7 cells)** and **PixFlux (5 cells)** — consistent with the profiles (BitForge reads *muddy*, PixFlux *flat/stylized*, not "detailed"). This is a **post-hoc** read of blind edits, and the reviewer was **anchored** to the agent's pre-fill, so it *corroborates* the profiles rather than independently proving them.

## Notes & caveats

- **A soft tension, stated plainly:** `in-game` is high on *every* model and **highest on Pro (13/16 > Pixen 11/16)**. So this broad tag does **not** corroborate "Pixen = the in-game look," and Pro actually reads in-game slightly more often. It doesn't *contradict* round 1 either — that claim was scene-specific *quality/fit* (Pixen won the scene category), a different construct from this general style tag. Net: the in-game tag is non-distinguishing here; keep Pixen's in-game strength as a **scene-specific** claim, not a universal one.
- **Weight:** lower than the ranking round. Anchoring (reviewer edited from agent pre-fill, not independent), small n (seed 7, ~1–2 samples/model/category), and a deliberately loose/quick reviewer pass all cap confidence. Directional confirmation only.
- **Instructions unchanged:** nothing here contradicts `SKILL.md`, the references, or the results doc, so no routing/instruction edits were made — this pass is validation, as intended.
- Raw tags: `pixellab-pip-generations/model-benchmark-20260713/style_tags_agent.txt` and `style_tags_user.txt` (git-ignored, local).
