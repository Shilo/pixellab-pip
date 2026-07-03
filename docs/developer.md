# Developer

Last reviewed: 2026-07-03.

## Table of Contents

- [Quality Assurance](#quality-assurance)
- [Codex Local Plugin Testing](#codex-local-plugin-testing)
- [PixelLab Docs Drift Checks](#pixellab-docs-drift-checks)
- [PixelLab MCP Tileset Simulator](#pixellab-mcp-tileset-simulator)
- [Repository Layout](#repository-layout)

## Quality Assurance

Run the repository QA gate before release-oriented changes:

```powershell
python dev-tools/qa.py
```

The gate validates tracked JSON, version consistency, Python compilation, local Markdown links, skill reference pointers, media signatures, and helper smoke tests.

Local helper scripts target Python 3.10 or newer.

## Codex Local Plugin Testing

Codex installs both remote and local plugins into its plugin cache. Editing files in this repository, such as `skills/pixellab-pip/SKILL.md`, does not live-update the active Codex skill. Refresh the local development install after repo edits, then open a fresh Codex thread so the new cached snapshot is loaded.

Use the Codex-only helper:

```powershell
.\dev-tools\manage-codex-plugin.ps1
```

The script resolves the repository path from its own location, so it can be launched from another working directory or by double-clicking the `.ps1` file. It pauses before exit so the result stays visible.

The menu offers:

- `Install <opposite mode>` - switch between `development local` and `production remote`.
- `Update <current mode>` - refresh the currently installed mode.
- `Uninstall <current mode>` - remove the installed plugin and marketplace entry.
- `Cancel` - exit without changes.

When no plugin is installed, the menu offers `Install development local`, `Install production remote`, `Uninstall pixellab-pip (not installed)`, and `Cancel`.

For `development local`, the script temporarily writes a Codex cachebuster version to `.codex-plugin/plugin.json`, installs from this repository, then restores the manifest. This creates a fresh cache path such as `0.4.0+codex.dev-YYYYMMDDHHMMSS` without permanently changing the repo version.

For `production remote`, the script installs from the GitHub marketplace source in `plugin.json`. Production updates run `codex plugin marketplace upgrade` before reinstalling because Codex does not currently provide a `codex plugin update` command.

To verify which build Codex is using, check the path shown when a skill is invoked or run:

```powershell
codex plugin list --json
codex debug prompt-input '@pixellab-pip bark off'
```

`development local` should show this repository as the source and a version containing `+codex.dev-`. `production remote` should show the GitHub marketplace source and the normal release version.

## PixelLab Docs Drift Checks

PixelLab's public REST and MCP documentation can change independently of this repository. Before updating routing, endpoint, schema, prompt-limit, or MCP-tool claims, refresh the local-only documentation cache:

```powershell
.\dev-tools\manage-pixellab-doc-cache.ps1
```

The menu offers `Initialize local docs cache` only before the cache has a manifest. Once initialized, it offers refresh and status actions. Explicit `-Action init` remains safe and syncs cache metadata/source definitions.

For noninteractive use, pass `-Action init`, `-Action refresh`, or `-Action status`.

Direct Python commands are useful for automation or non-Windows shells:

```powershell
python dev-tools/pixellab-doc-watch.py init
python dev-tools/pixellab-doc-watch.py refresh
python dev-tools/pixellab-doc-watch.py status
```

The watcher keeps downloaded upstream docs under `.local/pixellab-doc-watch/`, which is ignored by Git. It treats REST OpenAPI as the API source of truth, checks `llms.txt` for parity, tracks the `/v2/docs` and `/v2/redoc` documentation shells, and tracks MCP docs as the MCP tool inventory source.

Fresh checkout and maintenance instructions live in [PixelLab Documentation Watch Cache](pixellab/pixellab-doc-watch-cache.md).

## PixelLab MCP Tileset Simulator

Use [dev-tools/pixellab_mcp_tileset_sim.py](../dev-tools/pixellab_mcp_tileset_sim.py) when maintaining or validating the tileset workflow without spending PixelLab generations. It accepts the same MCP create-tool JSON used by `create_sidescroller_tileset` and `create_topdown_tileset`, validates the request shape, renders local component previews, and repacks the compact simulated sheet into PixelLab-style export layouts.

Typical smoke tests from the repository root:

```powershell
'{"lower_description":"stone brick","transition_description":"moss","transition_size":0.25}' | python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset --draw-grid
'{"lower_description":"ocean water","upper_description":"sandy beach","transition_description":"sea foam","transition_size":0.25}' | python dev-tools/pixellab_mcp_tileset_sim.py create_topdown_tileset --draw-grid
```

By default, generated PNGs and `sim-report.json` are written under `.local/mcp-tileset-sim-output/latest/`. Each run also writes stable component previews under `components/`, such as `lower-tile.png`, `upper-tile.png`, `top-tile.png`, `transition-tile.png`, and `center-tile.png` when applicable. Use `--output NAME` to keep multiple attempts side by side, and `--layout 15-tileset`, `--layout wang`, or `--layout godot-3x3` to preview the supported PixelLab export layouts.

Renderer modes:

- `--renderer deterministic` - local keyword/semantic rendering; fastest and default.
- `--renderer codex` - asks Codex for a constrained semantic recipe, then renders locally.
- `--renderer deepseek-v4-pro` - asks OpenCode's `deepseek/deepseek-v4-pro` model for the same constrained semantic recipe, then renders locally.

The simulator is intentionally not PixelLab. It does not call PixelLab, spend credits, poll jobs, download assets, or reproduce PixelLab model taste. Use it to inspect request shape, output layout, and broad terrain/transition semantics before deciding whether a live generation is worth running.

The execution-oriented runbook for agents lives in [PixelLab MCP Tileset Simulator](../dev-tools/pixellab_mcp_tileset_sim.md).

## Repository Layout

```text
README.md
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
.claude-plugin/plugin.json
.cursor-plugin/marketplace.json
.cursor-plugin/plugin.json
.github/plugin/marketplace.json
gemini-extension.json
GEMINI.md
.codex-plugin/plugin.json
plugin.json
docs/
  showcase/
skills/
  pixellab-pip/
    SKILL.md
    pixellab-pip.json (created on bark toggle)
    assets/
      bark.py
      bark.wav
    references/
```

The root plugin files are thin wrappers for each agent app. The only runtime skill is `skills/pixellab-pip/SKILL.md`.

`gemini-extension.json` installs PixelLab Pip as a Gemini CLI extension. `GEMINI.md` gives Gemini the invocation context and points back to the same skill contract; it does not create a second Pip skill.

Runtime files:

- `skills/pixellab-pip/SKILL.md` - the canonical skill file.
- `skills/pixellab-pip/pixellab-pip.json` - optional user-local bark preference file, created only when bark is toggled.
- `skills/pixellab-pip/assets/bark.py` - best-effort local helper for deterministic bark config and sound playback.
- `skills/pixellab-pip/assets/bark.wav` - bundled bark sound.
- `skills/pixellab-pip/references/credentials.md` - PixelLab bearer-token setup, UI naming, and MCP auth-source reuse.
- `skills/pixellab-pip/references/setup.md` - natural-language setup for MCP, documented REST v2 fallback, and auth after install.
- `skills/pixellab-pip/references/bark.md` - persistent completion sound toggle and generation-finish rules.
- `skills/pixellab-pip/references/browser-fallback.md` - permission rules for visible website/editor fallback.
- `skills/pixellab-pip/references/skill-icons.md` - skill, ability, spell, action-bar, and hotbar icon routing details.
- `skills/pixellab-pip/references/item-icons.md` - inventory item, equipment, loot, and pickup icon routing details.
- `skills/pixellab-pip/references/cost-routing.md` - cheap, budget, and Pro-vs-v3/new route selection.
- `skills/pixellab-pip/references/paperdolling.md` - layered character and outfit workflow contract.
- `skills/pixellab-pip/references/tilesets.md` - terrain/platformer/tile-variant routing details.
- `skills/pixellab-pip/references/image-input-roles.md` - image input roles for attachments, file paths, and endpoint fields.
- `skills/pixellab-pip/references/localization.md` - non-English request translation and response-language handling.
- `skills/pixellab-pip/references/usage-reporting.md` - usage, balance, job, and result reporting.
- `skills/pixellab-pip/references/job-lifecycle.md` - async status, MCP review state, rate limits, and expiring downloads.
- `skills/pixellab-pip/references/animation.md` - raw animation, interpolation, outfit transfer, and frame-anchor workflow details.
- `skills/pixellab-pip/references/editor-only-utilities.md` - editor-only utility routing and unsupported public-route caveats.
- `skills/pixellab-pip/references/prompt-limits.md` - REST v2 natural-language field limits and prompt-length retry handling.
- `skills/pixellab-pip/references/aseprite-cli.md` - Aseprite CLI/Lua workspace, import, export, and packaging workflows.
- `skills/pixellab-pip/references/aseprite-mcp.md` - explicit Aseprite MCP server/tooling routing.
- `skills/pixellab-pip/references/local-asset-assembly.md` - local GIF, spritesheet, and ImageMagick assembly after generation.
- `skills/pixellab-pip/references/official-pixellab-documentation.md` - when and how to refresh official PixelLab documentation.
