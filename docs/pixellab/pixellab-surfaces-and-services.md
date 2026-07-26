# PixelLab Surfaces And Services

Last reviewed: 2026-07-01.

Purpose: explain how PixelLab's public APIs, agent tools, website/editor surfaces, SDKs, and local integrations differ so Pip can choose the right automation boundary.

PixelLab is not one API surface. It has public REST endpoints, hosted MCP tools, product websites, editor workflows, SDKs, and local editor integrations. Pip works because it treats those as related but distinct services and chooses the right one for the user's intent.

For exact current schemas and tool lists, verify against the official [REST v2 docs](https://api.pixellab.ai/v2/docs), [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json), and [MCP docs](https://api.pixellab.ai/mcp/docs). For the full official resource list, see [Resources](../resources.md#official-pixellab).

## Surface Map

| Surface | What it is | Best use | Automation stance |
|---|---|---|---|
| Hosted MCP | A managed PixelLab tool server for agents. Tools create and manage PixelLab assets by task names. | Agent workflows with managed assets, IDs, polling, list/get/delete helpers, projects, sandboxes, and balance checks. | Use directly when the agent has PixelLab MCP tools configured. MCP tool names are not REST endpoints. |
| REST v2 | The current public HTTP API under `https://api.pixellab.ai/v2`. | Code, scripts, batch jobs, server integrations, direct endpoint control, exact schemas, and features not exposed by MCP. | Preferred programmatic fallback when MCP is unavailable or insufficient. |
| REST v1 | Older public HTTP API under `https://api.pixellab.ai/v1`. | Existing legacy code or SDK compatibility. | Avoid for new work unless the user explicitly needs v1. |
| Website and account UI | Human product surfaces such as the account page, creation pages, Map Workshop, and asset libraries. | Visual/manual workflows, account token setup, browsing existing assets, and website-only features. | Use as a visible user-guided surface. Do not treat undocumented internal website routes as public REST. |
| Pixelorama/editor | Pixelorama/editor integrations and website editor workflows. | Visible editor assistance, manual edits, and save-back flows when supported and permission-gated. | Ask before browser use and again before login, generation, spending credits, save/download/edit/delete actions. |
| Aseprite extension | Local editor integration for users working inside Aseprite. | In-editor asset creation or editing when the user is actively using Aseprite. | Treat as an editor integration, not as a public REST/MCP contract. |
| Official SDKs | Public client libraries under [pixellab-code](https://github.com/pixellab-code). | Convenience wrappers when installed SDK coverage matches the needed operation. | Verify installed SDK coverage before claiming a method exists. Use REST v2 directly when unsure. |

## Service Boundaries

The same asset type can appear across multiple surfaces. A character, object, tile, path tile, building kit, UI asset, font, portrait-character conversion, or raw image (generate/edit/inpaint/animate) may have:

- A hosted MCP tool name.
- A REST v2 endpoint path.
- A website/editor workflow.
- An SDK wrapper, depending on SDK version.

Do not assume these names are interchangeable. Hosted MCP tools are called through MCP. REST v2 endpoints are HTTP paths under `/v2`, and legacy REST v1 endpoints are HTTP paths under `/v1`. First-party website/editor/Aseprite operations can share the `https://api.pixellab.ai/` root host or similar operation names without being public REST endpoints.

## Route Selection

Use this order for most agent work:

1. If PixelLab MCP tools are configured and the task maps to a managed asset workflow, use MCP.
2. If the user asks for code, batch generation, server integration, exact request fields, or a route not exposed by MCP, use REST v2.
3. If the task requires visual editing, website libraries, account setup, Map Workshop, Pixelorama, or Aseprite, use a visible user-guided workflow.
4. If existing code is explicitly v1 or old-SDK based, use REST v1 compatibility.

## Important Distinctions

- `https://api.pixellab.ai/mcp` is the MCP endpoint, not a REST endpoint family.
- `https://api.pixellab.ai/v2` is the current public REST API base.
- `https://api.pixellab.ai/v1` is the legacy public REST API base.
- Undocumented root or unversioned endpoints under `https://api.pixellab.ai/` that are used by first-party surfaces such as the website or Aseprite extension are not public REST v1/v2 just because they share a host or operation name.
- Website login/session credentials are not the same thing as the public REST/MCP bearer token.
- Product labels such as `Pro`, `v3`, `new`, `Pixen`, `PixFlux`, and `BitForge` need to be interpreted in the context of the selected surface.
