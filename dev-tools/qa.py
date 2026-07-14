#!/usr/bin/env python3
"""Repository QA checks for PixelLab Pip."""

from __future__ import annotations

import html
import json
import posixpath
import re
import subprocess
import sys
import unittest
import wave
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HTTPISH = re.compile(r"^(?:https?:|mailto:|tel:|data:|#)")
MD_LINK = re.compile(r"(!?)\[[^\]]*\]\(([^)]+)\)")
HTML_SRC = re.compile(r"""<img\b[^>]*\bsrc=["']([^"']+)["']""", re.IGNORECASE)
HTML_HREF = re.compile(r"""<a\b[^>]*\bhref=["']([^"']+)["']""", re.IGNORECASE)
# Code fences and inline spans hold illustrative link *syntax*, not navigable
# links (e.g. connector wrapper examples like `[label](...)`). Strip them before
# scanning so doc examples don't read as real local links — real reference
# pointers in backticks are covered by check_skill_reference_files instead.
CODE_REGION = re.compile(r"(```|~~~).*?\1|`[^`\n]*`", re.DOTALL)
PLACEHOLDER_TARGETS = {"path-or-url", "url", "path"}
VERSION_PATHS = (
    (".agents/plugins/marketplace.json", ("plugins", 0, "version")),
    (".claude-plugin/marketplace.json", ("plugins", 0, "version")),
    (".claude-plugin/plugin.json", ("version",)),
    (".codex-plugin/plugin.json", ("version",)),
    (".cursor-plugin/marketplace.json", ("plugins", 0, "version")),
    (".cursor-plugin/plugin.json", ("version",)),
    (".github/plugin/marketplace.json", ("plugins", 0, "version")),
    ("gemini-extension.json", ("version",)),
    ("plugin.json", ("version",)),
)
DESCRIPTION_PATHS = (
    (".agents/plugins/marketplace.json", ("plugins", 0, "description")),
    (".claude-plugin/marketplace.json", ("plugins", 0, "description")),
    (".claude-plugin/plugin.json", ("description",)),
    (".codex-plugin/plugin.json", ("description",)),
    (".cursor-plugin/marketplace.json", ("plugins", 0, "description")),
    (".cursor-plugin/plugin.json", ("description",)),
    (".github/plugin/marketplace.json", ("plugins", 0, "description")),
    ("gemini-extension.json", ("description",)),
    ("plugin.json", ("description",)),
)
KEYWORDS_PATHS = (
    (".agents/plugins/marketplace.json", ("plugins", 0, "keywords")),
    (".claude-plugin/marketplace.json", ("plugins", 0, "keywords")),
    (".claude-plugin/plugin.json", ("keywords",)),
    (".codex-plugin/plugin.json", ("keywords",)),
    (".cursor-plugin/marketplace.json", ("plugins", 0, "keywords")),
    (".cursor-plugin/plugin.json", ("keywords",)),
    (".github/plugin/marketplace.json", ("plugins", 0, "keywords")),
    ("plugin.json", ("keywords",)),
)


def run_git_ls_files(*patterns: str) -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", *patterns],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return [REPO_ROOT / line for line in completed.stdout.splitlines() if line.strip()]


def check_json_files() -> None:
    for path in run_git_ls_files("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def read_json_path(path: str, parts: tuple[object, ...]) -> object:
    value: object = json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))
    for part in parts:
        value = value[part]  # type: ignore[index]
    return value


def read_string_path(path: str, parts: tuple[object, ...], label: str) -> str:
    value = read_json_path(path, parts)
    if not isinstance(value, str):
        raise AssertionError(f"{path} {label} value is not a string")
    return value


def check_manifest_metadata() -> None:
    versions = {read_string_path(path, parts, "version") for path, parts in VERSION_PATHS}
    if len(versions) != 1:
        raise AssertionError(f"version mismatch: {sorted(versions)}")

    canonical = json.loads((REPO_ROOT / "plugin.json").read_text(encoding="utf-8"))
    canonical_description = canonical["description"]
    canonical_keywords = canonical["keywords"]

    description_mismatches = [
        path for path, parts in DESCRIPTION_PATHS if read_string_path(path, parts, "description") != canonical_description
    ]
    if description_mismatches:
        raise AssertionError("description mismatch: " + ", ".join(description_mismatches))

    keyword_mismatches = [
        path for path, parts in KEYWORDS_PATHS if read_json_path(path, parts) != canonical_keywords
    ]
    if keyword_mismatches:
        raise AssertionError("keywords mismatch: " + ", ".join(keyword_mismatches))


