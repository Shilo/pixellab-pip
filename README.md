# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is friendly on the outside and practical under the collar: he maps plain-language asset requests to the right supported surface, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

<p>
  <a href="https://www.pixellab.ai/"><img src="https://www.pixellab.ai/apple-touch-icon.png" alt="PixelLab logo" width="48" /></a>
</p>

For [PixelLab.ai](https://www.pixellab.ai/).

## Table Of Contents

- [What Pip Does](#what-pip-does)
- [Install](#install)
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

### Marketplace Install

Install PixelLab Pip as a plugin when your agent supports plugins or marketplaces. This keeps the skill updatable and avoids copying runtime files into multiple places.

| Agent app | Install | Update |
|---|---|---|
| Claude Code | `/plugin marketplace add Shilo/pixellab-pip`, then `/plugin install pixellab-pip@pixellab-pip` | `/plugin marketplace update pixellab-pip`, then `/plugin update pixellab-pip` |
| Cursor | This repo includes Cursor marketplace metadata at `.cursor-plugin/marketplace.json`. Use Cursor's plugin marketplace or team marketplace flow when available for your workspace. | Refresh/update the Cursor marketplace entry for this repo. |
| Codex | `codex plugin marketplace add Shilo/pixellab-pip`, then install `pixellab-pip` from `/plugins` or the Codex plugin directory. | `codex plugin marketplace upgrade pixellab-pip` |
| GitHub Copilot CLI | `copilot plugin marketplace add Shilo/pixellab-pip`, then `copilot plugin install pixellab-pip@pixellab-pip` | `copilot plugin update pixellab-pip` |
| VS Code agent plugins | Enable `chat.plugins.enabled`, add `Shilo/pixellab-pip` to `chat.plugins.marketplaces`, or use **Chat: Install Plugin From Source** with this repo URL. | VS Code checks plugin marketplaces for updates automatically when extension updates run. |
| Gemini CLI | `gemini extensions install <repo-url>` using [Shilo/pixellab-pip](https://github.com/Shilo/pixellab-pip) | `gemini extensions update pixellab-pip` |

PixelLab Pip currently targets Claude Code, Cursor, Codex, GitHub Copilot CLI, VS Code agent plugins, and Gemini CLI. It does not auto-install into web-only chats such as Claude.ai, ChatGPT, or Gemini web.

Gemini uses `gemini-extension.json` for installation and `GEMINI.md` for invocation context. Gemini extensions are not native Agent Skills plugins, so those files adapt Gemini to the same Pip instructions in `skills/pixellab-pip/SKILL.md`.

### Agent-Assisted Install

You can try this prompt in a local coding agent that can run plugin-management commands:

> Install PixelLab Pip from [https://github.com/Shilo/pixellab-pip](https://github.com/Shilo/pixellab-pip) using the proper marketplace or plugin workflow for this agent. Prefer marketplace install/update over copying files.

This is mostly useful in Claude Code, Codex, Gemini CLI, GitHub Copilot CLI, or another local agent with shell access. It is not reliable in web-only assistants or agents that cannot install plugins from GitHub.

### Manual Install

Manual install is useful for project-local setup, quick testing, or agent apps that support raw Agent Skills without a marketplace. Copy only the runtime skill folder:

```text
skills/pixellab-pip/
```

into the agent app's documented skill directory. Common examples include:

```text
.agents/skills/pixellab-pip/
.claude/skills/pixellab-pip/
```

Manual copies are harder to update. Prefer plugin install when possible.

### Updating

Marketplace installs are the update path. Pulling this repository is only enough for development; installed agents usually use cached plugin copies.

- Codex: run `codex plugin marketplace upgrade pixellab-pip`.
- Claude Code: run `/plugin marketplace update pixellab-pip`, then `/plugin update pixellab-pip`.
- Cursor: refresh the marketplace or reinstall/update the plugin through Cursor's plugin UI.
- GitHub Copilot CLI: run `copilot plugin update pixellab-pip`; use `--all` for every installed plugin.
- Gemini CLI: run `gemini extensions update pixellab-pip`.

## Usage

Recommended explicit trigger:

```text
/pixellab-pip
```

If your agent app namespaces plugin skills, use the name it shows, such as `pixellab-pip:pixellab-pip`.

Implicit invocation should also work when an agent sees a PixelLab-specific request, such as pixel art, sprites, characters, objects, tilesets, tilemaps, UI, backgrounds, animations, MCP, REST v2, SDK/API, or PixelLab docs. Explicit invocation is still recommended when you want Pip used for sure.

## Authentication

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Configure the PixelLab bearer token locally as `PIXELLAB_SECRET` or through your agent app or MCP server's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into chat.

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
.codex-plugin/plugin.json
plugin.json
skills/
  pixellab-pip/
    SKILL.md
    references/
```

The root plugin files are thin wrappers for each agent app. The only runtime skill is `skills/pixellab-pip/SKILL.md`.

`gemini-extension.json` installs PixelLab Pip as a Gemini CLI extension. `GEMINI.md` gives Gemini the invocation context and points back to the same skill contract; it does not create a second Pip skill.

Runtime files:

- `skills/pixellab-pip/SKILL.md` - the canonical skill file.
- `skills/pixellab-pip/references/credentials.md` - PixelLab bearer-token setup, UI naming, and MCP auth-source reuse.
- `skills/pixellab-pip/references/browser-fallback.md` - permission rules for visible website/editor fallback.
- `skills/pixellab-pip/references/paperdolling.md` - layered character and outfit workflow contract.
- `skills/pixellab-pip/references/tilesets.md` - terrain/platformer/tile-variant routing details.
- `skills/pixellab-pip/references/image-inputs.md` - image input roles for attachments, file paths, and endpoint fields.
- `skills/pixellab-pip/references/usage-reporting.md` - usage, balance, job, and result reporting.
- `skills/pixellab-pip/references/official-docs.md` - when and how to refresh official PixelLab docs.

## Official PixelLab Links

- [PixelLab.ai](https://www.pixellab.ai/)
- [MCP endpoint](https://api.pixellab.ai/mcp)
- [MCP docs](https://api.pixellab.ai/mcp/docs)
- [REST v2 docs](https://api.pixellab.ai/v2/docs)
- [REST v2 LLM guide](https://api.pixellab.ai/v2/llms.txt)
