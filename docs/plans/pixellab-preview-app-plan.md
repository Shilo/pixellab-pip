# PixelLab Pip Preview App — Plan

Status: design proposal, pending user approval. Companion: `../pixellab-preview-app-research-spike.md`
(the evidence and rejected options behind every decision here).

## Goal

Give the user the play button they lost when they left Aseprite/the creator: a **standalone,
browser-based, folder-scoped pixel-art lightbox** that the coding agent launches automatically. It
plays and scrubs animations, switches instantly between many assets from one generation, and surfaces
each asset's blueprint detail — offline, zero-click, in any browser, on any agent.

**It is not a universal media viewer.** Its input is one Pip output folder
(`pixellab-pip-generations/<run>/`), which the pipeline already produces. Every "should it handle X?"
question is answered by "is it in a Pip run folder?" — and Pip only emits PNG and GIF.

## Architecture (winner from the spike)

**One static `preview.html` shipped in the skill + a generated `data.js` per run + images loaded by
relative path + one OS open command.** No server, no hosting, no network, no `fetch`, no base64
pixels.

```
skills/pixellab-pip/assets/preview/
  preview.html          # the player — ships in the skill, versioned, ~1 file
  build_preview.py      # helper: scans a run dir, writes data.js, copies preview.html (optional path)

pixellab-pip-generations/<run>/         # per run, at launch time:
  preview.html          # copied from the skill
  data.js               # generated:  window.PIP = { schema, assets:[…] }
  frame_000.png …       # existing outputs, referenced by RELATIVE path
  walk-sheet.png
  name.gif
  name.blueprint.json
```

Launch sequence the agent performs:

1. Copy the skill's `preview.html` into the run dir.
2. Write `data.js` beside it (see schema below). Paths in it are **relative to the run dir**.
3. Open it: `start "" preview.html` (Windows) / `open preview.html` (macOS) /
   `xdg-open preview.html` (Linux).

`preview.html` has `<script src="data.js"></script>` then the player. Frames load via `new Image()`
by relative path; the canvas renders with `drawImage` only (tainting is irrelevant — spike Crux 2).

### `data.js` schema

```js
window.PIP = {
  schema: 1,
  run: "knight-run",
  assets: [
    {
      name: "walk south",
      type: "sheet",              // "static" | "frames" | "sheet" | "gif"
      src: "walk-south-sheet.png",// sheet/static/gif: one file
      frames: null,               // "frames" type: ["frame_000.png", …] in order
      frameW: 48, frameH: 48, count: 8,  // sheet geometry (from blueprint size; overridable)
      fps: 12,                    // default playback fps (frames/sheet); GIF ignores (native timing)
      blueprint: {                // flattened per-step scalars for the detail panel, rendered generically
        prompt: "a knight in shining silver armor, walking",
        route: "POST /v2/animate-with-text-v3",
        size: 48, seed: 231       // whatever scalars the step actually has; no fixed field list
      },
      blueprintFile: "knight-run.blueprint.json"  // relative link for "Open blueprint ↗"
    }
  ]
}
```

The agent can write `data.js` directly (it is just JSON in a `window.PIP =` wrapper), or run
`build_preview.py <run-dir>` to derive it from the folder's files, blueprints, and manifest. See
Open Decision 2.

### Asset types (exactly four; "whatever else" is cut)

| Type | Source | Playback |
| --- | --- | --- |
| `static` | one PNG | shown; no transport |
| `frames` | ordered PNG list (`frame_000.png…`) | **scrubbable** via unified player |
| `sheet` | one PNG + `frameW/frameH/count` | sliced with `drawImage`; **scrubbable** |
| `gif` | one GIF | native `<img>` autoplay; **not scrubbable** (spike Crux 3) |

A directional rotation set (e.g. 8 separate PNGs) is just a **group of `static` assets** in the
filmstrip — not a special mode.

To make scrubbing universal, an optional build-time step explodes a bare GIF into PNG frames with
Pillow so it becomes a `frames` asset. Only used when a GIF has no accompanying frame PNGs.

