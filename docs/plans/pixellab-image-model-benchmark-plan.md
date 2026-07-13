# PixelLab Static-Image Model Benchmark — Execution Plan

Status: **PLAN, ready to execute.** This is a self-contained handoff brief for a fresh agent (no prior conversation context) working **with a human reviewer**. Read it top to bottom before spending a single credit.

Goal: settle, with evidence, **which PixelLab image model is best for which kind of static image** — because the current routing ("subject → Pixen, scene/background → PixFlux, candidates/refs → Pro") rests on API design intent and vendor wording, **not on a measured, blind quality comparison.** This benchmark produces that measurement.

---

## ▶ Executing agent — start here (this file is the whole brief; no other prompt is needed)

If you were handed this file with no other instructions, **you are the executing agent** — run the benchmark below. It is self-contained: everything you need (models, endpoints, limits, costs, auth rules) is in §0. Execute in this order, and expect **two required human checkpoints** — this is a paid, human-reviewed benchmark by design, so you cannot skip them:

1. Verify `PIXELLAB_SECRET` is set (never print it) and snapshot balance (`GET /v2/balance`).
2. **[Human checkpoint 1 — budget]** Build the full job list (§1–§3), show the user the item count and cost estimate, and get an explicit **budget cap** and **minimal-vs-full** choice, plus any prompt tweaks, **before any paid call.** Do not spend without it.
3. Generate per §3 — handle sync vs. async correctly; save every raw output + `blueprint.json` + `usage.usd`; hard-stop at the cap.
4. Auto-score per §4 (`auto_scores.csv`).
5. Build **blind, shuffled** review grids per §5. **[Human checkpoint 2 — scoring]** The user scores them blind on the rubric; you collect the scores, then un-blind via the hidden mapping.
6. Synthesize per §6: recommendation matrix + results doc (`docs/pixellab-image-model-benchmark-results.md`) + proposed skill/doc updates; validate (`python dev-tools/qa.py` and `python -m pytest tests/test_helpers.py`) and commit.

Everything between the two checkpoints runs autonomously — do not pause to ask the user about routes, sizes, frame mechanics, or scoring criteria; those are all specified below.

---

## 0. Context you need (do not skip — you have no other context)

PixelLab generates pixel art via REST v2 (`https://api.pixellab.ai/v2`). Four **raw text-to-image models** are under test. None are exposed as MCP tools — model selection is a **REST-only** decision, so call the REST endpoints directly.

| Model | Endpoint | Sync? | Returns | Measured cost | Hard limits |
|---|---|---|---|---|---|
| **PixFlux** | `POST /v2/create-image-pixflux` (async variant: `/create-image-pixflux-background`) | sync (variant async) | 1 image | ~$0.0067–0.0082 @128px | area **32×32 → 400×400**, per-axis 16–400. **Rejects 16×16** (32×32-area floor). Transparent output blanks area >200×200. |
| **Pixen** | `POST /v2/create-image-pixen` | sync | 1 image | ~$0.008–0.010 @128px | area **32×32 → 512×512**, **width & height ÷4**, per-axis 16–768. Accepts 16×16. |
| **Pro** | `POST /v2/generate-image-v2` | **async** (poll job) | **4–64 candidates** | ~$0.095 @≤256px (**~12–14× the others**) | min 16×16; max **512×512 square**, 688×384 at 16:9. Candidate count auto-scales by max dim: ≤42px→64, 43–85→16, 86–170→4, >170→1. |
| **BitForge** | `POST /v2/create-image-bitforge` | sync | 1 image | ~$0.007–0.008 @128px | area **≤200×200**, per-axis 16–200. **Cannot exceed 200 per axis** (so no 256-wide). |

**Field-level capabilities (the real differentiators — verified against OpenAPI):**

