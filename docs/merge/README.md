# Merge prototype: Pip × Game Art

This branch (`feat/pga-merge`) is a working prototype of PixelLab Pip merged with
pixellab-game-art, made to be tried before either maintainer decides anything.

## What it is

- **Pip, improved.** Game Art's host-neutral strengths move into Pip's one core skill, in Pip's voice and
  under Pip's rules: an animation doctor, project styles the user always chooses, a key-pose animation
  recipe, finishing helpers that write labelled copies, a poll-and-download helper, and motion references
  (weapons, martial arts, armour, effects). Every Pip host gets them.
- **A Claude edition on top.** A Claude Code plugin in `editions/claude/` that loads the same core and adds
  short `/pga-*` commands, a PixelLab connection set up on install, and a side panel: welcome page, style
  menu, pose review with Approve / Redo, finished moves, and a live activity strip.

## Shared rules

- Three approval levels: **Ask** (each paid job; the core default), **Plan** (one approval per plan, a pause
  at pose review; the Claude edition's default) and **Auto** (a budget and a retry cap).
- Raw PixelLab outputs are never changed; every local fix is a labelled derivative and is reported.
- One record per run: the blueprint plus `manifest.json`.
- The art style is always the user's choice; named example styles are offered, never applied silently.

## Credit

PixelLab Pip by Shilo; pixellab-game-art by lexingel. MIT, as both projects.
