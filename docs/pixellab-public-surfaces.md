# PixelLab Public Surfaces

Last reviewed: 2026-06-23.

PixelLab exposes several surfaces that are useful in different contexts. Pip should route by user intent and use documented public interfaces for automation.

## Surface Summary

| Surface | Use for | Notes |
|---|---|---|
| Hosted MCP | Agent workflows that benefit from managed assets, IDs, polling, downloads, and helper tools. | MCP tool names are not REST endpoints. Use tools directly when configured. |
| REST v2 | Programmatic generation, editing, batch processing, exact endpoint control, and integration code. | Base URL is `https://api.pixellab.ai/v2`. Verify exact schemas in OpenAPI. |
| Website/editor | Human visual workflows, account UI, Map Workshop, Character Creator, Simple Creator, and editor flows. | Treat as a user-facing product surface, not a public automation API unless PixelLab documents the route. |
| Pixelorama/editor | Visible editor assistance and save-back workflows after user permission. | Do not automate hidden session routes. |
| Aseprite | Local editor plugin workflows when the user is actively using Aseprite. | Treat plugin transport details as separate from public REST/MCP contracts. |
| REST v1 | Existing legacy code and older SDK compatibility. | Prefer REST v2 for new work unless v1 is explicitly required. |

## Routing Rules

- Use MCP first when tools are available and the request maps to a managed asset workflow.
- Use REST v2 when writing code, needing direct endpoint control, or using functionality not exposed by MCP.
- Use website/editor assistance only for visible user workflows and only after explicit permission.
- Use Aseprite or Pixelorama guidance only when the user is working inside those tools.
- Use REST v1 only for legacy compatibility.

## Automation Boundary

Do not treat unversioned website routes under `https://api.pixellab.ai/...` as public REST endpoints just because they share the same host. Public REST v2 is documented under the `/v2` base path, and MCP has its own documented tool interface.

If a workflow is not documented in REST v2 or MCP, route to the closest documented API/MCP option or a visible manual website/editor workflow.

## Current Official References

- [REST v2 LLM guide](https://api.pixellab.ai/v2/llms.txt)
- [REST v2 docs](https://api.pixellab.ai/v2/docs)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [MCP docs](https://api.pixellab.ai/mcp/docs)
- [MCP setup](https://www.pixellab.ai/mcp)
