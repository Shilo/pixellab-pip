# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is friendly on the outside and practical under the collar: he maps plain-language asset requests to the right supported surface, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

## Table Of Contents

- [What Pip Does](#what-pip-does)
- [Recommended Install](#recommended-install)
- [Agent-Assisted Install](#agent-assisted-install)
- [Manual Fallback](#manual-fallback)
- [Usage](#usage)
- [Updating](#updating)
- [Authentication](#authentication)
- [Project Layout](#project-layout)
- [Design Decisions](#design-decisions)
- [Official PixelLab Links](#official-pixellab-links)

## What Pip Does

Use Pip when an agent needs to create, edit, animate, or troubleshoot PixelLab assets such as characters, objects, tilesets, tiles, maps, UI, backgrounds, image edits, and animations.

Pip:

- Routes plain-language asset requests to the best PixelLab tool or endpoint.
- Separates official public REST/MCP surfaces from undocumented website/session endpoints.
- Explains confusing PixelLab terms such as `Pro`, `v3`, `new`, `create tiles`, and `create tileset`.
- Tells agents when to refresh official PixelLab docs before giving exact endpoint, schema, SDK, auth, or model/mode claims.
- Warns agents to verify installed SDK coverage before assuming every current REST v2 endpoint or parameter is available.

## Recommended Install

Install PixelLab Pip as a plugin when your agent supports plugins or marketplaces. This keeps the skill updatable and avoids copying runtime files into multiple places.

| Host | Install | Update |
|---|---|---|
| Codex | `codex plugin marketplace add Shilo/pixellab-pip`, then install `pixellab-pip` from `/plugins` or the Codex plugin directory. | `codex plugin marketplace upgrade pixellab-pip` |
| Claude Code | `/plugin marketplace add Shilo/pixellab-pip`, then `/plugin install pixellab-pip@pixellab-pip` | `/plugin marketplace update pixellab-pip`, then `/plugin update pixellab-pip` |
| GitHub Copilot CLI | `copilot plugin marketplace add Shilo/pixellab-pip`, then `copilot plugin install pixellab-pip@pixellab-pip` | `copilot plugin update pixellab-pip` |
| VS Code agent plugins | Enable `chat.plugins.enabled`, add `Shilo/pixellab-pip` to `chat.plugins.marketplaces`, or use **Chat: Install Plugin From Source** with this repo URL. | VS Code checks plugin marketplaces for updates automatically when extension updates run. |
| Cursor | This repo includes Cursor marketplace metadata at `.cursor-plugin/marketplace.json`. Use Cursor's plugin marketplace or team marketplace flow when available for your workspace. | Refresh/update the Cursor marketplace entry for this repo. |
| Gemini CLI | `gemini extensions install https://github.com/Shilo/pixellab-pip` | `gemini extensions update pixellab-pip` |

Gemini uses `GEMINI.md` as a thin wrapper because Gemini extensions are not native Agent Skills plugins.

## Agent-Assisted Install

You can try this prompt in an agent that can manage its own plugins:

```text
Install PixelLab Pip from https://github.com/Shilo/pixellab-pip using the proper marketplace or plugin workflow for this agent. Prefer marketplace install/update over copying files.
```

This is intentionally agent-agnostic, but it depends on the host exposing plugin management commands and permission to run them.

## Manual Fallback

Manual install is a fallback for hosts that support raw skills but not plugins. Copy only the runtime skill folder:

```text
plugins/pixellab-pip/skills/pixellab-pip/
```

into the host's documented skill root. Common raw-skill examples include:

```text
.agents/skills/pixellab-pip/
.claude/skills/pixellab-pip/
```

Manual copies are harder to update. Prefer plugin install when possible.

## Usage

After installing, invoke the canonical skill/plugin name:

```text
/pixellab-pip
```

If your host namespaces plugin skills, use the host's shown name, such as `pixellab-pip:pixellab-pip`.

If your host does not support slash commands, ask your agent to use PixelLab Pip.

To help implicit triggering, the skill metadata includes `PixelLab Pip`; the practical trigger words stay PixelLab-specific: pixel art, sprites, characters, objects, tilesets, tilemaps, UI, backgrounds, animations, MCP, REST v2, SDK/API, and PixelLab docs.

## Updating

Marketplace installs are the update path. Pulling this repository is only enough for development; installed agents usually use cached plugin copies.

- Codex: run `codex plugin marketplace upgrade pixellab-pip`.
- Claude Code: run `/plugin marketplace update pixellab-pip`, then `/plugin update pixellab-pip`.
- GitHub Copilot CLI: run `copilot plugin update pixellab-pip`; use `--all` for every installed plugin.
- Gemini CLI: run `gemini extensions update pixellab-pip`.

## Authentication

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Configure the PixelLab bearer token locally as `PIXELLAB_SECRET` or through your agent/MCP host's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into chat.

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Project Layout

```text
README.md
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
.cursor-plugin/marketplace.json
.github/plugin/marketplace.json
gemini-extension.json
GEMINI.md
plugins/
  pixellab-pip/
    plugin.json
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    .cursor-plugin/plugin.json
    skills/
      pixellab-pip/
        SKILL.md
        references/
```

Runtime files:

- `plugins/pixellab-pip/skills/pixellab-pip/SKILL.md` - the canonical skill file.
- `plugins/pixellab-pip/skills/pixellab-pip/references/credentials.md` - PixelLab bearer-token setup, UI naming, and MCP auth-source reuse.
- `plugins/pixellab-pip/skills/pixellab-pip/references/browser-fallback.md` - permission rules for visible website/editor fallback.
- `plugins/pixellab-pip/skills/pixellab-pip/references/paperdolling.md` - layered character and outfit workflow contract.
- `plugins/pixellab-pip/skills/pixellab-pip/references/tilesets.md` - terrain/platformer/tile-variant routing details.
- `plugins/pixellab-pip/skills/pixellab-pip/references/image-inputs.md` - image input roles for attachments, file paths, and endpoint fields.
- `plugins/pixellab-pip/skills/pixellab-pip/references/usage-reporting.md` - usage, balance, job, and result reporting.
- `plugins/pixellab-pip/skills/pixellab-pip/references/official-docs.md` - when and how to refresh official PixelLab docs.

## Design Decisions

- Canonical name: `pixellab-pip`.
- No `/pip` alias folder: aliases are cute, but duplicated skill folders drift and weaken updateability.
- One source of truth: every plugin wrapper points at `plugins/pixellab-pip/skills/pixellab-pip`.
- Plugin-first install: marketplaces are easier to update than copied local skill folders.
- `skills/` directory: this repo can grow to multiple PixelLab skills without moving the first one again.
- Claude versioning: the Claude manifest intentionally omits `version` so git marketplace updates can track commits instead of waiting for a version bump.

## Official PixelLab Links

- MCP endpoint: `https://api.pixellab.ai/mcp`
- MCP docs: `https://api.pixellab.ai/mcp/docs`
- REST v2 docs: `https://api.pixellab.ai/v2/docs`
- REST v2 LLM guide: `https://api.pixellab.ai/v2/llms.txt`
