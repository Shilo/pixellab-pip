# PixelLab Pixen 128×128 Head-and-Shoulders Portrait Prompt Research Spike

Last reviewed: 2026-08-04.

Status: MVP recommendation ready for another user run; prompt-only consistency is improved, not guaranteed.

## Question

Find a small, reusable Pixen prompt for square profile portraits that:

- uses a 128×128 canvas;
- asks for the PixelLab `south-west` direction;
- produces a traditional head-and-shoulders / upper-bust crop;
- avoids both a head-only close-up and a waist-up or full-body composition; and
- keeps the subject at a similar scale across repeated, text-only generations.

The two supplied examples were both 128×128. They were used as visual framing anchors only; Pixen has no reference image in this test.

## Terminology finding

Use **head-and-shoulders portrait** as the primary prompt term. It is the clearest common description of a portrait that stops around the shoulders; the Metropolitan Museum of Art notes that this is the crop most people associate with a portrait. **Bust-length portrait** is also a valid art-history term, but it is safer when paired with an explicit boundary such as “from the top of the head to the upper chest.” The National Gallery of Art uses “bust-length” and “three-quarter perspective” together for an upper-torso portrait.

Use **three-quarter view facing left** for the pose. “Three-quarter” describes the subject turned roughly 45 degrees while both eyes remain readable; it is not the same as “three-quarter length,” which asks for a much larger body crop. In this spike, `direction: "south-west"` is the PixelLab selector and the natural-language phrase is the traditional pose description.

