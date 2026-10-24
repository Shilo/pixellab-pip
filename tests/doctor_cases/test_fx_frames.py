"""--fx: frames with an effect baked in on purpose (a smoke vanish) - the archer test (2026-10-22): the doctor read a
smoke poof as a washed-out frame and its loose puffs as detached pieces, and planned paid re-rolls for both."""
import synth
from fixlib import plan
from test_cli import fix, report
from test_plan import F
from test_measure_clean import anim


def _smoky(tmp_path):
    fs = synth.walk(6)
    fs[2] = synth.bright(fs[2], 1.6)                         # reads as washed out
    fs[3] = synth.flash(fs[3], (2, 2, 10, 10))               # reads as an effect / detached piece
    synth.save(fs, tmp_path / 'k', 'archer_skill')
    return tmp_path / 'k'


def test_default_flags_the_effect_frames(tmp_path):
    fix(_smoky(tmp_path), '--out', tmp_path / 'o')
    frames = {i for f in report(tmp_path / 'o')['anims'][0]['findings_before'] for i in f['frames']}
    assert {3, 4} & frames


def test_fx_frames_are_not_judged_and_it_says_so(tmp_path):
    out = fix(_smoky(tmp_path), '--fx', '3,4', '--out', tmp_path / 'o')
    a = report(tmp_path / 'o')['anims'][0]
    assert not {3, 4} & {i for f in a['findings_before'] for i in f['frames']}
    assert not [p for p in a['plans'] if {3, 4} & set(p['frames'])]
    assert any('effect' in s and '3' in s for s in a['skipped'])


def test_size_plan_points_at_ref_for_an_added_prop():
    (p,) = plan.make(anim(synth.walk(6)), [F('size', [2])], None)
    assert '--ref' in p['prompt_change'] or '--ref' in p['cause']


def test_keys_get_no_reroll_plan(tmp_path):
    # the berserker test (2026-10-22): the doctor planned a 9-gen re-roll of the approved slam key pose
    fs = synth.walk(6)
    fs[5] = synth.bright(fs[5], 1.6)
    synth.save(fs, tmp_path / 'k', 'hero_skill')
    out = fix(tmp_path / 'k', '--keys', '6', '--out', tmp_path / 'o')
    a = report(tmp_path / 'o')['anims'][0]
    assert not [p for p in a['plans'] if 6 in p['frames']]
    assert any('key pose' in s and '6' in s for s in a['skipped'])
