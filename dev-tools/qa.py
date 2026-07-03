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
PLACEHOLDER_TARGETS = {"path-or-url", "url", "path"}
VERSION_PATHS = (
    (".claude-plugin/marketplace.json", ("plugins", 0, "version")),
    (".claude-plugin/plugin.json", ("version",)),
    (".codex-plugin/plugin.json", ("version",)),
    (".cursor-plugin/plugin.json", ("version",)),
    (".github/plugin/marketplace.json", ("plugins", 0, "version")),
    ("gemini-extension.json", ("version",)),
    ("plugin.json", ("version",)),
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
    for path in run_git_ls_files("*.json", "*/*.json", "*/*/*.json", "*/*/*/*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def read_version_path(path: str, parts: tuple[object, ...]) -> str:
    value: object = json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))
    for part in parts:
        if isinstance(part, int):
            value = value[part]  # type: ignore[index]
        else:
            value = value[part]  # type: ignore[index]
    if not isinstance(value, str):
        raise AssertionError(f"{path} version value is not a string")
    return value


def check_versions() -> None:
    versions = {read_version_path(path, parts) for path, parts in VERSION_PATHS}
    if len(versions) != 1:
        raise AssertionError(f"version mismatch: {sorted(versions)}")


def check_python_compiles() -> None:
    for path in run_git_ls_files("*.py", "*/*.py", "*/*/*.py"):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")


def strip_link_target(target: str) -> str:
    target = html.unescape(target.strip())
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target.split("#", 1)[0]


def check_markdown_local_links() -> None:
    missing: list[str] = []
    for path in run_git_ls_files("*.md", "*/*.md", "*/*/*.md", "*/*/*/*.md"):
        text = path.read_text(encoding="utf-8")
        targets = [match.group(2) for match in MD_LINK.finditer(text)]
        targets.extend(match.group(1) for match in HTML_SRC.finditer(text))
        for raw_target in targets:
            target = strip_link_target(raw_target)
            if not target or HTTPISH.match(target):
                continue
            if target in PLACEHOLDER_TARGETS:
                continue
            if target.startswith("/"):
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
    for path in run_git_ls_files("*.png", "*/*.png", "*/*/*.png", "*/*/*/*.png"):
        if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise AssertionError(f"invalid PNG signature: {path.relative_to(REPO_ROOT)}")
    for path in run_git_ls_files("*.gif", "*/*.gif", "*/*/*.gif", "*/*/*/*.gif"):
        if path.read_bytes()[:6] not in {b"GIF87a", b"GIF89a"}:
            raise AssertionError(f"invalid GIF signature: {path.relative_to(REPO_ROOT)}")
    for path in run_git_ls_files("*.wav", "*/*.wav", "*/*/*.wav", "*/*/*/*.wav"):
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
    ("manifest versions match", check_versions),
    ("Python files compile", check_python_compiles),
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
