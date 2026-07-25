# Publishing checklist

Where to publish PixelLab Pip for discovery, as both an **Agent Skill** and an **Agent Plugin**, plus the current status of each target. Do the open boxes in §1–§2 once; the rest is automatic, in review, or deliberately skipped.

**Priority rule:** High traffic → do it regardless of effort. Medium → only if low-effort (auto-index or a paste-URL form). Low → automatic only, else skip. "Traffic" is a reasoned tier from a visible signal (list-repo stars, catalog size, brand), not analytics.

## Status snapshot (2026-07-24)

- **Live now:** ClawHub, awesomeskills.dev, skills.sh, SkillsMP, LobeHub.
- **In review:** Cursor Marketplace, Anthropic community marketplace, ComposioHQ PR #1436, heilcheng PR #370.
- **Passive (will crawl on its own):** FindSkills, SkillsMD, claudemarketplaces.com, Gemini CLI gallery.
- **Skipped (broken/low-value):** awesomeskill.ai (broken auth), ClaudeSkills.info (submit API returns HTTP 500).
- **Later:** VoltAgent (needs install traction), github/awesome-copilot (optional PR).

---

## §1 — Skill directories (one-time)

Pip is a SKILL.md skill, so these apply.

**High traffic — do regardless of effort (PRs):**

- [x] **ComposioHQ/awesome-claude-skills** — ~70k★. Submitted as a link entry in Development: [PR #1436](https://github.com/ComposioHQ/awesome-claude-skills/pull/1436) (in review).
- [x] **heilcheng/awesome-agent-skills** — ~6k★. Submitted to Community Skills → Development and Testing: [PR #370](https://github.com/heilcheng/awesome-agent-skills/pull/370) (in review).
- [ ] **VoltAgent/awesome-agent-skills** — 28.9k★, ~1,500 skills. **On hold — do not submit yet.** Its `CONTRIBUTING.md` rejects brand-new skills ("Brand new skills that were just created are not accepted. Give your skill time to mature and gain users"). Revisit once installs grow; entry format is `- **[Shilo/pixellab-pip](https://github.com/Shilo/pixellab-pip)** — <=10-word desc` under Community Skills → Development and Testing.

**Medium traffic — attempted, both broken → skipped:**

- [ ] ~~**ClaudeSkills.info**~~ — https://claudeskills.info/submit/ — **skip.** The submit endpoint (`POST /api/submissions`) returns **HTTP 500** on a well-formed request; it is a server-side bug on their side, not an input problem. Retry later if desired.
- [ ] ~~**awesomeskill.ai**~~ — https://awesomeskill.ai/submit — **skip.** Login/auth flow is broken (`/api/auth/error` → "Not Found"). Lowest-traffic target; not worth registering.

---

## §2 — Plugin / extension marketplaces (one-time)

- [x] **Cursor Marketplace** — https://cursor.com/marketplace/publish — submitted (in review). Official, in-editor 1-click install, High traffic; must stay open source (it is).
- [x] **Anthropic community marketplace** (`anthropics/claude-plugins-community`) — submitted (in review). Installs via `@claude-community`. **Submit through the in-app form, not a PR (PRs are auto-closed):**
  - Individual authors → **Console form: https://platform.claude.com/plugins/submit**
  - Team/Enterprise orgs → claude.ai form: `claude.ai/admin-settings/directory/submissions/plugins/new` (needs directory-management access). The `clau.de/plugin-directory-submission` shortlink routes here, so an individual account cannot use it.
  - Run `claude plugin validate` first (passes). Plugin is at the repo root (`.claude-plugin/plugin.json`, `source: "./"`). After approval it is pinned to a commit SHA and CI auto-bumps it; the public catalog syncs nightly.
- [x] **Gemini CLI extensions gallery** — https://geminicli.com/extensions — **automatic.** The `gemini-cli-extension` GitHub topic is set and `gemini-extension.json` is at root; Google crawls daily, so it appears on its own.
- [ ] **github/awesome-copilot** — https://github.com/github/awesome-copilot — optional. A default-registered marketplace in Copilot CLI / VS Code agent mode. Single PR, Medium–High reach. Heavier than a link (it vendors a plugin entry into GitHub's repo); do only if chasing completeness.

---

## §3 — Automatic / self-updating (live, ignore)

These pull from GitHub or ClawHub on their own. A GitHub release *is* the publish.

| Target | Status / why it needs nothing |
|---|---|
| **ClawHub** — clawhub.ai/shilo/skills/pixellab-pip | **Live.** Republished + rescanned every release by [release-skill.yml](../../.github/workflows/release-skill.yml). The only automated push. |
| **awesomeskills.dev** — /en/skill/shilo-pixellab-pip | **Live.** The display card is a snapshot frozen at submit; the *install* it hands out targets your GitHub live. **Manual refresh lever:** re-paste the repo URL at /en/submit to re-parse `SKILL.md` — do this only after a real description/branding change. |
| **skills.sh** — /shilo/pixellab-pip/pixellab-pip | **Live.** Auto-listed via install telemetry; grows with installs, not submission. **No manual update exists** — read-only API, no publish/refresh/claim endpoint. Metadata is a snapshot it derives itself; the only input is people running `npx skills add`. Nothing to do. |
| **SkillsMP** — skillsmp.com/creators/shilo | **Live**, auto-indexed from the public repo. |
| **LobeHub** — lobehub.com/skills/shilo-pixellab-pip | **Live.** Auto-indexes public repos containing a valid `SKILL.md`; no submit form or PR. |
| **Smithery skills** — smithery.ai/skills | Passive. **No skill-publish command exists** (its CLI `publish` is MCP-server-only). Discovered from the GitHub `agent-skill`/`agent-skills` topic. |
| **FindSkills / SkillsMD / claudemarketplaces.com / quemsah/awesome-claude-plugins** | Passive scrapers; index off the repo (several off the `agent-skills` topic) and metrics. FindSkills has not crawled Pip yet; it mirrors ClawHub, so it follows on its own. |

**Keep these repo topics on** so the scrapers keep finding Pip: `agent-skills` and `gemini-cli-extension` (both present).

---

## §4 — Excluded, and why (do not re-litigate)

- **MCP-server registries — Glama, PulseMCP, mcp.so.** Pip *calls* PixelLab's MCP server; it is not itself an MCP server. Wrong category. (Smithery is the exception — it also lists plain skills, so it's in §3.)
- **VS Code Marketplace / Open VSX.** For traditional `.vsix` extensions. Pip's "VS Code Agent Plugins" is the Git-based agent-plugin system (the `awesome-copilot` mechanism in §2) — not a `.vsix`. Do not package for them.
- **Agensi (agensi.io) / MCP Market skills (mcpmarket.com/sell-skills).** Login/Stripe-gated seller flows for paid exposure. Skip unless selling.
- **Low-tier awesome-lists** (skillmatic-ai, nicepkg/ai-workflow, philipbankier, skills-hub.ai, small `awesome-claude-code-plugins` lists). Low traffic + PR effort. Skip; the auto-scraping ones pick Pip up passively anyway.

---

## §5 — Parking lot (revisit later)

- **OpenAI Codex official plugin directory** — self-serve publishing was "coming soon" / closed as of mid-2026. Pip already installs via Git URL. Re-check when submissions open.
- **Anthropic official marketplace** (`anthropics/claude-plugins-official`) — curated/partner-only, no self-submit; Anthropic pulls plugins in at its discretion. Nothing to do.

---

*Last updated: 2026-07-24. Re-scan §1–§2 only after a release with a big pitch/branding change, or when checking whether in-review submissions landed.*
