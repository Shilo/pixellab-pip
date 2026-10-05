# PixelLab Skeleton v3 Research Spike

Current contract recheck (2026-10-05): the refreshed REST/MCP descriptions still document beta status, 3–15 frames, and a 256×256 maximum, but no longer state a Tier 1 gate. MCP now specifies each of the 18 named joints exactly once per pose, in any order, and documents any-integer `z_index` draw order (default 0) plus `depth` from 0–255 (about 128 is body center; higher is nearer; omission uses the template's standing-pose depth for the selected direction). The live comparison findings below remain historical observations from the dated campaigns and were not rerun.

## Summary

Skeleton v3 is PixelLab’s pose-conditioned animation workflow: give it one sprite, a keypoint skeleton for the sprite’s existing pose, and a full skeleton for each desired output frame. The REST/MCP route supports 3–15 frames up to 256×256, is currently beta, and the refreshed public REST/MCP descriptions no longer state a Tier 1 gate. Its useful distinction from text animation is that the motion is laid out as explicit poses instead of left entirely to an action prompt. The tradeoff is substantially more pose-authoring work, plus the model still redraws pixel art and needs output review. For an existing managed character, `animate_character(mode="skeleton-v3", template_animation_id=...)` applies a named animation template with the Skeleton v3 model; it is a different workflow from supplying raw per-frame keypoints.

**Practical choice:** use text-v3 as the first try for ordinary walks and jumps. In the matched samples, PixMiniMax made punches and jumps more visually forceful, but added impact effects and sometimes turned the character away from the requested facing. Use raw Skeleton v3 when caller-authored pose order matters enough to justify writing a full 18-joint sequence and paying more; it guides the pose but does not lock the original pixels in place. For a stored character and a named motion, managed Skeleton v3 reuses a template with a different animation model. PixelLab claims steadier identity and colors than managed `mode="template"`, at 2–4 rather than 1 generation per direction; the earlier matched managed sample found no decisive visual improvement, so treat that as a possible benefit rather than a guarantee. [MCP docs](https://api.pixellab.ai/mcp/docs)

The public docs call REST `/animate-with-skeleton` the older three-frame engine, but the current OpenAPI does **not** mark that endpoint deprecated or removed. “Standard skeleton” can also mean managed `mode="template"`, which is a separate managed-character option. This spike keeps those terms distinct and avoids treating either legacy route as unavailable.

The expanded raw-image comparison on 2026-09-26 covered 18 matched cases: two 64×64 sprites, four actions, and three seeds, with 54 accepted jobs across raw Skeleton v3, text-v3, and PixMiniMax. All jobs completed with eight generated frames and transparent output. The estimated spend was 90 generations for the animation jobs plus 0.3 for three skeleton estimates; two text-v3 submissions omitted a response cost field, so their documented one-generation rate is included in that estimate. Text-v3 was clearest for walks and jumps in this sample; PixMiniMax was clearest for punches and also produced strong jumps, but often added unrequested hit effects; raw Skeleton v3 exposed the authored pose progression but did not consistently produce a readable stride or jump. These are single-reviewer observations from a narrow fixture set, not a general model benchmark.

The earlier 2026-09-25 campaign found that the initial hand-placed starting pose differed from REST `estimate-skeleton` by a median 10.5% of the normalized canvas. After repeating the 3-, 8-, and 15-frame walk with the estimate as the exact starting pose, the sampled output still showed only small visible motion for that sprite and pose sequence. Matched managed template and Skeleton v3 runs completed at eight frames; the Skeleton v3 REST run cost 3 generations but showed no decisive visual advantage in sampled frames. Recorded response-level usage totaled 37.1 generations; one of the two URL/base64 parity calls has no recorded usage. That separate campaign stayed below its 2,000-generation cap.

## Expanded Comparative Test Plan (2026-09-26)

The previous comparison sampled one text-animation output against one corrected raw Skeleton v3 sequence. This follow-up is designed to distinguish model behavior from a lucky or unlucky seed and to cover different kinds of motion.

### Questions

1. Do caller-authored skeletons make intended limb placement and action beats more readable than text prompts on matched sprites?
2. Does the answer change for cyclic, subtle, and large-amplitude actions?
3. How do identity/palette retention, frame-to-frame coherence, transparency, and loop closure compare across repeated outputs?
4. When is the added keypoint-authoring work and generation cost worthwhile compared with text animation?

### Protocol

- **Routes:** raw MCP `animate_with_skeleton_v3`; text-v3 MCP `animate_image`; and PixMiniMax MCP `animate_image_pixminimax`. Do not mix managed `animate_character` results into this raw-image comparison: managed Skeleton v3 consumes named template poses, while managed v3 consumes a text action.
- **Fixtures:** two existing 64×64, south-facing, low-top-down humanoid sprites with different silhouettes and palettes: a red-haired figure in a dark outfit and a colorful chibi girl. Use the same source PNG, view, direction, and background setting for all three routes within each matched case.
- **Actions:** walk cycle, breathing idle, cross-body punch, and jump/land on the first fixture; walk cycle and cross-body punch on the second. These cover periodic, subtle, contact/action-beat, and large-displacement movement without testing a rig that the published 18-joint schema does not support.
- **Repetitions:** three fixed seed values per fixture/action case, shared across the routes. Generate eight frames per case. Use the same concise motion intent for each text route; for raw Skeleton v3, keep the appearance description fixed and supply eight complete 18-joint poses plus the matching starting pose.
- **Review:** inspect every generated frame at native 64×64 pixels. Score each animation’s action readability from 1–5 (1 unclear, 3 recognizable with cleanup, 5 immediately clear); summarize median and range by action and route. Record perceived pose-sequence correspondence, identity/palette, frame coherence, transparency/edges, and loop closure descriptively. Do not treat visual review as pixel-level joint-coordinate measurement. Record response cost, generated frame count, job outcome, and required input structure; this compares setup burden, not timed authoring speed. This is a single-reviewer qualitative evaluation, not a blinded or statistically powered benchmark.

### Inputs For Reproduction

The text-v3 and PixMiniMax routes received the same action string for each matched case, with `frame_count=8`, `no_background=true`, and seeds `101`, `202`, and `303`:

| Action | Prompt |
|---|---|
| Walk | `Walk in place through one complete eight-frame cycle, with alternating footfalls and opposite arm swings. Keep facing south.` |
| Idle | `Breathe quietly in place, with a subtle chest rise and fall and a slight head bob. Keep facing south.` |
| Punch | `Perform one fast cross-body punch with a clear wind-up, impact, and recovery. Keep facing south.` |
| Jump | `Crouch, jump vertically with arms raised and legs tucked at the apex, then land and settle. Keep facing south.` |

Raw Skeleton v3 used the short action label (`walk`, `idle`, `punch`, or `jump`), `direction="south"`, `view="low top-down"`, and `template_id="mannequin"`. Its fixed appearance descriptions were `humanoid with spiky red hair, brown eyes, and a dark outfit` for fixture A and `chibi girl with purple hair and a colorful outfit` for fixture B. The source pose came from REST `estimate-skeleton`; each eight-frame action sequence used all 18 labels and manually authored normalized-coordinate offsets from that starting pose. The same per-fixture action sequence was reused across its three seeds. The two text routes did not receive a separate effect-suppression instruction or prompt enhancement.

### Budget And Stop Rules

The 18 matched fixture/action/seed cases are expected to use 54 generations for raw Skeleton v3 (3 per eight-frame job) and 36 total for the two text routes (1 per eight-frame job), for a planned 90 generations. Allow up to 10 more for an optional managed-route spot check only if the raw comparison leaves a question unresolved, plus 30 for any explicitly justified retry. The campaign ceiling is **150 generations**, well below the requested approximate 1,000-generation maximum. Count reported `usage.generations`; when a route does not return usage, count its published worst-case estimate against the ceiling. Do not submit further jobs once projected spend would exceed 150, and do not retry a failed/ambiguous job without checking its status and remaining budget first.

### Planned Reporting

Keep the observations fixture- and action-specific. Report per-route usage and completion, compare action-readability medians and ranges across repeated cases, describe the other review dimensions qualitatively, and separate live observations from conclusions inferred from route contracts. Do not claim that shared seed numbers make the different models deterministic or that this small fixture set predicts all art styles. The completed results follow.

## Expanded Comparative Results (2026-09-26)

### Completion and spend

- **Matrix:** 18 matched cases × 3 routes = 54 accepted jobs. Every case requested eight generated frames.
- **Completed jobs:** raw Skeleton v3 18/18, text-v3 18/18, PixMiniMax 18/18. The raw route returned eight images; both text routes returned nine images as documented (the unchanged source plus eight generated frames). All completed responses reported transparent output.
- **Generation estimate:** raw Skeleton v3 reported 54 generations total (18 × 3); PixMiniMax reported 18 (18 × 1); text-v3 reported 16, while two accepted text-v3 jobs omitted the response cost field. The published rate for each missing 64×64 eight-frame text job is 1 generation, so the animation-job estimate is **90 generations**. Three REST `estimate-skeleton` calls reported 0.1 generation each, for **90.3 generations total**. No account-specific dollar conversion is inferred.
- **Rejected submissions:** two text-route attempts returned a 20/20 concurrency-limit error before a job ID was issued. They were retried once after slots freed; the errors had no accepted job or cost. There were no failed accepted jobs and no charged retries.
- **Latency:** under the campaign’s 20-job peak concurrency, PixelLab’s `wait_for_jobs` reported 997–1,814 seconds for several completed jobs (about 17–30 minutes), longer than the published route estimates. The load and mixed routes were not controlled well enough to rank engines by latency.
- **Review material:** all 54 eight-frame sequences were inspected in nearest-neighbor contact sheets at native pixel scale. These temporary sheets are not committed; the findings below are the retained research record.

### Action readability

The 1–5 score is a single-reviewer ordinal judgment for how clearly the requested action reads across the generated sequence. Values are median (minimum–maximum) across the listed matched cases; they are not statistical confidence intervals.

| Action | Cases | Raw Skeleton v3 | Text-v3 | PixMiniMax |
|---|---:|---:|---:|---:|
| Walk | 6 | 3 (2–4) | 4 (3–4) | 2 (2–3) |
| Breathing idle | 3 | 2 (2–2) | 3 (3–3) | 1 (1–2) |
| Cross-body punch | 6 | 3 (3–4) | 2 (2–3) | 4 (4–4) |
| Jump and land | 3 | 3 (2–3) | 5 (4–5) | 4 (4–5) |

The action-specific pattern matters more than a single route-wide average: the routes traded strengths rather than producing one overall winner.

### Visual findings and practical fit

- **Raw Skeleton v3:** it exposed the caller-authored order of limb poses, and the punch sequence was more readable than text-v3 in several cases. Walk and jump motion was often compressed, delayed, or uneven, especially on the red-haired fixture; the colorful chibi fixture generally showed larger steps. A submitted skeleton is therefore a useful choreography input, not a guarantee that the rendered pixels will land exactly on every point. One eight-frame call required 18 starting-pose joints plus 8 × 18 target-pose joints (162 joint entries total), versus one action sentence for either text route. Its reported 3-generation cost was triple each text route’s documented 1-generation cost at this size.
- **Text-v3:** it gave the clearest walks and jumps with the least setup. The punch wording was not reliable in these samples: several outputs looked like a guard or crossed-arm stance rather than a clear wind-up, impact, and recovery. The idle was subtle and mostly appropriate, though face and eyelid changes varied between seeds.
- **PixMiniMax:** it made the clearest punches and strong jumps, but punch sequences frequently added bright impact/projectile effects and turned the sprite toward a side view. Those can be desirable for a hit effect but need to be explicitly accepted or cleaned up. Walks were often nearly static, and idles frequently showed little visible movement. The route’s extra motion amplitude did not make it the best general-purpose choice in this matrix.
- **Identity and output integrity:** all three routes kept each source character recognizable and retained its main palette. Facial expression, limb placement, and apparent facing varied; PixMiniMax punch effects were the largest additions outside the source design. Every completed job reported transparent output. No pixel-level alpha-mask or edge-quality measurement was made, and transparency success does not imply a finished loop.
- **Timing and closure:** generated motion was coherent enough to read as one sequence in most samples, but pose rhythm and frame-to-frame amplitude varied by seed. A number of walk and action sequences did not end exactly where they began. Check the first-to-last transition before treating any result as a seamless loop.

### Decision guidance from this sample

- Start with text-v3 for quick walks, jumps, and ordinary motion; it was the clearest and least labor-intensive path for those actions here.
- Try PixMiniMax for forceful hits or jumps when dynamic motion is desired, then review facing, extra impact graphics, and loop closure.
- Use raw Skeleton v3 when a specific pose sequence is part of the requirement and someone can author and revise the joints. Budget 3 generations per eight-frame 64×64 output and plan for visual cleanup.
- Do not choose among these routes from this sample alone for other styles, camera angles, resolutions, non-humanoids, or more elaborate motions. This campaign used two south-facing low-top-down humanoids, the four fixed prompts above, three shared seed numbers, and a single reviewer. The same raw pose sequences were reused across seeds; authoring time was not measured. The equal seed numbers do not control the different model routes’ random processes.

## Scope And Evidence Labels

Research checked on 2026-09-25 against PixelLab’s refreshed REST OpenAPI, MCP docs, exposed live MCP tool metadata, current API pricing page, product guides, the supplied Version 0.4.125 announcement, and the requested video. The comparative live campaign ran on 2026-09-26. The local documentation-watch snapshot is `.local/pixellab-doc-watch/snapshots/20260925T145051Z/`; its report says all seven sources fetched, REST OpenAPI and REST index were unchanged, and MCP and website source bytes changed without a normalized-content change.

- **Contract fact** means a current REST schema or official MCP tool description says it.
- **Product-guide fact** means it appears in PixelLab’s product documentation; some animation guides describe the earlier editor workflow and are not Skeleton v3 API specifications.
- **Walkthrough observation** means the video creator showed or said it. It is not an independent benchmark.
- **Inference** means a practical conclusion drawn from those facts; it is labeled as such.
- **Live observation** means a result from this campaign’s submitted PixelLab jobs. Visual comparisons are qualitative samples unless stated otherwise.

The earlier 2026-09-25 campaign stayed below its 2,000-generation ceiling. The expanded 2026-09-26 campaign has its separate job and estimator accounting above. MCP raw-animation and REST calls that returned `usage.generations` are recorded separately from managed-animation pricing estimates; PixelLab’s managed `animate_character` responses did not return per-job generation usage. The video transcript is YouTube’s auto-generated English transcript, not a human-verified transcript. The summary below paraphrases it and links to timestamps rather than reproducing the transcript.

## Controlled Live Tests (2026-09-25)

### Protocol and starting-pose calibration

The raw tests used one existing 64×64 south-facing, low-top-down humanoid sprite and a fixed appearance description. The same input image and action-specific target poses were reused within matched raw comparisons. Submitted raw MCP jobs completed, returned the requested number of frames, and reported transparent output; completed raw results were saved to the PixelLab gallery. Representative frames were inspected at native pixel size.

The first 3-, 8-, and 15-frame walk sweep used manually placed starting points. Afterward, REST `POST /v2/estimate-skeleton` returned 18 distinct joint labels and reported `usage.generations: 0.1`. The manual points had a median Euclidean displacement of 0.105 normalized canvas units from that estimate. This is a comparison between two pose sources, not an accuracy score for the estimator. The result prompted a corrected walk sweep: the first pose and the source `first_frame_keypoints` were both set to the estimate, then the planned 8-frame repeat was used for the corrected 8-frame case.

### Results and usage

| Case | Route and input | Reported usage | Live result |
|---|---|---:|---|
| Initial frame-count and motion checks | Raw MCP Skeleton v3: 3-, 8-, and 15-frame walk, then 8-frame idle and jump; manually placed starting pose | 15 generations total | Exact requested counts completed with transparent output and stable character/palette. Walk and idle samples looked nearly static; jump showed a more visible raised-arm/body shift. Because the starting pose was misaligned with the estimator by a median 0.105, these runs are calibration checks, not evidence of pose-control quality. |
| Corrected frame-count sweep | Raw MCP Skeleton v3 walk, 3, 8, and 15 frames; estimated starting pose reused exactly | 9 generations total | All three counts completed exactly with transparent output. At native size, sampled frames remained visually close and did not show a strong readable stride for this pose sequence. |
| Cross-body strike | Raw MCP Skeleton v3, 8 frames; same estimated starting pose and a large right-arm crossing sequence | 3 generations | Eight transparent frames completed. Sampled frames showed limited visible arm crossing; this is a qualitative observation for this authored sequence. |
| Explicit depth | Raw MCP Skeleton v3, 8-frame walk with explicit left/right/torso depth; compared with the corrected 8-frame walk using template defaults | 3 generations | Eight transparent frames completed. The sampled pair showed no obvious limb-order change; no pixel-level difference score was computed. |
| URL/base64 parity | Raw MCP Skeleton v3, corrected 3-frame walk; same sprite and poses sent once as URL and once as base64 | 2 generations recorded for one call; other call unrecorded | Both jobs returned three transparent frames. Sampled frames looked similar; this was not a pixel-equivalence test. |
| Text-animation control | MCP `animate_image`, same sprite, short eight-frame walk prompt | 1 generation | The response contained the original input plus eight generated frames (nine images total, as the MCP contract specifies). A sampled middle frame showed a clearer raised-arm pose than the corrected raw walk samples. |
| Legacy three-frame route | REST `POST /v2/animate-with-skeleton`, three corrected poses | 1 generation | The synchronous response contained exactly three images. The sampled poses looked similar to one another. The endpoint remains a separate older REST contract; it is not managed template mode. |
| Managed template baseline | MCP `animate_character(mode="template")`, `walking-8-frames`, south and east | Per-direction usage was not returned; public MCP pricing says 1 generation per direction | Both directions completed as eight-frame animations. The east result was selected as the matched managed baseline for the REST Skeleton v3 request. |
| Managed Skeleton v3 | MCP request for the existing south template reused completed output; REST `POST /v2/animate-character`, same character/template and east direction, accepted a distinct job | REST background-job response reported 3 generations | The REST job completed as an eight-frame east animation and saved to character storage. The MCP response returned “already complete” for the south template and exposed no separate job usage, so the REST run supplied the distinct managed Skeleton v3 sample. Representative east-facing samples from both managed modes kept the same side-facing character; the v3 sample showed small limb shifts but no decisive visual advantage in this review. |
| Quadruped boundary | Not submitted | 0 | The public schema exposes one humanoid-style 18-label rig; `template_id="horse"` only changes default depth and is not a separate quadruped joint schema. No alternate pose mapping was invented for this campaign. |

Raw MCP Skeleton v3 responses with recorded usage total 32 generations: 15 for the initial walk/motion checks, 9 for the corrected frame-count sweep, 3 for the strike, 3 for explicit depth, and 2 for one URL/base64 parity call. The other parity call's usage was not recorded. The text control reported 1 generation, the legacy REST route reported 1, `estimate-skeleton` reported 0.1, and the completed managed Skeleton v3 REST job reported 3. Recorded response-level usage totals 37.1 generations; this is incomplete for all submitted calls. Managed template usage is also not included because its MCP responses did not expose per-job usage; keep the public estimate of 1 generation per direction separate from the recorded response-level total.

### Interpretation

- **Live observation:** with this one sprite, the exact estimated start pose, and the tested target sequences, the raw Skeleton v3 samples showed little visible gait or arm-crossing change. Identity, palette, and transparent output remained stable in the sampled raw frames.
- **Live observation:** the text control produced a more visibly raised arm in the sampled walk sequence and required only a short motion description. It also includes the source frame in its result, so its returned image count should not be compared directly with raw Skeleton v3’s output-only count.
- **Live observation:** the matched managed east-facing `walking-8-frames` outputs both completed with eight frames. The sampled Skeleton v3 output retained the side-facing character and showed small limb movement; this small visual sample did not establish a decisive benefit over the template output.
- **Inference:** use raw Skeleton v3 when the caller needs ownership of each keypoint pose, but validate the start pose against the image and inspect whether the generated frames visibly follow the authored range before relying on it. For a simple walk draft on this fixture, text animation was easier to prepare and read more clearly in the selected samples.
- **Limitation:** the test did not use independent human-scored pose coordinates, repeated seeds, or an alternate subject. It does not establish general comparative quality or whether a different pose amplitude, view, seed, or sprite would behave the same way.

## What Skeleton v3 Does

PixelLab describes the raw route as animating a sprite “by posing it”: one skeleton for each output frame, with every output frame drawn from a single reference image. It is a learned image-generation workflow conditioned on poses, not a conventional exported bone rig that mechanically deforms the source pixels. PixelLab’s REST description says the first pose is redrawn to establish the background key and colors; that redraw is not returned. If the supplied starting skeleton does not match the sprite’s actual pose, transparency and color accuracy can suffer. [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) · [MCP docs](https://api.pixellab.ai/mcp/docs)

There are two public ways to use it:

1. **Raw pose sequence:** REST `POST /v2/animate-with-skeleton-v3` or MCP `animate_with_skeleton_v3`. You provide the source sprite and all pose keypoints yourself. This is for a raw image or a sequence whose poses you want to own.
2. **Managed character template:** MCP `animate_character` with `mode="skeleton-v3"` and a `template_animation_id`. PixelLab says it poses the same named template onto the managed character with its skeleton video model, moving the character instead of redrawing each frame; it reports steadier identity and colors than the regular template mode. This is for a character already stored in PixelLab and does not ask the caller for a raw keypoint sequence. [MCP `animate_character` docs](https://api.pixellab.ai/mcp/docs) · [REST schema](https://api.pixellab.ai/v2/openapi.json)

The Version 0.4.125 announcement supplied with the request lists Character Creator, Aseprite, and Pixelorama as product surfaces for Skeleton v3. The walkthrough demonstrates the Character Creator surface; the API facts below describe the separate programmatic REST/MCP routes.

## Raw REST And MCP Contract

### Request fields

The REST operation requires `description`, `action`, `direction`, `first_frame`, `first_frame_keypoints`, and `keypoints`. The current MCP descriptor exposes the same conceptual inputs, with either `first_frame_base64` or `first_frame_url` for the image. The exact surface-specific names and defaults should be checked in the live schema when integrating.

| Field | Meaning and constraints |
|---|---|
| `first_frame` | PNG sprite encoded as a base64 image on REST. The REST description sets the maximum canvas at 256×256; output frames use the same dimensions. MCP also accepts an image URL and recommends a URL for larger images because inline base64 can be truncated by some MCP clients. |
| `first_frame_keypoints` | All 18 joints describing the pose already visible in `first_frame`. PixelLab redraws this pose to establish the starting appearance/background; this initial redraw is not returned. |
| `keypoints` | Ordered pose list: one skeleton for every requested output frame, 3–15 frames total, all 18 joints in each. The finished response has exactly this many frames. |
| `description` | Required appearance noun phrase: subject, colors, clothing, held items. PixelLab says not to put pose, motion, style, or background here. |
| `action` | Required short motion label such as `walk`, `run`, or `attack`. The skeleton sequence carries the detailed pose/motion. |
| `direction` | Required facing direction: `south`, `north`, `east`, `west`, `south-east`, `south-west`, `north-east`, or `north-west`; south faces toward the camera. |
| `view` | Camera angle: `low top-down` (default), `high top-down`, or `side`. The MCP docs say this must match the sprite’s view. |
| `template_id` | `mannequin` (default), `bear`, `cat`, `dog`, `horse`, or `lion`. It supplies default depth positions for joints when `depth` is omitted. PixelLab warns that using mannequin depth for a quadruped makes it appear flat. |
| `no_background` | Boolean, defaults to `true`; returns transparent frames when true. |
| `seed` | Non-negative integer; `0` means random. |

Each keypoint is an object with a required label and normalized `x` and `y`: `0` is the left/top edge and `1` the right/bottom edge. MCP docs require each of the 18 labels exactly once in the starting pose and every animation frame; order is arbitrary. Optional `z_index` accepts any integer as draw order (higher draws on top; default `0`). Optional `depth` is a 0–255 camera-depth value; higher means nearer. If omitted, the template body’s standing-pose depth for that direction is used. REST OpenAPI lists the 18 label values below. [Exact REST schema](https://api.pixellab.ai/v2/openapi.json) · [MCP field descriptions](https://api.pixellab.ai/mcp/docs)

| Area | Required joint labels |
|---|---|
| Head and torso | `NOSE`, `NECK` |
| Right arm | `RIGHT SHOULDER`, `RIGHT ELBOW`, `RIGHT ARM` |
| Left arm | `LEFT SHOULDER`, `LEFT ELBOW`, `LEFT ARM` |
| Right leg | `RIGHT HIP`, `RIGHT KNEE`, `RIGHT LEG` |
| Left leg | `LEFT HIP`, `LEFT KNEE`, `LEFT LEG` |
| Face and ears | `RIGHT EYE`, `LEFT EYE`, `RIGHT EAR`, `LEFT EAR` |

**Schema caveat:** MCP prose explicitly requires each exact joint label once, while REST OpenAPI does not add `minItems`/`maxItems` or unique-label constraints to the arrays. Treat the prose contract as authoritative and do not infer that an incomplete or duplicate-label array is accepted merely because its JSON shape parses. The schema publishes one 18-label set; although `template_id` includes animal bodies for depth defaults, the docs do not define a separate quadruped joint-label schema.

### Response and job lifecycle

REST returns a `background_job_id` and processing status. Poll `GET /v2/background-jobs/{job_id}`; the REST operation recommends polling every 5–10 seconds. When complete, `last_response.images` contains exactly `len(keypoints)` images, in frame order and at the `first_frame` dimensions. The starting/reference frame itself is not included. The response schema also allows usage information. [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)

The current exposed MCP tool descriptor likewise describes an asynchronous job and `get_image(job_id)` polling. The general MCP `get_image` documentation’s list of raw-image tools does not name `animate_with_skeleton_v3`, however. The route’s own tool descriptor is the direct support evidence; the omission in the general getter list is a documentation gap, not proof that the getter cannot retrieve it. [Official MCP docs](https://api.pixellab.ai/mcp/docs)

### Practical call sequence

1. Choose a source sprite that fits within 256×256 and identify its actual facing and camera angle.
2. Create the initial 18-joint pose. REST `POST /v2/estimate-skeleton` can estimate keypoints from an image, but the estimate may need editing; PixelLab’s editor guide explicitly recommends checking and correcting estimates. `estimate-skeleton` is REST-only in the public tool inventory.
3. Author or convert the remaining 3–15 poses into the same 18-label format. The starting pose must match the pixels in `first_frame` closely.
4. Submit the appearance description, short action label, direction, view, starting pose, and complete ordered pose sequence.
5. Poll the job, retrieve all returned frames, and inspect timing, pose readability, silhouette, colors, edges, background transparency, and loop closure. Keep or correct the art based on actual output; the pose controls do not guarantee pixel-perfect limb placement.

This sequence is a synthesis of the public fields and lifecycle, not a claim that PixelLab provides an automatic multi-pose editor through the raw API. The product’s skeleton-editing workflows can help author poses, but Aseprite/editor file formats should not be assumed to map one-to-one to the REST keypoint schema.

## Managed Character Mode

The managed route is intentionally simpler than raw pose authoring: pass an existing managed `character_id`, a named `template_animation_id`, and `mode="skeleton-v3"` to `animate_character`. PixelLab states that this reuses the template motion but has the Skeleton v3 model pose that template onto the character. The docs describe more stable character identity/colors than the managed `template` mode, at 2–4 generations and about 3–5 minutes per direction; the refreshed descriptions no longer state a Tier 1 gate. [Official MCP `animate_character` docs](https://api.pixellab.ai/mcp/docs)

The REST `CreateCharacterAnimationRequest` schema includes the `skeleton-v3` mode and the template animation field. The same schema is attached to `POST /v2/characters/animations` and `POST /v2/animate-character`; the endpoint prose does not consistently spell out the new mode, so the mode schema and MCP tool descriptor are the clearest evidence. For managed calls, pass `directions` explicitly when direction scope matters: the public schema explains defaults for `template` and custom `v3`, but does not clearly document the default-direction behavior for `skeleton-v3`.

The current public MCP docs include `skeleton-v3` in the managed `mode` schema. A connected client may still have an older tool schema: check that the `animate_character` mode enum exposes it, refresh/reconnect if it does not, and use REST `POST /animate-character` with both `mode="skeleton-v3"` and `template_animation_id` if the connected MCP schema still cannot accept it. The managed mode consumes a named template; it is not the raw caller-authored keypoint route.

The managed mode is not the same as the raw `/animate-with-skeleton-v3` route:

- Managed mode starts from a stored character ID and a PixelLab animation template ID; PixelLab supplies the template poses.
- Raw mode starts from an image and caller-supplied 18-joint poses for every output frame.
- The managed mode’s “steadier identity and colours” claim is PixelLab’s comparison to its own managed `template` mode, not a published controlled comparison against arbitrary text animation.

## Comparisons: Which Animation Workflow Fits?

| Workflow | What you provide | What controls pose | Strong fit | Main tradeoff |
|---|---|---|---|---|
| REST `animate-with-text-v3` / MCP `animate_image` | One starting image and an action description | The model interprets the motion text | Quick motion drafts, loosely specified actions, or subjects that do not fit an 18-joint rig | Least explicit control of exact limb positions; output is guided by the prompt, not a supplied pose at every frame. |
| REST `animate-with-skeleton-v3` / MCP `animate_with_skeleton_v3` | One starting image, its keypoints, and 3–15 full per-frame poses | Caller-authored skeleton sequence | A character action whose pose progression needs explicit choreography | Highest pose-authoring burden; model still draws the pixels and needs review. |
| MCP managed `animate_character(mode="skeleton-v3", template_animation_id=...)` | Stored character, animation template ID, selected directions | PixelLab template poses passed through Skeleton v3 | Faster access to a known template motion on a managed character | Less control over the raw keypoint sequence; beta and per-direction processing. |
| MCP managed `animate_character(mode="template")` | Stored character and animation template ID | Existing managed template skeleton animation | Low-cost template animation when the older template output is acceptable | PixelLab describes it as 1 generation per direction; video creator reports the pre-update template quality was less usable/stable than Skeleton v3. |
| REST legacy `/animate-with-skeleton` | Reference image plus legacy skeleton payload; optional masks/init/palette inputs | Legacy three-pose skeleton window | Existing integrations that specifically need this route’s older options | Exactly three skeleton frames; REST OpenAPI calls it the older three-frame engine. It remains documented and has no `deprecated: true` flag. |

The text comparison is based on the public interfaces: text animation takes a motion description, while Skeleton v3 takes a full 18-joint pose for every generated frame. **Inference:** pose-by-pose input should make intended body placement more controllable, while text prompting is easier to use and accommodates motions without a joint rig. Neither interface promises exact pixel preservation or perfect motion; inspect generated frames.

### Skeleton v3 versus the “standard” skeleton system

“Standard skeleton” is ambiguous in PixelLab’s current public terms. There are two plausible referents:

1. **Managed `mode="template"`:** a named template skeleton animation for a managed character, documented at 1 generation per direction. `mode="skeleton-v3"` feeds that same named template through the Skeleton v3 video model; PixelLab claims steadier identity and colors and lists 2–4 generations per direction. This is the clearest current standard-vs-v3 comparison in the MCP docs.
2. **Legacy raw REST `POST /animate-with-skeleton`:** a separate endpoint whose payload’s `skeleton_keypoints` represents exactly three frames, with optional init images, inpainting masks, and color palette. The raw OpenAPI calls it the older three-frame engine. It is not the same as managed `mode="template"` and is not the same schema as Skeleton v3’s 3–15 full-pose sequence.

The current OpenAPI does not mark `/animate-with-skeleton` or `/estimate-skeleton` as deprecated, and the API documentation continues to list them. Therefore, “deprecated standard skeleton” should be treated as informal shorthand, not a verified lifecycle status. The API docs say the older route remains available; they do not announce a removal date. [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json) · [PixelLab skeleton editor guide](https://www.pixellab.ai/docs/tools/animate-with-skeleton)

### Why use Skeleton v3 instead of text-only animation?

Use Skeleton v3 when the motion must pass through known poses—such as distinct anticipation, contact, and recovery positions—or where the intended arm/leg placement matters more than minimizing setup. That recommendation is an inference from its per-frame pose inputs, not a vendor guarantee that it will obey every coordinate perfectly.

Use text animation when the desired movement can be explained adequately in words, when the subject is not a humanoid-style articulated sprite, or when quickly generating a candidate matters more than specifying each pose. The product guide describes a text-animation editor workflow and recommends skeleton animation for characters, but does not compare the current API models; treat it as supporting context, not a benchmark. [PixelLab animation guide](https://www.pixellab.ai/docs/tools/animation)

For a managed character and a standard named motion, the managed `skeleton-v3` mode is the middle path: it keeps template-based motion selection while using the newer model. For custom choreography, raw keypoints give direct ownership of pose input but require the most work.

## Strengths, Costs, And Limits

### Benefits supported by the current contract

- Per-frame poses make the intended motion structure explicit rather than relying only on a natural-language action description.
- The raw route returns 3–15 frames, rather than the legacy raw skeleton route’s fixed three-frame window.
- The live `animate_with_skeleton_v3` MCP tool description lists generation-time pricing of 2 generations for 3 frames, 3 for 8, and 4 for 15; frame size up to the documented 256×256 maximum does not change the price rung.
- In managed character mode, PixelLab says its skeleton video model moves the character instead of redrawing each frame and produces steadier identity/colors than regular template mode.
- Missing depth values can use the selected template’s default depth for the chosen facing direction, avoiding a need for authored 3D depth data in ordinary cases.

### Costs and limits

- **Availability:** Beta. The refreshed REST/MCP descriptions no longer state a Tier 1 gate; check the live surface for account availability.
- **Canvas:** first-frame image up to 256×256; output frame dimensions match it.
- **Length:** 3–15 output frames, one complete skeleton per frame.
- **Rig:** current request schema describes 18 joint labels and has no alternative public rig schema.
- **Latency:** the REST OpenAPI describes a typical 3–5 minute generation time; the live `animate_with_skeleton_v3` MCP tool description says approximately 3–6 minutes asynchronously; managed `skeleton-v3` mode in the static MCP docs describes approximately 3–5 minutes per direction. These are surface-specific estimates, not a service-level guarantee, and the raw MCP range is wider than REST's.
- **Price estimates:** public API catalog lists approximately $0.0436 for 3 frames, $0.0513 for 8, and $0.0622 for 15, at any listed size. These are catalog estimates, not an account-specific quote. The actual usage returned by the service is the billing evidence. [PixelLab API pricing catalog](https://www.pixellab.ai/pixellab-api)
- **Preparation:** each frame requires 18 named points. A 15-frame sequence means 270 points plus the 18-point starting pose if counting input entries; authoring, checking labels, and keeping poses coherent can exceed the effort of writing a text action.
- **Model uncertainty:** pose conditioning is not pixel locking. The source redraw, style rendering, occlusion, silhouette, and cleanup remain model-dependent.

The separate REST `estimate-skeleton` helper has its own public estimates around $0.0051 in the catalog. If used, account for that separately from the animation estimate. It is not an MCP equivalent in the published tool inventory.

### Failure modes and review checklist

| Failure risk | Why it happens | Check or mitigation |
|---|---|---|
| Palette drift, background leakage, or loss of transparency | The first pose is redrawn; if `first_frame_keypoints` do not represent the pixels in the reference image, the model may learn a different color/background representation. | Match the first pose carefully, use the correct view/direction, and inspect transparency and colors across all frames. |
| Wrong apparent depth/flat quadruped | Omitted depth is borrowed from `template_id`; default is mannequin. | Choose a matching template for supported animal depth defaults or supply depth when there is reliable depth data. The docs do not publish a distinct quadruped joint set. |
| Unreadable or inconsistent motion | Keypoints are normalized coordinates and each of the 18 labels must occur exactly once (order is arbitrary), but the contract does not guarantee the model’s pixel-level interpretation. | Validate frame order, joint locations, silhouette, limb crossing/occlusion, and motion rhythm. Fix poses or manually clean the result. |
| Wrong camera angle or facing | `view` and `direction` determine how the pose is interpreted. | Match the source sprite’s view; set required direction intentionally instead of relying on a default (REST has none). |
| Incorrect output count | There must be one target skeleton per requested output frame. | Confirm `keypoints.length` is between 3 and 15 and inspect that the returned `images` count equals it. |
| Submission rejected before a job is accepted | `POST /animate-with-skeleton-v3` returns 401 for an invalid token, 402 for insufficient credits, 422 for validation errors, or 429 when too many background jobs are concurrent. HTTP 200 means the background job was accepted; it does not mean the animation completed. | Check credentials, credits, request shape, and concurrency. Correct the cause before resubmitting; do not blindly repeat a potentially paid generation. |
| Accepted job later fails | A successful submission yields a `background_job_id`; the background-job resource can later report `status="failed"`. Its generic `last_response` is an object or null, and the schema does not define a Skeleton v3-specific failure payload. | Poll the returned job ID, stop when `completed` or `failed`, and inspect the returned status/details before deciding whether to retry. Job polling has its own 401 invalid-token, 404 missing/not-owned job, 422 validation, and 429 too-many-requests responses. |
| MCP payload corruption | Some clients truncate large inline base64. | Prefer `first_frame_url` for large sprites where the current MCP schema offers it; ensure the URL is accessible to PixelLab. |

**Output QA:** verify that all returned images have the input canvas size; no-background output has usable alpha; the same character remains recognizable; every frame follows the intended pose/action; limbs and held items read clearly at native pixel scale; and a loop’s first/last transition works. The video creator explicitly reminds viewers to clean up results because they are not always perfect.

## What The Requested Walkthrough Shows

The video is titled **“PixelLab Tutorial: Images Pro Flash, Skeleton V3 & PixMiniMax”**. Its available transcript is auto-generated English captions. Relevant observations:

- Around [8:45](https://www.youtube.com/watch?v=Y68m9k60Lg0&t=525s), the creator sends a beetle sprite into Character Creator, generates a managed character, and expands the canvas to 80×80 before animation to leave room for movement.
- Around [9:15–10:10](https://www.youtube.com/watch?v=Y68m9k60Lg0&t=555s), the creator chooses an eight-frame walking template and runs it through Skeleton v3. He describes the motion as more usable and stable than the previous setup, recommends trying templates again, and says to clean up frames because the result is not perfect.
- Around [10:12 onward](https://www.youtube.com/watch?v=Y68m9k60Lg0&t=612s), the creator switches to a custom PixMiniMax text action. Later facing-direction and effect-color prompt adjustments are about that text-animation example, not Skeleton v3; they should not be cited as Skeleton v3 behavior.

These are a single creator’s qualitative demonstrations. They support that the managed template workflow is practical and show one reported improvement over the prior setup, but they do not establish measured stability, identity retention, comparative error rates, or guaranteed quality.

## Unresolved Documentation Questions

1. The published REST OpenAPI descriptions say every skeleton contains 18 joints but do not encode array cardinality or unique labels as formal constraints. Public docs do not show the exact validation error for incomplete/mislabelled poses.
2. The MCP tool’s own descriptor documents `get_image(job_id)` polling, while the shared `get_image` prose list omits Skeleton v3 by name. A future MCP docs sync should reconcile that list.
3. Managed `skeleton-v3` supports a selected `directions` field, but its default direction behavior is not stated as clearly as for managed template and custom v3 modes. Specify directions when scope matters.
4. Connected MCP schemas may lag the public `skeleton-v3` mode documentation. Check the current enum before routing managed requests; refresh the connection or use REST if the mode is absent.
5. The current source does not define whether REST legacy `/animate-with-skeleton` will be retired; it is described as older and is not marked deprecated in the OpenAPI.
6. Product docs mention Skeleton v3 availability across Character Creator, Aseprite, and Pixelorama in the supplied 0.4.125 announcement, but the current public API specification does not document the editors’ internal skeleton-file format or guarantee interchangeability with the API keypoint schema.

## Sources

### Primary public contract

- [PixelLab REST v2 OpenAPI JSON](https://api.pixellab.ai/v2/openapi.json) — exact endpoint, request/response schemas, required properties, joint enum, frame counts, job ID, and the older three-frame route.
- [PixelLab REST v2 interactive docs](https://api.pixellab.ai/v2/docs) — human-readable API index and endpoint descriptions.
- [PixelLab MCP docs](https://api.pixellab.ai/mcp/docs) — `animate_with_skeleton_v3`, managed `animate_character(mode="skeleton-v3")`, and MCP parameters.
- Read-only live MCP tool metadata checked on 2026-09-25 for `animate_with_skeleton_v3` and `animate_character` — the raw 2/3/4-generation examples and ~3–6-minute estimate are dynamic tool-description values; do not attribute those raw estimates to the static guide.
- [PixelLab API pricing catalog](https://www.pixellab.ai/pixellab-api) — current tier, beta status, size/frame limits, and estimated USD prices.

### Product guidance and demonstration

- [PixelLab “Animate with skeleton” editor guide](https://www.pixellab.ai/docs/tools/animate-with-skeleton) — setup and manual editing guidance for the skeleton workflow; not a v3 API schema.
- [PixelLab “Animation with text” guide](https://www.pixellab.ai/docs/tools/animation) — product guidance recommending skeletons for character work; not a controlled comparison of current API models.
- [PixelLab tutorial video](https://www.youtube.com/watch?v=Y68m9k60Lg0) — auto-generated English transcript reviewed for timestamps 8:45–10:10 (managed character and Skeleton v3 template demonstration).
- Version 0.4.125 release announcement pasted into the task — names Character Creator, Aseprite, and Pixelorama as editor surfaces and says Skeleton v3 is available there. The pasted announcement is not a linkable API specification.

### Local evidence snapshot

- `.local/pixellab-doc-watch/snapshots/20260925T145051Z/raw/rest-openapi.json`
- `.local/pixellab-doc-watch/snapshots/20260925T145051Z/raw/mcp-docs.md`
- `.local/pixellab-doc-watch/reports/20260925T145051Z.md`

The local snapshot is gitignored; use the official URLs above as the durable references.
