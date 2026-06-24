---
name: pixellab-pip
description: Use for PixelLab or PixelLab Pip intents to setup, configure, connect, install, verify auth, create, generate, draw, make, edit, convert, animate, upscale, remove backgrounds, route, or troubleshoot pixel-art/game-asset workflows across MCP, REST/API v2, website/editor Pixelorama, Aseprite, and legacy v1. Trigger on PixelLab setup, MCP setup, API setup, PIXELLAB_SECRET, bearer-token auth, sprites, sprite sheets, characters, objects, tiles, tilesets, tilemaps, maps, UI, icons, backgrounds, palettes, image edits, animations, docs, endpoint/tool choice, SDK integration, troubleshooting, or vibe-coding. Use for generic asset wording only when the project/conversation implies PixelLab. Do not trigger for unrelated Python pip/package-manager requests or generic image/pixel-art requests with no PixelLab intent.
---

# PixelLab Pip

Classify the user's asset, API, or question intent first, then choose the supported PixelLab surface. Answer questions directly when the request is a question.

## Workflow

1. Classify the request:
   `question | setup | create asset | edit/transform | animate | prompt_enhancement | integrate/code | check balance/status | troubleshoot docs/API | website/editor assistance`.
   Treat a standalone `setup` word after an explicit skill invocation, such as `/pixellab-pip setup` or `@pixellab-pip setup`, as setup intent. If an app exposes structured arguments, use them only as another way to read the same natural-language intent.
2. Classify the target asset or surface:
   `general_image | background | character | object | effect_vfx | ui | whole_map | map_image | map_object | top_down_tileset | sidescroller_tileset | isometric_tile | tile_variants | animation | existing_image`.
3. Choose the surface:
   use PixelLab MCP for managed coding-agent assets, REST v2 for direct API/code/batch primitives, website/Aseprite/Pixelorama only as human/editor surfaces, and REST v1 only for legacy compatibility.
   For setup intent, read `references/setup.md` and run the setup wizard contract: recommend MCP + API first, support MCP-only/API-only/manual modes, and change settings only after a token-free preview and explicit approval.
4. Use MCP only if PixelLab MCP tools are available, either bare or prefixed. If MCP is unavailable, route to the matching REST v2 endpoint when one is documented. If MCP and REST v2 are both unavailable or fail, explain why before using any non-PixelLab fallback.
   If tools are prefixed, such as `mcp__pixellab__create_character`, match by suffix.
5. Refresh current facts when a needed tool/endpoint/field is missing or unclear, or when auth, SDK support, pricing, model/mode availability, or latest MCP tools matter.
6. For consistency-sensitive work, summarize the user's identity, style, palette, view, and reference anchors. Ask up to three blocking questions before a credit-spending call.
7. For PixelLab natural-language request parameters such as `description`, `action`, `*_description`, `item_descriptions`, `text`, or `color_palette`, improve vague user wording into endpoint-ready English parameter values unless the user opts out. Use a documented PixelLab enhance endpoint only when it fits the chosen route; otherwise enhance directly from the request and visible inputs. For non-English or mixed-language requests, read `references/localization.md`.
8. Before live generation, confirm the PixelLab bearer token is configured without asking the user to paste it into chat.
9. Act or answer. Ask a short clarification only for known collisions.

## Surface Rules

