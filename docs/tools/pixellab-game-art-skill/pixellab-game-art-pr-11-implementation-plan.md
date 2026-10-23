# PR #11 remediation plan and acceptance record

Baseline: `feat/pga-merge`, `e5313285523216ce8faa06cf241cc8bed8cce32e`. This plan implements the [29-finding review](pixellab-game-art-pr-11-review.md). Implementation starts only after independent plan challenges have been reconciled here.

## Intended product

One portable Pip core remains the router and source of authority. Preserve Game Art's user-selected project continuity, useful motion expertise, optional key-pose production, animation diagnostics/accepted repairs, deterministic assembly/exports, and history over the existing private manifest. Avoid a second permission model, log, installer, task-skill system or generic processing framework.

The new Claude Studio panel is not required for any source production capability and has multiple policy/project-state defects. Remove this optional edition, its marketplace entry and edition-only tests from this PR. Ordinary Claude users continue using the same core as every other host. Preserve historical demo evidence but label its removed prototype UI accurately. This resolves panel-specific findings by removing the unsafe surface rather than building a new UI framework.

Keep useful local finishers as explicit tools, including specialist fallbacks when genuinely requested; never run them merely because Auto is on. Prefer documented PixelLab workbench/editor operations for new visual content. No paid quality experiment or remote destructive action is authorized by this remediation task.

## Canonical boundaries

- `SKILL.md`: global provenance/authority/output rules, ordinary project discovery, route selection, inspection versus repair. Add only the missing decisions; preserve existing guarded MCP/REST/editor behavior.
- `references/auto.md`: one existing boolean Auto cost gate, whole-chain approval, explicit per-plan budget/retry constraints and resume authority. Remove `level` and redundant enum/global policy state; no migration alias for an unreleased prototype. Approval of spending does not approve art changes or delegate content review.
- `references/project-style.md`: selected-root, effective-style/temporary selection/opt-out/approved saves, anchors, legacy limits and migration trigger. `project_style.py` is a small deterministic resolver/writer, not an execution authority.
- `references/usage-reporting.md` and existing manifest: exact usage versus reservations, IDs/requests/outputs/outcomes/time, recorded approved run scope. A manifest describes prior authority; possession alone never grants new authority.
- Existing specific references: optional recipes, helper invocation, mode/layout limitations; point to globals instead of redefining them. Keep historical observations in existing evidence docs.

## Finding-by-finding implementation and proof

