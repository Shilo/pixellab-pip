# Usage Reporting

Read this after live PixelLab calls when preparing the final user report or a generation manifest. For polling, MCP review state, rate limits, and expiring download URLs, read `job-lifecycle.md`. Once the job returns image(s), apply the bark contract per SKILL.md, then give this report.

## Report Shape

Lead with the result and verification status; a completed job that fails the brief is a failed candidate, not a finished asset. List the usable requested files first with Markdown links and a faithful inline preview when supported. Mark alternatives as awaiting selection under `reviewable-candidates.md`; do not present a candidate contact sheet as a selected final icon. Keep raw outputs, copied inputs and audit files clearly separate from the usable deliverables.

For a small run, use a compact report rather than empty or repeated sections:

```markdown
[What was produced, whether the requested constraints passed, and anything still awaiting choice.]

- [Requested asset](path) · [Preview](path)
- Route: [surface/tool or exact REST method/path]; [single image, atlas, separate images or frames; managed when applicable].
- Inputs: [material changes, reference roles and prompt preparation]; [Manifest](path) for exact requests and seeds.
- Cost: [actual charged usage, qualified observation, or not exposed].
- Verified: [the user's constraints; failures or unverified limits].
```

Expand only for multiple assets, material settings or unresolved results. Account for every final natural-language field, material setting and image/frame input in the linked manifest/request record, including omitted anchors when that affects interpretation. Show newly changed prompt text in chat; previously approved unchanged values may be linked instead of repeated. Preserve exact field names and seed sent/resolved/omitted; never dump schema defaults or raw base64. For non-English reporting follow `localization.md`. Redact personal/confidential text from chat, warn when the local record contains it, and never store credentials.

Use the project output location required by SKILL.md. OpenCode does not render inline images; open the output folder. Report exact REST public methods and `/v2` paths, distinguishing creation from retrieval. If local crop/split/assembly made the usable file, say so and preserve PixelLab provenance.

Prefer actual per-call `usage` totals for the entire flow. If only balance is available, read it before/after; overlapping account activity makes that delta an observation, not an attributable charge. Never derive cost from call/image counts or turn a provisional quote into observed usage. If neither is exposed, say `Cost: not exposed by the tool/API`.

Never write account balances (`credits.usd`, `subscription.generations`, `subscription.total`) or before/after balances into a blueprint, manifest or repo file; chat is fine. `usage.generations` is charged and `subscription.generations` is remaining: label units and meaning explicitly. Audit usage may include numeric zero; unknown is not zero.

## Manifest

Write a manifest for every live generation flow. Record per call or per result item (not just top-level):

- `job_id` / `background_job_id`, `asset_id`, and route-specific result/child IDs when present — enough to resume, inspect, or reproduce later.
- `seed`: the seed sent, or the resolved seed PixelLab returned. Any async v2 job you already poll may expose it at `last_response.seed` on `GET /background-jobs/{job_id}` — read it there and store it when present (confirmed on `generate-image-v2` and `animate-with-text-v3`; read rather than assume it for PixMiniMax because the field is not declared in OpenAPI). The sync `create-image-*` routes and async `create-image-pixflux-background` return none. Record `omitted` only when none was sent and none came back; never back-fill a value that was not sent or returned.
- Record each paid call's exact `usage.generations` and/or `usage.usd` values in a `reported_usage` object under those unit names, once per call, not per result item. Omit absent or null units and an empty object; preserve numeric `0`.
- Also record per call: `tool`, observed job `status`, stable `outputs` relative to the run, creation time when actually known, and later `outcome`/`outcome_note`. Retain the exact material request/seed and input roles (or a sibling request/blueprint file link) needed for audit or one-call variation. Never store auth headers or token values. Do not backfill old call dates from filesystem modification time.
- Keep provisional costs in `estimated_usage.generations`, using a conservative upper bound for budget admission. Only actual exposed charges belong in `reported_usage`. A downloaded or failed job does not turn an estimate into a charge; preserve unresolved reservations until charge/refund evidence resolves them. Numeric zero is real; unknown is not zero.

Use one `<run>/manifest.json` with `{"jobs": [...]}`: `assets/manifest.py` serializes its read/modify/write transactions and preserves other audit fields. Record each returned paid job immediately, before admitting another call: `python <skill-dir>/assets/manifest.py add <run> <job_id> --tool <tool> --estimate <upper-bound>`; use `--generations` only for actual reported charge. API callers may use `add_job` to retain exact requests and route-specific fields. Later observations update that same ID; never count a refetch as another paid call. Invalid ledgers or unknown costs require investigation, not replacement with an empty record. An older Pip manifest without a `jobs` list is not a ledger: keep it and record new calls in a fresh run folder. A timed-out lock requires verifying that no writer is running before deliberate stale-lock removal. The lock protects record updates, not remote submission; resume/admission rules are in `auto.md`.

`manifest.py spent <run>` returns known charged generations; `spent <run> --unit usd` reports charged dollars separately. Each total is unknown if any included call lacks that unit; never convert dollars to generations. `committed <run> [<run>...]` counts known generation charges or unresolved generation estimates for every job regardless of success/failure. History and the review panel display reported dollars separately under the same unknown-unit rule.

For a bounded plan, record its current scope and constraints before the first paid call with `python <skill-dir>/assets/manifest.py plan <run> -`, piping the JSON on stdin; a plan file, if used, needs a name unique to this run, since parallel agents sharing a fixed name such as `plan.json` record each other's plans. The JSON object contains exactly `scope` and `approval_context` (nonempty strings identifying the named work and the user's conversation instruction/approval), `generation_cap` (finite nonnegative generations), `retry_limit` and `retries_used` (nonnegative integers, used no greater than the limit), and `remaining_work` (a list of nonempty descriptions, empty when complete). Remaining retries are `retry_limit - retries_used`. Update this metadata as work progresses. The helper locks the same ledger and preserves jobs and unrelated audit fields; do not hand-edit the manifest. It can initialize a fresh empty run before any submission; put the input JSON outside that empty directory. A nonempty run with no ledger requires investigation, never initialization as zero spend. Recorded metadata is evidence, not authority: resume still requires the conversation-established permission and identity checks in `auto.md`. The blueprint remains the portable recipe, not another log.

`assets/history.py` queries this same record (inspect `--help` for available run/date/tool/job filters). Disclose unknown dates/costs and query limits. For an ordinary historical reroll, identify the exact call and its stored request or blueprint step, apply only the requested change, and use the normal route/approval contract. If the request/inputs cannot be recovered, ask rather than inventing them. A doctor's suggested repair is one optional use, not the only kind of reroll.

## Pending Jobs

If an async call times out or stays pending, keep the job or asset ID and poll the matching status route or MCP getter; do not resubmit a paid generation unless the user explicitly wants a fresh run. If a managed object returns `review` status, report the selection step instead of treating the job as incomplete. Details: `job-lifecycle.md`.
