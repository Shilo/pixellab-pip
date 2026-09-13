# PixelLab PixMiniMax (MiniMax H3) vs v3 Animation Spike

Last reviewed: 2026-09-12.

Status: completed. This spike records the refreshed public contract, a source-backed MiniMax H3 prompt adaptation, website and Aseprite research, and a paired live comparison against PixelLab's v3 raw animation route. The planned fixed-seed control was not achieved because every executed request sent `seed=0`, which PixelLab documents as random.

## PixMiniMax pros and cons

These are the practical tradeoffs supported by PixelLab's public documentation and this comparison. The observed quality differences come from a limited set of test images, so they are useful guidance rather than a promise about every animation.

### Pros

- **Longer animations in one job.** PixMiniMax can generate up to 40 new frames, while v3 stops at 16. This gives a multi-step action more room to develop without joining several shorter clips.
- **Clearer multi-step actions in this test.** The PixMiniMax sword and bow animations showed more distinct wind-up, action, and recovery stages. The 40-frame fireplace also remained coherent across a much longer sequence than v3 can produce in one job.
- **Full frame range at the maximum canvas size.** It accepts up to 40 generated frames on images as large as 256×256. V3 reduces its allowed frame count as the image gets larger.
- **Works directly from an image.** It can animate a supplied image, with an optional ending image. The image does not need to belong to a saved PixelLab character or object.
- **Useful motion controls.** Optional prompt enhancement can expand a short instruction, direction guidance can be used with that enhancement, and the REST API includes a control for reducing color flicker.
- **Reliable output handling in the completed tests.** Every completed job kept the requested canvas size and transparency, and the larger robot and fireplace tests returned the starting image exactly.

### Cons

- **It cost more than v3 in the matched short tests.** For the tested 4-, 8-, and 16-frame robot clips, PixMiniMax used 2, 3, and 5 subscription generation units; v3 used 1, 2, and 4.
- **It followed supplied ending images less closely in this test.** PixMiniMax did not exactly reach either distinct ending pose, while v3 reached the same tested endings exactly. A required final pose must therefore be checked carefully.
- **Its stronger motion can become unwanted decoration.** The sword test produced a larger, brighter slash effect. That can make an attack easier to read, but it can also add visual effects the user did not want.
- **The starting image is not guaranteed to remain untouched.** PixMiniMax returned exact starting images for the larger robot and fireplace, but materially changed the tiny flame's first returned image.
- **Frame-count choices are less flexible.** PixMiniMax accepts only multiples of four. V3 accepts any even frame count from 4 through 16.
- **It is beta.** PixelLab says a job typically takes 1–5 minutes.
- **PixelLab exposes only part of MiniMax H3.** The PixMiniMax wrapper does not expose H3's standalone audio, shot-list, camera, or advanced reference controls.

### What remains uncertain

- The comparison used one robot, one tiny flame, and one fireplace. It does not establish a universal quality ranking.
- Repeatability with a fixed seed was not tested. Every request used `seed=0`, which asks for a random result.
- The run did not cleanly test direction control, so the results do not show how much that option changes an animation.
- Several planned image sizes were unavailable, so the run does not provide a complete cost comparison across canvas sizes.

## Executive answer

PixMiniMax is a real new public PixelLab animation family, not just a renamed v3 option. The REST route is POST /v2/animate-pixminimax and the hosted MCP tool is animate_image_pixminimax. PixelLab's public REST description says that the route is powered by MiniMax H3. It accepts up to 40 generated frames in multiples of four on a canvas up to 256×256, while v3 accepts 4–16 even frames and has a separate total-pixel budget.

In the qualitative review, PixMiniMax looked stronger on longer clips and actions with several distinct stages. Its sword, bow, and 40-frame fireplace runs read as coherent multi-stage motion, and it held the exact first frame on the 128×128 robot and 256×256 fireplace inputs. It also introduced stronger effect accents in the sword case and did not reproduce a supplied distinct last frame exactly in the tested PixMiniMax cases. V3 was cheaper on the same fixtures, reached several distinct supplied end anchors exactly, and produced more restrained action effects, but its 16-frame ceiling prevented a matching 40-frame stress test and some actions were less decisive. Treat these as directional single-sample comparisons because seed was uncontrolled.