| Finding | Implementation | Required acceptance evidence |
|---|---|---|
| R01 Auto grants art authority | Restore cost-only Auto; require requested/accepted operations for local pixel/playback changes. | Dry cases Auto + preserve frames/no local repaint; no permission table authorizing pixels. |
| R02 Studio changes global policy | Remove Studio edition and its marketplace entry. | No edition hooks/defaults; normal core remains installable. |
| R03 Unsafe budget/usage states | Validate manifest shape and numeric units; separate pending `estimated_usage` from exact `reported_usage`; unknown totals fail closed; failure is not refund; downloader never infers billing. | Unknown/null/zero/negative/NaN/invalid shape/failure/refund fixtures; estimated values never reported as charges. |
| R04 Concurrent ledger loss | Lock entire read-modify-write with a small portable stdlib lock; bounded wait and clear stale-lock recovery, no silent theft. Preserve unrelated values. | Concurrent processes and completion/outcome updates retain both jobs and totals. |
| R05 Fetch overwrite/stale/corrupt files | Validate decoded payload with optional Pillow; skip before HTTP/writes if unavailable. Use exclusively created destinations and complete preflight; reject stale/existing conflicts; record only downloaded paths. Fetch the exact getter-confirmed/expected count; an indexed 404 never proves a shorter completed clip. | Valid PNG/GIF, HTML/truncation, existing outputs, incomplete clips, redirects, timeout/error and no destructive refetch. |
| R06 Doctor source overwrite | Include containers/ref paths in protected set and preflight report/frame/preview destinations before writing. | Sheet/GIF/ref/alias/name-collision fixtures preserve all source bytes. |
| R07 Hurt reorder | Remove automatic house reorder; timing changes require explicit accepted proposal. | Every timing branch with empty acceptance preserves order; existing misleading test corrected. |
| R08 Wrong panel project | Remove Studio. | No panel submissions. Core selected root/path tests cover A/B isolation. |
| R09 Upstream notice | Include complete upstream MIT notice and source revision within the shipped skill and root licensing/provenance. | ZIP/raw-skill packaging fixture contains both notices; no private paths/data. |
| R10 Unsafe existing migration | Document read-only detection and previewed approved cleanup of known old skills/project/task-agent text; preserve edits, never auto-delete. Preview/pin previously implicit house appearance and resolve legacy caps before paid work; do not promise exact visual equivalence. | Representative synthetic old instruction/profile fixtures, appearance review, ambiguous caps stop spending; no automatic cleanup. |
| R11 Missing style discovery | One global check for selected project-root `pixellab.json` before already-routed generation. | Fresh-session plain icon task loads icon anchor; missing profile does not force setup. |
| R12 Style semantics | Resolve legacy appearance plus named style: recursively overlay known maps, lists/scalars/null replace; disclose difference from upstream shallow overlay during migration. Temporary selection/appearance opt-out never mutates state or bypasses caps. Validate malformed shapes without writes; deliberate save/replace/anchor updates and source-relative image validation; Python-unavailable read fallback. | Nested/legacy/unknown selection/opt-out/no-file/changed cwd/missing anchor/unrelated preservation/failed-write fixtures. |
| R13 Wrong anchor family | Canonical still remains per character; family anchor requires deliberate approval and correct family. | Monster first does not register heroes; one-job pick/override does not persist. |
| R14 Conflicting routes | Main router distinguishes ordinary managed characters, explicit stills and optional advanced production; references defer to that choice. Preserve existing cheap scene defaults. | Dry raw/managed/still/scene/reference cases, MCP/REST parity and existing benchmark scenarios. |
| R15 Scene excludes people | Conditional composition/exclusions; remove universal people/text/house negatives that contradict the request. | Party scene retains party; subjectless backdrop remains subjectless. |
| R16 Frame/pacing changes | Make drop/splice/holds/ping-pong/mirroring optional accepted derivatives; respect requested counts; no retroactive change to other moves. | Exact-count/order and eight-direction fixtures; recipes explicitly scope transformations. |
| R17 Review contradiction | Keep one explicit content checkpoint/delegation rule independent of Auto. | Auto without delegated review pauses; an explicit accepted delegation has a defined scope. |
| R18 Normal-map requirements | Correct canonical inputs to supported MCP reference/GIF/strip and REST strip+count; mode-specific evidence, optional conversion/segmentation/lighting only when needed. | Dry representation/mode cases; DirectX/size/split tests; no added paid test. |
| R19 Invalid/wrong reroll | Schema-valid minimum four generated v3 frames with area/even bounds; costs labeled estimates; exact output ownership, ambiguity unknown. | Two-frame proposals absent; multiple jobs in one folder map correctly; current schema before paid execution. |
| R20 Blank/remainder cells | Preserve every declared sheet cell; reject indivisible dimensions and invalid cell sizes. | Blank cells preserved in count/order; right/bottom remainder errors without writes. |
| R21 Soft alpha corruption | Source-over composite aligned/clipped overlays; no masked RGBA paste. | Partial-alpha effect over opaque/transparent bodies and clipped/rotated placements. |
| R22 Divergent GIF/matte | Extract one small faithful GIF writer/validator for standard previews and doctor reuse; retain task-specific showcase/lighting composition and disclose its transformation. | Decoded alpha/count/order/duration/repeated frames; doctor standard preview transparent. |
| R23 Panel state stale | Remove Studio; no independent permission cache/review identity. | Edition absence; core settings/state unchanged by project opening. |
| R24 Release version failure | Remove edition-only version locations/tests; test existing core release bump against actual manifests. | Extracted existing release bump and metadata checks succeed without stale entry. |
| R25 History/reroll claims | Add minimal timestamps and optional date/job/tool query over manifests; exact request/output data for reroll or use recorded blueprint. Unknown historical dates/costs disclosed, not guessed. | More than ten runs, date bounds, unknown dates/usage, outcome and ordinary single-call reroll dry case. |
| R26 Check means repair | Route inspect/check to `--check-only`; apply only under requested fix scope. Keep inspection observations faithful to source, label analysis preprocessing. | Read-only request produces reports without repaired frames; original bytes remain identical. |
| R27 Invented hit event | Emit `hit_frame` only with explicit valid `--hit`. | Idle/icon sheets omit it; explicit contact index validated. |
| R28 Blueprint reference/replay | Clarify only actual replay inherits recorded calls; visual source uses existing identified art, no inferred reference generation. | Icons-with-hero-blueprint differs from replay/red-cape override; absent outputs ask rather than spend. |
| R29 Forced expensive recipe | Advanced key-pose route only for requested choreography/anchors or known failure; finish/export only as required. | Simple attack retains normal animation route; explicit custom key poses load advanced recipe. |

