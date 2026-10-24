"""The six minor review findings (2026-10-21), one test each, written before the fix."""
import json
import os

import numpy as np
from PIL import Image

import synth
from conftest import SCRIPTS
from fixlib import measure
from test_cli import fix
import subprocess
import sys

from conftest import SCRIPTS


def run(script, *args, cwd=None):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *map(str, args)],
                          capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=cwd)
from test_measure_clean import anim
from test_measure_identity import CYAN


def test_report_counts_frames_like_the_file_names(tmp_path):
    fs = synth.walk(8)
    fs[3] = synth.specks_many(fs[3])                            # the 4th file: knight_attack_4.png
    synth.save(fs, tmp_path / 'k', 'knight_attack')
    r = json.loads(fix(tmp_path / 'k', '--json'))
    (f,) = [x for x in r['anims'][0]['findings_before'] if x['check'] == 'specks']
    assert f['frames'] == [4] and f['files'] == ['knight_attack_4.png']
    assert 'frame 4 ' in f['note']
    (c,) = [x for x in r['anims'][0]['changes'] if x['check'] == 'specks']
    assert c['frames'] == [4] and 'frame 4' in c['action']


def test_weird_change_is_one_finding_per_frame():
    fs = synth.walk(6)
    g = fs[3].copy()
    g[g[..., 3] > 0, :3] = (200, 60, 60)                        # the whole character recoloured for one frame
    fs[3] = g
    hits = [f for f in measure.run(anim(fs))[0] if f.check == 'weird_change']
    assert len(hits) == 1 and hits[0].frames == [3]


def test_check_only_keeps_gif_timing(tmp_path):
    paths = synth.save(synth.walk(3), tmp_path / 'src', 'k_idle')   # written by our own GIF writer: Pillow's drops alpha
    assert run('preview_gif.py', tmp_path / 'hero_idle.gif', *paths, '--durations', '80,160,240').returncode == 0
    fix(tmp_path / 'hero_idle.gif', '--check-only', '--out', tmp_path / 'o')
    out = fix(tmp_path / 'hero_idle.gif', '--out', tmp_path / 'o2')
    t = json.load(open(tmp_path / 'o2' / 'timing.json', encoding='utf-8'))
    assert t['hero/idle']['durations'] == [80, 160, 240]
    r = json.load(open(tmp_path / 'o' / 'fix_report.json', encoding='utf-8'))
    assert r['anims'][0]['durations'] == [80, 160, 240]


def test_sheet_output_keeps_the_sheet_name(tmp_path):
    sheet = np.concatenate(synth.walk(3), 1)
    Image.fromarray(sheet, 'RGBA').save(tmp_path / 'Big Boss Sheet.png')
    fix(tmp_path / 'Big Boss Sheet.png', '--sheet', '%dx%d' % (synth.W, synth.H), '--out', tmp_path / 'o')
    assert {'Big Boss Sheet_1.png', 'Big Boss Sheet_2.png', 'Big Boss Sheet_3.png'} <= set(os.listdir(tmp_path / 'o'))


def test_faithful_preview_reports_a_duration_mismatch_plainly(tmp_path):
    paths = synth.save(synth.walk(3), tmp_path, 'k_idle')
    r = run('preview_gif.py', tmp_path / 'p.gif', *paths, '--durations', '100,100')
    assert r.returncode != 0 and 'Traceback' not in r.stderr and 'duration' in (r.stderr + r.stdout)
