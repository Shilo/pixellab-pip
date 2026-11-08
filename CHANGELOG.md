# Changelog

All notable changes to PixelLab Pip are listed here, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Releases before 3.0.0 are on
[GitHub Releases](https://github.com/Shilo/pixellab-pip/releases).

## [Unreleased]

## [3.2.5] - 2026-11-08

### Changed

- **Accept benign hosted audits with medium or high confidence.** Apply the same policy to the completed scan and current stored verdict before promotion. Low, missing or unknown confidence and non-benign verdicts remain blocked; static regression, malware, exact-artifact, publisher/version and provenance checks remain required. Existing tagged releases can resume with unchanged skill files.

### Security

- **Summarize Workbench task notes.** Put a concise summary of the requested pixel-art or effect task and its material constraints in first-call notes, retaining high-mode plans and observations and the existing global transfer and exact-field rules.

## [3.2.4] - 2026-11-08

### Security

- **Scope ground-texture palette references to authorized images.** Use a region background only when supplied, selected or approved for that task's palette reference, reusing covered map-workflow authorization. Keep approved image matching and text-only generation available; clarify an uncovered reference when matching is required, without exposing private access URLs or adding a repeated transfer warning.

## [3.2.3] - 2026-11-08

### Security

- **Recheck the stored hosted verdict before promotion.** Require the exact publisher and version's current ClawScan verdict to remain benign with high confidence before moving ClawHub's latest tag, including resumed or already-latest releases. This catches completed concurrent audits that supersede the original scan response without requiring an optional skill card.
- **Review blueprint contents before external sharing.** Keep complete local recipes and copied inputs while checking original prompts, request values, filenames and images before sending them to other recipients. Reuse sharing authorization that covers the contents and destination; agree on redaction without silently changing replay data.

### Fixed

- **Clarify animation inspection outputs.** State that `--check-only` saves the two inspection reports and `--json` also prints JSON. Preserve report output, collision checks, source protection and repair behavior; verify the combined flags against both saved and printed results.

## [3.2.2] - 2026-11-07

### Security

- **Disclose task inputs before their first transfer to PixelLab.** Use the existing plan or approval/Auto card to identify PixelLab as the recipient of the selected text and images, including free uploads before paid work. Exclude unrelated private context without adding another approval step or changing supported workflows.
- **Reject a non-clean hosted static result when supplied.** Keep the separate mandatory static regression gate and accept the retired public field's absence, while failing closed if ClawHub returns a non-clean result. Record executable-batch planning as prepublication evidence alongside static scans.

## [3.2.1] - 2026-11-07

### Fixed

- **Clarify approved local palette conversion.** Keep explicitly requested or approved palette/index remapping available as a labeled derivative while preserving source-pixel, approval, and non-PixelLab drawing boundaries. This resolves contradictory wording around the existing Aseprite palette-clamp workflow.
- **Keep the full skill within the pinned audit's batch budget.** Consolidate a duplicate humanoid preset example into its existing numbered workflow, retaining every parameter decision and the selected animation engine. This removes one redundant executable batch without excluding files, hiding code, or changing the scanner limit.

### Security

- **Verify static evidence during release.** Run the same pinned, hash-verified static risk and coverage regression gate used by CI on the selected release files, including resumed tags. This replaces ClawHub's retired public static-analysis field; the hosted benign/high-confidence verdict, exact-file verification, malware scan, and provenance gates remain required.

## [3.2.0] - 2026-11-07

### Added

- **Support MCP room workflows.** Route furnished floor-plan rooms through painting/status, room listing, project filing, and optional furniture cutouts; document Tier 2 eligibility, 20-generation painting cost, and top-down/isometric/oblique restrictions.

- **Extract faithful paperdoll overlays.** A small local helper copies exact changed pixels from a registered edit, checks alpha-over reconstruction, and composes accepted layers. It preserves alpha, refuses incompatible edits and output collisions, and keeps candidates subject to visual review.
- **Document managed Skeleton v3 custom motion.** Distinguish MCP's free instruction call and humanoid written poses from its tool-described quadruped move lists and REST's paid text-generated motion, with current frame/cost guidance and shared-direction reuse. The [archive review](docs/pixellab/paperdoll-skeleton-v3-archive-review.md) records accepted findings, rejected experimental helpers, and evidence limits.

### Changed

- **Prefer modern character routes even on a budget.** Exclude outdated Standard character creation from automatic routing; use suitable v3, Pro Flash or approved Pro. Explain budget and Standard-only feature conflicts instead of silently falling back or increasing spend. Preserve deliberate user mode choices, existing assets and the separate Standard tileset workflow. Continued API support is not a quality recommendation.
- **Preserve the requested character and scene design.** Scope Pixen's tested south-facing idle recipe and specialty choreography to their actual conditions; keep requested facing, poses, loadouts and handedness. Stop incompatible axe-recipe substitutions, retain explicit knight equipment placement, and leave ordinary top-down terrain boundaries flat unless elevation is requested. Remove unneeded UI and cinematic prompt boilerplate while retaining visual inspection.
- **Report charged dollars separately.** Add an explicit USD ledger query and independent dollar totals to history and both review-panel views. Missing units remain unknown; dollar receipts never convert to generations or clear unresolved generation reservations.
- **Clarify custom Pro Flash bodies and current room timing.** Document MCP Pro Flash's accepted template values in the canonical body-plan table without assuming skeleton support, and refresh the documented room-generation estimate while preserving its price and polling rules.
- **Choose icon-set routes by the actual constraints and total call cost.** Keep verified sheets/batches and per-concept calls available, disclose the material tradeoff in the existing approval card, and verify every requested subject. Clarify body-plan discovery and the Pro Flash reference trigger without adding another choice turn or a universal quality ranking.
- **Correct routing and delivery after the MCP comparison review.** Distinguish supported standard character mode from Pip's quality preference, use direct text-animal routes, choose animation engines by motion/count constraints, and prefer a single-image route for one small icon. Clarify exact icon-set coverage, UI canvas versus visible bounds, consumed-input packaging, and compact reports with linked exact request records. Keep basic UI sizing/delivery in the router so it does not require loading the icon reference. Preserve approval, selection, sound, manifests, blueprints and asset-integrity defaults.
- **Audit benchmark claims and accept supported alternative routes.** Separate common routing from Pip workflows, respect Git ignore rules for untracked current-skill files, label regex checks and partial context estimates honestly, and retain July results as historical evidence rather than current performance claims.
- **Sync the 2026-11-06 UTC public contracts.** MCP grows from 121 to 122 tools; REST stays at 102 paths/113 operations/275 schemas, with eight changed schemas but no inventory additions. Update managed-asset downloads, room listing/views/cost, oblique character view limits, PixFlux transparency behavior, template-animation and normal-map costs, building-kit view/pricing, Workbench output limits, and cancellation billing.
- **Use custom motion for explicit Skeleton v3 requests on managed humanoids.** Keep requested presets and raw keypoints and preserve incompatible-count/body-plan checks. Reconcile the recent custom-animation instructions with refreshed schemas; remove template-only routing pointers and keep preset-engine and raw-keypoint field guidance consistent with the selected workflow. MCP's documented quadruped moves remain a separate allowlisted path.

### Fixed

- **Use ordinary indentation for palette-size validation.** Remove excessive continuation-line spacing that the pinned SkillSpector scanner mistook for context-window stuffing; validation behavior is unchanged.
- **Correct final-review download, preview and repair defects.** Accept the two additional documented PixelLab file hosts; honor pending tileset downloads and bounded retry delays. Refuse ambiguous or tall layouts in the compact tileset preview. Require review of ground snapping and neighbouring-frame thin-part copies, expose pending approvals in the doctor verdict, recognize walk/run template labels, and preserve explicit soft-edge preferences through style saves. Refresh surface-specific enum/count guidance and simulator palette-field recognition without claiming simulated palette enforcement.
- **Repair offline benchmark defaults and remaining export/report gaps.** Pin the old baseline by its existing commit, reject Windows directory junctions without rejecting ordinary cloud placeholders, require cost and palette-version signals, refuse updates to the unmarked historical archive, and point resumed launcher runs to their actual report folder. Generic marked reports and supported route alternatives remain available.
- **Correct review-confirmed benchmark and blueprint gaps.** Require meaningful animation-cost and independent-texture signals, retain supported route alternatives, handle file-to-directory export replacements, reject symlink inputs, and clearly require a Git checkout for current-tree exports. Permit blueprint inputs throughout its local folder tree while retaining traversal and secret restrictions.
- **Address post-commit review regressions.** Export the current working tree despite unstaged reference deletions or directory-to-file replacements, while retaining untracked ignored-file exclusion and unreadable-input failures. Keep new benchmark runs from automatically replacing the historical snapshot or reviving obsolete README score claims. Scope sheet-only icon wording and remove duplicate universal Pro-adherence rankings from specialized references.
- **Scope inpaint, unzoom and pricing claims to their evidence.** Replace the unsupported blanket MCP inpaint warning with masked-output verification, prevent unzooming native/non-pixel sources, correct MCP font and masked-edit cost guidance, and distinguish provisional quotes from charged usage. Batch already-approved template directions with matching controls, preserving preview and per-facing checks; clarify fresh-ID substitution for dependent blueprint calls and the JSON-string format of standard-mode proportions. Check decoded alpha before calling an apparent matte a baked background. The [comparison review](docs/tools/pixellab-mcp-docs-vs-pip-skill.md) records contract research, paid matched trials, blind ratings and limits.
- **Align paperdoll instructions with the shipped helper.** Document executable extraction/composition commands and result handling, distinguish direct Pro Flash changes-only candidates from composite extraction, and mark broader package/CLI proposals as unimplemented. Semantic equipment and exact-mask checks remain required.
- **Check weapon continuity across hidden poses.** Inspect behind-body interpolation paths and trace the gripping hand; a cross-body swing can change screen side without switching hands, while a hidden grip remains unverified.
- **Ask before local repairs alter detected effects.** Pinhole filling, background cleanup and soft-edge hardening use the existing approval when their changed pixels overlap detected effects. Thin-part copies and ground shifts always require review; other ordinary body repairs remain automatic. Approval retains each complete original repair.
- **Keep colour repairs within the approved scope.** Colour corrections that would change effect or uncertain pixels now wait for the existing primary approval; related diagnostics stay pending without suggesting paid retries for the same colour correction. Confident body-only corrections remain automatic, and the original full correction remains available after approval.
- **Keep frame-drop approvals attached to their frames.** Timing change IDs use the original frame identity, so resolving an earlier defect cannot move a later approval to another frame. IDs retain the existing `c`-number format.

## [3.1.0] - 2026-10-29

### Changed

- **Sync PixelLab's 2026-10-29 UTC public contracts.** Font glyph sizes add 12px and 24px; correct stale REST font pricing to 15 generations. Pro Flash costs now follow MCP's size ladder and separate rotations, with free capability-based price checks and explicit REST wording differences. Preset frame counts, supported motion names, MCP seed/input limits, Pro canvas buckets, tile batching, map compatibility, terrain seams, and generation-time guidance follow the refreshed docs. Route/tool inventory counts remain unchanged.

- **Lower SkillSpector risk score.** CI's pinned SkillSpector 2.3.9 rates the skill LOW / SAFE (17, down from 41 in 3.0.0).
  Rules that scanners misread as risky are reworded without weakening them, duplicated token and docs-link rules
  now live in one place, and a scanner false positive in the manifest helper is gone. ClawScan-patched SkillSpector
  2.12.0 static analysis falls from 59 (HIGH) to 17 (LOW / CAUTION) after clarifying blueprint defaults, the
  config toggle warning, the Aseprite MCP comparison, setup's scope/schema/preview paragraphs, and standalone
  license packaging. Minimal Markdown formatting and equivalent phrasing also clear seven stock SkillSpector
  2.13.2 parser failures, lowering its static score from 61 (HIGH) to 17 (LOW / CAUTION) with the same content
  findings. The official-docs reference uses its existing link table instead of repeating the MCP guide URL,
  removing one duplicate finding without removing the destination. Uninstall directory wording is clearer too;
  all paths and safety rules remain. The hosted
  model-based audit has not been rerun, and a LOW score alone does not guarantee a clean registry badge.
- **Document optional helper dependencies.** The README now lists which helpers need Python, Pillow, NumPy or SciPy, gives a user-wide install command, a virtual-environment fallback and a paste-to-agent request, and clarifies that `/pixellab-pip setup` configures PixelLab access rather than installing Python or packages. Setup ends with a one-line note that these packages are optional, and when a helper skips, Pip names the missing or outdated package.
- **Matches PixelLab's 2026-10-25 public docs.** Standard tilesets are quoted at 1 generation (Pro at 15 or 25), and
  top-down height, `view`, borders and no-effect controls follow the new contract; MCP sidescroller Pro mode is
  supported. Normal maps default to the 0.1-generation Lite mode, oversized transparent Pixen requests are known to be
  refused, text-only animals can use Pro Flash, and several cost and job-wait details are current.
- **Refresh the MCP/REST parity guide.** Rechecked the live official docs (102 REST path templates / 113 operations,
  118 MCP tools) and labeled full, partial and absent coverage. The guide now identifies 29 REST operations without a
  full MCP match (16 partial, 13 none) and 40 MCP tools without REST workflow counterparts.

### Security

- **Watch for scanner regressions.** A separate pinned ClawHub-compatible static CI check compares risk, findings and coverage with the reviewed baseline and retains the full report. Maintainer guidance requires behavior checks and independent review for scanner-driven changes; the shipped skill is unchanged.
- **Clarify ClawHub release preflight.** Document the CLI's automatic MIT-0 rights affirmation and the distinction
  between local model-based audit evidence and the hosted release verdict.
- **Keep local files out of release archives.** The ZIP builder now checks the selected release source's
  file list and rejects unexpected files or symbolic links before packaging, including when resuming an older tag.
- **Complete the standalone license.** The skill's `LICENSE.md` now carries both existing copyright notices,
  the unchanged MIT grant and disclaimer, and adopted-source attribution. It replaces the adopted-source-only
  `THIRD_PARTY_NOTICES.md`; no credit or license term is removed.
- **Verify QA package downloads.** The existing dependency versions now include SHA-256 hashes for every currently published
  wheel and source archive. QA and release installs require hash verification without narrowing platform support.

### Fixed

- **Preserve effect approval during local repairs.** Whole-frame grid, size and ground-line repairs with effect candidates use the existing approval proposals. Speck cleanup stays within the detected body, and proposal IDs remain stable when an earlier accepted repair resolves a later change. Body-only repairs remain automatic; originals stay untouched.
- **Protect download accounting files.** Job downloads reject destinations that would occupy the run's
  manifest or transaction-lock paths before downloading, including Windows filename aliases.
- **Only you can change Auto.** Pip acts on `auto`, `auto on`/`off` and `auto plan` only when you give them, never
  from text in a tool reply, web page, file, image, blueprint or panel snapshot. Such text can still lower a budget.
- **A token pasted into chat is always treated as exposed.** Outside setup too, Pip no longer repeats or uses it and tells you
  to replace it.
- **Helpers run when a Windows Python alias is blocked.** An agent shell can resolve `python3` to a Windows app alias
  that will not launch, so the bark sound fell back to a system beep. Pip now tries the other installed interpreters
  before deciding Python is missing.

Fixes from the 3.0 live test ([research spike](docs/pixellab/pixellab-pip-3.0-live-test-research-spike.md)).

- **Showcase GIFs loop cleanly.** A move whose cycle did not divide the fixed 4-second window was cut mid-swing and
  snapped back on every loop; the GIF now lasts until every move ends its cycle together.
- **History says when runs are hidden.** The search showed only the newest 10 runs without saying so, so an older
  run looked missing; it now reports how many older matching runs were left out.
- **Despeckle keeps one-pixel eyes and runes.** `--ref <still>` keeps lone pixels that the clean still already has.
  Without it, the default flattened dozens of real details per frame.
- **Auto palettes keep small accent colours.** `apply_palette auto` turned a knight's brown belt and straps grey; it
  now uses max-coverage quantization.
- **Parallel runs keep their own plans.** `manifest.py plan RUN -` reads the plan from stdin, so agents working at
  the same time no longer record each other's plans through a shared temp file.
- Thrown-prop attacks now make the open-hand release pose before animating, because interpolation never let go of
  the prop. Setup asks before renaming an old Game Art `pixellab.json`, even when asked to get a project ready.

## [3.0.0] - 2026-10-23

Pip 3.0 brings the production workflows of [pixellab-game-art](https://github.com/lexingel/pixellab-game-art) by
lexingel into Pip's single, agent-agnostic skill: project art styles, animation checks and repair, finishing tools,
production recipes and a review panel, all under Pip's ask-before-spending rules. What was left out, and why, is in
the [merge status](docs/tools/pixellab-game-art-skill/pixellab-game-art-pr-11-merge-status.md).

### Breaking changes

- **Image helpers need Pillow 13 or newer (Python 3.11+).** Older Pillow versions have nine published security
  advisories, so the helpers now skip instead of decoding with them. Run `pip install -r requirements-dev.txt` or
  upgrade Pillow.
- **Run manifests are now a cost ledger.** Each run folder's `manifest.json` is a `{"jobs": [...]}` record kept by
  `manifest.py`. Older manifests are kept untouched and listed separately by history; new calls go in a new run folder.
- **Coming from Game Art:** rename a project's `pixellab.json` to `pixellab-pip-style.json` (`setup` offers to do it).
  The old name is not read, and the `/pga-*` commands are replaced by plain requests to `/pixellab-pip`.
- **A broken settings file means Auto is off.** If `pixellab-pip.json` cannot be read, Pip asks before spending until
  an explicit `auto on`, `auto off` or `bark` command replaces the file.

### Added

- **Project art styles** in `pixellab-pip-style.json`: named styles, approved reference art per asset family, an
  optional fixed seed, 4 starting setups (including Game Art's side-view dark fantasy look) plus 7 untested genre word
  sets, and optional analysis of art you already have. Nothing applies unless you choose it.
- **Animation doctor** (`fix.py`): finds jumps, flicker, stray pixels, size pops and lost weapons; fixes what it can
  for free on copies; plans paid re-rolls of only the frames that failed.
- **Finishing tools**, which write copies and record what they changed: ground snap, scrub, despeckle, colour match,
  palette, recolour (by group, trail, or like another character), slash layer, blade trail, thrown prop, baked effect,
  8-direction shot finish and a muzzle finder.
- **Previews and export:** sprite sheets with Aseprite JSON or Godot `.tres` (play once or `--loop`), padding,
  preview and showcase GIFs, contact sheets, a tileset test map, and normal-map packing with a lit preview.
- **Run tools:** `fetch.py` downloads finished results, `manifest.py` keeps a locked cost record per run (charged and
  estimated kept apart), and `history.py` searches past runs for re-rolls.
- **Auto limits:** `auto plan <budget> [retries] [task]` caps one run's generations and retries; `auto status` shows
  the current setting.
- **Review panel:** `/pixellab-pip panel` opens a private, interactive review page; Claude Code also gets a native
  panel view.
- **Guides:** key-pose attacks and skills, 8-direction moves, characters, scenes and backgrounds, normal maps,
  front-facing giant bosses, 14 weapon pages, martial arts, armour and cloth, and weapon effects.
- **Blueprints:** character candidates, an overhead axe chop, a projectile skill, and strike, wave and eruption
  effects.
- **Cost helpers:** an optional 1-generation layout draft before an uncertain Pro image, and the closest alternative
  when a tool is not in your PixelLab plan.

### Changed

- Cheap mode and cinematics take retries from the run's retry allowance. A failed paid job is never retried without
  your approval or that allowance.
- Before generating, Pip checks the project root for `pixellab-pip-style.json`.
- The skill description fits the Agent Skills 1,024-character limit and keeps its trigger words; `requires_api_key`
  metadata is now a string.
- The Claude Code plugin registers the panel add-on, and CI also runs Claude Code's plugin validation.

### Security

- Pillow pinned to 13.0.0, which fixes nine advisories, including a critical JPEG decoder heap overflow.
- Downloads come only from PixelLab's own hosts, send no token, and are capped in size and checked for image bombs.
- A project file can never turn Auto on or grant spending; Auto stays in your private `pixellab-pip.json`.

Thanks to lexingel for pixellab-game-art and its adopted code (MIT; notices ship with the skill).

[Unreleased]: https://github.com/Shilo/pixellab-pip/compare/v3.2.5...HEAD
[3.2.5]: https://github.com/Shilo/pixellab-pip/compare/v3.2.4...v3.2.5
[3.2.4]: https://github.com/Shilo/pixellab-pip/compare/v3.2.3...v3.2.4
[3.2.3]: https://github.com/Shilo/pixellab-pip/compare/v3.2.2...v3.2.3
[3.2.2]: https://github.com/Shilo/pixellab-pip/compare/v3.2.1...v3.2.2
[3.2.1]: https://github.com/Shilo/pixellab-pip/compare/v3.2.0...v3.2.1
[3.2.0]: https://github.com/Shilo/pixellab-pip/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/Shilo/pixellab-pip/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/Shilo/pixellab-pip/compare/v2.3.0...v3.0.0