## Work sequence and ownership

1. **Plan challenge, no runtime edits.** Three independent agents challenge safety/completeness, KISS/YAGNI/DRY and useful feature parity. They exchange objections and counterproposals. Parent records resolutions here before implementation.
2. **Parallel bounded implementation after plan acceptance.** Worker A owns `manifest.py`, `fetch.py`, `history.py` and their tests. Worker B owns doctor/fixlib, assembly/finishing/preview helpers and their tests. Worker C owns project style resolver/tests and specialty motion/character/scene/normal-map/recipe references and blueprints. Parent owns `SKILL.md`, Auto/bark, canonical usage/lifecycle/assembly/finishing/blueprint references, migration/user docs, licensing, packaging and cross-component integration. Shared contracts are agreed before overlapping changes; no worker reverts another's work.
3. **Integration.** Resolve helper interfaces, run existing full QA with optional dependencies available; add focused regression cases from reproductions. Validate packaging and actual next-version bump. Compare all changed PR paths to the original merge base, not merely the remediation diff.
4. **Independent whole-PR challenge.** Reassign reviewers so each audits another's code, plus global contract/source parity. Reviewers send concrete findings, debate disputed conclusions with each other and the parent, and require evidence for closure. No rubber-stamp consensus.
5. **Repeat fixes and affected checks.** Address every accepted material finding and re-review its impact. Run full QA after integrated edits. Final status explicitly records all R01–R29, newly found issues, reviewer dispositions and any empirical limits. Commit and push ordinary changes to the existing merge branch only after checks pass; do not merge the PR or spend credits.

## Minimality and evidence gates

- Preserve safety checks and useful tests. New tests target demonstrated boundaries, not exact prose or every reversible documentation edit.
- No broad rewrite, workflow graph, database, new package manager, general migration engine, new telemetry, second logger or replacement host UI.
- Reuse existing references, helpers, QA, benchmark and release process. Do not copy policy into every recipe. Keep specialty content in its existing reference and source observations in evidence docs.
- Optional Python/image dependencies skip clearly; guidance and ordinary routing remain usable without them. A helper's success is not visual approval.
- No unverified provider limits promoted to facts. Read current primary tool schema/docs only for claims changed by implementation; do not invoke paid tools.
- Merge readiness means no unresolved material findings within implemented scope and passed applicable checks. It does not fabricate live visual-quality, engine-import or host-session evidence. Unperformed empirical checks must be disclosed and corresponding broad claims narrowed.

## Plan challenge resolutions

