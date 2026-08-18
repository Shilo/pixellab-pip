# PixelLab Armless Character Prompt Research Spike

Executed: 2026-08-17.

Status: exploratory prompt research complete; no runtime recommendation promoted.

Purpose: test whether PixelLab `create_character` can produce a genuinely
armless humanoid character when the request is fixed at 32px and eight
directions, while the description is varied from a long constrained prompt to
short positive wording such as `armless`. This is a research record, not a
change to the Pip skill or a new armless-character feature.

## Bottom line

The tested `create_character` v3 humanoid route did not produce an armless
character in any of the twelve prompt attempts. Every output had recognizable
arms, hands, or arm-like side armor/limbs in the reviewed directions.

The second, concise-positive block removed wording that duplicates structured
request fields. The shortest prompts did not solve the problem:

- `armless` still produced a conventional humanoid with arms;
- `armless human` was the least decorated and closest result, but still had
  clear arm-like side limbs; and
- adding `warrior`, `mohawk`, or `chest armor` preserved the identity while
  retaining obvious arms or arm armor.

The first block also found no benefit from long inline exclusions. That is a
finding for this small exploratory sample, not a universal claim about
negative wording on every PixelLab route or model build.

## Fixed request shape

Every request used the same MCP call shape. Only `description` changed.

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

## Test design

The test was split into two prompt blocks:

1. **Full prompt block (`U0`–`S1`)** — original wording, exact repeat,
   positive inventory, explicit positive geometry, concise exclusions, a long
   negative list, and semantic armless framing.
2. **Concise positive block (`A0`–`A4`)** — an identity ladder beginning with
   exactly `armless` and adding only the minimum identity nouns and clothing
   terms.

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

### Block 1 visual evidence

![Full prompt block sprite sheet](../../pixellab-pip-generations/armless-character-prompt-study-20260817/full-prompt-block/armless-32px-create-character-sprite-sheet.png)

The `C1` west frame could not be fetched after repeated CDN `502`/`520`
responses. The review sheet marks that one cell as missing; the other 55
direction files are preserved in the [full prompt block run folder](../../pixellab-pip-generations/armless-character-prompt-study-20260817/full-prompt-block/).

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

### Block 2 visual evidence

![Concise positive prompt sprite sheet](../../pixellab-pip-generations/armless-character-prompt-study-20260817/concise-positive-block/armless-32px-concise-positive-sprite-sheet.png)

The [concise positive block run folder](../../pixellab-pip-generations/armless-character-prompt-study-20260817/concise-positive-block/) contains the 40 original directional PNGs and its prompt map.

## Interpretation

### What this supports

1. Removing redundant layout and output wording is appropriate when those
   properties are already represented by `create_character` fields.
2. A concise positive semantic label is worth testing before adding a long
   inline blacklist. The `armless human` result was the cleanest candidate in
   this run, even though it still failed.
3. The `humanoid` v3 route has a strong conventional-human anatomy prior in
   this task. Saying `armless` did not override that prior.
4. The long exclusion list did not rescue the first block. Repeating more
   synonyms was not shown to be a productive next move.

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

For the current prompt-only question, stop this block at twelve attempts:
there is no passing prompt to promote, and additional synonyms would add
variation without testing a new hypothesis.

## Related repository research

- [16px character generation spike](pixellab-16px-character-generation-spike.md)
- [Negative prompting research spike](pixellab-negative-prompting-research-spike.md)
- [Current-model inline negative prompting results](pixellab-inline-negative-prompting-current-model-results.md)
- [Chibi character findings](pixellab-chibi-base-character-findings.md)

## Runtime boundary

This spike adds no routing rule, schema support, prompt normalization, or
armless-character feature to Pip. The tracked change is this research document;
the generated review assets remain in the ignored
`pixellab-pip-generations/armless-character-prompt-study-20260817/` folder.
