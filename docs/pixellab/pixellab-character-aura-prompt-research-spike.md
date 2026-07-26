# PixelLab Character Aura Prompt Research Spike

Last reviewed: 2026-07-26.

Purpose: record live Create Image prompt experiments for static `64x64` transparent character-aura effects. The target is an isolated, front-facing aura that can sit behind and around a standing character without generating the character itself. This is developer research, not the canonical runtime contract.

## Bottom Line

The best tested minimal prompt is:

> fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring

It consistently produced front-facing, vertically oriented aura effects. The energy ring anchored the lower edge without turning into physical ground, and small spikes continued around the front and sides of the ring. This made the effect feel integrated and immersive. Those foreground spikes may require a deliberate layer choice when compositing a character, but they are small enough to appear manageable.

The runner-up is:

> fully contained symmetrical energy aura with vertical power spikes and an energy ring at the base

It also consistently produced contained, front-facing aura effects. Its vertical spikes appeared mainly on the back side of the ring, leaving the sides and front comparatively empty. That separation may be useful when the entire aura should render behind a character and avoid foreground overlap. The tradeoff is weaker visual integration: concentrating the energy on one depth plane makes the result look flatter and more static, like background energy attached to a separate ring.

Touching the bottom canvas edge is acceptable when the touching pixels belong to the lower energy ring. It is not the same failure as spikes or ambient energy bleeding through the top or side boundaries.

Model-level conclusion: Create Image Pro (`POST /v2/generate-image-v2`) is the production route for
this asset. It repeatedly returned coherent batches of modular, character-free, front-facing aura
candidates from the best prompt. Pixen occasionally produced useful cells—most notably Batch 40
request 2 and Batch 42 request 2—but never produced the target reliably across repeated calls or
across all cells at acceptable quality. Pixen remains research-only for this aura family.

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

### `fully contained symmetrical energy aura with vertical power spikes and a subtle bottom energy ring`

Observed result:

- Retained the front-facing vertical composition.
- The subtler ring itself remained visually appealing.
- `Subtle` also reduced the small vertical spikes on the ring's front arc instead of affecting only ring prominence.
- Many candidates therefore emphasized rear spikes and a bright interior, repeating the runner-up's depth problem and reducing the clear front-side-back integration of the current best prompt.
- One candidate touched a canvas edge.
- This did not improve on the current best prompt.

Evidence: [`mvp-subtle-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-subtle-bottom-ring-auras-pro-20260721/).

### `fully contained symmetrical energy aura with vertical power spikes surrounding a bottom energy ring`

Observed result:

- Retained front-facing orientation and full containment.
- Energy consistently occupied the ring circumference, reinforcing surrounding depth.
- `Surrounding` made the lower ring too volumetric: instead of reading as a flat aura ring lying on the ground plane, it often read as a freestanding three-dimensional ring or circular object.
- The ring also became the dominant subject, and several candidates drifted toward thorns, vines, debris, or constructed ring materials.
- The original `with ... and a bottom energy ring` wording preserved a better balance between the vertical aura and its lower ring.
- This did not improve on the current best prompt.

Evidence: [`mvp-surrounding-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-surrounding-bottom-ring-auras-pro-20260721/).

### `fully contained symmetrical energy aura with vertical power spikes and a flat bottom energy ring`

Observed result:

- Containment passed, but `flat` did not reliably produce a fuller ground-plane aura ring.
- The vertical effect moved into the dead center of the ring instead of emerging around its outside perimeter.
- That central mass often read as an elemental object seated inside the ring rather than an aura surrounding a future character.
- Several candidates also became floating emblems, crystals, ornamental forms, or other constructed objects.
- The modifier weakened the established aura composition rather than improving only ring orientation.
- This did not improve on the current best prompt.

Evidence: [`mvp-flat-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-flat-bottom-ring-auras-pro-20260721/).

### `fully contained symmetrical energy aura with vertical power spikes and a wide bottom energy ring`

Observed result:

- Retained the front-facing composition overall.
- As in the `flat` batch, the effect became a dead-center elemental object inside the ring instead of energy distributed around the ring's outer circumference.
- `Wide` made the lower feature broad and visually dominant rather than merely fuller.
- Several candidates drifted into physical platforms, crystals, stones, or constructed bases, repeating part of the earlier `grounded base` failure.
- The wide ring also regained an overly three-dimensional, material-like form rather than the desired flat aura-circle appearance.
- One candidate touched a canvas edge.
- This did not improve on the current best prompt.

Evidence: [`mvp-wide-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-wide-bottom-ring-auras-pro-20260721/).

The shared failure across both batches is more important than their individual modifier effects: adding either `flat` or `wide` broke the established outside-perimeter distribution. The model centered a discrete subject inside the ring, making the output resemble an elemental summon, crystal, flame object, or emblem rather than a character aura. Because the two calls used different randomized seeds, the experiment cannot prove that either word deterministically causes this layout. The repeated batch-level tendency is sufficient to reject both variants for production, while a seed-locked repeat would be required to separate prompt causality from RNG.

### Seed-Locked `bottom aura ring` Versus `bottom aura circle`

These two calls used the same seed, `1379246801`, to reduce RNG as a comparison variable.

`fully contained symmetrical energy aura with vertical power spikes and a bottom aura ring`:

- Preserved containment and mostly upright compositions.
- Many candidates still placed a discrete elemental, emblem, flower, or crystal-like subject at the center.
- The rings were generally less full and coherent than those produced by `energy ring at the base`.
- Replacing `energy` with `aura` did not recover the desired Ragnarok-like lower ring.

Evidence: [`mvp-bottom-aura-ring-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-aura-ring-pro-20260721/).

`fully contained symmetrical energy aura with vertical power spikes and a bottom aura circle`:

- Preserved containment and mostly upright compositions.
- Circles were often fuller than the `aura ring` results.
- Several became portals, disks, constructed bases, or central elemental objects rather than perimeter aura energy.
- Replacing `ring` with `circle` improved fullness inconsistently while weakening aura identity.

Evidence: [`mvp-bottom-aura-circle-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-aura-circle-pro-20260721/).

The seed-locked comparison favors neither replacement over the current best. `Aura ring` weakened ring fullness; `aura circle` increased fullness at the cost of portals, disks, and central-object drift.

Most importantly, the central-subject failure was not present in the unmodified best batch. It appeared after replacing the proven phrase `bottom energy ring`:

- `Bottom aura ring` repeatedly generated an emblem, flower, crystal, or elemental symbol inside the ring rather than a continuous aura effect.
- `Bottom aura circle` came closer to the desired full lower shape, but it also repeatedly generated objects or discrete effects in the ring's center.

Because these two calls were seed-locked, this is stronger evidence than the earlier unpaired prompt comparisons. It does not prove that every future seed will behave identically, but it supports a practical conclusion: `energy ring` preserves the intended effect identity better than `aura ring` or `aura circle`. The added synonyms introduced a new center-object prior instead of refining the lower ring.

Further ring-synonym tweaking is low-value. It has made the causal picture harder to track while repeatedly degrading a prompt that already met the core requirements. Return to the unmodified best prompt for production and treat later variants as rejected research branches:

> fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring

### Current-Best Repeat: Seed Dominates The Center-Object Failure

The current-best prompt was repeated twice without wording changes.

Control seed `1379246801`, shared with the earlier `aura ring` and `aura circle` tests:

- Produced the same central-object and emblem-like tendency despite restoring the proven `bottom energy ring` wording.
- Most candidates did not distribute energy around the ring perimeter.
- This disproves the earlier working assumption that the two noun substitutions were the primary cause of the central-object failure.

Evidence: [`mvp-current-best-control-seed-pro-20260721`](../../pixellab-pip-generations/mvp-current-best-control-seed-pro-20260721/).

Fresh seed `2057719043`:

- Produced sixteen coherent front-facing aura rings with vertical energy distributed around their circumference.
- Avoided the emblem and central-elemental-object pattern.
- Closely reproduced the desirable behavior of the original current-best batch.

Evidence: [`mvp-current-best-fresh-seed-pro-20260721`](../../pixellab-pip-generations/mvp-current-best-fresh-seed-pro-20260721/).

This is the clearest causal result in the spike: seed `1379246801` strongly drives the central-object composition across multiple nearby prompts, while the fresh seed restores the desired perimeter aura using unchanged wording. The prompt remains the best tested production description, but a single Pro batch can land in an unsuitable compositional family. Production should omit the seed by default, review all sixteen candidates, and retry only when the returned batch is dominated by central objects. Do not reuse seed `1379246801` for this aura prompt family.

### Same-Seed Inline Exclusion Did Not Override The Composition

Prompt:

> fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring; continuous aura only, no central object or emblem

Seed: `1379246801`.

Observed result:

- The explicit exclusion did not remove the seed's central-subject tendency.
- Many candidates still contained crystals, stars, elemental forms, or emblem-like objects.
- The batch can plausibly look more explicitly object- or emblem-driven because the exclusion itself names `object` and `emblem`; text-to-image models may respond to named visual concepts even when they occur inside a negated clause.
- Several lower rings became detached, reduced, or visually secondary instead of integrating with perimeter energy.
- Containment still passed, but the target aura composition degraded.

This shows that a concise inline negative clause is weaker than the compositional prior selected by this seed and can introduce additional separation between the ring and effect. It does **not** prove that the negative wording caused or intensified the objects, because the clean current-best prompt already produced central objects at the same seed. A controlled attribution test would apply the negative wording to known-good seed `2057719043`, whose clean baseline already exists. Until then, treat prompt-token leakage as plausible and the seed as the demonstrated cause. Avoid spending more prompt effort trying to rescue seed `1379246801`; use a fresh randomized seed with the concise current-best prompt instead.

Evidence: [`mvp-current-best-no-central-object-pro-20260721`](../../pixellab-pip-generations/mvp-current-best-no-central-object-pro-20260721/).

### Random-Seed Ring-Consistency Modifiers

Three one-word variants were run without supplied seeds, as requested. Because each resolved to a different random seed, the batches compare production tendencies but do not cleanly isolate the modifiers.

`filled bottom energy ring`, resolved seed `1992979433`:

- Produced visible lower ring outlines, but none became the substantial, filled-out aura band intended by the modifier.
- Retained front-facing vertical energy and containment.
- Several candidates placed symbols or constructed details inside the ring.
- `Filled` modified neither the ring thickness nor its open-center topology reliably.

