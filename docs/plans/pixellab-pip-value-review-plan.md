# PixelLab Pip Value Review Plan

Status: Deferred. Not started.

Last reviewed: 2026-10-23.

This plan is self-contained. An agent picking it up should read this file, then
`AGENTS.md` (project rules), then the files named in each task. No earlier conversation
is needed.

## Background

PixelLab Pip (`skills/pixellab-pip/`) is an agent skill that tells coding agents how to
use PixelLab: which MCP tool or REST v2 endpoint to pick, how to write prompts, when to
ask for cost approval, and how to save outputs.

A PixelLab user challenged its purpose: the hosted PixelLab MCP already ships detailed
tool descriptions and a `search_help` tool (a knowledge agent that answers questions
from PixelLab's own docs). Why not just use those, plus a short instruction?

A review on 2026-10-21 compared the skill against the live MCP tool descriptions and
tested `search_help`. The goal of this plan is to act on what it found: make the skill
smaller, make the benchmark honest, and sharpen the pitch.

## Review Findings

### Where the challenge is right

- **The MCP tool descriptions are no longer bare technical docs.** They now include cost
  tables, "prefer v3" advice, a quality-escalation order for `animate_character`, and
  warnings such as "a non-front-facing reference shifts all 8 directions". Much of
  `SKILL.md`'s Intent Router repeats them.
- **`search_help` routes simple requests well.** Asked for a 64px top-down knight with
  walk, idle, and attack in 8 directions, it chose `create_character(mode="v3")`, explained
  that `standard` is cheaper but lower quality, and estimated about 26 generations.
- **"Standard is legacy" is Pip's opinion, not PixelLab's.** PixelLab's description says
  "Standard mode (default)". The real risk is narrower: `standard` is still the schema
  default, so an agent calling `create_character(description=...)` with no `mode` gets it.
  See `SKILL.md`, Model And Mode Terms, the `standard` bullet.

### Where Pip adds real value

- **`search_help` invented a template.** In the same answer it suggested
  `template_animation_id="slashing"`, which is not in the humanoid template list in the
  `animate_character` schema. That call would fail or waste a turn.
- **`search_help` gave no preview or cost step.** It said to animate all 8 directions of
  3 animations at once (about 24 generations). Pip animates `south` first and asks before
  doing all directions.
- **The workflow layer is not in the MCP docs**, and a short instruction would not
  recreate it:
  - one cost-approval message listing every paid call and its prompt
    (`references/auto.md`)
  - organized output folders and preview GIFs/spritesheets
  - asset-integrity rules (no local drawing, no fake transparency)
  - permission before deleting or overwriting remote assets
  - bearer-token safety
  - English prompt translation with approval (`references/localization.md`)
  - replayable blueprints (`references/blueprint.md`)

### Problems with Pip

1. **Size.** `SKILL.md` is about 15,600 tokens (chars/4) as of 2026-10-23. The 2026-07-06
   benchmark measured 7,509. A plain "make a character with a walk animation" request also
   loads `auto.md`, `usage-reporting.md`, `blueprint.md`, `bark.md`, `job-lifecycle.md`,
   and `preset-skeleton-template-animation.md`, which add about 21,900 more. That is
   roughly 37,500 tokens of rules for one simple request. This conflicts with
   `AGENTS.md`'s "lean router" rule for `SKILL.md`.
2. **The "cheap models get similar results" claim is untested.** Small models tend to do
   worse with very long, dense rule sets, not better.
3. **It repeats facts the live schemas already state:** size caps, costs, the
   `create_ui_asset` aspect-ratio caps, the Pixen transparency area limit, and similar.
   PixelLab updates often, so each copied fact can go stale.
4. **Pip costs more in some places.** It defaults to v3 (2–9 generations) over standard
   (1), and it adds agent tokens on every request. That is a fair trade for quality and
   visibility, but the pitch should say so.
5. **Mandatory side effects.** After every generation the skill plays a sound, writes a
   manifest, and writes a `*.blueprint.json` (`SKILL.md` Workflow step 12). Some users
   will see these as noise.

### Problems with the benchmark

The benchmark is `dev-tools/skill_benchmark.py`; the published results are
`docs/pixellab-pip-benchmark.md` (last generated 2026-07-06: Pip 98%, MCP Docs 58%,
Vanilla 24%).

- **Rubrics grade Pip's own opinions.** Scenarios are in the `SCENARIOS` list, each with
  regex `checks`. Examples:
  - `route-background-scene` passes only if the answer names `pixflux-background`, a
    REST route name. An agent using MCP docs cannot name it, so it scores 0%.
  - `plan-item-icon-sheet`, `route-skill-icons`, and `route-tiles-vs-tileset` pass only
    for Create Image Pro.
- **The MCP Docs arm is not realistic.** It pastes `https://api.pixellab.ai/mcp/docs`
  into a dry-run prompt. Real MCP users also have the live tool schemas in context and
  can call `search_help`.
- **It measures only whether the route was named correctly.** It does not measure image
  quality, credits spent, retries, or whether the user kept the result.
- **It is stale.** It ran against a `SKILL.md` about half the current size.

## Rules For This Work

- Follow `AGENTS.md`: KISS/YAGNI for runtime content, keep each rule in one place, and
  remove replaced text in the same change. `docs/` is exempt from the KISS rules.
- Never weaken routing accuracy, the public-vs-private endpoint boundary, secret safety,
  paid-credit control, or output integrity. Simplify by consolidating, not by deleting
  protections.
- Live MCP descriptions change. Before removing a fact from `SKILL.md` because "the
  schema already says it", confirm it in the live tool description (connected PixelLab
  MCP tools, or `https://api.pixellab.ai/mcp/docs`). Before relying on a REST fact,
  check `https://api.pixellab.ai/v2/openapi.json`.
