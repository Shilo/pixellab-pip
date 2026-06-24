# PixelLab Asset Routing

Last reviewed: 2026-06-23.

Purpose: map plain-language asset requests to the PixelLab workflow family most likely to satisfy the user without asking them to know PixelLab's internal product vocabulary.

PixelLab requests usually start as plain asset goals: "make a character," "generate a tileset," "edit this sprite," or "create UI." Pip should classify the asset intent first, then choose the PixelLab surface and endpoint/tool family.

Use this as routing guidance, not as a frozen schema. Refresh official docs for exact current parameters, result shapes, model/mode availability, pricing, and SDK coverage.

## Asset Intent Map

| User intent | Preferred route | Notes |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP character tools when configured; REST v2 character endpoints for code or exact control. | Character workflows often involve identity, directions, states, animations, and managed asset IDs. |
| Character state or outfit/layer change | MCP character-state tools when available; REST v2 state/edit routes when exact control is needed. | Clarify whether the output should preserve identity, change pose/state, or generate a new design. |
| Character animation | MCP animation tools for managed characters; REST v2 animation endpoints for direct API use. | Ask only when animation type, direction, frame count, or source asset is unclear. |
| Object, prop, pickup, weapon, furniture | MCP object tools when configured; REST v2 object endpoints for code or exact control. | Infer object for props/items/furniture/weapons; infer character for beings with identity or body animation. |
| Object animation or object state | MCP object animation/state tools when available; REST v2 object animation/state endpoints for direct API use. | Treat reusable objects differently from one-off generated images. |
| Top-down terrain tileset | MCP top-down tileset tools or REST v2 tileset endpoints. | Usually means terrain/autotile/Wang-style tileset. |
| Sidescroller/platformer tileset | MCP sidescroller tileset tools or REST v2 sidescroller tileset endpoints. | Distinct from top-down terrain and individual tile variants. |
| Individual tile variants | MCP tiles-pro tools or REST v2 tiles-pro endpoints. | This is different from a full terrain tileset. Clarify "tiles" vs "tileset" when ambiguous. |
| Isometric tile | MCP isometric tile tool or REST v2 isometric tile endpoint. | Ask whether the user wants one isometric tile or a full tileset when the wording is ambiguous. |
| General image, standalone sprite, icon, concept | REST v2 image generation. | MCP may not expose every raw image endpoint; use REST v2 for generic image primitives. |
| Background, scene, title image | REST v2 background/image generation. | Treat as image generation unless the user needs map/editor semantics. |
| UI, HUD, button, panel, menu | REST v2 UI generation. | Website UI libraries are human/editor surfaces unless a public endpoint covers the task. |
| Image edit, inpaint, remove background, resize, convert to pixel art | REST v2 edit/transform endpoints. | Supplied images are optional unless the selected route requires image fields. For image-to-pixel-art without a requested size, prefer Pro. For fixed output size within current `output_size` limits, use normal `image-to-pixelart`. If the requested size is outside those limits, use Pro, verify dimensions, and if they differ, warn the user and ask before using PixelLab `resize` or local nearest-neighbor/canvas resize/pad/crop. |
| Add VFX/effect/trail/aura to an existing sprite | REST v2 image edit. | When a target sprite/image is supplied, preserve that image and apply the effect to the same canvas. Generate a separate object/effect asset only when the user asks for an isolated reusable layer or no target image is supplied. |
| Reduce colors / quantize palette | Website/editor/local image tooling. | No public REST v2/MCP reduce-colors endpoint was documented. |
| Unzoom pixel art | Aseprite or Pixelorama extension. | Website docs list this as extension-only. |
| Try on garment/item | Website Try on for single-image compositing; REST `transfer-outfit-v2` for animation-frame outfit transfer. | Do not treat either as isolated layer extraction. |
| Multi image | Website experimental flow or closest documented REST image/edit route after checking current docs. | No direct public REST v2/MCP "multi image" route was documented. |
| Reshape | Website Reshape or closest documented edit/character route after checking current docs. | Website docs require exactly 64x64 canvas; no public REST v2/MCP reshape endpoint was documented. |
| Prompt enhancement | REST v2 prompt enhancement endpoints. | Pick the enhancer that matches the asset type when documented. |
| Map image or level concept | REST v2 image/background route unless the user needs Map Workshop behavior. | A visual map concept is not the same thing as a website Map Workshop project; map extension/texture flows are website workflows unless public endpoints are documented. |
| Map object | MCP map-object tool when configured; REST v2 map-object endpoint when documented. | Distinguish map objects from whole maps and terrain tilesets. MCP map objects auto-delete after 8 hours. |
| Whole map / Map Workshop project | Visible website workflow or generated component assets. | Do not invent public map CRUD/export APIs when not documented. |
| Balance, usage, async job status | MCP balance/status tools when configured; REST v2 balance/background-job endpoints for code. | Report usage/balance only when exposed by the selected route. |

## Clarify Only For Real Collisions

Ask a short clarification when one phrase maps to multiple PixelLab workflows:

- `tiles`: terrain tileset, sidescroller tileset, isometric tile, or tile variants.
- `map`: whole map, map image, map object, tilemap, tileset, or Map Workshop project.
- `object`: prop/item/furniture/weapon vs a character-like being.
- `effect`: static sprite vs animated effect, and reusable object vs one-off image.
- `edit this`: edit target, style reference, identity reference, mask, first frame, or last frame.

Avoid asking for clarification when the normal game-asset meaning is obvious.

## Image Inputs

Text-only requests are valid for many PixelLab generation routes. Do not ask for images just because the user wants an asset.

When images are supplied, infer each file's role from the request and the selected endpoint. Common roles include style reference, identity/reference image, concept image, edit target, mask, palette/color reference, init/source image, first frame, or last frame.

## Runtime Reference Links

For detailed execution rules used by the skill, see:

- [Tile and tileset routing](../../skills/pixellab-pip/references/tilesets.md)
- [Paperdolling and layered character workflows](../../skills/pixellab-pip/references/paperdolling.md)
- [Image input roles](../../skills/pixellab-pip/references/image-inputs.md)
- [Usage and result reporting](../../skills/pixellab-pip/references/usage-reporting.md)
- [Official docs refresh rules](../../skills/pixellab-pip/references/official-docs.md)
