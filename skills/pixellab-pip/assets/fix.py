"""fix.py - the /pga-fix animation doctor. Measures frames against "game ready" (smooth motion, clean transitions,
colour match, no dots or gaps, no artifacts between frames, no weird changes, crisp pixels at one scale), fixes for free
what it can from pixels the set already has, and writes a report with exact re-roll plans for the rest. Free: no
generations, no GPU. Originals are never written; same frame count and names out as in.

  python fix.py out/knight_attack_*.png                 # one animation (files, a folder, a sheet or a GIF)
  python fix.py out/                                    # a batch: every character x move in the folder
  python fix.py sheet.png --sheet 96x200 --move attack  # a sprite sheet of 96x200 frames
  python fix.py frames/ --ref hero.png                  # compare against this standing sprite
  python fix.py frames/ --accept c2,c5                  # also apply these proposed effect fixes (asked first)
  python fix.py frames/ --check-only --json             # measure and plan only; report to stdout
  python fix.py --table                                 # the defect -> cause -> change table (references/animation-doctor.md);
                                                        # with frames it prints the table, then checks them as usual

Writes into <first input folder>_fixed/ (or --out): the fixed frames, timing.json, fix_report.json, fix_report.txt,
fix_sheet.png and <character>_<move>_preview.gif (frames in subfolders keep their subfolder). Effects (slashes, glows) and frame drops are never changed without --accept. Every fixed frame is a local derivative
of PixelLab's output, reported as such.
Needs Pillow, numpy, scipy.
"""
import argparse
import dataclasses
import json
import os
import re
import sys
for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:   # optional helper: without numpy/scipy it skips, as Pip's helpers do
    import numpy  # noqa: F401
    import scipy  # noqa: F401
except ImportError as exc:
    print(json.dumps({'status': 'skipped', 'reason': 'the animation doctor needs numpy and scipy (%s)' % exc}))
    sys.exit(3)
from fixlib import frames as framesmod, measure, plan, repair, report, timing  # noqa: E402

SOFT_WORDS = ('soft edge', 'soft anti', 'anti-alias', 'antialias', 'painterly', 'smooth edges', 'no outline / soft edges')


def load_style(path):
    """Style facts the checks use, from a pixellab.json profile: top-level fields overlaid by the active style."""
    if not path or not os.path.exists(path):
        return None
    try:
        prof = json.load(open(path, encoding='utf-8-sig'))
    except ValueError:
        return None
    st = dict(prof)
    st.update(prof.get('styles', {}).get(prof.get('active_style', ''), {}))
    words = ' '.join(str(st.get(k, '')) for k in ('look', 'outline', 'style')).lower()
    return {'soft_edges': bool(st.get('soft_edges')) or any(w in words for w in SOFT_WORDS),
            'scale': st.get('scale'), 'palette_size': st.get('palette_size')}


def _out_dir(args, anims):
    if args.out:
        return args.out
    first = args.inputs[0].rstrip('/\\')
    folder = first if os.path.isdir(first) else os.path.dirname(os.path.abspath(first.replace('*', 'x')))
    return folder.rstrip('/\\') + '_fixed'


STEPPED_SKIP = ('jump', 'missing_inbetween', 'loop_seam', 'size_pop', 'weird_change', 'weapon_lost', 'broken_thin', 'ground')


def _measure(anim, style, stepped, fx=()):
    """measure.run; with stepped (key poses on purpose, no in-betweens) the motion checks are dropped: they read the
    deliberate steps as jumps, vanished weapons and airborne frames as defects. fx: 0-based frames with an effect
    baked in on purpose (a smoke vanish) - nothing is judged, fixed or re-rolled on them."""
    found, skipped = measure.run(anim, style)
    if stepped:
        found = [f for f in found if f.check not in STEPPED_SKIP]
        skipped = skipped + ['stepped: motion, weapon and ground checks off (key poses on purpose); timing kept as given']
    if fx:
        found = [dataclasses.replace(f, frames=[i for i in f.frames if i not in fx]) for f in found]
        found = [f for f in found if f.frames]
        skipped = skipped + ['effect frames %s: not judged (effects baked in on purpose) - look at them yourself'
                             % ', '.join(str(i + 1) for i in sorted(fx))]
    return found, skipped