def iter_blueprint_placeholders(value: str, label: str) -> list[tuple[str, str | None, int, int]]:
    placeholders: list[tuple[str, str | None, int, int]] = []
    position = 0
    while True:
        start = value.find("{{", position)
        if start < 0:
            if "}}" in value[position:]:
                raise AssertionError(f"{label}: blueprint variable has a closing marker without an opening marker")
            return placeholders

        cursor = start + 2
        object_depth = 0
        in_json_string = False
        escaped = False
        while cursor < len(value):
            character = value[cursor]
            if in_json_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_json_string = False
            elif character == '"':
                in_json_string = True
            elif character == "{":
                object_depth += 1
            elif character == "}" and object_depth:
                object_depth -= 1
            elif character == "}" and cursor + 1 < len(value) and value[cursor + 1] == "}":
                body = value[start + 2:cursor]
                markers = list(re.finditer(r"\|\s*default\s*:", body, re.IGNORECASE))
                if len(markers) > 1:
                    raise AssertionError(f"{label}: blueprint variable has multiple default markers")
                marker = markers[0] if markers else None
                if marker is None and "|" in body:
                    raise AssertionError(f"{label}: blueprint variable has unsupported syntax after '|'")
                description = body[:marker.start()] if marker else body
                description = " ".join(description.split())
                if not description:
                    raise AssertionError(f"{label}: blueprint variable description must not be blank")
                default = body[marker.end():].strip() if marker else None
                if marker and not default:
                    raise AssertionError(
                        f'{label}: blueprint variable {description!r} has a blank default; use default: "" for an empty string'
                    )
                position = cursor + 2
                placeholders.append((description, default, start, position))
                break
            cursor += 1
        else:
            raise AssertionError(f"{label}: blueprint variable starting at character {start + 1} is not closed")


def blueprint_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from blueprint_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from blueprint_strings(item)


def reject_blueprint_variable_keys(value: object, label: str) -> None:
    if isinstance(value, list):
        for item in value:
            reject_blueprint_variable_keys(item, label)
    elif isinstance(value, dict):
        for key, item in value.items():
            if "{{" in key or "}}" in key:
                raise AssertionError(f"{label}: blueprint variables are not allowed in object or route keys")
            reject_blueprint_variable_keys(item, label)


def normalize_blueprint_default(value: str) -> tuple[str, object]:
    try:
        resolved = json.loads(value)
    except json.JSONDecodeError:
        resolved = value
    if resolved is None:
        return "null", None
    if isinstance(resolved, bool):
        return "boolean", resolved
    if isinstance(resolved, str):
        return "string", resolved
    if isinstance(resolved, list):
        return "array", resolved
    if isinstance(resolved, dict):
        return "object", resolved
    return type(resolved).__name__, resolved


def whole_blueprint_placeholder(value: object, label: str) -> tuple[str, str | None] | None:
    if not isinstance(value, str):
        return None
    placeholders = iter_blueprint_placeholders(value, label)
    if len(placeholders) == 1 and placeholders[0][2] == 0 and placeholders[0][3] == len(value):
        return placeholders[0][0], placeholders[0][1]
    return None