- All three reviewers reject global budget/retry state and a second permission enum. Keep explicitly scoped run constraints and one boolean Auto.
- A manifest lock protects ledger mutation, not an atomic provider submission or shared cap across independent agents. One agent admits calls serially: check all plan runs plus the next conservative estimate, submit, immediately record returned ID before admitting another. On interruption, recover the tool result/getter; uncertain submission blocks resubmission. Unknown accounting blocks budget comparison. Do not claim crash-proof/cross-agent hard caps or construct a submission database.
- Failure does not mean refund. Retain reservation until actual charge/refund evidence resolves it; estimates never become reported usage merely because a download succeeds.
- Fetch requires known count and usable decoder before network/write. Existing destinations are refused rather than maintaining an idempotence cache or guessing short clips.
- Additional defect discovered during challenge: `--accept cN` is unsafe across a batch because IDs restart per animation. Restrict accepted proposals to one animation; unchanged source/proposal identity must be reviewed. Preflight aliases and duplicate generated filenames as well as input/output collisions.
- Extend collision protection to every imported writer, including sheet packing, padding, contact sheets and normal-map/showcase outputs; reuse one small destination preflight, not a framework. Separate analysis-only background keying from original pixels so an unchanged container frame is not silently keyed on export. Numeric costs/caps reject booleans and non-finite/negative values; zero remains meaningful.
- Useful source onboarding and mixed batch-input decisions must remain accessible in existing style/approval guidance and router, with optional setup and complete group review; no new command or batch engine.
- Choose and test explicit recursive known-map style overlay, preserving per-family values. Migration previews its difference from upstream shallow replacement and unstored house defaults; opt-out affects appearance only, not restrictive caps.
- Move sword/katana/pistol/kick specifics into existing specialty references and example values into the existing style-example reference. Shared GIF work is only encoding/validation, not a general media framework.
- Keep engine wiring claims conservative unless independently tested. Execute available representative dry host traces and record their results/limits rather than equating unit tests with live cross-host quality.

## Review record

Three independent reviewers (safety, minimality and source parity) discussed and accepted the amended plan before runtime implementation. Their additional writer/acceptance defects are included above. Final implementation results and independent whole-PR review dispositions are recorded below.

## Implemented resolution of all 29 findings

This section records completed behavior, distinct from the original acceptance plan above. Source task access is also summarized in [the merge guide](../../merge/README.md); migration decisions are explained in [the migration walkthroughs](../../merge/migration.md). The original review remains a pinned historical record, not the verdict on the revised head.

