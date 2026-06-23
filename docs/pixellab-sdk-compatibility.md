# PixelLab SDK Compatibility

Last reviewed: 2026-06-23.

PixelLab publishes official SDK and tooling repositories under [pixellab-code](https://github.com/pixellab-code). Pip should prefer official docs and installed package behavior over assumptions from memory.

## Guidance

- Use REST v2 directly when the user needs exact endpoint coverage, exact request/response schemas, or batch/server code.
- Use an official SDK when the installed package exposes the needed operation and version.
- Verify installed SDK coverage before claiming a method exists.
- Treat branch-specific SDK code as evidence only for that branch, not as released package behavior.
- Do not assume every current REST v2 endpoint is available in every SDK release.

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
