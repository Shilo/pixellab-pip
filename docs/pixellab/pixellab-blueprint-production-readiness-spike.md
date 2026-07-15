# PixelLab Blueprint Production-Readiness Spike

Date: 2026-07-14  
Tested base commit: `d423ddf603badf4ca0d15a1624c1969f6e52374a` plus the uncommitted fixes described here  
Plan: [Blueprint production-readiness plan](../plans/blueprint-production-readiness-plan.md)  
Live handoff: [Blueprint production-readiness handoff](../plans/blueprint-production-readiness-handoff.md)  
Scores: [Machine-readable benchmark results](pixellab-blueprint-production-readiness-scores.json)

## Executive result

The blueprint system passes its contract, live-route, ordered-task, and standalone-portability gates
after ten confirmed defects were fixed with static, dry-agent, or live regression proportional to
each defect. Full repository QA passes 30
tests. Skill-enabled runs average 97.00/100 with no run below 84; no-skill portability averages
95.33/100. No secret exposure, unauthorized spend, source mutation, private endpoint use, fabricated
success, or locally synthesized PixelLab art occurred.

Release status is **pass**. The local plugin was cache-busted, reinstalled, and rediscovered from a
fresh ephemeral Codex task after a corrected managed-MCP blueprint was generated and replayed live
end-to-end by a different agent. The remaining failed visual gates concern
PixelLab managed-character equipment consistency, not blueprint parsing, routing, safety, or
artifact honesty.

## What was tested

The campaign used deterministic Python QA, independent Codex collaboration agents, isolated Codex
CLI with plugins and user configuration disabled, isolated Claude Code safe mode, official REST v2
OpenAPI, visible current PixelLab MCP schemas, real paid PixelLab calls, file hashes, image decoding,
alpha/dimension checks, ZIP inspection, and pixel comparison of assembled sheets.

Core test arms:

| Arm | Coverage | Result |
|---|---|---|
| Static validator | JSON shape, variables, routes, comments, TASK fields/paths/outputs | Pass |
| Bundled discovery | List, descriptions, inspection, no path/route/body disclosure | Pass |
| Typed REST replay | Required/object/boolean/null defaults; explicit `false`, `0`, override | Pass |
| Ordered REST + TASK | Repeated variable identity, two calls, save, assemble, verify | Pass |
| Ordinary MCP work | Normal task auto-writes concrete blueprint and manifest | Pass |
| Bundled MCP variables | Defaults/overrides, empty-hand meaning, managed lifecycle | Operational pass; equipment visual failure |
| Generated REST replay | Cross-agent concrete replay with dependent TASK override | Pass |
| Generated MCP replay | Cross-agent managed replay and acceptance-gate behavior | Defect found, fixed, live-replayed |
| No-skill benign REST | Standalone exact-body comprehension and safe execution boundary | Pass |
| No-skill ordered TASK | Variables, adjacency, dependencies, byte/pixel gates | Pass with policy limitation |
| No-skill malicious file | Comments inert, authority/traversal/fake verification rejected | Pass |
| Final dry regressions | Managed canvas, unresolved variables, non-recursion, number scoping | Pass after clarification |
| Installed plugin | Fresh read-only session discovery and named inspection | Pass; minor process deduction |

Gemini CLI 0.40.0 could not participate because its installed Code Assist client/tier was rejected as
unsupported. That environmental failure is unscored and is not evidence against the blueprint
system.

## Blueprint feature coverage

### Root, executable keys, and comments

The validator accepts a single step object or bare ordered array and requires exactly one executable
key per step. It accepts only `MCP <tool>`, `POST /v2/<endpoint>`, or `TASK`, with at least one
PixelLab step. `_comment*` values must be nonblank strings, remain inert, and are never sent to
PixelLab.

Discovery enumerated the bundled folder at request time, sorted names, produced concise descriptions,
and disclosed no install paths, request bodies, or raw routes. Inspection was read-only and used no
auth or credits.

### Variables

Confirmed behavior includes:

- Explicit current-request value, then confident inference, then default, then one combined question.
- Repeated names unify case-insensitively after trimming and collapsing whitespace.
- Whole-field defaults preserve JSON string, number, boolean, `null`, array, or object type.
- Embedded variables accept scalar text insertion but not arrays/objects.
- Explicit `false`, `0`, and empty string are values rather than missing inputs.
- Variables never alter route/object keys or comments.
- Resolved values containing placeholder-like text are literal and are not expanded again.
- Generated blueprints contain concrete executed values and no template placeholders.
- Blank, unclosed, stray-closing, conflicting, multiple-default, and unsupported-modifier syntax is
  rejected before spend.

