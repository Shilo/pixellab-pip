import os

import numpy as np
from PIL import Image

import synth
from fixlib import frames


def _arr(p):
    return np.array(Image.open(p).convert('RGBA'))


def test_folder_batch_groups_by_character_and_move(tmp_path):
    synth.save(synth.walk(9), tmp_path, 'knight_attack')
    synth.save(synth.walk(6), tmp_path, 'knight_idle')
    synth.save(synth.walk(4), tmp_path, 'mage_attack')
    anims = {a.key: a for a in frames.load([str(tmp_path)])}
    assert set(anims) == {'knight/attack', 'knight/idle', 'mage/attack'}
    assert anims['knight/idle'].kind == 'loop' and anims['knight/attack'].kind == 'oneshot'
    assert anims['knight/idle'].kind_guessed and anims['knight/attack'].kind_guessed
    assert len(anims['knight/attack'].frames) == 9


def test_sheet_and_gif(tmp_path):
    fs = synth.walk(4)
    sheet = np.concatenate(fs, 1)
    Image.fromarray(sheet, 'RGBA').save(tmp_path / 'hero_walk.png')
    (a,) = frames.load([str(tmp_path / 'hero_walk.png')], sheet=(synth.W, synth.H))
    assert len(a.frames) == 4 and np.array_equal(a.frames[2], fs[2])
    ims = [Image.fromarray(f, 'RGBA') for f in fs[:2]]
    ims[0].save(tmp_path / 'g.gif', save_all=True, append_images=ims[1:], duration=[100, 200], loop=0, disposal=2)
    (g,) = frames.load([str(tmp_path / 'g.gif')])
    assert g.durations == [100, 200] and len(g.frames) == 2


def test_reference_guess(tmp_path):
    idle = synth.walk(5)
    synth.save(idle, tmp_path, 'knight_idle')
    synth.save(synth.walk(9), tmp_path, 'knight_attack')
    anims = {a.key: a for a in frames.load([str(tmp_path)])}
    a = anims['knight/attack']
    assert a.ref_guessed
    med = np.median(np.stack([f.astype(float) for f in idle]), 0)
    best = min(range(5), key=lambda i: np.abs(idle[i].astype(float) - med).sum())
    assert np.array_equal(a.ref, idle[best])


def test_given_reference_is_not_guessed(tmp_path):
    paths = synth.save(synth.walk(4), tmp_path, 'knight_attack')
    Image.fromarray(synth.figure(), 'RGBA').save(tmp_path.parent / 'still.png')
    (a,) = frames.load(paths, ref=str(tmp_path.parent / 'still.png'))
    assert not a.ref_guessed and np.array_equal(a.ref, synth.figure())


def test_detect_scale():
    assert frames.detect_scale(synth.upscale(synth.figure(), 4)) == 4
    assert frames.detect_scale(synth.figure()) == 1


def test_opaque_background_is_keyed(tmp_path):
    fs = [synth.solid_bg(f, (255, 0, 255)) for f in synth.walk(3)]
    synth.save(fs, tmp_path, 'knight_idle')
    (a,) = frames.load([str(tmp_path)])
    assert np.array_equal(a.frames[0][..., 3] > 0, synth.walk(3)[0][..., 3] > 0)
    assert a.bg == (255, 0, 255)


def test_mixed_canvas_sizes(tmp_path):
    big = synth.figure()
    small = big[6:, 4:44]                       # 40x50, same feet
    Image.fromarray(big, 'RGBA').save(tmp_path / 'k_idle_1.png')
    Image.fromarray(small, 'RGBA').save(tmp_path / 'k_idle_2.png')
    (a,) = frames.load([str(tmp_path)])
    assert a.frames[0].shape == a.frames[1].shape == (56, 48, 4)
    assert a.sizes == [(48, 56), (40, 50)]
    out = tmp_path / 'out'
    frames.write(a, str(out))
    assert np.array_equal(_arr(out / 'k_idle_2.png'), small)


def test_natural_order_and_literal_glob(tmp_path):
    d = tmp_path / 'my frames'
    fs = synth.walk(11)
    names = ['f %d.png' % i for i in range(1, 11)] + ['ç_1.png']
    d.mkdir()
    for f, n in zip(fs, names):
        Image.fromarray(f, 'RGBA').save(d / n)
    anims = {a.key: a for a in frames.load([str(d / '*.png')])}
    f = anims['f/other']
    assert [os.path.basename(p) for p in f.paths][:3] == ['f 1.png', 'f 2.png', 'f 3.png']
    assert os.path.basename(f.paths[-1]) == 'f 10.png'
    assert 'ç/other' in anims


def test_write_roundtrip(tmp_path):
    src = synth.save(synth.walk(4), tmp_path / 'in', 'knight_attack')
    (a,) = frames.load(src)
    written = frames.write(a, str(tmp_path / 'out'))
    assert [os.path.basename(p) for p in written] == [os.path.basename(p) for p in src]
    for s, w in zip(src, written):
        assert np.array_equal(_arr(s), _arr(w))
