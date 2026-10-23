"""The /pga-fix checks. run() measures one animation and returns (findings, skipped): one Finding per check per frame,
and the checks it couldn't run with the reason. Every number it flags at lives in thresholds.T."""
import numpy as np
from scipy import ndimage, signal

from fixlib.colour import oklab  # noqa: F401  (repair and the tests use measure.oklab)
from fixlib.frames import detect_scale
from fixlib.model import Finding
from fixlib.thresholds import T

EIGHT = np.ones((3, 3), bool)
GROUNDED_SKIP = {'death'}


def luma(rgb: np.ndarray) -> np.ndarray:
    return rgb.astype(float) @ [0.299, 0.587, 0.114]


class Frame:
    """Per-frame facts the checks share: opaque mask, pieces, the main body piece."""

    def __init__(self, a: np.ndarray):
        self.a = a
        self.on = a[..., 3] >= 128
        self.lab, n = ndimage.label(self.on, EIGHT)
        sizes = ndimage.sum(self.on, self.lab, range(1, n + 1)) if n else np.array([])
        self.sizes = sizes
        self.main_id = 1 + int(np.argmax(sizes)) if n else 0
        self.main = self.lab == self.main_id if n else np.zeros_like(self.on)
        self.n = n

    @property
    def core(self) -> np.ndarray:
        """The main body without its thin parts (weapons, staffs): what motion and the cell grid follow, so a
        swinging or missing weapon doesn't read as the body jumping."""
        if not hasattr(self, '_core'):
            c = ndimage.binary_opening(self.main, np.ones((5, 5), bool))
            self._core = c if c.any() else self.main
        return self._core

    def foot(self) -> int:
        ys = np.nonzero(self.main.any(1))[0]
        return int(ys.max()) if len(ys) else -1


def _ref_colours(ref: np.ndarray) -> np.ndarray:
    return np.unique(ref[ref[..., 3] >= 128][:, :3], axis=0)


def colour_distance(rgb: np.ndarray, ref_cols: np.ndarray) -> np.ndarray:
    """OKLab distance from each colour to its nearest reference colour (unique colours looked up once)."""
    if not len(rgb):
        return np.zeros(0)
    cols, inv = np.unique(rgb, axis=0, return_inverse=True)
    rl = oklab(ref_cols)
    d = np.sqrt(((oklab(cols)[:, None] - rl[None]) ** 2).sum(-1)).min(1)
    return d[inv.ravel()]


def body_mask(anim, i: int) -> np.ndarray:
    """The character's own pixels in frame i: opaque and near a reference colour. Opaque pixels outside it are
    effect candidates (flashes, slashes, glows)."""
    f = anim.frames[i]
    on = f[..., 3] >= 128
    out = np.zeros(on.shape, bool)
    if not on.any():
        return out
    px = f[on][:, :3].astype(float)
    ref_on = anim.ref[..., 3] >= 128
    lum, ref_lum = luma(px).mean(), luma(anim.ref[ref_on][:, :3]).mean() if ref_on.any() else 0
    if lum and ref_lum:   # a whole frame drawn brighter or darker is still the body: judge colours after levelling
        px = np.clip(px * (ref_lum / lum), 0, 255)
    out[on] = colour_distance(px.round().astype(np.uint8), _ref_colours(anim.ref)) <= T['effect_de']
    return out


def pinholes(on: np.ndarray) -> np.ndarray:
    """Transparent pixels whose 8 neighbours are all opaque: a pinhole, not a drawn gap (real art has small enclosed
    gaps between fingers, staff and arm, and 1 px outline notches open on a diagonal)."""
    p = np.pad(on, 1)
    h, w = on.shape
    out = ~on
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            if dy != 1 or dx != 1:
                out &= p[dy:dy + h, dx:dx + w]
    return out


def ref_loose(anim) -> np.ndarray:
    """The reference's own loose parts (sparks, a held orb): specks near these are kept."""
    r = Frame(anim.ref)
    return r.on & ~r.main


