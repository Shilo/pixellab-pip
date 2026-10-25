# Changelog

All notable changes to PixelLab Pip are listed here, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases before 3.0.0 are on
[GitHub Releases](https://github.com/Shilo/pixellab-pip/releases).

## [Unreleased]

### Changed

- **Matches PixelLab's 2026-10-25 public docs.** Standard tilesets are quoted at 1 generation (Pro at 15 or 25), and
  top-down height, `view`, borders and no-effect controls follow the new contract; MCP sidescroller Pro mode is
  supported. Normal maps default to the 0.1-generation Lite mode, oversized transparent Pixen requests are known to be
  refused, text-only animals can use Pro Flash, and several cost and job-wait details are current.

### Fixed

Fixes from the 3.0 live test ([research spike](docs/pixellab/pixellab-pip-3.0-live-test-research-spike.md)).

- **Showcase GIFs loop cleanly.** A move whose cycle did not divide the fixed 4-second window was cut mid-swing and
  snapped back on every loop; the GIF now lasts until every move ends its cycle together.
- **History says when runs are hidden.** The search showed only the newest 10 runs without saying so, so an older
  run looked missing; it now reports how many older matching runs were left out.
- **Despeckle keeps one-pixel eyes and runes.** `--ref <still>` keeps lone pixels that the clean still already has.
  Without it, the default flattened dozens of real details per frame.
- **Auto palettes keep small accent colours.** `apply_palette auto` turned a knight's brown belt and straps grey; it
  now uses max-coverage quantization.
- **Parallel runs keep their own plans.** `manifest.py plan RUN -` reads the plan from stdin, so agents working at
  the same time no longer record each other's plans through a shared temp file.
- Thrown-prop attacks now make the open-hand release pose before animating, because interpolation never let go of
  the prop. Setup asks before renaming an old Game Art `pixellab.json`, even when asked to get a project ready.

## [3.0.0] - 2026-10-23

Pip 3.0 brings the production workflows of [pixellab-game-art](https://github.com/lexingel/pixellab-game-art) by
lexingel into Pip's single, agent-agnostic skill: project art styles, animation checks and repair, finishing tools,
production recipes and a review panel, all under Pip's ask-before-spending rules. What was left out, and why, is in
the [merge status](docs/tools/pixellab-game-art-skill/pixellab-game-art-pr-11-merge-status.md).

### Breaking changes

- **Image helpers need Pillow 13 or newer (Python 3.11+).** Older Pillow versions have nine published security
  advisories, so the helpers now skip instead of decoding with them. Run `pip install -r requirements-dev.txt` or
  upgrade Pillow.
- **Run manifests are now a cost ledger.** Each run folder's `manifest.json` is a `{"jobs": [...]}` record kept by
  `manifest.py`. Older manifests are kept untouched and listed separately by history; new calls go in a new run folder.
- **Coming from Game Art:** rename a project's `pixellab.json` to `pixellab-pip-style.json` (`setup` offers to do it).
  The old name is not read, and the `/pga-*` commands are replaced by plain requests to `/pixellab-pip`.
- **A broken settings file means Auto is off.** If `pixellab-pip.json` cannot be read, Pip asks before spending until
  an explicit `auto on`, `auto off` or `bark` command replaces the file.

### Added

- **Project art styles** in `pixellab-pip-style.json`: named styles, approved reference art per asset family, an
  optional fixed seed, 4 starting setups (including Game Art's side-view dark fantasy look) plus 7 untested genre word
  sets, and optional analysis of art you already have. Nothing applies unless you choose it.
- **Animation doctor** (`fix.py`): finds jumps, flicker, stray pixels, size pops and lost weapons; fixes what it can
  for free on copies; plans paid re-rolls of only the frames that failed.
- **Finishing tools**, which write copies and record what they changed: ground snap, scrub, despeckle, colour match,
  palette, recolour (by group, trail, or like another character), slash layer, blade trail, thrown prop, baked effect,
  8-direction shot finish and a muzzle finder.
- **Previews and export:** sprite sheets with Aseprite JSON or Godot `.tres` (play once or `--loop`), padding,
  preview and showcase GIFs, contact sheets, a tileset test map, and normal-map packing with a lit preview.
- **Run tools:** `fetch.py` downloads finished results, `manifest.py` keeps a locked cost record per run (charged and
  estimated kept apart), and `history.py` searches past runs for re-rolls.
- **Auto limits:** `auto plan <budget> [retries] [task]` caps one run's generations and retries; `auto status` shows
  the current setting.
- **Review panel:** `/pixellab-pip panel` opens a private, interactive review page; Claude Code also gets a native
  panel view.
- **Guides:** key-pose attacks and skills, 8-direction moves, characters, scenes and backgrounds, normal maps,
  front-facing giant bosses, 14 weapon pages, martial arts, armour and cloth, and weapon effects.
- **Blueprints:** character candidates, an overhead axe chop, a projectile skill, and strike, wave and eruption
  effects.
- **Cost helpers:** an optional 1-generation layout draft before an uncertain Pro image, and the closest alternative
  when a tool is not in your PixelLab plan.

### Changed

- Cheap mode and cinematics take retries from the run's retry allowance. A failed paid job is never retried without
  your approval or that allowance.
- Before generating, Pip checks the project root for `pixellab-pip-style.json`.
- The skill description fits the Agent Skills 1,024-character limit and keeps its trigger words; `requires_api_key`
  metadata is now a string.
- The Claude Code plugin registers the panel add-on, and CI also runs Claude Code's plugin validation.

### Security

- Pillow pinned to 13.0.0, which fixes nine advisories, including a critical JPEG decoder heap overflow.
- Downloads come only from PixelLab's own hosts, send no token, and are capped in size and checked for image bombs.
- A project file can never turn Auto on or grant spending; Auto stays in your private `pixellab-pip.json`.

Thanks to lexingel for pixellab-game-art and its adopted code (MIT; notices ship with the skill).

[3.0.0]: https://github.com/Shilo/pixellab-pip/compare/v2.3.0...v3.0.0
