import numpy as np

import synth
from fixlib import measure
from test_measure_clean import anim, found


def test_walk_moves_smoothly():
    a = anim(synth.walk(8), 'walk')
    for c in ('jump', 'size_pop', 'missing_inbetween', 'loop_seam', 'return_to_stand'):
        assert found(a, c) == [], c


def test_jump():
    fs = synth.walk(8)
    fs[4] = synth.shift(fs[4], 8, 0)
    assert 4 in found(anim(fs, 'walk'), 'jump')


def test_size_pop():
    fs = synth.walk(8)
    fs[3] = synth.flash(fs[3], (18, 20, 30, 40), synth.BLUE)
    fs[3] = synth.flash(fs[3], (2, 20, 18, 40), synth.BLUE)      # the body suddenly 40% bigger, for one frame
    assert 3 in found(anim(fs, 'walk'), 'size_pop')


def test_loop_seam():
    fs = synth.walk(8)
    fs[-1] = synth.shift(fs[-1], 7, 0)
    assert found(anim(fs, 'idle'), 'loop_seam') == [7]


def test_return_to_stand():
    fs = synth.walk(6)
    end = np.zeros_like(fs[0])
    end = synth.flash(end, (10, 34, 40, 54), synth.BLUE)
    fs[-1] = end
    assert found(anim(fs, 'attack'), 'return_to_stand') == [5]
    assert found(anim(fs, 'death'), 'return_to_stand') == []


def test_missing_inbetween():
    fs = [synth.shift(synth.figure(), dx, 0) for dx in (0, 1, 2, 3, 10, 11, 12, 13)]
    assert found(anim(fs, 'attack'), 'missing_inbetween') == [3, 4]


def test_two_frames_skip_motion():
    fs = synth.walk(2)
    fs[1] = synth.shift(fs[1], 9, 0)
    findings, skipped = measure.run(anim(fs, 'attack'))
    assert not [f for f in findings if f.check in ('jump', 'size_pop', 'missing_inbetween', 'loop_seam')]
    assert 'motion: fewer than 3 frames' in skipped
