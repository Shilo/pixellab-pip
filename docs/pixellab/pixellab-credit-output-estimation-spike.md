# PixelLab Credit Output Estimation Spike

Last reviewed: 2026-07-08.

> **Important prefix: this is an estimation and may not be accurate.**
>
> PixelLab prices are documented as estimates, usage can vary with GPU processing time, and the practical value of 1 credit depends heavily on the workflow, endpoint, output size, frame count, grid behavior, retry count, and whether you count a sheet/tile/animation frame as one output or many outputs.

Purpose: estimate how many literal PixelLab outputs and generation-spend units a user might get when planning around 1 USD of PixelLab credit, while avoiding the false simplification that 1 credit equals 1 generation.

## Summary

Conversion:

- `$1` credit =
  - `~19-380` generation-units (`~25-380` without helper endpoints).
  - `~5-674` normal image outputs.
  - `~1,616-2,025` compact tile-cell outputs (`or up to ~3,165 observed expanded tile-cell outputs`).

Value:

- `Raw` credits = `100%` value (`benchmark at ~100 common simple-call generation-units per $1`).
- Monthly subscription:
  - `Tier 1` = `~167%` value (`$12/month`, `2,000` images/month).
  - `Tier 2` = `~208%` value (`$24/month`, `5,000` images/month).
  - `Tier 3` = `~200%` value (`$50/month`, `10,000` images/month).
- Annual subscription (`if monthly allowance repeats for 12 months`):
  - `Tier 1` = `~242%` value (`$99/year`, `24,000` images/year).
  - `Tier 2` = `~273%` value (`$220/year`, `60,000` images/year).
  - `Tier 3` = `~240%` value (`$500/year`, `120,000` images/year).

## Rough Estimate

For fast planning only, treating `1 credit` as `$1 USD` based on the observed purchase UI:

- Credit to generation-spend units: about `19-380` implied generation-units per credit across reviewed examples; about `25-380` if ignoring helper endpoints such as `estimate-skeleton`.
- Credit to literal outputs: about `5-674` normal image/candidate outputs per credit.
- Credit to literal tile outputs: about `1,616-2,025` tile cells per credit for compact 16-tile tilesets, or up to about `3,165` for locally observed expanded 25-populated-tile top-down outputs if the same USD pricing applies.

These are workflow-dependent estimates, not guaranteed account balances, quotas, or endpoint promises.

Subscription value, using the live subscription data and card logic observed on 2026-07-08:

- Raw USD credits: baseline `100%` when normalized to the common simple-call benchmark of about `100` generation-units per `$1`; actual observed endpoint-derived range is about `19-380` generation-units per `$1`.
- Tier 1 monthly (`$12`, `2,000` images/month): about `166.7` monthly image/generation allowance per `$1`, or about `167%` of the common raw-credit benchmark.
- Tier 2 monthly (`$24`, `5,000` images/month): about `208.3` monthly image/generation allowance per `$1`, or about `208%` of the common raw-credit benchmark.
- Tier 3 monthly (`$50`, `10,000` images/month): about `200` monthly image/generation allowance per `$1`, or about `200%` of the common raw-credit benchmark.

Annual billing improves the allowance-per-dollar calculation: Tier 1 is about `242%`, Tier 2 about `273%`, and Tier 3 about `240%` of the same common raw-credit benchmark, assuming the monthly allowance repeats for 12 months.

Primary sources checked:

- [PixelLab API pricing/examples](https://www.pixellab.ai/pixellab-api)
- [PixelLab homepage subscription tiers](https://www.pixellab.ai/)
- [PixelLab public subscription data](https://api.pixellab.ai/get-subscriptions)
- [REST v2 endpoint index](https://api.pixellab.ai/v2/llms.txt)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [PixelLab FAQ](https://www.pixellab.ai/docs/faq)
- [PixelLab refund policy](https://www.pixellab.ai/refundpolicy)
- [PixelLab terms](https://www.pixellab.ai/termsofservice)

## Key Finding

PixelLab exposes both USD credits and subscription generations. The live API page purchase modal observed during this spike stated that `1 credit = $1 USD`, while the public pricing examples are USD estimates and some PixelLab surfaces expose generation usage. Treat cross-unit ratios below as arithmetic derived from paired examples, not as a billing contract.

Therefore:

- For rough planning, `1 credit` was treated as `$1 USD` account balance based on the observed purchase UI.
- `generation` or `generation-unit` is a spend/accounting unit used by PixelLab tools.
- Literal outputs are the returned artifacts: images, candidate grid cells, frames, tiles, or generated asset entries, depending on workflow.
- Subscription tiers expose an `Image generation limit` in the homepage card logic; this spike treats that as a monthly image/generation allowance for normalization, but not as raw USD credit.
- There is no single stable conversion from USD credit to either generation-units or literal outputs across all tools.

## Subscription Value Per Dollar

This section normalizes each way of spending against a common raw-credit benchmark. The benchmark is not a universal billing rule: it uses the common simple image examples where `$0.01` maps to `1` generation-unit, or about `100` generation-units per `$1`.

Using that benchmark:

| Spend option | Observed price | Observed allowance | Allowance per `$1` | Value vs common raw-credit benchmark |
|---|---:|---:|---:|---:|
| Raw USD credits | `$1` | workflow-dependent | about `100` generation-units per `$1` for common simple calls | `100%` benchmark |
| Tier 1 monthly, Pixel Apprentice | `$12/month` | `2,000` images/month | about `166.7` images/month per `$1` | about `167%` |
| Tier 2 monthly, Pixel Artisan | `$24/month` | `5,000` images/month | about `208.3` images/month per `$1` | about `208%` |
| Tier 3 monthly, Pixel Architect | `$50/month` | `10,000` images/month | `200` images/month per `$1` | `200%` |

Annual billing, if the same monthly allowance is available for each month of the year:

| Spend option | Observed annual price | Annualized allowance | Allowance per `$1` | Value vs common raw-credit benchmark |
|---|---:|---:|---:|---:|
| Tier 1 annual, Pixel Apprentice | `$99/year` | `24,000` images/year | about `242.4` images/year per `$1` | about `242%` |
| Tier 2 annual, Pixel Artisan | `$220/year` | `60,000` images/year | about `272.7` images/year per `$1` | about `273%` |
| Tier 3 annual, Pixel Architect | `$500/year` | `120,000` images/year | `240` images/year per `$1` | `240%` |

Read this as rough value density, not pure substitutability. Raw credits are flexible USD balance and endpoint costs vary widely. Subscriptions add tier-specific benefits such as higher image-size caps, priority/concurrency, support level, and early access, but unused monthly allowance, billing-cycle behavior, feature access, and quality/retry patterns are outside this numeric percentage.

## Estimated Generation-Unit Range Per 1 Credit

Based on the documented examples reviewed, the implied generation-unit ratios for `$1` of USD credit are roughly:

| Workflow family | Example documented pricing | Approx spent generation-units per $1 |
|---|---:|---:|
| Low-cost helper endpoint (`estimate-skeleton`) | about `$0.0051` for `0.1` generation | about `19-20` generation-units |
| Prompt enhancement | `$0.002` for `0.05` generation | `25` generation-units |
| Common one-generation tools | about `$0.0055-$0.02` for `1` generation | `50-181` generation-units |
| Common simple image examples | about `$0.01` for `1` generation | `100` generation-units |
| Pro tools | `$0.095` for `20`, `$0.125` for `25`, `$0.185` for `40` generations | about `200-216` generation-units |
| Top-down/sidescroller tilesets | `$0.0079-$0.0099` for `3` generations | about `303-380` generation-units |

Estimated overall range from the reviewed examples: about `19-380` generation-units per `$1` of USD credit. If ignoring helper endpoints and considering generation/content endpoints only, the reviewed range is about `25-380`.

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
| Pro 2x2 grid | `4` candidate images | `$0.095` in the reviewed pricing ladder | about `42` images |
| Pro 4x4 grid | `16` candidate images | `$0.095` in the reviewed pricing ladder | about `168` images |
| Pro 8x8 grid | `64` candidate images | `$0.095` in the reviewed pricing ladder | about `674` images |

Estimated normal-image range: about `5-674` literal image outputs per 1 credit.

### Tileset Cells Counted As Outputs

If each returned tile cell counts as one output, tilesets push the upper bound higher:

| Workflow family | Outputs per call | Example cost | Approx literal outputs per $1 |
|---|---:|---:|---:|
| Compact top-down/sidescroller tileset | `16` tile cells | `$0.0079-$0.0099` | about `1,616-2,025` tile outputs |
| Expanded top-down tileset observed in local research | `25` populated tile cells | `$0.0079-$0.0099` if the same pricing applies | about `2,525-3,165` tile outputs |

The `16x16 tiles` and `32x32 tiles` labels on the pricing page are tile dimensions, not tile counts. The earlier `32`-tile interpretation was wrong. Current local routing docs treat compact top-down/sidescroller results as 16-tile outputs, while local live top-down research observed expanded `4x8` atlases with 25 populated tiles for some `transition_size: 1.0` or Pro-expanded cases.

This does not mean the tool costs less than 1 generation-unit. The reviewed tileset examples cost about `3` generation-units per call; the high literal-output count comes from each call returning many tiles.

Estimated inclusive range when tile cells count individually: about `5-2,025` literal outputs per `$1` for documented compact 16-tile outputs, or about `5-3,165` if applying the same USD examples to locally observed expanded 25-populated-tile top-down outputs. Treat the expanded case as an observed workflow caveat, not a public endpoint guarantee.

## Per Generation-Unit Output Density

For some reasoning, per-generation output density is clearer than per-credit output count:

| Workflow | Literal outputs | Generation-units | Outputs per generation-unit |
|---|---:|---:|---:|
| Single-output, one-generation tool | `1` image | `1` | `1` |
| Pro 8x8 grid | `64` candidates | `20` | `3.2` |
| Compact tileset | `16` tiles | `3` | `5.33` |
| Expanded top-down tileset observed locally | `25` populated tiles | `3` if the same pricing applies | `8.33` |

The highest output density observed in this estimate is tileset-style output, because one generation-spend event returns many tile cells.

## Recommended User-Facing Summary

When asked how much 1 PixelLab credit gives:

> When planning around `$1` of PixelLab USD credit, current public examples imply roughly `19-380` generation-units, or `25-380` if ignoring helper endpoints. In literal returned outputs, that is about `5-674` normal image/candidate outputs. If each tileset tile is counted separately, compact 16-tile outputs imply about `1,616-2,025` tile outputs, while locally observed expanded 25-populated-tile cases could imply up to about `3,165` if the same USD examples apply. The exact number depends heavily on the workflow.

When the user asks about budget planning, prefer route-specific estimates:

- For simple one-image calls, quote the selected endpoint's price.
- For Pro grids, state both candidate count and generation-unit cost.
- For tilesets, state both the call cost and the number of returned tile cells.
- For animations, state whether counting final animation files, frames, or directional frame sets.
- For retry-heavy work, budget attempts explicitly. Completed jobs can spend credits even if the result is rejected for quality; failed jobs should be reported from actual `usage` or balance delta instead of assumed.

## Do Not Overclaim

- Do not say `1 credit = 1 generation`.
- Do not say `$1 always buys 100 generations`.
- Do not compare routes only by generation-units when the user cares about literal outputs.
- Do not compare routes only by literal output count when the user cares about quality, consistency, editability, or final usable assets.
- Do not promote this research into runtime rules unless a stable agent behavior changes.
