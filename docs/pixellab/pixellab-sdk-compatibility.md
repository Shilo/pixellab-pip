# PixelLab SDK Compatibility

Last reviewed: 2026-06-25.

Purpose: help agents decide when to use an official PixelLab SDK and when to call REST v2 directly.

PixelLab publishes official SDK and tooling repositories under [pixellab-code](https://github.com/pixellab-code). Pip should prefer official docs and installed package behavior over assumptions from memory.

## Guidance

- Use REST v2 directly when the user needs exact endpoint coverage, exact request/response schemas, or batch/server code.
- Use an official SDK when the installed package exposes the needed operation and version.
- Verify installed SDK coverage before claiming a method exists.
- Treat branch-specific SDK code as evidence only for that branch, not as released package behavior.
- Do not assume every current REST v2 endpoint is available in every SDK release.

## Decision Table

| Situation | Recommended path |
|---|---|
| User asks for a PixelLab REST/API integration from scratch | Start from REST v2 docs/OpenAPI, then offer SDK code only after confirming coverage. |
| User already has PixelLab SDK code installed | Inspect the installed package or lockfile before choosing SDK method names. |
| User needs an endpoint that appears in REST v2 but not the installed SDK | Call REST v2 directly. |
| User asks for MCP setup or agent-managed assets | Use hosted MCP docs and tools, not SDK wrappers. |
| User asks about old code using v1/default SDK examples | Treat as legacy compatibility and explain the v2 path for new work. |
| User asks for exact enums, required fields, polling, or result shapes | Verify against REST v2 OpenAPI before finalizing code. |

## Official References

- [REST v2 LLM guide](https://api.pixellab.ai/v2/llms.txt)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [Python SDK](https://github.com/pixellab-code/pixellab-python)
- [JavaScript/TypeScript SDK](https://github.com/pixellab-code/pixellab-js)
- [MCP server](https://github.com/pixellab-code/pixellab-mcp)

## Safe Answer Pattern

When asked for PixelLab code:

1. Identify the intended endpoint or tool.
2. Check whether the installed SDK exposes it if SDK code is requested.
3. Use REST v2 directly when SDK coverage is missing or uncertain.
4. Include bearer-token setup without asking the user to paste credentials into chat.
5. Mention that exact schemas should be verified against REST v2 OpenAPI when current fields matter.
