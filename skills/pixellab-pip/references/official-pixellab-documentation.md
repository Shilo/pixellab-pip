# Official PixelLab Documentation

Read this when a needed endpoint/tool/field is not found in the local skill, or when auth setup, model/mode availability, prices, limits, SDK support, or exact request/response schemas matter.

Official docs can change after this skill. Prefer this skill for normal routing and ambiguity handling; refresh official docs only when local routing is missing something or code needs exact current schemas/setup.

## Links

| Link | Use for | Limits |
|---|---|---|
| `https://www.pixellab.ai/docs` | Human API guides and conceptual docs. | Not a complete machine-readable schema. |
| `https://api.pixellab.ai/v2/docs` | Interactive REST v2 API docs. | Good for exact endpoint parameters; less useful for high-level agent routing. |
| `https://api.pixellab.ai/v2/redoc` | REST v2 ReDoc reference pages linked from `llms.txt`. | Browseable operation docs; still use OpenAPI for machine-readable schemas. |
| `https://api.pixellab.ai/v2/llms.txt` | LLM-friendly REST v2 endpoint index and auth summary. | Curated index only; it intentionally points to OpenAPI/interactive docs for full endpoint parameters, enum values, and request/response shapes. |
| `https://api.pixellab.ai/v2/openapi.json` | Machine-readable REST v2 schema. | Requires parsing; current skill summarizes only stable routing. |
| `https://www.pixellab.ai/mcp` | Human Vibe Coding setup page for MCP clients. | Setup-oriented; its "Available Tools" list can be abbreviated and should not be treated as the full tool inventory. |
| `https://api.pixellab.ai/mcp` | Hosted MCP server URL. | This is a service endpoint, not documentation. Use through an MCP-capable client. |
| `https://api.pixellab.ai/mcp/docs` | LLM-readable MCP tool guide and authoritative public MCP tool inventory. | MCP tools are not REST endpoints; do not curl tool names. |
| `https://github.com/pixellab-code/pixellab-python` | Official Python SDK linked from `llms.txt`. | Check installed package/docs before assuming endpoint coverage. |
| `https://github.com/pixellab-code/pixellab-js` | Official JavaScript/TypeScript SDK linked from `llms.txt`. | Check installed package/docs before assuming endpoint coverage. |
| `https://github.com/pixellab-code/pixellab-mcp` | Official MCP server repository linked from `llms.txt`. | Hosted MCP tool availability can still vary by client/tool schema. |

## Vibe Coding Without This Skill

Without `/pixellab-pip`, the official MCP flow is:

1. User configures an MCP-capable agent with server URL `https://api.pixellab.ai/mcp`.
2. User configures the MCP client to send `Authorization: Bearer <PixelLab bearer token>` from secret/env config.
3. Agent sees PixelLab MCP tools, often bare or prefixed by the host.
4. User asks the agent to create assets.
5. Agent uses MCP tools directly and polls with corresponding `get_*` tools.

`https://api.pixellab.ai/mcp/docs` is the authoritative public MCP tool inventory for agents. It explains available MCP tools, non-blocking jobs, polling, downloads, and warns that MCP tools are not REST endpoints. Use `https://www.pixellab.ai/mcp` for setup instructions, but do not rely on its abbreviated "Available Tools" list to decide whether a current MCP tool exists.

MCP may also expose `pixellab://docs/...` documentation resources for engine/framework guides such as Godot, Unity, Python, Wang tilesets, sidescroller tilesets, isometric tiles, and platform overview. Use those resources when an MCP-capable client exposes them; otherwise fall back to the public docs URLs above.

`https://api.pixellab.ai/v2/llms.txt` is a REST API guide for agents. It lists v2 endpoints, base URL, bearer auth, async job behavior, ReDoc operation links, OpenAPI/interactive docs, and official Python, JavaScript/TypeScript, and MCP GitHub repositories.

## Prompt Enhancement Pricing Boundary

Public REST v2 docs list `enhance-pixen-prompt`, `enhance-character-v3-prompt`, and `enhance-animation-v3-prompt`. A live REST v2 check on 2026-06-25 returned `usage.generations: 0.05` with the same balance delta for `enhance-pixen-prompt`. Treat prompt enhancement as low-cost prompt prep, not a generation job. Ask first for bulk or unusually cost-sensitive enhancement, and honor opt-out. These endpoints are not root website/editor endpoints.

## MCP vs REST Image Editing Boundary