def loose_specks(f, ref_loose_mask: np.ndarray) -> np.ndarray:
    """Pieces of at most T['specks'] px, more than T['speck_gap'] px from the body and not next to the reference's
    own loose parts."""
    near_body = ndimage.binary_dilation(f.main, EIGHT, iterations=T['speck_gap'] + 1)
    near_ref = ndimage.binary_dilation(ref_loose_mask, EIGHT, iterations=3) if ref_loose_mask.shape == f.on.shape else None
    out = np.zeros(f.on.shape, bool)
    for k in range(1, f.n + 1):
        if k == f.main_id or f.sizes[k - 1] > T['specks']:
            continue
        piece = f.lab == k
        if not (piece & near_body).any() and not (near_ref is not None and (piece & near_ref).any()):
            out |= piece
    return out


def _ground_line(anim, fr) -> int:
    """Where the feet belong: the reference's foot line when it shares the frames' canvas, else frame 0's (a one-shot
    starts standing) or the median (a loop)."""
    if anim.ref.shape == anim.frames[0].shape:
        return Frame(anim.ref).foot()
    if anim.kind == 'oneshot':
        return fr[0].foot()
    return int(np.median([f.foot() for f in fr]))


def _clean_checks(anim, fr, out, skipped, style):
    ref_cols = _ref_colours(anim.ref)
    ref_fr = Frame(anim.ref)
    ref_loose = ref_fr.on & ~ref_fr.main
    ref_luma = luma(anim.ref[ref_fr.on][:, :3]).mean() if ref_fr.on.any() else 0
    ground = _ground_line(anim, fr) if anim.move not in GROUNDED_SKIP else None
    if ground is None:
        skipped.append('ground: %s moves leave the ground line' % anim.move)
    for i, f in enumerate(fr):
        a = f.a
        if not f.on.any():
            out.append(Finding('empty', [i], 0, 0, 'high', 'whole', 'frame %d is empty' % (i + 1)))
            continue
        h, w = f.on.shape
        sides = {'left': f.on[:, 0].sum(), 'right': f.on[:, w - 1].sum(), 'top': f.on[0].sum()}   # feet on the bottom are normal
        side, n = max(sides.items(), key=lambda kv: kv[1])
        if n > T['edge']:
            out.append(Finding('edge', [i], float(n), T['edge'], 'high', 'body',
                               'frame %d is cut off at the %s edge (%d px on the border)' % (i + 1, side, n)))
        if ground is not None:
            gap = ground - f.foot()
            if gap > T['ground']:
                out.append(Finding('ground', [i], float(gap), T['ground'], 'mid', 'body',
                                   'frame %d floats %d px above the ground line' % (i + 1, gap)))
        body = body_mask(anim, i)
        for k in range(1, f.n + 1):
            if k != f.main_id and f.sizes[k - 1] > T['detached'] and anim.move != 'death':
                if (body & (f.lab == k)).sum() * 2 < f.sizes[k - 1]:
                    continue   # mostly effect-coloured: a slash or spark, judged by the effect checks
                size = int(f.sizes[k - 1])
                out.append(Finding('detached', [i], float(size), T['detached'], 'high', 'body',
                                   'frame %d has a %d px piece off the body (a thrown weapon?)' % (i + 1, size)))
        specks = int((loose_specks(f, ref_loose) & body).sum())   # sparks and particles in effect colours are art
        if specks > T['specks_px']:
            out.append(Finding('specks', [i], float(specks), 0, 'low', 'body', 'frame %d has %d px of loose specks' % (i + 1, specks)))
        filled = ndimage.binary_fill_holes(f.on)
        small = int(pinholes(f.on).sum())
        if small > T['holes']:
            out.append(Finding('holes', [i], float(small), T['holes'], 'low', 'body', 'frame %d has %d px of pinholes' % (i + 1, small)))
        if anim.bg is not None and not (ref_cols == np.array(anim.bg)).all(1).any():   # a colour the art uses (black outlines, eyes) isn't a leak
            leak = int((filled & (a[..., :3] == anim.bg).all(-1) & f.on).sum())
            if leak > T['bg_leak']:
                out.append(Finding('bg_leak', [i], float(leak), T['bg_leak'], 'mid', 'body',
                                   'frame %d has %d px of background colour inside the body' % (i + 1, leak)))
        bpx = a[f.main & body][:, :3]
        px = bpx if len(bpx) * 2 >= f.main.sum() else a[f.main][:, :3]
        if ref_luma:
            r = luma(px).mean() / ref_luma
            if abs(r - 1) > T['brightness']:
                out.append(Finding('brightness', [i], round(float(r), 3), T['brightness'], 'mid', 'body',
                                   'frame %d is %d%% %s than the reference' % (i + 1, round(abs(r - 1) * 100), 'brighter' if r > 1 else 'darker')))
        allpx = a[f.main][:, :3]
        d = colour_distance(allpx, ref_cols) if len(allpx) else np.zeros(0)
        if len(d) and (d > T['effect_de']).mean() > 0.5:
            far = float((d > T['palette_de']).mean())        # most of the body is off: a recolour
        else:
            dd = d[d <= T['effect_de']]                        # effect-coloured pixels are judged as effects
            far = float((dd > T['palette_de']).mean()) if len(dd) else 0.0
        if far > T['palette']:
            out.append(Finding('palette', [i], round(far, 3), T['palette'], 'mid', 'body',
                               'frame %d: %d%% of the body is off the reference colours' % (i + 1, round(far * 100))))


