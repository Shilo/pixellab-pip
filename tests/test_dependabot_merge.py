from __future__ import annotations

import textwrap
import types
import json
import unittest
from pathlib import Path
from unittest.mock import patch


workflow_path = Path(__file__).resolve().parents[1] / ".github/workflows/dependabot-merge.yml"
workflow = workflow_path.read_text(encoding="utf-8")
source = textwrap.dedent(workflow.split("python3 - <<'PY'\n", 1)[1].split("\n          PY", 1)[0])
merge = types.ModuleType("dependabot_merge")
exec(compile(source, str(workflow_path), "exec"), merge.__dict__)


def passing_pr() -> dict:
    return {
        "state": "OPEN", "isDraft": False, "baseRefName": "main", "headRefOid": "expected",
        "statusCheckRollup": [
            {
                "__typename": "CheckRun", "name": name, "workflowName": workflow,
                "status": "COMPLETED", "conclusion": "SUCCESS",
            }
            for name, workflow in merge.REQUIRED_CHECKS.items()
        ],
    }


def verified_commit() -> dict:
    return {
        "sha": "expected", "author": {"login": "dependabot[bot]"},
        "commit": {"verification": {"verified": True}},
    }


class DependabotMergeTests(unittest.TestCase):
    def test_privileged_workflow_has_no_checkout(self):
        self.assertNotIn("actions/checkout@", workflow)
        self.assertNotIn("git checkout", workflow)

    def test_requires_one_signed_bot_commit_at_the_expected_head(self):
        merge.verify_commit([[verified_commit()]], "expected")
        for commits in ([], [verified_commit(), verified_commit()]):
            with self.subTest(commits=len(commits)), self.assertRaises(RuntimeError):
                merge.verify_commit([commits], "expected")
        for field, value in (
            ("sha", "changed"), ("author", None),
            ("author", {"login": "maintainer"}),
            ("commit", {"verification": {"verified": False}}),
        ):
            commit = verified_commit()
            commit[field] = value
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                merge.verify_commit([[commit]], "expected")

    def test_all_required_checks_must_succeed(self):
        self.assertTrue(merge.checks_passed(passing_pr(), "expected"))
        for status in ("QUEUED", "IN_PROGRESS"):
            pr = passing_pr()
            pr["statusCheckRollup"][0]["status"] = status
            self.assertFalse(merge.checks_passed(pr, "expected"))

    def test_missing_duplicate_and_wrong_workflow_checks_do_not_pass(self):
        for change in ("missing", "duplicate", "wrong_workflow", "wrong_type"):
            pr = passing_pr()
            checks = pr["statusCheckRollup"]
            if change == "missing":
                checks.pop()
            elif change == "duplicate":
                checks.append(checks[0].copy())
            elif change == "wrong_workflow":
                checks[0]["workflowName"] = "Unrelated workflow"
            else:
                checks[0]["__typename"] = "StatusContext"
            with self.subTest(change=change):
                self.assertFalse(merge.checks_passed(pr, "expected"))

    def test_failed_skipped_cancelled_and_unknown_results_abort(self):
        for result in ("FAILURE", "SKIPPED", "CANCELLED", "NEUTRAL", "TIMED_OUT", None):
            pr = passing_pr()
            pr["statusCheckRollup"][0]["conclusion"] = result
            with self.subTest(result=result), self.assertRaises(RuntimeError):
                merge.checks_passed(pr, "expected")

    def test_changed_commit_closed_draft_or_retargeted_pr_aborts(self):
        for field, value in (
            ("headRefOid", "changed"), ("state", "CLOSED"),
            ("isDraft", True), ("baseRefName", "other"),
        ):
            pr = passing_pr()
            pr[field] = value
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                merge.checks_passed(pr, "expected")

    def test_wait_rechecks_pending_checks_then_returns(self):
        pending = passing_pr()
        pending["statusCheckRollup"] = []
        with (
            patch.dict(merge.os.environ, {"GH_REPO": "owner/repo"}),
            patch.object(merge.subprocess, "check_output", side_effect=[
                json.dumps([[verified_commit()]]), json.dumps(pending), json.dumps(passing_pr()),
            ]) as read,
            patch.object(merge.time, "sleep") as sleep,
        ):
            merge.wait_for_checks("1", "expected")
        self.assertEqual(read.call_count, 3)
        sleep.assert_called_once_with(15)

    def test_wait_deadline_aborts(self):
        with (
            patch.dict(merge.os.environ, {"GH_REPO": "owner/repo"}),
            patch.object(merge.time, "monotonic", side_effect=[0, 1201]),
            patch.object(merge.subprocess, "check_output", return_value=json.dumps([[verified_commit()]])) as read,
            self.assertRaisesRegex(RuntimeError, "20 minutes"),
        ):
            merge.wait_for_checks("1", "expected")
        self.assertEqual(read.call_count, 1)
