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
- `bottom-heavy chibi`
- `graphic/geometric shape language`
- `tapered geometry`
- `bell-bottom limbs`
- `cone-shaped limbs`
- `triangle-shaped limbs`
- `wedge-shaped feet`
- `mitten-like hands`
- `flat low-shading pixel sprite`
- `silhouette-readable MMO sprite`

New clarification from user review:

- The desired limb shape overlaps with common chibi / super-deformed drawing language, where arms and legs can widen toward the ends.
- However, the target is not the soft `mochi`, `bean body`, plush, squishy, or Animal Crossing / Nendoroid branch of chibi.
- The desired branch is closer to Ragnarok Online's modular paper-doll RPG sprite silhouette: slim torso, bottom-heavy body weight, simplified limbs, and legs that taper outward into wider blocky or wedge-like feet.
- Gacha Life is an adjacent reference for thicker stylized limbs, but it does not appear to emphasize the same outward flare as strongly as Ragnarok Online.
- Trickster Online and Secret of the Solstice are adjacent 2D/isometric MMO references worth inspecting, but Ragnarok Online remains the strongest remembered match for the base-body flare.
- The attached Ragnarok Online-style base reference is the clearest current visual target: lower-resolution than RO's full-quality sprites, but with the same bottom-heavy flared limb and narrow torso construction.

Useful references:

- [Customizable Pixel Art Character Kit / CPACK v2 on Unity Asset Store](https://assetstore.unity.com/packages/2d/characters/customizable-pixel-art-character-kit-13984) - best current external morphology reference. It has the same RO-like half-chibi/isometric body grammar, but cleaner and less muscular than Ragnarok Online.
- [Customizable Pixel Art Character Kit on GameDev Market](https://www.gamedevmarket.net/asset/customizable-pixel-art-character-kit-1076) - alternate store/source page for the same Mizuko/Midaem asset.
- [CPACK v2 YouTube preview](https://www.youtube.com/watch?v=U3qQE__kXqE) - visual preview reference for the kit in motion.
- [Ragnarok Online official/concept art gallery](https://www.creativeuncut.com/art_ragnarok-online_a.html) - useful high-level art reference for RO's chibi and semi-chibi identity.
- [Ragnarok Online chibi characters art](https://www.creativeuncut.com/gallery-14/ro-sd-characters3.html) - useful reference for the official SD/chibi promotional direction.
- [RagnarokOnline Job Class & NPC Sprite List](https://nn.ai4rei.net/dev/npclist/?qq=8) - useful for inspecting actual RO sprite silhouettes and body/gear readability.
- [iRO Wiki Character Sprite Simulator](https://costume.irowiki.org/) - useful interactive visual reference for RO body/clothing/headgear combinations.
- [The Spriters Resource: Ragnarok Online](https://www.spriters-resource.com/pc_computer/ragnarokonline/) - useful for inspecting official ripped RO sprite sheets by class, NPC, enemy, head, weapon, and related categories. Use as visual study/reference only.
- [The Spriters Resource: Ragnarok Online Novice](https://www.spriters-resource.com/pc_computer/ragnarokonline/asset/141222/) - useful direct reference for a simpler playable-class body with multiple walking/action frames.
- [The Spriters Resource: Ragnarok Online NPCs Walking](https://www.spriters-resource.com/pc_computer/ragnarokonline/asset/127670/) - useful for broad low-top-down humanoid silhouette comparison.
- [Custom Characters Sprites (Ragnarok Online Style)](https://cheeseguy.artstation.com/projects/QXKYOB) - useful modern fan/professional reference; the page notes character sizes around 45-60px wide by 70-100px tall, which supports a taller-than-64 visible body target for RO-like work.
- [Ragnarok Online Base Templates for RPGM VX ACE](https://moonfaeriestudio.com/download/ragnarok-online-base-templates-for-rpgm-vx-ace/) - highly relevant scale reference because it explicitly adapts heavily edited RO-style bases for RPG Maker VX Ace. Terms are non-commercial/personal-use with credit, so treat this as inspiration and proportion study, not production input.
- [Ragnarok Online Base Female for RPGM VX Ace](https://www.deviantart.com/moonfaeriestudio/art/Ragnarok-Online-Base-Female-for-RPGM-VX-Ace-458217977) - companion MoonFaerie page; useful if accessible in a browser because search metadata confirms it is an RO-based RPG Maker base.
- [RO Young Male Base for RPGM VX Ace](https://www.deviantart.com/moonfaeriestudio/art/RO-Young-Male-Base-for-RPGM-VX-Ace-458232707) - companion MoonFaerie base variant; useful for comparing less gendered/taller young body proportions.
- [Ragnarok Online Sprite - 01 by Farheit](https://www.deviantart.com/farheit/art/Ragnarok-Online-Sprite-01-57059213) - useful example of a fan-made RPG Maker XP sprite modeled from a Ragnarok Online character; the page reports a 128x192 image size, implying RPG Maker-style frame layout.
- [Disgaea RO Sprites on PixelJoint](https://pixeljoint.com/pixelart/39574.htm) - useful art-process reference for what artists perceive as RO palette/shading style. Comments discuss palette/ramp choices in an RO context.
- [FXFreitas Sprites showcase on Hercules Board](https://board.herc.ws/topic/9831-showcase-fxfreitas-sprites/) - useful for custom/edited RO-style sprite discussion and examples, including Ragnarok DS sprite enhancement and RO color/texture matching notes.
- [Reddit comment calling the style "ragnarok half-chibi"](https://www.reddit.com/r/RagnarokOnline/comments/1h9zn24/comment/m18hle5/) - useful because it independently describes the exact discovery problem: RO's half-chibi style is hard to find references for, and AI tools struggle to reproduce it from generic terms.
- [Tree of Savior on Steam](https://store.steampowered.com/app/372000/Tree_of_Savior_English_Ver/) - adjacent cute/charming character reference, but not as exact for the target base silhouette.
- [Tree of Savior concept art gallery](https://toswiki.treeofsaviorgame.com/gallery/concept_art) - adjacent costume/character proportion reference.
- [La Tale official page](https://latale.papayaplay.com/latale.do?tp=download) - confirms La Tale as a 2D side-scrolling fantasy MMORPG. Useful for 2D avatar/clothing readability, but side-view proportions are less directly comparable to low-top-down base sprites.
- [Trickster Online overview](https://en.wikipedia.org/wiki/Trickster_Online) - useful adjacent 2D isometric anime MMORPG reference, but likely rounder and more animal/avatar-specific than the target.
- [Secret of the Solstice review on MMOs.com](https://mmos.com/review/secret-of-the-solstice) - useful adjacent reference because it describes the game as RO-inspired, with 3D backgrounds and 2D sprites. Visual style is close enough to inspect, but likely not as exact as RO for the flare target.
- [Celestian Tales: Old North Steam discussion on Ragnarok-like sprites](https://steamcommunity.com/app/315860/discussions/0/541907867783281124/?l=latam) - useful developer-side note: the developer says RO's style was the basis for their assets, but their sprites are larger and structurally different. Good reference for RO-inspired character direction, not for 64px base scale.
- [Celestian Tales: Old North Kickstarter](https://www.kickstarter.com/projects/ekuatorgames/celestian-tales-old-north-redefining-the-classic-r) - useful adjacent reference; search result text notes inspiration from older Suikoden titles and Ragnarok Online, though the page may block direct fetch.
- [Clip Studio chibi proportion guide](https://tips.clip-studio.com/en-us/articles/4829) - useful proportion reference: chibi can range up to about 3 heads tall, which supports testing `2.5 heads tall` and `3 heads tall` instead of generic `chibi`.
- [What the UPA Style Actually Is](https://animationobsessive.substack.com/p/what-the-upa-style-actually-is) - useful terminology for flat, graphic shape language rather than anatomical realism.
- [My Life as a Teenage Robot - Rob Renzetti](https://robrenzetti.com/my-life-as-a-teenage-robot/) - useful reference for stylized 1950s animation and "Future Deco" graphic design language, not a direct pixel-art game reference.
- [Action Platformer Character Template by Ozzbit Games (itch.io)](https://ozzbit-games.itch.io/action-platformer-character-template) - lower priority than the CPACK reference. Not chibi, and a side-view 32px platformer sprite rather than a low-top-down base, so it is a limb-shape reference only. Per user review, its limbs flare outward toward the hands and feet in the target silhouette, making it a useful example of the desired flared-extremity read. License is tiered (free personal-use / PRO commercial); use as visual limb-shape study, not production input.

Ragnarok Online remains the closest game reference found so far. Tree of Savior and La Tale are useful adjacent references for cute MMO avatars and clothing readability, but they do not appear to describe the exact base body problem as well as RO-like semi-chibi sprite construction.

Panty & Stocking and My Life as a Teenage Robot are useful for the shape-language half of the prompt: flat, graphic, angular, wedge-like, and not pillowy baby-chibi. They should not replace the RPG sprite reference; they should only add geometric language.

Web-search implications from 2026-06-30:

- For smaller-size inspiration, the best found target is not a generic RO rip; it is `Ragnarok Online Base Templates for RPGM VX ACE`, because it compresses heavily edited RO-style bodies into an RPG Maker-compatible format.
- Official RO class sheets from The Spriters Resource remain useful for the original bottom-heavy silhouette, but they are too detailed/large to directly describe a 64px PixelLab target.
- Celestian Tales is confirmed as RO-inspired by developer/community material, but its sprites are intentionally larger than RO, so it is less useful for the requested lower-resolution base.
- Secret of the Solstice is a valid adjacent game reference for RO-like 2D sprites in a 3D/isometric MMO, but current search results suggest it copies the general RO presentation more than the exact lower-resolution base-body flare.
- Use all found third-party sprite sheets and galleries as visual inspiration only. Licensing and ownership vary; do not feed them directly into generation or claim derived production rights without separate permission.

Why Ragnarok Online appears unusually isolated:

- Most `chibi` art references optimize for a soft head-heavy caricature: bean or pear bodies, equal-width tube limbs, plush roundness, and toy-like hands/feet.
- Ragnarok Online's silhouette solves a different production problem. It needs tiny low-top-down sprites that remain readable while wearing modular paper-doll equipment.
- That combination rewards a narrow core body with exaggerated extremities: small torso, separated head, simplified hands, and bottom-heavy wedge/block feet that keep pose and equipment readable at a distance.
- Other adjacent games usually change at least one of those constraints. Tree of Savior and Celestian Tales move larger and more detailed; Dofus/Wakfu-like isometric characters have bigger torsos and rounder/stubbier masses; Gacha-style avatars use thicker limbs but not the same low-top-down wedge-foot construction.
- The Reddit `ragnarok half-chibi` comment is useful supporting evidence because another artist independently ran into the same naming/reference-search problem.
- A useful human-facing label is therefore `Ragnarok Online half-chibi paper-doll sprite proportions`, not generic `chibi`, `SD`, or `super deformed`.

## CPACK V2 Reference Findings

The user's purchased `Customizable Pixel Art Character Kit` / `CPACK v2` is now the best external anchor for the target base body. It appears to capture the same useful silhouette family as Ragnarok Online, while avoiding the heavier muscular/anatomical detail that made direct RO references risky.

Local reference files reviewed:

- `C:\Users\shilo\Downloads\CPACK v2 Documentation.pdf`
- `C:\Users\shilo\Downloads\readme.rtf`
- `C:\Users\shilo\Downloads\Male_Skin_01.png`
- `C:\Users\shilo\Downloads\Female_Skin_01.png`

Documentation and readme facts:

- The kit contains male and female base pixel-art character sheets.
- It includes stand poses and walking animations in 8 directions, using an isometric perspective.
- Each walking animation is a perfect loop with 8 frames.
- Each sheet is 576x784px.
- Each frame/cell is 64x98px.
- The character is assembled from layered sprite sheets: skin, eyes, hair, shirt, pants, shoes, with optional hats/glasses and back-hair/front-hair ordering.
- The PDF recommends Unity import settings that preserve pixel art: Truecolor compression, mipmapping off, point sampling, anisotropic filtering off, and anti-aliasing off.
- The readme describes the kit as good for MMOs and classic 2D isometric/horizontal games.

Measured skin-sheet facts:

| File | Sheet size | Grid | Cell size | Visible body size range | First standing frame visible size |
|---|---:|---:|---:|---:|---:|
| `Male_Skin_01.png` | 576x784 | 9x8, 72 frames | 64x98 | 20-37px wide, 69-74px tall | 29x72px |
| `Female_Skin_01.png` | 576x784 | 9x8, 72 frames | 64x98 | 20-37px wide, 69-74px tall | 28x70px |

Visual morphology notes:

- The head is large but not baby-round or plush.
- The torso is narrow and small, but not an exaggerated hourglass.
- The shoulders/chest are restrained, leaving room for shirts and jackets.
- The limbs are simple and readable, with minimal anatomy.
- The arms and legs are visibly large compared with the torso. The torso reads as a narrow central connector, while the limbs carry much of the body mass and silhouette.
- The hands are small/simple rather than large gloves.
- The feet are the major shape anchor: larger, rounded wedge/block forms that make the character bottom-heavy and stable.
- The silhouette is outfit-friendly because the base is not over-muscled and the extremities are broad enough to support shoes, pants, sleeves, and layered clothing.
- The style reads like a clean, lower-muscle cousin of Ragnarok Online rather than a generic chibi tutorial base.

Derived proportion observation from the first standing frames:

- Male first standing frame visible size is about 29x72px; female first standing frame visible size is about 28x70px.
- In the front-facing standing pose, the full body span reaches about 24-28px through the shoulder/arm/hip region, while the central torso itself reads much narrower because the arms sit outside it.
- The lower-body rows separate into two limb masses around 7-9px wide each through the legs, then widen into foot shapes around 10-14px wide each.
- This means the target is not just `narrow torso` or `wedge feet`; it is a proportion relationship: small torso core, comparatively substantial limbs, and feet that are large enough to anchor the whole sprite.

Implications for the 64px target:

- CPACK's frame cell is 64x98, but the visible standing body is about 70-72px tall. Our PixelLab `64x64` target should be understood as a desired visible-body scale near 64px, not as the exact CPACK cell size.
- If recreating the feel at smaller scale, the likely target is a visible body around 60-64px tall inside a larger transparent canvas, with a possible future 48px visible-height downscale experiment.
- Prompting should preserve CPACK's clean body grammar: `customizable isometric pixel art avatar base`, `8-direction RPG sprite proportions`, `small narrow torso`, `simple low-anatomy limbs`, `arms and legs large compared with the small torso`, `bottom-heavy rounded wedge feet`, `outfit-layer friendly base`.
- Do not prompt for CPACK by name when generating unless the goal is explicitly reference discussion. Use its structural lessons rather than copying or redistributing the purchased asset.
- Keep CPACK as the primary external shape anchor and Ragnarok Online as the lineage/reference family. For future generation attempts, CPACK should take priority when the two conflict.

## Prompt Implications From Research

Avoid relying on `chibi` alone. It pushes the model toward head size, not necessarily the desired body silhouette.

Promising terms to test:

- `semi-chibi`
- `2.5 heads tall`
- `3 heads tall`
- `bottom-heavy chibi`
- `customizable isometric pixel art avatar base`
- `8-direction RPG sprite proportions`
- `CPACK-like clean half-chibi body grammar`
- `Ragnarok Online style semi-chibi MMO sprite`
- `RO-style semi-chibi base sprite`
- `flat low-shading`
- `minimal interior shading`
- `bell-bottom limbs`
- `cone-shaped limbs`
- `triangle-shaped limbs`
- `wedge-shaped feet`
- `mitten hands`
- `arms taper from thin shoulders to wide mitten hands`
- `legs taper from narrow thighs to wide wedge feet`
- `legs taper outward into wider blocky feet`
- `bottom-heavy rounded wedge feet`
- `small simple hands`
- `simple low-anatomy limbs`
- `arms and legs large compared with the small torso`
- `small torso core with substantial limbs`
- `outfit-layer friendly base`
- `legs close together`
- `no thigh gap`
- `compact thick limbs`
- `graphic geometric silhouette`
- `trapezoid torso`
- `flat chest and narrow waist`

Risky terms:

- `curvy`, which can pull the body toward gendered anatomy.
- `mochi`, `bean body`, `plush`, `squishy`, and `cuddly`, which pull toward the wrong soft rounded chibi branch.
- `Animal Crossing style` and `Nendoroid style`, which may reinforce toy-like or plush baby proportions rather than the RO-like modular base.
- Direct `Ragnarok Online` wording when it pulls in too much muscular/anatomical detail. Prefer CPACK-like clean half-chibi proportions when the goal is a blank base.
- `big eyes` without `unisex`, which can push gendered or infant-like face emphasis.
- `bald` too early in the prompt, which can dominate the result and produce baby-like heads.
- `super deformed` alone, which may mean 2-head bobblehead proportions instead of the desired 2.5-3-head semi-chibi avatar.

Next seed experiment to consider:

- Try `seed: 0` with `customizable isometric pixel art avatar base`, `clean half-chibi proportions`, `small narrow torso`, `simple low-anatomy limbs`, `bottom-heavy rounded wedge feet`, and `outfit-layer friendly base`, while keeping the canvas at 64x64, low top-down, and low/detail-light rendering.

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

Use this section to preserve the ranked set of results worth revisiting. These are the only current high-value anchors; the rest are lower-priority references unless a future result changes the pattern.

| Rank | Label | Character ID | Seed | Route | Artifact folder | Pros | Cons |
|---:|---|---|---:|---|---|---|---|
| 1 | Seeded V3 Best Wedge Low Flat | `4eb5d0a7-4e9a-4855-aa09-0eea36e68714` | `93636` | REST `/create-character-v3` | `pixellab-pip-generations/seeded-v3-pro-bald-style-comparison-93636/01-v3-best-wedge-low-flat/` | Highest-quality current direction; still reads hourglass; most reminiscent of Ragnarok Online without going too detailed or realistic. | Has glove-like hands and spread limbs. |
| 2 | Clean Chibi Base Template | `d5e4c061-0d01-43bf-a66f-b9b8feab71c3` | Unknown; not exposed by ZIP metadata, MCP, or REST detail | MCP `create_character`, standard | `pixellab-pip-generations/clean-chibi-base-template-d5e4c061/` | Best all-around shape, balanced detail, skin color, and cute clothing-template feel. | Added short dark hair; not bald. |
| 3 | Seeded Pro Best Wedge Low Flat | `70d2375a-3413-44bd-8f5b-773ddd9a3adb` | `93636` | REST `/create-character-pro` | `pixellab-pip-generations/seeded-v3-pro-bald-style-comparison-93636/03-pro-best-wedge-low-flat/` | Has the right hourglass flare and wedge body shape. | Far too flat and low quality. |
| 4 | Unified Limbs Narrow Torso | `dbd5b876-f7ec-4ae1-abf9-00f2a737332b` | Unknown; MCP run did not expose seed | MCP `create_character`, standard | `pixellab-pip-generations/standard-64-unified-simple-limbs-soft-rounded/narrow-torso/` | Sort of resembles the hourglass flare. | Proportions look unnatural and gender-based. |

Seed note:

- The original `Clean Chibi Base Template` seed could not be recovered from local ZIP metadata, MCP `get_character`, or authenticated REST `/characters/{id}`. Seed `93636` is a new fixed comparison seed derived from the original favorite's creation time `09:36:36`, not the hidden original seed.
- Seed `93636` appears to carry a strong style/quality bias across V3 and Pro. This helped create the current rank-1 V3 result, but it also appears to preserve failure modes such as Pro flatness and V3 anatomy/spread. Do not assume it is universally good.
- `e45281cf-b1e2-4af0-bee1-53bfcc7ca924` reused seed `93636` from the same Pro lineage as `70d2375a-3413-44bd-8f5b-773ddd9a3adb` and stayed extremely flat/low quality. This suggests it may be worth giving up on `93636` for Pro, even if it remains useful for V3.
- `32122f1b-9011-421a-941f-37ee3dfc9c68` also used seed `93636`; it looks Ragnarok-like, but far too heavily detailed and muscular for the desired blank base.

Dismissed or low-priority anchors:

- `a829518e-e5ac-411f-bdfa-fea2eff91494`, `7195dbce-f3dd-40f7-b811-e5270173bafa`, `bdd7b44f-185f-4ec5-ab28-c4f3d0745ba1`, and `28ac6e61-4dfd-4e2c-8616-3cee9c334661` are useful history but not current anchors. Do not prioritize generating from them unless a future prompt needs to revisit standard-mode wedge experiments.

Prompt control notes from liked seeded results:

- `Mitten hands` is risky because V3 can interpret it as actual gloves. Prefer `skin-colored simple hands`, `bare simple hands`, or `rounded hands` when no accessories are desired.
- For V3, add `arms close to body`, `legs close together`, `bare skin-colored hands and feet`, and `no gloves or accessories` when trying to keep the strong #1 style but remove the spread/glove failure.
- For Pro, keep the wedge body prompt but raise rendering guidance from `very low detail` to `medium-low pixel detail`, `basic pixel shading`, and `small readable body details`, while still forbidding 3D, realistic, painterly, or glossy rendering.

## Operating Rule For Future Numeric Replies

If the user replies with only a single number, interpret it as a request to run that many creative V3 attempts toward the current chibi-base style goal. Use the current best findings, especially seed `93636` unless there is a clear reason to vary seeds, and document relevant findings afterward.

When naming new generations, prefix the name with the route family: `V3 ...` for V3 generations and `PRO ...` for Pro generations. This keeps result folders and character lists scannable during prompt exploration.

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

## V3/Pro Four-To-One Compact Wedge Search

Artifact folder:

```text
pixellab-pip-generations/v3-pro-4to1-compact-wedge-search/
```

Settings:

| Field | Value |
|---|---|
| Date | 2026-06-30 |
| Ratio | 4 V3 attempts, 1 Pro attempt |
| V3 endpoint | REST `/create-character-v3` |
| Pro endpoint | REST `/create-character-pro` |
| Image size request | 64x64 |
| View | low top-down |
| Template | `mannequin` |
| V3 detail | low detail |
| V3 outline | single color outline |
| Prompt enhancement | disabled |
| Batch cost | 28 subscription generations |

Results:

| Prompt label | Character ID | Seed | Route | Folder | Main result |
|---|---|---:|---|---|---|
| V3 Seed93636 Compact Vertical Bare Hands | `5f02be9a-f3f0-4f42-90e4-b34cc7d5e424` | `93636` | REST `/create-character-v3` | `01-v3-seed93636-compact-vertical-bare-hands/` | Fixed the literal glove problem from rank-1, but kept the wide stance and still has too much anatomical definition. Not a better anchor than `4eb5d0a7-4e9a-4855-aa09-0eea36e68714`. |
| V3 Seed93636 Cute Compact Wedge Base | `7f84ea31-b564-4400-a6fb-50418823d854` | `93636` | REST `/create-character-v3` | `02-v3-seed93636-cute-compact-wedge-base/` | Worse than the first prompt. It became more baby-like and did not preserve the appealing style energy of the original `93636` wedge result. |
| V3 Seed93637 Compact Pose Wedge Search | `a8562812-53b8-4a3a-b3ac-6947f97d469f` | `93637` | REST `/create-character-v3` | `03-v3-seed93637-compact-pose-wedge-search/` | Most compact V3 body in this batch and reduced the stance spread, but lost charm and still did not reach the target flat hourglass/wedge avatar base. |
| V3 Seed93638 Clean Style Bald Compact | `1b55c2a6-e3ac-442e-8f40-220e7d3b54b7` | `93638` | REST `/create-character-v3` | `04-v3-seed93638-clean-style-bald-compact/` | Drifted into a short baby-like body. This reinforces that `bald hairless` plus `chibi` still risks infant proportions. |
| Pro Seed93639 Readable Wedge | `cf472bbd-b24b-4568-9b9f-241ca3fc605b` | `93639` | REST `/create-character-pro` | `05-pro-seed93639-readable-wedge/` | Preserved the Pro wedge/hourglass idea, but stayed too flat and low-character. Better than some failed Pro outputs, but not competitive with the best V3/standard anchors. |

Verification:

- All five completed successfully.
- All five downloaded as transparent PNG rotations.
- V3 returned 8 directions and 112x112 or 120x120 canvases, even with a 64x64 request.
- Pro returned 8 directions and a 104x104 canvas.
- Visible south sprite bounds ranged from roughly 50px to 60px tall.

Findings:

- `no gloves`, `bare hands`, and `bare feet` are useful and should stay in any prompt that uses hand-shape language.
- `compact vertical stance`, `feet below shoulders`, `arms hanging down`, and `legs close together` can reduce spread somewhat, but they do not reliably overcome seed `93636`'s wide-stance tendency.
- Reusing seed `93636` remains helpful for quality/style, but it also preserves the spread/anatomy failure. It is not enough to repair by prompt alone so far.
- Nearby seed `93637` reduced spread, but also lost the cuteness and style quality. This suggests seed exploration matters, but small numeric seed changes are not guaranteed to preserve the good traits.
- Pro with a different seed and `medium readable detail` still leaned too flat. The Pro route is not currently beating V3 or the original standard-mode favorite.
- None of these five should replace the ranked liked-result registry unless future human review chooses one as a partial anchor.

## Suggested Next Test Plan

Use standard mode first, with 4 directions, chibi proportions, low top-down view, size target 64, low or default detail, and omitted/default outline.

Prefer a small batch that tests only one variable at a time:

1. Candidate 1 prompt plus `bald hairless` at the end, but with a `tall chibi avatar` modifier near the front.
2. Candidate 1 prompt with hair removed from the image through an edit route rather than trying to regenerate the whole base as bald.
3. A new prompt centered on `tall chibi avatar base`, `young adult proportions`, and `tiny pinched torso`.
4. A prompt that avoids `oversized head` and `big eyes`, because those may amplify the infant-like read when combined with baldness and bare skin.

If preserving Candidate 1's body is more important than fresh generation, the most promising route may be an edit/paperdoll-style workflow: use Candidate 1 as the identity/reference and request removal of only the hair while preserving the body, pose, skin, canvas, and transparent background. That route should be documented as an edit experiment, not a solved base-generation prompt, until verified.

## Pixen Single-Image South-Facing Prompt Sweep

Artifact folder:

```text
pixellab-pip-generations/cpack-prompt-sweep-v3-pixen-20260630/
```

Plans and summaries:

| File | Purpose |
|---|---|
| `prompt-plan-v2-probe.json` | One V3 redundant CPACK-derived prompt plus four small Pixen probes. |
| `prompt-plan-v3-30-sweep.json` | Thirty 32x64 Pixen prompts compiled before generation. |
| `prompt-plan-v4-rescue-sweep.json` | Twenty 64x64 Pixen rescue prompts after 32x64 failed semantically. |
| `phase-2-pixen-probe/results.json` | Four-probe Pixen results and verification. |
| `phase-3-pixen-30-sweep/summary.json` | Thirty 32x64 Pixen results, contact sheet metadata, balance data. |
| `phase-4-pixen-rescue-64/summary.json` | Twenty 64x64 Pixen rescue results, contact sheet metadata, balance data. |

Settings used:

| Sweep | Route | Size | View | Direction | Detail | Outline | Prompt enhancement |
|---|---|---:|---|---|---|---|---|
| V3 redundant test | REST `/create-character-v3` | 64x64 request | low top-down | 8 rotations | low detail | omitted/null | disabled |
| Pixen probe | REST `/create-image-pixen` | 32x64 | low top-down | south | low detail | omitted/null | disabled |
| Pixen 30 sweep | REST `/create-image-pixen` | 32x64 | low top-down | south | low detail | omitted/null | disabled |
| Pixen rescue sweep | REST `/create-image-pixen` | 64x64 | low top-down | south | low detail | omitted/null | disabled |

Cost:

- Probe balance: `2305.45 -> 2299.45`, delta `6` subscription generations. This includes four Pixen probes and balance after the V3 job had already consumed its cost.
- Thirty-prompt Pixen sweep balance: `2299.45 -> 2269.45`, delta `30` subscription generations.
- Twenty-prompt 64x64 rescue sweep balance: `2269.45 -> 2249.45`, delta `20` subscription generations.
- Total tracked Pixen/image-sweep cost for this documented set: `56` subscription generations, excluding the earlier V3 cost already reflected before the probe balance snapshot.

### V3 Redundant CPACK-Derived Prompt

Prompt:

```text
customizable isometric pixel art avatar base, clean half-chibi proportions, small narrow torso core, arms and legs large compared with the torso, simple low-anatomy limbs, bottom-heavy rounded wedge feet, outfit-layer friendly base, light peach bare skin, bald hairless
```

Result:

- V3 completed and saved 8 transparent rotations under `phase-1-v3-character/`.
- South frame is bald and full body, but still more anatomical and less cute than the original `Clean Chibi Base Template`.
- The redundant CPACK-derived wording did not magically recover the desired base shape in V3.

### Pixen Probe Findings

Four 32x64 probes tested the initial prompt with `south-facing`, `front-facing`, `idle`, and `arms resting at sides`.

Findings:

- `front-facing` and `south-facing` helped orientation, but did not prevent scene/action/body-rendering drift.
- `idle` reduced the action feel slightly, but Pixen still created anatomy-heavy, posed, or clothing-like results.
- `arms resting at sides` was the best pose-control phrase, but it made the result more doll/anatomy-heavy.
- `bare skin` was not sufficient to prevent clothing-like artifacts. Future prompts need explicit `nude`, `no clothing`, and `no accessories` when searching for this base.
- Even with `detail: low detail`, Pixen still rendered more shading and anatomy than desired. Prompt-side `low quality`, `low shading`, and `flat colors` are worth testing, but they are not enough by themselves.

### 32x64 Thirty-Prompt Sweep

The 30-prompt sweep intentionally varied the body-language terms while keeping a consistent control set:

- `single`
- `front-facing` and/or `south-facing`
- `idle`
- `unisex`, `androgynous`, or `non-gendered`
- `nude bare skin`
- `no clothing`, `no clothes`, and/or `no accessories`
- `bald hairless`
- `low quality`, `low shading`, `flat colors`, and/or `low detail`
- small torso plus large/simple/wedge limbs

Main result:

- The sweep mostly failed. Pixen treated many 32x64 prompts as cropped portrait-like character art rather than a small complete body sprite.
- Many outputs had huge cropped heads, dramatic faces, extra rendering, action/scene energy, or implied clothing/accessory details.
- The 32x64 aspect ratio is valid according to the API, but for this content it appears to encourage tight crops and high visual emphasis on the head/face.

Prompt implications:

- Do not rely on `front-facing/south-facing idle character base` alone for Pixen single-image generation.
- Add `full body visible head to feet`, `small centered figure`, and `not portrait/not close-up` if using Pixen for this search again.
- If the goal is a complete sprite at 32x64, Pixen may need a reference image or a character route instead of prompt-only single-image generation.

### 64x64 Rescue Sweep

The rescue sweep switched to 64x64 and explicitly requested:

- `small centered full-body sprite`
- `entire body visible head to feet`
- `not portrait`, `not close-up`, `not a bust`
- `no scene`, `no action`
- the same nude/unisex/bald/low-shading controls

Main result:

- 64x64 reduced the crop/portrait failure and produced more complete bodies.
- The route still did not solve the target style. Outputs continued to drift toward dramatic faces, gendered body language, extra costume/body rendering, or the wrong silhouette.
- Several results are usable as evidence that 64x64 is better for full-body discovery than 32x64, but none should replace the existing liked anchors.

Best partial lessons:

- `full body visible with empty transparent space around it` and `small centered figure` were more effective than `32x64` for avoiding head crops.
- `small full-body`, `entire body visible`, and `not portrait` should be used together if Pixen is tried again.
- `RPG maker scale` and `sprite sheet cell` helped communicate small full-body scale, but still did not force the CPACK-like body shape.
- The single-image Pixen route is poor for discovering this very specific CPACK/RO-like base shape from text alone. It may be useful for cheap rough probing, but the stronger path is likely reference-guided editing or character generation anchored on a known-good body.

Current conclusion:

- Prompt-only Pixen is not the secret for this target yet.
- The most promising future direction is to use the purchased CPACK-style asset or the original `Clean Chibi Base Template` as a reference/identity anchor, then test hair removal or style transfer while preserving body proportions.
- If generating from text only, use V3/standard character routes rather than Pixen single-image, because character routes are more likely to preserve full-body sprite structure.
