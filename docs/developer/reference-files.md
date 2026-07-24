# Reference Files

Last reviewed: 2026-07-24.

How Pip's progressive-discovery reference system is meant to work, the rules every
`references/*.md` file must follow, the cross-client resolution caveat that makes those rules
load-bearing, and every external source behind them. For per-file length/token budgets, see
[Skill File Sizing](skill-file-sizing.md); this guide is about *structure and references*, not
size.

## Table of Contents

- [The progressive-discovery model](#the-progressive-discovery-model)
- [Rules for reference files](#rules-for-reference-files)
- [How relative paths resolve (and why it breaks)](#how-relative-paths-resolve-and-why-it-breaks)
- [What SKILL.md does about it](#what-skillmd-does-about-it)
- [Checklist before adding or editing a reference](#checklist-before-adding-or-editing-a-reference)
- [External sources](#external-sources)

## The progressive-discovery model

Agent Skills load in three tiers. Pip is built around this:

1. **Metadata** (~100 tokens) — the `name` + `description` in SKILL.md frontmatter, injected
   for every installed skill at session start. This is the only thing an agent sees before it
   decides Pip is relevant.
2. **Instructions** — the SKILL.md body, loaded when the skill activates. In Pip this is the
   router: intent classification, surface rules, the Intent Router table, and the References
   index. It should point to detail, not contain it.
3. **Resources** — the `references/*.md` files, each loaded individually only when SKILL.md
   routes the agent to it. A reference is paid for in tokens only when actually read, so the
   folder can hold far more than any one job needs.

The design goal: a request for one asset type pulls in only the one or two references that
job needs, never all 29. SKILL.md's `## References` section is the authoritative index of what
each file covers — keep it accurate, because it is what an agent reads to decide what to load.

## Rules for reference files

These are the durable authoring rules. Sources for each are in
[External sources](#external-sources).

- **One level deep from SKILL.md.** Every reference must be linked directly from SKILL.md
  (Intent Router or the References index). Anthropic's guidance: *"Keep references one level
  deep from SKILL.md. All reference files should link directly from SKILL.md."* A file
  reachable *only* through another reference risks a partial `head`-style read and incomplete
  loading. Reference→reference cross-links are fine **as long as** the target is also linked
  from SKILL.md — then the link is a lateral shortcut, not a dependency chain. Pip currently
  satisfies this: all 29 references are linked from SKILL.md, and every cross-link target is
  one of those 29.
- **Table of contents if over 100 lines.** Long files get previewed with partial reads; a TOC
  at the top makes the file's full scope visible even from a partial read. See the sizing doc
  for which files currently need one.
- **Relative paths, forward slashes.** Reference other files with paths relative to the skill
  root (`references/icon.md` from SKILL.md, or a bare `usage-reporting.md` sibling link from
  inside another reference). Never absolute paths, never backslashes — `reference/guide.md`,
  not `reference\guide.md` — because backslashes break on non-Windows agents.
- **One canonical home per rule.** A runtime rule lives in exactly one place: SKILL.md if it
  is global, or one reference if it is task-specific. Elsewhere, point to it. Never restate a
  SKILL.md global inside a reference — SKILL.md is always co-loaded. (This is an AGENTS.md
  project rule, reinforced here because references are where duplication tends to creep in.)
- **Keep each reference focused.** One cohesive contract per file. Split into two references
  only when the content covers genuinely independent domains that are usually needed
  separately — rare in Pip, where most references are a single workflow's contract. If you do
  split, link both halves directly from SKILL.md so neither drops below one level deep.
- **Don't restate the model's general knowledge.** A reference should carry only what changes
  an agent's decision, action, safety boundary, or verification step. Background, evidence, and
  rationale belong in `docs/`, not in a runtime reference.

## How relative paths resolve (and why it breaks)

There is no path resolver in the Agent Skills format. When SKILL.md says read
`references/auto.md`, the agent must join that relative path against the skill's install
directory itself — and it can only do that if the client told it where the skill lives. The
open standard puts that duty on the **client**
([client-implementation guide](https://agentskills.io/client-implementation/adding-skills-support)):
store the skill's absolute `location`, and either list it in the skill catalog or emit a
`Skill directory: /path/…` line, with the recommended instruction *"When a skill references
relative paths, resolve them against the skill's directory (the parent of SKILL.md) and use
absolute paths in tool calls."*

Not every client honors this, so the same relative reference behaves differently across
agents:

- **Claude Code** resolves relative paths against the process working directory (the user's
  repo), not the skill directory — so a bare `references/x.md` can miss unless the agent
  reconstructs the absolute path from the catalog. (`anthropics/claude-code#56325`.)
- **Claude.ai** rejects relative paths outright: *"not an absolute path."* (`anthropics/skills#1153`.)
- **Kiro** strips the skill directory on injection, so the agent searches the workspace root
  and finds nothing. (`kirodotdev/Kiro#6955`.)
- **Antigravity** requires an absolute path for `view_file` but its system prompt may omit the
  skill directory entirely, so the agent holds a relative string it cannot pass to its only
  file tool — and sometimes silently skips the read. (Forum bug: *missing path in system
  prompt*.) This is the failure that prompted Pip's fix.

Relative paths remain the correct authoring choice — absolute paths are unknowable at authoring
time, and the spec mandates relative. The gap is client-side, not ours.

## What SKILL.md does about it

Because clients under-deliver the resolution contract, Pip supplies it from inside the skill
body. The `## References` intro in SKILL.md carries a vendor-neutral anchor (the first sentence
is the open standard's own recommended wording):

- Resolve every `references/` path against the skill's own directory (the parent of SKILL.md)
  and use an absolute path in the tool call.
- If that directory is unknown, locate the `pixellab-pip/references/` folder by listing or
  searching the workspace and agent-skill directories before acting.
- Act from the reference's current text, never from memory, a summary, or an earlier session.
- If a required reference cannot be read, say so and stop — turning a silent skip into a
  visible failure.

It also names the four references every live job must read (`auto.md` before the first paid
call, then `bark.md`, `usage-reporting.md`, `blueprint.md` once images return), because those
"always" obligations are the ones an agent most often reconstructs from a decayed memory
instead of reading fresh.

## Checklist before adding or editing a reference

- [ ] Linked directly from SKILL.md (Intent Router row and/or the References index).
- [ ] SKILL.md's References index line accurately says what the file covers.
- [ ] Cross-links to other references use bare sibling filenames, forward slashes, and target
      files that are themselves linked from SKILL.md.
- [ ] No SKILL.md global is restated; the rule lives in exactly one place.
- [ ] Over 100 lines → has a table of contents (see the sizing doc).
- [ ] Only runtime-actionable content; background moved to `docs/`.
- [ ] `python dev-tools/qa.py` passes (validates that every SKILL.md reference pointer resolves
      to a real file and that local Markdown links resolve).

## External sources

### The open standard

- [Agent Skills — Specification](https://agentskills.io/specification) — the SKILL.md format,
  the `references/`/`scripts/`/`assets/` layout, progressive-disclosure tiers, "use relative
  paths … one level deep," and the 1024-char `description` limit.
- [Agent Skills — How to add skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
  — the client's duties: store `location`, resolve relative paths against the skill directory,
  allowlist skill dirs for permissions, and exempt skill content from context compaction.
- [agentskills.io — home](https://agentskills.io/home) — standard overview and adopting clients.

### Anthropic authoring guidance

- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  — progressive-disclosure patterns, "avoid deeply nested references," TOC for files over 100
  lines, forward-slash paths, `<500` lines / `<5000` tokens for SKILL.md.
- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
  — the discovery → activation → execution model.
- [Claude Code — Skills](https://code.claude.com/docs/en/skills) — reference supporting files
  from SKILL.md so the agent knows when to load them; Claude Code follows the open standard.
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

### Google Antigravity

- [Antigravity — Skills](https://antigravity.google/docs/skills) and
  [IDE Skills](https://antigravity.google/docs/ide/skills) — the three-stage model and install
  locations.
- [Antigravity — CLI plugins & skills](https://antigravity.google/docs/cli/plugins).
- [Antigravity — Rules & workflows](https://antigravity.google/docs/rules-workflows) — the
  12,000-char cap on *rules* files (not SKILL.md).
- [Authoring Antigravity Skills codelab](https://codelabs.developers.google.com/getting-started-with-antigravity-skills).
- [Where does Antigravity look for Agent Skills?](https://atamel.dev/posts/2026/07-01_where_agy_agent_skills/)
  — tested matrix of skill discovery paths across AGY / CLI / IDE.

### The relative-path gap, filed as bugs

- [anthropics/skills#1153](https://github.com/anthropics/skills/issues/1153) (open) — relative
  `references/` paths don't resolve from the skill directory; requests a `$SKILL_DIR`.
- [anthropics/claude-code#56325](https://github.com/anthropics/claude-code/issues/56325)
  (closed as duplicate) — same, with the "file is in this skill's directory" workaround.
- [kirodotdev/Kiro#6955](https://github.com/kirodotdev/Kiro/issues/6955) (open) — Kiro strips
  the skill directory on injection.
- [Antigravity: agent unaware of global skills due to missing path in system prompt](https://discuss.ai.google.dev/t/bug-report-agent-is-unaware-of-global-skills-due-to-missing-path-in-system-prompt/127260)
  (open) — `<skills>` block carries no directory while `<workflows>` does.
- [Antigravity 2.2.1: models not following rules, fake using skills/tools](https://discuss.ai.google.dev/t/bug-feedback-antigravity-2-2-1-models-not-following-global-nor-agents-rules-fake-using-skills-tools/172904)
  — instruction files read then discarded.
- [Antigravity has weak awareness of using necessary skills](https://discuss.ai.google.dev/t/antigravity-has-a-weak-awareness-of-using-necessary-skills/128468)
  — A/B where only Antigravity failed to use skills.