| Surface | Use for | Avoid |
|---|---|---|
| Hosted MCP | Workflows that need managed PixelLab assets with IDs, polling, downloads, list/get/delete helpers, and project/sandbox/agent helpers. | Raw image/edit/UI primitives that MCP does not expose, or any MCP call when PixelLab MCP tools are unavailable. |
| REST v2 | Scripts, batch jobs, server integrations, exact endpoint control, generic images, backgrounds, UI, inpaint/edit, prompt enhancement, raw animation, rotate, resize, remove background, and API parity checks. | Guessing SDK methods without checking the installed SDK or current docs. |
| Website / Map Workshop | Human product surface, full-map manual work, rich libraries, visible browser assistance, and website-only flows. | Programmatic use of copied browser session tokens or undocumented root endpoints. |
| Aseprite | Local in-editor plugin workflows when the user is actively working inside Aseprite. | Treating local plugin routes as public REST/MCP contracts. |
| Pixelorama / editor | Visible browser assistance for website editor workflows, including existing assets, save-back flows, and website-only manual flows after explicit permission. | Hidden automation, undocumented endpoint calls, public API assumptions, or any generation/save/download/edit/delete action without a second confirmation. |
| REST v1 | Existing legacy code and old SDK compatibility. | New work unless the user explicitly needs v1. |

Hosted MCP tool names are not REST endpoints. Do not curl MCP tool names as `/v2/...` paths.

## Intent Router

