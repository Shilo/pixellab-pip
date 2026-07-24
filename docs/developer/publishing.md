# Publishing checklist

Where to publish PixelLab Pip for discovery, as both an **Agent Skill** and an **Agent Plugin**. This is a one-time checklist plus a reference — not a status board. Do the boxes in §1–§2 once; the rest is automatic or deliberately skipped.

**Priority rule:** High traffic → do it regardless of effort. Medium → only if low-effort (auto-index or a paste-URL form). Low → automatic only, else skip. "Traffic" is a reasoned tier from a visible signal (list-repo stars, catalog size, brand), not analytics; the signal is cited per row so you can override it.

**Highest-ROI move first:** most auto-indexers key off GitHub repo **topics**. The repo already has `agent-skills` (feeds several skill scrapers). It is missing `gemini-cli-extension`, which is the *only* thing gating the free, official Gemini CLI gallery. Add that topic and one High-traffic plugin listing appears with zero further work — see §2.

---

## §1 — Skill directories to submit (one-time)

Pip is a SKILL.md skill, so these apply. Each is free and does not currently list Pip.

**High traffic — do regardless of effort (PRs):**

- [ ] **ComposioHQ/awesome-claude-skills** — ~70k★ (Composio brand). PR adding an entry per its `CONTRIBUTING.md`. Highest reach.
- [ ] **VoltAgent/awesome-agent-skills** — 28.9k★, ~1,500 skills. PR: add `- **[Shilo/pixellab-pip](https://github.com/Shilo/pixellab-pip)** — <=10-word desc` to the right category. Note: the list favors skills with usage traction, so a brand-new entry may be deferred — submit anyway, re-try after installs grow.
- [ ] **heilcheng/awesome-agent-skills** — ~6k★. Fork → edit per `CONTRIBUTING.md` → PR.

**Medium traffic — only because each is a low-effort paste-URL form or CLI:**

- [ ] **Smithery (skills)** — https://smithery.ai/skills — accepts plain SKILL.md skills via the `smithery-ai/cli` publish command. Medium–High reach; could later be automated in the release workflow like ClawHub.
- [ ] **LobeHub skills** — listed at https://lobehub.com/skills; submit by pasting the repo URL (import scrapes SKILL.md). Verify the current submit path on the site before relying on it.
- [ ] **ClaudeSkills.info** — https://claudeskills.info/submit/ — form + light moderation.
- [ ] **awesomeskill.ai** — https://awesomeskill.ai/submit — form, ~48h review.

---

## §2 — Plugin / extension marketplaces to submit (one-time)

Pip also ships plugin manifests (Claude, Codex, Cursor, Gemini, Copilot). These are the plugin-surface directories, all High/official and none listing Pip yet.

- [x] **Gemini CLI extensions gallery** — https://geminicli.com/extensions — **automatic once discoverable.** The `gemini-cli-extension` GitHub topic is set and `gemini-extension.json` is at root; Google crawls daily, so the listing appears on its own. Nothing more to do.
- [ ] **Cursor Marketplace** — https://cursor.com/marketplace/publish — official, in-editor 1-click install, High traffic. Form + manual review; must stay open source (it is). Worth the review wait.
- [ ] **Anthropic community marketplace** — submit at https://clau.de/plugin-directory-submission (repo `anthropics/claude-plugins-community`) — official Claude Code pipeline, auto security scan + Anthropic review. Installs via `@claude-community`. Direct PRs are auto-closed; use the form.
- [ ] **github/awesome-copilot** — https://github.com/github/awesome-copilot — a **default-registered** marketplace in Copilot CLI and VS Code agent mode. Single PR; Medium–High reach, low effort. This is also the correct home for the repo's `.agents/plugins/marketplace.json` ("VS Code Agent Plugins") surface.

---

## §3 — Automatic / self-updating — ignore

These pull from GitHub or ClawHub on their own. A GitHub release *is* the publish; there is nothing to submit or refresh.

| Target | Why it needs nothing |
|---|---|
| **ClawHub** — clawhub.ai/shilo/skills/pixellab-pip | **Live**, and republished + rescanned every release by [release-skill.yml](../../.github/workflows/release-skill.yml). The only automated push. |
| **awesomeskills.dev** — /en/skill/shilo-pixellab-pip | **Live.** Display card is a snapshot frozen at submit; the *install* it hands out targets your GitHub live. Optional lever: re-paste the URL at /en/submit only after a major description rewrite. |
| **SkillsMP** — skillsmp.com/creators/shilo | **Live**, auto-indexed from the public repo. |
| **skills.sh** — /shilo/pixellab-pip/pixellab-pip | Auto-listed via install telemetry; grows with installs, not submission. Metadata is a snapshot it derives itself — not controllable. |
| **FindSkills / SkillsMD / claudemarketplaces.com / quemsah/awesome-claude-plugins** | Passive scrapers; they index off the repo (several off the `agent-skills` topic) and metrics. Keep the repo topics on and they appear on their own. |

**Keep these repo topics on** so the scrapers keep finding Pip: `agent-skills` and `gemini-cli-extension` (both present).

---

## §4 — Excluded, and why (do not re-litigate)

- **MCP-server registries — Glama, PulseMCP, mcp.so.** Pip *calls* PixelLab's MCP server; it is not itself an MCP server. Wrong category. (Smithery is the exception — it also lists plain skills, so it's in §1.)
- **VS Code Marketplace / Open VSX.** Those are for traditional `.vsix` extensions. Pip's "VS Code Agent Plugins" is the Git-based agent-plugin system, which is the `awesome-copilot` mechanism in §2 — not a `.vsix`. Do not package for them.
- **Agensi (agensi.io) / MCP Market skills (mcpmarket.com/sell-skills).** Login/Stripe-gated seller flows aimed at paid exposure. Skip unless selling.
- **Low-tier awesome-lists** (skillmatic-ai, nicepkg/ai-workflow, philipbankier, skills-hub.ai, and the small `awesome-claude-code-plugins` lists). Low traffic + PR effort. Skip unless chasing completeness; the auto-scraping ones among them pick Pip up passively anyway.

---

## §5 — Parking lot (revisit later)

- **OpenAI Codex official plugin directory** — self-serve publishing was "coming soon" / closed as of mid-2026. Pip already installs via Git URL. Re-check when submissions open.
- **Anthropic official marketplace** (`anthropics/claude-plugins-official`) — curated/partner-only, no self-submit. Nothing to do.

---

*Last research pass: 2026-07-24. Re-scan §1–§2 targets only if a release makes a big pitch/description change, or roughly yearly — the manual set is small and static.*