def _aligned_iou(a: np.ndarray, b: np.ndarray) -> float:
    """Silhouette overlap with both masks cropped to their art, bottoms and centres lined up."""
    def crop(m):
        ys, xs = np.nonzero(m)
        return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(ys) else np.zeros((1, 1), bool)
    a, b = crop(a), crop(b)
    h, w = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
    def put(m):
        c = np.zeros((h, w), bool)
        x = (w - m.shape[1]) // 2
        c[h - m.shape[0]:, x:x + m.shape[1]] = m
        return c
    a, b = put(a), put(b)
    return float((a & b).sum() / max(1, (a | b).sum()))


def _step(f0, f1, height) -> float:
    """How far the body moves from one frame to the next: centroid distance (movement) + silhouette change after
    centring x body height (shape). Without centring, a 1 px shift of a thin figure read as a big change."""
    if not f0.core.any() or not f1.core.any():
        return 0.0
    c0, c1 = np.argwhere(f0.core).mean(0), np.argwhere(f1.core).mean(0)
    dy, dx = np.round(c0 - c1).astype(int)
    m1 = np.roll(np.roll(f1.core, dy, 0), dx, 1)
    iou = (f0.core & m1).sum() / max(1, (f0.core | m1).sum())
    return float(np.hypot(*(c1 - c0)) + (1 - iou) * height)


def _motion_checks(anim, fr, out, skipped, style):
    n = len(fr)
    if anim.kind == 'oneshot' and anim.move != 'death' and fr[-1].on.any() and anim.ref is not None:
        iou = _aligned_iou(fr[-1].main, Frame(anim.ref).main)
        if iou < T['return_iou']:
            out.append(Finding('return_to_stand', [n - 1], round(iou, 3), T['return_iou'], 'low', 'body',
                               'the move ends in a pose far from the standing one (overlap %d%%)' % round(iou * 100)))
    if n < 3:
        skipped.append('motion: fewer than 3 frames')
        return
    ys = np.nonzero(Frame(anim.ref).on.any(1))[0]
    height = float(ys.max() - ys.min() + 1) if len(ys) else float(fr[0].on.shape[0])
    steps = [_step(fr[i], fr[i + 1], height) for i in range(n - 1)]
    loop = anim.kind == 'loop'
    seam = _step(fr[-1], fr[0], height) if loop else None
    med = float(np.median(steps)) or 1.0
    big = [s >= max(T['jump_px'], T['jump_x'] * med) for s in steps]
    if loop:
        if seam > T['seam_x'] * med and seam >= T['jump_px']:
            out.append(Finding('loop_seam', [n - 1], round(seam, 1), round(T['seam_x'] * med, 1), 'mid', 'body',
                               'the loop jumps from the last frame back to the first'))
    ring = steps + ([seam] if loop else [])
    bigring = big + ([seam >= max(T['jump_px'], T['jump_x'] * med)] if loop else [])
    for i in range(n):            # frame i sits between step i-1 and step i
        before = bigring[i - 1] if (i > 0 or loop) else False
        after = bigring[i] if i < len(bigring) else False
        if before and after:
            out.append(Finding('jump', [i], round(max(ring[i - 1], ring[i % len(ring)]), 1), round(T['jump_x'] * med, 1),
                               'high', 'body', 'frame %d jumps out of the motion and back' % (i + 1)))
    for i, s in enumerate(steps):
        calm_before = i == 0 or steps[i - 1] <= med
        calm_after = i == len(steps) - 1 or steps[i + 1] <= med
        if s >= T['gap_x'] * med and s >= T['jump_px'] and calm_before and calm_after:
            out.append(Finding('missing_inbetween', [i, i + 1], round(s, 1), round(T['gap_x'] * med, 1), 'mid', 'body',
                               'frames %d to %d move too far in one step (in-betweens missing)' % (i + 1, i + 2)))
    if anim.move != 'death':
        mass = [float(f.main.sum()) for f in fr]
        for i in range(1, n - 1):
            prev = mass[i - 1] or 1.0
            if abs(mass[i] / prev - 1) > T['mass_pop'] and any(
                    abs(mass[j] / prev - 1) <= T['mass_pop'] / 2 for j in range(i + 1, min(n, i + 3))):
                out.append(Finding('size_pop', [i], round(mass[i] / prev, 2), T['mass_pop'], 'mid', 'body',
                                   'frame %d suddenly changes size and changes back' % (i + 1)))


