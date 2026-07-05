# Cost Routing

Read this when the user says cheap, affordable, low-cost, budget, minimize credits, avoid Pro, or asks for a cost-driven Pro-vs-cheap comparison. For normal route selection, use `SKILL.md` and the matching asset reference; a Pro/new/v3 label alone does not require this file.

The rule: satisfy the asset intent with the lowest documented-cost route likely to work, then report the tradeoff. Do not silently upgrade to Pro. Cheap mode also changes retry behavior: a first approved generation is not permission for open-ended paid iteration — before each additional paid attempt (prompt tweak, rerun, extra candidate, Pro comparison, retry after failure, batch expansion, or switch to a paid edit route), ask and include the route, expected cost category, and cost already spent, unless the user approved a concrete budget or attempt count. Free/local work (polling, downloads, cropping, assembly, packaging, manifests, verification) never needs permission.

Label semantics (`Pro` expensive; `v3`/`new`/Pixen/PixFlux/BitForge cheap-family hints; `inpaint-v3` is Pro despite the suffix): see SKILL.md Model And Mode Terms. Route by the concrete endpoint, not the label. Prompt enhancement (inline `enhance_prompt` or enhancer endpoints) costs extra (~0.05 generations); skip it when the user wants cheapest-possible output unless prompt-quality risk is high and you name the cost.

## Current Cost Findings

Checked against official REST v2 OpenAPI and MCP docs on 2026-07-04:

- Character 8-direction standard mode: 1 generation. Character `pro` / `create-character-pro`: 20-40 generations depending on size.
- `create-character-v3`: `ceil(width * height * 8 / 65536)` generations when rotating a reference image; `1 + ceil(s * s * 8 / 65536)` from scratch (s = max dimension). Cost is size-driven — read the output size before estimating.
- Character template animation: 1 generation per direction. Custom/Pro animation: 20-40 per direction (160-320 for a full 8-direction Pro run). v3 is the default custom family; prefer it for cheap custom animation.
- 1/8-direction object creation (MCP and REST): Pro Tools, 20-40 generations per call.
- Map objects (`create_map_object` / `POST /map-objects`): documented separately from object Pro Tools; cost is not labeled — report or measure it rather than assuming.
- `create-ui-asset` (MCP and REST): Pro, 20-40 generations.
- Pro-labeled REST summaries: `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `image-to-pixelart-pro`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, `inpaint-v3`, `edit-images-v2`, `generate-8-rotations-v2`. Treat as higher-cost even without exact counts.
- Non-Pro-labeled image routes: `create-image-pixen`, `create-image-pixflux`, `create-image-pixflux-background`, `create-image-bitforge`. `animate-with-text-v3` and `generate-8-rotations-v3` are the cheap v3 animation/rotation family.
- Do not lower `frame_count` as a cost optimization unless docs or a verified pricing response show frame count changes cost. Change documented cost drivers instead: route family, mode, direction count, candidate count, enhancement use, size.

If exact current costs matter, refresh official docs or run a small balance-before/after test with explicit approval. Do not invent prices for routes whose docs only show a label.

## Cheap Route Preferences

| Asset | Cheap default | Use Pro only when |
|---|---|---|
| General images | `create-image-pixen` (small/single/icon iteration, outline/detail/view controls) or `create-image-pixflux` (general/background style) | Style-reference generation or high-quality sheet output is required and approved |
| Icon sheets | Propose a non-Pro/Pixen comparison or a smaller test first; ask whether quality or savings wins | User approves the Pro sheet after the tradeoff is named |
| Characters | Standard mode or v3 | User accepts 20-40 generations for `pro` |
| Character animation | Template mode when a template fits; else v3 custom; one direction first | User approves Pro cost |
| Objects | For standalone visuals that don't need managed object IDs: a general-image/Pixen/PixFlux or isometric-tile route, labeled as not creating a managed object; map-object route when a map object is specifically needed (measure cost) | User accepts Pro Tools 20-40 generations |
| Object animation | `mode='v3'` (documented default) | User explicitly approves Pro |
| UI | Non-Pro general-image route for loose UI images (explain weaker structure); `generate-ui-v2` only if its cost is acceptable | Structured `create-ui-asset` is required and approved |
| Image-to-pixel-art | `image-to-pixelart` when the size fits its limits | Pro needed and approved |
| Inpaint/edit | Base `inpaint` / non-Pro edit routes | Pro capabilities required and cost accepted |

When choosing a cheap route, name the tradeoff plainly (lower cost, possibly less candidate variety or weaker Pro-quality detail) and follow `usage-reporting.md` for cost reporting.