Evidence: [`mvp-filled-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-filled-bottom-ring-auras-pro-20260721/).

`complete bottom energy ring`, resolved seed `1371509464`:

- Produced the weakest batch: objects, emblems, creatures, and constructed designs often dominated.
- Ring consistency and front-facing aura identity were mixed.
- One candidate touched a canvas edge.
- Given the known strength of seed effects, this run cannot establish that `complete` caused the failure.

Evidence: [`mvp-complete-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-complete-bottom-ring-auras-pro-20260721/).

`continuous bottom energy ring`, resolved seed `1090711118`:

- Produced coherent ring outlines and front-facing perimeter energy in many candidates, but did not create a substantial filled-out aura band.
- Several candidates still drifted toward central symbols or object-like forms.
- Passed containment throughout the batch.

Evidence: [`mvp-continuous-bottom-ring-auras-pro-20260721`](../../pixellab-pip-generations/mvp-continuous-bottom-ring-auras-pro-20260721/).

None of the three modifiers achieved the intended ring fullness. `Filled`, `complete`, and `continuous` continued to produce thin or open ring outlines, and all three batches showed some degree of central-object drift. This suggests that the noun `ring` itself may impose the wrong topology: a narrow loop surrounding an available center. Once the center is compositionally available, the model often places an emblem, crystal, creature, flame, or other discrete subject there.

This does not mean `ring` always fails—the earlier `energy ring at the base` batch produced attractive, substantial Ragnarok-like lower effects. It means adjective-level attempts to thicken `bottom energy ring` have not worked, and further modifiers are unlikely to repair the noun's loop prior reliably. The next meaningful branch should replace `ring` with a phrase describing a broad circular energy **field** or foot-level aura, then test whether that avoids both the thin outline and the central-object slot. Do not reinterpret these three unseeded batches as successful fullness tests.

### `bottom energy field` And `bottom energy glow`

Both replacements failed more severely than `bottom energy ring`.

`fully contained symmetrical energy aura with vertical power spikes and a bottom energy field`, resolved seed `1095428719`:

- Did not produce a consistent flat foot-level field.
- Most candidates became centered orbs, stars, crystals, portals, emblems, or discrete elemental effects.
- Two candidates touched a canvas edge.

Evidence: [`mvp-bottom-energy-field-auras-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-energy-field-auras-pro-20260721/).

`fully contained symmetrical energy aura with vertical power spikes and a bottom energy glow`, resolved seed `1830412773`:

- Did not produce a consistent flat foot-level glow.
- Nearly every candidate became a central object or emblem, including stars, crystals, portals, masks, and orb-like effects.
- Containment passed but aura identity failed.

Evidence: [`mvp-bottom-energy-glow-auras-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-energy-glow-auras-pro-20260721/).

Despite different randomized seeds, both batches converged on the same central-subject failure. `Field` and `glow` are too broad to preserve the lower circular aura structure; they allow the model to reinterpret the entire image as one centered energy asset. `Ring` remains valuable because it supplies the lower spatial scaffold, even though attempts to make that ring fuller have been inconsistent.

### Energy-Field Rerun And `bottom energy circle`

The `bottom energy field` prompt was rerun with fresh randomized seed `1441055806`:

- The second batch repeated the same centered-subject tendency as the first field batch.
- Orbs, eyes, emblems, and elemental objects occupied the center throughout.
- No broad flat foot-level energy field emerged.
- Candidates 09 through 16 contained nontransparent canvas-edge pixels.

The recurrence across two independent random seeds substantially weakens the seed-only explanation. `Bottom energy field` is now rejected as a prompt phrase for this target.

