import numpy as np
import synth
from fixlib import measure
from test_measure_clean import anim, found

CYAN = (120, 255, 255)


def test_one_frame_flash():
    fs = synth.walk(6)
    fs[2] = synth.flash(fs[2], (36, 20, 44, 28), CYAN)
    a = anim(fs)
    assert found(a, 'flash') == [2]
    assert found(a, 'effect') == []


def test_lasting_effect_is_not_a_flash():
    fs = synth.walk(6)
    for i in (2, 3, 4):
        fs[i] = synth.flash(fs[i], (36, 20, 44, 28), CYAN)
    a = anim(fs)
    assert found(a, 'flash') == []
    assert found(a, 'effect') == [2, 3, 4]
    (e,) = [f for f in measure.run(a)[0] if f.check == 'effect']
    assert e.severity == 'low' and e.region == 'effect'


def test_weird_change_that_reverts():
    fs = synth.walk(6)
    g = fs[3].copy()
    head = ((g[..., :3] == synth.SKIN).all(-1) | (g[..., :3] == synth.HAIR).all(-1)) & (g[..., 3] > 0)
    g[head, :3] = (200, 60, 60)                                   # the whole head redrawn red for one frame
    fs[3] = g
    hits = [f for f in measure.run(anim(fs))[0] if f.check == 'weird_change']
    assert [f.frames for f in hits] and all(f.frames == [3] for f in hits)
    assert any('top' in f.note for f in hits)


def test_weapon_lost():
    fs = synth.walk(9)
    fs[5] = synth.drop_staff(fs[5])
    assert found(anim(fs), 'weapon_lost') == [5]
    assert found(anim(fs), 'broken_thin') == []


def test_broken_thin():
    fs = synth.walk(9)
    fs[5] = synth.cut_staff(fs[5])
    assert found(anim(fs), 'broken_thin') == [5]
    assert found(anim(fs), 'weapon_lost') == []


def _face(f, rgb):
    g = f.copy()
    g[(g[..., :3] == synth.SKIN).all(-1) & (g[..., 3] > 0) & (np.arange(g.shape[0])[:, None] < 22), :3] = rgb
    return g


def test_head_turned_away_for_one_frame():
    # e2e demo (frost mage): one in-between showed the back of the hood; the doctor said "ready"
    fs = synth.walk(7)
    fs[3] = _face(fs[3], synth.HAIR)
    assert found(anim(fs), 'head_change') == [3]


def test_face_redrawn_dark_for_one_frame():
    # a shipped windup had its face drawn another colour for one frame; a slight skin-tone shift stays below the
    # calibrated gap and is the look checklist's job
    fs = synth.walk(7)
    fs[2] = _face(fs[2], (40, 40, 40))
    assert found(anim(fs), 'head_change') == [2]


def test_steady_head_has_no_head_change():
    assert found(anim(synth.walk(9)), 'head_change') == []


def test_frame_beside_empty_frames_is_not_a_head_change():
    # review: an empty frame scored a perfect head match, so the frame between two empties was flagged
    fs = synth.walk(5)
    fs[1] = np.zeros_like(fs[1])
    fs[3] = np.zeros_like(fs[3])
    fs[2] = _face(fs[2], (40, 40, 40))                         # unmeasurable neighbours: no verdict either way
    assert found(anim(fs), 'head_change') == []


def _staff_to_other_hand(f):
    """The staff moved against the body's other side (the other hand)."""
    g = f.copy()
    col = (g[..., :3] == synth.STAFF).all(-1) & (g[..., 3] > 0)
    ys = np.nonzero(col.any(1))[0]
    g[col] = 0
    x = int(np.nonzero((g[..., 3] > 0).any(0))[0].min()) - 1
    g[ys, x, :3], g[ys, x, 3] = synth.STAFF, 255
    return g


def test_prop_leaves_its_side_between_key_poses():
    # e2e demo: the staff drifted from beside the body to its centre line in the in-betweens
    fs = synth.walk(7)
    for i in (2, 3, 4):
        fs[i] = _staff_to_other_hand(fs[i])
    assert found(anim(fs), 'prop_drift') == [2, 3, 4]


def test_prop_on_its_path_has_no_drift():
    assert found(anim(synth.walk(9)), 'prop_drift') == []
