<p align="center">
  <a href="docs/showcase/pip-mascot.md"><img src="docs/showcase/pip/pip.gif" alt="Pip mascot idle animation" width="68"></a>
</p>

# PixelLab Pip

[![Skill Security Audit](https://github.com/Shilo/pixellab-pip/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Shilo/pixellab-pip/security/code-scanning)
[![ClawHub security audit](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fpixellab-pip%2Fversions%2F1.0.0&query=%24.version.security.status&label=ClawHub%20Audit&color=2b7fff&cacheSeconds=3600)](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit)
[![VirusTotal](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fpixellab-pip%2Fversions%2F1.0.0&query=%24.version.security.scanners.vt.normalizedStatus&label=VirusTotal&color=2ea44f&logo=virustotal&logoColor=white&cacheSeconds=3600)](https://www.virustotal.com/gui/file-analysis/NTlkNDdhNmE4MzdlMmRiNzRjNTc3NmM5MTM5YTExNjA6MTc4NDc5NjAzNA==/detection)
[![Build Provenance attested](https://img.shields.io/badge/Build_Provenance-attested-2ea44f)](https://github.com/Shilo/pixellab-pip/attestations/36720233)

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
| Easy PixelLab workflow | Ask in plain language — no tool names, settings, or modes to learn — and Pip works out which PixelLab tool fits each kind of asset (characters, animations, sprites, top-down and platformer tilesets, isometric tiles, map objects, icons, UI, backgrounds, portraits, fonts, effects), and whether to use PixelLab's MCP tools, its API, the website editor, or Aseprite. When PixelLab has no supported way to do something, Pip says so instead of inventing one. |
| Guided PixelLab setup | Pip connects PixelLab to your agent, works out what is missing when generation fails, and changes only what you approve — without ever reading or printing your secret. |
| Cost and credit control | By default Pip asks before spending anything: right before the first paid call it shows every PixelLab call it plans to make, the exact wording it will send, and a rough total cost — all in one message, so you approve, tweak, or cancel the whole job at once instead of waiting between steps. Let Pip run autonomously with `/pixellab-pip auto` (or just reply `auto`) to skip that check, and switch the check back on the same way. Say cheap or set a budget and Pip also picks the cheapest option that fits, names the tradeoff, does not quietly upgrade you to a pricier `Pro` one, and re-checks a stuck job instead of paying for it twice. |
| Asset integrity | Pip only delivers art that came from PixelLab or from you. It may crop, mask, assemble, package, and convert those pixels, and says when it did; it will not resize, combine, or patch a result and call it final without your approval, and anything it draws itself is labeled as not from PixelLab. Pip checks results against what you asked for, and reports a failure rather than papering over it. |
| Protects your remote assets | Pip never deletes, clears, or overwrites your characters, animations, tilesets, or other remote PixelLab assets without your permission — never as a guess, a cleanup, or a fix for something that merely looks missing. Pip may still think a destructive change is a good idea and suggest one, but it always asks first, shows exactly what would go, and waits for your approval. When a list comes back empty or out of sync, Pip investigates read-only and tells you what it found instead of destroying anything. |
| Local output folder | Pip saves downloads, previews, blueprints, packages, and a record of each job in a `pixellab-pip-generations/` folder in your project, unless you name another location. When a job comes back as separate frames, Pip also builds a single spritesheet. |
| Generation reports | Pip reports every generation: which PixelLab tool ran, the exact wording sent, the settings that mattered, where the files went, what it cost, and whether it passed the checks. When your request runs as several separate generations (a cinematic's shots, each direction of an animation, or a batch you approved), Pip shows each finished image as it lands instead of waiting until the end. It saves a record beside the files with the job IDs and seed. |
| Preset and custom animation | Describe an action and Pip sends it to PixelLab's text animation, its recommended default. Name a stock motion (walk, run, idle, jump, and more — for humanoids, dogs, cats, horses, bears, and lions) and Pip picks the matching PixelLab preset. Pip can also rig a sprite from its skeleton when you want control over the joints. It previews one direction before animating the rest, and keeps frames in the order PixelLab returned them. |
| Multi-shot cinematics and seamless loops | PixelLab animates one short clip at a time. For a longer or seamlessly looping scene, Pip decides between one looped clip and a chain of shots, plans the beats, checks each one, and stops dead at the budget it asks for up front — starting from a frame you supply or from scratch. |
| Attached images | Pip works out what each attached file is for — the image to edit, a character to match, a style to copy, a color palette, a mask, or the first frame of an animation — and asks first when guessing wrong would cost you credits. |
| Pick from generated variations | Some PixelLab tools return several versions of one asset. Pip lists them as a numbered menu and waits for your pick before saving or continuing, unless you tell it to choose. |
| Prompt preparation | Pip turns rough wording, your images, styles, palettes, and constraints into a clear PixelLab-ready description, using PixelLab's own prompt enhancer when the tool has one. It shows anything it adds before you pay, and sends wording you give exactly as-is. You can opt out any time. |
| Reusable Blueprints | Pip saves a workflow as a small, shareable blueprint holding the exact PixelLab requests plus the steps around them. It can recreate one anytime with plain-language changes, or run the bundled blueprints by name — a replay repeats the workflow and inputs, not the exact pixels, and spends credits again. Full guide: [docs/blueprint.md](docs/blueprint.md). |
| Aseprite handoff | Ask for an Aseprite workflow and Pip moves generated assets in through Aseprite's own command line rather than the PixelLab extension: `.aseprite` copies that leave your original untouched, imports and exports that keep frame order, and palette clamps (1-bit, Game Boy green, a palette Aseprite has installed, or your own hex colors) checked against the colors you asked for. |
| Fallback background removal | When you ask for a transparent asset and it comes back with a background, Pip checks whether it can be cleaned up locally without touching the art, and hands it to PixelLab's own background removal when unsure. |
| Paperdoll and layered characters | Pip fits hair, armor, hats, weapons, and accessories to an existing character, delivering the base, one transparent PNG per layer, and the finished composite, or Aseprite layers. It checks each layer holds only the new part, without pretending PixelLab returns layers where it does not. |
| Answer PixelLab questions | Pip explains setup, sign-in, docs, code libraries, troubleshooting, and confusing labels such as `Pro`, `v3`, `new`, `create tiles` vs `create tileset`, `Pixen`, `PixFlux`, `BitForge`, and `PixPatch`. It re-checks official docs when a needed fact is missing or unclear, and flags anything it cannot verify. |
| Any language | Talk to Pip in any language and it replies in yours. PixelLab only understands English, so Pip translates your request to English before sending it — and shows you both the English and your own wording so you can check it. |
| Token and secret handling | Pip sets up your PixelLab token without exposing its value, dumping environment variables, or scanning `.env*` files, shell history, or keychains. It never uses copied website session tokens, or the private endpoints PixelLab's own website and Aseprite extension use behind the scenes. |
| Bark completion sound | Pip plays a sound when a PixelLab generation, edit, or animation job succeeds. On by default, with an on/off toggle. |
| Agent-agnostic | Pip works from any agent that supports Agent Skills. |

## Install

### Agent-Assisted Install (Recommended)

Easiest for most people — your agent picks the right marketplace, plugin, extension, or skill method for its own platform. Ask your local coding agent:

```text
Install the PixelLab Pip plugin / extension / Agent Skill from
https://github.com/Shilo/pixellab-pip. First read the install steps at
https://github.com/Shilo/pixellab-pip#install, then install it with whatever
method fits you — marketplace, plugin, or extension if you support one,
otherwise copy the whole skill folder (every file inside `skills/pixellab-pip/`,
not just `SKILL.md`) into my skills directory as shown in the Manual Skill
Install steps — preferring marketplace install/update over copying files. If a
pre-v1.0 version is already installed under a `pixellab-pip` marketplace, remove
it first, then install fresh. Then run the PixelLab Pip setup command (for
example `/pixellab-pip setup`), and tell me about any blockers, whether I need
to restart or reload first, and when it is ready to use.
```

### Upgrading from a pre-v1.0 install

Pre-v1.0 used the `pixellab-pip` marketplace; v1.0 uses `pixellab-pip-plugins`. Do a one-time clean reinstall (a normal update won't switch marketplaces). Easiest: re-run the [Agent-Assisted Install](#agent-assisted-install-recommended) above. Or manually — remove the old, install the new:

```text
# Claude Code
/plugin uninstall pixellab-pip@pixellab-pip
/plugin marketplace remove pixellab-pip
/plugin marketplace add Shilo/pixellab-pip
/plugin install pixellab-pip@pixellab-pip-plugins

# Codex
codex plugin remove pixellab-pip@pixellab-pip
codex plugin marketplace remove pixellab-pip
codex plugin marketplace add Shilo/pixellab-pip
codex plugin add pixellab-pip@pixellab-pip-plugins
```

Other marketplace agents follow the same pattern; skill-copy installs are unaffected.

### Marketplace Install

Install PixelLab Pip as a plugin or extension when your agent supports marketplaces. Use manual skill install only when your agent does not support plugin installation.

#### Claude Code

Install:

```text
/plugin marketplace add Shilo/pixellab-pip
/plugin install pixellab-pip@pixellab-pip-plugins
/pixellab-pip setup
```

Update:

```text
/plugin marketplace update pixellab-pip-plugins
/plugin update pixellab-pip@pixellab-pip-plugins
```

#### Codex

Install:

```text
codex plugin marketplace add Shilo/pixellab-pip
codex plugin add pixellab-pip@pixellab-pip-plugins
@pixellab-pip setup
```

Update:

```text
codex plugin marketplace upgrade pixellab-pip-plugins
codex plugin remove pixellab-pip@pixellab-pip-plugins
codex plugin add pixellab-pip@pixellab-pip-plugins
```

#### Cursor

Use Cursor's plugin marketplace or team marketplace flow when available, or install the raw skill manually.

```text
/pixellab-pip setup
```

#### Antigravity

Antigravity supports two installation shapes:

1. **Custom plugin — Antigravity IDE / 2.0.** When the product supports custom plugins, copy or extract the whole repository so its root `plugin.json` lands at either path below. No Git installation is required. Keep `plugin.json` and `skills/` together; the manifest marks the plugin and `skills/pixellab-pip/` contains the complete skill.

```text
Global:    ~/.gemini/config/plugins/pixellab-pip/plugin.json
Workspace: <workspace-root>/.agents/plugins/pixellab-pip/plugin.json
```

2. **Native Agent Skill — fallback or Antigravity CLI.** Copy the entire `skills/pixellab-pip/` directory, including all references, helpers, assets, blueprints, and config files, so its top-level `SKILL.md` lands at the matching path:

```text
Antigravity IDE / 2.0 workspace: <workspace-root>/.agents/skills/pixellab-pip/SKILL.md
Antigravity IDE / 2.0 global:    ~/.gemini/antigravity/skills/pixellab-pip/SKILL.md
Antigravity CLI workspace:       <workspace-root>/.agents/skills/pixellab-pip/SKILL.md
Antigravity CLI global:          ~/.gemini/antigravity-cli/skills/pixellab-pip/SKILL.md
```

The plugin form is a packaging convenience, not a requirement for Pip's behavior. Antigravity does not document a third-party marketplace manifest, so do not use the repository's `.agents/plugins/marketplace.json`; that file belongs to the separate VS Code Agent Plugins format. Also do not install the repository root as an Antigravity CLI plugin because its strict manifest schema is incompatible with the shared root manifest. Restart or reload Antigravity after either supported install, then ask it to use `pixellab-pip` for setup. In Antigravity CLI, `/pixellab-pip setup` invokes the installed skill. The setup wizard supports Antigravity's MCP UI, global and workspace `mcp_config.json`, required remote `serverUrl` schema, and separate REST v2 fallback readiness.

Pip intentionally does not bundle an Antigravity `mcp_config.json`: PixelLab MCP requires a private bearer token, and Antigravity does not document environment-variable expansion in custom HTTP headers. `/pixellab-pip setup` gives a token-free MCP preview and guides the user through credential completion after approval, then separately checks `PIXELLAB_SECRET` for REST v2 fallback.

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
copilot plugin install pixellab-pip@pixellab-pip-plugins
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

#### Auto

```text
/pixellab-pip auto
@pixellab-pip auto
$pixellab-pip auto
/pixellab-pip auto on
/pixellab-pip auto off
```

Toggles whether Pip asks before spending credits. Auto is **off** by default: right before the first paid PixelLab call of a job, Pip shows every call it plans to make, the exact wording it will send, and a rough total cost, then asks once — approve, change anything, or decline. Reply `auto` to that prompt (or run the command) to turn Auto on and continue without stopping. With Auto on, Pip skips the check and instead shows a one-line reminder of how to turn it back off. The check is a single up-front gate, not a prompt between each step. Auto never overrides an explicit "ask me first" instruction or Pip's confirmation before deleting or overwriting remote assets. The setting persists in `skills/pixellab-pip/pixellab-pip.json` next to `SKILL.md` (the same file bark uses), with an exact user-config fallback if that directory is read-only.

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

#### Update

```text
/pixellab-pip update
@pixellab-pip update
$pixellab-pip update
```

Updates PixelLab Pip to the latest version using however your agent installed it — a marketplace, plugin, or extension update, or re-copying the latest skill folder. Manual alternative: run your agent's own update command (the per-agent **Update** blocks under [Install](#install)), or just ask your agent to update PixelLab Pip.

#### Uninstall

```text
/pixellab-pip uninstall
@pixellab-pip uninstall
$pixellab-pip uninstall
```

Removes PixelLab Pip — Pip confirms first and shows exactly what it will remove, and keeps your PixelLab Secret and `pixellab-pip-generations/` outputs unless you ask otherwise. Manual alternative: use your agent's plugin or extension uninstall command, or delete the copied `pixellab-pip` skill folder — or just ask your agent to uninstall PixelLab Pip.

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
