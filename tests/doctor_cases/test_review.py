"""Findings from the whole-release review (2026-10-21), one test each, written before the fix."""
import json
import os

import numpy as np
from PIL import Image

import synth
from fixlib import measure, plan, repair, timing
from test_cli import fix, report
from test_measure_clean import anim
from test_measure_identity import CYAN


def test_folders_dont_overwrite_each_other_and_orig_is_skipped(tmp_path):
    for move in ('walk', 'idle'):
        d = tmp_path / 'batch' / ('knight_' + move)
        fs = synth.walk(4)
        if move == 'idle':
            fs = [synth.flash(f, (0, 0, 2, 2), synth.BLUE) for f in fs]   # tell the two apart
        for i, f in enumerate(fs, 1):
            d.mkdir(parents=True, exist_ok=True)
            Image.fromarray(f, 'RGBA').save(d / ('%d.png' % i))
    synth.save(synth.walk(4), tmp_path / 'batch' / 'knight_walk' / 'orig', 'x')    # a colormatch backup
    fix(tmp_path / 'batch')
    out = str(tmp_path / 'batch') + '_fixed'
    keys = [a['key'] for a in report(out)['anims']]
    assert sorted(keys) == ['knight/idle', 'knight/walk']
    for sub in ('knight_walk', 'knight_idle'):
        assert sorted(os.listdir(os.path.join(out, sub))) == ['1.png', '2.png', '3.png', '4.png']


def test_body_soft_edge_fix_leaves_an_effect_glow_alone():
    fs = synth.walk(6)
    g = synth.blur_edges(fs[2])
    g[2:10, 2:10, :3], g[2:10, 2:10, 3] = CYAN, 90               # a separate soft glow
    fs[2] = g
    a = anim(fs)
    f, _ = measure.run(a)
    b, changes = repair.run(a, f)
    assert (b.frames[2][2:10, 2:10, 3] == 90).all()
    assert any(c.check == 'soft_edge' and c.result == 'proposed' for c in changes)


def test_black_background_keeps_black_eyes(tmp_path):
    fs = [synth.solid_bg(f, (0, 0, 0)) for f in synth.walk(4)]
    for f in fs:
        f[15, 22, :3] = f[15, 25, :3] = (0, 0, 0)                 # black eyes, like the outline colour
    ref = synth.figure()
    ref[15, 22, :3] = ref[15, 25, :3] = (0, 0, 0)
    a = anim([_key(f) for f in fs], bg=(0, 0, 0))
    a.ref = ref
    assert 'bg_leak' not in {x.check for x in measure.run(a)[0]}


def _key(f):
    from fixlib.frames import key_background
    return key_background(f)[0]


def test_hurt_with_only_a_lasting_effect_is_asked_not_reordered():
    fs = synth.walk(5)
    for i in (1, 2):
        fs[i] = synth.flash(fs[i], (36, 20, 46, 34), (230, 40, 40))   # a painted burst on frames 1-2
    a = anim(fs, 'hurt')
    f, _ = measure.run(a)
    b, changes, durations, order = timing.run(a, f)
    assert order == [0, 1, 2, 3, 4]
    assert not changes
    assert all(np.array_equal(got, want) for got, want in zip(b.frames, fs))


def test_verdict_is_not_ready_when_something_changed():
    from fixlib.model import Change
    assert plan.verdict([], [], [Change('c1', 'timing', [1], 'x', 'fixed')]) == 'ready after free fixes'


def test_sparkle_effects_dont_change_the_pixel_size():
    fs = [synth.upscale(f, 2) for f in synth.walk(6)]
    for i in (1, 2, 3, 4):
        for k in range(40):
            y, x = 2 + 2 * (k // 8), 2 + 2 * (k % 8)
            fs[i][y, x, :3], fs[i][y, x, 3] = CYAN, 255          # 40 lasting 1 px sparkles
    a = anim(fs, 'walk', ref=synth.upscale(synth.figure(), 2))
    a.scale = 2
    assert 'grid' not in {x.check for x in measure.run(a)[0]}


def test_a_question_is_not_also_a_reroll(tmp_path):
    fs = synth.walk(8)
    fs[5] = synth.flash(fs[5], (36, 20, 44, 28), CYAN)
    synth.save(fs, tmp_path / 'k', 'knight_attack')
    r = json.loads(fix(tmp_path / 'k', '--json'))
    (a,) = r['anims']
    assert a['proposals'] and not a['plans']
    assert r['verdict'] == 'ready after free fixes' and r['totals']['proposals'] == 1
