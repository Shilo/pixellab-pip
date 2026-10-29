"""The animation doctor's free repairs: only pixels the set already has (the reference's colours, the character's own clean
frames). Body only: effect pixels and soft effect edges are proposals, applied when their change id is accepted.
run() returns a repaired copy and one Change per finding it acted on (result "fixed" provisionally; the caller
re-measures and corrects it), in finding order, so ids are stable between runs."""
import copy

import numpy as np
from scipy import ndimage

from fixlib import measure
from fixlib.colour import group_of
from fixlib.model import Change
from fixlib.thresholds import T

COLOUR = ('brightness', 'palette', 'colour_count')
def snap(px: np.ndarray, ref_cols: np.ndarray) -> np.ndarray:
    """Each colour to the nearest reference colour of its own group (any group when the reference has none)."""
    if not len(px):
        return px
    cols, inv = np.unique(px, axis=0, return_inverse=True)
    d = ((measure.oklab(cols)[:, None] - measure.oklab(ref_cols)[None]) ** 2).sum(-1)
    g, rg = group_of(cols), group_of(ref_cols)
    d = d + 1e3 * ((g[:, None] != rg[None]) & np.isin(g, rg)[:, None])
    return ref_cols[d.argmin(1)][inv.ravel()]


def _shift(a, dx, dy):
    g = np.zeros_like(a)
    h, w = a.shape[:2]
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    g[yd, xd] = a[ys, xs]
    return g


def _fill_from_neighbours(a: np.ndarray, holes: np.ndarray) -> None:
    """Each hole pixel takes the most common opaque colour around it (repeated inward for bigger holes)."""
    todo = holes.copy()
    for _ in range(6):
        if not todo.any():
            return
        done = []
        for y, x in zip(*np.nonzero(todo)):
            nb = a[max(0, y - 1):y + 2, max(0, x - 1):x + 2].reshape(-1, 4)
            ok = ~todo[max(0, y - 1):y + 2, max(0, x - 1):x + 2].reshape(-1) & (nb[:, 3] >= 128)
            if ok.any():
                cols, n = np.unique(nb[ok], axis=0, return_counts=True)
                done.append((y, x, cols[n.argmax()]))
        for y, x, c in done:
            a[y, x] = c
            todo[y, x] = False


def _vote(a: np.ndarray, k: int, phase: tuple) -> np.ndarray:
    """Back onto the k px grid: each k x k block takes its most common colour (not the average)."""
    out = a.copy()
    py, px = phase
    h, w = a.shape[:2]
    for y in range(py - k if py else 0, h, k):
        for x in range(px - k if px else 0, w, k):
            y0, x0 = max(0, y), max(0, x)
            blk = a[y0:y + k, x0:x + k].reshape(-1, 4)
            if not len(blk) or not (blk[:, 3] > 0).any():
                continue
            cols, n = np.unique(blk, axis=0, return_counts=True)
            out[y0:y + k, x0:x + k] = cols[n.argmax()]
    return out


def _phase(a: np.ndarray, k: int) -> tuple:
    on = a[..., 3] > 0
    ys, xs = np.nonzero(on)
    if not len(ys):
        return (0, 0)
    best, bp = 2.0, (0, 0)
    for py in range(k):
        for px in range(k):
            share = measure._nonuniform_share(np.pad(a, ((py, 0), (px, 0), (0, 0)))[:a.shape[0] + py, :a.shape[1] + px], k)
            if share < best:
                best, bp = share, ((k - py) % k, (k - px) % k)
    return bp


def _rescale(a: np.ndarray, factor: float) -> np.ndarray:
    """Whole-factor rescale about the feet (bottom centre)."""
    from PIL import Image
    h, w = a.shape[:2]
    im = Image.fromarray(a, 'RGBA')
    nw, nh = max(1, round(w * factor)), max(1, round(h * factor))
    if factor < 1:
        k = round(1 / factor)
        b = _vote(a, k, (0, 0))[::k, ::k]
    else:
        b = np.array(im.resize((nw, nh), Image.NEAREST))
    out = np.zeros_like(a)
    ys, xs = np.nonzero(a[..., 3] > 0)
    feet, cx = ys.max(), int(xs.mean())
    bys, bxs = np.nonzero(b[..., 3] > 0)
    dy, dx = feet - bys.max(), cx - int(bxs.mean())
    for y, x in zip(bys, bxs):
        if 0 <= y + dy < h and 0 <= x + dx < w:
            out[y + dy, x + dx] = b[y, x]
    return out


