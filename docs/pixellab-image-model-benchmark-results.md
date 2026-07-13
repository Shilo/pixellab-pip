# PixelLab Static-Image Model Benchmark — Results

**Run date:** 2026-07-13 · **Models:** PixFlux, Pixen, Pro (`generate-image-v2`), BitForge
**Method:** blind, shuffled, rank-only human review · **Budget:** $5 cap, actual spend **~$5.20** (see Caveats) · balance $9.95 → $4.76

This is the measured answer to the open routing question: *which PixelLab image model is best for which kind of static image?* It replaces vendor-wording assumptions ("Pixen = sprites, PixFlux = scenes/backgrounds, Pro = candidates") with a blind quality comparison. **Read the Confidence & caveats section before acting on any single-category result.**

---

## Quick map (TL;DR)

Intent → model quality order, and the best-**value** pick (folds in Pro's ~12× cost). `>` = clearly better; `≈` = tied / too close to call (**not** the same model).

| Intent | Quality: best → worst | Best value |
|---|---|---|
| Character / single subject | Pro > Pixen > PixFlux > BitForge | **Pixen** |
| Item / small icon (≤~32px) | Pro > Pixen > PixFlux > BitForge | **Pro** |
| Object / standalone prop | PixFlux ≈ Pro > BitForge > Pixen | **PixFlux** |
| Background (no subject / backdrop) | Pro > PixFlux > Pixen > BitForge | **PixFlux** |
| Scene (subject + full environment) | Pixen > PixFlux > Pro > BitForge | **Pixen** |
| Parallax / transparent scenery band | PixFlux ≈ Pixen > Pro | **PixFlux / Pixen** |
| Style-consistent set / reference-driven | Pro > BitForge | **Pro** |

Model → tool (model choice is **REST-v2-only**; MCP/Aseprite don't expose it; `S-XL`/`M-XL`/… are *size* labels, not models):

| Model | REST v2 endpoint |
|---|---|
| PixFlux | `create-image-pixflux` (+ `create-image-pixflux-background`, async) |
| Pixen | `create-image-pixen` |
| Pro | `generate-image-v2` (async, returns candidates) |
| BitForge | `create-image-bitforge` |

---

## Method (short)

- **7 categories**, each a **simple** and **complex** prompt, two fixed seeds (7, 42): C1 Character, C2 Item, C3 Object, C4 Background (no subject), C5 Scene (subject + environment), C6 Parallax (transparent mid-ground band), C7 Style-consistent set (capability test, Pro + BitForge only).
- **124 generations**, zero failures. Each model run at its documented default plus the controls it natively exposes; same prompt/size/seed across models; no per-model prompt hand-tuning. BitForge excluded from every 256-wide run (200px per-axis cap) — recorded **N/A**, not a loss.
- **32 blind grids** (one per category × prompt × size × seed), model→label shuffled independently per grid, identities hidden until scoring closed. Reviewer ranked each grid **best→worst holistically** (adherence + pixel-art quality + category-fit). Pro scored on its **first candidate** for the apples-to-apples comparison.
- Score per grid normalized to `(N−rank)/(N−1)` → **1.0 = best, 0.0 = worst**, fair across N=3 (256-wide, no BitForge) and N=4.

---

## Per-category results (blind, un-blinded)

Score = mean normalized rank (higher better). Cost ≈ $0.008 cheap models, **~$0.095 Pro (~12×)**.

| Cat | Winner | Score | Runner-up | Best **value** | Key reading |
|---|---|---|---|---|---|
| **C1 Character** | Pro | 0.75 | Pixen 0.67 | **Pixen** | Pro wins but by only 0.08 — not worth 12×. Pixen > PixFlux for characters. BitForge dead last (0.00). |
| **C2 Item (32px)** | **Pro** | 0.92 | Pixen 0.75 | Pixen | Pro dominates tiny icons (3/4 firsts) — its candidate auto-scaling (32px → 64 candidates) is a real edge. Among cheap: Pixen ≫ PixFlux. |
| **C3 Object/prop** | PixFlux | 0.67 | Pro 0.67 (tie) | **PixFlux** | PixFlux ties Pro at 1/12 the cost. **Pixen is *worst* (0.25)** — surprise for the "sprite" model. |
| **C4 Background** (no subject) | Pro | 0.69 | PixFlux 0.56 | **PixFlux** | Pro edges it but PixFlux is best-value. **PixFlux > Pixen (0.375)** — confirms "backdrop → PixFlux". |
| **C5 Scene** (subject + env) | **Pixen** | 0.71 | PixFlux 0.56 | **Pixen** | **Surprise: Pixen wins full scenes; Pro is only 3rd (0.48).** Contradicts "solid scene → PixFlux". |
| **C6 Parallax** (transparent band) | PixFlux ≈ Pixen | 0.625 tie | — | **PixFlux / Pixen** | Both cheap models tie and work; **Pro is worst (0.25)** and produced 2 transparency-baked failures. |
| **C7 Style set** | **Pro** | 2–0 | BitForge | Pro (only option pair) | Pro's `reference_images`/`style_image` held cross-pair style better than BitForge's `style_image` in both seeds. |

Full per-model numbers (score / mean-rank / firsts) and the auto-metrics pre-pass are in the local (git-ignored) run folder: `pixellab-pip-generations/model-benchmark-20260713/aggregate_scores.json` and `auto_scores.csv`.

---

## The four questions the benchmark was built to answer

**1. Backgrounds & scenes — does PixFlux actually beat Pixen?**
*Split answer, and this is the headline finding.* For a **pure backdrop with no subject (C4)**, PixFlux beats Pixen (0.56 vs 0.375) — the existing "background → PixFlux" routing holds. But for a **full scene with a subject in an environment (C5)**, **Pixen wins outright** (0.71 vs 0.56). Head-to-head across all C4+C5 grids: Pixen ahead in 9, PixFlux in 7. The blanket rule "solid scene → PixFlux" is only half right: it's a *backdrop* rule, not a *scene* rule.

**2. Transparent mid-ground (parallax) layers — which yields depth scenery vs a floating subject?**
PixFlux and Pixen **tie and both work** as see-through foliage bands. **Pro is the worst** (0.25) and twice returned an opaque/near-opaque strip despite `no_background:true`. For parallax, the cheap models win on both quality and cost.

**3. Is Pro worth ~12–14×?**
**Only sometimes.** Clear yes: **tiny icons (C2)** where its candidate spread dominates, and **style/reference work (C7)**. Clear no: **scenes (C5)** — it loses to Pixen; **parallax (C6)** — worst of the field; **backgrounds (C4)** — it edges PixFlux but not by 12× worth. Characters (C1): a 0.08 margin — marginal upsell only. Note Pro was scored **first-candidate**; best-of-N would lift it further at *small* sizes (many candidates) but **not** for scenes/backgrounds — at ≥256px Pro returns a **single** candidate, so it has no candidate cushion, and still loses C5. Pixen's scene win is therefore robust to the best-of caveat.

**4. Any model winning outside its "intended" category?**
Yes, three:
- **Pixen** (billed "sprites/subjects") **wins full scenes (C5)** and is competitive on characters — but is **worst for standalone objects (C3)**.
- **PixFlux** (billed "scenes/backgrounds") is **best-value for objects (C3, tie with Pro)** and backgrounds, yet **loses scenes to Pixen**.
- **BitForge** is **consistently the weakest on raw quality** (last or near-last in C1/C2/C4/C5). Its value is its **unique capabilities** — `init_image`, `mask_image`/inpainting, `forced_palette`, `style_image` — not out-of-box quality. Never pick it as a default quality play.

---

## Recommendation matrix (evidence-based)

| Need | Recommend | When to use runner-up |
|---|---|---|
| **Character / single subject** | **Pixen** (best cheap) | **Pro** when quality is critical and the ~12× cost is acceptable (margin is small). |
| **Item / small icon (≤~32px)** | **Pro** (`generate-image-v2`) | Pixen when minimizing credits; it's the best cheap option and its 32px gap to Pro is the widest justification for Pro. |
| **Object / standalone prop** | **PixFlux** (ties Pro, 1/12 cost) | Pro for a quality upsell. **Avoid Pixen for props.** |
| **Background (no subject / backdrop)** | **PixFlux** | Pro only when backdrop quality is critical (edges PixFlux, not 12× worth). Avoid Pixen. |
| **Scene (subject + full environment)** | **Pixen** | PixFlux second. **Do not pay for Pro here** — it loses to both cheap models. |
| **Parallax / transparent scenery band** | **PixFlux or Pixen** (tie) | Either; keep transparent PixFlux under ~40k px². **Avoid Pro** (worst + transparency failures). |
| **Style-consistent set / reference-driven** | **Pro** (`reference_images`/`style_image`) | BitForge only if you need its inpaint/palette/init controls on the same call. |

---

## Confidence & caveats

- **Statistical weight is low.** 2 seeds × 2 prompts = **4 samples per model per category** (fewer where BitForge is excluded), scored by **one reviewer**, **rank-only** (order, not magnitude). Treat results as **directional evidence**, not a decisive ranking.
- **Strong, repeated signals** (trust more): Pixen wins scenes (C5); Pro dominates 32px icons (C2); BitForge weakest overall; Pixen weakest for objects (C3); Pro worst at parallax (C6).
- **Close calls** (trust less): C1 Character (Pro over Pixen by 0.08), C3 Object (PixFlux ≈ Pro tie), C4 Background (Pro over PixFlux by 0.13). Don't over-rewrite routing on these alone.
- **Pro = first-candidate.** Best-of-N would raise Pro at small sizes only; it changes none of the scene/background/parallax conclusions (single candidate at ≥256px).
- **Fairness note.** C1-simple's "facing left" was honored for Pixen via `direction:"west"` (regenerated); all other categories left facing unspecified and un-penalized. Each model ran at documented defaults + native controls only.
- **Budget overrun.** A concurrent-process race (four runners across session restarts) drove **actual spend to ~$5.20, ~$0.20 over the $5 cap**; ~$1.00 was duplicate generations before the race was caught and killed. The final dataset is clean: 124/124 unique jobs, zero failures. Fix for future runs: a single-writer cross-process spend lock, not per-process counters.

---

## Artifacts (this run)

Under `pixellab-pip-generations/model-benchmark-20260713/`: raw outputs + `*.blueprint.json` per job, `run_manifest.json`, `auto_scores.csv`, blind `grids/`, `mapping_hidden.json` (un-blind key), `aggregate_scores.json`, `blind_review.html` (self-contained blind gallery).
