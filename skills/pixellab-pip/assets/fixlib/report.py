"""The animation doctor's outputs: fix_report.json (for the agent), fix_report.txt (for a person), fix_sheet.png (analyzed input row,
fixed row, flagged frames outlined) and a preview GIF per animation."""
import json
import os
from dataclasses import asdict

import numpy as np
from PIL import Image, ImageDraw

BG = (0, 0, 0, 0)
FLAG = (255, 70, 70, 255)
ORDER = {'ready': 0, 'ready after free fixes': 1, 'needs re-rolls': 2}


def _number(d, names):
    """Frames counted from 1 like the file names, and the file names themselves."""
    d['files'] = [names[i] for i in d['frames'] if 0 <= i < len(names)]
    d['frames'] = [i + 1 for i in d['frames']]
    return d


def finding(f, names):
    return _number(asdict(f), names)


def change(c, names):
    d = asdict(c)
    d.pop('data', None)
    return _number(d, names)


LOOK = [   # what pixel checks can't see (the samurai test: an extra hand, a vanished scabbard, a short blade)
    'arms, hands and legs: the same count as the reference in every frame, each joined to the body',
    'props from the reference (scabbard, sheath, quiver, shield, belt items) stay where they belong; a drawn sword leaves its empty scabbard at the hip',
    'props point the same way and sit on the same side as in the reference (hilt forward, scabbard running back), never reversed',
    'gear on the right side of the body for the facing: a right-facing figure shows its right side, so left-hip gear sits on the far side',
    'the same number of weapons: a drawn blade leaves an empty scabbard, not a second hilt',
    'weapons whole: full length from hilt to tip, both ends, nothing drawn out of thin air',
    'the first frame holds the weapon like the idle does (sheathed in idle -> the move starts sheathed and draws)',
    'a sheathed weapon reads as one piece: the hilt and the scabbard end on one straight line through the hip',
    'nothing cut by the canvas edge (feet, blade tips, capes)',
    'a two-handed weapon keeps both hands on the hilt in every pose; a shield or buckler stays on its arm (not dropped, not doubled)',
    'a hand holding a staff or prop stays joined to the body by its arm: no gap of background between the grip and the body, the arm its normal length',
    'a bow keeps its string in every frame, and the arrow nock (feathered end) sits in the drawing hand on the string',
    'the move goes one way: a step done in one key pose is not undone in the next (a bow drawn overhead, then slack and drawn again)',
    'no in-between shows a pose that is in neither key pose (a blade raised overhead in a thrust or a draw-cut): drop it or re-roll the clip with motion wording that rules it out',
    'a staff, wand or other held prop stays in the same hand and on the same side of the body in every frame (it does not swap hands or drift to the body centre line)',
    'a thrown or cast projectile leaves the hand at the release frame and is not drawn again in the hand afterwards',
    'the same face and skin tone (no pale-to-warm flicker between frames, no single frame with the head turned away or toward the viewer), hair, headgear and outfit piece by piece (shoulder plates, sleeves, chest plate, ornaments), at the same body size',
]


def build(results) -> dict:
    """results: one dict per Anim with key, kind, kind_guessed, ref_guessed, scale, verdict, skipped,
    findings_before/after (Finding), changes (Change), plans (dict)."""
    anims = []
    for r in results:
        nm = r['names']
        changes = [change(c, nm) for c in r['changes']]
        plans = [_number(dict(p), nm) for p in r['plans']]
        anims.append({'key': r['key'], 'kind': r['kind'], 'kind_guessed': r['kind_guessed'], 'ref_guessed': r['ref_guessed'],
                      'scale': r['scale'], 'analysis_background_keyed': r.get('analysis_background_keyed', False), 'verdict': r['verdict'], 'skipped': r['skipped'],
                      'durations': r.get('durations'),
                      'findings_before': [finding(f, nm) for f in r['findings_before']],
                      'changes': [c for c in changes if c['result'] != 'proposed'],
                      'findings_after': [finding(f, nm) for f in r['findings_after']],
                      'proposals': [c for c in changes if c['result'] == 'proposed'],
                      'plans': plans})
    verdict = max((a['verdict'] for a in anims), key=ORDER.get, default='ready')
    return {'version': 1, 'verdict': verdict, 'anims': anims, 'look': LOOK,
            'totals': {'changes': sum(len(a['changes']) for a in anims), 'proposals': sum(len(a['proposals']) for a in anims),
                       'plans': sum(len(a['plans']) for a in anims), 'plan_cost': sum(p['cost'] for a in anims for p in a['plans'] if p['cost'] is not None),
                       'unquoted_plans': sum(p['cost'] is None for a in anims for p in a['plans'])}}


