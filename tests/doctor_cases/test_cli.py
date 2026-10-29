import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image

import synth
from conftest import SCRIPTS
from test_measure_identity import CYAN

FIX = os.path.join(SCRIPTS, 'fix.py')


def fix(*args, cwd=None):
    r = subprocess.run([sys.executable, FIX, *map(str, args)], capture_output=True, text=True, encoding='utf-8', cwd=cwd)
    assert r.returncode == 0, r.stderr
    return r.stdout


def report(out):
    return json.load(open(os.path.join(out, 'fix_report.json'), encoding='utf-8'))


def test_colour_approval_cannot_redirect_a_later_timing_approval(tmp_path):
    fs = synth.walk(12)
    fs[3] = synth.bright(fs[3], 1.3)
    for i in (3, 4, 5):
        fs[i] = synth.flash(fs[i], (2, 2, 9, 9), (0, 0, 0))
    for i in (6, 9):
        fs[i] = synth.bright(fs[i], 1.9)
    source = synth.save(fs, tmp_path / 'frames', 'hero_attack')
    originals = [Path(path).read_bytes() for path in source]
    reference = synth.png(synth.figure(), tmp_path / 'reference.png')
    fix(tmp_path / 'frames', '--ref', reference, '--out', tmp_path / 'pending')
    pending = report(tmp_path / 'pending')['anims'][0]
    colour = next(c for c in pending['proposals'] if c['check'] in ('brightness', 'palette', 'colour_count'))
    drop = next(c for c in pending['proposals'] if c['check'] == 'timing' and c['frames'] == [7])
    assert not any(p['check'] in ('brightness', 'palette', 'colour_count') for p in pending['plans'])
    fix(tmp_path / 'frames', '--ref', reference, '--accept', colour['id'] + ',' + drop['id'],
        '--out', tmp_path / 'accepted')
    accepted = report(tmp_path / 'accepted')['anims'][0]
    drops = [c for c in accepted['changes'] if c['check'] == 'timing' and c['result'] == 'fixed']
    assert len(drops) == 1 and drops[0]['id'] == drop['id'] and drops[0]['frames'] == [7]
    assert accepted['durations'][6] == 0 and accepted['durations'][9] > 0
    with Image.open(tmp_path / 'accepted' / 'hero_attack_10.png') as image:
        assert np.array_equal(np.asarray(image), fs[9])
    assert all(Path(path).read_bytes() == before for path, before in zip(source, originals))


def test_clean_set_is_ready_and_untouched(tmp_path):
    src = synth.save(synth.walk(8), tmp_path / 'knight', 'knight_idle')
    fix(tmp_path / 'knight')
    out = str(tmp_path / 'knight') + '_fixed'
    r = report(out)
    assert r['verdict'] == 'ready' and r['totals']['changes'] == 0
    for p in src:
        assert open(p, 'rb').read() == open(os.path.join(out, os.path.basename(p)), 'rb').read()


def test_free_fixes_then_a_question(tmp_path):
    fs = synth.walk(8)
    fs[1] = synth.specks_many(fs[1])
    fs[2] = synth.bright(fs[2], 1.3)
    fs[5] = synth.flash(fs[5], (36, 20, 44, 28), CYAN)
    synth.save(fs, tmp_path / 'k', 'knight_attack')
    fix(tmp_path / 'k')
    out = str(tmp_path / 'k') + '_fixed'
    r = report(out)
    (a,) = r['anims']
    assert r['verdict'] == 'ready after free fixes' and not a['plans']   # the question, not a paid re-roll
    (p,) = a['proposals']
    assert p['check'] == 'flash'
    assert {c['check'] for c in a['changes'] if c['result'] == 'fixed'} >= {'specks', 'brightness'}
    for name in ('fix_report.txt', 'fix_sheet.png', 'timing.json', 'knight_attack_preview.gif'):
        assert os.path.exists(os.path.join(out, name)), name
    fix(tmp_path / 'k', '--accept', p['id'], '--out', tmp_path / 'accepted')
    r2 = report(str(tmp_path / 'accepted'))
    assert r2['verdict'] == 'ready after free fixes'
    assert np.array(Image.open(tmp_path / 'accepted' / 'knight_attack_6.png'))[24, 40, 3] == 0   # the flash is gone


def test_check_only_writes_only_the_reports(tmp_path):
    fs = synth.walk(6)
    fs[1] = synth.speck(fs[1], (2, 50))
    synth.save(fs, tmp_path / 'k', 'knight_attack')
    fix(tmp_path / 'k', '--check-only')
    out = str(tmp_path / 'k') + '_fixed'
    assert sorted(os.listdir(out)) == ['fix_report.json', 'fix_report.txt']


def test_json_to_stdout(tmp_path):
    synth.save(synth.walk(6), tmp_path / 'k', 'knight_idle')
    r = json.loads(fix(tmp_path / 'k', '--json'))
    assert r['version'] == 1 and r['anims'][0]['key'] == 'knight/idle'


def test_table_command_lists_repair_choices():
    from fixlib import plan
    text = fix('--table')
    assert text == plan.table() + '\n'


def test_style_soft_edges_from_the_profile(tmp_path):
    fs = synth.walk(6)
    fs[2] = synth.blur_edges(fs[2])
    synth.save(fs, tmp_path / 'k', 'knight_idle')
    (tmp_path / 'pixellab-pip-style.json').write_text(json.dumps({'look': 'painterly, soft anti-aliased edges'}), encoding='utf-8')
    r = json.loads(fix(tmp_path / 'k', '--json', '--check-only', '--profile', tmp_path / 'pixellab-pip-style.json', cwd=tmp_path))
    assert 'soft_edge' not in {f['check'] for f in r['anims'][0]['findings_before']}


def test_default_output_stays_beside_input_files(tmp_path):
    # review: a sheet in the project root wrote to <project>_fixed, outside the project
    import argparse
    import importlib.util
    spec = importlib.util.spec_from_file_location('fix_cli', FIX)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = lambda first: mod._out_dir(argparse.Namespace(out=None, inputs=[str(first)]), [])
    (tmp_path / 'clip').mkdir()
    assert out(tmp_path / 'clip') == str(tmp_path / 'clip') + '_fixed'
    assert out(tmp_path / 'sheet.png') == str(tmp_path / 'sheet_fixed')
    assert out(tmp_path / 'clip' / '*.png') == str(tmp_path / 'clip' / 'frames_fixed')


def test_empty_frames_never_become_the_reference(tmp_path):
    # review: an empty first frame became the "typical" reference and the checks crashed on it
    from fixlib import frames as framesmod
    empty = np.zeros((8, 8, 4), np.uint8)
    body = empty.copy()
    body[2:6, 2:6] = (200, 40, 40, 255)
    assert framesmod._typical([empty, body, body]) is not empty
    try:
        framesmod._typical([empty, empty])
    except ValueError as exc:
        assert 'empty' in str(exc)
    else:
        raise AssertionError('all-empty frames must be refused')
    Image.fromarray(empty, 'RGBA').save(tmp_path / 'blank.png')
    r = subprocess.run([sys.executable, FIX, str(tmp_path / 'blank.png'), '--ref', str(tmp_path / 'blank.png'),
                        '--check-only', '--out', str(tmp_path / 'o')], capture_output=True, text=True)
    assert r.returncode == 2 and 'no visible pixels' in r.stderr and not (tmp_path / 'o').exists()
