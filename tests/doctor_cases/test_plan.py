import json
import os

import synth
from fixlib import plan
from fixlib.model import Change, Finding
from test_measure_clean import anim


def F(check, frames, sev='high'):
    return Finding(check, frames, 1.0, 0.5, sev, 'body', 'x')


def test_weapon_lost_plan_finds_the_job(tmp_path):
    # the merge: the original job comes from the run's manifest.json (Pip's one record), not a log
    out = tmp_path / 'out' / 'knight_attack'
    paths = synth.save(synth.walk(9), out, 'knight_attack')
    rel = [os.path.relpath(p, tmp_path).replace(os.sep, '/') for p in paths]
    log = tmp_path / 'manifest.json'
    log.write_text(json.dumps({'jobs': [
        {'job_id': 'old', 'tool': 'MCP animate_image', 'status': 'ok', 'reported_usage': {'generations': 3}, 'outputs': ['old/unrelated.png']},
        {'job_id': 'j-123', 'tool': 'MCP animate_image', 'status': 'ok', 'reported_usage': {'generations': 3}, 'outputs': rel,
         'outcome': 'kept'}]}), encoding='utf-8')
    a = anim(synth.walk(9))
    a.paths = paths
    (p,) = plan.make(a, [F('weapon_lost', [5])], str(log))
    assert p['tool'] == 'edit_image_pro_flash' and p['frames'] == [5]
    assert 'write the weapon into the pose' in p['prompt_change']
    assert p['cost'] == 5                                    # 48 x 56 canvas: the <= 96 px tier
    assert p['job']['job_id'] == 'j-123'
    assert p['reroll'] == 'Re-roll plan 1 for %s in fix_report.json' % a.key   # a plain request: no /pga-* command


def test_no_log_means_no_job():
    (p,) = plan.make(anim(synth.walk(9)), [F('flash', [3])], None)
    assert p['job'] is None and p['tool'] == 'animate_image'
    assert 'motion only' in p['prompt_change']
    assert p['cost'] == 1                                    # ceil(48*56*2/65536)


def test_every_failing_check_has_a_plan():
    for check in plan.RULES:
        (p,) = plan.make(anim(synth.walk(6)), [F(check, [2])], None)
        assert p['tool'] and p['prompt_change'] and p['cost'] >= 0


def test_low_findings_get_no_plan():
    assert plan.make(anim(synth.walk(6)), [F('specks', [2], 'low')], None) == []


def test_verdicts():
    assert plan.verdict([], [], []) == 'ready'
    assert plan.verdict([F('specks', [1], 'low')], [], []) == 'ready'
    assert plan.verdict([F('brightness', [1], 'mid')], [], [Change('c1', 'brightness', [1], 'x', 'fixed')]) == 'ready after free fixes'
    assert plan.verdict([F('flash', [1])], [F('flash', [1])], [Change('c1', 'flash', [1], 'x', 'proposed')]) == 'needs re-rolls'


def test_table_lists_every_rule():
    t = plan.table()
    for check in plan.RULES:
        assert '| `%s` |' % check in t


def test_head_change_plan_names_the_face():
    # e2e demo: a one-frame head turn needs a re-roll that pins the face and its direction
    (p,) = plan.make(anim(synth.walk(6)), [F('head_change', [2], 'mid')], None)
    assert p['tool'] == 'edit_image_pro_flash' and 'face' in p['prompt_change']


def test_whole_clip_requires_exact_raw_v3_source_route(tmp_path):
    paths = synth.save(synth.walk(9), tmp_path / 'frames', 'hero_attack')
    a = anim(synth.walk(9))
    a.paths = paths
    rel = [os.path.relpath(p, tmp_path).replace(os.sep, '/') for p in paths]
    log = tmp_path / 'manifest.json'
    for tool in ('animate_image_pixminimax', 'MCP animate_image_pixminimax',
                 'unrelated_animate_image_suffix', 'animate_image', 'MCP animate_image'):
        log.write_text(json.dumps({'jobs': [{'job_id': 'j', 'tool': tool, 'status': 'ok', 'outputs': rel}]}))
        result = plan.make(a, [F('weapon_lost', [2]), F('head_change', [5])], str(log))
        if tool in ('animate_image', 'MCP animate_image'):
            assert len(result) == 1 and result[0]['check'] == 'whole clip'
            assert result[0]['frame_count'] == 8
        else:
            assert len(result) == 2 and all(p['check'] != 'whole clip' for p in result)
