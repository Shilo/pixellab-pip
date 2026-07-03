# Cost Routing

Read this when the user says cheap, cheaper, affordable, low-cost, budget, minimize credits, save generations, avoid Pro, cheapest acceptable, or similar wording. Also read it when the user asks for a cost-driven comparison between Pro and a `new`, v3, standard, Pixen, PixFlux, or BitForge route. For normal route selection without cost concern, use `SKILL.md` and the matching asset reference instead of loading this file solely because an endpoint has a Pro/new/v3 label.

The cost-sensitive rule is: satisfy the user's asset intent with the lowest documented-cost route that is likely to work, then report the tradeoff. Do not silently upgrade to Pro just because it is the usual highest-quality route.

Cheap mode also changes retry behavior. A first approved generation is not permission for open-ended paid iteration. Before each additional paid attempt that spends more generations, ask for permission unless the user already approved a concrete budget, candidate count, or attempt count.

## Cost Labels

Treat these labels as route-selection hints, not provider internals:

- `standard`, `new`, `v3`, Pixen, PixFlux, BitForge, and other documented non-Pro routes are cheap-family hints when they fit the task, but route by the concrete endpoint/tool rather than by the label alone.
- `Pro`, `pro`, Pro Tools, and endpoint names ending in `-pro` or `-v2` with a Pro summary are the expensive family unless current docs say otherwise.
- `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `create-ui-asset`, `create-character-pro`, `image-to-pixelart-pro`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `inpaint-v3`, `edit-images-v2`, `generate-8-rotations-v2`, 1/8-direction object creation, and object Pro animation should be treated as expensive or potentially expensive.
- `v3` is not automatically cheap: REST `inpaint-v3` is documented as Pro. Use the endpoint summary/current docs to classify exceptions.
- `PixPatch` is a website/editor inpaint label, not a public v2 image endpoint. For cheap edits, route to the documented base `inpaint`/edit route when it fits; treat `inpaint-v3` as Pro.
- `Gemini` is stale/low-confidence older website wording for Create Tileset Pro. If current official docs reintroduce a Gemini/external-provider route, treat it as expensive or unknown until current cost is documented or measured; do not use it as a cheap route by default.
- Prompt enhancement calls and inline `enhance_prompt` are small extra costs when exposed; use one enhancement path and skip optional enhancement when the user prioritizes cheapest possible output unless prompt quality risk is high and you explain the added cost.

## Current Cost Findings

These were checked against the official REST v2 OpenAPI and MCP docs on 2026-06-29:

- Character 8-direction standard mode costs 1 generation; character `pro` costs 20-40 generations depending on size.
- `create-character-v3` costs `ceil(width * height * 8 / 65536)` generations when rotating a reference image, or `1 + ceil(size * size * 8 / 65536)` from scratch.
- Character template animation costs 1 generation per direction.
- Character custom/Pro animation costs 20-40 generations per direction. v3 is the default custom animation family and should be preferred for cheap custom animation when available.
- 1/8-direction object creation via MCP `create_1_direction_object`, MCP `create_8_direction_object`, REST `create-1-direction-object`, and REST `create-8-direction-object` uses Pro Tools and costs 20-40 generations per call.
- Map objects via MCP `create_map_object` / REST `POST /map-objects` are documented separately from 1/8-direction object Pro Tools. Current docs do not label them Pro or 20-40 generations; treat map-object cost as unknown/current-doc-dependent and report or measure cost before assuming it is cheap or expensive.
- Object animation `mode='pro'` costs 20-40 generations per direction, or 160-320 generations for a full 8-direction animation. Prefer `mode='v3'`, the documented default, for cheap object animation.
- MCP `create_ui_asset` / REST `create-ui-asset` is documented as Pro and costs 20-40 generations.
- REST summaries label `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `image-to-pixelart-pro`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `inpaint-v3`, `edit-images-v2`, and `generate-8-rotations-v2` as Pro-family routes. Treat them as higher-cost even when exact generation counts are not shown in the summary.
- REST `create-image-pixen`, `create-image-pixflux`, `create-image-pixflux-background`, and `create-image-bitforge` are public image routes whose current summaries are not Pro-labeled. Current docs and product labels use `new` differently by surface/tool, so do not equate `new` with exactly one endpoint without checking the selected surface. Use Pixen for cheap small/single-image/icon iteration when its controls fit, PixFlux for cheap general-image/background-style generation when its route fits, and BitForge only when its image/style route fits better than Pixen/PixFlux.
- REST `animate-with-text-v3` and `generate-8-rotations-v3` are the cheap v3 family when they fit.
- For animation routes, do not lower `frame_count` as a cost optimization unless current docs or a verified pricing response show that frame count changes cost or feasibility. Prefer changing documented cost drivers such as route family, mode, direction count, candidate count, enhancement use, or size when those are available and compatible with the user's request.

