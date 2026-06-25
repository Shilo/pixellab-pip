<p align="center">
  <a href="docs/showcase/pip.md"><img src="docs/showcase/pip/pip.gif" alt="Pip mascot idle animation" width="68"></a>
</p>

# PixelLab Pip

Meet PixelLab Pip: a tiny pup who fetches the right PixelLab workflow. He follows human commands to create, edit, and animate pixel assets, then sniffs out a bigger prompt, scouts for a useful tool, and carries back what happened.

For [PixelLab.ai](https://www.pixellab.ai/).

> Unofficial community project: PixelLab Pip is not affiliated with PixelLab.

## Table Of Contents

- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Setup MCP / API](#setup-mcp--api)
- [Showcase ↗](docs/showcase/README.md)
- [Developer ↗](docs/developer.md)
- [Resources ↗](docs/resources.md)
- [More Docs ↗](docs/README.md)

## Features

Use Pip when an agent needs to create, edit, animate, integrate, or troubleshoot PixelLab assets and workflows.

| Feature | What Pip helps with |
|---|---|
| Easy PixelLab workflow | Lets users ask for assets in plain language without knowing PixelLab tool names, endpoint names, modes, or editor differences. |
| Smart tool selection | Chooses between MCP, REST v2, website/editor flows, Aseprite, Pixelorama, and legacy v1 based on the task. |
| Guided PixelLab setup | Helps agents set up MCP/API access, diagnose missing auth, and configure only what the user approves without reading or printing the secret value. |
| Answer PixelLab questions | Explains setup, auth, docs, SDKs, troubleshooting, and confusing feature names. |
| Enhance prompts and descriptions | Turns rough user wording, visible inputs, styles, palettes, and constraints into concise PixelLab-ready descriptions, using PixelLab enhance endpoints only when they match the task. |
| Non-English request support | Translates or normalizes PixelLab-facing natural-language inputs to concise English while keeping confirmations, explanations, and reports in the user's language. |
| Use images and attachments correctly | Classifies supplied files as edit targets, identity references, style references, concept images, masks, palettes, init/source images, or animation frames instead of guessing one generic role. |
| Paperdoll and layered workflow guidance | Helps route layered character, outfit, equipment, isolated asset, and composited-output requests without pretending PixelLab returns layers where it does not. |
| Safer auth and automation | Uses bearer-token and MCP secret setup, avoids copied website session tokens, and keeps agents away from undocumented website/session endpoints. |
| Current docs and SDK checks | Tells agents when to refresh official PixelLab docs, OpenAPI schemas, MCP docs, SDK coverage, auth setup, pricing, limits, model labels, or endpoint fields before making exact claims. |
| Clear generation reports | Reports the PixelLab tool or endpoint used, prompt prep method, final natural-language parameters, key controls, IDs, output locations, async status, credit/balance delta when available, and verification status. |
| Bark completion sound | Can play a generic success sound after PixelLab generation-style jobs finish, with a persistent on/off toggle. |
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

You can also download the skill zip from the [latest release](https://github.com/Shilo/pixellab-pip/releases/latest) and extract it into your agent's skills directory.

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

Use Pip with a normal prompt:

```text
/pixellab-pip <prompt>
@pixellab-pip <prompt>
$pixellab-pip <prompt>
pip <prompt>
```

The plain `pip` form can work as an implicit skill call because Pip's metadata describes PixelLab and Pip intents. Explicit invocation is still recommended when you want this skill used for sure. If your agent app namespaces plugin skills, use the name it shows, such as `pixellab-pip:pixellab-pip`.

Examples:

```text
/pixellab-pip make a cute knight character sprite
pip animate this idle character
@pixellab-pip edit this image into cleaner 32px pixel art
```

Implicit invocation should also work when an agent sees PixelLab/Pip context plus setup or asset words such as "setup PixelLab", "configure PixelLab MCP", "connect the PixelLab API", "create an image", "make a sprite", "draw a character", "generate a tileset", "animate this", "edit this image", "use PixelLab MCP", "call the REST API", or "check PixelLab docs". Explicit invocation is still recommended when you want Pip used for sure.

### Commands

#### Setup

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
```

Runs the beginner-friendly PixelLab setup wizard. Pip recommends MCP + API for AI assistants/editors, can configure REST/API fallback for Pip with the same PixelLab Secret, and only changes settings after a token-free preview and explicit approval.

#### Bark

```text
/pixellab-pip bark
@pixellab-pip bark
$pixellab-pip bark
/pixellab-pip bark on
/pixellab-pip bark off
```

Toggles Pip's completion sound. Bark is on by default and persists in `skills/pixellab-pip/pixellab-pip.json` next to `SKILL.md` when the installed skill directory is writable, with an exact user-config fallback only if skill-local persistence fails. Because bark starts on, a first-run `bark` command usually toggles it off without playing; use `bark on` to test the sound. Pip only barks after a live PixelLab generation, edit, transform, conversion, background-removal, or animation job finishes successfully. It does not bark for setup, auth checks, balance/status checks, docs, failed or pending jobs, downloads alone, or local post-processing alone.

The current sound is hardcoded in the bundled helper as `skills/pixellab-pip/assets/bark.wav`. Running `bark` or `bark on` plays the sound immediately when bark ends up on, which doubles as a sound test. If the helper cannot run, Pip falls back to a native system success or alert sound instead of passing an audio file path to the app. Future custom audio can support `.wav`, `.wave`, or `.mp4` without changing the command shape.

## Setup MCP / API

For most users, run `/pixellab-pip setup` and choose MCP + API. MCP connects PixelLab directly to your AI assistant/editor/app, and API fallback lets Pip use documented REST/API routes when MCP tools are unavailable, incomplete, or insufficient.

PixelLab generation requires a PixelLab bearer token and may spend credits. PixelLab Pip does not include, store, or print that token. Do not use copied website session tokens or undocumented website endpoints for automation unless PixelLab documents them as supported.

| Wizard mode | Use it when | What Pip does |
|---|---|---|
| MCP + API | Recommended. You want direct PixelLab tools in your assistant/editor/app plus Pip REST/API fallback. | Sets up MCP first, then confirms the same `PIXELLAB_SECRET` source is visible to the assistant/editor/app session where Pip runs. |
| MCP only | You only want PixelLab MCP tools in your assistant/editor/app. | Detects or asks which app you use, prepares an MCP config preview, and applies it only after confirmation. It prefers app secret settings or an env/secret reference; a hardcoded MCP config is only an explicit user-chosen fallback when the app has no token-free option, and it does not configure Pip REST/API fallback. |
| API only | You only want Pip to use REST/API fallback when MCP tools are unavailable, incomplete, or insufficient. | Configures or verifies `PIXELLAB_SECRET` for Pip fallback without adding MCP. |
| Manual | You want to use PixelLab's website instructions yourself. | Opens or links to [PixelLab's MCP setup page](https://www.pixellab.ai/mcp), tells you to pick your app there, and stops. |

Open the PixelLab [account page](https://www.pixellab.ai/account) after signing in and copy the value labeled `Secret`. PixelLab may call this value an API key, API token, secret, or token. Pip calls it a bearer token for MCP/API auth. Store the token outside chat. The recommended local secret name for Pip REST/API fallback is:

```text
PIXELLAB_SECRET
```

Never paste the Secret into chat, commit it, print it in logs, copy browser session tokens, or ask an agent to scan `.env*`, shell history, home directories, or environment dumps. For deeper setup, auth, and service-boundary details, see [More Docs ↗](docs/README.md) and [PixelLab Auth And Security ↗](docs/pixellab/auth-and-security.md).

## Showcase

Example workflow notes live in [Showcase ↗](docs/showcase/README.md), including prompts, selected routes, outputs, and validation notes for real PixelLab Pip runs.

## MIT License

See [LICENSE ↗](LICENSE).
