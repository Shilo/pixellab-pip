# Official PixelLab Documentation

Read this when a needed endpoint/tool/field is not found in the local skill, or when auth setup, model/mode availability, prices, limits, SDK support, or exact request/response schemas matter.

Official docs can change after this skill. Prefer this skill for normal routing and ambiguity handling; refresh official docs only when local routing is missing something or code needs exact current schemas/setup.

## Links

| Link | Use for | Limits |
|---|---|---|
| `https://www.pixellab.ai/docs` | Human API guides and conceptual docs. | Not a complete machine-readable schema. |
| `https://api.pixellab.ai/v2/docs` | Interactive REST v2 API docs. | Good for exact endpoint parameters; less useful for high-level agent routing. |
| `https://api.pixellab.ai/v2/llms.txt` | LLM-friendly REST v2 endpoint index and auth summary. | Curated index only; it intentionally points to OpenAPI/interactive docs for full endpoint parameters, enum values, and request/response shapes. |
| `https://api.pixellab.ai/v2/openapi.json` | Machine-readable REST v2 schema. | Requires parsing; current skill summarizes only stable routing. |
| `https://www.pixellab.ai/mcp` | Human Vibe Coding setup page for MCP clients. | Setup-oriented; not a full tool reference. |
| `https://api.pixellab.ai/mcp` | Hosted MCP server URL. | This is a service endpoint, not documentation. Use through an MCP-capable client. |
| `https://api.pixellab.ai/mcp/docs` | LLM-readable MCP tool guide. | MCP tools are not REST endpoints; do not curl tool names. |

## Vibe Coding Without This Skill

Without `/pixellab-pip`, the official MCP flow is:

1. User configures an MCP-capable agent with server URL `https://api.pixellab.ai/mcp`.
2. User configures the MCP client to send `Authorization: Bearer <PixelLab bearer token>` from secret/env config.
3. Agent sees PixelLab MCP tools, often bare or prefixed by the host.
4. User asks the agent to create assets.
5. Agent uses MCP tools directly and polls with corresponding `get_*` tools.

`https://api.pixellab.ai/mcp/docs` is a tool guide for agents. It explains available MCP tools, non-blocking jobs, polling, downloads, and warns that MCP tools are not REST endpoints.

MCP may also expose `pixellab://docs/...` documentation resources for engine/framework guides such as Godot, Unity, Python, Wang tilesets, sidescroller tilesets, isometric tiles, and platform overview. Use those resources when an MCP-capable client exposes them; otherwise fall back to the public docs URLs above.

`https://api.pixellab.ai/v2/llms.txt` is a REST API guide for agents. It lists v2 endpoints, base URL, bearer auth, async job behavior, and links to OpenAPI/interactive docs.

## MCP vs REST Image Editing Boundary

As of the current MCP guide, PixelLab MCP documents managed asset tools for characters, character states, character animations, top-down tilesets, sidescroller tilesets, isometric tiles, tile variants, objects, map objects, projects, chat/sandbox helpers, and balance checks. It does not document raw image-editing tools equivalent to REST v2 `edit-image`, `edit-images-v2`, `inpaint`, `inpaint-v3`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, or `remove-background`.

MCP `create_map_object` may expose map-object-specific `background_image` or `inpainting` parameters. Treat those as map-object generation controls, not as generic replacements for REST v2 `inpaint` or `inpaint-v3`.

For supplied-image edits, image conversion, inpainting, resizing, background removal, and additive sprite effects on the same canvas, route to REST v2 unless current MCP docs or visible MCP tools expose a matching image-edit tool. Do not assume a REST endpoint has an MCP equivalent just because MCP is configured. If a future MCP tool appears, prefer the visible tool and update this reference.

## What This Skill Adds

`/pixellab-pip` does not replace official docs. It adds:

- Intent routing across MCP, REST v2, website/editor, Aseprite, Pixelorama, and legacy v1.
- Warnings about undocumented website/session endpoints.
- A plain-language map from user asset goals to tools/endpoints.
- Reference-image role disambiguation.
- Paperdolling and tileset workflow contracts.
- Usage reporting expectations.
- Credential safety rules.

Refresh official docs when local skill coverage is missing/unclear or exact schema/setup details are needed; use this skill when the user needs the right PixelLab surface or workflow.
