from __future__ import annotations

from contextlib import redirect_stdout
from datetime import date
import io
import json
from pathlib import Path
import tempfile
import unittest

from test_helpers import REPO_ROOT, load_module

ASSETS = REPO_ROOT / 'skills/pixellab-pip/assets'
manifest = load_module('manifest', ASSETS / 'manifest.py')
history = load_module('history', ASSETS / 'history.py')


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, run, job, stamp=None, usage=2, tool='MCP animate_image'):
        entry = {'job_id': job, 'tool': tool, 'reported_usage': {'generations': usage}, 'status': 'ok'}
        if stamp:
            entry['created_at'] = stamp
        manifest.add_job(str(self.root / run), entry)

    def test_searches_all_runs_before_limiting(self):
        for i in range(15):
            self.add('run-%02d' % i, 'job-%02d' % i, '2026-01-%02dT12:00:00+00:00' % (i + 1))
        self.assertEqual(len(history.history(str(self.root), 20)), 15)
        rows = history.history(str(self.root), 1, job='job-00')
        self.assertEqual(rows[0]['name'], 'run-00')
        self.assertEqual(rows[0]['entries'][0]['job_id'], 'job-00')

    def test_date_bounds_are_inclusive_and_do_not_use_mtime(self):
        self.add('old', 'a', '2026-01-01T23:59:59Z')
        self.add('next', 'b', '2026-01-02T00:00:00Z')
        path = self.root / 'undated'
        path.mkdir()
        (path / 'manifest.json').write_text(json.dumps({'jobs': [{'job_id': 'c', 'status': 'ok'}]}), encoding='utf-8')
        rows = history.history(str(self.root), 10, since=date(2026, 1, 1), until=date(2026, 1, 1))
        self.assertEqual([r['name'] for r in rows], ['old'])
        rows = {r['name']: r for r in history.history(str(self.root), 10)}
        self.assertIsNone(rows['undated']['created_at'])
        self.assertIsNone(rows['undated']['spent'])
        self.assertEqual(rows['undated']['unknown_dates'], 1)

    def test_matches_tool_case_insensitively_and_reports_only_matching_calls(self):
        self.add('mixed', 'a', '2026-01-01T00:00:00Z', 2)
        self.add('mixed', 'b', '2026-01-02T00:00:00Z', 6, 'MCP edit_image')
        rows = history.history(str(self.root), 10, tool='EDIT')
        self.assertEqual(rows[0]['jobs'], 1)
        self.assertEqual(rows[0]['spent'], 6)
        self.assertEqual(rows[0]['entries'][0]['job_id'], 'b')

    def test_failed_charge_is_reported_and_estimates_stay_unknown_actual(self):
        self.add('known', 'a', usage=5)
        manifest.add_job(str(self.root / 'known'), {'job_id': 'a', 'status': 'failed'})
        manifest.add_job(str(self.root / 'unknown'), {'job_id': 'b', 'status': 'failed',
                                                    'estimated_usage': {'generations': 7}})
        rows = {r['name']: r for r in history.history(str(self.root), 10)}
        self.assertEqual(rows['known']['spent'], 5)
        self.assertIsNone(rows['unknown']['spent'])
        self.assertEqual(rows['unknown']['committed'], 7)

    def test_invalid_manifest_is_reported_without_hiding_other_runs(self):
        self.add('valid', 'a')
        path = self.root / 'bad'
        path.mkdir()
        (path / 'manifest.json').write_text('{"calls": []}', encoding='utf-8')
        rows = {r['name']: r for r in history.history(str(self.root), 10)}
        self.assertIn('error', rows['bad'])
        self.assertEqual(rows['valid']['spent'], 2)

    def test_older_manifests_never_push_runs_out_of_the_limit(self):
        # review: 11 older-format manifests filled --runs 10 and hid the one real run
        for i in range(11):
            (self.root / ('old%02d' % i)).mkdir()
            (self.root / ('old%02d' % i) / 'manifest.json').write_text('{"calls": []}', encoding='utf-8')
        self.add('valid', 'a')
        rows = history.history(str(self.root), 10)
        self.assertEqual(rows[0]['name'], 'valid')
        self.assertEqual(sum('error' in r for r in rows), 11)
        out = io.StringIO()
        with redirect_stdout(out):
            history.main(['--root', str(self.root)])
        text = out.getvalue()
        self.assertIn('valid: 1 jobs', text)
        self.assertIn('11 manifests are not run ledgers', text)
        self.assertNotIn('invalid manifest', text)


if __name__ == '__main__':
    unittest.main()
