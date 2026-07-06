#!/usr/bin/env python3
"""Repository QA checks for PixelLab Pip."""

from __future__ import annotations

import html
import json
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


def check_blueprint_shapes() -> None:
    for path in run_git_ls_files("*.blueprint.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for step in data if isinstance(data, list) else [data]:
            routes = [key for key in step if not key.startswith("_comment")]
            if len(routes) != 1 or not routes[0].startswith(("MCP ", "POST /v2/")):
                rel = path.relative_to(REPO_ROOT)
                raise AssertionError(f"{rel}: expected exactly one 'MCP ' or 'POST /v2/' route key, got {routes}")


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
        text = path.read_text(encoding="utf-8")
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
    ("blueprint presets have exactly one route key", check_blueprint_shapes),
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