| Field / control | PixFlux | Pixen | Pro | BitForge |
|---|---|---|---|---|
| `description`, `image_size`, `seed`, `text_guidance_scale`, `no_background` | ✅ | ✅ | ✅ | ✅ |
| `negative_description` | ✅ | ✅ | ❌ | ✅ |
| `init_image` (+ `init_image_strength`) | ✅ | ❌ | ❌ | ✅ |
| `forced_palette` | ✅ | ❌ | ❌ | ✅ |
| `outline` / `detail` / `view` / `direction` (sprite art-direction) | ❌ | ✅ **(unique)** | ❌ | ❌ |
| `style_image` (+ `style_strength`) | ❌ | ❌ | ✅ | ✅ |
| `reference_images` (×4 subject refs) | ❌ | ❌ | ✅ **(unique)** | ❌ |
| Inpainting + `mask_image` | ❌ | ❌ | ❌ | ✅ **(unique)** |
| Multiple candidates per call | ❌ | ❌ | ✅ **(unique)** | ❌ |

Pixen's `outline` = `{no outline, single color outline, multi color outline}`; `detail` = `{minimal, medium, high}`; `view` = `{side, low top-down, high top-down}`; `direction` = 8 compass values.

**The hypothesis this test challenges:** PixFlux is billed for "larger image understanding" (scenes/backgrounds), Pixen for "sprites" — but Pixen actually supports a *larger canvas*, and there is **no measured scene-quality comparison** in the repo. Do not assume the routing is right; measure it.

Prior evidence lives in: [pixellab-image-size-limits.md](../pixellab/pixellab-image-size-limits.md), [pixellab-api-pricing-model-list.md](../pixellab/pixellab-api-pricing-model-list.md), [pixellab-asset-routing.md](../pixellab/pixellab-asset-routing.md), [create-image-pro.md](../../skills/pixellab-pip/references/create-image-pro.md), [16px item spike](../pixellab/pixellab-16px-item-sprite-generation-spike.md).

### Execution rules (non-negotiable)
- **Auth:** requires `PIXELLAB_SECRET` in the environment, used only as `Authorization: Bearer <token>`. **Never print, echo, log, or paste the token value.** If it is absent, stop and report.
- **Async models** (Pro; PixFlux-background): `POST` returns a `background_job_id`; poll `GET /v2/background-jobs/{job_id}` until `status=completed` (results at `last_response.images`) or `failed`. Read per-call cost from the job's top-level `usage.usd`. Tolerate transient 5xx by re-polling the same id; **never resubmit a paid job.**
- **Budget:** this is a paid batch. **Get an explicit budget cap from the user before generating.** Snapshot balance (`GET /v2/balance`) before and after. Hard-stop at the cap.
- **Asset Integrity:** every pixel must come from PixelLab. Local code may only stitch/crop/pad/format-convert/score/annotate. **Do not draw, repaint, or synthesize art.** A checkerboard is allowed only as a labeled transparency-inspection backdrop in review grids — never baked into a saved asset.
- **Outputs:** save everything under `pixellab-pip-generations/model-benchmark-<YYYYMMDD>/`. Write a `*.blueprint.json` (route + exact request body + `_comment_prompt`) and a `manifest.json` per generation. Keep raw outputs untouched alongside any review grids.

---

## 1. Test matrix — categories × prompts

Seven categories. The first six are **apples-to-apples** across all four models; the seventh is a **capability-specific** test only two models can do. Each category has a **simple** and a **complex** prompt (to test easy vs. hard cases). Use these prompts verbatim, or refine them *with the user* before the run.

