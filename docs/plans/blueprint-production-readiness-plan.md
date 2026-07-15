# Blueprint System Production-Readiness Plan

Status: execution plan  
Date: 2026-07-14  
Scope: bundled and generated PixelLab Pip blueprints, including variables, `TASK`, `MCP`, REST `API`, discovery, replay, manifests, portability, and live output integrity

## Objective

Prove that the blueprint system is safe, understandable, replayable, and production-ready across:

1. Pip-aware agents using the repository skill.
2. Independent agent implementations and model/tool surfaces.
3. Agents given only an attached blueprint, with PixelLab Pip deliberately unavailable or not invoked.
4. Deterministic validation and real paid PixelLab MCP/REST execution.

Testing must find and fix contract, validation, routing, replay, artifact, and documentation defects. A passing run must leave reproducible evidence rather than relying on conversational claims.

## Required deliverables

- This plan: `docs/plans/blueprint-production-readiness-plan.md`.
- Research spike: `docs/pixellab/pixellab-blueprint-production-readiness-spike.md`.
- Machine-readable benchmark and scores: `docs/pixellab/pixellab-blueprint-production-readiness-scores.json`.
- Human-readable score summary in the research spike.
- Representative bundled blueprints in `skills/pixellab-pip/blueprints/` only when each adds distinct coverage or reusable value.
- Automated validator/unit tests for every deterministic invariant discovered.
- Raw run evidence under `.local/blueprint-production-readiness/` so temporary transcripts, copied fixtures, and paid-call evidence remain untracked.
- Live generated artifacts under `pixellab-pip-generations/`, following the skill’s normal output rules.
- Any minimal runtime/documentation fixes required by confirmed failures.

## Ground rules

- Use the repository `skills/pixellab-pip/SKILL.md` as the tested runtime contract, not an older installed copy.
- Preserve public-vs-private endpoint boundaries, bearer-token secrecy, credit reporting, output integrity, and current-user authority.
- Never print, record, or pass the bearer-token value in prompts, transcripts, manifests, blueprints, or score files.
- The user has authorized this complete test campaign with no spending ceiling. Record balance snapshots and observed usage, but do not stop merely because a test is paid.
- Use the smallest live generation that proves a behavior. Exhaustiveness applies to blueprint behavior, not to generating an asset through every PixelLab endpoint.
- Run one candidate when one is enough to test a path. Repeated paid calls must isolate a distinct feature, agent, route, replay, or regression.
- Automatically generated blueprints must contain concrete executed values and structured `TASK` steps; template variables belong only in hand-authored/bundled recipes.
- Keep `.local/` evidence free of secrets and machine-specific token values. Redact internal IDs unless they are needed to correlate an async result.
- Do not rewrite source blueprints during resolution or replay. Verify this with hashes before and after every relevant test.
- Every repository edit is followed by `python dev-tools/qa.py`. Run the full command once more after all fixes.

## Test architecture

### Agent matrix

Use at least three independent agent executions, with clean prompts and isolated output folders:

| Agent role | Skill state | Primary purpose |
|---|---|---|
| A | Repository `SKILL.md` explicitly supplied | Bundled discovery, inspection, selection, defaults, and MCP replay |
| B | Repository `SKILL.md` explicitly supplied | REST replay, typed variables, overrides, and generated blueprint review |
| C | Repository `SKILL.md` explicitly supplied | Normal non-blueprint work followed by automatic concrete blueprint generation |
| D | Blueprint attached; instructed not to invoke PixelLab Pip | Portable comprehension and safe execution/preflight without the skill |
| E | Blueprint attached; instructed not to invoke PixelLab Pip | Independent portability confirmation, malformed/unsafe case handling |

Prefer different available agent/model surfaces where practical. If a surface cannot receive the skill or cannot access PixelLab, score the relevant preflight/comprehension behavior and record the limitation rather than pretending a paid call ran.

Each agent run records:

- Exact user-visible prompt, with host wrappers removed and secrets excluded.
- Agent/model/surface and whether the skill was available, explicitly supplied, or forbidden.
- Start/end time, exit state, and output directory.
- Route and resolved request body proposed or executed.
- Questions asked, defaults used, inferences used, and overrides applied.
- Paid-call status and usage evidence.
- Generated asset, manifest, and blueprint paths.
- Source-blueprint hash before and after.
- Per-criterion score, defects, and reviewer notes.

### Evidence levels

