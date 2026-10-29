"""Exercise accidental risk, failed-scan and missing-coverage regressions offline."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_helpers import REPO_ROOT, load_module


guard = load_module("check_scanner", REPO_ROOT / "dev-tools/check_scanner.py")


class ScannerGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "skill"
        self.skill.mkdir()
        self.baseline = json.loads((REPO_ROOT / "dev-tools/scanner-baseline.json").read_text(encoding="utf-8"))
        names = {"SKILL.md", "assets/bark.wav"} | {entry["path"] for entry in self.baseline["findings"]}
        for name in names:
            path = self.skill / name
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_bytes(b"fixture")
        self.report = {
            "skill": {"source": str(self.skill)},
            "metadata": {"skillspector_version": self.baseline["scanner_version"],
                         "llm_requested": False, "llm_available": False,
                         "meta_analysis_applied": False, "inference_usage": [], "filtering_mode": "heuristic"},
            "suppressed_count": 0, "suppressed": [], "execution_successful": True,
            "risk_assessment": deepcopy(self.baseline["risk_assessment"]),
            "components": [{"path": name, "type": "python" if name.endswith(".py") else "markdown"}
                           for name in sorted(names)],
            "issues": [{"id": entry["id"], "severity": entry["severity"], "location": {"file": entry["path"]}}
                       for entry in self.baseline["findings"] for _ in range(entry["count"])],
            "analysis_completeness": {
                "execution_successful": True, "status": "partial", "is_complete": False,
                "total_components": len(names) - 1, "scanned_components": len(names) - 1,
                "fully_inspected_files": len(names) - 1, "coverage_percent": 100,
                "partially_inspected_files": 0, "entirely_uninspected_files": 0,
                "limitations": [], "findings_before_filtering": 38, "findings_after_filtering": 38,
                "ledger_exceptions": [dict(entry, fatal=False) for entry in self.baseline["ledger_exceptions"]
                                      for _ in range(entry["count"])],
                "scope_exclusions": [dict(entry, fatal=False) for entry in self.baseline["scope_exclusions"]
                                     for _ in range(entry["count"])],
                "analyzer_statuses": [
                    {"analyzer_id": name, "status": status, "planned_work": int(status == "completed"),
                     "completed": int(status == "completed"), "partial": 0,
                     "skipped": 0, "failed": 0, "unaccounted": 0}
                    for name, status in self.baseline["analyzer_statuses"].items()],
            },
        }
        self.update_work_counts()

    def update_work_counts(self):
        for analyzer in self.report["analysis_completeness"]["analyzer_statuses"]:
            name = analyzer["analyzer_id"]
            count = analyzer["completed"]
            if name.startswith("static_patterns_"):
                count = len(self.report["components"]) - 1
            elif name in ("artifact_integrity", "static_yara", "mcp_rug_pull"):
                count = len(self.report["components"])
            analyzer.update(completed=count, planned_work=count)

    def check(self, report=None):
        guard.validate(report if report is not None else self.report, self.baseline, self.skill)

    def test_reviewed_partial_report_and_real_improvements_pass(self):
        self.check()
        self.report["issues"][0]["severity"] = "LOW"
        self.check()
        self.report["issues"] = []
        self.report["analysis_completeness"].update(findings_before_filtering=0, findings_after_filtering=0)
        self.report["risk_assessment"].update(score=0, severity="LOW", recommendation="SAFE", max_issue_severity="NONE")
        self.check()

    def test_new_supported_file_is_allowed_when_fully_scanned(self):
        (self.skill / "new-guide.md").write_text("fixture", encoding="utf-8")
        self.report["components"].append({"path": "new-guide.md", "type": "markdown"})
        for field in ("total_components", "scanned_components", "fully_inspected_files"):
            self.report["analysis_completeness"][field] += 1
        self.update_work_counts()
        self.check()

    def test_worse_score_or_rating_and_invalid_numeric_scores_fail(self):
        for field, values in {"score": [18, -1, True, float("nan"), float("inf"), "17"],
                              "severity": ["MEDIUM", "unknown"],
                              "recommendation": ["DO_NOT_INSTALL"],
                              "max_issue_severity": ["HIGH"]}.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    report = deepcopy(self.report)
                    report["risk_assessment"][field] = value
                    with self.assertRaises(ValueError):
                        self.check(report)

    def test_new_path_rule_severity_and_count_fail_even_without_score_increase(self):
        for change in ("id", "path", "severity", "count"):
            report = deepcopy(self.report)
            if change == "id":
                report["issues"][0]["id"] = "NEW"
            elif change == "path":
                report["issues"][0]["location"]["file"] = "SKILL.md"
            elif change == "severity":
                report["issues"][0]["severity"] = "HIGH"
            else:
                report["issues"].append(deepcopy(report["issues"][0]))
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check(report)

    def test_bad_execution_suppression_or_nonstatic_evidence_fail(self):
        changes = [("execution_successful", False), ("suppressed_count", 1), ("suppressed", [{}])]
        for field, value in changes:
            report = deepcopy(self.report)
            report[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.check(report)
        for field, value in (("skillspector_version", "different"), ("llm_requested", True),
                             ("llm_available", True), ("meta_analysis_applied", True),
                             ("inference_usage", [{}]), ("filtering_mode", "other")):
            report = deepcopy(self.report)
            report["metadata"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.check(report)

    def test_wrong_subset_duplicate_and_unsafe_component_paths_fail(self):
        for mode in ("wrong-source", "subset", "empty", "duplicate", "traversal", "absolute"):
            report = deepcopy(self.report)
            if mode == "wrong-source":
                report["skill"]["source"] = str(self.skill.parent)
            elif mode == "subset":
                report["components"].pop()
            elif mode == "empty":
                report["components"] = []
            elif mode == "duplicate":
                report["components"].append(report["components"][0])
            else:
                report["components"][0]["path"] = "../SKILL.md" if mode == "traversal" else "/SKILL.md"
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.check(report)

    def test_new_fatal_or_worse_coverage_fails(self):
        for mode in ("exception", "fatal", "exclusion", "partially_inspected_files", "entirely_uninspected_files",
                     "scanned_components", "coverage_percent", "execution_successful", "analyzer-missing", "analyzer-disabled", "analyzer-failed",
                     "analyzer-underreported", "limitations", "findings_after_filtering"):
            report = deepcopy(self.report)
            coverage = report["analysis_completeness"]
            if mode == "exception":
                coverage["ledger_exceptions"].append(deepcopy(coverage["ledger_exceptions"][0]))
            elif mode == "fatal":
                coverage["ledger_exceptions"][0]["fatal"] = True
            elif mode == "exclusion":
                coverage["scope_exclusions"].append(dict(coverage["scope_exclusions"][0], path="SKILL.md"))
            elif mode == "analyzer-missing":
                coverage["analyzer_statuses"].pop()
            elif mode == "analyzer-disabled":
                coverage["analyzer_statuses"][0].update(status="disabled", planned_work=0, completed=0)
            elif mode == "analyzer-failed":
                coverage["analyzer_statuses"][0]["failed"] = 1
            elif mode == "analyzer-underreported":
                coverage["analyzer_statuses"][0].update(planned_work=1, completed=1)
            elif mode == "limitations":
                coverage["limitations"] = ["transitive analysis truncated"]
            else:
                coverage[mode] = False if mode == "execution_successful" else 1
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.check(report)

    def test_cli_missing_invalid_and_malformed_reports_fail_closed(self):
        report_path = self.skill.parent / "report.json"
        command = [sys.executable, str(REPO_ROOT / "dev-tools/check_scanner.py"),
                   str(report_path), "--skill-dir", str(self.skill)]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        for raw in ("{", "{}", "null", "[]", "17", '{"execution_successful":true}'):
            report_path.write_text(raw, encoding="utf-8")
            with self.subTest(raw=raw):
                self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        for value in ({}, "", None, [None]):
            report = deepcopy(self.report)
            report["issues"] = value
            report_path.write_text(json.dumps(report), encoding="utf-8")
            with self.subTest(issues=value):
                self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        report_path.write_text(json.dumps(self.report), encoding="utf-8")
        # Defaults resolve from the repository, even from an unrelated working directory.
        result = subprocess.run(command, cwd=self.skill.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
