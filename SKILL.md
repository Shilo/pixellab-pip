---
name: pixellab-agent
description: Route and answer PixelLab game-asset requests across MCP, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1. Use when creating, editing, animating, generating, integrating, troubleshooting, or choosing PixelLab tools/endpoints for characters, objects, tilesets, tiles, maps, UI, backgrounds, image edits, animations, SDKs, API auth, MCP setup, or vibe-coding.
---

# PixelLab Agent

Use this skill as a PixelLab routing brain. Classify the user's asset or API intent first, then choose the supported PixelLab surface. Answer questions directly when the request is a question.

## Workflow

1. Classify the request:
   `question | create asset | edit/transform | animate | prompt_enhancement | integrate/code | check balance/status | troubleshoot docs/API | automate website/editor`.
2. Classify the target asset or surface:
   `general_image | background | character | object | effect_vfx | ui | whole_map | map_image | map_object | top_down_tileset | sidescroller_tileset | isometric_tile | tile_variants | animation | existing_image`.
3. Choose the surface:
   use hosted MCP for managed coding-agent assets, REST v2 for direct API/code/batch primitives, website/Aseprite/Pixelorama only as human/editor surfaces, and REST v1 only for legacy compatibility.
4. Use MCP only if the current agent actually exposes PixelLab MCP tools, either bare or prefixed. If not, say MCP is not configured and offer setup, or REST v2 code only when the user asks for direct API/code.
5. Refresh current facts when exact endpoint names, parameters, auth, SDK support, pricing, model/mode availability, or latest MCP tools matter.
6. Before live generation, confirm the single PixelLab account credential is configured without asking the user to paste it into chat.
7. Act or answer. Ask a short clarification only for known collisions.

## Surface Rules

| Surface | Use for | Avoid |
|---|---|---|
| Hosted MCP | Workflows that need managed PixelLab assets with IDs, polling, downloads, list/get/delete helpers, and project/sandbox/agent helpers. | Raw image/edit/UI primitives that MCP does not expose, or any MCP call when tools are not available in the current agent. |
| REST v2 | Scripts, batch jobs, server integrations, exact endpoint control, generic images, backgrounds, UI, inpaint/edit, prompt enhancement, raw animation, rotate, resize, remove background, and API parity checks. | Guessing SDK methods without checking the installed SDK or current docs. |
| Website / Map Workshop | Human product surface, full-map manual work, rich libraries, visible browser assistance, and website-only flows. | Programmatic use of copied browser session tokens or undocumented root endpoints. |
| Aseprite | Local in-editor plugin workflows when the user is actively working inside Aseprite. | Treating local plugin routes as public REST/MCP contracts. |
| Pixelorama / editor | Browser editor for existing website assets and save-back through `replace-png` routes. | New asset generation or public automation. |
| REST v1 | Existing legacy code and old SDK compatibility. | New work unless the user explicitly needs v1. |

Hosted MCP tool names are not REST endpoints. Do not curl MCP tool names as `/v2/...` paths.

## Intent Router

