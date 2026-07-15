# PixelLab Asset Routing

Last reviewed: 2026-07-10.

Purpose: map plain-language asset requests to the PixelLab workflow family most likely to satisfy the user without asking them to know PixelLab's internal product vocabulary.

PixelLab requests usually start as plain asset goals: "make a character," "generate a tileset," "edit this sprite," or "create UI." Pip should classify the asset intent first, then choose the PixelLab surface and endpoint/tool family.

Use this as routing guidance, not as a frozen schema. Refresh official docs for exact current parameters, result shapes, model/mode availability, pricing, and SDK coverage.

## Asset Intent Map

| User intent | Preferred route | Notes |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP character tools when configured; REST v2 character endpoints for code or exact control. | Character workflows often involve identity, directions, states, animations, and managed asset IDs. |
| Portrait to character or character to portrait | MCP portrait-character tools when configured; REST v2 `portrait-character-pro` for code or exact control. | This is an image conversion workflow. Use `portrait_to_character` for a bust portrait source and `character_to_portrait` for a full-body character source. |
| Character state or outfit/layer change | MCP character-state tools when available; REST v2 state/edit routes when exact control is needed. | Clarify whether the output should preserve identity, change pose/state, or generate a new design. |
| Character animation | MCP animation tools for managed characters; REST v2 animation endpoints for direct API use. | For existing multi-direction characters, default unspecified animation direction to `south` (down-facing) for one preview candidate. Ask or confirm before animating all directions, and do not silently choose a diagonal such as north-west. Ask only when animation type, direction, frame count, or source asset is unclear. |
| Object, prop, pickup, weapon, furniture that is not an icon or icon sheet | MCP object tools when configured; REST v2 object endpoints for code or exact control. | Infer object for standalone props, furniture, weapons, and managed reusable objects. Do not route inventory item icons, equipment icons, loot icons, pickup icons, or transparent RPG item-icon sheets through object generation. |
| Object animation or object state | MCP object animation/state tools when available; REST v2 object animation/state endpoints for direct API use. | Treat reusable objects differently from one-off generated images. |
| Top-down terrain tileset | MCP top-down tileset tools or REST v2 tileset endpoints. | Usually means terrain/autotile/Wang-style tileset. |
| Sidescroller/platformer tileset | MCP sidescroller tileset tools or REST v2 sidescroller tileset endpoints. | Distinct from top-down terrain and individual tile variants. |
| Individual tile variants | MCP tiles-pro tools or REST v2 tiles-pro endpoints. | This is different from a full terrain tileset. Clarify "tiles" vs "tileset" when ambiguous. |
| Isometric tile | MCP isometric tile tool or REST v2 isometric tile endpoint. | Ask whether the user wants one isometric tile or a full tileset when the wording is ambiguous. |
| Skill, ability, spell, action-bar, or hotbar icon | Create Image Pro (`generate-image-v2`) first. | Best-supported for complete/backgrounded sheets and single high-quality skill icons. For plural/complete requests, `32x32 icons` means per-icon cell size, not a 32x32 output canvas; use a sheet canvas such as `256x256` for 64 icons in an 8x8 grid. See [PixelLab Skill Icon Generation Spike](pixellab-skill-icon-generation-spike.md): the validated route is Create Image Pro (`generate-image-v2`), not object generation, tiles-pro, Create Image (New) / Pixen (`create-image-pixen`), or UI routes. Do not rewrite complete sheets as "each generated image is one standalone icon" unless the user explicitly wants separate generated files. Avoid positive rune/glyph/sigil concepts. For backgrounded skill-icon requests, preserve rich full-bleed background wording; for transparent/backgroundless requests, follow `icon.md` and omit background/opacity clauses. Do not route to UI asset tools unless the user asks for slots, buttons, bars, panels, or containers. |
| Inventory item, equipment, loot, pickup, consumable, or transparent RPG item icon | Create Image Pro (`generate-image-v2`) first. | Treat `32x32` as per-icon cell size for sheets. Use `no_background: true` for transparent item-icon sheets. Do not use object generation for item-icon requests; dedicated tests found noisy/downscaled-looking 32px results, incomplete or inconsistent contours, and weak readability. Note: Pixen over-shades/over-saturates small icons at its default detail — force low detail with a clamped palette, or prefer Pro. See [Icons](../../skills/pixellab-pip/references/icon.md). |
| General image, standalone sprite, icon, concept that is not a skill icon or item icon | REST v2 image generation. | MCP may not expose every raw image endpoint; use REST v2 for generic image primitives. Route skill/ability/spell/action-bar/hotbar icons through the skill-icon reference, and inventory/equipment/loot/pickup icons through the item-icon reference. |
| Background, scene, title image | REST v2 background/image generation. | Use documented `create-image-pixflux-background` for background-image generation when REST v2 is the selected surface; treat as normal image generation unless the user needs map/editor semantics. A blind single-reviewer benchmark ([results](../pixellab-image-model-benchmark-results.md)) split the model choice: **subject-less backdrops → PixFlux** (beats Pixen), but **full scenes with a subject → Pixen** (beats PixFlux; Pro only third). Pro is not worth its ~12× cost for scenes/backdrops/parallax — its edge is tiny icons and reference/style work. Two off-label findings from the same run: **Pixen is weakest for standalone objects/props** (prefer PixFlux there), and **BitForge is consistently weakest on raw image quality** — route to it for its unique controls (`init_image`, `mask_image`, `forced_palette`, `style_image`), not as a default quality pick. Directional evidence (2 seeds, one reviewer), not a decisive ranking. |
| UI, HUD, button, panel, menu | Use REST `/create-ui-asset` as the default structured UI asset route when REST and MCP are both available; use MCP `create_ui_asset` for MCP-first managed asset workflows; use REST `/generate-ui-v2` for loose UI images. | See [PixelLab UI Generation Surfaces Research](pixellab-ui-generation-surfaces-research.md). Website UI libraries are human/editor surfaces unless a public endpoint covers the task. |
| Pixel font, bitmap font, font atlas, generated game font | MCP font tools when configured; REST v2 `generate-font-pro` for code or exact control. | Use this for actual font generation with weight, glyph size, and optional font family name. Do not treat it as a generic lettering image route. |
| Image edit, inpaint, remove background, resize, convert to pixel art | REST v2 edit/transform endpoints. | Supplied images are optional unless the selected route requires image fields. For image-to-pixel-art without a requested size, prefer Pro. For fixed output size within current `output_size` limits, use normal `image-to-pixelart`. If the requested size is outside those limits, use Pro, verify dimensions, and if they differ, warn the user and ask before using PixelLab `resize` or local nearest-neighbor/canvas resize/pad/crop. |
| Multi-image edit or combine references | REST v2 `edit-images-v2` when the task is an edit with multiple source/reference images. | Aseprite's observed `generate-multi-edit` operation is an undocumented internal endpoint, not a public REST route. Use website/editor only when the user wants the visual experimental product flow. |
| Style reference or consistent-style generation | Create Image from Style Reference (Pro) (`generate-with-style-v2`) or another documented style/reference route. | Use Create Image from Style Reference (Pro) (`generate-with-style-v2`), Create Image Pro (`generate-image-v2`) style/reference fields, or documented image-model style fields as appropriate after checking current docs. In one focused house investigation, 24 reviewed Create Image (New) / Pixen (`create-image-pixen`) outputs failed to hold the requested top-down view. The user additionally reported the same practical failure with init-image guidance and Create Image Pro (`generate-image-v2`), and success with Create Image from Style Reference (Pro) (`generate-with-style-v2`). See [PixelLab Top-Down House Generation Routing Spike](pixellab-top-down-house-generation-routing-spike.md). Treat this as subject-specific observed routing evidence, not a universal model guarantee. |
| Canny/sketch, pose-guided image, depth/image-to-image | Visible website/editor/Aseprite workflow for exact Canny/Pose/Depth behavior; REST v2 only for an approximate documented image/init/reference workflow after explaining the difference and getting approval. | No exact public REST v2/MCP Canny, Pose, or Depth endpoint was documented. Observed Aseprite operation names include `generate-general-canny`, `generate-general-pose`, and `generate-pixelart-flux`; treat them as undocumented internal endpoints unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools. |
| Add VFX/effect/trail/aura to an existing sprite | REST v2 image edit. | When a target sprite/image is supplied, preserve that image and apply the effect to the same canvas. Generate a separate object/effect asset only when the user asks for an isolated reusable layer or no target image is supplied. |
| Reduce colors / quantize palette | Visible PixelLab website/editor, Aseprite, or Pixelorama workflow when the user wants exact PixelLab editor behavior. For direct file-level palette quantization, source-derived color reduction, bit-depth conversion, indexed conversion, strict palette clamps, or document palette replacement, use the agent-facing `aseprite-cli.md` contract. | PixelLab website docs include Reduce Colors, but no public REST v2/MCP reduce-colors endpoint was documented. Aseprite's observed `quantize-image` operation is an undocumented internal endpoint; do not invent `/v2/quantize-image`. |
| Unzoom pixel art | Aseprite or Pixelorama extension when the user is actively in that editor; otherwise local image tooling after labeling it as a non-PixelLab fallback. | Aseprite's observed `unzoom-pixelart` operation is an undocumented internal endpoint. No public REST v2 or MCP Unzoom endpoint was documented; do not invent `/v2/unzoom-pixelart`. |
| Try on garment/item | Website Try on for single-image compositing; REST `transfer-outfit-v2` for animation-frame outfit transfer. | Do not treat either as isolated layer extraction. |
| Reshape | Website Reshape or closest documented edit/character route after checking current docs. | Website docs require exactly 64x64 canvas; no public REST v2/MCP reshape endpoint was documented. |
| Pixel correction / clean-up | Aseprite extension for exact PixelLab behavior, or closest documented REST edit/convert route after checking docs. | Aseprite's observed `correct-pixelart` operation is an undocumented internal endpoint. No public REST v2/MCP pixel-correction endpoint was documented. |
| Prompt enhancement | REST v2 matching enhance endpoint; agent-side fallback. | Low-cost prompt prep. Pick the enhancer that matches the asset type; do not use them as generic optimizers. |
| Map image or level concept | REST v2 image/background route unless the user needs Map Workshop behavior. | A visual map concept is not the same thing as a website Map Workshop project; map extension/texture flows are website workflows unless public endpoints are documented. |
| Map object | MCP map-object tool when configured; REST v2 map-object endpoint when documented. | Distinguish map objects from whole maps and terrain tilesets. MCP map objects auto-delete after 8 hours. |
| Whole map / Map Workshop project | Visible website workflow or generated component assets. | Do not invent public map CRUD/export APIs when not documented. |
| Balance, usage, async job status | MCP balance/status tools when configured; REST v2 balance/background-job endpoints for code. | Report only what the selected route exposes. |

