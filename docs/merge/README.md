# Merge prototype: Pip × Game Art

This branch (`feat/pga-merge`) is a working prototype of PixelLab Pip merged with
pixellab-game-art, made to be tried before either maintainer decides anything.

## What it is

- **Pip, improved.** Game Art's host-neutral strengths move into Pip's one core skill, in Pip's voice and
  under Pip's rules: an animation doctor, project styles the user always chooses, a key-pose animation
  recipe, finishing helpers that write labelled copies, a poll-and-download helper, and motion references
  (weapons, martial arts, armour, effects). Every Pip host gets them.
- **A Claude edition on top.** A Claude Code plugin in `editions/claude/` that loads the same core and adds
  a PixelLab connection set up on install and a side panel: welcome page, style menu, pose review with
  Approve / Redo, finished moves, and a live activity strip. It adds no task commands: requests go through
  `/pixellab-pip` as on every host.

## Shared rules

- Three approval levels: **Ask** (each paid job; the core default), **Plan** (one approval per plan, a pause
  at pose review; the Claude edition's default) and **Auto** (a budget and a retry cap).
- Raw PixelLab outputs are never changed; every local fix is a labelled derivative and is reported.
- One record per run: the blueprint plus `manifest.json`.
- The art style is always the user's choice; named example styles are offered, never applied silently.

## From pixellab-game-art's commands

pixellab-game-art had one slash command per task. Here there is one entry, `/pixellab-pip`: describe the task and
`SKILL.md` routes it. Only settings keep a short word after it.

| pixellab-game-art | Here |
|---|---|
| `/pga-char`, `/pga-anim`, `/pga-vfx`, `/pga-bg`, `/pga-scene`, `/pga-building`, `/pga-icon`, `/pga-tiles`, `/pga-normal`, `/pga-batch` | ask for it: "make a red-haired archer", "animate hero.png doing an overhead axe chop" |
| `/pga-fix`, `/pga-reroll` | "check these frames and fix what you can", "re-roll plan 2 in fix_report.json" |
| `/pga-style`, `/pga-init`, `/pga-analyze` | "set up a style for this project", "match the style of this art" |
| `/pga-prompt`, `/pga-history`, `/pga-start`, `/pga-help`, `/pga-tech` | ask: "improve this prompt", "what have I spent this month", "walk me through a first project" |
| `/pga-level plan 45 2` | `/pixellab-pip level plan 45 2` |
| `/pga-doctor` (setup check), `/pga-update` | `/pixellab-pip setup`, `/pixellab-pip update` |
| `/pga-feedback` | not carried over (it shared results with pixellab-game-art's own server) |
| `/pga-panel`, `/pga-setup` (Claude edition) | the panel opens on the first PixelLab call; `/pixellab-pip-panel` reopens it |

## Credit

PixelLab Pip by Shilo; pixellab-game-art by lexingel. MIT, as both projects.
