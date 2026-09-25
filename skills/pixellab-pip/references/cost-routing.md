# Cost Routing

Read this when the user says cheap, affordable, low-cost, budget, minimize credits, avoid Pro, or asks for a cost-driven Pro-vs-cheap comparison. For normal route selection, use `SKILL.md` and the matching asset reference; a Pro/new/v3 label alone does not require this file.

The rule: satisfy the asset intent with the lowest documented-cost route likely to work, then report the tradeoff. Do not silently upgrade to Pro. Cheap mode also changes retry behavior: a first approved generation is not permission for open-ended paid iteration — before each additional paid attempt (prompt tweak, rerun, extra candidate, Pro comparison, retry after failure, batch expansion, or switch to a paid edit route), ask and include the route, expected cost category, and cost already spent, unless the user approved a concrete budget or attempt count. Free/local work (polling, downloads, cropping, assembly, packaging, manifests, verification) never needs permission.

Label semantics (`Pro` expensive; `v3`/`new`/Pixen/PixFlux/BitForge cheap-family hints; `inpaint-v3` is Pro despite the suffix): see SKILL.md Model And Mode Terms. Route by the concrete endpoint, not the label. Pro Flash is a separate, unbenchmarked family with provisional pricing; read `pro-flash.md` before comparing it. Inline `enhance_prompt` fields whose OpenAPI documents the surcharge add about 0.05 generations. Standalone enhancer endpoints have route-specific USD estimates; a prior live check observed 0.05 generations only for `enhance-pixen-prompt`. Treat prompt enhancement as extra cost, and skip it when the user wants cheapest-possible output unless prompt-quality risk is high and you name the cost. PixMiniMax is a separate paid animation route, not a cheap-family synonym for v3.

## Current Cost Findings

Checked against official REST v2 OpenAPI, MCP docs, and the public API pricing page on 2026-09-25:

