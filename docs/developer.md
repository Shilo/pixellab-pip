# Developer

Last reviewed: 2026-07-05.

## Table of Contents

- [Quality Assurance](#quality-assurance)
- [Security Checks](#security-checks)
  - [OpenSSF Scorecard (maintainer-only)](#openssf-scorecard-maintainer-only)
- [Codex Local Plugin Testing](#codex-local-plugin-testing)
- [PixelLab Docs Drift Checks](#pixellab-docs-drift-checks)
- [PixelLab MCP Tileset Simulator](#pixellab-mcp-tileset-simulator)
- [Skill Benchmark: Routing and Cost](#skill-benchmark-routing-and-cost)
- [Tileset Research Notes](#tileset-research-notes)
- [Repository Layout](#repository-layout)

## Quality Assurance

Run the repository QA gate before release-oriented changes:

```powershell
python dev-tools/qa.py
```

The gate validates tracked JSON, version consistency, Python compilation, local Markdown links, skill reference pointers, media signatures, and helper smoke tests.

Local helper scripts target Python 3.10 or newer.

Install the local QA dependencies first on a fresh checkout:

```powershell
python -m pip install -r requirements-dev.txt
```

## Security Checks

The user-facing security story lives in the [README](../README.md#security): the SkillSpector skill audit (Code Scanning tab), the ClawHub independent registry audit, the VirusTotal malware scan, and the Sigstore build-provenance attestation. `SECURITY.md` holds the vulnerability-reporting policy.

### OpenSSF Scorecard (maintainer-only)

[OpenSSF Scorecard](https://scorecard.dev/viewer/?uri=github.com/Shilo/pixellab-pip) runs weekly for repo-hygiene tracking, but is intentionally kept off the README and out of the Code Scanning tab. The score reads low and largely **cannot** be raised on a solo project: Scorecard measures supply-chain maturity for widely-depended-upon libraries, and its heaviest checks — `Code-Review` (requires a second developer to approve pull requests) and `Maintained` (penalizes repos under 90 days old) — are structurally unreachable for a one-person, mostly-Markdown skill, so they sit near zero no matter the effort. Read it as a rough hygiene signal (branch protection, workflow permissions, pinned dependencies), not a safety verdict — the SkillSpector skill audit is the check that actually matters here.

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

For `development local`, the script temporarily writes a Codex cachebuster version to `.codex-plugin/plugin.json`, installs from this repository, then restores the manifest. This creates a fresh cache path such as `<version>+codex.dev-YYYYMMDDHHMMSS` (the current manifest version plus a timestamp) without permanently changing the repo version.

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
- `--renderer claude` - asks Claude Code for a constrained semantic recipe, then renders locally.
- `--renderer deepseek-v4-pro` - asks OpenCode's `deepseek/deepseek-v4-pro` model for the same constrained semantic recipe, then renders locally.

The simulator is intentionally not PixelLab. It does not call PixelLab, spend credits, poll jobs, download assets, or reproduce PixelLab model taste. Use it to inspect request shape, output layout, and broad terrain/transition semantics before deciding whether a live generation is worth running.

Read the simulator PNGs as placement diagrams, not as visual previews. A simulator image answers questions like "did this prompt put white on the boundary, top surface, interior, or body?" and "did this sidescroller request preserve transparency and avoid middle-seam highlights?" It does not answer whether PixelLab will draw the same contour, bricks, dithering, gray palette drift, or appealing material style.

For prompt optimization, agents should inspect `sim-report.json` and the `components/` images first, then translate the schematic result into a human-readable conclusion. Useful conclusions look like "this wording collapses sparse white texture to black," "this wording creates explicit white boundary highlights," or "this wording puts light pixels in the platform body instead of only the exposed top." Do not present a simulator PNG as if it were a predicted live PixelLab result.

The execution-oriented runbook for agents lives in [PixelLab MCP Tileset Simulator](../dev-tools/pixellab_mcp_tileset_sim.md).

## Skill Benchmark: Routing and Cost

Use [dev-tools/skill_benchmark.py](../dev-tools/skill_benchmark.py) to measure the skill's agent-side token/context cost and routing efficiency across skill versions and agent CLIs (`claude`, `codex`, `deepseek-v4-pro` via OpenCode). It compares git variants of `skills/pixellab-pip/` — by default the `pre-kiss-yagni-refactor` tag (commit `6fdae41`) against the working tree — by injecting each variant's SKILL.md into an isolated session, letting the agent progressively read `references/*.md` with a read-only tool, and capturing each CLI's native usage JSON (input/output/cache tokens, cost where exposed, turns, duration) plus deterministic routing-correctness regex checks. It measures the agent session only, never PixelLab credits.

The current working-tree skill is always the first column, so `--variants` only lists what to compare it against: git refs (e.g. the `pre-kiss-yagni-refactor` tag) plus two context-strategy arms that measure the skill against not using it at all — `vanilla` (no injected context — the agent's own knowledge) and `mcp-docs` (no skill, but the official `https://api.pixellab.ai/mcp/docs` text injected, matching the pixellab.ai/mcp "include this link in your prompts" tip; fetched live and saved to the results dir for audit). See [Official MCP Docs vs Pip Skill](tools/pixellab-mcp-docs-vs-pip-skill.md) for when each context strategy fits.

```powershell
python dev-tools/skill_benchmark.py --list                 # scenarios
python dev-tools/skill_benchmark.py --static               # free context-size comparison, no CLI calls
python dev-tools/skill_benchmark.py --agents claude --reps 2
python dev-tools/skill_benchmark.py --agents claude,codex,deepseek-v4-pro --reps 1
python dev-tools/skill_benchmark.py --agents claude --variants vanilla,mcp-docs --reps 2   # current skill vs no-skill vs official docs
```

Results land under `.local/bench/<stamp>/` (`SUMMARY.md`, `results.json`, `static.json`, per-cell responses); `results.json` is checkpointed after every cell, so an interrupted run is never lost. Continue one with `--resume <dir>` (reuses successful cells, re-runs errored/missing ones — e.g. after an agent runs out of tokens), or turn a partial run into a report offline with `--rescore <dir>`. The launcher takes `-Resume <dir>`. `.local/` is gitignored, so reports stay on the machine that ran them and are never committed. Workspaces are materialized outside the repo so CLAUDE.md/AGENTS.md cannot contaminate arms; reps interleave variants so provider caching hits both alike; medians are reported.

Every scenario is **dry**: the agent plans the route and makes no network or PixelLab call, so the benchmark spends **no PixelLab credits at all** — it needs no `PIXELLAB_SECRET`. Each scenario scores only on the **exact** correct PixelLab tool/endpoint; a plausible-but-wrong plan earns no partial credit for guessable parameters (image sizes, `no_background`, generic words). Non-`--static` runs still call the agent CLIs themselves (`claude`/`codex`/`opencode`), which consume that provider's tokens — that is the only cost. `--static` calls nothing.

On Windows, [dev-tools/run-skill-benchmark.ps1](../dev-tools/run-skill-benchmark.ps1) wraps the common presets so you do not have to remember flags. It preflights for `python` and the required agent CLIs and prints the report path when done. Run it with no argument for a menu, or pass a preset:

```powershell
.\dev-tools\run-skill-benchmark.ps1 -Preset static        # free, no CLI calls
.\dev-tools\run-skill-benchmark.ps1 -Preset dry-claude -Reps 2
.\dev-tools\run-skill-benchmark.ps1 -Preset dry-all
.\dev-tools\run-skill-benchmark.ps1 -Preset full          # all agents + variants, refreshes the report
.\dev-tools\run-skill-benchmark.ps1 -Preset full -Resume .local/bench/<stamp>   # continue an interrupted run
```

The published report at [docs/pixellab-pip-benchmark.md](pixellab-pip-benchmark.md) contains a `<!-- BENCHMARK:GENERATED -->` block that `--report FILE` rewrites from a run (the surrounding prose is preserved). The `full` preset passes `--report docs/pixellab-pip-benchmark.md` automatically, so a full run refreshes the committed report. `--rescore <dir> --report FILE` regenerates the block from an existing results dir without re-calling any CLI. Each run also prints its own approximate agent token/cost total at the end.

The `full` preset is exhaustive but **spends no PixelLab credits** (every scenario is dry). At its default `-Reps 1` it runs 3 agents x 4 variants x 20 scenarios = 240 agent calls — cells run sequentially at ~30 s median, so budget **~2 hours per rep**; `-Reps 2` doubles that to 480 calls and ~4 hours, and more than 2 reps is rarely worth the wall-clock. Its only cost is agent-provider tokens — on the order of a million-plus input tokens per proprietary-model agent per rep; deepseek-v4-pro via OpenCode is far cheaper. Scope with `--scenarios` for quick checks. (Both the raw `skill_benchmark.py --reps` default and the launcher's `-Reps` default are 1.)

All 20 scenarios are dry routing checks — the agent names the route it would take and deterministic regexes score only the **exact** correct tool. They span the full Intent Router surface: all 6 [showcase](showcase/README.md) results (icon/tile **sheets** routing to REST `generate-image-v2` where a pure-MCP agent tends to pick `create_ui_asset`/`create_tiles_pro`, the tiles-vs-tileset distinction, local 1-bit/palette recolor as Aseprite processing, the modular GUI kit, the animated character) plus the routes that separate the skill from the docs: standalone objects, REST-only backgrounds (no MCP tool exists — the sharpest docs blind spot), fonts, isometric tiles, sidescroller tilesets, balance checks, blueprint-preset replay, the skeleton pipeline, setup, cost routing, background-removal fallback, the refusal floor, and the paperdoll trap (a fitted addition is an edit on the base frame, not object generation).

## Tileset Research Notes

Live PixelLab tileset experiments that are useful for future routing and simulator work should be saved under `pixellab-pip-generations/` with a short `REPORT.md`, exact requests, raw responses, PixelLab originals, assembled sheets, and any clearly labeled QA derivatives.

Current 1-bit tileset findings live in:

- [PixelLab 1-Bit Tileset Prompt Testing](pixellab/pixellab-1bit-tileset-prompt-testing.md)
- [PixelLab 1-Bit Tileset Optimization Workflow](pixellab/pixellab-1bit-tileset-optimization-workflow.md)
- Local (gitignored, maintainer machine only): `pixellab-pip-generations/rest-1bit-control-validation-20260703/REPORT.md` and `pixellab-pip-generations/1bit-palette-clamp-study-20260703/REPORT.md`.

The key maintainer lesson from the 2026-07-03 REST validation is that `color_image` is not a safe automatic fix for strict black/white tilesets with white transition pixels. In both top-down and sidescroller checks, black/white `color_image` could erase the requested white transition and collapse the result toward black. Preserve this as a routing caution in `skills/pixellab-pip/references/tileset.md`: optimize PixelLab-generated shape and transition placement first, then use palette controls only as a separately verified follow-up or report palette-clamped derivatives as local processing.

The palette-clamp study shows that top-down and sidescroller are at different maturity levels. Top-down REST reference-only output can clamp cleanly because the raw result already contains high-luminance contour pixels. Sidescroller still needs prompt discovery because REST reference-only outputs put the top layer in dark colors that do not survive a clean threshold without adding body noise.

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
    blueprints/
    references/
```

The root plugin files are thin wrappers for each agent app. The only runtime skill is `skills/pixellab-pip/SKILL.md`.

`gemini-extension.json` installs PixelLab Pip as a Gemini CLI extension. `GEMINI.md` gives Gemini the invocation context and points back to the same skill contract; it does not create a second Pip skill.

Runtime files:

- `skills/pixellab-pip/SKILL.md` - the canonical skill file (router and contract).
- `skills/pixellab-pip/pixellab-pip.json` - optional user-local bark preference file, created only when bark is toggled.
- `skills/pixellab-pip/assets/` - `bark.py` + `bark.wav` (completion sound) and `background_removal.py` (conservative local background removal).
- `skills/pixellab-pip/references/*.md` - progressive-discovery references; SKILL.md's "References" section is the authoritative index of what each file covers. Notable merges: `icon.md` covers both skill/ability and inventory item icons.
