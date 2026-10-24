# PixelLab Pip Value Review Plan

Status: Deferred. Not started.

Last reviewed: 2026-10-23.

## Why

A user asked why Pip is needed when the PixelLab MCP already has rich tool docs and a
`search_help` Q&A tool. A review on 2026-10-21 found:

- The live MCP tool descriptions now include costs, "prefer v3" advice, and quality
  escalation, so much of Pip's Intent Router repeats them.
- `search_help` routed a character request well (v3, not standard), but it suggested a
  template id (`slashing`) that does not exist, and it said to animate all 8 directions
  of 3 animations with no preview and no cost check.
- Pip's real value is the workflow layer: cost approval, south-first preview, output
  folders, asset-integrity rules, destructive-action guard, secret safety,
  localization, and blueprints.
- `SKILL.md` grew to about 14,600 tokens (chars/4), about double the 7,509 measured in
  the 2026-07-06 benchmark. A simple character request loads roughly 30,000 tokens of
  rules.
- The benchmark grades Pip's own opinions, uses an unrealistic MCP baseline, and
  measures route naming only.

## To Do

- [ ] Trim `SKILL.md`: remove facts the live MCP schemas already state (size caps,
      costs, UI aspect caps, Pixen transparency area). Keep only decisions the schemas
      do not make, and point the agent to the live schema for limits and costs.
- [ ] Keep the `create_character` mode rule: the schema default is still `standard`.
      Reword "standard is legacy" — PixelLab does not call it that.
- [ ] Consider making the blueprint and the completion sound opt-in instead of running
      after every generation.
- [ ] Benchmark: add an "MCP + `search_help` + live tool schemas" arm.
- [ ] Benchmark: fix rubrics that only accept REST route names or Pip-only opinions
      (for example `route-background-scene` requires `pixflux-background`).
- [ ] Benchmark: re-run against the current `SKILL.md` and update the summary.
- [ ] Run 3–5 live generation tasks with and without Pip. Compare credits spent,
      retries, and outputs kept. Include one cheap model to test the "cheaper model,
      similar results" claim.
- [ ] Update the README pitch: lead with cost approval, preview-before-spend, organized
      outputs, and multi-step workflows instead of "better routing".
