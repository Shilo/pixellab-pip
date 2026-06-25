# PixelLab AI Skill Comparison

Last reviewed: 2026-06-24.

This compares PixelLab Pip with the unofficial [PixelLab AI Skill](https://clawhub.ai/uncmatteth/skills/pixellab-ai) on ClawHub. The goal is to understand adjacent tooling, not to copy its implementation.

Sources reviewed:

- [ClawHub PixelLab AI Skill page](https://clawhub.ai/uncmatteth/skills/pixellab-ai).
- [ClawHub package metadata](https://clawhub.ai/api/v1/packages/pixellab-ai).
- [ClawHub version metadata](https://clawhub.ai/api/v1/packages/pixellab-ai/versions).
- [ClawHub v1.5.1 file metadata](https://clawhub.ai/api/v1/packages/pixellab-ai/versions/1.5.1).

## Summary

PixelLab AI Skill is a production-workflow skill for creating PixelLab asset packs with helper scripts, manifests, recipes, contact sheets, candidate approval, cost preflights, downloads, and validation.

PixelLab Pip is a compact, agent-agnostic routing assistant. Pip helps an agent choose the right PixelLab surface: hosted MCP, REST v2, website/editor workflows, Aseprite, Pixelorama, SDK/API docs, or legacy v1.

Use PixelLab AI Skill when you want its packaged recipe/script workflow. Use Pip when you want lightweight route selection, API/MCP guidance, auth and language boundaries, and concise PixelLab decision support across agent apps.

## Feature Comparison

| Area | PixelLab AI Skill | PixelLab Pip |
|---|---|---|
| Primary goal | Asset-production workflow for PixelLab jobs. | Agent-agnostic PixelLab route selection and execution guidance. |
| Distribution | ClawHub skill with OpenClaw-oriented install instructions. | Multi-agent plugin/skill repo with Claude, Codex, Cursor, Copilot, VS Code, Gemini, and manual skill paths. |
| Invocation scope | Explicit PixelLab / pixellab-ai workflow help. | PixelLab asset/API requests, explicit `/pixellab-pip`, and implicit PixelLab-specific tasks. |
| Secret name | Uses `PIXELLAB_API_KEY`. | Uses `PIXELLAB_SECRET` for local setup; calls the runtime auth value a PixelLab bearer token. |
| Secret setup pattern | Teaches repo-local `.env.local` setup and helper auto-load behavior. | Avoids `.env*` by default; prefers app secret settings, secret stores, or user-scoped environment setup with token-free previews. |
| Live generation | Provides helper commands for REST calls, polling, downloads, and output files. | Calls MCP/REST only when configured and appropriate; otherwise gives the selected route or minimal call shape. |
| REST helpers | Bundles `pixellab_client.py` and `pixellab_workflow.py` for REST calls, polling, manifests, and local files. | Does not bundle REST client scripts; prefers MCP when available or direct REST guidance. |
| Examples | Includes endpoint example JSON files for image, character, object, animation, tiles, UI, inpaint, resize, remove-background, prompt enhancement, rotation, interpolation, outfit transfer, and tags. | Does not bundle endpoint payload examples; refreshes official REST/MCP docs when exact schemas matter. |
| Recipes | Bundles recipe JSON for platformer packs, modular RPG characters, sidescroller tilesets, UI HUD packs, and enemy variants. | Does not bundle production recipes; routes each request to the right PixelLab surface. |
| Manifests | Plans dry-run manifests, lints them, budgets them, runs them, and resumes jobs. | No manifest system; keeps one-off or task-specific workflows concise. |
| Candidate review | Uses contact sheets, candidate folders, approval steps, and final asset promotion. | Reports candidate/final status after live calls; does not manage an approval directory workflow. |
| Output folders | Defines folders such as payloads, results, candidates, approved, downloads, reports, and logs. | Does not prescribe project output folders except reporting returned paths/URLs. |
| Prompt preparation | Turns rough ideas into visual briefs and PixelLab-ready prompts. | Enhances natural-language request parameters unless the user opts out, using PixelLab enhance endpoints only when route-matched. |
| Localization / non-English requests | No dedicated localization reference was found in the reviewed package inventory. | Translates or normalizes PixelLab-facing natural-language values to English and keeps user-facing replies in the user's requested or detected language. |
| Consistency gate | Uses visual briefs, seed/reference planning, and seed candidate review for packs. | Summarizes identity, style, palette, view, and reference anchors; asks up to three blocking questions before credit-spending calls. |
| Image input handling | Encourages seed/reference images and init images for consistency. | Classifies supplied images by endpoint role: subject, identity, style, concept, init/source, target, mask, palette, or frame. |
| Paperdolling | Includes modular outfit/equipment concepts and layered sprite validation. | Documents PixelLab layer limitations and routes paperdolling as a composition workflow outside PixelLab. |
| MCP strategy | Treats MCP as optional and often favors its REST helper workflow for bulk production. | Favors hosted MCP for managed PixelLab assets when tools are available; uses REST v2 for exact API/code/batch primitives. |
| Website/editor surfaces | Mostly focused on API/helper workflow. | Explicitly covers website/editor, Aseprite, Pixelorama, and website-only/manual flows with permission boundaries. |
| SDK guidance | Focused on helper scripts and endpoint use. | Warns not to assume SDK parity; refreshes official docs or installed packages when SDK coverage matters. |
| Unsupported endpoints | Uses its own endpoint/reference coverage matrix. | Keeps route warnings in `SKILL.md` and runtime references; refreshes official docs for current schemas. |
| Usage reporting | Reports endpoint, results, downloaded assets, costs, and errors. | Reports surface, tool/endpoint, prompt prep, final parameters, IDs, paths/URLs, polling/status, balance delta, and verification status. |
| Validation | Includes asset inspection and sprite validation commands. | Requires checking existence and requested constraints before calling an output final; no bundled validator scripts. |
| Subagents | Recommends worker subagents for live API calls. | Does not require subagents; stays portable across agents. |
| External/community references | Lists YouTube and Discord workflow references. | Uses official PixelLab docs and local technical notes; avoids community-derived claims unless separately reviewed. |

## Secret Setup Tradeoff

PixelLab AI Skill is more operational out of the box because its helper scripts can auto-load `PIXELLAB_API_KEY` from `.env.local`. That is convenient for a REST helper workflow, but it teaches agents and users to rely on a file pattern that often contains unrelated private project secrets.

Pip intentionally avoids `.env*` files by default. Its setup flow should use `PIXELLAB_SECRET` through app secret settings, a secret store, or a user-scoped environment setting, and should inspect `.env*` only when the user names an exact file and explicitly approves inspection. This is less automatic today, but it is safer for mixed projects where `.env.local` may contain database URLs, cloud keys, or other private tokens.

### How PixelLab AI Skill Loads `.env.local`

PixelLab AI Skill's `.env.local` behavior is helper-driven. Its documented setup stores `PIXELLAB_API_KEY` in a repo-local `.env.local`, and its helper scripts auto-load that file before making REST calls. The assistant, terminal, operating system, and MCP client do not load `.env.local` by themselves.

If Pip adopts a similar helper later, it should be an explicit loader/wrapper behavior: load only the PixelLab key it needs, prefer `PIXELLAB_SECRET`, never print loaded values, and continue treating app secret settings, secret stores, or user-scoped environment settings as the default path.

## PixelLab AI Skill Package Inventory

The reviewed v1.5.1 package contains:

- `_meta.json`, `SKILL.md`, `skill-card.md`, `agents/openai.yaml`, and two OpenClaw config examples.
- Two Python helper scripts: `scripts/pixellab_client.py` and `scripts/pixellab_workflow.py`.
- Five recipe JSON files.
- Thirty-eight endpoint example JSON files.
- Nine reference Markdown files:
  - `api-coverage-matrix.md`
  - `endpoint-mapping.md`
  - `prompt-cheatsheet.md`
  - `sprite-animation-layering.md`
  - `youtube-workflow-playbook.md`
  - `community-discord-workflows.md`
  - `community-discord-tutorials.md`
  - `install-and-secrets.md`
  - `official-youtube-index.md`

Notable `pixellab_workflow.py` commands include `list-recipes`, `plan`, `run`, `budget`, `retry-manifest`, `repair-placeholders`, `gallery`, `inspect-assets`, `validate-sprites`, `lint-manifest`, `contact-sheet`, `cost-summary`, `approve-candidate`, `balance-preflight`, `refresh-api-metadata`, `doctor`, and `subagent-brief`.

## Useful Ideas For Pip

- Keep prompt preparation opt-out, not opt-in.
- Keep PixelLab-facing natural-language parameters in English while preserving the user's language for replies.
- Summarize consistency anchors before spending credits.
- Report the route, parameters, IDs, outputs, status, and usage details after live calls.
- Treat MCP as configured-or-not; never pretend tools exist.
- Preserve paperdoll frame-grid contracts and distinguish composited outputs from reusable layers.

These ideas are already covered in Pip through `SKILL.md`, `references/localization.md`, `references/image-input-roles.md`, `references/paperdolling.md`, and `references/usage-reporting.md`.

## Ideas Not Adopted

- Do not copy PixelLab AI Skill's helper scripts, recipes, manifest workflow, or folder contract. Those are a separate production pipeline.
- Do not add a bundled REST client unless repeated use proves agents need one.
- Do not adopt `.env.local` as Pip's default secret setup path; use it only as an explicitly approved fallback if a future helper needs project-local configuration.
- Do not require worker subagents; Pip should stay useful in agents that do not support delegation.
- Do not replace Pip's bearer-token naming with `PIXELLAB_API_KEY`; Pip's README uses PixelLab's user-facing "secret token" wording, while the runtime skill uses bearer-token terminology.
- Do not add community tutorial or Discord-derived claims to runtime references without separate public-source review.

## Runtime Reference Decision

No new `skills/pixellab-pip/references/*.md` file is needed just because PixelLab AI Skill has more references. Pip already has the runtime references that match its scope:

- `image-input-roles.md` for role classification and prompt facts from attachments.
- `localization.md` for non-English request translation and response-language handling.
- `paperdolling.md` for layered character and equipment workflows.
- `usage-reporting.md` for live-call reporting and final-output checks.
- `official-pixellab-documentation.md` for current PixelLab documentation refresh.
- `tilesets.md`, `credentials.md`, and `browser-fallback.md` for focused edge cases.

Add a new runtime reference only when Pip gains a repeated workflow that cannot fit concisely in the existing files, such as a real manifest runner, a validated showcase recipe format, or a dedicated local asset validator.