| # | Category | Transparency | Size(s) | Simple prompt | Complex prompt |
|---|---|---|---|---|---|
| C1 | **Character** (single subject) | transparent (`no_background:true`) | 128×128 | "a knight in plate armor holding a sword, facing left" | "a hooded elven ranger with a longbow, green cloak, leather armor, and a quiver of arrows" |
| C2 | **Item / icon** (small object) | transparent | 32×32 | "a red health potion bottle" | "an ornate closed golden treasure chest with gems on the lid" |
| C3 | **Object / prop** (standalone) | transparent | 64×64 | "a wooden barrel" | "an ornate iron street lamp with a glowing lantern" |
| C4 | **Background** (full scene, no subject) | opaque (`no_background:false`) | 128×128 **and** 256×144 (widescreen) | "a misty pine forest at dawn" | "a bustling medieval market square with stalls, banners, and cobblestones at golden hour" |
| C5 | **Scene** (subject/objects + full background) | opaque | 128×128 **and** 256×144 | "a lone knight standing before a campfire at night in a snowy pine forest" | "a wizard casting a spell in a cluttered alchemy lab: bubbling potions, bookshelves, a black cat on the table" |
| C6 | **Parallax layer** (transparent mid-ground scenery) | transparent (`no_background:true`) | 256×128 (wide band) | "a row of pine trees" | "a mid-ground side-scroller layer of overlapping bushes, ferns, and tree trunks, spanning the full width" |
| C7 | **Style-consistent set** (capability test — **Pro & BitForge only**) | transparent | 64×64 | "generate a matching sword and shield in the same art style" (drive with `style_image`/`reference_images`) | — |

Notes:
- **BitForge is excluded from every 256-wide run** (background/scene widescreen **and** the parallax band C6) — per-axis 200 cap. Record as "N/A (size limit)", not a loss.
- **Parallax (C6) is the depth test:** a transparent mid-ground band (a tree line / foliage) that composites *between* the far opaque background (C4) and the foreground — not a full scene (C5), not a single subject (C1/C3). It exercises transparency **and** scenery composition together, and is the transparent-layer form of the PixFlux-vs-Pixen scene question. Bonus if it could tile horizontally for parallax scrolling.
- **PixFlux transparency at 256×128** (the parallax band) is fine: area 32,768 px² is under PixFlux's ~40,000-px² transparent-blanking threshold — keep any transparent PixFlux test under that area.
- C7 exists because `style_image`/`reference_images` are the whole point of Pro/BitForge; PixFlux/Pixen structurally cannot do it — that is itself the finding.

---

## 2. Per-model settings & fairness protocol

Fairness = **each model at its documented default plus the controls it natively exposes**, same prompt, same size, same seeds. Do **not** hand-tune `text_guidance_scale` per model (leave defaults) — we want out-of-the-box quality.

- **Seeds:** run every config with **two fixed seeds** (`7` and `42`) → two samples per model/prompt, to blunt luck. (Drop to one seed for a cheaper "minimal" run — see Budget.)
- **PixFlux:** defaults; `no_background` per category. Optionally a second variant using `-background` (async) for C4/C5 to compare sync vs. background job — optional, only if budget allows.
- **Pixen:** use its native controls per category — Character/Object/Item: `view:"side"`, `outline:"single color outline"`, `detail:"medium detail"`, `direction:"south"` (or the facing the prompt implies). Background/Scene: leave `view`/`direction` at defaults (they are subject concepts; letting Pixen render a scene *without* scene-specific tuning is exactly the comparison).
- **Pro:** it returns multiple candidates — **save all of them**. Score two ways: (a) **first candidate** (fair single-shot vs. the others), and (b) **best-of-N** (the user picks Pro's best candidate — this is Pro's real advantage). Report both so Pro's candidate edge is visible but not free.
- **BitForge:** defaults. For C7 (style set), drive with a `style_image`.
- **Parallax (C6):** transparent, wide band; treat as a scenery layer — Pixen at defaults (**no** `view`/`direction`: it is scenery, not a posed subject), the others at defaults. The question: does the model yield a transparent mid-ground band that reads as depth scenery (with see-through gaps) rather than a single hero tree or an opaque strip?
- **Common:** identical `description` string across models; identical `image_size`; `no_background` set by category; record every field sent in the blueprint.

---

## 3. Generation protocol (step by step)

