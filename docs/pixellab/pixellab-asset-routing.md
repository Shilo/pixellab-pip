# PixelLab Asset Routing

Last reviewed: 2026-06-25.

Purpose: map plain-language asset requests to the PixelLab workflow family most likely to satisfy the user without asking them to know PixelLab's internal product vocabulary.

PixelLab requests usually start as plain asset goals: "make a character," "generate a tileset," "edit this sprite," or "create UI." Pip should classify the asset intent first, then choose the PixelLab surface and endpoint/tool family.

Use this as routing guidance, not as a frozen schema. Refresh official docs for exact current parameters, result shapes, model/mode availability, pricing, and SDK coverage.

## Asset Intent Map

| User intent | Preferred route | Notes |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP character tools when configured; REST v2 character endpoints for code or exact control. | Character workflows often involve identity, directions, states, animations, and managed asset IDs. |
| Character state or outfit/layer change | MCP character-state tools when available; REST v2 state/edit routes when exact control is needed. | Clarify whether the output should preserve identity, change pose/state, or generate a new design. |
| Character animation | MCP animation tools for managed characters; REST v2 animation endpoints for direct API use. | For existing multi-direction characters, default unspecified animation direction to `south` (down-facing) for one preview candidate. Ask or confirm before animating all directions, and do not silently choose a diagonal such as north-west. Ask only when animation type, direction, frame count, or source asset is unclear. |
| Object, prop, pickup, weapon, furniture | MCP object tools when configured; REST v2 object endpoints for code or exact control. | Infer object for props/items/furniture/weapons; infer character for beings with identity or body animation. |
| Object animation or object state | MCP object animation/state tools when available; REST v2 object animation/state endpoints for direct API use. | Treat reusable objects differently from one-off generated images. |
| Top-down terrain tileset | MCP top-down tileset tools or REST v2 tileset endpoints. | Usually means terrain/autotile/Wang-style tileset. |
| Sidescroller/platformer tileset | MCP sidescroller tileset tools or REST v2 sidescroller tileset endpoints. | Distinct from top-down terrain and individual tile variants. |
| Individual tile variants | MCP tiles-pro tools or REST v2 tiles-pro endpoints. | This is different from a full terrain tileset. Clarify "tiles" vs "tileset" when ambiguous. |
| Isometric tile | MCP isometric tile tool or REST v2 isometric tile endpoint. | Ask whether the user wants one isometric tile or a full tileset when the wording is ambiguous. |
| General image, standalone sprite, icon, concept | REST v2 image generation. | MCP may not expose every raw image endpoint; use REST v2 for generic image primitives. |
| Background, scene, title image | REST v2 background/image generation. | Use documented `create-image-pixflux-background` for background-image generation when REST v2 is the selected surface; treat as normal image generation unless the user needs map/editor semantics. |
| UI, HUD, button, panel, menu | Use REST `/create-ui-asset` as the default structured UI asset route when REST and MCP are both available; use MCP `create_ui_asset` for MCP-first managed asset workflows; use REST `/generate-ui-v2` for loose UI images. | See [PixelLab UI Generation Surfaces Research](pixellab-ui-generation-surfaces-research.md). Website UI libraries are human/editor surfaces unless a public endpoint covers the task. |
| Image edit, inpaint, remove background, resize, convert to pixel art | REST v2 edit/transform endpoints. | Supplied images are optional unless the selected route requires image fields. For image-to-pixel-art without a requested size, prefer Pro. For fixed output size within current `output_size` limits, use normal `image-to-pixelart`. If the requested size is outside those limits, use Pro, verify dimensions, and if they differ, warn the user and ask before using PixelLab `resize` or local nearest-neighbor/canvas resize/pad/crop. |
| Multi-image edit or combine references | REST v2 `edit-images-v2` when the task is an edit with multiple source/reference images. | Aseprite's observed `generate-multi-edit` operation is an undocumented internal endpoint, not a public REST route. Use website/editor only when the user wants the visual experimental product flow. |
| Style reference or consistent-style generation | REST v2 style/reference image generation. | Use `generate-with-style-v2`, `generate-image-v2` style/reference fields, or documented image-model style fields as appropriate after checking current docs. |
| Canny/sketch, pose-guided image, depth/image-to-image | Visible website/editor/Aseprite workflow for exact Canny/Pose/Depth behavior; REST v2 only for an approximate documented image/init/reference workflow after explaining the difference and getting approval. | No exact public REST v2/MCP Canny, Pose, or Depth endpoint was documented. Observed Aseprite operation names include `generate-general-canny`, `generate-general-pose`, and `generate-pixelart-flux`; treat them as undocumented internal endpoints unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools. |
| Add VFX/effect/trail/aura to an existing sprite | REST v2 image edit. | When a target sprite/image is supplied, preserve that image and apply the effect to the same canvas. Generate a separate object/effect asset only when the user asks for an isolated reusable layer or no target image is supplied. |
| Reduce colors / quantize palette | Visible PixelLab website/editor, Aseprite, or Pixelorama workflow when the user wants PixelLab behavior; otherwise local image tooling after labeling it as a non-PixelLab fallback. | PixelLab website docs include Reduce Colors, but no public REST v2/MCP reduce-colors endpoint was documented. Aseprite's observed `quantize-image` operation is an undocumented internal endpoint; do not invent `/v2/quantize-image`. |
| Unzoom pixel art | Aseprite or Pixelorama extension when the user is actively in that editor; otherwise local image tooling after labeling it as a non-PixelLab fallback. | Aseprite's observed `unzoom-pixelart` operation is an undocumented internal endpoint. No public REST v2 or MCP Unzoom endpoint was documented; do not invent `/v2/unzoom-pixelart`. |
| Try on garment/item | Website Try on for single-image compositing; REST `transfer-outfit-v2` for animation-frame outfit transfer. | Do not treat either as isolated layer extraction. |
| Reshape | Website Reshape or closest documented edit/character route after checking current docs. | Website docs require exactly 64x64 canvas; no public REST v2/MCP reshape endpoint was documented. |
| Pixel correction / clean-up | Aseprite extension for exact PixelLab behavior, or closest documented REST edit/convert route after checking docs. | Aseprite's observed `correct-pixelart` operation is an undocumented internal endpoint. No public REST v2/MCP pixel-correction endpoint was documented. |
| Prompt enhancement | REST v2 matching enhance endpoint; agent-side fallback. | Low-cost prompt prep. Pick the enhancer that matches the asset type; do not use them as generic optimizers. |
| Map image or level concept | REST v2 image/background route unless the user needs Map Workshop behavior. | A visual map concept is not the same thing as a website Map Workshop project; map extension/texture flows are website workflows unless public endpoints are documented. |
| Map object | MCP map-object tool when configured; REST v2 map-object endpoint when documented. | Distinguish map objects from whole maps and terrain tilesets. MCP map objects auto-delete after 8 hours. |
| Whole map / Map Workshop project | Visible website workflow or generated component assets. | Do not invent public map CRUD/export APIs when not documented. |
| Balance, usage, async job status | MCP balance/status tools when configured; REST v2 balance/background-job endpoints for code. | Report usage/balance only when exposed by the selected route. |

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

- [Tilesets](../../skills/pixellab-pip/references/tilesets.md)
- [Paperdolling](../../skills/pixellab-pip/references/paperdolling.md)
- [Image Input Roles](../../skills/pixellab-pip/references/image-input-roles.md)
- [Usage Reporting](../../skills/pixellab-pip/references/usage-reporting.md)
- [Official PixelLab Documentation](../../skills/pixellab-pip/references/official-pixellab-documentation.md)
