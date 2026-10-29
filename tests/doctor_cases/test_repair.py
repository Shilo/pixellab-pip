import numpy as np

import synth
from fixlib import measure, repair
from test_measure_clean import anim
from test_measure_identity import CYAN


def fix(a, accept=(), style=None):
    fs, _ = measure.run(a, style)
    b, changes = repair.run(a, fs, set(accept), style)
    after, _ = measure.run(b, style)
    return b, changes, after


def checks(findings):
    return {(f.check, tuple(f.frames)) for f in findings}


def _hole(fs):
    fs[5] = synth.pinholes(fs[5])


def _red(fs):
    g = fs[4].copy()
    on = g[..., 3] > 0
    g[on, :3] = np.clip(g[on, :3].astype(int) + (70, -25, -25), 0, 255)
    fs[4] = g


CASES = {
    'specks': lambda fs: fs.__setitem__(1, synth.specks_many(fs[1])),
    'holes': _hole,
    'brightness': lambda fs: fs.__setitem__(2, synth.bright(fs[2], 1.3)),
    'palette': _red,
    'ground': lambda fs: fs.__setitem__(3, synth.shift(fs[3], 0, -5)),
    'broken_thin': lambda fs: fs.__setitem__(5, synth.cut_staff(fs[5])),
    'weapon_lost': lambda fs: fs.__setitem__(5, synth.drop_staff(fs[5])),
    'soft_edge': lambda fs: fs.__setitem__(2, synth.blur_edges(fs[2])),
}


def test_free_repair_clears_the_finding():
    for check in sorted(CASES):
        fs = synth.walk(9)
        CASES[check](fs)
        a = anim(fs)
        before = {f.check for f in measure.run(a)[0]}
        assert check in before, check
        b, changes, after = fix(a)
        assert check not in {f.check for f in after}, (check, [(f.check, f.frames) for f in after])
        assert any(c.check == check and c.result == 'fixed' for c in changes), check
        assert a.frames[0] is not b.frames[0]                       # a copy: the input Anim is untouched


def test_bg_leak_repair():
    fs = synth.walk(4)
    fs[2] = synth.speck(fs[2], (21, 30), (255, 0, 255), 2)
    b, changes, after = fix(anim(fs, bg=(255, 0, 255)))
    assert 'bg_leak' not in {f.check for f in after}


