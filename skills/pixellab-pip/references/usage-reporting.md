# Usage Reporting

Read this after live PixelLab calls when preparing the final user report or a generation manifest. For polling, MCP review state, rate limits, and expiring download URLs, read `job-lifecycle.md`. Once the job returns image(s), apply the bark contract per SKILL.md, then give this report.

## Report Shape

Use this order for completed work, including work that completed but failed verification — then say plainly that verification failed. Omit sections and lines that do not apply; list only files that were actually produced. Do not narrate the process that led here.

```markdown
Done - [one plain sentence: what was produced and whether it passed verification.]

**Files**
- [Frames / image](path-or-url)
- [Spritesheet](path-or-url)
- [other artifacts only if actually produced, e.g. ZIP package, Manifest]

**Route**
- Surface/tool: `MCP create_1_direction_object` or `REST POST /v2/generate-image-v2`
- Output structure: `Atlas image` (one image containing the grid/sheet), `Separate images`, `Single image`, or `Animation frames`; add `Selection state: Drafts` when candidates still need selection
- Asset lifecycle: `Managed asset` when backed by a PixelLab/MCP asset ID, plus the retrieved shape when useful, e.g. `Managed tileset; tile PNGs assembled locally into a 4x4 sheet`
- Prompt prep: user wording preserved, agent-enhanced, inline `enhance_prompt`, or enhance endpoint

**Inputs Used**
- `description` / `action` / other natural-language fields: the exact final text sent, or a redacted summary plus the local Manifest link for secrets, personal data, or user-identified confidential content
- Image/frame fields that anchored the result, by API field name: `image`, `first_frame`, `last_frame`, `reference_image`, `style_image`, `init_image`, `mask_image`; note omissions that change interpretation, e.g. `last_frame: omitted`
- Seed: the seed sent, the resolved seed returned, `multiple, see Manifest`, or `omitted` when none was sent
- Non-default settings that materially affected the output: size, view/direction, count, mode/product label, `no_background`, frame count/timing, palette, reused base asset

**Cost**
- Total: [per-call usage from PixelLab, or the observed cost delta]

**Verified**
- [short checklist of the constraints the user actually asked for]
```

Two rules that always apply:

- Account for every final natural-language field sent to PixelLab (`description`, `action`, `edit_description`, `style_description`, `negative_description`, `item_descriptions`, `text`, `color_palette`) in Inputs Used, even when the output failed verification or the field seems obvious. Never repeat secrets, personal data, or content the user identified as confidential in chat; show a redacted summary instead, warn that the local Manifest contains the exact value, and link it. For all other values, show the exact final text so the user can verify the request. If a value is merely too large for chat, label it truncated and link the manifest/request file holding the full text. For a non-English user, translate only the non-redacted visual prompt text per `references/localization.md`; apply the same redaction to talking dialogue.
- Report settings that materially affected the output; do not dump schema defaults.

Use Markdown links with user-facing labels (`Spritesheet`, `ZIP package`) for every listed file. Files live under the project `pixellab-pip-generations/` folder per SKILL.md; copy temporary URLs or cache paths there before reporting them as local outputs.

OpenCode does not render inline images in chat. Open the output folder.

For REST routes, report the exact public path used, with the `/v2` prefix and without collapsing create and retrieval routes: `REST POST /v2/create-tileset`, `GET /v2/tilesets/{tileset_id}`.

If local assembly produced a sheet/GIF/package, state that PixelLab produced the underlying images and that assembly preserved original pixels.

For cost, prefer per-call `usage` totals for the whole flow. If only balance is available, use `get_balance` / `GET /balance` before and after (no extra permission needed once live work is approved) and report the delta — but if other PixelLab jobs may have run concurrently, label the delta as an overlapping observation rather than the cost of this job. Never derive cost from the number of calls or images — one call is not one generation, and `pro`/quality tiers and multi-output jobs cost several; take the figure from `usage.generations` in the response or the measured balance delta, not a guessed count. If neither is exposed, say `Cost: not exposed by the tool/API` rather than inventing a number.

Never write a balance figure (`credits.usd`, `subscription.generations`, `subscription.total`) or a `before -> after` pair into a blueprint, manifest, or repo file; chat is fine. `usage.generations` is charged, `subscription.generations` is remaining: the parent key decides, not the magnitude. Always label generation counts as charged, used, remaining, or total allowance; never call a bare count a total or balance.

