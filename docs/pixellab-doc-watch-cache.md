# PixelLab Documentation Watch Cache

Last reviewed: 2026-06-28.

Use this workflow when PixelLab's public REST, MCP, SDK, or setup documentation might have changed and PixelLab Pip needs a repeatable local record before updating the Agent Skill.

The tracked repository contains only the watcher script and these instructions. Downloaded upstream documentation, snapshots, hashes, and reports stay local in `.local/pixellab-doc-watch/`, which is ignored by Git.

## What It Tracks

Default sources:

- `https://api.pixellab.ai/v2/openapi.json`
- `https://api.pixellab.ai/v2/llms.txt`
- `https://api.pixellab.ai/mcp/docs`
- `https://www.pixellab.ai/docs`
- `https://www.pixellab.ai/mcp`

The watcher stores raw files and normalized summaries. The normalized summaries are designed to surface skill-relevant drift such as added REST paths, added MCP tools, schema-name changes, prompt-limit fields, official links, and source hash changes.

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

`manifest.json` records the cache version, creation time, last refresh time, last report path, and whether the last refresh detected a change.

## Initialize On A Fresh Checkout

From the `pixellab-pip` repository root:

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

By default, `refresh` exits with code `2` when changes are detected, `0` when nothing changed, and `1` when one or more sources could not be fetched. Use `--exit-zero` for manual checks where any completed refresh should count as success; fetch failures still appear in the generated report.

Some agent shells display any nonzero process exit generically. For manual verification, trust the command output and manifest fields: `Changes detected.` plus `last_refresh_had_failures: false` means the refresh succeeded and found drift.

Verify the latest local state with:

```powershell
python dev-tools/pixellab-doc-watch.py status
```

Open the report path shown in `last_report` to inspect the latest findings.

## How To Read A Report

Start with the report summary table. Important signals:

- REST paths added or removed: inspect route tables and examples.
- MCP tools added or removed: inspect MCP routing and fallback rules.
- Schemas added or removed: inspect request/response guidance and prompt-limit docs.
- `llms.txt` links added or removed: inspect SDK, ReDoc, and official-repo references.
- `raw_changed`: the upstream file bytes changed but the watcher's normalized skill-relevant summary did not. Inspect manually if the source matters for a current task.

Every report includes an Agent Skill impact checklist. Review the listed files when a change affects routing, fields, limits, or public support status.

## Update The Agent Skill After A Change

Recommended flow:

1. Run `python dev-tools/pixellab-doc-watch.py refresh`.
2. Open the newest report listed in `manifest.json`.
3. Check the raw or normalized snapshot for any changed source.
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
- Treat `https://api.pixellab.ai/mcp/docs` as the public MCP tool inventory source of truth.

## Troubleshooting

If Python cannot be found, run the command with the Python launcher:

```powershell
py dev-tools/pixellab-doc-watch.py refresh
```

If a source fails to download, the watcher keeps the existing `latest/` cache entry for that source and writes `fetch_failed` in the report. Rerun later. Do not update routing claims from a partial failed refresh unless the needed source was fetched successfully.

If the report shows a change but the difference is unclear, compare the relevant normalized JSON under `latest/normalized/` with the matching timestamp under `snapshots/`.