def validate_blueprint_data(data: object, label: str) -> None:
    steps = data if isinstance(data, list) else [data]
    if not steps:
        raise AssertionError(f"{label}: blueprint must contain at least one step")

    pixellab_routes = 0
    variable_defaults: dict[str, tuple[str, object]] = {}
    task_outputs: set[str] = set()
    for number, step in enumerate(steps, 1):
        if not isinstance(step, dict):
            raise AssertionError(f"{label}: step {number} must be an object")
        reject_blueprint_variable_keys(step, f"{label}: step {number}")
        for key, comment in step.items():
            if key.startswith("_comment") and (not isinstance(comment, str) or not comment.strip()):
                raise AssertionError(f"{label}: step {number} {key} must be a nonblank string")
        actions = [key for key in step if not key.startswith("_comment")]
        if len(actions) != 1:
            raise AssertionError(f"{label}: step {number} must have exactly one executable key, got {actions}")

        action = actions[0]
        value = step[action]
        for text_value in blueprint_strings(value):
            for description, default, start, end in iter_blueprint_placeholders(
                text_value, f"{label}: step {number}"
            ):
                if default is None:
                    continue
                variable = description.casefold()
                normalized_default = normalize_blueprint_default(default)
                if normalized_default[0] in {"array", "object"} and (start != 0 or end != len(text_value)):
                    raise AssertionError(
                        f"{label}: blueprint variable {description!r} has a non-scalar default embedded in text"
                    )
                previous_default = variable_defaults.setdefault(variable, normalized_default)
                if previous_default != normalized_default:
                    raise AssertionError(
                        f"{label}: blueprint variable {description!r} has conflicting defaults"
                    )
        if action.startswith(("MCP ", "POST /v2/")):
            prefix = "MCP " if action.startswith("MCP ") else "POST /v2/"
            route_name = action[len(prefix):]
            route_pattern = r"[A-Za-z0-9_-]+" if prefix == "MCP " else r"[A-Za-z0-9_{}-]+(?:/[A-Za-z0-9_{}-]+)*"
            if not re.fullmatch(route_pattern, route_name):
                raise AssertionError(f"{label}: step {number} PixelLab route name must be nonblank with no whitespace")
            if not isinstance(value, dict):
                raise AssertionError(f"{label}: step {number} PixelLab request body must be an object")
            pixellab_routes += 1
            continue
        if action != "TASK":
            raise AssertionError(f"{label}: unsupported executable key {action!r}")
        if isinstance(value, str):
            if not value.strip():
                raise AssertionError(f"{label}: step {number} TASK instruction must not be blank")
            continue
        if not isinstance(value, dict):
            raise AssertionError(f"{label}: step {number} TASK value must be a string or object")

        allowed = {"instruction", "inputs", "outputs", "verify"}
        unknown = set(value) - allowed
        if unknown:
            raise AssertionError(f"{label}: step {number} TASK has unknown fields {sorted(unknown)}")
        instruction = value.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            raise AssertionError(f"{label}: step {number} TASK instruction must be a nonblank string")
        for field in ("instruction", "verify"):
            field_value = value.get(field)
            if field_value is None:
                continue
            placeholder = whole_blueprint_placeholder(field_value, f"{label}: step {number} TASK {field}")
            if placeholder and placeholder[1] is not None and normalize_blueprint_default(placeholder[1])[0] != "string":
                raise AssertionError(f"{label}: step {number} TASK {field} default must be a string")
        for field in ("inputs", "outputs"):
            paths = value.get(field)
            if paths is None:
                continue
            placeholder = whole_blueprint_placeholder(paths, f"{label}: step {number} TASK {field}")
            if placeholder:
                _, default = placeholder
                if default is None:
                    continue
                default_type, paths = normalize_blueprint_default(default)
                if default_type != "array":
                    raise AssertionError(f"{label}: step {number} TASK {field} default must be an array")
            if not isinstance(paths, list) or not paths or any(not isinstance(path, str) or not path.strip() for path in paths):
                raise AssertionError(f"{label}: step {number} TASK {field} must be a nonempty string array")
            normalized = [path.replace("\\", "/") for path in paths]
            if any(
                path.startswith("/")
                or path.endswith("/")
                or re.match(r"^[A-Za-z]:/", path)
                or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", path)
                or ".." in path.split("/")
                or posixpath.normpath(path) == "."
                for path in normalized
            ):
                raise AssertionError(f"{label}: step {number} TASK {field} must use local relative paths")
            portable_paths = [posixpath.normpath(path).casefold() for path in normalized]
            if len(portable_paths) != len(set(portable_paths)):
                raise AssertionError(f"{label}: step {number} TASK {field} must be unique")
            if field == "outputs":
                duplicates = task_outputs.intersection(portable_paths)
                if duplicates:
                    raise AssertionError(f"{label}: step {number} TASK output is already produced by an earlier step")
                task_outputs.update(portable_paths)
        verify = value.get("verify")
        if verify is not None and (not isinstance(verify, str) or not verify.strip()):
            raise AssertionError(f"{label}: step {number} TASK verify must be a nonblank string")

    if not pixellab_routes:
        raise AssertionError(f"{label}: blueprint must contain at least one MCP or REST v2 step")


def check_blueprint_shapes() -> None:
    paths = set(run_git_ls_files("*.blueprint.json"))
    for folder in ("skills", "docs", "tests"):
        paths.update((REPO_ROOT / folder).rglob("*.blueprint.json"))
    for path in sorted(paths):
        data = json.loads(path.read_text(encoding="utf-8"))
        validate_blueprint_data(data, str(path.relative_to(REPO_ROOT)))


def check_python_compiles() -> None:
    for path in run_git_ls_files("*.py"):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")