### Unified player model

On load, `frames` and `sheet` assets both normalize to **`frames[] + currentIndex`**. Play/pause,
timeline scrub, prev/next frame, frame counter, loop, and FPS then operate on that one structure, so
the two behave identically. `gif` and `static` bypass the frame model (native `<img>`).

Sheets default to 12 fps; a `frames` asset uses its manifest fps; both expose the same FPS override.

## UX

### Layout — a lightbox with transient chrome

Default state (chrome visible, info drawer closed):

```
┌──────────────────────────────────────────────────────────────┐
│  run: knight-run/                                        [i][⤢]│
├──────────────────────────────────────────────────────────────┤
│              ▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓                          │
│              ░▓░   ┌───────────┐   ░▓░                          │  CENTER STAGE
│              ▓░▓   │  SPRITE    │   ▓░▓   checkerboard bg       │  integer-scaled, crisp
│              ░▓░   └───────────┘   ░▓░                          │
│              ▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓                          │
│                          [▮__●______________]   4/8            │  frame ticks + counter
│                   ⏮ ◀ ▶⏸ ▶ ⏭   ↻loop  12fps  ⊞bg  🔍100%       │  transport (auto-hides)
├──────────────────────────────────────────────────────────────┤
│ ▣ south.gif │ □ walk-sheet │ □ idle │ □ north.png │ …          │  filmstrip (only if >1 asset)
└──────────────────────────────────────────────────────────────┘
```

Info drawer (`i`) slides over the right edge; the stage does **not** reflow. Fullscreen (`f`) hides
all chrome, revealed on mouse-move/keypress.

### Controls (ranked; below the line is cut for v1)

1. Play / pause (`Space`) — the entire reason the user churned
2. Timeline scrubber with frame ticks — the second reason
3. Prev / next frame (`←` / `→`) — "frame-by-frame" was explicitly requested
4. Frame counter (`3 / 8`)
5. Loop toggle
6. Integer zoom + fit (`+`/`-`/`0`)
7. Background toggle: checkerboard → dark solid → light solid
8. FPS control
   — cut line —
9. Onion skin — authoring aid; add later if asked
10. Ping-pong / per-frame timing / export / color tools — that's an editor

### Keyboard map (keyboard-first is most of "professional")

| Key | Action |
| --- | --- |
| `Space` | play / pause |
| `←` / `→` | prev / next frame (when paused) |
| `[` / `]` (or `Shift`+`←`/`→`) | prev / next **asset** |
| `Home` / `End` | first / last frame |
| `+` / `-` / `0` | zoom in / out (integer) / fit |
| `L` | loop |
| `B` | cycle background |
| `I` | info drawer |
| `F` | fullscreen |
| `Esc` | exit fullscreen / close drawer |

### Blueprint detail (tasteful minimum)

In the `i` drawer: prompt, route, size, then any remaining scalar fields rendered generically as
key/value (so `seed`, `view`, `mode` appear when present without special-casing — spike: blueprints
are per-step and field sets vary). Plus a relative `<a href="name.blueprint.json">Open blueprint ↗</a>`
that opens the raw recipe in the browser. No in-app JSON tree viewer.

### Style direction

Dark neutral chrome (near-black stage), one muted accent for the selected/active state, everything
else greyscale — the art is the only color. Nearest-neighbor `image-rendering: pixelated`,
**integer-only** zoom. Checkerboard transparency, toggle to solid. Zero layout shift (stage sized to
the largest asset; smaller ones center inside). Transient chrome that fades during playback and after
idle. No modals, no toasts, no onboarding — it opens showing pixels.

## The make-or-break flow

*Agent generates 4 candidate animations → user opens the app → plays all four → compares → picks
one.* The single thing that, if wrong, kills it: **asset switching must be instant and
state-preserving.** Guarantee it by:

1. Preloading/decoding the whole folder on open (no mid-comparison spinner).
2. A fixed stage box (no reflow switching between a 48px still and a 384px sheet).
3. A shared running clock (switching swaps the frame source but keeps play state and the clock, so
   the next candidate is already animating on arrival).
4. Frame-accurate scrub identical for `frames` and `sheet` (both are just `frames[]`).

If those hold, the churned user gets what Aseprite's preview gave them — without burning a blind
generation.

## Scope

**MVP (v1):**
- Reads one Pip run folder; filmstrip of its assets.
- Four asset types (static, frames, sheet-with-geometry-from-blueprint + manual count override, gif
  native).
- Unified `frames[]` player: play/pause, scrubber, prev/next, counter, loop, FPS.
- Integer zoom + fit; background toggle.
- Fullscreen lightbox with auto-hiding chrome; info drawer.
- Generic blueprint detail + "Open blueprint ↗" link.
- Keyboard-first nav; all assets preloaded for instant, state-preserving switching.
- Dark theme, crisp pixels, zero layout shift; `schema` version guard in `data.js`.

**Later (explicitly cut):** onion skin; in-app JSON viewer; local server; GitHub Pages / drag-drop /
FSA; base64 single-file export for sharing; ping-pong / timing editor / export / color tools;
"whatever else" formats; side-by-side multi-asset grid (fast keyboard switching covers "compare 4"
first — add a grid only if switching proves insufficient).

## Integrating into the skill

The app only helps if it fires **by itself**. Wire it into the flows that produce reviewable art:

- After an **animation** flow (`animation.md`) and after any **multi-candidate** flow, assembling
  and opening the preview becomes a default step — the same slot where `local-asset-assembly.md`
  currently builds a preview GIF. The GIF stays as the shareable/inline artifact; the app becomes the
  *playable review* surface.
- Document the launch contract (copy `preview.html`, write `data.js`, run the OS open command) in
  `local-asset-assembly.md`, with a one-line pointer from SKILL.md and `animation.md`.
- Respect existing globals: outputs go under `pixellab-pip-generations/<run>/`; the app never bakes a
  background into deliverables (checkerboard is a preview-only toggle); it displays PixelLab pixels
  and never repaints them.
- Auto-open honors the same "don't surprise the user with external actions" posture as the rest of
  the skill — see Open Decision 3.

## Build phases

1. **Player (`preview.html`)** — build against a hand-written `data.js` fixture pointing at an
   existing run folder (e.g. `astronaut-dusk-cliff-loop-20260712/`). Verify play/scrub/switch/zoom/bg
   and crisp integer pixels in Chrome, Firefox, and one WebKit browser, opened via `file://`.
2. **Generator (`build_preview.py`)** — scan a run dir, classify assets, read sheet geometry from
   blueprints, optionally explode a bare GIF to frames, emit `data.js`, copy `preview.html`. A tiny
   self-check (assert on a sample folder) per the repo's test norm.
3. **Wire-in** — update `local-asset-assembly.md` (+ pointers) with the launch contract; run
   `python dev-tools/qa.py`.

## Open decisions (need your call)

1. **Hosting** — recommend NO GitHub hosting for launch (can't read local files zero-click; FSA
   unsupported in FF/Safari; needs network). Local self-contained file is the mechanism; sharing =
   zip the folder. Agree, or do you still want a hosted drag-drop variant as a later add-on?
2. **Generator** — recommend shipping `build_preview.py` (matches `bark.py` / `background_removal.py`
   precedent; keeps per-run agent tokens low and sheet-geometry correct), with "agent writes
   `data.js` by hand" as the no-Python fallback. Or keep it pure-agent (no script) to avoid any
   Python dependency for preview?
3. **Auto-open default** — recommend the preview is assembled automatically after animation/
   multi-candidate flows and **opened automatically** (that's the whole point — the user shouldn't
   have to ask). Acceptable, or should opening be offered/confirmed rather than automatic?
4. **Onion skin** — recommend cut for v1 (add if requested). Keep cut?
