# Uninstall

Reference for natural-language removal: taking Pip out of an assistant/editor/app using whatever method installed it. This extends the existing Pip skill; it is not a separate skill. Uninstall is destructive, so confirmation before removal is the core of this contract.

The command is one word after the trigger, such as `/pixellab-pip uninstall`, `@pixellab-pip uninstall`, or `$pixellab-pip uninstall`. Some apps pass it as an argument, others as prose; treat it the same either way and require no flags or app-specific syntax.

## 1. Detect the install method first

Stay agent-agnostic and OS-agnostic until the app is named or detected; do not assume an app, OS, shell, or path. Pip is installed for an app in one of three shapes — remove via the same shape it was installed with:

- **Marketplace plugin / extension** — installed through the app's plugin or extension mechanism. Remove with that app's own uninstall command (section 2).
- **Manually-copied skill folder** — a `pixellab-pip` folder copied into a skills directory the app reads. Remove by deleting that one folder (section 2).

If you cannot tell which shape applies, ask, or use the app's documented listing command to check (e.g. `/plugin` list, `extensions list`) before acting. Never scan broad locations to discover an install — act only on the app's own uninstall command or a known skill path.

## 2. Per-app uninstall mechanics

Use the app's documented mechanism; if unsure of exact syntax, check its help/refresh its plugin list rather than guessing. The marketplace is `pixellab-pip-plugins` and the plugin is `pixellab-pip`.

- **Claude Code**: `/plugin uninstall pixellab-pip@pixellab-pip-plugins` (CLI: `claude plugin uninstall pixellab-pip@pixellab-pip-plugins`). Optionally also remove the marketplace: `/plugin marketplace remove pixellab-pip-plugins`.
- **Codex**: `codex plugin remove pixellab-pip@pixellab-pip-plugins`. Optionally `codex plugin marketplace remove pixellab-pip-plugins`.
- **Gemini CLI**: `gemini extensions uninstall pixellab-pip`.
- **GitHub Copilot CLI**: `copilot plugin uninstall pixellab-pip@pixellab-pip-plugins`.
- **Cursor**: `cursor-agent plugin marketplace remove pixellab-pip-plugins`, or delete the copied skill folder (`.cursor/skills/pixellab-pip`).
- **Antigravity CLI**: `agy plugin uninstall pixellab-pip`, or delete the skill folder (e.g. `~/.gemini/antigravity-cli/skills/pixellab-pip`).
- **OpenCode, Deep Code, Antigravity IDE/2.0, VS Code, or any manual skill-copy install**: delete the `pixellab-pip` skill folder from the skills directory the agent reads — e.g. `.opencode/skills/pixellab-pip`, `~/.agents/skills/pixellab-pip`, `.claude/skills/pixellab-pip`, `.cursor/skills/pixellab-pip`. If Pip was installed as an Antigravity plugin, delete the `pixellab-pip` plugin folder instead (e.g. `~/.gemini/config/plugins/pixellab-pip`).
- **Any other named app**: use its documented plugin/extension uninstall command, or delete the copied skill folder. Do not invent syntax.

Pre-v1.0 installs used a marketplace named `pixellab-pip` (not `pixellab-pip-plugins`) — an old install removes under the old names (e.g. `/plugin uninstall pixellab-pip@pixellab-pip` and `/plugin marketplace remove pixellab-pip`).

## 3. Confirm before removing

Uninstall is destructive. Report exactly what will be removed and get explicit approval before removing anything. Any bulk or broader-than-default removal needs its own explicit scope confirmation.

Before asking, report:

- **Method**: marketplace/plugin uninstall command, or delete a named skill folder.
- **Exact target**: the plugin/marketplace name, or the full skill-folder path.
- **Config entries touched**: which config entries the uninstall removes (none, for a plain folder delete).
- **Reload**: whether the app must restart or reload for the skill/tools to disappear.

By default remove **only** the Pip skill/plugin and its config entry. Keep everything that belongs to the user, unless they explicitly ask to remove it too:

- the `pixellab-pip-generations/` output folder and any generated assets in it,
- the user's remote PixelLab assets (characters, animations, tilesets, etc.),
- `PIXELLAB_SECRET` and any stored PixelLab credential.

## 4. Optional opt-in extras

You MAY offer, as separate explicit opt-ins never applied automatically:

- Removing a leftover `pixellab` MCP server config entry (the entry `setup.md` may have created), only from a config path the user names or approves.
- Unsetting `PIXELLAB_SECRET`. Never print, read, or echo the value while doing so — follow `credentials.md` for anything touching the Secret.

Offer each only after the default removal, and only if the user asks or agrees. Never scan broad locations to find these — act only on the known install path or a config path the user provides.

## 5. Reload after removal

Tell the user to restart or reload the app only if it requires that for the skill/tools to disappear (many apps drop a removed plugin or deleted skill folder on next launch, some need a manual reload). Do not tell them to restart when the app clears it live.

## 6. Verify after

Confirm Pip is gone, agent-agnostic: it is no longer listed by the app's plugin/extension/skill listing, or the skill folder no longer exists at its path. If PixelLab MCP tools were removed with it, confirm they are no longer exposed. Report what was removed, what was kept (the user's outputs, remote assets, and Secret unless they opted to remove them), and any reload still pending.

## Uninstall guardrails

- Confirm before any removal; never remove without explicit approval, and never remove more than the default scope without separate confirmation.
- Never delete the user's `pixellab-pip-generations/` folder, generated assets, remote PixelLab assets, or `PIXELLAB_SECRET` unless the user explicitly asks.
- Never scan broad locations to find what to delete; act only on the app's own uninstall command or a known install path.
- Never print, read, or measure the Secret when offering to unset it; follow `credentials.md`.
