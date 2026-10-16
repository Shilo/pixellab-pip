# PixelLab Game Art And Pip: Merge Research Spike

## Summary: What Is Needed

Work toward **a shared product that combines Pip's general PixelLab routing with Game Art's personalized project workflow**. Preserving project continuity is the main identity decision; one versus multiple skills remains open.

1. Agree common rules for API constraints, spending/retries, output changes and privacy. Saved preferences grant no execution authority.
2. Start with a jointly reviewed normal-map correction and a bounded test if needed, with separate approval for paid calls. Review blueprint reference-versus-replay routing next.
3. Define how a chosen project's style and approved references persist and apply to later jobs. Choose the smallest mechanism; do not substitute occasional manual notes for a promised continuity feature.
4. Before a shared release, settle naming, credit, maintenance ownership, QA and migration for anything that actually changes.

Original review: 2026-10-15. Follow-up: source and fixture research into personalization and packaging. Status: research and recommendation only; no runtime changes implemented.

Pip baseline: v2.2.0, commit `43da5765a44e1fba955592999cb10867ca990138`. Game Art baseline: v1.4.0, commit `92614b51bf99638899521cdf4fb74435ba8a47db`, verified against its remote default-branch HEAD for this review. See the [current feature comparison](pixellab-game-art-vs-pip-skill.md) for the complete inventory and helper limitations.

## Recommendation

Support joint maintenance and phased convergence toward a general-purpose, agent-agnostic product if both maintainers choose it. Preserve Game Art's project-personalized experience while retaining Pip's broad routes and protections. Avoid a mechanical union of instruction sets and helpers. One shared skill with commands is a starting candidate; multiple focused skills sharing the same contract are also open for evaluation.

This extends the original review to a collaboration scenario: shared fixes, complementary expertise, one maintained release and one source of documentation can benefit users. Co-maintenance distributes the work; dependency upkeep, testing and coordination still need owners. Those are potential benefits of joint development, not measured savings or an agreement already reached between maintainers. The earlier recommendation against a codebase merge concerned wholesale adoption under the then-reviewed scope; it was not a reason to keep competing projects or reject collaboration.

The corrected immediate proposal is deliberately small: shorten the normal-map row without excluding MCP strips, and distinguish a blueprint used only as a visual reference from a request to replay it. The earlier terrain-chain and extra tile-review proposals are withdrawn after checking connected MCP descriptions and existing Pip verification. These remain recommendations for later implementation, not features shipped by this spike.

Personalized project direction remains compatible with Pip: users can explicitly supply visual requirements and approved references today. Ordinary project notes can provide user-selected context, but Pip has no dedicated project-note selection mechanism; this is manual user/host work, not a shipped continuity feature. Existing blueprints already represent requested chains. Neither practice provides Game Art's automatic reuse of the user's selected active style and onboarding convenience; that usability gap remains real.

## Merging The Product Identity

**The main Game Art identity is an ongoing project-art workflow, not a collection of commands.** The user's two-part description correctly identifies personalization as central. Named commands may be ordinary task references or separate skill wrappers; their packaging does not create the personalization. A third dimension also matters: Game Art packages production choices such as drafts, key-pose chains, timing, review and finishing. Those choices need separate decisions from appearance and command packaging.

A merge that adds only inspection helpers or routing corrections while leaving all project-context selection to the user has not preserved this main identity. Conversely, preserving continuity does not require importing every preset, analyzer, helper or finishing rule. The combined product can be neutral before a project is selected and follow that project's deliberately chosen direction afterward.

### How The Reviewed Personalization Actually Works

All Game Art paths in this section refer to the pinned `any-agent/pixellab-game-art/` source unless stated otherwise.

