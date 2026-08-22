<p align="center">
  <a href="docs/showcase/pip-mascot.md"><img src="docs/showcase/pip/pip.gif" alt="Pip mascot idle animation" width="68"></a>
</p>

# PixelLab Pip

[![Skill Security Audit](https://github.com/Shilo/pixellab-pip/actions/workflows/security-scan.yml/badge.svg)](https://github.com/Shilo/pixellab-pip/security/code-scanning)
[![ClawHub security audit](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fpixellab-pip%2Fversions%2F1.5.0&query=%24.version.security.status&label=ClawHub%20Audit&color=2b7fff&cacheSeconds=3600)](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit)
[![VirusTotal](https://img.shields.io/static/v1?label=VirusTotal&message=0%20malicious%20%7C%200%20suspicious&color=2ea44f&logo=virustotal&logoColor=white)](https://www.virustotal.com/gui/file/bafea5a7f835fad126613fbf75a6a1778206787cdbbab6035987011e3ee01ef6/detection)
[![Build Provenance attested](https://img.shields.io/badge/Build_Provenance-attested-2ea44f)](https://github.com/Shilo/pixellab-pip/attestations/42269199)

Meet PixelLab Pip: a tiny pup who fetches the right PixelLab workflow. He follows human commands to create, edit, and animate pixel assets, then sniffs out a bigger prompt, scouts for a useful tool, and carries back what happened.

An unofficial Agent Skill for [PixelLab ↗](https://www.pixellab.ai/) that turns plain-language requests into the right documented tool or practical workflow. You do not need to know PixelLab's tool names, endpoint names, or model labels.

## Table Of Contents

- [Showcase](#showcase)
- [Features](#features)
  - [Create Pixel Art You Want](#create-pixel-art-you-want)
  - [Protect Your Art And Credits](#protect-your-art-and-credits)
  - [Bring Characters To Life](#bring-characters-to-life)
  - [Save, Clean Up, And Reuse Your Art](#save-clean-up-and-reuse-your-art)
  - [Get Help In Any Language And Agent](#get-help-in-any-language-and-agent)
- [Install](#install)
- [Usage](#usage)
- [Benchmark](#benchmark)
- [Security](#security)
- [More Documentation](#more-documentation)

## Showcase

See the [Showcase ↗](docs/showcase/README.md) for real prompts and results.

<p align="center">
  <a href="docs/showcase/README.md"><img src="docs/showcase/visual-effects/fantasy-aura-effects.gif" alt="Sixteen animated fantasy aura effects created through Pip workflows" width="256"></a>
</p>

## Features

Use me when you need to create, edit, animate, integrate, or troubleshoot PixelLab assets and workflows.

### Create Pixel Art You Want

| Feature | What it does |
|---|---|
| Easy PixelLab workflow | Ask in plain language — no tool names, settings, or modes to learn — and Pip works out which PixelLab tool fits each kind of asset (characters, animations, sprites, top-down and platformer tilesets, isometric tiles, map objects, icons, UI, backgrounds, portraits, fonts, effects), and whether to use PixelLab's MCP tools, its API, the website editor, or Aseprite. When PixelLab has no supported way to do something, Pip says so instead of inventing one. |
| Attached images | Pip works out what each attached file is for — the image to edit, a character to match, a style to copy, a color palette, a mask, or the first frame of an animation — and asks first when guessing wrong would cost you credits. |
| Pick from generated variations | Some PixelLab tools return several versions of one asset. Pip lists them as a numbered menu and waits for your pick before saving or continuing, unless you tell it to choose. |
| Prompt preparation | Pip turns rough wording, your images, styles, palettes, and constraints into a clear PixelLab-ready description, using PixelLab's own prompt enhancer when the tool has one. It shows anything it adds before you pay, and sends wording you give exactly as-is. You can opt out any time. |

### Protect Your Art And Credits

| Feature | What it does |
|---|---|
| Guided PixelLab setup | Pip connects PixelLab to your agent, works out what is missing when generation fails, and changes only what you approve — without ever reading or printing your secret. |
| Cost and credit control | By default Pip asks before spending anything: right before the first paid call it shows every PixelLab call it plans to make, the exact wording it will send, and a rough total cost — all in one message, so you approve, tweak, or cancel the whole job at once instead of waiting between steps. Let Pip run autonomously with `/pixellab-pip auto` (or just reply `auto`) to skip that check, and switch the check back on the same way. Say cheap or set a budget and Pip also picks the cheapest option that fits, names the tradeoff, does not quietly upgrade you to a pricier `Pro` one, and re-checks a stuck job instead of paying for it twice. |
| Asset integrity | Pip only delivers art that came from PixelLab or from you. It may crop, mask, assemble, package, and convert those pixels, and says when it did; it will not resize, combine, or patch a result and call it final without your approval, and anything it draws itself is labeled as not from PixelLab. Pip checks results against what you asked for, and reports a failure rather than papering over it. |
| Protects your remote assets | Pip never deletes, clears, or overwrites your characters, animations, tilesets, or other remote PixelLab assets without your permission — never as a guess, a cleanup, or a fix for something that merely looks missing. Pip may still think a destructive change is a good idea and suggest one, but it always asks first, shows exactly what would go, and waits for your approval. When a list comes back empty or out of sync, Pip investigates read-only and tells you what it found instead of destroying anything. |
| Generation reports | Pip reports every generation: which PixelLab tool ran, the exact wording sent, the settings that mattered, where the files went, what it cost, and whether it passed the checks. When your request runs as several separate generations (a cinematic's shots, each direction of an animation, or a batch you approved), Pip shows each finished image as it lands instead of waiting until the end. It saves a record beside the files with the job IDs and seed. |
| Token and secret handling | Pip sets up your PixelLab token without exposing its value, dumping environment variables, or scanning `.env*` files, shell history, or keychains. It never uses copied website session tokens, or the private endpoints PixelLab's own website and Aseprite extension use behind the scenes. |

### Bring Characters To Life

| Feature | What it does |
|---|---|
| Preset and custom animation | Describe an action and Pip sends it to PixelLab's text animation, its recommended default. Name a stock motion (walk, run, idle, jump, and more — for humanoids, dogs, cats, horses, bears, and lions) and Pip picks the matching PixelLab preset. Pip can also rig a sprite from its skeleton when you want control over the joints. It previews one direction before animating the rest, and keeps frames in the order PixelLab returned them. |
| Talking portraits and lip sync | Pip can attach a portrait to a character, generate mood-specific mouth shapes, render a talking GIF from dialogue, or return a frame-by-frame lip-sync plan for a game. |
| Multi-shot cinematics and seamless loops | PixelLab animates one short clip at a time. For a longer or seamlessly looping scene, Pip decides between one looped clip and a chain of shots, plans the beats, checks each one, and stops dead at the budget it asks for up front — starting from a frame you supply or from scratch. |
| Paperdoll and layered characters | Pip fits hair, armor, hats, weapons, and accessories to an existing character, delivering the base, one transparent PNG per layer, and the finished composite, or Aseprite layers. It checks each layer holds only the new part, without pretending PixelLab returns layers where it does not. |

### Save, Clean Up, And Reuse Your Art

| Feature | What it does |
|---|---|
| Local output folder | Pip saves downloads, previews, blueprints, packages, and a record of each job in a `pixellab-pip-generations/` folder in your project, unless you name another location. When a job comes back as separate frames, Pip also builds a single spritesheet. |
| Reusable Blueprints | Pip saves a workflow as a small, shareable blueprint holding the exact PixelLab requests plus the steps around them. It can recreate one anytime with plain-language changes, or run the bundled blueprints by name — a replay repeats the workflow and inputs, not the exact pixels, and spends credits again. Full guide: [docs/blueprint.md ↗](docs/blueprint.md). |
| Aseprite handoff | Ask for an Aseprite workflow and Pip moves generated assets in through Aseprite's own command line rather than the PixelLab extension: `.aseprite` copies that leave your original untouched, imports and exports that keep frame order, and palette clamps (1-bit, Game Boy green, a palette Aseprite has installed, or your own hex colors) checked against the colors you asked for. |
| Fallback background removal | When you ask for a transparent asset and it comes back with a background, Pip checks whether it can be cleaned up locally without touching the art, and hands it to PixelLab's own background removal when unsure. |

### Get Help In Any Language And Agent

| Feature | What it does |
|---|---|
| Answer PixelLab questions | Pip explains setup, sign-in, docs, code libraries, troubleshooting, and confusing labels such as `Pro`, `v3`, `new`, `create tiles` vs `create tileset`, `Pixen`, `PixFlux`, `BitForge`, and `PixPatch`. It re-checks official docs when a needed fact is missing or unclear, and flags anything it cannot verify. |
| Any language | Talk to Pip in any language and it replies in yours. Pip translates visual prompts to English and shows you both the English and your own wording so you can check it. Pip keeps spoken dialogue exactly as written when it uses the supported Latin alphabet; for other scripts, it asks before transliterating. |
| Bark completion sound | Pip plays a sound when a PixelLab generation, edit, or animation job succeeds. On by default, with an on/off toggle. |
| Agent-agnostic | Pip works from any agent that supports Agent Skills. |

## Install

### Agent-Assisted Install (Recommended)

Easiest for most people — your agent picks the right marketplace, plugin, extension, or skill method for its own platform. Ask your local coding agent:

```text
Install the PixelLab Pip plugin / extension / Agent Skill from
https://github.com/Shilo/pixellab-pip. First read the install steps at
https://github.com/Shilo/pixellab-pip/blob/main/docs/install.md. If a pre-v1.0
version is already installed under a `pixellab-pip` marketplace, remove it first.
Then install it using whichever method your platform supports, preferring a marketplace,
plugin, or extension over copying files, and non-interactive CLI commands over
interactive ones you cannot type yourself. If you do copy the skill, copy the
whole `skills/pixellab-pip/` folder, not just `SKILL.md`, into my skills
directory as shown in the Manual Skill Install steps. Finally, run
the PixelLab Pip setup command (for example `/pixellab-pip setup`), and tell me
about any blockers, whether I need to restart or reload first, and when it is
ready to use.
```

On [Claude Code on the web ↗](docs/install.md#claude-code-on-the-web)? Cloud sessions have no plugin manager, so use the cloud prompt there instead.

Upgrading from a pre-v1.0 marketplace install? A normal update does not switch marketplaces; re-run the prompt above or follow the [one-time clean reinstall ↗](docs/install.md#upgrade-from-pre-v10).

### Direct Install

<details>
<summary><strong>Claude Code</strong></summary>

From inside Claude Code:

```text
/plugin marketplace add Shilo/pixellab-pip
/plugin install pixellab-pip@pixellab-pip-plugins
```

Reload Claude Code, then run `/pixellab-pip setup`.

Claude Code on the web needs a repository or account install instead. Follow the [cloud installation guide ↗](docs/install.md#claude-code-on-the-web).

</details>

<details>
<summary><strong>Codex</strong></summary>

From a terminal:

```text
codex plugin marketplace add Shilo/pixellab-pip
codex plugin add pixellab-pip@pixellab-pip-plugins
```

Reload Codex, then run `@pixellab-pip setup`.

</details>

<details>
<summary><strong>Other agents or a raw Agent Skill</strong></summary>

Use the cross-agent installer and select your agent:

```text
npx skills add Shilo/pixellab-pip --skill pixellab-pip
```

Then run PixelLab Pip setup using the prefix your agent supports.

You can also install the skill manually when your agent does not support the cross-agent installer.

</details>

For every supported platform, updates, migration, and safe manual copying, read the [full installation guide ↗](docs/install.md).

## Usage

Invoke Pip with the form your agent supports:

```text
/pixellab-pip make a cute knight character sprite
@pixellab-pip animate this idle character
$pixellab-pip create a mossy top-down tileset
pip edit this image into cleaner 32px pixel art
```

Explicit invocation is the most reliable. Plain `pip` can also work when your agent supports automatic skill discovery.

Common commands:

| Command | Purpose |
|---|---|
| `pixellab-pip setup` | Connect PixelLab MCP and/or documented REST v2 fallback. |
| `pixellab-pip auto` | Toggle Auto mode, which skips the before-you-spend confirmation. Auto is off by default, so Pip asks first. |
| `pixellab-pip bark` | Toggle the completion sound. On by default. |
| `pixellab-pip update` | Update through the current install method. |
| `pixellab-pip uninstall` | Remove Pip while keeping secrets and generated outputs by default. |

The leading `/`, `@`, or `$` depends on your agent. Read the [usage and setup guide ↗](docs/usage.md) for command behavior, MCP/API modes, token safety, and more examples.

## Benchmark

Pip is tested on plain-language routing scenarios against the official MCP docs alone and an agent with no added PixelLab context. The benchmark is dry: it spends no PixelLab credits.

| Method | Routes to the exact PixelLab tool | Context tokens per session |
|---|---|---|
| **PixelLab Pip skill** | **~98%** | ~7.5k base + discoverable references = ~9.1k average |
| Official `mcp/docs` injected | ~58% | ~7.7k |
| No skill (agent knowledge only) | ~24% | 0 |

Dated, nondeterministic results from 20 scenarios and three agents: official docs handled MCP well but missed every REST-only route.

[Full report and reproduction steps ↗](docs/pixellab-pip-benchmark.md)

## Security

Pip is Markdown instructions plus two small Python 3.10+ local helpers. It ships no compiled binaries, the helpers make no network calls, and guidance, setup, and routing work without a PixelLab token. Live generation may spend credits and requires a bearer token, but Pip never needs it pasted into chat, never automates undocumented private endpoints, asks before destructive remote changes, and labels local processing.

Read [Security and trust ↗](docs/security.md) for the complete access boundary, public audits, release provenance, and scanner disclosures, or [report a concern ↗](SECURITY.md).

## More Documentation

- [Resources ↗](docs/resources.md) — official PixelLab links and related tools.
- [Developer guide ↗](docs/developer.md) — repository structure, local development, testing, and releases.
- [More guides ↗](docs/README.md) — research, integration background, and every specialized guide.
- [MIT License ↗](LICENSE)
