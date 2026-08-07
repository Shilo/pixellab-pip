# Installation

Use the [README quick start](../README.md#install) for the shortest path. This guide covers every supported install shape, upgrades, migration, and Claude Code cloud sessions.

After any install, restart or reload the agent if required, then run PixelLab Pip setup using the prefix your agent supports: `/pixellab-pip setup`, `@pixellab-pip setup`, or `$pixellab-pip setup`.

## Agent-Assisted Install (Recommended)

Easiest for most people: copy the protected [agent-assisted install prompt](../README.md#agent-assisted-install-recommended) from the README. It tells your agent to read this full guide before choosing the correct marketplace, plugin, extension, or skill route.

Claude Code on the web has no plugin manager. Use the [cloud-specific route](#claude-code-on-the-web) instead.

If you are upgrading from a pre-v1.0 marketplace install, re-run the prompt above or follow the [one-time clean reinstall](#upgrade-from-pre-v10) before using the platform instructions below. A normal update does not switch marketplaces.

## Marketplace And Extension Installs

Install PixelLab Pip as a plugin or extension when your agent supports marketplaces. Use manual skill install only when your agent does not support plugin installation.

<details>
<summary><strong>Claude Code</strong></summary>

Inside a session:

```text
/plugin marketplace add Shilo/pixellab-pip
/plugin install pixellab-pip@pixellab-pip-plugins
/pixellab-pip setup
```

Or from a terminal:

```text
claude plugin marketplace add Shilo/pixellab-pip
claude plugin install pixellab-pip@pixellab-pip-plugins
```

Then reload and run `/pixellab-pip setup` in Claude Code.

Update inside a session:

```text
/plugin marketplace update pixellab-pip-plugins
/plugin update pixellab-pip@pixellab-pip-plugins
```

Terminal equivalent:

```text
claude plugin marketplace update pixellab-pip-plugins
claude plugin update pixellab-pip@pixellab-pip-plugins
```

</details>

<details>
<summary><strong>Codex</strong></summary>

```text
codex plugin marketplace add Shilo/pixellab-pip
codex plugin add pixellab-pip@pixellab-pip-plugins
```

Reload Codex, then run `@pixellab-pip setup`.

Update:

```text
codex plugin marketplace upgrade pixellab-pip-plugins
codex plugin remove pixellab-pip@pixellab-pip-plugins
codex plugin add pixellab-pip@pixellab-pip-plugins
```

</details>

<details>
<summary><strong>Cursor</strong></summary>

Use Cursor's plugin marketplace or team marketplace flow when available, or [install the raw skill manually](#manual-skill-install).

```text
/pixellab-pip setup
```

</details>

<details>
<summary><strong>VS Code Agent Plugins</strong></summary>

Use **Chat: Install Plugin From Source** with this repo URL or VS Code's plugin marketplace flow, or [install the skill manually](#manual-skill-install).

```text
/pixellab-pip setup
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

```text
gemini extensions install https://github.com/Shilo/pixellab-pip
/pixellab-pip setup
```

Gemini uses `gemini-extension.json` for installation and `GEMINI.md` for invocation context. Both point back to the same skill contract in `skills/pixellab-pip/SKILL.md`.

Update:

```text
gemini extensions update pixellab-pip
```

</details>

<details>
<summary><strong>GitHub Copilot CLI</strong></summary>

```text
copilot plugin marketplace add Shilo/pixellab-pip
copilot plugin install pixellab-pip@pixellab-pip-plugins
/pixellab-pip setup
```

Update with `copilot plugin update pixellab-pip`.

</details>

<details>
<summary><strong>Antigravity</strong></summary>

Antigravity supports two installation shapes:

1. **Custom plugin — Antigravity IDE / 2.0.** When the product supports custom plugins, copy or extract the whole repository so its root `plugin.json` lands at either path below. No Git installation is required. Keep `plugin.json` and `skills/` together; the manifest marks the plugin and `skills/pixellab-pip/` contains the complete skill.

When copying an existing local working tree, do not carry over a gitignored `skills/pixellab-pip/pixellab-pip.json` preference file.

```text
Global:    ~/.gemini/config/plugins/pixellab-pip/plugin.json
Workspace: <workspace-root>/.agents/plugins/pixellab-pip/plugin.json
```

2. **Native Agent Skill — fallback or Antigravity CLI.** Copy the entire bundled `skills/pixellab-pip/` directory, including all references, helpers, assets, and blueprints, so its top-level `SKILL.md` lands at the matching path. Do not carry over a gitignored `pixellab-pip.json` preference file from another install or working tree.

```text
Any Antigravity workspace: <workspace-root>/.agents/skills/pixellab-pip/SKILL.md
Any Antigravity global:     ~/.gemini/config/skills/pixellab-pip/SKILL.md
```

Prefer the workspace path; it is scanned by every Antigravity flavor (base `agy`, the CLI, and the IDE). For a global install use `~/.gemini/config/skills/` — it is the only global directory read by all of them. Other `~/.gemini/*/skills/` locations (such as `antigravity/skills/` or `antigravity-cli/skills/`) are read by some flavors but not others, so a skill placed there can appear to vanish when you switch flavor. Install a real directory, not a symlink — Antigravity's skill scan does not follow symlinks (and likely not Windows junctions), so a linked install is silently skipped with no error.

The plugin form is a packaging convenience, not a requirement for Pip's behavior. Antigravity does not document a third-party marketplace manifest, so do not use the repository's `.agents/plugins/marketplace.json`; that file belongs to the separate VS Code Agent Plugins format. Also do not install the repository root as an Antigravity CLI plugin because its strict manifest schema is incompatible with the shared root manifest. Restart or reload Antigravity after either supported install, then ask it to use `pixellab-pip` for setup. In Antigravity CLI, `/pixellab-pip setup` invokes the installed skill. The setup wizard supports Antigravity's MCP UI, global and workspace `mcp_config.json`, required remote `serverUrl` schema, and separate REST v2 fallback readiness.

Pip intentionally does not bundle an Antigravity `mcp_config.json`: PixelLab MCP requires a private bearer token, and Antigravity does not document environment-variable expansion in custom HTTP headers. `/pixellab-pip setup` gives a token-free MCP preview and guides the user through credential completion after approval, then separately checks `PIXELLAB_SECRET` for REST v2 fallback.

</details>

<details>
<summary><strong>OpenCode</strong></summary>

OpenCode discovers Agent Skills natively — there is no marketplace step (its `opencode plugin` command installs JavaScript code plugins, not skills). Use [Manual Skill Install](#manual-skill-install) to place it in any path OpenCode reads: `.opencode/skills/`, `.agents/skills/`, or `.claude/skills/` (project, or their `~/.config/opencode`, `~/.agents`, `~/.claude` globals). OpenCode loads it on demand through its built-in `skill` tool.

```text
.opencode/skills/pixellab-pip/SKILL.md
```

Then ask OpenCode to set up PixelLab Pip.

</details>

<details>
<summary><strong>Deep Code (DeepSeek V4)</strong></summary>

Deep Code — the DeepSeek V4 terminal agent — discovers Agent Skills natively; there is no marketplace. Install the CLI, then use [Manual Skill Install](#manual-skill-install) to place the skill in a path it reads — `~/.agents/skills/` for every project, or `.agents/skills/` or `.deepcode/skills/` inside one project:

```text
npm install -g @vegamo/deepcode-cli
```

```text
.agents/skills/pixellab-pip/SKILL.md
```

Open Deep Code's skill picker with `/` or type the skill name, then run PixelLab Pip setup.

</details>

## Cross-Agent CLI

The [`npx skills`](https://www.skills.sh/shilo/pixellab-pip/pixellab-pip) installer copies the complete skill into a supported agent directory:

```text
npx skills add Shilo/pixellab-pip --skill pixellab-pip
```

For a non-interactive global install, select an agent with `-a`, add `-g`, and skip prompts with `-y`:

```text
npx skills add Shilo/pixellab-pip --skill pixellab-pip -a claude-code -g -y
```

This copies `SKILL.md` plus its `references/`, `assets/`, and `blueprints/`. Then run `/pixellab-pip setup`.

To run it once without installing (prints the skill's prompt to stdout):

```text
npx skills use Shilo/pixellab-pip --skill pixellab-pip
```

## Manual Skill Install

Manual install is useful for project-local setup or agent apps that support raw Agent Skills without plugin installation. Copy the bundled contents of `skills/pixellab-pip/` into a folder named `pixellab-pip` inside your agent's skills directory, so `SKILL.md` is directly inside the final folder. Include all references, helpers, assets, and blueprints, but exclude a gitignored `pixellab-pip.json` preference file from an existing install or working tree.

You can also download the skill zip from the [latest release](https://github.com/Shilo/pixellab-pip/releases/latest) and extract it into your agent's skills directory.

Common project-local destinations:

```text
.agents/skills/pixellab-pip/SKILL.md
.claude/skills/pixellab-pip/SKILL.md
.cursor/skills/pixellab-pip/SKILL.md
.opencode/skills/pixellab-pip/SKILL.md
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force .agents\skills\pixellab-pip
Copy-Item -Recurse -Force -Exclude pixellab-pip.json skills\pixellab-pip\* .agents\skills\pixellab-pip\
```

macOS or Linux:

```bash
mkdir -p .agents/skills/pixellab-pip
cp skills/pixellab-pip/SKILL.md .agents/skills/pixellab-pip/
for directory in assets blueprints references; do
  mkdir -p ".agents/skills/pixellab-pip/$directory"
  cp -R "skills/pixellab-pip/$directory/." ".agents/skills/pixellab-pip/$directory/"
done
```

Choose the destination your agent reads, restart or reload it, and run setup.

## Upgrade From Pre-v1.0

Pre-v1.0 used the `pixellab-pip` marketplace; v1.0 and later use `pixellab-pip-plugins`. A normal update does not switch marketplaces, so perform a one-time clean reinstall.

Claude Code terminal:

```text
claude plugin uninstall pixellab-pip@pixellab-pip
claude plugin marketplace remove pixellab-pip
claude plugin marketplace add Shilo/pixellab-pip
claude plugin install pixellab-pip@pixellab-pip-plugins
```

Codex:

```text
codex plugin remove pixellab-pip@pixellab-pip
codex plugin marketplace remove pixellab-pip
codex plugin marketplace add Shilo/pixellab-pip
codex plugin add pixellab-pip@pixellab-pip-plugins
```

Other marketplace agents follow the same remove-old-marketplace, add-new-marketplace pattern. Copied-skill installs are unaffected.

## Claude Code On The Web

Cloud sessions at [claude.ai/code](https://claude.ai/code) have no plugin manager: `/plugin` does not run there, and plugins installed in the CLI or desktop app do not carry over. Pip reaches a cloud session only when the repository you work in declares it, or when the skill is enabled on your claude.ai account. Read [Cloud limits](#cloud-limits) before spending credits from a cloud session.

### Agent-Assisted Install (Recommended)

Easiest — paste this into a cloud session and let it set itself up:

```text
You are running in a Claude Code cloud session (claude.ai/code), so the plugin
manager is unavailable — do not try `/plugin`, `claude plugin`, or anything that
assumes a local install. Set up PixelLab Pip from
https://github.com/Shilo/pixellab-pip the way cloud sessions support instead.
First read the install steps at
https://github.com/Shilo/pixellab-pip/blob/main/docs/install.md#claude-code-on-the-web,
then use the plugin route: create or merge the `extraKnownMarketplaces` and
`enabledPlugins` entries shown there into this repository's
`.claude/settings.json`, preserving existing keys, and commit it. If this
repository cannot take a committed settings file, or the plugin does not load
in a fresh session, use the skill route instead: copy the whole
`skills/pixellab-pip/` folder — not just `SKILL.md` — to
`.claude/skills/pixellab-pip/` in this repository and commit that. Either way,
get that commit onto the branch my future cloud sessions start from — a cloud
session can only push to its own working branch, so open a pull request if that
is the default branch. Then tell me which route you used, that I need to start a
new cloud session for it to load, and how to invoke it. Finally, warn me about
the cloud limits before I spend any credits: `api.pixellab.ai` and
`www.pixellab.ai` are not on the default network allowlist, so no live PixelLab
call works until I add them; a PixelLab token can only live in this environment's
plaintext variables; and PixelLab MCP needs a committed `.mcp.json` in this
repository.
```

### Manual Install

#### Repository Plugin Route

Plugin route (updates from this repo automatically) — commit this to your project's `.claude/settings.json`, merging with any keys already there:

```json
{
  "extraKnownMarketplaces": {
    "pixellab-pip-plugins": {
      "source": { "source": "github", "repo": "Shilo/pixellab-pip" }
    }
  },
  "enabledPlugins": { "pixellab-pip@pixellab-pip-plugins": true }
}
```

Start a new cloud session — the plugin installs at session start — then invoke it as `/pixellab-pip:pixellab-pip <prompt>`, or as plain `/pixellab-pip <prompt>` unless another command already claims that name.

#### Repository Skill Route

Skill route (no marketplace) — copy `skills/pixellab-pip/` into your project's `.claude/skills/pixellab-pip/` as in [Manual Skill Install](#manual-skill-install), excluding a gitignored `pixellab-pip.json` preference file, and commit it. Invoke it as `/pixellab-pip <prompt>`. It loads mid-session when `.claude/skills/` already existed when the session started; if you created that directory just now, start a new session.

#### Account Route

Account route (no repository changes) — zip the skill folder so `pixellab-pip/SKILL.md` sits at the zip root, excluding a gitignored `pixellab-pip.json` preference file, then upload it under **Customize → Skills** on claude.ai with code execution enabled. Cloud sessions load the skills enabled on your account, in every repository. Use this when you cannot commit to the repository you work in.

For either repository route, a cloud session pushes only to its own working branch, so merge the commit into the branch your future sessions start from.

### Cloud Limits

Then run `/pixellab-pip setup` in the new session, and plan around these — the first one blocks every paid call:

- **Network.** `api.pixellab.ai` and `www.pixellab.ai` are not on the cloud default **Trusted** allowlist, so live generation, PixelLab MCP, balance checks, and doc lookups all fail until you open the environment selector at claude.ai/code, set **Network access** to **Custom**, add both hosts, and keep *Also include default list of common package managers* ticked. `github.com` is on Trusted, so installing Pip itself works untouched.
- **MCP.** Commit a project-scope `.mcp.json` to your own repository — a user-scope `claude mcp add -s user` never reaches the cloud — and approve the server when the session prompts. Reference the token by name, never as a literal value, because this file is committed. This repository gitignores its own `.mcp.json`, so cloning it does not hand you one.

  ```json
  {
    "mcpServers": {
      "pixellab": {
        "type": "http",
        "url": "https://api.pixellab.ai/mcp",
        "headers": { "Authorization": "Bearer ${PIXELLAB_SECRET}" }
      }
    }
  }
  ```

- **Secret.** A cloud environment has no secrets store, so `PIXELLAB_SECRET` can only go in its variables field — plaintext, readable by anyone using that environment, every member if it is org-shared, and applied only to sessions started afterwards. Ignore the OS dialog, `setx`, and shell-profile advice the setup wizard gives for local machines. Use a personal environment rather than a shared one, and rotate the Secret on your PixelLab account when you are done with it. If that exposure is not acceptable, do not run PixelLab from a cloud session at all: either keep cloud sessions token-free — routing, planning, prompt preparation, and blueprint authoring all work without one — or drive a session on your own machine from the same claude.ai/code interface with [Remote Control](https://code.claude.com/docs/en/remote-control), where your existing `.mcp.json` and local `PIXELLAB_SECRET` work untouched and no allowlist change is needed.
- **Output.** The session VM is reclaimed when the session ends and `pixellab-pip-generations/` is gitignored by default, so commit and push anything you paid for before you leave.
- **Update and uninstall.** `/pixellab-pip update` and `/pixellab-pip uninstall` drive the plugin manager, which cloud sessions lack. The plugin route already re-installs from the marketplace at every session start; to remove Pip, drop the entries from `.claude/settings.json` or delete `.claude/skills/pixellab-pip/`.
- **Missing local tools.** ImageMagick is not pre-installed — add `apt install -y imagemagick` to the environment's setup script for spritesheets and preview GIFs. Aseprite, Pixelorama, and the website editor are unreachable, the bark sound cannot play on a headless VM, and the `bark` and `auto` toggles reset each session.

Guidance, routing, prompt preparation, and docs work with no token and no allowlist change at all.
