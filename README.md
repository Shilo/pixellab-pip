# PixelLab Pip

Meet PixelLab Pip: a tiny Pixel Pup who fetches the right route through PixelLab's MCP tools, REST v2 API, website/editor workflows, Aseprite, Pixelorama, and legacy v1.

Pip is helpful and practical under the collar: he maps plain-language requests to the right PixelLab tool or workflow, keeps agents away from undocumented website/session endpoints, and helps untangle overlapping tool names, endpoint paths, model labels, and editor workflows.

For [PixelLab.ai](https://www.pixellab.ai/).

> Unofficial community project: PixelLab Pip is not affiliated with PixelLab.

## Table Of Contents

- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Commands](#commands)
- [MCP And API Setup](#mcp-and-api-setup)
- [Authentication](#authentication)
- [Documentation](#documentation)
- [Showcase](#showcase)
- [Repository Layout](#repository-layout)
- [Other Tools](#other-tools)
- [PixelLab Resources](#pixellab-resources)
- [License](#license)

## Features

Use Pip when an agent needs to create, edit, animate, integrate, or troubleshoot PixelLab assets and workflows.

| Feature | What Pip helps with |
|---|---|
| Easy PixelLab workflow | Lets users ask for assets in plain language without knowing PixelLab tool names, endpoint names, modes, or editor differences. |
| Smart tool selection | Chooses between MCP, REST v2, website/editor flows, Aseprite, Pixelorama, and legacy v1 based on the task. |
| Guided PixelLab setup | Helps agents set up MCP/API access, diagnose missing auth, and configure only what the user approves without reading or printing the secret value. |
| Answer PixelLab questions | Explains setup, auth, docs, SDKs, troubleshooting, and confusing feature names. |
| Improve prompts and descriptions | Turns rough user wording, visible inputs, styles, palettes, and constraints into concise PixelLab-ready descriptions, using PixelLab enhance endpoints only when they match the task. |
| Non-English request support | Translates or normalizes PixelLab-facing natural-language inputs to concise English while keeping confirmations, explanations, and reports in the user's language. |
| Use images and attachments correctly | Classifies supplied files as edit targets, identity references, style references, concept images, masks, palettes, init/source images, or animation frames instead of guessing one generic role. |
| Paperdoll and layered workflow guidance | Helps route layered character, outfit, equipment, isolated asset, and composited-output requests without pretending PixelLab returns layers where it does not. |
| Safer auth and automation | Uses bearer-token and MCP secret setup, avoids copied website session tokens, and keeps agents away from undocumented website/session endpoints. |
| Current docs and SDK checks | Tells agents when to refresh official PixelLab docs, OpenAPI schemas, MCP docs, SDK coverage, auth setup, pricing, limits, model labels, or endpoint fields before making exact claims. |
| Clear generation reports | Reports the PixelLab tool or endpoint used, prompt prep method, final natural-language parameters, key controls, IDs, output locations, async status, credit/balance delta when available, and verification status. |
| PixelLab terminology support | Explains confusing labels such as `Pro`, `v3`, `new`, `create tiles`, `create tileset`, Pixen, PixFlux, BitForge, and PixPatch at the documented product level. |
| Agent-agnostic | Works with any agent that supports Agent Skills. |
| Privacy-focused setup | Helps users connect PixelLab without exposing token values, dumping environment variables, or inspecting private `.env*` files. |

## Install

### Agent-Assisted Install

Ask your local coding agent:

```text
Install PixelLab Pip from https://github.com/Shilo/pixellab-pip using the proper marketplace or plugin workflow for this agent. Prefer marketplace install/update over copying files.
Then run `/pixellab-pip setup` or `@pixellab-pip setup`.
```

### Marketplace Install

Install PixelLab Pip as a plugin or extension when your agent supports marketplaces. Use manual skill install only when your agent does not support plugin installation.

#### Claude Code

Install:

```text
/plugin marketplace add Shilo/pixellab-pip
/plugin install pixellab-pip@pixellab-pip
/pixellab-pip setup
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
# Install pixellab-pip from /plugins or the Codex plugin directory.
@pixellab-pip setup
```

Update:

```text
codex plugin marketplace upgrade pixellab-pip
```

#### Gemini CLI

Install:

```text
gemini extensions install https://github.com/Shilo/pixellab-pip
/pixellab-pip setup
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
/pixellab-pip setup
```

Update:

```text
copilot plugin update pixellab-pip
```

#### Cursor

Use Cursor's plugin marketplace or team marketplace flow when available, or install the raw skill manually.

```text
/pixellab-pip setup
```

#### VS Code Agent Plugins

Use **Chat: Install Plugin From Source** with this repo URL or VS Code's plugin marketplace flow.

```text
/pixellab-pip setup
```

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
# Then run in Codex: $pixellab-pip setup
```

macOS/Linux shell:

```bash
mkdir -p .agents/skills/pixellab-pip
cp -R skills/pixellab-pip/. .agents/skills/pixellab-pip/
# Then run in Codex: $pixellab-pip setup
```

Use `.claude/skills/pixellab-pip` or `.cursor/skills/pixellab-pip` instead if that is the skill directory your assistant reads.

## Usage

Recommended explicit trigger:

```text
/pixellab-pip
@pixellab-pip
$pixellab-pip
```

If your agent app namespaces plugin skills, use the name it shows, such as `pixellab-pip:pixellab-pip`.

Example prompt:

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
/pixellab-pip make a cute knight character sprite
```

Implicit invocation should also work when an agent sees PixelLab/Pip context plus setup or asset words such as "setup PixelLab", "configure PixelLab MCP", "connect the PixelLab API", "create an image", "make a sprite", "draw a character", "generate a tileset", "animate this", "edit this image", "use PixelLab MCP", "call the REST API", or "check PixelLab docs". Explicit invocation is still recommended when you want Pip used for sure.

## Commands

### Setup

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
```

Runs the beginner-friendly PixelLab setup wizard. Pip recommends MCP + API for AI assistants/editors, can configure REST/API fallback for Pip with the same PixelLab Secret, and only changes settings after a token-free preview and explicit approval.

## MCP And API Setup

For most users, run `/pixellab-pip setup` and choose MCP + API. MCP connects PixelLab directly to your AI assistant/editor/app, and API fallback lets Pip use documented REST/API routes when MCP tools are unavailable, incomplete, or insufficient.

The setup command behaves like a wizard, not a static help page. It infers what it can, asks at most the next short question when needed, and keeps secrets out of chat and shared files.

| Wizard mode | Use it when | What Pip does |
|---|---|---|
| MCP + API | Recommended. You want direct PixelLab tools in your assistant/editor/app plus Pip REST/API fallback. | Sets up MCP first, then confirms the same `PIXELLAB_SECRET` source is visible to the assistant/editor/app session where Pip runs. |
| MCP only | You only want PixelLab MCP tools in your assistant/editor/app. | Detects or asks which app you use, prepares an MCP config preview, and applies it only after confirmation. This may use an app secret setting, an env/secret reference, or a user-chosen hardcoded MCP config when the app has no token-free option. |
| API only | You only want Pip to use REST/API fallback when MCP tools are unavailable, incomplete, or insufficient. | Configures or verifies `PIXELLAB_SECRET` for Pip fallback without adding MCP. |
| Manual | You want to use PixelLab's website instructions yourself. | Opens or links to [PixelLab's MCP setup page](https://www.pixellab.ai/mcp), tells you to pick your app there, and stops. |

PixelLab Pip can tailor MCP setup for the supported assistant/app names already used by this project: Claude Code, Codex, Gemini CLI, Cursor, VS Code Agent Plugins, GitHub Copilot CLI, and generic MCP-compatible apps. It stays agent-agnostic and OS-agnostic until the detected or named app requires a specific settings location.

MCP + API and API-only setup require `PIXELLAB_SECRET` because Pip needs that local secret source for REST/API fallback. MCP-only setup also needs the PixelLab account Secret, but some MCP clients can store it directly in their own config instead of exposing it as `PIXELLAB_SECRET`.

Open the PixelLab [account page](https://www.pixellab.ai/account) after signing in and copy the value labeled `Secret`. PixelLab may call this value an API key, API token, secret, or token. Pip calls it a bearer token for MCP/API auth.

Store the token outside chat. The recommended local secret name is:

```text
PIXELLAB_SECRET
```

Token setup options, from safest default to more manual:

1. App/editor secret settings or app secret store named `PIXELLAB_SECRET`.
2. OS user environment-variable UI for `PIXELLAB_SECRET`.
3. A hidden local prompt or secret-store command that does not put the Secret in command text.
4. A normal external terminal command such as `setx`, `export`, or PowerShell env setup if you accept shell-history/process-history tradeoffs.
5. A project-local file such as `.env.local` or `.pixellab`, only when a specific helper, dotenv loader, or wrapper explicitly reads it. Project-local files do not configure MCP, Codex, Claude, Pip, your terminal, or the OS by themselves.

Do not run literal-Secret commands through assistant prompt lines, Claude/Codex shell escapes, or a Codex-readable integrated terminal. `setx` and `export` are not forbidden; the risk is putting the actual Secret in command text that can be saved or exposed. If a Secret is pasted into chat or visible tool output, treat it as exposed and replace it before continuing setup.

### What The Wizard Is Allowed To Do

- Detect the current assistant/editor/app when possible, or ask which one you use.
- Inspect only the specific config path or setting it explains and you approve; it should not scan home directories or existing `.env*` files.
- Prefer app secret settings, OS/user-level environment settings, or an app secret store named `PIXELLAB_SECRET`.
- Show a token-free preview before writing any environment variable, app config, MCP settings file, shell profile, or loader-backed project-local secret file.
- Use `https://api.pixellab.ai/mcp` for MCP and `https://api.pixellab.ai/v2` for REST API.
- Verify setup only after you approve a no-credit check, such as MCP `get_balance` or REST `GET /balance`.

Pip must never ask you to paste the Secret into chat, print it, echo it, log it, summarize it, transform it, use it from chat/tool output, or show raw auth headers. If you choose Manual, Pip should only open or link to `https://www.pixellab.ai/mcp`, tell you to pick your app there, and stop.

### Recommended: MCP

Choose MCP when you want PixelLab tools inside an AI assistant/editor/app. Pip should configure your app to use:

```text
https://api.pixellab.ai/mcp
```

with authorization supplied from a private `PIXELLAB_SECRET` setting, for example:

```text
Authorization: Bearer <PIXELLAB_SECRET>
```

In docs and previews, `<PIXELLAB_SECRET>` means a reference to the private local secret, not a value to paste into chat. Use your app's secret settings when available. If the app requires a config file, keep that file private and do not commit it.

Some apps, including some Claude Code MCP header flows, may not provide a reliable token-free secret reference. In that case Pip should not write the config automatically. It can instead offer a manual fallback command for you to run in your own external terminal, with a placeholder such as `<paste-your-Secret-here>`, after warning that the app may store the raw Secret in local MCP config or shell history. That can make MCP-only work, but it does not configure `PIXELLAB_SECRET` for Pip REST/API fallback.

### Backup: REST v2 API

Use the REST API setup path when you want Pip to fall back to documented REST/API routes because MCP tools are unavailable, incomplete, or insufficient for the requested PixelLab workflow.

For REST v2 API calls, Pip uses the same PixelLab account Secret stored as `PIXELLAB_SECRET` and sends:

```text
Authorization: Bearer <PIXELLAB_SECRET>
```

Setup mode should not micromanage your frameworks, scripts, backends, SDKs, package files, or deployment platforms. Once `PIXELLAB_SECRET` is visible to the assistant/editor/app session, Pip can route REST calls internally when fallback is needed. Do not paste the Secret into chat, commit it, put it in examples, print it in logs, copy browser session tokens, or ask an agent to scan `.env*`, shell history, home directories, or environment dumps.

## Authentication

PixelLab generation requires a PixelLab bearer token and may spend credits. PixelLab Pip does not include, store, or print that token. For setup steps, see [MCP And API Setup](#mcp-and-api-setup).

Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

## Documentation

Supplemental PixelLab technical notes live in [docs/pixellab/](docs/pixellab/). They explain PixelLab tools, workflows, terminology, SDK compatibility, and auth/security boundaries for agents that need deeper implementation context.

## Showcase

Example workflow notes live in [docs/showcase/](docs/showcase/), including prompts, selected routes, outputs, and validation notes for real PixelLab Pip runs.

## Repository Layout

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
- `skills/pixellab-pip/references/setup.md` - natural-language setup mode for MCP/API/auth after install.
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

Use PixelLab AI Skill for its recipe, manifest, and helper-script production workflow. Its `.env.local` pattern works because its helper auto-loads that file. Use Pip for concise, agent-agnostic PixelLab tool selection across MCP, REST v2, website/editor, Aseprite, Pixelorama, and legacy v1. Pip does not install or run PixelLab AI Skill's helper scripts, and copying that `.env.local` pattern is not enough unless a loader or wrapper reads it.

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
