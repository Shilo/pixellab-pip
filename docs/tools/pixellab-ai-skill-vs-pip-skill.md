# PixelLab AI Skill vs Pip Skill

Last reviewed: 2026-07-06, against PixelLab AI Skill v1.5.5 (published 2026-06-25, still the latest ClawHub release — unchanged since the prior review) and the current PixelLab Pip repository (now with a blueprint system — see [Blueprints vs Recipes](#blueprints-vs-recipes)).

This compares PixelLab Pip with the unofficial [PixelLab AI Skill](https://clawhub.ai/uncmatteth/skills/pixellab-ai) by uncmatteth on ClawHub. The goal is to understand adjacent tooling and find real feature gaps, without copying its implementation or ranking the projects.

Sources reviewed:

- [ClawHub PixelLab AI Skill page](https://clawhub.ai/uncmatteth/skills/pixellab-ai) and [package](https://clawhub.ai/api/v1/packages/pixellab-ai) / [version](https://clawhub.ai/api/v1/packages/pixellab-ai/versions) metadata.
- A full download of the v1.5.5 package (all 60 files), unpacked for side-by-side reference at the sibling folder `pixellab-ai-skill/` next to this repository (not part of this repo).
- Live checks of `https://api.pixellab.ai/v2/openapi.json` (68 paths) and `https://api.pixellab.ai/v1/openapi.json` (8 paths) on 2026-07-04.
- The full current Pip repository: `skills/pixellab-pip/SKILL.md`, all 23 runtime references, bundled `assets/` helpers and `blueprints/` examples, `dev-tools/`, `tests/`, and `docs/`.

## Summary

PixelLab AI Skill is a production-pipeline skill: it bundles Python helper scripts, recipe JSON, dry-run manifests, budget/balance preflights, contact sheets, candidate approval folders, and sprite validation commands so an agent can plan and run multi-asset PixelLab packs through REST.

PixelLab Pip is an agent-agnostic routing and execution contract: it teaches an agent to pick the right PixelLab surface (hosted MCP, REST v2, website/editor, Aseprite, Pixelorama, legacy v1), prepare prompts and image roles correctly, control cost, respect auth and integrity boundaries, and report honestly — using whatever tools the host agent already has.

Use PixelLab AI Skill when you want its packaged recipe/manifest/approval pipeline (see [When To Use PixelLab AI Skill Instead](#when-to-use-pixellab-ai-skill-instead)). Use Pip when you want broad-surface route selection, deeper per-asset operational knowledge, and portable behavior across agent apps.

## Feature Inventory

Every observable feature of either project, grouped by area. Categories and rows are ordered by importance to a user choosing between the projects.

Legend: ✅ shipped as documented behavior or code · 🟡 partial or different-shaped equivalent · ❌ absent.

### PixelLab Surface Coverage

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| REST v2 endpoint routing | ✅ — 63-path coverage matrix (refreshed 2026-06-21) plus routing rules | ✅ — intent router plus per-asset references |
| Hosted MCP tools | 🟡 — optional path naming seven tools; REST helper preferred for bulk | ✅ — MCP-first for managed assets, prefix/suffix tool matching, no-silent-fallback rules |
| Newer v2 routes: `create-ui-asset`, `generate-font-pro`, `portrait-character-pro` | ❌ — absent from its matrix and routing (they post-date its refresh) | ✅ — routed with MCP equivalents (`create_ui_asset`, `create_font`, `create_portrait_character`) |
| Website/editor (Pixelorama) assistance with permission boundaries | ❌ | ✅ |
| Aseprite plugin boundary, CLI/Lua workspace integration | ❌ | ✅ — `references/aseprite-cli.md`, `references/aseprite-mcp.md` |
| Editor-only utilities mapping (Canny/Pose/Depth, reduce colors, unzoom, pixel correction, reshape, Try on) | ❌ | ✅ — `references/editor-only-utilities.md` |
| Undocumented/internal endpoint prohibition | 🟡 — "do not invent an API path if the route is not present in current docs" | ✅ — named prohibitions: website root routes, Aseprite extension internals, session tokens |
| Account asset management (list/get/tags/ZIP) | ✅ — DELETE excluded by policy | ✅ — delete helpers allowed behind approval gates |
| MCP platform tools (projects, sandbox, chat, deployed agents, help/feedback) | ❌ | ✅ — `references/mcp-platform-tools.md` with approval boundaries |
| `ui-assets` list/get/delete management routes | ❌ | 🟡 — create side routed; management via matching-getter guidance rather than named routes |
| Legacy v1 boundary (legacy-only use) | ✅ | ✅ |
| Balance check | ✅ | ✅ |

### Execution And Production Tooling

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Bundled REST client (submit, bounded retries, polling, downloads, base64 decode, size/alpha checks) | ✅ — `scripts/pixellab_client.py` | ❌ — the host agent's own tools make calls per route guidance |
| Manifest system (plan, lint, repair placeholders, budget, run, resume, retry manifest, skip-existing) | ✅ — `scripts/pixellab_workflow.py` | ❌ — one-candidate-first contract plus per-call approval |
| Per-route cost knowledge | 🟡 — coarse local budget units | ✅ — documented generation costs per route family, checked 2026-07-04 (`references/cost-routing.md`) |
| Cheap-route selection and paid-retry gating | ❌ | ✅ — cost-sensitive intent changes routes and requires per-attempt approval |
| Balance preflight | ✅ — dedicated command | ✅ — balance snapshot before nontrivial paid calls, delta reporting |
| Async job lifecycle detail (423/404 early lookups, review state, expiring URLs, 8-hour map-object expiry, backoff) | 🟡 — `--poll`, timeout files, resume | ✅ — `references/job-lifecycle.md` |
| Resume pending jobs without resubmitting paid work | ✅ — `poll-result-file`, saved job IDs | ✅ — keep IDs, poll the matching getter, never resubmit |
| Bundled pack recipes (platformer, modular RPG character, sidescroller tileset, UI HUD, enemy variants) | ✅ — templated payloads with placeholder dependencies and seed offsets, run through the manifest pipeline | 🟡 — no templated multi-asset packs; blueprint bundles plus a `blueprints/` folder cover ordered, replayable recipes run by the host agent (`references/blueprint.md`) |
| Replayable/shareable per-generation record (portable single file, plain-language overrides) | 🟡 — recipes and saved job IDs reproduce work inside its own pipeline; no portable single-file share format | ✅ — `*.blueprint.json` = route plus exact request body, auto-written after each run, replayed with overrides, shared as one file, `_comment*` human notes, example blueprints (`references/blueprint.md`) |
| Contact sheets, galleries, candidate/approved folder promotion | ✅ | ❌ — candidates reported for user selection; local assembly limited to previews and labeled inspection aids |
| HTTP error-code guidance | ✅ — 401/402/422/429/529/5xx | ✅ — 400/401/402/403/409/422/423/429/529 |
| Worker-subagent workflow for live calls | ✅ — subagent briefs and context-isolation rules | ❌ — deliberately portable to agents without delegation |
| Runtime package self-check (`doctor`) | ✅ | ❌ — repo-side QA/CI instead (`dev-tools/qa.py`, pytest, GitHub Actions) |
| JSONL progress/event logs | ✅ | ❌ |

### Prompting And Input Handling

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Prompt preparation from rough ideas | ✅ — plain-English visual-brief gate plus labeled prompt blocks | ✅ — Text Preparation contract: opt-out enhancement, visual-content-only prompts, no structured-parameter repetition |
| Consistency gate before spending credits | ✅ — visual brief, seed candidates, approved anchor before bulk | ✅ — identity/style/palette/view/reference anchor summary, at most three blocking questions, one candidate first |
| Image input role classification | 🟡 — general init/reference/style guidance | ✅ — endpoint-specific goal router across 13 roles (`references/image-input-roles.md`) |
| Enhance endpoints and inline `enhance_prompt` | 🟡 — routes the three enhance endpoints | ✅ — inline-flag constraints per route, ~0.05-generation cost, one-enhancement-path-per-call rule |
| Localization for non-English or mixed-language requests | ❌ | ✅ — `references/localization.md` |
| Preset/template/skeleton animation catalog (template IDs, species families, view/direction traps) | ❌ — routes to endpoints only | ✅ — `references/preset-skeleton-template-animation.md` |
| Tileset depth (MCP field schemas, human-label-to-field mapping, transition sizing, reference-image controls, strict 1-bit workflows, dual-grid sheet assembly order) | 🟡 — tileset prompt terms and size notes | ✅ — `references/tileset.md` |
| Icon and icon-sheet engineering (validated prompts, cell math, background defaults, failure anchors) | ❌ | ✅ — `references/icon.md` |
| Idle-loop and near-identical `last_frame` artifact risk | ❌ | ✅ — `references/animation.md` |
| Exact-grid/packed-sheet recipes for below-32px cells | ❌ | ✅ — `references/create-image-pro.md` |
| Prompt character limits (OpenAPI-verified) | ❌ | ✅ — `references/prompt-limits.md` |
| Community-derived workflow recipes (Discord/YouTube tuning values, e.g. style guidance and init-strength ranges) | ✅ — three community references plus two video indexes | ❌ — official docs and locally verified research only, by policy |
| Endpoint example payloads | ✅ — 38 JSON files | ❌ — refreshes OpenAPI when exact schemas matter |
| Seed-reuse technique guidance (reuse for near-variants, vary for fresh candidates, keep seed across frame batches) | ✅ | 🟡 — seed recording and vary-across-retries rules; no near-variant reuse tip |

### Layered Sprites And Paperdolling

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Outfit-transfer → edit-animation body-removal composite pipeline | ✅ — recipe plus reference workflow (second generative pass removes the body) | ✅ — documented as composite routes / two-pass fallback with drift and labeling warnings |
| Frame-grid contract (canvas, frame count/order, pivot, transparency) | ✅ — reference plus recipe `sprite_contract` | ✅ — paperdoll preservation list |
| State-first animation (pose a state before animating) | ✅ — `sprite-animation-layering.md` | ✅ — state / custom start-frame routes (`references/animation.md`) |
| Local pixel-diff isolated-layer extraction with QA gates | ❌ — no local extraction; relies on the edit-animation body-removal composite | ✅ — alpha-aware diff-extraction contract (`references/paperdolling.md`); drift/temporal/round-trip QA in `docs/pixellab/` plan |
| `validate-sprites` file-checker (already-separated layer files) | ✅ — command checks frame set/order vs the reference layer and PNG-header size; no pixel/transparency check | ❌ — equivalent checks are a manual paperdoll checklist, no tool |
| Honest layer-vs-composite labeling (no semantic layer extraction claimed) | 🟡 — recipe QA notes only | ✅ — reusable-vs-composite output labels enforced |
| Skeleton / hardpoint anchoring | 🟡 — `estimate-skeleton` / `animate-with-skeleton` example payloads only, no paperdoll wiring or hardpoint manifest | 🟡 — skeleton endpoints routed (`references/animation.md`); hardpoint manifest planned in `docs/pixellab/`, not shipped |
| Engine-export packaging (paperdoll manifest plus engine adapters) | ❌ — PNG-frames/atlas export is prose guidance only | 🟡 — manifest plus Godot/Unity/Phaser/Pixi exporters planned in `docs/pixellab/`, not shipped |

### Output Handling And Reporting

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Usage reporting shape | ✅ — endpoint, result files, downloads, costs, errors | ✅ — files, route, exact final inputs, seeds, cost, verification checklist (`references/usage-reporting.md`) |
| Verification-before-final contract | ✅ — inspect/validate commands before calling assets game-ready | ✅ — per-route verification sections; failed verification reported plainly |
| Asset integrity rules (all pixels from PixelLab or the user, no local drawing, no baked backgrounds, no silent repair) | ❌ | ✅ — SKILL.md Asset Integrity |
| Background-removal recovery after failed `no_background` | 🟡 — routes to `/remove-background` | ✅ — bundled conservative helper plus PixelLab fallback contract (`assets/background_removal.py`, `references/background-removal.md`) |
| Seed/ID recording for reproduction | ✅ — recipe seed offsets, saved job IDs | ✅ — per-call seed rules and ID capture in manifests |
| GIF/spritesheet assembly with disposal-method verification | ❌ | ✅ — `references/local-asset-assembly.md` |
| Standard output folders | ✅ — payloads/results/seed-candidates/candidates/approved/downloads/reports/logs | ✅ — single `pixellab-pip-generations/` tree |
| Completion sound toggle | ❌ | ✅ — `references/bark.md`, `assets/bark.py` |

### Credentials And Security

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Named secret env var | ✅ — `PIXELLAB_API_KEY` | ✅ — `PIXELLAB_SECRET` |
| Never print/commit/paste-into-chat token rules | ✅ | ✅ |
| Guided setup wizard (mode choice, token-free previews, write approval, no-credit verification) | ❌ — install instructions only | ✅ — `references/setup.md` |
| Browser/session-token prohibition | ❌ — not addressed | ✅ |
| Broad secret-scan prohibition | 🟡 — helper does not auto-discover secret files | ✅ — explicit no-scan rules for home/config/history/keychain/project trees |
| MCP auth reuse guidance | 🟡 — Codex `--bearer-token-env-var` example | ✅ — `references/credentials.md` lookup order and literal-token boundaries |
| `.env` file loading | ✅ — explicit `--env-file` flag only (auto-discovery removed in v1.5.4) | 🟡 — discouraged default; allowed only with a named loader and explicit user approval |
| Custom API base | ✅ — `--allow-custom-base` for trusted test endpoints | ❌ — official base only, by policy |

### Trust And Disclosure

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Third-party registry security scan with public result | ✅ — ClawHub/SkillSpector "Security audit: Pass" badge on the skill page | 🟡 — CI SkillSpector audit on public Code Scanning (weekly, risk-score gate) plus Sigstore build-provenance attestations; the release workflow also auto-publishes to ClawHub for its independent audit once a `CLAWHUB_TOKEN` secret is set |
| Declared permissions manifest (env vars, network hosts, filesystem scope, commands) in SKILL.md frontmatter | ✅ | ✅ — lean, honest scope (`env: PIXELLAB_SECRET`, `commands: python`); no network declared because the skill's own code makes no calls |
| Machine-readable `requires_api_key` metadata | ✅ — `true` | ✅ — and more accurate: `false` with a note, since guidance/setup/routing need no key |
| Skill card (use case, known risks and mitigations, license, output types) | ✅ — `skill-card.md` | 🟡 — README Security section covers access, risks, and expected findings; no separate card file |
| Security-scan disclosure section (explains expected scanner findings) | ✅ | ✅ — README Security section pre-discloses expected SkillSpector findings |
| Permissive license | ✅ — MIT-0 | ✅ — MIT |

### Distribution And Invocation

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Multi-agent install manifests (Claude Code, Codex, Cursor, Copilot, VS Code, Gemini) | 🟡 — Codex/OpenClaw focus plus generic copy-paste instructions | ✅ — per-app plugin/marketplace manifests plus manual paths |
| ClawHub-packaged install (`npx clawhub install`) | ✅ | 🟡 — release workflow auto-publishes to ClawHub once `CLAWHUB_TOKEN` is set, enabling `clawhub install`; GitHub marketplaces/plugins remain primary |
| Copy-paste agent install prompt | ✅ — "Easy Install" block | ✅ — README Agent-Assisted Install |
| Release artifact (skill zip) | ✅ — ClawHub package | ✅ — GitHub release zip via CI |
| OpenClaw skill metadata and config examples | ✅ | ❌ — omitted by design to stay agent-agnostic; ClawHub publishing needs none |
| Explicit invocation gating (PixelLab named or clearly intended) | ✅ | ✅ |
| Post-trigger commands (`setup`, `bark`) | ❌ | ✅ |

### Documentation And Maintenance

| Feature | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Official docs refresh path | 🟡 — `refresh-api-metadata` command, `/llms.txt` | ✅ — annotated URL table, refresh triggers, authoritative MCP inventory (`references/official-pixellab-documentation.md`) |
| Model/mode label semantics (Pro, v3, Pixen/PixFlux/BitForge, size labels) | ❌ | ✅ — SKILL.md Model And Mode Terms |
| SDK-parity warnings | ❌ | ✅ |
| Repo QA/CI (link checks, manifest sync, tests) | 🟡 — runtime `doctor` self-check | ✅ — CI-enforced `dev-tools/qa.py` and pytest |
| Official YouTube corpus index (156 items with transcript status) | ✅ | ❌ |

## When To Use PixelLab AI Skill Instead

The complete list of features PixelLab AI Skill has that Pip does not, in one place:

1. Bundled REST client script — submit, bounded retries, polling, downloads, base64 decoding, size/alpha validation flags, timeout resume (`pixellab_client.py`).
2. Manifest pipeline commands — `plan`, `lint-manifest`, `repair-placeholders`, `budget`, `run --yes` with skip-existing/resume, `retry-manifest`, `cost-summary` (`pixellab_workflow.py`).
3. Five bundled pack recipes (NES platformer, modular RPG character, sidescroller tileset, UI HUD, enemy variants) with templated payloads, dependencies, and seed offsets. (Partially addressed — Pip's blueprint bundles and `blueprints/` folder cover ordered, replayable, shareable recipes; the templated multi-asset packs with placeholder dependencies and seed offsets remain a deliberate skip. See [Blueprints vs Recipes](#blueprints-vs-recipes).)
4. Candidate review tooling — numbered `contact-sheet` PNGs with index JSON, `gallery`, `approve-candidate` promotion into `approved/`, seed-candidate naming convention.
5. Asset inspection commands — `inspect-assets`, `validate-sprites` (layer set, frame glob, expected size).
6. `balance-preflight` and `refresh-api-metadata` as ready-made commands.
7. Worker-subagent briefs (`subagent-brief`) and context-isolation rules for live runs.
8. JSONL progress/event logs and a runtime `doctor` package self-check.
9. ClawHub distribution: one-command install, registry versioning, and the ClawHub/SkillSpector security-scan badge. (Now addressed — Pip's release workflow auto-publishes to ClawHub once a token is set; see verdicts.)
10. OpenClaw skill metadata and config examples. (Deliberately not matched — Pip stays agent-agnostic.)
11. Declared permissions frontmatter and machine-readable `requires_api_key` metadata. (Now addressed in Pip's SKILL.md frontmatter.)
12. `skill-card.md` risk/mitigation disclosure and a security-scan-notes section. (Now addressed by Pip's README Security section.)
13. Distilled community knowledge — Discord workflow/tutorial references and two official-YouTube indexes with tuning starting points.
14. 38 offline endpoint example payload JSON files.
15. Explicit `--env-file` loading and a `--allow-custom-base` escape hatch for test endpoints.

Choose PixelLab AI Skill over Pip when you want that shape of work: an OpenClaw/ClawHub environment, recipe-driven bulk pack production through its bundled scripts without MCP, a folder-contract approval pipeline, or community-lore tuning values as starting points. Choose Pip when you want the widest PixelLab surface coverage (MCP, fonts, portraits, structured UI, website/editor, Aseprite), per-asset operational depth, cost control, localization, and portable behavior in any skill-capable agent.

## Coverage Freshness

PixelLab AI Skill's coverage matrix says v2 exposes 63 paths (refreshed 2026-06-21). The live OpenAPI on 2026-07-04 exposes 68. The five additions — `create-ui-asset`, `generate-font-pro`, `portrait-character-pro`, `ui-assets`, and `ui-assets/{ui_asset_id}` — are absent from its matrix and routing rules. Pip routes structured UI assets, fonts, and portrait-character conversion on both REST and MCP; UI-asset list/get/delete management is handled through Pip's matching-getter guidance rather than named routes. Its v1 count (8 legacy paths) still matches.

## Blueprints vs Recipes

Both projects can capture "how an asset was made" and replay it, but the shapes and use cases differ.

A PixelLab AI Skill **recipe** is an author-time template for producing a whole multi-asset pack. Each of the five bundled recipes (NES platformer, modular RPG character, sidescroller tileset, UI HUD, enemy variants) carries placeholder fields, inter-asset dependencies, seed offsets, and budget units, and is planned and executed through the manifest runner (`plan` → `run`). It is forward-looking and pipeline-bound: the recipe plus the bundled scripts produce the pack; reproduction lives inside its own output-folder contract and saved job IDs.

A Pip **blueprint** (`references/blueprint.md`) is the minimal shareable record of one generation: a single `*.blueprint.json` holding the route (`MCP <tool>` or `POST /v2/...`) plus the exact request body, auto-written beside the outputs after each successful run. It is both backward-looking (captures what was made) and forward-looking (replay it, with plain-language overrides like "same seed, new prompt"), needs no bundled runner — the host agent executes it — and is portable: one file is the shareable unit, images travel alongside by relative path. A blueprint can be a bundle (an ordered array of steps where a later step reads an earlier step's output), and hand-authored blueprints in the skill's `blueprints/` folder can be run by name ("create the knight blueprint"). Human notes ride along in `_comment*` keys that are stripped before any request is sent.

So the overlap is the replay idea; the divergence is intent and packaging. Recipes optimize for **producing a parameterized pack through bundled tooling**; blueprints optimize for **reproducing and sharing an exact single generation (or ordered bundle) in any agent, with no tooling**. Pip deliberately does not ship the templated-pack-with-seed-offsets recipes or the runner (see verdicts); the blueprint format covers the portable, shareable, replayable slice of that idea.

## Secret Setup Tradeoff

PixelLab AI Skill is more operational out of the box because its helper scripts perform live REST calls once `PIXELLAB_API_KEY` is set. Since v1.5.4 the helper no longer auto-discovers `.env.local`; it reads the key from the process environment and loads a file only when the user passes an explicit `--env-file PATH`. It also allows a non-default API base behind an explicit `--allow-custom-base` flag.

Pip intentionally ships no REST helper and no `.env` loading path. Its setup flow uses `PIXELLAB_SECRET` through app secret settings, a secret store, or user-scoped environment configuration, previews every write token-free, and inspects `.env*` files only when the user names an exact file and approves inspection. This is less automatic, but safer in mixed projects where `.env.local` may hold unrelated private secrets, and it avoids teaching agents that a custom API base is ever a normal option.

## PixelLab AI Skill Package Inventory

The reviewed v1.5.5 package contains 60 files:

- `_meta.json`, `SKILL.md`, `skill-card.md`, `agents/openai.yaml`, and two OpenClaw config examples.
- Two Python helper scripts: `scripts/pixellab_client.py` (884 lines) and `scripts/pixellab_workflow.py` (2121 lines).
- Five recipe JSON files.
- Thirty-eight endpoint example JSON files.
- Nine reference Markdown files: `api-coverage-matrix.md`, `endpoint-mapping.md`, `prompt-cheatsheet.md`, `sprite-animation-layering.md`, `youtube-workflow-playbook.md`, `community-discord-workflows.md`, `community-discord-tutorials.md`, `install-and-secrets.md`, `official-youtube-index.md`.

Notable `pixellab_workflow.py` commands: `list-recipes`, `plan`, `run`, `budget`, `retry-manifest`, `repair-placeholders`, `gallery`, `inspect-assets`, `validate-sprites`, `lint-manifest`, `contact-sheet`, `cost-summary`, `approve-candidate`, `balance-preflight`, `refresh-api-metadata`, `doctor`, and `subagent-brief`.

## Useful Ideas Already Covered In Pip

- Opt-out prompt preparation: SKILL.md Text Preparation.
- English PixelLab-facing parameters with user-language replies: `references/localization.md`.
- Consistency anchors before spending credits: SKILL.md workflow step 6.
- Route/parameter/ID/output/cost reporting after live calls: `references/usage-reporting.md`.
- MCP treated as configured-or-not, never pretended: SKILL.md workflow step 4.
- Frame-grid preservation and composite-vs-layer honesty: `references/paperdolling.md`, `references/animation.md`.
- Balance preflight and job resume without paid resubmission: SKILL.md Auth And Execution, `references/job-lifecycle.md`.
- Context hygiene for live runs (no raw base64/full JSON in chat): SKILL.md Auth And Execution.
- Error-code guidance: `references/job-lifecycle.md`.

## Gaps In Pip And Verdicts

Every feature from [When To Use PixelLab AI Skill Instead](#when-to-use-pixellab-ai-skill-instead), with an adopt/defer/skip judgment under Pip's KISS/YAGNI rules:

- **Adopt: batch plan preview.** The one genuinely transferable behavior from the manifest pipeline: before an approved multi-asset batch, present a short per-item plan (route plus cost category) and record it in the run manifest. Pip already asks before batches and records IDs/seeds; a written plan is one contract line, not tooling.
- **Adopt: trust and disclosure metadata.** Done 2026-07-05: CI SkillSpector scanning with public Code Scanning results, release build-provenance attestations, optional VirusTotal release scanning, OpenSSF Scorecard, declared permissions frontmatter, an accurate `requires_api_key: false` note, and a README Security section that doubles as the risk/mitigation and expected-findings disclosure. A separate `skill-card.md` file is intentionally not added — the README covers the same facts in one place.
- **Adopt (distribution decision): ClawHub publishing.** Done 2026-07-05: the release workflow auto-publishes the skill folder to ClawHub (headless `clawhub skill publish` with GitHub source provenance) once a `CLAWHUB_TOKEN` secret is set, which triggers ClawHub's independent audit and badge. The skill folder stays agent-agnostic — no OpenClaw files are added. One-time user setup: a ClawHub account and token.
- **Adopt (micro): seed-reuse-for-near-variants clause.** One sentence in the seed rules: reuse the recorded seed when the user wants a near-variant of an approved result; vary it for fresh candidates. Complements the existing vary-across-retries rule.
- **Defer: sprite-layer validator tool.** The paperdolling checklist covers the same checks manually, and `AGENTS.md` already names "a dedicated local asset validator" as the trigger. Add it when layered-pack work recurs.
- **Defer: community technique corpus.** Do not import unverified Discord/YouTube tuning values (standing policy). Individually promising techniques (held-equipment sketch-and-inpaint, non-human humanoid baseline, pose libraries) can be tested locally and promoted through `docs/pixellab/` findings, as the icon and tileset research was.
- **Adopt (done): blueprint system.** Done 2026-07-06: `*.blueprint.json` records a generation's route plus exact request body, auto-written after each run, replayed with plain-language overrides, shared as one portable file, with `_comment*` notes and example blueprints in `blueprints/` (`references/blueprint.md`). This covers the portable/shareable/replayable slice of the recipe idea without a bundled runner; the templated multi-asset pack recipes (placeholder dependencies, seed offsets, budget) remain a deliberate skip below. See [Blueprints vs Recipes](#blueprints-vs-recipes).
- **Skip: bundled REST client, manifest runner, pack-template recipes, approval-folder pipeline.** A different product shape — a self-contained batch pipeline. Pip's contract is that the host agent's own tools execute the selected route; every target agent already has shell/HTTP tooling, and Pip's references carry the exact schemas. Revisit only if real use shows agents failing to execute routes without a helper.
- **Skip: contact sheets and approved-folder promotion.** Pip already reports candidates for user selection, and SKILL.md's inspection-aid rule permits a clearly labeled review sheet assembled from PixelLab pixels when a host needs one.
- **Skip: worker-subagent briefs.** Pip must stay useful in agents without delegation; hosts with subagents can use them without a Pip contract.
- **Skip: runtime `doctor`, JSONL event logs, offline payload examples, `refresh-api-metadata` command.** Pip's QA runs repo-side in CI, reporting is per-run in chat/manifests, and OpenAPI is refreshed on demand — runtime self-diagnostics serve a bundled-script pipeline Pip does not have.
- **Reject: custom API base flag.** Official base only; a base override is an attack surface with no Pip use case.
- **Reject: `.env` loader.** Pip's credential policy deliberately keeps secrets in app settings/secret stores; a bundled loader would legitimize the riskier pattern.

## Runtime Reference Decision

A new runtime reference is added only when Pip gains a repeated workflow that cannot fit the existing files, never to match PixelLab AI Skill's reference count. That trigger fired once since the prior review: `references/blueprint.md` (the 23rd reference) for the replayable/shareable generation workflow, with a `blueprints/` folder. Pip's 23 runtime references cover its scope more deeply than the sibling in every shared area (routing, prompting, cost, jobs, layering, reporting, localization, credentials, blueprints). Remaining standing examples for a future reference or bundled tool are a real manifest runner or a dedicated local asset validator.
