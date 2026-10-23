import numpy as np

import synth
from fixlib import measure
from fixlib.model import Anim


def anim(fs, move='attack', ref=None, bg=None):
    kind = 'loop' if move in ('idle', 'walk') else 'oneshot'
    return Anim(key='k/' + move, character='k', move=move, kind=kind, kind_guessed=False, paths=[], frames=fs,
                offsets=[(0, 0)] * len(fs), sizes=[(f.shape[1], f.shape[0]) for f in fs], scale=1,
                ref=synth.figure() if ref is None else ref, ref_guessed=False, bg=bg)


def found(a, check, style=None):
    fs, _ = measure.run(a, style)
    return sorted({i for f in fs if f.check == check for i in f.frames})


def test_clean_walk_has_no_findings():
    fs, skipped = measure.run(anim(synth.walk(8), 'walk'))
    assert fs == [], fs


def test_edge():
    fs = synth.walk(6)
    fs[2] = synth.cut_left(fs[2], 20)
    assert found(anim(fs), 'edge') == [2]


def test_ground():
    fs = synth.walk(6)
    fs[3] = synth.shift(fs[3], 0, -5)
    assert found(anim(fs), 'ground') == [3]


def test_death_may_go_below_or_above_the_foot_line():
    fs = synth.walk(6)
    fs[3] = synth.shift(fs[3], 0, -5)
    assert found(anim(fs, 'death'), 'ground') == []


def test_detached():
    fs = synth.walk(6)
    fs[4] = synth.flash(fs[4], (0, 0, 17, 26), synth.BLUE)       # a 442 px body-coloured piece away from the body
    assert found(anim(fs), 'detached') == [4]


def test_specks_but_not_next_to_the_staff_tip():
    fs = synth.walk(6)
    fs[1] = synth.specks_many(fs[1])                             # 120 loose px, over the calibrated 100
    fs[2] = synth.speck(fs[2], (33, 8))                          # one px gap above the staff tip (x 33, top y 10)
    assert found(anim(fs), 'specks') == [1]


def test_holes():
    fs = synth.walk(6)
    fs[5] = synth.pinholes(fs[5])                                # 45 enclosed 1 px holes
    assert found(anim(fs), 'holes') == [5]


def test_bg_leak():
    fs = synth.walk(4)
    fs[2] = synth.speck(fs[2], (21, 30), (255, 0, 255), 2)       # background colour inside the body
    assert found(anim(fs, bg=(255, 0, 255)), 'bg_leak') == [2]


def test_brightness():
    fs = synth.walk(6)
    fs[2] = synth.bright(fs[2], 1.35)
    assert found(anim(fs), 'brightness') == [2]


def test_palette():
    fs = synth.walk(6)
    red = fs[4].copy()
    on = red[..., 3] > 0
    red[on, :3] = red[on, :3][:, ::-1]                           # colours swapped around: a recolour
    fs[4] = red
    assert 4 in found(anim(fs), 'palette')