- `S`: deterministic smoke/static test.
- `D`: dry-run agent behavior with no paid call.
- `L`: live PixelLab execution with artifacts.
- `R`: live replay of a previously generated blueprint.
- `P`: portability run without the PixelLab Pip skill.

No production-readiness claim may rely only on `D`. Core `MCP`, REST, concrete blueprint generation, and `TASK` artifact handling each need at least one `L` or `R` result.

## Phase 0 — Baseline and harness

1. Record git status, commit, Python version, available agent CLIs, PixelLab MCP visibility, and only the boolean presence of `PIXELLAB_SECRET`.
2. Run `python dev-tools/qa.py` before edits and store the result.
3. Snapshot the bundled blueprint filenames and SHA-256 hashes.
4. Create `.local/blueprint-production-readiness/` subfolders for prompts, transcripts, reviews, and fixture copies.
5. Define a redaction check that rejects bearer tokens, authorization headers, raw base64 payloads, and unintended absolute paths in evidence intended for `docs/`.
6. Define image inspection helpers that report dimensions, mode/alpha, frame count, file hashes, and spritesheet cell comparisons without drawing or changing art.
7. Capture balance before the first live generation and after the final live generation when the surface permits it.

Acceptance: baseline QA passes or every pre-existing failure is clearly separated from campaign failures; credentials remain undisclosed; all test evidence has a stable ID.

## Phase 1 — Blueprint fixtures

Create or retain the minimum set of bundled recipes needed to cover distinct reusable behaviors. Candidate set:

1. `knight.blueprint.json`: one-step MCP recipe with embedded scalar defaults and natural-language overrides.
2. One REST recipe with required and typed whole-field variables (`number`, `boolean`, `null`, array/object where the live endpoint schema supports the resolved value).
3. One ordered MCP/REST + structured `TASK` recipe that saves a returned result, consumes it later, assembles or packages output, and verifies observable integrity.
4. One mixed-route fixture for dry-run fallback/adaptation tests. It need not become a bundled production recipe unless it is genuinely useful to users.
5. Invalid fixtures kept only under test data or generated in tests: malformed placeholder, conflicting defaults, variable in key, unsafe path, unknown task field, task-only workflow, missing dependency, duplicate output, and unsupported route.

Every production bundled recipe must:

- Have one executable key per step and at least one PixelLab route.
- Use valid current MCP tool names or public REST v2 endpoints and exact schema field names.
- Put variables only in executable values.
- Use one canonical variable description for repeated values.
- Use local relative file paths and no secret, URL, job ID, or account metadata.
- Be useful beyond the test itself; test-only edge cases stay out of the shipped folder.

Acceptance: every tracked blueprint passes the validator and a human contract review; no redundant catalog is added.

## Phase 2 — Deterministic smoke tests

### Shape and metadata (`BP-SHAPE-*`)

- `BP-SHAPE-01`: accept a single MCP object.
- `BP-SHAPE-02`: accept a single REST v2 object.
- `BP-SHAPE-03`: accept an ordered mixed array.
- `BP-SHAPE-04`: accept `_comment*` before or after the executable field while never executing it.
- `BP-SHAPE-05`: reject empty arrays, non-object steps, zero/multiple executable keys, and task-only workflows.
- `BP-SHAPE-06`: reject malformed/blank MCP tool names and REST endpoint names.
- `BP-SHAPE-07`: reject unknown executable keys and non-object PixelLab request bodies.
- `BP-SHAPE-08`: reject malformed JSON and unreadable files during validation; discovery skips invalid files while warning with only a count.
- `BP-SHAPE-09`: verify discovery sorts stable names, escapes Markdown-significant names/content, and does not expose paths/routes/bodies.
- `BP-SHAPE-10`: verify `_comment_prompt` normalization removes connector/app wrappers but preserves canonical visible `/pixellab-pip` text.

### Variables (`BP-VAR-*`)