- Live generation spends the user's PixelLab credits. Get the user's approval and a
  budget before task 7.
- Validate every edit with `python dev-tools/qa.py` (exit code 0). Use conventional
  commits.

## To Do

### 1. Trim `SKILL.md` to decisions the schemas don't make

- [ ] For each Intent Router row and Model And Mode Terms bullet, keep it only if it adds
      a decision, action, safety boundary, or verification step that the live tool
      schema does not. Remove copied limits and costs, and add one pointer telling the
      agent to read the live schema for limits and costs.
- [ ] Keep every safety and credit-control rule (Asset Integrity, Destructive Remote
      Actions, Auth And Execution, the cost gate).
- [ ] Measure the size before and after:
      `python -c "print(len(open('skills/pixellab-pip/SKILL.md',encoding='utf-8').read())//4)"`.
      Done when the size is clearly below the current ~15,600, no rule was lost, and QA
      passes.

### 2. Fix the `standard` mode wording

- [ ] In `SKILL.md` Model And Mode Terms, keep the routing rule (always pass
      `mode="v3"` by default; don't recommend `standard`). Replace "deprecated" with the
      real reason: it is the schema default and lower quality.

### 3. Decide whether per-generation side effects stay on by default

- [ ] Review `SKILL.md` Workflow step 12, `references/bark.md`, and
      `references/blueprint.md`. Propose to the user which of sound, manifest, and
      blueprint should become opt-in. Don't change defaults without their approval.

### 4. Benchmark: add a realistic MCP arm

- [ ] In `dev-tools/skill_benchmark.py`, add an arm with the live MCP tool schemas in
      context and `search_help` described as available. Keep the existing `mcp-docs` arm
      for comparison.

### 5. Benchmark: fix opinion-only rubrics

- [ ] Change rubrics so that every reasonable correct route passes, including the MCP
      tool name for the same route. Start with `route-background-scene`
      (`create_image_pixflux` should pass), then review `plan-item-icon-sheet`,
      `route-skill-icons`, and `route-tiles-vs-tileset`.
- [ ] Keep a strict check only where the alternative is actually wrong (for example, an
      internal endpoint or a tool that doesn't exist).

### 6. Benchmark: re-run and publish

- [ ] Run the static context-size table (no agent CLI or credits needed):
      `python dev-tools/skill_benchmark.py --static --variants pre-kiss-yagni-refactor,mcp-docs,vanilla`.
- [ ] Run the full routing set with `--report docs/pixellab-pip-benchmark.md`, or the
      `full` preset in `dev-tools/run-skill-benchmark.ps1`. It is a dry run with no
      credits, but expect about 2 hours per rep. See the Reproduce section of
      `docs/pixellab-pip-benchmark.md`.

### 7. Live outcome test (needs user approval and a budget)

- [ ] Pick 3–5 common tasks (for example: a character with walk and idle, an item icon
      sheet, a top-down tileset, a background). Run each with and without Pip, and
      record:
      - credits spent (`get_balance` before and after)
      - retries
      - whether the output met the request
- [ ] Include one cheap model to test the "cheap model, similar results" claim.
- [ ] Write the results to `docs/` and link them from `docs/pixellab-pip-benchmark.md`.

### 8. Update the README pitch

- [ ] In `README.md` (Features section), lead with what the MCP docs don't do: cost
      approval before spending, preview before animating every direction, organized
      outputs, and multi-step workflows (characters with states and animations,
      tilesets, cinematics, paperdolls, blueprints). Treat routing as a supporting point.
- [ ] Be honest that for a strong model doing a quick one-off asset, MCP plus
      `search_help` may be enough.