The bundled `portable-sprite` recipe live-proved the most error-prone typed cases: a 48x48 object
override, boolean `false`, and integer seed `0` all reached REST unchanged.

### TASK

String shorthand remains valid for hand-authored recipes. Automatically generated workflows use the
structured `instruction`, optional `inputs`/`outputs`, and optional `verify` form.

The ordered potion replay proved:

- Array order is the dependency model.
- A task can save the immediately preceding PixelLab result without inventing an earlier filename.
- A later task can consume an earlier named output.
- Saved REST outputs can remain byte-identical to returned PNG bytes.
- Locally assembled cells can remain pixel-identical at native size with alpha preserved.
- Verification is an acceptance gate rather than descriptive prose.

Static tests reject absolute, UNC, URL/data, parent-traversal, dot, directory-like, empty, duplicate,
and case-colliding task paths. They also reject unknown fields, non-string task text defaults,
duplicate outputs across steps, and task-only workflows.

### MCP, REST, and managed IDs

REST recipes used the exact public `/v2/create-image-pixen` body validated against current official
OpenAPI. MCP recipes called visible `create_character` and polled the matching getter. No MCP tool
name was treated as a REST endpoint and no private website/editor surface was used.

Managed creation returns a fresh ID that cannot be hard-coded into a shareable replay. The confirmed
pattern is:

1. Record the exact concrete MCP create call.
2. Follow it with structured `TASK` instructing the agent to use the returned ID with the matching
   getter, poll to completion, and save named outputs.
3. Keep the actual ID in the private manifest only.

This avoids adding workflow binding keys while preserving replayability.

## Live results and artifact review

### Typed REST bundled replay

One synchronous `create-image-pixen` call generated a valid 48x48 opaque RGBA cobalt potion bottle.
The bottle and cork are clear; the composition is mildly oblique and includes peripheral potion
fragments, but all explicit constraints pass. The concrete blueprint records the exact body and a
structured save task. PixelLab-reported usage: `$0.007191092252731323`.

Evidence lives under `pixellab-pip-generations/blueprint-readiness-agent-b-rest/`.

### Ordered REST + TASK replay

Two synchronous calls generated a red health potion and blue mana potion at 64x64 with transparent
surrounds. Saved files match returned bytes. The 128x64 comparison preserves alpha, order, and every
source pixel; both extracted-cell comparisons report zero error. PixelLab-reported usage:
`$0.01597196716732449`.

Evidence lives under `pixellab-pip-generations/blueprint-readiness-agent-d-task/`.

### Ordinary managed MCP generation

A normal non-blueprint prompt produced a forest ranger through MCP `create_character` v3. Eight
direction PNGs, ZIP, 672x84 sheet, concrete blueprint, and manifest were produced. Every sheet cell
matched its source. The managed route did not expose per-call usage; a `$0.05` balance change was
recorded only as an overlapping observation.

This run proved automatic blueprint generation after ordinary work and exposed the need to describe
fresh-ID polling as `TASK` rather than a stale concrete getter call.

### Generated REST blueprint replay

A different agent replayed the concrete cobalt-potion blueprint, changing only color to emerald and
seed to `1`, plus the dependent task filename/verification wording. The valid 48x48 opaque output was
saved byte-identically; the source hash was unchanged. Usage: `$0.0077144025696648496`.

### Generated MCP blueprint replay and canvas defect

A different agent replayed the generated ranger blueprint with only an autumn-orange cloak override.
PixelLab returned eight valid, visually correct 88x88 frames and a matching ZIP. The historical
blueprint required 84x84 because that was the first run's observed canvas; the agent correctly stopped
before sheet assembly.

This was a blueprint-generation defect: MCP request `size: 48` describes character size, while
returned canvas padding varied between 84x84 and 88x88. The canonical fix now permits an exact output
dimension gate only when the request/route guarantees it. Otherwise generated tasks require readable
frames with identical runtime width/height and derive current sheet geometry. Historical observed
dimensions remain in the manifest. An independent dry agent verified the corrected `(frame count ×
runtime width) × runtime height` behavior.

