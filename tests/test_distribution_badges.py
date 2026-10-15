from __future__ import annotations

import json
import io
import textwrap
import types
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError


workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/distribution-badges.yml").read_text(encoding="utf-8")
source = textwrap.dedent(workflow.split("python3 - <<'PY'\n", 1)[1].split("\n          PY", 1)[0])
badges = types.ModuleType("distribution_badges")
exec(compile(source, "distribution-badges.yml", "exec"), badges.__dict__)


class DistributionBadgeTests(unittest.TestCase):
    def test_downloads_paginate_and_exclude_drafts(self):
        published = {"draft": False, "assets": [{"download_count": 2}]}
        draft = {"draft": True, "assets": [{"download_count": 999}]}
        with patch.object(badges, "request", side_effect=[[published] * 99 + [draft], [published]]) as request:
            self.assertEqual(badges.github_downloads("owner/repo", "token"), 200)
        self.assertIn("page=2", request.call_args.args[0])

    def test_source_total_stays_separate_from_clones_and_credentials(self):
        def request(url, token="", *args):
            if url == badges.CLAWHUB_URL:
                self.assertEqual(token, "")
                return {"skill": {"stats": {"downloads": 1359, "installs": 3}}}
            self.assertEqual(token, "traffic-secret")
            return {"count": 1232, "uniques": 389}

        with patch.object(badges, "request", side_effect=request), patch.object(badges, "github_downloads", return_value=42):
            files, failures = badges.collect("owner/repo", "write-secret", "traffic-secret", "2026-10-15T10:00:00+00:00")
        self.assertEqual(failures, [])
        self.assertEqual(files["downloads.json"]["message"], "1,401")
        self.assertEqual(files["clones.json"]["message"], "1,232 · 2026-10-15")
        self.assertNotIn("secret", json.dumps(files))

    def test_download_failure_never_publishes_partial_total_or_fake_zero(self):
        with patch.object(badges, "request", side_effect=[
            {"skill": {"stats": {"downloads": 100}}}, {"count": 0},
        ]), patch.object(badges, "github_downloads", side_effect=ValueError("bad response")):
            files, failures = badges.collect("owner/repo", "token", "traffic-token", "2026-10-15T10:00:00+00:00")
        self.assertEqual(files["downloads.json"]["message"], "unavailable")
        self.assertIsNone(files["metrics.json"]["downloads"])
        self.assertEqual(files["clones.json"]["message"], "0 · 2026-10-15")
        self.assertEqual(len(failures), 1)

    def test_clone_auth_failure_preserves_downloads_without_old_clone_value(self):
        with patch.object(badges, "request", side_effect=[
            {"skill": {"stats": {"downloads": 100}}},
            HTTPError("url", 403, "Forbidden", {}, None),
        ]), patch.object(badges, "github_downloads", return_value=20):
            files, failures = badges.collect("owner/repo", "token", "traffic-token", "2026-10-15T10:00:00+00:00")
        self.assertEqual(files["downloads.json"]["message"], "120")
        self.assertEqual(files["clones.json"]["message"], "unavailable")
        self.assertIsNone(files["metrics.json"]["clones"])
        self.assertEqual(len(failures), 1)

    def test_invalid_counters_cannot_be_published(self):
        for value in (None, True, -1, 1.5, "12"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                badges.count(value)

    def test_missing_traffic_credential_does_not_reuse_write_credential(self):
        with patch.object(badges, "request", return_value={"skill": {"stats": {"downloads": 0}}}) as request, \
                patch.object(badges, "github_downloads", return_value=0):
            files, failures = badges.collect("owner/repo", "write-token", "", "2026-10-15T10:00:00+00:00")
        self.assertEqual(request.call_args_list, [unittest.mock.call(badges.CLAWHUB_URL)])
        self.assertEqual(files["downloads.json"]["message"], "0")
        self.assertEqual(files["clones.json"]["message"], "unavailable")
        self.assertEqual(len(failures), 1)

    def test_get_retries_transient_failures_with_a_bound(self):
        for error in (URLError("offline"), HTTPError("url", 503, "Unavailable", {}, None)):
            with self.subTest(error=type(error).__name__), \
                    patch.object(badges, "urlopen", side_effect=[error, io.BytesIO(b'{"count": 7}')]) as open_url, \
                    patch.object(badges.time, "sleep") as sleep:
                self.assertEqual(badges.request("https://api.github.com/repos/owner/repo", "token"), {"count": 7})
            self.assertEqual(open_url.call_count, 2)
            sleep.assert_called_once_with(1)
            headers = dict(open_url.call_args.args[0].header_items())
            self.assertEqual(headers["X-github-api-version"], "2026-03-10")
        with patch.object(badges, "urlopen", side_effect=URLError("offline")) as open_url, \
                patch.object(badges.time, "sleep") as sleep, self.assertRaises(URLError):
            badges.request("https://example.test/stats")
        self.assertEqual(open_url.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    def test_request_does_not_retry_auth_rate_limits_or_writes(self):
        for method, status in (("GET", 401), ("GET", 403), ("GET", 429), ("POST", 503), ("PATCH", 503)):
            with self.subTest(method=method, status=status), \
                    patch.object(badges, "urlopen", side_effect=HTTPError("url", status, "Failure", {}, None)) as open_url, \
                    patch.object(badges.time, "sleep") as sleep, self.assertRaises(HTTPError):
                badges.request("https://api.github.com/test", "token", method)
            open_url.assert_called_once()
            sleep.assert_not_called()

    def test_main_publishes_unavailable_state_before_failing_the_job(self):
        files = {"downloads.json": {"message": "unavailable"}}
        with patch.dict(badges.os.environ, {"GH_REPO": "owner/repo", "GH_TOKEN": "token"}), \
                patch.object(badges, "collect", return_value=(files, ["Downloads unavailable."])), \
                patch.object(badges, "publish") as publish, patch("builtins.print") as output, \
                self.assertRaises(SystemExit) as failure:
            badges.main()
        self.assertEqual(failure.exception.code, 1)
        publish.assert_called_once_with("owner/repo", "token", files)
        output.assert_any_call("::error::Downloads unavailable.")

    def test_main_success_and_workflow_triggers(self):
        with patch.dict(badges.os.environ, {"GH_REPO": "owner/repo", "GH_TOKEN": "token"}), \
                patch.object(badges, "collect", return_value=({}, [])), patch.object(badges, "publish"), \
                patch("builtins.print"):
            badges.main()
        self.assertIn("github.repository == 'Shilo/pixellab-pip'", workflow)
        self.assertIn("workflows: [Release New Version]", workflow)
        self.assertIn("schedule:", workflow)
        self.assertIn("workflow_dispatch:", workflow)

    def test_publish_creates_or_updates_only_data_branch_without_force(self):
        for exists in (True, False):
            calls = []

            def request(url, token, method="GET", data=None):
                calls.append((url, method, data))
                if method == "GET":
                    if not exists:
                        raise HTTPError(url, 404, "Not Found", {}, None)
                    return {"object": {"sha": "parent"}}
                return {"sha": "new"}

            with self.subTest(exists=exists), patch.object(badges, "request", side_effect=request):
                badges.publish("owner/repo", "token", {"downloads.json": {"message": "10"}})
            self.assertNotIn("main", json.dumps(calls))
            self.assertEqual(calls[2][2]["parents"], ["parent"] if exists else [])
            if exists:
                self.assertFalse(calls[-1][2]["force"])
            else:
                self.assertEqual(calls[-1][2]["ref"], "refs/heads/codex/badges")
        self.assertNotIn("actions/checkout", workflow)
        self.assertNotIn("pull_request", workflow)
