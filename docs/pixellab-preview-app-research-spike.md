# PixelLab Pip Preview App — Research Spike

Status: research complete, design pending approval. Companion: `plans/pixellab-preview-app-plan.md`.

Research/evidence doc (docs/ is user-facing, exempt from the runtime KISS/YAGNI rules). This
records *why* the preview app is designed the way the plan proposes, including the options that were
tested and rejected. Nothing here is a runtime routing rule; promote a finding into SKILL.md or a
reference only when it changes agent behavior.

## Problem

A user churned from Pip to Aseprite + the PixelLab web "creator" for one reason: they could not
**preview/play animations** before continuing, and burned many paid generations doing blind manual
review. Aseprite and the creator both give a play button (play/pause, loop, scrub, onion skin); the
agent chat panel gives nothing comparable.

This is **not a PixelLab-MCP defect**. It is a structural limit of every coding agent:

- **No agent chat panel reliably plays animation, and none has a play button.** Terminal agents
  (Claude Code) render no inline images at all. Webview agents (Cursor, Windsurf, Copilot Chat,
  Cline, Continue) render chat in a Chromium webview, so an animated GIF/APNG/WebP *may* animate —
  but it is undocumented, best-effort, frequently re-encoded to a frozen frame 0, and has a history
  of MCP image display bugs. Zed only recently added GIF animation. None support inline `<video>` /
  scrub controls.
- **MCP cannot deliver a playing animation.** MCP has TextContent, ImageContent, AudioContent, and
  EmbeddedResource — **no video/animation content type**. Clients may cap frame count/size, and the
  receiving model flattens any image to a **single static frame** regardless of format. The LLM
  never "sees" motion.
- **The only universally reliable animator is the web browser**, launched via `start` (Windows) /
  `open` (macOS) / `xdg-open` (Linux). OS default *image viewers* are inconsistent (Windows Photos
  freezes APNG/WebP; macOS Preview shows frames, not playback).

Conclusion that drives everything below: **stop trying to preview in chat.** Have the agent write a
preview to disk and open it in the user's browser as an automatic step. The browser is the play
button.

