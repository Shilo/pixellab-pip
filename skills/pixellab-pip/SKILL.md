---
name: pixellab-pip
description: Use for PixelLab/Pip setup, auth, MCP/API routing, asset generation, editing, animation, skeleton/template/preset animations, docs/troubleshooting, bark completion sounds, and explicit PixelLab cost/budget/credit questions across MCP, REST v2/API, website/editor Pixelorama, Aseprite, and legacy v1. Trigger only when PixelLab context is present, including PixelLab setup, MCP/API setup, PIXELLAB_SECRET, bearer-token auth, PixelLab sprites, sprite sheets, characters, objects, tiles, tilesets, tilemaps, maps, UI, icons, backgrounds, palettes, image edits, animations, skeletons, template animations, preset animations, endpoint choice, SDK integration, troubleshooting, or PixelLab credits/cost/budget. Do not trigger for unrelated Python pip/package-manager requests or generic image/pixel-art requests with no PixelLab intent.
---

# PixelLab Pip

Classify the user's asset, API, or question intent first, then choose the supported PixelLab surface. Answer questions directly when the request is a question.

## Workflow

1. Classify the primary request plus any modifiers; values are not mutually exclusive, such as `animate + cost_sensitive`:
   `question | setup | bark | create asset | edit/transform | animate | prompt_enhancement | cost_sensitive | integrate/code | check balance/status | troubleshoot docs/API | website/editor assistance | aseprite_integration`.
   Treat a standalone `setup` word after an explicit skill invocation, such as `/pixellab-pip setup` or `@pixellab-pip setup`, as setup intent. If an app exposes structured arguments, use them only as another way to read the same natural-language intent.
   Treat a standalone `bark` word after an explicit skill invocation, with optional `on` or `off`, as bark intent. For bark intent, read `references/bark.md` and apply the persistent toggle contract.
2. Classify the target asset or surface:
   `general_image | skill_icon | item_icon | background | character | object | effect_vfx | ui | whole_map | map_image | map_object | top_down_tileset | sidescroller_tileset | isometric_tile | tile_variants | animation | preset_template_animation | skeleton_animation | existing_image`.
   Treat fitted visual additions to an existing character image, such as hair, facial features, wearables, accessories, held gear, or other body-part details, as `existing_image` edit/paperdoll requests rather than standalone `object` requests unless the user explicitly asks for a separate unattached prop sprite.
3. Choose the surface:
   use PixelLab MCP for managed coding-agent assets, REST v2 for direct API/code/batch primitives, website/Aseprite/Pixelorama only as human/editor surfaces, and REST v1 only for legacy compatibility. For preset skeleton/template animations on managed characters, read `references/preset-skeleton-template-animations.md`: prefer MCP `animate_character` when visible, even if a REST bearer token exists, and fall back to REST v2 `/characters/animations` when MCP is unavailable or exact API/code control is requested.
   When the user explicitly asks for Aseprite handling, route to `references/aseprite-cli.md`; use PixelLab MCP/REST for generation and documented Aseprite CLI/Lua only for local workspace, existing-file import/export, packaging, or launch behavior.
   For setup intent, read `references/setup.md` and run the setup wizard contract: recommend MCP + API first, support MCP-only/API-only/manual modes, and change settings only after a token-free preview and explicit approval.
