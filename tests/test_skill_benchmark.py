from pathlib import Path
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
            ('plan-item-icon-sheet', 'create_image_pixen per concept, assemble one sheet'),
            ('route-skill-icons', 'create_image_pro, verify sheet layout'),
            ('route-skill-icons', 'generate-with-style-v2; verify the sheet'),
            ('plan-item-icon-sheet', 'generate-with-style-v2; pack the sheet'),
            ('route-tiles-vs-tileset', 'create_tiles_pro independent tiles, pack a grid'),
            ('route-tiles-vs-tileset', 'create_image_pro_flash per texture, assemble a grid'),
            ('route-object-prop', 'create_image_pro_flash'),
            ('route-1bit-tileset-palette', 'create_topdown_tileset with palette, approved palette variant'),
            ('cheap-animation', 'get_character size; compare animate_character template and v3 costs'),
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

    def test_current_export_omits_unlisted_private_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'repo'
            source = root / benchmark.SKILL_REL
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('test skill', encoding='utf-8')
            (source / 'pixellab-pip.json').write_text('{"auto": true}', encoding='utf-8')
            listed = (benchmark.SKILL_REL.as_posix() + '/SKILL.md\0').encode()
            with patch.object(benchmark, 'REPO', root), patch.object(benchmark.subprocess, 'check_output', return_value=listed):
                exported = benchmark.materialize_variant('current', Path(temporary) / 'export')
            self.assertTrue((exported / 'SKILL.md').is_file())
            self.assertFalse((exported / 'pixellab-pip.json').exists())


if __name__ == '__main__':
    unittest.main()
