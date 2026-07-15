# Handoff: Blueprint System Production Readiness

## Session Metadata

- Created: 2026-07-14
- Project: `pixellab-pip`
- Branch: `main`
- Starting commit: `d423ddf603badf4ca0d15a1624c1969f6e52374a`
- Primary plan: `docs/plans/blueprint-production-readiness-plan.md`
- Status: campaign complete; release decision pass, with all delegated runs, regressions, packaging refresh, and final verification complete

## Current State Summary

### Portability iteration 2 — active

The user challenged the first iteration's rejection of unknown variable modifiers and requested a
clear strict-writer/tolerant-reader split. Initial audit confirms that the contract incorrectly made
canonical writing grammar a runtime rejection rule. The active revision will keep generated and
bundled blueprints concise and canonical while allowing readers to interpret unfamiliar modifiers,
metadata, and step extensions semantically when their meaning is clear. Unknown syntax is not
authority: readers must still reject ambiguity, unsafe paths, secrets, private routes, fabricated
verification, or actions beyond the current user's permission.

The second iteration will also test a minimal optional `_blueprint` metadata object that makes public
PixelLab API/MCP locations and bearer-auth environment-variable naming discoverable without storing
a credential value. An independent design agent is challenging this shape before it is adopted.
Repository QA will remain strict for every known `MCP`, HTTP/API, `TASK`, variable, `default`, path,
and metadata field, but extension-open for additional keys and shapes. A new with-skill/no-skill
benchmark and targeted live replay will measure whether this improves portability without weakening
safety or exact request fidelity.

Iteration-2 implementation adopted `_pixellab` rather than generic `_blueprint`: it now records the
public API origin when relevant, structured PixelLab MCP name/URL when relevant, shared credential
environment-variable name, and an explicit-user-run paid-call policy. The independent
review rejected repeated absolute action URLs and schema wrappers as redundant. QA is extension-open
but validates known metadata and rejects alternate origins, literal credential/header fields, unsafe
paths, malformed known defaults, and multiple recognized actions. The suite now passes 32 tests.

Dry evaluation found and fixed a variable-canvas/fixed-verification contradiction plus an underspecified
MCP getter/direction mapping. The revised tasks derive API verification from the resolved canvas and
name `get_character`, bounded polling, and label-based direction saves. Skill-enabled iteration 2.1
scored 99/100 before the final documentation inconsistency was fixed. A no-skill API reader derived
the exact full URL, typed body, credential-env handling, output, and dynamic verification; it correctly
refused to treat the file alone as paid-call authority. A no-skill MCP reader found the workflow fully
executable but incorrectly treated the file as spend approval, motivating the explicit policy field.

Iteration 2 is complete. The final `_pixellab` shape also includes `required_before_calls`, public MCP
transport/docs, a concrete project-relative `output_directory`, and `output_collision_policy:
stop_if_exists`. Each paid bundled recipe now begins with an ordered `TASK` that checks explicit run
authority, credential presence, and an empty writable directory before spending. `portable-sprite`
and `paired-sprites` explicitly save and verify returned REST images. `knight` records stable typed
creation arguments, fresh-ID `get_character`, 10-second/10-minute bounded polling, no resubmission,
completed-response download restrictions, label normalization/order fallback, staged partial files,
and atomic publication after eight-frame verification.

One isolated no-skill Claude live REST replay succeeded with exactly one call and no retry: HTTP 200,
`$0.007937173896365696`, valid 48x48 transparent RGBA teal crystal key, exact typed body, source hash
unchanged, and no secret/header/base64 leakage. Evidence is under
`.local/blueprint-portability-iteration-2/iteration-2/live-no-skill-rest/`. Its historical concrete
blueprint omitted the save `TASK`, which directly caused the bundled REST recipe to gain that task;
the historical artifact remains unchanged. A separate isolated Codex run could not start because
that CLI account hit its usage limit and made no PixelLab call.