- Character 8-direction standard mode: 1 generation. Character `pro` / `create-character-pro`: 20-40 generations depending on size.
- `create-character-v3`: `ceil(width * height * 8 / 65536)` generations when rotating a reference image; `1 + ceil(s * s * 8 / 65536)` from scratch (s = max dimension). Cost is size-driven — read the output size before estimating.
- `create_character_state` / `create-character-state`: 20-40 generations per call.
- Character template animation: 1 generation per direction. Pro animation: 20-40 per direction (160-320 for a full 8-direction Pro run). v3 custom animation is size-and-frame-scaled on the generated canvas: `ceil(width * height * frame_count / 65536)` per direction. Silhouettes may expand beyond the source image, so inspect the returned dimensions and usage instead of estimating from source size. v3 is the default custom family; prefer it for cheap custom animation.
- Skeleton v3 is a separate paid Tier 1+ beta route. The live MCP `animate_with_skeleton_v3` tool description lists 2 generations for 3 raw frames, 3 for 8, and 4 for 15; static MCP docs describe the managed-character `skeleton-v3` mode at 2–4 per direction. Check returned usage for the exact charge. Current public USD estimates for the raw endpoint are about `$0.0436`/3 frames, `$0.0513`/8, and `$0.0622`/15.
- 1/8-direction object creation (MCP and REST): Pro Tools, 20-40 generations per call.
- Map objects (`create_map_object` / `POST /map-objects`): documented separately from object Pro Tools; cost is not labeled — report or measure it rather than assuming.
- `create-ui-asset` (MCP and REST): Pro, 20-40 generations.
- Pro-labeled REST summaries: `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `image-to-pixelart-pro`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `inpaint-v3`, `edit-images-v2`, `generate-8-rotations-v2`. Treat as higher-cost even without exact counts. MCP `edit_image` and `inpaint_image` are these same Pro routes (`edit-images-v2`/`inpaint-v3`, confirmed by field-level schema match, not the base `edit-image`/`inpaint`) — treat them as Pro-cost even when called via MCP; MCP `create_image_pro` is likewise `generate-image-v2`.
- MCP `edit_image` / REST `edit-images-v2` are Pro: outputs up to 256px cost 20 generations, 257-314px cost 25, and 315-512px cost 40 per accepted call.
- The Version 0.4.123 notes advertise Pro Flash's single-image beta option at 4–6 generations with a 256×256 maximum; the current REST OpenAPI documents a provisional five-generation first-image charge. Edit/inpaint prices and visual quality are untested here. Read `pro-flash.md` for the canonical stage, reuse, and live-estimate rules before comparing total costs; do not infer cheaper-than-Pro output from the name.
- Cheap edit and convert: `edit_image_pixen`/`edit-image-pixen` and `image_to_pixelart`/`image-to-pixelart` cost 1 generation. The cleanup family — `unzoom_image`, `correct_pixelart`, `reduce_colors` and their REST twins — costs 0.1 generations per call. `correct_pixelart` and `reduce_colors` take several same-size frames per call, so batch rather than loop; `unzoom_image` is one image per call.
- Tilesets cost more than one generation: MCP documents `create_topdown_tileset` standard mode at 1-4 generations (usually 3 or 4) and `create_sidescroller_tileset` at 2 or 3. Do not quote a tileset as a 1-generation route.
- Non-Pro-labeled image routes: MCP `create_image_pixen` and `create_image_pixflux` each cost 1 generation; their REST counterparts are `create-image-pixen` and `create-image-pixflux` (`-background` is a second URL for the identical PixFlux schema, same tier). `create-image-bitforge` is REST-only with no MCP tool. `animate-with-text-v3`/MCP `animate_image` (documented cost `ceil(width * height * frame_count / 65536)` generations) and `generate-8-rotations-v3` are the cheap v3 animation/rotation family.
- PixMiniMax (`POST /animate-pixminimax` / MCP `animate_image_pixminimax`) is priced by generation time. Current public examples are `32x32`/4 frames = 1 generation; `64x64`/4, 8, 16, and 40 frames = 1, 1, 2, and 6; and `80x80`/8 = 1. The route accepts 4–40 generated frames in multiples of four at up to 256×256. Use returned `usage.generations` for the actual charge; website USD estimates are a separate reporting unit. Do not call or document the unversioned/private cost route mentioned in descriptive text.
- REST `POST /image-to-text` returns a generic image description or custom visual answer as text, not an image. PixelLab estimates about 0.09 generations for a typical sprite or screenshot; longer answers cost more. See the SKILL.md Intent Router for when to use it. The actual usage is returned in the response.
- `frame_count` is a documented cost driver for both v3 and PixMiniMax, but their pricing rules differ. Use the v3 area formula only for v3; for PixMiniMax use the published examples or returned usage. Change documented cost drivers instead of guessing: route family, mode, direction count, candidate count, enhancement use, size, and frame count where the selected route documents it.
- Talking portraits: portrait attachment, talking GIF rendering, and lip-sync plans are free; `create_vocal_animation` / `POST /vocal-animation` is the only paid-plan generation step and has no exact published unit price in the reviewed docs. Generate one mood per approved call.
- Font generation has fixed current pricing: 25 subscription generations, or at least `$0.125` in credits. The former `image_size` pricing tier has been removed.

If exact current costs matter, refresh official docs or run a small balance-before/after test with explicit approval. Do not invent prices for routes whose docs only show a label.

## Cheap Route Preferences

| Asset | Cheap default | Use Pro only when |
|---|---|---|
| General images | `create-image-pixen`/`create_image_pixen` (small/single/icon iteration, outline/detail/view controls) or `create-image-pixflux`/`create_image_pixflux` (general/background style) | Style-reference generation or high-quality sheet output is required and approved |
| Icon sheets | Propose a non-Pro/Pixen comparison or a smaller test first; ask whether quality or savings wins | User approves the Pro sheet after the tradeoff is named |
| Characters | Standard mode or v3 | User accepts 20-40 generations for `pro`; use it when user instructions must be followed closely because Pixen/v3/new may underweight them |
| Character animation | Template mode when a template fits; else v3 custom; one direction first | User approves Pro cost |
| Objects | For standalone visuals that don't need managed object IDs: a general-image/Pixen/PixFlux or isometric-tile route, labeled as not creating a managed object; map-object route when a map object is specifically needed (measure cost) | User accepts Pro Tools 20-40 generations |
| Object animation | `mode='v3'` (documented default) | User explicitly approves Pro |
| UI | Non-Pro general-image route for loose UI images (explain weaker structure); `generate-ui-v2` only if its cost is acceptable | Structured `create_ui_asset`/`create-ui-asset` is required and approved |
| Image-to-pixel-art | `image-to-pixelart`/`image_to_pixelart` (1 generation) when the size fits its limits | Pro needed and approved |
| Edit | MCP `edit_image_pixen` (1 generation) when the source is ≤256px per side and the target area ≤256×256; otherwise base `edit-image` via REST. MCP `edit_image` is Pro-tier (`edit-images-v2`) | Larger canvas, multi-image batch, or reference-mode edit is required and Pro cost accepted |
| Inpaint | Base `inpaint` **via REST** — MCP's `inpaint_image` is Pro-tier only (`inpaint-v3`), so there is still no cheap MCP path for masked regeneration | Pro capabilities required and cost accepted, or MCP-first with no REST fallback available |
| Palette reduction, clean-up, unzoom | `reduce_colors`/`correct_pixelart`/`unzoom_image` or their REST twins, 0.1 generations — far cheaper than regenerating a bad frame | Never; there is no Pro variant |

When choosing a cheap route, name the tradeoff plainly (lower cost, possibly less candidate variety or weaker Pro-quality detail) and follow `usage-reporting.md` for cost reporting.

Pixen/v3/new may underweight user instructions and has isometric bias despite `view`/`direction`; prefer Pro when the user's instructions or static south-facing view matter and higher cost and different character style are acceptable.
