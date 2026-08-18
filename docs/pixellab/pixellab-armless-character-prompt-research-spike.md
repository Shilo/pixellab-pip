# PixelLab Armless Character Prompt Research Spike

Executed: 2026-08-17.

Status: exploratory prompt research complete; no runtime recommendation promoted.

Purpose: test whether PixelLab `create_character`, standalone Pixen, or Pro can
produce a genuinely armless 32px character, using eight directions for the
character route and explicit full-body south-facing descriptions for the
freeform routes, while varying the wording from long constraints to concise
positive and geometric terms. This is a research record, not a change to the
Pip skill or a new armless-character feature.

## Bottom line

Neither the tested `create_character` v3 humanoid route, Pixen freeform route,
nor the Pro candidate sweep produced an armless character. Across 25 prompt
calls and 192 Pro candidates, every reviewed output had recognizable arms,
hands, or arm-like side armor/limbs.

The second, concise-positive block removed wording that duplicates structured
request fields. The shortest prompts did not solve the problem:

- `armless` still produced a conventional humanoid with arms;
- `armless human` was the least decorated and closest result, but still had
  clear arm-like side limbs; and
- adding `warrior`, `mohawk`, or `chest armor` preserved the identity while
  retaining obvious arms or arm armor.

Pixen did reliably honor the additional composition wording: all five Pixen
outputs were single, full-body, south-facing, transparent `32x32px` images.
That framing success did not remove the arms.

The first block also found no benefit from long inline exclusions. That is a
finding for this small exploratory sample, not a universal claim about
negative wording on every PixelLab route or model build.

## Fixed character-creator request shape

Every `create_character` request used the same MCP call shape. Only
`description` changed.

```python
create_character(
    description="{{PROMPT}}",
    body_type="humanoid",
    mode="v3",
    n_directions=8,
    size=32,
    view="low top-down",
)
```

The following were omitted from every call: `outline`, `shading`, `detail`,
`proportions`, reference images, style-character inputs, seed, and any separate
negative field. The test intentionally relied on the structured fields for
size, directions, body type, and view.

## Research basis

This spike combines the live outputs with the repository's route contracts and
prior prompt research. The linked documents are evidence and guidance for the
experiment; none is being promoted into a new runtime rule here.

| Research source | Finding used in this spike |
|---|---|
| [Pixen character prompt reference](../../skills/pixellab-pip/references/pixen-character-prompt.md) | The empirical Pixen framing prefix is `full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet.` The `arms at sides` phrase conflicted with this target, so the Q block kept the framing but removed that phrase. |
| [Create Image Pro reference](../../skills/pixellab-pip/references/create-image-pro.md) | Pro follows descriptions more closely than Pixen/v3/new at higher cost; small canvases return many candidates. Candidate siblings are correlated alternatives, so the paid call—not each sibling—is the experimental unit. |
| [Reviewable candidates reference](../../skills/pixellab-pip/references/reviewable-candidates.md) | All Pro candidates were reviewed, and the contact sheet uses user-facing labels `1`–`64`; the raw files retain the route's zero-based filenames. |
| [Pixen full-body prompt spike](pixellab-pixen-character-prompt-research-spike.md) | Pixen can be improved by explicit full-body/front/south/idle framing, but `view` and `direction` remain weak guidance and the route has no exposed humanoid/body-type mode. |
| [Inline negative prompting best practices](pixellab-inline-negative-prompting-best-practices.md) | Negative wording is route/model dependent. The useful hypotheses are concise guardrails, positive replacement/geometry, combined constraints, and long-list dilution—not a universal negative-prompt rule. |
| [Current-model inline negative results](pixellab-inline-negative-prompting-current-model-results.md) | Pro and Pixen respond differently: concise inline exclusions helped some Pro pseudo-text tasks, while Pixen projection failures were fixed by positive structural wording rather than repeated negatives. This justified testing both positive and negative anatomy variants here. |
| [16px character generation spike](pixellab-16px-character-generation-spike.md) | Pro's candidate sweep can be useful for small-silhouette exploration, while Pixen is a cheaper one-shot route; the result is target-specific and does not make Pro a universal winner. |
| [Chibi base character findings](pixellab-chibi-base-character-findings.md) | Anatomy and proportion language is soft; over-explaining anatomy can degrade outputs, and stored outline/detail settings are not proof that the model honored them. This supported keeping the new prompts explicit but compact. |
| [Official PixelLab documentation reference](../../skills/pixellab-pip/references/official-pixellab-documentation.md) | MCP and REST are overlapping but not identical surfaces. No undocumented humanoid switch, hidden system prompt, or unsupported negative field was assumed. |