| Finding | Final disposition and evidence |
|---|---|
| R01 | Cost-only Auto restored; explicit art/playback scope retained. Codex dry trace preserved every returned frame/pixel and required acceptance of a replacement. |
| R02 | Studio hooks, panel, marketplace entry and edition-only tests removed. Opening a project has no separate policy-writing surface. |
| R03 | Invalid/unknown/non-finite usage fails closed; actual zero remains valid; estimates and actual charges remain distinct across failures. Manifest and fetch behavioral fixtures pass. |
| R04 | Complete ledger mutations use bounded exclusive locking and atomic replacement; concurrent IDs, charges and outcomes survive. The Windows contention defect found in full QA is included in the final regression gate below. |
| R05 | Exact expected image count, full decoding, bounded waits, fresh exclusive writes and exact recorded paths. Corrupt/truncated/HTML/redirect/stale/incomplete fixtures pass; missing decoder skips before HTTP/writes. |
| R06 | All containers, references, frame paths and generated destinations are preflighted; aliases/duplicates are refused. Doctor and shared assembly source-integrity regressions pass. |
| R07 | House hurt reorder removed; unaccepted timing preserves order. Accepted replacement geometry is checked and source background metadata follows the selected frame. |
| R08 | Studio project binding defect removed with that surface. Core style/helper selected-root isolation remains covered by changed-cwd and explicit-profile fixtures. |
| R09 | One complete shipped MIT notice includes both copyrights and pinned upstream provenance. Raw-skill ZIP and existing release-bump fixtures pass. |
| R10 | Runtime setup includes read-only migration detection, previewed approved cleanup, user-edit preservation, appearance drift and cap reconciliation. Synthetic resolver walkthroughs retain zero caps and nested anchors without writes; copied-instruction and pending-job decisions were manually challenged. No installed-user configuration was deleted. |
| R11 | Ordinary already-routed generation checks only the selected root for the profile; absent profile requires no setup. Dry icon/style plans and resolver fixtures cover discovery/selection decisions, not a paid fresh-session workflow. |
| R12 | Validated recursive appearance overlay, temporary named selection/opt-out, deliberate saves/replacement, source-relative references and Python-free read fallback. Twenty style tests cover state, failure preservation and unavailable/outdated decoder handling. |
| R13 | Canonical character still and per-family anchors are separate; registering/replacing a family anchor is deliberate. Wrong-family substitution and implicit persistent picks are prohibited. |
| R14 | Managed, raw, explicit still and optional advanced recipes retain separate routes. Hardcoded route upgrades were removed from character/scene/icon advice; dry simple attack stays on raw animation. |
| R15 | Composition preserves requested people/subjects. Clean plates and separate buildings require an actual requested output need; a city panorama stays one scene. |
| R16 | Counts/order are preserved; holds, drops, splices, mirrors and timing changes require accepted derivative scope. Sheet/doctor/finishing regressions cover counts, blank cells, timing and source metadata. |
| R17 | Review delegation is independent of Auto and scoped to exact current outputs. Candidate/pose blueprints honor the canonical delegation/checkpoint rule. |
| R18 | Supported normal-map representations/modes are explicit; GIF conversion, segmentation and lighting are optional. Conversion/split/dimension/DirectX checks pass; lighting is a labeled derived inspection aid. |
| R19 | Rerolls use schema-check-required estimates, minimum/even/pixel-budget controls and unique exact output ownership. Whole-clip shortcuts require exact raw-v3 labels and exclude protected keys/effects. Negative PixMiniMax and ambiguous-ownership fixtures pass. |
| R20 | Every declared sheet cell, including blank cells, is preserved; indivisible dimensions/invalid sizes are refused before writes. |
| R21 | Soft-alpha overlays use clipped source-over composition; opaque and translucent body/effect regressions pass. |
| R22 | Standard, doctor, normal-map and showcase GIF encoding uses one verified primitive. Repeated opaque frames, alpha, encoded colors and timing are decoded and checked. Quantization/alpha thresholding/timing rounding and task-specific composition are disclosed. |
| R23 | Independent panel permission/cache/review state removed; no replacement state framework. |
| R24 | Release metadata contains only the existing shipped core; the actual release bump script is exercised on copied manifests and updates every version consistently. |
| R25 | One manifest supports recorded UTC date, exact job and tool-text filters and outcomes; filtering precedes run limits. Unknown old dates/charges remain unknown. Same-job downloads preserve all saved output paths and cannot downgrade an observed status to submitted. |
| R26 | Inspection routes to reports-only check mode. Doctor uses explicit selected profile, preserves original pixels separately from analysis keying, and points inspection reports to existing source files. |
| R27 | Unrequested hit events are omitted; explicit hit indices are validated by sheet tests. |
| R28 | Reference-only blueprints reuse identifiable existing art and route the new requested asset normally. Missing reference art does not authorize replay; dry icon/reference case follows this distinction. |
| R29 | Simple animation needs no paid edited key stages, finishing chain or engine export. The retained advanced route is selected for requested choreography/anchors or accepted recovery, with specialty guidance loaded only as needed. |

## Adversarial implementation review and reconciliation

Three independent reviewers collectively covered the complete merge-base-to-working-tree PR with cross-assigned code and shared-contract reviews, not just remediation changes. They exchanged findings with each other and the parent, challenged proposed fixes and reread affected code/contracts. This followed the three-reviewer plan challenge before implementation.

Additional issues found and corrected during implementation/review included:

- Local saved references were not validated/rebased; an empty rename could corrupt a profile; unused stale family anchors blocked unrelated work; unknown named-style metadata entered appearance. Resolver fixes preserve unrelated data and return per-family diagnostics.
- Doctor accepted frame substitution could crop across different geometries or restore the wrong keyed background. Geometry is rejected conservatively and selected-source metadata follows accepted substitutions; analysis preprocessing never replaces unchanged source pixels.
- Opaque repeated GIF frames were coalesced despite palette changes. The shared encoder now emits each full frame explicitly and verifies its decoded output.
- Doctor profile discovery used ambient cwd, check-only reports pointed to an absent inspection sheet, and a duplicated defect table drifted. Explicit profile selection, mode-aware report instructions and one `--table` source replace those paths.
- Scene/icon advice forced optional routes or extra paid deliverables; wrong-hand guidance silently relaxed the brief; blueprint checkpoints ignored delegated review. All now follow the selected route, current request and canonical authority.
- The whole-clip retry substring matched PixMiniMax; late filtering swept approved keys/excluded effects into rerolls. Exact labels, pre-plan protected-index filtering and conservative shortcut suppression fix both.
- Refetches lost saved path provenance and could race completed status. Both merge inside the existing transaction; no second log or state database was added.
- Dangling destination symlinks bypassed existence checks. Shared preflight rejects lexical symlinks; its unused overwrite escape hatch was removed.
- Raw-skill packaging omitted Pip's own copyright; ZIP assertions now cover both notices. VFX ZIP/JSON downloads no longer use the decoded-image-only helper.
- Documentation distinguished actual reused-source composition from procedural painting, and estimates from historical charges. Preview looping and GIF approximation are disclosed instead of promising unsupported playback/fidelity.
- A dry simple-animation trace confused generated and returned counts. A direct pointer to canonical input-echo verification was added; the follow-up trace correctly distinguished generated frames from the echoed input.

