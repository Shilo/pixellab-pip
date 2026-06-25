# PixelLab Pip

PixelLab Pip is an unofficial, agent-agnostic PixelLab workflow router implemented as a portable Agent Skill. It teaches coding agents how to choose between documented PixelLab MCP tools, REST v2 endpoints, website/editor fallback, Aseprite, Pixelorama, and local asset assembly workflows without pretending those surfaces have identical capabilities. The repository is mostly Markdown because the product is the routing contract itself: task detection, progressive reference loading, prompt normalization, image-role classification, credential handling, usage reporting, localization, and specialty workflows for sprites, tilesets, layered characters, edits, animation, and completion sounds. Treat the main skill file as the source of truth, and open reference files only when the user's request needs that exact topic.

Canonical skill contract: skills/pixellab-pip/SKILL.md
Product overview and user-facing install flow: README.md
PixelLab terminology and surface model: docs/pixellab/
Tool comparison and integration notes: docs/tools/
MCP/API setup flow: skills/pixellab-pip/references/setup.md
Credential and bearer-token rules: skills/pixellab-pip/references/credentials.md
Official PixelLab docs refresh rules: skills/pixellab-pip/references/official-pixellab-documentation.md
Image attachment role routing: skills/pixellab-pip/references/image-input-roles.md
Usage, balance, job, and result reporting: skills/pixellab-pip/references/usage-reporting.md
Website/editor fallback rules: skills/pixellab-pip/references/browser-fallback.md
Prompt and local assembly workflows: skills/pixellab-pip/references/local-asset-assembly.md
Localization behavior: skills/pixellab-pip/references/localization.md
Layered character and outfit workflows: skills/pixellab-pip/references/paperdolling.md
Tileset workflow routing: skills/pixellab-pip/references/tilesets.md
Aseprite CLI/MCP workflow: skills/pixellab-pip/references/aseprite-cli.md
Bark completion sound behavior: skills/pixellab-pip/references/bark.md
Developer context: docs/developer.md only when changing repository structure
Git conventional commits: <type>[optional scope]: <description>