| User intent | Default route | REST v2 route when coding/exact control is needed |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP `create_character`, then `create_character_state`, `animate_character`, `get_character`, list/delete helpers as needed. | Character endpoints such as `create-character-v3`, 4/8-direction character endpoints, `create-character-pro`, state, animation, tags, ZIP/list/get/delete endpoints. |
| Object, prop, item, pickup, weapon, furniture | MCP `create_1_direction_object`, `create_8_direction_object`, `create_map_object`, object state/animation/review tools. | Object endpoints such as `create-1-direction-object`, `create-8-direction-object`, `map-objects`, object state/animation/list/get/delete endpoints. |
| Top-down terrain tileset, Wang/autotile/RPG tileset | MCP `create_topdown_tileset`. | `create-tileset`, `tilesets`. |
| Sidescroller/platformer tileset | MCP `create_sidescroller_tileset`. | `create-tileset-sidescroller`, sidescroller tileset endpoints. |
| Isometric tile/block/floor | MCP `create_isometric_tile`. | `create-isometric-tile`. |
| Tile variants / tiles pro | MCP `create_tiles_pro` for individual tile variants such as hex, octagon, square top-down, and isometric tiles. | `create-tiles-pro`, `tiles-pro/{tile_id}`. |
| General image, sprite, icon-like standalone asset | REST v2. | `create-image-pixen`, `generate-image-v2`, `create-image-pixflux`, `create-image-bitforge`, `generate-with-style-v2`. |
| Background, scene, environment, backdrop | REST v2; no direct hosted MCP background tool was documented. | `create-image-pixflux-background` or normal image generation with background in the prompt. |
| UI, HUD, button, panel, health bar, menu | REST v2. | `generate-ui-v2`. Website UI library is a human/editor surface unless public lifecycle endpoints exist. |
| Image edit, inpaint, mask, convert, resize, remove background | REST v2. | `inpaint`, `inpaint-v3`, `edit-image`, `edit-images-v2`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background`. |
| Prompt enhancement, improve generation prompt | REST v2. | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, or `enhance-animation-v3-prompt` depending on target asset. |
| Raw animation, skeleton, interpolation, outfit transfer, rotate | REST v2 unless animating a managed MCP character/object. | `animate-with-text*`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, `generate-8-rotations-v2/v3`. |
| Map image, generated level image, visual map concept | REST v2 image/background route. | No full public REST/MCP map CRUD surface was documented. |
| Map object | MCP `create_map_object` plus `get_map_object` by default. | `POST /map-objects`; verify current result and polling behavior from OpenAPI before writing code. |
| Whole map, Map Workshop, map CRUD/export | Website manually, or generate components with MCP/REST. | No full public REST/MCP map CRUD surface was documented in the research. |
| Static effect or VFX sprite | REST v2 image/object route depending whether it should be a reusable object. | No standalone public VFX endpoint was documented. |
| Animated effect or VFX | REST v2 raw animation or MCP object animation if it should become a managed object. | Use animation endpoints; treat VFX as an option/description, not a separate public model. |
| Balance, credits, account check | MCP `get_balance` if available. | `GET /balance`. |
| REST async job status | REST v2. | `GET /background-jobs/{job_id}`. MCP managed assets use resource-specific `get_*` tools instead. |
| PixelLab projects, sandbox, agent workflows, chat | MCP `list_projects`, `sandbox_*`, `agent_*`, and `chat_*` tools if available. | No public REST v2 equivalent was documented. |

## Clarify Only For Collisions

- "Tiles": ask whether the user wants a terrain/autotile tileset, platformer/sidescroller tileset, or individual tile variants.
- "Map": ask whether they want a whole map, map object, map image, tileset, isometric tile, or tile variants.
- "Object/character": infer character for people, NPCs, creatures, body templates, or identity/state animation; infer object for props/items/furniture/weapons. Ask only if unclear.
- "Effect": ask static sprite or animated effect when not obvious. For static VFX, ask whether it should be a reusable managed object or a one-off sprite.
- "Isometric tileset": ask whether they need one isometric tile or a full tileset, because public docs expose a single isometric tile route.
- "Paperdoll": ask for base character, layers, directions, animation list, and whether outputs must be isolated layers or composited previews. Preserve canvas, frame count/order, origin, transparency, and palette; warn that text-only output can drift.
- Supplied images: infer role from the request, but ask when one file could be identity, style, concept, edit target, palette, pose, first frame, or last frame. Check current endpoint schema before choosing parameter names or base64 shape.

Read only the relevant reference:

- Credential naming (`API key`, `API token`, `bearer token`, `secret`) and MCP credential reuse: `references/credentials.md`.
- Browser fallback and website automation boundaries: `references/browser-fallback.md`.
- Paperdolling and layered character workflows: `references/paperdolling.md`.
- Tileset and tile-variant details: `references/tilesets.md`.
- Image inputs, user goals, and attachment/file-path handling: `references/image-inputs.md`.
- Official PixelLab docs, MCP docs, REST docs, and web-refresh routing: `references/official-docs.md`.
- Usage, balance, job, and result reporting: `references/usage-reporting.md`.

## Model And Mode Terms

Treat PixelLab model/provider language as product labels unless official docs disclose more.

- `Pixen`, `PixFlux`, `BitForge`, `PixPatch`: public product/workflow labels, not guaranteed provider names.
- `Pro`: quality/tier/mode label across many unrelated tools, not one endpoint or model.
- `v3` and `new`: workflow/version labels scoped to a selected operation, not a universal model.
- `S-XL`, `M-XL`, `S-M`, `M-L`: size/product labels, not asset intents.
- `Gemini`: observed in website Create Tileset Pro copy, but no public v2 tileset parameter was documented that exactly selects that website Pro/Gemini mode.

Do not invent provider internals where PixelLab docs are silent.

## Do Not Use

- Do not automate undocumented website/session endpoints such as root `/tilesets/create` with copied DevTools bearer tokens. Treat them as unsupported unless PixelLab documents them.
- Do not ask users to paste the PixelLab account credential into chat. Direct them to local environment or MCP secret setup instead.
- Do not treat `https://api.pixellab.ai/` redirecting to v1 docs as proof that root website routes map to `/v1`.
- Do not confuse website Create Tileset Pro with public `create_tiles_pro` / `create-tiles-pro`; they are different flows.
- Do not call website session bearer tokens API tokens. Public REST/MCP bearer tokens and website session tokens are different auth contexts.
- Do not default to v1 or old SDK README examples for new work.
- Do not assume `pip install pixellab` or `npm install @pixellab-code/pixellab` gives v2 coverage. The published/default SDKs have historically defaulted to v1; confirm the installed package or call REST v2 directly.
- Do not claim public SDK coverage without checking the installed package or current official repo state.

