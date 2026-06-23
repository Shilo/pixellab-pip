# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is friendly on the outside and very practical under the collar: he maps plain-language asset requests to the right supported surface, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

## Table Of Contents

- [What Pip Does](#what-pip-does)
- [Install](#install)
- [Auto Install](#auto-install)
- [Manual Install](#manual-install)
- [Usage](#usage)
- [Authentication](#authentication)
- [Project Layout](#project-layout)
- [Official PixelLab Links](#official-pixellab-links)

## What Pip Does

Use Pip when an agent needs to create, edit, animate, or troubleshoot PixelLab assets such as characters, objects, tilesets, tiles, maps, UI, backgrounds, image edits, and animations.

Pip:

- Routes plain-language asset requests to the best PixelLab tool or endpoint.
- Separates official public REST/MCP surfaces from undocumented website/session endpoints.
- Explains confusing PixelLab terms such as `Pro`, `v3`, `new`, `create tiles`, and `create tileset`.
- Tells agents when to refresh official PixelLab docs before giving exact endpoint, schema, SDK, auth, or model/mode claims.
- Warns agents to verify installed SDK coverage before assuming every current REST v2 endpoint or parameter is available.

## Install

Recommended skill name: `pixellab-pip`.

Recommended commands:

- `/pixellab-pip`
- `/pip`

Keep `pixellab-pip` as the canonical package and install folder name so GitHub, installers, docs, and implicit triggering stay PixelLab-specific. The installer creates `/pip` by copying the same runtime payload to a sibling `pip` skill folder.

Installed runtime payload:

```text
pixellab-pip/
  SKILL.md
  references/

pip/
  SKILL.md
  references/
```

The installer does not install `README.md`, `docs/`, `package.json`, `bin/`, or `.git/`.

## Auto Install

Use the GitHub installer:

```bash
npx -y github:Shilo/pixellab-pip install --target auto --scope project
```

Installer options:

| Option | Values | Default | Meaning |
|---|---|---|---|
| `--target` | `auto`, `codex`, `claude`, `cursor` | `auto` | Chooses the skill root layout. |
| `--scope` | `project`, `user` | `project` | Installs into the current project or user-global skill folder. |
| `--no-alias` | none | off | Installs only `/pixellab-pip`, without the `/pip` alias folder. |

Default install targets:

| Target | Project Scope | User Scope |
|---|---|---|
| `auto` / `codex` | `.agents/skills/` | `~/.agents/skills/` |
| `claude` | `.claude/skills/` | `~/.claude/skills/` |
| `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |

## Manual Install

Manual install is useful when you do not want to run installer code. Copy only the runtime skill folder into your skill root.

POSIX shell:

```bash
mkdir -p .agents/skills/pixellab-pip .agents/skills/pip
cp pixellab-pip/SKILL.md .agents/skills/pixellab-pip/
cp -R pixellab-pip/references .agents/skills/pixellab-pip/
cp pixellab-pip/SKILL.md .agents/skills/pip/
cp -R pixellab-pip/references .agents/skills/pip/
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force .agents/skills/pixellab-pip, .agents/skills/pip | Out-Null
Copy-Item pixellab-pip/SKILL.md .agents/skills/pixellab-pip/
Copy-Item pixellab-pip/references .agents/skills/pixellab-pip/ -Recurse -Force
Copy-Item pixellab-pip/SKILL.md .agents/skills/pip/
Copy-Item pixellab-pip/references .agents/skills/pip/ -Recurse -Force
```

For Claude or Cursor, replace `.agents/skills/` with the desired skill root, such as `.claude/skills/` or `.cursor/skills/`.

## Usage

After installing, invoke:

```text
/pixellab-pip
/pip
```

If your host does not support slash commands, ask your agent to use PixelLab Pip.

To help implicit triggering, the skill metadata includes `PixelLab Pip`; the practical trigger words stay PixelLab-specific: pixel art, sprites, characters, objects, tilesets, tilemaps, UI, backgrounds, animations, MCP, REST v2, SDK/API, and PixelLab docs.

## Authentication

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Configure the PixelLab bearer token locally as `PIXELLAB_SECRET` or through your agent/MCP host's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into chat.

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Project Layout

```text
README.md
package.json
bin/
  pixellab-pip.js
pixellab-pip/
  SKILL.md
  references/
```

Runtime files:

- `pixellab-pip/SKILL.md` - the portable skill file.
- `pixellab-pip/references/credentials.md` - PixelLab bearer-token setup, UI naming, and MCP auth-source reuse.
- `pixellab-pip/references/browser-fallback.md` - permission rules for visible website/editor fallback.
- `pixellab-pip/references/paperdolling.md` - layered character and outfit workflow contract.
- `pixellab-pip/references/tilesets.md` - terrain/platformer/tile-variant routing details.
- `pixellab-pip/references/image-inputs.md` - image input roles for attachments, file paths, and endpoint fields.
- `pixellab-pip/references/usage-reporting.md` - usage, balance, job, and result reporting.
- `pixellab-pip/references/official-docs.md` - when and how to refresh official PixelLab docs.

No platform-specific plugin wrapper is required for the first version.

## Official PixelLab Links

- MCP endpoint: `https://api.pixellab.ai/mcp`
- MCP docs: `https://api.pixellab.ai/mcp/docs`
- REST v2 docs: `https://api.pixellab.ai/v2/docs`
- REST v2 LLM guide: `https://api.pixellab.ai/v2/llms.txt`
