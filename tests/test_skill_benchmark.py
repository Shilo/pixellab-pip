from pathlib import Path
import os
import subprocess
import tempfile
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
            ('cheap-animation', 'get_character size; compare animate_character template and v3 costs'),
            ('cheap-animation', 'animate_character with walking-8-frames template'),
            ('cheap-animation', 'animate_character v3 at 2 generations per approved direction'),
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
            ('cheap-animation', "animate_character(mode='pro') 8 frames"),
            ('cheap-animation', 'animate_character mode=pixminimax with 40 frames, all 8 directions'),
            ('cheap-animation', 'animate_character v3; inspect canvas size and frame count'),
        ]
        for scenario, response in cases:
            with self.subTest(scenario=scenario, response=response):
                self.assertFalse(all(benchmark.apply_checks(SCENARIOS[scenario], response).values()))

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
