# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is lightweight and practical under the collar: he maps plain-language asset requests to the right supported surface, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

For [PixelLab.ai](https://www.pixellab.ai/).

> Unofficial community project: PixelLab Pip is not affiliated with PixelLab.

## Table Of Contents

- [What Pip Does](#what-pip-does)
- [Install](#install)
- [Usage](#usage)
- [Authentication](#authentication)
- [Documentation](#documentation)
- [Showcase](#showcase)
- [Project Layout](#project-layout)
- [Other Tools](#other-tools)
- [PixelLab Resources](#pixellab-resources)

## What Pip Does

Use Pip when an agent needs to create, edit, animate, integrate, or troubleshoot PixelLab assets and workflows.

| Feature | What Pip helps with |
|---|---|
| Asset routing | Maps plain-language requests to the right PixelLab surface for characters, objects, tilesets, tiles, maps, UI, backgrounds, image edits, animations, and VFX. |
| MCP and REST v2 selection | Chooses hosted MCP for managed agent assets, REST v2 for direct API/code/batch control, website/editor flows for human-visible work, Aseprite or Pixelorama for editor workflows, and legacy v1 only when needed. |
| Prompt and description preparation | Turns rough user wording, visible inputs, styles, palettes, and constraints into concise PixelLab-ready descriptions, using PixelLab enhance endpoints only when they match the route. |
| Non-English request support | Translates or normalizes PixelLab-facing natural-language inputs to concise English while keeping confirmations, explanations, and reports in the user's language. |
| Image and attachment handling | Classifies supplied files as edit targets, identity references, style references, concept images, masks, palettes, init/source images, or animation frames instead of guessing one generic role. |
| Paperdoll and layered workflow guidance | Helps route layered character, outfit, equipment, isolated asset, and composited-output requests without pretending PixelLab returns layers where it does not. |
| Safe auth and automation boundaries | Uses bearer-token and MCP secret setup, avoids copied website session tokens, and keeps agents away from undocumented website/session endpoints. |
| Current docs and SDK checks | Tells agents when to refresh official PixelLab docs, OpenAPI schemas, MCP docs, SDK coverage, auth setup, pricing, limits, model labels, or endpoint fields before making exact claims. |
| Usage and result reporting | Reports the surface, tool or endpoint, prompt prep method, final natural-language parameters, key controls, IDs, output locations, async status, credit/balance delta when available, and verification status. |
| PixelLab terminology support | Explains confusing labels such as `Pro`, `v3`, `new`, `create tiles`, `create tileset`, Pixen, PixFlux, BitForge, and PixPatch at the documented product level. |

## Install

### Agent-Assisted Install

You can try this first in local coding agents that can run plugin-management commands:

> Install PixelLab Pip from [https://github.com/Shilo/pixellab-pip](https://github.com/Shilo/pixellab-pip) using the proper marketplace or plugin workflow for this agent. Prefer marketplace install/update over copying files.

This is realistic for Claude Code, Codex, Gemini CLI, and GitHub Copilot CLI. It may work in Cursor when the agent can run shell commands or plugin commands. It is not reliable in VS Code UI-only flows or web-only chats such as Claude.ai, ChatGPT, or Gemini web.

### Marketplace Install

Install PixelLab Pip as a plugin when your agent supports plugins or marketplaces. This keeps the skill updatable and avoids copying runtime files into multiple places.

| Agent app | Install | Update |
|---|---|---|
| Claude Code | `/plugin marketplace add Shilo/pixellab-pip`, then `/plugin install pixellab-pip@pixellab-pip` | `/plugin marketplace update pixellab-pip`, then `/plugin update pixellab-pip` |
| Cursor | This repo includes Cursor marketplace metadata at `.cursor-plugin/marketplace.json`. Use Cursor's plugin marketplace or team marketplace flow when available for your workspace. | Refresh/update the Cursor marketplace entry for this repo. |
| Codex | `codex plugin marketplace add Shilo/pixellab-pip`, then install `pixellab-pip` from `/plugins` or the Codex plugin directory. | `codex plugin marketplace upgrade pixellab-pip` |
| GitHub Copilot CLI | `copilot plugin marketplace add Shilo/pixellab-pip`, then `copilot plugin install pixellab-pip@pixellab-pip` | `copilot plugin update pixellab-pip` |
| VS Code agent plugins | Enable `chat.plugins.enabled`, add `Shilo/pixellab-pip` to `chat.plugins.marketplaces`, or use **Chat: Install Plugin From Source** with this repo URL. | VS Code checks plugin marketplaces for updates automatically when extension updates run. |
| Gemini CLI | `gemini extensions install https://github.com/Shilo/pixellab-pip` | `gemini extensions update pixellab-pip` |

PixelLab Pip is agent-agnostic. It can be used by any agent app that supports Agent Skills or compatible plugin/extension wrappers. This repo includes ready-to-use metadata for Claude Code, Cursor, Codex, GitHub Copilot CLI, VS Code agent plugins, and Gemini CLI.

Gemini uses `gemini-extension.json` for installation and `GEMINI.md` for invocation context. Gemini extensions are not native Agent Skills plugins, so those files adapt Gemini to the same Pip instructions in `skills/pixellab-pip/SKILL.md`.

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

Example prompt:

```text
/pixellab-pip make a cute knight character sprite
```

Implicit invocation should also work when an agent sees a PixelLab-specific request such as "create an image", "make a sprite", "draw a character", "generate a tileset", "animate this", "edit this image", "use PixelLab MCP", "call the REST API", or "check PixelLab docs". Explicit invocation is still recommended when you want Pip used for sure.

## Authentication

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Get your secret token from the PixelLab [account page](https://www.pixellab.ai/account) after signing in, or follow PixelLab's [MCP setup page](https://www.pixellab.ai/mcp). Configure it locally as `PIXELLAB_SECRET` or through your agent app or MCP server's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into chat.

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Documentation

Supplemental PixelLab technical notes live in [docs/pixellab/](docs/pixellab/). They explain PixelLab surfaces, asset routing, terminology, SDK compatibility, and auth/security boundaries for agents that need deeper implementation context.

## Showcase

Future examples and generated showcase notes will live in [docs/showcase/](docs/showcase/). The first planned showcase is using Pip to route and generate its own Pixel Pup icon.

## Project Layout

```text
README.md
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
.claude-plugin/plugin.json
.cursor-plugin/marketplace.json
.cursor-plugin/plugin.json
.github/plugin/marketplace.json
gemini-extension.json
GEMINI.md
.codex-plugin/plugin.json
plugin.json
docs/
  showcase/
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
- `skills/pixellab-pip/references/localization.md` - non-English request translation and response-language handling.
- `skills/pixellab-pip/references/usage-reporting.md` - usage, balance, job, and result reporting.
- `skills/pixellab-pip/references/official-docs.md` - when and how to refresh official PixelLab docs.

## Other Tools

### [PixelLab AI Skill](https://clawhub.ai/uncmatteth/skills/pixellab-ai) (By [@uncmatteth](https://clawhub.ai/uncmatteth))

An **unofficial** asset workflow and API helper for pixel-art generation, conversion, rotation, animation, layered sprites, modular outfits/equipment, tilesets, UI assets, and prompt enhancement.

Use PixelLab AI Skill for its recipe, manifest, and helper-script production workflow. Use Pip for concise, agent-agnostic PixelLab surface routing across MCP, REST v2, website/editor, Aseprite, Pixelorama, and legacy v1. Pip does not install or run PixelLab AI Skill's helper scripts.

### [Ultimate PixelLab Prompt Generator](https://pixellabpromptgenerator.vercel.app/) (By TheSyntheticFeed)

An **unofficial** browser tool for building PixelLab-style pixel-art prompts from deterministic option sets such as asset type, perspective, camera direction, effects, materials, art style, color, and palette. It also includes a no-API prompt enhancer and a shading/lighting reference guide.

Use it when you want to manually craft or learn stronger PixelLab prompts before generation. Use Pip when you want an agent to route the request, choose the right PixelLab surface, handle auth boundaries, or provide API/MCP implementation guidance.

### [Vibe Coding AI Toolkit](https://www.pixellab.ai/mcp) (By [PixelLab](https://pixellab.ai))

PixelLab's MCP setup page for connecting PixelLab to AI coding assistants. It helps users configure direct MCP access so an agent can generate game-ready characters, animations, tilesets, and map objects inside coding workflows.

Use the Vibe Coding AI Toolkit directly when you already know MCP is the right surface and want to configure PixelLab tools in a supported MCP client. Use Pip when you want an agent to decide whether MCP, REST v2, website/editor workflows, Aseprite, Pixelorama, legacy v1, or SDK/API docs are the right route.

### [PixelLab API](https://www.pixellab.ai/pixellab-api) (By [PixelLab](https://pixellab.ai))

PixelLab's official API catalog for programmatic pixel-art generation, editing, animation, tilesets, characters, objects, prompt enhancement, Pro tools, pricing, and endpoint links.

Use the PixelLab API directly when you are writing code against REST v2 and already know the endpoint you need. Use Pip when you want help choosing the endpoint or deciding whether REST v2, MCP, website/editor workflows, SDKs, or legacy v1 are a better fit.

## PixelLab Resources

- [PixelLab.ai](https://www.pixellab.ai/) - PixelLab's official product homepage.
- [Account page](https://www.pixellab.ai/account) - Sign in and get the PixelLab token used for REST/MCP bearer auth.
- [Vibe Coding AI Toolkit](https://www.pixellab.ai/mcp) - Official PixelLab MCP setup page for AI coding assistants.
- [PixelLab API](https://www.pixellab.ai/pixellab-api) - Official PixelLab API catalog with endpoint families, pricing summaries, and docs links.
- [MCP endpoint](https://api.pixellab.ai/mcp) - Hosted PixelLab MCP endpoint for compatible agent clients.
- [MCP docs](https://api.pixellab.ai/mcp/docs) - Official PixelLab MCP tool and setup documentation.
- [REST v2 docs](https://api.pixellab.ai/v2/docs) - Interactive official REST v2 API documentation.
- [REST v2 LLM guide](https://api.pixellab.ai/v2/llms.txt) - LLM-readable REST v2 endpoint guide and auth summary.
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) - Exact current REST v2 schemas for endpoint, field, enum, and response verification.