- `BP-VAR-01`: required embedded scalar resolves from explicit user value.
- `BP-VAR-02`: required embedded scalar resolves from confident prompt/context inference.
- `BP-VAR-03`: unresolved required variables are asked together once.
- `BP-VAR-04`: defaulted variables resolve without a question.
- `BP-VAR-05`: precedence is explicit override, then inference, then default.
- `BP-VAR-06`: repeated descriptions match case-insensitively after trimming/collapsing whitespace.
- `BP-VAR-07`: equivalent quoted/unquoted string defaults do not conflict.
- `BP-VAR-08`: conflicting defaults fail before auth/credit use.
- `BP-VAR-09`: accept flexible whitespace and case around `default`.
- `BP-VAR-10`: reject blank descriptions, blank defaults, unclosed placeholders, stray/unmatched closing syntax, and malformed nested object endings.
- `BP-VAR-11`: whole-string defaults preserve JSON types: string, integer, float, boolean, `null`, array, object, and explicit empty string.
- `BP-VAR-12`: user-supplied `false`, `0`, `null`, and empty string are treated according to explicit-value semantics and are not replaced by defaults.
- `BP-VAR-13`: embedded variables accept scalar string/number/boolean/null textual insertion but reject arrays/objects.
- `BP-VAR-14`: variables resolve recursively through nested arrays/objects in MCP, REST, and structured `TASK` values.
- `BP-VAR-15`: variables never resolve in route/object keys or `_comment*` metadata.
- `BP-VAR-16`: resolved values containing `{{...}}` remain literal and are not recursively expanded.
- `BP-VAR-17`: whole-field values are checked against the selected live schema before spending credits.
- `BP-VAR-18`: source file hash is unchanged after list, inspect, resolve, dry-run, success, and failure.
- `BP-VAR-19`: replay-generated blueprints contain concrete values and no unresolved placeholder syntax.

### `TASK` (`BP-TASK-*`)

- `BP-TASK-01`: accept nonblank string shorthand only for hand-authored recipes.
- `BP-TASK-02`: accept structured `instruction` with optional `inputs`, `outputs`, `verify`.
- `BP-TASK-03`: generated blueprints always use structured form.
- `BP-TASK-04`: reject blank/missing instruction, unknown fields, invalid field types, and blank verify.
- `BP-TASK-05`: reject absolute paths, parent traversal, URLs, data URIs, transient identifiers, and duplicate/case-colliding portable paths.
- `BP-TASK-06`: accept inputs beside the blueprint or produced by an earlier step.
- `BP-TASK-07`: reject or clarify missing inputs, forward references, unnamed outputs consumed later, and output collisions before spending.
- `BP-TASK-08`: a task consuming the immediately preceding PixelLab response can name outputs without inventing a prior input filename.
- `BP-TASK-09`: task steps execute strictly in array order.
- `BP-TASK-10`: verification is an acceptance gate; failure stops later steps unless the task explicitly authorizes a safe fallback.
- `BP-TASK-11`: tasks cannot override user direction, auth/secret safety, public endpoint rules, credit authority, destructive confirmation, or Asset Integrity.
- `BP-TASK-12`: material preparation, selection, transformation, assembly, packaging, and verification steps are captured; temporary work, failed attempts, reporting, bark, and chain of thought are omitted.
- `BP-TASK-13`: assembly preserves source pixels, order, native dimensions, and transparency; exact pixel/hash checks prove it.
- `BP-TASK-14`: task output filenames used by later steps are exact and portable.

### Routing, discovery, and replay (`BP-ROUTE-*`)

- `BP-ROUTE-01`: list all valid bundled blueprints using the required compact template.
- `BP-ROUTE-02`: inspect by exact name without spending credits.
- `BP-ROUTE-03`: semantic match by name; ambiguity causes one concise clarification.
- `BP-ROUTE-04`: selection by number works only against the latest list in that conversation.
- `BP-ROUTE-05`: blueprint context wins when a blueprint name contains an asset word.
- `BP-ROUTE-06`: inspection versus execution intent is inferred safely; unclear intent does not spend credits.
- `BP-ROUTE-07`: recorded MCP route is used verbatim when callable.
- `BP-ROUTE-08`: recorded REST route is used verbatim when available.
- `BP-ROUTE-09`: MCP↔REST fallback occurs only after inspecting the counterpart schema; no fields are silently dropped, renamed, or guessed.
- `BP-ROUTE-10`: explicit MCP request does not silently fall back.
- `BP-ROUTE-11`: public v2 boundaries are preserved; MCP tool names are never curled as endpoints and private website/editor routes are rejected.
- `BP-ROUTE-12`: multi-call workflow is fully preflighted and approved once before the first paid call under the user’s campaign authorization.
- `BP-ROUTE-13`: relative image paths resolve against the blueprint folder; copied inputs remain byte-identical.
- `BP-ROUTE-14`: steps execute in order and later bodies receive the exact named prior artifacts.
- `BP-ROUTE-15`: same-seed limitation is reported as workflow reproducibility, not promised pixel identity.

