# PixelLab Pip Skill Benchmark

Last measured: 2026-07-05.

This benchmark measures what the PixelLab Pip skill costs an agent and how well it routes, compared with the other ways to give an agent PixelLab knowledge:

- **`current`** — the Pip skill (this repo's working tree): `SKILL.md` injected, `references/*.md` read on demand.
- **`vanilla`** — no skill and no docs: the agent's own knowledge only.
- **`mcp-docs`** — no skill, but PixelLab's official [`api.pixellab.ai/mcp/docs`](https://api.pixellab.ai/mcp/docs) injected into the session (the [pixellab.ai/mcp](https://www.pixellab.ai/mcp) "include this link in your prompts" tip).
- **`pre-kiss-yagni-refactor`** — the Pip skill before its size refactor, for the efficiency-over-time view.

It measures the **agent session only** (context tokens, output, cost, routing correctness) — never PixelLab credits. Everything here is produced by [`dev-tools/skill_benchmark.py`](../dev-tools/skill_benchmark.py) and is reproducible; see [Reproduce](#reproduce). Routing correctness is scored by deterministic regexes (no LLM judge), so the same response always scores the same.

## Summary

On this sample, the skill routed every scenario correctly while costing about the same session context as injecting the official docs, and less than its own pre-refactor version:

| Method | Correct-routing rate | Typical session input (routing tasks) | PixelLab knowledge |
|---|---|---|---|
| **`current` (Pip skill)** | **100%** | ~13.9k tokens | Task-specific routing, cost, and safety rules |
| `mcp-docs` (official docs injected) | ~79% | ~15.3k tokens | Full MCP tool inventory, always in context |
| `vanilla` (no skill) | ~31% | ~3.0k tokens | None — guesses from training data |

"Correct-routing rate" is the mean of the deterministic per-scenario checks below. The two context strategies (skill vs official docs) are complementary, not rivals — the skill itself treats the official docs as the authoritative MCP inventory; see [Official MCP Docs vs Pip Skill](tools/pixellab-mcp-docs-vs-pip-skill.md).

## Context efficiency (static, reproducible)

Estimated context tokens (chars/4) that each method injects. Because the skill loads references **on demand**, its real per-request cost is the per-scenario row — only the reference a task needs is loaded, never the whole corpus at once. The "all references" row is the theoretical maximum if every reference loaded together, which does not happen in a single task.

| Scope | `current` | `pre-kiss-yagni-refactor` | `vanilla` | `mcp-docs` |
|---|---|---|---|---|
| Injected context (SKILL.md / MCP docs / none) | 7,227 | 10,756 | 0 | 7,745 |
| Context + all skill references (theoretical max) | 46,856 | 73,957 | 0 | 7,745 |
| route-hex-tiles (context + expected refs) | 7,227 | 10,756 | 0 | 7,745 |
| route-character | 7,227 | 10,756 | 0 | 7,745 |
| plan-item-icon-sheet | 9,192 | 16,091 | 0 | 7,745 |
| cheap-animation | 8,473 | 13,163 | 0 | 7,745 |
| report-format | 8,506 | 13,474 | 0 | 7,745 |
| setup-codex | 12,043 | 19,566 | 0 | 7,745 |
| refuse-internal-endpoint | 7,227 | 10,756 | 0 | 7,745 |
| skeleton-pipeline | 12,343 | 18,396 | 0 | 7,745 |

Per request, the skill's injected context is close to the official docs (~7.2k vs ~7.7k) and well below its own pre-refactor size. The refactor cut the base `SKILL.md` context ~33% (10,756 → 7,227).

## Routing correctness and session cost (live snapshot)

`claude`, 2 reps, medians. Correctness is `checks_rate` — the fraction of a scenario's deterministic routing checks the response passed (1.0 = fully correct).

| Scenario | Metric | `current` | `vanilla` | `mcp-docs` |
|---|---|---|---|---|
| route-hex-tiles | routing correct | **1.0** | 0.0 | 1.0 |
| route-hex-tiles | input tokens | 13,884 | 3,049 | 15,286 |
| route-character | routing correct | **1.0** | 0.5 | 0.67 |
| route-character | input tokens | 13,895 | 3,058 | 15,295 |
| cheap-animation | routing correct | **1.0** | 0.5 | 0.5 |
| cheap-animation | input tokens | 39,164 | 5,022 | 15,294 |
| refuse-internal-endpoint | routing correct | **1.0** | 0.25 | 1.0 |
| refuse-internal-endpoint | input tokens | 13,872 | 3,037 | 15,280 |

Reading this honestly:

- **`vanilla` is cheapest but least reliable.** Without PixelLab knowledge it picked the wrong tool for hex tiles (0.0), gave partial character/animation plans, and mostly failed to refuse an unsafe internal-endpoint request (0.25).
- **`mcp-docs` routes well** on tool selection because it carries the full MCP inventory, but it missed the documented *cheapest* animation route (`cheap-animation` 0.5) and part of the character pipeline (`route-character` 0.67) — task-specific cost and ordering knowledge the general docs don't specialize in.
- **`current` (the skill)** routed every scenario correctly. On simple routing it is slightly *leaner* than injecting the official docs (~13.9k vs ~15.3k input). On the harder `cheap-animation` question it deliberately reads `cost-routing.md`, spending more tokens (~39k) to return the correct documented cost — the reference load is what buys the right answer.

## Reproduce

Free, deterministic, no CLI calls or secret — this reproduces the [context efficiency](#context-efficiency-static-reproducible) table exactly:

```powershell
python dev-tools/skill_benchmark.py --static --variants pre-kiss-yagni-refactor,vanilla,mcp-docs
```

The [live snapshot](#routing-correctness-and-session-cost-live-snapshot) needs an agent CLI; numbers vary run to run:

```powershell
python dev-tools/skill_benchmark.py --agents claude --variants vanilla,mcp-docs `
  --scenarios route-hex-tiles,route-character,cheap-animation,refuse-internal-endpoint --reps 2
```

On Windows, [`dev-tools/run-skill-benchmark.ps1`](../dev-tools/run-skill-benchmark.ps1) wraps the common runs (`-Preset static`, `dry-claude`, `full`, …). Full methodology, arms, and flags are in [Developer → Skill Token Benchmark](developer.md#skill-token-benchmark).

## Method and caveats

- **Agent session only.** Tokens/cost are the agent's, not PixelLab credits.
- **Static tokens are chars/4 estimates**, not a tokenizer count; treat them as relative, not absolute.
- **The live snapshot is a dated, single-agent (`claude`), 2-rep sample.** Agent runs are nondeterministic; the static table is the reproducible part. Rerun with more agents/reps (or the `full` preset) for your own numbers.
- **Fairness controls:** each variant runs in an isolated workspace outside the repo (so no stray `CLAUDE.md`/`AGENTS.md` leaks in), variants interleave within each rep, medians are reported, and routing is scored by fixed regexes rather than a model.
- **`mcp-docs` content is fetched live** from `api.pixellab.ai/mcp/docs` at run time and saved alongside the results for audit.
