# Game Art merge (PR #11): what came over, what didn't, and what to revisit

Last reviewed: 2026-10-23, on `feat/pga-merge` against pixellab-game-art v1.4.3 (`claude-code/` and `any-agent/`).
Two independent reviews were challenged against the code until both sides agreed on every point below.

This page is the current summary. The history behind it lives in the
[merge position](pixellab-game-art-pip-merge-position-by-lexingel.md),
[research spike](pixellab-game-art-pip-merge-research-spike.md),
[first PR #11 review](pixellab-game-art-pr-11-review.md),
[remediation plan](pixellab-game-art-pr-11-implementation-plan.md),
[review response](pixellab-game-art-claude-review-response.md) and
[panel/Auto decision](pixellab-game-art-panel-auto-reconsideration.md).

Part of the PR comes from the contributor's unpublished Game Art 1.5.0, so it cannot be checked against the public
v1.4.3 repo. Those parts are marked "new" below.

## Brought over from Game Art

| Game Art feature | Where it lives in Pip | How it changed |
|---|---|---|
| Finishing scripts: ground snap, scrub, colour match, apply palette, recolour trail, recolour like, slash layer, 8-direction finish, find muzzle | `skills/pixellab-pip/assets/finish/`, guide `references/finishing.md` | Rewritten. Each needs `--out`, writes copies only, records a `derivative.json`, refuses to overwrite, and needs Pillow 13. Frames are named `0.png` onward as before. |
| Preview and export: sprite sheets (Aseprite JSON, Godot `.tres`), padding, preview GIF, contact sheet, tileset test map, normal-map packing | `skills/pixellab-pip/assets/`, guides `local-asset-assembly.md`, `tileset.md`, `normal-maps.md` | Simplified: the house rhythm presets (`--beat`, `--step`) and the GIF effect overlay are gone. |
| Download helper | `assets/fetch.py`, `references/job-lifecycle.md` | Only downloads links PixelLab returned, from PixelLab's own hosts, with a 32 MiB cap, image-bomb checks, cleanup after a failed write, and no overwriting. The built-in download URL, batch and tileset modes and the "failed = refunded, resubmit" rule were dropped. |
| History and outcomes | `assets/history.py`, `assets/manifest.py`, `references/usage-reporting.md` | Reads the new per-run ledger instead of `log.jsonl`. Older manifests are listed after the runs and never hide them. |
| Project styles, named styles, family anchors | `assets/project_style.py`, `references/project-style.md`, `style-examples.md` | Nothing is saved or applied without the user choosing it. Style inheritance merges nested settings. Old `max_cost`/`ask_above` stay as restrictions. |
| Style analysis | `assets/analyze_style.py` | Advice only; never writes rules into the profile. |
| Asset know-how (characters, backgrounds, scenes, buildings, icons, tiles) | `characters.md`, `scenes-and-backgrounds.md`, `icon.md`, `tileset.md` | Condensed; premium-model defaults are now offers. |
| Key-pose attack animation | `key-pose-animation.md`, `animation.md` | Opt-in recipe; ordinary attacks use Pip's normal routes. |
| 8 directions | `eight-direction.md` | Faithful; mirroring is offered, not automatic. |
| VFX templates (strike, wave, eruption) | `blueprints/vfx-*.blueprint.json`, `vfx-workbench.md` | Same recipes as replayable blueprints. |
| "Draft first" before an expensive Pro image | `create-image-pro.md` | An offer in the approval card, never a default. |
| Tools that need a higher PixelLab plan, and their fallbacks | `job-lifecycle.md` (REST Error Handling) | Fallbacks only; the tier numbers and job limits were left out because they go stale. |
| The 21 `/pga-*` commands | Plain requests through `/pixellab-pip`; mapping in `docs/merge/README.md` | Batch runs became the mixed-batch rule in `auto.md`; rerolls became the historical-reroll rule in `usage-reporting.md`. |

## Left out on purpose

| Game Art feature | Why it stays out |
|---|---|
| "Never ask permission" mode | It would bypass Pip's cost approval and spend credits unasked. `auto on` and `auto plan <budget> [retries]` give the same "don't nag me" within limits the user sets. |
| Feedback and telemetry (`share.py`, `/pga-feedback`) | Sends usage data to a third party; Pip makes no hidden network calls. |
| Self-updater and installer (`update.py`, `install.py`, `/pga-update`) | Pip has its own setup and update; editing installed skill files clashes with plugin installs. |
| Per-task model picker (`models.json`) | Claude-only; Pip is agent-agnostic. |
| Fixed dark-fantasy house look and seed 7 | Forces a look the user did not choose. Pip lets the user pick a style; its seed rule covers consistency. |
| "A failed job means a refund, resubmit" | Wrong and risky: a failure is not proof of a refund, and resubmitting can charge twice. |
| Measured price tables (`costs.md`) | Prices change. Pip uses its own cost notes plus PixelLab's live estimates. |
| Demo images | No art licence was supplied; they were removed and must not reach `main` (see Merge). |

Already covered by Pip on `main`: the setup check (`setup.md`), the tool table (Pip's router), prompt improvement
(its useful rules are in `characters.md`), and quality checks (`inspect_images.py` plus the new animation doctor).

## Lost, and when to revisit

These are not in the PR. Re-add one only when the trigger in the last column happens, and through Pip's normal rules
(one canonical place, smallest change, no new defaults).

| Missing feature | What it did | Revisit when |
|---|---|---|
| Spend per command and per day (`cost_report.py`) | Totals across runs by command and date | Users ask for spend reports beyond per-run totals; extend `history.py`, don't add a second ledger. |
| Reading old Game Art `log.jsonl` history | History from before the merge | A migrating user needs old Game Art history in Pip; a one-off read-only importer would do. |
| Plan levels and concurrency table | Jobs allowed at once per plan | PixelLab documents these numbers officially; they currently come only from its help agent. |
| 6 of the 10 genre presets | Untested word lists (cyberpunk, western, horror...) | A preset is tested like the 4 kept examples; add it to `style-examples.md` and `project_style.py` together. |
| Usage stats and "why" notes (`stats.md`, `rationale.md`) | Background for `/pga-tech` | Never at runtime; copy into `docs/` if the history is wanted. |
| Giant front-facing boss tips | Waist-up bosses, naming sides by the image, 11 frames in 256 px, on-screen scale | Bosses become a common request; about 5 lines in `key-pose-animation.md`. |
| Most verbatim example prompts | Full prompts per asset type | A reference page shows an agent picking worse wording without them. |
| `--draft` / `--n` / `--size` options | Command flags | Not needed: plain requests, candidate batches and the draft offer cover them. |

## New in the PR (not from Game Art v1.4.3)

- Animation doctor: `fix.py`, `fixlib/`, `animation-doctor.md`. Its thresholds were tuned on the contributor's own
  animations, which were not supplied, so they cannot be re-checked.
- More finishing tools: despeckle, recolour groups, throw prop, bake effect, blade trail; plus `showcase_gif.py`.
- 15 `weapon-*.md` pages, `martial-arts.md`, `armor-clothing.md`. Four (anime, firearms, futuristic, whip) have no
  listed sources; see `docs/pixellab/weapon-page-sources.md`.
- Blueprints: `character-candidates`, `overhead-axe-chop`, `projectile-skill`.
- A locked cost ledger per run (`manifest.py`), `auto plan` and `auto status`.
- The review panel (`panel.py`, `panel.html`, `panel.md`) and a Claude Code adapter (`hooks/claude/`).

## What changes for an existing Pip user

- A `pixellab.json` in the project root is read before generating.
- Image helpers, including the two that already existed, need Pillow 13 (Python 3.11+); older Pillow has nine known
  security advisories, so they skip instead.
- New commands: `panel`, `auto status`, `auto plan`.
- Cheap mode and cinematics take retries from a run's retry allowance.
- Run manifests are now a `{"jobs": [...]}` ledger; older manifests are kept and listed separately.
- Claude Code users get a panel tool at every session start.
- A broken settings file means Auto is off (ask first); an explicit `auto`/`bark` command replaces it.

## Open decisions

| Topic | Question |
|---|---|
| Claude Code panel adapter | Keep it? It registers a tool every session; loading on Claude Code versions older than the CI-pinned one is untested. |
| Codex "send" button in the panel | Keep it? It rests only on the contributor's note about the host's renderer. |
| Size | `auto.md` and the panel add complexity; informational, not a defect. |
| Routing benchmark | Re-run `python dev-tools/skill_benchmark.py --agents claude --variants current`? It spends no PixelLab credits but uses Claude usage. Four newer scenarios have never run. |
| Release notes | Call out the Pillow 13 requirement, the new commands and the panel tool in the next release. |

## Merge

- Squash-merge with a `Co-authored-by` credit for lexingel. A merge commit would bring the removed unlicensed demo
  images, the abandoned prototype "Studio" edition and personal commit emails into `main`'s history.
- No version bump in the PR; versions change only in the separate release commit.
