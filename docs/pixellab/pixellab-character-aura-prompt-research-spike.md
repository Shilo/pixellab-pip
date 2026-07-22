# PixelLab Character Aura Prompt Research Spike

Last reviewed: 2026-07-21.

Purpose: record live Create Image prompt experiments for static `64x64` transparent character-aura effects. The target is an isolated, front-facing aura that can sit behind and around a standing character without generating the character itself. This is developer research, not the canonical runtime contract.

## Bottom Line

The best tested minimal prompt is:

> fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring

It consistently produced front-facing, vertically oriented aura effects. The energy ring anchored the lower edge without turning into physical ground, and small spikes continued around the front and sides of the ring. This made the effect feel integrated and immersive. Those foreground spikes may require a deliberate layer choice when compositing a character, but they are small enough to appear manageable.

The runner-up is:

> fully contained symmetrical energy aura with vertical power spikes and an energy ring at the base

It also consistently produced contained, front-facing aura effects. Its vertical spikes appeared mainly on the back side of the ring, leaving the sides and front comparatively empty. That separation may be useful when the entire aura should render behind a character and avoid foreground overlap. The tradeoff is weaker visual integration: concentrating the energy on one depth plane makes the result look flatter and more static, like background energy attached to a separate ring.

Touching the bottom canvas edge is acceptable when the touching pixels belong to the lower energy ring. It is not the same failure as spikes or ambient energy bleeding through the top or side boundaries.

## Target Composition

The experiments converged on these requirements:

- Static `64x64` transparent pixel-art effect.
- Front-facing or side-view-gameplay presentation, not an orthographic top-down ground effect.
- No generated character or humanoid silhouette.
- Natural aura coverage behind the future character; no required hole or empty center.
- Visible containment at the top and sides.
- A lower energy anchor rather than physical ground, a platform, or a hard material.
- Enough design freedom for palette, energy texture, and internal detail to vary.
- Minimal positive wording; do not rely on a long negative prompt.

## Controlled Setup

Unless noted otherwise, the MVP comparisons used:

| Field | Value |
|---|---|
| Route | `POST /v2/generate-image-v2` |
| Image size | `64x64` |
| Background | `no_background: true` |
| Outputs | 16 candidates per call |
| Usage | 20 generations per call |
| Reference image | none |
| Style image | none |
| Seed | omitted; each call received its own resolved seed |

Because each call used a different random seed, the results support prompt-level tendencies rather than a pixel-controlled causal proof. Strong repetition across all or most of sixteen candidates is still useful evidence.

## Prompt Evolution

### Reference-Guided Baseline

Prompt:

> An isolated symmetrical explosive energy aura with a completely empty center, jagged flame-like violet and electric-blue power spikes rising upward, branching white-blue lightning arcs spreading outward, bright purple plasma wisps and a glowing energy ring at the base; aura effect only, no person, no character, no face, no body, no silhouette, no text

Route: `generate-with-style-v2`, using the supplied violet aura as a style reference.

Observed result:

- Produced several attractive upright character-aura compositions.
- Established the useful combination of isolation, symmetry, upward power spikes, and a lower energy ring.
- The style reference strongly influenced palette and identity, so this run did not isolate the text prompt.
- The empty-center and long negative clauses were later found unnecessary for the desired compositing model.

Evidence: [`violet-energy-aura-20260721`](../../pixellab-pip-generations/violet-energy-aura-20260721/).

### Detailed Text-Only Pro Baseline

Prompt:

> An isolated symmetrical explosive energy aura with a completely empty transparent center large enough to contain a standing fighter sprite, jagged flame-like violet and electric-blue power spikes forming a hollow shell around that empty center, branching white-blue lightning arcs spreading outward along the aura perimeter, bright purple plasma wisps and a glowing energy ring at the base. Aura effect only: no person, no character, no face, no body, no silhouette, no figure-shaped fill, no central orb, no explosion core, no starburst, no text. Crisp chunky low-resolution pixel art with hard stair-stepped edges, near-black violet shadows, saturated purple and electric-blue glow, sparse white-hot highlights, high contrast, and transparent negative space.