1. **Confirm scope with the user:** budget cap, minimal vs. full run, and whether to tweak any prompts. Snapshot balance.
2. **Build the job list:** category × prompt × model × size × seed, honoring exclusions (BitForge>200px; C6 = Pro+BitForge only). Print the full list with a **cost estimate** and get the user's go before spending.
3. **Generate** each job. Handle sync vs. async correctly. Save: raw image(s), the request `blueprint.json`, and `usage.usd`. For Pro, save every candidate as `..._cand00.png`, `_cand01.png`, ….
4. **Verify each output on arrival:** dimensions match request; transparency correct for the category; not empty/failed. Re-poll on transient errors; never resubmit a charged job. Log failures honestly (some models may reject some sizes — record as N/A).
5. **Do not stop to ask the user mid-batch** unless a hard-stop (budget) or a systematic failure occurs. Complete the batch, then hand off to scoring.

---

## 4. Automated scoring (objective pre-pass)

Write a Python/Pillow script (`score.py`) that computes, per output image, an objective metrics row. These are **proxies** — they pre-filter and inform, but the human review is authoritative for aesthetics and adherence.

Metrics (per image):
- `dimensions_ok` — matches the requested `image_size`.
- `has_alpha` / `opaque_fraction` — for transparent categories: expect a real alpha channel and a **low** opaque fraction (a cut-out subject, not a filled canvas). For opaque categories: expect ~100% opaque, no stray holes. Flag `no_background` requests that came back >85% opaque (a baked background — a known Pro/16px failure mode).
- `unique_color_count` — count distinct RGBA colors. Pixel art is usually tens–low-hundreds; **very high** (thousands) signals anti-aliasing/gradients (un-pixel-art-like); **very low** signals flatness. Report, don't over-weight.
- `edge_antialias_score` — sample transitions along the subject's alpha edge (or high-contrast interior edges); fraction that are soft/intermediate rather than hard steps. Lower = more authentic pixel art.
- `subject_fill` (transparent categories) — bounding box of opaque content ÷ canvas area; extreme values (tiny subject / overflowing) are flags.
- `cost_usd` — from `usage.usd`.
- `h_tile_continuity` (parallax C6 only) — mean abs diff between the left-edge and right-edge pixel columns; low = it could tile horizontally for a seamless parallax scroll. A bonus proxy, not a requirement — most prompts will not tile perfectly.

Emit `auto_scores.csv` (one row per image) and a per-category summary. **Do not rank models on auto-metrics alone** — use them to catch technical failures and to annotate the human-review grids (e.g., "⚠ 91% opaque despite no_background").

---

## 5. Human review protocol (the user scores — blind)

This is the decisive step. Keep it **blind and shuffled** to remove brand/position bias.

1. **Build review grids** — one contact sheet per (category × prompt × size × seed): the four models' outputs side by side (Pro = its first candidate for the apples-to-apples grid; add a separate "Pro candidates" sheet for best-of). Composite transparent outputs over a **neutral checkerboard** (labeled inspection aid only). **Anonymize:** label each cell `A/B/C/D`, and **shuffle the model→label mapping independently per grid.** Write the mapping to `mapping_hidden.json` — do **not** reveal it to the user until scoring is done.
2. **Give the user a scoring template** (`review_template.md` / `.csv`) — for each grid and each label, a 1–5 score on:
   - **Adherence** — does it match the prompt?
   - **Pixel-art quality** — clean, readable, authentic pixel art (not blurry/AA/mushy)?
   - **Category fit** — does it *read as the category*? (A character reads as a character; a **scene reads as a full scene with a real background**, not a floating subject; a background reads as a complete backdrop; a **parallax layer reads as a transparent mid-ground scenery band** — foliage/trees with see-through gaps that would composite *between* a far background and a foreground, not a single hero tree or an opaque strip.)
   - **Overall rank** (1–4 within the grid) + a free-text note.
   - For C6: rank Pro vs. BitForge on **style consistency across the pair**.