def _soft_regions(a, main):
    soft = (a[..., 3] > 0) & (a[..., 3] < 255)
    if not soft.any():
        return soft, soft.copy()
    if main is None:
        main = measure.Frame(a).main
    body = ndimage.binary_dilation(main, measure.EIGHT, iterations=1) & soft
    return body, soft & ~body


def run(anim, findings, accept=frozenset(), style=None):
    b = copy.copy(anim)
    b.frames = [f.copy() for f in anim.frames]
    ref_cols = np.unique(anim.ref[anim.ref[..., 3] >= 128][:, :3], axis=0)
    ref_luma = measure.luma(anim.ref[anim.ref[..., 3] >= 128][:, :3]).mean()
    rl = measure.ref_loose(anim)
    k = measure.set_scale(anim)[1] if findings and {f.check for f in findings} & {'grid', 'mixels'} else max(1, anim.scale)
    by_frame = {}
    for f in findings:
        for i in f.frames:
            by_frame.setdefault(i, set()).add(f.check)
    weapon = {i for i, cs in by_frame.items() if cs & {'weapon_lost', 'broken_thin'}}
    changes, colour_done, n = [], {}, 0
    phase = None
    effect_frames = {i for f in findings if f.region == 'effect' for i in f.frames}
    whole_frame_risk = {}
    original_soft = {}

    def new(check, frames, action, result='fixed'):
        nonlocal n
        n += 1
        c = Change('c%d' % n, check, frames, action, result)
        changes.append(c)
        return c

    def whole_frame(check, i, candidate, action):
        c = new(check, [i], action)
        if i not in whole_frame_risk:
            whole_frame_risk[i] = i in effect_frames
            if not whole_frame_risk[i]:
                original = anim.frames[i]
                frame = measure.Frame(original)
                original_soft[i] = body_soft, effect_soft = _soft_regions(original, frame.main)
                # Reuse the doctor's candidates, including uncertain detached parts;
                # classify the original, not pixels changed by an earlier repair.
                whole_frame_risk[i] = bool((frame.on & ~frame.main).any() or effect_soft.any()
                    or (frame.on & ~measure.body_mask(anim, i) & ~body_soft).any())
        if whole_frame_risk[i] and not np.array_equal(candidate, b.frames[i]):
            c.action += '; whole-frame change may also alter effects'
            c.result = 'proposed'
        if c.result != 'proposed' or c.id in accept:
            b.frames[i] = candidate
            c.result = 'fixed'

    for f in findings:
        i = f.frames[0]
        a = b.frames[i]
        if f.check in ('grid', 'mixels'):
            if phase is None:
                good = next((j for j in range(len(b.frames)) if not by_frame.get(j, set()) & {'grid', 'mixels'}), i)
                phase = _phase(anim.frames[good], k) if k > 1 else (0, 0)
            if k > 1:
                whole_frame(f.check, i, _vote(a, k, phase),
                            'put frame %d back on the %d px grid (most common colour per block)' % (i + 1, k))
        elif f.check == 'size':
            r = f.measured
            factor = 1 / round(r) if r > 1 else round(1 / r)
            if round(r if r > 1 else 1 / r) >= 2 and T['size_lo'] <= r * factor <= T['size_hi']:
                whole_frame('size', i, _rescale(a, factor),
                            'rescaled frame %d by a whole factor (x%s)' % (i + 1, factor if factor >= 1 else '1/%d' % round(1 / factor)))
            else:
                new('size', [i], 'frame %d is %d%% off size; no whole-factor rescale fits' % (i + 1, round(abs(r - 1) * 100)), 'still failing')
        elif f.check == 'soft_edge':
            body, rest = _soft_regions(a, None)
            if np.array_equal(a[..., 3], anim.frames[i][..., 3]):
                original_body, original_rest = body, rest
            else:
                if i not in original_soft:
                    original_soft[i] = _soft_regions(anim.frames[i], None)
                original_body, original_rest = original_soft[i]
            # Keep the original action slots even when an accepted whole-frame
            # change already resolved a soft region, so later --accept IDs stay put.
            if not original_body.any():
                rest |= body
                body = np.zeros_like(body)
            elif not original_rest.any():
                body |= rest
                rest = np.zeros_like(rest)
            if original_body.any():   # the character's own soft outline: hardened (free)
                a[body, 3] = np.where(a[body, 3] >= 128, 255, 0)
                new('soft_edge', [i], ('hard edges on the character in frame %d (no half-transparent pixels)'
                                     if body.any() else 'body soft edges in frame %d already resolved') % (i + 1))
            if original_rest.any():   # soft pixels away from the body are an effect (a glow): asked first
                c = new('soft_edge', [i], ('harden the soft edges of the effect in frame %d'
                                         if rest.any() else 'effect soft edges in frame %d already resolved') % (i + 1),
                        'proposed' if rest.any() else 'fixed')
                if c.id in accept:
                    a[rest, 3] = np.where(a[rest, 3] >= 128, 255, 0)
                    c.result = 'fixed'
        elif f.check == 'specks':
            fr = measure.Frame(a)
            a[measure.loose_specks(fr, rl) & measure.body_mask(b, i)] = 0
            new('specks', [i], 'removed %d px of loose specks from frame %d' % (f.measured, i + 1))
        elif f.check == 'holes':
            _fill_from_neighbours(a, measure.pinholes(a[..., 3] >= 128))
            new('holes', [i], 'filled the pinholes in frame %d' % (i + 1))
        elif f.check == 'bg_leak':
            on = a[..., 3] >= 128
            leak = ndimage.binary_fill_holes(on) & (a[..., :3] == anim.bg).all(-1) & on
            _fill_from_neighbours(a, leak)
            new('bg_leak', [i], 'painted over the background colour inside frame %d' % (i + 1))
        elif f.check in ('weapon_lost', 'broken_thin'):
            src = next((j for d in (1, -1, 2, -2) for j in [i + d] if 0 <= j < len(b.frames) and j not in weapon), None)
            if src is None:
                new(f.check, [i], 'no clean frame within 2 frames to copy the %s from' % 'weapon', 'still failing')
                continue
            g = anim.frames[src]
            gon, on = g[..., 3] >= 128, a[..., 3] >= 128
            best = max(((((np.roll(np.roll(gon, dy, 0), dx, 1) & on).sum() / max(1, (np.roll(np.roll(gon, dy, 0), dx, 1) | on).sum())), dx, dy)
                        for dy in range(-3, 4) for dx in range(-3, 4)), key=lambda t: (t[0], -abs(t[1]) - abs(t[2])))
            gs = _shift(g, best[1], best[2])
            thin = measure._thin(gs[..., 3] >= 128)
            a[thin] = gs[thin]
            new(f.check, [i], 'copied the thin parts (weapon, staff) into frame %d from frame %d' % (i + 1, src + 1))
        elif f.check in COLOUR:
            if i in colour_done:
                new(f.check, [i], 'colours of frame %d fixed together with %s' % (i + 1, colour_done[i]))
                continue
            on = a[..., 3] >= 128
            target = on.copy()
            target[on] = measure.colour_distance(a[on][:, :3], ref_cols) <= T['repair_de']
            px = a[target][:, :3]
            lum = measure.luma(px).mean() if len(px) else 0
            if lum and lum / ref_luma > 1 + T['washed']:
                new(f.check, [i], 'frame %d is washed out; colour matching would turn it muddy - drop or re-roll it' % (i + 1), 'still failing')
                colour_done[i] = changes[-1].id
                continue
            if lum and f.check != 'colour_count':
                px = np.clip(px.astype(float) * (ref_luma / lum), 0, 255).astype(np.uint8)
            a[target, :3] = snap(px, ref_cols)
            colour_done[i] = new(f.check, [i], 'matched frame %d to the reference colours and brightness' % (i + 1)).id
        elif f.check == 'ground':
            whole_frame('ground', i, _shift(a, 0, int(f.measured)),
                        'moved frame %d down %d px onto the ground line' % (i + 1, f.measured))
        elif f.check == 'flash':
            c = new('flash', [i], 'remove the one-frame effect in frame %d' % (i + 1), 'proposed')
            if c.id in accept:
                eff = a[..., 3] > 0
                eff[eff] = measure.colour_distance(a[eff][:, :3], ref_cols) > T['effect_de']
                lab, ne = ndimage.label(eff, measure.EIGHT)
                for p in range(1, ne + 1):
                    if (lab == p).sum() >= T['flash_px']:
                        a[lab == p] = 0
                c.result = 'fixed'
    return b, changes