## Current Docs Refresh

Use local routing rules for stable judgment. Check official docs before exact current claims or code:

- `https://api.pixellab.ai/mcp/docs`
- `https://api.pixellab.ai/v2/llms.txt`
- `https://api.pixellab.ai/v2/docs`
- `https://api.pixellab.ai/v2/openapi.json`
- `https://www.pixellab.ai/mcp`
- `https://github.com/pixellab-code` for official SDK/MCP repo state
- `https://api.pixellab.ai/v1/openapi.json` only for legacy checks

If web access is unavailable, answer from this skill and say which current claim was not freshly verified.

## Answer Shape

For questions, answer with:

1. Recommended surface or endpoint/tool.
2. Why that route fits.
3. Warnings for unsupported or confusing alternatives.
4. Official-doc caveat when the answer was not freshly verified.

For tasks, execute generation/editing only when the user clearly requested it and credentials/tooling are configured. Ask before ambiguous credit-spending batch work, destructive deletes, or unsupported automation. Otherwise provide the exact route and minimal code or call shape the user needs.

If no PixelLab account credential is configured, stop before generation and tell the user to configure the single credential locally as `PIXELLAB_SECRET` or through agent/MCP secret config. PixelLab surfaces may call the same value an API key, API token, bearer token, or secret; these are product labels, not separate credentials. Never request the credential value in chat.

After any live PixelLab call, report the surface, tool or endpoint, mode/model label if supplied, job/asset/result IDs, output paths or URLs, async polling/status when relevant, and credit/balance delta when exposed. If usage is not exposed, say so.

Use browser automation only for visible website assistance after explicit user permission. Ask again before login/session actions, spending credits, submitting generations, downloads, or edits. Never scrape session tokens or call undocumented website endpoints.

## Examples

| Request | Route |
|---|---|
| "Make a wizard with idle and walk animations." | MCP `create_character`, then `animate_character`. |
| "Generate a mossy platformer tileset from code." | REST v2 `create-tileset-sidescroller`; use MCP `create_sidescroller_tileset` if working inside an MCP-enabled agent. |
| "Create a 512x512 title screen background." | REST v2 `create-image-pixflux-background` or another current image endpoint verified from docs. |
| "Make HUD buttons and a health bar." | REST v2 `generate-ui-v2`. |
| "Convert this image to pixel art and remove the background." | REST v2 `image-to-pixelart` or Pro variant, then `remove-background`. |
| "Inpaint this masked area." | REST v2 `inpaint` or `inpaint-v3` after checking current docs and inputs. |
| "Make an 8-direction treasure chest object." | MCP `create_8_direction_object`; REST v2 `create-8-direction-object` for code. |
| "Make hex terrain tiles." | MCP `create_tiles_pro`, not top-down Wang tileset. |
| "Use `/tilesets/create` with my browser token." | Do not use it; route to public MCP/REST tileset tools or manual website use. |
| "What does Pro use?" | Explain only documented/product-level facts; do not infer provider internals. Refresh official docs if current model/mode details matter. |
