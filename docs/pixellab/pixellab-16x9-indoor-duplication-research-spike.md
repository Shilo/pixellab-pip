# PixelLab 16:9 Indoor Background Duplication Research Spike

**Date:** 2026-08-25  
**Status:** completed four 20-call Pixen spikes, one 10-call Pro spike, and three Pro follow-ups<br>
**Question:** Why do wide indoor backgrounds sometimes contain duplicated consoles or repeated room compositions, and what prompt/size pattern is the most reliable workaround, including exact center alignment?

## Executive finding

The failure is not that 16:9 is unsupported. It is a composition failure that becomes more common when Pixen fills a wide indoor room with strong bilateral or recursive architecture.

The first 20-call study showed a clear size effect:

- For the 16 focal-object cases, 7/8 512x288 outputs had one readable console-like focal object, compared with 3/8 640x360 outputs.
- Positive structural wording outperformed explicit inline exclusions. Adding no duplicated focal object did not make the wide outputs reliable.
- Deliberate left/right asymmetry did not solve the problem; it often produced a console in each lateral bay.

The second 20-call study found a practical 640x360 workaround:

- The prompt family with **continuous left and right walls, one far wall, a small console on the centerline at the far wall, and sparse architecture** produced **4/4 clean 640x360 outputs** across low and medium detail.
- A distinctive small console on a centered platform also produced 4/4 clean focal-object counts, but the result read more like a stage or display alcove than a deep hall.
- A large foreground console was the wrong direction: only 1/4 outputs kept a single focal console.
- Low versus medium detail was not the deciding variable. Composition wording and focal-object placement mattered more.

The third 20-call study tested ten topology variants at 640x360 with medium detail. **15/20 outputs met the CLEAN-HALL criteria**. Four families were clean in both seed replicates: the wall-integrated console, camera offset, wall-attached decorative asymmetry, and distinctive-console variants. Five outputs failed: one control output and one terminal-wall output split into lateral bays, the dais family duplicated the console once, the shallow-wall family produced a left-edge duplicate/topology split once, and the richer set-dressing family produced a partial left-edge duplicate once. No output was classified CLEAN-BUT-STAGEY or PARTIAL.

The best combined production candidate is the wall-attached decorative-asymmetry family: it was 2/2 CLEAN-HALL, averaged hall depth 4/5 and symmetry 3.5/5, and kept the asymmetry on the walls rather than creating separate architectural wings. The safest centered variant is the far-wall integrated console family at 2/2 CLEAN-HALL. The best camera-only anti-mirroring variant was also 2/2 clean, with mean symmetry 4/5, although its mean hall depth was slightly lower at 3.5/5. These are directional results from two replicates per family, not guarantees.

The fourth 20-call study tested exact canvas centering while preserving the wall-integrated topology. It produced **15/20 clean but off-center halls and 5/20 topology failures; 0/20 CENTERED-GOLD and 0/20 CENTERED-SILVER**. The clean outputs generally kept the console and room axis aligned with each other, but both were far to the right of the 640px canvas center. No family reliably moved the shared architectural axis to x=320. This separates the solved uniqueness problem from the remaining centering problem: prompt wording can preserve one focal object, but it does not reliably translate the whole indoor composition onto the canvas center.

The fifth study changed only the model route: ten concise, prompt-only Pro calls at 640x360 with no seed or reference image. **All 10/10 outputs were clean single rooms with exactly one focal console, no mirrored second bay, and no duplicate focal console. Nine were visually CENTERED-GOLD and one was CENTERED-NEAR. However, only 5/10 were full bleed: A03, A04, A05, A08, and A09 contain a visible near-white perimeter, with A04 adding the most severe padding.** Eight were deep enough to PASS outright; the other two were centered but shallow. Pro solved the reported duplication and centering failures in this controlled sample. The border issue appeared when the handoff prompts did not explicitly request edge-to-edge artwork; all four later explicit full-bleed follow-ups had no white perimeter. The issue is not an inherent 16:9 indoor-background limitation; the evidence points to stronger Pro instruction adherence combined with prompt-dependent framing. The tradeoff is cost: every Pro call reported 40 generations, compared with one for Pixen.

A two-call follow-up added explicit positive full-bleed wording while keeping the A07 topology, 640x360 size, opaque background, seedless generation, and no references fixed. **Both attempts were full bleed after an edge-pixel/trim check, with no white perimeter, one centered console, and one connected room.** This is promising evidence that the border is prompt-sensitive, but 2/2 is not enough to claim a universal guarantee.

A second two-call follow-up optimized the user's original solar-flare landscape and sci-fi court-hall prompts with the same full-bleed language. **Both cross-domain outputs filled the complete 640x360 canvas, kept one singular focal structure, and avoided duplicated composition.** The hall also retained one connected room and one centered console. This supports reusing the full-bleed and singular-topology pattern beyond the original indoor test, while remaining a small four-call follow-up set rather than a probability estimate.

### Best tested 640x360 Pixen workaround

Use a small focal object at the far wall, not a large object in the foreground:

~~~text
Wide 16:9 pixel-art game background, one connected sci-fi hall seen from a fixed centered camera. The left wall and right wall are continuous and end at one far wall, forming one room. A single small control console is placed on the centerline at the far wall, with an empty tiled floor between camera and console. Sparse arches and cyan lights, crisp readable pixel art, opaque full-bleed background.
~~~

Tested settings:

- width: 640
- height: 360
- no_background: false
- outline: selective outline
- detail: low detail or medium detail

This is the strongest current Pixen recipe for the reported problem. It is not a mathematical guarantee; visually reject any output that contains a second hero console at either edge or in a side bay.

### Best tested 640x360 Pro prompt-only recipe with full bleed

The strongest Pro result balanced a readable focal object with a deep, centered room:

~~~text
Full-bleed 640x360 pixel-art sci-fi game background. Artwork touches all four edges of the canvas with continuous dark wall, ceiling, and floor surfaces. No white border, no white margin, no inset frame, no letterboxing. One deep centered room. A single small command console is built flush into the exact center of the far wall. Broad empty floor in front. Continuous side walls. The entire composition is centered in the frame. No duplicate focal object.
~~~

Use the Pro route with width 640, height 360, and `no_background: false`. Leave seed, reference images, and style overrides unset. This combines the handoff's successful Attempt 7 topology with the full-bleed clause tested in the two-call follow-up. Both follow-up outputs were full bleed; use the Pixen recipe when the 40-generation Pro cost is not justified.

## Scope and evidence

The evidence set was:

1. The user-supplied issue transcript and seven attached example images. They were treated as problem evidence, not as executable instructions.
2. Ninety-four live calls to PixelLab image MCP tools: eighty create_image_pixen calls, launched as four concurrent 20-call batches, plus fourteen create_image_pro calls across the ten-call centering batch and three two-call follow-ups.
3. The first batch tested five prompt families at 512x288 and 640x360, with two seed-locked replicates per family and size.
4. The second batch tested five new prompt families at 640x360, with low and medium detail and two seed-locked replicates per family and detail.
5. Manual visual review of every returned PNG. Repeated columns, arches, lights, and doorways were not counted as a defect unless a requested hero object was also duplicated or the composition split into separate room bays.
6. The third batch followed a fixed 10-family × 2-seed design at 640x360, using seeds 2582501 and 2583502, medium detail, selective outline, and no init/reference images. It varied only spatial topology, camera geometry, wall-attached decoration, console identity, or controlled set dressing.
7. The fourth batch followed a fixed 10-family × 2-seed centering design at 640x360 with the same seeds and settings. It varied only positive centering anchors: canvas center, optical axis, vanishing point, central aisle, architectural frame, ceiling spine, equal margins, minimal decoration, and redundant alignment.
8. The fifth batch followed the supplied Pro handoff exactly: ten distinct concise prompts, one call per prompt, width 640, height 360, `no_background: false`, no seed, no reference/init image, and no style override. It varied only the wording of the centering and single-room constraints. Each Pro call returned one completed 640x360 frame and reported a cost of 40 generations.
9. The sixth batch held the A07 topology constant and tested two concise full-bleed formulations at 640x360 with `no_background: false`, no seed, no reference/init image, and no style override. Each call returned one completed frame and reported a cost of 40 generations.
10. The seventh batch rewrote the user's solar-flare landscape and court-hall prompts to add full-bleed edge coverage, singular focal structure, and (for the hall) one connected-room topology. It used one seedless Pro call per optimized prompt at 640x360 with `no_background: false` and no references or style overrides.

