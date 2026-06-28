# PixelLab Documentation Watch Cache

Last reviewed: 2026-06-28.

Use this workflow when PixelLab's public REST, MCP, SDK, or setup documentation might have changed and PixelLab Pip needs a repeatable local record before updating the Agent Skill.

The tracked repository contains only the watcher script and these instructions. Downloaded upstream documentation, snapshots, hashes, and reports stay local in `.local/pixellab-doc-watch/`, which is ignored by Git.

## What It Tracks

Default sources:

- `https://api.pixellab.ai/v2/openapi.json`
- `https://api.pixellab.ai/v2/llms.txt`
- `https://api.pixellab.ai/v2/docs`
- `https://api.pixellab.ai/v2/redoc`
- `https://api.pixellab.ai/mcp/docs`
- `https://www.pixellab.ai/docs`
- `https://www.pixellab.ai/mcp`

The watcher stores raw files and normalized summaries. The normalized summaries are designed to surface skill-relevant drift such as added REST paths, added MCP tools, schema-name changes, prompt-limit fields, and official links. Raw source hash changes are recorded as a separate review signal.

For REST v2 endpoint truth, treat `https://api.pixellab.ai/v2/openapi.json` as primary. The interactive docs at `https://api.pixellab.ai/v2/docs` and ReDoc at `https://api.pixellab.ai/v2/redoc` are documentation shells that currently load `/v2/openapi.json`. The `llms.txt` file is useful as an agent-readable index and parity cross-check, but it should not replace OpenAPI for exact endpoint, field, enum, required-property, response, or prompt-limit tracking.

## Cache Layout

After initialization, the local-only cache looks like this:

```text
.local/pixellab-doc-watch/
  sources.json
  manifest.json
  latest/
    raw/
    normalized/
  snapshots/
    YYYYMMDDTHHMMSSZ/
      raw/
      normalized/
  changes/
    YYYYMMDDTHHMMSSZ.json
  reports/
    YYYYMMDDTHHMMSSZ.md
```

`manifest.json` records the cache version, creation time, last refresh time, last report path, whether the last refresh initialized a baseline, and whether the last refresh detected normalized docs drift.

## Initialize On A Fresh Checkout

From the `pixellab-pip` repository root:

```powershell
.\dev-tools\manage-pixellab-doc-cache.ps1
```

The Windows menu wrapper hides the init option after the cache has a `manifest.json`. Explicit `-Action init` remains safe and syncs cache metadata/source definitions.

For noninteractive use, pass `-Action init`, `-Action refresh`, or `-Action status`.

For direct CLI use:

```powershell
python dev-tools/pixellab-doc-watch.py init
```

Optional: make the ignored cache its own private local Git repository so you can use Git history inside the cache without pushing snapshots to the main repository:

```powershell
python dev-tools/pixellab-doc-watch.py init --private-git
```

The private Git repository, if used, lives inside `.local/pixellab-doc-watch/.git/`. It is still ignored by the outer repository.

## Refresh And Compare

From the `pixellab-pip` repository root:

```powershell
.\dev-tools\manage-pixellab-doc-cache.ps1
```

Choose `Refresh and compare docs`.

For direct CLI use:

```powershell
python dev-tools/pixellab-doc-watch.py refresh
```

Useful variants:

```powershell
python dev-tools/pixellab-doc-watch.py refresh --snapshot always
python dev-tools/pixellab-doc-watch.py refresh --exit-zero
python dev-tools/pixellab-doc-watch.py status
```

The refresh command:

1. Downloads each default source.
2. Saves raw upstream responses.
3. Writes normalized summaries.
4. Compares normalized output against `latest/`.
5. Writes a timestamped report under `.local/pixellab-doc-watch/reports/`.
6. Updates `.local/pixellab-doc-watch/manifest.json`.
7. Replaces `latest/` with the newly fetched files.

When a source changes, the timestamped snapshot contains the newly fetched content plus a `previous/` subfolder copied from the prior `latest/` cache for that source. Compare those two folders when you need to inspect the actual before/after content.

By default, `refresh` exits with code `2` when normalized skill-relevant changes are detected, `3` when skill-relevant changes were detected but one or more sources could not be fetched, `1` when one or more sources could not be fetched and no skill-relevant change was detected, and `0` when nothing changed, only raw bytes changed, only OpenAPI metadata changed, or a baseline was initialized. Use `--exit-zero` for manual checks where a completed changed-docs refresh should count as success; fetch failures still exit nonzero and appear in the generated report.

