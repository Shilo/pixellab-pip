# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is helpful and practical under the collar: he maps plain-language requests to the right PixelLab tool or workflow, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

For [PixelLab.ai](https://www.pixellab.ai/).

> Unofficial community project: PixelLab Pip is not affiliated with PixelLab.

## Table Of Contents

- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Authentication](#authentication)
- [Documentation](#documentation)
- [Showcase](#showcase)
- [Project Layout](#project-layout)
- [Other Tools](#other-tools)
- [PixelLab Resources](#pixellab-resources)
- [License](#license)

## Features

Use Pip when an agent needs to create, edit, animate, integrate, or troubleshoot PixelLab assets and workflows.

| Feature | What Pip helps with |
|---|---|
| Create and edit game art | Helps agents create characters, objects, tilesets, tiles, maps, UI, backgrounds, icons, image edits, animations, and VFX. |
| Pick the right PixelLab tool | Chooses hosted MCP for managed agent assets, REST v2 for direct API/code/batch control, website/editor flows for visible work, Aseprite or Pixelorama for editor workflows, and legacy v1 only when needed. |
| Answer PixelLab questions | Answers questions about PixelLab tools, endpoints, docs, setup, auth, SDKs, model labels, troubleshooting, and confusing feature names. |
| Improve prompts and descriptions | Turns rough user wording, visible inputs, styles, palettes, and constraints into concise PixelLab-ready descriptions, using PixelLab enhance endpoints only when they match the task. |
| Non-English request support | Translates or normalizes PixelLab-facing natural-language inputs to concise English while keeping confirmations, explanations, and reports in the user's language. |
| Use images and attachments correctly | Classifies supplied files as edit targets, identity references, style references, concept images, masks, palettes, init/source images, or animation frames instead of guessing one generic role. |
| Paperdoll and layered workflow guidance | Helps route layered character, outfit, equipment, isolated asset, and composited-output requests without pretending PixelLab returns layers where it does not. |
| Safer auth and automation | Uses bearer-token and MCP secret setup, avoids copied website session tokens, and keeps agents away from undocumented website/session endpoints. |
| Current docs and SDK checks | Tells agents when to refresh official PixelLab docs, OpenAPI schemas, MCP docs, SDK coverage, auth setup, pricing, limits, model labels, or endpoint fields before making exact claims. |
| Clear generation reports | Reports the PixelLab tool or endpoint used, prompt prep method, final natural-language parameters, key controls, IDs, output locations, async status, credit/balance delta when available, and verification status. |
| PixelLab terminology support | Explains confusing labels such as `Pro`, `v3`, `new`, `create tiles`, `create tileset`, Pixen, PixFlux, BitForge, and PixPatch at the documented product level. |
| Agent-agnostic | Works with any agent that supports Agent Skills. |

## Install

### Agent-Assisted Install

Ask your local coding agent:

```text
Install PixelLab Pip from https://github.com/Shilo/pixellab-pip using the proper marketplace or plugin workflow for this agent. Prefer marketplace install/update over copying files.
```

### Marketplace Install

Install PixelLab Pip as a plugin or extension when your agent supports marketplaces. Use manual skill install only when your agent does not support plugin installation.

#### Claude Code

Install:

```text
/plugin marketplace add Shilo/pixellab-pip
/plugin install pixellab-pip@pixellab-pip
```

Update:

```text
/plugin marketplace update pixellab-pip
/plugin update pixellab-pip
```

#### Codex

Install:

```text
codex plugin marketplace add Shilo/pixellab-pip
```

Then install `pixellab-pip` from `/plugins` or the Codex plugin directory.

Update:

```text
codex plugin marketplace upgrade pixellab-pip
```

#### Gemini CLI

Install:

```text
gemini extensions install https://github.com/Shilo/pixellab-pip
```

Gemini uses `gemini-extension.json` for installation and `GEMINI.md` for invocation context. Both point back to the same skill contract in `skills/pixellab-pip/SKILL.md`.

Update:

```text
gemini extensions update pixellab-pip
```

#### GitHub Copilot CLI

Install:

```text
copilot plugin marketplace add Shilo/pixellab-pip
copilot plugin install pixellab-pip@pixellab-pip
```

Update:

```text
copilot plugin update pixellab-pip
```

#### Cursor

Use Cursor's plugin marketplace or team marketplace flow when available, or install the raw skill manually.

#### VS Code Agent Plugins

Use **Chat: Install Plugin From Source** with this repo URL or VS Code's plugin marketplace flow.

### Manual Skill Install

Manual install is useful for project-local setup or agent apps that support raw Agent Skills without plugin installation. Copy the contents of `skills/pixellab-pip/` into a folder named `pixellab-pip` inside your agent's skills directory, so `SKILL.md` is directly inside the final folder.

```text
.agents/skills/pixellab-pip/SKILL.md
.claude/skills/pixellab-pip/SKILL.md
.cursor/skills/pixellab-pip/SKILL.md
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force .agents\skills\pixellab-pip
Copy-Item -Recurse -Force skills\pixellab-pip\* .agents\skills\pixellab-pip\
```

macOS/Linux shell:

```bash
mkdir -p .agents/skills/pixellab-pip
cp -R skills/pixellab-pip/. .agents/skills/pixellab-pip/
```

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

Implicit invocation should also work when an agent sees PixelLab/Pip context plus asset words such as "create an image", "make a sprite", "draw a character", "generate a tileset", "animate this", "edit this image", "use PixelLab MCP", "call the REST API", or "check PixelLab docs". Explicit invocation is still recommended when you want Pip used for sure.

## Authentication

PixelLab generation requires a PixelLab bearer token and may spend credits. This skill does not include or store that token.

Get your secret token from the PixelLab [account page](https://www.pixellab.ai/account) after signing in, or follow PixelLab's [MCP setup page](https://www.pixellab.ai/mcp). Configure it locally as `PIXELLAB_SECRET` or through your agent app or MCP server's secret configuration. PixelLab UI/docs may call the same value an API key, API token, or secret; for REST/MCP bearer auth, call it a bearer token. Do not paste the token into chat.

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Documentation

Supplemental PixelLab technical notes live in [docs/pixellab/](docs/pixellab/). They explain PixelLab tools, workflows, terminology, SDK compatibility, and auth/security boundaries for agents that need deeper implementation context.

## Showcase

Example workflow notes live in [docs/showcase/](docs/showcase/), including prompts, selected routes, outputs, and validation notes for real PixelLab Pip runs.

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

Use PixelLab AI Skill for its recipe, manifest, and helper-script production workflow. Use Pip for concise, agent-agnostic PixelLab tool selection across MCP, REST v2, website/editor, Aseprite, Pixelorama, and legacy v1. Pip does not install or run PixelLab AI Skill's helper scripts.

### [Ultimate PixelLab Prompt Generator](https://pixellabpromptgenerator.vercel.app/) (By TheSyntheticFeed)

An **unofficial** browser tool for building PixelLab-style pixel-art prompts from deterministic option sets such as asset type, perspective, camera direction, effects, materials, art style, color, and palette. It also includes a no-API prompt enhancer and a shading/lighting reference guide.

Use it when you want to manually craft or learn stronger PixelLab prompts before generation. Use Pip when you want an agent to choose the right PixelLab tool, handle auth boundaries, or provide API/MCP implementation guidance.

### [Vibe Coding AI Toolkit](https://www.pixellab.ai/mcp) (By [PixelLab](https://pixellab.ai))

PixelLab's MCP setup page for connecting PixelLab to AI coding assistants. It helps users configure direct MCP access so an agent can generate game-ready characters, animations, tilesets, and map objects inside coding workflows.

Use the Vibe Coding AI Toolkit directly when you already know MCP is the right tool and want to configure PixelLab tools in a supported MCP client. Use Pip when you want an agent to decide whether MCP, REST v2, website/editor workflows, Aseprite, Pixelorama, legacy v1, or SDK/API docs are the right route.

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

## License

MIT. See [LICENSE](LICENSE).