def doctor(anim, accept, style, log_path, report_name, check_only, stepped=False, fx=(), keys=()):
    before, skipped = _measure(anim, style, stepped, fx)
    if check_only or stepped:
        n = len(anim.frames)
        durations = list(anim.durations) if anim.durations and len(anim.durations) == n else [100] * n
        fixed, changes, order = anim, [], list(range(n))
        if stepped and not check_only:
            fixed, changes = repair.run(anim, before, accept, style)
    else:
        fixed, changes = repair.run(anim, before, accept, style)
        mid, _ = _measure(fixed, style, stepped, fx)   # an effect frame is never offered as a drop
        fixed, tchanges, durations, order = timing.run(fixed, mid, start=len(changes), accept=accept)
        changes += tchanges
    after, _ = _measure(fixed, style, stepped, fx) if not check_only else (before, None)
    still = {(f.check, tuple(f.frames)) for f in after}
    for c in changes:
        if c.result == 'fixed' and c.check != 'timing' and any((c.check, (i,)) in still for i in c.frames):
            c.result = 'still failing'
    # a finding with a question waiting gets no re-roll plan and doesn't hold the verdict: one "yes" fixes it for free
    pending = {(c.check, i) for c in changes if c.result == 'proposed' for i in c.frames}
    open_after = [f for f in after if not any((f.check, i) in pending for i in f.frames)]
    plans = plan.make(fixed, open_after, log_path, report_name)
    if keys:   # key poses the user already approved: findings stay in the report, no paid re-roll is planned
        kept = {i for i, o in enumerate(order) if o in keys}
        plans = [p for p in plans if not set(p['frames']) <= kept]
        skipped = skipped + ['key poses %s: approved already, so no re-roll is planned - findings on them are listed; '
                             'look at them at 3x' % ', '.join(str(i + 1) for i in sorted(keys))]
    return fixed, {'key': anim.key, 'kind': anim.kind, 'kind_guessed': anim.kind_guessed, 'ref_guessed': anim.ref_guessed,
                   'scale': anim.scale, 'verdict': plan.verdict(before, open_after, changes), 'skipped': skipped,
                   'findings_before': before, 'findings_after': after, 'changes': changes, 'plans': plans,
                   'durations': durations, 'order': order, 'names': framesmod.names(anim)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('inputs', nargs='*')
    ap.add_argument('--sheet', help='frame size WxH when the input is a sprite sheet')
    ap.add_argument('--ref', help='the standing sprite to compare against (default: the most typical frame)')
    ap.add_argument('--move', help='idle|walk|run|attack|skill|cast|hurt|death (default: from the file names)')
    ap.add_argument('--out')
    ap.add_argument('--accept', default='', help='proposal ids to apply, e.g. c2,c5')
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--stepped', action='store_true',
                    help='key poses on purpose, no in-betweens: skip motion/weapon/ground checks, never drop or reorder')
    ap.add_argument('--fx', default='', help='frames (1-based, e.g. 3,4,5) with an effect baked in on purpose: not judged')
    ap.add_argument('--keys', default='', help='frames (1-based) that are key poses you approved: no re-roll is planned for them')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--table', action='store_true')
    args = ap.parse_args(argv)
    if args.table:
        print(plan.table())
        if not args.inputs:
            return
    if not args.inputs:
        ap.error('give frames, a folder, a sheet or a GIF')
    sheet = tuple(int(v) for v in args.sheet.lower().split('x')) if args.sheet else None
    anims = framesmod.load(args.inputs, sheet=sheet, ref=args.ref, move=args.move)
    if not anims:
        sys.exit('no frames found in %s' % ' '.join(args.inputs))
    style = load_style('pixellab.json' if os.path.exists('pixellab.json') else None)   # the project style, when present
    out = _out_dir(args, anims)
    outa = os.path.normcase(os.path.abspath(out))
    for a in anims:   # raw PixelLab frames are never written: the output folder may not hold any input
        for p in a.paths:
            if os.path.normcase(os.path.abspath(p)).startswith(outa + os.sep):
                ap.error('--out %s holds the input frames; choose a new folder (raw frames are never written)' % out)
    os.makedirs(out, exist_ok=True)
    report_path = os.path.join(out, 'fix_report.json')
    accept = {a.strip() for a in args.accept.split(',') if a.strip()}
    results, rows, timings = [], [], {}
    for anim in anims:
        near = [os.path.join(os.path.dirname(os.path.abspath(p)), d, 'manifest.json') for p in anim.paths[:1] for d in ('.', '..', '../..')]
        log = next((p for p in near if os.path.exists(p)), None)   # the run's manifest, beside or above the frames
        fixed, res = doctor(anim, accept, style, log, report_path, args.check_only, args.stepped,
                            {int(v) - 1 for v in args.fx.split(',') if v.strip()},
                            {int(v) - 1 for v in args.keys.split(',') if v.strip()})
        results.append(res)
        if args.check_only:
            continue
        changed = {i for i in range(len(anim.frames)) if not (fixed.frames[i] == anim.frames[i]).all()}
        framesmod.write(fixed, out, changed)
        timings[anim.key] = {'order': res['order'], 'durations': res['durations']}
        flagged = {i for f in res['findings_before'] if f.severity != 'low' for i in f.frames}
        rows.append((anim.frames, fixed.frames, flagged, anim.ref))
        report.gif(os.path.join(out, '%s_preview.gif' % re.sub(r'\W+', '_', anim.key).strip('_')), fixed.frames, res['durations'])
    rep = report.build(results)
    report.write_json(report_path, rep)
    with open(os.path.join(out, 'fix_report.txt'), 'w', encoding='utf-8') as fh:
        fh.write(report.text(rep))
    if not args.check_only:
        with open(os.path.join(out, 'timing.json'), 'w', encoding='utf-8') as fh:
            json.dump({'note': 'order = the input frame each output frame shows; a 0 ms frame is a dropped one kept as a copy',
                       **timings}, fh, indent=1)
        report.sheet(os.path.join(out, 'fix_sheet.png'), rows)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1, default=str))
    else:
        print(report.text(rep), end='')
        print('-> %s' % out)


if __name__ == '__main__':
    main()
