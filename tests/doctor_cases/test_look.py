"""The samurai test (2026-10-21): what pixels can't catch goes to a look checklist, and re-roll plans stop
costing more than a fresh clip."""
import json
import os

from PIL import Image

import synth
from fixlib import plan
from test_cli import fix, report
from test_measure_clean import anim
from test_plan import F


def test_sheet_puts_the_reference_first(tmp_path):
    fs = synth.walk(4)
    synth.save(fs, tmp_path / 'k', 'knight_walk')
    ref = synth.figure()
    Image.fromarray(ref, 'RGBA').save(tmp_path / 'ref.png')
    fix(tmp_path / 'k', '--ref', tmp_path / 'ref.png', '--out', tmp_path / 'o')
    sheet = Image.open(tmp_path / 'o' / 'fix_sheet.png')
    z, pad = 2, 4
    assert sheet.width == 5 * (synth.W * z + pad) + pad        # reference + 4 frames
    cell = sheet.crop((pad, pad, pad + synth.W * z, pad + synth.H * z)).resize((synth.W, synth.H), Image.NEAREST)
    assert cell.getpixel((synth.W // 2, synth.H // 2)) == Image.fromarray(ref, 'RGBA').getpixel((synth.W // 2, synth.H // 2))


def test_report_carries_the_look_checklist(tmp_path):
    synth.save(synth.walk(4), tmp_path / 'k', 'knight_walk')
    out = fix(tmp_path / 'k', '--out', tmp_path / 'o')
    r = report(tmp_path / 'o')
    assert any('arms' in q for q in r['look']) and any('scabbard' in q for q in r['look'])
    assert any('reversed' in q for q in r['look']) and any('second hilt' in q for q in r['look'])
    assert any('shoulder plates' in q for q in r['look']) and any('neither key pose' in q for q in r['look'])
    assert any('like the idle' in q for q in r['look']) and any('one straight line' in q for q in r['look'])
    # e2e demo (frost mage): a staff swapping hands, a one-frame head turn and a thrown shard were not on the list
    assert any('same hand' in q for q in r['look']) and any('head turned' in q for q in r['look'])
    assert any('projectile' in q for q in r['look'])
    assert 'look at fix_sheet.png' in out.lower()


def test_one_plan_per_frame_not_per_check():
    plans = plan.make(anim(synth.walk(9)), [F('brightness', [7]), F('palette', [7])], None)
    assert len(plans) == 1 and plans[0]['frames'] == [7] and plans[0]['check'] == 'brightness, palette'


def test_a_fresh_clip_replaces_dearer_frame_plans(tmp_path):
    out = tmp_path / 'skill'
    paths = synth.save(synth.walk(9), out, 'knight_skill')
    log = tmp_path / 'manifest.json'
    rel = [os.path.relpath(p, tmp_path).replace(os.sep, '/') for p in paths]
    log.write_text(json.dumps({'jobs': [{'job_id': 'j-9', 'tool': 'MCP animate_image', 'status': 'ok',
                                         'reported_usage': {'generations': 4}, 'outputs': rel}]}), encoding='utf-8')
    a = anim(synth.walk(9))
    a.paths = paths
    plans = plan.make(a, [F('brightness', [6]), F('brightness', [7]), F('brightness', [8])], str(log))
    (p,) = plans
    assert p['check'] == 'whole clip' and p['tool'] == 'animate_image' and p['cost'] == 4
    assert p['frames'] == list(range(9)) and p['job']['job_id'] == 'j-9'


def test_look_checklist_covers_bows_and_one_way_moves(tmp_path):
    # the archer test (2026-10-22): a string vanished, the nock floated off the hand, and the raise drew the bow
    # overhead and the next key pose drew it again from slack
    synth.save(synth.walk(4), tmp_path / 'k', 'archer_attack')
    fix(tmp_path / 'k', '--out', tmp_path / 'o')
    look = report(tmp_path / 'o')['look']
    assert any('string' in q and 'nock' in q for q in look)
    assert any('undone' in q for q in look)


def test_look_checklist_covers_grip_and_shield(tmp_path):
    # weapon references (01-sword, 2026-10-22): a longsword keeps both hands on the hilt; a buckler stays on its arm
    synth.save(synth.walk(4), tmp_path / 'k', 'knight_attack')
    fix(tmp_path / 'k', '--out', tmp_path / 'o')
    look = report(tmp_path / 'o')['look']
    assert any('both hands' in q and 'shield' in q for q in look)