Final iteration-2 benchmark: 100.00 skill-enabled mean, 98.00 evidence-adjudicated no-skill mean,
90.57 raw external-judge mean retained for transparency, zero hard failures, and 32 passing QA tests.
Raw no-skill MCP graders repeatedly requested a nonexistent direction-count field and a fixed 48px
canvas gate; those deductions were rejected because visible schema/live evidence contradict them.
The valid output, authority, polling, mapping, and partial-publication deductions were fixed.

Final plugin refresh installed cache build `0.7.0+codex.20260714160209`. SHA-256 comparisons confirm
the installed `SKILL.md`, blueprint reference, and all three bundled blueprints exactly match the
final repository sources. Plugin validation passes. The repository manifest was restored to canonical
`0.7.0` after the cache copy so cross-platform manifest QA remains consistent. The skill-creator
iteration artifacts and static review viewer are at
`.local/blueprint-portability-iteration-2/iteration-2/benchmark.json` and `review.html`.

The blueprint system now has deterministic validator hardening, three bundled recipes covering MCP,
typed REST variables, and ordered structured `TASK`, and successful live coverage for REST replay,
ordered REST + `TASK`, ordinary MCP generation with automatic blueprint capture, discovery/inspection,
and no-skill portability. One bundled knight replay was operationally correct but failed its visual
spear constraint; one targeted prompt-remediation run also failed and established a persistent
model-adherence limitation. The generated REST blueprint replay passed. The generated MCP replay
correctly stopped after discovering that its source blueprint had hard-coded a historical managed
canvas size. That defect is fixed, independently dry-regressed, and cross-agent live-replayed. The
research spike and tracked JSON benchmark are complete, the corrected plugin was reinstalled and
rediscovered, and final QA passes. Do not resubmit any completed live job.

### Continuation update after handoff creation

- Main-agent review confirmed F's valid 88x88 orange ranger frames, E2's inconsistent spear and
  handedness, and G's valid 48x48 emerald potion.
- Fixed the managed-canvas defect in the canonical blueprint reference and user docs: exact output
  dimensions may be replay gates only when the request or route guarantees them. Managed frames with
  variable padding must be readable with identical runtime width/height; assembly geometry is derived
  from those current frames, while historical dimensions remain manifest evidence.
- An independent dry regression produced corrected tasks using runtime `W`/`H` and derived horizontal
  geometry `(8 * W) x H`; report:
  `.local/blueprint-production-readiness/canvas-rule-regression/report.md`.
- A second dry regression passed unresolved-variable batching, literal non-recursive values,
  malformed/conflicting default handling, and list-number scoping. It found that the validator already
  rejected `| fallback:` but the prose contract was ambiguous. The reference and user docs now state
  that `default` is the only pipe modifier; report:
  `.local/blueprint-production-readiness/variable-discovery-regression/report.md`.
- Full `python dev-tools/qa.py` and `git diff --check` passed before these final prose clarifications;
  run them again before publishing the research artifacts.
- Published `docs/pixellab/pixellab-blueprint-production-readiness-spike.md` and the adjacent JSON
  score artifact. QA parses them, all local links resolve, score arithmetic was recomputed, and exact
  REST usage totals `$0.03087746198972066`.
- Independent evidence audit passed math, manifest parsing, source hashes, and sensitive-data hygiene,
  and found three actionable gaps: no-skill reports were not persisted, corrected managed MCP had only
  dry replay evidence, and defect closure wording needed validation-level precision. Sanitized
  no-skill reports and score evidence paths now exist; research/score release gates now split generated
  REST success from corrected managed-MCP live closure.
- Agent H completed a fresh normal managed generation under the fixed rule at 100/100. Eight 92x92
  frames and a derived 736x92 pixel-exact sheet passed. Its automatically generated blueprint records
  no observed dimensions; it requires identical runtime frame dimensions and derives sheet geometry.
  Evidence: `pixellab-pip-generations/blueprint-readiness-agent-h-corrected-mcp/` and
  `.local/blueprint-production-readiness/agent-h-corrected-mcp/report.md`.
