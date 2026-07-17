---
name: pixellab-pip
description: Use for PixelLab/Pip setup, auth, MCP/API routing, asset generation, editing, animation, skeleton/template/preset animations, multi-shot/looping cinematics, docs/troubleshooting, bark completion sounds, and explicit PixelLab cost/budget/credit questions across MCP, REST v2/API, website/editor Pixelorama, Aseprite, and legacy v1. Trigger only when PixelLab context is present, including PixelLab setup, MCP/API setup, PIXELLAB_SECRET, bearer-token auth, PixelLab sprites, sprite sheets, characters, portrait characters, fonts, objects, tiles, tilesets, tilemaps, maps, UI, icons, backgrounds, palettes, image edits, animations, skeletons, template animations, preset animations, cinematics, looping or seamless-loop scenes, multi-shot scenes, endpoint choice, SDK integration, blueprints/recipes, recreating/replaying `*.blueprint.json` generations, troubleshooting, or PixelLab credits/cost/budget. Do not trigger for unrelated Python pip/package-manager requests or generic image/pixel-art requests with no PixelLab intent.
license: MIT
metadata:
  requires_api_key: false
  api_key_env: PIXELLAB_SECRET
  api_key_note: "Optional. Guidance, setup, routing, and docs need no key. Live PixelLab generation needs a bearer token, configured in the MCP client or as PIXELLAB_SECRET for REST v2 fallback; the skill uses it only as an auth header and never reads, prints, or stores its value."
permissions: # declared least-privilege capabilities: reads env var PIXELLAB_SECRET, runs the python command, reads/writes its own output and config files
  - env
  - shell
  - file_read
  - file_write
---

# PixelLab Pip

Classify the request, choose the supported PixelLab surface, then act. Answer questions directly when the request is a question.

## Workflow

1. Classify intent; values combine, such as `animate + cost_sensitive`:
   `question | setup | bark | create asset | edit/transform | animate | prompt_enhancement | cost_sensitive | integrate/code | check balance/status | troubleshoot docs/API | website/editor assistance | aseprite_integration | blueprint/recipe`.
   A standalone `setup` or `bark` word after an explicit skill invocation, such as `/pixellab-pip setup` or `@pixellab-pip bark off`, is that intent. For setup, read `references/setup.md` and run the wizard contract: recommend MCP + API first, support MCP-only/API-only/manual modes, and change settings only after a token-free preview and explicit approval. For bark, read `references/bark.md` and apply the persistent toggle contract.
2. Classify the target:
   `general_image | skill_icon | item_icon | background | character | portrait_character | font | object | effect_vfx | ui | whole_map | map_image | map_object | top_down_tileset | sidescroller_tileset | isometric_tile | tile_variants | animation | existing_image`.
   Fitted visual additions to an existing character image, such as hair, facial features, wearables, accessories, or held gear, are `existing_image` paperdoll edits, not standalone `object` requests, unless the user explicitly wants a separate unattached prop.