| User intent | Default route after Surface Rules | REST v2 route when coding/exact control is needed |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP `create_character`, then `create_character_state`, `animate_character`, `get_character`, list/delete helpers, and `delete_animation` when explicitly requested. | Character endpoints such as `create-character-v3`, `create-character-with-4-directions`, `create-character-with-8-directions`, `create-character-pro`, state, animation, tags, ZIP/list/get/delete endpoints. |
| Object, prop, item, pickup, weapon, furniture | MCP `create_1_direction_object`, `create_8_direction_object`, `create_map_object`, object state/animation/review/tag tools. | Object endpoints such as `create-1-direction-object`, `create-8-direction-object`, `map-objects`, object state/animation/tags/list/get/delete endpoints. |
| Top-down terrain tileset, Wang/autotile/RPG tileset | MCP `create_topdown_tileset`. | `create-tileset`, `tilesets`. |
| Sidescroller/platformer tileset | MCP `create_sidescroller_tileset`. | `create-tileset-sidescroller`, sidescroller tileset endpoints. |
| Isometric tile/block/floor | MCP `create_isometric_tile`. | `create-isometric-tile`. |
| Tile variants / tiles pro | MCP `create_tiles_pro` for individual tile variants such as hex, octagon, square top-down, and isometric tiles. | `create-tiles-pro`, `tiles-pro/{tile_id}`. |
| General image, sprite, icon-like standalone asset | REST v2. | `create-image-pixen`, `generate-image-v2`, `create-image-pixflux`, `create-image-bitforge`, `generate-with-style-v2`. |
| Background, scene, environment, backdrop | REST v2 image generation; no direct hosted MCP background tool was documented. | Use normal image generation with a scene/background prompt. Do not assume `create-image-pixflux-background` means a scene-backdrop generator without checking current docs. |
| UI, HUD, button, panel, health bar, menu | REST v2. | `generate-ui-v2`. Website UI library is a human/editor surface unless public lifecycle endpoints exist. |
| Image edit, inpaint, mask, convert, resize, remove background | REST v2. | `inpaint`, `inpaint-v3`, `edit-image`, `edit-images-v2`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background`. |
| Reduce colors / quantize palette | Website/editor/local image tooling. | No public REST v2/MCP reduce-colors endpoint was documented; use website docs or local tooling instead of inventing a route. |
| Unzoom pixel art / remove upscaling | Aseprite or Pixelorama extension. | Website docs list this as editor-extension only; do not route to REST/MCP unless official docs add an endpoint. |
| Try on garment/item on character | Website Try on for single-image experimental output; REST `transfer-outfit-v2` only for animation-frame outfit transfer. | Try on returns a composited image, not isolated paperdoll layers. |
| Multi image combine references | Website experimental flow or closest documented REST image/edit route after verifying docs. | No direct public REST v2/MCP "multi image" route was documented. |
| Reshape character proportions | Website Reshape or closest documented edit/character route after verifying docs. | Website docs require exactly 64x64 canvas; no public REST v2/MCP reshape endpoint was documented. |
| Prompt enhancement, improve generation prompt | Agent-side rewrite by default for unmatched routes; REST v2 only for documented matching enhance endpoints. | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, or `enhance-animation-v3-prompt`. Do not use a mismatched enhance endpoint as a generic optimizer unless the user explicitly asks. |
| Raw animation, skeleton, interpolation, outfit transfer, rotate | REST v2 unless animating a managed MCP character/object. | `animate-with-text*`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, `generate-8-rotations-v2/v3`. |
| Map image, generated level image, visual map concept | REST v2 image/background route; website for map extension/texture workflows. | No full public REST/MCP map CRUD, map extension, or map texture surface was documented. |
| Map object | MCP `create_map_object` plus `get_map_object` by default. | `POST /map-objects`; MCP map objects auto-delete after 8 hours. Verify current REST result and polling behavior from OpenAPI before writing code. |
| Whole map, Map Workshop, map CRUD/export | Website manually, or generate components with MCP/REST. | No full public REST/MCP map CRUD surface was documented in the research. |
| Static effect or VFX sprite | REST v2 image/object route depending whether it should be a reusable object. | No standalone public VFX endpoint was documented. |
| Animated effect or VFX | REST v2 raw animation or MCP object animation if it should become a managed object. | `animate-with-text-v3`, `animate-with-skeleton`, or object animation endpoints; treat VFX as a description, not a separate endpoint. |
| Balance, credits, account check | MCP `get_balance` if available. | `GET /balance`. |
| REST async job status | REST v2. | `GET /background-jobs/{job_id}`. MCP managed assets use resource-specific `get_*` tools instead. |
| PixelLab projects, sandbox, deployed agent workflows, chat, MCP help/feedback | MCP `list_projects`, `sandbox_*`, `chat_*`, `agent_help`, `agent_feedback`, `agent_list`, `agent_inspect`, and `agent_talk` tools if available. | No public REST v2 equivalent was documented. |

## Clarify Only For Collisions

- "Tiles": ask whether the user wants a terrain/autotile tileset, platformer/sidescroller tileset, or individual tile variants.
- "Map": ask whether they want a whole map, map object, map image, tileset, isometric tile, or tile variants.
- "Object/character": infer character for people, NPCs, creatures, body templates, or identity/state animation; infer object for props/items/furniture/weapons. Ask only if unclear.
- "Effect": ask static sprite or animated effect when not obvious. For static VFX, ask whether it should be a reusable managed object or a one-off sprite.
- "Isometric tileset": ask whether they need one isometric tile or a full tileset, because public docs expose a single isometric tile route.
- "Paperdoll": gather base, layers, directions, animations, and isolated-vs-composited output; see `references/paperdolling.md`.
- Supplied images are optional unless the chosen route requires image fields. When images are supplied, infer each file's endpoint-specific role from the request; ask only when one file could reasonably be identity, style, concept, edit target, mask, palette, init/source, first frame, or last frame.
- If prompt enhancement adds material inferred details from images or user shorthand, show the proposed description and get confirmation before a credit-spending generation or edit.

Read only the relevant reference:

- Bearer-token setup, PixelLab UI naming, and MCP auth reuse: `references/credentials.md`.
- Natural-language setup mode for MCP/API/auth after install: `references/setup.md`.
- Browser fallback and website automation boundaries: `references/browser-fallback.md`.
- Paperdolling and layered character workflows: `references/paperdolling.md`.
- Tileset and tile-variant details: `references/tilesets.md`.
- Attachments, file paths, supplied image roles, endpoint fields, or fixed-size image-to-pixel-art: `references/image-inputs.md`.
- Non-English or mixed-language user requests and response-language handling: `references/localization.md`.
- Official PixelLab docs, MCP docs, REST docs, and web-refresh routing: `references/official-docs.md`.
- Usage, balance, job, and result reporting: `references/usage-reporting.md`.

Optional broader docs: in full plugin/repo installs, these paths resolve relative to this `SKILL.md`; raw skill installs may omit them. If runtime `references/` are not enough, read at most one matching file if it exists. If absent, continue with `references/official-docs.md` and current official PixelLab docs; do not search or load the set.

- Surface boundaries and service selection: `../../docs/pixellab/surfaces-and-services.md`.
- Plain-language asset routing: `../../docs/pixellab/asset-routing.md`.
- Product/model/mode terminology: `../../docs/pixellab/terminology.md`.
- SDK-vs-REST compatibility: `../../docs/pixellab/sdk-compatibility.md`.
- Bearer-token, session, and security boundaries: `../../docs/pixellab/auth-and-security.md`.

## Model And Mode Terms

Treat PixelLab model/provider language as product labels unless official docs disclose more.

- `Pixen`, `PixFlux`, `BitForge`: public product/workflow labels, not guaranteed provider names.
- `PixPatch`: website-surface label; no public v2 `PixPatch` image endpoint was documented.
- `Pro`: quality/tier/mode label across many unrelated tools, not one endpoint or model.
- `v3` and `new`: workflow/version labels scoped to a selected operation, not a universal model.
- `S-XL`, `M-XL`, `S-M`, `M-L`: size/product labels, not asset intents.
- `Gemini`: observed in website Create Tileset Pro copy, but no public v2 tileset parameter was documented that exactly selects that website Pro/Gemini mode.

Do not invent provider internals where PixelLab docs are silent.

## Text Preparation

Prompt enhancement is opt-out. For natural-language request parameters such as `description`, `style_description`, `negative_description`, `lower_description`, `upper_description`, `transition_description`, `edit_description`, `action`, `action_description`, `animation_description`, `item_descriptions`, `text`, and `color_palette`, produce the best concise PixelLab-ready English value from the user's request and any visible inputs before calling a tool.

Use REST `enhance-pixen-prompt` for Pixen image prompts, `enhance-character-v3-prompt` for character v3 prompts, and `enhance-animation-v3-prompt` for animation v3 actions with `first_frame` and optional `last_frame`. For other tools, enhance directly as the agent; do not force a nonmatching enhance endpoint.

## Do Not Use

- Do not automate undocumented website/session endpoints such as root `/tilesets/create` with copied browser session tokens. Treat them as unsupported unless PixelLab documents them.
- Do not ask users to paste the PixelLab bearer token into chat. Direct them to the setup wizard, local `PIXELLAB_SECRET`, or app secret settings instead.
- Do not treat `https://api.pixellab.ai/` redirecting to v1 docs as proof that root website routes map to `/v1`.
- Do not confuse website Create Tileset Pro with public `create_tiles_pro` / `create-tiles-pro`; they are different flows.
- Do not refer to website session tokens as API tokens or PixelLab bearer tokens. Public REST/MCP bearer tokens and website session tokens are different auth contexts.
- Do not default to v1 or old SDK README examples for new work.
- Do not assume an installed SDK exposes every current v2 endpoint or parameter. Live `llms.txt` links official Python and JavaScript/TypeScript SDKs, but for exact v2 coverage confirm the installed package/docs or call REST v2 directly.
- Do not claim public SDK coverage without checking the installed package, current docs, or official repo state.

