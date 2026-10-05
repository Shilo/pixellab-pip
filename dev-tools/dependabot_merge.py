#!/usr/bin/env python3
"""Wait for the existing CI gates before merging a verified Dependabot update."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time


REQUIRED_CHECKS = {
    "Repository QA": "Quality Assurance",
    "SkillSpector skill audit": "Skill Security Audit",
    "HOL Plugin Scanner": "HOL Plugin Scanner",
}


def verify_commit(pages: list[list[dict]], expected_head: str) -> None:
    commits = [commit for page in pages for commit in page]
    if (
        len(commits) != 1
        or commits[0]["sha"] != expected_head
        or (commits[0].get("author") or {}).get("login") != "dependabot[bot]"
        or commits[0]["commit"]["verification"].get("verified") is not True
    ):
        raise RuntimeError("Expected one signed Dependabot commit; leave the PR open.")


def checks_passed(pr: dict, expected_head: str) -> bool:
    if (
        pr["state"] != "OPEN"
        or pr["isDraft"]
        or pr["baseRefName"] != "main"
        or pr["headRefOid"] != expected_head
    ):
        raise RuntimeError("PR is no longer eligible or its commit changed; leave it open.")

    ready = True
    for name, workflow in REQUIRED_CHECKS.items():
        checks = [
            check
            for check in pr["statusCheckRollup"]
            if check.get("__typename") == "CheckRun"
            and check.get("name") == name
            and check.get("workflowName") == workflow
        ]
        if len(checks) != 1:
            ready = False
            continue
        check = checks[0]
        if check.get("status") != "COMPLETED":
            ready = False
        elif check.get("conclusion") != "SUCCESS":
            raise RuntimeError(f"{name} did not succeed; leave the PR open.")
    return ready


def wait_for_checks(pr_number: str, expected_head: str) -> None:
    verify_commit(
        json.loads(subprocess.check_output(
            [
                "gh", "api",
                f"repos/{os.environ['GH_REPO']}/pulls/{pr_number}/commits?per_page=100",
                "--paginate", "--slurp",
            ],
            text=True,
            timeout=60,
        )),
        expected_head,
    )
    deadline = time.monotonic() + 20 * 60
    while time.monotonic() < deadline:
        pr = json.loads(
            subprocess.check_output(
                [
                    "gh", "pr", "view", pr_number, "--json",
                    "state,isDraft,baseRefName,headRefOid,statusCheckRollup",
                ],
                text=True,
                timeout=60,
            )
        )
        if checks_passed(pr, expected_head):
            print("All three required CI checks succeeded for the expected commit.")
            return
        time.sleep(15)
    raise RuntimeError("CI did not finish within 20 minutes; leave the PR open.")


if __name__ == "__main__":
    try:
        wait_for_checks(*sys.argv[1:])
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
