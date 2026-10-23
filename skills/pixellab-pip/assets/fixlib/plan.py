"""Re-roll plans for what the free fixes couldn't cure, and the verdict. RULES is the one table of defect -> likely cause
-> the tool and the one wording change that addresses it; references/fix.md prints it (fix.py --table), and
/pga-reroll reads the plans this writes into fix_report.json."""
import json
import math
import os


def _pro_flash(anim, frames):
    side = max(anim.frames[0].shape[:2])
    return (5 if side <= 96 else 6 if side <= 200 else 9) * len(frames)


def _animate(anim, frames):
    h, w = anim.frames[0].shape[:2]
    return math.ceil(w * h * max(2, len(frames)) / 65536)


PF, AN = 'edit_image_pro_flash', 'animate_image'
RULES = {
    'weapon_lost': dict(cause='the pose prompt left the weapon out, so the generator dropped it',
                        tool=PF, prompt_change='write the weapon into the pose ("... raising the staff high in both hands")', cost=_pro_flash),
    'broken_thin': dict(cause='thin parts (blades, staffs) break when a pose is redrawn',
                        tool=PF, prompt_change='name the weapon and its whole length in the pose; the reference as style image', cost=_pro_flash),
    'flash': dict(cause='the action words invited a painted effect (burst, swipe)',
                  tool=AN, prompt_change='motion only, no burst, no swipe arc ("... in one fast snap")', cost=_animate),
    'weird_change': dict(cause='the in-between redrew part of the character',
                         tool=PF, prompt_change='same face, same outfit as the reference; the reference as style image', cost=_pro_flash),
    'head_change': dict(cause='the in-between redrew the head: turned it away or toward the viewer, or changed the skin colour',
                        tool=PF, prompt_change='the same face, facing the same way as the frames around it, the same skin colour; the reference as style image', cost=_pro_flash),
    'jump': dict(cause='an in-between left the motion path',
                 tool=AN, prompt_change='pin the path in the action ("the same arc, smoothly")', cost=_animate),
    'missing_inbetween': dict(cause='too few frames for that span of the move',
                              tool=AN, prompt_change='animate between these two frames (first_frame + last_frame), 2-4 frames', cost=_animate),
    'size_pop': dict(cause='a frame was drawn at another size', tool=PF,
                     prompt_change='the same size as the reference; the reference as style image', cost=_pro_flash),
    'loop_seam': dict(cause="the loop's last frame doesn't lead back to its first",
                      tool=AN, prompt_change='animate from the last frame back to the first (last_frame = frame 0)', cost=_animate),
    'return_to_stand': dict(cause='the move ends away from the standing pose',
                            tool=AN, prompt_change='animate from the last frame back to the standing pose', cost=_animate),
    'edge': dict(cause='the pose touches the canvas border, so every in-between is cut',
                 tool=PF, prompt_change='re-pose on a canvas with more room on that side', cost=_pro_flash),
    'detached': dict(cause='a piece came off the body (a thrown weapon or a floating bit)',
                     tool=PF, prompt_change='write the weapon into the pose, held in the hand', cost=_pro_flash),
    'grid': dict(cause='the frame was drawn at another pixel size than the set',
                 tool=PF, prompt_change='re-draw the frame at the set\'s pixel size (no upscaling)', cost=_pro_flash),
    'mixels': dict(cause='mixed pixel sizes in one frame (an upscale painted over)',
                   tool=PF, prompt_change='re-draw the frame at the set\'s pixel size (no upscaling)', cost=_pro_flash),
    'size': dict(cause='the character is drawn bigger or smaller than the reference (a prop added on purpose, like a bow on the back, makes it taller: pass the new sprite as --ref)',
                 tool=PF, prompt_change='the same size as the reference; the reference as style image', cost=_pro_flash),
    'brightness': dict(cause='a washed-out frame (colour matching would turn it muddy)',
                       tool=PF, prompt_change='the reference as style image, colour palette correction on', cost=_pro_flash),
    'palette': dict(cause='the frame was drawn in other colours',
                    tool=PF, prompt_change='the reference as style image, colour palette correction on', cost=_pro_flash),
    'empty': dict(cause='the generator returned an empty frame', tool=AN, prompt_change='re-run the same span', cost=_animate),
}


