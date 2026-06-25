# PixelLab Pip

PixelLab Pip is an unofficial, agent-agnostic PixelLab workflow router packaged as a plugin and Agent Skill. It helps coding agents handle PixelLab asset generation, editing, animation, MCP setup, REST v2 integration, website/editor fallback, Aseprite and Pixelorama workflows, bearer-token setup, SDK/docs checks, endpoint selection, image input roles, prompt normalization, localization, usage reporting, and completion sound behavior. The core product is not an application server or library build; it is a portable skill contract plus manifests for multiple agent/plugin ecosystems. Treat `skills/pixellab-pip/SKILL.md` as the source of truth, and treat reference files as progressive context that should be opened only when the user's request needs that specialty.

Canonical skill contract: `skills/pixellab-pip/SKILL.md`

Product overview and install instructions: `README.md`

Developer workflow and repository layout: `docs/developer.md`

Documentation index: `docs/README.md`

PixelLab terminology and surface model: `docs/pixellab/`

Tool comparison and integration notes: `docs/tools/`

Showcase assets and examples: `docs/showcase/`

Root plugin manifest: `plugin.json`

Codex plugin manifest: `.codex-plugin/plugin.json`

Claude plugin manifests: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`

Cursor plugin manifests: `.cursor-plugin/plugin.json`, `.cursor-plugin/marketplace.json`

GitHub Copilot plugin marketplace manifest: `.github/plugin/marketplace.json`

Gemini extension context: `gemini-extension.json`, `GEMINI.md`

Release packaging workflow: `.github/workflows/release-skill.yml`

Codex local install helper: `dev-tools/manage-codex-plugin.ps1`

Credential and bearer-token rules: `skills/pixellab-pip/references/credentials.md`

MCP/API setup flow: `skills/pixellab-pip/references/setup.md`

Official PixelLab docs refresh rules: `skills/pixellab-pip/references/official-pixellab-documentation.md`

Image attachment role routing: `skills/pixellab-pip/references/image-input-roles.md`

Usage, balance, job, and result reporting: `skills/pixellab-pip/references/usage-reporting.md`

Website/editor fallback rules: `skills/pixellab-pip/references/browser-fallback.md`

Localization behavior: `skills/pixellab-pip/references/localization.md`

Prompt and local assembly workflows: `skills/pixellab-pip/references/local-asset-assembly.md`

Layered character and outfit workflows: `skills/pixellab-pip/references/paperdolling.md`

Tileset workflow routing: `skills/pixellab-pip/references/tilesets.md`

Aseprite CLI workflow: `skills/pixellab-pip/references/aseprite-cli.md`

Aseprite MCP workflow: `skills/pixellab-pip/references/aseprite-mcp.md`

Bark completion sound behavior: `skills/pixellab-pip/references/bark.md`, `skills/pixellab-pip/assets/bark.py`, `skills/pixellab-pip/assets/bark.wav`

Git conventional commits: use focused messages such as `docs(aseprite): add aseprite-mcp documentation`, `feat(aseprite-cli): enhance safety guidelines`, or `fix(setup): clarify bearer-token reuse`.

Security posture: never print secrets, ask users to paste bearer tokens into chat, inspect private `.env*` files, or automate undocumented internal PixelLab endpoints.
