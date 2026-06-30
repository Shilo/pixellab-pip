# PixelLab Chibi Base Character Findings

Last reviewed: 2026-06-30.

Purpose: record live-generation findings from attempts to create a reusable chibi base character for clothing and paperdoll-style outfit work. This is an unresolved prompt and routing spike. The best current result is useful as a style reference, but no tested prompt has reliably produced the desired bald, hairless, no-clothes template with the target proportions.

## Target Asset Definition

The desired asset is a cute unisex chibi avatar base for later clothing work:

- Tall chibi avatar proportions, not an infant-like or baby-short body.
- Large head, but with enough body height for readable outfits.
- Tiny narrow torso with an upside-down-hourglass or pinched trapezoid read.
- Chest/torso noticeably narrower than the head, hands, and feet.
- Simple limbs that feel slightly heavier toward the hands and feet.
- Bigger simple hands and feet, useful for readable gloves, sleeves, shoes, and boots.
- Light warm peach bare skin.
- No clothing.
- Ideally bald and hairless, while still avoiding an infant-like read.
- Transparent background.
- Low top-down RPG view.

The visual target is closer to a dress-up avatar or classic 2D MMO base than a generic baby chibi. Comparable style references include Ragnarok Online / MapleStory-like readable clothing proportions: small body core, larger head and extremities, and simplified limbs that leave room for outfit silhouettes.

## Current Status

No prompt has solved the full target. The most successful generation still added hair. The best bald candidate is acceptable only as a partial reference and does not nail the narrow torso or flared extremity feel.

Current working hypothesis:

- The combination of `bald hairless`, `no clothes`, `oversized head`, `big eyes`, and `chibi` can push the model toward an infant-like or baby-doll interpretation.
- Hair may help the model read the character as a stylized avatar rather than a bald baby-like body.
- Prompts that over-explain anatomy, safety framing, or template mechanics tend to degrade the result.
- The desired proportions may need wording such as `tall chibi avatar base`, `young adult proportions`, `tiny pinched torso`, `narrow upside-down hourglass torso`, `longer simple limbs`, and `big simple hands and feet`.

## Closest Candidate 1: Best Overall, But Has Hair

Artifact folder:

```text
pixellab-pip-generations/clean-chibi-base-template-d5e4c061/
```

Prompt:

```text
Cute unisex chibi base character with no clothes, bare skin, oversized head, big eyes, small nose and smile, soft rounded proportions, simple hands and feet, neutral standing pose, clean base sprite for outfits.
```

Settings:

| Field | Value |
|---|---|
| Surface | MCP `create_character` |
| Mode | `standard` |
| Body type | `humanoid` |
| Directions | 4 |
| Proportions | chibi preset |
| View | low top-down |
| Size target | 64 |
| Detail | medium/default behavior from the run |
| Outline | selective outline in the run |
| Cost | 1 subscription generation |

Observed result:

- This is the best current match for cuteness, skin color, clothing-template usefulness, and general proportions.
- It has the most successful avatar-like read.
- It produced transparent 4-direction PNGs.
- PixelLab returned a 92x92 canvas.
- The visible south-facing sprite is roughly 27px wide and 64px tall.
- Failure: PixelLab added short dark hair, so it is not a blank bald template.

Important lesson:

- The prompt includes several terms later suspected to be risky (`oversized head`, `small nose and smile`, `neutral standing pose`, `clean base sprite`), but in this specific standard-mode run they produced the closest overall result. Do not remove these terms from historical notes merely because later prompt theory changed.

## Closest Candidate 2: Best Bald Partial, But Proportions Still Weak

Artifact folder:

```text
pixellab-pip-generations/standard-64-lowdetail-bald-prompt-comparison/prompt-3-flared-limbs-bald/
```

Prompt:

```text
Cute unisex chibi base character, narrow torso, flared limbs, light peach bare skin, hairless bald.
```

Settings:

| Field | Value |
|---|---|
| Surface | MCP `create_character` |
| Mode | `standard` |
| Body type | `humanoid` |
| Directions | 4 |
| Proportions | chibi preset |
| View | low top-down |
| Size target | 64 |
| Detail | low detail |
| Outline | omitted; PixelLab resolved to single color black outline |
| Batch cost | 7 subscription generations for the comparison batch |

Observed result:

- This is the closest bald/hairless candidate from the low-detail prompt comparison.
- It has acceptable skin color and stays closer to a blank base than many later attempts.
- It produced transparent 4-direction PNGs.
- PixelLab returned a 92x92 canvas.
- The visible south-facing sprite is roughly 27px wide and 65px tall.
- Failure: it does not strongly achieve the desired narrow upside-down-hourglass torso, flared extremities, or the same cute avatar feel as Candidate 1.

Important lesson:

- `flared limbs` by itself is too weak or ambiguous. It does not reliably create the desired MapleStory/Ragnarok-like limb silhouette.

