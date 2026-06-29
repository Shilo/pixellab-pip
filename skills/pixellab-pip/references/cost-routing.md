# Cost Routing

Read this when the user says cheap, cheaper, low-cost, budget, minimize credits, save generations, avoid Pro, cheapest acceptable, or similar wording. Also read it when comparing a Pro route to a `new`, v3, standard, or Pixen route.

The cost-sensitive rule is: satisfy the user's asset intent with the lowest documented-cost route that is likely to work, then report the tradeoff. Do not silently upgrade to Pro just because it is the usual highest-quality route.

## Cost Labels

Treat these labels as route-selection hints, not provider internals:

- `standard`, `new`, `v3`, Pixen, and other non-Pro routes are the cheap family when they fit the task.
- `Pro`, `pro`, Pro Tools, and endpoint names ending in `-pro` or `-v2` with a Pro summary are the expensive family unless current docs say otherwise.
- `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `create-ui-asset`, `create-character-pro`, `image-to-pixelart-pro`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `inpaint-v3`, `edit-images-v2`, `generate-8-rotations-v2`, object creation, and object Pro animation should be treated as expensive or potentially expensive.
- Prompt enhancement calls and inline `enhance_prompt` are small extra costs when exposed; use one enhancement path and skip optional enhancement when the user prioritizes cheapest possible output unless prompt quality risk is high and you explain the added cost.

## Current Cost Findings

These were checked against the official REST v2 OpenAPI and MCP docs on 2026-06-29:

- Character 8-direction standard mode costs 1 generation; character `pro` costs 20-40 generations depending on size.
- `create-character-v3` costs `ceil(width * height * 8 / 65536)` generations when rotating a reference image, or `1 + ceil(size * size * 8 / 65536)` from scratch.
- Character template animation costs 1 generation per direction.
- Character custom/Pro animation costs 20-40 generations per direction. v3 is the default custom animation family and should be preferred for cheap custom animation when available.
- Object creation via MCP `create_1_direction_object`, MCP `create_8_direction_object`, REST `create-1-direction-object`, and REST `create-8-direction-object` uses Pro Tools and costs 20-40 generations per call.
- Object animation `mode='pro'` costs 20-40 generations per direction, or 160-320 generations for a full 8-direction animation. Prefer `mode='v3'`, the documented default, for cheap object animation.
- MCP `create_ui_asset` / REST `create-ui-asset` is documented as Pro and costs 20-40 generations.
- REST summaries label `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `image-to-pixelart-pro`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `inpaint-v3`, `edit-images-v2`, and `generate-8-rotations-v2` as Pro-family routes. Treat them as higher-cost even when exact generation counts are not shown in the summary.
- REST `create-image-pixflux` is called "Create image (new)" in plugin wording and is the cheap general-image family when it fits.
- REST `animate-with-text-v3` and `generate-8-rotations-v3` are the cheap v3 family when they fit.

If exact current costs matter to the user, refresh official docs or use a small balance-before/balance-after test with explicit approval. Do not invent exact prices for routes whose docs expose only a Pro/new/v3 label.

## Route Preferences

When the user says cheap:

- General images: prefer `create-image-pixflux` / "new" or Pixen over `generate-image-v2` Pro, unless the request specifically needs Pro-only behavior such as style-reference generation or high-quality sheet output.
- Single small icons: consider Pixen for cheap iteration and explicit outline/detail/view controls. Verify it still reads as the requested icon type.
- Skill-icon or item-icon sheets: Pro `generate-image-v2` can be the best quality route, but if the user asks cheap, propose a lower-cost single-icon/Pixen or `new` comparison first, or ask whether quality or credit savings wins. Do not run a large Pro sheet silently under a cheap request.
- Characters: prefer standard mode or v3 over `pro` / `create-character-pro` unless the user accepts the 20-40 generation cost.
- Character animation: prefer template mode when a suitable template exists; otherwise prefer v3/custom defaults before Pro. Animate one direction first unless the user explicitly asks for all directions.
- Objects: object creation is Pro Tools and expensive. For cheap standalone visual props that do not need managed object IDs, propose a general image/Pixen/new route or isometric tile route when it matches the art need; label the tradeoff that it will not create a managed PixelLab object.
- Object animation: use `mode='v3'` unless the user explicitly approves Pro.
- UI: `create-ui-asset` is Pro/expensive. For cheap loose UI images, consider `generate-ui-v2` only if current docs/usage make its cost acceptable; otherwise use a non-Pro general-image route and explain the weaker UI-asset structure.
- Image-to-pixel-art: prefer normal `image-to-pixelart` when exact output size fits its current limits; use Pro only when needed and approved.
- Inpainting/editing: prefer non-Pro edit/inpaint routes when they can do the job. Use Pro edit routes only when their capabilities are required and the user accepts the cost.

## User-Facing Behavior

When choosing a cheap route, say the tradeoff plainly:

- "Cheap route: v3/new/Pixen/standard; lower cost, possibly less candidate variety or weaker Pro-quality details."
- "Quality route: Pro; likely better for this specific sheet/workflow, but higher cost."

For live work, still follow `usage-reporting.md`: check balance before/after when cost may not be returned per call, report total cost for the whole flow, and include non-default cost-affecting inputs such as mode, Pro/new/v3 choice, direction count, size, candidate count, and enhancement use.
