# PixelLab Pip Preview App — Research Spike

Status: research expanded with archived-cinematic replay tests; design pending approval. Companion:
`plans/pixellab-preview-app-plan.md`.

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

A current `*.blueprint.json` is usually an **array of steps** (or one step). Each step's executable
key is `MCP <tool>`, `POST /v2/<endpoint>`, or `TASK`, with the literal request body as its value,
plus `_comment` / `_comment_prompt` metadata. Fields vary by step: `seed` appears on some REST steps
and is absent on other routes. Archived runs are less uniform: `pip-cinematic.blueprint.json` is
one older object with a request template, not executable steps. The duel blueprint is an array, but
its twenty animation steps have **neither `size` nor `image_size`**; the six still/edit steps use
`image_size`, not `size`. Its sheet geometry cannot be derived from one animation-step field.

**Therefore the detail panel renders blueprint fields generically** (prompt/`description`, route,
available geometry, then remaining scalars) and links to the raw file rather than reimplementing a
JSON tree viewer. For playback, use an explicit frame manifest where present; otherwise inspect
companion frame PNG dimensions. A bare sheet still needs explicit frame geometry: neither its total
PNG size nor an arbitrary blueprint step reliably tells the player how to slice it. Do not guess.
The duel's one finished cut spans 26 paid steps, so attaching any one step's prompt to the whole
295-frame asset would be misleading. Show per-step details only when an asset has one clear source;
for a multi-step cut, label it as such and link the complete blueprint.
The old duel blueprint is also not a byte-for-byte record of the original PixFlux request: its
runner always sent `text_guidance_scale` (default 8.0 unless overridden), but the script that
later reconstructed the blueprint left that field out. The fresh replay follows the archived
blueprint as written, not an invented claim of identical original HTTP bodies. Future blueprints
should capture the body actually submitted, as the current blueprint contract already requires.

Source: `skills/pixellab-pip/references/blueprint.md`; real blueprints under
`pixellab-pip-generations/`.

## Cinematic tests — archived runs and live replays (2026-09-12–13)

The preview proposal must handle real Pip outputs, not only a tidy eight-frame walk cycle. This
round uses four deliberately different archives:

| Case | What it stresses | Archived evidence |
| --- | --- | --- |
| Pip virtual pet | Long transparent loop, chained handoffs, a separate locally repaired final cut | 37 animation jobs; 600-frame, 100 ms GIF; 128×128 PNG frames; old single-object blueprint |
| Brick-figure space duel | Opaque scene cuts, independent keyframes, speech bubbles, slow dramatic beats | 26 paid calls, 20 animation clips; 295-frame cut; 192×108; per-frame timing manifest |
| Astronaut at dusk | Short opaque loop with a transient star and explicit closing-frame anchor | One opening still plus three chained shots; 42-frame, 100 ms cut; 224×144 |
| Dusk hoverboard ride | Short anchored/free-run mix and rejected re-rolls left alongside accepted shots | Six accepted clips, 97-frame cut; 256×128; `rejected/` and inspection artifacts |

For the three live cases, the replay sends the archived request text, seeds, and dependency order to
the documented REST routes, but uses **new outputs as each next input**. It retains every raw PNG,
job identifier, exact executable request body, and returned generation-unit charge in a fresh local
run folder. The source archives are not overwritten. A pre-call balance guard reserves 100 units
below the user's 3,000-generation ceiling; charged POSTs are never blindly retried. The test checks
image count and dimensions, and compares each returned frame 0 (the service's echo of its starting
image) to the supplied handoff both bytewise and ignoring RGB values at fully transparent pixels.
No local pixel repair is applied to the replays.

This is a **generation and artifact-structure test**, not a browser acceptance test: the preview app
does not exist yet, and this environment's browser security policy blocks opening `file://` pages.
Browser playback smoothness, memory use, and cross-browser `file://` behavior therefore remain to
be measured when the app is built. Counts below are filesystem measurements, not browser telemetry.

### Archive measurements that change the design

- **Timing is not always one FPS.** The duel's 295-frame `frames_manifest.json` has ten distinct
  frame delays from 95 to 440 ms, totaling **57.41 seconds**. A uniform 12 fps would play it in
  **24.58 seconds** and erase the intended pauses. Its delivered GIF rounds 95/125 ms to 90/120 ms
  (GIF centisecond granularity), so that file actually plays for **56.76 seconds**. The preview
  should use recorded per-frame delays by default, or the GIF's extracted delays when matching the
  delivered GIF specifically. The FPS control may flatten them deliberately for inspection; it
  must not flatten them silently. This is playback fidelity, **not** a timing editor.