def _effect_pieces(anim, fr):
    """Per frame: (label array, list of piece ids) of effect-coloured pieces of at least flash_px."""
    out = []
    for i, f in enumerate(fr):
        eff = f.on & ~body_mask(anim, i)
        lab, n = ndimage.label(eff, EIGHT)
        sizes = ndimage.sum(eff, lab, range(1, n + 1)) if n else []
        out.append((lab, [k + 1 for k, s in enumerate(sizes) if s >= T['flash_px']]))
    return out


def _cells(anim, a: np.ndarray, on: np.ndarray, ref_cols: np.ndarray, box: np.ndarray = None):
    """The body's bounding box (of `box`, default `on`) cut 3 x 3; each cell's mix of reference colours."""
    ys, xs = np.nonzero(on if box is None else box)
    if not len(ys):
        return None
    yb = np.linspace(ys.min(), ys.max() + 1, 4).astype(int)
    xb = np.linspace(xs.min(), xs.max() + 1, 4).astype(int)
    rl = oklab(ref_cols)
    out = []
    for r in range(3):
        for c in range(3):
            m = on[yb[r]:yb[r + 1], xb[c]:xb[c + 1]]
            px = a[yb[r]:yb[r + 1], xb[c]:xb[c + 1]][m][:, :3]
            h = np.zeros(len(ref_cols) + 1)
            if len(px):
                cols, inv = np.unique(px, axis=0, return_inverse=True)
                d = ((oklab(cols)[:, None] - rl[None]) ** 2).sum(-1)
                idx = np.where(np.sqrt(d.min(1)) <= T['palette_de'], d.argmin(1), len(ref_cols))
                np.add.at(h, idx[inv.ravel()], 1)
                h /= h.sum()
            out.append(h)
    return out


CELL_NAMES = ['top left', 'top centre', 'top right', 'middle left', 'centre', 'middle right',
              'bottom left', 'bottom centre', 'bottom right']


def _thin(on: np.ndarray) -> np.ndarray:
    """Thin parts: what a 5 x 5 opening removes from the silhouette (staffs, blades, fingers)."""
    return on & ~ndimage.binary_opening(on, np.ones((5, 5), bool))


