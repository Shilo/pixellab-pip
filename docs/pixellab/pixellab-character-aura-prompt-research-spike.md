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
spikes` and makes only the spike theme configurable. This preserves the strongest known composition
constraint while allowing elemental and non-elemental variation.

### Configurable Blueprint Decision

Bundled blueprint: [`aura.blueprint.json`](../../skills/pixellab-pip/blueprints/aura.blueprint.json)

```text
fully contained symmetrical energy aura with vertical {{power spike theme | default: ""}} power spikes and a bottom energy ring
```

`Power spike theme` is preferred over `elements`. It is singular, precisely scopes the value to the
emitted spikes, and accepts broader concepts such as `fire`, `lightning`, `shadow`, `floral`, or
`cosmic`. Calling the variable `element` would imply a narrower classical-element vocabulary;
calling it only `effect` would be too ambiguous about which part of the composition changes.

The canonical empty default is `{{power spike theme | default: ""}}`. The proposed `{elements : }`
form is not Pip blueprint syntax and cannot be relied on for portable replay. With no supplied value,
literal substitution produces two adjacent spaces between `vertical` and `power`; with `fire`, it
produces `vertical fire power spikes`. The extra whitespace is a presentational blemish rather than a
prompt concept. The current blueprint grammar has no conditional-space operator, and adding one only
for this sentence would make the recipe more complex and less portable than leaving the benign space.

The blank default also does not create thematic variety by itself. It deliberately reproduces the
current best neutral prompt. A caller must supply a theme to move the spikes away from the baseline
raw-energy tendency, and each new theme remains subject to full-batch candidate review because it
may introduce its own object or material prior.

The blueprint accepts a configurable `aura size`, defaulting to `64x64`. Candidate count is derived
from the completed Pro response because changing native size changes how many images the route may
return. All returned candidates are preserved and assembled into a compact review sheet without
assuming sixteen images or a four-by-four layout.

Animation is a separately approved optional branch implemented by the bundled
[`aura-animation.blueprint.json`](../../skills/pixellab-pip/blueprints/aura-animation.blueprint.json).
Keeping it separate avoids pretending that a sequential blueprint can conditionally skip a paid
`POST`. After the static sheet is presented, the agent asks whether to run one additional
`animate-with-text-v3` job and explains that V3 treats the sheet as one canvas, applying simultaneous
motion across its cells rather than producing an independent animation sequence per candidate. The
theme-neutral action is:

```text
all aura effects animate in place within their original cells, preserving the spritesheet layout and transparent background
```

This wording avoids assuming fire, lightning, or another specific motion family. It is intentionally
broad about motion but strict about cell containment and layout. The companion uses eight generated
frames because a 256x256 sheet reaches V3's documented `width × height × frame_count ≤ 524288`
budget at that count.

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
