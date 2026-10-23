from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from test_helpers import REPO_ROOT, load_module

ASSETS = REPO_ROOT / 'skills/pixellab-pip/assets'
panel = load_module('panel', ASSETS / 'panel.py')


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.run = self.root / 'pixellab-pip-generations' / 'chosen'
        self.run.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def ledger(self, entries):
        (self.run / 'manifest.json').write_text(json.dumps({'jobs': entries}), encoding='utf-8')

    def image(self, name='hero.png', color=(12, 34, 56, 255)):
        path = self.run / name
        Image.new('RGBA', (4, 5), color).save(path)
        return path.relative_to(self.root).as_posix()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(ASSETS / 'panel.py'), *map(str, args)], capture_output=True, text=True)

    def test_private_ignore_is_local_and_existing_policy_is_preserved(self):
        top_ignore = self.run.parent / '.gitignore'
        top_ignore.write_text('keep-existing-policy\n', encoding='utf-8')
        result = self.cli(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        out = Path(json.loads(result.stdout)['snapshot']).parent
        self.assertEqual((out / '.gitignore').read_text(), '*\n')
        self.assertEqual(top_ignore.read_text(), 'keep-existing-policy\n')
        self.ledger([])
        refused = self.cli(self.root, '--out', self.run.relative_to(self.root))
        self.assertEqual(refused.returncode, 2)
        self.assertFalse((self.run / '.gitignore').exists())
        self.assertTrue((self.run / 'manifest.json').exists())
        collision = self.run.parent / 'existing-review'
        collision.mkdir()
        (collision / '.gitignore').write_text('user policy\n')
        refused = self.cli(self.root, '--out', collision.relative_to(self.root))
        self.assertEqual(refused.returncode, 2)
        self.assertEqual((collision / '.gitignore').read_text(), 'user policy\n')
        self.assertFalse((collision / 'panel.json').exists())
        refused = self.cli(self.root, '--out', 'pixellab-pip-generations')
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(top_ignore.read_text(), 'keep-existing-policy\n')

    def test_explicit_language_and_invalid_tags(self):
        result = self.cli(self.root, '--lang', 'zh-Hant')
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = json.loads(result.stdout)
        self.assertEqual(json.loads(Path(paths['snapshot']).read_text())['lang'], 'zh-Hant')
        self.assertIn('<html lang="zh-Hant">', Path(paths['panel']).read_text())
        for value in ['en" onclick="x', 'en_US', '', 'a' * 64]:
            result = self.cli(self.root, '--lang', value, '--out', 'pixellab-pip-generations/invalid')
            self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((self.run.parent / 'invalid').exists())

    def test_open_only_unchanged_standalone_and_report_browser_failure(self):
        self.ledger([])
        image = self.image()
        result = self.cli(self.root, '--run', self.run.relative_to(self.root), '--image', 'standing', image)
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = json.loads(result.stdout)
        with patch.object(panel.webbrowser, 'open', return_value=True) as browser:
            self.assertTrue(panel.open_review(paths['snapshot'])['opened'])
            browser.assert_called_once_with(Path(paths['panel']).as_uri(), new=2)
        with patch.object(panel.webbrowser, 'open', return_value=False):
            with self.assertRaisesRegex(ValueError, 'browser could not'):
                panel.open_review(paths['snapshot'])
        html_file = Path(paths['panel'])
        original = html_file.read_text(encoding='utf-8')
        for tampered in ['<script>alert(1)</script>', panel.render(json.loads(Path(paths['snapshot']).read_text()), Path(paths['snapshot']), True)]:
            html_file.write_text(tampered, encoding='utf-8')
            with patch.object(panel.webbrowser, 'open') as browser:
                with self.assertRaisesRegex(ValueError, 'differs'):
                    panel.open_review(paths['snapshot'])
                browser.assert_not_called()
        html_file.write_text(original, encoding='utf-8')
        (self.run / 'manifest.json').write_text('{"jobs":[],"changed":true}')
        with patch.object(panel.webbrowser, 'open', return_value=True):
            self.assertTrue(panel.open_review(paths['snapshot'])['opened'])
        with self.assertRaisesRegex(ValueError, 'manifest'):
            panel.verify(paths['snapshot'])

    def test_open_inspection_with_unavailable_accounting_does_not_grant_review(self):
        result = self.cli(self.root, '--run', self.run.relative_to(self.root), '--image', 'standing', self.image())
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = json.loads(result.stdout)
        snapshot = json.loads(Path(paths['snapshot']).read_text())
        self.assertFalse(snapshot['review_ready'])
        self.assertIsNone(snapshot['manifest_sha256'])
        with patch.object(panel.webbrowser, 'open', return_value=True):
            self.assertTrue(panel.open_review(paths['snapshot'])['opened'])
        with self.assertRaises(ValueError):
            panel.verify(paths['snapshot'])

    def test_unknown_failed_and_pending_costs_reuse_the_ledger(self):
        self.ledger([{'job_id': 'failed', 'status': 'failed', 'reported_usage': {'generations': 4}},
                     {'job_id': 'pending', 'status': 'submitted', 'estimated_usage': {'generations': 7}}])
        before = (self.run / 'manifest.json').read_bytes()
        result = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)))
        self.assertEqual(result['usage'], {'charged': None, 'committed': 11})
        self.assertEqual([j['status'] for j in result['jobs']], ['failed', 'submitted'])
        self.assertEqual(result['manifest_sha256'], hashlib.sha256(before).hexdigest())
        self.assertEqual((self.run / 'manifest.json').read_bytes(), before)
        self.assertTrue(result['warnings'])

    def test_empty_project_requires_no_profile_or_manifest_and_does_not_create_them(self):
        result = self.cli(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = json.loads(result.stdout)
        snapshot = json.loads(Path(paths['snapshot']).read_text(encoding='utf-8'))
        self.assertIsNone(snapshot['run'])
        self.assertEqual(snapshot['usage'], {'charged': None, 'committed': None})
        self.assertFalse((self.root / 'pixellab.json').exists())
        self.assertFalse((self.root / 'manifest.json').exists())
        self.assertEqual(set(paths), {'snapshot', 'panel'})
        self.assertNotIn('base64', result.stdout)

    def test_run_is_explicit_not_newest_and_profile_notes_are_not_exposed(self):
        self.ledger([{'job_id': 'old', 'reported_usage': {'generations': 0}}])
        other = self.run.parent / 'newer'
        other.mkdir()
        (other / 'manifest.json').write_text('{"jobs":[{"job_id":"wrong"}]}', encoding='utf-8')
        (self.root / 'pixellab.json').write_text(json.dumps({'active_style': 'chosen', 'styles': {'chosen': {'notes': 'private direction'}}}), encoding='utf-8')
        snapshot = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)))
        self.assertEqual(snapshot['style'], 'chosen')
        self.assertEqual([j['job_id'] for j in snapshot['jobs']], ['old'])
        self.assertNotIn('private direction', json.dumps(snapshot))

    def test_same_length_image_replacement_and_manifest_change_invalidate_review(self):
        self.ledger([{'job_id': 'a', 'reported_usage': {'generations': 1}}])
        relative = self.image()
        result = self.cli(self.root, '--run', self.run.relative_to(self.root), '--image', 'standing', relative)
        self.assertEqual(result.returncode, 0, result.stderr)
        path = json.loads(result.stdout)['snapshot']
        self.assertTrue(panel.verify(path)['verified'])
        image_path = self.root / relative
        original = image_path.read_bytes()
        self.image(color=(56, 34, 12, 255))
        self.assertEqual(len(image_path.read_bytes()), len(original))
        with self.assertRaisesRegex(ValueError, 'image changed'):
            panel.verify(path)
        image_path.write_bytes(original)
        self.ledger([{'job_id': 'a', 'reported_usage': {'generations': 2}}])
        with self.assertRaisesRegex(ValueError, 'manifest.*changed'):
            panel.verify(path)

    def test_path_escape_absolute_paths_and_existing_outputs_are_refused(self):
        for option in ('../outside', str(self.root), 'C:\\outside', '\\\\host\\share'):
            with self.assertRaises(ValueError):
                panel.contained(self.root, option)
        result = self.cli(self.root, '--out', '../outside')
        self.assertEqual(result.returncode, 2)
        output = self.root / 'pixellab-pip-generations' / 'review'
        output.mkdir()
        marker = output / 'panel.json'
        marker.write_text('keep', encoding='utf-8')
        result = self.cli(self.root, '--out', 'pixellab-pip-generations/review')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(marker.read_text(encoding='utf-8'), 'keep')
        self.assertFalse((output / 'panel.html').exists())

    def test_output_hardlink_cannot_overwrite_source(self):
        self.ledger([])
        output = self.root / 'pixellab-pip-generations' / 'review'
        output.mkdir()
        source = self.run / 'manifest.json'
        os.link(source, output / 'panel.json')
        before = source.read_bytes()
        result = self.cli(self.root, '--out', 'pixellab-pip-generations/review')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(source.read_bytes(), before)

    def test_symlink_input_escape_and_output_escape_are_refused(self):
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other)
            target = self.root / 'linked'
            try:
                target.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest('symlink creation unavailable: ' + str(exc))
            for relative in ('linked/image.png', 'linked/output'):
                with self.assertRaisesRegex(ValueError, 'escapes'):
                    panel.contained(self.root, relative)

    def test_unreadable_oversize_and_unpatched_previews_have_diagnostics(self):
        self.ledger([])
        relative = self.image()
        with patch.object(panel, 'load_pillow', side_effect=ImportError('Pillow 13 required')):
            data = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)), [('hero', relative)])
        self.assertEqual(data['images'], [])
        self.assertIn('Pillow 13', data['warnings'][0])
        with patch.object(panel, 'MAX_IMAGE_BYTES', 5):
            data = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)), [('hero', relative), ('missing', 'missing.png')])
        self.assertEqual(data['images'], [])
        self.assertEqual(len(data['warnings']), 2)

    def test_corrupt_profile_and_manifest_are_visible_and_preserved(self):
        profile = self.root / 'pixellab.json'
        profile.write_text('{invalid', encoding='utf-8')
        ledger = self.run / 'manifest.json'
        ledger.write_text('{invalid', encoding='utf-8')
        snapshot = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)))
        self.assertEqual(snapshot['style'], 'Style unavailable')
        self.assertIsNone(snapshot['manifest_sha256'])
        self.assertEqual(len(snapshot['warnings']), 2)
        self.assertEqual(profile.read_text(encoding='utf-8'), '{invalid')
        self.assertEqual(ledger.read_text(encoding='utf-8'), '{invalid')

    def test_html_contains_real_payload_without_script_injection_and_fragment_is_available(self):
        self.ledger([{'job_id': '</script><script>alert(1)</script>', 'reported_usage': {'generations': 0}}])
        relative = self.image()
        snapshot = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)), [('windup', relative)])
        markup = panel.render(snapshot, self.run / 'panel' / 'panel.json')
        self.assertNotIn('</script><script>alert(1)</script>', markup)
        self.assertIn('\\u003c/script\\u003e', markup)
        self.assertIn('connect-src \'none\'', markup)
        fragment = panel.render(snapshot, self.run / 'panel' / 'panel.json', True)
        self.assertFalse(fragment.startswith('<!doctype'))
        self.assertIn('data:image/png;base64,', fragment)

    def test_verification_binds_displayed_bytes_as_well_as_original_files(self):
        self.ledger([])
        relative = self.image()
        snapshot = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)), [('hero', relative)])
        snapshot['images'][0]['data_url'] = 'data:image/png;base64,Y2hhbmdlZA=='
        path = self.run / 'tampered.json'
        path.write_text(json.dumps(snapshot), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'displayed image'):
            panel.verify(str(path))

    def test_job_display_is_bounded_without_changing_whole_run_usage(self):
        self.ledger([{'job_id': str(i), 'reported_usage': {'generations': 1}} for i in range(205)])
        snapshot = panel.build_snapshot(str(self.root), str(self.run.relative_to(self.root)))
        self.assertEqual(len(snapshot['jobs']), panel.MAX_JOBS)
        self.assertEqual(snapshot['usage'], {'charged': 205, 'committed': 205})
        self.assertIn('usage covers all', snapshot['warnings'][0])

    def test_oversize_inline_fragment_requires_standalone_render(self):
        snapshot = panel.build_snapshot(str(self.root))
        snapshot['style'] = 'x' * 1_000_000
        with self.assertRaisesRegex(ValueError, '1 MB'):
            panel.render(snapshot, self.root / 'panel.json', True)
        self.assertTrue(panel.render(snapshot, self.root / 'panel.json').startswith('<!doctype'))

    def test_localized_labels_are_literal_and_only_known_keys_are_accepted(self):
        path = self.root / 'panel-labels.json'
        translations = {'title': 'Revisión </script><script>invalid()</script>', 'project': 'Proyecto', 'style_none': 'Sin estilo'}
        path.write_text(json.dumps(translations), encoding='utf-8')
        original = path.read_bytes()
        snapshot = panel.build_snapshot(str(self.root), labels='panel-labels.json')
        self.assertEqual(snapshot['labels']['project'], 'Proyecto')
        self.assertEqual(snapshot['style'], 'Sin estilo')
        self.assertEqual(set(snapshot['labels']), set(panel.DEFAULT_LABELS))
        rendered = panel.render(snapshot, self.root / 'panel.json')
        self.assertNotIn('</script><script>invalid()', rendered)
        self.assertEqual(path.read_bytes(), original)
        for contents in ('{"typo":"text"}', '{"title":[]}', '{"title":" "}', '{broken'):
            path.write_text(contents, encoding='utf-8')
            with self.assertRaises(ValueError):
                panel.build_snapshot(str(self.root), labels='panel-labels.json')
            self.assertEqual(path.read_text(encoding='utf-8'), contents)

    def test_outputs_with_embedded_private_paths_stay_in_generation_directory(self):
        result = self.cli(self.root, '--out', 'review')
        self.assertEqual(result.returncode, 2)
        self.assertIn('pixellab-pip-generations', result.stderr)
        self.assertFalse((self.root / 'review').exists())

    def test_accounting_and_style_warnings_do_not_block_prepared_review_requests(self):
        self.ledger([{'job_id': 'unknown', 'status': 'failed'}])
        (self.root / 'pixellab.json').write_text('{invalid', encoding='utf-8')
        relative = self.image()
        run = str(self.run.relative_to(self.root))
        snapshot = panel.build_snapshot(str(self.root), run, [('hero', relative)])
        self.assertTrue(snapshot['warnings'])
        self.assertTrue(snapshot['review_ready'])
        snapshot = panel.build_snapshot(str(self.root), run, [('hero', relative), ('missing', 'absent.png')])
        self.assertFalse(snapshot['review_ready'])

    def test_alternate_run_source_stays_unchanged_with_private_default_output(self):
        alternate = self.root / 'art' / 'hero'
        alternate.mkdir(parents=True)
        ledger = alternate / 'manifest.json'
        ledger.write_text('{"jobs":[{"job_id":"a","reported_usage":{"generations":2}}]}', encoding='utf-8')
        image = alternate / 'hero.png'
        Image.new('RGBA', (3, 4), (100, 80, 60, 255)).save(image)
        before = {path: path.read_bytes() for path in (ledger, image)}
        result = self.cli(self.root, '--run', 'art/hero', '--image', 'standing', 'art/hero/hero.png')
        self.assertEqual(result.returncode, 0, result.stderr)
        paths = json.loads(result.stdout)
        snapshot_file = Path(paths['snapshot'])
        self.assertTrue(snapshot_file.is_relative_to(self.root / 'pixellab-pip-generations'))
        snapshot = json.loads(snapshot_file.read_text(encoding='utf-8'))
        self.assertEqual(snapshot['run'], 'art/hero')
        self.assertTrue(snapshot['review_ready'])
        self.assertEqual(snapshot['usage']['charged'], 2)
        self.assertTrue(panel.verify(str(snapshot_file))['verified'])
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)
        self.assertFalse((alternate / 'panel').exists())
        self.assertFalse((self.root / 'pixellab.json').exists())

    def test_private_generation_root_cannot_redirect_outputs_into_tracked_art(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            art = root / 'art'
            art.mkdir()
            try:
                (root / 'pixellab-pip-generations').symlink_to(art, target_is_directory=True)
            except OSError as exc:
                self.skipTest('symlink creation unavailable: ' + str(exc))
            result = self.cli(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn('must not redirect', result.stderr)
            self.assertEqual(list(art.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
