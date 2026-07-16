<p align="center">
  <a href="docs/showcase/pip-mascot.md"><img src="docs/showcase/pip/pip.gif" alt="Pip mascot idle animation" width="68"></a>
</p>

# PixelLab Pip

[![Skill Security Audit](https://github.com/Shilo/pixellab-pip/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Shilo/pixellab-pip/security/code-scanning)
[![ClawHub security audit](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fpixellab-pip%2Fversions%2F0.7.0&query=%24.version.security.status&label=ClawHub%20Audit&color=2b7fff&cacheSeconds=3600)](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit)
[![VirusTotal](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fpixellab-pip%2Fversions%2F0.7.0&query=%24.version.security.scanners.vt.normalizedStatus&label=VirusTotal&color=2ea44f&logo=virustotal&logoColor=white&cacheSeconds=3600)](https://www.virustotal.com/gui/file-analysis/YzliZmI5ZDhiYjcyMTA1ODJmMTlkMDlkZmJjNTAyZmY6MTc4Mzk5MjE0MA==/detection)
[![Build Provenance attested](https://img.shields.io/badge/Build_Provenance-attested-2ea44f)](https://github.com/Shilo/pixellab-pip/attestations/35177857)

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

| Feature | What it does |
|---|---|
| All PixelLab asset types | Characters, sprites, item and skill icons, top-down and platformer tilesets, isometric tiles, bitmap fonts, portraits, UI, backgrounds, map objects, effects, and animations. |
| Easy PixelLab workflow | Ask for assets in plain language without knowing PixelLab tool names, endpoint names, modes, or editor differences. Pip picks the surface — MCP tools, REST v2, the website editor, or Aseprite — and reports which it used. |
| Guided PixelLab setup | Set up MCP/API access, diagnose missing auth, and configure only what you approve without reading or printing the secret value. |
| Cost and credit control | Say cheap or set a budget and Pip prefers the lowest-cost route that fits, names the tradeoff, and does not silently upgrade to Pro. It lists planned items with cost category before a batch, asks before each extra paid attempt, and re-checks a stalled job instead of resubmitting a paid one. |
| Asset integrity | Every pixel of requested art comes from PixelLab or from you — nothing drawn, repainted, or patched locally and passed off as generated. Outputs are checked against your stated constraints, and a failure is reported rather than salvaged. |
| Local output folder | Downloads, previews, manifests, and packages are saved under a project `pixellab-pip-generations/` folder. When a job returns separate frames, Pip also compiles a single spritesheet. |
| Clear generation reports | Report the PixelLab tool or endpoint used, the exact wording sent, the settings that mattered, IDs, output locations, async status, cost, and verification status, plus a manifest saved beside the outputs. |
| Preset and custom animation | Named template motions (walk, run, idle, jump, and more, per body type — humanoid, dog, cat, horse, bear, lion), custom described actions, auto-rigging from an estimated skeleton, or a start-to-end tween. One direction is previewed before animating all eight. |
| Multi-shot cinematics and seamless loops | Describe a scene, a length, and a budget, and get a multi-second or seamlessly looping animation — built as one seamless loop or shot by shot, from a supplied frame or from scratch. Pip decides the approach, plans the beats, validates every step, and stops at the budget you set. |
| Use images and attachments correctly | Identify each supplied file's role — edit target, identity reference, style reference, concept image, mask, palette, init/source image, or animation frame — instead of guessing one generic role, and ask when a wrong guess would cost credits. |
| Pick from generated variations | Some PixelLab routes return several versions of one asset. Pip lists them as a numbered menu and waits for your pick before saving, editing, or continuing from one, unless you delegate the choice. |
| Auto-enhance prompts and descriptions | Turn rough wording, visible inputs, styles, palettes, and constraints into concise PixelLab-ready descriptions by default, with opt-out support. Material additions are shown before a paid call; exact field values you supply are sent unchanged. |
| Reusable Blueprints | Save a PixelLab workflow as a small, shareable blueprint with exact MCP/REST requests plus flexible agent tasks for preparation, selection, assembly, and verification. Recreate it anytime with plain-language overrides, or run bundled blueprints by name. Full guide: [docs/blueprint.md](docs/blueprint.md). |
| Local Aseprite CLI workspaces | Move generated assets into Aseprite without driving the PixelLab extension UI: create or update `.aseprite` copies, import frames as layers/tags, export PNG sequences, GIFs, sprite sheets, and metadata, or locally clamp/reduce colors to palettes such as 1-bit black/white, Game Boy green, any palette Aseprite has installed, or supplied hex colors through documented Aseprite CLI/Lua. |
| Fallback background removal | When a requested transparent asset still comes back with a background, verify a safe local cleanup first and fall back to PixelLab background removal when uncertain. |
| Paperdoll and layered workflow guidance | Fitted hair, armor, hats, weapons, and accessories on an existing character, delivered as the base, one transparent PNG per layer, and the composite, or as Aseprite layers. Each layer is verified to hold only the addition, without pretending PixelLab returns layers where it does not. |
| Answer PixelLab questions | Explain setup, auth, docs, SDKs, troubleshooting, and confusing labels such as `Pro`, `v3`, `new`, `create tiles`, `create tileset`, Pixen, PixFlux, BitForge, and PixPatch at the documented product level. Official docs, schemas, pricing, and limits are refreshed before exact claims, and anything unverifiable is flagged. |
| Non-English request support | Translate or normalize PixelLab-facing natural-language inputs to concise English while keeping confirmations, explanations, and reports in your language. |
| Safer auth and privacy | Bearer-token and MCP secret setup without exposing token values, dumping environment variables, or inspecting private `.env*` files. No copied website session tokens, and no undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension. |
| Bark completion sound | Play a generic success sound after PixelLab generation-style jobs finish. On by default, with an on/off toggle. |
| Agent-agnostic | Work from any agent that supports Agent Skills. |

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

#### Cursor

Use Cursor's plugin marketplace or team marketplace flow when available, or install the raw skill manually.

```text
/pixellab-pip setup
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

#### VS Code Agent Plugins

Use **Chat: Install Plugin From Source** with this repo URL or VS Code's plugin marketplace flow.

```text
/pixellab-pip setup
```

#### OpenCode

OpenCode discovers Agent Skills natively — there is no marketplace step (its `opencode plugin` command installs JavaScript code plugins, not skills). Install the skill (see [Manual Skill Install](#manual-skill-install)) into any path OpenCode reads: `.opencode/skills/`, `.agents/skills/`, or `.claude/skills/` (project, or their `~/.config/opencode`, `~/.agents`, `~/.claude` globals). OpenCode loads it on demand through its built-in `skill` tool.

```text
.opencode/skills/pixellab-pip/SKILL.md
```

Then ask OpenCode to set up PixelLab Pip.

#### Deep Code (DeepSeek V4)

Deep Code — the DeepSeek V4 terminal agent — discovers Agent Skills natively; there is no marketplace. Install the CLI, then drop the skill into a path it reads — `~/.agents/skills/` for every project, or `.agents/skills/` or `.deepcode/skills/` inside one project:

```text
npm install -g @vegamo/deepcode-cli
```

```text
.agents/skills/pixellab-pip/SKILL.md
```

Open Deep Code's skill picker with `/` or type the skill name, then run PixelLab Pip setup.

### Manual Skill Install

Manual install is useful for project-local setup or agent apps that support raw Agent Skills without plugin installation. Copy the contents of `skills/pixellab-pip/` into a folder named `pixellab-pip` inside your agent's skills directory, so `SKILL.md` is directly inside the final folder.

You can also download the skill zip from the [latest release](https://github.com/Shilo/pixellab-pip/releases/latest) and extract it into your agent's skills directory.

```text
.agents/skills/pixellab-pip/SKILL.md
.claude/skills/pixellab-pip/SKILL.md
.cursor/skills/pixellab-pip/SKILL.md
.opencode/skills/pixellab-pip/SKILL.md
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

Expected scan disclosures: Pip legitimately documents PixelLab bearer-token handling, official `api.pixellab.ai` documentation URLs, and a local sound-playback helper, so instruction scanners flag those as by-design findings. Each is dismissed on the [Code Scanning tab](https://github.com/Shilo/pixellab-pip/security/code-scanning?query=is%3Aclosed) with a public, per-finding rationale you can read. No scanner can prove an instruction file safe; these are layered, independently verifiable checks, not a guarantee.

## Benchmark

Reproducible measurement of what the skill costs an agent and how well it routes, versus the alternatives. Produced by [`dev-tools/skill_benchmark.py`](dev-tools/skill_benchmark.py) — it measures the agent session (context tokens, output, cost, routing correctness), never PixelLab credits.

| Method | Routes to the exact PixelLab tool | Context tokens per session |
|---|---|---|
| **PixelLab Pip skill** | **~98%** | ~7.5k base + discoverable references = ~9.1k tokens average |
| Official `mcp/docs` injected | ~58% | ~7.7k tokens (the full doc, every session) |
| No skill (agent knowledge only) | ~24% | 0 tokens |

Across 20 scenarios phrased as **plain human requests** (`claude` + `codex` + `deepseek-v4-pro`, 1 rep) — no tool names or "which endpoint" hints, so the only difference between arms is what that user would actually have: the skill, the docs link's content, or nothing — each agent *plans* the route and is scored only when it identifies the correct PixelLab route (no partial credit for a plausible-sounding plan that names the wrong tool; the table averages per-scenario check rates across the three agents). The skill routed **every** scenario correctly across all three agents (the only dropped sub-check is the exact credit *figure* on one cost question); the official docs got ~58% — strong on pure MCP tool-selection but **0** on every REST-only route (backgrounds, image-pro sheets, the skeleton flow) and near-0 on setup, with mixed credit on blueprint replay; no skill was mostly lost. The skill starts slightly leaner than the docs up front (~7.5k vs ~7.7k) but reads a reference when a task calls for one (11 of these 20 scenarios), averaging ~9.1k per session — the routing accuracy costs more context than the docs on reference-needing tasks. The benchmark is **dry — it spends no PixelLab credits**. A dated, nondeterministic snapshot; see the full per-scenario tables and reproduce steps in the **[full benchmark report ↗](docs/pixellab-pip-benchmark.md)**.