This run did not test fixed-seed determinism: its repeated requests used `seed=0` (random). Those random-seed samples were not identical, but they cannot establish fixed-seed reproducibility or identify the cause of every difference. Neither route should be treated as automatically pixel-preserving: v3 changed transparent RGB values in the echoed robot frame, while PixMiniMax materially changed the echoed tiny flame frame. Verify the actual returned frames before treating the first result as an untouched input or before building a loop.

## Public contract delta

The docs-watch refresh compared the complete current REST OpenAPI, REST LLM index, and MCP tool guide. The public inventory changed as follows:

| Surface | Before | After | Change |
|---|---:|---:|---|
| REST v2 paths | 85 | 86 | Added POST /animate-pixminimax |
| REST schemas | 244 | 246 | Added AnimatePixminimaxRequest and AnimatePixminimaxResponse |
| Hosted MCP tools | 99 | 100 | Added animate_image_pixminimax |
| Removals | — | — | None |

The existing REST animation enhancer also changed: EnhanceAnimationV3PromptRequest now supports engine=v3 or engine=pixminimax, plus optional direction and frame_count fields. Website docs and the MCP page HTML changed at the same refresh, but their raw build churn did not reveal another public route or schema change.

### REST

POST /v2/animate-pixminimax is a beta route. It uses the public bearer-token contract and returns HTTP 200 with a background_job_id. Poll GET /v2/background-jobs/{job_id}; the completed result is in last_response.images.

The request shape is:

| Field | Public behavior |
|---|---|
| first_frame | Required PNG Base64Image, maximum 256×256 |
| last_frame | Optional PNG Base64Image, same-size end anchor |
| description | Required 1–1000-character motion description; describe motion, not appearance |
| frame_count | Default 8; endpoint prose says 4–40 generated frames in multiples of four |
| seed | Optional non-negative integer; zero means random |
| no_background | Default true; removes an opaque input backdrop when enabled |
| drift_threshold | Optional de-flicker threshold; zero applies correction every frame, higher values correct only larger color drift |
| enhance_prompt | Optional inline PixMiniMax prompt expansion; the public docs price it at about 0.05 generations |
| direction | Optional south/north/east/west and four diagonal values; valid with enhance_prompt and used as facing/attack guidance |

The completed response includes background_job_id, status, optional enhanced_prompt and enhance_usage, and usage when exposed. The public description says the result contains frame_count + 1 images: index 0 is the input frame and the following images are the generated frames. This is a contract to verify, not a reason to skip pixel and visual checks.

The public REST description describes cost by generation time and gives examples: 32×32 at 4 frames costs 1 generation; 64×64 at 4, 8, 16, and 40 frames costs 2, 3, 5, and 12 generations; 80×80 at 8 frames costs 2. The website API page shows separate estimated USD values, including 64×64 at 4 frames for $0.0123, 64×64 at 8 for $0.0153, and 256×256 at 40 for $0.0471. These are not a documented conversion. For a real call, use response usage.generations; do not infer charged usage from image count or from the website USD estimate.

### MCP

The new hosted MCP tool is animate_image_pixminimax. It is a raw-image tool and does not require a managed character or object. Supply exactly one required first-frame input (`first_frame_url` preferred, or `first_frame_base64`); `last_frame_url` or `last_frame_base64` is an optional end anchor, also one alternative. Its public description matches the route's core behavior: motion description, 4–40 frames in multiples of four, maximum 256×256, optional end frame, optional seed, optional no-background control, and optional prompt enhancement/direction guidance. MCP does not expose REST's drift_threshold; it does expose enhance_prompt and direction in its own tool schema. MCP tool names are called through MCP and must not be treated as REST paths.

The corresponding public parity is:

| REST | MCP | Parity |
|---|---|---|
| POST /animate-pixminimax | animate_image_pixminimax | Core animation workflow parity; REST additionally exposes drift_threshold |
| POST /animate-with-text-v3 | animate_image | Full functional parity for the shared raw workflow; each surface has route-specific controls |

MCP does not expose REST's drift_threshold field on the new tool. On an MCP-first request, use the tool's enhance_prompt/direction controls when appropriate, or perform prompt improvement as the agent; preserve the user's wording when they explicitly provide it.

### Boundary decisions

The REST description mentions the semantics of a cost helper associated with the operation. That unversioned/private cost route is not in the public REST v2 path inventory and is not documented here as an endpoint. The installed Aseprite extension uses a private editor transport as well. Both are evidence about first-party behavior only; Pip routes code and automation through public REST v2 or MCP.

