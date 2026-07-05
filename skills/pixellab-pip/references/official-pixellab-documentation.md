# Official PixelLab Documentation

Read this when a needed endpoint, tool, field, price, limit, SDK detail, or exact request/response schema is missing or unclear in the skill. Official docs can change after this skill ships; prefer the skill for routing and refresh docs only for the gap. Refresh triggers and the URL shortlist are in SKILL.md (Current Docs Refresh) — this file adds the annotated link table and the surface boundaries below.

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

## Authoritative MCP Inventory

- `https://api.pixellab.ai/mcp/docs` is the authoritative public MCP tool inventory. It explains available tools, non-blocking jobs, polling, downloads, and warns that MCP tools are not REST endpoints. Do not rely on the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` to decide whether a current MCP tool exists.
- An MCP-capable client may also expose `pixellab://docs/...` documentation resources (engine/framework guides such as Godot, Unity, Python, Wang tilesets, sidescroller tilesets, isometric tiles, and platform overview). Use those resources when visible; otherwise fall back to the public docs URLs above.

## Prompt Enhancement Pricing

`enhance-pixen-prompt`, `enhance-character-v3-prompt`, and `enhance-animation-v3-prompt` are public REST v2. A live check on 2026-06-25 returned `usage.generations: 0.05` with a matching balance delta for `enhance-pixen-prompt` — treat prompt enhancement as low-cost prompt prep, not a generation job. These are not root website/editor endpoints. Ask first for bulk or unusually cost-sensitive enhancement, and honor opt-out.

## Boundaries Beyond The Intent Router

SKILL.md's Intent Router already states MCP-vs-REST routing per asset type. These are the extra facts it does not:

- MCP documents managed asset tools only; it has no raw image-editing tools equivalent to REST v2 `edit-image`, `edit-images-v2`, `inpaint`, `inpaint-v3`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, or `remove-background`. Route those to REST v2 unless a matching MCP tool is visible; do not assume a REST endpoint has an MCP equivalent just because MCP is configured.
- MCP `create_map_object` may expose `background_image` or `inpainting` parameters. These are map-object generation controls, not generic replacements for REST v2 `inpaint`/`inpaint-v3`.
- MCP and REST versions of the same workflow (for example `create_ui_asset` vs `create-ui-asset`) are not guaranteed pixel-identical for the same prompt and seed; treat them as one workflow family with overlapping controls, while REST currently exposes the fuller documented schema. More generally, same-seed regeneration is not guaranteed to reproduce pixels exactly.
- Font and portrait-character conversion have dedicated Pro routes on both REST and MCP (see the Intent Router). Do not fall back to generic image/icon or text-to-character generation for them; portrait-to-character is an image-conversion workflow with `image` as the source input.
- Aseprite extension operation names (observed: `generate-image-new`, `generate-pixelart-flux`, `generate-multi-edit`, `quantize-image`, `unzoom-pixelart`, `correct-pixelart`) are undocumented internal endpoints unless they appear in public REST v2/OpenAPI or MCP docs. Do not cite extension source filenames, source layout, source contents, or internal request payloads as public documentation. When an Aseprite workflow maps to a documented public route, use that route instead.