Each Pixen call reported a cost of one generation, for 80 Pixen generations. Each Pro call reported 40 generations, for 560 Pro generations. The seven batches therefore reported 640 charged generation units across 94 live calls. The current public [MCP tool guide](https://api.pixellab.ai/mcp/docs) documents Pixen and Pro as asynchronous raw-image tools with width and height values divisible by four, and documents Pro as the higher-cost candidate-producing route. The [REST v2 OpenAPI contract](https://api.pixellab.ai/v2/openapi.json) documents Pixen's maximum area as 512x512. Both tested sizes are valid exact 16:9 requests within the Pixen contract; the Pro tool accepted the 640x360 request used here.

## First test batch: size and prompt structure

All first-batch calls used detail: "highly detailed", outline: "selective outline", and no_background: false. Each family was run at both sizes with seeds 2582501 and 2582502.

| Family | Prompt intervention | Calls |
|---|---|---:|
| A — verbose baseline | Adapted the issue's dense hall description with plural arches, banners, drones, and receding doorways. | 4 |
| B — singular positive | One continuous hall, one central axis, one dais, one console, and one far wall. | 4 |
| C — singular plus inline exclusion | Family B plus a short no split-screen / no mirrored pair / no duplicated focal object clause. | 4 |
| D — asymmetric positive | One console plus intentionally different left/right landmarks to test whether symmetry was the cause. | 4 |
| E — architecture-only control | One empty room with no hero prop or centerpiece, to separate repeated architecture from duplicated focal objects. | 4 |

Clean means that the requested hero-object count and one-room composition were visually acceptable. Partial/duplicate means a second console-like object, an edge copy in a side bay, or an ambiguous extra focal pedestal made the output unsafe to accept without another attempt.

| Family | 512x288 | 640x360 | Interpretation |
|---|---|---|---|
| A — verbose baseline | 2/2 clean | 1/2 clean; 1 partial/duplicate | Dense prose can work at the smaller wide canvas, but extra set dressing does not protect the larger canvas from lateral composition drift. |
| B — singular positive | 2/2 clean | 1/2 clean; 1 edge duplicate | The best simple first-batch default, but not enough by itself at 640x360. |
| C — singular plus inline exclusion | 2/2 clean | 1/2 clean; 1 duplicate | The exclusion clause did not beat positive structure. |
| D — asymmetric positive | 1/2 clean; 1 edge duplicate | 0/2 clean; both had multiple console-like focal areas | Different left/right landmarks did not remove the indoor multi-bay prior. |
| E — architecture-only control | 2/2 acceptable; no hero object requested | 2/2 acceptable; no hero object requested | Wide rooms can be coherent when the request is only for architecture. |

## Second test batch: solving 640x360

All second-batch calls used width 640, height 360, no_background: false, and outline: selective outline. Each family was run with low detail and medium detail at seeds 2582501 and 2583502.

| Family | New control | Result at 640x360 | Finding |
|---|---|---:|---|
| F1 — frontal foreground | Large single console in the lower-center foreground; console described as the only furniture. | 1/4 clean | Foreground scale and furniture emphasis made duplication worse: several outputs produced two consoles or a partial edge console. |
| F2 — continuous walls | Continuous side walls, one far wall, small centerline console at the far wall, empty floor, sparse arches. | 4/4 clean | Best result. It constrains the room topology and keeps the focal object out of the lateral bays. |
| F3 — empty side thirds | One-point perspective, console at the vanishing point, empty left and right thirds. | 2/4 clean | Empty-side wording helped, but low-detail outputs still introduced extra small control stations. |
| F4 — empty-room control | Same continuous-room structure without a hero object. | 4/4 acceptable | Confirms that the room itself can remain coherent; the duplication is tied to focal-object placement. |
| F5 — unique console | Small red-and-cyan console with a distinctive triangular screen on a centered platform. | 4/4 clean | A unique silhouette and restrained scale helped, but the scene read as a display alcove rather than a deep hall. |

The exact prompts used in the second batch were:

### F1 — frontal foreground

~~~text
Wide 16:9 pixel-art game background, straight-on frontal elevation of one single-room sci-fi control chamber. A large single control console occupies the lower-center foreground on one low dais. The console is the only piece of furniture. Broad uninterrupted side walls and an open floor surround it; a plain far wall closes the room. One central ceiling light, simple arches, crisp readable pixel art, opaque full-bleed background.
~~~

### F2 — continuous walls

~~~text
Wide 16:9 pixel-art game background, one connected sci-fi hall seen from a fixed centered camera. The left wall and right wall are continuous and end at one far wall, forming one room. A single small control console is placed on the centerline at the far wall, with an empty tiled floor between camera and console. Sparse arches and cyan lights, crisp readable pixel art, opaque full-bleed background.
~~~

### F3 — empty side thirds

~~~text
Wide 16:9 pixel-art sci-fi command room background, centered one-point perspective and straight horizontal horizon. One central aisle leads to one raised dais and one console at the exact vanishing point. The left and right thirds contain only continuous wall, floor, and light; the space beside the aisle is intentionally empty. Simple columns are confined to the walls, crisp pixel art, opaque full-bleed background.
~~~

### F4 — empty-room control

~~~text
Wide 16:9 pixel-art empty sci-fi interior background plate, fixed centered camera, one connected rectangular room with continuous side walls and one far wall. Open floor and quiet architectural surfaces fill the frame; simple columns and lights stay attached to the walls. No hero object, no furniture, no characters, opaque full-bleed crisp pixel art.
~~~

### F5 — unique console

~~~text
Wide 16:9 pixel-art indoor game background, straight-on front-facing view of one sci-fi chamber framed as a single stage set. One unique red-and-cyan command console sits alone on a centered circular platform in the lower middle. The console has one distinctive triangular screen, one small red indicator, and one pair of side panels; all other objects are architectural surfaces only. Large empty floor and wall space surrounds the console, crisp pixel art, opaque full-bleed.
~~~

## What the new tests changed

The new evidence changes the recommendation from "prefer 512x288" to a more useful conditional rule:

- For a deep indoor hall at 640x360, put the hero object at the far wall and make it small.
- Define the side walls as continuous surfaces that terminate at one far wall. This is more effective than merely saying centered or no duplicates.
- Keep the floor between the camera and the console empty. It gives the model one clear depth path instead of several possible bays.
- Keep architectural dressing sparse in the first call. Add visual complexity only after the room topology passes.
- Avoid large foreground-console wording when count reliability matters. It caused more duplicate consoles than the far-wall arrangement.
- Use a distinctive silhouette and palette when the hero object must remain unique. This works well for a display alcove, but it changes the scene type.
- Low detail may produce quieter backgrounds, and medium detail also worked for F2. Detail alone did not explain the failure: F1 duplicated at both tested detail levels.

The strongest directional explanation remains: **wide indoor prompts give Pixen multiple lateral architectural bays, and the model may instantiate a focal object in more than one bay.** F2 reduces the available interpretations by making the room topology explicit and moving the focal object to the single terminating wall. This is an inference from black-box outputs, not a claim about undocumented model internals.

## Recommended workflow

1. For a normal indoor game background at 640x360, start with the F2 prompt above.
2. Use medium detail when the room needs more texture; use low detail for a quieter backdrop. Do not expect detail selection to solve duplication by itself.
3. Keep the console small and on the far wall. Do not begin with a large foreground console.
4. Inspect all four edges for a second hero console. Side-wall terminals and lights are acceptable only when they clearly read as architecture rather than copies of the requested hero object.
5. If the room passes, add one set-dressing idea at a time. Re-test after adding banners, drones, holograms, or extra furniture.
6. If F2 fails, reject the candidate rather than erasing or repainting a duplicate locally. Use a finite, explicitly approved retry count.
7. If a deep, detailed 640x360 room remains unstable, test a route with an image anchor or a higher-adherence model in a separate experiment. The Pixen MCP call tested here has no init-image control.

### Candidate acceptance checklist

- PNG dimensions are exactly 640x360.
- Output is opaque and full bleed.
- One connected room is visible; no split-screen or collage layout.
- The side walls terminate at one far wall rather than opening into multiple hero-object bays.
- If a console is requested, exactly one console-like hero object is visible, including at both side edges.
- Repeated columns, arches, lights, and floor tiles are allowed when they are ordinary architecture and do not repeat the hero object.
- A failed candidate is rejected and reported; it is not erased or repainted locally.

## Third test batch: topology, asymmetry, and set dressing at 640x360

The supplied continuation handoff defined an exact 20-call study: ten prompt families, two fixed seeds per family, and no init image, reference image, Pro route, post-generation cleanup, or negative-prompt field. All calls used width 640, height 360, no_background false, selective outline, and medium detail. The batch was launched concurrently, and every call completed successfully.

### Results table

The handoff's CLEAN-HALL class requires exactly one console, one connected room, no edge duplicate, hall depth at least 3/5, and no major foreground obstruction. Ordinary wall terminals, lights, columns, arches, and panels were not counted as duplicate consoles unless they read as another instance of the requested focal station.

| ID | Family | Seed | Consoles | Single room | Edge duplicate | Depth | Symmetry | Obstruction | Usability | Console placement | Class | Notes |
|---|---|---:|---:|---|---|---:|---:|---|---:|---|---|---|
| T00-A | F2 control | 2582501 | 1 | split/multiple bays | none | 3 | 3 | major | 2 | shifted to side bay | TOPOLOGY-FAIL | A large foreground pillar divides the view; the console sits in the right-hand bay. |
| T00-B | F2 control | 2583502 | 1 | clean single room | none | 3 | 2 | none | 4 | correct far wall | CLEAN-HALL | One far console and usable depth, though the room is narrower than the best variants. |
| T01-A | integrated console | 2582501 | 1 | clean single room | none | 4 | 2 | none | 4 | correct far wall | CLEAN-HALL | The flush console and continuous arch sequence hold together. |
| T01-B | integrated console | 2583502 | 1 | clean single room | none | 4 | 2 | none | 4 | correct far wall | CLEAN-HALL | Same topology remains stable under the second seed. |
| T02-A | far-wall dais | 2582501 | 1 | clean single room | none | 4 | 3 | none | 4 | correct far wall | CLEAN-HALL | The dais is largely omitted, but the single far-end station remains coherent. |
| T02-B | far-wall dais | 2583502 | 2 | clean single room | none | 4 | 3 | none | 4 | multiple locations | DUPLICATE-FAIL | Two console-like stations appear at the far end near the requested dais. |
| T03-A | terminal-wall geometry | 2582501 | 1 | split/multiple bays | none | 3 | 3 | major | 2 | shifted to side bay | TOPOLOGY-FAIL | A foreground pillar reveals a left bay beside a separate right-hand hall. |
| T03-B | terminal-wall geometry | 2583502 | 1 | clean single room | none | 4 | 2 | none | 4 | correct far wall | CLEAN-HALL | Strong terminal-wall wording works when the pillar does not split the frame. |
| T04-A | shallow side-wall topology | 2582501 | 2 | split/multiple bays | left | 3 | 3 | major | 2 | multiple locations | DUPLICATE-FAIL | A left-edge console-like unit appears beside a foreground partition. |
| T04-B | shallow side-wall topology | 2583502 | 1 | clean single room | none | 4 | 2 | none | 4 | correct far wall | CLEAN-HALL | Flat wall panels and pilasters produce a coherent long hall. |
| T05-A | slightly off-center camera | 2582501 | 1 | clean single room | none | 3 | 4 | minor | 4 | correct far wall | CLEAN-HALL | Camera offset creates natural variation; wall terminals remain architectural. |
| T05-B | slightly off-center camera | 2583502 | 1 | clean single room | none | 4 | 4 | none | 4 | correct far wall | CLEAN-HALL | Best camera-offset composition with one far console and no edge copy. |
| T06-A | elevated centered camera | 2582501 | 1 | clean single room | none | 4 | 3 | none | 4 | correct far wall | CLEAN-HALL | Slight elevation favors the left wall without adding another focal station. |
| T06-B | elevated centered camera | 2583502 | 1 | clean single room | none | 3 | 2 | none | 4 | correct far wall | CLEAN-HALL | More centered and tunnel-like; depth remains acceptable but less monumental. |
| T07-A | decorative asymmetry only | 2582501 | 1 | clean single room | none | 4 | 4 | none | 4 | correct far wall | CLEAN-HALL | Wall-attached asymmetry survives while the console stays singular. |
| T07-B | decorative asymmetry only | 2583502 | 1 | clean single room | none | 4 | 3 | none | 4 | correct far wall | CLEAN-HALL | Unequal side panels vary the frame without creating a second station. |
| T08-A | distinctive console + deep hall | 2582501 | 1 | clean single room | none | 4 | 3 | none | 4 | correct far wall | CLEAN-HALL | The red-and-cyan identity remains unique and the hall stays deep. |
| T08-B | distinctive console + deep hall | 2583502 | 1 | clean single room | none | 4 | 3 | none | 4 | correct far wall | CLEAN-HALL | The distinctive console is more prominent but remains at the far wall. |
| T09-A | richer set dressing | 2582501 | 1 | clean single room | none | 4 | 4 | none | 5 | correct far wall | CLEAN-HALL | Banners and a drone add useful asymmetry without duplicating the hero object. |
| T09-B | richer set dressing | 2583502 | 2 | ambiguous | left | 4 | 4 | minor | 3 | multiple locations | DUPLICATE-FAIL | A partial console-like station enters from the left edge beside the center console. |

**Batch result:** 15/20 CLEAN-HALL, 0/20 CLEAN-BUT-STAGEY, 0/20 PARTIAL, and 5/20 DUPLICATE-FAIL or TOPOLOGY-FAIL.

### Family summary

| Family | CLEAN-HALL | CLEAN-BUT-STAGEY | PARTIAL | Duplicate/Topology Fail | Mean depth | Mean symmetry | Interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| T00 — F2 control | 1 | 0 | 0 | 1 | 3.0 | 2.5 | The previous winner did not reproduce twice; one seed exposed a foreground-bay split. |
| T01 — integrated console | 2 | 0 | 0 | 0 | 4.0 | 2.0 | Strongest centered reliability; physically tying the console to the far wall helped. |
| T02 — far-wall dais | 1 | 0 | 0 | 1 | 4.0 | 3.0 | A dais is not yet safe; one seed produced two far-end stations and the clean seed omitted the dais. |
| T03 — terminal-wall geometry | 1 | 0 | 0 | 1 | 3.5 | 2.5 | Stronger far-wall wording alone did not prevent a lateral bay in both seeds. |
| T04 — shallow side-wall topology | 1 | 0 | 0 | 1 | 3.5 | 2.5 | Shallow panels help when the frame stays intact, but one seed still exposed an edge duplicate. |
| T05 — off-center camera | 2 | 0 | 0 | 0 | 3.5 | 4.0 | Best camera-only anti-mirroring variant; locked topology kept the console singular. |
| T06 — elevated camera | 2 | 0 | 0 | 0 | 3.5 | 2.5 | Safe mild perspective variation, but less visibly asymmetric than T05 or T07. |
| T07 — decorative asymmetry | 2 | 0 | 0 | 0 | 4.0 | 3.5 | Best combined production candidate: deep, clean, and visibly less mirrored. |
| T08 — distinctive console | 2 | 0 | 0 | 0 | 4.0 | 3.0 | The unique silhouette improves object identity without reverting to the earlier stage-like result. |
| T09 — richer set dressing | 1 | 0 | 0 | 1 | 4.0 | 4.0 | Banners and a drone work once, but the added complexity reintroduced an edge console once. |

### Exact prompts used

#### T00 — F2 control

~~~text
Wide 16:9 pixel-art game background, one connected sci-fi hall seen from a fixed centered camera. The left wall and right wall are continuous and end at one far wall, forming one room. A single small control console is placed on the centerline at the far wall, with an empty tiled floor between camera and console. Sparse arches and cyan lights, crisp readable pixel art, opaque full-bleed background.
~~~

#### T01 — far-wall integrated console

~~~text
Wide 16:9 pixel-art game background of one deep sci-fi hall viewed from a fixed centered camera. Two continuous side walls extend directly to one full-width far wall, enclosing a single room. A single small command console is built flush into the center of the far wall beneath one cyan display panel. A broad empty reflective floor stretches uninterrupted from the camera to that wall. Shallow wall-mounted arches and cyan light strips provide sparse architectural detail, crisp readable pixel art, opaque full-bleed background.
~~~

#### T02 — attached far-wall dais

~~~text
Wide 16:9 pixel-art sci-fi court hall, one connected deep room viewed from a centered camera. Continuous left and right walls meet one far wall. A shallow raised dais touches the center of the far wall, and one small control console sits on that dais. A large empty reflective tiled floor fills the distance between the camera and dais. Sparse wall-attached arches, dark obsidian surfaces, brushed metal trim, and cyan illumination, crisp readable pixel art, opaque full-bleed background.
~~~

#### T03 — strong terminal-wall geometry

~~~text
Wide 16:9 pixel-art game background showing one very deep sci-fi hall. Parallel continuous side walls extend through the entire depth of the room and visibly terminate against one broad far wall spanning the rear of the scene. One small control console sits at the center of that far wall. The long floor between camera and far wall is open and unobstructed. Architectural details remain shallow and attached to the wall surfaces, with restrained cyan lighting and dark metallic materials, crisp readable pixel art, opaque full-bleed background.
~~~

#### T04 — flat side-wall / shallow-pilaster topology

~~~text
Wide 16:9 pixel-art sci-fi hall, a single long rectangular interior seen from a fixed centered camera. Broad continuous side walls run from foreground to one far wall. The side walls use shallow attached pilasters, narrow cyan light strips, and flat decorative panels while remaining one continuous wall plane. One small command console is centered against the far wall. The reflective floor between camera and console is completely open, crisp readable pixel art, opaque full-bleed background.
~~~

#### T05 — slightly off-center camera

~~~text
Wide 16:9 pixel-art sci-fi court hall viewed from a camera positioned slightly left of the room centerline, looking gently diagonally through one connected hall. Continuous left and right walls still terminate at one far wall. One small control console remains near the center of that far wall. The right side exposes slightly more open reflective floor because of the camera position. Wall architecture stays shallow and continuous, with sparse cyan lighting and dark metallic arches, crisp readable pixel art, opaque full-bleed background.
~~~

#### T06 — mild elevated camera

~~~text
Wide 16:9 pixel-art game background of one deep sci-fi hall viewed from a slightly elevated centered camera, looking gently downward across a broad reflective floor toward one far wall. Continuous left and right walls enclose the hall and terminate at that wall. One small control console is centered at the far end. Shallow arches and cyan wall lights follow the room depth while leaving the floor open, crisp readable pixel art, opaque full-bleed background.
~~~

#### T07 — controlled decorative asymmetry

~~~text
Wide 16:9 pixel-art sci-fi court hall, one deep connected room with continuous side walls meeting one far wall. A single small control console sits at the center of the far wall beyond a broad empty reflective floor. The room structure stays simple and continuous. The left wall carries one tall cyan illuminated panel, while the right wall carries two slim holographic banners at different heights. These decorations remain attached to the wall surfaces. Sparse dark arches and cyan lighting, crisp readable pixel art, opaque full-bleed background.
~~~

#### T08 — distinctive hero identity plus deep hall

~~~text
Wide 16:9 pixel-art game background showing one deep sci-fi hall with continuous left and right walls terminating at one far wall. A single small red-and-cyan command console stands at the center of the far wall. It has a distinctive triangular cyan screen and one small red indicator. A long empty reflective floor separates the camera from the console. Sparse shallow arches and cyan wall lighting emphasize the hall depth, crisp readable pixel art, opaque full-bleed background.
~~~

#### T09 — controlled richer set dressing

~~~text
Wide 16:9 pixel-art sci-fi court hall, one large connected room with continuous side walls ending at one far wall. One small control console is centered at that far wall beyond a broad empty reflective floor. Tall dark arches stay attached to the side walls. Two translucent celestial-map banners hang along the right wall at different depths, while one small surveillance drone floats high near the left wall. Cyan conduits trace the architecture, with restrained metallic detail and deep atmospheric perspective, crisp readable pixel art, opaque full-bleed background.
~~~

### Answers to the handoff questions

1. **Does the original F2 result reproduce at 2/2?** No. It reproduced at 1/2 in this seed pair. The failed seed did not show a clear second console, but a large foreground pillar split the composition into lateral bays. F2 remains a strong starting topology, not a deterministic guarantee.
2. **Does integrating the console into the far wall outperform a freestanding far-wall console?** In this batch, yes: T01 was 2/2 CLEAN-HALL versus T00 at 1/2. Integration appears to reduce the number of plausible places for the hero object.
3. **Can a far-wall dais be restored safely?** Not yet. T02 was 1/2 clean; the other seed produced two far-end stations, and the clean seed barely expressed the requested dais.
4. **Does stronger far-wall language improve reliability?** T03 was 1/2, so stronger terminal-wall wording alone did not beat the control. The foreground partition/bay structure remained a bigger variable.
5. **Are shallow wall-mounted pilasters safer than recessed bay-like architecture?** Only conditionally. T04 produced one excellent clean hall and one left-edge duplicate/topology failure, so shallow wording helps but does not guarantee a single topology.
6. **Can camera-position asymmetry be introduced safely?** Yes in this 2/2 sample. T05 produced the strongest natural asymmetry without a duplicate, although one output had slightly less monumental depth and a minor framing obstruction.
7. **Does mild camera elevation help?** Yes for reliability: T06 was 2/2 CLEAN-HALL. Its visual asymmetry was modest, so elevation is a safer but weaker anti-mirroring lever than lateral camera offset.
8. **Can wall-attached decoration break symmetry safely?** Yes in this 2/2 sample. T07 improved on the earlier asymmetric family D, which was 0/2 clean at 640x360, because the room topology stayed locked and only surface decoration varied.
9. **Can a distinctive console be combined with a deep hall?** Yes. T08 was 2/2 CLEAN-HALL at mean depth 4/5, improving on the earlier F5 display-alcove tradeoff.
10. **How much richer set dressing can be restored?** T09 worked once out of two. Banners and a drone can coexist with the topology, but the second seed returned a partial left-edge console; add these elements incrementally and re-test.

### Ranking and exact winners

Ranked by duplication reliability first, then one-room topology, depth, and useful asymmetry:

1. **T07 — controlled decorative asymmetry:** 2/2 CLEAN-HALL, depth 4, symmetry 3.5. Best balance of the complete target.
2. **T05 — slightly off-center camera:** 2/2 CLEAN-HALL, depth 3.5, symmetry 4. Best camera-only anti-mirroring result.
3. **T08 — distinctive console plus deep hall:** 2/2 CLEAN-HALL, depth 4, symmetry 3. Strong identity without a stage-like collapse.
4. **T01 — far-wall integrated console:** 2/2 CLEAN-HALL, depth 4, symmetry 2. Safest centered duplication baseline.
5. **T06 — mild elevated camera:** 2/2 CLEAN-HALL, depth 3.5, symmetry 2.5. Reliable but still fairly centered.
6. **T02 — far-wall dais:** 1/2 CLEAN-HALL, depth 4, symmetry 3. A useful next-stage experiment, not production-safe yet.
7. **T09 — richer set dressing:** 1/2 CLEAN-HALL, depth 4, symmetry 4. The clean output is attractive, but the edge duplicate makes the family higher risk.
8. **T03 — strong terminal-wall geometry:** 1/2 CLEAN-HALL, depth 3.5, symmetry 2.5. Far-wall emphasis helps only when the frame does not split.
9. **T04 — shallow side-wall topology:** 1/2 CLEAN-HALL, depth 3.5, symmetry 2.5. A good clean result, but the left-edge failure is too close to the reported issue.
10. **T00 — F2 control:** 1/2 CLEAN-HALL, depth 3, symmetry 2.5. Retain as a baseline, not as an unconditional solution.

**Best exact prompt for the combined goal (T07):**

~~~text
Wide 16:9 pixel-art sci-fi court hall, one deep connected room with continuous side walls meeting one far wall. A single small control console sits at the center of the far wall beyond a broad empty reflective floor. The room structure stays simple and continuous. The left wall carries one tall cyan illuminated panel, while the right wall carries two slim holographic banners at different heights. These decorations remain attached to the wall surfaces. Sparse dark arches and cyan lighting, crisp readable pixel art, opaque full-bleed background.
~~~

**Safest exact prompt when duplication reliability is the only priority (T01):**

~~~text
Wide 16:9 pixel-art game background of one deep sci-fi hall viewed from a fixed centered camera. Two continuous side walls extend directly to one full-width far wall, enclosing a single room. A single small command console is built flush into the center of the far wall beneath one cyan display panel. A broad empty reflective floor stretches uninterrupted from the camera to that wall. Shallow wall-mounted arches and cyan light strips provide sparse architectural detail, crisp readable pixel art, opaque full-bleed background.
~~~

### Findings by variable

- **Console integration:** Building the console flush into the far wall (T01) was more reliable than a freestanding far-wall control in this pair.
- **Far-wall emphasis:** T03's stronger terminal-plane wording did not solve the problem when a foreground partition created an alternate bay.
- **Dais placement:** T02 reintroduced duplication once and was often not rendered as a distinct dais. Add a dais only after the simpler topology passes.
- **Shallow versus bay-like architecture:** T04 confirms that attached flat panels can work, but a strong foreground partition or side bay still destabilizes the composition.
- **Lateral camera offset:** T05 is the strongest tested way to reduce mirroring without changing room topology. Keep the offset slight and preserve one terminal wall.
- **Camera elevation:** T06 is a lower-risk, lower-impact asymmetry lever; it changes the view without opening lateral focal zones.
- **Decorative asymmetry:** T07 shows that unequal wall-attached panels/banners can break visual mirroring while retaining one console. This is the preferred production asymmetry pattern from this spike.
- **Distinctive console identity:** T08 suggests that a unique silhouette and restrained color identity help preserve focal-object singularity even in a deep hall.
- **Richer set dressing:** T09 shows that banners and a drone should be added one at a time. Complexity is compatible with the topology, but not yet reliably at once.

### Updated production recipe

1. Define one deep connected room with continuous left and right walls that terminate at one far wall.
2. Put one small command console at that wall; integrate it into the wall when duplication reliability matters most.
3. Keep a broad empty reflective floor between the camera and the console.
4. Keep the first architectural pass shallow and wall-attached: pilasters, panels, light strips, and sparse arches.
5. For a less mirrored composition, use either a slight camera offset (T05) or, preferably, asymmetric wall-attached decoration (T07). Do not add asymmetric wings, side platforms, or separate alcoves.
6. If object identity needs reinforcement, use a distinctive small console as in T08.
7. Add a dais, banners, drones, and other richer set dressing one idea at a time, re-testing after each addition.
8. Inspect the entire 640x360 output, especially the outer 10% of both sides. Reject any candidate with a second hero console or a split-room bay; do not erase or repaint the duplicate locally.
9. If repeated retries remain unstable, use the earlier 512x288 evidence as a lower-risk fallback or run a separate image-anchor/higher-adherence study. Do not silently switch routes inside this prompt experiment.

## Fourth test batch: exact centering at 640x360

The fourth batch held the successful integrated-console scene topology constant and changed only positive centering language. It used ten prompt families × two seeds, width 640, height 360, medium detail, selective outline, no_background false, and no init/reference images, editing, cropping, or retries. The canvas center target was x=320.

Exact x estimates were not recorded because manual inspection did not provide a reproducible pixel-measurement method. The table therefore uses the handoff's categorical bands rather than invented coordinates. `FAR OFF` means the apparent center was more than approximately 64px from x=320.

### Results table

| ID | Family | Seed | Console X | Console offset | Console centering | Room axis X | Room offset | Room centering | Alignment | L/R balance | Consoles | Topology | Depth | Obstruction | Perceptual | Class | Notes |
|---|---|---:|---:|---:|---|---:|---:|---|---|---|---|---|---:|---|---:|---|---|
| T00-A | integrated-console control | 2582501 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | Console and room axis drift right together. |
| T00-B | integrated-console control | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | Baseline topology survives, but it is not centered on the canvas. |
| T01-A | canvas-center language | 2582501 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | “Exact horizontal center of the image” does not overcome the shifted hall axis. |
| T01-B | canvas-center language | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | The console remains aligned with the off-canvas room axis. |
| T02-A | optical-axis language | 2582501 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | Optical-axis wording preserves a coherent but right-shifted composition. |
| T02-B | optical-axis language | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | Console and far-wall axis co-drift rather than separating. |
| T03-A | centered vanishing point | 2582501 |  |  | FAR OFF |  |  | FAR OFF | strongly misaligned | strong imbalance | exactly 1 | split/multiple bays | 3 | major | 1 | DUPLICATE/TOPOLOGY-FAIL | A foreground partition creates a left bay and a right hall despite centered-perspective wording. |
| T03-B | centered vanishing point | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | The room remains coherent but its vanishing axis is shifted right. |
| T04-A | central aisle | 2582501 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | A physical aisle follows the generated off-canvas axis. |
| T04-B | central aisle | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | Floor alignment does not translate the whole room to x=320. |
| T05-A | architectural frame | 2582501 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | The frame centers within the generated hall, not within the canvas. |
| T05-B | architectural frame | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | A larger anchor does not correct the shared rightward translation. |
| T06-A | ceiling spine | 2582501 |  |  | FAR OFF |  |  | FAR OFF | strongly misaligned | strong imbalance | exactly 1 | split/multiple bays | 3 | major | 1 | DUPLICATE/TOPOLOGY-FAIL | The ceiling cue coexists with a foreground partition and alternate lateral bay. |
| T06-B | ceiling spine | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | The vertical cue reinforces the generated axis, not the canvas center. |
| T07-A | equal left/right framing | 2582501 |  |  | FAR OFF |  |  | FAR OFF | strongly misaligned | strong imbalance | exactly 1 | split/multiple bays | 3 | major | 1 | DUPLICATE/TOPOLOGY-FAIL | Equal-space wording does not stop a foreground partition from opening a side bay. |
| T07-B | equal left/right framing | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | The clean output is coherent but visibly shifted right. |
| T08-A | minimal central destination | 2582501 |  |  | FAR OFF |  |  | FAR OFF | strongly misaligned | strong imbalance | exactly 1 | split/multiple bays | 3 | major | 1 | DUPLICATE/TOPOLOGY-FAIL | Removing decorative competition did not prevent a foreground bay split. |
| T08-B | minimal central destination | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | Minimal decoration produces a clean but still off-canvas hall. |
| T09-A | redundant centering hierarchy | 2582501 |  |  | FAR OFF |  |  | FAR OFF | strongly misaligned | strong imbalance | exactly 1 | split/multiple bays | 3 | major | 1 | DUPLICATE/TOPOLOGY-FAIL | Redundant positive alignment language does not prevent the known partition failure. |
| T09-B | redundant centering hierarchy | 2583502 |  |  | FAR OFF |  |  | FAR OFF | aligned | strong imbalance | exactly 1 | clean single room | 4 | none | 2 | CLEAN-OFFCENTER | The console follows the shifted room axis rather than x=320. |

**Batch result:** 0/20 CENTERED-GOLD, 0/20 CENTERED-SILVER, 0/20 OBJECT-ONLY-CENTERED, 0/20 ROOM-ONLY-CENTERED, 15/20 CLEAN-OFFCENTER, and 5/20 DUPLICATE/TOPOLOGY-FAIL.

### Family summary

| Family | GOLD | SILVER | Off-center | Fail | Mean console offset | Mean room offset | Interpretation |
|---|---:|---:|---:|---:|---|---|---|
| T00 — integrated-console control | 0 | 0 | 2 | 0 | FAR OFF (2/2) | FAR OFF (2/2) | Reliable one-room baseline, but both focal and room centers co-drift right. |
| T01 — canvas-center language | 0 | 0 | 2 | 0 | FAR OFF (2/2) | FAR OFF (2/2) | Explicit canvas coordinates did not improve on the baseline. |
| T02 — optical-axis language | 0 | 0 | 2 | 0 | FAR OFF (2/2) | FAR OFF (2/2) | Camera terminology binds the console to the wrong shared axis. |
| T03 — centered vanishing point | 0 | 0 | 1 | 1 | FAR OFF (1/1 clean) | FAR OFF (1/1 clean) | One clean shifted hall and one foreground-bay topology failure. |
| T04 — central aisle | 0 | 0 | 2 | 0 | FAR OFF (2/2) | FAR OFF (2/2) | A physical aisle follows rather than corrects the generated axis. |
| T05 — architectural frame | 0 | 0 | 2 | 0 | FAR OFF (2/2) | FAR OFF (2/2) | A larger anchor centers locally within the same shifted hall. |
| T06 — ceiling spine | 0 | 0 | 1 | 1 | FAR OFF (1/1 clean) | FAR OFF (1/1 clean) | Vertical alignment cues do not solve horizontal translation. |
| T07 — equal left/right framing | 0 | 0 | 1 | 1 | FAR OFF (1/1 clean) | FAR OFF (1/1 clean) | Equal-space language is not reliable and can coexist with a bay split. |
| T08 — minimal destination | 0 | 0 | 1 | 1 | FAR OFF (1/1 clean) | FAR OFF (1/1 clean) | Reducing clutter improves simplicity, not canvas alignment. |
| T09 — redundant hierarchy | 0 | 0 | 1 | 1 | FAR OFF (1/1 clean) | FAR OFF (1/1 clean) | Redundant positive anchors do not compound into exact centering. |

### Exact prompts used

#### T00 — baseline reproduction

~~~text
Wide 16:9 pixel-art game background of one deep sci-fi hall viewed from a fixed centered camera. Two continuous side walls extend directly to one full-width far wall, enclosing a single room. A single small command console is built flush into the center of the far wall beneath one cyan display panel. A broad empty reflective floor stretches uninterrupted from the camera to that wall. Shallow wall-mounted arches and cyan light strips provide sparse architectural detail, crisp readable pixel art, opaque full-bleed background.
~~~

#### T01 — explicit canvas-center language

~~~text
Wide 16:9 pixel-art game background of one deep sci-fi hall viewed straight ahead. Two continuous side walls terminate at one full-width far wall. The exact horizontal center of the image is the architectural center of the hall. One small command console is built into the far wall exactly at the center of the image. The console and the room's central axis align on the same vertical centerline of the frame. A broad empty reflective floor fills the space between camera and far wall. Sparse shallow arches and cyan lights, crisp readable pixel art, opaque full-bleed background.
~~~

#### T02 — optical-axis wording

~~~text
Wide 16:9 pixel-art sci-fi hall viewed from a straight-on fixed camera. The camera's optical axis runs through the exact center of the room and directly through one small command console built into the far wall. The console, center of the far wall, and camera axis form one straight line through the middle of the image. Continuous side walls enclose one deep room, with a broad empty reflective floor leading directly toward the console. Sparse wall-mounted arches and cyan lighting, crisp readable pixel art, opaque full-bleed background.
~~~

#### T03 — vanishing-point anchor

~~~text
Wide 16:9 pixel-art sci-fi hall using centered one-point perspective. The single vanishing point lies exactly at the horizontal center of the canvas on the far wall. One small command console is built into that far wall directly over the vanishing point. The floor lines, ceiling lines, and wall depth all converge toward this same centered point. Continuous side walls enclose one room. Sparse dark architecture and cyan illumination, crisp readable pixel art, opaque full-bleed background.
~~~

#### T04 — central aisle

~~~text
Wide 16:9 pixel-art sci-fi hall viewed straight down one central aisle. The aisle begins at the exact lower center of the canvas and runs straight through the middle of the floor to one small console built into the center of the far wall. The aisle, console, far-wall center, and room axis remain perfectly aligned. Continuous left and right walls frame one deep room. Sparse shallow arches and cyan lighting, crisp readable pixel art, opaque full-bleed background.
~~~

#### T05 — centered architectural frame

~~~text
Wide 16:9 pixel-art sci-fi hall, one deep connected room viewed straight ahead. At the exact center of the far wall is one tall architectural frame containing one small integrated command console. This central frame is the primary architectural anchor of the entire composition and sits exactly on the vertical centerline of the image. Continuous side walls extend evenly toward it, with open reflective floor in front. Sparse cyan lighting and shallow wall detail, crisp readable pixel art, opaque full-bleed background.
~~~

#### T06 — centered ceiling spine

~~~text
Wide 16:9 pixel-art sci-fi hall with one continuous room viewed from a centered camera. A narrow illuminated ceiling spine runs exactly along the middle of the ceiling toward the center of the far wall. Directly beneath its endpoint, one small command console is built into the far wall. The ceiling spine, console, and room axis share the exact vertical centerline of the canvas. Broad empty reflective floor and continuous side walls emphasize the centered depth, crisp readable pixel art, opaque full-bleed background.
~~~

#### T07 — equal left/right framing

~~~text
Wide 16:9 pixel-art sci-fi hall viewed straight ahead. One deep room fills the frame with equal visible architectural width on the left and right sides of the central axis. Continuous side walls terminate at one far wall. One small command console is integrated into the exact middle of that wall and appears with equal horizontal room space to its left and right. A broad empty reflective floor leads toward it. Sparse shallow arches and cyan illumination, crisp readable pixel art, opaque full-bleed background.
~~~

#### T08 — central destination without decorative competition

~~~text
Wide 16:9 pixel-art game background, one long rectangular sci-fi hall viewed directly from its center. Continuous plain side walls lead to one flat far wall. One small command console is built into the exact center of the far wall and is the only focal feature in the room. The open reflective floor, wall geometry, and ceiling all lead directly toward the center of the canvas. Minimal cyan light strips, no prominent side landmarks, crisp readable pixel art, opaque full-bleed background.
~~~

#### T09 — redundant centering hierarchy

~~~text
Wide 16:9 pixel-art sci-fi hall viewed directly straight ahead from the exact center of one connected room. The camera axis, central floor aisle, one-point-perspective vanishing point, center of the far wall, and one small wall-integrated command console all occupy the same vertical centerline through the exact middle of the canvas. Equal room width is visible to the left and right of this axis. Continuous side walls terminate at the far wall, and a broad empty reflective floor remains unobstructed between camera and console. Sparse shallow architecture and cyan lighting, crisp readable pixel art, opaque full-bleed background.
~~~

### Answers to the centering questions

1. **Does “center of the image” outperform “center of the room”?** No. T01 and T00 were both 2/2 clean but FAR OFF in both console and room-axis categories.
2. **Does optical-axis terminology improve centering?** No. T02 was 2/2 clean but both outputs remained FAR OFF; the console followed the shifted hall axis.
3. **Is a centered one-point vanishing point the strongest geometric anchor?** No. T03 produced one clean off-center hall and one foreground-bay topology failure. It also increased the risk of objectionable bilateral/partitioned architecture.
4. **Does a physical floor aisle improve center adherence?** No. T04 was 2/2 clean but FAR OFF; the aisle reinforced the wrong axis.
5. **Does a centered architectural frame work better than centering the small object directly?** No. T05 was 2/2 clean but FAR OFF. The frame and console centered within the generated room, not within the canvas.
6. **Do multiple aligned vertical cues improve reliability?** No. T06 was 1/2 clean off-center and 1/2 topology-fail; the ceiling cue did not correct horizontal translation.
7. **Does equal-left/right-space language improve canvas centering?** No. T07 was 1/2 clean off-center and 1/2 topology-fail.
8. **Is visual clutter responsible for the off-centering?** No. T08's minimal scene was still FAR OFF in its clean output, and its other output split into bays.
9. **Does redundant centering language help or hurt?** It does not help. T09 was 1/2 clean off-center and 1/2 topology-fail; redundancy did not compound into a reliable constraint.

### Geometric and perceptual diagnosis

- **Geometric centering:** No output reached CENTERED-GOLD or CENTERED-SILVER. In all clean outputs, both console and room axis were FAR OFF to the right of x=320.
- **Console-to-room relationship:** The console was usually aligned with the generated room axis. This is not primarily an independent console-placement failure.
- **Perceptual centering:** Clean outputs scored 2/5: visibly off-center at first glance. Topology failures scored 1/5 because the foreground partition made the imbalance stronger.
- **Most important diagnosis:** The remaining problem is primarily the inability to keep the entire indoor composition centered on the canvas while preserving the hall topology. Pixen often generates a coherent room and then translates that shared room/console axis rightward; foreground architecture can additionally create a separate lateral bay.

### Best exact prompt and best centering phrase

No prompt achieved the handoff's preferred centering success, so there is no true centering winner. The **best available exact prompt** is T01 because it retained a clean single-room result in both seeds while directly testing canvas-center language:

~~~text
Wide 16:9 pixel-art game background of one deep sci-fi hall viewed straight ahead. Two continuous side walls terminate at one full-width far wall. The exact horizontal center of the image is the architectural center of the hall. One small command console is built into the far wall exactly at the center of the image. The console and the room's central axis align on the same vertical centerline of the frame. A broad empty reflective floor fills the space between camera and far wall. Sparse shallow arches and cyan lights, crisp readable pixel art, opaque full-bleed background.
~~~

The **best centering phrase is none**: canvas center, optical axis, vanishing point, aisle, frame, ceiling spine, equal margins, and redundant alignment all remained FAR OFF in their clean outputs. The useful reusable language is still the positive topology chain—continuous walls, one far wall, open floor, one integrated console—but it solves uniqueness and room coherence, not exact pixel centering.

## Fifth test batch: prompt-only Pro centering

The fifth batch followed the supplied handoff's ten concise prompts exactly. Each prompt was run once through the Pro model with width 640, height 360, `no_background: false`, no seed, no reference image, and no style override. The only intentional variable was prompt wording. The evaluation used the handoff's categories: canvas centering, single-room topology, focal-object count, mirroring/duplication, depth, and overall verdict.

### Results table

| Attempt | Prompt label | Centering | Topology | Focal count | Mirroring | Depth | Verdict | Notes |
|---|---|---|---|---:|---|---:|---|---|
| A01 | centered baseline | Perfect | clean single room | 1 | None | 4 | PASS | Broad floor, continuous walls, and a centered far-wall console; safest baseline. |
| A02 | centered frame emphasis | Perfect | clean single room | 1 | None | 3 | ALMOST | Centered and clean, but the room reads shallower and more court-like. |
| A03 | vanishing-point emphasis | Perfect | clean single room | 1 | None | 5 | PASS | Deepest hall in the batch; the far console is small but unambiguous. A near-white side perimeter prevents strict full bleed. |
| A04 | optical-axis wording | Near | clean single room | 1 | None | 5 | ALMOST | Centered long hall, but the output has the largest white padding: about 45px at each side and 18px at top/bottom. |
| A05 | symmetrical frame, singular subject | Perfect | clean single room | 1 | None | 3 | ALMOST | Balanced and centered, but shallow enough to feel like a vestibule or stage; it also has a near-white perimeter. |
| A06 | central aisle emphasis | Perfect | clean single room | 1 | None | 5 | PASS | Strong central aisle and deep perspective; the far console remains singular. |
| A07 | integrated-console emphasis | Perfect | clean single room | 1 | None | 4 | PASS | Best balance of readable console, depth, centered axis, and clean topology. |
| A08 | minimal topology lock | Perfect | clean single room | 1 | None | 4 | PASS | Minimal topology holds; the rear control station is singular and centered, but about 10px of near-white side padding remains. |
| A09 | restrained asymmetry | Perfect | clean single room | 1 | None | 4 | PASS | Side equipment differs left/right without creating a second bay or focal console; about 7px of near-white side padding remains. |
| A10 | strongest concise instruction | Perfect | clean single room | 1 | None | 4 | PASS | Readable centered console; right-side window detail does not split the hall. |

**Batch result:** 9/10 CENTERED-GOLD, 1/10 CENTERED-NEAR, 0/10 CENTERED-OFF; 10/10 clean single rooms; 10/10 exactly one focal console/station; 10/10 no mirrored second bay or duplicate focal console; 5/10 full bleed and 5/10 with a near-white perimeter; 8/10 PASS and 2/10 ALMOST.

The focal count treats ordinary wall terminals, monitors, and side equipment as room dressing. It counts only a second hero console or station that competes with the requested far-wall focal object as duplication.

### Exact Pro prompts used

#### A01 — centered baseline

~~~text
Wide 16:9 pixel-art sci-fi hall. One single connected room. Front-on centered camera. Continuous left and right walls meet one far wall. One small control console is exactly centered on the far wall. Broad empty floor in front. The entire room composition is centered on the canvas. No duplicate console.
~~~

#### A02 — centered frame emphasis

~~~text
Wide 16:9 pixel-art sci-fi court hall. One deep room only. The room is centered in the frame with equal space on the left and right. One small console sits at the exact center of the far wall. Continuous side walls, open floor, sparse cyan lights.
~~~

#### A03 — vanishing point emphasis

~~~text
Wide 16:9 pixel-art sci-fi interior. One long hall only. One-point perspective with the vanishing point at the exact center of the image. One small command console is centered at that vanishing point on the far wall. Continuous side walls, open reflective floor.
~~~

#### A04 — optical axis wording

~~~text
Wide 16:9 pixel-art sci-fi hall. A single deep room aligned to the image center. The architectural axis and focal console are exactly on the canvas centerline. One small console on the center of the far wall. No mirrored side bay, no second console.
~~~

#### A05 — symmetrical frame, singular subject

~~~text
Wide 16:9 pixel-art sci-fi hall viewed straight on. The room is perfectly centered in the image. Left and right walls balance evenly and end at one far wall. One and only one small console is centered on the far wall. Deep floor space, sparse architecture.
~~~

#### A06 — central aisle emphasis

~~~text
Wide 16:9 pixel-art sci-fi hall. One connected room with a central aisle leading straight to one small centered console on the far wall. The aisle, room axis, and console are centered on the canvas. Continuous walls, minimal detail, deep perspective.
~~~

#### A07 — integrated-console emphasis

~~~text
Wide 16:9 pixel-art sci-fi hall. One deep centered room. A single small command console is built flush into the exact center of the far wall. Broad empty floor in front. Continuous side walls. The entire composition is centered in the frame. No duplicate focal object.
~~~

#### A08 — minimal topology lock

~~~text
Wide 16:9 pixel-art sci-fi room. One rectangular hall only. Straight-on centered camera. Continuous wall planes on both sides and one far wall. One small centered console at the rear center. Very clear centered framing, no side bay duplication, no extra station.
~~~

#### A09 — restrained asymmetry

~~~text
Wide 16:9 pixel-art sci-fi hall. One single centered room. One small console centered on the far wall. The overall hall is centered on the canvas, but the wall decorations are slightly different left versus right. Continuous side walls, open floor, sparse cyan lights.
~~~

#### A10 — strongest concise instruction

~~~text
Wide 16:9 pixel-art sci-fi hall. Keep the whole room centered on the canvas. One room only. One centered far wall. One small console exactly centered on that wall. Continuous left and right walls. Open floor. No mirrored composition. No duplicate console.
~~~

### Answers to the Pro handoff questions

1. **Did prompt-only Pro solve both remaining problems?** Yes in this ten-call sample. Every output was a single connected room with one centered focal console and no mirrored or duplicated focal composition. It did not guarantee full bleed: half the outputs had visible near-white canvas padding.
2. **Which attempt worked best overall?** A07. Its integrated far-wall console is readable without becoming a foreground object, and the room retains depth 4/5.
3. **Which was best-centered?** A01 is the cleanest centered baseline with depth 4/5 and no presentation artifact. A03 and A06 matched its centering while providing deeper perspective.
4. **Which was best for non-duplication?** All ten tied under the focal-object rubric. A07 is the safest reusable choice because its flush far-wall placement gives the model the fewest alternate focal locations.
5. **Should a Pro prompt become the default?** Yes for high-value 640x360 indoor backgrounds where exact centering matters. Use A07 as the default Pro prompt, and keep the Pixen recipe for cost-sensitive generation.

### What changed relative to Pixen

- Pro obeyed the same class of concise positive constraints that Pixen could not reliably honor: one connected room, continuous walls, one far wall, one centered focal object, and whole-canvas centering.
- The difference was not a single magic centering phrase. All ten short formulations succeeded, including the plain baseline and the integrated-console wording. The best-supported explanation is that Pro follows concise spatial and singularity instructions more reliably than Pixen/new; this is a route-level adherence finding, not a claim about undocumented internals or a proven lexical winner.
- The remaining Pro imperfections were presentation tradeoffs, not the reported duplication bug: A02 and A05 were shallow, A03 and A06 made the console very small, and A03/A04/A05/A08/A09 had near-white perimeter padding. A04 was the most severe case.
- `no_background: false` means an opaque scene rather than a transparent cutout; it does not enforce edge-to-edge artwork. The original handoff prompts omitted a full-bleed constraint, while the four explicit full-bleed follow-ups succeeded, so the border behavior is prompt-sensitive in this evidence set rather than an unavoidable Pro defect.
- The full-bleed follow-ups qualify that framing result: once the prompt explicitly said that artwork must touch all four edges and forbade white margins/letterboxing, all four follow-up outputs occupied the complete canvas. This makes explicit full-bleed wording the current recommended fix for the border issue, with edge validation retained as a safety check.
- The cost is substantial. The tool reported 40 generations per Pro call, so the ten-call centering batch plus all three two-call follow-ups consumed 560 reported generation units. Pro is therefore a targeted solution for important backdrops, not a blanket replacement for Pixen.

## Sixth test batch: explicit full-bleed wording

The sixth batch tested whether the white perimeter could be reduced without changing the successful Pro topology. It used two prompt-only attempts at width 640, height 360, `no_background: false`, no seed, no reference image, and no style override. The only new intervention was explicit positive edge-to-edge language paired with short border/letterbox exclusions.

### Results table

| Attempt | Prompt label | Centering | Topology | Focal count | Mirroring | Depth | Full bleed | Verdict | Notes |
|---|---|---|---|---:|---|---:|---|---|---|
| F01 | positive full-bleed surfaces | Perfect | clean single room | 1 | None | 4 | Yes | PASS | Continuous dark wall, ceiling, and floor reach all four edges; console is centered and singular. |
| F02 | edge-to-edge canvas wording | Perfect | clean single room | 1 | None | 4 | Yes | PASS | Artwork fills the canvas edge-to-edge; one centered station and no split hall. |

**Batch result:** 2/2 full bleed, 2/2 clean single rooms, 2/2 exactly one focal console/station, 2/2 no mirrored or duplicated focal composition, and 2/2 centered. An ImageMagick edge-pixel/trim check found both images occupied the complete 640x360 canvas and had non-white corner pixels.

### Exact prompts used

#### F01 — positive full-bleed surfaces

~~~text
Full-bleed 640x360 pixel-art sci-fi game background. Artwork touches all four edges of the canvas with continuous dark wall, ceiling, and floor surfaces. No white border, no white margin, no inset frame, no letterboxing. One deep centered room. A single small command console is built flush into the exact center of the far wall. Broad empty floor in front. Continuous side walls. The entire composition is centered in the frame. No duplicate focal object.
~~~

#### F02 — edge-to-edge canvas wording

~~~text
Edge-to-edge 16:9 pixel-art sci-fi hall background filling the entire canvas. The room's wall, floor, and ceiling surfaces extend to every image edge; no white canvas, border, margin, frame, or letterbox. One connected deep centered hall, continuous side walls, one far wall, one small console at the exact center of the far wall, broad open floor, no duplicate station.
~~~

### Interpretation

- Explicit positive surface-continuity wording is the first tested prompt change to address the white-edge failure directly, and it succeeded in both attempts.
- The fix did not require changing `no_background`; both calls remained opaque scene generations.
- This is a small follow-up, not a probability estimate. Keep the edge-pixel acceptance check and retain crop/reframe as the deterministic fallback for any future padded result.

## Seventh test batch: optimized original prompts

This batch rewrote the user's two original prompts instead of merely appending a generic negative clause. The solar-flare prompt received continuous edge coverage and a singular sun/horizon. The court-hall prompt received the same edge coverage plus a straight-on centered camera, one connected room, one far wall, one dais, and one console. Decorative detail was kept but constrained to wall-attached or secondary elements so it could not create a second lateral room.

### Results table

| ID | Domain | Full bleed | Singular structure | Duplication | Verdict | Notes |
|---|---|---|---|---|---|---|
| P01 | solar-flare landscape | Yes | one sun and one horizon | None | PASS | Sky and volcanic ground reach all four edges; one solar disc and one continuous landscape read clearly. |
| P02 | sci-fi court hall | Yes | one connected room, one dais, one console | None | PASS | Straight-on centered hall reaches all edges; continuous walls do not split into mirrored bays. |

**Batch result:** 2/2 full bleed, 2/2 singular focal structures, 2/2 without duplicated or split composition, and 2/2 visually usable at 640x360. The edge-pixel/trim check found both PNGs occupied the complete canvas with non-white corners.

### Optimized prompts used

#### P01 — solar flare

~~~text
Full-bleed 640x360 pixel-art game background. The sky, atmosphere, and volcanic ground continue to all four edges of the canvas. No white border, no white margin, no inset frame, no letterboxing. One single desolate alien landscape during a violent solar flare. A single massive erupting sun hangs low on the distant horizon; no second sun and no duplicated horizon. Jagged obsidian rock formations and deep glowing fissures lead across the foreground. The sky is a continuous gradient of searing orange, deep violet, and blinding yellow with wisps of ionized gas. Crystalline dust and restrained heat haze texture the ground. Wide cinematic composition, full scene to the edges.
~~~

#### P02 — court hall

~~~text
Full-bleed 640x360 pixel-art game background. The artwork reaches all four canvas edges; no white border, margin, frame, or letterbox. One single connected deep sci-fi court hall viewed straight-on from the south entrance with a centered camera. Continuous left and right walls terminate at one far wall; one central vanishing axis and broad reflective floor. One raised dais at the center of the far wall holds one unique floating control console with tactile backlit buttons and metallic levers. Use wall-attached obsidian and chrome arches, sparse cyan conduits, and a few holographic celestial maps. Keep the side walls continuous; no mirrored hall, split bay, duplicate dais, duplicate console, or rows of separate rooms. Add a few small surveillance drones tethered near the ceiling without creating another focal object. Deep atmospheric perspective, full scene to the edges.
~~~

### Interpretation

- The full-bleed clause transferred from the controlled hall fix to both a landscape and a detailed indoor hall: 2/2 outputs reached the complete canvas.
- The landscape benefited from explicitly singularizing the sun and horizon. The hall benefited more from topology constraints than from additional decorative description.
- Replacing “rows of receding doorways” with continuous wall-attached architecture is deliberate: repeated lateral doorways are a plausible source of alternate room-bay interpretations.
- This is cross-domain validation, not a guarantee. Keep the edge-pixel check and reject any output with a near-white perimeter or duplicate focal structure.

### Production recommendation after 94 calls

1. For a 640x360 scene where exact canvas centering, no duplication, and full bleed are hard requirements, use the full-bleed prefix plus scene-specific singular/topology constraints, width 640, height 360, and `no_background: false`; omit seed and references.
2. For cost-sensitive work, use the Pixen continuous-wall/far-wall recipe. It is the best tested one-console workaround, but the fourth Pixen batch shows that prompt-only centering is not reliable there.
3. Inspect the full frame and its edge pixels before accepting a result. Reject any second hero console, split-room bay, stage-like shallow composition, or unwanted canvas padding; do not try to erase a duplicate locally as part of this workflow. “Opaque” is not the same as “full bleed.”
4. For halls, explicitly state one connected room, continuous side walls, one far wall, one focal console, and a centered camera. Keep repeated doorways and lateral bays out of the foreground.
5. If Pro misses exact placement or full bleed in a future theme, stop spending retries on synonyms and escalate to a composition/reference image or a generate-then-crop/reframe workflow.
6. Keep route comparisons separate: do not mix Pro, image anchoring, cropping, and post-generation repositioning into the Pixen prompt-only rates.

## Limitations

- Pro was tested in one ten-call prompt-only centering batch plus three two-call follow-ups, with one unseeded call per prompt. No PixFlux, init-image, reference-image, website/editor, crop/reframe, or engine-side comparison was run.
- There were two replicates per prompt/detail cell in the first follow-up batch and two replicates per family in each of the third and fourth batches. The Pro centering batch had one call per prompt, and each follow-up had two calls total. The result is directional, not a model-wide probability estimate.
- Same-seed calls provide a useful control but do not establish pixel identity across size or prompt changes.
- Visual centering and duplication scoring was manual. A side terminal can be semantically ambiguous, so the counts distinguish obvious hero-console duplication from normal wall equipment. A simple edge-pixel/trim check was used for the Pro padding observations: five outputs in the original ten-call batch had a near-white perimeter, while all four full-bleed follow-up outputs occupied the complete 640x360 canvas.
- The study used one sci-fi indoor-room theme. Fantasy halls, shops, bedrooms, and industrial interiors may have different failure rates.
- The study did not test image editing, local scaling, or engine-side presentation.

## Reproduction record

This tracked research note records the live-test counts, settings, seed values, exact follow-up prompts, visual scoring rule, Pro handoff prompts, full-bleed follow-up prompts, optimized original prompts, and conclusions. It is intentionally self-contained so the findings do not depend on private run records or untracked output paths.

## Sources

- User-supplied issue transcript and attached example images.
- [PixelLab MCP documentation](https://api.pixellab.ai/mcp/docs) — current create_image_pixen and create_image_pro fields, size rules, async lifecycle, and cost labels.
- [PixelLab REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) — current Pixen endpoint size contract.
- [PixelLab background and wallpaper model research](pixellab-background-wallpaper-model-research-spike.md) — broader model-routing context; this spike narrows the question to indoor composition duplication.
- [Inline negative prompting best practices](pixellab-inline-negative-prompting-best-practices.md) — route-specific caution about treating inline exclusions as probabilistic guidance rather than structural enforcement.
