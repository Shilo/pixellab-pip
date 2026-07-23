# Update

Reference for natural-language updates: bringing an installed Pip up to the latest version using whatever method installed it. This extends the existing Pip skill; it is not a separate skill. Update only replaces skill/plugin files — it never touches the user's `PIXELLAB_SECRET` or their `pixellab-pip-generations/` outputs.

The command is one word after the trigger, such as `/pixellab-pip update`, `@pixellab-pip update`, or `$pixellab-pip update`. Some apps pass it as an argument, others as prose; treat it the same either way and require no flags or app-specific syntax.

## 1. Detect the install method first

Update via the same method that installed Pip; do not assume. Three shapes exist:

- **Marketplace plugin** — installed through the app's plugin/marketplace command (plugin id `pixellab-pip`, marketplace `pixellab-pip-plugins`).
- **Extension** — installed through the app's extension mechanism.
- **Manual skill copy** — the `skills/pixellab-pip/` folder copied into the app's skills directory, or an extracted release zip.

Detect from what the app exposes (an installed-plugin list, an extensions list, or a skill folder on disk) before choosing an update path. If detection is ambiguous, ask which way the user installed it rather than guessing. If unsure of an app's exact command, use the app's own documented update mechanism or refresh its plugin/extension list — do not invent syntax.

## 2. Per-app update mechanics

Stays agent-agnostic and OS-agnostic until the app is named or detected. The commands below are the documented mechanism for each app; use the named/detected app's mechanism only. Prefer the non-interactive CLI form and run the update yourself; only hand the user an interactive in-app command when the app has no CLI.

- **Claude Code** (marketplace): refresh the marketplace, then update the plugin.

  ```text
  claude plugin marketplace update pixellab-pip-plugins
  claude plugin update pixellab-pip@pixellab-pip-plugins
  ```

  Claude's `plugin update` needs the qualified `plugin@marketplace` id — the bare `pixellab-pip` reports "not found".

- **Codex** (marketplace): upgrade the marketplace, then remove and re-add the plugin.

  ```text
  codex plugin marketplace upgrade pixellab-pip-plugins
  codex plugin remove pixellab-pip@pixellab-pip-plugins
  codex plugin add pixellab-pip@pixellab-pip-plugins
  ```

- **Gemini CLI** (extension):

  ```text
  gemini extensions update pixellab-pip
  ```

- **GitHub Copilot CLI** (marketplace):

  ```text
  copilot plugin update pixellab-pip
  ```

- **Cursor**: if installed via its marketplace, re-index/update it through that flow; otherwise re-copy the skill (below).
- **OpenCode, Deep Code, Antigravity, VS Code Agent Plugins, or any manual skill-copy install**: re-copy the entire latest `skills/pixellab-pip/` folder (every file, not just `SKILL.md`) over the existing install, or re-download and extract the latest release zip. Overwrite in place; do not delete sibling files first.
- **Any other named marketplace/extension app**: use the app's own documented update or refresh command with plugin id `pixellab-pip` / marketplace `pixellab-pip-plugins`. Do not invent syntax; fall back to the skill re-copy when no update command exists.

## 3. Restart or reload

Tell the user to restart or reload to activate the updated version — many apps load plugins and skills at startup, so the running session keeps the old version until then; a few pick up the change live. Also restart if the new version does not appear.

## 4. Verify after

Confirm the new version is active, agent-agnostic: use the app's plugin/extension list (e.g. `plugin list` showing the new version), or the app's own version display. For a skill-copy install, confirm the updated files landed at the install path. No credit spend and no secret handling here — this is a version check only.

## Update guardrails

- Update replaces only skill/plugin files. Do not read, move, rewrite, or clear `PIXELLAB_SECRET` or the `pixellab-pip-generations/` folder.
- Do not guess the install method or invent an app's update syntax; detect or ask, then use the app's documented mechanism.
- Do not spend credits or run any generation, edit, or animation as part of an update or its verification.
