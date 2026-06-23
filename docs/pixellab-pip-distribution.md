# PixelLab Pip Distribution

Last reviewed: 2026-06-23.

PixelLab Pip is distributed as an agent-agnostic plugin/skill repository. The public repository should keep runtime skill files separate from docs and packaging metadata so installed agents only load the files they need.

## Chosen Layout

```text
README.md
plugin.json
gemini-extension.json
GEMINI.md
.codex-plugin/plugin.json
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
.cursor-plugin/plugin.json
.cursor-plugin/marketplace.json
.github/plugin/marketplace.json
.agents/plugins/marketplace.json
docs/
skills/
  pixellab-pip/
    SKILL.md
    references/
```

The runtime skill is:

```text
skills/pixellab-pip/
```

Docs, plugin manifests, and repository metadata should not be copied into raw skill directories unless an agent app's plugin system intentionally installs the whole plugin bundle.

## Installation Priority

Prefer marketplace/plugin installs when available. They are easier to update and avoid drifting manual copies.

Manual install remains useful for project-local setup, testing, and agent apps that support raw Agent Skills without a marketplace. Manual instructions should copy only:

```text
skills/pixellab-pip/
```

## Agent Support

PixelLab Pip is agent-agnostic at the skill level. The repo includes wrapper metadata for popular agent apps and CLIs, but the core skill is the same `SKILL.md` plus `references/` folder.

Supported public packaging targets in this repo:

- Claude Code plugin metadata.
- Codex plugin metadata.
- Cursor plugin metadata.
- GitHub Copilot plugin marketplace metadata.
- VS Code agent plugin metadata.
- Gemini CLI extension adapter.
- Raw Agent Skill folder for compatible agents.

## Alias Decision

The public repo should not maintain a separate `/pip` skill folder. Duplicated skill folders can drift and make updates harder. If an agent platform later supports true aliases without duplicate runtime files, `/pip` can be added as metadata only.
