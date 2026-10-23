"""Regression boundaries from the PR review: preserve source art and scope accepted repairs."""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
import synth
from fixlib import frames, plan
from fixlib.model import Finding
from test_measure_clean import anim

ASSETS = Path(__file__).resolve().parents[2] / 'skills/pixellab-pip/assets'


def cli(*args):
    return subprocess.run([sys.executable, str(ASSETS / 'fix.py'), *map(str, args)], capture_output=True, text=True)


def test_sheet_keeps_blank_cells_and_rejects_remainders(tmp_path):
    cells = [synth.figure(), np.zeros((synth.H, synth.W, 4), np.uint8), synth.figure()]
    src = tmp_path / 'sheet.png'
    Image.fromarray(np.concatenate(cells, 1)).save(src)
    (a,) = frames.load([str(src)], sheet=(synth.W, synth.H))
    assert len(a.frames) == 3 and not a.frames[1].any()
    bad = tmp_path / 'bad.png'
    Image.new('RGBA', (synth.W * 2 + 1, synth.H)).save(bad)
    result = cli(bad, '--sheet', f'{synth.W}x{synth.H}', '--out', tmp_path / 'out')
    assert result.returncode != 0 and not (tmp_path / 'out').exists()


def test_doctor_protects_sheet_container_and_reference_before_reports(tmp_path):
    src = tmp_path / 'fix_sheet.png'
    Image.fromarray(np.concatenate(synth.walk(3), 1)).save(src)
    before = src.read_bytes()
    result = cli(src, '--sheet', f'{synth.W}x{synth.H}', '--out', tmp_path)
    assert result.returncode != 0 and src.read_bytes() == before
    assert not (tmp_path / 'fix_report.json').exists()
    paths = synth.save(synth.walk(3), tmp_path / 'frames', 'hero_walk')
    result = cli(*paths, '--ref', src, '--out', tmp_path)
    assert result.returncode != 0 and src.read_bytes() == before
    assert not (tmp_path / 'fix_report.json').exists()


def test_batch_accept_is_rejected_before_writing(tmp_path):
    synth.save(synth.walk(3), tmp_path / 'frames', 'hero_walk')
    synth.save(synth.walk(3), tmp_path / 'frames', 'hero_idle')
    result = cli(tmp_path / 'frames', '--accept', 'c1', '--out', tmp_path / 'out')
    assert result.returncode != 0 and 'one animation' in result.stderr
    assert not (tmp_path / 'out').exists()


def test_inspection_report_points_to_existing_inputs(tmp_path):
    paths = synth.save(synth.walk(3), tmp_path / 'frames', 'hero_walk')
    out = tmp_path / 'inspection'
    result = cli(*paths, '--check-only', '--out', out)
    assert result.returncode == 0, result.stderr
    text = (out / 'fix_report.txt').read_text(encoding='utf-8')
    assert 'original inputs and reference' in text and 'fix_sheet.png' not in text
    assert sorted(p.name for p in out.iterdir()) == ['fix_report.json', 'fix_report.txt']


def test_opaque_container_exports_original_pixels_not_keyed_analysis(tmp_path):
    originals = [synth.solid_bg(f, (10, 20, 30)) for f in synth.walk(4)]
    src = tmp_path / 'hero_walk.png'
    Image.fromarray(np.concatenate(originals, 1)).save(src)
    (a,) = frames.load([str(src)], sheet=(synth.W, synth.H))
    assert a.backgrounds and all(c is not None for c in a.backgrounds)
    paths = frames.write(a, str(tmp_path / 'out'), changed=set())
    for path, original in zip(paths, originals):
        assert np.array_equal(np.asarray(Image.open(path).convert('RGBA')), original)
    preview = tmp_path / 'out/opaque.gif'
    from fixlib import report
    report.gif(str(preview), [frames.output_pixels(a, i, set()) for i in range(4)], [100] * 4)
    with Image.open(preview) as gif:
        assert gif.n_frames == 4 and gif.convert('RGBA').getpixel((0, 0)) == (10, 20, 30, 255)