def _identity_checks(anim, fr, out, skipped, style):
    n = len(fr)
    eff = _effect_pieces(anim, fr)
    def present(i, mask):
        lab, ids = eff[i]
        return bool(ids) and bool((np.isin(lab, ids) & ndimage.binary_dilation(mask, EIGHT, iterations=3)).any())
    run = []
    for i in range(n):
        lab, ids = eff[i]
        if not ids:
            continue
        mask = np.isin(lab, ids)
        lasting = (i > 0 and present(i - 1, mask)) or (i < n - 1 and present(i + 1, mask))
        if lasting:
            run.append(i)
        else:
            px = int(mask.sum())
            out.append(Finding('flash', [i], float(px), T['flash_px'], 'high', 'effect',
                               'frame %d has a %d px effect that appears in no other frame' % (i + 1, px)))
    if run:
        out.append(Finding('effect', run, float(len(run)), 2, 'low', 'effect',
                           'frames %s carry a lasting effect (looks intended: slash, glow, trail)' % ', '.join(str(j + 1) for j in run)))
    if n < 3:
        skipped.append('identity: fewer than 3 frames')
        return
    ref_cols = _ref_colours(anim.ref)
    cells = [_cells(anim, f.a, f.core, ref_cols) for f in fr]   # the body core: a weapon coming and going is the weapon checks' job
    dist = lambda p, q: 0.5 * float(np.abs(p - q).sum())
    for i in range(1, n - 1):
        if cells[i] is None or cells[i - 1] is None or cells[i + 1] is None:
            continue
        hit = [(dist(cells[i][c], cells[i - 1][c]), CELL_NAMES[c]) for c in range(9)
               if dist(cells[i][c], cells[i - 1][c]) > T['cell_change'] and dist(cells[i][c], cells[i + 1][c]) > T['cell_change']
               and dist(cells[i - 1][c], cells[i + 1][c]) <= T['cell_change'] / 2]
        if hit:   # one finding per frame, naming every part that changed
            out.append(Finding('weird_change', [i], round(max(d for d, _ in hit), 2), T['cell_change'], 'high', 'body',
                               'frame %d: the %s of the character change%s and change%s back' % (
                                   i + 1, ', '.join(nm for _, nm in hit), '' if len(hit) > 1 else 's', '' if len(hit) > 1 else 's')))
    thin = [_thin(f.main) for f in fr]   # the body's own thin parts: loose specks aren't a weapon
    mass = [float(t.sum()) for t in thin]
    def missing(i, j):
        """Share of frame j's thin detail (weapons, staffs) that frame i lacks: by amount, not place, since weapons
        swing far between frames (place-based matching flagged 80% of a shipped set)."""
        if not 0 <= j < n or mass[j] < 10:
            return None
        return max(0.0, 1.0 - mass[i] / mass[j])
    for i in range(n):
        worst = None
        for side in (-1, 1):   # each side: the frame next to it, or the one after when that one lacks it too
            got = [m for m in (missing(i, i + side), missing(i, i + 2 * side)) if m is not None]
            if got:
                worst = max(got) if worst is None else min(worst, max(got))
        if worst is None:
            continue
        if worst >= T['thin_lost']:
            out.append(Finding('weapon_lost', [i], round(worst, 2), T['thin_lost'], 'high', 'body',
                               'frame %d lost a thin part (weapon, staff) its neighbours have' % (i + 1)))
        elif worst >= T['thin_broken']:
            out.append(Finding('broken_thin', [i], round(worst, 2), T['thin_broken'], 'mid', 'body',
                               'frame %d has a broken thin part (weapon, staff)' % (i + 1)))


