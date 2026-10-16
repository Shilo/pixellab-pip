# PixelLab Game Art And Pip: Merge Research Spike

Reviewed: 2026-10-15. Status: research and recommendation only; no runtime changes implemented.

Pip baseline: v2.2.0, commit `43da5765a44e1fba955592999cb10867ca990138`. Game Art baseline: v1.4.0, commit `92614b51bf99638899521cdf4fb74435ba8a47db`, verified against its remote default-branch HEAD for this review. See the [current feature comparison](pixellab-game-art-vs-pip-skill.md) for the complete inventory and helper limitations.

## Recommendation

Support joint maintenance and phased convergence toward one general-purpose, agent-agnostic skill if both maintainers choose a shared product. Avoid an immediate mechanical union of the codebases, helper suite and runtime instructions. Start with selectively adapted, verified operational improvements in existing references; no new project-style state is needed for that first step.

This extends the original review to a collaboration scenario: shared fixes, complementary expertise, one maintained release and one source of documentation can benefit users. Those are potential benefits of joint development, not measured savings or an agreement already reached between maintainers. The earlier recommendation against a codebase merge concerned wholesale adoption under the then-reviewed scope; it was not a reason to keep competing projects or reject collaboration.

The corrected immediate proposal is deliberately small: shorten the normal-map row without excluding MCP strips, and distinguish a blueprint used only as a visual reference from a request to replay it. The earlier terrain-chain and extra tile-review proposals are withdrawn after checking connected MCP descriptions and existing Pip verification. These remain recommendations for later implementation, not features shipped by this spike.

Personalized project direction remains compatible with Pip: users can explicitly supply visual requirements and approved references today. Ordinary project notes can provide user-selected context, but Pip has no dedicated project-note selection mechanism; this is manual user/host work, not a shipped continuity feature. Existing blueprints already represent requested chains. Neither practice provides Game Art's automatic reuse of the user's selected active style and onboarding convenience; that usability gap remains real.

## Recommended Next Tasks (Not Implemented)

