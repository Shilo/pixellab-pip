---
name: update-pixellab-docs
description: Refresh the local PixelLab public-documentation cache, inspect every artifact from the refresh, determine the complete PixelLab Pip impact, update affected Skill and project documentation, validate the result, and complete a mandatory independent adversarial subagent review. Use when synchronizing PixelLab Pip with current public MCP, REST v2, SDK, setup, schema, parameter, limit, lifecycle, or routing changes.
---

# Update PixelLab Pip From Public Documentation

Work from the repository root. Own the investigation and implementation yourself. Use a subagent only for the mandatory post-implementation review described below.

Do not commit, push, publish, or alter unrelated work unless the user explicitly requests it.

## 1. Load The Repository Contract

Read these files completely before refreshing:

- `AGENTS.md`
- `docs/README.md`
- `docs/developer.md`
- `docs/pixellab/pixellab-doc-watch-cache.md`
- `skills/pixellab-pip/SKILL.md`

Run `git status --short`. Preserve existing user changes and distinguish them from your edits throughout the task. If existing changes overlap required files, inspect and integrate with them; never discard them.

Apply `AGENTS.md` throughout, especially its KISS/YAGNI, canonical-placement, progressive-discovery, public/private boundary, secret-safety, paid-credit, output-integrity, and personal-data rules.

## 2. Refresh Before Drawing Conclusions

Run each command separately so its exit code and output remain visible:

```powershell
.\dev-tools\manage-pixellab-doc-cache.ps1 -Action status
.\dev-tools\manage-pixellab-doc-cache.ps1 -Action refresh
.\dev-tools\manage-pixellab-doc-cache.ps1 -Action status
```

The initial status is context only. Never conclude that nothing changed until a new refresh completes and the post-refresh status is inspected.

Interpret `refresh` exit codes rather than treating every nonzero exit as a command failure:

- `0`: complete refresh with no normalized skill-relevant drift, or baseline initialization.
- `1`: refresh incomplete because at least one source failed and no normalized drift was detected.
- `2`: complete refresh with normalized skill-relevant drift.
- `3`: normalized drift was detected, but at least one source failed.

For `status`, `0` means the configured `latest/raw` and `latest/normalized` files exist; it does not prove that the last refresh succeeded. `1` means the manifest or configured latest files are missing. Always inspect `manifest.last_refresh_had_failures` and the report independently of the status exit code.

Do not rerun `init`; `refresh` initializes automatically. Do not delete or reset the cache because that destroys the comparison baseline.

## 3. Inspect Every Artifact From The New Refresh

After the post-refresh status, read all of the following completely:

1. `.local/pixellab-doc-watch/manifest.json`.
2. `.local/pixellab-doc-watch/sources.json`; reconcile its source IDs, URLs, raw filenames, and count with the manifest, report, and changes JSON.
3. The report named by `manifest.last_report`.
4. The matching `.local/pixellab-doc-watch/changes/<timestamp>.json`.
5. For every source whose status is not `unchanged`, its complete current raw and normalized content from the matching snapshot and its complete prior content under the snapshot's `previous/` directory when present.
6. For a failed source, its error entry plus the retained `latest/raw` and `latest/normalized` files, while keeping clear that those retained files are not a successful current refresh.

Derive `<timestamp>` from the latest report filename; do not guess that the newest filesystem entry belongs to this run. Confirm that the report timestamp, changes timestamp, and manifest refresh metadata agree.

Inspect raw before/after content even when the report labels a source only `raw_changed` or `metadata_changed`. Do not update tracked files for byte churn or metadata alone unless that inspection reveals a meaningful public-contract change.

Treat a source with `fetch_failed` or `parse_failed` as unverified. Never add, remove, or revise a claim based on that source. If failed coverage prevents a reliable update, stop and report the exact blocker. Do not fill gaps from memory, search-engine snippets, website internals, or private endpoints.