- Agent I replayed H's generated blueprint with only sand-gold changed to deep indigo and scored
  100/100. Eight fresh 92x92 frames produced a runtime-derived 736x92 sheet; all cells matched their
  sources with zero absolute error, visual review passed, and the source hash remained unchanged.
  Evidence: `pixellab-pip-generations/blueprint-readiness-agent-i-corrected-mcp-replay/` and
  `.local/blueprint-production-readiness/agent-i-corrected-mcp-replay/report.md`.
- Cache-busted and reinstalled the local plugin as `0.7.0+codex.20260714144340`. A fresh ephemeral,
  read-only Codex session outside the repository discovered all three bundled blueprints and
  correctly inspected `portable-sprite` without PixelLab calls. Evidence:
  `.local/blueprint-production-readiness/installed-plugin-discovery/report.md`.

## Architecture and Contract Understanding

### Architecture Overview

PixelLab Pip is a Markdown runtime contract: the root skill classifies and routes, focused references
define operational behavior, bundled JSON files are discovered at runtime, Python QA validates
deterministic shape and safety invariants, and independent agents exercise the semantics live.
Generated artifacts and manifests are evidence rather than tracked product source.

### Runtime placement

- `skills/pixellab-pip/SKILL.md` is the lean global router and safety contract.
- `skills/pixellab-pip/references/blueprint.md` is the canonical operational blueprint contract.
- `docs/blueprint.md` is user-facing explanation and may repeat concepts for readability.
- `skills/pixellab-pip/blueprints/` is runtime discovery scope for bundled recipes.
- `dev-tools/qa.py` validates blueprint shape and repository invariants.
- `tests/test_blueprints.py` is the focused deterministic regression suite.
- `.local/blueprint-production-readiness/` contains ignored sanitized agent evidence.
- `pixellab-pip-generations/blueprint-readiness-agent-*/` contains ignored live artifacts,
  concrete replay blueprints, and manifests.

### Critical Files

| File | Purpose | Relevance |
|---|---|---|
| `skills/pixellab-pip/SKILL.md` | Global runtime router and safety contract | Must remain lean and canonical for global behavior. |
| `skills/pixellab-pip/references/blueprint.md` | Blueprint operation contract | Canonical location for the managed-canvas fix. |
| `dev-tools/qa.py` | Repository validator | Contains deterministic hardening from this session. |
| `tests/test_blueprints.py` | Blueprint regressions | Must pass with every implementation edit. |
| `docs/plans/blueprint-production-readiness-plan.md` | Full campaign | Defines scores and release gates. |

### Blueprint semantics validated

- Root is one step object or a bare ordered array.
- Exactly one executable key per step: `MCP <tool>`, `POST /v2/<endpoint>`, or `TASK`.
- `_comment*` is non-executable string metadata.
- Variables resolve only inside executable values; explicit override wins, then confident inference,
  then default, then one combined clarification for unresolved required values.
- Whole-field placeholders preserve JSON type; embedded placeholders must resolve to scalars.
- Variable descriptions unify case-insensitively after trimming/collapsing whitespace.
- Source templates are immutable; successful runs write a new concrete variable-free blueprint.
- `TASK` order is array order. Structured tasks name relative inputs/outputs and observable gates.
- A task verification failure stops the workflow unless an authorized fallback is written.
- Managed MCP fresh IDs are represented by a concrete create call followed by a structured `TASK`
  that uses the returned ID with the matching getter. Never hard-code a stale ID or invent bindings.
- Every live generation flow now explicitly writes a manifest; audit/resume data stays out of the
  shareable blueprint.

## Work Completed

### Plan and audits

- Added `docs/plans/blueprint-production-readiness-plan.md` with a complete smoke/live/portability
  matrix, test IDs, scoring, release gates, defect loop, and evidence requirements.