def text(rep) -> str:
    q = rep['totals']['proposals']
    lines = ['Verdict: %s%s' % (rep['verdict'], ' - %d question%s waiting (the "ask" lines)' % (q, '' if q == 1 else 's') if q else ''), '']
    for a in rep['anims']:
        lines.append('%s - %s' % (a['key'], a['verdict']))
        if a.get('analysis_background_keyed'):
            lines.append('  analysis only: border background keyed for measurements/inspection; exported source backgrounds preserved')
        guessed = [w for w, g in (('move kind (%s)' % a['kind'], a['kind_guessed']), ('reference (most typical frame)', a['ref_guessed'])) if g]
        if guessed:
            lines.append('  guessed: ' + ', '.join(guessed))
        for c in a['changes'][:8]:
            lines.append('  changed: %s - %s' % (c['action'], c['result']))
        if len(a['changes']) > 8:
            lines.append('  ... and %d more changes' % (len(a['changes']) - 8))
        for p in a['proposals']:
            lines.append('  ask (%s): %s?' % (p['id'], p['action']))
        for p in a['plans'][:6]:
            lines.append('  re-roll frames %s (%s): %s - %s, ~%s gen (estimate; schema check required)' % (p['frames'], p['check'], p['tool'], p['prompt_change'], str(p['cost']) if p['cost'] is not None else 'unknown'))
        for s in a['skipped']:
            lines.append('  skipped: ' + s)
        lines.append('')
    target = 'the original inputs and reference' if rep.get('check_only') else 'fix_sheet.png (reference first)'
    lines.append('Look at %s before calling it ready - pixels miss these:' % target)
    lines.extend('  - ' + q for q in rep.get('look', LOOK))
    lines.append('')
    t = rep['totals']
    n = lambda k, word: '%d %s%s' % (k, word, '' if k == 1 else 's')
    lines.append('%s, %s, %s (%s)' % (n(t['changes'], 'change'), n(t['proposals'], 'question'), n(t['plans'], 're-roll plan'),
                                      n(t['plan_cost'], 'estimated generation')) + ('; %d plans need re-quoting' % t['unquoted_plans'] if t['unquoted_plans'] else ''))
    return '\n'.join(lines) + '\n'


def sheet(path, rows):
    """rows: [(input frames, fixed frames, flagged indices, reference)] per animation. The reference comes first in
    the top row, so the look checklist (LOOK) compares every frame with it."""
    if not rows:
        return
    h = max(f.shape[0] for r in rows for f in list(r[0]) + [r[3]])
    w = max(f.shape[1] for r in rows for f in list(r[0]) + [r[3]])
    z = 2 if max(h, w) <= 128 else 1
    cols = max(len(r[0]) for r in rows) + 1
    pad = 4
    img = Image.new('RGBA', (cols * (w * z + pad) + pad, len(rows) * 2 * (h * z + pad) + pad), BG)
    d = ImageDraw.Draw(img)
    for r, (before, after, flagged, ref) in enumerate(rows):
        for row, frames in enumerate((before, after)):
            y = pad + (2 * r + row) * (h * z + pad)
            if row == 0:
                img.alpha_composite(Image.fromarray(ref, 'RGBA').resize((ref.shape[1] * z, ref.shape[0] * z), Image.NEAREST), (pad, y))
            for i, f in enumerate(frames):
                i += 1
                x = pad + i * (w * z + pad)
                im = Image.fromarray(f, 'RGBA').resize((f.shape[1] * z, f.shape[0] * z), Image.NEAREST)
                img.alpha_composite(im, (x, y))
                if row == 0 and i - 1 in flagged:
                    d.rectangle([x - 2, y - 2, x + w * z + 1, y + h * z + 1], outline=FLAG, width=2)
    img.save(path)


def gif(path, frames, durations):
    # Zero slots arise only from accepted timing drops. Their files remain in the derivative set.
    from _gif import write_gif
    keep = [(f, d) for f, d in zip(frames, durations) if d != 0]
    if not keep:
        raise ValueError("preview has no positive-duration frames")
    return write_gif(path, [Image.fromarray(f, 'RGBA') for f, _ in keep], [d for _, d in keep])


def write_json(path, rep):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(rep, fh, indent=1, ensure_ascii=False, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else str(o))