3. **The user reviews and scores.** The agent presents grids clearly (link the files, describe what to look at) and collects the scores. Do not lead the user toward a model.
4. **Un-blind** using `mapping_hidden.json` only after all scores are in.

---

## 6. Synthesis & deliverables

1. **Aggregate** human scores per model per category (mean of Adherence/Quality/Fit, plus average rank), across both seeds and both prompts. Attach the auto-metrics as supporting signal (cost, transparency correctness, AA score).
2. **Per-category winner** + runner-up, with the concrete reason and the score gap. Separate **best-absolute** from **best-value** (fold in the ~12–14× Pro cost multiple — Pro must *clearly* win to justify its price).
3. **Recommendation matrix:** `category → recommended model (+ when to use the runner-up)`. Explicitly answer the open question: **for backgrounds and scenes, does PixFlux actually beat Pixen, and is Pro worth its cost?**
4. **Write results** into `docs/pixellab-image-model-benchmark-results.md` (public-facing: describe findings, no raw filenames, keep the scoring evidence). Include the recommendation matrix and any surprises (e.g., a model winning outside its "intended" category).
5. **Propose skill/doc updates** only where the evidence changes agent behavior: the "General image" / "Background" router rows in [SKILL.md](../../skills/pixellab-pip/SKILL.md), [asset-routing.md](../pixellab/pixellab-asset-routing.md), and the scene-model note in [cinematic.md](../../skills/pixellab-pip/references/cinematic.md). Do not overwrite existing rules — reconcile with evidence, cite the results doc.
6. **Validate** any repo edits: `python dev-tools/qa.py` and `python -m pytest tests/test_helpers.py`. Commit with a conventional message.

---

## 7. Budget, size & guardrails

**Cost estimate (get user approval before running):**
- **Minimal run** (1 seed, simple+complex prompts, 6 apples-to-apples categories + C7): ~58 generations. ~46 cheap (~$0.008 → $0.37) + ~12 Pro (~$0.095 → $1.14) ≈ **~$1.50**.
- **Full run** (2 seeds): ~115 generations ≈ **~$3.00**, plus optional PixFlux-background variants and re-rolls. Set a cap around **$5** with a hard stop.

**Guardrails:**
- Get the budget cap and prompt sign-off from the user **before** the first paid call; hard-stop at the cap and report where it stands.
- Record model rejections (unsupported size) as **N/A**, not quality losses.
- Keep the run **blind** through scoring; never reveal the model↔label mapping early.
- No token printing; no local art; checkerboard only as a labeled inspection aid; raw outputs preserved.
- If a model systematically fails a category (e.g., transparency ignored at a size), that is a **finding** — record it, don't silently drop it.

---

## 8. Results template (fill during execution)

```
Run date: __________   Budget cap: $____   Actual spend: $____   Balance before/after: ____ / ____

Per-category winners (human-scored, blind):
  C1 Character:    winner ____  runner-up ____  (Δ score ___)  best-value ____
  C2 Item/icon:    winner ____  runner-up ____  (Δ ___)        best-value ____
  C3 Object/prop:  winner ____  runner-up ____  (Δ ___)        best-value ____
  C4 Background:   winner ____  runner-up ____  (Δ ___)        best-value ____
  C5 Scene:        winner ____  runner-up ____  (Δ ___)        best-value ____
  C6 Parallax:     winner ____  runner-up ____  (Δ ___)        best-value ____
  C7 Style set:    Pro vs BitForge → ____

Key questions answered:
  - Scene/background: PixFlux vs Pixen — measured winner & margin: __________
  - Transparent mid-ground (parallax) layers: which model yields depth scenery vs a floating subject: __________
  - Is Pro worth ~12–14×? Where yes / where no: __________
  - Any model winning outside its "intended" category: __________

Recommendation matrix (category → model): __________
Proposed skill/doc updates: __________
```