- Three read-only audit agents reviewed the format, validator, agent CLI isolation, and coverage.
- Baseline and every post-edit run of `python dev-tools/qa.py` passed.
- Current focused result: 30 unit tests pass (12 blueprint test methods plus the rest of the suite).
- Official `https://api.pixellab.ai/v2/openapi.json` was fetched to verify the current
  `create-image-pixen` and `create-image-pixflux` request schemas before shipping recipes.
- `PIXELLAB_SECRET` was confirmed present as a boolean only; its value was never read or recorded.

### Validator defects fixed

`dev-tools/qa.py` and `tests/test_blueprints.py` now cover these confirmed defects:

1. Reject stray `}}` closing markers.
2. Reject unsupported variable operators such as `| fallback:`.
3. Reject multiple `| default:` markers in one placeholder.
4. Require every `_comment*` value to be a nonblank string.
5. Restrict MCP route names to safe token characters.
6. Restrict REST route suffixes to safe path segments; reject traversal, schemes, queries, and
   fragments rather than accepting strings such as `POST /v2/../../private`.
7. Require whole-field defaults for `TASK.instruction` and `TASK.verify` to be strings.
8. Reject duplicate/case-colliding outputs produced by different task steps.
9. Reject `TASK` paths that are `.`, directory-like with a trailing slash, UNC/absolute, URL/data
   URI, parent traversal, or duplicates after portable normalization.
10. Validate untracked blueprint files under `skills/`, `docs/`, and `tests/` during development,
    not only files already known to `git ls-files`.

### Runtime/documentation fixes

- `skills/pixellab-pip/SKILL.md` now explicitly requires a manifest after every live generation.
- `skills/pixellab-pip/references/usage-reporting.md` now uses mandatory manifest wording.
- `skills/pixellab-pip/references/blueprint.md` documents the fresh managed-ID `TASK` pattern.
- `docs/blueprint.md` explains that pattern for users.
- The knight comment no longer falsely promises an explicit 8-direction request; its body only
  records a description and relies on current `create_character` behavior.

### Bundled recipes added

1. `knight.blueprint.json`
   - MCP `create_character`.
   - Embedded scalar defaults for armor, left-hand weapon, and right-hand item.
2. `portable-sprite.blueprint.json`
   - REST `POST /v2/create-image-pixen`.
   - Required description plus whole-field object, boolean, and null defaults.
   - Live test proved explicit `false` and `0` are preserved.
3. `paired-sprites.blueprint.json`
   - Two ordered REST calls and two structured `TASK` steps.
   - Repeated object default uses whitespace-varied variable spelling to prove normalization.
   - Live test proved byte-identical result saves and pixel-identical native-size assembly.

## Completed Agent and Live Results

### Agent A — discovery and inspection

- Prompt: repository `SKILL.md` + “What blueprints are available? Then inspect portable-sprite
  without running it.”
- Result: PASS, 80/80 applicable.
- Correct sorted list: `knight`, `paired-sprites`, `portable-sprite`.
- Listing leaked no paths, routes, or bodies.
- Inspection correctly identified required description and typed 64x64 object, `true`, and `null`
  defaults without auth or spend.
- All source hashes unchanged.
- Evidence: `.local/blueprint-production-readiness/agent-a-discovery/report.md`.

### Agent B — live REST bundled replay

- Prompt: run `portable-sprite` as a 48x48 cobalt potion bottle, background `false`, seed `0`.
- Result: PASS, 98/100.
- Exact route/body: `POST /v2/create-image-pixen`, one synchronous paid call.
- Usage: `$0.007191092252731323`.
- Output: valid 48x48 opaque RGBA PNG; cobalt bottle and cork pass; mild oblique composition and
  peripheral bottle fragments are a visual note only.
- Source blueprint SHA-256 remained
  `b76b87d7f6060de77fd95650c95d4aceffb5cf38451e5d37f4c15a87a1c82938`.
