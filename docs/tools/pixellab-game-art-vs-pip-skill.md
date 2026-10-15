# PixelLab Game Art vs Pip Skill

Initial review: 2026-10-14, against `pixellab-game-art` v1.3.0 at commit `601159dd2801ddc75c1320df596d0c3517683d78` and the PixelLab Pip working tree based on commit `4f7abb9f226d3b52684b2473cd6afc058a86a261`, with local changes already present. The Pip columns now also reflect the canvas-planning and offline-inspection follow-up described below; upstream remains pinned to the original review.

This compares PixelLab Pip with the unofficial [pixellab-game-art](https://github.com/lexingel/pixellab-game-art) skill by lexingel. It follows the comparison structure of [PixelLab AI Skill vs Pip Skill](pixellab-ai-skill-vs-pip-skill.md): summary, feature inventory, practical use cases, workflow tradeoffs, package inventory, and evidence limits. Its purpose is to help users choose between the skills. It does not compare generated art quality through new paid experiments.

Sources reviewed:

- The full upstream checkout, stored in the sibling `pixellab-game-art/` folder outside this repository. [Pinned source tree](https://github.com/lexingel/pixellab-game-art/tree/601159dd2801ddc75c1320df596d0c3517683d78).
- Upstream [README](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/README.md), [changelog](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/CHANGELOG.md), both distribution variants, task contracts, references, templates, installer, and helper source. Detailed evidence links appear below.
- Pip's [SKILL.md](../../skills/pixellab-pip/SKILL.md), relevant runtime references, blueprints, bundled helpers, installation documentation, and QA tooling. Pip comparisons describe the working tree at review time, including existing edits; they are not a claim about an immutable released package.
- Live [official MCP guide](https://api.pixellab.ai/mcp/docs), [REST v2 endpoint index](https://api.pixellab.ai/v2/llms.txt), and [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json), retrieved on the review date for selected capability and pricing checks. No account token, installer execution, live generation, or telemetry submission was needed.

## Summary

PixelLab Game Art is a project-oriented game-art production assistant. It combines task commands, persistent named styles, reference-art measurements, battle-animation recipes, VFX templates, local review/cleanup scripts, history, and engine-oriented export. Its default look comes from a side-view dark-fantasy project, but genre, density, palette, view, and timing can be overridden or learned from supplied art.

PixelLab Pip is an agent-agnostic routing and execution contract. It chooses between callable PixelLab MCP tools, public REST v2, visible website/editor workflows, Aseprite, Pixelorama, and legacy compatibility. Its operational depth includes image-role selection, asset-specific constraints, cost approval, remote-action safety, output integrity, localization, async lifecycle handling, reports, and portable blueprints.

Use Game Art when you want its saved-style project workflow, combat-animation finishing tools, and broader local production-helper suite. Use Pip when route accuracy, broader surface coverage, preservation of returned assets, explicit spending control, or portable workflow records are central. Pip also bundles a limited read-only image inspector. Both work across multiple agents; this is a workflow choice, not a Claude-versus-Codex distinction.

## Feature Inventory

Observable behavior and code, grouped by the decisions a user needs to make. A tool mention is distinguished from a dedicated operational workflow.

Legend: ✅ shipped as documented behavior or code · 🟡 partial or different-shaped equivalent · ❌ absent in the reviewed package. Source inspection does not establish live success or enforcement by an agent.

### PixelLab Surface Coverage

| Feature | PixelLab Game Art | PixelLab Pip |
|---|---|---|
| Hosted MCP routing | ✅ — primary generation surface; tool names support host prefixes | ✅ — MCP-first where supported, with explicit availability checks |
| REST v2 execution and REST-only capabilities | ❌ — acknowledges REST for integrations but excludes it from this skill's execution | ✅ — public REST fallback and exact-control routing |
| Website/editor, Aseprite, Pixelorama | ❌ — no corresponding execution workflows | ✅ — surface-specific contracts and permission boundaries |
| Characters, backgrounds, scenes, props, icons | ✅ — dedicated `pga-*` tasks | ✅ — asset-intent router and specialized references |
| Pro Flash | ✅ — preferred for single hero/foe sprites and key-pose edits | ✅ — explicit family routing, native-size checks, provisional cost checks; defaults remain evidence-dependent |
| Tilesets, road tiles, building kits, structured UI, fonts | 🟡 — routing table and selected parameter notes; no dedicated tasks for most of these | ✅ — router plus deeper operational contracts, especially tilesets and UI surface distinctions |
| Talking portraits and lip sync | 🟡 — tool-chain mention in API guide | ✅ — dedicated vocal-animation contract, including dialogue handling |
| PixelArt and VFX Workbenches | ✅ — both routed; VFX has a dedicated task and templates | ✅ — dedicated contracts for both, including live help and export verification |
| Cleanup/conversion tools | ✅ — names conversion, unzoom, correction, and color reduction | ✅ — public MCP/REST routes, image-role and native-grid guidance |
| Maps and platform/project helpers | 🟡 — map tools appear in API notes; not the main task workflow | ✅ — map intent and project/sandbox/chat/job-control contracts |
| Legacy v1 | ❌ — no execution path | ✅ — explicit legacy-only boundary |

Game Art's broader MCP coverage is visible in its [API guide](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/pixellab_api.md). Its smaller command menu does not mean tilesets, fonts, portraits, or cleanup tools are unknown to it. Pip's distinction is broader surface selection and more detailed operational guidance.

### Execution And Production Tooling

| Feature | PixelLab Game Art | PixelLab Pip |
|---|---|---|
| Bundled submit client | ❌ — agent calls MCP; Python helpers support the surrounding workflow | ❌ — host tools execute the selected public route |
| Download/poll helper | ✅ — `fetch.py` for raw MCP image/animation download URLs, bounded waits, frame indexes, logging | 🟡 — matching-getter/resume contract executed by host tools |
| Batch production | ✅ — CSV/TXT/list inputs, task grouping, queued jobs, QA and one contact sheet | 🟡 — approved batches and blueprints; no bundled batch runner |
| No-repeat / resume rules | ✅ — reuse logged matching calls and re-fetch pending jobs; failed/defective jobs can be retried automatically | ✅ — persist IDs and resume getters; new paid attempts require applicable approval |
| Cost preview and estimated-plan cap | ✅ — call plan, dry-run, project or per-command `max_cost`; not an enforced actual-billing ceiling | ✅ — whole-chain approval plan, budget-sensitive routing, `auto` toggle |
| Local job/outcome history | ✅ — JSONL job records, latest verdicts, search, totals by task/tool/day | 🟡 — per-run private manifests with IDs, seeds, and reported usage; no history-query helper |
| Workflow replay | 🟡 — `pga-reroll` reconstructs a past call with one change | ✅ — ordered, shareable MCP/REST and local-task blueprints |
| Runtime setup diagnostics | ✅ — `pga-doctor` plus package/profile checks | 🟡 — setup/readiness contracts; repository QA rather than a runtime doctor command |
| Per-task model/effort dispatch | ✅ — optional installer-generated subagents and `models.json` | ❌ — no bundled host-specific task/model dispatch |

Batching and rerolls are agent instructions rather than a standalone execution engine: see [pga-batch](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/tasks/pga-batch.md) and [pga-reroll](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/tasks/pga-reroll.md). Pip's corresponding contracts are [Job Lifecycle](../../skills/pixellab-pip/references/job-lifecycle.md), [Auto](../../skills/pixellab-pip/references/auto.md), [Usage Reporting](../../skills/pixellab-pip/references/usage-reporting.md), and [Blueprint](../../skills/pixellab-pip/references/blueprint.md).

### Prompting, Style, And Input Handling

| Feature | PixelLab Game Art | PixelLab Pip |
|---|---|---|
| Prompt preparation | ✅ — subject/layout/detail/style/palette sequence with category templates | ✅ — visual-content-only English preparation, supported controls, exact-field preservation |
| Persistent named project styles | ✅ — `pixellab.json`, active style, per-call selection, CRUD, family anchors | 🟡 — consistency anchors and recorded inputs, without a named-style manager |
| Analyze supplied PNG/GIF/folder into style rules | ✅ — local metrics plus agent visual interpretation and user-reviewed saved rules | 🟡 — bundled dimensions/alpha/bounds and GIF timing/loop measurements plus style/palette routing; no style inference, folder discovery, or measurement-to-profile tool |
| Genre/density presets | ✅ — ten named genres, arbitrary setting text, low/mid/high density, user precedence | 🟡 — user-led intent and constraints rather than a preset style system |
| Seed defaults | ✅ — fixed family seed, default 7, changed for rerolls | ✅ — omit by default; user seed or shared seed for a composition-lock attempt |
| Negative-prompt approach | ✅ — house/category exclusions, with conflicting exclusions removed for user requests | ✅ — targeted exclusions and route-specific field availability; no generic boilerplate |
| Image-role classification | 🟡 — style anchors, supplied sprite, first/last frames, references | ✅ — dedicated endpoint-specific role classification |
| Localization and exact dialogue | ❌ — no dedicated localization contract | ✅ — translation approval and preservation of talking dialogue |
| Offline examples | ✅ — category prompt library and VFX JSON templates | ✅ — specialized references and example blueprints |

The [parameter contract](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/parameters.md) makes the house style a fallback, not a requirement. Named styles are managed by [style.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/style.py). [pga-analyze](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/tasks/pga-analyze.md) connects measurements to rules; those measurements are heuristics, not proof that a new generation will reproduce the style.

### Animation, VFX, And Layered Assets

| Feature | PixelLab Game Art | PixelLab Pip |
|---|---|---|
| Combat key-pose recipe | ✅ — padded canvas, wind-up and hit edits, interpolation, hold timing, optional slash layer | 🟡 — motion-aware canvas planning, first/last/custom-start-frame routes and verification, without that packaged combat finishing pipeline |
| Local combat finishing | ✅ — flash cleanup, trail recoloring, slash extraction, ground alignment, mirrored directions | 🟡 — permitted assembly/inspection; altered final art requires approval |
| Preset/template/skeleton animations | 🟡 — named tools, example template IDs, and selected parameters | ✅ — dedicated template/skeleton catalog and constraints |
| Walk/idle/death guidance | ✅ — house recipes and timing | ✅ — route-dependent guidance, returned-frame preservation, idle-loop artifact warnings |
| VFX templates | ✅ — strike, party wave, eruption, recolored via ramps | ✅ — VFX parts/presets and replayable effect blueprints; different recipe selection |
| Multi-shot cinematic chains | ❌ — no dedicated workflow | ✅ — budgeted shot planning, handoffs, per-shot validation |
| Paperdoll layers and layer-vs-composite distinction | ❌ — no dedicated paperdoll contract | ✅ — layered edits/extraction, alignment constraints, honest output labeling |
| Engine-oriented sprite export | ✅ — PNG sheet, Aseprite-format JSON, optional Godot SpriteFrames resource | 🟡 — host assembly and Aseprite import/export; no bundled generic sprite-to-engine exporter |

Game Art's combat workflow is described in [pga-anim](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/tasks/pga-anim.md) and its [animation reference](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/animation.md). Pip covers overlapping primitives in [Animation](../../skills/pixellab-pip/references/animation.md) and [Local Asset Assembly](../../skills/pixellab-pip/references/local-asset-assembly.md), with separate [Paperdolling](../../skills/pixellab-pip/references/paperdolling.md), [Cinematic](../../skills/pixellab-pip/references/cinematic.md), and [VFX Workbench](../../skills/pixellab-pip/references/vfx-workbench.md) contracts.

### Output Handling, Credentials, And Distribution

| Feature | PixelLab Game Art | PixelLab Pip |
|---|---|---|
| Advisory image QA script | ✅ — empty/alpha/edge/palette/animation-flash flags, flagged sheet | 🟡 — read-only all-frame decoder with optional exact size/count checks, plus route-specific and visual verification; no heuristic quality verdicts or flagged sheet |
| Contact sheets and GIF previews | ✅ — bundled scripts, half-size review strategy, combat timing/VFX preview | ✅ — host assembly, spritesheet/GIF previews and grid inspection requirements |
| Pixel integrity | 🟡 — reports cleanup but routinely modifies colors, alignment, and selected frames | ✅ — PixelLab/user pixel origin, approval for altered final assets, failed verification disclosed |
| Reporting | ✅ — beginner summary, detailed batch table, logs and outcomes | ✅ — exact inputs, route, outputs, reported usage, verification, manifest and blueprint |
| Completion sound | ❌ | ✅ — configurable bundled bark helper |
| Token setup | ✅ — `PIXELLAB_TOKEN` in any-agent instructions; token never requested in chat | ✅ — `PIXELLAB_SECRET`, secret-source boundaries, token-free setup previews |
| Browser-token/private-endpoint boundary | 🟡 — MCP-only workflow reduces exposure; no equivalent detailed credential contract | ✅ — explicit prohibitions and public-surface boundaries |
| Remote destructive-action gate | ❌ — no equivalent global gate found | ✅ — approval and exact scope for deleting/replacing existing remote content |
| Local outcomes shared with authors | ✅ — opt-in off/stats/prompts controls, preview/forget and machine-level disable | ❌ — no analogous outcome-sharing client |
| Cross-agent distribution | ✅ — any-agent package plus Claude task skills and optional subagents | ✅ — portable skill plus multiple app/plugin manifests |
| Update handling | ✅ — version check, backup, edited-file conflict copies, undo, offline ZIP | ✅ — installed-skill/plugin update contract and repo/app helpers; different update mechanism |
| License | ✅ — MIT | ✅ — MIT |

Game Art's [shared task loop](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/prompt_improver.md) defines reporting, automatic defect retries, and outcome recording. The [any-agent README](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/README.md) documents setup and sharing. Pip's detailed boundaries live in SKILL.md and [Credentials](../../skills/pixellab-pip/references/credentials.md).

## When To Use PixelLab Game Art Instead

Choose Game Art when these are the workflow you actually want:

1. **A first game-art project with guided steps.** `pga-start` suggests starter assets, explains generations and waits, offers cheap drafts, and introduces reference anchors. Its [starter task](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/tasks/pga-start.md) includes draft-to-production choice points even though the global paid-call policy avoids confirmation prompts.
2. **Several reusable looks in one project.** Save and switch named styles, keep separate hero/monster/background anchors, and apply an alternate style to one call without changing the active project style.
3. **Learning rules from existing pixel art.** Analyze a PNG, GIF, or folder for native scale, palette, outline, shading/dither/light heuristics, and animation timing; let the agent interpret the look and save reviewed rules.
4. **Side-view combat moves with a known finishing recipe.** Produce padded wind-up/hit poses, interpolate, review/clean frames, set damage timing, and export the move for a game. This assumes the user accepts that recipe's local transformations and cost policy.
5. **A broad local production-helper suite.** Use its QA, contact-sheet, palette, padding, finishing, preview, and export scripts with their Python dependencies. Pip's bundled inspector covers objective frame facts and explicit size/count checks; most other local operations use host tools.
6. **A project history browser.** Search prior results and verdicts, aggregate recorded costs, and reroll one previous step with one change.
7. **Optional per-task agent dispatch.** Install host-specific task agents with configurable model/effort tiers. Actual savings depend on host support and model configuration; a cheaper model is not automatically configured for every host.

These features make Game Art convenient for an ongoing asset roster and combat-art workflow. They do not establish better art quality, lower total cost, or coverage of every possible engine import.

## When To Use Pip Instead

Choose Pip for supported-surface decisions and execution across MCP, REST, the website/editor, and Aseprite; REST-only controls; or work that needs detailed tileset, paperdoll, cinematic, vocal-animation, image-role, or localization guidance.

Pip also fits a workflow where extra paid attempts, remote overwrites, palette changes, mirroring, or removal of returned frames must remain explicit decisions. Its `auto` option can remove the initial cost pause when selected, while preserving destructive-action boundaries and applicable budget/retry rules.

For sharing or recreating a whole workflow, Pip's blueprint is an ordered portable record rather than a query against one project's job log. For a host without the Game Art image-helper dependencies or task-agent setup, Pip's routing guidance remains usable through the host's existing tools.

| User request | Better fit | Why |
|---|---|---|
| “Learn this game's GIF style and save separate town and dungeon looks.” | Game Art | Measurement-to-profile workflow and named style management |
| “Make this knight's axe attack and export damage timing for Godot.” | Game Art | Packaged combat recipe and sprite export metadata |
| “What did I generate last week, and reroll the rejected helmet?” | Game Art | History search, verdicts, and call-level reroll workflow |
| “Choose the public API route for my server-side asset generator.” | Pip | REST v2 and MCP are distinguished by intent and surface |
| “Give me separate transparent armor layers for this animated character.” | Pip | Paperdoll contract and layer/composite verification |
| “Build a connected terrain set with precise transition behavior.” | Pip | Dedicated tileset controls, sizing and assembly guidance |
| “Make a budgeted multi-shot scene, then share how it was made.” | Pip | Cinematic validation and ordered portable blueprint |
| “Generate some matching icons or a spell effect.” | Either | Both route and review these; choose based on project-style tooling versus Pip's boundaries |

## Named Styles vs Blueprints And Manifests

A Game Art **style profile** describes how future art should look: named rules, sizes, palette, facing, timing, and approved family anchors in `pixellab.json`. It is reusable project state. Its **history log** describes earlier jobs and their latest keep/reroll/reject outcomes; a reroll asks the agent to reuse one record's parameters with a deliberate change.

A Pip **manifest** keeps private audit/resume data, including job/result IDs, seeds, and exposed per-call usage. A **blueprint** captures exact requests and material local tasks in order, with connection metadata and relative supporting inputs. It can describe a whole multi-step workflow and be replayed with overrides in another agent.

The overlap is consistency and reproducibility. The distinction is persistent art direction versus an audit file and portable workflow record. A named style is not a successful request log; a blueprint is not a named-style catalog. Neither a recorded seed nor a saved style guarantees deterministic provider output.

## Spending And Output-Integrity Tradeoffs

Game Art shows the call plan and estimated cost before submitting, supports dry runs and caps, and instructs the agent to reuse completed matching jobs. It also allows one automatic retry for a failed job or hard defect. Beginner flows can pause for a draft choice. Therefore “never repeat a call” is a reuse/resume principle with retry exceptions, not a guarantee that a request will spend only once.

Pip defaults to approval of the complete paid chain before generation. Additional paid attempts outside the approved plan require applicable approval; failed output is reported honestly. `auto` changes the initial spending gate, not every other safety boundary.

Game Art's local finishing tools intentionally change generated art: quantize colors, remove flashes, recolor trails, align feet, choose/drop frames, extract slash pixels, and mirror selected directions. This is useful production machinery when those operations match the user's intent. Pip permits assembly and inspection of existing pixels but requires approval before altered output is represented as final, and preserves returned animation order/count unless the user requests a different playback treatment.

## Helper Implementation Limits

These limits matter when choosing a packaged workflow; they are source-review findings, not reports of live failures.

- **Download helper scope:** [fetch.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/fetch.py) polls raw MCP image download URLs, including indexed frames. It does not submit paid jobs or implement the full managed-character/object/tileset lifecycle. It deduplicates completed log entries by job ID. Its late-404/410 failure handling and caller-provided cost metadata do not independently verify refunds or actual billing; history totals are only as accurate as the supplied log values.
- **Advisory QA:** [qa.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/qa.py) flags heuristics and exits successfully even when assets are flagged. Palette distance is not a semantic identity check; edge pixels do not prove clipping. Animation dimension checking occurs on intermediate frames, not a complete first-to-last validation. Agent review remains necessary.
- **Engine export:** [make_sheet.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/make_sheet.py) writes frame rectangles/durations and optional pad/facing/hit metadata. Its Godot resource uses a basename `res://` texture path and exports a non-looping animation. Project placement may require a path adjustment. Unity and other engines mainly receive generic files and import instructions, not native adapters. No engine-import test was run here.
- **Preview behavior:** [preview_gif.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/preview_gif.py) adds a standing-pose beat, scales the preview, and uses an opaque inspection background with disposal 1. It is a review visualization, not a transparent faithful copy of the returned frame sequence. Pip separately requires transparent-preview disposal and rendered-frame verification.
- **Update behavior:** [update.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/update.py) uses recorded hashes, backup/undo, and conflict copies for changed files. Conflict resolution is left to the agent. A raw installer rerun replaces the skill; it is not the same preservation path as `pga-update`. [check_setup.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/check_setup.py) can trigger a weekly version lookup, independently of outcome-sharing consent; a separate environment switch disables that lookup.

## Coverage Freshness And Evidence Quality

Game Art's MCP guide is dated 2026-10-12; its release series is dated 2026-10-14. It covers recent Pro Flash and workbench tools, so it should not be treated as an old MCP-only list. However, it contains both an instruction that measured house settings win over docs and a later instruction that live tool definitions win. Tool schemas must resolve accepted parameters; project-specific observations need separate verification.

Selected checks against current official sources:

- The MCP guide documents **VFX Workbench as free for subscribers**. Game Art also describes broad free-trial/all-plan operation. Access on a particular trial or credits-only account was not checked; do not equate zero generation cost with universal eligibility.
- Official template-animation pricing includes **size-dependent batches**, not a universal one generation per direction. Game Art's short template notes omit that qualification.
- Official v3 character guidance allows **quadrupeds with a south-facing reference and matching template**; the from-scratch generator is humanoid-only. Game Art's short “humanoid-only” comparison should be read in that narrower context.
- Official `get_pro_flash_capabilities` documents sizes, controls, and output counts. Its signature is not evidence that it returns a price quote. REST separately exposes `/pro-flash/cost`; Pip distinguishes that provisional estimate from reported usage.

These checks use the [official MCP guide](https://api.pixellab.ai/mcp/docs) and [REST schema](https://api.pixellab.ai/v2/openapi.json). They do not re-verify every upstream price, wait time, subscription limit, or historical observation.

Game Art publishes aggregate usage counts, cost observations, and tested prompt recipes in [stats.md](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/stats.md), [costs.md](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/references/costs.md), and the category libraries. These are the author's observations from one project; the underlying complete call logs, images, account receipts, and controlled benchmark were not supplied in the reviewed package. In particular, Pro Flash size-tier prices, automatic refunds, quality rankings, and cost formulas remain attributed observations rather than independently measured results of this spike.

The changelog describes a planned weekly feedback/update process. All versioned entries reviewed here are dated the same day, so the checkout does not establish a history of weekly maintenance or demonstrate that shared outcomes already improved results.

## Secret Setup And Sharing Tradeoffs

Game Art's any-agent setup uses `PIXELLAB_TOKEN` and instructs users to enter their token outside chat; some host examples also permit literal bearer headers. Its installer can add task agents and image dependencies, while actual generation remains in connected MCP tools. Pip uses `PIXELLAB_SECRET`, provides explicit secret-source/config-write boundaries, and does not ship a comparable image-production installer.

Game Art's outcome sharing is off by default. [share.py](https://github.com/lexingel/pixellab-game-art/blob/601159dd2801ddc75c1320df596d0c3517683d78/any-agent/pixellab-game-art/scripts/share.py) implements opt-in levels, preview, deletion requests, and a machine-level disable. Stats sharing includes allowlisted settings and style summaries; prompts sharing also includes textual prompts/reasons that may contain user-written names. The intended payload excludes credentials, images, file paths, and raw job IDs. However, QA strings are agent-provided and passed through without the parameter/style allowlist filtering, so the client does not establish a blanket guarantee that arbitrary text is sanitized. The remote service's retention/deletion behavior was not audited; a client delete request is not independent evidence of server deletion.

Pip has no analogous author-operated outcome-sharing channel. Its private manifest and portable blueprint serve local audit and replay rather than a shared telemetry loop.

## PixelLab Game Art Package Inventory

The reviewed repository contains two distributions of the same core workflow:

- `any-agent/`: one `pixellab-game-art/SKILL.md`, 20 task Markdown files under `references/tasks/`, project `AGENTS.md`, README/setup/changelog, installer, and model configuration.
- `claude-code/`: the core skill plus 20 separate `pga-*` task skills, README/setup/changelog, and installer.
- Each core skill contains 23 Python helpers, three VFX JSON templates, `VERSION`, ten category-library files, and ten other reference Markdown files. The any-agent variant additionally carries its task references inside the core skill.
- Root README, setup dispatcher, changelog, license, and ignore rules. No repository test directory or CI workflow was found in the tracked inventory; selected helpers contain self-test modes.

Helper groups:

| Area | Files |
|---|---|
| Setup/update | `check_setup.py`, `update.py` |
| Upload/download | `upload.py`, `fetch.py` |
| Project/style | `profile.py`, `style.py`, `analyze_style.py` |
| QA/review/export | `qa.py`, `contact_sheet.py`, `pad_sprite.py`, `preview_gif.py`, `make_sheet.py` |
| Combat/palette finishing | `apply_palette.py`, `scrub.py`, `ground_snap.py`, `find_muzzle.py`, `recolor_trail.py`, `slash_layer.py`, `dir8_finish.py` |
| History/outcomes/sharing | `history.py`, `cost_report.py`, `outcome.py`, `share.py` |

## Pip Follow-Up: Canvas Planning And Offline Inspection

Pip's existing [Animation](../../skills/pixellab-pip/references/animation.md) reference now plans transparent padding when a supplied raw sprite's requested motion needs space beyond its canvas. It preserves source pixels and placement offsets, keeps anchor canvases aligned, honors fixed requested dimensions, and rechecks route limits and cost after padding. This applies to motion generally; it does not adopt Game Art's complete combat recipe or claim padding guarantees unclipped output.

Pip also adds [inspect_images.py](../../skills/pixellab-pip/assets/inspect_images.py), documented in [Local Image Inspection](../../skills/pixellab-pip/references/local-asset-assembly.md#local-image-inspection). It decodes every frame from explicitly ordered files and reports dimensions, alpha extrema, nonzero-alpha bounds, and observed GIF duration/loop metadata as JSON on stdout. Optional expected dimensions and total decoded-frame count produce explicit failures alongside decode errors. Missing GIF timing remains unknown rather than receiving an invented playback default. The helper writes no files, makes no network calls, and uses Pillow, already used by Pip's background-removal helper and repository QA.

There is existing demand for these measurements: the [cinematic spike's validation methodology](../pixellab/pixellab-cinematic-spike.md#validation-methodology) checks count, canvas, and alpha for every job; the [aura](../../skills/pixellab-pip/blueprints/aura.blueprint.json), [knight](../../skills/pixellab-pip/blueprints/knight.blueprint.json), and [turntable](../../skills/pixellab-pip/blueprints/turntable-rotate-16.blueprint.json) blueprints also record frame-verification requirements. A correct host script can perform the same checks; the helper provides one reusable implementation with all-frame decoding and consistent error reporting. No speed or generation-cost advantage was measured.

Offline synthetic fixtures in [test_image_inspection.py](../../tests/test_image_inspection.py) cover:

- Opaque, palette-transparent, partially transparent, and empty images, with unchanged input hashes and no added output files.
- Explicit input order and duplicate paths; size checks through a multi-frame file's final frame; total decoded-count mismatches.
- GIF variable durations, zero versus absent delays, finite/infinite/absent loop metadata, and late-frame corruption followed by another valid input.
- Invalid explicit expectations and nonzero exits for decode or expectation failures.

These are structural checks, not proof that art meets the request. Empty frames may be intentional, edge contact does not prove clipping, and alpha does not establish correct background removal. The helper does not compare source pixels, infer style or native scale, diagnose flashes/drift, repair art, or trigger retries. It also does not verify GIF disposal: the separate metadata, coalescing, and source-frame comparisons in Local Asset Assembly remain necessary. No paid combat comparison or engine-import experiment was performed.

## Review Scope And Verification

The initial comparison was a read-only review of upstream source plus a documentation change in Pip. The follow-up adds Pip's canvas-planning rule, a local inspector, its runtime documentation, and synthetic regression fixtures. No upstream skill was installed, no third-party helper script was executed, no credentials were inspected, no art was generated through PixelLab, and no outcome was sent to its authors. The comparison describes shipped instructions/code and identifies where claims require live verification. It does not certify upstream helper reliability, model quality, privacy-service behavior, or engine compatibility.

Pip's repository validation command is `python dev-tools/qa.py`, which includes the unit tests. Future upstream changes or changes to Pip's working tree require refreshing the comparison rather than assuming these findings remain current.