Observed result:

- Produced sixteen highly consistent upright aura shells.
- Most had a large opaque light center despite the request for transparent negative space.
- Confirmed that vertical spikes plus a lower ring can strongly establish the intended presentation without a style image.
- Over-specified palette, texture, and exclusions; unsuitable as an MVP prompt intended to preserve variety.

Evidence: [`text-only-violet-energy-aura-pro-20260721`](../../pixellab-pip-generations/text-only-violet-energy-aura-pro-20260721/).

### PixFlux And Pixen Text-Only Checks

The same detailed text-only concept was also tried through PixFlux and Pixen.

- PixFlux produced a filled radial or starburst-like result rather than a usable aura shell.
- Pixen produced a filled purple-white blast rather than the intended character aura.
- For this variety experiment, Create Image Pro was more useful because one call returned sixteen reviewable candidates.

Evidence: [`text-only-violet-energy-aura-20260721`](../../pixellab-pip-generations/text-only-violet-energy-aura-20260721/) and [`text-only-violet-energy-aura-pixen-20260721`](../../pixellab-pip-generations/text-only-violet-energy-aura-pixen-20260721/).

### `aura effects`

Observed result:

- Maximized semantic variety: fire, water, lightning, wind, earth, cosmic, rings, crystals, and other effects.
- Did not reliably produce character auras.
- Demonstrated that an unconstrained category prompt is too broad even when variety is desirable.

Evidence: [`mvp-aura-effects-pro-20260721`](../../pixellab-pip-generations/mvp-aura-effects-pro-20260721/).

### `character power-up aura effects with an empty center`

Observed result:

- Frequently became flat top-down rings or portal-like effects.
- `empty center` encouraged circular negative-space compositions.
- `character power-up` did not reliably establish a front-facing view.

Evidence: [`mvp-character-aura-effects-pro-20260721`](../../pixellab-pip-generations/mvp-character-aura-effects-pro-20260721/).

### `front-view full-body character aura effects, empty center, no character`

Observed result:

- Reduced some top-down behavior but frequently generated actual humanoid bodies or silhouettes.
- Several candidates became full-bleed or scene-like.
- `front-view full-body character` activated a character-subject prior despite the later exclusion.
- `full-body` also encouraged subject-scale framing that occupied most of the canvas.

Evidence: [`mvp-front-view-character-auras-pro-20260721`](../../pixellab-pip-generations/mvp-front-view-character-auras-pro-20260721/).

### `isolated symmetrical upright energy aura with a hollow center`

Observed result:

- Removed the humanoid silhouettes.
- Most candidates became rings, portals, symbols, or bursts.
- The hollow-center requirement was conceptually wrong: the character will stand in front of the aura, so the aura should exist naturally behind the character rather than contain a cutout.
- `upright` alone was not a strong enough front-facing aura cue.

Evidence: [`mvp-isolated-upright-auras-pro-20260721`](../../pixellab-pip-generations/mvp-isolated-upright-auras-pro-20260721/).

### `isolated symmetrical vertical energy aura with power spikes and a grounded base`

Observed result:

- All candidates read as front-facing rather than top-down.
- `vertical energy aura` and `power spikes` together were treated as the likely orientation cue.
- `grounded base` was interpreted literally: many candidates gained platforms, crystals, stone-like structures, or other hard ground materials.
- Some effects still touched or crossed canvas boundaries.

Evidence: [`mvp-vertical-power-spike-auras-pro-20260721`](../../pixellab-pip-generations/mvp-vertical-power-spike-auras-pro-20260721/).

### `isolated symmetrical vertical energy aura with a grounded base`

Observed result:

- Removing `power spikes` allowed top-down rings and other incorrect views to return.
- Hard materials and platform-like bases remained.
- This comparison implicated `power spikes` as an important orientation cue and `grounded base` as the material/platform trigger.

Evidence: [`mvp-vertical-grounded-auras-pro-20260721`](../../pixellab-pip-generations/mvp-vertical-grounded-auras-pro-20260721/).

### `fully contained symmetrical energy aura with vertical power spikes`

Observed result:

- Strongest prompt before adding a lower anchor.
- All candidates were contained away from the canvas boundaries.
- Consistently produced the desired upright/front-facing presentation; a few spiral or orb-like motifs remained.
- Avoided hard ground and platform materials.
- Frequently left an unnatural triangular gap at the bottom because the model had no instruction for terminating the lower boundary.

Evidence: [`mvp-contained-vertical-spikes-auras-pro-20260721`](../../pixellab-pip-generations/mvp-contained-vertical-spikes-auras-pro-20260721/).

### `fully contained symmetrical vertical energy aura with power spikes`

Observed result:

- Word order mattered materially.
- Roughly ten candidates read as top-down, radial, spiral, emblem-like, or horizontal rather than front-facing.
- Multiple candidates touched the canvas edges.
- `vertical energy aura` did not perform as reliably as placing `vertical` directly on `power spikes`.

Evidence: [`mvp-contained-vertical-aura-power-spikes-pro-20260721`](../../pixellab-pip-generations/mvp-contained-vertical-aura-power-spikes-pro-20260721/).

### Best: `fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring`

Observed result:

- All candidates used an upright/front-facing aura composition.
- The lower ring removed the triangular bottom gap.
- Vertical energy continued around the front and sides of the ring, giving the aura an integrated, immersive volume.
- The ring consistently read as energy rather than a hard platform.
- One candidate touched the bottom boundary through its ring; this is acceptable for the intended composition.
- Foreground spikes introduce a possible character-overlap concern, but they are relatively small and can plausibly render in front of the character.

