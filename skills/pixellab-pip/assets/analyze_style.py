"""analyze_style.py <image.png|anim.gif|folder> [--out DIR] [--frames]
Measures a pixel-art image, GIF or folder of them so its style can be written down as rules:
candidate pixel scale (an advisory block-pattern estimate), subject size -> density, colour
count + palette, outline, tones per colour ramp, dithering, light direction, background; for a GIF
also frame count, per-frame timing, holds, motion per frame and ground-line drift.

Writes to --out (default ./style_analysis): analysis.json and palette.png (swatches); with --frames also native/
(frames at 1 px = 1 pixel) and look.png (one small sheet to look at once). Prints a short summary. It measures only;
the user's art is never changed. The words (genre, mood, materials) come from looking at the art itself.

  python analyze_style.py ref.gif --out style_analysis
"""
import sys
import _assembly  # noqa: E402,F401  (UTF-8-safe console)
if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    sys.exit(__doc__)
import colorsys
import glob
import json
import os
from _assembly import require_numpy, preflight_outputs  # noqa: E402

require_numpy()
import numpy as np  # noqa: E402
from PIL import Image, ImageSequence  # noqa: E402

src = sys.argv[1]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'style_analysis'
FRAMES = '--frames' in sys.argv


def load(path):
    """[(rgba array, duration ms)] for every frame."""
    im = Image.open(path)
    fr = []
    for f in ImageSequence.Iterator(im):
        fr.append((np.array(f.convert('RGBA')), f.info.get('duration', im.info.get('duration', 0)) or 0))
    return fr, im.info.get('loop')


def native_scale(a):
    """Candidate scale only: require exact blocks, so padding cannot hide a small detailed subject."""
    h, w = a.shape[:2]
    best = (1, 0, 0)
    for s in range(16, 1, -1):
        if h < 4 * s or w < 4 * s:
            continue
        for oy in range(s):
            for ox in range(s):
                small = a[oy::s, ox::s]
                up = np.repeat(np.repeat(small, s, 0), s, 1)[:h - oy, :w - ox]
                # Offsets discard border pixels, so only an aligned whole-image match is evidence.
                if ox or oy or h % s or w % s:
                    continue
                if np.array_equal(up, a):
                    return s, ox, oy
    return best


def key_background(a):
    """Opaque art: treat the border colour as background if most of the border is one colour."""
    if (a[..., 3] < 255).any():
        return a, 'transparent'
    edge = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])[:, :3]
    cols, cnt = np.unique(edge, axis=0, return_counts=True)
    if cnt.max() / len(edge) > 0.6:
        bg = cols[cnt.argmax()]
        a = a.copy()
        a[(a[..., :3] == bg).all(-1), 3] = 0
        return a, 'solid colour #%02x%02x%02x (keyed out)' % tuple(bg)
    return a, 'opaque scene'