4. Use MCP only if PixelLab MCP tools are visible as callable tools in the current agent runtime, either bare or prefixed. If the user explicitly asked to use MCP, do not silently fall back; report that MCP tools are unavailable and offer setup or an approved REST v2 fallback. For generic PixelLab asset requests, if MCP is unavailable, route to the matching REST v2 endpoint when one is documented. If MCP and REST v2 are both unavailable or fail, explain why before using any non-PixelLab fallback.
   If tools are prefixed, such as `mcp__pixellab__create_character`, match by suffix.
   PixelLab asset rule: every pixel of the requested art must originate from PixelLab or the user. Local tools may read, download, assemble, package, import/export, preview, verify, mask, pad, crop, resize, and format-convert those files. Do not draw, repaint, or synthesize requested content locally unless the user explicitly requests or approves a labeled non-PixelLab fallback. Do not bake a colored, checkerboard, white, black, green-screen, matte, or other background into transparent PixelLab/user frames for final outputs, final GIFs, spritesheets, thumbnails, or report images unless the user explicitly asks for that background. Checkerboard previews are allowed only as clearly labeled inspection/QA aids, separate from final deliverables, and must not be presented as the final asset.
   Do not post-process original PixelLab outputs into a claimed final asset unless the user explicitly asks or approves. Local crop/split/format work for inspection, packaging, or separate files is allowed when it preserves original pixels and is reported honestly; resizing, reassembling, unapproved compositing, repainting, or otherwise fixing failed outputs locally must not be called final without user approval.
   Exception: when a PixelLab request used `no_background: true` but the output still has a background, read `references/background-removal.md` and attempt safe background removal when verification shows the background is removable without changing the requested art.
   Save downloaded PixelLab generations, derived previews, manifests, packages, and generated workspace files under a project/workspace `pixellab-pip/` folder by default. Use another output directory only when the user explicitly states one or approves it. Generate only the output formats the user requested or the minimal standard artifacts needed for the route, such as original frames and a spritesheet for animation. Do not create APNG, alternate animated formats, extra preview formats, or viewer-convenience derivatives unless the user explicitly asks for them.
5. Refresh current facts when a needed tool/endpoint/field is missing or unclear, or when auth, SDK support, pricing, model/mode availability, or latest MCP tools matter.
6. For consistency-sensitive work, summarize the user's identity, style, palette, view, and reference anchors. Ask up to three blocking questions before a credit-spending call.
7. For PixelLab natural-language request parameters such as `description`, `action`, `*_description`, `item_descriptions`, `text`, or `color_palette`, improve vague user wording into endpoint-ready English parameter values unless the user opts out. Use a matching PixelLab prompt-enhancement endpoint when it fits the chosen route; otherwise enhance directly from the request and visible inputs. For non-English or mixed-language requests, read `references/localization.md`.
8. For animation routes, preserve the user's requested frame count when provided; otherwise use the endpoint or template default. Exception: for preset/template character animations, do not pass `frame_count`; choose a matching template id such as `walk-4-frames`, `walk-6-frames`, or `walk-8-frames`, or clarify/fallback to v3 custom mode if no matching template exists. Preserve PixelLab's returned frame order in previews and spritesheets; do not create ping-pong, reversed, duplicated, trimmed, or otherwise reordered outputs unless the user explicitly asks for that playback style.
   For transparent animation frames, final previews and spritesheets must preserve transparency. Do not add green-screen or any other matte/background to make transparency visible in a final deliverable. If visual QA needs contrast, a checkerboard inspection preview is acceptable only when clearly labeled as inspection-only and kept separate from the final transparent frames/GIF/spritesheet.
9. If the user asks for cheap, affordable, low-cost, budget, fewer credits, cheapest, or minimizing generations, read `references/cost-routing.md` before choosing a paid route. Prefer documented low-cost routes such as standard, `new`, v3, Pixen, PixFlux, or other non-Pro routes when they satisfy the request, but do not route by label alone because labels are surface-specific. Avoid Pro and Pro Tools routes unless no low-cost route fits or the user approves the cost/quality tradeoff after you name it. In cost-sensitive mode, ask before any extra paid iteration, retry, regeneration, comparison candidate, or batch expansion unless the user already approved a concrete budget, candidate count, or attempt count; include cost so far when asking.
10. Before live generation, confirm the PixelLab bearer token is configured without asking the user to paste it into chat.
11. Act or answer. Ask a short clarification only for known collisions.

## Surface Rules

