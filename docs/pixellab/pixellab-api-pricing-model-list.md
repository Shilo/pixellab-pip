# PixelLab API Pricing and Model List

Last reviewed: 2026-09-13.

This is a quick reference for public PixelLab API endpoint labels, plugin labels, model/tool families, and official estimated USD prices. Treat prices as estimates: PixelLab states that prices vary with GPU processing time. For exact schemas, verify against the live REST v2 docs or OpenAPI.

Primary sources:

- [PixelLab API catalog](https://www.pixellab.ai/pixellab-api)
- [REST v2 docs](https://api.pixellab.ai/v2/docs)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [MCP tool guide](https://api.pixellab.ai/mcp/docs)

## Billing Notes

- Public REST/MCP auth uses the PixelLab bearer token.
- PixelLab account balance can include subscription generations and USD credits.
- Hosted MCP help reports that billing uses subscription generations first, then USD credits.
- Official USD estimates and API `usage.generations` / credit deltas are distinct reporting units unless PixelLab documents a conversion for the selected route.
- The pricing page shows the same estimate two ways: **generations** (the subscription-spend unit, its default view) and the USD values recorded below. Baselines: most base/`new`/`v3` routes ~1 generation; enhancers ~0.05; `estimate-skeleton` ~0.1; top-down and sidescroller tilesets ~3; Pro Tools ~20-40. Size- and frame-driven routes (`create-character-v3`, `generate-8-rotations-v3`, `animate-with-text-v3`, and PixMiniMax) need route-specific estimates — see [cost-routing.md](../../skills/pixellab-pip/references/cost-routing.md).
- Prompt-enhancement endpoints are separately priced when called or enabled through an endpoint option.

## Version 0.4.123 Product Update

- **Pro Flash (Beta):** the single-image option is advertised at 4–6 generations and a maximum size of `256x256`. The current REST OpenAPI describes a provisional five-generation first-image estimate for `POST /v2/create-image-pro-flash`; query `GET /v2/pro-flash/cost` when an estimate matters and report completed-job usage.
- **PixMiniMax:** available to Tier 1+ subscribers and surfaced in Character Creator, Creator, Aseprite, and Pixelorama. Programmatic routing remains REST `POST /v2/animate-pixminimax` or MCP `animate_image_pixminimax`.
- **Game Builder:** available to Tier 1+ subscribers. It is a visible product workflow; public MCP project/chat/sandbox helpers can provide approved project context, but no dedicated public REST v2 Game Builder endpoint is documented. See the [official tutorial/showcase](https://youtu.be/Iaxk_8ftJ5s).
- **Creator queue:** submitted Creator work is queued so closing or changing the window does not discard the job. This is a product/UI behavior, not a new public REST route.
- **Map export:** Map Workshop can export for Godot and Unity. The public REST v2 inventory still has no map or map-export route; MCP map tools remain the programmatic map surface.

## Concurrency and Priority Slots

The account view shows **Concurrent jobs** (labeled with your subscription **tier**) and **priority slots** — concurrent jobs that skip added queue time.

Confirmed mechanism (PixelLab account UI, 2026): priority slots are **earned by sustained parallel usage** on a rolling 30-minute utilization window. The account UI states the rule as: **sustain ≥ 80% utilization for 30 min → +1 slot; drop below 60% for 30 min → -1 slot.** PixelLab's owner confirmed this is a recent addition where "stable usage will increase your concurrency."

Two nuances: utilization is active jobs as a fraction of your limit, **time-averaged over the whole 30-min window** (a short burst barely moves it, so slots reward continuous heavy use, not one big batch); and priority slots only save time **under contention** — when jobs would otherwise queue — so with no queue they change nothing. Practical takeaway: for a one-off batch, running up to your limit in parallel is the fastest option regardless; slot-farming only pays off for sustained continuous workloads.

Observed datapoint: a **Tier 2** account shows a priority-slot **limit of 10**. Unconfirmed: whether that limit differs for Free, Tier 1, or Tier 3. Do not quote a per-tier number you have not verified for that tier; if an exact limit matters, check the live account view or ask PixelLab support.

No API query route: there is **no public REST v2 endpoint that reports your slot count, concurrency, utilization, or a list of active jobs** (verified against the live OpenAPI). Only per-job status (`GET /background-jobs/{job_id}`) and `GET /balance` (generations/credits, not slots) are exposed. The slot/utilization view is UI-only for now: the `pixellab-api` page populates it from internal first-party endpoints (`api-limit-status`, `get-account-data`, `get-subscription-status`) that are not versioned under `/v2/`, use website-session auth, and must not be called programmatically — see SKILL.md "Do Not Use".

Agent behavior on the ceiling (`429`/`529`, batch pacing): see [job-lifecycle.md](../../skills/pixellab-pip/references/job-lifecycle.md).

## Image Generation

| Tool label | Endpoint | Model/tool family | Useful for | Estimated price |
|---|---|---|---|---|
| Create M-XL image (new) | `POST /v2/create-image-pixflux` | Pixflux | General image generation, larger image understanding, init images, forced palettes, transparent background | `64x64 $0.00793`; `128x128 $0.00793`; `320x320 $0.0101`; `400x400 $0.0132`; transparent `64x64 $0.0084`; transparent `128x128 $0.00848` |
| Create M-XL image, background | `POST /v2/create-image-pixflux-background` | Pixflux | Background-oriented pixflux generation; shares the identical `CreateImagePixfluxRequest` schema with the row above | no separate USD row found on the public pricing page — same request schema as `create-image-pixflux`, so likely priced identically; verify with a balance-before/after check before treating this as confirmed |
| Create image S-XL (new) | `POST /v2/create-image-pixen` | Pixen | Cheap text-to-image sprites, outline/detail controls, view/direction, transparent background; focused character tests found weak static south-facing adherence and frequent isometric/3/4 drift | `32x32 $0.007`; `64x64 $0.00718`; `128x128 $0.00793`; `256x256 $0.0089`; `512x512 $0.0169` |
| Generate S-M image (style) | `POST /v2/create-image-bitforge` | Bitforge | Small/medium text-to-image, style image, inpainting, init image, forced palette, transparent background | `32x32 $0.0071`; `64x64 $0.00716`; `128x128 $0.00797`; `200x200 $0.01122`; transparent `32x32 $0.00734`; transparent `64x64 $0.00738`; transparent `128x128 $0.00821`; transparent `200x200 $0.01285` |
| Create S-XL image (Pro) | `POST /v2/generate-image-v2` | Pro image generation | Closer adherence to user instructions than Pixen/v3/new, especially for explicit shape/feature details, plus multiple candidates, reference images, style image, and static south-facing candidates; costs more and produces a different, broader character style | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Generate with style (Pro) | `POST /v2/generate-with-style-v2` | Pro style generation | Matching a reference style across new images | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Create UI elements (Pro) | `POST /v2/generate-ui-v2` | Pro UI generation | Buttons, health bars, slots, menus | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Create UI asset (Pro) | `POST /v2/create-ui-asset` | Structured UI asset generation | Saved UI panels with `pieces`, `elements`, style image, project assignment, and polling | current public pricing page has no USD row; local cost docs treat this as Pro / `20-40` generations |

## Pro Flash (Beta, Provisional Pricing)

The current public REST/MCP docs use the Pro Flash display name. It has not been quality-, latency-, or charge-tested in this repository. It is separate from the older Pro image/edit/character/object routes and should not displace tested defaults because its name suggests speed.

| Operation | REST v2 | MCP | Billing and output distinction |
|---|---|---|---|
| Create one image | `POST /create-image-pro-flash` | `create_image_pro_flash` | One image per call; Version 0.4.123 advertises 4–6 generations, while REST describes a provisional five-generation first-image estimate. Older Pro may return a size-dependent batch. |
| Create character | `POST /create-character-pro-flash` | `create_character_pro_flash` | First south-facing image plus eight V3 views; using an owned prior `source_image_id` avoids the new-image stage, not the rotations. |
| Create object | `POST /create-object-pro-flash` | `create_object_pro_flash` | One or eight directions. Finalizing one direction from an already-paid source image is documented as free; eight directions still incur rotation charges. |
| Edit one image | `POST /edit-image-pro-flash` | `edit_image_pro_flash` | Keeps the input's native canvas dimensions; no published fixed cost here. |
| Masked edit | `POST /inpaint-image-pro-flash` | `inpaint_image_pro_flash` | Source and mask must share native size; no published fixed cost here. Exact outside-mask preservation is claimed, not live-verified. |

Use `GET /v2/pro-flash/cost` with operation, width, height, and direction count for a provisional estimate before a paid call, and `GET /v2/pro-flash/capabilities` (or MCP `get_pro_flash_capabilities`) to check dimensions. The public MCP inventory has no cost-estimator tool. Actual usage comes from the completed job, not the provisional number. The live capability endpoint required bearer auth during this review, so no account-specific response or paid probe is included.

## Image Operations

| Tool label | Endpoint | Useful for | Estimated price |
|---|---|---|---|
| Convert image to pixel art | `POST /v2/image-to-pixelart` | Regular image to pixel art | `64x64 $0.006`; `128x128 $0.00666`; `256x256 $0.01164` |
| Edit image (pixen) | `POST /v2/edit-image-pixen` | Text-instruction edit on the Pixen model; source ≤256px per side, target area ≤256x256 | not covered by the pricing rows recorded here — the endpoint documents a cost of 1 generation |
| Correct pixel art | `POST /v2/correct-pixelart` | Sharpen edges, drop stray pixels, tighten palette without resizing | not covered by the pricing rows recorded here — MCP documents 0.1 generations |
| Reduce colors | `POST /v2/reduce-colors` | Quantize one or more same-size frames onto one shared palette | not covered by the pricing rows recorded here — MCP documents 0.1 generations |
| Unzoom pixel art | `POST /v2/unzoom` | Recover native-resolution pixel art from an upscaled image | not covered by the pricing rows recorded here — MCP documents 0.1 generations |
| Convert image to pixel art (Pro) | `POST /v2/image-to-pixelart-pro` | Pro image-to-pixel-art conversion, exact-size flexibility beyond the base route's limits | no separate USD row found on the public pricing page — treat as Pro-tier cost (comparable to the other `up to 256x256 $0.095`/`341x341 $0.125`/`512x512 $0.185` Pro rows above) until confirmed |
| Resize | `POST /v2/resize` | Pixel-art-aware resizing | `64x64 $0.01788`; `128x128 $0.01777` |
| Remove background | `POST /v2/remove-background` | Transparent PNG foreground extraction | `64x64 $0.00554`; `128x128 $0.00554`; `256x256 $0.00593` |
| Inpaint | `POST /v2/inpaint` | Non-Pro inpainting/editing | `64x64 $0.00716`; `128x128 $0.00797`; `200x200 $0.01122`; transparent `64x64 $0.00738`; transparent `128x128 $0.00821`; transparent `200x200 $0.01285` |
| Edit image | `POST /v2/edit-image` | Text edit on existing pixel art | `64x64 $0.0118` |
| Inpaint (Pro) | `POST /v2/inpaint-v3` | Pro mask-based inpainting | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Edit images (Pro) | `POST /v2/edit-images-v2` | Pro multi-image/reference editing | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |

## Animation

| Tool label | Endpoint | Model/tool family | Useful for | Estimated price |
|---|---|---|---|---|
| Animate with text | `POST /v2/animate-with-text` | Base text animation | 64x64 text animation with init/inpainting/palette options | `64x64`, 4 frames: `$0.01565` |
| Animate with text (new) | `POST /v2/animate-with-text-v3` | v3 text animation | First-frame animation, optional last-frame guidance, 4-16 frames, up to 256x256 | `32x32`, 4 frames: `$0.0221`; `256x256`, 8 frames: `$0.0302`; `128x128`, 16 frames: `$0.0424` |
| Animate with text (PixMiniMax) | `POST /v2/animate-pixminimax` | PixMiniMax animation, publicly disclosed as powered by MiniMax H3 | Tier 1+; beta; first/end frame anchors, 4-40 generated frames in multiples of four, up to 256x256 | Independently observed website estimates (2026-09-12): `64x64`, 4 frames `$0.0123`; 8 `$0.0153`; `256x256`, 8 `$0.0153`; 40 `$0.0471` — see [dated observation](pixellab-pixminimax-website-pricing-observation-2026-09-12.md). REST docs also publish generation-unit examples; use returned `usage.generations` for charged usage. |
| Animate with text (Pro) | `POST /v2/animate-with-text-v2` | Pro text animation | Reference-image animation, 4/9/16 frames, view and direction controls | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Animate with skeleton | `POST /v2/animate-with-skeleton` | Skeleton-guided animation | Pose/skeleton-driven animation up to 256x256 (endpoint prose lists 16/32/64/128/256; priced rows below stop at 128x128) | `32x32 $0.0136`; `64x64 $0.01433`; `128x128 $0.01572` |
| Estimate skeleton | `POST /v2/estimate-skeleton` | Skeleton helper | Skeleton extraction for skeleton animation | `16x16 $0.00511`; `64x64 $0.00513`; `256x256 $0.00516` |
| Edit animation (Pro) | `POST /v2/edit-animation-v2` | Pro animation editing | Apply edits consistently across 2-16 frames | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Interpolate (Pro) | `POST /v2/interpolation-v2` | Pro interpolation | Generate in-between frames | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Transfer outfit (Pro) | `POST /v2/transfer-outfit-v2` | Pro animation transfer | Apply outfit/appearance to animation frames | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Generate vocal animation | `POST /v2/vocal-animation` | Talking portrait / visemes | Generate one mood's mouth-shape set from a managed character portrait or raw portrait | Paid-plan generation; exact public unit/USD estimate not found, so verify current usage before a cost-sensitive call |
| Render talking GIF | `POST /v2/talking-gif` | Talking portrait renderer | Render stored or supplied visemes against dialogue | Free and synchronous |
| Create lip-sync plan | `POST /v2/lip-sync` | Talking portrait timing | Return viseme columns and durations for dialogue | Free and synchronous |

## Rotation, Tiles, Maps, Characters, and Objects

| Tool label | Endpoint | Useful for | Estimated price |
|---|---|---|---|
| Rotate | `POST /v2/rotate` | Rotate object or character | `64x64 $0.01057`; `128x128 $0.01091` |
| Create 8 rotations (new) | `POST /v2/generate-8-rotations-v3` | v3 8-direction sprite rotation | `32x32 $0.0293`; `64x64 $0.0337`; `128x128 $0.0345`; `256x256 $0.0377` |
| Generate 8 rotations (Pro) | `POST /v2/generate-8-rotations-v2` | Pro 8-direction sprite generation/rotation | up to `85x85 $0.095`; up to `113x113 $0.125`; up to `168x168 $0.185` |
| Create top-down tileset | `POST /v2/create-tileset` | Wang/top-down tilesets | `16x16 tiles $0.0079`; `32x32 tiles $0.0099` |
| Create sidescroller tileset | `POST /v2/create-tileset-sidescroller` | Platformer tilesets | `16x16 tiles $0.0079`; `32x32 tiles $0.0099` |
| Create isometric tile | `POST /v2/create-isometric-tile` | One isometric tile | `32x32 $0.0156`; `64x64 $0.0166` |
| Create map object | `POST /v2/map-objects` | Map object generation | per object `$0.0099` |
| Create character with 4 directions | `POST /v2/create-character-with-4-directions` | 4-direction character | `48x48 $0.0105`; `64x64 $0.0122` |
| Create character with 8 directions | `POST /v2/create-character-with-8-directions` | 8-direction character | `48x48 $0.0133`; `64x64 $0.0173` |
| Create character (Pro) | `POST /v2/create-character-pro` | Pro 8-direction character | up to `85x85 $0.095`; up to `113x113 $0.125`; up to `168x168 $0.185` |
| Create character v3 | `POST /v2/create-character-v3` | v3 8-direction character | `64x64 $0.041`; `128x128 $0.042`; `168x168 $0.045` |
| Portrait to character / character to portrait (Pro) | `POST /v2/portrait-character-pro` | Pro portrait-character conversion | Convert a portrait image to a full-body character or the reverse | current public pricing page has no USD row; verify current usage before cost-sensitive calls |
| Set character portrait | `POST /v2/characters/{character_id}/portrait` | Managed portrait attachment | Attach or replace the portrait used by vocal animation | Free and synchronous; replacing an existing portrait is destructive |
| Animate character | `POST /v2/animate-character` | Character animation, per direction | template `64x64 $0.0323`, `128x128 $0.0956`; v3 4 frames `64x64 $0.0129`, `128x128 $0.0145`; Pro up to `128x128 $0.095`, up to `168x168 $0.185` |
| Create character state | `POST /v2/create-character-state` | Character state/variant | up to `84x84 $0.095`; up to `112x112 $0.125`; up to `168x168 $0.185` |
| Create single direction objects | `POST /v2/create-1-direction-object` | Style-consistent object candidates | up to `168x168 $0.095` |
| Create 8 directional objects | `POST /v2/create-8-direction-object` | 8-direction object | up to `84x84 $0.095`; up to `112x112 $0.125`; up to `168x168 $0.185` |
| Animate object | `POST /v2/objects/{object_id}/animations` | Object animation, per direction | v3 4 frames `64x64 $0.0129`, `128x128 $0.0144`; Pro up to `128x128 $0.095`, up to `168x168 $0.185` |
| Create object state | `POST /v2/objects/{object_id}/states` | Object variant/state | single-direction up to `168x168 $0.095`; 8-direction up to `84x84 $0.095`, up to `112x112 $0.125`, up to `168x168 $0.185` |
| Create tiles (Pro) | `POST /v2/create-tiles-pro` | Multiple tile variations; also the shared endpoint behind MCP's `create_path_tiles` (`tile_feature: "roads"`) and `create_building_kit` (`tile_feature: "building"`), which have no REST route or pricing row of their own | tile up to `42x42 $0.095`; up to `56x56 $0.125`; up to `85x85 $0.185`; MCP `create_path_tiles`/`create_building_kit` likely bill on this same Pro rung — unconfirmed, no separate USD row exists to check against |
| Generate pixel font (Pro) | `POST /v2/generate-font-pro` | Pro bitmap font generation | Generate a font atlas / pixel font from description and font controls | fixed 25 subscription generations, or at least `$0.125` when billed to credits |

## Prompt Enhancement

| Tool label | Endpoint | Useful for | Estimated price |
|---|---|---|---|
| Enhance Pixen prompt | `POST /v2/enhance-pixen-prompt` | Expand a Pixen image prompt | official estimate per call `$0.002`; live check observed `usage.generations: 0.05` |
| Enhance character v3 prompt | `POST /v2/enhance-character-v3-prompt` | Expand a v3 character prompt | official estimate per call `$0.002`; treat reported usage/credits as a separate unit |
| Enhance animation prompt | `POST /v2/enhance-animation-v3-prompt` | Expand an animation action using frames as context; `engine=v3` or `engine=pixminimax` | official estimate per call `$0.002`; treat reported usage/credits as a separate unit |

## Practical Routing Notes

- For cheap image prompt iteration, start with Pixflux or Pixen.
- For multiple image candidates from one call, use Pro image generation.
- For first-frame animation or chained VFX animation, prefer `animate-with-text-v3`.
- For an explicit PixMiniMax/MiniMax H3 request, use `animate-pixminimax`; it supports longer clips than v3 but has a distinct cost model and motion-prompt contract.
- For Pro text animation with view/direction fields and a reference image, use `animate-with-text-v2`.
- Exception for duplicate-filled atlases: observed `animate-with-text-v3` runs synchronized repeated cells instead of making them unique phases. `animate-with-text-v2` followed the cell-diversity instruction reasonably well, but produced lower apparent quality and greater color drift. Prefer single-sprite animation plus local atlas assembly; use Pro only as an approved tradeoff candidate.
- For managed character/object assets, prefer the resource-specific character/object endpoints or MCP tools instead of raw image animation endpoints.