def lum(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


paths = sorted(p for p in glob.glob(os.path.join(src, '*')) if p.lower().endswith(('.png', '.gif', '.webp'))) \
    if os.path.isdir(src) else [src]
if not paths:
    sys.exit('no PNG/GIF/WebP images to analyse')
items = []
for p in paths:
    frames, loop = load(p)
    s, ox, oy = native_scale(frames[0][0])
    nat = [(f[oy::s, ox::s], d) for f, d in frames]
    keyed, bgkind = zip(*[key_background(f) for f, _ in nat])
    items.append(dict(path=p, frames=list(keyed), dur=[d for _, d in nat], loop=loop, scale=s, bg=bgkind[0]))

# ---- still-image measures over every frame of every file ----
allpx = np.concatenate([f[f[..., 3] > 0][:, :3] for it in items for f in it['frames']])
if not len(allpx):
    sys.exit('no visible subject after advisory background analysis; inspect the original art')
cols, cnt = np.unique(allpx, axis=0, return_counts=True)
order = cnt.argsort()[::-1]
cols, cnt = cols[order], cnt[order]
n_colours = len(cols)
sig = cols[(np.cumsum(cnt) - cnt) / cnt.sum() < 0.99]   # include the colour that reaches 99%, omit the remaining tail
palette = ['#%02x%02x%02x' % tuple(c) for c in (sig if len(sig) <= 64 else cols[:32])]

hsv = np.array([colorsys.rgb_to_hsv(*(c / 255.0)) for c in sig]) if len(sig) else np.zeros((0, 3))
sat, val = (float(np.average(hsv[:, i], weights=cnt[:len(sig)])) for i in (1, 2)) if len(sig) else (0, 0)
# tones per ramp: colours grouped by hue (12 bins, saturated only) -> distinct brightness levels
tones = []
for b in range(12):
    m = (hsv[:, 1] > 0.15) & (np.floor(hsv[:, 0] * 12) % 12 == b)
    if m.sum() >= 2:
        tones.append(len(np.unique(np.round(hsv[m, 2] * 10))))
grey = hsv[:, 1] <= 0.15   # greys / steel / stone count as one more ramp
if grey.sum() >= 2:
    tones.append(len(np.unique(np.round(hsv[grey, 2] * 10))))
tones_med = int(max(np.median(tones), max(tones) - 1)) if tones else 0   # the main ramps decide, not the accents

outline_dark = outline_sel = dith = 0.0
light_v = light_h = 0.0
heights, widths = [], []
k = 0
for it in items:
    for f in it['frames']:
        al = f[..., 3] > 0
        if al.sum() < 20:
            continue
        ys, xs = np.nonzero(al)
        heights.append(int(ys.max() - ys.min() + 1)); widths.append(int(xs.max() - xs.min() + 1))
        L = lum(f[..., :3].astype(float))
        pad = np.pad(al, 1)
        edge = al & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
        inner = al & ~edge
        dark_cut = np.percentile(L[al], 12)
        outline_dark += (L[edge] <= dark_cut + 8).mean()
        # selective outline: edge pixel darker than the inside neighbour it touches
        sh = [np.roll(L, 1, 0), np.roll(L, -1, 0), np.roll(L, 1, 1), np.roll(L, -1, 1)]
        shi = [np.roll(inner, 1, 0), np.roll(inner, -1, 0), np.roll(inner, 1, 1), np.roll(inner, -1, 1)]
        darker = np.zeros_like(al)
        for v, iv in zip(sh, shi):
            darker |= iv & (L < v - 12)
        outline_sel += (darker & edge).sum() / max(1, edge.sum())
        # dithering: 2x2 checkerboards of two different colours inside the subject
        c = f[..., :3].astype(np.int32)
        code = c[..., 0] * 65536 + c[..., 1] * 256 + c[..., 2]
        a_, b_, c_, d_ = code[:-1, :-1], code[:-1, 1:], code[1:, :-1], code[1:, 1:]
        ins = al[:-1, :-1] & al[:-1, 1:] & al[1:, :-1] & al[1:, 1:]
        chk = ins & (a_ == d_) & (b_ == c_) & (a_ != b_)
        dith += chk.sum() / max(1, ins.sum())
        # light: brightness of the top vs bottom half, left vs right half of the subject
        cy, cx = ys.mean(), xs.mean()
        def mean_or_zero(values):
            return float(values.mean()) if values.size else 0.0
        light_v += mean_or_zero(L[al & (np.arange(f.shape[0])[:, None] < cy)]) - mean_or_zero(L[al & (np.arange(f.shape[0])[:, None] >= cy)])
        light_h += mean_or_zero(L[al & (np.arange(f.shape[1])[None, :] < cx)]) - mean_or_zero(L[al & (np.arange(f.shape[1])[None, :] >= cx)])
        k += 1
k = max(k, 1)
outline_dark, outline_sel, dith, light_v, light_h = (x / k for x in (outline_dark, outline_sel, dith, light_v, light_h))
outline = 'dark (near-black) 1 px outline' if outline_dark > 0.6 else \
    'selective outline (each colour edged in its own darker shade)' if outline_sel > 0.45 else 'no outline / soft edges'
ldir = ('top' if light_v > 6 else 'bottom' if light_v < -6 else '') + \
    ('-left' if light_h > 6 else '-right' if light_h < -6 else '')
ldir = ldir.strip('-') or 'flat / front'
subj_h = int(np.median(heights)) if heights else 0
density = 'low' if subj_h <= 48 else 'mid' if subj_h <= 110 else 'high'

res = {
    'advisory': 'Style, lighting, density and native scale are heuristics; inspect original art before approving rules.',
    'analysis_preprocessing': 'Candidate exact-block subsampling and dominant opaque-border colour keying affect analysis copies only.',
    'files': [dict(path=it['path'], frames=len(it['frames']), native_scale=it['scale'], background=it['bg'],
                   size=list(it['frames'][0].shape[1::-1])) for it in items],
    'subject_px': {'height': subj_h, 'width': int(np.median(widths)) if widths else 0},
    'density': density,
    'colours': {'count': n_colours, 'significant': len(sig), 'palette': palette},
    'saturation': round(sat, 2), 'brightness': round(val, 2),
    'tones_per_ramp': tones_med,
    'outline': outline, 'outline_scores': {'dark': round(outline_dark, 2), 'selective': round(outline_sel, 2)},
    'dithering': 'yes' if dith > 0.04 else 'light' if dith > 0.015 else 'no', 'dither_score': round(dith, 3),
    'light_from': ldir,
}

# ---- animation measures (GIFs / multi-frame files) ----
anims = []
for it in items:
    fr = it['frames']
    if len(fr) < 2:
        continue
    d = [x if x > 0 else 100 for x in it['dur']]
    med = float(np.median(d))
    bottoms = [int(np.nonzero((f[..., 3] > 0).any(1))[0].max()) for f in fr if (f[..., 3] > 0).any()]
    areas = [int((f[..., 3] > 0).sum()) for f in fr]
    motion = [round(float((np.abs(fr[i].astype(int) - fr[i - 1].astype(int)).sum(-1) > 0).mean() * 100), 1)
              for i in range(1, len(fr))]
    anims.append({
        'path': it['path'], 'frames': len(fr), 'durations_ms': d, 'median_ms': med,
        'duration_defaulted_indices': [i for i, value in enumerate(it['dur']) if value <= 0],
        'fps_equivalent': round(1000 / med, 1), 'total_ms': int(sum(d)),
        'holds': [i for i, x in enumerate(d) if x >= 1.8 * med],
        'loops': it['loop'] is not None and it['loop'] >= 0,
        'motion_pct_per_frame': motion,
        'ground_drift_px': (max(bottoms) - min(bottoms)) if bottoms else 0,
        'effect_frames': [i for i, a in enumerate(areas) if a > 1.35 * np.median(areas)],
    })
res['animations'] = anims
outputs = [os.path.join(out, 'analysis.json'), os.path.join(out, 'palette.png')]
if FRAMES:
    outputs.append(os.path.join(out, 'look.png'))
    for it in items:
        base = os.path.splitext(os.path.basename(it['path']))[0]
        outputs.extend(os.path.join(out, 'native', '%s_%d.png' % (base, i)) for i in range(len(it['frames'])))
try:
    preflight_outputs(outputs, paths)
except ValueError as exc:
    sys.exit(str(exc))
os.makedirs(os.path.join(out, 'native') if FRAMES else out, exist_ok=True)
with open(os.path.join(out, 'analysis.json'), 'w', encoding='utf-8') as handle:
    json.dump(res, handle, indent=1, allow_nan=False)

# ---- palette swatches, native frames, one look sheet ----
sw = Image.new('RGB', (16 * max(1, min(len(palette), 16)), 16 * max(1, ((len(palette) + 15) // 16))), (40, 40, 48))
for i, h in enumerate(palette):
    sw.paste(tuple(int(h[j:j + 2], 16) for j in (1, 3, 5)), ((i % 16) * 16, (i // 16) * 16, (i % 16) * 16 + 16, (i // 16) * 16 + 16))
sw.save(os.path.join(out, 'palette.png'))
thumbs = []
for n, it in enumerate(items if FRAMES else []):
    base = os.path.splitext(os.path.basename(it['path']))[0]
    for i, f in enumerate(it['frames']):
        Image.fromarray(f).save(os.path.join(out, 'native', '%s_%d.png' % (base, i)))
    step = max(1, len(it['frames']) // 8)
    thumbs += [Image.fromarray(f) for f in it['frames'][::step][:8]]
thumbs = thumbs[:16]
if thumbs:   # --frames: one small look sheet
    cw, ch = max(t.width for t in thumbs), max(t.height for t in thumbs)
    sc = max(1, min(4, 256 // max(cw, ch)))
    look = Image.new('RGBA', (cw * sc * min(8, len(thumbs)), ch * sc * ((len(thumbs) + 7) // 8)), (60, 60, 70, 255))
    for i, t in enumerate(thumbs):
        look.alpha_composite(t.resize((t.width * sc, t.height * sc), Image.NEAREST), ((i % 8) * cw * sc, (i // 8) * ch * sc))
    look.save(os.path.join(out, 'look.png'))

print('files: %d (%s)' % (len(items), ', '.join('%s %d fr x%d %s' % (os.path.basename(f['path']), f['frames'], f['native_scale'], f['background'])
        for f in res['files'])))
print('subject ~%dx%d px -> density %s' % (subj_h, res['subject_px']['width'], density))
print('colours %d (%d significant), saturation %.2f, brightness %.2f, %d tones per ramp' % (
    n_colours, len(sig), sat, val, tones_med))
print('outline: %s | dithering: %s | light from %s' % (outline, res['dithering'], ldir))
for a in anims:
    print('anim %s: %d frames, %d ms median (~%s fps), total %d ms, holds at %s, loops %s, ground drift %d px, effect frames %s' % (
        os.path.basename(a['path']), a['frames'], a['median_ms'], a['fps_equivalent'], a['total_ms'], a['holds'], a['loops'],
        a['ground_drift_px'], a['effect_frames']))
print('wrote', os.path.join(out, 'analysis.json'), 'palette.png', *(['look.png', 'native/'] if FRAMES else []))