3. Choose the surface with Surface Rules, then the route with the Intent Router. When the user explicitly asks for Aseprite handling, read `references/aseprite-cli.md`; PixelLab MCP/REST generates, documented Aseprite CLI/Lua handles local workspace, import/export, packaging, and launch only.
4. Use MCP only if PixelLab MCP tools are visible as callable tools, bare or prefixed such as `mcp__pixellab__create_character` (match by suffix). If the user explicitly asked for MCP, do not silently fall back; report that MCP is unavailable and offer setup or an approved REST v2 fallback. Otherwise, when MCP is unavailable, use the matching documented REST v2 endpoint. If both are unavailable or fail, explain why before any non-PixelLab fallback.
5. Before repeated paid prompt-only retries, inspect the chosen tool or endpoint schema for generation controls such as guidance, adherence/strength, reference images, palette images, or style options, and use the ones that target the failure mode. Refresh official docs only when a needed tool, endpoint, field, auth, SDK, pricing, or model/mode fact is missing or unclear (see Current Docs Refresh).
6. For consistency-sensitive work, summarize the user's identity, style, palette, view, and reference anchors. Ask up to three blocking questions before a credit-spending call.
7. Prepare natural-language parameters per Text Preparation. For non-English or mixed-language requests, read `references/localization.md`.
8. For animation, preserve the user's requested frame count; otherwise use the endpoint or template default. Exception: preset/template character animations take no `frame_count`; pick a matching template id such as `walking-8-frames` (catalog in `references/preset-skeleton-template-animation.md`) or fall back to v3 custom mode. Preserve PixelLab's returned frame order; no ping-pong, reversed, duplicated, or trimmed outputs unless the user asks for that playback style.
9. If the user says cheap, budget, low-cost, fewer credits, or similar, read `references/cost-routing.md` before choosing a paid route, and ask before each extra paid attempt unless a concrete budget or attempt count was approved.
10. Before live generation, confirm the PixelLab bearer token is configured without asking the user to paste it into chat (see Auth And Execution).
11. `seed`: omit by default; PixelLab randomizes it. Send it in two cases only — the user gave a seed (send verbatim), or two or more calls share near-identical wording and must land on the same composition (seed-lock): generate one random positive integer (`0` means random, so never 0) and send that same value on every call in the set. Never ask the user for a seed.
12. Act or answer, then report once. Ask a short clarification only for known collisions. After the first tool call, send nothing but blockers and questions — no status, plans, or notes on routing, schema checks, balance, calls, polling, downloads, or file writes. Silence until the report is correct; the report carries all of it.

## Asset Integrity

- Every pixel of requested art must originate from PixelLab or the user. Local tools may read, download, assemble, package, import/export, preview, verify, mask, pad, crop, resize, and format-convert those pixels. Locally authored generation controls such as masks, palette swatches/`color_image`, reference guides, and shape templates are allowed as inputs; report them as inputs. Do not draw, repaint, or synthesize requested content locally unless the user explicitly approves a labeled non-PixelLab fallback.
- Reviewable static candidates: when a static image-style MCP tool or REST endpoint returns multiple alternatives, read `references/reviewable-candidates.md` before selecting, saving, or continuing from one.
- Do not bake a colored, checkerboard, white, black, green-screen, or matte background into transparent frames, final GIFs, spritesheets, previews, or report images unless the user explicitly asks for it. A checkerboard is allowed only as a clearly labeled inspection aid kept separate from final deliverables.
- Do not post-process PixelLab output into a claimed final asset without explicit approval. Local crop/split/format work that preserves original pixels is allowed when reported honestly; resizing, reassembling, compositing, or repairing failed outputs locally must not be called final without approval. Exception: when a request used `no_background: true` but the output kept a background, read `references/background-removal.md` and attempt safe removal when verification shows the background is removable without changing the art.
- Save downloaded generations, derived previews, manifests, and packages under a project `pixellab-pip-generations/` folder unless the user names another location. Produce only the requested output formats or the route's minimal standard artifacts. When a job returns multiple separate images/frames, always compile a single spritesheet of those frames as a standard deliverable alongside the individual files (read `references/local-asset-assembly.md` for grid inspection previews). No APNG or extra preview/viewer formats unless asked.
- After a generation returns image(s), write a `<name>.blueprint.json` beside the outputs per `references/blueprint.md` — canonical portable `_pixellab` connection metadata, the exact route bodies, structured `TASK` steps for material work performed outside PixelLab calls, and a `_comment_prompt` holding the user's original prompt as they intended it. Remove host-added wrappers such as connector Markdown, app URIs, hidden local paths, or tool-call serialization; keep the visible command text, such as `/pixellab-pip`. When the generation used one or more user-supplied input images (any role — source, reference, style, mask, init, frame, and the like), copy each into the folder by copying the file, not by reading and re-writing it.
- After every live generation flow, write a manifest beside the outputs using `references/usage-reporting.md`; keep its private audit/resume data out of the shareable blueprint.

## Surface Rules