def table() -> str:
    rows = ['| check | likely cause | tool | the change to make |', '|---|---|---|---|']
    rows += ['| `%s` | %s | `%s` | %s |' % (c, r['cause'], r['tool'], r['prompt_change']) for c, r in RULES.items()]
    return '\n'.join(rows)


def lookup_job(frame_paths, manifest_path, name=None):
    """The newest manifest entry (Pip's run record) whose outputs hold these frames: it names the job a re-roll redoes."""
    if not manifest_path or not os.path.exists(manifest_path):
        return None
    run = os.path.dirname(os.path.abspath(manifest_path))
    try:
        with open(manifest_path, encoding='utf-8-sig') as fh:
            entries = json.load(fh).get('jobs', [])
    except (ValueError, AttributeError):
        return None
    dirs = {os.path.normcase(os.path.abspath(os.path.dirname(p))) for p in frame_paths}
    best = None
    for e in entries:   # later entries are newer
        outs = {os.path.normcase(os.path.abspath(os.path.join(run, o))) for o in e.get('outputs', [])}
        if any(os.path.dirname(o) in dirs for o in outs) and e.get('status', 'ok') == 'ok':
            best = e
    return best



def make(anim, still_failing, log_path, report='fix_report.json'):
    """One plan per mid/high finding still failing (low ones are noted, not re-rolled)."""
    stem = os.path.splitext(os.path.basename(anim.paths[0]))[0].rsplit('_', 1)[0] if anim.paths else anim.key.replace('/', '_')
    job = lookup_job(anim.paths, log_path, stem)
    plans = {}
    for f in still_failing:
        if f.severity == 'low' or f.check not in RULES:
            continue
        r = RULES[f.check]
        k = (tuple(f.frames), r['tool'])
        if k in plans:   # one re-roll per frame fixes every check on it (brightness + palette came as two 6-gen plans)
            p = plans[k]
            p['check'] += ', ' + f.check
            p['why'] += '; ' + f.note
            p['prompt_change'] += '; ' + r['prompt_change']
            continue
        plans[k] = {'check': f.check, 'frames': list(f.frames), 'why': f.note, 'cause': r['cause'], 'tool': r['tool'],
                    'prompt_change': r['prompt_change'], 'cost': int(r['cost'](anim, f.frames)), 'job': job}
    plans = list(plans.values())
    job_cost = (job or {}).get('reported_usage', {}).get('generations', 1e9)
    if job and 'animate_image' in job.get('tool', '') and len(plans) > 1 and sum(p['cost'] for p in plans) > job_cost:
        plans = [{'check': 'whole clip', 'frames': list(range(len(anim.frames))), 'why': '; '.join(p['why'] for p in plans),
                  'cause': 'cheaper than %d frame re-rolls (%d gen)' % (len(plans), sum(p['cost'] for p in plans)),
                  'tool': 'animate_image', 'prompt_change': 'same key frames, a new seed; the action says motion only, '
                  'and names any prop that must stay (the empty scabbard at the hip)', 'cost': int(job_cost), 'job': job}]
    for n, p in enumerate(plans, 1):
        p['reroll'] = '/pga-reroll fix:%s %s %d' % (report, anim.key, n)
    return plans


def verdict(findings_before, findings_after, changes) -> str:
    serious = lambda fs: [f for f in fs if f.severity in ('mid', 'high')]
    if not serious(findings_before) and not any(c.result == 'fixed' for c in changes):
        return 'ready'
    return 'needs re-rolls' if serious(findings_after) else 'ready after free fixes'
