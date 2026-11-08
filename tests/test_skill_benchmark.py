from pathlib import Path
import os
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_helpers import REPO_ROOT, load_module

benchmark = load_module('skill_benchmark', REPO_ROOT / 'dev-tools/skill_benchmark.py')
SCENARIOS = {s['id']: s for s in benchmark.SCENARIOS}


class BenchmarkTests(unittest.TestCase):
    def test_supported_routes_are_not_graded_as_pip_preferences(self):
        cases = [
            ('route-background-scene', 'create_image_pixflux'),
            ('route-background-scene', 'create_image_pixen'),
            ('route-background-scene', 'create_image_pro for the forest clearing'),
            ('plan-item-icon-sheet', 'create_image_pixen per concept, assemble one sheet'),
            ('plan-item-icon-sheet', 'create_image_pixen once at 256x256 for one sheet of 64 icons'),
            ('plan-item-icon-sheet', 'create_image_pro complete 8x8 sheet; verify every icon and alpha'),
            ('route-skill-icons', 'create_image_pro, verify sheet layout'),
            ('route-skill-icons', 'generate-with-style-v2; verify the sheet'),
            ('plan-item-icon-sheet', 'generate-with-style-v2; pack the sheet'),
            ('route-tiles-vs-tileset', 'create_tiles_pro independent tiles, pack a grid'),
            ('route-tiles-vs-tileset', 'create_image_pro_flash per texture, assemble a grid'),
            ('route-tiles-vs-tileset', 'create_image_pro grid of separate texture tiles'),
            ('route-tiles-vs-tileset', 'create_tiles_pro grid, not a seamless connecting tileset'),
            ('route-tiles-vs-tileset', 'create_tiles_pro grid of non-connecting textures'),
            ('route-tiles-vs-tileset', 'create_tiles_pro nonconnecting texture sheet'),
            ('route-object-prop', 'create_image_pro_flash'),
            ('route-object-prop', 'generate-image-v2 (10 generations) for one chest'),
            ('route-object-prop', 'create_map_object for the chest'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset with palette, approved palette variant'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset in 1-bit; apply the Game Boy palette'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset target_palette for the approved green derivative'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset; local recolour to the Game Boy palette'),
            ('cheap-animation', 'get_character size; compare animate_character template and v3 costs'),
            ('cheap-animation', 'animate_character v3 at 2 generations per approved direction'),
            ('cheap-animation', 'animate_character pixminimax: 40 frames, 8 directions, about 48 generations'),
            ('cheap-animation', 'compare credit costs for animate_character v3 and pixminimax'),
            ('cheap-animation', 'animate_character v3 for $0.03; verify the generated canvas'),
            ('cheap-animation', 'compare v3 and pixminimax costs for animate_character'),
            ('cheap-animation', 'animate_character v3 is cheaper than pixminimax for this canvas'),
            ('cheap-animation', "Do not use animate_character(mode='pro'); compare template and v3 costs"),
        ]
        for scenario, response in cases:
            with self.subTest(scenario=scenario, response=response):
                self.assertTrue(all(benchmark.apply_checks(SCENARIOS[scenario], response).values()))

    def test_wrong_routes_and_missing_structure_fail(self):
        cases = [
            ('route-background-scene', 'create_background'),
            ('route-background-scene', 'create_image_pro_fake'),
            ('route-background-scene', 'create-image-pro-fake'),
            ('route-object-prop', 'create_object_state'),
            ('plan-item-icon-sheet', 'create_image_pixen'),
            ('route-tiles-vs-tileset', 'create_topdown_tileset'),
            ('route-tiles-vs-tileset', 'create_tiles_pro for a seamless connecting grid'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset using a 1-bit palette'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset with 1-bit palette; separately generate a new green set'),
            ('cheap-animation', "animate_character(mode='pro') 8 frames"),
            ('cheap-animation', 'animate_character mode=pixminimax with 40 frames, all 8 directions'),
            ('cheap-animation', 'animate_character v3; inspect canvas size and frame count'),
        ]
        for scenario, response in cases:
            with self.subTest(scenario=scenario, response=response):
                self.assertFalse(all(benchmark.apply_checks(SCENARIOS[scenario], response).values()))

    def test_template_mentions_are_routes_without_cost_evidence(self):
        for response in ('animate_character with walking-8-frames template',
                         "animate_character(mode='pro') with the walking template",
                         'animate_character v3 mode; no template needed'):
            with self.subTest(response=response):
                self.assertEqual(benchmark.apply_checks(SCENARIOS['cheap-animation'], response),
                                 {'route': True, 'cost_basis': False})

    @unittest.skipUnless(os.name == 'nt', 'Windows directory junctions')
    def test_current_export_rejects_native_junction_ancestor(self):
        shell = shutil.which('pwsh') or shutil.which('powershell')
        if not shell:
            self.skipTest('PowerShell unavailable for native junction fixture')
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary).resolve()
            root = fixture / 'repo'
            source = root / benchmark.SKILL_REL
            link = source / 'references'
            link.mkdir(parents=True)
            (source / 'SKILL.md').write_text('test skill', encoding='utf-8')
            (link / 'canary.md').write_text('tracked reference', encoding='utf-8')
            subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(root), 'add', '-A'], check=True, capture_output=True)
            (link / 'canary.md').unlink()
            link.rmdir()
            outside = fixture / 'outside'
            outside.mkdir()
            canary = outside / 'canary.md'
            canary.write_text('synthetic outside canary', encoding='utf-8')
            (source / '.gitignore').write_text('/references\n', encoding='utf-8')
            create = fixture / 'junction.ps1'
            create.write_text("param($Link, $Target)\n$ErrorActionPreference = 'Stop'\n"
                              'New-Item -ItemType Junction -Path $Link -Target $Target | Out-Null\n', encoding='utf-8')
            try:
                subprocess.run([shell, '-NoProfile', '-NonInteractive', '-File', str(create), str(link), str(outside)],
                               check=True, capture_output=True)
                with patch.object(benchmark, 'REPO', root), self.assertRaisesRegex(SystemExit, 'junction'):
                    benchmark.materialize_variant('current', fixture / 'export')
                self.assertFalse((fixture / 'export' / benchmark.SKILL_REL / 'references/canary.md').exists())
            finally:
                # Remove only the junction before TemporaryDirectory can recurse into this fixture.
                if os.path.lexists(link):
                    self.assertTrue(link.absolute().is_relative_to(fixture))
                    self.assertTrue(outside.resolve().is_relative_to(fixture))
                    self.assertEqual(link.lstat().st_reparse_tag, benchmark.stat.IO_REPARSE_TAG_MOUNT_POINT)
                    os.rmdir(link)
                    self.assertEqual(canary.read_text(encoding='utf-8'), 'synthetic outside canary')

    def test_current_export_reparse_tag_policy_preserves_other_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repo'
            source = root / benchmark.SKILL_REL / 'SKILL.md'
            source.parent.mkdir(parents=True)
            source.write_text('test skill', encoding='utf-8')
            listed = (benchmark.SKILL_REL.as_posix() + '/SKILL.md\0').encode()
            original_lstat = Path.lstat
            with patch.object(benchmark, 'REPO', root), patch.object(benchmark.subprocess, 'check_output', return_value=listed):
                for tag in (None, 0, 0x9000001A, 0xA0000003):
                    with self.subTest(tag=tag):
                        def tagged_lstat(path, *args, **kwargs):
                            metadata = original_lstat(path, *args, **kwargs)
                            if path == source.parent:
                                return SimpleNamespace(st_mode=metadata.st_mode, st_reparse_tag=tag)
                            return metadata
                        # Supply the platform-specific constant so this policy runs on POSIX too.
                        with patch.object(benchmark.stat, 'IO_REPARSE_TAG_MOUNT_POINT', 0xA0000003, create=True), patch.object(Path, 'lstat', tagged_lstat):
                            destination = Path(temporary) / str(tag)
                            if tag == 0xA0000003:
                                with self.assertRaisesRegex(SystemExit, 'junction'):
                                    benchmark.materialize_variant('current', destination)
                            else:
                                exported = benchmark.materialize_variant('current', destination)
                                self.assertEqual((exported / 'SKILL.md').read_text(encoding='utf-8'), 'test skill')

    @unittest.skipUnless(os.name == 'nt', 'Windows PowerShell launcher')
    def test_launcher_reports_resumed_folder_instead_of_newest(self):
        shell = shutil.which('pwsh') or shutil.which('powershell')
        if not shell:
            self.skipTest('PowerShell unavailable')
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            tools = fixture / 'dev-tools'
            tools.mkdir()
            launcher = tools / 'run-skill-benchmark.ps1'
            shutil.copyfile(REPO_ROOT / 'dev-tools/run-skill-benchmark.ps1', launcher)
            old = fixture / '.local/bench/20260101T000000Z'
            latest = fixture / '.local/bench/20261201T000000Z'
            old.mkdir(parents=True)
            latest.mkdir()
            wrapper = fixture / 'intercept.ps1'
            wrapper.write_text("param($Launcher, $Resume)\n"
                               'function global:python { $global:LASTEXITCODE = 0 }\n'
                               "if ($Resume) { & $Launcher -Preset static -Resume $Resume }\n"
                               "else { & $Launcher -Preset static }\n", encoding='utf-8')
            for resume, expected in [(str(old), old), (str(old.relative_to(fixture)), old), ('', latest)]:
                with self.subTest(resume=bool(resume)):
                    run = subprocess.run([shell, '-NoProfile', '-NonInteractive', '-File', str(wrapper), str(launcher), resume],
                                         cwd=fixture.parent, check=True, capture_output=True, text=True)
                    self.assertIn(f'Report: {expected / "SUMMARY.md"}', run.stdout)

    def test_summary_separates_common_and_workflow_and_selected_scenarios(self):
        variants = ['current', 'mcp-docs']
        static = {'variants': {v: {'context_est_tokens': 10} for v in variants},
                  'scenarios': {sid: {v: {'context_est_tokens': 20} for v in variants}
                                for sid in ('route-character', 'replay-blueprint')}}
        summary = {sid: {'agent': {v: {'checks_rate': rate} for v in variants}}
                   for sid, rate in [('route-character', 1), ('replay-blueprint', 0)]}
        report = benchmark.render_report_block(static, summary, variants, ['agent'], 1, '20261107')
        self.assertIn('| Common routing | Pip | 100%', report)
        self.assertIn('| Pip workflow | Pip | 0%', report)
        self.assertNotIn('Routing correct (avg)', report)

    def test_current_export_handles_working_tree_changes_and_ignored_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repo'
            source = root / benchmark.SKILL_REL
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('test skill', encoding='utf-8')
            (source / 'obsolete.md').write_text('old reference', encoding='utf-8')
            (source / 'now-directory.md').write_text('old file', encoding='utf-8')
            (source / 'tracked-config.txt').write_text('synthetic tracked config', encoding='utf-8')
            replaced = source / 'references'
            replaced.mkdir()
            (replaced / 'old.md').write_text('nested reference', encoding='utf-8')
            subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(root), 'add', '--', benchmark.SKILL_REL.as_posix()],
                           check=True, capture_output=True)
            (source / 'obsolete.md').unlink()
            (source / 'now-directory.md').unlink()
            (source / 'now-directory.md').mkdir()
            (source / 'now-directory.md' / 'new.md').write_text('replacement child', encoding='utf-8')
            (replaced / 'old.md').unlink()
            replaced.rmdir()
            replaced.write_text('replacement file', encoding='utf-8')
            (source / 'new.md').write_text('new reference', encoding='utf-8')
            (source / '.gitignore').write_text('pixellab-pip.json\ntracked-config.txt\n', encoding='utf-8')
            (source / 'pixellab-pip.json').write_text('{"auto": true}', encoding='utf-8')
            with patch.object(benchmark, 'REPO', root):
                exported = benchmark.materialize_variant('current', Path(temporary) / 'export')
                original_lstat = Path.lstat

                def posix_lstat(path, *args, **kwargs):
                    if path == replaced / 'old.md':
                        raise NotADirectoryError('POSIX lookup through replacement file')
                    return original_lstat(path, *args, **kwargs)

                with patch.object(Path, 'lstat', posix_lstat):
                    posix_export = benchmark.materialize_variant('current', Path(temporary) / 'posix-export')
                (source / 'SKILL.md').unlink()
                with self.assertRaisesRegex(SystemExit, 'has no'):
                    benchmark.materialize_variant('current', Path(temporary) / 'missing-entry')
            self.assertEqual((exported / 'SKILL.md').read_text(encoding='utf-8'), 'test skill')
            self.assertEqual((exported / 'new.md').read_text(encoding='utf-8'), 'new reference')
            self.assertEqual((exported / 'now-directory.md' / 'new.md').read_text(encoding='utf-8'), 'replacement child')
            self.assertEqual((exported / 'tracked-config.txt').read_text(encoding='utf-8'), 'synthetic tracked config')
            self.assertEqual((exported / 'references').read_text(encoding='utf-8'), 'replacement file')
            self.assertEqual((posix_export / 'references').read_text(encoding='utf-8'), 'replacement file')
            self.assertFalse((exported / 'obsolete.md').exists())
            self.assertFalse((exported / 'pixellab-pip.json').exists())

    def test_current_export_requires_git_inventory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'notgit'
            source = root / benchmark.SKILL_REL
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('test skill', encoding='utf-8')
            # Prevent Git from finding an outer checkout when tests use a repo-local temp directory.
            with patch.dict(os.environ, {'GIT_CEILING_DIRECTORIES': temporary}), patch.object(benchmark, 'REPO', root):
                with self.assertRaisesRegex(SystemExit, 'requires Git and a Git working tree'):
                    benchmark.materialize_variant('current', Path(temporary) / 'export')

    def test_current_export_rejects_native_links_including_ignored_ancestors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repo'
            source = root / benchmark.SKILL_REL
            references = source / 'references'
            references.mkdir(parents=True)
            (source / 'SKILL.md').write_text('test skill', encoding='utf-8')
            (references / 'canary.md').write_text('tracked reference', encoding='utf-8')
            subprocess.run(['git', 'init', '--quiet', str(root)], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(root), 'add', '-A'], check=True, capture_output=True)
            outside = Path(temporary) / 'outside'
            outside.mkdir()
            (outside / 'canary.md').write_text('synthetic outside canary', encoding='utf-8')
            link = source / 'linked.md'
            with patch.object(benchmark, 'REPO', root):
                for label, target in [('external', outside / 'canary.md'),
                                      ('internal', source / 'SKILL.md'), ('dangling', outside / 'missing.md')]:
                    with self.subTest(link=label):
                        try:
                            link.symlink_to(target)
                        except OSError as exc:
                            self.skipTest('Native symbolic links unavailable: ' + str(exc))
                        with self.assertRaisesRegex(SystemExit, 'symbolic link'):
                            benchmark.materialize_variant('current', Path(temporary) / label)
                        link.unlink()
                (references / 'canary.md').unlink()
                references.rmdir()
                references.symlink_to(outside, target_is_directory=True)
                (source / '.gitignore').write_text('/references\n', encoding='utf-8')
                with self.assertRaisesRegex(SystemExit, 'symbolic link'):
                    benchmark.materialize_variant('current', Path(temporary) / 'ignored-ancestor')
                self.assertFalse((Path(temporary) / 'ignored-ancestor' / benchmark.SKILL_REL / 'references' / 'canary.md').exists())

    def test_current_export_does_not_hide_unreadable_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repo'
            source = root / benchmark.SKILL_REL / 'SKILL.md'
            source.parent.mkdir(parents=True)
            source.write_text('test skill', encoding='utf-8')
            listed = (benchmark.SKILL_REL.as_posix() + '/SKILL.md\0').encode()
            original_lstat = Path.lstat

            def checked_lstat(path, *args, **kwargs):
                if path == source:
                    raise PermissionError('unreadable input metadata')
                return original_lstat(path, *args, **kwargs)

            with patch.object(benchmark, 'REPO', root), patch.object(benchmark.subprocess, 'check_output', return_value=listed):
                with patch.object(Path, 'lstat', checked_lstat), self.assertRaises(PermissionError):
                    benchmark.materialize_variant('current', Path(temporary) / 'metadata-error')
                with patch.object(benchmark.shutil, 'copyfile', side_effect=PermissionError), self.assertRaises(PermissionError):
                    benchmark.materialize_variant('current', Path(temporary) / 'copy-error')
                # Exercise link policy even on hosts that cannot create native symbolic links.
                for linked in (source.parent, source):
                    with self.subTest(link_component=linked.name):
                        def linked_lstat(path, *args, **kwargs):
                            if path == linked:
                                return os.stat_result((benchmark.stat.S_IFLNK, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                            return original_lstat(path, *args, **kwargs)

                        with patch.object(Path, 'lstat', linked_lstat), self.assertRaisesRegex(SystemExit, 'symbolic link'):
                            benchmark.materialize_variant('current', Path(temporary) / 'linked-input')


if __name__ == '__main__':
    unittest.main()