| Surface | Use for | Avoid |
|---|---|---|
| Hosted MCP | Managed PixelLab assets with IDs, polling, downloads, list/get/delete helpers, and project/sandbox/agent helpers, including `create_ui_asset`, `create_font`, or `create_portrait_character` when visible. | Raw image/edit primitives MCP does not expose, REST-only controls such as `style_image` or `project_id`, or any MCP call when PixelLab MCP tools are not visible. |
| REST v2 | Scripts, batch jobs, server integrations, exact endpoint control, generic images, backgrounds, UI, inpaint/edit, prompt enhancement, raw animation, rotate, resize, remove background. | Guessing SDK methods without checking the installed SDK or current docs. |
| Website / Map Workshop | Human product surface, full-map manual work, rich libraries, visible browser assistance. | Programmatic use of copied browser session tokens or undocumented internal endpoints used by first-party surfaces. |
| Aseprite plugin | In-editor workflows when the user is actively working inside Aseprite. | Treating private first-party extension endpoints as public REST/MCP contracts. |
| Aseprite CLI | Explicit Aseprite handling after PixelLab produced files: `.aseprite` workspaces, importing frames as layers/frames/tags, palette work, export/open via documented CLI/Lua. | Mouse/OCR UI automation or hidden control of the PixelLab Aseprite extension. |
| Pixelorama / website editor | The PixelLab website editor is Pixelorama-powered; assist it only as visible browser automation after explicit permission, and ask again before login/session actions, spending credits, generations, downloads, edits, or deletes. | Hidden automation, undocumented endpoint calls, or any destructive action without a second confirmation. |
| REST v1 | Existing legacy code and old SDK compatibility. | New work unless the user explicitly needs v1. |

Hosted MCP tool names are not REST endpoints; do not curl MCP tool names as `/v2/...` paths.

## Intent Router

For any atlas or spritesheet request with known or requested cell dimensions, also read `references/local-asset-assembly.md` for the required grid inspection preview.