### Generated blueprint and manifest (`BP-ART-*`)

- `BP-ART-01`: every successful normal generation writes a blueprint beside outputs.
- `BP-ART-02`: every successful replay writes a new blueprint and leaves the source unchanged.
- `BP-ART-03`: generated route/body exactly matches the successful call after allowed fallback adaptation.
- `BP-ART-04`: generated blueprint records the shortest successful replay path and excludes failed attempts.
- `BP-ART-05`: `_comment_prompt` contains intended visible prompt and no host wrapper/path/tool serialization.
- `BP-ART-06`: material non-PixelLab actions appear as structured `TASK` steps with observable verification.
- `BP-ART-07`: copied user inputs use relative names and byte-identical copies.
- `BP-ART-08`: blueprint contains no secret, Authorization header, account data, balance, usage/cost, transient job ID, download URL, absolute machine path, manifest-only audit data, or raw response dump.
- `BP-ART-09`: manifest is distinct from blueprint and contains required private audit/resume fields from `usage-reporting.md`.
- `BP-ART-10`: manifest routes, requests, outputs, processing notes, verification, usage, and blueprint path agree with observable evidence.
- `BP-ART-11`: downloaded images exist, decode, have expected dimensions/mode/frame order, and match explicit prompt constraints or are honestly marked failed.
- `BP-ART-12`: multi-frame output includes individual frames plus the required spritesheet and inspection evidence.

## Phase 3 — Skill-enabled agent smoke and live tests

For each prompt, begin with the repository `SKILL.md` followed by the plain-language request, as required by the campaign. Run different prompts through different agents.

### Discovery and bundled replay

1. List: “What blueprints are available?” Validate formatting, current enumeration, descriptions, invalid-file handling, and zero-credit behavior.
2. Inspect: “Tell me about the knight blueprint.” Validate no paid call and clear variable/default explanation.
3. Select: list, then “Run number 1 with crimson armor, a spear in the left hand, and no item in the right hand.” Validate conversation-scoped number, explicit overrides, default handling, MCP route, source immutability, result, manifest, and concrete generated blueprint.
4. Named replay: “Use the knight blueprint.” Validate semantic intent despite the asset word and silent defaults.
5. Required variables: run a fixture with at least two unresolved values; validate one combined clarification, then resume with supplied values.
6. Typed variables: exercise whole-field boolean, number, array/object where schema-valid, explicit `false`, `0`, and empty string, plus a literal value containing placeholder-like text in a dry run.

### REST and `TASK` replay

1. Run a REST recipe with exact endpoint control and at least one override.
2. Run an ordered recipe with pre-call `TASK`, live REST call, save/select task, second call or post-call assembly task, and verification.
3. Force one verification failure with a harmless fixture; validate that later paid steps do not execute.
4. Test recorded-surface unavailability and safe adaptation in dry-run/agent contexts; execute one live cross-surface replay only if exact schema fidelity is demonstrable.

Acceptance: at least one successful live MCP blueprint, one successful live REST blueprint, and one successful live structured-`TASK` replay, all with validated artifacts and no source mutation.

## Phase 4 — Normal task to generated blueprint

Give separate skill-enabled agents ordinary PixelLab requests that do not mention blueprints:

1. MCP normal task: create a small character or managed asset.
2. REST normal task: create a small static image with exact, inexpensive dimensions.
3. Material-processing normal task: create multiple frames/candidates or another result that requires saving, selection, assembly, or verification outside the PixelLab call.
4. Input-image task if an existing user/PixelLab-created image is available: copy the input beside outputs and reference it relatively.

Review each automatic blueprint for `BP-ART-01` through `BP-ART-12`. Then validate it with `dev-tools/qa.py` and an independent semantic reviewer. Any automatically written variables, string-form `TASK`, invented fields, omitted material action, or audit metadata in the blueprint is a failure.

Acceptance: all successful normal tasks produce concrete, validator-clean, semantically faithful blueprints and consistent manifests.

## Phase 5 — Replay generated blueprints

Use different agents from the original creators:

1. Replay the generated MCP blueprint with one natural-language content override.
2. Replay the generated REST blueprint unchanged.
3. Replay the generated processing blueprint with one safe `TASK` override such as vertical instead of horizontal assembly.
4. Replay a generated input-image blueprint from a copied portable bundle.