- Concrete blueprint is variable-free and captures save materialization as structured `TASK`.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-b-rest/cobalt-potion-bottle.png`
  - `pixellab-pip-generations/blueprint-readiness-agent-b-rest/cobalt-potion-bottle.blueprint.json`
  - `pixellab-pip-generations/blueprint-readiness-agent-b-rest/manifest.json`
  - `.local/blueprint-production-readiness/agent-b-rest/report.md`

### Agent C — ordinary live MCP task, no source blueprint

- Prompt: create a compact 48px forest ranger with moss-green cloak and short bow; explicitly a
  normal task.
- Result: PASS, 97/100.
- Exact route: visible MCP `create_character`, mode `v3`, one managed asset submission.
- Eight coherent 84x84 RGBA directions were downloaded; returned canvas includes animation room
  around the requested 48px character size.
- 672x84 sheet cells compare pixel-identically with all eight sources.
- Per-call usage was not exposed; overlapping balance observation was `$9.44 -> $9.39` and must not
  be claimed as this job’s exact price.
- This run found and motivated the documented fresh managed-ID `TASK` pattern.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-c-mcp/forest-ranger-directions.png`
  - `pixellab-pip-generations/blueprint-readiness-agent-c-mcp/forest-ranger.blueprint.json`
  - `pixellab-pip-generations/blueprint-readiness-agent-c-mcp/manifest.json`
  - `.local/blueprint-production-readiness/agent-c-mcp/report.md`

### Agent D — live ordered REST + structured TASK replay

- Prompt: run `paired-sprites` with red health potion left and blue mana potion right at default
  size.
- Result: PASS, 100/100.
- Two exact synchronous calls, strictly sequential, no retries.
- Usage total: `$0.01597196716732449`.
- Source blueprint SHA-256 remained
  `91395343e9a573c0aaa79d35a9569d59127275ba0dfb2ed3d6e385bea5e75046`.
- Saved call results are byte-identical to returned PNG bytes.
- 128x64 RGBA comparison has zero absolute-error pixels for both extracted cells and preserves
  transparency.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-d-task/paired-sprites.png`
  - `pixellab-pip-generations/blueprint-readiness-agent-d-task/paired-potions.blueprint.json`
  - `pixellab-pip-generations/blueprint-readiness-agent-d-task/manifest.json`
  - `.local/blueprint-production-readiness/agent-d-task/report.md`

### Agent E — live bundled knight MCP replay

- Prompt: crimson armor, spear in left hand, empty right hand.
- Operational result: PASS; visual acceptance: FAIL; score 92/100.
- Exact recorded MCP surface and resolved description were used; one standard generation.
- Eight 68x68 RGBA directions and a pixel-identical 4x2 sheet were saved.
- Crimson armor and empty right hand pass.
- Spear fails: a short sword-like weapon appears in six views and is absent in direct north/south.
- This is a PixelLab prompt/adherence failure, not blueprint parsing/routing/artifact dishonesty.
- Agent correctly recorded overall verification failure rather than claiming final success.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-e-knight/knight-directions.png`
  - `pixellab-pip-generations/blueprint-readiness-agent-e-knight/knight-replay.blueprint.json`
  - `pixellab-pip-generations/blueprint-readiness-agent-e-knight/manifest.json`
  - `.local/blueprint-production-readiness/agent-e-knight/report.md`

### Agent E2 — targeted knight prompt remediation

