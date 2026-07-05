<p align="center">
  <a href="docs/showcase/pip-mascot.md"><img src="docs/showcase/pip/pip.gif" alt="Pip mascot idle animation" width="68"></a>
</p>

# PixelLab Pip

[![Skill Security Audit](https://github.com/Shilo/pixellab-pip/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Shilo/pixellab-pip/security/code-scanning)

Meet PixelLab Pip: a tiny pup who fetches the right PixelLab workflow. He follows human commands to create, edit, and animate pixel assets, then sniffs out a bigger prompt, scouts for a useful tool, and carries back what happened.

For [PixelLab.ai](https://www.pixellab.ai/).

> Unofficial community project: PixelLab Pip is not affiliated with PixelLab.

## Table Of Contents

- [Features](#features)
- [Install](#install)
- [Usage](#usage)
- [Setup MCP / API](#setup-mcp--api)
- [Security](#security)
- [Benchmark](#benchmark)
- [Showcase ↗](docs/showcase/README.md)
- [Developer ↗](docs/developer.md)
- [Resources ↗](docs/resources.md)
- [More Documentation ↗](docs/README.md)
- [MIT License ↗](LICENSE)

## Features

Use me when you need to create, edit, animate, integrate, or troubleshoot PixelLab assets and workflows.

| Feature | What you can ask me to do |
|---|---|
| Easy PixelLab workflow | Ask for assets in plain language without knowing PixelLab tool names, endpoint names, modes, or editor differences. |
| Smart tool selection | Choose between MCP, REST v2, website/editor flows, Aseprite, Pixelorama, and legacy v1 based on the task. |
| Guided PixelLab setup | Set up MCP/API access, diagnose missing auth, and configure only what you approve without reading or printing the secret value. |
| Answer PixelLab questions | Explain setup, auth, docs, SDKs, troubleshooting, and confusing feature names. |
| Auto-enhance prompts and descriptions | Turn rough wording, visible inputs, styles, palettes, and constraints into concise PixelLab-ready descriptions by default, with opt-out support. |
| Non-English request support | Translate or normalize PixelLab-facing natural-language inputs to concise English while keeping confirmations, explanations, and reports in your language. |
| Use images and attachments correctly | Classify supplied files as edit targets, identity references, style references, concept images, masks, palettes, init/source images, or animation frames instead of guessing one generic role. |
| Fallback background removal | When a requested transparent asset still comes back with a background, verify a safe local cleanup first and fall back to PixelLab background removal when uncertain. |
| Paperdoll and layered workflow guidance | Route layered character, outfit, equipment, isolated asset, and composited-output requests without pretending PixelLab returns layers where it does not. |
| Local Aseprite CLI workspaces | Move generated assets into Aseprite without driving the PixelLab extension UI: create or update `.aseprite` copies, import frames as layers/tags, export PNG sequences, GIFs, sprite sheets, and metadata, or locally clamp/reduce colors to palettes such as 1-bit black/white, Game Boy green, PICO-8, or supplied hex colors through documented Aseprite CLI/Lua. |
| Safer auth and automation | Use bearer-token and MCP secret setup, avoid copied website session tokens, and stay away from undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension. |
| Current docs and SDK checks | Refresh official PixelLab docs, OpenAPI schemas, MCP docs, SDK coverage, auth setup, pricing, limits, model labels, or endpoint fields before making exact claims. |
| Clear generation reports | Report the PixelLab tool or endpoint used, prompt prep method, final natural-language parameters, key controls, IDs, output locations, async status, credit/balance delta when available, and verification status. |
| Bark completion sound | Play a generic success sound after PixelLab generation-style jobs finish, with a persistent on/off toggle. |
| PixelLab terminology support | Explain confusing labels such as `Pro`, `v3`, `new`, `create tiles`, `create tileset`, Pixen, PixFlux, BitForge, and PixPatch at the documented product level. |
| Agent-agnostic | Work from any agent that supports Agent Skills. |
| Privacy-focused setup | Connect PixelLab without exposing token values, dumping environment variables, or inspecting private `.env*` files. |

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
codex plugin add pixellab-pip@pixellab-pip
@pixellab-pip setup
```

Update:

```text
codex plugin marketplace upgrade pixellab-pip
codex plugin remove pixellab-pip
codex plugin add pixellab-pip@pixellab-pip
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

The plain `pip` form can work as an implicit skill call because Pip's metadata describes PixelLab and Pip intents. Explicit `/pixellab-pip` invocation is still recommended when you want this skill used for sure.

Examples:

```text
/pixellab-pip make a cute knight character sprite
pip animate this idle character
@pixellab-pip edit this image into cleaner 32px pixel art
@pixellab-pip create a tiny potion sprite, then make an Aseprite workspace with frames, a tag, a GIF preview, and a sprite sheet
@pixellab-pip create a mossy top-down tileset, then clamp the result to 1-bit black and white
@pixellab-pip make a small item icon sheet and reduce it to a Game Boy green palette
```

Implicit invocation should also work when an agent sees PixelLab/Pip context plus setup or asset words such as "setup PixelLab", "configure PixelLab MCP", "connect the PixelLab API", "create an image", "make a sprite", "draw a character", "generate a tileset", "animate this", "edit this image", "use PixelLab MCP", "call the REST API", or "check PixelLab docs". Explicit invocation is still recommended when you want Pip used for sure.

### Commands

#### Setup

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
```

Runs the beginner-friendly PixelLab setup wizard. Pip recommends MCP + API for AI assistants/editors, can configure documented REST v2 fallback for Pip with the same PixelLab Secret, and only changes settings after a token-free preview and explicit approval.

#### Bark

```text
/pixellab-pip bark
@pixellab-pip bark
$pixellab-pip bark
/pixellab-pip bark on
/pixellab-pip bark off
```

Toggles Pip's completion sound. Bark is on by default and persists in `skills/pixellab-pip/pixellab-pip.json` next to `SKILL.md` when the installed skill directory is writable, with an exact user-config fallback only if skill-local persistence fails. Because bark starts on, a first-run `bark` command usually toggles it off without playing; use `bark on` to test the sound. Pip only barks after a live PixelLab generation, edit, transform, conversion, background-removal, or animation job finishes successfully. It does not bark for setup, auth checks, balance/status checks, docs, failed or pending jobs, downloads alone, or local post-processing alone.

The current sound is hardcoded in the bundled helper as `skills/pixellab-pip/assets/bark.wav`. Running `bark` or `bark on` plays the sound immediately when bark ends up on, which doubles as a sound test. If the helper cannot run, Pip falls back to a native system success or alert sound instead of passing an audio file path to the app.

## Setup MCP / API

For most users, run `/pixellab-pip setup` and choose MCP + API. MCP connects PixelLab directly to your AI assistant/editor/app, and API fallback means documented REST v2 fallback when MCP tools are unavailable, incomplete, or insufficient.

Bundled helper scripts require Python 3.10 or newer when your agent runs local tooling such as background-removal validation, bark configuration, docs-drift checks, or release QA.

PixelLab generation requires a PixelLab bearer token and may spend credits. PixelLab Pip does not include, store, or print that token. Do not use copied website session tokens or undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension for automation unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools.

| Wizard mode | Use it when | What Pip does |
|---|---|---|
| MCP + API | Recommended. You want direct PixelLab tools in your assistant/editor/app plus Pip REST v2 fallback. | Sets up MCP first, then confirms the same `PIXELLAB_SECRET` source is visible to the assistant/editor/app session where Pip runs. |
| MCP only | You only want PixelLab MCP tools in your assistant/editor/app. | Detects or asks which app you use, prepares an MCP config preview, and applies it only after confirmation. It prefers app secret settings or an env/secret reference; a hardcoded MCP config is only an explicit user-chosen fallback when the app has no token-free option, and REST-only features will not be available through Pip fallback. |
| API only | You only want Pip to use REST v2 fallback when MCP tools are unavailable, incomplete, or insufficient. | Configures or verifies `PIXELLAB_SECRET` for Pip fallback without adding MCP. |
| Manual | You want to use PixelLab's website instructions yourself. | Opens or links to [PixelLab's MCP setup page](https://www.pixellab.ai/mcp), tells you to pick your app there, and stops. |

Open the PixelLab [account page](https://www.pixellab.ai/account) after signing in and copy the value labeled `Secret`. PixelLab may call this value an API key, API token, secret, or token. Pip calls it a bearer token for MCP and REST v2 auth. Store the token outside chat. The recommended local secret name for Pip REST v2 fallback is:

```text
PIXELLAB_SECRET
```

Never paste the Secret into chat, commit it, print it in logs, copy browser session tokens, or ask an agent to scan `.env*`, shell history, home directories, or environment dumps. For deeper setup, auth, and service-boundary details, see [More Documentation ↗](docs/README.md) and [PixelLab Auth And Security ↗](docs/pixellab/pixellab-auth-and-security.md).

## Security

**PixelLab Pip is safe to install — and checked by outside services, not just by us.** It is plain-Markdown instructions plus two tiny local Python helpers (a completion sound and a background-removal check): no compiled binaries, no hidden network calls, and it never reads or prints your PixelLab token. Every release is independently scanned and cryptographically signed. See any of it for yourself:

- **Skill audit** — [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) (the same engine ClawHub's registry uses) scans the skill on every push and weekly. Results are public on the [Code Scanning tab](https://github.com/Shilo/pixellab-pip/security/code-scanning), and a release is blocked if it goes over the risk threshold.
- **Independent registry audit** — every release auto-publishes to [ClawHub](https://clawhub.ai/shilo/skills/pixellab-pip), whose own third-party audit (SkillSpector + VirusTotal + ClawScan) posts a public verdict: **[view the ClawHub security audit ↗](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit)**.
- **Malware scan** — each release links a public [VirusTotal](https://www.virustotal.com/) report of the exact download in its [release notes](https://github.com/Shilo/pixellab-pip/releases/latest).
- **Tamper-proof build** — every release zip comes with a cryptographic proof-of-origin (a Sigstore *build-provenance attestation*): confirmation that GitHub built this exact file from the public repo and no one altered it afterward. Anyone can check a downloaded zip:

  ```bash
  gh attestation verify pixellab-pip-<version>.zip --repo Shilo/pixellab-pip
  ```

- **Report a concern** — see [SECURITY.md](SECURITY.md); private vulnerability reporting is enabled on this repo.

What the skill uses: your PixelLab token — only as an auth header for PixelLab requests. Your MCP client passes it (or REST fallback references `PIXELLAB_SECRET` by name); Pip is designed never to read the token's value into the conversation, print it, log it, or store it. The skill also uses the `python` command for two small bundled helpers (completion sound and a background-removal check, which make no network calls of their own) and writes only to your project's `pixellab-pip-generations/` output folder and the skill's own config file. It never scans your other secrets, `.env` files, shell history, or browser sessions — and it works for guidance, setup, and routing with no token at all.

Expected scan disclosures: Pip legitimately documents PixelLab bearer-token handling, official `api.pixellab.ai` documentation URLs, and a local sound-playback helper, so instruction scanners report those as informational findings — that is the disclosed design, reviewable line-by-line on the Code Scanning tab. No scanner can prove an instruction file safe; these are layered, independently verifiable checks, not a guarantee.

## Benchmark

Reproducible measurement of what the skill costs an agent and how well it routes, versus the alternatives. Produced by [`dev-tools/skill_benchmark.py`](dev-tools/skill_benchmark.py) — it measures the agent session (context tokens, output, cost, routing correctness), never PixelLab credits.

| Method | Benchmark routing checks passed | Context injected up front |
|---|---|---|
| **PixelLab Pip skill** | **~100%** | ~7.2k tokens (+ references on demand) |
| Official `mcp/docs` injected | ~54% | ~7.7k tokens (all, always) |
| No skill (agent knowledge only) | ~51% | 0 |

Across 13 routing scenarios — several drawn from the [showcase](docs/showcase/README.md) — the skill routed every check correctly, versus roughly half for injecting PixelLab's official docs or using no skill: the docs alone miss REST-only routes, local post-processing, and cost/ordering detail. The skill injects about the same up-front context as those docs (~7.2k vs ~7.7k) and reads a reference only when a task needs it. Routing is scored by deterministic checks, not a model; these are a dated `claude` snapshot (nondeterministic). See the full tables, per-scenario results, and reproduce steps in the **[full benchmark report ↗](docs/pixellab-pip-benchmark.md)**.