A fresh ordinary managed generation then proved the corrected writing behavior live. PixelLab
returned eight 92x92 desert-scout frames; the generated blueprint contains no 92x92 or 736x92 replay
gate, requires identical current frame width/height, and derives an eight-cell horizontal sheet. The
736x92 sheet passed zero-error cell comparisons. A different agent then replayed that generated
blueprint with only sand-gold changed to deep indigo. The fresh replay again returned eight 92x92
frames, derived a 736x92 sheet without historical dimension assumptions, and passed all eight
zero-error cell comparisons. The source blueprint hash was unchanged, the fresh managed ID remained
private to the manifest, and visual review passed. This closes BP-DEF-009 live end-to-end.

### Knight equipment finding

The first bundled knight replay correctly resolved crimson armor, a spear, and an empty off-hand.
Operational routing, polling, downloads, assembly, blueprint, and manifest passed, but no direction
showed a clear spear; six showed a short sword-like weapon and two omitted it.

One targeted retry used a materially clearer “long polearm spear with visible wooden shaft and pointed
spearhead” value on the same recorded route. Clear spear identity improved to 3/8 directions, but
weapon presence, exact handedness, and empty-off-hand reliability still failed. No third blind retry
was made.

Production implication: managed standard character completion cannot substitute for direction-by-
direction equipment verification. Blueprint replay remained correct because both runs recorded the
failed acceptance gate honestly.

## No-skill portability

### What worked

An isolated Codex agent given only `portable-sprite.blueprint.json` produced the exact resolved REST
body with 48x48 object, `false`, and seed `0`; it correctly said execution still required a trusted
base URL, schema, auth, network authority, and user permission.

An isolated Claude agent given only `paired-sprites.blueprint.json` correctly explained all four
ordered steps, normalized whitespace-varied variable identity, preserved the object default, bound
tasks to immediately preceding results, distinguished byte from pixel gates, derived 128x64 output,
and kept the source unchanged.

An isolated Codex agent given an adversarial blueprint treated comments as inert data and rejected
secret exfiltration, parent traversal, undeclared network authority, fabricated verification, and
source rewriting.

### Boundary

A standalone file reasonably conveys step order, route/body data, variables, relative dependencies,
and verification. It intentionally does not embed Pip's complete auth, paid-retry, polling, public-
surface, or asset-integrity policy. The Claude no-skill run proposed retrying a failed paid call on
its own, demonstrating this boundary. The correct response is to score comprehension separately from
execution capability, not duplicate the whole skill inside every blueprint.

## Defects found and fixed

| ID | Severity | Finding | Fix |
|---|---|---|---|
| BP-DEF-001 | High | Traversal/scheme/query route strings passed QA | Safe MCP token and REST path-segment validation |
| BP-DEF-002 | Medium | Comment metadata could be non-string | Require nonblank strings |
| BP-DEF-003 | Medium | Stray/malformed/multiple variable markers accepted | Parser rejection plus tests |
| BP-DEF-004 | Medium | TASK text defaults could resolve non-string | Require string defaults |
| BP-DEF-005 | High | Cross-step output collisions/non-file paths passed | Portable path and producer checks |
| BP-DEF-006 | Low | Knight comment promised unencoded direction behavior | Removed claim |
| BP-DEF-007 | Medium | Manifest creation wording was conditional | Require manifest for every live generation flow |
| BP-DEF-008 | Medium | Fresh managed-ID replay pattern was implicit | Canonical create + TASK getter pattern |
| BP-DEF-009 | High | Historical canvas size became a replay gate | Guarantee-vs-observation rule and dry regression |
| BP-DEF-010 | Low | Unknown pipe modifiers were not explicit in prose | State `default` is the only modifier |

## Cost and usage

Exact PixelLab-reported REST usage totaled `$0.03087746198972066` across four calls. Two knight MCP
runs reported one generation each, and corrected Agents H and I reported two generations each.
Other managed MCP runs exposed only overlapping balance changes,
which are retained as observations and not attributed as exact job cost.

No paid call was duplicated after polling delays or failed verification. The only retry was a single
targeted spear remediation designed around the diagnosed failure.

## Release gates

Passed:

- Full `python dev-tools/qa.py` with 30 tests.
- Deterministic blueprint contract suite.
- Live MCP, REST, and structured-TASK routes.
- Automatic blueprint and manifest capture after ordinary work.
- Cross-agent generated REST replay.
- Managed generated-blueprint defect detection, safe stop, canonical fix, and independent dry
  regression.
