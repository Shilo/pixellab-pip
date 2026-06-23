# Official PixelLab Docs

Read this when exact current endpoint names, MCP tools, parameters, auth setup, model/mode availability, prices, limits, or SDK support matter.

Official docs can change after this skill. Prefer this skill for routing and ambiguity handling; refresh official docs for exact current schemas and setup.

## Links

| Link | Use for | Limits |
|---|---|---|
| `https://www.pixellab.ai/docs` | Human API guides and conceptual docs. | Not a complete machine-readable schema. |
| `https://api.pixellab.ai/v2/docs` | Interactive REST v2 API docs. | Good for exact endpoint parameters; less useful for high-level agent routing. |
| `https://api.pixellab.ai/v2/llms.txt` | LLM-friendly REST v2 endpoint index and auth summary. | Broad index, not enough for every field nuance; use OpenAPI/docs for full schema. |
| `https://api.pixellab.ai/v2/openapi.json` | Machine-readable REST v2 schema. | Requires parsing; current skill summarizes only stable routing. |
| `https://www.pixellab.ai/mcp` | Human Vibe Coding setup page for MCP clients. | Setup-oriented; not a full tool reference. |
| `https://api.pixellab.ai/mcp` | Hosted MCP server URL. | This is a service endpoint, not documentation. Use through an MCP-capable client. |
| `https://api.pixellab.ai/mcp/docs` | LLM-readable MCP tool guide. | MCP tools are not REST endpoints; do not curl tool names. |

## Vibe Coding Without This Skill

Without `/pixellab-agent`, the official MCP flow is:

1. User configures an MCP-capable agent with server URL `https://api.pixellab.ai/mcp`.
2. User sends `Authorization: Bearer <PixelLab account credential>` through that MCP client config.
3. Agent sees PixelLab MCP tools, often bare or prefixed by the host.
4. User asks the agent to create assets.
5. Agent uses MCP tools directly and polls with corresponding `get_*` tools.

`https://api.pixellab.ai/mcp/docs` is a tool guide for agents. It explains available MCP tools, non-blocking jobs, polling, downloads, and warns that MCP tools are not REST endpoints.

`https://api.pixellab.ai/v2/llms.txt` is a REST API guide for agents. It lists v2 endpoints, base URL, bearer auth, async job behavior, and links to OpenAPI/interactive docs.

## What This Skill Adds

`/pixellab-agent` does not replace official docs. It adds:

- Intent routing across MCP, REST v2, website/editor, Aseprite, Pixelorama, and legacy v1.
- Warnings about undocumented website/session endpoints.
- A plain-language map from user asset goals to tools/endpoints.
- Reference-image role disambiguation.
- Paperdolling and tileset workflow contracts.
- Usage reporting expectations.
- Credential safety rules.

Refresh official docs when a current exact claim matters; use this skill when the user needs the right PixelLab surface or workflow.

