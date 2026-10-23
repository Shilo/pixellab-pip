"""--stepped: animations built from key poses on purpose (no in-betweens), as the samurai and ninja tests made them.
Motion checks read their steps as defects; the clean checks still apply; frames are never dropped or reordered."""
import json

import synth
from test_cli import fix, report


def _stepped(tmp_path, name='ninja_attack'):
    fs = synth.walk(8)
    fs[4] = synth.shift(fs[4], 8, 0)            # a deliberate pose step: reads as a jump to the motion checks
    fs[6] = synth.shift(fs[6], 0, -20)          # an airborne key pose (a flying kick): reads as off the ground
    synth.save(fs, tmp_path / 'k', name)
    return tmp_path / 'k'


def test_default_mode_flags_the_steps(tmp_path):
    fix(_stepped(tmp_path), '--out', tmp_path / 'o')
    checks = {f['check'] for f in report(tmp_path / 'o')['anims'][0]['findings_before']}
    assert 'jump' in checks


def test_stepped_skips_the_motion_checks_and_says_so(tmp_path):
    out = fix(_stepped(tmp_path), '--stepped', '--out', tmp_path / 'o')
    a = report(tmp_path / 'o')['anims'][0]
    skipped = {'jump', 'missing_inbetween', 'loop_seam', 'size_pop', 'weird_change', 'weapon_lost', 'broken_thin', 'ground'}
    assert not skipped & {f['check'] for f in a['findings_before']}
    assert any('stepped' in s for s in a['skipped']) and 'stepped' in out


def test_stepped_never_drops_reorders_or_moves_frames(tmp_path):
    src = _stepped(tmp_path)
    fix(src, '--stepped', '--out', tmp_path / 'o')
    timing = json.load(open(tmp_path / 'o' / 'timing.json', encoding='utf-8'))
    (t,) = [v for k, v in timing.items() if k != 'note']
    assert t['order'] == list(range(8)) and all(d > 0 for d in t['durations'])
    a = report(tmp_path / 'o')['anims'][0]
    assert not [c for c in a['changes'] if c['check'] in ('timing', 'ground')]


def test_stepped_still_cleans(tmp_path):
    src = _stepped(tmp_path)
    fs = synth.walk(8)
    fs[2] = synth.specks_many(fs[2])
    synth.save(fs, tmp_path / 'k2', 'ninja_attack')
    fix(tmp_path / 'k2', '--stepped', '--out', tmp_path / 'o2')
    a = report(tmp_path / 'o2')['anims'][0]
    assert any(c['check'] == 'specks' and c['result'] == 'fixed' for c in a['changes'])
