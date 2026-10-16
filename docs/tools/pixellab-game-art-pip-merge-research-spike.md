# PixelLab Game Art And Pip: Merge Research Spike

Reviewed: 2026-10-15. Status: research and recommendation only; no runtime changes implemented.

Pip baseline: v2.2.0, commit `43da5765a44e1fba955592999cb10867ca990138`. Game Art baseline: v1.4.0, commit `92614b51bf99638899521cdf4fb74435ba8a47db`, verified against its remote default-branch HEAD for this review. See the [current feature comparison](pixellab-game-art-vs-pip-skill.md) for the complete inventory and helper limitations.

## Recommendation

Support joint maintenance and phased convergence toward one general-purpose, agent-agnostic skill if both maintainers choose a shared product. Avoid an immediate mechanical union of the codebases, helper suite and runtime instructions. Start with selectively adapted, verified operational improvements in existing references; no new project-style state is needed for that first step.

This extends the original review to a collaboration scenario: shared fixes, complementary expertise, one maintained release and one source of documentation can benefit users. Those are potential benefits of joint development, not measured savings or an agreement already reached between maintainers. The earlier recommendation against a codebase merge concerned wholesale adoption under the then-reviewed scope; it was not a reason to keep competing projects or reject collaboration.

The immediate proposal is deliberately small: correct the MCP-versus-REST normal-map input distinction, explain shared base-tile reuse for a requested terrain chain, and review all returned tile configurations rather than relying on an example map. These are recommendations for a later implementation, not features shipped by this spike.

Personalized project direction remains compatible with Pip: users can explicitly supply art-direction notes and approved references today. Existing blueprints already represent requested chains. Those practices do not provide Game Art's automatic reuse of the user's selected active style and onboarding convenience; that usability gap remains real.

## Recommended Next Tasks (Not Implemented)

