# PixelLab 32px VFX Atlas Density Spike

Last reviewed: 2026-07-10.

Purpose: record live `generate-image-v2` findings for strict `32x32` transparent explosion VFX atlases, explain why a `512x512` one-shot request produced larger cells, and identify better experiments. This is developer research, not the canonical runtime contract.

## Bottom Line

Text-only Create Image Pro did not produce a valid one-shot `16x16` atlas of `256` transparent `32x32` explosion effects in four controlled attempts. The original prompt and two optimized variants produced approximately `10x10` layouts; a semantic row/column matrix improved density to approximately `12x12`, but still exceeded the requested cell size and drifted toward generic geometric symbols.

The evidence does **not** support a general claim that non-tile or non-UI sheets cannot hold a proper grid. Existing showcases contain successful one-shot `8x8` sheets of transparent `32x32` item icons and opaque `32x32` skill icons. The unvalidated boundary is the much denser one-shot request: `256` recognizable transparent effects in one `512x512` image.

For an exact `512x512` deliverable, native `32x32` PixelLab images solve cell dimensions, but a follow-up experiment showed that one prompt's 64 outputs can repeat one dominant composition or inherit caption-like text from a long named catalog. Native-size generation therefore needs semantic-diversity, no-label, and view verification before assembly. Four independently planned `8x8` sheets remain the strongest whole-sheet alternative.

## Related Evidence

- [`pixellab-16px-item-sprite-generation-spike.md`](pixellab-16px-item-sprite-generation-spike.md) found that semantic objects tend to drift toward larger readable scales while full-cell textures tolerate denser grids.
- [`../showcase/item-icons.md`](../showcase/item-icons.md) documents successful transparent `8x8` sheets of `32x32` inventory objects.
- [`../showcase/skill-icons.md`](../showcase/skill-icons.md) documents successful opaque `8x8` sheets of `32x32` skill effects.
- [`../showcase/tiles.md`](../showcase/tiles.md) includes one mechanically useful `16x16` full-cell texture atlas, but also records rejected full-atlas attempts whose texture detail crossed cell boundaries.

Together, these results show that subject type matters, but it interacts with density, transparency, visual complexity, and semantic count. Tiles are not universally reliable, and non-tile sheets are not universally unreliable.

## Experiment Setup

All three comparison jobs used the same controls so prompt wording was the main changed variable:

| Field | Value |
|---|---|
| Route | `POST /v2/generate-image-v2` |
| Image size | `512x512` |
| Background | `no_background: true` |
| Seed | `32003216` |
| Reference images | omitted |
| Style image/options | omitted |
| Requested structure | `16x16`, `256` effects, `32x32` cells |
| Observed usage | `$0.185` per call; `$0.555` total |

The generated files remain in the local `pixellab-pip-generations/explosion-atlas-prompt-test/` run folder. They are failed research outputs, not showcase assets.

## Baseline Failure

The original one-shot prompt asked for a strict `16x16` atlas, named sixteen broad effect families, requested many combinations, and said to vary silhouette, scale, timing impression, flame shape, smoke shape, debris, highlights, and palette.

Observed result:

- Approximately `10x10`, or about `51px` pitch.
- Visually strong explosion sprites, but only about `100` visible effects.
- The first visible effect exceeded a `32x32` intended cell.

The phrase `vary scale` directly conflicted with uniform `32x32` containment. `Timing impression` and the long list of visual dimensions also rewarded detail and recognizability over density. Only sixteen semantic families were provided for a request requiring 256 unique results.

## Three-Prompt Comparison

### A. Semantic Matrix

Prompt strategy:

- Define sixteen energy-family rows.
- Define sixteen silhouette columns.
- Use each row/column combination once.
- Limit each visible effect to a centered `24x24` footprint.
- Require consistent apparent scale and low visual noise.

Observed result:

| Check | Observation |
|---|---|
| Canvas | `512x512`, passed |
| Transparency | present, passed |
| Estimated pitch | about `43x42px` |
| Observed grid | approximately `12x12` |
| First visible bounds | `(3,3)-(38,38)`, about `35x35px` |
| Requested `16x16` / `32x32` | failed |

The matrix materially increased density from roughly 100 to roughly 144 visible regions. It also made rows and columns more systematic. However, many columns became triangles, pillars, rings, or simple orbs rather than convincing explosion VFX. Semantic matrix wording is therefore useful for count and organization, but an overly abstract shape taxonomy can weaken the target asset identity.

### B. Independent Sprite Files

Prompt strategy:

- Describe 256 independent sprite files packed row-major.
- Define fixed `32x32` regions and a `24x24` visible bound.
- Emphasize single-frame detonations and prohibit scale changes.

Observed result:

| Check | Observation |
|---|---|
| Canvas | `512x512`, passed |
| Transparency | present, passed |
| Estimated pitch | about `51x51px` |
| Observed grid | approximately `10x10` |
| First visible bounds | `(5,5)-(48,46)`, about `43x41px` |
| Requested `16x16` / `32x32` | failed |

The `independent sprite files` framing produced strong explosion art but did not improve density over the baseline. File-oriented wording is not structural enforcement.

### C. Technical Game-Engine Atlas

Prompt strategy:

- Frame the output as fixed game-engine cell coordinates rather than an illustration or contact sheet.
- Require four transparent pixels of clearance from every cell edge.
- Use simple shapes, limited detail, and uniform density.

Observed result:

| Check | Observation |
|---|---|
| Canvas | `512x512`, passed |
| Transparency | present, passed |
| Estimated pitch | about `51x51px` |
| Observed grid | approximately `10x10` |
| First visible bounds | `(4,6)-(47,47)`, about `43x41px` |
| Requested `16x16` / `32x32` | failed |

Technical atlas terminology and explicit clearance did not override the larger VFX composition prior. This prompt behaved almost identically to the independent-file prompt.

## What The Comparison Isolates

### Supported Findings

1. **Prompt wording can influence density, but did not enforce it.** The semantic matrix improved the layout from approximately `10x10` to `12x12`; the other framings did not.
2. **The model favored readable effects around a `42-51px` pitch.** All outputs used substantially larger regions than requested despite exact canvas and cell arithmetic.
3. **Transparent VFX are semantic objects, not full-cell textures.** Their glow, debris, smoke, rings, and negative space create pressure for a larger readable footprint.
4. **A `24x24` textual bound is not structural.** The model ignored the requested inner footprint in every trial.
5. **A one-shot request for 256 unique semantic effects is under-specified and overloaded.** The baseline named only sixteen families; the matrix supplied combinatorial structure but lost explosion specificity.

### Findings Not Established

- There is no evidence that `10x10` is a fixed PixelLab maximum or default. It is only the repeated result for these related prompts.
- There is no evidence that every non-tile `16x16` grid will fail.
- Canvas size alone is not the cause: successful `512x512` `8x8` item sheets exist.
- Transparency alone is not the cause: successful transparent `8x8` `32px` item sheets exist.
- Tiles are not guaranteed to succeed: full-atlas tile attempts have also crossed intended cells.

## Likely Failure Mechanism

The most plausible explanation is semantic scale selection. A `512px` canvas divided into ten regions provides about `51px` per effect, near the common readable scale for detailed item and ability artwork. PixelLab appears to have sacrificed requested count to preserve recognizable explosions. The matrix reduced that pressure by giving the model repeated row/column structure, but the resulting geometric simplification still stopped around a `42-43px` pitch.

This remains a hypothesis. A controlled size/count ladder is needed to identify the point where layout reliability drops.

## Better Next Experiments

### 1. Native `32x32` Outputs, Then Assemble

