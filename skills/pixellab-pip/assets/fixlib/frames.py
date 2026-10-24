"""Loading frames for the animation doctor: files, folders (a batch of characters x moves), sprite sheets and GIFs, all put on
one canvas per animation; and writing them back at each frame's own size and name."""
import glob
import os
import re
import shutil

import numpy as np
from PIL import Image

from fixlib.model import Anim

MOVES = {'idle': 'loop', 'walk': 'loop', 'run': 'loop', 'attack': 'oneshot', 'skill': 'oneshot',
         'cast': 'oneshot', 'hurt': 'oneshot', 'death': 'oneshot'}
EXT = ('.png', '.gif')


def _natural(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


SKIP_DIRS = ('orig',)   # colormatch.py's backups of the raw frames; *_fixed folders are the animation doctor's own output


def _expand(inputs):
    """(file, input folder) in natural order. Folders are walked (not into orig/ or *_fixed/); * and ? are expanded
    here (cmd/PowerShell pass them literally)."""
    out = []
    for p in inputs:
        root = ''
        if '*' in p or '?' in p:
            hits = glob.glob(p)
        elif os.path.isdir(p):
            root = p
            hits = []
            for r, dirs, fs in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.endswith('_fixed')]
                hits += [os.path.join(r, f) for f in fs]
        else:
            hits = [p]
        out += [(h, root) for h in sorted((h for h in hits if h.lower().endswith(EXT)), key=_natural)]
    return out


def _rgba(im: Image.Image) -> np.ndarray:
    return np.array(im.convert('RGBA'))


def key_background(img: np.ndarray):
    """A frame with no transparency whose corners share one colour: that colour, where it touches the border, becomes
    transparent. Returns (frame, colour or None)."""
    if (img[..., 3] < 255).any():
        return img, None
    c = img[0, 0, :3]
    corners = [img[0, -1, :3], img[-1, 0, :3], img[-1, -1, :3]]
    if not all((k == c).all() for k in corners):
        return img, None
    from scipy import ndimage
    same = (img[..., :3] == c).all(-1)
    lab, _ = ndimage.label(same)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    out = img.copy()
    out[np.isin(lab, list(edge)), 3] = 0
    return out, tuple(int(v) for v in c)