As of the current MCP guide, PixelLab MCP documents managed asset tools for characters, portrait-character conversion, fonts, character states, character animations, top-down tilesets, sidescroller tilesets, isometric tiles, tile variants, UI assets, objects, map objects, projects, chat/sandbox helpers, and balance checks. It does not document raw image-editing tools equivalent to REST v2 `edit-image`, `edit-images-v2`, `inpaint`, `inpaint-v3`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, or `remove-background`.

MCP `create_map_object` may expose map-object-specific `background_image` or `inpainting` parameters. Treat those as map-object generation controls, not as generic replacements for REST v2 `inpaint` or `inpaint-v3`.

For supplied-image edits, image conversion, inpainting, resizing, background removal, and additive sprite effects on the same canvas, route to REST v2 unless current MCP docs or visible MCP tools expose a matching image-edit tool. Do not assume a REST endpoint has an MCP equivalent just because MCP is configured. If a future MCP tool appears, prefer the visible tool and update this reference.

## UI Asset Boundary

Current public UI automation has two REST routes and one MCP-managed asset route:

- REST `POST /create-ui-asset`: structured/saved UI asset generation. Use this as the default when an agent can call REST and needs `pieces`, `elements`, `style_image`, `project_id`, exact OpenAPI schemas, or backend integration.
- MCP `create_ui_asset`: managed UI asset generation when the tool is visible in an MCP-capable host. Use it for MCP-first workflows when the visible schema has the needed overlapping fields such as `description`, size, `pieces`, `elements`, `color_palette`, `no_background`, `seed`, or `name`.
- REST `POST /generate-ui-v2`: loose/raw UI image generation. Use it for standalone UI art such as buttons, bars, slots, or dialogue boxes, especially when `concept_image` should guide the design. It does not expose `pieces` or `elements`.

Do not assume MCP `create_ui_asset` and REST `create-ui-asset` are pixel-identical for the same prompt and seed. Treat them as the same workflow family with overlapping controls, while REST currently exposes the fuller documented schema.

## Font And Portrait-Character Boundary

Current public docs expose Pro font and portrait-character conversion on both REST v2 and MCP:

- REST `POST /generate-font-pro`; MCP `create_font` and `get_font`.
- REST `POST /portrait-character-pro`; MCP `create_portrait_character` and `get_portrait_character`.

Use the MCP tools for MCP-first asset workflows when visible. Use REST v2 when writing code, when exact fields such as `glyph_px`, `image_size`, `font_name`, `direction`, `view`, or `result_size` matter, or when MCP is unavailable and REST auth is configured.

Do not route font requests to generic image/icon generation unless the public font routes are unavailable or the user explicitly wants a non-font image of lettering. Do not route portrait-to-character conversion to normal text-to-character generation; it is an image conversion workflow with `image` as the source input.

## Aseprite Extension Boundary

The official Aseprite extension is an editor integration. Observed extension operation names include `generate-image-new`, `generate-pixelart-flux`, `generate-multi-edit`, `quantize-image`, `unzoom-pixelart`, and `correct-pixelart`. Treat those as undocumented internal endpoints used by first-party surfaces unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools. Do not cite extension source filenames, source layout, source contents, or internal request payloads in public documentation.

When an Aseprite workflow maps to current public REST v2, use the documented route instead, for example `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `create-ui-asset`, `edit-image`, `edit-images-v2`, `inpaint`, `inpaint-v3`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background`, `animate-with-text-v3`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `rotate`, `generate-8-rotations-v2/v3`, `create-tileset`, `create-tileset-sidescroller`, `create-isometric-tile`, and `create-tiles-pro`.

For exact editor-only behavior such as PixelLab extension quantize/reduce-colors, unzoom pixel art, pixel correction, old/root map-extension tools, and reshape, route to Aseprite/Pixelorama as visible editor surfaces. For direct file-level palette quantization, source-derived color reduction, bit-depth conversion, indexed conversion, strict palette clamps, or document palette replacement, read `aseprite-cli.md`; do not treat that file-level Aseprite route as PixelLab's private editor utility.

## What This Skill Adds

`/pixellab-pip` does not replace official docs. It adds:

- Intent routing across MCP, REST v2, website/editor, Aseprite, Pixelorama, and legacy v1.
- Warnings about undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension.
- A plain-language map from user asset goals to tools/endpoints.
- Reference-image role disambiguation.
- Paperdolling and tileset workflow contracts.
- Usage reporting expectations.
- Credential safety rules.

Refresh official docs when local skill coverage is missing/unclear or exact schema/setup details are needed; use this skill when the user needs the right PixelLab surface or workflow.