Evidence: [`mvp-bottom-energy-field-rerun-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-energy-field-rerun-pro-20260721/).

`fully contained symmetrical energy aura with vertical power spikes and a bottom energy circle`, resolved seed `732782691`:

- Preserved containment but failed the aura composition.
- The circle became a central disk, orb, target, eye, or portal in nearly every candidate.
- `Circle` strengthened the centered-shape prior rather than producing a flat aura around a character.

Evidence: [`mvp-bottom-energy-circle-pro-20260721`](../../pixellab-pip-generations/mvp-bottom-energy-circle-pro-20260721/).

These results clarify the noun tradeoff: `field`, `glow`, and `circle` all collapse toward a centered standalone asset. `Ring` is the only tested noun that reliably maintains the lower perimeter scaffold, despite inconsistent band fullness.

### Known-Good Seed: `energy field` Versus `energy ring`

Known-good seed: **`2057719043`**. This seed produced the successful fresh-seed current-best batch and should be retained as the reproducible reference seed for this research.

Both prompts were run with that exact seed.

`fully contained symmetrical energy aura with vertical power spikes and a bottom energy field`:

- Some candidates retained broad lower energy shapes that are directionally closer to the desired full foot aura.
- Central symbols, emblems, crystals, and discrete elemental objects still appeared throughout the batch.
- Because the same seed produces clean perimeter auras with `bottom energy ring`, the persistent object drift is attributable to `bottom energy field`, not merely RNG.

Evidence: [`mvp-energy-field-working-seed-pro-20260721`](../../pixellab-pip-generations/mvp-energy-field-working-seed-pro-20260721/).

`fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring`:

- Produced sixteen highly consistent, contained, front-facing aura effects.
- Coherent bottom rings appeared throughout.
- Vertical spikes occupied the back, sides, and front rather than collapsing into discrete center objects.
- This independently reproduces the earlier successful batch at the same known-good seed.

Evidence: [`mvp-energy-ring-working-seed-pro-20260721`](../../pixellab-pip-generations/mvp-energy-ring-working-seed-pro-20260721/).

The controlled result favors `energy ring`, but the `2057719043` ring batch still contains circular motifs that can be read as objects. It should therefore be described as a previously favorable seed, not a guaranteed working seed. Seed `1379246801` remains a clearly poor central-object seed for this prompt family.

### Additional Unseeded Field And Ring Rerun

Both prompts were run again with no supplied seed.

`bottom energy field`, resolved seed `1600192573`:

- Repeated the central-object failure for a fourth field batch.
- Produced orbs, bowls, architecture, flowers, a bird-like emblem, and other standalone subjects.
- Did not produce a consistent foot-level perimeter field.

Evidence: [`mvp-energy-field-unseeded-rerun-pro-20260721`](../../pixellab-pip-generations/mvp-energy-field-unseeded-rerun-pro-20260721/).

`bottom energy ring`, resolved seed `1734275022`:

- Produced sixteen consistent front-facing aura rings.
- Vertical energy surrounded the lower ring without discrete center objects.
- The ring centers remained open, but they read as character placement space rather than object slots.
- One candidate touched a canvas edge.

Evidence: [`mvp-energy-ring-unseeded-rerun-pro-20260721`](../../pixellab-pip-generations/mvp-energy-ring-unseeded-rerun-pro-20260721/).

The growing evidence is no longer consistent with a seed-only explanation for `energy field`: four field runs across distinct seeds, including the previously favorable ring seed, all produced substantial object drift. By contrast, `energy ring` repeatedly produces coherent aura batches on random seeds, although individual batches can still contain motifs or thin/open rings. The reliable production strategy remains an unseeded `bottom energy ring` call followed by batch review.

## Consolidated Findings After The Initial Spike

The later experiments resolve several earlier uncertainties:

1. **Seed has a major effect, but it is not the whole explanation.** Seed `1379246801` repeatedly favored central objects across nearby prompts. A concise inline exclusion did not overcome it and may have reinforced the named `object` and `emblem` concepts. Seed `2057719043` was favorable for some ring batches but still produced motifs in later review, so it is a reproducible reference seed rather than a guaranteed good seed.
2. **`Bottom energy field` has a prompt-level object prior.** Four field batches across distinct seeds—including `2057719043`—produced orbs, emblems, architecture, flowers, crystals, and other standalone subjects. The failure persists beyond ordinary seed variance.
3. **`Bottom energy glow` is a total composition failure for this target.** It discarded the lower scaffold and produced centered standalone effects almost throughout.
4. **`Bottom energy circle` is a top-down cue.** It produced disks, eyes, targets, portals, and other centered circular assets rather than a front-facing character aura.
5. **`Ring` is structurally necessary in the tested vocabulary.** It is the only lower-feature noun that repeatedly preserves a foot-level perimeter, character-placement space, and front-facing vertical effect.
6. **Attempts to thicken the ring did not reliably work.** `Filled`, `complete`, `continuous`, `flat`, and `wide` did not create a consistently substantial aura band. Some introduced central objects, physical materials, excessive three-dimensionality, or weakened foreground energy.
7. **The clean unseeded ring rerun is the strongest production validation.** Resolved seed `1734275022` produced sixteen consistent front-facing aura rings without discrete center objects. This supports omitting the seed in production and reviewing the returned batch.

Current reliable structural prompt:

> fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring

The next research axis is no longer the ring. The ring should remain unchanged while the emitted effect vocabulary is varied. `Energy aura` plus `vertical power spikes` reliably establishes orientation, but it also strongly favors flame-, crystal-, lightning-, and raw-energy-like silhouettes and palettes. A more flexible prompt should preserve containment, symmetry, vertical presentation, and `bottom energy ring` while replacing those morphology-heavy words with a broader aura-effect phrase.

### Broad Emitted-Effect Wording While Keeping The Ring

`fully contained symmetrical aura effect emanating vertically from a bottom energy ring`, resolved seed `1862474265`:

- Greatly increased semantic variety, but became too broad for aura production.
- Produced crystals, trees, machinery, fountains, tornadoes, winged symbols, and other standalone objects.
- Several candidates lost or minimized the ring, and three touched canvas edges.
- `Emanating vertically` did not preserve aura identity without the stronger `power spikes` morphology cue.

Evidence: [`mvp-vertical-emanating-aura-ring-pro-20260721`](../../pixellab-pip-generations/mvp-vertical-emanating-aura-ring-pro-20260721/).

`fully contained symmetrical vertical aura effect with a bottom energy ring`, resolved seed `961142007`:

- Preserved containment and produced somewhat more usable aura-like candidates than the emanating variant.
- Still drifted broadly into fire objects, smoke columns, spirals, wings, crystals, pillars, pedestals, and portals.
- Ring preservation was inconsistent.
- Removing `power spikes` increased variety but also removed the strongest constraint preventing standalone objects.

Evidence: [`mvp-vertical-aura-effect-ring-pro-20260721`](../../pixellab-pip-generations/mvp-vertical-aura-effect-ring-pro-20260721/).

The result exposes a real tradeoff. `Vertical power spikes` narrows style toward flame, crystal, lightning, and energy-crown silhouettes, but it also maintains the asset's identity as a surrounding aura. Broad replacements allow more effect families but frequently become objects. Future experiments should preserve a perimeter-distribution cue while relaxing the word `spikes`; removing the morphology cue entirely is too unconstrained.

The user review confirms that neither broad replacement is consistent enough for production. Both
prompts were too permissive, and both frequently placed a discrete object in the center instead of
distributing an effect around the character space. The blueprint therefore retains `vertical power
spikes` and makes the aura theme configurable. This preserves the strongest known composition
constraint while allowing elemental and non-elemental variation.

### Configurable Blueprint Decision

Bundled blueprint: [`aura.blueprint.json`](../../skills/pixellab-pip/blueprints/aura.blueprint.json)

```text
fully contained symmetrical {{aura theme | default: energy}} aura with vertical power spikes and a bottom energy ring
```

The final variable is `aura theme`, not `elements` or `power spike theme`. It replaces the first
`energy` in `energy aura`, so neutral input resolves to the proven `energy aura`, `fire` resolves to
`fire aura`, and a phrase such as `fire, water, ice` is inserted once as one literal scalar. The
blueprint explicitly forbids splitting a comma-separated theme into multiple calls or assigning
themes to individual candidates; Pro infers variation inside its single returned candidate set.

The default is `energy`, not an empty string. Earlier empty-default syntax was valid and the
blueprint reader still resolves both `''` and `""` as empty strings, but an empty theme would leave
an awkward generic `aura` phrase and no longer reproduce the proven neutral prompt. The current
placement provides the requested thematic flexibility without producing constructions such as
`fire energy aura` or changing the number of paid calls.

The blueprint accepts a configurable `aura size`, defaulting to `64x64`. Candidate count is derived
from the completed Pro response because changing native size changes how many images the route may
return. All returned candidates are preserved and assembled into a compact review sheet without
assuming sixteen images or a four-by-four layout.

Animation is a separately approved optional branch inside the same portable
[`aura.blueprint.json`](../../skills/pixellab-pip/blueprints/aura.blueprint.json). An approval `TASK`
acts as a stop-or-continue gate immediately before a canonical `POST /v2/animate-with-text-v3` step.
Declining ends the workflow successfully with the static outputs; approval continues to the exact
animation request. This preserves one-file sharing, canonical request-field fidelity, and separate
authority for the additional paid call without adding a conditional-step schema.
After the static sheet is presented, the agent asks whether to run one additional
`animate-with-text-v3` job and explains that V3 treats the sheet as one canvas, applying simultaneous
motion across its cells rather than producing an independent animation sequence per candidate.

The current animation action is deliberately theme-neutral and motion-light:

```text
all aura effects flicker and pulse simultaneously in place with subtle brightness variation
```

Earlier actions that named vertical spikes rising and falling, perimeter ripples, edge shimmer, or
layered spike-only motion produced cell crossing, center glow, drifting elements, frozen regions, or
visible seams. Animating cells separately preserved isolation but was rejected because the desired
workflow animates the sheet as one job. The simplified action reduces semantic invention, but V3
still treats the sheet as one canvas and cannot guarantee independent cell motion. The blueprint
therefore warns before approval and verifies visual cell isolation separately from technical frame
validity. Eight generated frames are used because a `256x256` sheet reaches V3's documented
`width × height × frame_count <= 524288` budget at that count.

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

## Ragnarok Online Ring Reference

Ragnarok Online is a useful reference for why the runner-up's ring remains aesthetically strong. Gameplay examples emphasize a substantial luminous ring concentrated around the character's feet. The effect reads as an aura largely because the lower ring is visually complete and prominent, not because tall energy occupies every depth plane.

Community documentation for Ragnarok aura modification explicitly lists separate `Middle` and `Bottom` effects for normal, transcendent, and later-class auras. This supports treating the foot ring as a major aura component rather than a minor termination detail. See the [Hercules aura modification guide](https://board.herc.ws/threads/guide-aura-modification.3357/) and [rAthena aura examples](https://rathena.org/board/topic/112357-aura-color/). The Ragnarök Wiki likewise describes the original level-99 aura as condensed around the character; see [Aura](https://ragnarok.fandom.com/wiki/Aura).

This changes the interpretation of the two leading prompts:

- `Bottom energy ring` remains the best complete composition because energy occupies the back, sides, and front, creating volume and immersion.
- `Energy ring at the base` produces the better ring morphology: fuller, more substantial, and more reminiscent of Ragnarok Online's foot-focused aura language.
- Its weakness is not the ring. Its weakness is that the vertical spikes sit mainly behind that ring, so the combined effect feels flatter and less enveloping.

The desired next improvement is therefore a hybrid, not simply a smaller or less prominent ring: preserve the runner-up's full Ragnarok-like lower ring while restoring the current best prompt's restrained energy on the sides and front.

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

## Pixen Prompt Search (2026-07-25)

### Batch 1: direct aura nouns

Eight `64x64` transparent Pixen calls used `view: low top-down`, `detail: low detail`,
`outline: lineless`, and no prompt enhancement or fixed seed. The tested MVP descriptions were
`upright aura effect`, `vertical aura effect`, `standing aura effect`, `character aura effect`,
`power-up aura effect`, `aura rising from a foot-level glow`, `aura surrounding a standing point`,
and `vertical aura anchored at ground level`.

The batch failed. Pixen usually converted the short aura phrase into a concrete subject: shrines,
staffs, humanoids, framed portraits, or circular emblems. `power-up aura effect` was a fully
top-down radial burst. `aura rising from a foot-level glow` was the closest composition because it
produced a vertical effect above a lower anchor, but the anchor became a hard platform and the
effect remained too object-like. The endpoint's explicit low-top-down view and low-detail controls
were insufficient to overcome those noun associations.

Next test: remove `aura`, `character`, `standing point`, and physical anchor language. Compare
minimal `VFX` descriptions under seed-locked low-top-down and side views to determine whether the
camera field or the prompt noun is the stronger source of flat radial results.

### Batch 2: VFX nouns and camera view

Four seed-locked prompt pairs compared `view: low top-down` with `view: side`: `upward energy VFX`,
`rising power VFX`, `vertical magic VFX`, and `power-up VFX`. Other controls matched Batch 1.

The entire batch failed by producing humanoid combatants rather than isolated effects. This
happened in both camera views, so changing `low top-down` to `side` did not solve subject leakage.
The shared `VFX` wording, combined with energy/power/magic language, appears to invoke a character
or action-subject prior in Pixen. The failure was stronger than the direct-aura batch: none of the
eight results was usable as an effect layer.

Next test: keep `view: side` to rule out flat top-down presentation, but remove `aura`, `VFX`,
`character`, `power`, `magic`, and ground/base nouns. Describe only vertically arranged light or
particle phenomena.

### Batch 3: abstract light and particle phenomena

This side-view, low-detail batch tested `ascending light particles`, `rising translucent wisps`,
`vertical glowing streaks`, `upward flowing light`, `radiating vertical waves`, `pillar of soft
light`, `upward spiral of light`, and `rising luminous haze`, all without prompt enhancement or
fixed seeds. Two synchronous calls timed out without recoverable results; six returned images were
reviewed.

Removing aura/VFX/power/magic/character nouns successfully stopped character generation in all six
observed results. It did not produce a player aura: the outputs became an arrow-like particle trail,
smoke wisps, a spotlight/beam, an architectural light column, a flat spiral, and an isolated rising
streak. `rising translucent wisps` was the most reusable effect fragment, but it lacked the broad
behind-player coverage and lower surround needed for an aura.

This establishes a useful boundary: abstract phenomenon wording prevents characters, while an
unqualified phenomenon becomes a single object or trail rather than a surrounding layer. The next
batch reintroduces `aura` while explicitly framing the result as an empty backdrop/layer around
space, still using side view to prevent fully top-down circles.

### Batch 4: empty aura backdrops and layers

Eight side-view prompts combined aura/glow/radiance wording with `empty`, `backdrop`, `layer`,
`behind`, `around`, or `semicircular`. No characters or humanoid silhouettes appeared, confirming
that layer/backdrop framing is substantially safer than character/VFX/power-up wording.

The batch was still unusable as a modular aura. `empty` strongly produced literal holes: ornate
portals, framed voids, radial emblems, or a dark rectangular opening. `vertical glow around empty
space` produced a top-down platform with a light column; it had usable under/behind depth cues but
was too architectural and materially detailed. `empty vertical aura backdrop` came closest to a
behind-player silhouette, but read as an elaborate portal arch rather than a natural effect.

Next test: retain the successful compositional nouns `backdrop` and `layer`, remove `empty` and
center-hole language, and compare minimal aura/glow/radiance/field variants. This tests whether
backdrop/layer alone can suppress characters without forcing a portal.

### Batch 5: backdrop/layer without empty-center wording

Eight side-view prompts tested minimal combinations of vertical/upright/low-angle/surrounding with
aura/energy/glow/radiance/power-field and backdrop/layer. Removing `empty` eliminated the repeated
portal holes, but did not make the batch consistently subject-free. Three prompts generated a face
or full character, while others became a rainbow arc, radial starburst, or ornate platform.

`vertical aura backdrop` was the only promising result: it produced a free-standing vertical
aurora-like mass with no character, emblem, hard object, or fully top-down presentation. It could
sit behind a player, but it was tall, visually noisy, lacked a useful lower surround, and approached
the canvas boundaries. This is the first Pixen wording in the search to satisfy the core semantic
role, even though its composition and containment still need improvement.

Next test: refine only the successful `vertical aura backdrop` family with `contained` and
`compact`, plus close aura/glow and backdrop/background-layer variants. Keep side view and the
endpoint's low-detail control unchanged so prompt effects remain attributable.

### Batch 6: contained/compact backdrop refinements

The apparent Batch 5 improvement did not reproduce. The eight contained/compact aura/glow
backdrop/background-layer variants generated an energy doorway, patterned scene strips, a planet,
a character, a framed character panel, dense decorative columns, a portrait emblem, and a flat
galaxy disc. None was a reusable aura.

This confirms the user's concern that results remain highly random and inconsistent. More
importantly, `backdrop` and `background layer` are now rejected prompt nouns: Pixen often reads them
as scenery, panels, or full environmental compositions. `contained` and `compact` constrain the
result's framing but do not preserve its semantic type. Flat top-down discs also remain possible
despite `view: side`, so the camera field is weak guidance rather than a guarantee.

Next test: remove all scene/environment language and avoid circle/ring/radial cues. Use `sprite` as
the asset noun with minimal vertical/upright/contained/surrounding aura variants. A useful wording
must reproduce across multiple calls; one lucky output is not sufficient evidence.

### Batch 7: aura sprite wording

All eight side-view `aura sprite`/`glow sprite` variants failed. Seven generated explicit humanoid
characters or character portraits; the remaining result was a flame sitting in a decorative bowl.
`sprite` is therefore rejected as an asset noun for Pixen aura generation: the model strongly
associates it with a complete game subject rather than a reusable effect layer. Modifiers including
vertical, upright, contained, rising, surrounding, low-angle, and symmetrical did not overcome that
prior.

Next test: avoid `sprite`, `aura`, scene nouns, and geometry nouns. Use `game effect layer` or `game
overlay` followed by only vertical/upright light phenomena. Include spell/status/combat/power
variants to see whether any game-context noun gives Pixen an effect-only semantic class without
invoking a character.

### Batch 8: game effect layer and overlay wording

The eight game-effect/overlay prompts remained inconsistent and mostly unusable. Four produced
explicit characters or character groups; three became a tile-mounted flame, radial emblem, or
ornate mask/totem. `game overlay, vertical radiance` avoided characters and produced a narrow
vertical diamond of light, but it was a single centered streak rather than an aura surrounding the
future player position.

`game effect layer` did not reliably mean a compositing layer to Pixen. Spell/status/combat/power
context increased character and emblem generation. The only effect-only result came from the more
neutral `game overlay`, but it lacked aura coverage.

The search has exhausted positive-only asset nouns without finding consistency. Because generated
characters are an absolute failure, the next controlled batch adds the shortest explicit exclusion
inside each description: `effect only, no character`. This tests whether Pixen can obey the
required subject boundary without adding a new scene, portal, or object prior.

### Batch 9: explicit no-character clauses

All eight prompts containing `effect only, no character` generated humanoid characters. The
exclusion did not merely fail occasionally; it correlated with the strongest all-character batch
in the search. This repeats the earlier Pro observation that mentioning the forbidden subject can
reinforce it. Explicit no-character wording is therefore rejected for Pixen.

The prompt search also changed several endpoint controls at once relative to the first Pixen test:
`detail: low detail`, `outline: lineless`, and `view: side` or `low top-down`. Before drawing a
strong conclusion that wording alone is the blocker, the next batch performs a seed-locked control
ablation using the original best Pro description. It compares omission or inclusion of detail,
view, and outline controls. This determines whether an endpoint control is pushing Pixen toward
characters, icons, or flat discs.

### Batch 10: endpoint-control ablation

Eight seed-locked calls used the original best Pro description while varying omission or inclusion
of `detail: low detail`, `outline: lineless`, `view: side`, and `view: low top-down`. Every result
remained the same semantic family: a dense circular orb/emblem with spikes and a lower ring. Some
controls changed styling or the ring projection, but none converted the emblem into a modular
behind-player aura.

This shows that the prompt and seed dominate composition more strongly than Pixen's detail, outline,
and view controls for this case. The controls are not the primary cause of characters or flat
effects. It also confirms that `view: side` cannot rescue a prompt/seed already committed to a
radial emblem.

The first four-theme Pixen comparison produced its only near-aura from the water-themed version of
the original prompt. The next batch repeats that exact water description eight times with random
seeds and no view/detail/outline overrides. This measures whether the success was a reproducible
wording effect or a lucky seed before attempting further refinements.

### Batch 11: water-prompt reproducibility

Eight random-seed calls repeated `fully contained symmetrical water aura with vertical power spikes
and a bottom energy ring` with no view/detail/outline overrides. All eight were subject-free,
contained, vertically presented, and compositionally related. This is the first prompt family to
remain consistent across random seeds. Several results had a credible lower ring plus rising energy
that could sit under and behind a separate player sprite.

The family is not yet acceptable as a general aura. Most results read as ornate magical objects:
crowns, lotus forms, crystalline cages, fountains, or decorative crests. The output is also strongly
water-colored and highly detailed. Still, the consistency proves that the original structured
prompt can work in Pixen when an elemental modifier supplies a coherent visual process.

The likely object/fanciness drivers are now `power spikes`, `energy ring`, and possibly
`symmetrical`; the likely consistency driver is `water` or its implied flowing organization. The
next batch removes those ornate geometry nouns incrementally and tests whether neutral `flowing`
can replace the water element while retaining an effect-only vertical composition.

### Batch 12: removing ornate geometry nouns

Eight one-off variants removed the full `power spikes`/`energy ring` structure or replaced `water`
with `flowing`. The outputs were all subject-free but reverted to standalone motifs: a wave cone,
snowflake, spiked orb, bowl, sphere, isolated arc, spiral emblem, and narrow portal. None provided
the broad under-and-behind coverage of Batch 11.

This falsifies the simple hypothesis that removing `power spikes` and `energy ring` would preserve
the useful composition while reducing ornament. In Pixen, the full combination of contained,
symmetrical, vertical spikes, and a lower ring appears to create the consistent multi-depth layout;
removing those anchors causes the model to collapse the aura into one central object. `flowing`
alone does not reproduce the organizing effect of `water`.

Next test: preserve the successful complete sentence structure but soften only the ornate nouns.
Compare water and flowing families using vertical energy/flow/rising wisps plus bottom/foot-level/
lower glow. This keeps both upper and lower compositional clauses while avoiding literal spikes and
rings.

### Batch 13: softened upper and lower clauses

All eight water/flowing variants with vertical energy, vertical flow, rising energy, or upward
wisps plus a lower glow remained subject-free. However, every result became a centered ornamental
symbol, plant, flame, or crest. None formed a broad modular layer around a future player position.

The softer nouns reduced literal ring-and-spike imagery but also removed the only reliable depth
layout. The successful Batch 11 sentence must remain intact for now. Prompt-only simplification is
not reducing ornament without losing aura structure.

Next test: return to the exact Batch 11 prompt and use Pixen's real style controls rather than more
noun substitutions. Four random calls use only `detail: low detail`; four use low detail plus
`outline: lineless` and `view: side`. This measures whether the consistent water composition can be
made simpler and less object-like without changing its semantic structure.

### Batch 14: simplifying the successful water family with controls

The first four results used only `detail: low detail`. Two were credible modular aura candidates:
a lower elliptical energy ring with tall water-like spikes rising behind and partly around the
future player position. One was fully top-down, and one became a cage-like object. This is the best
quality/concision tradeoff observed so far, but its approximate 50% success rate is not yet
consistent enough.

The last four added `view: side` and `outline: lineless`. All four became more object-like: lotus,
emblem, crown, or bowl forms. Those controls are counterproductive for this prompt family and are
rejected. In particular, the side-view field does not reliably create a gameplay-facing aura and
may encourage a standalone side-profile object.

Next test: retain the successful low-detail-only setup and the full bottom energy ring clause, but
replace only `vertical power spikes` with less ornamental rising phenomena. This isolates whether
`power spikes` is responsible for crown/cage forms while preserving the lower depth anchor that was
lost in Batch 12.

### Batch 15: softer vertical phenomena with the ring retained

All eight low-detail results were subject-free, contained, vertical rather than fully top-down, and
visibly connected to a lower elliptical ring. This is the strongest batch so far. Replacing `power
spikes` while keeping the complete sentence and `bottom energy ring` preserved the useful depth
layout and substantially reduced crowns, cages, characters, and radial emblems.

`vertical wisps` produced the most natural conventional aura: a broad lower ring with a tapered
vertical mass that could sit behind a player. `vertical currents` produced the second-best result:
a broader splash/fountain-like aura with a clear ring and under/behind depth. `vertical waves` was
also viable but slightly more bowl-like. `rising aura`, `upward energy`, `rising streams`, and
`vertical light` drifted toward wings, crystals, fountains, or ornate crests.

Next test: repeat the two winners four times each at random seeds. The candidate wording is not
accepted until it proves that the effect-only, gameplay-facing composition is reproducible rather
than another one-seed success.

### Batch 16: reproducibility of wisps and currents

Neither Batch 15 winner reproduced consistently enough. Four `vertical wisps` calls produced an
ornate crest, a narrow light column, a fountain/bowl, and a bright orb. Four `vertical currents`
calls produced two plausible aura layers, one ornate tree/crest, and one platform with a central
spike. All remained character-free and generally non-top-down, but only about half were usable even
under a generous acceptance threshold.

The lower ring plus vertical-clause structure is robust at preventing characters, but water-based
vertical nouns still drift toward fountains, plants, crystals, and ritual objects. The next batch
removes `water` while retaining the successful grammatical structure and low-detail control. It
tests non-material vertical phenomena—particles, sparks, haze, shimmer, trails, pulses, mist, and
glow—to find a less object-like organizing word.

### Batch 17: non-material vertical phenomena without water

All eight prompts produced centered emblems or ritual objects: ornate trees, compass-like stars,
crystals, framed orbs, floral symbols, and pedestals. None was a reusable aura. Removing `water`
while keeping the ring structure therefore lost the one theme token that had been suppressing hard
emblem geometry. Particles, sparks, haze, shimmer, trails, pulses, mist, and glow did not act as
equivalent organizing words.

The evidence now suggests Pixen needs an elemental/material modifier to interpret the structured
sentence as a coherent effect rather than an icon, but water is not necessarily unique. The next
batch restores the exact successful sentence and compares eight theme tokens under the same
low-detail setup: water as control, then fire, lightning, wind, smoke, mist, shadow, and spirit.
This tests whether another theme yields a softer aura while preserving the repeatable layout.

### Batch 18: theme-token comparison

Water, lightning, and wind were the only promising themes. Water produced a clean lower ring with
a vertical energy mass. Lightning produced a tall, narrow, ring-anchored effect, although it risked
reading as a spear or crystal. Wind produced stacked lower rings and vertical arcs, but was more
ornamental. Fire reverted to a fully top-down radial burst. Smoke and mist became rock/tree objects;
shadow and spirit became orb/star emblems.

The theme token materially controls both view and semantic type even though the surrounding prompt
is identical. This means a single arbitrary theme variable cannot currently guarantee a usable
Pixen aura. Water remains the best control, while lightning and wind are plausible alternatives
that need random-seed reproduction. The next batch runs three lightning, three wind, and two water
calls with identical low-detail settings to compare their failure rates directly.

### Batch 19: water, lightning, and wind reproduction

The three themes had similar low success rates. One of three lightning results was a plausible
ring-anchored vertical effect; the others were a star emblem and a rigid ring/spike object. One of
three wind results was a plausible compact aura; the others were ring sculptures. One of two water
results was a good flame-shaped aura with a lower ring; the other was a diamond emblem.

No tested elemental noun reliably exceeds seed randomness. However, the successful wind and water
results independently converged on a simple upright flame-like silhouette above a lower ring. That
shape may be a stronger Pixen prior than abstract aura wording. The next batch tests flame as the
explicit vertical organizer while retaining low detail and the bottom energy ring. Although this
narrows visual behavior, the current Pixen search prioritizes finding a reliable modular effect;
theme flexibility can be evaluated only after a stable base composition exists.

### Batch 20: flame as the vertical organizer

The batch was far more semantically consistent than abstract or arbitrary-theme tests: every result
was a contained orange flame/light effect, and none contained a character or fully top-down scene.
However, several still became portals, suns, campfire piles, flowers, or orb pedestals.

`fully contained vertical flame aura with a bottom energy ring` was the best prompt. Its result was
a simple vertical flame mass rising from an elliptical lower ring, with enough open surrounding
space to composite beneath and behind a separate player. It was less ornate and less object-like
than the water/power-spike family. A close variant, `fully contained flame aura rising from a bottom
energy ring`, was also usable but slightly more like a standalone flame.

Next test: repeat the best prompt eight times with low detail and random seeds. This directly tests
whether the first genuinely simple Pixen aura wording is robust enough to recommend.

### Batch 21: reproducibility of the vertical flame aura

Eight random-seed calls repeated:

> fully contained vertical flame aura with a bottom energy ring

with `detail: low detail`, `image_size: 64x64`, `no_background: true`, no explicit view or outline,
and no prompt enhancement. All eight results passed the hard subject and view gates: no characters,
humanoid silhouettes, emblems, scenery, or fully top-down compositions appeared. Every result was
a contained upright flame mass connected to an elliptical lower ring. The family is visually much
simpler and more consistent than every earlier Pixen prompt family tested.

This is the most reproducible Pixen prompt so far, but it is not a finished modular aura. It solved
characters, view, containment, and noise, yet placed a flame element inside the ring. Several seeds
read as a campfire or narrow flame column rather than energy distributed around the ring's edge.
That center-subject composition fails the original Pro goal: the ring should organize the aura
around the future player position, not hold a standalone elemental object.

## Interim Pixen Recommendation After Batch 21

Closest baseline:

> fully contained vertical flame aura with a bottom energy ring

with Pixen `detail: low detail`, `64x64`, transparent background, no prompt enhancement, and no
explicit `view` or `outline`. It is a research baseline, not the final recommendation. Do not add
`character`, `sprite`, `VFX`, `backdrop`, `background`,
`empty`, or an explicit no-character clause; live tests showed those words increase characters,
scenery, portals, or emblems. Do not add `view: side` plus `outline: lineless`; that combination made
the successful water family more object-like.

Treat this as a stable flame-aura baseline, not proof that arbitrary theme substitution is safe.
Water is the best runner-up theme, but its tested success rate remained seed-dependent and its
outputs frequently became fountains, crowns, crystals, or ritual objects.

### Batch 22 direction: move energy from center to circumference

The next batch preserves the stable vertical-flame and low-detail signals but changes the spatial
relationship to the lower ring. It compares `along`, `around`, `surrounding`, `distributed around`,
`rim`, and `perimeter` wording. Acceptance now requires the vertical effect to originate around the
ring's circumference, especially its back and side arcs, without becoming a central flame subject,
portal wall, or fully top-down ring.

### Batch 22: circumference relationship wording

None of the eight variants fully passed. `along`, `rising along`, `rising around`, and `rim` still
placed one dominant flame in the center. `from the perimeter` became a campfire pile. `around the
perimeter` became a vertical portal ring. `surrounding` added some perimeter flames but retained a
large central flame.

`distributed around` was the only phrase that clearly moved the effect out of the center and onto
the lower ring's circumference. Its failure was discreteness: it produced several separate flame
objects rather than one continuous aura. This is useful causal evidence—distribution language
controls location, while the singular flame prior still controls objecthood.

Future batches are capped at three generations to limit cost. The next three prompts combine the
successful perimeter relationship with `continuous`, `all sides`, or `entire` to test whether Pixen
can join the distributed flames into one aura around the ring instead of a central object or a set
of separate flames.

### Batch 23: continuous/all-sides/entire wording

All three prompts failed identically: one narrow flame column occupied the center of a lower ring.
`continuous`, `rising from all sides`, and `rising along the entire` did not distribute the flame.
These phrases were weaker than the singular `vertical flame aura` prior and added no visible
perimeter coverage.

The next batch returns to the one proven location phrase, `distributed around`, but replaces the
singular flame subject with plural `flame wisps`. It tests `connected`, `spaced around`, and
`distributed along` variants. The goal is to retain the perimeter placement from Batch 22 while
reducing the appearance of independent flame objects.

### Batch 24: plural flame wisps

Plural/location wording controlled placement more reliably. `connected flame wisps distributed
around` produced separate blue flame droplets outside a small ring. `vertical flame wisps spaced
around` produced several orange flames on the ring and was the closest result, but each flame still
read as an independent object. `vertical flame aura distributed along` collapsed back into one
central flame.

The useful signal is now precise: plural `wisps` plus `spaced/distributed around` moves content onto
the circumference; singular `aura` pulls it back to the center. The remaining objecthood likely
comes from `flame`. The next batch preserves plural perimeter wisps but replaces flame with energy,
aura, or no material noun, testing whether the distributed marks can read as one surrounding field
instead of small elemental objects.

### Batch 25: non-flame perimeter wisps

This batch produced the first two results that satisfy the corrected composition. `vertical energy
wisps spaced around a bottom energy ring` created a low elliptical ring with irregular wisps rising
from its circumference; the center remained available for a separately composited player and no
single object dominated it. `vertical aura wisps distributed around a bottom energy ring` produced
the same spatial logic with shorter multicolored spikes around the rim. Both were contained,
non-top-down, subject-free, and materially simpler than the flame baseline.

`connected vertical wisps around` failed by turning the wisps into pearl-like nodes and a decorative
fan. `connected` is therefore rejected; it encourages literal linkage and ornament rather than a
continuous field.

The current best Pixen prompt candidate is:

> fully contained vertical energy wisps spaced around a bottom energy ring

The next three-call batch repeats that candidate twice and the aura-wisps runner-up once. This is a
limited-cost reproducibility check before promoting either wording.

### Batch 26: perimeter-wisp reproducibility

Both repeats of `vertical energy wisps spaced around a bottom energy ring` preserved the desired
layout: the wisps rose from the ring's circumference and left the center free of a dominant object.
One seed made the wisps somewhat rigid like narrow posts, but neither collapsed into a central
element, character, emblem, scene, or fully top-down effect. The `vertical aura wisps distributed
around` runner-up also reproduced successfully with a denser blue aura around the lower ring.

The successful Pixen wording and the proven Pro prompt share three anchors: `fully contained`, a
vertical upper effect, and `bottom energy ring`. Pro uses `symmetrical {{aura theme}} aura with
vertical power spikes`; Pixen currently succeeds by using plural `vertical energy wisps` and the
explicit spatial relationship `spaced around`.

The next three controlled hybrids test whether Pro's useful `symmetrical energy aura` prefix can be
restored without losing Pixen's perimeter placement. They compare: the full hybrid, the hybrid
without `symmetrical`, and perimeter wisps with `symmetrical` but without the singular `aura` noun.

### Batch 27: Pro/Pixen structural hybrids

All three hybrids failed. Restoring `energy aura`—with or without `symmetrical`—produced a large
central orb/emblem above a decorative base. Keeping `symmetrical` while removing `aura` produced a
central spear/portal-like form. The explicit `spaced around` phrase could not overcome those stronger
central-object priors.

For Pixen, Pro's `symmetrical` and singular `aura` language are not portable even though the
containment, vertical, and bottom-ring anchors are portable. The current best therefore remains:

> fully contained vertical energy wisps spaced around a bottom energy ring

The likely Pixen blueprint shape places the theme directly before plural `wisps`, not before
`energy aura`: `fully contained vertical {{aura theme}} wisps spaced around a bottom energy ring`.
The next three-call batch tests that shape with energy as control, then fire and water, to determine
whether theme substitution preserves perimeter placement.

### Batch 28: theme directly modifies wisps

All three themes preserved the corrected perimeter layout and avoided a central subject. Energy
produced several tall blue wisps around an elliptical ring and was a direct success. Fire produced
small discrete flames around the ring; water produced droplets/splashes around it. Those two were
spatially correct but still read as collections of elemental objects more than a unified aura.

This is nevertheless the first successful theme substitution test: changing the theme before
plural `wisps` changes material appearance without reverting to a central emblem, character, scene,
or fully top-down view. To make elemental variants more aura-like, the next batch inserts the stable
noun `energy` after the optional theme: default `energy wisps`, fire `fire energy wisps`, and water
`water energy wisps`. This also supports an empty-default blueprint variable without producing
`energy energy`.

### Batch 29: theme plus energy wisps

Adding `energy` changed the elemental results but did not solve continuity. The default energy
result formed many narrow vertical streaks around the ring and was spatially close, but still read
as separate spikes. Fire collapsed back into one central flame, while water produced repeated
wave-shaped curls around the ring.

The user's correction is decisive: `wisps` is a discrete plural noun, so even successful placement
naturally yields separate marks rather than a fully enclosed aura around the ring. It is rejected as
the final composition noun. The next batch retains the proven containment/vertical/lower-ring
anchors but tests continuous media—`energy field`, `energy curtain`, and `energy veil`—each
explicitly surrounding the ring.

### Batch 30: continuous media nouns

`Energy field`, `energy curtain`, and `energy veil` all failed. Field became an ornate vertical
portal/object; curtain became one narrow central beam inside a ring; veil became a dense scenic or
architectural column. These nouns imply a bounded surface or environmental layer, not the soft
continuous aura surrounding the ring.

### Online terminology research

Ragnarok Online sources describe the original level-99 aura as cyan energy **condensed around the
character**; later versions expanded it into a **spherical cloud**. The useful compositional terms
are therefore `condensed` and `cloud`, not spikes or discrete wisps. The player remains absent from
the generation prompt because it is composited separately. See the [Ragnarok Aura overview](https://ragnarok.fandom.com/wiki/Aura).

Contemporary game-VFX descriptions commonly separate the effect into a glowing circular zone below
the player plus rising energy. One asset description uses a ground circle, rising energy rings,
subtle particle emission, and a **continuous flow of energy** to communicate buffs and status
effects. The continuous-flow wording is more relevant than the asset's implementation details. See
[Energy Rings Effect](https://www.fab.com/listings/4eaf13b8-b476-422a-bc15-7a59accafd56).

Ragnarok customization communities use `aura style`, `effects surrounding your character`, and
ring-oriented names such as Flower Ring or Music Ring. This reinforces an attached perimeter effect
rather than a spell projectile or standalone element. See the [rAthena aura-style guide](https://rathena.org/board/topic/132752-guide-add-new-hateffect-aura-style/page/2/)
and [Ragnarok magic-aura discussion](https://forum.forsaken-ro.net/topic/31413-magic-auras/).

The next three source-derived prompts test `condensed aura cloud`, `continuous rising energy flow`,
and `continuous energy emission` around the proven bottom energy ring. They avoid player/character,
portal, backdrop, wall, curtain, veil, object, and discrete-wisp wording.

### Batch 31: source-derived cloud/flow/emission terminology

All three failed by creating a central subject. `Condensed aura cloud` became a jeweled cloud/tree
object; `continuous rising energy flow` became a narrow helix; `continuous energy emission` became
a central blue flame on a stone-like base. The online terms accurately describe completed game VFX
but are not sufficient Pixen prompt nouns: cloud, flow, and emission each became the thing depicted
inside the ring.

The useful part of the source language may be the relationship, not the nouns: energy is continuous,
rises, and surrounds the entire lower ring. The next batch removes cloud/flow/emission entirely and
tests the bare continuous predicates `glow rising`, `aura rising`, and `energy rising around an
entire bottom energy ring`. This is the smallest wording that directly states the desired enclosure
without introducing a new drawable subject.

### Batch 32: bare continuous predicates

`Continuous glow rising around an entire bottom energy ring` was the only prompt to distribute a
connected effect around the circumference. It left the center substantially open and avoided a
single central element, but the result was noisy and wreath-like. `Continuous aura rising` became a
central helix on a platform; `continuous energy rising` became one thin central beam.

This isolates `glow rising around an entire ... ring` as the useful relationship. `Aura` and
`energy` are stronger central-subject nouns in this construction, while `glow` can behave as a
property spread over the ring. The next batch keeps that exact relationship and tests whether
removing `continuous`, or adding only `simple` or `soft`, reduces the ornate wreath appearance while
preserving enclosure.

## Long-form Pixen prompt phase

The short-prompt search did not reliably control a specific standalone game effect. Pixen often
treated one strong noun as the subject and improvised an emblem, prop, portal, or environment around
it. For this aura target, longer prompts are justified when every clause fixes a visible spatial
relationship: shallow gameplay angle, elliptical footprint, energy around the perimeter, rear/side/
front depth, and a center reserved for later character compositing.

### Batch 33: explicit spatial anatomy

All three requests failed. They consistently produced polished circular objects viewed from above:
a decorated basin, a mechanical platform with a central crystal, and a metallic device. The terms
`anchors the player position`, `footprint`, `complete circumference`, and `compositing area` did not
make Pixen treat the image as an overlay; instead, the detailed ring anatomy strongly reinforced a
physical platform. Two results also inserted a central object. This prompt is consistent, but
consistently wrong: too much geometric ring specification converts the aura into a manufactured
object and pulls the camera toward full top-down.

### Batch 34: Ragnarok-style condensed cloud

All three requests failed more severely as compositable auras. Every result placed a dominant
subject in the center: an ornate fire emblem, a clustered orb/tree object, and a blue elemental
mass. `Condensed luminous energy cloud` behaved as a drawable central object, while `max-level` and
`classic Ragnarok-style` encouraged ornate rarity/status decoration. The prompt did produce some
rear/side/front layering, but around the unwanted subjects rather than around an empty player
position. Genre and prestige language adds detail and symbolism without solving the spatial target.

### Batch 35: production compositing vocabulary

All three requests became constructed platforms or arena-like objects. The center stayed relatively
available, but only because Pixen rendered it as a physical floor. `Overlay`, `ground-plane ellipse`,
`footprint`, `full boundary`, and explicit rear/side/front layering were interpreted as production
geometry rather than atmospheric energy. The repeated vertical marks also became fence posts or
pillars. This family is spatially consistent but unusable: technical compositing language does not
translate into the intended pixels and strengthens the top-down platform failure mode.

### Batch 36: continuous perimeter emission

All three requests failed, with high variation. Two became mostly top-down spell circles with a
single central peak; one generated a literal character despite the intended separately rendered
player. `Emission follows the ellipse's full perimeter` did not overcome Pixen's tendency to
collapse energy toward the center. Referring to the player—even only as a spatial position—is also
unsafe because Pixen may render that subject. This prompt neither preserved an empty center nor a
front/low-top-down aura silhouette.

### Batch 37: layered aura shell

All three requests generated characters or character-like central subjects inside oval capsules.
`Character aura layer`, `player position`, and `wraps around the complete footprint` made the
missing character salient enough for Pixen to supply it. The soft shell/glow wording also enclosed
the entire composition as a bubble rather than forming energy around a lower ring. This is the
clearest evidence in the long-prompt set that mentioning the eventual character—even to describe
compositing—must be avoided in the image description.

### Five-prompt comparison

Fifteen requests were run: three requests for each of five distinct long prompts. None met the full
target. Batch 33 was the most visually consistent but consistently produced top-down manufactured
platforms. Batch 35 was the runner-up only in the narrow sense that it usually kept the middle
available, but it also produced physical arena floors and fences. Batch 34 centered ornate elemental
objects, batch 36 centered spell emissions and once generated a character, and batch 37 generated
characters in every request.

Longer Pixen prompts improved repeatability but not semantic accuracy. The failed clauses cluster
into three causes:

- geometric/compositing terms (`footprint`, `ground-plane`, `boundary`, `overlay`) become platforms;
- character/player references cause a character to appear even when described as separate;
- atmospheric subject nouns (`cloud`, `shell`, `emission`) become a central object or enclosing
  capsule.

The strongest prior lead remains Batch 32's `glow rising around an entire bottom energy ring` and
the earlier plural-wisp layouts, not any of these five long prompts. A next iteration should be
medium-length: preserve `glow rising around` as the spatial relation, avoid every player/compositing
term, and describe the low viewing angle without detailed ring geometry.

### Reassessment of Batch 37

Batch 37 was visually the most promising long-prompt family despite failing the reusable-layer
constraint. Its character references did two things at once: they caused Pixen to draw a character,
but they also gave the surrounding glow a clear scale, upright orientation, and rear/side/front
relationship. The shell composition should therefore remain the branch under test. The next two
batches remove the character references while retaining its shallow angle, elliptical glow, upright
surrounding form, and asymmetric height from back to front.

### Batch 38: Batch 37 without character cues

All three requests failed. One became a decorated translucent dome, one became a tiny landscape
inside a capsule, and one became an oval artifact on a stand. Removing `character`, `player`, and
`footprint` did prevent literal people, but `upright aura shell` was no longer anchored to a status
effect and became a physical enclosing object. The useful composition from Batch 37 did not survive
simple deletion of its character cues.

### Batch 39: corona substitution

All three requests failed as reusable auras. They produced an upright portal, an ornate cylindrical
cage/platform, and a radiant mirror-like object. Replacing `shell` with `translucent corona` avoided
characters but strengthened the upright object/portal interpretation. The flat oval base survived,
yet the vertical energy stood on it as a separate object instead of wrapping naturally around it.

The combined result changes the earlier conclusion: character wording was not merely contamination
in Batch 37; it was the spatial anchor that made the energy read as an aura. Deleting it removes the
figure but also removes the aura relationship. `Shell` and `corona` cannot independently carry that
relationship in Pixen. The next useful experiment should not keep substituting aura nouns. It should
test a non-character scale anchor or an explicit empty status-effect slot while retaining Batch 37's
successful rear/side/front composition.

## User-supplied Pixen atlas attempts

Two additional `256x256` Pixen generations requested a complete `4x4` atlas in one call rather than
generating isolated `64x64` images. This changes the model context materially: Pixen sees a family
of related VFX cells and can repeat a shared visual grammar across the sheet.

### Packed 8x8 player-aura atlas

The `512x512` request produced sixty-four cleanly separated `64x64` cells, but almost every cell was
a fully top-down ring, radial icon, emblem, stone disc, or portal. The broad theme list changed color
and material while preserving the same incorrect icon grammar. Sheet size and repetition alone do
not create the desired low-angle aura; `circular and elliptical energy auras`, `centered`, and
`negative space` strongly reinforced top-down icon composition.

Evidence: [`player-auras-8x8-20260726`](../../pixellab-pip-generations/player-auras-8x8-20260726/).

### Side-scroller player-aura atlas

The strict side-view request generated a humanoid silhouette in nearly every cell, usually with an
effect wrapped around or attached to the body. Repeated `player`, `feet`, `body`, `humanoid`, and
`absent` wording made the excluded subject salient rather than reserving empty compositing space.
This is stronger evidence than the isolated tests that character vocabulary cannot be safely used
as a scale anchor in Pixen.

Evidence: [`player-auras-4x4-sidescroller-20260726`](../../pixellab-pip-generations/player-auras-4x4-sidescroller-20260726/).

### Low-detail player-aura atlas

The low-detail atlas is closer to the modular target than the later isolated-image batches. It
contains sixteen distinct transparent cells, no characters, and mostly shallow elliptical bases
with upright energy. Several cells approach the desired under/behind structure. Its systematic
failure is central placement: fire, ice, lightning, and other theme tokens usually become the main
element standing inside the ellipse rather than an aura distributed around its rim.

The likely useful drivers are the sheet-level `player aura VFX effects` context, repetition across
sixteen cells, `low detail`, and explicit shallow-camera description. The likely central-subject
driver is the long list of elemental themes: each theme becomes a drawable object or column. The
negative list also names many unwanted concepts, so it is not a clean causal control and should not
be carried into the next prompt.

### Clean high-detail player-aura atlas

The second atlas is a clear regression: almost every cell is a top-down icon, portal, solid disc,
platform, or ornate ring. It also fails its requested empty-center constraint. `Completely empty
transparent center`, `ground-hugging`, `smooth layered bands`, the long exclusion list, and `highly
detailed` collectively encourage bounded circular designs rather than an upright surrounding aura.

This is not a clean low-versus-high detail ablation because both the prompt and detail setting
changed. Still, it proves the complete high-detail recipe is unsuitable. It also confirms the
user's earlier correction that an empty center is the wrong target: it produces holes, discs, and
icon-like rings instead of natural aura energy behind the eventual sprite.

### New direction from the atlas comparison

The next prompt-only experiment should use one `256x256` atlas request, `low detail`, and the proven
Pro structural sentence, without an elemental theme list, character/absent-player language, empty-
center language, or a negative description. This tests whether sheet-level repetition supplies the
missing spatial anchor while the Pro wording supplies the ring-plus-upright-aura structure.

A separate, higher-confidence pipeline experiment is to preserve the useful character-anchored
composition from Batch 37 and remove only the generated figure with a PixelLab mask edit. That is
not a pure Pixen text-to-image solution, but it directly separates two tasks Pixen has struggled to
satisfy simultaneously: arranging an aura around a body-sized volume and delivering the aura alone.

### Batch 40: Pro structure inside a low-detail Pixen atlas

Three random requests used one `256x256` Pixen atlas prompt built from the successful Pro structural
sentence. One of the three sheets is the closest Pixen result found in the entire search. All sixteen
cells are character-free, scene-free, low-angle, and modular. Each uses an elliptical lower ring
with contained vertical spikes distributed around it; there is no dominant object occupying the
center. The expected `64x64` grid inspection also shows that the effects remain inside their cells.

The other two sheets failed in different ways: one produced narrow beams, platforms, and pedestal
objects; the other produced ornate repeated ring objects with central flames or crystals. The
prompt therefore has a strong successful mode but is seed-sensitive, approximately one successful
sheet in three in this small sample.

This is the first evidence that the Pro sentence transfers successfully to Pixen when it is framed
as a repeated atlas rather than sixteen isolated requests. Sheet-level repetition supplies the
missing structural prior: once Pixen chooses the correct interpretation, it repeats that grammar
consistently across all cells.

### Batch 41: continuous perimeter atlas

The continuous-atlas alternative failed all three requests. One sheet produced upright rectangular
light columns on oval bases, one produced circular portal/platform objects, and one produced cage-
like rectangular frames around small bases. The explicit rear/side/front perimeter prose again
encouraged constructed enclosures rather than organic aura forms.

The result rejects the continuous-description family and elevates Batch 40's exact structural
wording as the Pixen recommendation. Do not replace `vertical power spikes and a bottom energy ring`
with geometric perimeter anatomy. For Pixen, request a full low-detail atlas and review/retry the
whole sheet when it lands in the wrong compositional mode. The character-removal pipeline was not
run in this round because Batch 40 produced a direct, character-free text-to-image success and the
edit would no longer target the active blocker.

### Batch 42: high-detail structural atlas

Three requests repeated Batch 40's exact prompt and changed only Pixen's `detail` field from `low
detail` to `highly detailed`. This clean ablation produced one strong high-quality sheet, one
borderline sheet, and one ornate failure.

The strongest sheet contains roughly twelve useful cells with crisp elliptical rings and tall thin
spikes distributed around them. Four cells collapse into fully top-down radial discs, so the sheet
is not uniformly valid, but its successful cells are materially more polished than Batch 40's
low-detail winner. The borderline sheet preserves upright ring-and-column compositions throughout
but often reads as glowing pedestals. The failed sheet contains ornate emblems and central objects.

High detail therefore does not destroy the structural prompt, but it increases both polish and
ornament risk. The same atlas-level wording remains the best prompt family; production should treat
the returned sheet as candidates rather than expecting all sixteen cells to pass.

### Batch 43: high-detail continuous atlas

All three requests failed consistently. They produced repeated stone or metallic platforms with
upright rectangular pillars, arches, and cage-like light walls. Increasing detail made Batch 41's
constructed-enclosure interpretation stronger and more uniform rather than more aura-like.

This confirms that quality was not the main blocker in the continuous prompt. Its geometric
`perimeter`, rear/side/front, and integrated-base description defines an architectural object for
Pixen. The continuous family should be retired at both detail levels.

## Continuation Checkpoint

This section is the restart point for future work.

### Production decision

Use Create Image Pro, not Pixen, for modular character-aura candidates. Pro reliably returns a
reviewable candidate set at `64x64`; Pixen returns only one generated image per call and never found
a prompt/control combination that reliably satisfied composition, modularity, subject exclusion,
view, and quality together. After forty-three numbered Pixen batches plus the user-supplied atlas
experiments, further Pixen prompt-only synonym search is not justified without a new model control,
reference mechanism, or generation strategy.

This is an evidence-based production decision, not a claim that Pixen can never emit a good cell.
Batch 40 request 2 produced sixteen simple modular ring-and-spike effects, and Batch 42 request 2
produced roughly twelve polished useful cells. Both were surrounded by failed repetitions using the
same prompt, so neither establishes a reliable workflow.

### Pro prompt hierarchy

1. Immersive default:

   > fully contained symmetrical energy aura with vertical power spikes and a bottom energy ring

   This is the most reliable complete composition. Energy occupies the rear, sides, and front of
   the ring, creating surrounding depth. Use an unseeded call and review the returned candidates.

2. Layering-safe runner-up:

   > fully contained symmetrical energy aura with vertical power spikes and an energy ring at the base

   Its fuller Ragnarok-like ring is aesthetically strong, but most vertical energy sits behind the
   ring. It is flatter and less immersive while reducing foreground overlap.

3. Pre-ring structural baseline:

   > fully contained symmetrical energy aura with vertical power spikes

   This reliably establishes upright containment but leaves an unnatural triangular termination at
   the bottom.

The current blueprint generalizes only the theme token:

> fully contained symmetrical {{aura theme | default: energy}} aura with vertical power spikes and a bottom energy ring

A comma-separated or multiword theme is one literal value and one Pro call. Candidate count comes
from the resolved size and response; it is never inferred from the number of supplied theme words.

### Pro controls and seed findings

- Default route: `POST /v2/generate-image-v2`, `64x64`, transparent background, no style or subject
  reference, prompt enhancement omitted, seed omitted.
- At `64x64`, Pro returned sixteen candidates and reported twenty generations per tested call.
- Seed `1379246801` repeatedly drove central objects and emblems across nearby prompts. Do not reuse
  it for this family.
- Seed `2057719043` produced favorable ring batches but later still showed motifs; retain it only as
  a historical comparison seed, not a production guarantee.
- Resolved seed `1734275022` produced the cleanest unseeded validation: sixteen front-facing ring
  auras without discrete central objects. Production should still omit the seed because seed quality
  did not generalize.
- Same-seed comparisons proved that prompt vocabulary matters in addition to RNG: `bottom energy
  field` retained central-object drift under a seed that worked for `bottom energy ring`.

### Locked phrase findings

- Keep `fully contained`; it is the strongest positive top/side containment cue.
- Keep the word order `energy aura with vertical power spikes`. Moving `vertical` onto `energy aura`
  allowed radial and top-down results.
- Keep `bottom energy ring`; `field`, `glow`, and `circle` collapse toward central assets or top-down
  disks, while `aura ring` weakens the lower scaffold.
- Do not require an empty or hollow center. The aura naturally exists behind the future sprite;
  explicit holes encourage portals, disks, icons, and top-down negative space.
- Do not use `grounded base`, `flat`, `wide`, or `surrounding` to refine the lower feature. They
  encouraged hard platforms, central objects, or volumetric constructed rings.
- `filled`, `complete`, and `continuous` did not reliably make the lower ring fuller.
- Broad replacements for `vertical power spikes` increased thematic variety but lost aura identity
  and produced trees, crystals, machinery, fountains, wings, pillars, and portals.
- Bottom-edge contact by the energy ring is acceptable; top/side bleed or spike contact is not.

### Pixen findings to retain

- Short prompts were highly stochastic and commonly produced characters, scenes, emblems, portals,
  central elemental objects, or fully top-down effects.
- Long prompts improved repetition but over-specified physical geometry: footprint/boundary/overlay
  language became platforms; shell/corona/cloud/emission became capsules, portals, or center objects.
- Character/player wording sometimes supplied useful aura scale and depth but also caused literal
  characters. Removing it removed both the character and the useful spatial anchor.
- Explicit `view` and `outline` controls were weak guidance and did not rescue an incorrect prompt
  family. Low detail reduced ornament; high detail improved polish while increasing emblems,
  platforms, and top-down radial failures.
- Elemental themes acted as morphology priors rather than safe palette substitutions. Water, wind,
  and lightning occasionally organized vertical effects; fire was the most reproducible upright
  family but became a central flame or campfire rather than a perimeter aura.
- A full `4x4` atlas gave Pixen a stronger repeated VFX grammar than isolated `64x64` calls. The Pro
  structural sentence was the only atlas prompt to produce a full directly useful sheet, and it did
  so in only one of three low-detail calls. High detail produced one partially useful sheet in three.
- The continuous-perimeter atlas wording failed at both detail levels and should remain retired.

### Animation caution

The static Pro candidate sheet is reliable; V3 whole-sheet animation is not. V3 treats the sheet as
one canvas, so text cannot guarantee cell isolation. Spike motion crossed boundaries, center glow
was invented, selective/layered motion left seams or frozen regions, and some candidates drifted or
bobbed. Separate per-cell animation worked technically but did not satisfy the requested one-job
sheet workflow. The blueprint's current low-invention flicker/pulse action is the least aggressive
tested wording, not a proven visual solution. Always report technical frame validity separately from
visual acceptability.

## Next Pro Static-Aura Test Plan

The next phase returns to Create Image Pro and tests static images only. Animation is out of scope
until a static prompt family is reliable.

### Why one universal prompt is the wrong target

The current blueprint hard-codes one successful morphology:

> fully contained symmetrical {{aura theme | default: energy}} aura with vertical power spikes and a bottom energy ring

`Vertical power spikes` is doing two jobs: it establishes an upright, gameplay-facing silhouette and
it dictates a narrow flame/crystal/lightning-like shape language. Removing it without replacing its
orientation role caused central objects, top-down disks, and lost aura identity in earlier tests.

The desired expansion also contains three incompatible compositing contracts:

1. **Rear-wall aura:** upright energy sits behind and around the future character. Its center may
   contain natural aura energy; a forced hole is undesirable.
2. **Ground-only aura:** a ring, circle, or textured status effect lies on the ground. It has no
   upright wall or emitted spikes.
3. **Foreground-overlay aura:** a thick power-up border renders in front of the character while its
   center stays transparent so the character remains visible.

A single loose phrase cannot state all three without contradiction. The research target is one
reliable minimal prompt per family, followed later by one blueprint mode selector that resolves to
the tested full prompt. The theme remains a separate literal scalar. Do not change the production
blueprint until a new prompt survives an unseeded repeat.

### Terminology taken from external references

- Pixel-art aura packs describe status effects as appearing **around or under units**, using glowing
  circles, pulsing energy, or animated elements. That supports separating upright/around effects
  from ground-only effects instead of treating them as one prompt family. See [Aura - Effect Pixel
  Art](https://sanctumpixel.itch.io/aura-effect-pixel-art).
- Effekseer treats a ring as its own circular renderer with independently shaped inner and outer
  rings. Applying an image to the ring is specifically presented as useful for shock waves and
  auras. This supports testing `textured energy ring` as a ground-only noun rather than adding
  `filled`, `wide`, or `flat`, which failed in Pro. See [Effekseer circular-particle
  tutorial](https://effekseer.github.io/Help_Tool/en/ToolTutorial/06.html).
- Ragnarok Online describes its classic aura as energy condensed around the character. This is a
  useful reminder that an aura does not require tall spikes or a violent emission. See the
  [Ragnarok Aura overview](https://ragnarok.fandom.com/wiki/Aura).
- The supplied [RPG Maker MV Super Warrior
  Aura](https://manugamingcreations.itch.io/rpg-maker-mv-super-warrior-aura-loop) and [RPG Maker MZ
  Effekseer version](https://manugamingcreations.itch.io/rpg-maker-mz-effekseer-animation-super-warrior-aura-loop)
  are marketed as looping visual-state effects. Visual inspection shows a distinct foreground
  contract: a thick teardrop/capsule-shaped luminous border, an open center that reveals the
  character, and a strong lower-front flare. This is not the same composition as the current
  rear-wall ring aura.

These sources provide vocabulary and composition hypotheses, not prompt guarantees. Earlier Pixen
research showed that production terminology can turn into literal objects; every term below must be
validated visually in Pro.

### Fixed test controls

Use these controls for every discovery call so prompt wording remains the principal variable:

| Field | Test value |
|---|---|
| Route | `POST /v2/generate-image-v2` |
| Size | `64x64` |
| Background | `no_background: true` |
| Theme | `energy` during structural discovery |
| Seed | omitted |
| Style/reference images | none |
| Prompt enhancement | none |
| Expected response | sixteen native-size candidates; verify the actual response |
| Observed usage baseline | twenty generations per call |

Do not seed-lock the broad discovery prompts. Seed had a large effect in the prior Pro tests, so a
prompt must work across fresh random seeds rather than win only a same-seed comparison. Use a
same-seed A/B only later to attribute one narrow wording change after a viable family exists.

Do not add a long negative clause. Pro has no `negative_description` field, and inline exclusions
previously leaked unwanted `object`, `emblem`, `character`, and `empty-center` concepts into the
composition. The foreground family is the one exception in intent: transparent central space is a
required positive part of that asset, so it must be stated and its portal risk measured.

### Discovery matrix

Run the two primary prompts in each family first. They are intentionally different semantic tests,
not minor synonym variations. Run the fallback only when both primary prompts fail that family.

#### A. Rear-wall aura

The test must preserve the current prompt's orientation and ring anchor while removing its spike
morphology.

| ID | Prompt | What it isolates | Principal risk |
|---|---|---|---|
| `RW-A` | `fully contained symmetrical energy aura rising around a bottom energy ring` | A spatial relationship replaces the spike noun while retaining upright distribution around the ring. | `rising` may still bias flame-like motion or concentrate energy in the center. |
| `RW-B` | `fully contained symmetrical upright energy aura with a bottom energy ring` | `upright` supplies orientation without prescribing spikes, wisps, flames, or particles. | The unconstrained aura may become an emblem, column, or top-down ring. |
| `RW-C` fallback | `fully contained symmetrical energy aura as an upright backdrop above a bottom energy ring` | Explicitly tests a rear-wall/depth category rather than a morphology. | `backdrop` may become a scene panel or detach the ring from the aura. |

The existing `vertical power spikes` prompt is the historical control and does not require another
paid call in discovery. A new rear-wall prompt must beat its rigidity without losing its reliability.

#### B. Ground-only aura

The desired result is a simple ring, circle, or textured status layer on the ground, closer to the
foot-focused readability associated with Ragnarok-style auras. Upright emissions are a failure in
this family.

| ID | Prompt | What it isolates | Principal risk |
|---|---|---|---|
| `GR-A` | `fully contained energy ground aura ring` | The shortest direct category test: ground aura plus ring, without spike or emission language. | It may become a hard platform or a thin empty outline. |
| `GR-B` | `fully contained textured energy ring in low top-down view` | Effekseer-derived textured-ring language tests visual richness without `filled`, `wide`, or `flat`. | Texture may become material, runes, or a discrete object. |
| `GR-C` fallback | `fully contained circular energy status aura on the ground plane` | Status-effect vocabulary tests whether Pro produces a readable gameplay indicator rather than an object. | `circular` and `ground plane` may create an AoE disk, emblem, or environment patch. |

Fully top-down presentation is valid here, unlike the rear-wall family. The result still fails when
it becomes a physical platform, portal, emblem, scenery patch, or discrete object in the center.

#### C. Foreground-overlay power-up aura

This family targets the supplied Super Warrior reference: a luminous foreground border around
transparent character space. It deliberately reverses the prior rule against empty centers, but
only for this mode.

| ID | Prompt | What it isolates | Principal risk |
|---|---|---|---|
| `FO-A` | `fully contained symmetrical energy power-up aura outline with a transparent center` | Functional power-up vocabulary plus an outline tests the simplest foreground shell. | `power-up` may imply a fighter silhouette; `transparent center` may become a portal. |
| `FO-B` | `fully contained symmetrical teardrop energy aura border around transparent space` | The reference's visible silhouette is specified without mentioning a player or character. | `teardrop` may become a gem, shield, or rigid frame. |
| `FO-C` fallback | `fully contained symmetrical foreground energy aura shell with an open center` | Compositing/depth vocabulary tests a layer intended to sit above the character. | `foreground`, `shell`, and `open center` may create a capsule, doorway, or scene. |

Do not mention `fighter`, `player`, `body`, `character`, or `silhouette` in the PixelLab description.
Those words supplied useful scale in Pixen but repeatedly generated the forbidden subject. Judge
the open center from alpha and visual structure rather than prompting for a missing person.

### Candidate scoring

Score every returned candidate individually before comparing prompts. A candidate passes the global
gate only when it is:

- a valid transparent `64x64` image;
- an isolated aura asset rather than a character, scene, platform, emblem, portal, or central object;
- contained at the top and sides, with bottom contact accepted only when it belongs to the intended
  lower ring or ground effect;
- free of text and label-like marks; and
- visually readable as a modular game effect at native size.

Then apply the family gate:

| Family | Required composition |
|---|---|
| Rear wall | Upright front/low-top-down presentation; energy occupies the rear and may continue along the sides or as restrained front accents; the center is natural aura, not a forced hole. |
| Ground only | All meaningful effect structure lies on the ground plane; the center may be transparent or effect-textured but contains no discrete object; no upright wall, column, or emitted spikes. |
| Foreground overlay | A continuous luminous border surrounds visibly transparent central space; a lower-front flare or arc is allowed; the border reads as energy rather than a rigid frame or portal. |

Use these prompt-level thresholds:

- **Promising:** at least `8/16` candidates pass the family gate and the failures are varied rather
  than one systematic wrong interpretation.
- **Blueprint-worthy:** at least `12/16` candidates pass on each of two independent unseeded calls,
  with no recurring character generation and no dominant scene/platform/portal failure.
- **Flexible:** after reliability passes, a broad theme stress call preserves the family contract in
  at least `8/16` candidates and produces at least three materially different effect morphologies.

Pixel hashes, dimensions, and transparency do not establish composition. The numbered review sheet
and human visual scoring remain authoritative.

### Staged call and generation budget

At `64x64`, the prior observed cost was twenty generations and sixteen candidates per Pro call.
Keep every stage behind its own approval gate and stop early when evidence resolves the question.

| Stage | Calls | Generation budget | Purpose and stop rule |
|---|---:|---:|---|
| Existing control review | `0` | `0` | Reuse the documented current-best Pro sheets; do not pay to rediscover the spike baseline. |
| Primary discovery | `6` | `120` | Run `A` and `B` for all three families. Stop a family if neither is promising until its fallback is approved. |
| Conditional fallbacks | `0-3` | `0-60` | Run only `C` for families whose two primary prompts failed. Do not add more coarse synonyms after this. |
| Reliability repeats | `0-3` | `0-60` | Repeat the best prompt once, unseeded, for each promising family. Drop any family that cannot reproduce. |
| Theme-flexibility stress | `0-3` | `0-60` | One call per reproducible family using a diverse literal theme phrase. Do not require one-to-one theme assignment. |

The initial commitment is therefore **six calls / 120 generations / 96 candidates**. The maximum
pre-refinement search is **fifteen calls / 300 generations**, reached only if every fallback and
every family remains viable. Using the historical approximately `$0.095` Pro call estimate, those
two bounds are roughly `$0.57` and `$1.43`; verify current pricing and balance before execution.

For the theme-flexibility call, replace only `energy` with this one literal scalar:

> fire, water, lightning, nature, bone, ghost, smoke, and sand

This deliberately spans emissive, fluid, electric, organic, rigid, intangible, gaseous, and granular
shape priors. It is not a request to assign one named theme to each candidate. The question is
whether the chosen structural sentence permits varied morphology without collapsing into objects or
losing its family composition.

### Refinement rule after discovery

Do not pre-plan a cloud of minor variants. After review, identify the single dominant failure of a
promising prompt and change one phrase that directly targets it. Examples:

- rear wall too flat: change only the depth relation, not the theme and ring noun together;
- ground ring too thin: test one texture/band noun, not `filled`, `wide`, and `flat` together;
- foreground border becomes a portal: change only the border/shell noun while keeping the open-center
  requirement and silhouette geometry fixed.

Budget at most **two refinement calls per surviving family**: one single-change candidate and one
unseeded reproduction if it wins. This optional refinement budget is separate from the fifteen-call
discovery/reliability ceiling and requires a new approval.

### Blueprint decision after testing

Keep the current `vertical power spikes` prompt as the production default until another rear-wall
prompt reaches the blueprint-worthy threshold. Ground-only and foreground-overlay prompts should not
replace it; they are additional aura modes.

If all three families succeed, keep one portable blueprint but resolve an `aura mode` such as
`rear wall`, `ground ring`, or `foreground overlay` to one of three tested full descriptions. Keep
`aura theme` and `aura size` independent. Do not expose a free-form `effect shape` fragment in the
middle of one universal sentence: that would restore the ambiguity this test plan is designed to
remove.