Reviewers rejected unnecessary machinery: a new approval enum/global budget, migration engine, distributed submission database, generic processing graph, extra playback/timing flags and a second host UI. Existing references, manifests, helpers, release tooling and benchmark were reused.

All 22 supplied-source task families were reconciled. Optional onboarding, mixed batches, named styles/anchors, analysis, production recipes, all motion specialties, diagnostics/accepted repairs, history/reroll and exports remain available through normal Pip tasks. Telemetry/author sharing, automatic model dispatch, duplicate installers/updaters and the host-specific prototype UI are intentionally excluded. The 13 finishers have distinct requested operations; their availability grants no permission to run them or create local art. No helper is required merely because Auto is enabled.

## Acceptance evidence and limits

- Integrated `python dev-tools/qa.py` on Python 3.14 with Pillow 12.3.0, numpy 2.4.0 and scipy 1.17.1: **299 tests passed, no skips; all repository checks passed**. This includes the actual release bump/raw-skill ZIP fixtures and source alias protections. The earlier 297-test run exposed Windows exclusive-create `PermissionError`; the fix retries only within the existing deadline, never steals a lock, and fails closed. Transient/persistent denial fixtures and twenty additional eight-process stress rounds across two reviewers passed.
- Local `claude plugin validate .` passed with the expected warning that root contributor `CLAUDE.md` is not plugin context; the shipped context is the portable skill. No removed edition is advertised or validated as shipped.
- Independent focused evidence includes style (19), packaging (2), manifest (21), fetch (16), doctor/rules (110), assembly (15) and finishing (25) tests. These are component checks, not additive totals or provider quality measurements.
- Read-only Codex planning compared four current cases with main: inspect without repair, simple attack, Auto without art/playback authority, and blueprint reference without replay. Manual response review confirmed the intended authority/routing decisions; the simple-count mistake triggered the corrective pointer/recheck above. Regex scores were not treated as semantic proof: one valid acceptance response missed the approval-word regex, and baseline inspection correctly chose its available workbench rather than the new doctor. Three additional positive traces selected animation diagnosis, custom reviewed poses/interpolation and saved-style icons. The key-pose scoring check was corrected to accept the supported REST interpolation route as well as MCP. No performance/routing percentage claim is derived from this tiny nondeterministic sample.
- Fresh Claude runs were attempted but could not authenticate because the local OAuth session had expired. A proposed DeepSeek comparison was rejected by automatic approval review because it would send repository content to an unverified external provider; it was not executed. This limits current cross-host empirical evidence, not the portable core's documented interface.
- No paid PixelLab generation, live art-quality experiment, private 818-animation calibration corpus, actual engine import, or real legacy-installer cleanup was validated. Historical demos are labeled as such; none is claimed as proof of the revised head.

All three independent reviewers accepted the reconciled fixes after code/contract rereads and focused checks; the 299-test combined QA gate passed. The release-gate discoveries below reopened readiness and were subsequently addressed; the updated local result supersedes this earlier dependency baseline. Readiness is bounded by these explicit results and limits. No review can prove the absence of every future defect; the acceptance criterion is implemented useful parity, no unresolved material finding within the reviewed scope, and passing applicable verification.


## Release-gate discoveries after the first push

Pushing the remediation exposed two additional concrete issues, so the earlier readiness disposition was reopened instead of treating local QA as sufficient.