Evidence: [`mvp-bottom-energy-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-energy-ring-auras-pro-20260721/).

### Runner-Up: `fully contained symmetrical energy aura with vertical power spikes and an energy ring at the base`

Observed result:

- All candidates used an upright/front-facing aura composition and remained contained.
- The lower ring removed the triangular gap without creating hard ground.
- Vertical energy appeared primarily on the back side of the ring; the sides and front were comparatively empty.
- This creates a cleaner all-behind-character layering option with fewer z-index conflicts.
- It feels flatter, more static, and less immersive because the energy occupies one depth plane and the ring and background energy can read as two separated layers.

Evidence: [`mvp-energy-ring-at-base-auras-pro-20260721`](../../pixellab-pip-generations/mvp-energy-ring-at-base-auras-pro-20260721/).

## Phrase-Level Findings

| Wording | Observed tendency |
|---|---|
| `fully contained` | Strongest tested positive cue for keeping top and side pixels inside the canvas. |
| `isolated` | Helpful but insufficient by itself to prevent full bleed. |
| `vertical power spikes` | Strongest tested front-facing/upright orientation cue. |
| `vertical energy aura` | Unreliable; allowed many radial and top-down results when `vertical` no longer directly modified the spikes. |
| `power spikes` | Important in combination with vertical wording; removing it allowed top-down effects to return. |
| `grounded base` | Encouraged physical platforms, crystals, stone, and other hard materials. |
| `bottom energy ring` | Produced an integrated ring with small energy spikes at the front and sides. |
| `energy ring at the base` | Produced a cleaner background-oriented layer, but the ring and aura felt less integrated. |
| `empty center` / `hollow center` | Encouraged portals, rings, cutouts, and top-down negative-space compositions. |
| `front-view full-body character` | Encouraged actual character bodies and silhouettes, plus full-canvas framing. |
| `upright` | Too weak by itself; did not prevent rings, symbols, or portals. |

## Integration Tradeoff

The best prompt and runner-up are both valid, but they solve different compositing priorities:

The primary visual difference is depth distribution. `Bottom energy ring` produced energy on the back, sides, and front of the ring, making the aura appear to surround a volume. `Energy ring at the base` produced energy mainly on the back side, making the aura read as a flatter background layer. The first is therefore the stronger immersive result; the second is a specialized layering-safe alternative rather than an equal aesthetic result.

| Priority | Preferred prompt |
|---|---|
| Immersive aura surrounding the character | `...and a bottom energy ring` |
| Simplest all-behind-character layering | `...and an energy ring at the base` |

For the best prompt, a game may split the final composition into a background aura and a subtle foreground accent, or render the complete effect above the character when the small front spikes do not obscure important body details. That is an engine compositing decision; the static PixelLab output is still one image.

## Why `Bottom Energy Ring` Looks More Immersive

The evidence points to the complete phrase structure, not conclusively to the word `base` by itself.

The best prompt describes `a bottom energy ring`. Here, `bottom` directly modifies `energy ring`, and the ring is introduced as another feature of the aura. Across the batch, PixelLab treated that ring as an integrated part of the effect: energy occupied the rear arc, continued along both sides, and added smaller spikes across the front arc. Those overlapping depth cues make the aura appear to wrap around a volume.

The runner-up describes `an energy ring at the base`. This can be parsed as two spatially related components:

1. A vertical spiked aura.
2. A ring placed at its base.

Across that batch, PixelLab separated those components. The vertical energy rose mainly from the ring's rear arc while the front arc remained comparatively clean. With most energy on one depth plane, the image reads as a background aura standing behind a separate ring. That reduces occlusion and may help character layering, but it also removes the front-to-back overlap that created depth, so the result feels flatter and more static.

`Base` likely contributes because it commonly names a supporting location or attachment point rather than an intrinsic visual part. However, the earlier `grounded base` experiment produced physical platforms and hard materials, not the same rear-only energy distribution. That means the current runs do **not** prove that `base` alone causes the flat result. The more defensible working explanation is the relational construction `energy ring at the base`, which encourages separation and placement, versus the compound feature `bottom energy ring`, which encourages integration.

The [official Generate Image Pro API documentation](https://api.pixellab.ai/v2/docs) exposes a free-text `description` but no depth-plane, front-arc, rear-arc, or ring-integration field. PixelLab does not document this phrase-level behavior as a guarantee. The explanation above is therefore an inference from sixteen outputs per prompt, not an official model rule.

A controlled causal test would seed-lock these positive-only variants while holding every other field constant:

- `...and a bottom energy ring`
- `...and an energy ring at the bottom`
- `...and a base energy ring`
- `...and an energy ring at the base`

That comparison would separate word order, the relational phrase `at the`, and the noun `base`. Until such a test is run, use `bottom energy ring` because it is the best observed production wording, not because `base` has been proven universally harmful.

## Current Recommendation

Use this as the default MVP description for an immersive static character aura:

> fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring

Use this alternative when foreground overlap is unacceptable and a behind-character effect is preferred:

> fully contained symmetrical energy aura with vertical power spikes and an energy ring at the base

Keep color, material, motion, brightness, and center occupancy unspecified unless the request requires them. This preserves useful variation while maintaining the tested composition.

## Limits And Next Questions

- The prompt comparison was not seed-locked, so word-order conclusions should be treated as strong working evidence, not deterministic guarantees.
- `fully contained` may still permit contact at the bottom when the energy ring is treated as the anchor. Acceptance checks should distinguish intentional bottom-ring contact from top/side bleed.
- The foreground-spike z-index tradeoff has not yet been tested with an actual character composite.
- Animation may change containment or layering and should be evaluated separately from the static prompt.
- Different resolutions may alter how strongly the ring, spikes, and negative space are expressed.