## MiniMax H3 research and PixelLab adaptation

### What the official H3 material says

MiniMax's official H3 announcement describes a general omni-modal model that can take text, image, video, and audio inputs and produce video with native stereo audio. The open-source announcement describes 4–15 second output, 24 fps video, 32 kHz stereo audio, multiple image-input modes, and separate base/regeneration resolutions. The official repository publishes prompt-writing guidance for T2VA, I2VA, FL2VA, L2VA, and reference-driven modes.

The official prompt skill is timeline-oriented. It asks the writer to establish the initial state, describe observable changes in time order, and resolve the transition toward the target state. Its base guide gives separate patterns for a first-frame anchor, first/last-frame interpolation, and last-frame convergence. It also defines structured multimodal description, soundscape, non-diegetic music, camera motion, shots, and reference labels.

Those official capabilities are important context, but they are not all PixelLab fields. PixelLab's PixMiniMax wrapper exposes one motion description, first/end pixel frames, frame controls, optional direction, background handling, de-flicker, and prompt enhancement. It does not expose H3 audio fields, shot lists, camera fields, reference-label blocks, or the full multimodal prompt schema. Sending those fields as prose would add noise rather than unlock hidden controls.

### What transfers to PixMiniMax

| H3 principle | PixelLab adaptation |
|---|---|
| Establish the initial state | Say what starts moving and explicitly say “start moving on the first frame” for a first-frame animation |
| Describe a timeline | Use a short ordered sequence of visible phases: raise, aim, release, recover |
| Converge toward an end state | Supply a genuinely distinct last_frame for a target pose and describe the transition |
| Use camera and scene controls | Only use them if they are actual PixelLab fields; do not put unsupported H3 shot/audio schema into description |
| Stable reference identity | State the sprite's identity, palette, outline, scale, placement, transparency, and stationary parts positively |
| Resolve ambiguous motion | Use an explicit facing direction and enhance_prompt when the public route supports it; otherwise clarify in the agent-authored description |

### Prompt recipe

For PixelLab's wrapper, the useful structure is:

> Start [subject] moving on the first frame. [Ordered phase 1], then [phase 2], then [result]. Keep the subject in place; preserve [identity anchors].

For a walk:

> A natural 8-frame walk cycle facing south toward the viewer. Start moving on the first frame; alternate arms and legs with clear contact and passing poses, a relaxed weight shift, and a subtle torso bob. Keep the character in place; preserve the helmet, blue armor, yellow accents, outline, scale, palette, and transparent background.

For a discrete action:

> Start the character moving on the first frame. Raise the sword overhead, strike once with a clear downward arc, then recover to the starting stance, facing south and staying in place. Preserve the character's silhouette, palette, outline, scale, and transparent background.

For an effect:

> Start the fire moving on the first frame. Animate an irregular flame in place: tongues rise, curl, split, merge, contract, and swell with varied timing. Keep the stone hearth and ember base stationary; preserve the pixel-art scale, palette, placement, and transparency.

Use enhance_prompt when the user's short motion wording is ambiguous enough to benefit from expansion and the extra charge is accepted. Use direction only with enhancement. Enhancement is not a replacement for a clear first-frame phase order. For a precise request, preserve the user's exact field value rather than silently rewriting it. MCP exposes `enhance_prompt` and `direction`; REST additionally exposes `drift_threshold`.

Avoid appearance-only prompts such as “a robot” in the animation description. Avoid vague cinematic language when the task is a sprite clip. Avoid unsupported H3 audio instructions, shot labels, reference tags, or camera blocks. One coherent action with ordered visible phases is a better wrapper input than a long list of simultaneous concepts.

## Website and Aseprite research

### PixelLab website