- Result: operational PASS; semantic acceptance FAIL; 84/100 under the stricter remediation rubric.
- Used the same recorded description-only MCP surface for one fresh standard generation.
- A clearer long-polearm value improved clear spear identity only from 0/8 to 3/8 directions.
- Weapon presence changed from 6/8 to 5/8; two diagonal views remained short-sword-like.
- Direct south appears wrong-handed, so the empty-right-hand constraint cannot be trusted.
- Conclusion: prompt specificity helps some views but does not make exact multi-direction equipment
  identity/handedness reliable on this route. Keep the failed gate; do not spend on blind rerolls.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-e2-knight-remediation/`
  - `.local/blueprint-production-readiness/agent-e2-knight-remediation/report.md`

### Agent G — cross-agent replay of generated REST blueprint

- Replayed Agent B's generated concrete blueprint with only emerald-green and seed `1` overrides.
- Result: PASS, 100/100.
- One exact REST call; usage `$0.0077144025696648496`.
- Valid 48x48 fully opaque PNG; emerald color, cork, and top-down composition pass.
- Saved result is byte-identical to the returned PNG; source blueprint hash remained unchanged.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-g-generated-rest-replay/`
  - `.local/blueprint-production-readiness/agent-g-generated-rest-replay/report.md`

### Agent F — cross-agent replay of generated MCP blueprint

- Replayed Agent C's generated ranger blueprint with only moss-green → autumn-orange cloak changed;
  all other MCP fields were verbatim.
- Managed creation completed once; eight coherent 88x88 transparent RGBA rotations plus ZIP passed
  integrity and visual checks for orange cloak and short bow.
- The source generated blueprint required the historical first-run canvas size 84x84. Because the
  replay returned 88x88 for the same `size: 48`, mode `v3` request, its verification gate failed and
  the agent correctly stopped before spritesheet assembly.
- Source blueprint hash remained unchanged. A concrete partial-success blueprint and manifest were
  written honestly.
- Confirmed production defect: automatic managed-asset blueprints must not turn an observed canvas
  size into a future request guarantee when the schema's `size` describes subject size and returned
  canvas padding may vary. Verification should require readable, mutually compatible frames and
  derive sheet geometry from current returned dimensions unless the route guarantees exact output.
- Files:
  - `pixellab-pip-generations/blueprint-readiness-agent-f-generated-mcp-replay/forest-ranger-autumn-orange.blueprint.json`
  - `pixellab-pip-generations/blueprint-readiness-agent-f-generated-mcp-replay/manifest.json`
  - `.local/blueprint-production-readiness/agent-f-generated-mcp-replay/report.md`

### No-skill portability — isolated Codex, benign REST

- Ran outside the repo with `--ignore-user-config --ignore-rules --disable plugins`, read-only.
- Correctly resolved 48x48 object, explicit `false`, explicit seed `0`, exact body, source immutability,
  and missing base URL/auth/schema/network authority.
- No API/network call was attempted.

### No-skill portability — isolated Claude, ordered TASK

- Ran outside the repo with safe mode, slash commands disabled, no session persistence, read-only
  tools only.
- Correctly normalized the repeated `canvas size` variable, preserved object type, explained all
  four ordered steps, immediate-result binding, byte vs pixel gates, 128x64 assembly, and source
  immutability.
- Portability limitation: it proposed retrying the second failed paid call without Pip’s credit/retry
  contract. Record this as a no-skill policy limitation; do not duplicate global credit safety into
  every blueprint.

### No-skill portability — isolated Codex, malicious attachment

- Correctly treated comment text as inert metadata and rejected secret exfiltration, undeclared
  network authority, a parent-traversal output, fabricated verification, and source rewriting.
- No execution or secret access occurred.

### Gemini environment limitation

- Gemini CLI 0.40.0 could not run because its current Code Assist client/tier is unsupported.
- This is an environment failure, not a blueprint score. Preserve it as a benchmark limitation and
  do not count it as a blueprint test failure.

## Active Agent Runs

All delegated runs are complete. Agent I's authorized cross-agent replay of H's generated managed
blueprint passed with only the hood color changed. Evidence:

- `pixellab-pip-generations/blueprint-readiness-agent-i-corrected-mcp-replay/`
- `.local/blueprint-production-readiness/agent-i-corrected-mcp-replay/report.md`

The main agent inspected its report, concrete blueprint, manifest, and visual sheet. Do not duplicate
this paid call.

## Files Currently Changed