| Surface | Use for | Avoid |
|---|---|---|
| Hosted MCP | Workflows that need managed PixelLab assets with IDs, polling, downloads, list/get/delete helpers, and project/sandbox/agent helpers, including MCP `create_ui_asset` when visible. | Raw image/edit primitives that MCP does not expose, REST-only UI controls such as `style_image` or `project_id`, or any MCP call when PixelLab MCP tools are unavailable. |
| REST v2 | Scripts, batch jobs, server integrations, exact endpoint control, generic images, backgrounds, UI, inpaint/edit, prompt enhancement, raw animation, rotate, resize, remove background, and API parity checks. | Guessing SDK methods without checking the installed SDK or current docs. |
| Website / Map Workshop | Human product surface, full-map manual work, rich libraries, visible browser assistance, and website-only flows. | Programmatic use of copied browser session tokens or undocumented internal endpoints used by first-party surfaces. |
| Aseprite | Local in-editor plugin workflows when the user is actively working inside Aseprite. | Treating private first-party editor integration endpoints as public REST/MCP contracts. |
| Aseprite CLI integration | Explicit Aseprite handling such as opening output in Aseprite, creating or updating `.aseprite` workspaces, importing generated frames as layers/frames/tags, and exporting through documented Aseprite CLI/Lua after PixelLab MCP/REST has produced files. | Mouse/OCR UI automation, hidden control of the PixelLab Aseprite extension, or claiming extension-private operations are public APIs. |
| Pixelorama / editor | Visible browser assistance for website editor workflows, including existing assets, save-back flows, and website-only manual flows after explicit permission. | Hidden automation, undocumented endpoint calls, public API assumptions, or any generation/save/download/edit/delete action without a second confirmation. |
| REST v1 | Existing legacy code and old SDK compatibility. | New work unless the user explicitly needs v1. |

Hosted MCP tool names are not REST endpoints. Do not curl MCP tool names as `/v2/...` paths.

## Intent Router

