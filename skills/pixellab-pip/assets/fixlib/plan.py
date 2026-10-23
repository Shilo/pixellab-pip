"""Re-roll plans for what the free fixes couldn't cure, and the verdict. RULES is the one table of defect -> likely cause
-> the tool and the one wording change that addresses it; references/fix.md prints it (fix.py --table), and
A re-roll request names a plan this writes into fix_report.json."""
import json
import math
import os


def _pro_flash(anim, frames):
    side = max(anim.frames[0].shape[:2])
    return (5 if side <= 96 else 6 if side <= 200 else 9) * len(frames)


def _animate(anim, frames):
    h, w = anim.frames[0].shape[:2]
    return math.ceil(w * h * max(4, min(16, (len(frames) + 1) // 2 * 2)) / 65536)


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
                              tool=AN, prompt_change='animate between these two frames (first_frame + last_frame), 4 generated frames (plus the echoed input)', cost=_animate),
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


def lookup_job(frame_paths, manifest_path):
    """The unique manifest entry whose recorded outputs include every supplied source frame."""
    if not manifest_path or not os.path.exists(manifest_path):
        return None
    run = os.path.dirname(os.path.abspath(manifest_path))
    try:
        with open(manifest_path, encoding='utf-8-sig') as fh:
            entries = json.load(fh).get('jobs', [])
    except (ValueError, AttributeError):
        return None
    wanted = {os.path.normcase(os.path.realpath(p)) for p in frame_paths}
    if not wanted or not isinstance(entries, list):
        return None
    matches = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get('outputs'), list):
            continue
        if not all(isinstance(o, str) for o in entry['outputs']):
            continue
        outs = {os.path.normcase(os.path.realpath(os.path.join(run, o))) for o in entry['outputs']}
        if wanted <= outs and entry.get('status', 'ok') == 'ok':
            matches.append(entry)
    # Shared folders and conflicting ownership are not evidence of a particular source job.
    return matches[0] if len(matches) == 1 else None




def make(anim, still_failing, log_path, report='fix_report.json', *, allow_whole_clip=True):
    """One plan per mid/high finding still failing (low ones are noted, not re-rolled)."""
    job = lookup_job(anim.paths or ([anim.source] if anim.source else []), log_path)
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
    for p in plans:
        p['cost_estimate'] = True
        p['schema_check_required'] = True
        if p['tool'] == AN:
            h, w = anim.frames[0].shape[:2]
            count = max(4, min(16, (len(p['frames']) + 1) // 2 * 2))
            p['frame_count'] = count
            if max(w, h) > 256 or w * h * count > 524288:
                p['cost'] = None
                p['requires_replan'] = 'input canvas/frame count exceeds raw v3 limits; choose an approved supported route'
    # Offer the cheaper whole-clip retry only for an unambiguous complete raw v3 result.
    # Historical charged usage is not a current quote.
    if allow_whole_clip and job and job.get('tool') in ('animate_image', 'MCP animate_image') and len(plans) > 1:
        count = len(anim.frames) - 1
        h, w = anim.frames[0].shape[:2]
        whole_cost = math.ceil(w * h * count / 65536)
        if (4 <= count <= 16 and count % 2 == 0 and max(w, h) <= 256
                and w * h * count <= 524288 and len(job.get('outputs', [])) == len(anim.paths)
                and all(p['cost'] is not None for p in plans) and sum(p['cost'] for p in plans) > whole_cost):
            plans = [{'check': 'whole clip', 'frames': list(range(len(anim.frames))),
                      'why': '; '.join(p['why'] for p in plans),
                      'cause': 'estimated cheaper than the listed frame repairs; confirm current route and inputs',
                      'tool': AN, 'prompt_change': 'same key frames, motion-only action naming the props that must stay',
                      'frame_count': count, 'cost': whole_cost, 'cost_estimate': True,
                      'schema_check_required': True, 'job': job}]
    for n, p in enumerate(plans, 1):
        p['reroll'] = 'Re-roll plan %d for %s in %s' % (n, anim.key, report)   # what the user says to run it
    return plans


def verdict(findings_before, findings_after, changes) -> str:
    serious = lambda fs: [f for f in fs if f.severity in ('mid', 'high')]
    if not serious(findings_before) and not any(c.result == 'fixed' for c in changes):
        return 'ready'
    return 'needs re-rolls' if serious(findings_after) else 'ready after free fixes'