| Stage | Actual behavior | Evidence and boundary |
|---|---|---|
| Establish the project | `pga-init` accepts reference art, parameters or both; proposes direction with provenance, offers changes and an optional paid draft, then saves reviewed settings | `references/tasks/pga-init.md`. The shared loop requires setup for most generating tasks without a profile; several tasks are exempt. This mandatory onboarding is a product choice, not necessary for one-off Pip requests. |
| Select reusable direction | `pixellab.json` stores project fields, named `styles` and `active_style`; `--style` selects a different style for one task | `references/parameters.md` and `scripts/style.py`. Existing data persists across processes; the agent is instructed to interpret precedence. |
| Reuse appropriate images | Approved family anchors distinguish heroes, monsters, backgrounds, scenes, buildings, icons and UI | `references/tasks/pga-style.md` and `scripts/style.py`. There is no terrain anchor family in this helper. One hero image is not a universal reference for every asset class. |
| Apply direction to a job | The host reads project/profile rules, overlays the selected style, applies current-request overrides, chooses the task template and maps appearance/anchors to tool inputs | `references/prompt_improver.md` and `references/parameters.md`. No bundled effective-style resolver or submit client enforces this pipeline; it depends on the agent following instructions. |
| Review and approve changes | Local QA and visual review compare results with the anchor; `pga-style anchor` explicitly replaces a family's stored reference | `references/prompt_improver.md` and `references/tasks/pga-style.md`. Job verdicts are history, not model training or automatic promotion of every good result to a new anchor. |
| Continue in another session | The next applicable task reads the same project file and selected style instead of requiring the user to reconstruct the direction | `references/prompt_improver.md`, project-profile section. The state is in project files, not durable model memory. Helpers default to a profile in the process working directory; `--profile` selects another file but does not rebase stored relative anchor paths. |

`pga-analyze` is one optional way to establish direction: it combines scripted measurements with agent visual interpretation and a user-reviewed save step. Its light/outline/dither/native-scale outputs are heuristics, not objective style truth. It writes derived native frames, including approximate downsampling and background keying; those may differ from the input art. Reviewed direction and approved references can therefore be preserved without importing this analyzer or automatically accepting its derived images.

The shared loop also connects profile fields to local palette enforcement, drafts and animation finishing. Preserving a palette preference must not silently import permission to recolor final art, add paid drafts or remove frames. Appearance requirements and execution authority need distinct treatment.

### What The Source And Offline Checks Do Not Guarantee

Ten isolated checks of fully inspected `profile.py` and `style.py` confirmed persistence and specific CRUD behavior; they did not execute generation, analysis, installers or a whole agent session. In particular, showing a style returns that saved object, not a resolved effective profile; saving without `--from` copies top-level style fields rather than the active style's effective values; saving an existing name replaces the whole saved style. Anchor registration stores a path without copying the image and can persist an existing non-image file while silently ignoring decode failure. Rename collisions overwrite the target, and deleting the active style selects another alphabetically.

These behaviors make direct code adoption a separate decision from preserving the experience. Nested-field inheritance, path resolution, stale references and style replacement need a deliberate contract; no code resolver exists to prove how the host merges nested fields. Persistence tests establish neither prompt compliance nor matching generated art.

### Challenge To The Proposed Identity

- **Personalized does not have to mean a fixed house look.** The useful part is carrying the user's reviewed game direction forward. Dark-fantasy presets, fixed seeds and particular combat timings are replaceable choices. Some category templates retain house wording despite the general user-precedence instruction, so copying both can reintroduce conflicting defaults.
- **Commands, skills and subagents are different.** The portable package has one skill with 22 task references. The Claude package has a core plus 22 explicit task-skill wrappers; optional portable-host installation can create 19 subagent configurations. These do not establish that personalization needs multiple skills or that every command is an isolated subagent. Both distributions share the same style/profile logic.
- **Manual notes are a workaround, not equivalent continuity.** A selected project file still needs real save/select/read/override/update behavior even if its format is plain Markdown. Calling it simple notes does not eliminate those state decisions.
- **Continuity does not require the whole manager.** One selected, saved project direction with appropriate approved references is the smallest design candidate. Multiple saved looks can be useful when, for example, the same project deliberately switches between overworld and nightmare-realm art for the same asset families; that scenario motivates evaluating named variants, not automatically building a catalog. Ordinary icon-versus-character differences can be handled by family references and do not alone require several styles.

### Minimum Experience To Preserve And Validate