| User intent | Default route after Surface Rules | REST v2 route when coding/exact control is needed |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP `create_character`, then `create_character_state`, `animate_character`, `get_character`, list/delete helpers, and `delete_animation` when explicitly requested. For a follow-up animation on an existing multi-direction character, default to `south` (down-facing) for the first candidate when the user does not specify direction; ask or get confirmation before animating all directions. | Character endpoints such as `create-character-v3`, `create-character-with-4-directions`, `create-character-with-8-directions`, `create-character-pro`, state, animation, tags, ZIP/list/get/delete endpoints. |
| Inventory item icon, item icon sheet, equipment icon, loot icon, pickup icon, or transparent RPG inventory set | Read `references/item-icons.md` before choosing an endpoint or generating. | Use the reference for REST v2 route choice, transparent-background handling, sheet sizing, prompt wording, anti-patterns, and verification. |
| Standalone object, prop, pickup, weapon, furniture that is not an icon or icon sheet | MCP `create_1_direction_object`, `create_8_direction_object`, `create_map_object`, object state/animation/review tools. | Object endpoints such as `create-1-direction-object`, `create-8-direction-object`, `map-objects`, object state/animation/tags/list/get/delete endpoints. |
| Top-down terrain tileset, Wang/autotile/RPG tileset | MCP `create_topdown_tileset`. | `create-tileset`, `tilesets`. |
| Sidescroller/platformer tileset | MCP `create_sidescroller_tileset`. | `create-tileset-sidescroller`, sidescroller tileset endpoints. |
| Isometric tile/block/floor | MCP `create_isometric_tile`. | `create-isometric-tile`. |
| Tile variants / tiles pro | MCP `create_tiles_pro` for individual tile variants such as hex, octagon, square top-down, and isometric tiles. | `create-tiles-pro`, `tiles-pro/{tile_id}`. |
| Skill icon, ability icon, spell icon, action-bar icon, hotbar icon, or icon set for a skill tree/ability tree | Read `references/skill-icons.md` before choosing an endpoint or generating. | Use the reference for REST v2 route choice, background handling, sheet sizing, prompt wording, anti-patterns, and verification. |
| General image, sprite, icon-like standalone asset that is not a skill/ability/spell/action-bar/hotbar/inventory-item icon | REST v2. | `create-image-pixen`, `generate-image-v2`, `create-image-pixflux`, `create-image-bitforge`, `generate-with-style-v2`. |
| Background, scene, environment, backdrop | REST v2 image generation; no direct hosted MCP background tool was documented. | Use the documented `create-image-pixflux-background` endpoint for background-image generation when REST v2 is the selected surface; verify current size and field support from official docs before writing exact code. |
| UI, HUD, button, panel, health bar, menu | Prefer REST v2 `/create-ui-asset` for structured/saved UI assets, panels, windows, HUD pieces, shape `pieces`, named `elements`, `style_image`, `project_id`, or exact schema control. Use MCP `create_ui_asset` when the user is in an MCP-first workflow and the visible tool has the needed fields. Use REST `/generate-ui-v2` for loose/raw UI images such as a standalone button, slot, bar, or dialogue-box image, especially when `concept_image` should guide the design. | `create-ui-asset` for structured UI assets; `generate-ui-v2` for loose UI images. Do not route shape-piece/layout requests to `generate-ui-v2`. Website UI libraries are human/editor surfaces unless public lifecycle endpoints exist. |
| Image edit, inpaint, mask, convert, resize, remove background | REST v2. | `inpaint`, `inpaint-v3`, `edit-image`, `edit-images-v2`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background`. |
| Fitted paperdoll addition on an existing character image | Treat as an `existing_image` edit anchored on the base character frame, then read `references/paperdolling.md` before choosing layer/composite outputs. At this level, keep fitted additions character-anchored, distinguish editor-native layers from separate transparent image layer files, and prompt with character identity, direction, target body region, placement, rotation/facing, occlusion, and preservation rules. | Do not use `create_map_object` or standalone object generation for fitted paperdoll layers unless the user explicitly asks for an unattached prop. Public REST/MCP image edits are not editor layer workflows; only call a result a layer after the paperdoll reference's verification rules pass. |
| Style reference or consistent-style image creation | REST v2. | Use `generate-with-style-v2`, `generate-image-v2` style/reference fields, or documented image-model style fields as appropriate after checking current docs. |
| Editor-only utilities such as Canny/Pose/Depth, reduce colors, unzoom, pixel correction, and reshape | Use visible website/editor/Aseprite/Pixelorama workflow when the user wants exact PixelLab editor behavior; otherwise use the closest documented REST route or a labeled local fallback only after explaining the difference. Read `references/editor-only-utilities.md` before giving exact route advice. | No public REST v2/MCP route was documented for the exact editor-only utility behaviors. Do not invent `/v2/...` routes or automate first-party internal endpoints. |
| Try on garment/accessory on character | Website Try on for single-image experimental output; REST `transfer-outfit-v2` only for animation-frame outfit transfer. | Try on returns a composited image, not isolated paperdoll layers. |
| Multi image combine references or edit multiple source images | REST v2 for documented multi-image edit; website/editor for visual experimental flows. | Use `edit-images-v2` when the task is an image edit with multiple source/reference images. Aseprite's observed `generate-multi-edit` operation is an undocumented internal endpoint, not a public REST route. |
| Prompt enhancement, improve generation prompt | REST v2 matching enhance endpoint; agent-side fallback. | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, or `enhance-animation-v3-prompt`. Do not use a mismatched enhancer as a generic optimizer unless the user explicitly asks. |
| Preset skeleton animation, template animation, built-in character animation, or named managed character motion such as walk/idle/jump/bark | Read `references/preset-skeleton-template-animations.md`. Prefer MCP `animate_character` on a managed character with `template_animation_id` and explicit `directions`; use MCP `create_character` first when creating a new managed character. Use REST v2 fallback only when MCP is unavailable, exact API/code control is requested, or the user is integrating outside an MCP-capable agent. | `POST /characters/animations` or `POST /animate-character` with `mode="template"` and `template_animation_id`. Do not call website root `/generate-animation/background` or Aseprite extension `generate-animation` internals. |
| Raw animation, skeleton, interpolation, outfit transfer, rotate | REST v2 unless animating a managed MCP character/object. Read `references/animation.md` for frame anchors, idle-loop risk, preview verification, and outfit/frame constraints. | `animate-with-text*`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, `generate-8-rotations-v2/v3`. For 4 rotations, use current documented rotate/8-rotation routes or editor workflow; no public REST v2 4-rotation route was documented. |
| Map image, generated level image, visual map concept | REST v2 image/background route; website or Aseprite for map extension/texture workflows. | No full public REST/MCP map CRUD, map extension, or map texture surface was documented. Do not treat undocumented internal endpoints used by first-party surfaces as public REST. |
| Map object | MCP `create_map_object` plus `get_map_object` by default; download or persist MCP map-object results promptly because they auto-delete after 8 hours. | `POST /map-objects`; verify current REST result and polling behavior from OpenAPI before writing code. |
| Whole map, Map Workshop, map CRUD/export | Website manually, or generate components with MCP/REST. | No full public REST/MCP map CRUD surface was documented in the research. |
| Static effect or VFX sprite | REST v2 image/edit route. When a target sprite/image is supplied and the user asks to add, draw, overlay, or apply an effect/trail/aura/impact, treat the supplied image as the edit target and use REST image edit. Use object/image generation only when the user asks for a separate reusable effect asset/layer or no target image is supplied. | No standalone public VFX endpoint was documented. PixelLab edit routes return a whole edited image, not an isolated effect layer. |
| Animated effect or VFX | REST v2 raw animation or MCP object animation if it should become a managed object. | `animate-with-text-v3`, `animate-with-skeleton`, or object animation endpoints; treat VFX as a description, not a separate endpoint. |
| Balance, credits, account check | MCP `get_balance` if available. | `GET /balance`. |
| REST async job status | REST v2. | `GET /background-jobs/{job_id}`. MCP managed assets use resource-specific `get_*` tools instead. |
| PixelLab projects, sandbox, deployed agent workflows, chat, MCP help/feedback | MCP `list_projects`, `sandbox_*`, `chat_*`, `agent_help`, `agent_feedback`, `agent_list`, `agent_inspect`, and `agent_talk` tools if available. | No public REST v2 equivalent was documented. |

## Clarify Only For Collisions

- "Tiles": ask whether the user wants a terrain/autotile tileset, platformer/sidescroller tileset, or individual tile variants.
- "Map": ask whether they want a whole map, map object, map image, tileset, isometric tile, or tile variants.
- "Object/character": infer character for people, NPCs, creatures, body templates, or identity/state animation; infer object for standalone props, pickups, furniture, or weapons. Ask only if unclear.
- "Character animation direction": if the user asks to add an animation to an existing multi-direction character and does not name a direction, default to `south` (down-facing) for one preview candidate. Do not animate north-west, diagonal, or all directions by default. Ask which direction only when `south` is unavailable, the asset's directions are unknown, or the user needs a different gameplay-facing direction. Animate all directions only when the user explicitly asks for all/8 directions, a complete direction set, or approves the larger batch.
- "Effect": ask static sprite or animated effect when not obvious. If a target sprite/image is supplied and the user asks to add an effect to it, infer a one-off image edit. Ask reusable object/layer vs one-off sprite only when there is no clear edit target or the user asks for a separate asset.
- "Isometric tileset": ask whether they need one isometric tile or a full tileset, because public docs expose a single isometric tile route.
- "Paperdoll": gather base image/frame, desired layers, fitted visual additions, target body regions, directions, animations, and whether the user wants separate transparent layer images, editor layers, composited previews, or both; see `references/paperdolling.md`.
- "Skeleton/template animation": if the user means a built-in/preset motion for a managed character, use `template_animation_id` through MCP/REST managed character animation. If they mean custom keypoints, pose JSON, or authored skeletons, route to REST skeleton endpoints after reading `references/preset-skeleton-template-animations.md` and `references/animation.md`; ask only when this distinction changes the endpoint.
- Supplied images are optional unless the chosen route requires image fields. When images are supplied, infer each file's low-risk endpoint-specific role from explicit wording. Before credit-spending calls, ask when role uncertainty would change the endpoint, field, or output semantics, such as identity vs style vs concept vs edit target vs mask vs palette vs first/last frame.
- If prompt enhancement adds material inferred details from images or user shorthand, show the proposed description and get confirmation before a credit-spending generation or edit.

Read only the relevant reference:

- Bearer-token setup, PixelLab UI naming, and MCP auth reuse: `references/credentials.md`.
- Natural-language setup for MCP, documented REST v2 fallback, and auth after install: `references/setup.md`.
- Browser fallback and website automation boundaries: `references/browser-fallback.md`.
- Persistent completion sound toggle: `references/bark.md`.
- Safe post-processing when `no_background: true` fails: `references/background-removal.md`.
- Skill/ability/spell/action-bar/hotbar icon sheet prompt, sizing, and verification details: `references/skill-icons.md`.
- Inventory item/equipment/loot icon sheet prompt, transparent-background routing, and verification details: `references/item-icons.md`.
- Cheap, affordable, low-cost, budget, credit-minimizing, and cost-driven Pro-vs-v3/new route selection: `references/cost-routing.md`.
- Paperdolling and layered character workflows: `references/paperdolling.md`.
- Tileset and tile-variant details: `references/tilesets.md`.
- Attachments, file paths, supplied image roles, endpoint fields, or fixed-size image-to-pixel-art: `references/image-input-roles.md`.
- Non-English or mixed-language user requests and response-language handling: `references/localization.md`.
- Official PixelLab documentation, MCP documentation, REST documentation, and web-refresh routing: `references/official-pixellab-documentation.md`.
- Usage, balance, job, and result reporting: `references/usage-reporting.md`.
- Async job lifecycle, MCP object review state, rate limits, and download expiry: `references/job-lifecycle.md`.
- Preset skeleton/template animations, built-in character animation ids, MCP-vs-REST priority, and website/Aseprite private-route boundaries: `references/preset-skeleton-template-animations.md`.
- Raw animation, interpolation, outfit transfer, frame anchors, and idle-loop artifact risk: `references/animation.md`.
- Editor-only utilities and unsupported public route caveats: `references/editor-only-utilities.md`.
- REST v2 natural-language field character limits or prompt-length rejections: `references/prompt-limits.md`.
- Explicit Aseprite handling, `.aseprite` workspace creation/update, generated-frame import, Aseprite layers/frames/tags, or Aseprite CLI/Lua export/open behavior: `references/aseprite-cli.md`.
- Explicit Aseprite MCP server/tooling requests: `references/aseprite-mcp.md`.
- Local animation preview GIFs, spritesheets, or ImageMagick/`magick` assembly from generated frames: `references/local-asset-assembly.md`.

Optional broader docs: in full plugin/repo installs, these paths resolve relative to this `SKILL.md`; raw skill installs may omit them. If runtime `references/` are not enough, read at most one matching file if it exists. If absent, continue with `references/official-pixellab-documentation.md` and current official PixelLab documentation; do not search or load the set.

- Surface boundaries and service selection: `../../docs/pixellab/pixellab-surfaces-and-services.md`.
- Plain-language asset routing: `../../docs/pixellab/pixellab-asset-routing.md`.
- Product/model/mode terminology: `../../docs/pixellab/pixellab-terminology.md`.
- SDK-vs-REST compatibility: `../../docs/pixellab/pixellab-sdk-compatibility.md`.
- Bearer-token, session, and security boundaries: `../../docs/pixellab/pixellab-auth-and-security.md`.
- UI generation, UI asset, shape-piece, and MCP-vs-REST UI routing details: `../../docs/pixellab/pixellab-ui-generation-surfaces-research.md`.

## Model And Mode Terms

Treat PixelLab model/provider language as product labels unless official docs disclose more.

- `Pixen`, `PixFlux`, `BitForge`: public product/workflow labels, not guaranteed provider names.
- `PixPatch`: website-surface label; no public v2 `PixPatch` image endpoint was documented.
- `Pro`: quality/tier/mode label across many unrelated tools, not one endpoint or model. Treat Pro and Pro Tools routes as expensive unless current docs prove otherwise.
- `v3` and `new`: workflow/version labels scoped to a selected operation, not universal model selectors. Treat them as cheap-family hints when the route fits, but check the selected endpoint because exceptions exist, such as REST `inpaint-v3` being documented as Pro.
- `S-XL`, `M-XL`, `S-M`, `M-L`: size/product labels, not asset intents.
- `Gemini`: stale/low-confidence older website Create Tileset Pro wording; do not mention it as current unless refreshed official website docs reintroduce it.

Do not invent provider internals where PixelLab docs are silent.

## Text Preparation

Prompt enhancement is opt-out. For natural-language request parameters such as `description`, `style_description`, `negative_description`, `lower_description`, `upper_description`, `transition_description`, `edit_description`, `action`, `action_description`, `animation_description`, `item_descriptions`, `text`, and `color_palette`, produce the best concise PixelLab-ready English value from the user's request and any visible inputs before calling a tool.

Prompt strings should describe the visual content or, for animation fields, the depicted motion/behavior. Avoid describing the tool operation, output metadata, or report status. Prefer a single concise content-focused description. Include only details that materially change the requested output. Avoid boilerplate such as `create this image`, `the final image should`, or redundant clauses already carried by structured tool parameters, such as canvas dimensions when `image_size` is set or transparent background when `no_background` is set. Do not restate PixelLab defaults such as `pixel`, `pixel art`, or `game-ready` unless the distinction matters for the selected endpoint or user request. Do not add unnecessary `\n` paragraph formatting. If prompt enhancement adds redundant operation, canvas, transparency, or PixelLab-default wording, trim it before generation and report the adjustment when material.

Respect documented character limits for natural-language fields. Do not assume every prompt is capped at 500 characters: many REST v2 descriptions are 2000 characters, while `animate-with-text-v3.action`, `animate-with-text-v2.action`, `enhance-animation-v3-prompt.action`, `interpolation-v2.action`, `edit-image.description`, and several style/reference fields are 500. If PixelLab rejects a prompt for length, trim the field without changing intent, report that adjustment, then retry. For exact current REST v2 limits, read `references/prompt-limits.md` or refresh OpenAPI.

Use one enhancement path. Use REST `enhance-pixen-prompt` for standalone Pixen image prompts and `enhance-animation-v3-prompt` for standalone animation v3 actions with `first_frame` and optional `last_frame`. Current OpenAPI also exposes inline `enhance_prompt` flags on `create-image-pixen`, `animate-with-text-v3`, `create-character-v3`, `animate-character`, `characters/animations`, and `objects/{object_id}/animations`; docs currently price those enhancement uses at `0.05` generations or equivalent credits. When the selected generation route has an inline `enhance_prompt`, prefer that over a separate enhancer call. For `animate-character` / `characters/animations`, use inline `enhance_prompt` only when `mode="v3"`; never set it for `mode="template"` or `mode="pro"`. Use `enhance-character-v3-prompt` only for standalone character-v3 prompt enhancement. For other tools, enhance directly as the agent; do not force a nonmatching enhance endpoint.

## Do Not Use

- Do not use local code or editor automation to create or alter requested visual content for PixelLab asset requests. Examples: PIL/Pillow drawing, canvas/SVG drawing, ImageMagick draw commands, Aseprite Lua drawing, ASCII-to-image, and procedural pixel placement. Local code may still copy, mask, composite, and verify pixels that already came from PixelLab or the user.
- Do not add colored/matte backgrounds to transparent generated assets, final GIFs, final previews, spritesheets, or report images unless explicitly requested. Green backgrounds are not a harmless preview default; they are an unwanted derivative that can be mistaken for asset content. Checkerboard backgrounds may be used for separate, clearly labeled inspection previews only, never baked into final deliverables.
- Do not create APNGs or other extra preview/export formats unless explicitly requested. Prefer the original PixelLab frames and only the requested or route-standard packaging artifacts.
- Do not automate undocumented internal endpoints used by first-party surfaces such as root website routes, unversioned `https://api.pixellab.ai/` paths like `/tilesets/create`, or Aseprite extension operation URLs. Treat them as unsupported for automation unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools.
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

