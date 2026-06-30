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
- `Unisex` appears important. When omitted, PixelLab more often invents gendered body signals, facial styling, or anatomy emphasis instead of treating the image as a neutral outfit base.
- A visible thigh gap is a failure signal for this target. The desired limb shape is compact and thick, with legs reading as close-set columns or simple wedges rather than separated stick legs.
- V3 can still look high-detail even when `detail="low detail"` is passed. In MCP V3, detail and outline are soft guidance, while proportions and shading controls are ignored. If lower finish is important in V3, prompt text should explicitly say `flat low-shading`, `minimal interior shading`, or similar, but this is still not a guaranteed control.

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
- V3 minimal-body-term batch, 10 prompts, size target 64, low top-down, low detail. It confirmed that V3 tends to make random chibi variants instead of respecting the specific torso/limb construction. The `limbs flare outward toward big hands and big feet` variant drifted into extra/overactive arms and hands, not clean flared limbs.
- Prompting only `narrow torso`, `tiny pinched torso`, or `narrow upside-down hourglass torso` in V3 was not enough to prevent small bald baby-like bodies.
- Prompting `tall chibi avatar proportions` and `young adult proportions` made some V3 outputs taller, but did not solve the target silhouette.

## External Reference Findings

The target should not be described as generic `chibi` alone. Research and visual comparison suggest the better taxonomy is:

- `semi-chibi`
- `2.5 to 3 heads tall`
- `stylized avatar proportions`
- `graphic/geometric shape language`
- `tapered geometry`
- `wedge-shaped feet`
- `mitten-like hands`
- `flat low-shading pixel sprite`
- `silhouette-readable MMO sprite`

Useful references:

- [Ragnarok Online official/concept art gallery](https://www.creativeuncut.com/art_ragnarok-online_a.html) - useful high-level art reference for RO's chibi and semi-chibi identity.
- [Ragnarok Online chibi characters art](https://www.creativeuncut.com/gallery-14/ro-sd-characters3.html) - useful reference for the official SD/chibi promotional direction.
- [RagnarokOnline Job Class & NPC Sprite List](https://nn.ai4rei.net/dev/npclist/?qq=8) - useful for inspecting actual RO sprite silhouettes and body/gear readability.
- [iRO Wiki Character Sprite Simulator](https://costume.irowiki.org/) - useful interactive visual reference for RO body/clothing/headgear combinations.
- [Custom Characters Sprites (Ragnarok Online Style)](https://cheeseguy.artstation.com/projects/QXKYOB) - useful modern fan/professional reference; the page notes character sizes around 45-60px wide by 70-100px tall, which supports a taller-than-64 visible body target for RO-like work.
- [Tree of Savior on Steam](https://store.steampowered.com/app/372000/Tree_of_Savior_English_Ver/) - adjacent cute/charming character reference, but not as exact for the target base silhouette.
- [Tree of Savior concept art gallery](https://toswiki.treeofsaviorgame.com/gallery/concept_art) - adjacent costume/character proportion reference.
- [La Tale official page](https://latale.papayaplay.com/latale.do?tp=download) - confirms La Tale as a 2D side-scrolling fantasy MMORPG. Useful for 2D avatar/clothing readability, but side-view proportions are less directly comparable to low-top-down base sprites.
- [Trickster Online overview](https://en.wikipedia.org/wiki/Trickster_Online) - useful adjacent 2D isometric anime MMORPG reference, but likely rounder and more animal/avatar-specific than the target.
- [Clip Studio chibi proportion guide](https://tips.clip-studio.com/en-us/articles/4829) - useful proportion reference: chibi can range up to about 3 heads tall, which supports testing `2.5 heads tall` and `3 heads tall` instead of generic `chibi`.
- [What the UPA Style Actually Is](https://animationobsessive.substack.com/p/what-the-upa-style-actually-is) - useful terminology for flat, graphic shape language rather than anatomical realism.
- [My Life as a Teenage Robot - Rob Renzetti](https://robrenzetti.com/my-life-as-a-teenage-robot/) - useful reference for stylized 1950s animation and "Future Deco" graphic design language, not a direct pixel-art game reference.

Ragnarok Online remains the closest game reference found so far. Tree of Savior and La Tale are useful adjacent references for cute MMO avatars and clothing readability, but they do not appear to describe the exact base body problem as well as RO-like semi-chibi sprite construction.

Panty & Stocking and My Life as a Teenage Robot are useful for the shape-language half of the prompt: flat, graphic, angular, wedge-like, and not pillowy baby-chibi. They should not replace the RPG sprite reference; they should only add geometric language.

## Prompt Implications From Research

Avoid relying on `chibi` alone. It pushes the model toward head size, not necessarily the desired body silhouette.

Promising terms to test:

- `semi-chibi`
- `2.5 heads tall`
- `3 heads tall`
- `Ragnarok Online style semi-chibi MMO sprite`
- `RO-style semi-chibi base sprite`
- `flat low-shading`
- `minimal interior shading`
- `wedge-shaped feet`
- `mitten hands`
- `arms taper from thin shoulders to wide mitten hands`
- `legs taper from narrow thighs to wide wedge feet`
- `legs close together`
- `no thigh gap`
- `compact thick limbs`
- `graphic geometric silhouette`
- `trapezoid torso`
- `flat chest and narrow waist`

Risky terms:

- `curvy`, which can pull the body toward gendered anatomy.
- `big eyes` without `unisex`, which can push gendered or infant-like face emphasis.
- `bald` too early in the prompt, which can dominate the result and produce baby-like heads.
- `super deformed` alone, which may mean 2-head bobblehead proportions instead of the desired 2.5-3-head semi-chibi avatar.

## Next Six-Prompt Test Plan

Run the next test in two groups:

No game reference, maximum descriptive body language:

1. `Unisex semi-chibi avatar base character, 2.75 heads tall, light peach bare skin, no clothes, bald hairless, flat low-shading pixel sprite, narrow trapezoid torso, flat chest, compact thick limbs, arms taper from thin shoulders to wide mitten hands, legs taper from narrow thighs to wide wedge feet, legs close together, no thigh gap.`
2. `Unisex stylized chibi base character, light peach bare skin, no clothes, bald hairless, graphic geometric silhouette, tiny pinched torso, narrow waist, simple column legs with thick wedge feet, simple arms with oversized mitten hands, flat low-detail shading, cute neutral avatar proportions.`
3. `Unisex semi-chibi dress-up avatar base, 3 heads tall, light peach bare skin, no clothes, bald hairless, flat cartoon pixel-art shading, small narrow torso, broad simple hands and heavy wedge feet, thick close-set limbs, tapered geometry, readable outfit-template silhouette.`

Game/reference-anchored:

4. `Unisex Ragnarok Online style semi-chibi MMO base sprite, light peach bare skin, no clothes, bald hairless, 3 heads tall, low top-down RPG view, narrow torso, simplified mitten hands, wedge-shaped feet, compact thick limbs, legs close together, flat low-shading pixel art.`
5. `Unisex RO-style 2.5D isometric semi-chibi avatar base, light peach bare skin, no clothes, bald hairless, tiny trapezoid torso, narrow waist, arms taper to mitten hands, legs taper to wide wedge feet, no thigh gap, readable clothing-template silhouette, flat low-detail pixel sprite.`
6. `Unisex semi-chibi MMO avatar base inspired by Ragnarok Online sprite proportions and flat geometric cartoon shape language, light peach bare skin, no clothes, bald hairless, 2.75 heads tall, narrow pinched torso, thick tapered limbs, mitten hands, wedge feet, minimal interior shading.`

## Researched Six-Prompt Batch Results

Artifact folder:

```text
pixellab-pip-generations/standard-64-flat-researched-chibi-base-prompts/
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
| Shading | flat shading |
| Outline | single color black outline |
| Batch cost | 6 subscription generations |

Ranking from human review:

1. Prompt 3, `Unisex semi-chibi dress-up avatar base... broad simple hands and heavy wedge feet... thick close-set limbs... tapered geometry...`, is the strongest direction from this batch. It leaned into wedge-shaped legs and heavy feet more than prior attempts.
2. Prompts 1 and 2 are secondary partial successes. They preserve the lower-detail standard-mode look and stay closer to a base template than the game-name prompts, but they do not improve the torso or arm wedge shape enough.
3. Prompts 4, 5, and 6, which mention Ragnarok Online / RO, failed for this specific blank base target. The game reference did not produce the desired proportions, and prompt 5 contaminated the result with colored clothing or footwear details.

Important visual findings:

- Prompt 3's legs moved closer to the desired wedge style.
- Prompt 3 still did not solve the arms; the arms did not clearly become wedge-shaped.
- Prompt 3 still has a more defined torso than desired. The target torso should read flatter and more like a simple narrow hourglass or trapezoid, not a detailed anatomical torso.
- Long prompts are not proven to help. The stronger result may have come from specific terms such as `dress-up avatar base`, `heavy wedge feet`, `thick close-set limbs`, and `tapered geometry`, not from prompt length.
- Ragnarok Online is still useful as a human-facing research reference, but direct `Ragnarok Online style` or `RO-style` prompt wording should be treated as risky for blank base generation.

Next focused prompt direction:

- Stay in standard mode with low detail and flat shading.
- Build around prompt 3's successful terms.
- Remove direct game names.
- Reduce anatomical-detail cues.
- Test shorter versus medium-length prompts around the same wedge-leg idea.
- Add more explicit arm shape language: `wedge arms`, `sleeve-shaped arms`, `arms widen from shoulder to mitten hands`, or `flat tapered arms`.
- Add torso simplification: `flat narrow hourglass torso`, `simple torso silhouette`, or `no detailed torso anatomy`.

Next three prompts to test:

1. `Unisex semi-chibi dress-up avatar base, 3 heads tall, light peach bare skin, no clothes, bald hairless, flat low-shading pixel sprite, flat narrow hourglass torso, no detailed torso anatomy, thick close-set wedge legs, heavy wedge feet, sleeve-shaped arms that widen into mitten hands.`
2. `Unisex semi-chibi base character, light peach bare skin, no clothes, bald hairless, simple flat hourglass torso, compact thick limbs, wedge legs, wedge arms, large mitten hands, heavy wedge feet, legs close together, flat low-detail shading.`
3. `Unisex dress-up chibi avatar base, light peach bare skin, no clothes, bald hairless, small flat torso, thick close-set tapered legs with heavy wedge feet, tapered sleeve-like arms with mitten hands, cute outfit-template silhouette, low-detail flat shading.`

## Liked Result Registry

Use this section to preserve seeds, character IDs, prompts, and failure notes for results worth revisiting.

| Label | Character ID | Seed | Route | Artifact folder | Why it matters | Caveats |
|---|---|---:|---|---|---|---|
| Clean Chibi Base Template | `d5e4c061-0d01-43bf-a66f-b9b8feab71c3` | Unknown; not exposed by ZIP metadata, MCP, or REST detail | MCP `create_character`, standard | `pixellab-pip-generations/clean-chibi-base-template-d5e4c061/` | Best overall cute base style, skin color, and clothing-template feel. | Added short dark hair; not bald. |
| Standard Prompt 3 Flared Limbs Bald | `a829518e-e5ac-411f-bdfa-fea2eff91494` | Unknown; MCP run did not expose seed | MCP `create_character`, standard | `pixellab-pip-generations/standard-64-lowdetail-bald-prompt-comparison/prompt-3-flared-limbs-bald/` | One of the closer bald partials. | Did not nail torso or wedge limb shape. |
| Researched Prompt 3 Dress-Up Wedge Feet | `7195dbce-f3dd-40f7-b811-e5270173bafa` | Unknown; MCP run did not expose seed | MCP `create_character`, standard | `pixellab-pip-generations/standard-64-flat-researched-chibi-base-prompts/03-dress-up-wedge-feet/` | First meaningful wedge-leg direction; useful prompt lineage. | Arms and torso still not right. |
| Wedge Follow-Up 1 Hourglass Wedge | `bdd7b44f-185f-4ec5-ab28-c4f3d0745ba1` | Unknown; MCP run did not expose seed | MCP `create_character`, standard | `pixellab-pip-generations/standard-64-flat-wedge-followup-prompts/01-hourglass-wedge/` | Better wedge mass and close-set legs than most prior standard runs. | Less cute than the original hair version. |
| Wedge Follow-Up 3 Dress-Up Shorter | `28ac6e61-4dfd-4e2c-8616-3cee9c334661` | Unknown; MCP run did not expose seed | MCP `create_character`, standard | `pixellab-pip-generations/standard-64-flat-wedge-followup-prompts/03-dress-up-shorter/` | Cuter/better base silhouette than follow-up 1. | Less assertively wedge-shaped. |
| Seeded V3 Best Wedge Low Flat | `4eb5d0a7-4e9a-4855-aa09-0eea36e68714` | `93636` | REST `/create-character-v3` | `pixellab-pip-generations/seeded-v3-pro-bald-style-comparison-93636/01-v3-best-wedge-low-flat/` | Strongest V3 style hit so far; resembles the desired Ragnarok-like detail level and silhouette energy. | Limbs are spread too wide; `mitten hands` was literalized into green glove-like hands. |
| Seeded Pro Best Wedge Low Flat | `70d2375a-3413-44bd-8f5b-773ddd9a3adb` | `93636` | REST `/create-character-pro` | `pixellab-pip-generations/seeded-v3-pro-bald-style-comparison-93636/03-pro-best-wedge-low-flat/` | Very close to the desired wedge body shape. | Too flat and under-detailed; needs a richer detail/shading prompt. |

Seed note:

- The original `Clean Chibi Base Template` seed could not be recovered from local ZIP metadata, MCP `get_character`, or authenticated REST `/characters/{id}`. Seed `93636` is a new fixed comparison seed derived from the original favorite's creation time `09:36:36`, not the hidden original seed.

Prompt control notes from liked seeded results:

- `Mitten hands` is risky because V3 can interpret it as actual gloves. Prefer `skin-colored simple hands`, `bare simple hands`, or `rounded hands` when no accessories are desired.
- For V3, add `arms close to body`, `legs close together`, `bare skin-colored hands and feet`, and `no gloves or accessories` when trying to keep the strong #1 style but remove the spread/glove failure.
- For Pro, keep the wedge body prompt but raise rendering guidance from `very low detail` to `medium-low pixel detail`, `basic pixel shading`, and `small readable body details`, while still forbidding 3D, realistic, painterly, or glossy rendering.

## Operating Rule For Future Numeric Replies

If the user replies with only a single number, interpret it as a request to run that many creative V3 attempts toward the current chibi-base style goal. Use the current best findings, especially seed `93636` unless there is a clear reason to vary seeds, and document relevant findings afterward.

## Seed 93636 Glove/Detail Follow-Up

Artifact folder:

```text
pixellab-pip-generations/seed-93636-v3-pro-fix-gloves-detail-set/
```

Settings:

| Prompt | Character ID | Seed | Route | Main result |
|---|---|---:|---|---|
| V3 close limbs bare hands | `32122f1b-9011-421a-941f-37ee3dfc9c68` | `93636` | REST `/create-character-v3` | Removed the green glove issue, but stance remained wide and anatomy became too muscular/defined. |
| V3 compact wedge RPG detail | `babe78c9-8765-413f-a9b9-1d6834f308e4` | `93636` | REST `/create-character-v3` | Kept skin-colored hands and the strong V3 wedge/RPG energy, but still had a wide stance and anatomical torso. |
| Pro wedge with readable detail | `e45281cf-b1e2-4af0-bee1-53bfcc7ca924` | `93636` | REST `/create-character-pro` | Maintained Pro's wedge body shape and added a little readable detail, but remained restrained and less charming than the V3 direction. |

Findings:

- `bare skin-colored hands` and `no gloves` fixed the literal glove problem caused by `mitten hands`.
- The wide-limb spread did not resolve just from `arms close to body` and `legs close together`.
- `Ragnarok-like low top-down RPG sprite detail` helped preserve the appealing V3 energy, but may pull the torso toward too much anatomy.
- Pro can be nudged away from totally flat output with `medium-low readable detail`, `basic pixel shading`, and `subtle skin shading`, but the result still lacks the charm and visual punch of the best V3 seeded result.

Next prompt implications:

- Avoid `mitten hands`.
- Try `small bare hands` or `simple rounded bare hands` instead of `large hands` or `mitten hands`.
- To reduce wide stance in V3, try pose/silhouette wording such as `standing straight`, `feet below shoulders`, `compact vertical stance`, or `arms hanging down`.
- Avoid `Ragnarok-like detail` when the torso starts getting too anatomical; use `RPG sprite detail` or `cute sprite detail` instead.
- The best current V3 path is still seed `93636`, but with pose constraints and accessory avoidance.

## Suggested Next Test Plan

Use standard mode first, with 4 directions, chibi proportions, low top-down view, size target 64, low or default detail, and omitted/default outline.

Prefer a small batch that tests only one variable at a time:

1. Candidate 1 prompt plus `bald hairless` at the end, but with a `tall chibi avatar` modifier near the front.
2. Candidate 1 prompt with hair removed from the image through an edit route rather than trying to regenerate the whole base as bald.
3. A new prompt centered on `tall chibi avatar base`, `young adult proportions`, and `tiny pinched torso`.
4. A prompt that avoids `oversized head` and `big eyes`, because those may amplify the infant-like read when combined with baldness and bare skin.

If preserving Candidate 1's body is more important than fresh generation, the most promising route may be an edit/paperdoll-style workflow: use Candidate 1 as the identity/reference and request removal of only the hair while preserving the body, pose, skin, canvas, and transparent background. That route should be documented as an edit experiment, not a solved base-generation prompt, until verified.