Some agent shells display any nonzero process exit generically. For manual verification, trust the command output and manifest fields: `Changes detected.` plus `last_refresh_had_failures: false` means the refresh succeeded and found drift.

Inspect the latest local state with the wrapper:

```powershell
.\dev-tools\manage-pixellab-doc-cache.ps1 -Action status
```

The wrapper prints the machine-readable status JSON, then adds plain-English guidance for incomplete caches, failed refreshes, initialized baselines, detected drift, old caches, and clean caches.

For direct machine-readable status:

```powershell
python dev-tools/pixellab-doc-watch.py status
```

`status` prints the manifest plus whether every configured source has a matching `latest/raw` and `latest/normalized` file. Unlike `init` and `refresh`, direct `status` does not sync source definitions before reading them. Open the report path shown in `last_report` to inspect the latest findings.

## How To Read A Report

Start with the report summary table. Important signals:

- REST paths added or removed: inspect route tables and examples.
- MCP tools added or removed: inspect MCP routing and fallback rules.
- Schemas added or removed: inspect request/response guidance and prompt-limit docs.
- `llms.txt` links added or removed: inspect SDK, ReDoc, and official-repo references.
- `raw_changed`: the upstream file bytes changed but the watcher's normalized summary did not. This can recur when upstream serves dynamic documentation bytes. It is report-only, writes `normalized_change: false` plus manual-review guidance in the changes JSON, and does not make `refresh` exit `2`. Inspect raw before/after content if the source matters for a current task.
- `metadata_changed`: OpenAPI metadata such as title, version, or description changed while tracked paths and schemas stayed the same. This is visible in the report but does not make `refresh` exit `2`.

The normalized OpenAPI summary is a routing and schema-drift heuristic, not a full compatibility proof. When exact response bodies, nested inline request schemas, or subtle field behavior matter, inspect `latest/raw/rest-openapi.json` or the relevant snapshot directly.

Every report includes an Agent Skill impact checklist. Review the listed files when a change affects routing, fields, limits, or public support status.

## Update The Agent Skill After A Change

Recommended flow:

1. Run `.\dev-tools\manage-pixellab-doc-cache.ps1` and choose `Refresh and compare docs`, or run `python dev-tools/pixellab-doc-watch.py refresh`.
2. Open the newest report listed in `manifest.json`.
3. Check the raw or normalized snapshot for any changed source. For before/after inspection, compare `snapshots/<timestamp>/previous/` with `snapshots/<timestamp>/`.
4. Update only the relevant tracked docs or skill references.
5. Refresh again after editing only if you need to confirm the upstream source did not change mid-work.

Common files to update:

- `skills/pixellab-pip/SKILL.md`
- `skills/pixellab-pip/references/official-pixellab-documentation.md`
- `skills/pixellab-pip/references/prompt-limits.md`
- `skills/pixellab-pip/references/image-input-roles.md`
- `docs/pixellab-ui-generation-surfaces-research.md`
- `docs/pixellab/pixellab-asset-routing.md`
- `docs/pixellab/pixellab-user-facing-term-backend-mapping.md`

## Local-Only Rules

- Do not commit `.local/pixellab-doc-watch/`.
- Do not place PixelLab bearer tokens, website session tokens, cookies, or private account data in the cache.
- Do not use cached website internals as public API contracts.
- Treat `https://api.pixellab.ai/v2/openapi.json` as the REST schema source of truth.
- Treat `https://api.pixellab.ai/v2/llms.txt` as an LLM-friendly REST index and parity check, not as the only API documentation source.
- Treat `https://api.pixellab.ai/mcp/docs` as the public MCP tool inventory source of truth.

## Troubleshooting

If Python cannot be found, run the command with the Python launcher:

```powershell
py dev-tools/pixellab-doc-watch.py refresh
```

If a source fails to download, the watcher keeps the existing `latest/` cache entry for that source and writes `fetch_failed` in the report. Rerun later. Do not update routing claims from a partial failed refresh unless the needed source was fetched successfully.

If the report shows a change but the difference is unclear, compare the relevant files under `snapshots/<timestamp>/previous/` with the current files under `snapshots/<timestamp>/`. If there is no `previous/` file, that source was initialized in that run.
