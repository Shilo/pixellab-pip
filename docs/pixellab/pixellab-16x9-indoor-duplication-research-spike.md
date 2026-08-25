# PixelLab 16:9 Indoor Background Duplication Research Spike

**Date:** 2026-08-25  
**Status:** completed two directional 20-call spikes  
**Question:** Why do wide indoor backgrounds sometimes contain duplicated consoles or repeated room compositions, and what prompt/size pattern is the most reliable workaround?

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
2. Forty live calls to MCP create_image_pixen, launched as two concurrent 20-call batches.
3. The first batch tested five prompt families at 512x288 and 640x360, with two seed-locked replicates per family and size.
4. The second batch tested five new prompt families at 640x360, with low and medium detail and two seed-locked replicates per family and detail.
5. Manual visual review of every returned PNG. Repeated columns, arches, lights, and doorways were not counted as a defect unless a requested hero object was also duplicated or the composition split into separate room bays.

Each Pixen call reported a cost of one generation. The two batches therefore used 40 charged generations in total. The current public [MCP tool guide](https://api.pixellab.ai/mcp/docs) documents Pixen as an asynchronous raw-image tool with width and height values divisible by four. The [REST v2 OpenAPI contract](https://api.pixellab.ai/v2/openapi.json) documents Pixen's maximum area as 512x512. Both tested sizes are valid exact 16:9 requests within that contract.

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

## Limitations

- Only Pixen was tested. No Pro, PixFlux, init-image, reference-image, or website/editor comparison was run.
- There were two replicates per prompt/detail cell in the follow-up batch. The result is directional, not a model-wide probability estimate.
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

