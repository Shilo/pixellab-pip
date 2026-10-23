"""Timing repairs for /pga-fix: drop a frame that still fails (it becomes a copy of the frame before, which is held
longer), and the batch audit's hurt orders. The frame count and names never change, so the fixed frames still drop
into an engine that loads a fixed number of them; durations and order are reported for engines that can use them."""
import copy

import numpy as np

from fixlib import measure
from fixlib.model import Change
from fixlib.thresholds import T

DROPPABLE = {'weird_change', 'weapon_lost', 'jump'}   # body defects only: a flash is an effect, so it's asked about
HURT_ORDERS = {0: [2, 4, 4, 3, 1], 2: [3, 4, 4, 3, 0], 3: [4, 4, 4, 4, 0]}   # by how many early frames are dirty


def _hurt_dirty(anim) -> int:
    """How many of a 5-frame hurt's frames 1-3 are dirty in a row from frame 1 (painted burst or darkened body):
    more than T['hurt_mass'] extra mass or T['hurt_light'] lightness change against frames 0 and 4."""
    fr = [measure.Frame(f) for f in anim.frames]
    def stats(f):
        px = f.a[f.on][:, :3]
        return float(f.on.sum()), float(measure.luma(px).mean()) if len(px) else 0.0
    m0, l0 = np.mean([stats(fr[0])[0], stats(fr[4])[0]]), np.mean([stats(fr[0])[1], stats(fr[4])[1]])
    n = 0
    for i in (1, 2, 3):
        m, l = stats(fr[i])
        if m > m0 * (1 + T['hurt_mass']) or abs(l / max(l0, 1) - 1) > T['hurt_light']:
            n += 1
        else:
            break
    return n


def run(anim, findings, start=0, accept=frozenset()):
    b = copy.copy(anim)
    b.frames = list(anim.frames)
    n = len(b.frames)
    durations = list(anim.durations) if anim.durations and len(anim.durations) == n else [100] * n
    order = list(range(n))
    changes = []

    def new(frames, action, result):
        changes.append(Change('c%d' % (start + len(changes) + 1), 'timing', frames, action, result))

    if anim.move == 'hurt' and n == 5:
        dirty = _hurt_dirty(anim)
        if dirty >= 2:
            want = HURT_ORDERS[min(dirty, 3)]
            body = any(f.severity in ('mid', 'high') and f.region != 'effect' and set(f.frames) & {1, 2, 3} for f in findings)
            action = 'reorder hurt frames to %s (frames 2-%d are dirty)' % ([j + 1 for j in want], dirty + 1)   # counted from 1, like the files
            if body:          # a body defect on the early frames: the audit's reorder is a free fix
                result = 'fixed'
            else:             # only an effect (a painted burst): reordering removes it, so it's asked first
                new([1, 2, 3][:dirty], action, 'proposed')
                if changes[-1].id not in accept:
                    return b, changes, durations, order
                changes.pop()
                result = 'fixed'
            order = want
            b.frames = [anim.frames[j] for j in order]
            changes.append(Change('c%d' % (start + len(changes) + 1), 'timing', [1, 2, 3][:dirty], action.replace('reorder ', 'reordered ', 1), result))
            return b, changes, durations, order
    bad = sorted({i for f in findings if f.check in DROPPABLE and f.severity == 'high' for i in f.frames})
    budget = n // 3
    clean = [i not in bad for i in range(n)]
    for i in bad:
        blocked = anim.kind == 'oneshot' and i in (0, n - 1)
        if blocked or i == 0 or not clean[i - 1] or budget == 0:
            changes.append(Change('c%d' % (start + len(changes) + 1), 'timing', [i],
                                  'frame %d still fails and could not be dropped (%s)' % (
                                      i + 1, 'first/last frame of the move' if blocked or i == 0 else
                                      'the frame before it is bad too' if not clean[i - 1] else 'already dropped a third'),
                                  'still failing'))
            continue
        clean[i] = True
        budget -= 1
        # a drop repeats a frame, and Pip keeps the frames PixelLab returned: proposed, done only when accepted
        new([i], 'drop frame %d, hold frame %d' % (i + 1, i), 'proposed')
        if changes[-1].id not in accept:
            continue
        b.frames[i] = b.frames[i - 1]
        order[i] = order[i - 1]
        durations[i - 1] += durations[i]
        durations[i] = 0
        changes[-1] = Change(changes[-1].id, 'timing', [i], 'dropped frame %d, held frame %d' % (i + 1, i), 'fixed')
    return b, changes, durations, order