For tasks, execute PixelLab generation/editing only when the user clearly requested it and both the bearer token and tooling are configured. For nontrivial live generation, prefer one candidate first, report enough route details to review it, then continue only if the user asks for more. Ask before ambiguous credit-spending batch work or destructive deletes. Refuse unsupported automation, then route to the closest documented MCP/REST option or a visible manual website flow. Create locally authored non-PixelLab visual content only when the user explicitly asks for a local fallback or approves one after both MCP and documented REST v2 are unavailable or fail; label the result as a non-PixelLab fallback. Otherwise provide the exact route and minimal code or call shape the user needs.

If no PixelLab bearer token is configured, stop before PixelLab generation and offer the setup wizard. Tell the user to open `https://www.pixellab.ai/account` after signing in and copy the value labeled `Secret`, then store it locally as `PIXELLAB_SECRET` or in app secret settings; never ask them to paste it into chat. If the user chooses Manual setup, open or link `https://www.pixellab.ai/mcp`, tell them to pick their app there, and stop. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token.

Before the first credit-spending live PixelLab call, read `references/usage-reporting.md` when cost may require a before/after balance check; after any live PixelLab call, report in that concise user-facing Markdown layout with the section names `Files`, `Route`, `Inputs Used`, `Cost`, and `Verified`. Use those same section names when planning or describing what the final report will contain. Verify the original PixelLab output against the user's explicit constraints before calling it final. If the original output fails and any local derivative is only an inspection, crop, split, format conversion, or proposed repair, say so plainly instead of silently salvaging. For safe background removal after `no_background: true`, report the final as PixelLab output with background-removal post-processing and include the method, source image, cost when a PixelLab call was used, and alpha/preservation checks. Do not paste secrets, raw files/base64, full response JSON, or internal IDs unless needed for pending status, follow-up, or debugging exact schemas.