## Clarify Only For Real Collisions

Ask a short clarification when one phrase maps to multiple PixelLab workflows:

- `tiles`: terrain tileset, sidescroller tileset, isometric tile, or tile variants.
- `map`: whole map, map image, map object, tilemap, tileset, or Map Workshop project.
- `object`: prop/item/furniture/weapon vs a character-like being.
- `character animation direction`: default to `south` (down-facing) for the first candidate when direction is unspecified and available; ask if `south` is unavailable or if the desired gameplay-facing direction matters.
- `effect`: static sprite vs animated effect, and reusable object vs one-off image.
- `edit this`: edit target, style reference, identity reference, mask, first frame, or last frame.

Avoid asking for clarification when the normal game-asset meaning is obvious.

## Image Inputs

Text-only requests are valid for many PixelLab generation routes. Do not ask for images just because the user wants an asset.

When images are supplied, infer each file's role from the request and the selected endpoint. Common roles include style reference, identity/reference image, concept image, edit target, mask, palette/color reference, init/source image, first frame, or last frame.

## Runtime Reference Links

For detailed execution rules used by the skill, see:

- [Tilesets](../../skills/pixellab-pip/references/tileset.md)
- [Icons](../../skills/pixellab-pip/references/icon.md)
- [Skill Icon Generation Spike](pixellab-skill-icon-generation-spike.md)
- [Paperdolling](../../skills/pixellab-pip/references/paperdolling.md)
- [Image Input Roles](../../skills/pixellab-pip/references/image-input-roles.md)
- [Usage Reporting](../../skills/pixellab-pip/references/usage-reporting.md)
- [Official PixelLab Documentation](../../skills/pixellab-pip/references/official-pixellab-documentation.md)

## Related Research

- [Top-Down House Generation Routing Spike](pixellab-top-down-house-generation-routing-spike.md)