## Manifest

Write a manifest for every live generation flow. Record per call or per result item (not just top-level):

- `job_id` / `background_job_id`, `asset_id`, and route-specific result/child IDs when present — enough to resume, inspect, or reproduce later.
- `seed`: the seed sent, or the resolved seed PixelLab returned. Any async v2 job you already poll may expose it at `last_response.seed` on `GET /background-jobs/{job_id}` — read it there and store it when present (confirmed on `generate-image-v2` and `animate-with-text-v3`; read rather than assume it for PixMiniMax because the field is not declared in OpenAPI). The sync `create-image-*` routes and async `create-image-pixflux-background` return none. Record `omitted` only when none was sent and none came back; never back-fill a value that was not sent or returned.
- Record each paid call's exact `usage.generations` and/or `usage.usd` values in a `reported_usage` object under those unit names, once per call, not per result item. Omit absent or null units and an empty object; preserve numeric `0`.
- Also record per call: `tool`, observed job `status`, stable `outputs` relative to the run, creation time when actually known, and later `outcome`/`outcome_note`. Retain the exact material request/seed and input roles (or a sibling request/blueprint file link) needed for audit or one-call variation. Never store auth headers or token values. Do not backfill old call dates from filesystem modification time.
- Keep provisional costs in `estimated_usage.generations`, using a conservative upper bound for budget admission. Only actual exposed charges belong in `reported_usage`. A downloaded or failed job does not turn an estimate into a charge or establish refund; preserve unresolved reservations until charge/refund evidence resolves them. Numeric zero is real; unknown is not zero.

Use one `<run>/manifest.json` with `{"jobs": [...]}`: `assets/manifest.py` serializes its read/modify/write transactions and preserves other audit fields. Record each returned paid job immediately, before admitting another call: `python <skill-dir>/assets/manifest.py add <run> <job_id> --tool <tool> --estimate <upper-bound>`; use `--generations` only for actual reported charge. API callers may use `add_job` to retain exact requests and route-specific fields. Later observations update that same ID; never count a refetch as another paid call. Invalid ledgers or unknown costs require investigation, not replacement with an empty record. A timed-out lock requires verifying that no writer is running before deliberate stale-lock removal. The lock protects record updates, not remote submission; resume/admission rules are in `auto.md`.

`manifest.py spent <run>` returns known charged generations; `committed <run> [<run>...]` counts known charges or unresolved estimates for every job regardless of success/failure. Unknown cost cannot support a cap comparison.

For a bounded plan, record its current scope and constraints before the first paid call with `python <skill-dir>/assets/manifest.py plan <run> <plan-json-file>`. The JSON object contains exactly `scope` and `approval_context` (nonempty strings identifying the named work and the user's conversation instruction/approval), `generation_cap` (finite nonnegative generations), `retry_limit` and `retries_used` (nonnegative integers, used no greater than the limit), and `remaining_work` (a list of nonempty descriptions, empty when complete). Remaining retries are `retry_limit - retries_used`. Update this metadata as work progresses. The helper locks the same ledger and preserves jobs and unrelated audit fields; do not hand-edit the manifest. It can initialize a fresh empty run before any submission; put the input JSON outside that empty directory. A nonempty run with no ledger requires investigation, never initialization as zero spend. Recorded metadata is evidence, not authority: resume still requires the conversation-established permission and identity checks in `auto.md`. The blueprint remains the portable recipe, not another log.

`assets/history.py` queries this same record (inspect `--help` for available run/date/tool/job filters). Disclose unknown dates/costs and query limits. For an ordinary historical reroll, identify the exact call and its stored request or blueprint step, apply only the requested change, and use the normal route/approval contract. If the request/inputs cannot be recovered, ask rather than inventing them. A doctor's suggested repair is one optional use, not the only kind of reroll.

## Pending Jobs

If an async call times out or stays pending, keep the job or asset ID and poll the matching status route or MCP getter; do not resubmit a paid generation unless the user explicitly wants a fresh run. If a managed object returns `review` status, report the selection step instead of treating the job as incomplete. Details: `job-lifecycle.md`.