If exact current costs matter to the user, refresh official docs or use a small balance-before/balance-after test with explicit approval. Do not invent exact prices for routes whose docs expose only a Pro/new/v3 label.

## Route Preferences

When the user says cheap:

- General images: prefer a fitting non-Pro route such as `create-image-pixen` or `create-image-pixflux` over `generate-image-v2` Pro, unless the request specifically needs Pro-only behavior such as style-reference generation or high-quality sheet output.
- Single small icons: consider Pixen for cheap iteration and explicit outline/detail/view controls. Verify it still reads as the requested icon type.
- Skill-icon or item-icon sheets: Pro `generate-image-v2` can be the best quality route, but if the user asks cheap, propose a lower-cost single-icon/Pixen or non-Pro comparison first, or ask whether quality or credit savings wins. Do not run a large Pro sheet silently under a cheap request.
- Characters: prefer standard mode or v3 over `pro` / `create-character-pro` unless the user accepts the 20-40 generation cost.
- Character animation: prefer template mode when a suitable template exists; otherwise prefer v3/custom defaults before Pro. Animate one direction first unless the user explicitly asks for all directions.
- Objects: 1/8-direction object creation is Pro Tools and expensive. For cheap standalone visual props that do not need managed object IDs, propose a general image/Pixen/PixFlux route or isometric tile route when it matches the art need; label the tradeoff that it will not create a managed PixelLab object. If the user specifically needs a map object, use the map-object route and report/measure cost instead of assuming it has the 1/8-direction object Pro Tools cost.
- Object animation: use `mode='v3'` unless the user explicitly approves Pro.
- UI: `create-ui-asset` is Pro/expensive. For cheap loose UI images, consider `generate-ui-v2` only if current docs/usage make its cost acceptable; otherwise use a non-Pro general-image route and explain the weaker UI-asset structure.
- Image-to-pixel-art: prefer normal `image-to-pixelart` when exact output size fits its current limits; use Pro only when needed and approved.
- Inpainting/editing: prefer non-Pro edit/inpaint routes when they can do the job. Do not assume `inpaint-v3` is cheap from the `v3` suffix; current docs label it Pro. Use Pro edit routes only when their capabilities are required and the user accepts the cost.

## Iteration Permission

When a cheap request needs more paid attempts, ask before spending again. This includes prompt tweaks, reruns for quality, generating more candidates, Pro comparison runs, paid retries after failures, batch expansion, animation pass expansion, or switching to a paid edit route. Report the route/tool you would use, the expected or observed cost category, cost already spent, and what will change in the next attempt.

Do not ask for permission for free/local work such as status polling, downloads, cropping, spritesheet assembly, ZIP packaging, manifest writing, or filesystem verification. For balance checks, no extra permission is needed when the user has already approved live generation and the check is only for cost reporting; for setup, readiness, status-only, or account-data requests, follow `setup.md` and ask before checking balance.

## User-Facing Behavior

When choosing a cheap route, say the tradeoff plainly:

- "Cheap route: standard/v3/new/Pixen/PixFlux where the selected endpoint is non-Pro; lower cost, possibly less candidate variety or weaker Pro-quality details."
- "Quality route: Pro; likely better for this specific sheet/workflow, but higher cost."
- "One more paid iteration would use X and has already spent Y. Continue?"

For live work, still follow `usage-reporting.md`: check balance before/after when cost may not be returned per call, report total cost for the whole flow, and include non-default cost-affecting inputs such as mode, Pro/new/v3 choice, direction count, size, candidate count, and enhancement use.