## Prompting Findings

Prompts that helped:

- `Cute unisex chibi base character`
- `soft rounded proportions`
- `simple hands and feet`
- `light warm peach bare skin` or `light peach bare skin`
- `hairless bald`, when baldness is required
- `narrow torso` or `narrow chest`, as weak guidance
- `limbs flare outward toward big hands and big feet`, as a clearer version of `flared limbs`

Prompts that are risky or failed in later tests:

- `mannequin`
- `non-sexual`
- `doll-like`
- `simplified anatomy`
- `no explicit details`
- `smooth head`
- `paperdoll base`
- `clean sprite`
- `neutral standing pose`
- `oversized head`, especially combined with `bald hairless` and `no clothes`
- `big eyes`, especially combined with `bald hairless` and `no clothes`
- `super deformed`, because it mainly increases compressed/head-heavy chibi behavior and does not imply the desired limb shape.
- `tapered limbs`, because it is ambiguous and may mean limbs narrow toward the ends, the opposite of the desired silhouette.
- `bell-bottom`, because it can imply clothing rather than body/limb structure.

Prompt theory still worth testing:

```text
Cute unisex tall chibi avatar base character, young adult proportions, tiny pinched torso with narrow upside-down hourglass shape, longer simple limbs, big simple hands and feet, soft rounded proportions, light peach bare skin, no clothes, bald hairless.
```

Alternate wording if `upside-down hourglass` is too abstract:

```text
Cute unisex tall chibi avatar base character, young adult proportions, tiny tapered torso, narrow waist, slightly wider shoulders and hips, longer simple limbs, big simple hands and feet, soft rounded proportions, light peach bare skin, no clothes, bald hairless.
```

## Model And Setting Findings

Standard mode:

- Produced the two closest candidates so far.
- Best fit for small, simple, clothing-template-style character bases.
- Cheaper, making prompt exploration practical.
- Supports 4-direction output and chibi proportions.

V3 mode:

- Did not produce the desired style in these tests.
- Tended to over-stylize the head, face, fingers, or body.
- Always returned 8 directions in the MCP tool.
- Ignored chibi proportions in the MCP tool behavior.
- Cost more than standard mode.

Pro mode:

- Produced a cleaner result than V3 in the final best-prompt comparison, but still did not beat Candidate 1.
- Ignored detail settings.
- Always returned 8 directions in the MCP tool.
- Cost substantially more than standard mode.
- Not justified as the default route for this unresolved base-template search.

Detail:

- High detail is a poor fit for this target. It adds complexity that works against a cute, clean base.
- Low detail is better than high detail for bald/blank attempts, but it has not solved the target proportions.
- The best overall candidate did not come from the later low-detail bald attempts.

Outline:

- Selective outline performed poorly in later bald tests.
- Default or omitted outline resolved to single color black outline and generally produced more usable pixel sprites.
- Single color outline remains a reasonable fallback if default outline is unavailable or inconsistent.

Canvas and size:

- A `size` target of 64 in MCP `create_character` returned larger transparent canvases around the sprite, commonly 92x92 for standard-mode 4-direction characters.
- The visible south-facing sprite in the two closest standard-mode candidates was about 64-65px tall.
- Do not confuse the MCP `size` target with exact output canvas dimensions.

## Failed Experiment Summary

The following directions did not solve the target:

- Adding safety or negative-style wording around nudity/body details.
- Over-simplifying the prompt with terms such as `mannequin`, `doll-like`, or `simplified anatomy`.
- Switching to V3 for higher quality.
- Switching to Pro as a blanket quality fix.
- High-detail generation.
- `super deformed` as a substitute for the desired limb proportions.
- `tapered limbs` as the limb-shape phrase.
- `flared limbs` alone without clearer extremity wording.
- Repeating the desired limb phrase across all prompt variants without addressing the infant-like bald/no-clothes read.

## Suggested Next Test Plan

Use standard mode first, with 4 directions, chibi proportions, low top-down view, size target 64, low or default detail, and omitted/default outline.

Prefer a small batch that tests only one variable at a time:

1. Candidate 1 prompt plus `bald hairless` at the end, but with a `tall chibi avatar` modifier near the front.
2. Candidate 1 prompt with hair removed from the image through an edit route rather than trying to regenerate the whole base as bald.
3. A new prompt centered on `tall chibi avatar base`, `young adult proportions`, and `tiny pinched torso`.
4. A prompt that avoids `oversized head` and `big eyes`, because those may amplify the infant-like read when combined with baldness and bare skin.

If preserving Candidate 1's body is more important than fresh generation, the most promising route may be an edit/paperdoll-style workflow: use Candidate 1 as the identity/reference and request removal of only the hair while preserving the body, pose, skin, canvas, and transparent background. That route should be documented as an edit experiment, not a solved base-generation prompt, until verified.
