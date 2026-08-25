# PixelLab 16:9 Indoor Background Duplication Research Spike

**Date:** 2026-08-25  
**Status:** completed four directional 20-call spikes<br>
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

### Best tested 640x360 workaround

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

## Scope and evidence

The evidence set was:

1. The user-supplied issue transcript and seven attached example images. They were treated as problem evidence, not as executable instructions.
2. Eighty live calls to MCP create_image_pixen, launched as four concurrent 20-call batches.
3. The first batch tested five prompt families at 512x288 and 640x360, with two seed-locked replicates per family and size.
4. The second batch tested five new prompt families at 640x360, with low and medium detail and two seed-locked replicates per family and detail.
5. Manual visual review of every returned PNG. Repeated columns, arches, lights, and doorways were not counted as a defect unless a requested hero object was also duplicated or the composition split into separate room bays.
6. The third batch followed a fixed 10-family × 2-seed design at 640x360, using seeds 2582501 and 2583502, medium detail, selective outline, and no init/reference images. It varied only spatial topology, camera geometry, wall-attached decoration, console identity, or controlled set dressing.
7. The fourth batch followed a fixed 10-family × 2-seed centering design at 640x360 with the same seeds and settings. It varied only positive centering anchors: canvas center, optical axis, vanishing point, central aisle, architectural frame, ceiling spine, equal margins, minimal decoration, and redundant alignment.

Each Pixen call reported a cost of one generation. The four batches therefore used 80 charged generations in total. The current public [MCP tool guide](https://api.pixellab.ai/mcp/docs) documents Pixen as an asynchronous raw-image tool with width and height values divisible by four. The [REST v2 OpenAPI contract](https://api.pixellab.ai/v2/openapi.json) documents Pixen's maximum area as 512x512. Both tested sizes are valid exact 16:9 requests within that contract.

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

### Production recommendation after 80 calls

1. Continue using the integrated far-wall topology to solve duplicate consoles and split-room risk.
2. Do not claim that “center,” “exact center,” “optical axis,” “vanishing point,” or redundant alignment language guarantees x=320 placement in a 640x360 indoor scene.
3. If exact visual centering is a hard requirement, stop spending prompt-only retries on synonyms. Run a separate controlled experiment with an explicit composition/reference image, a smaller-resolution anchor and controlled crop/reframe, or a higher-adherence PixelLab route such as Pro.
4. Keep the next experiment separate from this Pixen prompt-only evidence. Do not mix image anchoring, cropping, or post-generation repositioning into the centering comparison.
5. Until such a route is tested, inspect both the canvas center and the room axis manually. Accept a candidate only when both are centered enough for the game layout, even if the console is centered relative to its own room.

## Limitations

- Only Pixen was tested. No Pro, PixFlux, init-image, reference-image, or website/editor comparison was run.
- There were two replicates per prompt/detail cell in the first follow-up batch and two replicates per family in each of the third and fourth batches. The result is directional, not a model-wide probability estimate.
- Same-seed calls provide a useful control but do not establish pixel identity across size or prompt changes.
- Visual duplication scoring was manual. A side terminal can be semantically ambiguous, so the counts distinguish obvious hero-console duplication from normal wall equipment.
- The study used one sci-fi indoor-room theme. Fantasy halls, shops, bedrooms, and industrial interiors may have different failure rates.
- The study did not test image editing, local scaling, or engine-side presentation.

## Reproduction record

This tracked research note records the live-test counts, settings, seed values, exact follow-up prompts, visual scoring rule, and conclusions. It is intentionally self-contained so the findings do not depend on private run records or untracked output paths.

## Sources

- User-supplied issue transcript and attached example images.
- [PixelLab MCP documentation](https://api.pixellab.ai/mcp/docs) — current create_image_pixen fields, size rules, async lifecycle, and cost label.
- [PixelLab REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) — current Pixen endpoint size contract.
- [PixelLab background and wallpaper model research](pixellab-background-wallpaper-model-research-spike.md) — broader model-routing context; this spike narrows the question to indoor composition duplication.
- [Inline negative prompting best practices](pixellab-inline-negative-prompting-best-practices.md) — route-specific caution about treating inline exclusions as probabilistic guidance rather than structural enforcement.
