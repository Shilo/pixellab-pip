"""Timing repairs for the animation doctor: drop a frame that still fails (it becomes a copy of the frame before, which is held
longer), when explicitly accepted. The frame count and names never change, so the fixed frames still drop
into an engine that loads a fixed number of them; durations and order are reported for engines that can use them."""
import copy

from fixlib.model import Change

DROPPABLE = {'weird_change', 'weapon_lost', 'jump'}   # body defects only: a flash is an effect, so it's asked about

def run(anim, findings, start=0, accept=frozenset()):
    b = copy.copy(anim)
    b.frames = list(anim.frames)
    b.backgrounds = list(anim.backgrounds)
    b.originals = list(anim.originals)
    n = len(b.frames)
    durations = list(anim.durations) if anim.durations and len(anim.durations) == n else [100] * n
    order = list(range(n))
    changes = []

    def new(frames, action, result):
        changes.append(Change('c%d' % (start + frames[0] + 1), 'timing', frames, action, result))

    bad = sorted({i for f in findings if f.check in DROPPABLE and f.severity == 'high' for i in f.frames})
    budget = n // 3
    clean = [i not in bad for i in range(n)]
    for i in bad:
        geometry_differs = i > 0 and (anim.sizes[i] != anim.sizes[i - 1] or anim.offsets[i] != anim.offsets[i - 1])
        blocked = (anim.kind == 'oneshot' and i in (0, n - 1)) or geometry_differs
        if blocked or i == 0 or not clean[i - 1] or budget == 0:
            new([i], 'frame %d still fails and could not be dropped (%s)' % (
                    i + 1, 'different frame geometry' if geometry_differs else 'first/last frame of the move' if blocked or i == 0 else
                    'the frame before it is bad too' if not clean[i - 1] else 'already dropped a third'), 'still failing')
            continue
        clean[i] = True
        budget -= 1
        # a drop repeats a frame, and Pip keeps the frames PixelLab returned: proposed, done only when accepted
        new([i], 'drop frame %d, hold frame %d' % (i + 1, i), 'proposed')
        if changes[-1].id not in accept:
            continue
        b.frames[i] = b.frames[i - 1]
        order[i] = order[i - 1]
        if b.backgrounds:
            b.backgrounds[i] = b.backgrounds[i - 1]
        if b.originals:
            b.originals[i] = b.originals[i - 1]
        durations[i - 1] += durations[i]
        durations[i] = 0
        changes[-1] = Change(changes[-1].id, 'timing', [i], 'dropped frame %d, held frame %d' % (i + 1, i), 'fixed')
    return b, changes, durations, order
