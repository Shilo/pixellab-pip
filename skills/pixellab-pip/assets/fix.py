"""Heuristic animation inspection, optional local repairs and advisory re-roll plans.

Without --check-only, writes repair copies; originals remain untouched.
Findings require visual review and do not certify art quality.

  python fix.py out/knight_attack_*.png                 # one animation (files, a folder, a sheet or a GIF)
  python fix.py out/                                    # a batch: every character x move in the folder
  python fix.py sheet.png --sheet 96x200 --move attack  # a sprite sheet of 96x200 frames
  python fix.py frames/ --ref hero.png                  # compare against this standing sprite
  python fix.py frames/ --accept c2,c5                  # also apply these proposed effect fixes (asked first)
  python fix.py frames/ --check-only --json             # measure and plan only; report to stdout
  python fix.py --table  # defect -> cause -> change guidance; with inputs, also inspects them

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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _assembly  # noqa: E402,F401  (UTF-8-safe console)
_assembly.require_numpy(scipy=True)
from fixlib import frames as framesmod, measure, plan, repair, report, timing  # noqa: E402

SOFT_WORDS = ('soft edge', 'soft anti', 'anti-alias', 'antialias', 'painterly', 'smooth edges', 'no outline / soft edges')


def load_style(path):
    """Style facts the checks use, from a pixellab.json profile: top-level fields overlaid by the active style."""
    if not path:
        return None
    if not os.path.isfile(path):
        raise ValueError("no profile at the selected path: " + path)
    from project_style import load, validate_profile, overlay
    prof = load(path)
    styles = validate_profile(prof)
    st = overlay(prof, styles.get(prof.get('active_style'), {}))
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
    reroll_findings = open_after
    if keys:   # key poses the user already approved: findings stay in the report, no paid re-roll is planned
        kept = {i for i, o in enumerate(order) if o in keys}
        reroll_findings = [dataclasses.replace(f, frames=[i for i in f.frames if i not in kept]) for f in open_after]
        reroll_findings = [f for f in reroll_findings if f.frames]
        skipped = skipped + ['key poses %s: approved already, so no re-roll is planned - findings on them are listed; '
                             'look at them at 3x' % ', '.join(str(i + 1) for i in sorted(keys))]
    plans = plan.make(fixed, reroll_findings, log_path, report_name, allow_whole_clip=not (keys or fx))
    return fixed, {'key': anim.key, 'kind': anim.kind, 'kind_guessed': anim.kind_guessed, 'ref_guessed': anim.ref_guessed,
                   'scale': anim.scale, 'analysis_background_keyed': any(c is not None for c in anim.backgrounds), 'verdict': plan.verdict(before, open_after, changes), 'skipped': skipped,
                   'findings_before': before, 'findings_after': after, 'changes': changes, 'plans': plans,
                   'durations': durations, 'order': order, 'names': framesmod.names(anim)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('inputs', nargs='*')
    ap.add_argument('--sheet', help='frame size WxH when the input is a sprite sheet')
    ap.add_argument('--ref', help='the standing sprite to compare against (default: the most typical frame)')
    ap.add_argument('--move', help='idle|walk|run|attack|skill|cast|hurt|death (default: from the file names)')
    ap.add_argument('--out')
    ap.add_argument('--profile', help='selected project pixellab.json; no implicit cwd profile')
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
    try:
        sheet = tuple(int(v) for v in args.sheet.lower().split('x')) if args.sheet is not None else None
    except ValueError:
        ap.error('--sheet needs positive WxH')
    if sheet and (len(sheet) != 2 or min(sheet) <= 0):
        ap.error('--sheet needs positive WxH')
    try:
        anims = framesmod.load(args.inputs, sheet=sheet, ref=args.ref, move=args.move)
    except ValueError as exc:
        ap.error(str(exc))
    if args.accept and (len(anims) != 1 or args.check_only):
        ap.error('--accept requires one animation and cannot be combined with --check-only; rerun that animation alone')
    if not anims:
        sys.exit('no frames found in %s' % ' '.join(args.inputs))
    indexes = {}
    for flag, value in (('--fx', args.fx), ('--keys', args.keys)):
        try:
            indexes[flag] = {int(v.strip()) - 1 for v in value.split(',')} if value else set()
        except ValueError:
            ap.error('%s needs comma-separated positive frame numbers' % flag)
        if any(i < 0 or any(i >= len(a.frames) for a in anims) for i in indexes[flag]):
            ap.error('%s frame numbers must exist in every selected animation' % flag)
    if not args.check_only and any(a.durations and any(d <= 0 for d in a.durations) for a in anims):
        ap.error('GIF contains zero-delay frames; use --check-only to inspect it. '
                 'Choose positive preview timing explicitly via local-asset-assembly.md before repair; '
                 'source timing is unchanged')
    style = load_style(args.profile)
    out = _out_dir(args, anims)
    report_path = os.path.join(out, 'fix_report.json')
    protected = [p for a in anims for p in a.paths + ([a.source] if a.source else [])] + ([args.ref] if args.ref else [])
    destinations = [report_path, os.path.join(out, 'fix_report.txt')]
    if not args.check_only:
        destinations += [os.path.join(out, 'timing.json'), os.path.join(out, 'fix_sheet.png')]
        for a in anims:
            destinations += [os.path.join(out, a.subdir, n) for n in framesmod.names(a)]
            destinations.append(os.path.join(out, '%s_preview.gif' % re.sub(r'\W+', '_', a.key).strip('_')))
    try:
        _assembly.preflight_outputs(destinations, protected)
    except ValueError as exc:
        ap.error(str(exc))
    os.makedirs(out, exist_ok=True)
    accept = {a.strip() for a in args.accept.split(',') if a.strip()}
    results, rows, timings = [], [], {}
    for anim in anims:
        near = [os.path.join(os.path.dirname(os.path.abspath(p)), d, 'manifest.json') for p in (anim.paths[:1] or [anim.source]) for d in ('.', '..', '../..')]
        log = next((p for p in near if os.path.exists(p)), None)   # the run's manifest, beside or above the frames
        fixed, res = doctor(anim, accept, style, log, report_path, args.check_only, args.stepped,
                            indexes['--fx'], indexes['--keys'])
        results.append(res)
        if args.check_only:
            continue
        changed = {i for i in range(len(anim.frames)) if res['order'][i] != i or not (fixed.frames[i] == anim.frames[i]).all()}
        framesmod.write(fixed, out, changed)
        timings[anim.key] = {'order': res['order'], 'durations': res['durations']}
        flagged = {i for f in res['findings_before'] if f.severity != 'low' for i in f.frames}
        rows.append((anim.frames, fixed.frames, flagged, anim.ref))
        report.gif(os.path.join(out, '%s_preview.gif' % re.sub(r'\W+', '_', anim.key).strip('_')), framesmod._canvas([framesmod.output_pixels(fixed, i, changed) for i in range(len(fixed.frames))])[0], res['durations'])
    rep = report.build(results)
    rep['check_only'] = args.check_only
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