| Next task | Canonical home or review location | Completion check | Status |
|---|---|---|---|
| Shorten and correct normal-map input wording | Existing [image-role row](../../skills/pixellab-pip/references/image-input-roles.md#goal-router) | Remove the universal strip requirement; retain MCP animation reference/GIF/strip support and shared size/frame limits; keep the explicit strip count REST-only | Proposed; not implemented |
| Distinguish blueprint reference use from replay | Existing [SKILL intent router](../../skills/pixellab-pip/SKILL.md#intent-router) | Route a different asset normally when a blueprint is only its look/identity source; use identifiable existing output images, never replay to obtain them; scope the recorded-route column to actual replay | Proposed; not implemented; no observed misgeneration |
| Jointly review a small integration pilot and the shared product contract | This spike and the existing review process | Review the two edits under Pip's current contract; map overlapping rules/helpers to keep, adapt or defer; record unresolved default, personalization and release decisions | Proposed; no merger agreement assumed |

The [comparison spike](pixellab-game-art-vs-pip-skill.md#recommended-next-tasks-not-implemented) carries the same immediate tasks. The bounded edits and acceptance scenarios below define their scope. They may be contributed and reviewed before deciding a shared name or final repository structure; run `python dev-tools/qa.py` after implementation.

## Questions And Evidence

The review asks which v1.4.0 additions change an agent decision Pip currently gets wrong or omits, whether hosts can already perform the local work, and whether a combined product can preserve neutrality, broad applicability, and a single skill entry point.

Evidence reviewed:

- Pip's [canonical skill](../../skills/pixellab-pip/SKILL.md), [image roles](../../skills/pixellab-pip/references/image-input-roles.md), [tilesets](../../skills/pixellab-pip/references/tileset.md), [animation](../../skills/pixellab-pip/references/animation.md), [cinematics](../../skills/pixellab-pip/references/cinematic.md), [style references](../../skills/pixellab-pip/references/style-reference.md), [blueprints](../../skills/pixellab-pip/references/blueprint.md), [cost approval](../../skills/pixellab-pip/references/auto.md), and [local assembly](../../skills/pixellab-pip/references/local-asset-assembly.md).
- Game Art's pinned [portable skill](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/SKILL.md), [task loop](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/prompt_improver.md), [style precedence and profiles](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/parameters.md), [terrain task](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-tiles.md), [normal-map task](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/any-agent/pixellab-game-art/references/tasks/pga-normal.md), animation recipes and helper implementations.
- Both Game Art distributions, installer/model-task mappings, and its [MIT license](https://github.com/lexingel/pixellab-game-art/blob/92614b51bf99638899521cdf4fb74435ba8a47db/LICENSE).
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
| Keep separate companion skills | Each workflow keeps its identity and defaults | Two entry points/configurations and potential trigger conflicts; fails this project's one-skill direction | Not the recommended Pip architecture |
| Jointly maintained neutral skill with optional, user-requested workflows | Combines maintainer expertise and can preserve personalized production depth behind one entry point | Shared defaults and responsibility need agreement; each imported reference, helper or state mechanism still needs justification | Recommended convergence target if jointly chosen; no new feature/state build implied |
| Keep the architecture; selectively adapt useful decisions | Small changes, existing canonical homes, no new state or dependency framework | Leaves automatic style selection and the turnkey helper suite unavailable | **Recommended now** |

The immediate recommendation is selective integration within the existing architecture. Joint authorship and one eventual product do not require importing every behavior. No style profile schema, automatic project discovery, second log, installer merger, workflow graph or second execution framework is proposed now.

## A Practical Path To One Shared Skill

There is no demonstrated technical incompatibility that prevents one combined skill. Both products are chiefly instructions plus Python helpers. The difficult part is choosing one consistent behavior when their current instructions disagree; combining files alone leaves the agent with conflicting directions.

The product identity can accommodate both strengths: one neutral entry point for any PixelLab request, with user-selected project direction and requested production workflows loaded only when relevant. A one-off icon request should remain usable without setting up a project profile. An ongoing project may deliberately reuse approved direction without imposing its aesthetic on unrelated requests. This is a proposed product boundary, not a new profile system or implemented automatic continuity.

Practical next steps:

1. **Start with a joint-reviewed contribution.** Use the two bounded guidance changes above as a small pilot under Pip's existing contract. This tests review, canonical placement and shared ownership without importing helpers or waiting for a rebrand.
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
| Is terrain review too specialized? | A renderer import looked narrow; personalization emphasized terrain continuity | Review is useful within tileset intent, but the follow-up found existing all-tile assembly/grid checks and no distinct Pip gap. The proposed extra rule is withdrawn. |
| Is listing chaining fields enough? | The first review checked Pip's field names but missed the live tool's full recipe | The original acceptance is superseded: MCP already teaches the linkage, and REST visual equivalence is unproven. No tileset edit remains proposed. |
| Which terrain description and schedule should be reused? | The first debate narrowed text preservation but relied on the web example for timing | The whole chain addition is withdrawn. Connected MCP and the guide conflict on waiting; no new scheduling rule is justified by this research. |
| Should normal-map lighting checks be added too? | Addition reviewer initially proposed structural/lighting checks alongside transport correction | Parent challenged duplication, binary alpha and unwanted previews. Reviewer narrowed the immediate recommendation to input correctness. |
| Does a merge need new state now? | Personalization supplied the strongest case for automatic continuity | It reduces retrieval/selection effort but no reviewed task establishes sufficient current friction to justify a new runtime contract. Both rejected state/profile work now. |

Original review consensus rejected an immediate architectural/codebase union, new helper or profile system. Its normal-map format restriction and both tileset proposals were subsequently corrected or withdrawn after the independent review and live-tool checks; both original reviewers accepted the revised scope. The current proposals are the smaller normal-map correction and blueprint routing clarification. Both reviewers continue to support joint maintenance and phased convergence if maintainers choose that path. This correction is evidence against mechanical policy imports, not against cooperation.

## Validation And Decision Gates

No provider generation, installer run, upstream helper execution, engine import, telemetry submission or runtime implementation was performed. Repository QA validates the research artifact and existing code; it is not a live test of the proposed behavior.

For the proposed normal-map correction, review dry scenarios for one sprite, MCP GIF, MCP managed animation reference, MCP strip and REST strip plus frame count. Keep 8–512 px / 32-frame limits on both surfaces, preserve convention, invent no MCP `frames` argument and add no conversion or segmentation. This checks documented routing, not whether MCP correctly detects frame count for an arbitrary strip.

For blueprint routing, review: "shop icons in the style of hero.blueprint.json" uses the icon route and existing hero images as references; "remake hero.blueprint.json" replays; "hero.blueprint.json but with a red cape" remains replay with an override. Missing, ambiguous or template-only outputs must not cause reference-generating replay. No recorded route/size/seed/mode leaks into the different asset. These are semantic acceptance cases, not evidence that an agent has already misgenerated an asset. Make no tileset runtime changes. Run `python dev-tools/qa.py` after implementation.

Any future project-continuity feature must first demonstrate repeated failure or cumbersome manual selection using explicit notes and references. Any future recipe must solve a repeated request better than existing references/blueprints without imposing its aesthetic or cost policy. Any helper must solve demonstrated host-tool friction and pass fixtures for every layout, image representation and transformation it claims to support. If a claim needs paid quality or engine-import testing, define that experiment and cost before treating it as proven.

Remaining empirical questions are MCP strip frame-count detection, REST base IDs' visual effect, contradictory chain scheduling, actual blueprint-as-reference frequency, manual project-direction effort, and comparative recipe quality/cost. A scoped, separately approved experiment can investigate provider behavior; no paid test was run here. Agreement among agents cannot answer these questions. No implementation is implied by this corrected recommendation.
