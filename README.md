# PixelLab Agent

Agent-agnostic skill for helping AI assistants choose the right PixelLab surface: MCP, REST v2 API, website/editor workflows, Aseprite, Pixelorama, or legacy v1.

Use it when an agent needs to create, edit, animate, or troubleshoot PixelLab assets such as characters, objects, tilesets, tiles, maps, UI, backgrounds, image edits, and animations.

## What It Does

- Routes plain-language asset requests to the best PixelLab tool or endpoint.
- Separates official public REST/MCP surfaces from undocumented website/session endpoints.
- Explains confusing PixelLab terms such as `Pro`, `v3`, `new`, `create tiles`, and `create tileset`.
- Tells agents when to refresh official PixelLab docs before giving exact endpoint, schema, SDK, auth, or model/mode claims.
- Warns agents to verify installed SDK coverage before assuming every current REST v2 endpoint or parameter is available.

## Quick Start

Place this folder wherever your agent loads Agent Skills, such as `~/.codex/skills/pixellab-agent` for Codex or a Claude/Cursor-compatible skills folder.

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Configure the PixelLab bearer token locally as `PIXELLAB_SECRET` or through your agent/MCP host's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into agent chat.

Useful official entry points:

- MCP endpoint: `https://api.pixellab.ai/mcp`
- MCP docs: `https://api.pixellab.ai/mcp/docs`
- REST v2 docs: `https://api.pixellab.ai/v2/docs`
- REST v2 LLM guide: `https://api.pixellab.ai/v2/llms.txt`

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Files

- `SKILL.md` - the portable Agent Skills file.
- `references/credentials.md` - PixelLab bearer-token setup, UI naming, and MCP auth-source reuse.
- `references/browser-fallback.md` - permission rules for visible website/editor fallback.
- `references/paperdolling.md` - layered character and outfit workflow contract.
- `references/tilesets.md` - terrain/platformer/tile-variant routing details.
- `references/image-inputs.md` - image input roles for attachments, file paths, and endpoint fields.
- `references/usage-reporting.md` - usage, balance, job, and result reporting.
- `references/official-docs.md` - when and how to refresh official PixelLab docs.

No platform-specific plugin wrapper is required for the first version.

## Recommended Use

Install or point your agent at this folder, then invoke it as `/pixellab-agent` if your agent supports slash commands. Otherwise, ask the agent to use the `pixellab-agent` skill.

The skill is intentionally small: it is a routing brain, not a PixelLab SDK.