The current [PixelLab API page](https://www.pixellab.ai/pixellab-api) exposes PixMiniMax as “Animate with text (PixMiniMax)” and identifies the operation as POST /v2/animate-pixminimax. The page agrees with the REST contract on beta gating, first/end frames, the 256×256 cap, four-frame increments, the 40-frame maximum, optional enhancement, and H3 disclosure. Its USD estimates were independently observed on 2026-09-12 and recorded in the dated [website pricing observation](pixellab-pixminimax-website-pricing-observation-2026-09-12.md); they are separate from REST generation-unit examples and are not a billing conversion.

The current [PixelLab REST OpenAPI](https://api.pixellab.ai/v2/openapi.json), [REST LLM index](https://api.pixellab.ai/v2/llms.txt), and [MCP guide](https://api.pixellab.ai/mcp/docs) are the public schema and inventory sources. The human [PixelLab docs](https://www.pixellab.ai/docs) and [MCP setup page](https://www.pixellab.ai/mcp) were also refreshed; their raw HTML changed, but the meaningful new API contract came from the REST/MCP documents above.

### Aseprite extension observations

The installed first-party Aseprite extension now exposes PixMiniMax-labeled animation and interpolation dialogs. Source inspection covered the extension's implementation and package registration. The editor behavior is consistent with the public shape: a motion description, 256px maximum dimension, four-frame control increments, a 40-frame ceiling, optional start/end frames for interpolation, and a returned reference frame alongside generated frames. The editor prepares the returned frame sequence so the reference frame is not treated as a newly generated motion frame in the displayed animation.

The extension also exposes prompt-enhancement UI for the PixMiniMax model and stores its editor settings locally. Its operation identifiers, implementation filenames, and transport URLs are private editor details. They were used only to understand labels, frame handling, and UI behavior; they are not included as Pip endpoints.

### Official Aseprite model

The official [Aseprite animation guide](https://github.com/aseprite/docs/blob/main/animation.md) treats animation as a timeline of frames, layers, and cels, with controls for copying, moving, removing, reusing, tagging, and previewing frames. The [sprite guide](https://github.com/aseprite/docs/blob/main/sprite.md) defines frame duration and the layer/frame intersection as a cel. This matters to PixMiniMax output handling: returned PNG frames should be imported in order, and timing/tag decisions belong to the Aseprite document rather than being guessed from a contact sheet.

The official [exporting guide](https://www.aseprite.org/docs/exporting) documents GIF and PNG-sequence export, frame selection, and resizing. The official [CLI guide](https://github.com/aseprite/docs/blob/main/cli.md) documents sheet/data export, frame ranges, tags, trimming, and save-as operations. The [Lua Frame API](https://www.aseprite.org/api/frame), [Lua Sprite API](https://www.aseprite.org/api/sprite), [Lua Layer API](https://www.aseprite.org/api/layer), and [ExportSpriteSheet command](https://github.com/aseprite/api/blob/main/api/command/ExportSpriteSheet.md) provide the programmatic terminology used by the editor workflow.

The official [Aseprite source repository](https://github.com/aseprite/aseprite) corroborates the document model: sprite creation initializes a first frame and frame duration, cels are associated with a layer/frame pair, and the new-frame command supports empty, duplicate, copy, and linked-frame behavior. The official [sprite-sheet export implementation](https://raw.githubusercontent.com/aseprite/aseprite/main/src/app/commands/cmd_export_sprite_sheet.cpp) selects frames and layers for export rather than inventing a new animation timeline. This source research informs import/export and verification guidance only; it does not turn private PixelLab editor operations into public API.

## Paired comparison

### Protocol

The [test plan](../plans/pixellab-pixminimax-vs-v3-animation-test-plan.md) was written before the first paid generation. It fixed a public-only route set, reused existing source frames, defined A–D cases, set the 3,000-generation hard ceiling, and required a per-call ledger. The runner sent `seed=0` on every request even though the plan called for a fixed seed; because the public schemas define zero as random, route, input, prompt, frame count, and background handling were paired but seed was not controlled. The run used only:

- POST /v2/animate-with-text-v3
- POST /v2/animate-pixminimax
- GET /v2/background-jobs/{job_id}

The runner persisted request metadata, job IDs, polling responses, raw returned frames, contact sheets, GIF previews, per-call verification, and usage. A transient poll connection reset was recovered by polling the accepted job ID; no paid create request was resubmitted. The PixMiniMax robot payloads also sent `direction=south` when enhancement was disabled, although the public schema says direction is used only with enhancement. The server accepted those requests, but they do not isolate a direction effect; no conclusion below depends on one. The planned 0–4 visual scorecard was not completed, so the findings combine objective frame measurements with qualitative visual review; no case-level or mean scores were calculated.

Fixtures were exact existing source files: a 128×128 south-facing robot, a 16×32 flame/fireplace effect, and a 256×256 fireplace. No new art or local resize was used. The planned 32×32, 64×64, and 80×80 robot cases were not run because no exact-size source existed. The 256×256/40-frame case was run once on PixMiniMax because v3's public maximum is 16 frames.

The run root is [the ignored evidence folder](../../pixellab-pip-generations/pixminimax-vs-v3-animation-20260912/). The [run ledger](../../pixellab-pip-generations/pixminimax-vs-v3-animation-20260912/ledger.json) is the usage authority and the [run manifest](../../pixellab-pip-generations/pixminimax-vs-v3-animation-20260912/run-manifest.json) records the sanitized flow metadata.

### Budget and completion

| Group | Paid calls | Provider-reported generations | Conservative bound |
|---|---:|---:|---:|
| A common baselines | 12 | 24.1 | 134.1 |
| B motion families | 16 | 48 | 188.0 |
| C endpoint/drift/scale | 11 | 37 | 126.0 |
| D repeats/failure checks | 10 | 19 | 111.0 |
| Total | 49 | 128.1 | 559.1 |

All 49 paid jobs completed and reported usage. The total combines 128 base generation units with 0.1 enhancement units from A6. The two D4 validation requests were rejected with HTTP 422 before a job was accepted; they did not consume generation units. The measured total was 128.1 generations and the conservative bound was 559.1, below the 3,000-unit ceiling.

### Contract and integrity results

| Check | PixMiniMax | v3 |
|---|---|---|
| 8 requested generated frames | 9 returned images in every tested 8-frame job | 9 returned images in every tested 8-frame job |
| 16 requested generated frames | 17 returned images | 17 returned images |
| 40 requested generated frames | 41 returned images | Not legal on the public route |
| Canvas dimensions | Consistent in every completed job | Consistent in every completed job |
| Transparency | Preserved on tested transparent inputs | Preserved on tested transparent inputs |
| First-frame echo | Exact on robot and 256×256 fireplace; tiny flame differed by 293 pixels | Robot raw RGBA differed by 14,095 pixels with very small channel changes; tiny flame differed by about 311 pixels |
| Random-seed repeats (`seed=0`) | Two repeated robot and flame runs were not pixel-identical; fixed-seed behavior untested | Two repeated robot and flame runs were not pixel-identical; fixed-seed behavior untested |

The v3 robot echo difference was largely transparent-RGB normalization rather than a visible redesign. The PixMiniMax tiny-flame difference was a material first-frame change for that small input. The public “unchanged first frame” convention therefore needs output verification on both routes, especially for very small effects.

### Case findings

| Cases | Finding |
|---|---|
| A1 baseline walk | PixMiniMax held the robot's first frame exactly and produced a steadier, smoother-looking walk. V3 produced a coherent walk but normalized the echoed robot RGBA. |
| A2 distinct start/end | V3 reached the supplied end frame exactly. PixMiniMax held the start exactly but ended 15,157 differing pixels from the supplied last frame. |
| A3/A4 tiny flame | Both routes animated the tiny flame despite the small canvas. PixMiniMax changed the first frame by 293 pixels; v3 changed it by about 311. Matching end anchors did not eliminate middle-frame verification. |
| A5/A6 short prompt | Without enhancement, PixMiniMax kept the robot first frame exact; with enhancement it returned a phase-rich expanded prompt. V3's enhancement also expanded the action but in more generic terms. |
| B1–B3 idle/walk/run | Both routes produced legal and distinct frame sequences. PixMiniMax used 2/3/5 reported generations for 4/8/16 frames; v3 used 1/2/4. |
| B4 sword | PixMiniMax made the attack phase and green slash effect more decisive; v3 was more restrained with a lighter slash effect. The extra PixMiniMax effect is a quality tradeoff, not an unconditional win. |
| B5 bow | PixMiniMax showed a clearer draw → aim → release sequence across 16 frames. V3 was more gradual and less consistent about the discrete release. |
| B6 jump | Both produced readable in-place vertical motion. |
| B7 coin spin | Both produced 17 unique frames and a usable rigid-object turn. |
| B8 16-frame flame | Both produced distinct flame motion. PixMiniMax had larger temporal changes and a more expressive sequence; v3 was calmer on the tiny effect. |
| C1 distinct anchors, 4 frames | V3 reached the supplied end exactly; PixMiniMax did not, with 15,471 differing pixels. Both produced a readable short transition. |
| C2 same anchor, 16 frames | PixMiniMax's final frame differed from the matching anchor in 956 visible pixels. V3 had 14,095 raw RGBA differences, but every change was an invisible RGB value inside a fully transparent pixel; its visible pixels and transparency matched the anchor exactly. Visually, v3 closed the loop exactly and PixMiniMax did not. This deviated from the planned distinct-anchor case, and the fixed prompt still said “8-frame” while requesting 16 generated frames, so treat it only as evidence for this executed sample, not a general endpoint guarantee. |
| C3/C4 drift threshold | Both routes completed both settings. With the default/omitted threshold, v3 averaged 103.2 changed pixels per adjacent-frame comparison (max 129; same-anchor endpoint diff 311), while PixMiniMax averaged 120.4 (max 204; endpoint diff 476). With `drift_threshold=0`, v3 averaged 112.0 (max 128; endpoint diff 311), while PixMiniMax averaged 108.6 (max 124; endpoint diff 323). Each produced 9 unique images; zero did not clearly improve endpoint integrity or establish a flicker winner on this tiny flame, so use the control when drift is observed and verify visually. |
| C8 128×128/16 | PixMiniMax completed the longer clip at 5 reported generations and v3 completed it at 4. |
| C9 256×256/40 | PixMiniMax completed the maximum legal clip at 12 reported generations and returned 41 unique frames. This was a successful stress result; no v3 comparison was legal. |
| D1/D2 anchored repeats | The requests used `seed=0`, which means random. The repeated previews were not identical but showed the same broad motion family. These are random-seed samples and cannot establish fixed-seed reproducibility. |
| D3 last frame without enhancement | PixMiniMax completed the end-frame path without enhancement but did not reach the distinct end exactly; v3 reached the tested end exactly. |
| D4 validation | Missing first_frame was rejected with HTTP 422 on both routes without an accepted job. |

### Qualitative conclusion

The strongest PixMiniMax advantage in this sample is temporal planning for a multi-phase action and a longer sequence. It is the better first candidate when the user explicitly asks for PixMiniMax/H3, wants 16–40 generated frames, or needs a richer raise/aim/release/impact sequence. It should be inspected for stronger effect accents and endpoint fidelity.

The strongest v3 advantages are lower reported usage on matched short runs, a smaller established frame budget, and exact distinct end anchors in several tested cases. It remains the default v3 route when PixMiniMax is not requested, when a restrained short clip is sufficient, or when the user values the tested end-anchor behavior more than long-clip capacity. This is not a universal model ranking: the study used one robot, one tiny flame, one fireplace stress fixture, one main motion prompt family, and a finite random-seed sample.

### Follow-up: v3 cinematic replays (2026-09-12–13)

A later [preview-app research spike](../pixellab-preview-app-research-spike.md) replayed three archived cinematic recipes with fresh PixelLab jobs. These were **v3 animation checks, not new PixMiniMax-vs-v3 pairs**, so they refine the verification caveats but do not change the model ranking above. The three replays used 360 reported generation units in total, including still-image routes; that total is not a v3 animation price comparison.

| Replay | What the returned frames showed |
|---|---|
| Pip, 37 chained v3 clips | Six first-frame echoes were exact, three differed only in invisible RGB under full transparency, and 28 changed visible pixels. The final frame visually matched the opening, but the dog was much larger immediately before that return; the requested red ball was also absent in sampled catch/hold frames. |
| Space duel, 20 v3 clips plus still-image jobs | Nineteen first-frame echoes were exact. The other was a new scene cut from an edited still: 11,404 opaque pixels changed by a very small amount on average, so the raw count alone overstated the visible effect. Requested speech-bubble punctuation also drifted. |
| Astronaut, three chained v3 clips plus an opening still | All first-frame echoes and the final anchor were pixel-exact. The assembled cut omitted that closing anchor, however, and its bright-moon-to-pink-moon wrap still had an obvious visual jump. |

These replays show why the C2 visually exact v3 endpoint is a **case result**, not a guarantee for every clip or assembled loop. Inspect the displayed cut around handoffs and the wrap, along with the raw endpoint images; an exact anchor can coexist with an abrupt approach or a visible cut. The replay's request blueprints, per-job ledger, and frame checks are documented in the linked preview-app spike.

## Routing and verification recommendations

1. Route an explicit PixMiniMax, PixMiniMax/H3, or MiniMax H3 request to REST POST /v2/animate-pixminimax or MCP animate_image_pixminimax. Route an unspecified raw animation request to the existing v3 family.
2. For PixMiniMax prompts, start the action on frame 1, order visible phases, say “in place” for locomotion, preserve identity anchors positively, and keep the field motion-only. Use enhancement for short ambiguous wording when the approximately 0.05-generation surcharge is acceptable.
3. Use direction only with PixMiniMax enhancement. Do not copy MiniMax H3's audio, reference-label, shot, or soundscape fields into PixelLab's description.
4. Use last_frame for a real target pose or transition. Treat identical/near-identical anchors as high risk for low-motion loops, and inspect the middle frames even when the endpoints match.
5. Expect frame_count + 1 returned images on both raw routes. Preserve the raw sequence and identify whether index 0 is truly the input before dropping it during a chained stitch or Aseprite import.
6. Report usage.generations when present. Keep website USD estimates separate from generation units, and never infer a route cost from the number of output images.
7. Verify canvas size, alpha, frame order, first-frame echo, last-frame equality, palette/identity stability, bounding-box drift, and detached effects before calling a clip final. A technically valid frame count is not the same as a visually acceptable loop.

## Limitations and unresolved questions

- Website USD estimates and REST generation-unit examples are both official but are not presented as a conversion. The dated website observation is separate from the doc-watch cache; the response's usage.generations remains the billing ledger.
- The official H3 materials describe audiovisual modes and richer multimodal prompting than PixelLab exposes. The adaptation here is evidence-based prompt structure, not a claim that PixelLab provides raw H3 mode parity.
- Fixed-seed determinism remains untested because all requests used `seed=0` (random). A future repeatability check needs the same explicit nonzero seed on both repeats.
- No exact 32×32, 64×64, or 80×80 robot source existed in the archive, so those planned scale points remain untested. The 16×32 flame and 256×256 fireplace provide small-effect and maximum-canvas evidence, but not a complete pricing curve.
- The live sample was designed to fit safely under the user's 3,000-unit cap. It is a routing spike, not a benchmark leaderboard or a substitute for visual review of a user's own sprite.

## Sources

PixelLab:

- [PixelLab API catalog](https://www.pixellab.ai/pixellab-api)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [REST v2 LLM guide](https://api.pixellab.ai/v2/llms.txt)
- [Hosted MCP tool guide](https://api.pixellab.ai/mcp/docs)
- [PixelLab docs](https://www.pixellab.ai/docs)
- [PixelLab MCP setup page](https://www.pixellab.ai/mcp)

MiniMax H3:

- [MiniMax H3 official open-source announcement](https://www.minimax.io/news/minimax-h3-open-source)
- [MiniMax-H3 official repository](https://github.com/MiniMax-AI/MiniMax-H3)
- [Official H3 prompt-skill README](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/README.md)
- [Official H3 prompt skill](https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3/main/skills/h3-prompt-writing/SKILL.md)
- [Official H3 base prompt guide](https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3/main/skills/h3-prompt-writing/references/base-en.txt)
- [Official H3 reference prompt guide](https://raw.githubusercontent.com/MiniMax-AI/MiniMax-H3/main/skills/h3-prompt-writing/references/ref-en.txt)

Aseprite:

- [Aseprite source repository](https://github.com/aseprite/aseprite)
- [Aseprite documentation source](https://github.com/aseprite/docs)
- [Animation documentation](https://github.com/aseprite/docs/blob/main/animation.md)
- [Sprite documentation](https://github.com/aseprite/docs/blob/main/sprite.md)
- [Exporting documentation](https://www.aseprite.org/docs/exporting)
- [CLI documentation](https://github.com/aseprite/docs/blob/main/cli.md)
- [Frame Lua API](https://www.aseprite.org/api/frame)
- [Sprite Lua API](https://www.aseprite.org/api/sprite)
- [Layer Lua API](https://www.aseprite.org/api/layer)
- [ExportSpriteSheet command API](https://github.com/aseprite/api/blob/main/api/command/ExportSpriteSheet.md)
- [Sprite-sheet export source](https://raw.githubusercontent.com/aseprite/aseprite/main/src/app/commands/cmd_export_sprite_sheet.cpp)
- [Sprite source](https://raw.githubusercontent.com/aseprite/aseprite/main/src/doc/sprite.cpp)
- [Cel source](https://raw.githubusercontent.com/aseprite/aseprite/main/src/doc/cel.cpp)
- [New-frame command source](https://raw.githubusercontent.com/aseprite/aseprite/main/src/app/commands/cmd_new_frame.cpp)