def test_reroll_matches_exact_outputs_and_reports_ambiguous_owner(tmp_path):
    one, two = str(tmp_path / 'raw/attack.png'), str(tmp_path / 'raw/idle.png')
    manifest = tmp_path / 'manifest.json'
    records = [{'job_id': 'attack', 'status': 'ok', 'outputs': ['raw/attack.png']},
               {'job_id': 'idle', 'status': 'ok', 'outputs': ['raw/idle.png']}]
    manifest.write_text(json.dumps({'jobs': records}))
    assert plan.lookup_job([one], str(manifest))['job_id'] == 'attack'
    records.append({'job_id': 'conflict', 'status': 'ok', 'outputs': ['raw/attack.png']})
    manifest.write_text(json.dumps({'jobs': records}))
    assert plan.lookup_job([one], str(manifest)) is None
    assert plan.lookup_job([one, two], str(manifest)) is None


def test_reroll_count_minimum_and_canvas_boundaries():
    finding = Finding('missing_inbetween', [1], 1, 0.5, 'high', 'body', 'jump')
    (p,) = plan.make(anim(synth.walk(6)), [finding], None)
    assert p['frame_count'] == 4 and p['cost_estimate'] and p['schema_check_required']
    assert '2-4' not in p['prompt_change']
    a = anim(synth.walk(6))
    a.frames = [np.zeros((256, 257, 4), np.uint8)] * 6
    (p,) = plan.make(a, [finding], None)
    assert p['cost'] is None and p['requires_replan']


def test_accepted_drop_with_different_geometry_is_rejected():
    from fixlib import timing
    a = anim(synth.walk(6))
    a.sizes[2] = (synth.W - 2, synth.H)
    finding = Finding('jump', [2], 1, 0.5, 'high', 'body', 'jump')
    b, changes, durations, order = timing.run(a, [finding], accept={'c1'})
    assert order == list(range(6)) and durations == [100] * 6
    assert changes[0].result == 'still failing' and 'geometry' in changes[0].action
    assert all(np.array_equal(got, want) for got, want in zip(b.frames, a.frames))


def test_doctor_does_not_load_another_projects_cwd_style(tmp_path):
    from fix import load_style
    one = tmp_path / 'a'
    two = tmp_path / 'b'
    one.mkdir()
    two.mkdir()
    (one / 'pixellab.json').write_text(json.dumps({'look': 'soft anti-aliased edges'}))
    (two / 'pixellab.json').write_text(json.dumps({'look': 'hard edges'}))
    previous = os.getcwd()
    try:
        os.chdir(one)
        assert load_style(None) is None
        assert load_style(str(two / 'pixellab.json'))['soft_edges'] is False
    finally:
        os.chdir(previous)


def test_reroll_plans_exclude_approved_keys_and_protected_effect_frames(tmp_path):
    from fix import doctor
    from unittest.mock import patch
    a = anim(synth.walk(9))
    a.paths = synth.save(a.frames, tmp_path / 'frames', 'hero_attack')
    log = tmp_path / 'manifest.json'
    log.write_text(json.dumps({'jobs': [{'job_id': 'j', 'tool': 'MCP animate_image', 'status': 'ok',
                                       'outputs': [os.path.relpath(p, tmp_path) for p in a.paths]}]}))
    found = [Finding('weapon_lost', [1, 2], 1, 0.5, 'high', 'body', 'lost'),
             Finding('head_change', [5], 1, 0.5, 'high', 'body', 'changed')]
    for keys, fx in (({2}, set()), (set(), {2})):
        with patch('fix.measure.run', return_value=(found, [])), patch('fix.repair.run', return_value=(a, [])):
            _, result = doctor(a, set(), None, str(log), 'report.json', True, fx=fx, keys=keys)
        assert len(result['plans']) == 2
        assert all(2 not in p['frames'] and p['check'] != 'whole clip' for p in result['plans'])
        assert all(p['job']['job_id'] == 'j' for p in result['plans'])