When a live PixelLab generation, edit, transform, conversion, background-removal, or animation job finishes successfully, read `references/bark.md` and apply the bark completion-sound contract after final success verification.

Use browser automation only for visible website/editor/Pixelorama assistance after explicit user permission. Ask again before login/session actions, spending credits, submitting generations, downloads, edits, or deletes. Never scrape session tokens or call undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension.

## Examples

| Request | Route |
|---|---|
| "Setup PixelLab." | Setup mode; diagnose MCP and REST v2 fallback intent, credential readiness, and ask before config writes. |
| "Make a wizard with idle and walk animations." | MCP `create_character`, then `animate_character`; if direction is unspecified, animate `south` (down-facing) first and ask before expanding to every direction. |
| "Generate a mossy platformer tileset from code." | REST v2 `create-tileset-sidescroller`; use MCP `create_sidescroller_tileset` if working in an MCP-enabled agent. |
| "Create a title screen background." | REST v2 `create-image-pixflux-background`; verify current fields and size support from docs. |
| "Make HUD buttons and a health bar." | REST v2 `create-ui-asset` when the user wants a saved/structured UI asset or layout; REST v2 `generate-ui-v2` when they want a loose raw UI image. |
| "Make a 512x256 UI panel with a portrait circle and three buttons." | REST v2 `create-ui-asset` with `pieces`/`elements`; MCP `create_ui_asset` only when MCP-first and its visible schema has the needed fields. |
| "Convert this image to pixel art and remove the background." | REST v2 `image-to-pixelart-pro`, then `remove-background`. |
| "Inpaint this masked area." | REST v2 `inpaint` or `inpaint-v3` after checking current docs and inputs. |
| "Add a wind dash effect to this runner sprite." | REST v2 `edit-image`; preserve the runner as the target image and add the effect to the same canvas. |
| "Add a walking animation." after creating an 8-direction character | MCP `animate_character` for `south` (down-facing) first unless the user asks for all directions. |
| "Use the dog Walk (8 frames) template animation." | Read `preset-skeleton-template-animations.md`; MCP `animate_character` with `template_animation_id="walk-8-frames"` and explicit directions, REST `/characters/animations` fallback. |
| "Animate this character with a custom skeleton JSON." | Read `preset-skeleton-template-animations.md` and `animation.md`; use REST `animate-with-skeleton` / `estimate-skeleton` after clarifying image and keypoint roles. |
| "Make an 8-direction treasure chest object." | MCP `create_8_direction_object`; REST v2 `create-8-direction-object` for code. |
| "Make hex terrain tiles." | MCP `create_tiles_pro`, not top-down Wang tileset. |
| "Use `/tilesets/create` with my browser token." | Do not use it; route to public MCP/REST tileset tools or manual website use. |
| "What does Pro use?" | Explain only documented/product-level facts; do not infer provider internals. Refresh official docs if current model/mode details matter. |
