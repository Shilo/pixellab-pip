# PixelLab Pip Docs

Last reviewed: 2026-06-24.

These docs explain PixelLab tools, workflows, terminology, SDK boundaries, and auth rules that Pip needs in order to automate PixelLab correctly. They supplement the repository README; install, update, and plugin metadata stay there.

## Showcase

- [PixelLab Pip Showcase](showcase/README.md) - examples of using Pip to route PixelLab requests, enhance prompts, generate assets, and document results.

## Research

- [PixelLab Surfaces And Services](pixellab/surfaces-and-services.md) - where MCP, REST v2, website/editor, Aseprite, Pixelorama, SDKs, and legacy v1 fit.
- [PixelLab Asset Requests](pixellab/asset-routing.md) - how common requests map to PixelLab tools, endpoints, and workflows.
- [PixelLab Auth And Security](pixellab/auth-and-security.md) - bearer-token handling and automation boundaries.
- [PixelLab SDK Compatibility](pixellab/sdk-compatibility.md) - official SDK guidance and when to call REST v2 directly.
- [PixelLab Terminology](pixellab/terminology.md) - product labels, endpoint labels, and terms agents should not over-interpret.
- [Official PixelLab MCP Service Comparison](tools/pixellab-mcp-service-comparison.md) - technical comparison between Pip and the official hosted MCP service.
- [PixelLab AI Skill Comparison](tools/pixellab-ai-skill-comparison.md) - feature comparison between Pip and the unofficial PixelLab AI Skill.

## Official PixelLab Links

For exact current endpoint schemas, tool lists, model/mode availability, pricing, and authentication behavior, verify against [PixelLab Pip Resources](resources.md#official-pixellab-links).

## Publication Rules

These docs intentionally avoid:

- Copied credentials, session tokens, cookies, JWTs, or private account data.
- Instructions for automating undocumented website session endpoints.
- Local machine paths or user-specific filesystem details.
- Provider/internal model claims not documented in public PixelLab sources.
- Informal, mocking, or critical language about PixelLab.

PixelLab Pip can document caveats when they matter for correct implementation, but the tone should stay neutral and technical.
