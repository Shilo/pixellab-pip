#!/usr/bin/env python3
"""Compare a pinned static SkillSpector report with the reviewed baseline.

This is a regression check, not a scanner, suppression list or security verdict.
The calling workflow attests the source commit and upstream patch; report JSON
alone cannot prove scanner provenance. Full findings remain in the input report.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path, PurePosixPath
import sys


ROOT = Path(__file__).resolve().parents[1]
SEVERITIES = ["NONE", "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def relative_path(value: object) -> str:
    require(isinstance(value, str) and bool(value), "Missing component or finding path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and "\\" not in value
            and ":" not in value and str(path) == value,
            "Expected a normalized skill-relative path")
    return value


def count_rows(rows: list[dict], keys: tuple[str, ...]) -> Counter:
    result = Counter()
    require(isinstance(rows, list), "Expected report entries")
    for row in rows:
        require(isinstance(row, dict), "Invalid report entry")
        values = tuple(row[key] for key in keys)
        require(all(isinstance(value, str) and value for value in values), "Invalid report entry key")
        if "path" in keys:
            relative_path(row["path"])
        result[values] += 1
    return result


def within_baseline(actual: Counter, rows: list[dict], keys: tuple[str, ...], label: str) -> None:
    allowed = Counter()
    for row in rows:
        count = row["count"]
        require(type(count) is int and count > 0, "Invalid baseline count")
        key = tuple(row[name] for name in keys)
        require(key not in allowed, "Duplicate baseline entry")
        allowed[key] = count
    require(not (actual - allowed), f"New or increased {label}; inspect the full report")


def validate(report: dict, baseline: dict, skill_dir: Path) -> None:
    """Raise ValueError for regressions or incomplete/invalid evidence."""
    require(report["execution_successful"] is True, "Scanner execution failed")
    metadata = report["metadata"]
    require(metadata["skillspector_version"] == baseline["scanner_version"], "Scanner version mismatch")
    require(metadata["llm_requested"] is False and metadata["llm_available"] is False
            and metadata["meta_analysis_applied"] is False and metadata["inference_usage"] == [],
            "Expected static-only analysis without model execution")
    require(metadata["filtering_mode"] == "heuristic", "Unexpected filtering mode")
    require(type(report["suppressed_count"]) is int and report["suppressed_count"] == 0
            and report["suppressed"] == [], "Suppressed findings are not accepted")

    assessment = report["risk_assessment"]
    score = assessment["score"]
    require(type(score) in (int, float) and math.isfinite(score) and 0 <= score <= baseline["risk_assessment"]["score"],
            "Risk score exceeds the reviewed baseline or is invalid")
    for field, levels in (("severity", ["SAFE", "LOW", "MEDIUM", "HIGH", "CRITICAL"]),
                          ("max_issue_severity", SEVERITIES),
                          ("recommendation", ["SAFE", "CAUTION", "DO_NOT_INSTALL"])):
        require(assessment[field] in levels, f"Unknown {field}")
        require(levels.index(assessment[field]) <= levels.index(baseline["risk_assessment"][field]),
                f"Worsened {field}")

    require(skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file(), "Skill directory missing")
    inventory = set()
    for path in skill_dir.rglob("*"):
        require(not path.is_symlink(), "Skill symlink cannot establish scan coverage")
        if path.is_file():
            inventory.add(path.relative_to(skill_dir).as_posix())
    require(Path(report["skill"]["source"]).resolve() == skill_dir.resolve(), "Report scanned a different skill directory")
    require(isinstance(report["components"], list), "Invalid component inventory")
    component_paths = [relative_path(component["path"]) for component in report["components"]]
    require(len(component_paths) == len(set(component_paths)), "Duplicate report components")
    require(set(component_paths) == inventory, "Report component inventory differs from the skill directory")

    findings = []
    require(isinstance(report["issues"], list), "Invalid findings collection")
    for issue in report["issues"]:
        path = relative_path(issue["location"]["file"])
        require(path in inventory, "Finding outside inspected inventory")
        findings.append({"id": issue["id"], "path": path, "severity": issue["severity"]})
    # Cumulative severity ceilings allow downgraded findings without exchanging a
    # decrease in one file/rule for an increase in another.
    actual, allowed = Counter(), Counter()
    for entries, counts, counted in ((findings, actual, False), (baseline["findings"], allowed, True)):
        for entry in entries:
            severity = entry["severity"]
            require(severity in SEVERITIES[1:], "Invalid finding severity")
            require(isinstance(entry["id"], str) and bool(entry["id"]), "Invalid finding rule")
            count = entry["count"] if counted else 1
            require(type(count) is int and count > 0, "Invalid finding count")
            for threshold in SEVERITIES[1:SEVERITIES.index(severity) + 1]:
                counts[(entry["id"], relative_path(entry["path"]), threshold)] += count
    require(not (actual - allowed), "New or increased findings; inspect the full report")

    coverage = report["analysis_completeness"]
    require(coverage["execution_successful"] is True, "Analysis execution failed")
    require(coverage["limitations"] == [], "Additional analysis limitations")
    before, after = coverage["findings_before_filtering"], coverage["findings_after_filtering"]
    require(type(before) is int and type(after) is int and before >= after == len(findings),
            "Finding accounting differs from the report")
    require(coverage["status"] in ("complete", "partial") and type(coverage["is_complete"]) is bool,
            "Invalid completeness status")
    require(coverage["is_complete"] == (coverage["status"] == "complete"), "Inconsistent completeness status")
    for field, entries in (("ledger_exceptions", coverage["ledger_exceptions"]),
                           ("scope_exclusions", coverage["scope_exclusions"])):
        for entry in entries:
            require(entry["fatal"] is False, "Fatal analysis exception")
            require(relative_path(entry["path"]) in inventory, "Coverage exception outside inventory")
        keys = ("outcome", "phase", "reason_code", "path")
        within_baseline(count_rows(entries, keys), baseline[field], keys, field)
    excluded = {entry["path"] for entry in coverage["scope_exclusions"]}
    expected = len(inventory - excluded)
    for field in ("total_components", "scanned_components", "fully_inspected_files"):
        require(type(coverage[field]) is int and coverage[field] == expected, f"Lost coverage: {field}")
    for field in ("partially_inspected_files", "entirely_uninspected_files"):
        require(type(coverage[field]) is int and coverage[field] == 0, f"Lost coverage: {field}")
    require(type(coverage["coverage_percent"]) in (int, float) and coverage["coverage_percent"] == 100,
            "Lost component coverage")
    analyzers = coverage["analyzer_statuses"]
    require(isinstance(analyzers, list), "Invalid analyzer inventory")
    actual_ids = [entry["analyzer_id"] for entry in analyzers]
    require(len(actual_ids) == len(set(actual_ids)) and set(actual_ids) == set(baseline["analyzer_statuses"]),
            "Analyzer inventory changed")
    for analyzer in analyzers:
        require(analyzer["status"] == baseline["analyzer_statuses"][analyzer["analyzer_id"]],
                "Analyzer status changed")
        for field in ("planned_work", "completed", "partial", "skipped", "failed", "unaccounted"):
            require(type(analyzer[field]) is int and analyzer[field] >= 0, "Invalid analyzer accounting")
        require(analyzer["planned_work"] == analyzer["completed"]
                and all(analyzer[field] == 0 for field in ("partial", "skipped", "failed", "unaccounted")),
                "Analyzer work was not completed")
        require((analyzer["completed"] > 0) == (analyzer["status"] == "completed"),
                "Analyzer work/status inconsistent")
        name = analyzer["analyzer_id"]
        if name.startswith("static_patterns_"):
            require(analyzer["completed"] == expected, "Static analyzer omitted supported files")
        elif name in ("artifact_integrity", "static_yara", "mcp_rug_pull"):
            require(analyzer["completed"] == len(inventory), "Artifact analyzer omitted files")
        elif name in ("behavioral_ast", "behavioral_taint_tracking"):
            python_files = sum(component["type"] == "python" for component in report["components"])
            require(analyzer["completed"] == python_files, "Behavioral analyzer omitted Python files")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--baseline", type=Path, default=ROOT / "dev-tools/scanner-baseline.json")
    parser.add_argument("--skill-dir", type=Path, default=ROOT / "skills/pixellab-pip")
    args = parser.parse_args(argv)
    try:
        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        report = json.loads(args.report.read_text(encoding="utf-8"))
        validate(report, baseline, args.skill_dir)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f"[scanner] FAIL: {error}", file=sys.stderr)
        return 1
    print(f"[scanner] PASS: score {report['risk_assessment']['score']}; findings and coverage within reviewed baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