The related official links used by the repository research are [PixelLab camera
options](https://www.pixellab.ai/docs/options/camera), the [v2 OpenAPI
schema](https://api.pixellab.ai/v2/openapi.json), and the [MCP documentation
inventory](https://api.pixellab.ai/mcp/docs).

## Complete run accounting

| Block | Calls | Returned output | Per-call usage reported | Review record |
|---|---:|---|---:|---|
| `U0`–`S1` | 7 | 56 expected character directions | v3 reported 2 generations | 55 direction frames reviewed; `C1-west` CDN download unavailable |
| `A0`–`A4` | 5 | 40 character directions | v3 reported 2 generations | 40 direction frames reviewed |
| `P0`–`P4` | 5 | 5 Pixen images | 1 generation | 5 images reviewed |
| `Q0`–`Q4` | 5 | 5 Pixen images | 1 generation | 5 images reviewed |
| `R0`–`R2` | 3 | 192 Pro candidates | 20 generations | 192 candidates reviewed |
| **Total** | **25** | **96 character directions + 10 Pixen images + 192 Pro candidates** | route-specific | all available outputs reviewed; `C1-west` was unavailable |

All live calls were made after the subscription generation pool was exhausted,
so PixelLab billed them to account credits. Balance snapshots were used only as
a paid-call safety check, not as an outcome measure; the service's concurrent
usage accounting did not provide a reliable basis for inferring an exact total
from balance deltas.

The 192 Pro candidates are 64 correlated siblings from each of three paid
calls, not 192 independent prompt experiments. The independent prompt units
are the three Pro descriptions and the 25 total calls across all blocks.

## Review and acceptance protocol

Every result was checked at native `32x32` size and in a nearest-neighbor
enlargement. The primary anatomy target was scored independently of visual
quality:

| Score | Meaning |
|---:|---|
| `0` | Pass: readable head, continuous torso/chest, two legs, two feet, no arm-like side geometry, and visible empty side silhouette. |
| `1` | Ambiguous: crop, occlusion, tiny scale, or view prevents a reliable anatomy judgment. |
| `2` | Fail: any recognizable arm, hand, sleeve, glove, gauntlet, shoulder pad, stump, side appendage, or missing required region. |
| `3` | Severe fail: extra limbs are prominent, duplicated, or dominate the silhouette. |

An apparent pass could not be credited if it depended on cropping, hiding the
arms behind the torso, turning away, losing the requested identity, or treating
the `32x32` canvas size alone as proof of armless anatomy. Transparency and
canvas dimensions were verified separately from silhouette compliance. No
secondary quality score was allowed to override a primary anatomy failure.

## Route comparison

| Route | Structured controls used | Prompt responsibilities | Observed result |
|---|---|---|---|
| `create_character` v3 | `body_type="humanoid"`, `mode="v3"`, `n_directions=8`, `size=32`, `view="low top-down"` | Subject identity and anatomy only; redundant size/direction/framing words were intentionally removed in Block 2. | Stable eight-direction character output, but all 12 jobs retained arms, hands, or arm-like armor. |
| `create_image_pixen` | `width=32`, `height=32`, `no_background=true`, `direction="south"`, `view="low top-down"` | Full-body and south-facing wording, plus the anatomy hypothesis. | All 10 outputs honored the single-image framing well enough to read as full-body south-facing sprites, but all retained arms or side limbs. |
| `create_image_pro` | `width=32`, `height=32`, `no_background=true` | Full-body, south-facing, low top-down, identity, and anatomy all had to be explicit because the MCP tool exposes no direction/view fields. | 192 candidates varied in palette, hair, clothing, and face, but none passed the armless anatomy target. |

The comparison separates a framing problem from an anatomy problem: Pixen's
explicit full-body/south-facing wording and structured selectors were enough to
make the composition readable, while neither Pixen nor Pro could suppress the
humanoid arm prior. Character Creator v3 supplied the strongest directional
workflow, but its humanoid prior also remained dominant.

## Test design

The test was split into three prompt blocks:

1. **Full prompt block (`U0`–`S1`)** — original wording, exact repeat,
   positive inventory, explicit positive geometry, concise exclusions, a long
   negative list, and semantic armless framing.
2. **Concise positive block (`A0`–`A4`)** — an identity ladder beginning with
   exactly `armless` and adding only the minimum identity nouns and clothing
   terms.
3. **Pixen block (`P0`–`P4`)** — the same concise identity ladder, with
   `full body` and `south-facing` explicitly included in each freeform image
   description.
4. **Pixen framing-first block (`Q0`–`Q4`)** — the repository's established
   Pixen framing prefix, with the normal `arms at sides` wording removed and
   replaced by five armless-specific anatomy hypotheses.
5. **Pro block (`R0`–`R2`)** — three explicit but concise prompts spanning
   positive inventory, concise exclusions, and arm-free geometry; each call
   returned 64 candidates at 32×32.

No reference image, seed, or post-generation edit was used. The calls were
exploratory and were not a same-seed statistical experiment; visual claims are
therefore limited to this run.

## Block 1: full prompt matrix

All seven outputs completed as transparent `32x32px` characters with eight
directions. The request IDs and south-frame alpha bounds are recorded below.

| Arm | Character ID | South alpha bounds | Anatomy score |
|---|---|---|---:|
| `U0` | `d24f2dcd-1e7c-4f95-b255-ddf9e5a0eb3a` | `17x30+0+0` | 3 |
| `R0` | `f9509f2e-035d-44e4-8d47-cc125f5185b5` | `22x30+0+0` | 3 |
| `B0` | `ac9cdb64-8ba7-4f98-a468-440a84c25273` | `23x30+0+0` | 3 |
| `P1` | `3a341cf3-e079-4960-94f6-cb5f9bd8f1f1` | `24x29+0+0` | 3 |
| `C1` | `762fcc5e-5e9e-4319-b150-620acbb26ceb` | `25x30+0+0` | 3 |
| `L1` | `e8382a8d-1436-4506-ad21-35b3208fbe4b` | `22x30+0+0` | 3 |
| `S1` | `da69082f-927c-4e17-a798-7d99a5151da8` | `24x30+0+0` | 3 |

Scoring used `0 = pass`, `1 = ambiguous`, `2 = fail`, and `3 = severe fail`.
The full block received a score of `3` because arms, hands, gauntlets, or
arm-like side armor were prominent across the directional set.

### U0 — original request

```text
Male human warrior with mohawk. Create only head, chest, legs and feet. DO NOT GENERATE HANDS AND ARMS!!!!!!
```

### R0 — exact repeat

```text
Male human warrior with mohawk. Create only head, chest, legs and feet. DO NOT GENERATE HANDS AND ARMS!!!!!!
```

### B0 — positive inventory and geometry

```text
32px full-body front-facing south-facing idle game character sprite, low top-down view. Centered male human warrior with a bright red mohawk and torso-only dark chest armor. Head, chest/torso, two legs, and two feet are the complete visible character. Clean flat pixel art, transparent background.
```

### P1 — explicit positive geometry

```text
32px full-body front-facing south-facing idle game character sprite, low top-down view. Centered male human warrior with a bright red mohawk and torso-only dark chest armor. Four visible regions only: head, chest/torso, legs, and feet. The final sprite has one head, one continuous chest/torso, two legs, and two feet. The torso tapers directly from the neck edge to the hips; both sides of the torso are open background; legs begin immediately below the torso; feet are the only horizontal projections. Clean flat pixel art, transparent background.
```

### C1 — positive geometry plus exclusions

```text
32px full-body front-facing south-facing idle game character sprite, low top-down view. Centered male human warrior with a bright red mohawk and torso-only dark chest armor. Four visible regions only: head, chest/torso, legs, and feet. The final sprite has one head, one continuous chest/torso, two legs, and two feet. The torso tapers directly from the neck edge to the hips; both sides of the torso are open background; legs begin immediately below the torso; feet are the only horizontal projections. Clean flat pixel art, transparent background. Constraint: exclude arms, forearms, hands, sleeves, gloves, gauntlets, shoulder armor, and side appendages.
```

### L1 — long negative list

```text
32px full-body front-facing south-facing idle game character sprite, low top-down view. Centered male human warrior with a bright red mohawk and torso-only dark chest armor. Four visible regions only: head, chest/torso, legs, and feet. The final sprite has one head, one continuous chest/torso, two legs, and two feet. The torso tapers directly from the neck edge to the hips; both sides of the torso are open background; legs begin immediately below the torso; feet are the only horizontal projections. Clean flat pixel art, transparent background. Exclude arms, forearms, hands, elbows, wrists, fingers, sleeves, gloves, gauntlets, shoulder pads, arm armor, side appendages, arm stumps, extra limbs, weapons, shields, capes, backpacks, text, watermarks, scenery, and background art.
```

### S1 — semantic armless framing

```text
32px full-body front-facing south-facing idle game character sprite, low top-down view. Centered male human warrior with a bright red mohawk and torso-only dark chest armor, designed as an armless four-region character: head, chest/torso, legs, and feet. The final sprite has one head, one continuous chest/torso, two legs, and two feet. The torso tapers directly from the neck edge to the hips; both sides of the torso are open background; legs begin immediately below the torso; feet are the only horizontal projections. Clean flat pixel art, transparent background.
```

### Block 1 review record

The generated contact sheet and raw direction files were local-only run
artifacts and are intentionally not linked from this repository document. The
tables, exact prompts, IDs, alpha bounds, and scores above are the retained
research record. The `C1` west frame could not be fetched after repeated CDN
`502`/`520` responses, so it was excluded from visual scoring.

## Block 2: concise positive matrix

The second block removed redundant description terms such as size, full-body,
front-facing, south-facing, idle, game, sprite, centered, and low top-down view.
Those properties were already fixed by the request shape.

All five outputs completed as transparent `32x32px` characters with eight
directions.

| Arm | Description | Character ID | South alpha bounds | Anatomy score |
|---|---|---|---|---:|
| `A0` | `armless` | `765d4cbf-8849-4717-a38a-c45ecc64348c` | `23x29+4+2` | 3 |
| `A1` | `armless human` | `edad4094-30b8-4d79-8052-81f694c199b0` | `17x30+7+1` | 2 |
| `A2` | `armless human warrior` | `20cf4e3c-1e69-4a49-a390-518e9cdf777c` | `17x26+7+3` | 3 |
| `A3` | `armless male human warrior with a mohawk` | `290ef3fa-b2e2-4bed-a4a6-7b074125feb2` | `18x28+6+2` | 3 |
| `A4` | `armless male human warrior with a mohawk and chest armor` | `44303b76-76cc-42b1-ad7f-9d5c9b6f1100` | `22x30+5+1` | 3 |

`A1` was scored `2` rather than `3` because its side limbs were less
decorated and less dominant than the other variants. It still failed the hard
requirement: the side geometry was recognizable as arms or arm-like limbs.

### A0

```text
armless
```

### A1

```text
armless human
```

### A2

```text
armless human warrior
```

### A3

```text
armless male human warrior with a mohawk
```

### A4

```text
armless male human warrior with a mohawk and chest armor
```

### Block 2 review record

The generated contact sheet and raw directional PNGs were local-only run
artifacts and are intentionally not linked from this repository document. The
exact prompts, IDs, alpha bounds, and scores above preserve the test result.

## Block 3: Pixen freeform image prompts

Pixen is not the character-creator route, so the description explicitly names
`full body` and `south-facing`. The structured `direction="south"` field was
also set, along with the target canvas and transparent background:

```python
create_image_pixen(
    description="{{PROMPT}}",
    width=32,
    height=32,
    no_background=True,
    direction="south",
    view="low top-down",
)
```

`detail`, `outline`, and `seed` were omitted. Each call cost one generation and
returned one image.

| Arm | Job ID | Alpha bounds | Anatomy score |
|---|---|---|---:|
| `P0` | `fa2b5dad-e230-4344-a2ae-3aa9acdb4e7b` | `17x30+7+1` | 3 |
| `P1` | `1e1350bc-2bd1-43b7-a3f1-3e4cc08ac66a` | `18x30+7+1` | 3 |
| `P2` | `d0f520ca-8506-4bec-ba60-ff3d597abb93` | `18x29+7+1` | 3 |
| `P3` | `d93c8644-78f6-4d39-ab85-7e651e97a382` | `18x30+7+1` | 3 |
| `P4` | `bf19a1ec-093a-49e2-9acd-b0bf9eb3fe63` | `22x29+5+1` | 3 |

### P0

```text
full body, south-facing, armless
```

### P1

```text
full body, south-facing, armless human
```

### P2

```text
full body, south-facing, armless human warrior
```

### P3

```text
full body, south-facing, armless male human warrior with a mohawk
```

### P4

```text
full body, south-facing, armless male human warrior with a mohawk and chest armor
```

### Pixen review record

All five Pixen outputs read as full-body south-facing sprites, but every one
still contains arms, hands, or arm-like side geometry. The generated images and
prompt map were local-only run artifacts and are intentionally not linked from
this repository document; the exact prompts, IDs, alpha bounds, and scores are
recorded above.

## Block 4: Pixen framing-first geometry prompts

The existing Pixen reference recommends a framing prefix for reliable
full-body, front/south-facing, idle composition. The normal `arms at sides`
phrase was intentionally omitted because it conflicts with the armless target.
The same structured request shape as Block 3 was used for all five calls.

| Arm | Hypothesis | Job ID | Alpha bounds | Anatomy score |
|---|---|---|---|---:|
| `Q0` | Framing prefix + `armless` | `432b7772-3cd4-4ef7-8107-75168a73c176` | `19x26+6+3` | 3 |
| `Q1` | Positive body-part inventory | `a5b6cd88-374e-4fc5-8606-087d018b4f11` | `21x29+5+1` | 3 |
| `Q2` | Short inline negative | `a9f8642e-cb0d-42f9-9265-8a9bbd3f209c` | `20x30+6+1` | 3 |
| `Q3` | Torso and side-limb geometry | `ad62fb87-77fd-48d1-b97f-1099aadc0e13` | `19x30+6+1` | 3 |
| `Q4` | `arm-free` semantic label | `ca5dc2c6-e7ee-40f3-945c-b7e0fe49d137` | `19x28+6+1` | 3 |

### Q0

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose, full figure from head to feet. armless male human warrior with a mohawk.
```

### Q1

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose, full figure from head to feet. one head, one torso, two legs, two feet; armless male human warrior with a mohawk.
```

### Q2

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose, full figure from head to feet. male human warrior with a mohawk. no arms, no hands, no sleeves, no shoulder armor.
```

### Q3

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose, full figure from head to feet. male human warrior with a mohawk, torso with no side limbs, legs directly below torso, feet only.
```

### Q4

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose, full figure from head to feet. arm-free male human warrior with a mohawk, head torso legs and feet only.
```

### Framing-first review record

The stronger framing prefix improved composition consistency but did not change
the anatomy outcome. All five still had recognizable arms, hands, or side
limbs. The generated images and prompt map were local-only run artifacts and
are intentionally not linked from this repository document; the exact prompts,
IDs, alpha bounds, and scores are recorded above.

## Block 5: Pro candidate sweep

Pro was tested only after the single-image routes failed. The block was kept
small because Pro returns a large candidate set and charges per call:

```python
create_image_pro(
    description="{{PROMPT}}",
    width=32,
    height=32,
    no_background=True,
)
```

Pro exposes no structured `direction` or `view` fields in this MCP tool, so
`full-body`, `south-facing`, and `low top-down` remained explicit in every
description. No reference image, style image, seed, or other optional field
was supplied. Each call returned 64 candidates and reported a cost of 20
generations; three calls were submitted.

| Arm | Prompt strategy | Job ID | Candidates | Armless passes |
|---|---|---|---:|---:|
| `R0` | Positive four-region inventory | `ec96df7b-ce28-41e2-a2bc-58babc1a2697` | 64 | 0 |
| `R1` | Concise exclusions | `188e9204-f70e-455a-84bc-17859cab8161` | 64 | 0 |
| `R2` | Arm-free torso geometry | `f4df9437-e61a-4dd8-90ec-00bdafea97f3` | 64 | 0 |

### R0 — positive four-region inventory

```text
full-body south-facing low top-down pixel-art game character sprite. Centered male human warrior with a mohawk. Exactly four visible regions: one head, one continuous torso, two legs, two feet. Armless silhouette; the torso has no side limbs, and the feet are the only horizontal projections. Transparent background.
```

### R1 — concise exclusions

```text
full-body south-facing low top-down pixel-art game character sprite. Armless male human warrior with a mohawk and chest armor. Head and torso connect directly to the legs; no arms, hands, sleeves, gloves, shoulders, or side appendages. Two feet only. Transparent background.
```

### R2 — arm-free geometry

```text
full-body south-facing low top-down pixel-art game character sprite. A deliberately arm-free male human warrior with a mohawk: head, broad torso, two legs, and two feet only. Empty background on both sides of the torso; legs start immediately below the torso; no arm-like shapes or equipment. Transparent background.
```

### Pro review record

All 192 candidates were reviewed in nearest-neighbor enlarged form. Pro
provided useful variation in faces, hair, palettes, and clothing, but every
candidate still had conventional arms, hands, or arm-like side geometry. The
generated candidates and prompt map were local-only run artifacts and are
intentionally not linked from this repository document; the exact prompts, job
IDs, candidate count, and result are recorded above.

## Interpretation

### What this supports

1. Removing redundant layout and output wording is appropriate when those
   properties are already represented by `create_character` fields.
2. A concise positive semantic label is worth testing before adding a long
   inline blacklist. The `armless human` result was the cleanest candidate in
   this run, even though it still failed.
3. Both the `humanoid` v3 route and Pixen had a strong conventional-human
   anatomy prior in this task. Saying `armless` did not override that prior.
4. The long exclusion list did not rescue the first block. Repeating more
   synonyms was not shown to be a productive next move.
5. Pixen's freeform prompt was enough to establish the requested framing, but
   framing control and anatomy control are separate problems.
6. The repository's stronger Pixen framing prefix improved composition but did
   not overcome the arm prior. The short negative, positive inventory,
   geometric, and `arm-free` variants all failed.
7. Pro's 64-candidate sweep increased variation but did not produce even one
   armless candidate across three explicit prompt strategies. More prompt
   breadth on this same route is unlikely to be the highest-value next test.

### What this does not support

- It does not prove that `armless` is ignored by PixelLab in general.
- It does not prove that positive wording is always better than negative
  wording.
- It does not compare seeds, model builds, routes, reference images, or
  post-generation editing.
- It does not establish a production workaround or authorize a Pip runtime
  change.

## Recommended next research boundary

If an armless asset remains a requirement, the next experiment should change
one representation or generation strategy rather than keep expanding the same
prompt vocabulary. Candidate research directions are a supplied visual
reference, a route that starts from an existing silhouette, or local assembly
from separately generated head/torso/legs/feet pieces. Those are separate
spikes and were not run here.

For the current prompt-only question, stop this block at 25 calls plus the 192
Pro candidates: there is no passing prompt to promote, and additional synonyms
would add variation without testing a new representation or route.

## Related repository research

- [16px character generation spike](pixellab-16px-character-generation-spike.md)
- [Negative prompting research spike](pixellab-negative-prompting-research-spike.md)
- [Current-model inline negative prompting results](pixellab-inline-negative-prompting-current-model-results.md)
- [Chibi character findings](pixellab-chibi-base-character-findings.md)

## Runtime boundary

This spike adds no routing rule, schema support, prompt normalization, or
armless-character feature to Pip. The tracked change is this research document;
the generated review sheets and raw outputs were local-only artifacts and are
intentionally not linked from this tracked document.
