import numpy as np
from PIL import Image

import synth
from test_measure_clean import anim, found


def up4(n):
    return [synth.upscale(f, 4) for f in synth.walk(n)]


def test_clean_upscaled_set_is_crisp():
    a = anim(up4(6), 'walk', ref=synth.upscale(synth.figure(), 4))
    a.scale = 4
    for c in ('grid', 'mixels', 'soft_edge', 'colour_count', 'size'):
        assert found(a, c) == [], c


def test_grid_and_mixels():
    fs = up4(6)
    g = fs[3].copy()
    body = (g[..., :3] == synth.BLUE).all(-1)
    yy, xx = np.indices(body.shape)
    g[body & ((yy // 2 + xx // 2) % 2 == 0), :3] = synth.SHADE    # 2 px detail inside a 4 px set
    fs[3] = g
    a = anim(fs, 'walk', ref=synth.upscale(synth.figure(), 4))
    a.scale = 4
    assert found(a, 'grid') == [3]
    assert found(a, 'mixels') == [3]


def test_soft_edges_and_colour_count():
    fs = synth.walk(6)
    fs[2] = synth.blur_edges(fs[2])
    fs[3] = synth.noisy(fs[3])
    a = anim(fs)
    assert found(a, 'soft_edge') == [2]
    assert found(a, 'colour_count') == [3]
    assert found(a, 'soft_edge', style={'soft_edges': True}) == []


def test_size():
    fs = synth.walk(6)
    big = np.array(Image.fromarray(fs[4], 'RGBA').resize((55, 64), Image.NEAREST))
    frame = np.zeros_like(fs[4])
    crop = big[8:64, 3:51]                                       # 15% bigger, feet near row 53 after the crop
    frame[:crop.shape[0], :crop.shape[1]] = crop
    fs[4] = frame
    assert found(anim(fs, 'walk'), 'size') == [4]
    assert found(anim(fs, 'attack'), 'size') == []          # a mid-move pose may stand taller or crouch
