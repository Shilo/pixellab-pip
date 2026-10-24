# PixelLab Game Art merge: PR #11 adversarial review

Historical review of the pinned original head. The [implementation plan and acceptance record](pixellab-game-art-pr-11-implementation-plan.md) tracks subsequent fixes and current readiness.

Review date: 2026-10-23. **Recommendation: request changes; do not merge this head.**

There is valuable production work here, but the current implementation does not yet preserve Pip's authority, output-integrity, portability and project-continuity contracts. Passing QA does not resolve the demonstrated failures below. A review cannot promise zero concerns; it can identify material failures, account for the useful source features, and define evidence needed before acceptance.

## Scope and method

- PR: [Shilo/pixellab-pip #11](https://github.com/Shilo/pixellab-pip/pull/11), exact head `e5313285523216ce8faa06cf241cc8bed8cce32e`, merge base `050c51679d0adbb9bb659bf8d5c3b4f6bfbef1e5`.
- Current Pip checkout reviewed: `b4d09e587673889370444ef9594cf6c2f9f2d3de`. Its change after the merge base converts the maintainer's position document from HTML to Markdown; that conversion is not a PR regression.
- Supplied Game Art checkout: version 1.4.3 at `8b407e9cee6e3c8c7d8e5d89edde74cc18acd23f`. Both portable and Claude distributions were examined. The older research pins a different revision; its conclusions were checked against current supplied files rather than treated as implementation truth.
- Read all three documents in this directory: the feature comparison, merge research spike and maintainer's merge position; also the PR's merge README, demo account, benchmark and motion evidence.
- Four specialist sub-reviews covered runtime/design, Python correctness/necessity, source-feature parity/Claude integration, and independently researched skill-authoring practices. The parent challenged their conclusions, reconciled overlaps and distinguished inherited issues, design choices, reproducible defects and untested claims.
- Review only: no implementation fixes, installation changes, paid PixelLab calls, PR comments, GitHub reviews, merges or external messages. Disposable local snapshots, dependencies, tests and mock probes were used.

Every source path and line below refers to the pinned PR head unless explicitly identified as baseline or source. The [pinned tree](https://github.com/Shilo/pixellab-pip/tree/e5313285523216ce8faa06cf241cc8bed8cce32e) makes the references stable.

### What the size actually means

The PR changes **137 files: 11,769 text additions and 22 deletions**, plus media. That is not by itself evidence of bloat. Its distribution explains the real review burden:

| Family | Changed files | Added text lines |
|---|---:|---:|
| Core and operational references | 20 | 844 |
| Motion specialty references | 17 | 2,024 |
| Doctor implementation | 11 | 1,629 |
| Finishing implementation | 14 | 1,260 |
| Other runtime helpers | 14 | 1,356 |
| Production blueprints | 6 | 820 |
| Claude adapter | 6 | 732 |
| Doctor tests/fixtures | 18 | 1,383 |
| Other regression tests | 10 | 1,227 |
| Evidence/user documentation | 15 | 410 |
| Packaging/development/top-level documentation | 6 | 84 |

The root skill grows from 265 to 275 lines, and from 58,546 to 61,549 UTF-8 bytes. Long lines make line count a poor context-cost measure. Tests and human documentation deserve separate treatment from always-loaded instructions. The repository explicitly exempts `docs/` from its runtime KISS/placement rules; this review does not propose deleting evidence merely to reduce the diff.

## Material findings

P1 means fix before merging the affected behavior. P2 means a concrete correctness/design issue that must be resolved or explicitly removed/deferred before claiming the corresponding capability. Conditional release risks are identified as such.

### R01 — P1: `auto` grants authority to alter art, not just skip the cost gate

**Evidence:** `skills/pixellab-pip/references/auto.md:32-36,124`; `references/finishing.md:22-24`; `SKILL.md:33,41,44,253`.

The new table makes global Auto allow local cleanup, new pixels and frame drops/reorders with disclosure alone. The same reference still says Auto governs only spending approval. Pip's globals still require explicit acceptance of non-PixelLab fallback/final alterations and preserve frame count/order unless requested. Someone who enabled Auto to avoid cost prompts has not accepted procedurally painted trails or changed playback. Labeling the result afterward does not provide that acceptance.

**Smallest complete remedy:** keep one cost gate. Let an explicitly accepted job plan authorize its listed transformations and review delegation. Do not derive art authority from a global spending preference. An accepted plan that explicitly names a local fallback can already satisfy Pip's approval boundary; that legitimate case is not the defect.

### R02 — P1: Starting a Claude project changes installation-wide execution settings

**Evidence:** `editions/claude/hooks/register.tsx:249-256`; `references/auto.md:30`.

Opening a named folder without a profile synthesizes an `asUser: true` prompt to set Plan, budget 50 and two redos. The actual user chose a project name, not a global permission change. This can replace a more restrictive setting used by other projects. Plan still requires a cost card, so this is not proof of an immediate unapproved charge; it is an unintended persistent policy change.

**Remedy:** project creation leaves execution policy unchanged. A deliberate settings action must identify its installation-wide scope and exact values and use the core's existing setting.

### R03 — P1: Budget accounting confuses unknown, estimated, failed and refunded usage

**Evidence:** `assets/manifest.py:24-29,69-80`; `assets/fetch.py:7-14,70-73,135-143`; `references/usage-reporting.md:60-62`. All `assets/` and `references/` paths here and below are under `skills/pixellab-pip/`.

Four related defects undermine the ledger used to enforce budgets:

1. Missing/null usage contributes zero, even for submitted work.
2. An existing JSON object without a valid `jobs` list becomes an empty ledger; the next write discards its data. A fixture with existing `calls` and audit text returns committed zero and loses those keys after an add.
3. Fetch describes Pro Flash's `estimated_generations` as `reported_usage.generations`, although Pip reserves that field for actual exposed usage.
4. A download 404 after 60 seconds becomes failed/refunded, releases its cost from committed spend and prints “refunded; resubmit.” An unavailable download does not establish terminal job state or a refund.

**Remedy:** reject invalid ledger shape without writing. Distinguish known actual zero from unknown cost; keep conservative pending reservations/estimates separate from reported charges. Verify terminal status through the matching getter and never infer refund from download HTTP status. This needs no generic compatibility framework: refusing an unknown record is sufficient.

### R04 — P1: Atomic manifest replacement loses concurrent paid jobs

**Evidence:** `assets/manifest.py:50-66`.

Atomic file replacement protects JSON syntax, not the read/modify/write transaction. Two completing downloads can both read the old ledger and then overwrite each other's additions. A deterministic local interleaving records two submitted six-generation jobs but leaves only one: committed spend is **6 instead of 12**. Resume IDs and outcomes can disappear too.

**Remedy:** serialize mutations through one writer or lock the entire transaction. Add one focused interleaving regression test. A database is unnecessary.

### R05 — P1: Downloading can overwrite raw art and mix stale frames into a new result

**Evidence:** `assets/fetch.py:77-100,104-123`.

Only the URL branch refuses an existing destination. Ordinary job download overwrites a file or numbered frames. A shorter refetch leaves old trailing frames, and `outputs()` records every PNG in the directory as belonging to the new job. A local two-frame result in a folder containing an older third frame is recorded as three frames. Additionally, the URL branch saves HTML successfully, and the job path accepts a PNG prefix without decoding a valid image; the tests themselves use prefix-plus-arbitrary bytes.

**Remedy:** preflight every destination, preserve existing raw bytes, allow idempotent reuse only when identity/content is established, validate the downloaded representation, and record exactly this result's files. Never delete old raw files to hide a collision.

### R06 — P1: Doctor overwrite protection excludes sheet/GIF containers

**Evidence:** `assets/fix.py:141-146,175`; `assets/fixlib/frames.py:146-163`.

The guard inspects `Anim.paths`, empty for sheet/GIF inputs. A source sheet named `fix_sheet.png`, processed with `--sheet 48x56 --out` pointing to its own folder, exits successfully and is overwritten by the inspection report. This was reproduced locally.

**Remedy:** protect all input containers, source frames and reference files; resolve aliases and preflight every output name before any write.

### R07 — P1: A special hurt repair changes playback without `--accept`

**Evidence:** `assets/fixlib/timing.py:46-63`; `tests/doctor_cases/test_timing.py:38-44`; `references/animation-doctor.md:59-62`.

The five-frame hurt branch automatically applies a house reorder when early frames have body findings. Only the effect-only branch requires acceptance. A synthetic case with no accepted proposals returns order **[3,4,4,3,0]** instead of [0,1,2,3,4], repeating and omitting poses. The existing test expects this unauthorized change, explaining why QA passes.

**Remedy:** every playback substitution must be a proposal. Prefer removing the house-specific reorder table from generic repair unless the user selects that recipe.

### R08 — P1: The panel can submit work for a different project than it displays

**Evidence:** `editions/claude/hooks/register.tsx:236-248,314-315,388-401`.

Opening an existing project updates the panel directory but not session cwd. Generic submissions send only the user's text. A mock opens project B while the session is in A; “Make a hero” is submitted without B's root/context. The agent can therefore use A's style and output folder while the user sees B.

**Remedy:** bind task submissions to the selected root and applicable run/source identities, or synchronize the working project explicitly before accepting tasks. Do not scan other projects to guess.

### R09 — P1: Adopted source lacks its upstream copyright notice

**Evidence:** PR `LICENSE:1-9`; supplied Game Art `LICENSE:3-12`; `assets/analyze_style.py` retains 201 identical lines of the 221-line source analyzer.

The supplied upstream MIT notice names lexingel; the PR retains only Pip's copyright notice. README credit and the word MIT do not reproduce the upstream notice. Raw-skill archives particularly need attention because a root-only file may not ship with them.

**Remedy:** preserve the upstream copyright and complete permission notice in every distribution containing substantial copied/adapted material, and record its revision/provenance. This finding compares the supplied notices and copied source; it does not assert ownership of generated artwork.

### R10 — P1 for migration/release: Existing no-ask instructions and restrictive caps are unresolved

**Evidence:** source `any-agent/AGENTS.md:13-17` and installer-generated task-agent instructions; PR `references/project-style.md`; `docs/merge/README.md:30-39`.

Game Art project instructions can remain at higher priority than the newly installed skill and forbid permission questions. A skill cannot guarantee it overrides them. Legacy restrictive `max_cost`/`ask_above` values may remain in JSON but have no reconciliation with the new budget. Preserving bytes does not preserve their safety meaning. The demo removed the old skill first; it did not validate real migration/coexistence.

**Remedy:** identify old installation components, preview a scoped cleanup preserving user edits, obtain approval for removals, reconcile restrictive caps before spending, and test representative existing projects. Do not write an automatic destructive migration or import the old installer. A prototype may defer release, but cannot claim migration safety.

### R11 — P2: Ordinary generation does not discover the saved project style

**Evidence:** `SKILL.md:103,163`; `references/project-style.md:3-4`.

The instruction to read an existing project profile before generation is inside the reference that must first be discovered. The global workflow has no ordinary-generation check for that profile. Explicit “use my saved style” requests can work; a fresh session asking only for shop icons is not guaranteed to load the active style/icon anchor. That is the main continuity experience being merged.

**Remedy:** add one narrow discovery action for already-routed PixelLab generation in the selected project root. No profile means ordinary one-off operation, not mandatory onboarding; generic non-PixelLab art remains outside the trigger.

### R12 — P2: Temporary style selection and safe preference updates are missing

**Evidence:** `references/project-style.md:8-31`; `assets/project_style.py:90-145,172-181`.

The source supported a named style for one task without changing active style. The merge offers persistent `use`, no per-job opt-out, no specified legacy/nested inheritance, no stale-anchor behavior, and tells the agent to save a one-off request that names a look. Missing active style forces a setup question before paid work. The helper also accepts an existing non-image as an anchor and does not validate nested style structures.

**Remedy:** define the minimum read/select/override/approved-save contract. Current-job art direction must not silently mutate project state. Resolve anchors relative to the profile and treat missing/unreadable art explicitly. Provide a graceful instruction-only read path when Python cannot run. Implement these essentials before expanding rename/delete/catalog conveniences.

### R13 — P2: The first character can become an unapproved anchor for the wrong family

**Evidence:** `references/characters.md:9`.

The row covers heroes, NPCs, monsters and bosses. For a new project with no anchor, it then registers the selected still as `anchor heroes`. A first monster/boss can therefore become the hero-family reference. The text does not establish that every later selection overwrites an existing anchor; the demonstrated issue is wrong-family initial registration and treating an output pick as approval to establish persistent project direction.

**Remedy:** keep the character's own canonical source separate from family style anchors. Use the correct family and save/replace an anchor only when explicitly accepted.

### R14 — P2: New still/scene defaults contradict canonical routing

**Evidence:** `SKILL.md:77,99`; `references/characters.md:9-13`; `references/scenes-and-backgrounds.md:3,8`.

The main router defaults characters to managed v3 and backdrops/scenes to PixFlux/Pixen; the new still reference defaults side-view stills to Pro Flash, while the scene page claims the router chooses Pro for full scenes. Those alternatives can be useful, but the dispatch/precedence is unresolved and costs differ substantially. A reference-list entry is not a clear choice between competing defaults.

**Remedy:** classify static still versus managed multiview and applicable style-reference needs once in the router. Specialty pages add decisions rather than redefine defaults. Keep existing tested defaults unless a narrow replacement is supported.

### R15 — P2: The scene template excludes requested people

**Evidence:** `references/scenes-and-backgrounds.md:11,17,26`.

It always adds “no characters, no people” and reviews for no figures, yet covers story pictures with a focal subject. “The party camping under a dead tree” conflicts with those imposed exclusions.

**Remedy:** apply people exclusions only to requested subjectless backdrops. Keep scene composition advice without automatic negative boilerplate or a mandatory muted house palette.

### R16 — P2: Production recipes overrule requested frame counts and playback

**Evidence:** `references/key-pose-animation.md:124-145,213-219`; `references/eight-direction.md:39`; `SKILL.md:33`.

Rules prescribe six-frame thrusts, make every move use one count, shorten other moves after a failed take, drop/replace stages and frames, and play hurt there and back. Eight-direction finishing repeats poses to equalize counts. These are legitimate optional creative choices, but cannot override an exact requested sequence or silently apply to unrelated moves.

**Remedy:** make the derivative recipe an explicit selection and include its transformations in accepted scope. Preserve raw output independently. Respect requested counts and localize a repair to the affected move.

### R17 — P2: Content-review authority has two incompatible definitions

**Evidence:** `references/auto.md:40`; `references/key-pose-animation.md:107`.

One rule requires user key-pose approval at every level; another allows self-approval at Auto “when the level says so.” The level table does not resolve that contradiction. Agents can either stop unnecessarily or continue without the promised review.

**Remedy:** put content-checkpoint/delegation semantics in one canonical place, separate from spending preference, and point to it.

### R18 — P2: Normal-map observations became universal, outdated requirements

**Evidence:** `references/normal-maps.md:8-18`; `assets/normal_map.py:4-6`; existing `references/image-input-roles.md:46`.

The imported page declares MCP strips one image, mandates GIF conversion, assumes first-frame planning, segments major pose changes into additional paid requests, and always adds lighting artifacts. Connected MCP metadata explicitly advertises GIF/strip/managed-animation inputs and now distinguishes Lite and Pro; Lite is the default. The existing input-role row still imposes a universal strip, so the two pages also contradict each other. The research had explicitly withdrawn these universal restrictions and mandatory additions.

**Remedy:** preserve supported representations and one canonical input contract. Keep specific historical failures/banding as dated evidence; offer conversion or segmentation when justified by an actual case and approved plan. GIF conversion changes palette/alpha, so it is not a neutral transport step. Current primary evidence: [PixelLab MCP guide](https://api.pixellab.ai/mcp/docs) and connected `create_normal_map` schema. Arbitrary strip frame detection was not live-tested in this review.

### R19 — P2: Diagnostic reroll plans can name an invalid repair or the wrong paid job

**Evidence:** `references/animation-doctor.md:89`; `assets/fixlib/plan.py:9-16,32-33,65-81`.

“2-4 frames” includes unsupported two-frame raw v3 animation. The cost calculation can consequently underquote the minimum valid call. Separately, job lookup compares directories rather than actual output paths: the newest run job in a shared raw folder can be attached to an attack's repair. A local probe returns the unrelated job and cost.

**Remedy:** resolve repair parameters/cost against the selected current schema before approval; match exact recorded outputs, reporting ambiguous ownership as unknown. Heuristic defect-to-cause explanations should remain suggestions, not proven diagnoses.

### R20 — P2: Doctor sheet loading discards intentional empty frames

**Evidence:** `assets/fixlib/frames.py:156-160`.

The loader removes fully transparent cells and ignores right/bottom grid remainders. A two-cell sheet with one sprite and one intentional blank loads as one frame, violating count/order guarantees even before repair.

**Remedy:** validate divisibility and preserve every declared cell. If an atlas has unused cells, require layout/count information rather than guessing from alpha.

### R21 — P2: Soft effect compositing makes opaque bodies transparent

**Evidence:** `assets/finish/bake_fx.py:67`; `assets/finish/dir8_finish.py:79,120`.

RGBA `paste(effect, ..., effect)` interpolates alpha as a color band instead of source-over compositing. A half-alpha red effect over opaque black yields `(128,0,0,191)`, where alpha must remain 255. Opaque-only tests miss it.

**Remedy:** clip/pad an aligned overlay and alpha-composite. Verify partial-alpha effects over transparent and opaque bodies, including rotated/clipped placement.

### R22 — P2: The doctor duplicates GIF assembly and adds an opaque matte

**Evidence:** `assets/fixlib/report.py:131-140`; `assets/preview_gif.py`.

The doctor fills transparency with a colored background and converts to RGB. A transparent fixture's preview is fully opaque. Meanwhile a separate new helper already implements transparent, decoded-and-checked GIF output. The preview policy and implementation have diverged.

**Remedy:** reuse the faithful preview path. Keep any differently treated inspection visualization explicitly labeled and within Pip's permitted inspection exceptions; do not silently turn it into the standard report preview.

### R23 — P2: The Claude UI is a second, potentially stale source of truth

**Evidence:** `editions/claude/hooks/register.tsx:18,143-179,266-269,429-435`.

The panel marks a level selected before the queued agent request changes canonical config, never reads that config, and does not restore its own stored level. Its refresh signature omits style/title and compares pose path plus byte length rather than content. A same-length replacement can leave old art displayed for approval. It also pairs the newest keys folder with the project's hero anchor, shows at most four poses and ignores explicit output-root overrides.

**Remedy if retained:** read canonical acknowledged settings, bind review to the actual run/reference/version, and cover all displayed state in refresh identity. An optional UI must adapt to core metadata rather than require portable folder conventions. Removing/deferring this optional edition avoids these particular merge obligations without losing the production features.

### R24 — P2: The next release does not update the new edition's versions

**Evidence:** `.github/workflows/release-skill.yml:160-169`; `.claude-plugin/marketplace.json` second plugin entry; `editions/claude/.claude-plugin/plugin.json`; `tests/test_claude_edition.py:27-30`.

The existing bump table updates only marketplace plugin zero and existing core manifests. The new test requires core and Studio marketplace versions to match. Running the exact extracted bump script in a disposable fixture changes core to 2.3.1 while Studio stays 2.3.0; the existing version-equality test then fails. The same omission affects the edition's own manifest.

**Remedy:** if the edition remains, extend the existing canonical version locations/checks, including its manifest. Do not add a second release framework.

### R25 — P2: History and ordinary reroll parity are overstated

**Evidence:** `docs/merge/README.md:33-35`; `assets/history.py:19-25,31-32`; source history/reroll task references.

The mapping suggests questions such as monthly spend, while the helper returns only ten newest run summaries ordered by manifest modification time. It lacks call timestamps, time filtering and prompt/job search. Doctor repair plans also do not replace ordinary “repeat this old call with one wording change” behavior from Game Art.

**Remedy:** describe the smaller capability accurately, or query canonical manifests/blueprints with the minimum needed filters/request data. Do not restore a second log or generation client. Missing useful behavior is not an argument for importing every upstream history tool.

### R26 — P2: “Check” and “fix” are routed to the same modifying operation

**Evidence:** `SKILL.md` row beginning “Check or fix animation frames”; `assets/fix.py:87-101,125`.

The router runs the doctor without `--check-only` for both intents. A user asking for inspection can receive repaired derivative copies, rather than only findings, even though the CLI already supports inspection. This does not necessarily overwrite originals; R06 identifies the separate collision defect.

**Remedy:** inspection uses `--check-only`; repair requires the requested/accepted scope. Distinguish tool success, heuristic findings and visual acceptance. Do not create another helper to make this distinction.

### R27 — P2: Generic export invents a damage event

**Evidence:** `assets/make_sheet.py:24,39,53`; `references/local-asset-assembly.md` engine-export instructions.

Without `--hit`, the helper writes the penultimate frame as `hit_frame`, including icon sheets, walk/idle clips and any move whose actual contact differs. The runtime says to include hit metadata only when known/requested, but the helper always emits it.

**Remedy:** omit unknown gameplay metadata; require an explicit known hit frame when applicable. Preserve the useful optional Godot export and frame durations. Actual engine import compatibility still needs an engine check before broad claims.

### R28 — P2 acceptance gap: Blueprint-as-reference remains unresolved

**Evidence:** unchanged `SKILL.md` blueprint router and `references/blueprint.md`; merge research's bounded reference-versus-replay cases.

This ambiguity predates the PR. The research explicitly identified it as a merge acceptance item: “shop icons in the style of hero.blueprint.json” should route icons using existing output images, not replay the hero workflow. The broad merge adds project styles and replayable recipes without resolving that selection boundary.

**Remedy:** clarify reference use versus actual replay in the existing router; do not infer paid regeneration merely to obtain a missing reference. An explicit approved request to reconstruct that reference remains valid. Treat this as an unmet documented research recommendation, not a maintainer agreement, observed failed run or regression newly introduced by this PR.

### R29 — P2: A simple attack is promoted to an elaborate paid production pipeline

**Evidence:** `SKILL.md:112`; `references/key-pose-animation.md:38-48,80,245-261`.

The new broad attack/skill route selects paid key-pose edits, matching, review, in-betweens, picking/finishing, doctor and export. The example pipeline quotes 22/31 generations per melee move. Custom key poses are valuable for choreography or known direct-generation failures, but a simple raw/managed attack request does not inherently require those extra calls and artifacts. Showing a cost card makes the plan reviewable; it does not establish that every step is necessary.

**Remedy:** retain ordinary animation routing and make the advanced recipe conditional on the requested choreography/anchors or demonstrated failure. Apply finishing only to observed defects within accepted scope, and engine export only when needed. Preserve Pip's existing standard preview/manifest/blueprint obligations.

## Researched agent-skill best practices

The independent research used current primary sources, not community rules of thumb. These have different authority:

| Source | Guidance used in this review |
|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | Metadata constraints are format requirements; progressive disclosure and short, focused references are authoring guidance. Size guidance is not an instruction to delete necessary safeguards. |
| [AgentSkills creator guidance](https://agentskills.io/skill-creation/best-practices) | Add missing operational knowledge, ground rules in real failures and choose suitable freedom for each task. This favors precise API/output boundaries and optional creative recipes. |
| [Anthropic authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Concise instructions, task-specific loading, documented dependencies, useful errors and evaluated examples. Host-specific APIs remain adapter details. |
| [OpenAI Build skills](https://developers.openai.com/plugins/build/skills) | Define inputs, outputs, stops and resource triggers; use scripts when deterministic work or existing-tool limits justify them. Evaluate direct, indirect, incomplete, negative and edge-case requests. |
| [OpenAI instruction-design guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | A minimal router with on-demand detail reduces irrelevant context; elaborate universal itineraries can overconstrain tasks. Model-specific advice does not override Pip's cross-agent safeguards. |
| [AgentSkills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills) | Compare representative clean-context outcomes/traces with a baseline; avoid treating brittle phrase matches as proof of behavior. |
| [AgentSkills script guidance](https://agentskills.io/skill-creation/using-scripts) | Discover existing tools, make dependencies reproducible, and provide clear machine-usable success/error behavior. This does not justify adding another installer/framework. |

Applied acceptance tests are: every runtime addition must earn a decision/action/boundary/check; one canonical policy must govern each concern; ordinary requests load only applicable detail; deterministic helpers must preserve inputs and expose honest failures; optional dependencies must not disable unrelated routes; saved data and examples grant no execution authority; and representative behavior must work outside one host.

Two qualifications prevent overcorrection:

- Both baseline and PR have a 1,164-character description, over the specification's 1,024-character maximum. That is inherited portability debt, not a regression introduced by this merge. The inherited non-string metadata values also deserve a separate compatibility cleanup. Do not expand this merge into an unrequested router rewrite merely because the baseline has debt.
- The PR does directly link all weapon references and says to load only the relevant page. It would be wrong to claim all 60 references load at activation. The actual issue is misplaced specialty content inside the generic page and several competing authorities. Tracked reference content grows from 34 to 60 files, and assets from 4 to 42 files; these measure maintenance scope, not startup loading.

## KISS, YAGNI and DRY decisions

These principles are not a file-count quota. Retain complexity that prevents wrong routes, lost art, unsafe spending or ambiguous state. Remove complexity that exists only to support another unnecessary abstraction.

### One setting instead of a second approval architecture

Original Auto-off already obtains approval for a whole paid chain, including batches. The useful new capabilities are an explicit budget, bounded retries and pending-job accounting—not the existence of a Plan name. `auto` plus `level`, a boolean plus enum, global budgets plus per-plan scope, and independent UI state introduce several representations of the same choice.

**Decision:** adapt useful budget/retry constraints into the existing cost-approval contract and custom command grammar. Remove `level` as an independent authority. An optional migration alias is justified only by an actual supported migration need. Never conflate cost, content review and pixel alteration.

### One core; host adapters must earn their maintenance cost

The current PR has already removed the old separate `pga-*` task skills/commands; the concern is not unchanged duplication of all those skills. Studio is a new optional Claude plugin, with one panel command and the shared core dependency. A host adapter is not inherently incompatible with an agent-agnostic product.

However, this panel is not required to preserve Game Art's style memory, doctor or recipes. It adds a second product, connector, policy defaults, state, filesystem discovery and release obligations. The source package did not require a panel.

**Decision:** defer Studio from this core merge unless maintainers explicitly choose and validate that additional product. Keep task access in the existing agent-neutral core/custom commands. A later adapter can call the same contract without changing its authority or forcing its folder names.

### Consolidate repeated decisions, not every similar-looking sentence

Concrete duplication requiring action:

- Generic `key-pose-animation.md:180-215` carries sword/katana stance tables, iai sequences, pistol draw and flying-kick instructions despite dedicated sword/katana/firearms/martial-arts references. A basic axe request loads unrelated specialties. Keep generic pose/anchor/padding/review mechanics in one place and load only the selected specialty.
- `fixlib/report.py`, `normal_map.py`, `showcase_gif.py` and `preview_gif.py` have separate GIF encoding/palette/timing policies. Their products may differ, but shared preservation mechanics should not independently drift. R22 demonstrates an actual consequence.
- The doctor and finishers implement overlapping normalization/cleanup, and effect ramps/extraction occur in several finishers. Consolidate only the retained shared operations; do not create a generic art-processing framework.
- `_assembly.require_numpy` and `finish/_derive.require_numpy` have different dependency/skip behavior. Some helpers import Pillow after a guard that checks only numpy/scipy and can traceback instead of returning the documented skip.
- Route defaults and approval decisions appear in the router, specialty pages and panel. One canonical decision with a pointer is safer than repeated prose. Repeating the output-invariance assertion in a test is not a behavioral test.

Not every blueprint repetition is waste: an independently replayable recipe needs its actual call bodies. Likewise a specialty page may need its weapon-specific pose wording. Delete repeated *policy and procedure authority*, not the concrete values needed to execute the selected recipe.

### Challenge automatic finishing and procedural drawing

`despeckle` can remove intentional single-pixel eyes; the fixture demonstrates this, and its test counts the removals as expected. The analyzer can infer scale 16 for a native figure in a large transparent canvas and report a zero-size subject. These are heuristic limits, not proof the capabilities have no use.

**Decision:** keep measurement/review advisory; require explicit requested transformations. Defer automatic median repainting, automatic brightness normalization, omnibus direction finishing and local procedural blade trails from the default pipeline. PixelLab workbench and existing palette/Aseprite routes already cover many uses. Reuse them where reliable; keep a local fallback only for a demonstrated need and accepted non-PixelLab scope.

The doctor's calibration on 818 animations is an attributed source claim, not a supplied representative validation corpus. It does not justify universal “game ready” conclusions for tiny sprites, effects, intentional lighting, airborne attacks and other art domains. Preserve objective checks and visual checklists; qualify unsupported judgments.

## Useful source features: preserve, adapt, or deliberately exclude

All 22 Game Art task families were reconciled. Preserving a capability does not require preserving its old command name, helper filename or house defaults.

| Game Art task | Disposition in a Pip-aligned merge |
|---|---|
| `pga-start` | Preserve optional understandable onboarding; no forced profile, drafts or fixed starter bundle. Portable guided flow is weaker than the source and must not be advertised as complete parity. |
| `pga-help` | Consolidate into the existing skill router/user docs. |
| `pga-init` | Keep approved project direction setup; complete provenance/propose/review/save and project isolation. |
| `pga-style` | Keep named styles and family anchors; restore temporary selection/opt-out and safe legacy/nested semantics before extra management conveniences. |
| `pga-analyze` | Optional advisory measurements with visual review; no automatic truth or saved authority. |
| `pga-prompt` | Existing Pip prompt enhancement/direct questions cover it; no extra command needed. |
| `pga-char` | Keep useful still/candidate/prop review; adapt route scope and deliberate anchor registration. |
| `pga-bg` | Keep composition hints on demand; preserve neutral defaults and supported route choices. |
| `pga-scene` | Keep composition/reference reuse; remove unconditional subject exclusions. |
| `pga-building` | Keep silhouette-preserving upgrade chains inside existing building guidance. |
| `pga-icon` | Keep useful tier/relationship guidance; reuse Pip's stronger icon/palette routes. |
| `pga-anim` | Keep opt-in key-pose production and useful checks; adapt authority, timing, frame preservation and finishing. |
| `pga-vfx` | Three reusable workbench templates fit Pip blueprints; no second VFX authoring contract. |
| `pga-tiles` | Existing routes cover generation/chaining; optional narrow metadata preview is useful when requested, not universal tileset proof. |
| `pga-normal` | Keep optional packing/splitting/light preview and engine notes; correct supported inputs/modes and scope segmentation. |
| `pga-batch` | Existing approved batches can retain CSV/text/group requests; the source's mixed-batch interpretation/review flow is not fully documented in this PR. Add only missing user decisions, not a batch engine. |
| `pga-doctor` | Old command means setup diagnostics, distinct from the new animation doctor. Reuse setup checks for the actually needed surface/dependency. |
| `pga-feedback` | Deliberately exclude author telemetry/sharing. |
| `pga-history` | Keep one-record history; current ten-run summary loses useful date/job search behavior. Be precise about scope. |
| `pga-reroll` | Keep historical same-call variation via canonical request/blueprint and normal approval; doctor plans alone are incomplete parity. |
| `pga-update` | Reuse Pip update lifecycle; do not import another updater/weekly promise. |
| `pga-tech` | Answer directly; no separate task skill, model or delegation system needed. |

The supplied source's Claude wrappers, optional model dispatch, installer, `AGENTS.md`, update framework and author sharing are correctly excluded as runtime additions. Existing installed copies still need migration. The PR's newer doctor/motion material is not all present in the supplied older source, so provenance and calibration cannot be certified solely by comparing that checkout.

### Every runtime helper family

| Files under `assets/` | Decision and justification |
|---|---|
| `_assembly.py` | Keep shared support only for retained helpers; one consistent dependency/error contract. |
| `bark.py` changes | Reuse atomic setting writes; simplify duplicated permission state; validate budget/retry values. |
| `pad_sprite.py` | Keep concrete pixel-preserving padding with placement/collision checks. |
| `contact_sheet.py` | Keep ordered, labeled review aid; no mandatory extra artifact for unrelated questions. |
| `preview_gif.py` | Keep faithful decode-and-verify path; reuse preservation mechanics elsewhere and state GIF limits. |
| `make_sheet.py` | Keep exact ordered assembly and requested metadata/Godot export; omit invented hit frame and protect inputs. |
| `manifest.py` | Keep one private record; fix R03/R04 before using it for paid limits/resume. |
| `fetch.py` | Useful optional bounded downloader; fix R03/R05 and use actual lifecycle status. |
| `history.py` | Keep a small read-only view; accurate scope and data completeness before broader queries. |
| `project_style.py` | Keep a small validated resolver/writer; essential selection semantics before CRUD growth. |
| `analyze_style.py` | Optional explicit analysis; defer automatic extraction/persistence. |
| `fix.py`, `fixlib/__init__.py`, `colour.py`, `frames.py`, `measure.py`, `model.py`, `plan.py`, `repair.py`, `report.py`, `thresholds.py`, `timing.py` | Keep complementary diagnostics; stage/adapt the repair implementation, scope heuristics, and fix output/count/authority/accounting failures. Modules are implementation structure, not independent required features. |
| `finish/_derive.py` | Keep only if finishers retained; preflight all writes and reuse dependency support. |
| `finish/ground_snap.py` | Useful explicit grounded-motion alignment; not jumps/flyers or guessed footlines. |
| `finish/scrub.py` | Explicit region/clip cleanup with visual verification; no generic harmless-cleanup claim. |
| `finish/despeckle.py` | Defer automatic use; keep only explicit risky detail cleanup. |
| `finish/colormatch.py`, `finish/apply_palette.py` | Requested normalization only; consolidate mapping where practical and compare existing supported routes. |
| `finish/recolor_groups.py`, `finish/recolor_like.py` | Optional explicit variants/transfers, labeled and verified. |
| `finish/recolor_trail.py`, `finish/slash_layer.py` | Separate source-pixel extraction/reuse from painting new ramps; consolidate retained mechanics. |
| `finish/dir8_finish.py` | Defer omnibus pipeline; select explicit constituent operations and correct alpha/playback authority. |
| `finish/bake_fx.py` | Useful accepted composition; fix source-over alpha and account for added holds/timing. |
| `finish/throw_prop.py` | Optional specific recipe, not generic repair; component selection does not prove semantic prop identity. |
| `finish/blade_trail.py` | Defer procedural art subsystem from default core; retain only if a demonstrated explicitly approved fallback is wanted. |
| `normal_map.py` | Optional targeted preparation/review; supported inputs, size checks, disclosed GIF loss and labeled lighting visualization. |
| `tileset_preview.py` | Optional 16-corner metadata preview; no cliff/hex/iso/platformer claims. |
| `showcase_gif.py` | Optional requested sharing artifact; not a faithful original playback preview. Four-second truncation/repetition, 128-color quantization and color-key transparency need disclosure/validation. |

## Research and acceptance reconciliation

| Prior requirement | Result at this head |
|---|---|
| Dedicated branch; one shared art core | Structurally met; optional Studio introduces independent policy/state problems. |
| Preserve broad MCP/REST/editor/auth boundaries | Mostly retained; new references still conflict with routing and authority. |
| Automatic approved style continuity on ordinary future requests | Incomplete discovery and effective-style contract. |
| One-off use, temporary named selection, opt-out | Incomplete or absent. |
| Deliberate approved family-anchor replacement | Not preserved by automatic heroes registration. |
| Saved appearance grants no execution authority | Stated, but weakened by global approval-level coupling. |
| One record; actual exposed usage; no new telemetry | Correct architecture intent; accounting and concurrency fail. Telemetry excluded correctly. |
| Normal-map supported inputs versus scoped observations | Unresolved contradiction; imported universal restrictions exceed evidence. |
| Blueprint visual reference versus actual replay | Inherited ambiguity left unresolved. |
| Preserve source pixels; only accepted derivative transformations | Labels added, but raw overwrites, timing and alpha defects remain. |
| Existing install migration, cap reconciliation and appearance drift | Not implemented/validated. |
| Cross-host and representative workflow acceptance | Claude-only dry benchmark and constrained demos; Codex/migration/real panel untested. |
| License, provenance, maintainership/release agreement | Credit present; upstream notice missing; later-source provenance and ownership decisions remain open. |

The maintainer's position is a proposal, not an agreement. The older spike's “do not import now” dispositions are also not immutable bans: this broader user request can justify useful production work. The issues above concern actual necessity, contradictory authority and missing verification, not disobedience to historical recommendations.

## Validation and limits

- Full PR `dev-tools/qa.py`: **255 tests, all passed**, Python 3.13.13, Pillow 12.3.0, numpy 2.5.4, scipy 1.18.1. CI targets Python 3.14; this local run does not substitute for that matrix.
- Focused finishing suite: **22 tests passed**. Additional synthetic probes reproduced the overwrite, accounting, timing, cell-count, compositing and job-ownership defects described above.
- Current Claude plugin validation and **9 existing panel tests passed** in the specialist's run. Three additional mock probes checked project binding, premature settings display and conditional regex cost double counting. These are not a live rendered-panel test.
- The PR body claims 259 QA tests and seven panel tests. Those counts do not match the pinned head's independently observed 255 and nine; documentation should identify the tested revision rather than mix prototype/rebuild results.
- The published 23/23 benchmark is Claude only, one repetition, with route-name/substring scoring. It establishes routing smoke coverage, not authority, artifact integrity, migration, engine import, cross-host behavior or visual quality. Three production demos show real usefulness but remain attributed prototype evidence; complete billing receipts/corpus were not independently audited here.
- No paid provider experiments were run. The normal-map strip-detection dispute, recipe quality generality and engine import fidelity remain empirical limits.

Extend the existing QA and benchmark rather than create another test framework. Prioritize meaningful boundary cases: concurrent ledger mutation; unknown usage/refund; corrupted downloads and output collisions; sheet/GIF/ref preservation; every timing branch without acceptance; blank cells; partial-alpha composition; ordinary saved-style use across fresh sessions; one-job override without persistence; stale/missing family anchors; restrictive legacy caps; old installed instructions; exact reviewed pose identity; and next-version release metadata.

Tests that only assert a particular sentence, filename, table of contents or tool-name regex cannot establish behavior. Some are useful structural checks, but they must not be presented as evidence that the underlying policy is followed.

## Smallest complete route to acceptance

1. Settle one authority contract: existing cost gate, explicit bounded paid plan/retries, separate content review and explicit pixel/playback acceptance. Remove the independent `level` authority and silent host-policy defaults.
2. Preserve the main source identity with a complete narrow style workflow: selected project root, active/temporary style, request override/opt-out, approved save/anchor replacement, nested/legacy behavior and restrictive cap handling.
3. Land the doctor as a reviewed staged capability, beginning with inspection and visual checklist. Correct overwrite/count/timing/job/preview bugs before enabling repair as routine production work.
4. Retain faithful assembly and useful opt-in motion recipes. Consolidate generic mechanics and load only relevant specialty advice. Keep uncertain creative wording as optional guidance/evidence.
5. Keep only finishers with a demonstrated role in an accepted workflow; correct alpha and input protection. Defer the host panel, omnibus finishers and procedural drawing subsystem unless their additional scope is deliberately selected.
6. Preserve upstream notices/provenance, supply safe migration guidance and update existing release checks. Validate representative existing installs and supported host behavior before describing a combined release as ready.

This retains Game Art's useful project and production strengths while keeping Pip's router, portability, neutral defaults and safety boundaries as the foundation.

## Complete changed-file accounting

The following index accounts for all 137 changed PR paths by review family. Family recommendations above apply to every listed file; a file's presence in this index is not unconditional approval. Tests follow retained behavior, and evidence remains useful even when implementation is deferred.

### Packaging, development and top-level documentation

- `.claude-plugin/marketplace.json`
- `.gitignore`
- `README.md`
- `SECURITY.md`
- `dev-tools/skill_benchmark.py`
- `requirements-dev.txt`

### Evidence and user documentation

- `docs/merge/README.md`
- `docs/merge/benchmark-claude.md`
- `docs/merge/demo/README.md`
- `docs/merge/demo/attack-poses.png`
- `docs/merge/demo/attack.gif`
- `docs/merge/demo/candidates.png`
- `docs/merge/demo/farmer-walk.gif`
- `docs/merge/demo/frost-icons.png`
- `docs/merge/demo/marine-attack.gif`
- `docs/merge/demo/marine-skill.gif`
- `docs/merge/demo/skill-poses.png`
- `docs/merge/demo/skill.gif`
- `docs/pixellab/key-pose-animation-evidence.md`
- `docs/pixellab/weapon-page-sources.md`
- `docs/security.md`

### Claude adapter

- `editions/claude/.claude-plugin/plugin.json`
- `editions/claude/.mcp.json`
- `editions/claude/hooks/hooks.json`
- `editions/claude/hooks/panel.test.tsx`
- `editions/claude/hooks/register.tsx`
- `editions/claude/types/index.d.ts`

### Core and operational references

- `skills/pixellab-pip/SKILL.md`
- `skills/pixellab-pip/references/animation-doctor.md`
- `skills/pixellab-pip/references/animation.md`
- `skills/pixellab-pip/references/auto.md`
- `skills/pixellab-pip/references/characters.md`
- `skills/pixellab-pip/references/eight-direction.md`
- `skills/pixellab-pip/references/finishing.md`
- `skills/pixellab-pip/references/icon.md`
- `skills/pixellab-pip/references/image-input-roles.md`
- `skills/pixellab-pip/references/job-lifecycle.md`
- `skills/pixellab-pip/references/key-pose-animation.md`
- `skills/pixellab-pip/references/local-asset-assembly.md`
- `skills/pixellab-pip/references/normal-maps.md`
- `skills/pixellab-pip/references/project-style.md`
- `skills/pixellab-pip/references/reviewable-candidates.md`
- `skills/pixellab-pip/references/scenes-and-backgrounds.md`
- `skills/pixellab-pip/references/style-examples.md`
- `skills/pixellab-pip/references/tileset.md`
- `skills/pixellab-pip/references/usage-reporting.md`
- `skills/pixellab-pip/references/vfx-workbench.md`

### Other runtime helpers

- `skills/pixellab-pip/assets/_assembly.py`
- `skills/pixellab-pip/assets/analyze_style.py`
- `skills/pixellab-pip/assets/bark.py`
- `skills/pixellab-pip/assets/contact_sheet.py`
- `skills/pixellab-pip/assets/fetch.py`
- `skills/pixellab-pip/assets/history.py`
- `skills/pixellab-pip/assets/make_sheet.py`
- `skills/pixellab-pip/assets/manifest.py`
- `skills/pixellab-pip/assets/normal_map.py`
- `skills/pixellab-pip/assets/pad_sprite.py`
- `skills/pixellab-pip/assets/preview_gif.py`
- `skills/pixellab-pip/assets/project_style.py`
- `skills/pixellab-pip/assets/showcase_gif.py`
- `skills/pixellab-pip/assets/tileset_preview.py`

### Finishing implementation

- `skills/pixellab-pip/assets/finish/_derive.py`
- `skills/pixellab-pip/assets/finish/apply_palette.py`
- `skills/pixellab-pip/assets/finish/bake_fx.py`
- `skills/pixellab-pip/assets/finish/blade_trail.py`
- `skills/pixellab-pip/assets/finish/colormatch.py`
- `skills/pixellab-pip/assets/finish/despeckle.py`
- `skills/pixellab-pip/assets/finish/dir8_finish.py`
- `skills/pixellab-pip/assets/finish/ground_snap.py`
- `skills/pixellab-pip/assets/finish/recolor_groups.py`
- `skills/pixellab-pip/assets/finish/recolor_like.py`
- `skills/pixellab-pip/assets/finish/recolor_trail.py`
- `skills/pixellab-pip/assets/finish/scrub.py`
- `skills/pixellab-pip/assets/finish/slash_layer.py`
- `skills/pixellab-pip/assets/finish/throw_prop.py`

### Doctor implementation

- `skills/pixellab-pip/assets/fix.py`
- `skills/pixellab-pip/assets/fixlib/__init__.py`
- `skills/pixellab-pip/assets/fixlib/colour.py`
- `skills/pixellab-pip/assets/fixlib/frames.py`
- `skills/pixellab-pip/assets/fixlib/measure.py`
- `skills/pixellab-pip/assets/fixlib/model.py`
- `skills/pixellab-pip/assets/fixlib/plan.py`
- `skills/pixellab-pip/assets/fixlib/repair.py`
- `skills/pixellab-pip/assets/fixlib/report.py`
- `skills/pixellab-pip/assets/fixlib/thresholds.py`
- `skills/pixellab-pip/assets/fixlib/timing.py`

### Production blueprints

- `skills/pixellab-pip/blueprints/character-candidates.blueprint.json`
- `skills/pixellab-pip/blueprints/overhead-axe-chop.blueprint.json`
- `skills/pixellab-pip/blueprints/projectile-skill.blueprint.json`
- `skills/pixellab-pip/blueprints/vfx-eruption-per-target.blueprint.json`
- `skills/pixellab-pip/blueprints/vfx-strike-single-target.blueprint.json`
- `skills/pixellab-pip/blueprints/vfx-wave-across-party.blueprint.json`

### Motion specialty references

- `skills/pixellab-pip/references/armor-clothing.md`
- `skills/pixellab-pip/references/martial-arts.md`
- `skills/pixellab-pip/references/weapon-anime.md`
- `skills/pixellab-pip/references/weapon-axe.md`
- `skills/pixellab-pip/references/weapon-bow.md`
- `skills/pixellab-pip/references/weapon-dagger.md`
- `skills/pixellab-pip/references/weapon-effects.md`
- `skills/pixellab-pip/references/weapon-firearms.md`
- `skills/pixellab-pip/references/weapon-futuristic.md`
- `skills/pixellab-pip/references/weapon-katana.md`
- `skills/pixellab-pip/references/weapon-mace.md`
- `skills/pixellab-pip/references/weapon-spear.md`
- `skills/pixellab-pip/references/weapon-staff.md`
- `skills/pixellab-pip/references/weapon-sword-and-shield.md`
- `skills/pixellab-pip/references/weapon-sword.md`
- `skills/pixellab-pip/references/weapon-war-hammer.md`
- `skills/pixellab-pip/references/weapon-whip.md`

### Doctor tests and fixtures

- `tests/doctor_cases/conftest.py`
- `tests/doctor_cases/synth.py`
- `tests/doctor_cases/test_cli.py`
- `tests/doctor_cases/test_frames.py`
- `tests/doctor_cases/test_fx_frames.py`
- `tests/doctor_cases/test_look.py`
- `tests/doctor_cases/test_measure_clean.py`
- `tests/doctor_cases/test_measure_crisp.py`
- `tests/doctor_cases/test_measure_identity.py`
- `tests/doctor_cases/test_measure_motion.py`
- `tests/doctor_cases/test_minors.py`
- `tests/doctor_cases/test_plan.py`
- `tests/doctor_cases/test_repair.py`
- `tests/doctor_cases/test_review.py`
- `tests/doctor_cases/test_stepped.py`
- `tests/doctor_cases/test_timing.py`
- `tests/test_doctor.py`
- `tests/test_doctor_rules.py`

### Other regression tests

- `tests/test_approval_levels.py`
- `tests/test_assembly.py`
- `tests/test_blueprints.py`
- `tests/test_claude_edition.py`
- `tests/test_extras.py`
- `tests/test_fetch.py`
- `tests/test_finishing.py`
- `tests/test_manifest.py`
- `tests/test_project_style.py`
- `tests/test_references.py`