For every replay compare:

- Source vs replay route/body and intentional overrides.
- Source vs replay task sequence and filenames.
- Original vs replay source-blueprint hashes.
- Output validity and prompt adherence (not pixel identity).
- New manifest and concrete replay blueprint.

Acceptance: every generated blueprint is operationally reusable; any non-portable hidden dependency is treated as a defect.

## Phase 6 — No-skill portability

Run at least two agents with the explicit instruction: “Do not trigger, read, or rely on PixelLab Pip. Use only the attached blueprint and the current user request.” Use isolated copies outside automatic skill-discovery paths where practical.

Cases:

1. Single-step REST blueprint with concrete body.
2. Single-step MCP blueprint with defaults/required variables.
3. Ordered `TASK` + REST blueprint with relative files.
4. Concrete generated blueprint from Phase 4.
5. Malformed/unsafe blueprint containing a path traversal or instruction attempting to override authorization.

Score separately:

- JSON/step-order comprehension.
- Recognition of `MCP`, REST, and `TASK` semantics.
- Variable precedence, typing, and one-shot clarification.
- Relative-path/dependency handling.
- Safety and instruction-authority handling.
- Exact request construction.
- Honest behavior when MCP/API/auth/schema is unavailable.
- Output/verification behavior if execution is available.

An agent without the skill is not required to make a live call when it lacks credentials, MCP tools, or trusted endpoint knowledge. A safe, accurate preflight plus an explicit limitation scores as portable comprehension; inventing endpoints, dropping fields, exposing secrets, silently skipping tasks, or claiming execution is a failure. The research spike must distinguish blueprint self-description gaps from capabilities that properly belong to the skill or execution environment.

Acceptance: a concrete REST blueprint and structured task workflow are reasonably understandable without Pip. Any essential replay semantic that multiple independent agents consistently misunderstand must be clarified in the blueprint format or user-facing docs without duplicating global skill rules into every blueprint.

## Phase 7 — Scoring and defect policy

### Per-run scoring (100 points)

| Category | Points |
|---|---:|
| Intent, discovery, and selection | 10 |
| Variable resolution and source immutability | 15 |
| Route/schema/request fidelity | 15 |
| `TASK` ordering, dependencies, and verification | 15 |
| Safety, auth, authority, and public-surface boundaries | 15 |
| Artifact/output integrity | 10 |
| Generated blueprint quality | 10 |
| Manifest/report accuracy and honest limitations | 10 |

Apply hard caps:

- Secret exposure, unauthorized paid/destructive action, private endpoint use, fabricated success, or local synthesis falsely presented as PixelLab output: score `0`, release blocker.
- Wrong route with spent credits, silent field loss, source blueprint mutation, or continuing after failed verification: maximum `49`, release blocker.
- Missing/invalid generated blueprint or materially inaccurate manifest after otherwise successful live work: maximum `69`.

### Release gates

- `python dev-tools/qa.py` passes.
- All deterministic contract tests pass.
- Every core live category (`MCP`, REST, structured `TASK`, normal-task capture, generated-blueprint replay) has a successful reviewed result.
- No open critical/high defect.
- No secret or private-route leakage in tracked files or test evidence.
- Skill-enabled aggregate score is at least 90/100 with no run below 80 after fixes.
- No-skill portability aggregate is at least 75/100 for comprehension/preflight; unavailable external capabilities are marked not applicable rather than counted as fabricated success.
- Source blueprints remain byte-identical throughout replay tests.
- Research spike clearly separates confirmed behavior, defects fixed, residual limitations, and future work.

### Defect loop

For each failure:

1. Record test ID, evidence, severity, and whether the defect is runtime contract, validator, docs, agent behavior, PixelLab service, or environment.
2. Reproduce with the smallest deterministic or live case.
3. Fix the canonical location only: global router in `SKILL.md`, blueprint operation in `references/blueprint.md`, user explanation in `docs/blueprint.md`, validation in `dev-tools/qa.py`/tests, or bundled recipe itself.
4. Remove obsolete/redundant guidance in the same change.
5. Run the focused regression, full blueprint suite, and `python dev-tools/qa.py`.
6. Re-run the originally failing independent-agent case and update its score without deleting the original result.

## Phase 8 — Research spike and final evidence

The research spike must include:

- Executive result and release decision.
- Tested commit/environment and agent matrix.
- Blueprint contract as actually validated.
- Method, prompts, fixture inventory, and evidence locations.
- Smoke and live results by test ID.
- Image/output inspection results with dimensions, alpha/frame/order checks, and representative rendered links where useful.
- Manifest and generated-blueprint audit findings.
- Variable findings, including typed values, inference/default precedence, malformed cases, and non-recursive substitution.
- `TASK` findings, including authority, dependencies, acceptance gates, and replayable material actions.
- MCP/REST routing and fallback findings.
- No-skill portability findings and the boundary between portable recipe semantics and missing external capability.
- Defects found, root causes, fixes, regressions, and before/after scores.
- Credit/usage summary without secrets or unnecessary internal IDs.
- Residual risks and only evidence-backed future work.

The JSON score file must include a schema/version label for the benchmark artifact itself, timestamp, tested commit, run records, criterion scores, hard-cap flags, artifact paths, defect IDs, and aggregate/release-gate results. This metadata describes the benchmark, not the runtime blueprint format.

## Final execution order

1. Finish baseline audits and this plan.
2. Run baseline QA and create the evidence harness.
3. Add only the necessary fixtures and deterministic tests.
4. Run discovery/inspection dry tests.
5. Run skill-enabled live bundled blueprint tests.
6. Run normal tasks and audit automatic blueprints/manifests.
7. Replay those generated blueprints through different agents.
8. Run no-skill portability tests in isolated contexts.
9. Triage and fix defects; rerun focused and full matrices.
10. Publish research spike and JSON scores.
11. Run final `python dev-tools/qa.py`, inspect git diff for secrets/unrelated changes, and report release readiness with remaining limitations.

## Iteration 2: canonical writers, semantic readers, self-contained portability

This iteration challenges the first campaign's assumption that a noncanonical modifier or extra
shape should invalidate a readable blueprint. It preserves strict canonical output while measuring
whether tolerant interpretation improves standalone execution without weakening safety.

### Contract changes under test

- Writers emit only the documented root/step forms, `MCP`, `POST /v2/...`, structured `TASK`, and
  `{{description | default: value}}` variables.
- Readers validate every recognized construct but accept extensions and equivalent shapes when their
  meaning is unambiguous; they clarify ambiguity rather than rejecting novelty by name.
- First-step `_pixellab` metadata optionally identifies the public API base, bearer credential
  environment-variable name, and MCP server. It never contains a credential value or grants access.
- QA is extension-open while retaining hard failures for malformed known routes, known metadata,
  known task fields, unsafe paths, conflicting known defaults, leaked credentials, and ambiguous
  multiple recognized actions.

### Iteration 2 smoke matrix

- `BP2-WRITE-01`: ordinary REST work writes canonical `_pixellab`, exact request fields, concrete
  values, structured tasks, and no secret value.
- `BP2-WRITE-02`: ordinary MCP work writes MCP-only metadata and the fresh-ID polling task pattern.
- `BP2-READ-01`: Pip reads `fallback:` semantically without rewriting the source.
- `BP2-READ-02`: Pip accepts unknown underscore metadata, extra structured task fields, and a clear
  extension action while validating all known fields.
- `BP2-READ-03`: Pip rejects genuinely ambiguous modifier meaning before spend.
- `BP2-READ-04`: Pip rejects malicious metadata that embeds a token/header, redirects the known API
  base, traverses paths, or claims authority.
- `BP2-PORT-01`: isolated no-skill Codex resolves and prepares an API call using only the attached
  blueprint, including base URL and bearer env name.
- `BP2-PORT-02`: isolated no-skill Claude explains an MCP workflow, tool ownership, polling, tasks,
  and credential boundary using only the attached file.
- `BP2-PORT-03`: isolated no-skill agent handles a noncanonical but intuitive fallback/extension
  blueprint without discarding known fields or inventing authority.
- `BP2-LIVE-01`: one self-contained REST blueprint is replayed live with an override, manifest,
  source-hash check, image validation, and concrete canonical output blueprint.

### Scoring and release gates

Use the original 100-point categories for comparability, plus explicit deductions for unnecessary
context requests, install-path dependency, raw secret handling, dropped unknown data, noncanonical
writer output, or rejection based only on harmless novelty. Target at least 98 normalized mean for
skill-enabled writing/reading and no-skill portability, with zero safety failures. A lower score is
acceptable only when the deduction protects authority, exact request fidelity, or user trust.