## Current Docs Refresh

Use local routing rules for stable route choice. Refresh official docs only when the local skill/reference does not contain the needed tool, endpoint, field, schema, SDK detail, auth setup, pricing/limit, model/mode claim, or latest MCP tool behavior.

Start with lightweight official docs. Fetch `openapi.json` only when exact request/response schema, enum values, required fields, or polling/result shapes are needed.

- `https://api.pixellab.ai/v2/llms.txt` for REST v2 endpoint index and auth summary
- `https://api.pixellab.ai/v2/docs` for interactive REST v2 endpoint parameters
- `https://api.pixellab.ai/v2/openapi.json` only for exact REST v2 schema checks
- `https://api.pixellab.ai/mcp/docs` for MCP tool behavior
- `https://www.pixellab.ai/mcp` for MCP setup
- `https://github.com/pixellab-code` only for official SDK/MCP repo state
- `https://api.pixellab.ai/v1/openapi.json` only for legacy checks

If web access is unavailable, answer from this skill and say only which necessary current claim could not be freshly verified.

## Answer Shape

For questions, answer with:

1. Recommended surface or endpoint/tool.
2. Why that route fits.
3. Warnings for unsupported or confusing alternatives.
4. Verification note only when the answer depends on a current fact that was missing, unclear, or not freshly verified.

