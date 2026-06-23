# PixelLab Pip Design

Last reviewed: 2026-06-23.

PixelLab Pip is an assistant for routing PixelLab asset, API, and documentation requests across the supported PixelLab surfaces. Pip helps agents pick the right path without requiring users to know whether their request belongs in MCP, REST v2, website/editor workflows, Aseprite, Pixelorama, or legacy v1.

## Goal

PixelLab has several useful public and product surfaces that overlap by asset type, naming, and workflow. Pip gives agents a compact decision layer for common requests:

- Create game-ready pixel art assets such as sprites, characters, objects, tilesets, tiles, maps, UI, backgrounds, icons, and animations.
- Edit or transform existing assets through documented PixelLab routes.
- Choose between hosted MCP tools and REST v2 endpoints.
- Avoid treating website/editor session routes as public automation APIs.
- Explain terminology such as `Pro`, `v3`, `new`, `create tiles`, `create tileset`, and model/product labels.
- Refresh official docs when a current endpoint, schema, SDK capability, model/mode, pricing, or tool list matters.

## Scope

Pip should:

- Prefer hosted MCP when PixelLab MCP tools are available and the workflow benefits from managed assets, IDs, polling, and helper tools.
- Prefer REST v2 when the user needs code, batch processing, exact endpoint control, or a feature not exposed by MCP.
- Treat website, Pixelorama, and Aseprite as user-facing/editor surfaces unless PixelLab documents a public automation route.
- Treat REST v1 as legacy compatibility unless the user explicitly needs it.

Pip should not:

- Use copied browser session tokens for automation.
- Call undocumented website routes as though they were REST v2 endpoints.
- Invent SDK methods, provider details, pricing, or model behavior where public docs are silent.
- Ask users to paste PixelLab credentials into chat.

## Triggering

The canonical skill name is `pixellab-pip`. The description should remain technical and keyword-rich so agents can invoke Pip for PixelLab-specific asset/API requests.

Explicit invocation is most reliable:

```text
/pixellab-pip make a cute knight character sprite
```

Implicit invocation should also work for PixelLab-specific requests such as creating sprites, generating tilesets, editing assets, checking PixelLab docs, using PixelLab MCP, or writing REST v2 integration code.