def detect_scale(img: np.ndarray) -> int:
    """The pixel size the art is drawn at: the largest k whose k x k blocks over the art are one colour in >= 97% of
    blocks (best grid phase)."""
    on = img[..., 3] > 0
    if not on.any():
        return 1
    ys, xs = np.nonzero(on)
    a = img[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    for k in (8, 6, 5, 4, 3, 2):
        if min(a.shape[:2]) < 2 * k:
            continue
        for py in range(k):
            for px in range(k):
                b = a[py:, px:]
                h, w = (b.shape[0] // k) * k, (b.shape[1] // k) * k
                if not h or not w:
                    continue
                blocks = b[:h, :w].reshape(h // k, k, w // k, k, 4).transpose(0, 2, 1, 3, 4).reshape(h // k, w // k, -1, 4)
                used = (blocks[..., 3] > 0).any(-1)
                uniform = (blocks == blocks[:, :, :1]).all((-1, -2))
                if used.sum() and (uniform & used).sum() / used.sum() >= 0.97:
                    return k
    return 1


def _parse(path):
    """(character, move, frame number) from a file name like knight_attack_3.png; a bare number takes the folder."""
    stem = os.path.splitext(os.path.basename(path))[0]
    toks = [t for t in re.split(r'[_\-\s]+', stem) if t]
    num = int(toks.pop()) if toks and toks[-1].isdigit() else 0
    if not toks:
        folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
        toks = [t for t in re.split(r'[_\-\s]+', folder) if t] or ['frames']
    move = 'other'
    for i in range(len(toks) - 1, -1, -1):
        if toks[i].lower() in MOVES:
            move = toks[i].lower()
            toks = toks[:i] + toks[i + 1:]
            break
    return '_'.join(toks) or 'frames', move, num


def _canvas(raw):
    """Frames of different sizes on one canvas, bottom-centre."""
    W, H = max(f.shape[1] for f in raw), max(f.shape[0] for f in raw)
    frames, offsets = [], []
    for f in raw:
        x, y = (W - f.shape[1]) // 2, H - f.shape[0]
        c = np.zeros((H, W, 4), np.uint8)
        c[y:y + f.shape[0], x:x + f.shape[1]] = f
        frames.append(c)
        offsets.append((x, y))
    return frames, offsets


def _anim(character, move, raw, paths, durations=None, source=''):
    keyed = [key_background(f) for f in raw]
    bgs = {b for _, b in keyed if b}
    raw2 = [f for f, _ in keyed]
    frames_, offsets = _canvas(raw2)
    kind = MOVES.get(move, 'oneshot')
    return Anim(key='%s/%s' % (character, move), character=character, move=move, kind=kind, kind_guessed=True,
                paths=paths, frames=frames_, offsets=offsets, sizes=[(f.shape[1], f.shape[0]) for f in raw2],
                scale=detect_scale(frames_[0]), durations=durations, bg=bgs.pop() if len(bgs) == 1 else None,
                source=source, originals=[f.copy() for f in raw], backgrounds=[c for _, c in keyed])


def _typical(fs):
    seen = [i for i, f in enumerate(fs) if (f[..., 3] >= 128).any()]   # an empty frame is never the reference
    if not seen:
        raise ValueError('every frame is empty; nothing to compare')
    med = np.median(np.stack([fs[i].astype(float) for i in seen]), 0)
    return fs[min(seen, key=lambda i: np.abs(fs[i].astype(float) - med).sum())]


def load(inputs, sheet=None, ref=None, move=None):
    files = _expand(inputs)
    anims = []
    groups = {}
    for p, root in files:
        sub = os.path.relpath(os.path.dirname(os.path.abspath(p)), os.path.abspath(root)) if root else '.'
        sub = '' if sub == '.' else sub
        if p.lower().endswith('.gif'):
            im = Image.open(p)
            raw, dur = [], []
            for i in range(getattr(im, 'n_frames', 1)):
                im.seek(i)
                raw.append(_rgba(im))
                dur.append(int(im.info.get('duration', 100)))
            ch, mv, _ = _parse(p)
            anims.append(_anim(ch, move or mv, raw, [], dur, p))
            anims[-1].subdir = sub
        elif sheet:
            a = _rgba(Image.open(p))
            w, h = sheet
            if w <= 0 or h <= 0 or a.shape[1] % w or a.shape[0] % h:
                raise ValueError("sheet dimensions must divide exactly into positive cells")
            raw = [a[y:y + h, x:x + w] for y in range(0, a.shape[0] - h + 1, h) for x in range(0, a.shape[1] - w + 1, w)]
            ch, mv, _ = _parse(p)
            anims.append(_anim(ch, move or mv, raw, [], None, p))
            anims[-1].subdir = sub
        else:
            ch, mv, num = _parse(p)
            groups.setdefault((os.path.dirname(os.path.abspath(p)), sub, ch, move or mv), []).append((num, p))
    for (_, sub, ch, mv), items in groups.items():
        items.sort(key=lambda t: (t[0], _natural(t[1])))
        paths = [p for _, p in items]
        anims.append(_anim(ch, mv, [_rgba(Image.open(p)) for p in paths], paths))
        anims[-1].subdir = sub
    seen = {}
    for a in anims:   # two animations never share a key: the report, timing.json and re-roll requests name them by it
        seen.setdefault(a.key, []).append(a)
    for key, same in seen.items():
        if len(same) > 1:
            for a in same:
                a.key = '%s (%s)' % (key, a.subdir or os.path.basename(a.source or a.paths[0]))
    if move:
        for a in anims:
            a.kind, a.kind_guessed = MOVES.get(move, 'oneshot'), False
    given = key_background(_rgba(Image.open(ref)))[0] if ref else None
    if given is not None and not (given[..., 3] >= 128).any():
        raise ValueError('--ref has no visible pixels (alpha >= 128): ' + ref)
    by_char = {}
    for a in anims:
        by_char.setdefault(a.character, []).append(a)
    for ch, group in by_char.items():
        if given is not None:
            r, guessed = given, False
        else:
            base = next((a for a in group if a.move == 'idle'), group[0])
            r, guessed = _typical(base.frames), True
        for a in group:
            a.ref, a.ref_guessed = r, guessed
    return anims


def names(anim) -> list:
    """Each frame's file name: the input's own, or <sheet/GIF name>_<n>.png counted from 1."""
    if anim.paths:
        return [os.path.basename(p) for p in anim.paths]
    stem = os.path.splitext(os.path.basename(anim.source))[0] if anim.source else '%s_%s' % (anim.character, anim.move)
    return ['%s_%d.png' % (stem, i + 1) for i in range(len(anim.frames))]


def output_pixels(anim, index, changed=None):
    """Undo analysis-only keying/padding; unchanged decoded containers keep original RGBA."""
    (x, y), (w, h) = anim.offsets[index], anim.sizes[index]
    if changed is not None and index not in changed and anim.originals:
        return anim.originals[index].copy()
    pixels = anim.frames[index][y:y + h, x:x + w].copy()
    bg = anim.backgrounds[index] if anim.backgrounds else anim.bg
    if bg:
        off = pixels[..., 3] == 0
        pixels[off, :3] = bg
        pixels[..., 3] = 255
    return pixels


def write(anim, out_dir, changed=None):
    """Preserve unchanged PNG bytes and decoded sheet/GIF pixels, not analysis-only keying."""
    out_dir = os.path.join(out_dir, anim.subdir) if anim.subdir else out_dir
    os.makedirs(out_dir, exist_ok=True)
    out = []
    for i, name in enumerate(names(anim)):
        dst = os.path.join(out_dir, name)
        if anim.paths and changed is not None and i not in changed:
            shutil.copyfile(anim.paths[i], dst)
        else:
            Image.fromarray(output_pixels(anim, i, changed), 'RGBA').save(dst)
        out.append(dst)
    return out
