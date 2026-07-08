# PixelLab Credit Output Estimation Spike

Last reviewed: 2026-07-08.

Important prefix: this is an estimation and may not be accurate. PixelLab prices are documented as estimates, usage can vary with GPU processing time, and the practical value of 1 credit depends heavily on the workflow, endpoint, output size, frame count, grid behavior, retry count, and whether you count a sheet/tile/animation frame as one output or many outputs.

Purpose: estimate how many literal PixelLab outputs and generation-spend units a user might get from 1 PixelLab credit, while avoiding the false simplification that 1 credit equals 1 generation.

Primary sources checked:

- [PixelLab API pricing/examples](https://www.pixellab.ai/pixellab-api)
- [REST v2 endpoint index](https://api.pixellab.ai/v2/llms.txt)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [PixelLab FAQ](https://www.pixellab.ai/docs/faq)
- [PixelLab refund policy](https://www.pixellab.ai/refundpolicy)
- [PixelLab terms](https://www.pixellab.ai/termsofservice)

## Key Finding

PixelLab credits are USD-denominated. The live API page purchase modal states that `1 credit = $1 USD`, and the API pricing page presents endpoint estimates in both USD and generation units.

Therefore:

- `1 credit` is best treated as `$1 USD` account balance.
- `generation` or `generation-unit` is a spend/accounting unit used by PixelLab tools.
- Literal outputs are the returned artifacts: images, candidate grid cells, frames, tiles, or generated asset entries, depending on workflow.
- There is no single stable conversion from `1 credit` to either generation-units or literal outputs across all tools.

## Estimated Generation-Unit Range Per 1 Credit

Based on the documented examples reviewed, 1 credit can represent roughly:

| Workflow family | Example documented pricing | Approx spent generation-units per $1 |
|---|---:|---:|
| Prompt enhancement | `$0.002` for `0.05` generation | `25` generation-units |
| Common one-generation tools | about `$0.0055-$0.02` for `1` generation | `50-181` generation-units |
| Common simple image examples | about `$0.01` for `1` generation | `100` generation-units |
| Pro tools | `$0.095` for `20`, `$0.125` for `25`, `$0.185` for `40` generations | about `200-216` generation-units |
| Top-down/sidescroller tilesets | `$0.0079-$0.0099` for `3` generations | about `303-380` generation-units |

Estimated overall range from the reviewed examples: about `25-380` generation-units per 1 credit.

Do not quote this as a guarantee. It is a cross-endpoint estimate from public examples, not a billing contract.

## Estimated Literal Output Range Per 1 Credit

Literal output count depends on what is counted as an output.

### Normal Image Outputs

If a returned image file or candidate cell counts as one output, the rough range is:

| Workflow family | Outputs per call | Example cost | Approx literal outputs per $1 |
|---|---:|---:|---:|
| Large Pro single-output jobs | `1` image | `$0.185` | about `5` images |
| Smaller Pro single-output jobs | `1` image | `$0.095` | about `10` images |
| Basic single-image tools | `1` image | about `$0.0055-$0.02` | about `50-181` images |
| Pro 2x2 grid | `4` candidate images | `$0.095-$0.125` | about `32-42` images |
| Pro 4x4 grid | `16` candidate images | `$0.095-$0.125` | about `128-168` images |
| Pro 8x8 grid | `64` candidate images | `$0.095-$0.125` | about `512-674` images |

Estimated normal-image range: about `5-674` literal image outputs per 1 credit.

### Tileset Cells Counted As Outputs

If each returned tile cell counts as one output, tilesets push the upper bound higher:

| Workflow family | Outputs per call | Example cost | Approx literal outputs per $1 |
|---|---:|---:|---:|
| Top-down/sidescroller tileset | `16-32` tile cells | `$0.0079-$0.0099` | about `1,600-4,000` tile outputs |

The commonly cited example from this review was a `32`-tile output at about `$0.0099`: `$1 / $0.0099 ~= 101` calls, and `101 * 32 ~= 3,232` tile outputs.

This does not mean the tool costs less than 1 generation-unit. The reviewed tileset examples cost about `3` generation-units per call; the high literal-output count comes from each call returning many tiles.

Estimated inclusive range when tile cells count individually: about `5-3,232+` literal outputs per 1 credit, with `4,000` possible from the lowest reviewed 16-tile cost example if counted purely arithmetically. Treat these as upper-bound math, not a user-facing promise.

## Per Generation-Unit Output Density

For some reasoning, per-generation output density is clearer than per-credit output count:

| Workflow | Literal outputs | Generation-units | Outputs per generation-unit |
|---|---:|---:|---:|
| Single-output, one-generation tool | `1` image | `1` | `1` |
| Pro 8x8 grid | `64` candidates | `20` | `3.2` |
| 32-tile tileset | `32` tiles | `3` | `10.67` |

The highest output density observed in this estimate is tileset-style output, because one generation-spend event returns many tile cells.

## Recommended User-Facing Summary

When asked how much 1 PixelLab credit gives:

> 1 PixelLab credit is `$1 USD`, not a fixed number of generations. Based on current public examples, it roughly represents `25-380` generation-units. In literal returned outputs, that is about `5-674` normal image/candidate outputs, or up to roughly `3,232+` tile outputs if each tileset tile is counted separately. The exact number depends heavily on the workflow.

When the user asks about budget planning, prefer route-specific estimates:

- For simple one-image calls, quote the selected endpoint's price.
- For Pro grids, state both candidate count and generation-unit cost.
- For tilesets, state both the call cost and the number of returned tile cells.
- For animations, state whether counting final animation files, frames, or directional frame sets.
- For retry-heavy work, budget attempts explicitly; failed or low-quality outputs still spend credits if the call completes.

## Do Not Overclaim

- Do not say `1 credit = 1 generation`.
- Do not say `$1 always buys 100 generations`.
- Do not compare routes only by generation-units when the user cares about literal outputs.
- Do not compare routes only by literal output count when the user cares about quality, consistency, editability, or final usable assets.
- Do not promote this research into runtime rules unless a stable agent behavior changes.