Generate at `image_size: 32x32` so every returned image is structurally the requested cell size. Plan four distinct 64-effect semantic batches, reject duplicates or off-target outputs, then assemble 256 PixelLab-origin PNGs into a `16x16` atlas without resizing.

Why this is strongest:

- Cell dimensions are enforced by the returned file, not inferred from a prompt.
- Local assembly gives exact `512x512` structure.
- Failed or duplicate effects can be rejected individually.

Risks:

- Cross-batch style drift.
- Repeated semantics among alternatives.
- Higher review and generation cost.

### 2. Four Proven-Density `8x8` Sheets

Generate four `256x256` sheets of `64` transparent `32x32` effects, each with a disjoint theme and concept list, then assemble them as four quadrants.

Suggested batches:

1. Fire, smoke, dust, debris.
2. Ice, water, steam, wind.
3. Lightning, plasma, arcane, solar.
4. Toxic, acid, holy, void/shadow.

This keeps the validated `8x8` non-tile density while preserving more within-sheet style consistency than separate-image generation.

### 3. Controlled Density Ladder

Hold the prompt family and seed constant while testing:

- `8x8` at `256x256` (`32px` cells).
- `10x10` at `320x320` (`32px` cells).
- `12x12` at `384x384` (`32px` cells).
- `14x14` at `448x448` (`32px` cells).
- `16x16` at `512x512` (`32px` cells).

This would test whether the model follows lower requested counts and reveal the transition where it begins choosing a larger visual pitch. It is more informative than three more `16x16` wording variants.

### 4. Explosion-Specific Matrix

Keep the useful row/column structure but replace abstract geometry labels such as `triangle`, `pillar`, or `orb` with explosion-native distinctions:

- Core behavior: flash, fireball, pressure bloom, implosion, ground burst, air burst, delayed secondary burst, fragmentation.
- Particle behavior: sparks, embers, smoke lobes, shards, droplets, rubble, arcs, wisps.

This may retain matrix density without turning rows into generic symbols.

### 5. One Approved Style Anchor

Use one or a few approved individual VFX sprites as limited style/reference inputs for later native-size batches. Avoid a complete finished atlas as the style image: earlier item research found that full-atlas references can copy identities, row order, and silhouettes too closely.

Verify both style consistency and source copying. A style anchor should influence palette, outline, shading, and particle treatment—not reproduce the same effect.

### 6. Neutral Layout Reference

Test a locally authored neutral shape/layout guide through `reference_images`, with no finished art identities to copy. The guide could demonstrate cell centers and maximum occupancy without serving as a complete style target.

Risks:

- The generated output may bake in guide marks.
- The route may still ignore the intended density.
- A guide strong enough to enforce layout may over-constrain composition.

Keep this experimental and reject outputs with visible guide artifacts.

### 7. Structured UI Route As A Negative-Control Experiment

`create-ui-asset` can describe explicit pieces, so it could test whether structured placement enforces 256 regions. Existing skill-icon research found that UI routes tend to create buttons, frames, and slots, making this unlikely to produce reusable transparent VFX. Treat it as a diagnostic experiment, not the recommended production route.

### 8. Separate Static Variations From Animation Frames

Avoid phrases such as `timing impression` when the request is for independent static effects. If the desired atlas actually represents explosion animation stages, route it as animation and preserve frame order instead of asking an image model to infer timing inside a variation sheet.

## Prompt Guidance From This Spike

For strict transparent VFX sheets:

- Use one consistent apparent scale; never ask to vary scale.
- State whether the cells are independent variations or ordered animation frames.
- Use explosion-native variation categories rather than generic geometric symbols.
- Keep the concept count proportional to the tested sheet density.
- Prefer `8x8` whole-sheet requests until a denser non-tile layout is validated.
- Treat `32x32`, inner footprint sizes, grid counts, file wording, and game-engine terminology as prompt guidance—not structural guarantees.
- Verify the first visible effect and observed grid before crop, hash, uniqueness, or packaging checks.

## Native 32px Follow-Up