| User intent | Default route | REST v2 route for code/exact control |
|---|---|---|
| Character, player, NPC, enemy, creature | MCP `create_character` with `mode="v3"` by default, then `create_character_state`, `animate_character`, `get_character`, list/delete helpers. For a follow-up animation on a multi-direction character, animate `south` first; ask before animating all directions. `outline` and outline wording in `description` are both ignored on v3 and Pro character generation; say so instead of spending credits tuning it. Neither the schema nor an echoed `get_character` value is evidence otherwise — only changed art is. | `create-character-v3`, `create-character-with-4-directions`, `create-character-with-8-directions`, `create-character-pro`, state/animation/tags/ZIP/list/get/delete endpoints. |
| Portrait-to-character or character-to-portrait | MCP `create_portrait_character` + `get_portrait_character` when visible. | `portrait-character-pro` (Pro image conversion). Supplied-image roles: `references/image-input-roles.md`. |
| Pixel/bitmap font, font atlas | MCP `create_font` + `get_font` when visible. | `generate-font-pro` (Pro). |
| Skill/ability/spell/action-bar/hotbar icon, inventory item/equipment/loot/pickup icon, emoji, or icon sheet | Read `references/icon.md` before choosing an endpoint or generating. | The reference covers route choice, background defaults, sheet sizing, prompt wording, and verification. |
| Standalone object, prop, pickup, weapon, furniture (not an icon) | MCP `create_1_direction_object`, `create_8_direction_object`, object state/animation/review tools. Object creation is Pro Tools (20-40 generations). | `create-1-direction-object`, `create-8-direction-object`, object state/animation/tags/list/get/delete endpoints. |
| Top-down terrain/Wang/autotile tileset | Read `references/tileset.md`, then MCP `create_topdown_tileset`. | `create-tileset`, `tilesets`. |
| Sidescroller/platformer tileset | Read `references/tileset.md`, then MCP `create_sidescroller_tileset`. | `create-tileset-sidescroller`. |
| Isometric tile/block/floor | MCP `create_isometric_tile`; map thickness wording to `tile_shape` (`thin`, `thick`, `block`). | `create-isometric-tile` with `isometric_tile_shape` (`thin tile`, `thick tile`, `block`). |
| Tile variants (hex, octagon, square, isometric singles) | MCP `create_tiles_pro`. | `create-tiles-pro`, `tiles-pro/{tile_id}`. |
| General image, sprite, standalone asset that is not an icon or emoji | REST v2. For explicit Create Image Pro, `generate-image-v2`, exact grids/sheets, or below-32px cells, read `references/create-image-pro.md` first. Model character: `create-image-pixflux` = lower detail, loose/painterly (frames whole subjects); `create-image-pixen` = high detail, tight framing; Pixen and Pro crop larger subjects; Pro for style/variety; `create-image-bitforge` only for `coverage_percentage`, its one unique control (`color_image`/`init_image` are on `create-image-pixflux`), never a default. | `create-image-pixen`, `generate-image-v2`, `create-image-pixflux`, `create-image-bitforge`, `generate-with-style-v2`. |
| Background, scene, backdrop | REST v2 image generation; no hosted MCP background tool is documented. Route by whether a subject is present: subject-less backdrop (empty landscape/sky/room, no figure) → `create-image-pixflux`; full scene with a subject in an environment → `create-image-pixen` with `no_background: false`. Do not use Pro `generate-image-v2` here — not worth its ~12× cost for backdrops or scenes. | `create-image-pixflux-background`; verify current size/field support before exact code. |
| UI, HUD, button, panel, health bar, menu | REST v2 `create-ui-asset` (Pro) for structured/saved UI assets, `pieces`, named `elements`, `style_image`, or `project_id`; MCP `create_ui_asset` when MCP-first and its visible schema has the needed fields; `generate-ui-v2` for loose/raw UI images, especially with a `concept_image`. | Do not route shape-piece/layout requests to `generate-ui-v2`. |
| Image edit, inpaint, mask, convert, resize, remove background | REST v2. | `inpaint`, `inpaint-v3` (Pro), `edit-image`, `edit-images-v2`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background`. |
| Fitted paperdoll addition on an existing character image | Treat as an `existing_image` edit anchored on the base frame; read `references/paperdolling.md` before choosing layer/composite outputs. | Do not use object generation for fitted layers unless the user explicitly wants an unattached prop. |
| Style-reference or consistent-style generation | Read `references/style-reference.md`, then REST v2. | `generate-with-style-v2` or `generate-image-v2` style/reference fields after checking current docs. |
| Editor-only utilities (Canny/Pose/Depth, reduce colors, unzoom, pixel correction, reshape) | Read `references/editor-only-utilities.md`. For file-level palette quantization/reduction/replacement, read `references/aseprite-cli.md` even without explicit Aseprite wording. | No public REST/MCP route exists for these; do not invent `/v2/...` routes. |
| Try on garment/accessory | Website Try on (single composited image); REST `transfer-outfit-v2` only for animation-frame outfit transfer. | Try on does not return isolated paperdoll layers. |
| Multi-image combine/edit | REST v2 `edit-images-v2` for documented multi-source edits; website/editor for visual experimental flows. | Aseprite's `generate-multi-edit` is an internal endpoint, not public REST. |
| Prompt enhancement | Matching enhance endpoint or inline `enhance_prompt` per Text Preparation. | `enhance-pixen-prompt`, `enhance-character-v3-prompt`, `enhance-animation-v3-prompt`. |
| Preset/template/built-in animation, named motion, or custom skeleton/keypoints | Read `references/preset-skeleton-template-animation.md`; it splits MCP managed-template vs REST raw-skeleton routes. | Do not call website root `/generate-animation/background` or Aseprite extension internals. |
| Auto-rig, estimate skeleton, animate from keypoints | Read `references/preset-skeleton-template-animation.md`. | `estimate-skeleton`, then `animate-with-skeleton`. |
| Raw non-skeleton animation, interpolation, outfit transfer, rotate | REST v2 unless animating a managed MCP character/object. Read `references/animation.md` for frame anchors, idle-loop risk, and verification. | `animate-with-text-v3`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, `generate-8-rotations-v2/v3`. No public 4-rotation route. For a start→end tween prefer `animate-with-text-v3` (`first_frame`+`last_frame`); use `interpolation-v2` only on an explicit Pro/v2 request. |
| Multi-shot, multi-second, or seamless-loop cinematic (a scene longer than one clip) | Read `references/cinematic.md`; requires a user-specified budget, a documented plan, and per-shot validation. | `animate-with-text-v3` — one looped clip for cyclic motion, chained shots (each from the previous handoff frame) for evolving scenes, or `first_frame`+`last_frame` for a strict start→end tween. |
| Map image / visual level concept | REST v2 image/background route; website or Aseprite for map extension workflows. | No public map CRUD/extension/texture surface is documented. |
| Map object | MCP `create_map_object` + `get_map_object`; download promptly — MCP map objects auto-delete after 8 hours. | `POST /map-objects` (POST-only; verify polling shape from OpenAPI). |
| Whole map, Map Workshop, map CRUD/export | Website manually, or generate components via MCP/REST. | No public map CRUD surface is documented. |
| Static effect/VFX sprite | If a target image is supplied and the user asks to add an effect to it, REST image edit on that target; otherwise object/image generation for a separate reusable asset. For native-size multi-output VFX batches, read `references/create-image-pro.md`. | Edit routes return a whole edited image, not an isolated effect layer; no standalone VFX endpoint exists. |
| Animated effect/VFX | REST v2 raw animation, or MCP object animation for a managed object. | `animate-with-text-v3`, `animate-with-skeleton`, or object animation endpoints; VFX is a description, not an endpoint. |
| Balance, credits, account check | MCP `get_balance` if available. | `GET /balance`. |
| REST async job status | `GET /background-jobs/{job_id}`. | MCP managed assets use resource-specific `get_*` tools instead. |
| PixelLab projects, sandbox, chat, deployed agents, MCP help/feedback | Read `references/mcp-platform-tools.md` before using `list_projects`, `sandbox_*`, `chat_*`, or `agent_*` tools. | No public REST v2 equivalent is documented. |
| Discover, inspect, select, or replay blueprints/recipes, including a supplied `*.blueprint.json` | Read `references/blueprint.md` and follow its discovery, selection, and replay contract. A blueprint name that contains an asset word (e.g. "knight") is still blueprint intent when the conversation identifies it as one. | The exact route recorded in the blueprint (`MCP <tool>` or `POST /v2/...`). |

## Clarify Only For Collisions

- "Presets": infer bundled blueprints from established blueprint context and preset/template
  animations from animation or motion context; ask which collection only when neither is clear.
- "Tiles": terrain/autotile tileset, platformer tileset, or individual tile variants?
- "Map": whole map, map object, map image, tileset, isometric tile, or tile variants?
- "Isometric tileset": one isometric tile or a full set? Public docs expose a single-tile route.
- "Object/character": infer character for people, NPCs, creatures, or identity/state animation; object for standalone props, pickups, furniture, weapons. Ask only if unclear.
- Animation direction on a multi-direction character: default to `south` for one preview candidate; ask only when `south` is unavailable, directions are unknown, or the user needs another gameplay-facing direction. Animate all directions only on explicit request or approval.
- "Effect": static or animated? If a target image is supplied, infer a one-off edit; ask reusable-asset vs one-off only without a clear edit target.
- "Paperdoll": gather base image, desired layers, target regions, directions, and whether the user wants separate transparent layer files, editor layers, composited previews, or both; see `references/paperdolling.md`.
- Supplied images: infer each file's low-risk endpoint-specific role from wording. Before credit-spending calls, ask when role uncertainty (identity vs style vs concept vs edit target vs mask vs palette vs first/last frame) would change the endpoint or output; see `references/image-input-roles.md`.
- If prompt enhancement adds material inferred details, show the proposed description and confirm before a credit-spending call.

## References

Read only the relevant reference:

- Bearer-token setup, PixelLab UI naming, MCP auth reuse: `references/credentials.md`.
- Setup wizard for MCP, REST v2 fallback, auth after install: `references/setup.md`.
- Persistent completion sound toggle: `references/bark.md`.
- Safe post-processing when `no_background: true` fails: `references/background-removal.md`.
- Skill/ability and inventory item icon sheets: `references/icon.md`.
- Create Image Pro, native-size multi-output batches, exact grids, below-32px cells: `references/create-image-pro.md`.
- Cheap/budget/credit-minimizing route selection: `references/cost-routing.md`.
- Paperdolling and layered characters: `references/paperdolling.md`.
- Review/choice handling for static candidate alternatives: `references/reviewable-candidates.md`.
- Tilesets and tile variants: `references/tileset.md`.
- Style-reference generation, Aseprite-equivalent square padding, and output sizing: `references/style-reference.md`.
- Supplied image roles, endpoint image fields, fixed-size image-to-pixelart: `references/image-input-roles.md`.
- Non-English or mixed-language requests: `references/localization.md`.
- Official PixelLab doc URLs and boundaries: `references/official-pixellab-documentation.md`.
- Generation reports and manifests after PixelLab calls: `references/usage-reporting.md`.
- Per-generation blueprint (PixelLab calls + agent tasks), recreation, and sharing: `references/blueprint.md`.
- Async jobs, MCP review state, rate limits, download expiry: `references/job-lifecycle.md`.
- Preset/template/skeleton character animations: `references/preset-skeleton-template-animation.md`.
- Raw animation, interpolation, outfit transfer, idle-loop risk: `references/animation.md`.
- Multi-shot, multi-second, or seamless-loop cinematics from chained animations: `references/cinematic.md`.
- Editor-only utilities without public routes: `references/editor-only-utilities.md`.
- PixelLab project/sandbox/chat/agent MCP tools: `references/mcp-platform-tools.md`.
- REST v2 prompt/field character limits: `references/prompt-limits.md`.
- Explicit Aseprite handling, `.aseprite` workspaces, palette quantization, CLI/Lua export: `references/aseprite-cli.md`.
- Third-party Aseprite MCP servers: `references/aseprite-mcp.md`.
- Atlas/spritesheet grid inspection previews, local assembly, preview GIFs, and ImageMagick: `references/local-asset-assembly.md`.

Optional broader docs: in full plugin/repo installs these resolve relative to this `SKILL.md`; raw skill installs may omit them. Read at most one matching file if runtime references are not enough; if absent, continue with `references/official-pixellab-documentation.md` and current official docs.

- Surface boundaries and service selection: `../../docs/pixellab/pixellab-surfaces-and-services.md`.
- Plain-language asset routing: `../../docs/pixellab/pixellab-asset-routing.md`.
- Product/model/mode terminology: `../../docs/pixellab/pixellab-terminology.md`.
- SDK-vs-REST compatibility: `../../docs/pixellab/pixellab-sdk-compatibility.md`.
- Bearer-token, session, and security boundaries: `../../docs/pixellab/pixellab-auth-and-security.md`.
- UI generation and MCP-vs-REST UI routing research: `../../docs/pixellab/pixellab-ui-generation-surfaces-research.md`.
- Multi-shot cinematic technique research (chained-animation findings): `../../docs/pixellab/pixellab-cinematic-spike.md`.
- Cinematic scene composition and motion technique (inspiration): `../../docs/pixellab/pixellab-cinematic-inspiration.md`.

## Model And Mode Terms

Treat PixelLab model/provider language as product labels unless official docs disclose more. Do not invent provider internals where docs are silent.

- `Pixen`, `PixFlux`, `BitForge`: product/workflow labels, not guaranteed provider names.
- `PixPatch`: website-surface label; no public v2 `PixPatch` endpoint exists.
- `Pro`: a quality/tier label across many unrelated tools, not one endpoint or model. Treat Pro and Pro Tools routes as expensive unless current docs prove otherwise.
- `v3` and `new`: workflow/version labels scoped to a selected operation. Cheap-family hints, but check the endpoint — REST `inpaint-v3` is documented as Pro.
- `standard`: a legacy generation mode, not a quality tier (the `standard`/`pro` split on characters, tilesets). Use it only when the user explicitly asks or a route reference directs it.
- `S-XL`, `M-XL`, `S-M`, `M-L`: size/product labels, not asset intents.
- `Gemini`: stale older website Create Tileset Pro wording; do not present it as current.

## Text Preparation

Exact field values win over prompt prep. If the user explicitly supplies a PixelLab-facing field value, such as `prompt: ...`, `description: ...`, `action: ...`, or `use exactly ...`, send that value unchanged and do not enhance it. If it is invalid, over limit, or unsafe, stop and ask for an approved replacement or trim before spending credits.

Prompt enhancement is opt-out. Otherwise, for natural-language parameters such as `description`, `style_description`, `negative_description`, `*_description`, `action`, `item_descriptions`, `text`, and `color_palette`, produce the best concise PixelLab-ready English value from the request and visible inputs before calling a tool.

Prompts describe the visual content or, for action fields, the depicted motion — never the tool operation, output metadata, or report status. Include only details that materially change the output. Omit boilerplate such as `create this image`, canvas dimensions when `image_size` is set, transparency when `no_background` is set, and PixelLab defaults such as `pixel art` or `game-ready` unless the distinction matters. If enhancement adds redundant wording, trim it before generation. When a specific look is at stake — especially flat pixel art — the distinction matters: state it explicitly (`flat pixel art, chunky low-resolution pixels, limited palette, hard edges`), keep render-y adjectives (`glossy, plastic, diorama, cinematic lighting, 3D, photorealistic, depth of field`) out of `description` and put them in `negative_description`, and enforce the look with the endpoint's flat-shading / outline / low-detail / palette controls rather than prompt words alone — a large canvas plus render wording pushes the image models toward a smooth semi-realistic render.

Respect documented character limits: many REST v2 description fields allow 2000 characters, but several action/edit/style fields cap at 500. On a length rejection, trim without changing intent, note the adjustment, and retry. Exact limits: `references/prompt-limits.md` or OpenAPI.

Use one enhancement path per call. Inline `enhance_prompt` flags exist on `create-image-pixen`, `animate-with-text-v3`, `create-character-v3`, `animate-character`/`characters/animations`, and object animations, cost about 0.05 generations, and are preferred over a separate enhancer call when the route has one. Constraints: for character/object animation, `enhance_prompt` is valid only with `mode="v3"`; for `create-character-v3` it is valid only for from-scratch generation. Standalone enhancers: `enhance-pixen-prompt` for Pixen image prompts, `enhance-animation-v3-prompt` for animation v3 actions, `enhance-character-v3-prompt` for character-v3 prompts. Otherwise enhance directly as the agent; do not force a mismatched enhancer.

## Do Not Use

- No local code or editor automation to create or alter requested visual content: no PIL/Pillow drawing, canvas/SVG drawing, ImageMagick draw, Aseprite Lua drawing, ASCII-to-image, or procedural pixel placement. Local code may copy, mask, composite, and verify pixels that came from PixelLab or the user.
- No undocumented internal endpoints used by first-party surfaces: root website routes, unversioned `https://api.pixellab.ai/` paths like `/tilesets/create`, or Aseprite extension operation URLs. Treat them as unsupported unless they appear in public REST v2 docs/OpenAPI or MCP docs.
- Never ask users to paste the PixelLab bearer token into chat; direct them to the setup wizard, local `PIXELLAB_SECRET`, or app secret settings.
- Never scrape browser session tokens or cookies. Website session tokens are not API bearer tokens; never use one for the other.
- Do not confuse website Create Tileset Pro with public `create_tiles_pro` / `create-tiles-pro`; different flows.
- Do not default to v1 or old SDK README examples for new work, and do not assume an installed SDK covers every current v2 endpoint — confirm the installed package or call REST v2 directly.