def check_workflows() -> None:
    qa_workflow = (REPO_ROOT / ".github/workflows/qa.yml").read_text(encoding="utf-8")
    release_workflow = (REPO_ROOT / ".github/workflows/release-skill.yml").read_text(encoding="utf-8")
    # Assert the step is present regardless of the pinned major version, so a
    # routine setup-python/@vN bump does not red QA on an otherwise correct
    # workflow.
    if "actions/setup-python@" not in qa_workflow:
        raise AssertionError("qa.yml must set up Python explicitly")
    if "actions/setup-python@" not in release_workflow:
        raise AssertionError("release-skill.yml must set up Python explicitly before QA")
    if "python -m pip install -r requirements-dev.txt" not in qa_workflow:
        raise AssertionError("qa.yml must install requirements-dev.txt before QA")
    if "python -m pip install -r requirements-dev.txt" not in release_workflow:
        raise AssertionError("release-skill.yml must install requirements-dev.txt before QA")
    if "actions/setup-node@" not in release_workflow:
        raise AssertionError("release-skill.yml must set up Node.js explicitly before version bump")
    if release_workflow.find("actions/setup-node@") > release_workflow.find("node <<'NODE'"):
        raise AssertionError("release-skill.yml must set up Node.js before running node")


def check_no_tracked_generated_artifacts() -> None:
    generated = run_git_ls_files(
        ".local/*",
        "pixellab-pip-generations/*",
        "*__pycache__/*",
    )
    if generated:
        rels = [str(path.relative_to(REPO_ROOT)) for path in generated]
        raise AssertionError("generated/cache files are tracked:\n" + "\n".join(rels))


def strip_link_target(target: str) -> str:
    target = html.unescape(target.strip())
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target.split("#", 1)[0]


def check_markdown_local_links() -> None:
    missing: list[str] = []
    for path in run_git_ls_files("*.md"):
        text = CODE_REGION.sub("", path.read_text(encoding="utf-8"))
        targets = [match.group(2) for match in MD_LINK.finditer(text)]
        targets.extend(match.group(1) for match in HTML_SRC.finditer(text))
        targets.extend(match.group(1) for match in HTML_HREF.finditer(text))
        for raw_target in targets:
            target = strip_link_target(raw_target)
            if not target or HTTPISH.match(target):
                continue
            if target in PLACEHOLDER_TARGETS:
                continue
            if target.startswith("/"):
                continue
            # Links into the gitignored local-only research/output folder are
            # intentionally absent from the repo (see docs/developer.md); skip them.
            if "pixellab-pip-generations/" in target:
                continue
            if not (path.parent / target).resolve().exists():
                rel = path.relative_to(REPO_ROOT)
                missing.append(f"{rel}: {raw_target}")
    if missing:
        raise AssertionError("missing local markdown links:\n" + "\n".join(missing))


def check_skill_reference_files() -> None:
    skill = REPO_ROOT / "skills/pixellab-pip/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    refs = sorted(set(re.findall(r"`(references/[^`]+\.md)`", text)))
    missing = [ref for ref in refs if not (skill.parent / ref).exists()]
    if missing:
        raise AssertionError("missing SKILL.md reference files: " + ", ".join(missing))


def check_media_files() -> None:
    for path in run_git_ls_files("*.png"):
        if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise AssertionError(f"invalid PNG signature: {path.relative_to(REPO_ROOT)}")
    for path in run_git_ls_files("*.gif"):
        if path.read_bytes()[:6] not in {b"GIF87a", b"GIF89a"}:
            raise AssertionError(f"invalid GIF signature: {path.relative_to(REPO_ROOT)}")
    for path in run_git_ls_files("*.wav"):
        with wave.open(str(path), "rb") as handle:
            if handle.getnframes() <= 0:
                raise AssertionError(f"empty WAV: {path.relative_to(REPO_ROOT)}")


def run_unit_tests() -> None:
    suite = unittest.defaultTestLoader.discover(str(REPO_ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


CHECKS = [
    ("JSON manifests parse", check_json_files),
    ("blueprint step shapes are valid", check_blueprint_shapes),
    ("manifest metadata matches", check_manifest_metadata),
    ("Python files compile", check_python_compiles),
    ("workflows declare required runtimes", check_workflows),
    ("no generated cache artifacts are tracked", check_no_tracked_generated_artifacts),
    ("Markdown local links resolve", check_markdown_local_links),
    ("SKILL.md reference files exist", check_skill_reference_files),
    ("tracked media signatures are valid", check_media_files),
    ("unit tests pass", run_unit_tests),
]


def main() -> int:
    for label, check in CHECKS:
        print(f"[qa] {label}...")
        check()
    print("[qa] all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