Sources: [MDN — image types](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types),
[caniuse APNG](https://caniuse.com/apng), [Cursor MCP docs](https://cursor.com/docs/mcp),
[Cursor image-in-chat bug](https://forum.cursor.com/t/image-not-displaying-in-chat-when-returned-from-mcp-server/103623),
[Claude Code inline-image issue #29254](https://github.com/anthropics/claude-code/issues/29254),
[MCP tools spec (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools),
[Zed 0.234.0 GIF support](https://zed.dev/releases/preview/0.234.0).

## Cruxes

### Crux 1 — `file://` loading reality (decides the architecture)

A double-clicked local HTML page (origin = opaque `null`) can load some things and not others:

| Mechanism | Chrome / Edge | Firefox | Safari |
| --- | --- | --- | --- |
| `fetch()` / XHR of sibling `.json` / `.png` | **BLOCKED** (opaque `null` origin; "Cross origin requests are only supported for protocol schemes: http, data, https…") | **BLOCKED** (deliberately broken in FF68 for CVE-2019-11730; WONTFIX) | Blocked/restricted |
| `<img src="relative.png">` | **WORKS** | **WORKS** | WORKS |
| `<script src="data.js">` global var | **WORKS** (the documented workaround) | **WORKS** | WORKS |

**Verdict:** `fetch()` of a local manifest is dead on arrival everywhere. But `<img>` and `<script>`
were never part of that restriction. So the app loads its **manifest via `<script src="data.js">`**
(a `window.PIP = {…}` global) and its **pixels via `<img>` / `new Image()` by relative path**. Never
`fetch()`.

Sources: [MDN — CORS request not HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp),
[Bugzilla 1566051 (FF file:// XHR WONTFIX)](https://bugzilla.mozilla.org/show_bug.cgi?id=1566051),
[Loading local files without a server](https://www.javaspring.net/blog/loading-local-files-with-javascript-without-a-web-server/).

### Crux 2 — canvas tainting does NOT break scrubbing (corrects the original plan)

A `file://` image drawn to canvas taints it. But tainting only blocks **pixel readback**
(`getImageData`, `toDataURL`, `toBlob` throw `SecurityError`). **`drawImage()` works fine on a
tainted canvas.** A previewer never needs readback:

- Sprite-sheet frame scrub = `drawImage(sheet, sx, sy, fw, fh, …)` per frame.
- Onion skin (if ever added) = two `drawImage` calls with `globalAlpha`.
- Pixel-perfect = `image-rendering: pixelated` + integer zoom (CSS).

`getImageData` is only needed for export, color-picking, or background removal — none of which a
previewer does. **Therefore we do NOT base64-inline the pixels to "avoid tainting" — that solves a
problem we do not have, at the cost of megabytes per run.** Inline only the small manifest; load
frames by relative path.

Sources: [MDN — CORS-enabled image / tainting](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image),
[Tainted canvas explained](https://corsfix.com/blog/tainted-canvas).

### Crux 3 — in-browser GIF frame decode: cut it

`ImageDecoder` (WebCodecs) can decode animated GIF, but it needs the GIF bytes as an `ArrayBuffer`
(→ `fetch`, blocked on `file://`) and is absent in Safari < 26 and older Firefox. Shipping a
decoder + Safari polyfill (gifuct-js) is a mountain of code for a format we do not need to scrub.

**Verdict:** PixelLab animation flows already emit `frame_000.png…`. Scrub those PNG frames. For a
bare GIF (no frame PNGs), either (a) display it in a native `<img>` (plays, no scrub) or (b) explode
it to PNG frames **at build time** with Pillow (already a dev dependency) so the unified frame model
still applies. Never decode GIF in the browser.

Sources: [MDN — ImageDecoder](https://developer.mozilla.org/en-US/docs/Web/API/ImageDecoder),
[WebCodecs browser support](https://www.testmuai.com/learning-hub/webcodecs-browser-support/).

### Crux 4 — distribution models

| Model | Zero-click | Offline | No runtime dep | Agent-agnostic | Verdict |
| --- | --- | --- | --- | --- | --- |
| **(a) static `preview.html` in skill + generated `data.js` + relative images** | ✅ (`start`/`open`/`xdg-open`) | ✅ | ✅ | ✅ (write files + 1 command) | **WINNER** |
| (b) static HTML that `fetch()`es a manifest | ❌ broken on file:// | — | — | — | Dead (Crux 1) |
| (c) GitHub Pages + File System Access API / drag-drop | ❌ needs clicks; FSA unsupported in FF & Safari | ❌ needs network | ✅ | ❌ | Rejected as primary |
| (d) local `python -m http.server` + open localhost | ⚠️ | ✅ | ❌ needs Python/Node | ⚠️ long-lived process | Over-built |

Model (d) is the only way to regain `fetch` + `getImageData`, but the previewer needs neither, and
it adds a backgrounded process, port collisions, a Windows Firewall prompt, and a LAN-exposure
footgun (`http.server` binds `0.0.0.0` by default). **Decision rule for the future:** spin a local
server only if a feature that needs `getImageData`/canvas export is added (in-browser bg-removal,
palette extraction). Until then, no server.

The **GitHub-hosting idea** (raised by the author) is rejected as the launch path: a hosted page
cannot read local generated files without drag-drop/File-System-Access clicks, FSA is permanently
unsupported in Firefox and Safari, and it needs a network. The local self-contained file already
gives shareability (zip the run folder — Pip already zips multi-file bundles). A hosted "drag your
folder here" variant is a possible *later* convenience for sharing with people who lack the repo,
not the primary mechanism.

Sources: [MDN — File System API (FSA unsupported FF/Safari)](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API),
[Python bug 39211 (http.server binds 0.0.0.0)](https://bugs.python.org/issue39211).

### Crux 5 — versioning

Ship `preview.html` **inside the skill** (offline, versioned atomically with the skill; no
`raw.githubusercontent`/Pages runtime dependency). Per run, the agent (or a helper) copies
`preview.html` into the run dir and writes `data.js` beside it. Because the same skill version
produces both, there is no skew. A single `schema` integer in `data.js` lets the player warn on a
stale run dir. That is the whole compatibility story.

## Prior art in the repo

`pixellab-pip-generations/model-benchmark-20260713/blind_review.standalone.html` is an existing
self-contained review page that **base64-inlines every image** (`data:image/png;base64,…`) and uses
a `cb` checkerboard class. It works from `file://` with no server — validating the self-contained-
HTML instinct. But it inlines *pixels*, which is why it is 250 KB+. Per Crux 2 we improve on it:
inline only the manifest, load pixels by relative path. Base64 single-file export is retained only as
a *later* option for single-file sharing.

## Blueprint reality (drives the detail panel)

A `*.blueprint.json` is an **array of steps** (or one step). Each step's executable key is
`MCP <tool>`, `POST /v2/<endpoint>`, or `TASK`, with the literal request body as its value, plus
`_comment` / `_comment_prompt` metadata. Fields vary by step: `seed` appears on REST steps
(`animate-with-text-v3`, `create-image-pixflux`) and is absent on `MCP create_character`. Verified
against real blueprints in `pixellab-pip-generations/` (some have `seed`, many do not).

**Therefore the detail panel renders blueprint fields generically** (prompt/`description`, the route
key, `size`, then remaining scalars as key/value) — it never hardcodes a fixed field list, and it
shows a "Open blueprint ↗" relative link rather than reimplementing a JSON tree viewer (the user's
own editor already opens the file). Blueprint geometry (`size`) is also the reliable source for
**sprite-sheet frame dimensions**, which raw pixels cannot convey.

Source: `skills/pixellab-pip/references/blueprint.md`; real blueprints under
`pixellab-pip-generations/`.

## Rejected / cut (with reason)

- **GitHub Pages hosting as the launch path** — can't read local files zero-click; FSA unsupported
  in FF/Safari; needs network. (Possible later drag-drop sharing variant only.)
- **Local HTTP server** — YAGNI; the previewer needs neither `fetch` nor `getImageData`; adds a
  process, port, firewall prompt, and LAN-exposure footgun.
- **`fetch()`-based loading** — broken on `file://` in all Chromium browsers and Firefox.
- **Base64-inlining the pixels** — unnecessary (Crux 2); relative `<img>` works and stays lean.
- **In-browser GIF decoder (ImageDecoder / gifuct-js)** — needs fetch + missing in Safari < 26; PNG
  frames + native `<img>` cover it.
- **In-app JSON/blueprint tree viewer** — the user's editor opens the file; link instead.
- **Onion skin (v1)** — an authoring aid, not a preview/pick need; even Aseprite disables it in its
  preview window. Cheap to add later if asked.
- **Ping-pong / per-frame timing editor / export / color tools / pan / fractional zoom** — that is
  an editor, not a previewer.
- **"Whatever else" arbitrary formats** — Pip only emits PNG and GIF; auto-handling unknown formats
  invites flaky heuristics.

## What "professional" means here (evidence)

For a pixel-art tool, "professional" is almost entirely *not betraying the pixels*: nearest-neighbor
`image-rendering: pixelated`, **integer-only** zoom (fractional zoom shimmers), checkerboard
transparency, dark neutral chrome that auto-hides during playback (PhotoSwipe pattern), zero layout
shift, and instant state-preserving asset switching (preload the folder; a source swap, not a
reload). A blur, a shimmer, a reflow, a reset-to-frame-0, or a wrong sheet slice with no fix reads as
a toy.

Sources: [MDN — Crisp pixel art look](https://developer.mozilla.org/en-US/docs/Games/Techniques/Crisp_pixel_art_look),
[MDN — image-rendering](https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering),
[Aseprite preview window](https://www.aseprite.org/docs/preview-window/),
[Aseprite onion-skinning](https://www.aseprite.org/docs/onion-skinning/),
[PhotoSwipe options](https://photoswipe.com/options/).