## Current Docs Refresh

Route from this skill first. Refresh official docs only when a needed tool, endpoint, field, schema, SDK detail, auth step, price/limit, or model/mode claim is missing or unclear. Start lightweight; fetch `openapi.json` only for exact schemas.

- `https://api.pixellab.ai/v2/llms.txt` — REST v2 endpoint index and auth summary
- `https://api.pixellab.ai/v2/docs` — interactive REST v2 parameters
- `https://api.pixellab.ai/v2/openapi.json` — exact schema checks only; read a field's existence, type, or default from the raw JSON, not a prose summary
- `https://api.pixellab.ai/mcp/docs` — MCP tool behavior
- `https://www.pixellab.ai/mcp` — MCP setup
- `https://github.com/pixellab-code` — official SDK/MCP repo state only
- `https://api.pixellab.ai/v1/openapi.json` — legacy checks only

If web access is unavailable, answer from this skill and say which current claim could not be freshly verified.

## Auth And Execution

If no bearer token is configured, stop before generation and offer the setup wizard: the user opens `https://www.pixellab.ai/account` after signing in, copies the value labeled `Secret`, and stores it locally as `PIXELLAB_SECRET` or in app secret settings — never pasted into chat. For Manual setup, link `https://www.pixellab.ai/mcp` and stop. PixelLab UI/docs may call this value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token.