For tasks, execute PixelLab generation/editing only when the user clearly requested it and both the bearer token and tooling are configured. For nontrivial live generation, prefer one candidate first, report enough route details to review it, then continue only if the user asks for more. Ask before ambiguous credit-spending batch work or destructive deletes. Refuse unsupported automation, then route to the closest documented MCP/REST option or a visible manual website flow. Create local replacement art/files only when the user explicitly asks for a local fallback or approves one after both MCP and REST/API are unavailable or fail; label the result as a non-PixelLab fallback. Otherwise provide the exact route and minimal code or call shape the user needs.

If no PixelLab bearer token is configured, stop before PixelLab generation and offer the setup wizard. Tell the user to open `https://www.pixellab.ai/account` after signing in and copy the value labeled `Secret`, then store it locally as `PIXELLAB_SECRET` or in app secret settings; never ask them to paste it into chat. If the user chooses Manual setup, open or link `https://www.pixellab.ai/mcp`, tell them to pick their app there, and stop. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. If the user requested an output asset and a local fallback is possible, offer it as a separate non-PixelLab fallback and wait for approval before creating files.

After any live PixelLab call, report the surface, tool or endpoint, prompt/description prep method, final natural-language parameter values used, key result-affecting controls such as size/view/direction/mode/seed/frame count/image roles or asset IDs, job/asset/result IDs, output paths or URLs, async polling/status when relevant, credit/balance delta when exposed, and candidate/final status. Do not call an output final unless existence and explicitly requested constraints were verified. If usage is not exposed, say so. Do not paste secrets, raw files/base64, or full response JSON unless debugging exact schemas.

Use browser automation only for visible website/editor/Pixelorama assistance after explicit user permission. Ask again before login/session actions, spending credits, submitting generations, downloads, edits, or deletes. Never scrape session tokens or call undocumented website endpoints.

## Examples

| Request | Route |
|---|---|
| "Setup PixelLab." | Setup mode; diagnose MCP/API intent, credential readiness, and ask before config writes. |
| "Make a wizard with idle and walk animations." | MCP `create_character`, then `animate_character`. |
| "Generate a mossy platformer tileset from code." | REST v2 `create-tileset-sidescroller`; use MCP `create_sidescroller_tileset` if working in an MCP-enabled agent. |
| "Create a title screen background." | REST v2 image generation with a scene/background prompt; verify the current endpoint and size support from docs. |
| "Make HUD buttons and a health bar." | REST v2 `generate-ui-v2`. |
| "Convert this image to pixel art and remove the background." | REST v2 `image-to-pixelart-pro`, then `remove-background`. |
| "Inpaint this masked area." | REST v2 `inpaint` or `inpaint-v3` after checking current docs and inputs. |
| "Make an 8-direction treasure chest object." | MCP `create_8_direction_object`; REST v2 `create-8-direction-object` for code. |
| "Make hex terrain tiles." | MCP `create_tiles_pro`, not top-down Wang tileset. |
| "Use `/tilesets/create` with my browser token." | Do not use it; route to public MCP/REST tileset tools or manual website use. |
| "What does Pro use?" | Explain only documented/product-level facts; do not infer provider internals. Refresh official docs if current model/mode details matter. |