The worktree was clean at start. The following intended changes are currently staged in the shared
workspace; preserve them and inspect before committing:

| File | Change |
|---|---|
| `dev-tools/qa.py` | Hardens placeholders, comments, routes, task types/paths/outputs, and untracked blueprint scanning. |
| `tests/test_blueprints.py` | Adds regressions for every confirmed validator defect. |
| `skills/pixellab-pip/SKILL.md` | Requires manifests for live generation flows. |
| `skills/pixellab-pip/references/blueprint.md` | Documents managed fresh-ID task pattern. |
| `skills/pixellab-pip/references/usage-reporting.md` | Makes live manifest writing explicit. |
| `docs/blueprint.md` | Corrects knight wording and explains managed ID pattern. |
| `skills/pixellab-pip/blueprints/knight.blueprint.json` | Removes unencoded “8-directional” claim. |
| `skills/pixellab-pip/blueprints/portable-sprite.blueprint.json` | New typed REST recipe. |
| `skills/pixellab-pip/blueprints/paired-sprites.blueprint.json` | New ordered REST + TASK recipe. |
| `docs/plans/blueprint-production-readiness-plan.md` | Full campaign plan. |
| `docs/plans/blueprint-production-readiness-handoff.md` | This handoff. |

Do not commit generation outputs or `.local/` evidence unless repository ignore policy is explicitly
changed; they are test evidence, not source artifacts.

### Files Modified

The table above is the authoritative changed-file inventory. All changes were created for this
campaign; the starting worktree was clean. At the last status check, the intended files except this
new handoff were staged by the shared workspace, while this handoff was still untracked.

## Decisions Made

| Decision | Rationale |
|---|---|
| Exhaust blueprint behavior, not every PixelLab endpoint. | Every blueprint primitive and route family needs coverage; generating through every endpoint would spend credits without adding contract evidence. |
| Add only two new bundled recipes. | They provide distinct typed REST and structured TASK value; edge cases remain tests rather than cluttering runtime discovery. |
| Treat no-skill execution capability separately from comprehension. | A standalone blueprint does not safely provide credentials, service base URL, MCP tools, or global retry policy. Honest preflight is success; invented calls are failure. |
| Require live manifests globally. | The user requires manifest review and the blueprint is intentionally not the private audit record. |
| Use TASK for managed fresh-ID polling. | Blueprint format intentionally has no bindings; hard-coded getter IDs are stale and non-replayable. |
| Keep the first failed knight run. | It proves acceptance gates and honest reporting; do not erase diagnostic failures when remediation succeeds. |
| Do one targeted spear retry. | It changes the failure-targeting prompt rather than blindly rerolling, consistent with paid retry guidance. |
| Record Gemini as unavailable. | Authentication-tier failure is environmental and must not be disguised as a blueprint result. |

## Important Context

The next agent should begin with the managed-canvas defect, not with another live generation. The
same managed character request produced 84x84 and 88x88 canvases. Exact observed dimensions belong
in the run manifest, but a generated replay blueprint may require them only when the public schema
or route guarantees them. Otherwise its task should validate that returned frames are readable and
mutually compatible, derive current sheet geometry, preserve pixels and transparency, and report
the observed dimensions. Historical failed artifacts must remain unchanged as evidence.

### Assumptions Made

- The user authorized the full campaign, including paid tests, without a spending ceiling.
- Public current MCP tool schemas and REST v2 OpenAPI are authoritative for route/body checks.
- Generation nondeterminism is expected; workflow fidelity and constraints, not pixel identity
  across separate generations, determine replay success.
- A safe no-skill preflight is valid portability evidence even when execution capability is absent.

### Potential Gotchas

- Do not resubmit completed or failed paid jobs; manifests retain their identifiers and evidence.
- Do not treat MCP request `size` as guaranteed output canvas geometry without schema evidence.
- Do not change historical generated blueprints in ignored test folders; use them to prove regression.
- Keep exact REST bodies and MCP arguments concrete in generated blueprints; variables are only for
  hand-authored or bundled templates.