- **There is no global "drop frame 0" rule.** The duel keeps the returned first frame for seven
  fresh-keyframe cut openings, but drops it at thirteen continued handoffs. Dropping all twenty
  would lose opening poses; keeping all twenty would insert repeated frames. The accepted cut's
  explicit sequence is the reliable source of this choice.
- **A folder is not a candidate list.** The Pip archive has 1,861 PNGs: 600 finished frames, 589
  raw assembled frames, 629 job frames, 40 inspection images, and three root PNGs including two
  3,072×3,200 sheets. Decoding all of those simultaneously as RGBA would represent about **252 MB**
  of pixel buffers, versus **39 MB** for the 600 finished frames alone (before browser overhead).
  The duel likewise has 315 raw job PNGs, 295 numbered cut PNGs, and a sheet. The hoverboard folder
  also contains rejected attempts. A generic recursive scan would show duplicates and rejected
  work as if they were candidates. Use the accepted output manifest/sequence first; never preload
  every PNG just because it is present. These byte counts flag a risk, not measured browser memory.
- **A finished cut is not necessarily raw model output.** Pip's final 600-frame GIF includes speck
  cleanup, a composited ball repair, and a locally made loop-reset tween. Its 37 jobs produce at
  most 593 assembled frames when each echoed handoff is dropped. The preview must label the raw
  model sequence and the edited final cut distinctly; showing the finished GIF as if it were
  untouched PixelLab evidence would be misleading.
- **Timing and geometry metadata differ by archive.** The duel has an explicit ordered
  `frames_manifest.json`; Pip's older blueprint records 100 ms only in prose, but its GIF exposes
  that delay. None of the duel's 20 animation blueprint steps contains a `size` field, and Pip's
  blueprint has no structured size at all. Use manifest timing/order and companion frame dimensions
  where available. If only a sheet survives, require frame width, height, and count explicitly;
  do not infer them from the total sheet dimensions.

### Replay blueprints and observed results

These are the human-readable recipes; the **exact request bodies, seeds, new job IDs, and frame
paths** are in each replay's `blueprint.json` and `ledger.jsonl` under its local
`pixellab-pip-generations/preview-spike-*-replay-20260912/` folder. The files remain local because
generated art and account-specific job records are gitignored.

| Replay | Recipe | Assembly |
| --- | --- | --- |
| Pip | Original `pip_start_frame.png`; 37 chained `POST /v2/animate-with-text-v3` requests, 16 frames each, transparent, `enhance_prompt=false`, recorded actions and seeds. The earlier manifest has two attempts at job 13; this replay uses the later recorded prompt. Job 37 points `last_frame` to the opening echo. | Use the next job's recorded handoff to choose each prior clip's last kept frame (job 5 stops at frame 13; job 15 at 15). Keep every raw endpoint frame separately; omit continuation frame-0 echoes from this diagnostic cut as the archived cut did, while recording visible mismatches. Play at 100 ms/frame. |
| Space duel | One `create-image-pixflux` master at 192×108; four `generate-image-v2` keyframes with the new master as reference and style, one `edit-image` keyframe, and 20 `animate-with-text-v3` clips with the archived seed and actions. Every dependent input comes from this new replay, not the old finished movie. | Use the original explicit 295-entry frame manifest for shot order and per-frame delays. Keep cut frames, keyframes, raw job frames, and GIF as different roles. |
| Astronaut | One unseeded `create-image-pixflux` opening at 224×144, then three chained 14-frame `animate-with-text-v3` jobs with seeds 221, 231, and 251. The final job targets the opening image. | Opening plus 14 + 14 + 13 frames; omit duplicate frame-0 echoes and the exact closing anchor; 100 ms/frame. |

The fresh **Pip** run completed all 37 calls for **148 reported generation units**. It produced 629
raw returned PNGs and a 589-frame, 58.9-second diagnostic cut. Every decoded GIF frame matches its
source PNG, including transparency. Of the 37 returned frame-0 echoes, six were pixel-exact, three
differed only in invisible transparent RGB, and **28 changed visible pixels** (usually a few; four
changed more than 50). Thus a viewer or stitcher must not assume every echo is a safe duplicate.

The diagnostic cut also makes two story/loop failures clear. In sampled catch and hold frames
(`j12_f16.png` and `j16_f16.png`), the requested separate red ball is not visibly present. Job 5's
frame 13 still has the ball, but its last three frames lose it; the recorded frame-13 handoff avoids
that loss. The final returned frame visually equals the opening, yet the dog immediately before it
is much larger. That return changes **3,706 visible pixels**, versus a median **1,044** between
neighboring frames in this cut; the wrap itself changes zero. Endpoint equality proves closure of
the last *image*, not a smooth approach to it. The earlier 600-frame final had local ball repair and
a reset tween; this raw replay deliberately does not.