def test_grid_repair():
    fs = [synth.upscale(f, 4) for f in synth.walk(6)]
    g = fs[3].copy()
    body = (g[..., :3] == synth.BLUE).all(-1)
    yy, xx = np.indices(body.shape)
    g[body & ((yy // 2 + xx // 2) % 2 == 0), :3] = synth.SHADE
    fs[3] = g
    a = anim(fs, ref=synth.upscale(synth.figure(), 4))
    a.scale = 4
    b, changes, after = fix(a)
    assert not {'grid', 'mixels'} & {f.check for f in after}


def test_lasting_effect_is_never_touched():
    fs = synth.walk(6)
    for i in (2, 3, 4):
        fs[i] = synth.flash(fs[i], (36, 20, 44, 28), CYAN)
    a = anim(fs)
    b, changes, _ = fix(a)
    for i in (2, 3, 4):
        assert np.array_equal(a.frames[i], b.frames[i])


def test_flash_is_a_proposal_until_accepted():
    fs = synth.walk(6)
    fs[2] = synth.flash(fs[2], (36, 20, 44, 28), CYAN)
    a = anim(fs)
    b, changes, after = fix(a)
    (p,) = [c for c in changes if c.check == 'flash']
    assert p.result == 'proposed' and np.array_equal(b.frames[2], a.frames[2])
    b2, changes2, after2 = fix(a, accept={p.id})
    assert 'flash' not in {f.check for f in after2}
    assert [c.result for c in changes2 if c.id == p.id] == ['fixed']


def test_change_ids_are_stable():
    fs = synth.walk(6)
    fs[1] = synth.speck(fs[1], (2, 50))
    fs[2] = synth.flash(fs[2], (36, 20, 44, 28), CYAN)
    a = anim(fs)
    assert [c.id for c in fix(a)[1]] == [c.id for c in fix(a)[1]]


def test_washed_frame_is_not_colour_matched():
    fs = synth.walk(6)
    fs[2] = synth.bright(fs[2], 1.9)                             # washed out
    a = anim(fs)
    b, changes, after = fix(a)
    assert np.array_equal(a.frames[2], b.frames[2])
    assert any(c.check == 'brightness' and c.result == 'still failing' for c in changes)


def _grid_with_effect(soft=False):
    fs = [synth.upscale(f, 4) for f in synth.walk(6)]
    body = (fs[2][..., :3] == synth.BLUE).all(-1)
    yy, xx = np.indices(body.shape)
    fs[2][body & ((yy // 2 + xx // 2) % 2 == 0), :3] = synth.SHADE
    for i in ((2, 4, 5) if soft else range(6)):
        if soft:
            fs[i][5:50, 5, :3], fs[i][5:50, 5, 3] = CYAN, 110
        else:
            fs[i] = synth.flash(fs[i], (145, 17, 152, 24), CYAN)
    a = anim(fs, ref=synth.upscale(synth.figure(), 4))
    a.scale = 4
    return a


def test_whole_frame_repairs_preserve_effects_until_their_change_is_accepted():
    cases = [('grid', _grid_with_effect())]
    for check in ('ground', 'size'):
        fs = synth.walk(6)
        if check == 'ground':
            fs[3] = synth.shift(fs[3], 0, -5)
        else:
            fs[3] = np.zeros_like(fs[3])
            fs[3][26:54, 12:36] = synth.figure()[::2, ::2]
        fs = [synth.flash(f, (38, 13, 45, 20), CYAN) for f in fs]
        cases.append((check, anim(fs, move='walk')))
    for check, a in cases:
        before = [f.copy() for f in a.frames]
        b, changes, _ = fix(a)
        proposals = [c for c in changes if c.check == check]
        assert proposals and all(c.result == 'proposed' for c in proposals), check
        for i in proposals[0].frames:
            assert np.array_equal(b.frames[i], before[i]), check
        accepted, applied, _ = fix(a, {proposals[0].id})
        assert any(c.id == proposals[0].id and c.result == 'fixed' for c in applied), check
        assert not np.array_equal(accepted.frames[proposals[0].frames[0]], before[proposals[0].frames[0]]), check
        assert all(np.array_equal(old, new) for old, new in zip(before, a.frames)), check


def test_accepted_grid_cannot_shift_a_later_effect_approval_to_another_frame():
    a = _grid_with_effect(soft=True)
    _, pending, _ = fix(a)
    grid = next(c for c in pending if c.check == 'grid')
    target = next(c for c in pending if c.check == 'soft_edge' and c.frames == [4])
    b, changes, _ = fix(a, {grid.id, target.id})
    assert [(c.id, c.check, c.frames) for c in changes] == [(c.id, c.check, c.frames) for c in pending]
    assert not np.array_equal(b.frames[4], a.frames[4])
    assert np.array_equal(b.frames[5], a.frames[5])
    assert any(c.check == 'soft_edge' and c.frames == [2] and 'already resolved' in c.action for c in changes)


def test_body_specks_are_removed_without_erasing_a_lasting_effect():
    fs = synth.walk(6)
    fs[3] = synth.specks_many(fs[3])
    for i in (2, 3, 4):
        fs[i] = synth.flash(fs[i], (40, 2, 44, 7), CYAN)
    a = anim(fs)
    b, changes, after = fix(a)
    assert any(c.check == 'specks' and c.result == 'fixed' for c in changes)
    assert 'specks' not in {f.check for f in after}
    for i in (2, 3, 4):
        assert np.array_equal(b.frames[i][2:7, 40:44], a.frames[i][2:7, 40:44])
    assert not np.array_equal(b.frames[3], a.frames[3])