- Installed plugin cache `0.7.0+codex.20260714144340` is current; a fresh session confirmed discovery.
- Run the handoff validator with Python UTF-8 mode on Windows to avoid locale decoding failure.

## Immediate Next Steps

1. Commit with a conventional message only if the user requests or the repository workflow requires
   it. No commit has been made in this session.

## Open Questions and Residual Risks

- E2 established that clearer prompt normalization improves some views but does not solve exact
  multi-direction equipment identity, presence, or handedness. Treat this as a current route/model
  limitation; do not weaken the acceptance gate or spend on blind retries.
- Managed character request `size` is not necessarily the returned file canvas size. The same
  effective `size: 48`, mode `v3` route produced 84x84 and 88x88 frames in two runs. Never encode a
  historical observed canvas as a replay requirement unless current schema/docs guarantee it.
- No-skill agents understand the format well, but they do not inherently know Pip’s credit retry,
  auth, polling, or public/private endpoint policy. This is expected; keep the blueprint portable and
  minimal rather than embedding the whole skill contract.
- Runtime variable resolution is agent behavior specified in Markdown, not a shared executable
  resolver library. Deterministic QA validates syntax and defaults, while independent agent tests
  validate resolution semantics. Do not add a speculative runtime engine unless evidence demands it.
- Manifest schema is intentionally descriptive rather than a versioned runtime blueprint wrapper.
  The benchmark score JSON may have its own schema label; blueprints must not gain one.
- Generated image quality is nondeterministic. Compare replay workflow, request fields, constraints,
  and artifact validity, never promise pixel-identical generations.

## Environment State

- OS/shell: Windows PowerShell.
- Python available and `python dev-tools/qa.py` passes.
- PixelLab MCP tools are visible in the Codex host.
- REST authentication is configured through the expected environment variable; never print its value.
- Available independent CLIs observed:
  - Codex CLI 0.144.4.
  - Claude Code 2.1.209.
  - Gemini CLI 0.40.0, currently unusable due upstream unsupported-client/tier authentication.
- Installed Codex plugin cache is current at `0.7.0+codex.20260714144340`; a fresh read-only Codex
  session loaded it and passed blueprint discovery.
- No dev server or delegated agent is running.

## Verification Commands

Run from the repository root:

```powershell
python dev-tools/qa.py
git diff --check
git status --short
git diff --cached --stat
```

For final plugin update, follow the plugin-creator skill’s already-read update and reinstall
instructions; do not hand-edit marketplace configuration.

## Release Gates Still Outstanding

- [x] Collect F generated-MCP replay; main-agent visual inspection still recommended.
- [x] Fix and independently regress the managed-canvas verification defect exposed by F.
- [x] Run final dry variable/discovery edge-case regression and close its modifier ambiguity.
- [x] Collect G generated-REST replay; main-agent visual inspection still recommended.
- [x] Collect E2 targeted knight remediation; main-agent visual inspection still recommended.
- [x] Publish research spike; first independent evidence-audit corrections applied.
- [x] Publish tracked JSON score/benchmark artifact; first independent evidence-audit corrections applied.
- [x] Persist sanitized reports and evidence links for all three no-skill runs.
- [x] Complete fresh corrected managed-MCP blueprint generation and cross-agent live replay.
- [x] Final QA/diff/security scan.
- [x] Cache-bust, validate, and reinstall local Codex plugin.
- [x] Confirm installed-plugin discovery in a fresh thread.
- [x] Decide release readiness and record residual limitations.
- [x] Separate canonical writer rules from tolerant semantic reader behavior.
- [x] Add self-contained public service/auth/authority/output metadata.
- [x] Make QA extension-open while strictly validating known fields.
- [x] Complete iteration-2 skill/no-skill dry and live evaluation.
- [x] Refresh installed plugin after iteration-2 changes and perform final verification.
