# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is friendly on the outside and very practical under the collar: he maps plain-language asset requests to the right supported surface, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

Use Pip when an agent needs to create, edit, animate, or troubleshoot PixelLab assets such as characters, objects, tilesets, tiles, maps, UI, backgrounds, image edits, and animations.

## Name And Triggering

Recommended skill name: `pixellab-pip`.

Recommended command: `/pixellab-pip`.

Recommended alias: `/pip`.

Keep `pixellab-pip` as the canonical package and install folder name so GitHub, installers, docs, and implicit triggering stay PixelLab-specific. The installer creates `/pip` by copying the same runtime payload to a sibling `pip` skill folder.

To help implicit triggering, the skill metadata includes `PixelLab Pip`; the practical trigger words should stay PixelLab-specific: pixel art, sprites, characters, objects, tilesets, tilemaps, UI, backgrounds, animations, MCP, REST v2, SDK/API, and PixelLab docs.

## What It Does

- Routes plain-language asset requests to the best PixelLab tool or endpoint.
- Separates official public REST/MCP surfaces from undocumented website/session endpoints.
- Explains confusing PixelLab terms such as `Pro`, `v3`, `new`, `create tiles`, and `create tileset`.
- Tells agents when to refresh official PixelLab docs before giving exact endpoint, schema, SDK, auth, or model/mode claims.
- Warns agents to verify installed SDK coverage before assuming every current REST v2 endpoint or parameter is available.

## Quick Start

Install with:

```bash
npx -y github:Shilo/pixellab-pip install --target auto --scope project
```

The installer copies only the runtime payload into your skill folder:

```text
pixellab-pip/
  SKILL.md
  references/

pip/
  SKILL.md
  references/
```

It does not install `README.md`, `docs/`, `package.json`, `bin/`, or `.git/`.

Manual clean install:

```bash
mkdir -p .agents/skills/pixellab-pip .agents/skills/pip
cp pixellab-pip/SKILL.md .agents/skills/pixellab-pip/
cp -R pixellab-pip/references .agents/skills/pixellab-pip/
cp pixellab-pip/SKILL.md .agents/skills/pip/
cp -R pixellab-pip/references .agents/skills/pip/
```

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Configure the PixelLab bearer token locally as `PIXELLAB_SECRET` or through your agent/MCP host's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into chat.

Useful official entry points:

- MCP endpoint: `https://api.pixellab.ai/mcp`
- MCP docs: `https://api.pixellab.ai/mcp/docs`
- REST v2 docs: `https://api.pixellab.ai/v2/docs`
- REST v2 LLM guide: `https://api.pixellab.ai/v2/llms.txt`

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Files

- `pixellab-pip/SKILL.md` - the portable skill file.
- `pixellab-pip/references/credentials.md` - PixelLab bearer-token setup, UI naming, and MCP auth-source reuse.
- `pixellab-pip/references/browser-fallback.md` - permission rules for visible website/editor fallback.
- `pixellab-pip/references/paperdolling.md` - layered character and outfit workflow contract.
- `pixellab-pip/references/tilesets.md` - terrain/platformer/tile-variant routing details.
- `pixellab-pip/references/image-inputs.md` - image input roles for attachments, file paths, and endpoint fields.
- `pixellab-pip/references/usage-reporting.md` - usage, balance, job, and result reporting.
- `pixellab-pip/references/official-docs.md` - when and how to refresh official PixelLab docs.

No platform-specific plugin wrapper is required for the first version.

## Recommended Use

Install Pip, then invoke `/pixellab-pip` or `/pip` if your host supports slash commands. Otherwise, ask your agent to use PixelLab Pip.

The skill is intentionally small: Pip fetches the right route, not a whole PixelLab SDK.
