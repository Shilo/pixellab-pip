# Skill File Sizing

Last reviewed: 2026-07-24.

Recommended lengths for `skills/pixellab-pip/SKILL.md` and every `references/*.md`, the
authorities behind them, current measurements, and what to do when a file is over. This is a
maintainer guide — it does not gate CI (`dev-tools/qa.py` checks reference *existence*, not
size), so treat the thresholds as review signals, not hard failures.

## Table of Contents

- [Why size matters here](#why-size-matters-here)
- [The recommended limits](#the-recommended-limits)
- [Current measurements](#current-measurements)
- [Per-file verdicts and actions](#per-file-verdicts-and-actions)
- [When a file is over](#when-a-file-is-over)
- [How to re-measure](#how-to-re-measure)
- [Sources](#sources)

## Why size matters here

Agent Skills load in three tiers ([Agent Skills specification](https://agentskills.io/specification)):

1. **Metadata** (~100 tokens) — `name` + `description`, injected for every skill at startup.
2. **Instructions** (`SKILL.md` body) — loaded when the skill activates.
3. **Resources** (`references/*.md`) — loaded individually, only when SKILL.md points to them.

Two different costs follow from this, and they set two different budgets:

- **SKILL.md is paid on every activation** and then competes with conversation history for
  the rest of the session. Smaller is cheaper *and* less prone to being diluted or dropped
  during context compaction. This is the file with a real token budget.
- **A reference is paid only when read**, so raw length is cheap. The risk there is not token
  cost but **partial reads**: agents preview long files with `head`-style partial reads, and
  Anthropic warns this yields incomplete information unless the file starts with a table of
  contents. So the reference budget is about *readability under a partial read*, not tokens.

Token figures below are approximate (`chars / 4`), which is close enough for English Markdown
to judge against the thresholds. Use them as ratios, not exact counts.

## The recommended limits

| File | Lines | Tokens | Extra rules |
|---|---|---|---|
| `SKILL.md` body | **< 500** | **< 5000** | Keep it a router that points to references; move detail out. |
| `description` frontmatter | — | ~part of the ~100-token metadata tier | **≤ 1024 chars** (spec hard limit). |
| Each `references/*.md` | no hard cap; **keep focused** | no hard cap | **One level deep** from SKILL.md; **table of contents if > 100 lines**. |

Line and token limits are Anthropic's authoring guidance for the instructions tier; the
one-level-deep and 100-line-TOC rules are from the same best-practices guide (see
[Sources](#sources)). The 1024-char `description` cap is a normative limit in the open spec.

## Current measurements

Measured 2026-07-24. Re-run the command in [How to re-measure](#how-to-re-measure) after edits.

### SKILL.md

| File | Lines | Chars | ~Tokens | Line budget | Token budget |
|---|---|---|---|---|---|
| `SKILL.md` | 242 | 39,086 | ~9,771 | ✅ < 500 | ⚠️ ~2× over 5000 |

### references/ (sorted largest first)

| File | Lines | Chars | ~Tokens | > 100 lines → TOC? |
|---|---|---|---|---|
| `preset-skeleton-template-animation.md` | 453 | 21,233 | ~5,308 | ⚠️ needs TOC |
| `aseprite-cli.md` | 363 | 27,850 | ~6,962 | ⚠️ needs TOC |
| `blueprint.md` | 356 | 19,252 | ~4,813 | ⚠️ needs TOC |
| `setup.md` | 131 | 18,268 | ~4,567 | ⚠️ needs TOC |
| `bark.md` | 105 | 5,749 | ~1,437 | ⚠️ borderline (just over) |
| `tileset.md` | 98 | 11,685 | ~2,921 | ✅ |
| `paperdolling.md` | 86 | 10,804 | ~2,701 | ✅ |
| `icon.md` | 84 | 9,095 | ~2,273 | ✅ |
| `auto.md` | 82 | 6,874 | ~1,718 | ✅ |
| `animation.md` | 74 | 8,479 | ~2,119 | ✅ |
| `local-asset-assembly.md` | 71 | 4,630 | ~1,157 | ✅ |
| `uninstall.md` | 68 | 6,117 | ~1,529 | ✅ |
| `image-input-roles.md` | 68 | 7,962 | ~1,990 | ✅ |
| `update.md` | 66 | 4,292 | ~1,073 | ✅ |
| `job-lifecycle.md` | 64 | 5,929 | ~1,482 | ✅ |
| `usage-reporting.md` | 62 | 5,397 | ~1,349 | ✅ |
| `reviewable-candidates.md` | 61 | 3,319 | ~829 | ✅ |
| `create-image-pro.md` | 60 | 7,521 | ~1,880 | ✅ |
| `cinematic.md` | 55 | 19,765 | ~4,941 | ✅ lines; dense — watch |
| `background-removal.md` | 54 | 4,378 | ~1,094 | ✅ |
| `style-reference.md` | 48 | 3,557 | ~889 | ✅ |
| `credentials.md` | 47 | 6,797 | ~1,699 | ✅ |
| `prompt-limits.md` | 40 | 2,717 | ~679 | ✅ |
| `cost-routing.md` | 39 | 4,992 | ~1,248 | ✅ |
| `official-pixellab-documentation.md` | 38 | 5,358 | ~1,339 | ✅ |
| `localization.md` | 21 | 2,789 | ~697 | ✅ |
| `mcp-platform-tools.md` | 19 | 2,171 | ~542 | ✅ |
| `aseprite-mcp.md` | 17 | 1,860 | ~465 | ✅ |
| `editor-only-utilities.md` | 14 | 2,251 | ~562 | ✅ |

## Per-file verdicts and actions

**SKILL.md — over on tokens (~9.8k vs 5k), fine on lines. Do not split; leave it.** The
overage is a router doing its job: the Intent Router table and Surface Rules are load-bearing
classification, not filler, and this is the one file whose content can't be pushed to
references without weakening the thing that decides *which* reference to read. If tokens ever
need to come down, the lazy lever is prose density (e.g. Workflow step 12, the Model/Mode and
Do-Not-Use restatements), done as a separate evidence-driven pass — not as a split.

**The four references over 100 lines** (`preset-skeleton-template-animation.md`,
`aseprite-cli.md`, `blueprint.md`, `setup.md`) — **add a table of contents, do not split.**
Splitting a reference into sub-references creates the deeply-nested chain the best-practices
guide warns against (SKILL → A → B), which is worse for an agent than one long file, and on
path-resolution-fragile clients (see the Antigravity note below) it multiplies the cold
lookups. A TOC is the sanctioned fix: it makes a partial `head` read still reveal the file's
full scope. `bark.md` (105) is marginally over — a short TOC is optional.

**`cinematic.md`** — only 55 lines but ~4,941 tokens (very long lines). Under every rule, but
it is the densest reference per line; if it grows, treat it like the >100-line group.

**Everything else** — within budget. No action.

### Antigravity note

These sizes interact with a separate, confirmed problem: Antigravity's `view_file` needs an
absolute path and its system prompt may not tell the agent where the skill lives, so
references sometimes go unread entirely. That is a *discovery* failure, addressed by the
path-resolution anchor in SKILL.md's `## References` intro — not a sizing failure. Sizing (the
TOC guidance above) only helps once the file is actually opened, by protecting against
*partial* reads of the long ones. Fix discovery first, then size; do not conflate them.

## When a file is over

- **SKILL.md over token budget** → trim prose density; never split the router. Re-measure.
- **Reference over 100 lines** → add a `## Table of Contents` (or `## Contents`) listing every
  `##` section, near the top. Keep the file whole.
- **Reference genuinely covers two unrelated domains** and each is usually needed alone → a
  domain split *is* justified (the BigQuery `reference/finance.md` vs `reference/sales.md`
  pattern). Rare here; most Pip references are one cohesive contract. If you do split, keep
  every new file linked directly from SKILL.md so nothing sits more than one level deep.
- **description over 1024 chars** → hard spec violation; tighten it. This is the only size rule
  worth enforcing strictly, because it is normative.

## How to re-measure

From the repo root:

```bash
cd skills/pixellab-pip
for f in SKILL.md references/*.md; do
  lines=$(wc -l < "$f"); chars=$(wc -c < "$f")
  printf "%-52s %5s lines %8s chars ~%6s tok\n" "$f" "$lines" "$chars" "$((chars/4))"
done | sort -k5 -n
```

PowerShell:

```powershell
Get-ChildItem SKILL.md, references/*.md | ForEach-Object {
  $c = (Get-Content $_ -Raw).Length
  [pscustomobject]@{ File=$_.Name; Lines=(Get-Content $_).Count; Chars=$c; Tokens=[int]($c/4) }
} | Sort-Object Tokens
```

## Sources

- [Agent Skills — Specification](https://agentskills.io/specification) — three tiers,
  `references/` layout, "use relative paths … one level deep," 1024-char `description` limit.
- [Anthropic — Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  — "Keep SKILL.md body under 500 lines," "< 5000 tokens recommended," "Avoid deeply nested
  references," "Structure longer reference files with table of contents" (files > 100 lines),
  forward-slash paths only.
- [Claude Code — Skills](https://code.claude.com/docs/en/skills) — reference supporting files
  from SKILL.md so the agent knows when to load them.