The fresh **astronaut** run completed its four calls for **22 reported generation units**. It has
42 cut frames, 4.2 seconds, three pixel-exact frame-0 echoes, and a pixel-exact final anchor. Its
new GIF also matches all 42 source PNGs. Yet the moon is bright in the last displayed frame and
pink at the opening: the visible wrap changes **9,207 pixels**, versus a median **2,940** per
neighboring-frame step. The user-requested astronaut-at-left composition also came back on the
right. A playable preview and prompt detail would make both issues easy to spot; an endpoint check
and a frame count do not.

The duel replay exposed two job-lifecycle wrinkles before its cut was assembled. Its sixth
request (the close-up speech-bubble keyframe) returned a generic PixelLab policy failure and no
reported charge; one **unchanged** restart, requested by the user, succeeded. The reason the first
attempt was rejected is not known, so the result is not evidence that a particular word or image
was prohibited. Later, a local test helper treated an image field as a finished PNG before the
edit job reported `completed`; that field was not a PNG. Fetching the **same completed job ID**
recovered its final PNG (`quantized_image`) without another paid POST. The existing job-lifecycle
rule to wait for completion and re-poll rather than resubmit an uncertain job is necessary here; no
new runtime rule is needed.

The fresh **space-duel** run then completed all 26 intended calls for **190 reported generation
units**. It saved 314 final raw PNG outputs and assembled the intended 295-frame cut from the
recorded shot order. All 295 decoded GIF frames match their source PNGs exactly. The manifest's
delays total 57.41 seconds; the new GIF, like the archived one, plays for 56.76 seconds after GIF
rounding. Nineteen of its twenty animation frame-0 echoes were pixel-exact. The exception is the
edited still used as a *new scene cut*: its returned opening differs at 11,404 opaque pixels, yet
the average channel shift across the image is under 1 on a 0–255 scale and the scene looks nearly
the same. A large raw difference count alone would overstate this as a severe seam, and this is not
even a continuation seam. The inspected speech bubbles also vary from their exact requested
punctuation ("ME FATHER" gains a period; "NOOOOOO!" loses its exclamation), despite otherwise
recognizable scene and characters. Prompt text needs visual inspection at pixel-art zoom.

Across all three fresh replays, the accepted calls used **360 generation units total**, leaving
**2,640 units unspent** from the user's 3,000-unit test ceiling. This includes the successful
unchanged retry but no charged replacement for the failed edit *save* (the original edit job was
recovered). The Pip opening clip's last frame differs from the archived one at 195 displayed pixels
under the recorded seed, prompt, and starting image. That shows these blueprints do not promise
byte-identical historical output; this one replay cannot separate sampling variation from service
or model changes, or from archived request fields that were not preserved. The old duel blueprint's
omitted guidance field makes that warning concrete.
Across the three assembled cuts, every tested spritesheet slice also matches its corresponding
numbered PNG exactly. The PNG frames are the authoritative pixels; GIF and sheet are verified
viewing/packaging formats, with GIF timing rounding noted above.

**Smallest design correction:** keep the four proposed asset types and the no-server local player.
Add only an optional per-frame delay list, accepted-cut selection, verified sheet geometry, clear
raw-versus-edited labels, and an honest multi-step blueprint link. Do not add an editor, video
pipeline, automatic prompt scoring, or browser GIF decoder. The still-unverified browser play/scrub
test remains a build-phase gate, not a result of this spike.

The [PixelLab REST OpenAPI](https://api.pixellab.ai/v2/openapi.json) documents the asynchronous
generation routes and job polling used by the replays. The local archive names above are under
`pixellab-pip-generations/`; their generated outputs are gitignored, while this research record is
committed.

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
shift, and state-preserving asset switching. Preload only **reviewable candidates**, not every raw
job frame and duplicate export in the folder; long sequences still need a measured browser-memory
test before "instant" can be promised. A blur, a shimmer, a reflow, a reset-to-frame-0, or a wrong
sheet slice with no fix reads as a toy.

Sources: [MDN — Crisp pixel art look](https://developer.mozilla.org/en-US/docs/Games/Techniques/Crisp_pixel_art_look),
[MDN — image-rendering](https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering),
[Aseprite preview window](https://www.aseprite.org/docs/preview-window/),
[Aseprite onion-skinning](https://www.aseprite.org/docs/onion-skinning/),
[PhotoSwipe options](https://photoswipe.com/options/).