Three approved `image_size: 32x32`, `no_background: true` calls each returned 64 separate images. All 192 source files had native dimensions and transparency, and all three locally assembled `8x8` atlases round-tripped every RGBA crop exactly. Geometry succeeded; content-set behavior exposed three different prompt risks.

### Long Explicit Catalog

One description requested 64 unique effects and supplied a semicolon-separated list of 64 named concepts, followed by a trailing no-text clause.

Observed result:

- Strong palette and subject-family variety.
- 64 exact-unique files.
- Caption-like text marks appeared beneath nearly every effect.
- The output did not prove one-to-one coverage of the named concepts.

The evidence does not show that native `32x32` sizing caused text. The two same-size single-concept prompts did not produce captions. The differentiating condition was the long named catalog, which likely activated a labeled icon-catalog prior; this remains a one-run hypothesis rather than a universal rule. A trailing `no text` clause was too weak to override it.

For named multi-output lists, front-load the semantic boundary: `Unlabeled pictorial assets only; the following names are prompt guidance and must never appear as visible text.` Keep the final no-text clause as reinforcement, and prefer smaller disjoint concept batches when exact coverage matters.

### Arcane Ring Variations

The arcane description centered on `a luminous violet energy ring collapsing around a bright cyan center`. The 64 outputs retained palette and theme well but were overwhelmingly circle-and-core compositions.

This is not evidence that small native images inherently lack variety. The prompt specified one dominant silhouette and did not request alternatives. PixelLab returned variations of that design. When broader variety is required, vary independent axes explicitly—ring, starburst, spiral, shard rupture, crescent, irregular tear, cross-flare, particle cloud—or run disjoint thematic prompts. `Unique` and different pixel hashes do not establish meaningful silhouette diversity.

### Ground-Impact Variations

The ground-impact description requested an `asymmetrical plume` with smoke `rising from a bright impact flash`. The 64 outputs consistently used a side-view profile, a visible ground baseline, and a diagonal or vertical plume. They also repeated the same fire-at-base plus smoke-column composition.

Top-down was not specified, so the side-view result followed the wording more closely than the user's unstated assumption. For top-down gameplay effects, say `top-down orthographic view looking straight down at the ground plane`, request radial debris around the center, and forbid a horizon, side profile, visible baseline, or vertical rising plume. View is a functional input, not a style detail to infer from `ground impact`.

### Revised Finding

Native-size generation is structurally reliable for file dimensions, not for set planning. At small sizes, one `generate-image-v2` call returns many candidates responding to one description:

- A narrow composition produces many close variations.
- A broad named catalog can increase diversity but may trigger labels and cannot guarantee one output per name.
- Exact hashes detect duplicate pixels, not duplicate composition or semantics.
- View remains ambiguous unless the prompt states the gameplay plane.

The efficient production pattern is to use several disjoint, moderately broad prompts with explicit silhouette axes, an early unlabeled-pictorial clause when names are listed, and an explicit view when orientation matters. Review all candidates for text, motif repetition, view, and semantics before keeping or assembling them.

## Recommended Production Direction

For a strict all-unique `512x512` atlas of 256 transparent `32x32` explosion effects:

1. Plan several disjoint, moderately broad prompts and show every input before spending credits; do not rely on one 64-name catalog to bind concepts to outputs.
2. Front-load unlabeled-pictorial wording whenever concept names could be interpreted as captions.
3. State the gameplay view when orientation changes usability, especially top-down versus side-view VFX.
4. Prefer native `32x32` outputs when exact cell dimensions outrank one-shot cohesion.
5. Use four `8x8` sheets when within-sheet cohesion is more important and accept that each sheet still needs visual grid verification.
6. Create a separate expected-grid inspection preview for every atlas or spritesheet result; never bake that grid into the final asset.
7. Review every candidate for readable or text-like marks, repeated dominant composition, requested view, and semantic duplication; pixel hashes only detect exact duplication.