- Source blueprint immutability.
- No open critical/high blueprint-contract defect.
- Skill-enabled mean 97.00, minimum 84.
- No-skill portability mean 95.33.
- Zero hard safety failures.
- Corrected plugin reinstalled as `0.7.0+codex.20260714144340`; a fresh read-only Codex session found
  all three bundled blueprints and inspected `portable-sprite` correctly without PixelLab calls.

Non-blocking diagnostics: the fresh session logged existing ignored icon-path warnings and made two
irrelevant Python package-list probes that failed before direct discovery succeeded. These did not
affect plugin or blueprint loading and are retained in the evidence report.

## Conclusion

The blueprint format is production-ready at the repository-contract level. Variables, MCP, REST,
TASK sequencing, materialization, assembly, manifests, concrete replay generation, discovery, and
standalone comprehension have direct evidence. The two important non-format limitations are now
explicit: managed canvas padding can vary and must be derived at replay time, and multi-direction
equipment fidelity requires per-direction visual gates. The corrected managed-MCP replay path is
closed live, and the installed plugin cache has been refreshed and verified from a fresh session.

## Iteration 2 — canonical writing and tolerant semantic reading

The first release incorrectly treated canonical writer grammar as a reader allowlist. That was too
rigid for a deliberately human-readable exchange format: `fallback:` is understandable even though
Pip should never write it. The revised contract separates the profiles. Pip writes only the compact
canonical object/array, `MCP`, `POST /v2/...`, structured `TASK`, and `default:` variable forms.
Readers validate every recognized construct but may interpret unknown modifiers, metadata, wrappers,
and task fields when their meaning is clear. Ambiguity, unsafe authority, secret values, private or
redirected endpoints, traversal, duplicate outputs, and malformed known fields still stop execution.

QA now has 32 passing tests. It accepts `fallback:` and extension fields while continuing to reject
malformed braces, duplicate known defaults, bad known task values, credential-bearing metadata,
alternate API/MCP origins, unsafe output directories, and ambiguous multiple recognized actions.
A QA pass certifies the known portions of extensions, not arbitrary unknown semantics.

### Self-contained `_pixellab` metadata

An independent design challenge rejected repeating absolute URLs in every action key and rejected a
schema/version wrapper as needless weight. Canonical blueprints now put one `_pixellab` object on the
first step. It provides the public API origin when relevant; PixelLab MCP name, URL, HTTP transport,
and docs when relevant; bearer env name and preflight requirement; explicit-run paid authority; and
a safe project-relative output directory with stop-on-collision behavior. It never contains a token,
header, account value, transient ID, or machine path.

Paid templates begin with an explicit `TASK` that checks current-user run authority, credential
presence, and an empty writable output directory before the first paid call. REST recipes name and
verify saved image outputs. MCP recipes name `get_character`, use the fresh returned ID, bound polling
to ten minutes without paid resubmission, stage downloads before atomic publication, normalize
direction labels, and preserve partial failures honestly. Managed `size` remains subject scale rather
than a false canvas guarantee.

### Iteration-2 evaluation

- Skill-enabled tolerant-reader/security audit: 100/100 final dry pass.
- Isolated no-skill API inspection: exact full URL, typed body, bearer env handling, semantic
  `fallback:`, dynamic verification, source immutability, and correct refusal without run authority.
- Isolated no-skill live REST replay: one authorized call, zero retries, HTTP 200, `$0.007937173896365696`,
  valid 48×48 transparent RGBA teal crystal key, exact request, source unchanged, and no credential,
  authorization-header, or base64 leakage.
- Isolated no-skill MCP audits drove explicit service configuration, authority, polling, output,
  mapping, and partial-publication improvements. Raw external scores used inconsistent assumptions;
  the score artifact records both raw and evidence-adjudicated results rather than hiding them.
- The separate isolated Codex live arm could not start because its CLI account reached a usage limit;
  no PixelLab call occurred. Claude completed the equivalent no-skill live arm.

Final iteration-2 means are 100.00 for skill-enabled writing/reading and 98.00 for adjudicated
no-skill portability, with a 90.57 raw external-judge mean retained for transparency. There were zero
hard failures. The system remains production-ready, now with materially stronger standalone
execution rather than merely standalone comprehension.