For questions, answer with: recommended surface/endpoint, why it fits, warnings for unsupported alternatives, and a verification note only when the answer depends on an unverified current fact.

For tasks, generate only when the user clearly requested it and token plus tooling are configured. For nontrivial work, produce one candidate first, report it, and continue only if asked. Before a multi-asset batch, list each planned item with its route and cost category so the user approves the full scope and rough total first. Ask before ambiguous credit-spending batches or destructive deletes. Refuse unsupported automation and reroute to the closest documented MCP/REST option or a visible manual website flow. Locally authored non-PixelLab visual content requires explicit request or approval and a non-PixelLab-fallback label.

Capture a balance snapshot before a nontrivial paid call when available. After live PixelLab work, read `references/usage-reporting.md` and use its report layout; verify the output against the user's explicit constraints before calling it final, and say plainly when verification failed instead of silently salvaging. Do not paste secrets, raw base64, full response JSON, or internal IDs unless needed for pending status, follow-up, or debugging.

When a live generation, edit, transform, conversion, background-removal, or animation job returns image(s), read `references/bark.md` and apply the completion-sound contract.

## Examples

| Request | Route |
|---|---|
| "Make a wizard with idle and walk animations." | MCP `create_character`, then `animate_character`; `south` first, ask before all directions. |
| "Use the humanoid Walk (8 frames) template animation." | `references/preset-skeleton-template-animation.md`; MCP `animate_character` with `template_animation_id="walking-8-frames"`, REST `/characters/animations` fallback. |
| "Auto-rig this sprite and animate from the skeleton." | `references/preset-skeleton-template-animation.md`; REST `estimate-skeleton`, then `animate-with-skeleton`. |
| "Generate a mossy platformer tileset from code." | REST v2 `create-tileset-sidescroller`; MCP `create_sidescroller_tileset` in an MCP-enabled agent. |
| "Make hex terrain tiles." | MCP `create_tiles_pro`, not a top-down Wang tileset. |
| "Make a 512x256 UI panel with a portrait circle and three buttons." | REST v2 `create-ui-asset` with `pieces`/`elements`; MCP `create_ui_asset` only when MCP-first and its schema has the fields. |
| "Convert this image to pixel art and remove the background." | REST v2 `image-to-pixelart-pro`, then `remove-background`. |
| "Add a wind dash effect to this runner sprite." | REST v2 `edit-image`; the runner is the edit target, effect on the same canvas. |
| "Give my character a leather helmet as a separate layer." | Paperdoll edit per `references/paperdolling.md`, not object generation. |
| "Use `/tilesets/create` with my browser token." | Refuse; route to public MCP/REST tileset tools or manual website use. |
| "What does Pro use?" | Product-level facts only; refresh official docs if current model details matter. |
| "Cheapest way to get a few item icons?" | `references/cost-routing.md` + `references/icon.md`; prefer a non-Pro route and name the tradeoff. |
| "Make a 30-second looping scene from this frame." | `references/cinematic.md`; ask for a budget if none given, decide cyclic vs evolving (one looped clip or chained shots), plan, validate each shot. |