When exact REST behavior matters, use the refreshed raw OpenAPI document rather than a normalized summary. Use the public MCP docs cache as the MCP inventory authority. Apply every source-precedence and public-surface rule in `docs/pixellab/pixellab-doc-watch-cache.md`.

If the refresh initializes a missing baseline, do not claim that those sources changed over time because no before/after conclusion is possible. Still compare their successfully fetched current public contracts against every semantically related tracked claim and correct any evidence-proven contradiction. Otherwise a fresh cache could never repair an already-stale repository.

## 4. Build A Complete Impact Map

From the report, changes JSON, and raw diffs, list every affected public-contract element before editing:

- MCP tools, names, inputs, outputs, availability, retention, and lifecycle behavior.
- REST v2 paths, methods, request and response schemas, required fields, enums, defaults, limits, auth, polling, and result shapes.
- MCP-to-REST parity and intentional surface-only capabilities.
- SDK/setup links or behavior, terminology, model/mode labels, cost implications, and public-vs-private boundaries.
- Routing decisions, clarification rules, examples, safety gates, and verification steps affected by those facts.

Read `docs/pixellab/pixellab-mcp-vs-rest-route-parity.md` first for any MCP or REST inventory change. Reconcile the authoritative parity mapping before editing downstream descriptions.

Do not rely only on the report's suggested file list. For every changed or retired route, tool, field, schema, limit, and term:

1. Search all tracked project files with `rg` using exact names plus meaningful old/new variants.
2. Inspect every relevant match in context.
3. Follow pointers to any reference or document that owns the affected rule.
4. Check tests, helper scripts, manifests, examples, blueprints, setup guidance, and packaging metadata when the changed contract could affect them.
5. Record each related file as `update`, `verified unaffected`, or `intentionally unchanged`, with evidence.

Review the full project-file inventory with `git ls-files` so related files are not missed merely because their names were absent from a canned checklist. “Review the entire project” means inspect every file with a plausible semantic dependency on the changed facts, not mechanically edit or reread unrelated assets.

Resolve contradictions using current official public documentation and repository canonical-placement rules. Do not preserve stale behavior for backward compatibility unless the current repository requirement explicitly requires it.

If the completed refresh contains no meaningful public-contract drift, do not manufacture edits. Still finish any initialized-source current-state reconciliation, artifact inspection, impact searches, independent subagent review, and final evidence report.

## 5. Implement The Smallest Complete Update

Update every affected file and no unaffected file.

- Put global task detection, guardrails, surface selection, and direct reference pointers in `skills/pixellab-pip/SKILL.md`.
- Put detailed operational routing, schema mappings, safety constraints, and verification in the single appropriate file under `skills/pixellab-pip/references/`.
- Put human/developer research, evidence, and background in `docs/`.
- Keep MCP-vs-REST inventory canonical in `docs/pixellab/pixellab-mcp-vs-rest-route-parity.md`; make downstream files agree without duplicating its full inventory.
- Search for an existing canonical rule before adding a section, example, file, schema mapping, or helper. Replace and remove obsolete guidance in the same change.
- Preserve protections for routing accuracy, public endpoint boundaries, secrets, paid credits, output integrity, and user trust.
- Never copy local cache paths containing machine-specific data, secrets, tokens, cookies, private account data, or undocumented website internals into tracked files.

Do not perform live paid PixelLab calls merely to update documentation. If public documentation is insufficient to prove behavior that requires a paid experiment, document the unresolved question rather than presenting a guess as fact.

## 6. Validate Your Implementation

Before requesting review:

1. Search the entire tracked repository for every stale old name, removed route/tool, changed field, contradicted limit, and obsolete example identified in the impact map.
2. Inspect `git diff -- <files-you-changed>` completely. Because ordinary `git diff` omits untracked files, also read every task-created untracked file completely or produce an explicit no-index diff for it. Run `git diff --no-index --check -- /dev/null <new-file>` for each such file and inspect its output; exit `1` is expected when content differs, but whitespace-error output is not. Run the file's applicable syntax or format validation too.
3. Run:

```powershell
python dev-tools/qa.py
git diff --check
```

Run any narrower tests or syntax checks implicated by the files changed. If the watcher or its documentation contract changed, also run:

```powershell
python -m py_compile dev-tools/pixellab-doc-watch.py
```

Fix failures caused by your work. Clearly separate unrelated pre-existing failures.

## 7. Require An Independent Adversarial Subagent Review

After implementation or a no-edit determination and initial validation, start a fresh subagent with read-only review ownership. The subagent is mandatory for every completed synchronization, including a no-drift or no-edit conclusion. If subagent tooling is unavailable, stop and tell the user the required review could not be completed; do not claim the update is finished. This stricter requirement supersedes the self-review fallback in `docs/pixellab/pixellab-doc-watch-cache.md` for runs using this skill.

Give the reviewer the repository root and require it to read:

- `AGENTS.md` and this skill.
- The refresh `sources.json`, manifest, complete report, complete changes JSON, and all changed-source before/after artifacts.
- The primary agent's impact map or summary.
- The pre-task `git status`, a task-scoped diff, the complete contents or no-index diffs of task-created untracked files, and every project file plausibly affected by the upstream changes. Identify unrelated user changes and instruct the reviewer not to disposition them; include overlapping context only when needed to assess your work safely.

Do not give the reviewer your conclusions about likely mistakes. Do not ask it to confirm correctness. Use a challenge prompt with this substance:

```text
Act as an independent, adversarial, read-only reviewer. Find omissions and defects; do not edit files. Reconstruct the upstream change from the refresh artifacts and inspect the complete diff plus all semantically related project files. Challenge factual accuracy, exact MCP/REST parity, fields and schemas, routing consequences, source precedence, failed-source handling, public/private boundaries, stale names, overclaims, underclaims, contradictions, duplicated guidance, canonical placement, SKILL.md bloat, missing removals, examples, tests, and regressions. For every finding, provide severity, exact file/location, official-cache evidence, repository evidence, consequence, and the smallest valid correction. Also list the searches and related files checked. Explicitly state when no actionable defect remains.
```

The reviewer must not modify files, run paid calls, commit, push, or use private/undocumented surfaces as evidence.

## 8. Challenge The Reviewer Before Editing Again

Treat every reviewer finding as an untrusted hypothesis. For each one:

1. Restate the precise claim.
2. Recheck it against the refreshed raw official source, report/changes artifact, and canonical repository file.
3. Search for counterevidence and downstream consequences the reviewer may have missed.
4. Classify it as `accept`, `accept with narrower correction`, `reject`, or `cannot verify`.
5. Record the evidence and reasoning for that classification.

Reject preference-only rewrites, speculative future-proofing, unsupported claims, duplicated rules, compatibility machinery without a current requirement, and changes based on failed sources. Do not defer to reviewer confidence or severity labels.

Implement only accepted findings, using the smallest complete correction. Then repeat all relevant repository searches, inspect the complete final diff, and rerun `python dev-tools/qa.py`, `git diff --check`, and any implicated checks. If a correction materially changes the contract, ask the same reviewer to re-check that correction or start another fresh read-only reviewer.

## 9. Report Completion

Report:

1. Refresh completeness, exit interpretation, and the exact official sources that meaningfully changed or failed.
2. The upstream public-contract changes, including report-only signals that were intentionally not applied.
3. Every related project file reviewed and whether it was updated, verified unaffected, or intentionally unchanged.
4. Files changed and why each change belongs in that canonical location.
5. Validation commands and results.
6. Every reviewer finding, your evidence-based disposition, and any correction made.
7. Remaining uncertainties or blockers.

Do not say PixelLab Pip is current unless the refresh was sufficiently complete, all meaningful artifacts and impacts were reviewed, the adversarial cycle finished, and final validation passed.