| Next task | Canonical home or review location | Completion check | Status |
|---|---|---|---|
| Correct normal-map input wording | Existing [image-role row](../../skills/pixellab-pip/references/image-input-roles.md#goal-router) | Distinguish MCP animation references/GIF from REST PNG strips and their frame count; retain correct single-sprite behavior without a new helper | Proposed; not implemented |
| Clarify requested terrain-chain linkage and complete tile review | Existing [tileset reference](../../skills/pixellab-pip/references/tileset.md) | Reuse the shared returned base ID/stored description; inspect actual returned configurations and shared seams without new artifacts, defaults, scheduling rules or retries | Proposed; not implemented |
| Jointly review a small integration pilot and the shared product contract | This spike and the existing review process | Review the two edits under Pip's current contract; map overlapping rules/helpers to keep, adapt or defer; record unresolved default, personalization and release decisions | Proposed; no merger agreement assumed |

The [comparison spike](pixellab-game-art-vs-pip-skill.md#recommended-next-tasks-not-implemented) carries the same immediate tasks. The bounded edits and acceptance scenarios below define their scope. They may be contributed and reviewed before deciding a shared name or final repository structure; run `python dev-tools/qa.py` after implementation.

## Questions And Evidence

The review asks which v1.4.0 additions change an agent decision Pip currently gets wrong or omits, whether hosts can already perform the local work, and whether a combined product can preserve neutrality, broad applicability, and a single skill entry point.

Evidence reviewed:

- Pip's [canonical skill](../../skills/pixellab-pip/SKILL.md), [image roles](../../skills/pixellab-pip/references/image-input-roles.md), [tilesets](../../skills/pixellab-pip/references/tileset.md), [animation](../../skills/pixellab-pip/references/animation.md), [cinematics](../../skills/pixellab-pip/references/cinematic.md), [style references](../../skills/pixellab-pip/references/style-reference.md), [blueprints](../../skills/pixellab-pip/references/blueprint.md), [cost approval](../../skills/pixellab-pip/references/auto.md), and [local assembly](../../skills/pixellab-pip/references/local-asset-assembly.md).
- Game Art's pinned [portable skill](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/SKILL.md), [task loop](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/prompt_improver.md), [style precedence and profiles](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/parameters.md), [terrain task](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-tiles.md), [normal-map task](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-normal.md), animation recipes and helper implementations.
- Both Game Art distributions, installer/model-task mappings, and its [MIT license](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/LICENSE).
- The [official MCP guide](https://api.pixellab.ai/mcp/docs) and [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json), retrieved on 2026-10-15 for normal-map input contracts and tileset chaining/metadata. These checks do not establish generated-art quality or the success of an engine import.

One reviewer challenged the additions. Two others directly debated personalization versus minimalism, exchanged rebuttals, and revised their positions. The parent challenged their conclusions again for duplication, hidden state, unnecessary artifacts, description enhancement, and imposed scheduling. The material disagreements and concessions appear below. Agreement is a design judgment, not experimental proof.

## Correcting The Starting Assumptions

**One skill does not mean one flat instruction file.** Game Art's portable distribution already uses one `SKILL.md` with task references and optional host-specific dispatch. Its Claude distribution exposes separate `pga-*` task skills. Multiple visible skills are a distribution choice, not a requirement for personalized workflows. Pip can retain one discoverable skill and load only relevant references.

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

## Which New Additions Are Worth Adapting Now?

All decisions below concern the v1.4.0 delta. Pip's earlier motion-aware padding rule and optional image inspector are already shipped and are not proposed again.

| Addition | Case for adapting it | Challenge and agreed disposition |
|---|---|---|
| Normal-map input handling | Pip's image-role row says an animation must be a strip while also listing MCP GIF/reference support. This can steer MCP to the wrong representation. | **Recommend a correctness fix now:** make the row surface-specific. The existing SKILL router is already correct; no new reference or helper. |
| Shared terrain in a requested chain | Pip lists lower/upper base-ID fields but does not explain the concrete A → B, B → C linkage. | **Recommend one conditional action now:** reuse the returned shared-terrain ID in the next set's matching field and retain its stored description when available. Respect existing enhancement behavior. |
| Complete tileset review | A random/example map may omit diagonal cases; correct atlas packaging does not prove every transition is usable. | **Recommend targeted verification now:** inspect returned configurations and shared-terrain seams with actual metadata. No mandatory map, fixed 16-tile logic, new generation or automatic retry. |
| Normal-map packing, splitting and lighting helper | Convenient preparation and visual shading checks for actual engine workflows | **Do not import now.** Host tools cover preparation; the reviewed GIF path quantizes colors/alpha, and the preview assumes OpenGL. Extra validation/engine tooling needs a concrete task. |
| Terrain preview helper | Repeatable preview can expose seams before engine import | **Do not import now.** Reviewed code handles 16-tile square-corner sets, rejects cliffs, and has a single-sheet CLI guard problem. One narrow renderer cannot stand in for Pip's broader layout support. |
| Brightness/color matching | May remove unwanted drift across generated frames | **Reject automatic normalization; no helper now.** Mean brightness cannot distinguish drift from intentional lighting or effects, and the default overwrites files. Requested palette work already has supported routes. |
| Hit/kick recipes and pose-based normal segmentation | Concrete key poses and shorter segments may improve some actions | **No global recipe or automatic segmentation.** Existing anchors/chains cover the mechanism. Fixed models, frame counts, timing, cleanup and extra paid calls lack general validation. |
| Expanded palette notes and beginner examples | Better explanations and examples can improve discoverability | Palette routing is **already covered** in Pip. Upstream examples do not establish a new Pip capability or justify another runtime contract. |

The two proposed canonical edits are bounded as follows:

1. **Image-role row:** MCP uses documented image/animation references or PNG/GIF input; REST uses a PNG sprite (default `frames=1`) or equal-frame horizontal PNG strip with explicit `frames`. Do not invent an MCP `frames` field or require GIF conversion when an animation reference already exists. Keep provider-supported facts separate from upstream's observations about a PNG strip being treated as one image.
2. **Existing tileset reference:** clarify requested-chain base-ID reuse and review all returned configurations. Do not blindly repeat original text when `enhance` has stored rewritten terrain descriptions. Do not add a wait-until-complete scheduling rule: the official MCP chaining example permits immediate use of returned base IDs. Keep actual returned atlas order and layout.

A broader normal-map verification proposal was considered and removed from the immediate scope. The row already describes dimensions and binary alpha, while new mandatory lighting previews would add dependencies or deliverables. Exact equality with source alpha would also be wrong for partially transparent source pixels when the normal-map output uses binary alpha.

## Merge Options Challenged

| Approach | Benefit | Cost or conflict | Recommendation |
|---|---|---|---|
| Vendor both codebases and adopt all workflows | Fastest access to the full helper/profile suite | Conflicting execution policies, duplicate contracts, dependency and update ownership, mixed state and attribution obligations | Reject now |
| Mechanically repackage commands under one skill, in the main file or task references | One visible entry point and familiar task names | Packaging alone leaves conflicting behavior and duplicate routing; a flat main file additionally increases loaded instructions | Reject a packaging-only merge |
| Keep separate companion skills | Each workflow keeps its identity and defaults | Two entry points/configurations and potential trigger conflicts; fails this project's one-skill direction | Not the recommended Pip architecture |
| Jointly maintained neutral skill with optional, user-requested workflows | Combines maintainer expertise and can preserve personalized production depth behind one entry point | Shared defaults and responsibility need agreement; each imported reference, helper or state mechanism still needs justification | Recommended convergence target if jointly chosen; no new feature/state build implied |
| Keep the architecture; selectively adapt useful decisions | Small changes, existing canonical homes, no new state or dependency framework | Leaves automatic style selection and the turnkey helper suite unavailable | **Recommended now** |

The immediate recommendation is selective integration within the existing architecture. Joint authorship and one eventual product do not require importing every behavior. No style profile schema, automatic project discovery, second log, installer merger, workflow graph or second execution framework is proposed now.

## A Practical Path To One Shared Skill

There is no demonstrated technical incompatibility that prevents one combined skill. Both products are chiefly instructions plus Python helpers. The difficult part is choosing one consistent behavior when their current instructions disagree; combining files alone leaves the agent with conflicting directions.

The product identity can accommodate both strengths: one neutral entry point for any PixelLab request, with user-selected project direction and requested production workflows loaded only when relevant. A one-off icon request should remain usable without setting up a project profile. An ongoing project may deliberately reuse approved direction without imposing its aesthetic on unrelated requests. This is a proposed product boundary, not a new profile system or implemented automatic continuity.

Practical next steps:

1. **Start with a joint-reviewed contribution.** Use the two bounded reference edits above as a small pilot under Pip's existing contract. This tests review, canonical placement and shared ownership without importing helpers or waiting for a rebrand.
2. **Map behavior before combining it.** In this spike, identify one canonical home for overlapping rules and record what is retained, adapted or excluded. Agree one behavior for spending/retries, original preservation, public fields, privacy and user-selected defaults. Small contributions need only resolve the policies they touch; a merged release needs a coherent overall contract.
3. **Choose a concrete shared workflow.** Walk through a real user request together using current Pip, explicitly selected project direction and existing blueprints. Add only the missing actions that improve that request. Do not build a generic style manager or a new workflow format to make the partnership look complete.
4. **Settle identity and release responsibilities before combined distribution.** Agree the product name, contributor credit, repository/release ownership, public documentation and what existing users should expect. There is no evidence yet that either maintainer has accepted a particular name or migration policy.
5. **Migrate only what the adopted design requires.** If commands, config, styles, outputs or installation paths change, define their treatment and test representative existing projects in an isolated checkout. Do not overwrite user profiles or artifacts, promise compatibility without tests, or build migration machinery for unchanged formats. Ship the shared product only after the selected workflows and supported hosts have been checked.

This allows cooperation immediately while keeping unproven feature imports out of the runtime. It also leaves a real decision for maintainers: whether the shared identity promises a neutral PixelLab tool for everyone with optional project continuity, or a prescriptive production system. Those identities can coexist only when the production choices are deliberately selected and their authority is explicit.

## Conflicts A Real Merge Would Have To Resolve

| Area | Material difference | Required disposition for any future Pip integration |
|---|---|---|
| Aesthetic and model defaults | Game Art supplies genre, density, facing, size, seed and recipe defaults; Pip follows the request and selected route | User-chosen direction may guide art; absence of direction must not activate a house aesthetic or fixed recipe |
| Paid work and retries | Game Art's loop avoids permission prompts and allows defect retries; Pip has explicit whole-chain and extra-spend rules | Pip's approval/budget contract governs every adapted chain; a style preference is not spending authority |
| Final pixels and playback | Game Art normalizes colors, cleans flashes and selects/drops/mirrors frames in finishing | Preserve raw outputs; requested/approved transformations remain explicit and labeled; no silent repairs |
| Schema authority | Upstream includes both house-observation precedence and live-schema precedence language | Current public tool/endpoint schema determines fields; measured anecdotes do not override validation |
| Credentials and surfaces | Game Art executes through MCP; Pip also supports public REST and editor/website boundaries | Preserve Pip's secret handling and public/private endpoint distinction; never import credential values |
| Reporting and external sharing | Game Art has project logs and opt-in author feedback; Pip has manifests and blueprints | Reuse Pip records and actual exposed usage; do not add a second log or an external-sharing channel as a merge side effect |
| State and task authority | Active styles and project profiles can affect many future calls | No hidden scope expansion. Art notes cannot grant permission for paid, destructive, external or local pixel-changing actions |
| Packaging and maintenance | Host task wrappers, optional model dispatch, helper dependencies and updater behavior differ | Retain one portable skill and on-demand resources; own tests, compatibility and updates for anything actually adopted |

The upstream license is MIT. If future work copies source or substantial portions, preserve its copyright and permission notice; this spike copies no helper code. Record an upstream revision and provenance for any adopted material. Skill-source licensing does not establish rights for generated or supplied art.

## Debate Record And Agreed Concessions

The table summarizes arguments actually exchanged, not hypothetical reviewers. Detailed working notes and challenge excerpts are retained privately for the Claude handoff.

| Challenge | Initial tension | Result after rebuttal |
|---|---|---|
| Does existing replay remove the need for project continuity? | Both distinguished named styles from replay at the outset; minimalism challenged whether the continuity example needs a new runtime contract | Explicit project notes can serve the reviewed workflow. Automatic reuse of a selected active style remains a genuine convenience gap, without establishing a current need for a manager. |
| Does neutrality prohibit project direction? | Compatibility with user-selected direction was a shared premise; the debate tested where preferences would become imposed defaults | Both retained user-led personalization. Its usefulness alone does not justify new state, discovery or a profile schema. |
| Are optional recipes inherently out of scope? | Minimalism resisted fixed combat defaults; personalization defended requested recipes | Both accept a tested requested chain could fit one skill. Pip already has the mechanism, so no fixed hit/kick recipe is needed now. |
| Is terrain review too specialized? | A renderer import looked narrow; personalization emphasized the frequency of terrain continuity | General usefulness is judged within a supported intent. All-configuration review is useful for tilesets; a fixed-layout renderer still needs evidence. |
| Is listing chaining fields enough? | Parent initially treated chaining as already covered | Addition reviewer showed that field names omit upper-to-lower shared-terrain reuse. Parent and both merge reviewers accepted a conditional clarification. |
| Which terrain description should be reused? | Copying Game Art's exact original-text advice conflicted with Pip's enhancement semantics | Reuse the shared base ID and stored description when available; no blind original-text override and no new scheduling mandate. |
| Should normal-map lighting checks be added too? | Addition reviewer initially proposed structural/lighting checks alongside transport correction | Parent challenged duplication, binary alpha and unwanted previews. Reviewer narrowed the immediate recommendation to input correctness. |
| Does a merge need new state now? | Personalization supplied the strongest case for automatic continuity | It reduces retrieval/selection effort but no reviewed task establishes sufficient current friction to justify a new runtime contract. Both rejected state/profile work now. |

Original review consensus: no immediate architectural/codebase union, new helper or profile system; propose the two bounded canonical edits above. After considering voluntary joint maintenance, both reviewers supported phased convergence and clarified that shared authorship is compatible with this limited initial scope. The unresolved question is whether richer packaged workflows improve quality or total effort for Pip's varied users. Published examples and agreement among reviewers cannot answer it.

## Validation And Decision Gates

No provider generation, installer run, upstream helper execution, engine import, telemetry submission or runtime implementation was performed. Repository QA validates the research artifact and existing code; it is not a live test of the proposed behavior.

For the proposed normal-map correction, review dry scenarios for one sprite, MCP GIF, MCP managed animation reference and REST strip plus frame count. Preserve the route, supported representation and convention; do not add conversion, segmentation or paid calls without need. The evidence is the current provider schema, not a test that searches for particular prose.

For the proposed tileset clarification, review A → B → C linkage, stored enhanced descriptions, existing base IDs, 16-tile diagonals, 25-tile cliff metadata, and hex/sidescroller layouts. Confirm no extra A → C set, mandatory preview output, sorting/repacking rule, wait policy or automatic retry is introduced. Run `python dev-tools/qa.py` after actual implementation.

Any future project-continuity feature must first demonstrate repeated failure or cumbersome manual selection using explicit notes and references. Any future recipe must solve a repeated request better than existing references/blueprints without imposing its aesthetic or cost policy. Any helper must solve demonstrated host-tool friction and pass fixtures for every layout, image representation and transformation it claims to support. If a claim needs paid quality or engine-import testing, define that experiment and cost before treating it as proven.

Claude's next review should challenge this consensus from the source evidence, including whether even the proposed sentences add enough value, whether general-use scope has been mistaken for "every task uses it," and whether an alternative preserves project convenience with less machinery. No implementation is implied by the recommendation.