def _nonuniform_share(a: np.ndarray, k: int) -> float:
    """Share of the k x k blocks over the art that aren't one colour (best grid phase)."""
    on = a[..., 3] > 0
    ys, xs = np.nonzero(on)
    if not len(ys):
        return 0.0
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = 1.0
    for py in range(k):
        for px in range(k):
            b = a[py:, px:]
            h, w = (b.shape[0] // k) * k, (b.shape[1] // k) * k
            if not h or not w:
                continue
            bl = b[:h, :w].reshape(h // k, k, w // k, k, 4).transpose(0, 2, 1, 3, 4).reshape(h // k, w // k, -1, 4)
            used = (bl[..., 3] > 0).any(-1)
            if used.sum():
                best = min(best, float((~(bl == bl[:, :, :1]).all((-1, -2)) & used).sum() / used.sum()))
    return best


def body_only(anim, i: int) -> np.ndarray:
    """Frame i with everything but the character's own pixels cleared (effects, sparkles)."""
    a = anim.frames[i].copy()
    a[~body_mask(anim, i)] = 0
    return a


def set_scale(anim) -> tuple:
    """(each frame's pixel size, the set's), measured on the character's own pixels: lasting 1 px sparkles drawn over
    2x art made the clean frames read as the odd ones out."""
    scales = [detect_scale(body_only(anim, i)) for i in range(len(anim.frames))]
    return scales, max(set(scales), key=scales.count)


def _crisp_checks(anim, fr, out, skipped, style):
    style = style or {}
    scales, k = set_scale(anim)
    ref_on = anim.ref[..., 3] > 0
    ref_n = len(np.unique(anim.ref[ref_on][:, :3], axis=0))
    ys = np.nonzero(Frame(anim.ref).main.any(1))[0]
    ref_h = float(ys.max() - ys.min() + 1) if len(ys) else 0.0
    for i, f in enumerate(fr):
        a = f.a
        if not f.on.any():
            continue
        if scales[i] != k:
            out.append(Finding('grid', [i], float(scales[i]), float(k), 'high', 'body',
                               'frame %d is drawn at %d px pixels, the rest at %d' % (i + 1, scales[i], k)))
        if k > 1:
            share = _nonuniform_share(body_only(anim, i), k)
            if share > T['mixels']:
                out.append(Finding('mixels', [i], round(share, 3), T['mixels'], 'mid', 'body',
                                   'frame %d mixes pixel sizes (%d%% of %d px blocks are not one colour)' % (i + 1, round(share * 100), k)))
        if not style.get('soft_edges'):
            soft = (a[..., 3] > 0) & (a[..., 3] < 255)
            if soft.sum() > T['soft_px']:
                near = ndimage.binary_dilation(f.main, EIGHT, iterations=1)
                body_soft = int((soft & near).sum())
                region = 'body' if body_soft * 2 >= soft.sum() else 'effect'
                out.append(Finding('soft_edge', [i], float(soft.sum()), T['soft_px'], 'mid', region,
                                   'frame %d has %d half-transparent pixels (soft edges)' % (i + 1, soft.sum())))
        n = len(np.unique(a[a[..., 3] > 0][:, :3], axis=0))
        limit = T['colour_ratio'] * max(ref_n, (style.get('palette_size') or 0))
        if ref_n and n > limit:
            out.append(Finding('colour_count', [i], round(n / max(ref_n, 1), 2), T['colour_ratio'], 'mid', 'body',
                               'frame %d uses %d colours, the reference %d (blur or anti-aliasing?)' % (i + 1, n, ref_n)))
        if ref_h and anim.kind == 'loop':   # poses change height (a one-shot may start from a wind-up); loops stand
            ys = np.nonzero(f.main.any(1))[0]
            r = (ys.max() - ys.min() + 1) / ref_h
            if not T['size_lo'] <= r <= T['size_hi']:
                out.append(Finding('size', [i], round(float(r), 2), T['size_hi'] if r > 1 else T['size_lo'], 'mid', 'body',
                                   'frame %d draws the character %d%% %s than the reference' % (i + 1, round(abs(r - 1) * 100), 'bigger' if r > 1 else 'smaller')))


def _largest(m: np.ndarray) -> np.ndarray:
    lab, n = ndimage.label(m, EIGHT)
    return lab == 1 + int(np.argmax(ndimage.sum(m, lab, range(1, n + 1)))) if n else m


def _head_template(ref: np.ndarray):
    """The reference's head: the top band of its body core (a staff tip above it is cut off by the core)."""
    body = _largest(Frame(ref).core)
    ys = np.nonzero(body.any(1))[0]
    if not len(ys):
        return None
    top, h = ys.min(), ys.max() - ys.min() + 1
    rows = max(4, int(h * T['head_band']))
    band = body[top:top + rows]
    xs = np.nonzero(band.any(0))[0]
    box = (slice(top, top + rows), slice(xs.min(), xs.max() + 1))
    on = ref[box][..., 3] >= 128
    return oklab(ref[box][..., :3]) * on[..., None], on


def _head_cost(a: np.ndarray, tpl):
    """Best mean squared OKLab distance of the reference head over the upper half of the frame's body; a template
    pixel over a transparent one counts as a miss. None when the frame can't be measured (empty, or too small)."""
    t, m = tpl
    body = _largest(Frame(a).core)
    ys, xs = np.nonzero(body)
    if not len(ys):
        return None
    th, tw = m.shape
    y0, y1 = max(0, ys.min() - th), min(a.shape[0], ys.min() + (ys.max() - ys.min()) // 2 + th)
    x0, x1 = max(0, xs.min() - tw), min(a.shape[1], xs.max() + tw)
    sub = a[y0:y1, x0:x1]
    if sub.shape[0] < th or sub.shape[1] < tw:
        return None
    on = (sub[..., 3] >= 128).astype(float)
    w = oklab(sub[..., :3]) * on[..., None]
    mf = m.astype(float)
    corr = lambda x, k: signal.correlate(x, k, mode='valid', method='fft')
    ssd = corr((w ** 2).sum(-1), mf) - 2 * sum(corr(w[..., c], t[..., c]) for c in range(3)) + corr(on, (t ** 2).sum(-1))
    cost = (ssd + T['head_miss'] * corr(1 - on, mf)) / mf.sum()
    return float(cost.min())


def _head_checks(anim, fr, out, skipped, style):
    """A head or face that differs from the frames on both sides (turned away, toward the viewer, a pale-to-warm
    skin flicker): the cell checks dilute it into the whole top of the body."""
    n = len(fr)
    tpl = _head_template(anim.ref) if n >= 3 and anim.move != 'death' else None
    if tpl is None:
        skipped.append('head: fewer than 3 frames, a death, or no reference head')
        return
    cost = [_head_cost(f.a, tpl) if f.on.any() else None for f in fr]
    for i in range(1, n - 1):
        if None in (cost[i - 1], cost[i], cost[i + 1]):   # an empty or unmeasurable neighbour: no verdict
            continue
        nb = max(cost[i - 1], cost[i + 1])
        if cost[i] - nb >= T['head_gap'] and cost[i] >= T['head_x'] * nb:
            out.append(Finding('head_change', [i], round(cost[i], 4), round(max(T['head_x'] * nb, nb + T['head_gap']), 4), 'mid', 'body',
                               'frame %d: the head or face differs from the frames around it (turned away, toward the viewer, '
                               'or another skin colour)' % (i + 1)))


def _prop_side(f) -> float:
    """Where the thin parts (staff, blade) sit across the body: (their centre - the core's centre) / core width."""
    thin = _thin(f.main)
    if thin.sum() < 10 or not f.core.any():
        return None
    xs = np.nonzero(f.core.any(0))[0]
    return float((np.nonzero(thin)[1].mean() - np.nonzero(f.core)[1].mean()) / (xs.max() - xs.min() + 1))


def _prop_checks(anim, fr, out, skipped, style):
    """A one-shot's in-betweens keep a held prop between where its first and last frames hold it: a staff that drifts
    to the body's centre line or swaps hands in between leaves that span."""
    n = len(fr)
    side = [_prop_side(f) for f in fr]
    if n < 3 or anim.kind != 'oneshot' or side[0] is None or side[-1] is None:
        skipped.append('prop: not a one-shot of 3+ frames with a thin prop at both ends')
        return
    lo, hi = min(side[0], side[-1]) - T['prop_side'], max(side[0], side[-1]) + T['prop_side']
    off = [i for i in range(1, n - 1) if side[i] is not None and not lo <= side[i] <= hi]
    if off:
        worst = max(max(lo - side[i], side[i] - hi) for i in off)
        out.append(Finding('prop_drift', off, round(worst, 3), T['prop_side'], 'low', 'body',
                           'frames %s: the held prop (staff, blade) leaves the side of the body it holds at the start and end '
                           '(drifts to the centre line or changes hands): look, then re-roll if it is not the swing'
                           % ', '.join(str(i + 1) for i in off)))


CHECKS = [_clean_checks, _motion_checks, _identity_checks, _crisp_checks, _head_checks, _prop_checks]


def run(anim, style=None):
    fr = [Frame(a) for a in anim.frames]
    out, skipped = [], []
    for check in CHECKS:
        check(anim, fr, out, skipped, style)
    return out, skipped
