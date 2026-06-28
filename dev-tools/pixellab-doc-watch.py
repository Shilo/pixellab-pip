#!/usr/bin/env python3
"""Local-only watcher for upstream PixelLab documentation drift."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any


SOURCE_DEFS = [
    {
        "id": "rest_openapi",
        "url": "https://api.pixellab.ai/v2/openapi.json",
        "kind": "openapi",
        "raw_name": "rest-openapi.json",
    },
    {
        "id": "rest_llms",
        "url": "https://api.pixellab.ai/v2/llms.txt",
        "kind": "llms",
        "raw_name": "rest-llms.txt",
    },
    {
        "id": "rest_docs_shell",
        "url": "https://api.pixellab.ai/v2/docs",
        "kind": "html_text",
        "raw_name": "rest-docs.html",
    },
    {
        "id": "rest_redoc_shell",
        "url": "https://api.pixellab.ai/v2/redoc",
        "kind": "html_text",
        "raw_name": "rest-redoc.html",
    },
    {
        "id": "mcp_docs",
        "url": "https://api.pixellab.ai/mcp/docs",
        "kind": "mcp_docs",
        "raw_name": "mcp-docs.md",
    },
    {
        "id": "website_docs",
        "url": "https://www.pixellab.ai/docs",
        "kind": "html_text",
        "raw_name": "website-docs.html",
    },
    {
        "id": "website_mcp",
        "url": "https://www.pixellab.ai/mcp",
        "kind": "html_text",
        "raw_name": "website-mcp.html",
    },
]

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def stamp(now: dt.datetime) -> str:
    return now.strftime("%Y%m%dT%H%M%SZ")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_cache_dir() -> Path:
    return repo_root() / ".local" / "pixellab-doc-watch"


def ensure_dirs(cache_dir: Path) -> None:
    for rel in [
        "latest/raw",
        "latest/normalized",
        "snapshots",
        "reports",
        "changes",
    ]:
        (cache_dir / rel).mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(source: dict[str, str], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "pixellab-pip-doc-watch/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        headers = dict(response.headers.items())
        return {
            "source_id": source["id"],
            "url": source["url"],
            "status": getattr(response, "status", None),
            "content_type": headers.get("Content-Type"),
            "etag": headers.get("ETag"),
            "last_modified": headers.get("Last-Modified"),
            "raw_sha256": sha256_bytes(body),
            "body": body,
        }


def compact_schema(schema: Any, depth: int = 0) -> Any:
    if depth > 5:
        return "<max-depth>"
    if isinstance(schema, list):
        return [compact_schema(item, depth + 1) for item in schema]
    if not isinstance(schema, dict):
        return schema

    keep_keys = [
        "$ref",
        "type",
        "format",
        "title",
        "description",
        "enum",
        "const",
        "default",
        "required",
        "minLength",
        "maxLength",
        "minimum",
        "maximum",
        "minItems",
        "maxItems",
    ]
    result: dict[str, Any] = {key: schema[key] for key in keep_keys if key in schema}
    if "items" in schema:
        result["items"] = compact_schema(schema["items"], depth + 1)
    for union_key in ("anyOf", "oneOf", "allOf"):
        if union_key in schema:
            result[union_key] = compact_schema(schema[union_key], depth + 1)
    if "properties" in schema and isinstance(schema["properties"], dict):
        result["properties"] = {
            key: compact_schema(value, depth + 1)
            for key, value in sorted(schema["properties"].items())
        }
    return result


def request_schema_refs(operation: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    content = operation.get("requestBody", {}).get("content", {})
    for media in content.values():
        ref = media.get("schema", {}).get("$ref")
        if ref:
            refs.append(ref.rsplit("/", 1)[-1])
    return sorted(set(refs))


def response_codes(operation: dict[str, Any]) -> list[str]:
    return sorted(str(code) for code in operation.get("responses", {}).keys())


def normalize_openapi(raw: bytes, source: dict[str, str], fetched: dict[str, Any]) -> dict[str, Any]:
    doc = json.loads(raw.decode("utf-8"))
    paths: dict[str, Any] = {}
    for path, path_item in sorted(doc.get("paths", {}).items()):
        methods: dict[str, Any] = {}
        for method, operation in sorted(path_item.items()):
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            methods[method.upper()] = {
                "operation_id": operation.get("operationId"),
                "summary": operation.get("summary"),
                "tags": operation.get("tags", []),
                "request_schemas": request_schema_refs(operation),
                "response_codes": response_codes(operation),
            }
        paths[path] = methods

    schemas = doc.get("components", {}).get("schemas", {})
    compact_schemas = {
        name: compact_schema(schema)
        for name, schema in sorted(schemas.items())
    }
    return {
        "source_id": source["id"],
        "url": source["url"],
        "kind": source["kind"],
        "raw_sha256": fetched["raw_sha256"],
        "openapi": doc.get("openapi"),
        "info": doc.get("info", {}),
        "path_count": len(paths),
        "paths": paths,
        "schema_count": len(compact_schemas),
        "schemas": compact_schemas,
    }


def normalize_llms(raw: bytes, source: dict[str, str], fetched: dict[str, Any]) -> dict[str, Any]:
    text = raw.decode("utf-8", errors="replace")
    method_paths = sorted(set(re.findall(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9_./{}-]+)", text)))
    links = sorted(set(re.findall(r"https?://[^\s)>\]]+", text)))
    endpoint_mentions = sorted(set(re.findall(r"(?<!https:)(/[A-Za-z0-9_./{}-]+)", text)))
    return {
        "source_id": source["id"],
        "url": source["url"],
        "kind": source["kind"],
        "raw_sha256": fetched["raw_sha256"],
        "method_paths": [f"{method} {path}" for method, path in method_paths],
        "endpoint_mentions": endpoint_mentions,
        "links": links,
    }


def normalize_mcp_docs(raw: bytes, source: dict[str, str], fetched: dict[str, Any]) -> dict[str, Any]:
    text = raw.decode("utf-8", errors="replace")
    heading_tools = re.findall(r"^#{2,4}\s+`?([a-z][a-z0-9_]{2,})`?\s*$", text, flags=re.MULTILINE)
    code_identifiers = sorted(set(re.findall(r"`([a-z][a-z0-9_]{2,})`", text)))
    tools = sorted(set(heading_tools))
    return {
        "source_id": source["id"],
        "url": source["url"],
        "kind": source["kind"],
        "raw_sha256": fetched["raw_sha256"],
        "tool_count": len(tools),
        "tools": tools,
        "code_identifiers": code_identifiers,
        "headings": re.findall(r"^#{1,4}\s+(.+?)\s*$", text, flags=re.MULTILINE),
    }


def normalize_text(raw: bytes, source: dict[str, str], fetched: dict[str, Any]) -> dict[str, Any]:
    text = raw.decode("utf-8", errors="replace")
    title_match = re.search(r"<title>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    links = sorted(set(re.findall(r"https?://[^\s\"'<>]+", text)))
    return {
        "source_id": source["id"],
        "url": source["url"],
        "kind": source["kind"],
        "raw_sha256": fetched["raw_sha256"],
        "title": re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else None,
        "links": links[:500],
    }


def normalize(raw: bytes, source: dict[str, str], fetched: dict[str, Any]) -> dict[str, Any]:
    if source["kind"] == "openapi":
        return normalize_openapi(raw, source, fetched)
    if source["kind"] == "llms":
        return normalize_llms(raw, source, fetched)
    if source["kind"] == "mcp_docs":
        return normalize_mcp_docs(raw, source, fetched)
    return normalize_text(raw, source, fetched)


def list_delta(before: list[str], after: list[str]) -> dict[str, list[str]]:
    before_set = set(before)
    after_set = set(after)
    return {
        "added": sorted(after_set - before_set),
        "removed": sorted(before_set - after_set),
    }


def source_delta(previous: Any, current: dict[str, Any]) -> dict[str, Any]:
    if previous is None:
        delta: dict[str, Any] = {"status": "initialized"}
        if current["kind"] == "openapi":
            delta["path_count"] = current.get("path_count", 0)
            delta["schema_count"] = current.get("schema_count", 0)
        elif current["kind"] == "mcp_docs":
            delta["tool_count"] = current.get("tool_count", 0)
        elif current["kind"] == "llms":
            delta["method_path_count"] = len(current.get("method_paths", []))
            delta["link_count"] = len(current.get("links", []))
        return delta

    metadata_keys = {"info", "openapi"} if current["kind"] == "openapi" else set()
    report_only_keys = {"raw_sha256"}
    previous_semantic = {key: value for key, value in previous.items() if key not in report_only_keys | metadata_keys}
    current_semantic = {key: value for key, value in current.items() if key not in report_only_keys | metadata_keys}
    previous_metadata = {key: previous.get(key) for key in metadata_keys}
    current_metadata = {key: current.get(key) for key in metadata_keys}
    if previous_semantic == current_semantic:
        if previous_metadata != current_metadata:
            delta = {
                "status": "metadata_changed",
                "normalized_change": True,
                "action_required": False,
                "meaning": "OpenAPI metadata changed, but tracked paths and schemas are unchanged. This is not counted as skill-relevant docs drift.",
                "metadata": {
                    key: {"before": previous_metadata.get(key), "after": current_metadata.get(key)}
                    for key in sorted(metadata_keys)
                    if previous_metadata.get(key) != current_metadata.get(key)
                },
            }
            if previous.get("raw_sha256") != current.get("raw_sha256"):
                delta["raw_sha256"] = {"before": previous.get("raw_sha256"), "after": current.get("raw_sha256")}
            return delta
        if previous.get("raw_sha256") != current.get("raw_sha256"):
            return {
                "status": "raw_changed",
                "normalized_change": False,
                "manual_review": "Inspect raw before/after only if this source matters for the current task.",
                "meaning": "Raw bytes changed, but the normalized summary is unchanged. This is not counted as docs drift.",
                "raw_sha256": {"before": previous.get("raw_sha256"), "after": current.get("raw_sha256")},
            }
        return {"status": "unchanged"}

    delta: dict[str, Any] = {"status": "changed"}
    if current["kind"] == "openapi":
        delta["paths"] = list_delta(list(previous.get("paths", {}).keys()), list(current.get("paths", {}).keys()))
        delta["schemas"] = list_delta(list(previous.get("schemas", {}).keys()), list(current.get("schemas", {}).keys()))
        shared_paths = sorted(set(previous.get("paths", {})) & set(current.get("paths", {})))
        modified_paths = [
            path for path in shared_paths
            if previous.get("paths", {}).get(path) != current.get("paths", {}).get(path)
        ]
        if modified_paths:
            delta["modified_paths"] = modified_paths
        shared_schemas = sorted(set(previous.get("schemas", {})) & set(current.get("schemas", {})))
        modified_schemas = [
            name for name in shared_schemas
            if previous.get("schemas", {}).get(name) != current.get("schemas", {}).get(name)
        ]
        if modified_schemas:
            delta["modified_schemas"] = modified_schemas
    elif current["kind"] == "mcp_docs":
        delta["tools"] = list_delta(previous.get("tools", []), current.get("tools", []))
        delta["code_identifiers"] = list_delta(previous.get("code_identifiers", []), current.get("code_identifiers", []))
    elif current["kind"] == "llms":
        delta["method_paths"] = list_delta(previous.get("method_paths", []), current.get("method_paths", []))
        delta["links"] = list_delta(previous.get("links", []), current.get("links", []))
    if previous.get("raw_sha256") != current.get("raw_sha256"):
        delta["raw_sha256"] = {"before": previous.get("raw_sha256"), "after": current.get("raw_sha256")}
    return delta


def write_sources_file(cache_dir: Path) -> None:
    sources_path = cache_dir / "sources.json"
    if not sources_path.exists():
        write_json(sources_path, SOURCE_DEFS)
        return
    existing = read_json(sources_path, [])
    existing_by_id = {
        source.get("id"): source
        for source in existing
        if isinstance(source, dict) and source.get("id")
    }
    custom_sources = [
        source for source in existing
        if isinstance(source, dict)
        and source.get("id")
        and source.get("id") not in {default["id"] for default in SOURCE_DEFS}
    ]
    merged = list(SOURCE_DEFS) + custom_sources
    changed = len(merged) != len(existing)
    for source in SOURCE_DEFS:
        if existing_by_id.get(source["id"]) != source:
            changed = True
    if changed:
        write_json(sources_path, merged)


def load_sources(cache_dir: Path) -> list[dict[str, str]]:
    write_sources_file(cache_dir)
    return read_json(cache_dir / "sources.json", SOURCE_DEFS)


def read_sources(cache_dir: Path) -> list[dict[str, str]]:
    return read_json(cache_dir / "sources.json", SOURCE_DEFS)


def save_snapshot(cache_dir: Path, run_stamp: str, source: dict[str, str], raw: bytes, normalized: dict[str, Any]) -> None:
    snap = cache_dir / "snapshots" / run_stamp
    (snap / "raw").mkdir(parents=True, exist_ok=True)
    (snap / "normalized").mkdir(parents=True, exist_ok=True)
    (snap / "raw" / source["raw_name"]).write_bytes(raw)
    write_json(snap / "normalized" / f"{source['id']}.json", normalized)


def save_previous_snapshot(cache_dir: Path, run_stamp: str, source: dict[str, str]) -> None:
    previous_raw = cache_dir / "latest" / "raw" / source["raw_name"]
    previous_normalized = cache_dir / "latest" / "normalized" / f"{source['id']}.json"
    if not previous_raw.exists() and not previous_normalized.exists():
        return

    snap = cache_dir / "snapshots" / run_stamp / "previous"
    if previous_raw.exists():
        (snap / "raw").mkdir(parents=True, exist_ok=True)
        shutil.copy2(previous_raw, snap / "raw" / source["raw_name"])
    if previous_normalized.exists():
        (snap / "normalized").mkdir(parents=True, exist_ok=True)
        shutil.copy2(previous_normalized, snap / "normalized" / f"{source['id']}.json")


def update_latest(cache_dir: Path, source: dict[str, str], raw: bytes, normalized: dict[str, Any]) -> None:
    (cache_dir / "latest" / "raw" / source["raw_name"]).write_bytes(raw)
    write_json(cache_dir / "latest" / "normalized" / f"{source['id']}.json", normalized)


def render_report(run_stamp: str, generated_at: str, cache_dir: Path, changes: dict[str, Any]) -> str:
    lines = [
        f"# PixelLab Documentation Watch Report {run_stamp}",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Cache directory: `{cache_dir}`",
        "",
        "## Summary",
        "",
        "| Source | Status | Notes |",
        "|---|---|---|",
    ]
    for source_id, change in changes["sources"].items():
        notes: list[str] = []
        if "paths" in change:
            notes.append(f"REST paths +{len(change['paths']['added'])}/-{len(change['paths']['removed'])}")
        if "schemas" in change:
            notes.append(f"schemas +{len(change['schemas']['added'])}/-{len(change['schemas']['removed'])}")
        if "modified_paths" in change:
            notes.append(f"modified REST paths {len(change['modified_paths'])}")
        if "modified_schemas" in change:
            notes.append(f"modified schemas {len(change['modified_schemas'])}")
        if "tools" in change:
            notes.append(f"MCP tools +{len(change['tools']['added'])}/-{len(change['tools']['removed'])}")
        if "code_identifiers" in change:
            notes.append(f"MCP identifiers +{len(change['code_identifiers']['added'])}/-{len(change['code_identifiers']['removed'])}")
        if "method_paths" in change:
            notes.append(f"LLMS method paths +{len(change['method_paths']['added'])}/-{len(change['method_paths']['removed'])}")
        if change["status"] == "fetch_failed":
            notes.append(change.get("error", "fetch failed"))
        if change["status"] == "initialized":
            if "path_count" in change:
                notes.append(f"{change['path_count']} REST paths")
            if "schema_count" in change:
                notes.append(f"{change['schema_count']} schemas")
            if "tool_count" in change:
                notes.append(f"{change['tool_count']} MCP tools")
            if "method_path_count" in change:
                notes.append(f"{change['method_path_count']} LLMS method paths")
            if "link_count" in change:
                notes.append(f"{change['link_count']} links")
        if change["status"] == "raw_changed":
            notes.append("raw byte change only; normalized summary unchanged")
        if change["status"] == "metadata_changed":
            notes.append(f"OpenAPI metadata changed: {', '.join(change.get('metadata', {}).keys())}")
        elif not notes and "raw_sha256" in change:
            notes.append("raw content hash changed")
        lines.append(f"| `{source_id}` | `{change['status']}` | {'; '.join(notes) or ''} |")

    lines.extend(["", "## Details", ""])
    for source_id, change in changes["sources"].items():
        lines.extend([f"### `{source_id}`", "", f"Status: `{change['status']}`", ""])
        for key in ("paths", "schemas", "tools", "code_identifiers", "method_paths", "links"):
            if key not in change:
                continue
            for side in ("added", "removed"):
                items = change[key][side]
                if items:
                    lines.append(f"{key} {side}:")
                    lines.extend(f"- `{item}`" for item in items[:100])
                    if len(items) > 100:
                        lines.append(f"- ... {len(items) - 100} more")
                    lines.append("")
        for key in ("modified_paths", "modified_schemas"):
            if key in change:
                items = change[key]
                if items:
                    lines.append(f"{key}:")
                    lines.extend(f"- `{item}`" for item in items[:100])
                    if len(items) > 100:
                        lines.append(f"- ... {len(items) - 100} more")
                    lines.append("")
        if "metadata" in change:
            lines.append("metadata changes:")
            for key, value in change["metadata"].items():
                lines.append(f"- `{key}`:")
                lines.append("  - before:")
                lines.append(f"    ```json\n{json.dumps(value.get('before'), indent=2, sort_keys=True)}\n    ```")
                lines.append("  - after:")
                lines.append(f"    ```json\n{json.dumps(value.get('after'), indent=2, sort_keys=True)}\n    ```")
            lines.append("")

    lines.extend(
        [
            "## Agent Skill Impact Checklist",
            "",
            "Review the PixelLab Pip skill when this report shows added or removed REST paths, MCP tools, request schemas, prompt limits, or official SDK/MCP links.",
            "",
            "Common files to inspect:",
            "",
            "- `skills/pixellab-pip/SKILL.md`",
            "- `skills/pixellab-pip/references/official-pixellab-documentation.md`",
            "- `skills/pixellab-pip/references/prompt-limits.md`",
            "- `skills/pixellab-pip/references/image-input-roles.md`",
            "- `docs/pixellab-ui-generation-surfaces-research.md`",
            "- `docs/pixellab/pixellab-asset-routing.md`",
            "",
        ]
    )
    return "\n".join(lines)


def init_cache(cache_dir: Path, private_git: bool) -> None:
    ensure_dirs(cache_dir)
    write_sources_file(cache_dir)
    manifest = read_json(cache_dir / "manifest.json", {})
    manifest.setdefault("created_at", utc_now().isoformat().replace("+00:00", "Z"))
    manifest["cache_version"] = 1
    manifest["source_count"] = len(load_sources(cache_dir))
    write_json(cache_dir / "manifest.json", manifest)
    if private_git and not (cache_dir / ".git").exists():
        subprocess.run(["git", "init"], cwd=cache_dir, check=True)


def refresh(cache_dir: Path, timeout: int, snapshot_mode: str, private_git: bool) -> int:
    init_cache(cache_dir, private_git=private_git)
    now = utc_now()
    run_stamp = stamp(now)
    generated_at = now.isoformat().replace("+00:00", "Z")
    changes: dict[str, Any] = {"generated_at": generated_at, "sources": {}}
    any_changed = False
    any_failed = False
    any_initialized = False

    for source in load_sources(cache_dir):
        try:
            fetched = fetch(source, timeout=timeout)
        except Exception as exc:  # Keep the existing cache intact on transient upstream failures.
            any_failed = True
            changes["sources"][source["id"]] = {
                "status": "fetch_failed",
                "error": f"{type(exc).__name__}: {exc}",
                "url": source["url"],
            }
            continue
        raw = fetched["body"]
        normalized = normalize(raw, source, fetched)
        latest_path = cache_dir / "latest" / "normalized" / f"{source['id']}.json"
        previous = read_json(latest_path)
        delta = source_delta(previous, normalized)
        changes["sources"][source["id"]] = delta
        changed = delta["status"] not in ("unchanged", "raw_changed", "metadata_changed", "initialized")
        reportable = delta["status"] != "unchanged"
        any_changed = any_changed or changed
        any_initialized = any_initialized or delta["status"] == "initialized"
        if snapshot_mode == "always" or (snapshot_mode == "changed" and reportable):
            if reportable:
                save_previous_snapshot(cache_dir, run_stamp, source)
            save_snapshot(cache_dir, run_stamp, source, raw, normalized)
        update_latest(cache_dir, source, raw, normalized)

    write_json(cache_dir / "changes" / f"{run_stamp}.json", changes)
    report = render_report(run_stamp, generated_at, cache_dir, changes)
    report_path = cache_dir / "reports" / f"{run_stamp}.md"
    report_path.write_text(report, encoding="utf-8")

    manifest = read_json(cache_dir / "manifest.json", {})
    manifest.update(
        {
            "last_refreshed_at": generated_at,
            "last_report": str(report_path.relative_to(cache_dir)),
            "last_change_detected": any_changed,
            "last_refresh_initialized_sources": any_initialized,
            "last_refresh_had_failures": any_failed,
        }
    )
    write_json(cache_dir / "manifest.json", manifest)

    print(f"Refreshed PixelLab docs cache: {cache_dir}")
    print(f"Report: {report_path}")
    if any_failed:
        if any_changed:
            print("Changes were detected in successfully fetched sources, but the refresh is incomplete.")
        print("One or more sources failed to refresh. Existing latest cache entries were kept for failed sources.")
        if any_changed and not args.exit_zero:
            return 3
        return 1
    if any_changed:
        print("Changes detected.")
    elif any_initialized:
        print("Initialized baseline. No prior cache existed for one or more sources.")
    else:
        print("No changes detected.")
    return 2 if any_changed else 0


def status(cache_dir: Path) -> int:
    manifest = read_json(cache_dir / "manifest.json")
    if not manifest:
        print(f"No cache manifest found at {cache_dir}")
        return 1
    sources = read_sources(cache_dir)
    latest_files = {}
    latest_complete = True
    for source in sources:
        raw_exists = (cache_dir / "latest" / "raw" / source["raw_name"]).exists()
        normalized_exists = (cache_dir / "latest" / "normalized" / f"{source['id']}.json").exists()
        latest_files[source["id"]] = {
            "raw_exists": raw_exists,
            "normalized_exists": normalized_exists,
        }
        latest_complete = latest_complete and raw_exists and normalized_exists
    manifest = dict(manifest)
    manifest["latest_complete"] = latest_complete
    manifest["latest_files"] = latest_files
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0 if latest_complete else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch upstream PixelLab docs in a local ignored cache.")
    parser.add_argument("--cache-dir", type=Path, default=default_cache_dir())
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Create the local cache directory and source config.")
    init_parser.add_argument("--private-git", action="store_true", help="Initialize a nested private git repo inside the ignored cache.")

    refresh_parser = sub.add_parser("refresh", help="Download docs, compare against latest cache, and write a report.")
    refresh_parser.add_argument("--timeout", type=int, default=45)
    refresh_parser.add_argument("--snapshot", choices=["always", "changed", "never"], default="changed")
    refresh_parser.add_argument("--private-git", action="store_true", help="Initialize a nested private git repo inside the ignored cache if missing.")
    refresh_parser.add_argument("--exit-zero", action="store_true", help="Return exit code 0 instead of 2 when changes are detected; fetch failures still return nonzero.")

    sub.add_parser("status", help="Print the local cache manifest.")

    args = parser.parse_args()
    cache_dir = args.cache_dir.resolve()
    if args.command == "init":
        init_cache(cache_dir, private_git=args.private_git)
        print(f"Initialized PixelLab docs cache: {cache_dir}")
        return 0
    if args.command == "refresh":
        code = refresh(cache_dir, args.timeout, args.snapshot, private_git=args.private_git)
        return 0 if args.exit_zero and code == 2 else code
    if args.command == "status":
        return status(cache_dir)
    return 1


if __name__ == "__main__":
    sys.exit(main())
