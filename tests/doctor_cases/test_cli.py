import json
import os
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
    (tmp_path / 'pixellab.json').write_text(json.dumps({'look': 'painterly, soft anti-aliased edges'}), encoding='utf-8')
    r = json.loads(fix(tmp_path / 'k', '--json', '--check-only', '--profile', tmp_path / 'pixellab.json', cwd=tmp_path))
    assert 'soft_edge' not in {f['check'] for f in r['anims'][0]['findings_before']}