1. **Known-vulnerable inherited image dependency.** GitHub reported nine open Dependabot alerts for `requirements-dev.txt`'s Pillow 12.3 pin, including a reported critical decoder alert. The [Pillow 13 release notes](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html) and [JPEG advisory](https://github.com/python-pillow/Pillow/security/advisories/GHSA-8g5g-8vmr-9782) identify 13.0.0 as patched. The advisory's specific exploit preconditions were not demonstrated in these helpers; vulnerable dependency presence is sufficient reason to stop recommending that version. Upgrade the development pin to 13.0.0 and use one shared stable-version loader before image decoding, including existing inspection/background removal and optional style-image validation. Missing/outdated/uncertain versions skip or remain explicitly unverified without decoding, writing, network fetch or package installation. JSON-only profile reads remain usable. Pillow 13 drops Python 3.10: distinguish standard-library helpers (3.10+) from optional image helpers/development dependencies (3.11+), with CI on 3.14. Two reviewers independently challenged the guard's necessity and implementation; a pin-only fix was rejected because copied raw skills use the user's existing packages.
2. **Undeclared downloader capability.** SkillSpector identified `fetch.py` networking without a matching declaration. Add `network` to the existing permissions list and describe its documented PixelLab download/file-host scope. This accurately declares current behavior; it does not expand accepted URLs or grant new execution authority. Preserve URL validation, redirect checks, auth boundaries and the security threshold.

The first pushed head passed Linux Repository QA and HOL Plugin Scanner, while SkillSpector failed; these results are not represented as final-head CI success. Pillow 13 compatibility fixtures cover decoded repeated frames/quantization/alpha/delays, normal-map conversion, showcase composition, soft-alpha effects and corrupt/full-count downloads. The runtime guard has separate old/prerelease/unknown-version and no-decode/no-write regressions. The final integrated rerun and final-head CI results supersede the earlier 299-test dependency baseline.


Independent scanner triage distinguished the real LP1 declaration error from expected matches: E1 identifies the documented PixelLab URLs in connection metadata/download code; MP2 matches ordinary Python alignment spaces (46–56 spaces), not instructions to fill context; EA3 matches `NOT LIMITED TO` in the complete MIT license. The pinned scanner's [capability rules](https://github.com/NVIDIA/skillspector/tree/dde36f258729b5aec7c835295a9556e64a2def0c) were inspected and the exact matches reproduced. Do not rewrite legal notices, hide supported URLs, suppress rules or lower the threshold to get green CI. The actual final scan, not an estimated score or count of newly opened GitHub alerts, is the acceptance gate.


Updated integrated gate: `python dev-tools/qa.py` passed **303 tests, no skips, all repository checks**, using Python 3.14, Pillow 13.0.0, numpy 2.4.0 and scipy 1.17.1. The new missing-numpy fixture preserves the configured patched Pillow path so it actually tests missing numpy rather than accidentally selecting an old global decoder. Both security implementers independently reviewed one another's changes; the scanner reviewer accepted the real declaration fix and retained expected findings. No unresolved material implementation finding remains in their reviewed scopes.

The branch addresses the reported affected Pillow ranges; GitHub's default-branch Dependabot state updates when that change lands there. Final published CI results are the checks attached to [PR #11](https://github.com/Shilo/pixellab-pip/pull/11); require the exact reviewed head's Repository QA, Skill Security Audit and HOL Plugin Scanner gates before merging. Passing local tests or estimated scanner scores never substitute for those results.


The complete uploaded SARIF still failed after the LP1 fix: it contained 33 results, including inherited accepted sound/credential/token-safety findings absent from the new-open-alert list. Reviewers explicitly rejected using that partial list to predict a pass. They accepted three ordinary formatting fixes for excessive alignment whitespace; additionally, the doctor CLI help still described measuring against “game ready,” so it was corrected to heuristic inspection, optional repair copies and advisory rerolls. Executable AST equality was checked for all three helpers (excluding the deliberately corrected module help text). Endpoint URLs, MIT wording, credential safeguards and scanner configuration/threshold are unchanged. The actual rerun remains the deciding gate.
