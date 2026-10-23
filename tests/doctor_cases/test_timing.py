import numpy as np

import synth
from fixlib import measure, timing
from test_measure_clean import anim
from test_measure_identity import CYAN


def run(a):
    """Accepts every proposal: frame drops are proposals since the merge (Pip keeps the frames PixelLab returned)."""
    fs, _ = measure.run(a)
    _, first, _, _ = timing.run(a, fs)
    return timing.run(a, fs, accept={c.id for c in first if c.result == 'proposed'})


def test_frame_drop_is_a_proposal():
    fs = synth.walk(8)
    fs[4] = synth.shift(fs[4], 8, 0)
    a = anim(fs)
    b, changes, durations, order = timing.run(a, measure.run(a)[0])
    (c,) = changes
    assert c.result == 'proposed' and c.frames == [4]
    assert np.array_equal(b.frames[4], a.frames[4]) and order == list(range(8)) and durations == [100] * 8


def test_drop_a_jump_frame_and_hold_its_neighbour():
    fs = synth.walk(8)
    fs[4] = synth.shift(fs[4], 8, 0)
    a = anim(fs)
    b, changes, durations, order = run(a)
    assert np.array_equal(b.frames[4], a.frames[3])
    assert durations[3] == 200 and durations[4] == 0 and sum(durations) == 800
    assert order == [0, 1, 2, 3, 3, 5, 6, 7]
    (c,) = changes
    assert c.action == 'dropped frame 5, held frame 4' and c.frames == [4]      # messages count from 1, like file names
    assert len(b.frames) == 8


def test_hurt_with_dirty_early_frames_is_reordered():
    fs = synth.walk(5)
    fs[1], fs[2] = synth.bright(fs[1], 1.3), synth.bright(fs[2], 1.3)
    b, changes, durations, order = run(anim(fs, 'hurt'))
    assert order == [3, 4, 4, 3, 0]
    assert np.array_equal(b.frames[0], fs[3]) and np.array_equal(b.frames[4], fs[0])
    assert any('reordered' in c.action for c in changes)


def test_at_most_a_third_of_the_frames_are_dropped():
    fs = synth.walk(9)
    for i in (1, 4, 7):
        fs[i] = synth.drop_staff(fs[i])
    b, changes, durations, order = run(anim(fs))
    dropped = [c for c in changes if c.result == 'fixed']
    failing = [c for c in changes if c.result == 'still failing']
    assert len(dropped) == 3 and not failing              # 9 frames: a third is 3

    fs = synth.walk(6)
    for i in (1, 3, 4):
        fs[i] = synth.drop_staff(fs[i])
    b, changes, durations, order = run(anim(fs))
    assert [c.frames for c in changes if c.result == 'fixed'] == [[1], [3]]
    assert [c.frames for c in changes if c.result == 'still failing'] == [[4]]


def test_first_and_last_frame_of_a_one_shot_stay():
    fs = synth.walk(6)
    fs[5] = synth.drop_staff(fs[5])
    b, changes, durations, order = run(anim(fs))
    assert order[-1] == 5
    assert [c.result for c in changes] == ['still failing']


def test_flash_is_never_dropped_without_asking():
    fs = synth.walk(8)
    fs[4] = synth.flash(fs[4], (36, 20, 44, 28), CYAN)
    b, changes, durations, order = run(anim(fs))
    assert changes == [] and order == list(range(8))


def test_ids_continue_after_repairs():
    fs = synth.walk(8)
    fs[4] = synth.shift(fs[4], 8, 0)
    a = anim(fs)
    f, _ = measure.run(a)
    _, changes, _, _ = timing.run(a, f, start=3)
    assert changes[0].id == 'c4'