The proposed combined identity should let a user establish and approve project direction, select it, and have later applicable jobs visibly reuse it with the correct family reference. Current-job overrides should leave saved direction unchanged unless the user asks to update it. Reference replacement must be deliberate, other projects must remain isolated, and one-off tasks must work without forced project setup. Missing or ambiguous references must not trigger paid reconstruction or silent cross-family substitution.

For example: choose a game's shared palette/outline and separate approved hero and icon references; return in a later session to request shop icons; the agent uses the selected direction and icon reference while choosing the icon route. A one-job outline override does not rewrite the project's style. This is more than replaying a hero blueprint and more convenient than repeatedly attaching all project notes. It is proposed behavior, not implemented Pip functionality or guaranteed pixel-level fidelity.

Maintainers still need to agree the state format and location, explicit activation/deactivation, path base, nested overrides, missing/stale-reference behavior and whether named multi-style switching belongs in the first release. A full style-manager CLI, automatic art analysis, history search and the finishing suite do not follow automatically from this requirement.

## Recommended Next Tasks (Not Implemented)

| Next task | Canonical home or review location | Completion check | Status |
|---|---|---|---|
| Define the shared project-personalization experience | Identity section above; joint product design | Agree save/select/reuse/override/update behavior, family references and project isolation; distinguish the minimum continuity goal from a full style manager | Primary merge design task; no implementation |
| Choose skill and command packaging | Options below | Compare one portable skill with commands against focused skills sharing one contract and project context; test policy loading and intent separation rather than assuming a skill count | Open design decision |
| Shorten and correct normal-map input wording | Existing [image-role row](../../skills/pixellab-pip/references/image-input-roles.md#goal-router) | Remove the universal strip requirement; retain MCP animation reference/GIF/strip support and shared size/frame limits; keep the explicit strip count REST-only | Proposed; not implemented |
| Distinguish blueprint reference use from replay | Existing [SKILL intent router](../../skills/pixellab-pip/SKILL.md#intent-router) | Route a different asset normally when a blueprint is only its look/identity source; use identifiable existing output images, never replay to obtain them; scope the recorded-route column to actual replay | Proposed; not implemented; no observed misgeneration |
| Agree authority boundaries and jointly review a normal-map pilot | This spike and each repository's normal-map guidance | Agree request/schema/preference boundaries; define a bounded experiment if needed, obtain paid-call approval separately, retain observations and review each other's evidence-based changes; blueprint routing follows as the second contribution | Proposed; no test, contact or merger agreement assumed |

The [comparison spike](pixellab-game-art-vs-pip-skill.md#recommended-next-tasks-not-implemented) carries the same immediate tasks. The bounded edits and acceptance scenarios below define their scope. They may be contributed and reviewed before deciding a shared name or final repository structure; run `python dev-tools/qa.py` after implementation.

## Questions And Evidence

The review asks which additions change an agent decision Pip currently gets wrong or omits, how Game Art's personalization actually works, and how a combined product can preserve neutrality, broad applicability and useful project continuity. The latest discussion reopens one versus multiple skill entry points; the earlier single-skill preference is no longer treated as a fixed merged-product constraint.

Evidence reviewed:

- Pip's [canonical skill](../../skills/pixellab-pip/SKILL.md), [image roles](../../skills/pixellab-pip/references/image-input-roles.md), [tilesets](../../skills/pixellab-pip/references/tileset.md), [animation](../../skills/pixellab-pip/references/animation.md), [cinematics](../../skills/pixellab-pip/references/cinematic.md), [style references](../../skills/pixellab-pip/references/style-reference.md), [blueprints](../../skills/pixellab-pip/references/blueprint.md), [cost approval](../../skills/pixellab-pip/references/auto.md), and [local assembly](../../skills/pixellab-pip/references/local-asset-assembly.md).
- Game Art's pinned [portable skill](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/SKILL.md), [task loop](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/prompt_improver.md), [style precedence and profiles](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/parameters.md), [terrain task](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-tiles.md), [normal-map task](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-normal.md), animation recipes and helper implementations.
- Both Game Art distributions, installer/model-task mappings, and its [MIT license](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/LICENSE).
- The personalization follow-up traces [init](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-init.md), [style management](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-style.md), [analysis](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-analyze.md), category tasks, and the fully inspected [style](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/scripts/style.py) and [profile](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/scripts/profile.py) helpers. Ten disposable local checks exercise only their saved-state behavior. Installer and wrapper conclusions are static source findings, not host compatibility tests.
- The [official MCP guide](https://api.pixellab.ai/mcp/docs) and [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json), retrieved on 2026-10-15, followed by a corrective review against the connected `create_normal_map` and `create_topdown_tileset` tool descriptions and argument definitions exposed to the agent. These are different provider evidence surfaces; the web guide alone did not capture all accepted inputs or resolve contradictory scheduling advice. Tool definitions were inspected without invoking generation. These checks do not establish generated-art quality or the success of an engine import.

One reviewer challenged the additions. Two others directly debated personalization versus minimalism, exchanged rebuttals, and revised their positions. The parent challenged their conclusions again for duplication, hidden state, unnecessary artifacts, description enhancement, and imposed scheduling. The material disagreements and concessions appear below. Agreement is a design judgment, not experimental proof.

### Corrections After The Independent Claude Review

The earlier research treated the web guide as sufficient MCP evidence. That missed material information in the connected tool descriptions. The parent and both original merge reviewers independently checked those descriptions and revised their recommendations:

- `create_normal_map` explicitly accepts an animation reference, GIF or strip and documents 8–512 px per frame, up to 32 frames. It has no `frames` argument. REST explicitly pairs a PNG strip with `frames`. Do not turn Game Art's reported strip failure into a universal MCP restriction.
- `create_topdown_tileset` already explains shared base-ID chaining. REST's lower/upper base-ID fields are described as metadata identifiers; that does not document equivalent visual linkage. The proposed generic chaining rule is withdrawn.
- The connected tileset description says to wait for completion; the web guide's example says no waiting. The earlier unqualified scheduling conclusion is withdrawn. Record this provider conflict without adding either rule to Pip or treating it as resolved behavior.
- Pip already assembles all returned tiles in their returned order and has constraint/grid inspection. No missing Pip verification action was demonstrated by Game Art's random-map diagonal issue, so the extra tile-review proposal is withdrawn. Inspection itself never authorizes a paid retry; redundancy and lack of a demonstrated gap are the reasons for dropping it.
- The blueprint router has a separate textual ambiguity: a file supplied only as a look/identity reference can enter the recreation path. This is supported by the routing text, not an observed failed run. Its frequency and practical cost remain unmeasured.

## Correcting The Starting Assumptions

**One skill does not mean one flat instruction file.** Game Art's portable distribution already uses one `SKILL.md` with task references and optional host-specific dispatch. Its Claude distribution exposes separate `pga-*` task skills. Multiple visible skills are a distribution choice, not a requirement for personalized workflows. Retaining one discoverable skill with relevant references is an option; it is not the only permissible outcome of this identity discussion.

**Neutrality does not mean refusing personalization.** A user asking to reuse their own palette, proportions, view and references is giving task requirements. An automatic dark-fantasy preset, fixed seed, preferred character size or mandatory combat timing would be a product opinion. The first fits Pip; silently imposing the second does not.

**Chains are already part of Pip.** Whole-chain approval, first/last-frame anchors, cinematics, ordered blueprints and local `TASK` steps already exist. Game Art contributes packaged recipes and convenient project continuity, not a missing general workflow engine.

**A style profile is not a blueprint.** A named style applies art direction across unrelated future assets; a blueprint records/replays particular requests and local steps. Pip's manifests record private usage and resume information. Neither existing mechanism is an automatic style catalog.

## Strengths And Costs Of Each Product

| Concern | Pip | Game Art |
|---|---|---|
| General requests and exact controls | Broad surface routing, field fidelity and specialized operational constraints; the user/agent still makes production choices | Guided tasks reduce planning for matching workflows; house choices can bias unrelated requests |
| Ongoing project continuity | Accepts explicitly supplied direction and references; users/hosts must retrieve and select them again | Named styles, active selection and family anchors make repeated work easier; adds profile precedence and persistent-state maintenance |
| Multi-step production | Existing chains and blueprints allow request-specific plans; less ready-made finishing | Combat/terrain/lighting recipes package preparation and review; assumptions, transformations and costs must fit the request |
| Local tooling | Small optional inspector, existing assembly/editor routes and host tools; some work requires host scripting | Larger helper suite saves assembly work in supported cases; more dependencies, formats, edge cases and tests to own |
| Spending and preservation | Explicit approved chains, raw-output preservation and declared processing; may require more deliberate choices | Fewer permission interruptions and automatic defect handling; different authority for retries and local changes |
| Portability and upkeep | One skill with progressive discovery and multiple public surfaces; broad provider contracts need maintenance | Portable one-skill package plus Claude task wrappers; profile, helper, dispatch and update machinery adds upkeep |

Neither source review nor the published examples establishes a universal best skill, lower total cost, or better art. Game Art is a better fit for someone who wants its personalized production system and accepts its policies. Pip is a better base for this project's stated goals. A union of both would not automatically retain the benefits of either.

## Which Additions And Review Findings Are Worth Adapting Now?

The table covers the v1.4.0 delta and the blueprint-routing ambiguity identified during the independent follow-up. The latter is a Pip finding, not a new Game Art feature. Pip's earlier motion-aware padding rule and optional image inspector are already shipped and are not proposed again.

| Addition | Case for adapting it | Challenge and agreed disposition |
|---|---|---|
| Normal-map input handling | The row's universal strip requirement excludes documented MCP alternatives and unnecessarily scopes shared limits to REST. | **Recommend a shorter correction:** remove that requirement and the REST-only limit qualifier; include MCP strip support and keep explicit `frames` REST-only. Leave the already-correct SKILL normal-map router unchanged. |
| Shared terrain in a requested chain | Chaining is useful, but the connected MCP tool already teaches it. REST documents the fields only as metadata identifiers. | **Withdraw the proposed rule:** redundant for MCP and not justified as REST visual-linkage guidance. |
| Complete tileset review | Game Art's example map may miss diagonals. Pip's returned sheet already includes every tile and existing checks apply. | **Withdraw the proposed rule:** no distinct missing Pip action established. Keep existing inspection and spending boundaries. |
| Blueprint supplied only as a visual source | The router includes any supplied blueprint, while the recreation path selects its recorded workflow; this can compete with new-asset intent. | **Recommend a routing clarification:** classify the new asset normally and use identifiable existing output images as references; actual replay keeps its recorded-route behavior. No new style state or automatic reference generation. |
| Normal-map packing, splitting and lighting helper | Convenient preparation and visual shading checks for actual engine workflows | **Do not import now.** Host tools cover preparation; the reviewed GIF path quantizes colors/alpha, and the preview assumes OpenGL. Extra validation/engine tooling needs a concrete task. |
| Terrain preview helper | Repeatable preview can expose seams before engine import | **Do not import now.** Reviewed code handles 16-tile square-corner sets, rejects cliffs, and has a single-sheet CLI guard problem. One narrow renderer cannot stand in for Pip's broader layout support. |
| Brightness/color matching | May remove unwanted drift across generated frames | **Reject automatic normalization; no helper now.** Mean brightness cannot distinguish drift from intentional lighting or effects, and the default overwrites files. Requested palette work already has supported routes. |
| Hit/kick recipes and pose-based normal segmentation | Concrete key poses and shorter segments may improve some actions | **No global recipe or automatic segmentation.** Existing anchors/chains cover the mechanism. Fixed models, frame counts, timing, cleanup and extra paid calls lack general validation. |
| Expanded palette notes and beginner examples | Better explanations and examples can improve discoverability | Palette routing is **already covered** in Pip. Upstream examples do not establish a new Pip capability or justify another runtime contract. |

The two proposed canonical edits are bounded as follows:

1. **Image-role row:** delete the universal strip sentence, remove the REST-only qualifier from the shared 8–512 px / 32-frame limits, and include documented MCP animation-reference/GIF/strip inputs. Keep the REST PNG strip plus explicit `frames` distinction; a single sprite may use default `frames=1`. Do not invent an MCP frame-count argument or impose format conversion. MCP's method of determining strip frame count remains untested.
2. **Blueprint router:** when a blueprint is supplied only as the look/identity source for a different asset, route that asset normally and classify identifiable existing output images through the existing image-role guidance. Do not replay the blueprint to create missing references. A blueprint may name no outputs, or its recorded outputs may not exist; use existing clarification rules where the source is unavailable or ambiguous. Do not inherit recorded endpoints, size, seed, mode or unrelated subject details. Scope the row's recorded-route column to actual replay so it does not contradict the exception. This is a routing distinction, not a new output resolver or style manager.

A broader normal-map verification proposal was considered and removed from the immediate scope. The row already describes dimensions and binary alpha, while new mandatory lighting previews would add dependencies or deliverables. Exact equality with source alpha would also be wrong for partially transparent source pixels when the normal-map output uses binary alpha.

## Merge Options Challenged

| Approach | Benefit | Cost or conflict | Recommendation |
|---|---|---|---|
| Vendor both codebases and adopt all workflows | Fastest access to the full helper/profile suite | Conflicting execution policies, duplicate contracts, dependency and update ownership, mixed state and attribution obligations | Reject now |
| Mechanically repackage commands under one skill, in the main file or task references | One visible entry point and familiar task names | Packaging alone leaves conflicting behavior and duplicate routing; a flat main file additionally increases loaded instructions | Reject a packaging-only merge |
| Keep both broad skills unchanged | Preserves both existing installations | Overlapping triggers, duplicate policy and conflicting state/authority remain unresolved | Reject unchanged coexistence as the merge design |
| One shared skill with named commands and on-demand task references | One general entry point and canonical contract; project continuity can be shared across tasks | Router growth and project-context selection still need testing; native command exposure varies by host | Simplest starting candidate, not a settled requirement |
| Multiple focused skills sharing the project context and canonical contract | Explicit setup/style/task entry points may improve discoverability or separate curator/planner work from execution | Must prove shared safeguards load, avoid competing generators and keep state selection consistent; extra packaging/update work | Open alternative if concrete UX or dispatch benefit justifies it |
| Keep the architecture; selectively adapt useful decisions | Small contributions can start without a new framework | Router fixes alone do not preserve Game Art's primary personalized identity | Useful collaboration pilot; insufficient as the complete identity merge |

The immediate implementation scope remains research and small proposed guidance fixes. The shared product now needs an explicit personalization design in addition to those fixes. That does not yet select a profile schema, automatic project discovery, second log, installer merger, workflow graph or second execution framework.

## A Practical Path To A Shared Product

There is no demonstrated technical incompatibility that prevents one combined skill. Both products are chiefly instructions plus Python helpers. The difficult part is choosing one consistent behavior when their current instructions disagree; combining files alone leaves the agent with conflicting directions.

The product identity can accommodate both strengths: neutral general PixelLab handling and persistent user-selected project direction with relevant production workflows. One or several entry points can expose that experience if they share consistent authority and state. A one-off icon request should remain usable without a project profile. This is a proposed product boundary, not an implemented profile system.

Practical next steps:

1. **Agree precedence and authority alongside the pilot.** The current request defines the desired result within valid API fields and spending, credential and output-integrity protections. Selected project preferences supply applicable defaults within those boundaries; they grant no execution authority. Record overlapping rules' canonical homes and unresolved decisions here rather than creating another governance framework. Small contributions need only resolve the policies they touch; a merged release needs a coherent overall contract.
2. **Use normal maps as the first reciprocal contribution.** Define a small reproducible case together, or review the creator's existing evidence. If a paid experiment is needed, obtain separate approval for its inputs, calls and cost before running it. Use a known number of distinguishable frames and check returned frame count, dimensions and correspondence. Each maintainer then reviews the other's evidence-based documentation correction. A successful or failed case establishes those conditions, not all possible strip arrangements. The already-supported correction to Pip's universal-strip wording need not wait for a paid test.
3. **Review blueprint routing second.** Use the bounded clarification and semantic cases below. It is an improvement to reference-versus-replay routing, not automatic project-style continuity. It requires no imported helper, new profile state or rebrand.
4. **Choose the combined MVP and release identity together.** Early collaboration fixes may ship without a continuity feature, but a release claiming to preserve Game Art's personalized identity must implement the agreed minimum continuity behavior. A user-visible, explicitly selected project file is one candidate mechanism; define project scope, overrides, staleness and read timing before adding state. Walk through a concrete shared workflow and include multiple-style switching if the intended users require it. Before combined distribution, agree the name, contributor credit, canonical rule ownership, review/QA responsibilities and public expectations. No particular packaging, profile design or migration policy has been agreed by this research.
5. **Migrate only what the adopted design requires.** If commands, credential-variable names, config, styles, outputs or installation paths change, define their treatment and test representative existing projects in an isolated checkout. Do not overwrite user profiles or artifacts, promise compatibility without tests, or build migration machinery for unchanged formats. Publish appropriate version/migration notes and ship only after the selected workflows and supported hosts have been checked.

This allows cooperation immediately while keeping unproven feature imports out of the runtime. It also leaves a real decision for maintainers: whether the shared identity promises a neutral PixelLab tool for everyone with optional project continuity, or a prescriptive production system. Those identities can coexist only when the production choices are deliberately selected and their authority is explicit.

## Conflicts A Real Merge Would Have To Resolve

| Area | Material difference | Required disposition for any future Pip integration |
|---|---|---|
| Aesthetic and model defaults | Game Art supplies genre, density, facing, size, seed and recipe defaults; Pip follows the request and selected route | User-chosen direction may guide art; absence of direction must not activate a house aesthetic or fixed recipe |
| Paid work and retries | Game Art's loop avoids permission prompts and allows defect retries; Pip has explicit whole-chain and extra-spend rules | Preserve Pip's spending protections. Any retry allowance needs approved operations, attempt limits, stop conditions and budget; a budget alone is not an open-ended retry mandate, and a style preference grants no spending authority |
| Final pixels and playback | Game Art normalizes colors, cleans flashes and selects/drops/mirrors frames in finishing | Preserve raw outputs and label derivatives. Any workflow-authorized transforms must be clearly disclosed and deliberately accepted for the job; selecting a broad skill or saved style does not approve them |
| Schema authority | Upstream includes both house-observation precedence and live-schema precedence language | Public schemas define accepted fields; reproducible observed behavior remains separate evidence of what actually works. Retain both when they disagree, without inventing parameters or erasing failures |
| Credentials and surfaces | Game Art executes through MCP; Pip also supports public REST and editor/website boundaries | Preserve Pip's secret handling and public/private endpoint distinction; never import credential values |
| Reporting and external sharing | Game Art has project logs and opt-in author feedback; Pip has manifests and blueprints | Reuse Pip records and actual exposed usage; do not add a second log or an external-sharing channel as a merge side effect |
| State and task authority | Active styles and project profiles can affect many future calls | No hidden scope expansion. Art notes cannot grant permission for paid, destructive, external or local pixel-changing actions |
| Packaging and maintenance | Host task wrappers, optional model dispatch, helper dependencies and updater behavior differ | Choose one or multiple entry points deliberately; verify shared-contract loading, intent separation and project context, and own tests/updates for adopted behavior |

The upstream license is MIT. If future work copies source or substantial portions, preserve its copyright and permission notice; this spike copies no helper code. Record an upstream revision and provenance for any adopted material. Skill-source licensing does not establish rights for generated or supplied art.

## Debate Record And Agreed Concessions

The table summarizes arguments actually exchanged, not hypothetical reviewers. Detailed working notes and challenge excerpts are retained privately for the Claude handoff.

| Challenge | Initial tension | Result after rebuttal |
|---|---|---|
| Does existing replay remove the need for project continuity? | The first debate established manual task satisfiability, not preservation of the other product's identity | The personalization follow-up rejects equivalence: saved direction reused across sessions needs real state/selection semantics. The minimum mechanism remains a design candidate. |
| Does neutrality prohibit project direction? | Compatibility with user-selected direction was a shared premise; the debate tested where preferences would become imposed defaults | Both retained user-led personalization. Its usefulness alone does not justify new state, discovery or a profile schema. |
| Are optional recipes inherently out of scope? | Minimalism resisted fixed combat defaults; personalization defended requested recipes | Both accept a tested requested chain could fit one skill. Pip already has the mechanism, so no fixed hit/kick recipe is needed now. |
| Is terrain review too specialized? | A renderer import looked narrow; personalization emphasized terrain continuity | Review is useful within tileset intent, but the follow-up found existing all-tile assembly/grid checks and no distinct Pip gap. The proposed extra rule is withdrawn. |
| Is listing chaining fields enough? | The first review checked Pip's field names but missed the live tool's full recipe | The original acceptance is superseded: MCP already teaches the linkage, and REST visual equivalence is unproven. No tileset edit remains proposed. |
| Which terrain description and schedule should be reused? | The first debate narrowed text preservation but relied on the web example for timing | The whole chain addition is withdrawn. Connected MCP and the guide conflict on waiting; no new scheduling rule is justified by this research. |
| Should normal-map lighting checks be added too? | Addition reviewer initially proposed structural/lighting checks alongside transport correction | Parent challenged duplication, binary alpha and unwanted previews. Reviewer narrowed the immediate recommendation to input correctness. |
| Does a merge need new state now? | Earlier Pip-only scope deferred style tooling; the user now prioritizes personalized continuity in the combined product | Both reviewers support researching a narrow save/select/load/apply/review/update loop. This reopens state design without approving a complete manager or implementation. |

Original review consensus rejected an immediate architectural/codebase union and deferred a profile system under the earlier scope. Its normal-map format restriction and both tileset proposals were subsequently corrected or withdrawn. The later source/fixture follow-up and two further direct debate rounds changed the identity recommendation: project continuity is a primary shared-product design task, and one versus multiple skills is open. The normal-map and blueprint corrections remain small contribution candidates; neither is a substitute for preserving personalization. No profile implementation or wholesale helper import is approved by these findings.

## Validation And Decision Gates

No provider generation, installer run, engine import, telemetry submission or runtime implementation was performed. The earlier source review executed no upstream helpers; the personalization follow-up executed only fully inspected `profile.py` and `style.py` in disposable synthetic profiles, with ten checks passing. No analyzer, finisher or generation client ran. Repository QA validates the research artifact and existing code; neither QA nor CRUD checks test a complete personalized agent workflow or generated style quality.

For the proposed normal-map correction, review dry scenarios for one sprite, MCP GIF, MCP managed animation reference, MCP strip and REST strip plus frame count. Keep 8–512 px / 32-frame limits on both surfaces, preserve convention, invent no MCP `frames` argument and add no conversion or segmentation. This checks documented routing, not whether MCP correctly detects frame count for an arbitrary strip.

For blueprint routing, review: "shop icons in the style of hero.blueprint.json" uses the icon route and existing hero images as references; "remake hero.blueprint.json" replays; "hero.blueprint.json but with a red cape" remains replay with an override. Missing, ambiguous or template-only outputs must not cause reference-generating replay. No recorded route/size/seed/mode leaks into the different asset. These are semantic acceptance cases, not evidence that an agent has already misgenerated an asset. Make no tileset runtime changes. Run `python dev-tools/qa.py` after implementation.

Project continuity is now an explicit shared-product design goal, superseding the earlier treatment as merely a deferred convenience. Validate the smallest candidate with cross-session hero/icon reference selection, current-job overrides without unintended saves, explicit anchor replacement, project switching, missing references and one-off use. If multiple named looks are required, test explicit switching and stale/missing selections. Any skill arrangement must load the same safeguards and selected context. These are future behavior tests; the ten helper checks do not establish them.

Any future recipe must solve a repeated request better than existing references/blueprints without imposing its aesthetic or cost policy. Any helper must solve a demonstrated need and pass fixtures for every layout, image representation and transformation it claims to support. If a claim needs paid quality or engine-import testing, define that experiment and cost before treating it as proven.

Remaining empirical questions are MCP strip frame-count detection, REST base IDs' visual effect, contradictory chain scheduling, actual blueprint-as-reference frequency, manual project-direction effort, and comparative recipe quality/cost. A scoped, separately approved experiment can investigate provider behavior; no paid test was run here. Agreement among agents cannot answer these questions. No implementation is implied by this corrected recommendation.