Sources: [The Metropolitan Museum of Art, “What Makes a Portrait?”](https://www.metmuseum.org/de/perspectives/portraits), [National Gallery of Art, “Oriental with a Turban, Three-Quarter View”](https://www.nga.gov/artworks/157148-oriental-turban-three-quarter-view), and [PixelLab camera options](https://www.pixellab.ai/docs/options/camera).

PixelLab documents the camera and direction controls as weak guidance, so the selector and prompt wording must be treated as probabilistic inputs and every output must be checked visually.

## Local evidence reviewed first

Before the live run, I reviewed the canonical Pixen prompt reference, the earlier Pixen full-body prompt spike, image-model benchmark/style evidence, image-size limits, asset routing, MCP/REST parity, terminology, job lifecycle, blueprint, usage-reporting, and candidate-review references.

The relevant existing findings were:

- Pixen is a tight framer and can crop larger subjects; that makes explicit portrait boundaries important.
- Pixen is a good value choice for characters/single subjects, but its view and direction controls can be underweighted.
- 128×128 is valid for Pixen and is a useful square test size.
- A seed was omitted so the test measured normal stochastic variation rather than a seed-locked composition.
- The final request used MCP `create_image_pixen` followed by `get_image`; no REST, Pro, PixFlux, style reference, or local art generation was used.

## Controlled test

Every successful call used:

```json
{
  "width": 128,
  "height": 128,
  "direction": "south-west",
  "no_background": false
}
```

The subject-sweep prompts used one weathered old man and a plain dark muted background to keep background complexity from becoming a second framing variable. The first wave tested four prompt forms with three seedless attempts each. The pilot call counted as the first repeat of P1. One extra P3 submission was refused by the live 20/20 concurrency limit before a job was created; it was retried after a slot opened and was not charged.

### Prompt sweep

P0 — minimal natural wording:

```text
a weathered old man with a balding crown, wisps of gray hair, a full gray beard, and a heavy dark coat; pixel art portrait, three-quarter view facing left, both eyes visible. Plain dark muted background.
```

P1 — explicit common crop term:

```text
Head-and-shoulders pixel art portrait of a weathered old man with a balding crown, wisps of gray hair, a full gray beard, and a heavy dark coat; three-quarter view facing left, both eyes visible, shoulders and upper chest visible, centered, medium portrait framing, plain dark muted background.
```

P2 — art term plus explicit boundary:

```text
Bust-length pixel art portrait of a weathered old man with a balding crown, wisps of gray hair, a full gray beard, and a heavy dark coat; three-quarter view facing left, both eyes visible, from the top of the head to the upper chest, both shoulders fully visible, centered, plain dark muted background.
```

P3 — longer exclusions and lower-left wording:

```text
Traditional head-and-shoulders pixel art portrait of a weathered old man with a balding crown, wisps of gray hair, a full gray beard, and a heavy dark coat; three-quarter view turned toward the lower-left, both eyes visible; head and shoulders only, from the top of the head through the upper chest, both shoulders fully visible, centered with clear space above the head, medium portrait crop, not a head-only close-up, not waist-up, not full body. Plain dark muted background.
```

P4 — concise crop contract plus a scale anchor:

```text
Classic head-and-shoulders pixel art portrait of a weathered old man with a balding crown, wisps of gray hair, a full gray beard, and a heavy dark coat; three-quarter view facing left, both eyes visible; top of head to upper chest, both shoulders fully visible; medium, consistent portrait scale, head about half the canvas height, clear margin above the head, no head-only close-up, no waist-up or full body. Plain dark muted background.
```

## Results

The acceptance gate was visual and applied to every saved PNG:

1. decoded PNG is exactly 128×128;
2. face reads as a left-facing three-quarter view with both eyes visible;
3. top of head through upper chest is present, both shoulders are visible, and no lower-body crop appears;
4. the head is not cropped or presented as a head-only close-up; and
5. repeated outputs do not contain an obvious scale outlier relative to the same prompt.

| Variant | Attempts | Crop/orientation | Scale finding | Decision |
|---|---:|---|---|---|
| P0 minimal | 3 | 3/3 pass | Acceptable, but the scale anchor is implicit | Keep as a useful baseline only |
| P1 head-and-shoulders | 3 | 3/3 pass | Good; “medium portrait framing” is less concrete than P4 | Viable short form |
| P2 bust-length | 3 | 3/3 pass | Good and concise when paired with explicit upper-chest bounds | Viable art-history form |
| P3 long exclusions | 3 | 3/3 pass | Repeat 3 is a visibly smaller head; the exclusions did not prevent drift | Reject as the blueprint |
| P4 scale anchor | 3 | 3/3 pass | All three stayed near the intended medium scale | Promote |

The P3 result is important: “not head-only” and “not waist-up” did not act as a reliable scale control. Concise positive composition plus one approximate scale anchor worked better in this sample.

### Cross-subject validation of P4

P4 was run three times for each subject, still at 128×128 with `direction: "south-west"`, no seed, and the same plain-background constraint.

| Subject class | Attempts | Crop/orientation | Scale consistency | Result |
|---|---:|---|---|---|
| Weathered old man | 3 | 3/3 pass | No obvious outlier | Pass |
| Older woman with glasses | 3 | 3/3 pass | No obvious outlier | Pass |
| Young adult | 3 | 3/3 pass | No obvious outlier | Pass |

This is a 9/9 validation sample, not a deterministic guarantee. The renders vary in palette, clothing details, background treatment, and facial proportions, but they remain in the same head-and-shoulders scale band and do not drift into head-only or waist-up framing.

## MVP recommendation

Use this as the reusable prompt template:

```text
Classic head-and-shoulders pixel art portrait of [SUBJECT]; three-quarter view facing left, both eyes visible; top of head to upper chest, both shoulders fully visible; medium, consistent portrait scale, head about half the canvas height, clear margin above the head, no head-only close-up, no waist-up or full body. Flat, solid-color dark muted background with no gradient.
```

Send it to Pixen with:

```json
{
  "description": "Classic head-and-shoulders pixel art portrait of [SUBJECT]; three-quarter view facing left, both eyes visible; top of head to upper chest, both shoulders fully visible; medium, consistent portrait scale, head about half the canvas height, clear margin above the head, no head-only close-up, no waist-up or full body. Flat, solid-color dark muted background with no gradient.",
  "width": 128,
  "height": 128,
  "direction": "south-west",
  "no_background": false
}
```

Keep `[SUBJECT]` focused on identity, hair, face, clothing, and one or two defining features. Do not add `waist-up` when the target is a bust/head-and-shoulders crop. Avoid “profile picture” as the composition term because it can pull the model toward a face-only crop. Keep the background flat and single-color during scale calibration; explicitly forbid gradients. The original conversation’s stacked ledgers, lamp, lantern, and other scene props should be added only after the crop contract is stable, and then retested.

Generate directly at 128×128 for this MVP. A 128×192 render followed by a square crop is a different composition experiment and may reintroduce scale drift; it needs its own validation if vertical slack remains part of the production pipeline.

The portable tested blueprint is [`portrait-head-shoulders-mvp.blueprint.json`](../../skills/pixellab-pip/blueprints/portrait-head-shoulders-mvp.blueprint.json). The live run manifest and inspection sheets are in the ignored run folder: [`manifest`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/portrait-bust-mvp-20260804.manifest.json), [`prompt sweep P0`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/wave1/P0-contact.png), [`prompt sweep P1`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/wave1/P1-contact.png), [`prompt sweep P2`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/wave1/P2-contact.png), [`prompt sweep P3`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/wave1/P3-contact.png), [`scale ablation P4`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/wave2-scale/P4-contact.png), and [`9-image validation sheet`](../../pixellab-pip-generations/portrait-bust-mvp-20260804/wave3-validation/validation-all-contact.png).

## Limitations and next test

- The run proves a useful Pixen MVP for plain-background text-only portraits, not exact pixel identity across generations.
- The PixelLab camera page explicitly warns that direction/view are weak controls; visual rejection remains required.
- No style image, 128×192-to-128×128 crop, rich scene background, or cross-run identity test was included.
- For production, keep the existing eye-line alignment and add a head-size acceptance gate. Reject or retry obvious scale outliers instead of trusting the prompt alone.
