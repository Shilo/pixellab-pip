# PixelLab Credit Output Estimation Spike

Last reviewed: 2026-07-16.

> **Important prefix: this is an estimation and may not be accurate.**
>
> PixelLab prices are documented as estimates, usage can vary with GPU processing time, and the practical value of 1 credit depends heavily on the workflow, endpoint, output size, frame count, grid behavior, retry count, and whether you count a sheet/tile/animation frame as one output or many outputs.

Purpose: estimate how many literal PixelLab outputs and generation-spend units a user might get when planning around 1 USD of PixelLab credit, while avoiding the false simplification that 1 credit equals 1 generation.

## Summary

Conversion:

- `$1` credit =
  - `~10-380` generation-units.
  - `~5-674` normal image outputs.
  - `~1,616-2,025` compact tile-cell outputs (`or up to ~3,165 observed expanded tile-cell outputs`).

Value:

There is no single subscription-vs-credits percentage. Value is **per route**, and it flips sign across the catalog. Compare each route's **implied $/generation** (USD price divided by generation count) against your plan's **$/generation** (price divided by monthly allowance):

- Subscription `$/generation`: `$0.0060` (Tier 1, first month) down to `$0.0037` (Tier 2 annual). Monthly prices step down with tenure, which moves this rate by up to `25%`.
- Route implied `$/generation`: about `$0.0026` (tilesets) up to `$0.0956` (template animation at `128x128`).
- Subscription wins whenever a route's implied `$/generation` is **above** your plan's rate.

Observed regimes, quoted against Tier 1 first month (`$0.0060/generation`, the worst generally-available rate — Brazil-only Tier 0 is worse at `$0.0071`; tenure brackets, higher tiers, and annual billing all improve every figure):

- Helper routes (`estimate-skeleton`, prompt enhancers) and template animation = strongest subscription value, roughly `5-16x`.
- `v3` character routes = strong subscription value, roughly `1.5-6.8x` depending on size and whether a reference image is used.
- Base image routes (Pixen, PixFlux, BitForge) = mild-to-moderate subscription value, roughly `1.2-2.8x`, rising with output size.
- Pro Tools = near break-even; roughly `0.77-1.36x` across all plans, with the tenure bracket deciding the sign.
- Tilesets = credits win on every plan, roughly `0.44-0.90x`.

Sweeping all `124` published priced rows: at first-month Tier 1 the subscription wins only `63/124`; at the deepest tenure bracket it wins `119/124`. **Even at the deepest discount, tilesets remain credits-only — the only family that loses on all 12 plans.** The fifth loser at max discount is `animate-with-text-v3` `@256`/8 frames, which is not a tileset. See [Every Endpoint At Maximum Discount](#every-endpoint-at-maximum-discount). Tier choice is worth only `2.3%` and is dominated by utilization, tenure, and billing period — see [Choosing A Tier: Volume, Not Unit Rate](#choosing-a-tier-volume-not-unit-rate).

These bands overlap and are not a strict ranking — `generate-8-rotations-v3` `@64` at `5.6x` outranks template animation at `64`/dir at `5.4x`, and the same route `@256` drops to `0.79x`. Size drives more variation than family does. Three caveats bound the whole table: the figures assume **full allowance utilization** (see [Utilization Breaks These Rates](#utilization-breaks-these-rates)); every max-discount figure assumes a **tenure bracket you must earn over months**; and Tier 1 physically cannot reach `12` of the `124` rows (see [Outside the arithmetic](#outside-the-arithmetic)). Generation counts are **published by PixelLab, not inferred**.

## Rough Estimate

For fast planning only, treating `1 credit` as `$1 USD` based on the observed purchase UI:

- Credit to generation-spend units: about `10-380` implied generation-units per credit across reviewed examples. Excluding helper endpoints (`estimate-skeleton`, prompt enhancers) does **not** raise the floor: template animation at `128`/dir is a content route and sits at about `10`.
- Credit to literal outputs: about `5-674` normal image/candidate outputs per credit.
- Credit to literal tile outputs: about `1,616-2,025` tile cells per credit for compact 16-tile tilesets, or up to about `3,165` for locally observed expanded 25-populated-tile top-down outputs if the same USD pricing applies.

These are workflow-dependent estimates, not guaranteed account balances, quotas, or endpoint promises.

Subscription value cannot be reduced to one percentage. See [Credits Versus Subscription](#credits-versus-subscription) for the per-route method; the short version is that subscription generations cost `$0.0037-$0.0060` each depending on tier and billing period, and whether that beats credits depends entirely on which route you call.

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
- Subscription tiers expose an `Image generation limit` in the homepage card logic; this spike treats that as a monthly generation allowance, which makes tier price divided by allowance a usable `$/generation` rate. It is not raw USD credit, and is believed not to roll over (see [Outside the arithmetic](#outside-the-arithmetic) — indicated by a "resets next month" string, not documented).
- There is no single stable conversion from USD credit to either generation-units or literal outputs across all tools.
- USD prices track GPU processing time; generation counts are a coarser, step-quantized unit (several routes do scale with output area, but in integer steps via `ceil`). The two do **not** track each other, and that divergence — not any bundle discount — is what decides whether credits or a subscription is cheaper for a given route.
- Subscription monthly prices step down with tenure (Tier 1 `$12`/`$10`/`$9.50`/`$9.00`; Tier 2 `$24`/`$23`/`$22.50`/`$22`). These brackets are not exposed by [get-subscriptions](https://api.pixellab.ai/get-subscriptions), which reports only the first-month price.

## Credits Versus Subscription

An earlier version of this spike normalized every spend option against a "common simple call = about `100` generation-units per `$1`" benchmark and reported subscription value as `167%`/`208%`/`242%`. **That method was wrong and those numbers are withdrawn.** The benchmark was an arbitrary pick from one cheap route, so the percentages measured the choice of baseline rather than any real cost difference, and it compared `images/month per $1` against `generation-units per $1` as if the two units were substitutable. They are not.

The two payment units only meet at a single question: for the route you are about to call, what is a generation worth in USD, and what are you paying for one?

**Scope limit — read before using this section.** The rates below are **average** cost at full allowance utilization, which answers *"should I buy this plan for this workflow mix?"*. It does **not** answer *"which should I spend on this call?"* — if you already hold a subscription with unused allowance, the marginal cost of a generation is `$0` and every route favors the subscription; once the allowance is exhausted, credits are all that is left. The per-route flip below is real only at the buy decision, and only at high utilization. See [Utilization Breaks These Rates](#utilization-breaks-these-rates).

### Step 1: your subscription rate

Tier price divided by monthly generation allowance. Base prices are confirmed against [get-subscriptions](https://api.pixellab.ai/get-subscriptions). Allowances are published in the homepage card logic, keyed by the same `plan_id` values `get-subscriptions` returns (`{914016:700, 902410:2000, 902412:2000, 902411:5000, 902413:5000, 840828:10000, 921083:10000}`) — verified, not inferred.

**The tenure brackets are a loyalty ladder you must earn.** The checkout bundle renders them from per-account `discount_steps` under the label **"Monthly Discount Progress"**, with copy describing a discount you "built up" that cancelling forfeits (with roughly a one-week grace to reactivate and keep it), gated to non-annual plans. The bracket values below are user-reported; `discount_steps` comes from an authenticated endpoint and is absent from every public bundle, so they are **not independently verifiable** and Tier 3's ladder is unknown. **Read bracket 4 as a month-4-and-later rate that a new subscriber cannot buy today.** Every "max discount" figure in this document carries that condition.

| Plan | Price | Allowance | `$/generation` |
|---|---:|---:|---:|
| Tier 0 monthly, Pixel Novice (Brazil only) | `$5` | `700` | `$0.0071` |
| Tier 1 monthly, bracket 1 | `$12` | `2,000` | `$0.0060` |
| Tier 1 monthly, bracket 2 | `$10` | `2,000` | `$0.0050` |
| Tier 1 monthly, bracket 3 | `$9.50` | `2,000` | `$0.0047` |
| Tier 1 monthly, bracket 4 | `$9.00` | `2,000` | `$0.0045` |
| Tier 2 monthly, bracket 1 | `$24` | `5,000` | `$0.0048` |
| Tier 2 monthly, bracket 2 | `$23` | `5,000` | `$0.0046` |
| Tier 2 monthly, bracket 3 | `$22.50` | `5,000` | `$0.0045` |
| Tier 2 monthly, bracket 4 | `$22` | `5,000` | `$0.0044` |
| Tier 3 monthly | `$50` | `10,000` | `$0.0050` |
| Tier 1 annual | `$99` | `24,000` | `$0.0041` |
| Tier 2 annual | `$220` | `60,000` | `$0.0037` |
| Tier 3 annual | `$500` | `120,000` | `$0.0042` |

Five consequences:

- **Tier 0 (`$0.0071`) is the worst rate in the catalog**, not first-month Tier 1. It is Brazil-only, so it rarely enters the comparison, but it is the floor.
- **First-month Tier 1 (`$0.0060`) is the worst generally-available rate**, and it is the rate most cost complaints are computed against.
- **The tenure discount is worth more than the tier choice.** Tier 1 falls `25%` from `$0.0060` to `$0.0045` — but only after several monthly bills. A long-tenured Tier 1 (`$0.0045`) beats a first-month Tier 2 (`$0.0048`).
- **Annual still beats every monthly bracket**, including the deepest: `$0.0041` vs `$0.0045` on Tier 1, `$0.0037` vs `$0.0044` on Tier 2. Annual is also excluded from the loyalty ladder.
- **Tier 2 annual (`$0.0037`) is the best rate in the catalog.** Tier 3 is *worse* per generation than Tier 2 on both billing periods; Tier 3 buys volume headroom, size caps, and concurrency, not a better unit rate.

### Step 2: the route's implied rate

USD price divided by generation count. Subscription wins when this exceeds your Step 1 rate.

**Both numbers are published.** The pricing page's Credits/Generations toggle is backed by a data object in which every one of its `124` priced rows carries both a `credits:` (USD) and a `generations:` field. Nothing in this section is inferred, and no generation count here needs a balance-delta test. Independently verified by parsing the bundle (`/_next/static/chunks/pages/pixellab-api-<hash>.js`).

| Route | Gens | USD | Implied `$/gen` | vs T1 bracket 1 | vs T1 bracket 4 | vs T2 annual |
|---|---:|---:|---:|---:|---:|---:|
| `create-tileset` `16x16` | `3` | `$0.0079` | `$0.0026` | `0.44x` | `0.59x` | `0.72x` |
| `create-tileset` `32x32` | `3` | `$0.0099` | `$0.0033` | `0.55x` | `0.73x` | `0.90x` |
| `animate-with-text-v3` `256`, 8f | `8` | `$0.0302` | `$0.0038` | `0.63x` | `0.84x` | `1.03x` |
| Pro Tools, large rung | `40` | `$0.185` | `$0.0046` | `0.77x` | `1.03x` | `1.26x` |
| `generate-8-rotations-v3` `256` | `8` | `$0.0377` | `$0.0047` | `0.79x` | `1.05x` | `1.28x` |
| Pro Tools, small rung | `20` | `$0.095` | `$0.0047` | `0.79x` | `1.06x` | `1.30x` |
| Pro Tools, mid rung | `25` | `$0.125` | `$0.0050` | `0.83x` | `1.11x` | `1.36x` |
| `remove-background` `64x64` | `1` | `$0.00554` | `$0.0055` | `0.92x` | `1.23x` | `1.51x` |
| `create-image-pixen` `64x64` | `1` | `$0.00718` | `$0.0072` | `1.20x` | `1.60x` | `1.96x` |
| `create-image-pixflux` `64x64` | `1` | `$0.00793` | `$0.0079` | `1.32x` | `1.76x` | `2.16x` |
| `create-character-v3` `168` | `5` | `$0.045` | `$0.0090` | `1.50x` | `2.00x` | `2.45x` |
| `create-map-object` per object | `1` | `$0.0099` | `$0.0099` | `1.65x` | `2.20x` | `2.70x` |
| `animate-with-text-v3` `128`, 16f | `4` | `$0.0424` | `$0.0106` | `1.77x` | `2.36x` | `2.89x` |
| `create-character-4-dir` `64x64` | `1` | `$0.0122` | `$0.0122` | `2.03x` | `2.71x` | `3.33x` |
| `animate-character` v3 `64x64` | `1` | `$0.0129` | `$0.0129` | `2.15x` | `2.87x` | `3.52x` |
| `create-character-v3` `128` | `3` | `$0.042` | `$0.0140` | `2.33x` | `3.11x` | `3.82x` |
| `generate-8-rotations-v3` `128` | `2` | `$0.0345` | `$0.0173` | `2.88x` | `3.83x` | `4.70x` |
| `create-character-8-dir` `64x64` | `1` | `$0.0173` | `$0.0173` | `2.88x` | `3.84x` | `4.72x` |
| `create-character-v3` `64` | `2` | `$0.041` | `$0.0205` | `3.42x` | `4.56x` | `5.59x` |
| `animate-with-text-v3` `32`, 4f | `1` | `$0.0221` | `$0.0221` | `3.68x` | `4.91x` | `6.03x` |
| `animate-character` template `64`/dir | `1` | `$0.0323` | `$0.0323` | `5.38x` | `7.18x` | `8.81x` |
| `generate-8-rotations-v3` `64` | `1` | `$0.0337` | `$0.0337` | `5.62x` | `7.49x` | `9.19x` |
| Prompt enhancement (all three) | `0.05` | `$0.002` | `$0.0400` | `6.67x` | `8.89x` | `10.91x` |
| `estimate-skeleton` `256` | `0.1` | `$0.00516` | `$0.0516` | `8.60x` | `11.47x` | `14.07x` |
| `animate-character` template `128`/dir | `1` | `$0.0956` | `$0.0956` | `15.93x` | `21.24x` | `26.07x` |

Notes on the inputs:

- **The Pro rung mapping is published, not assumed:** `20`→`$0.095`, `25`→`$0.125`, `40`→`$0.185`, uniform across all `51` Pro rows. This does **not** license a claim about PixelLab's intent — the rungs landing near the subscription rate is an observation, not evidence of design.
- **`create-character-v3` published counts (`2`/`3`/`5` at `64`/`128`/`168`) exactly match the documented from-scratch formula** `1 + ceil(s * s * 8 / 65536)`. The reference-image variant (`ceil(w * h * 8 / 65536)`) is documented in [cost-routing.md](../../skills/pixellab-pip/references/cost-routing.md), but the pricing page publishes **one row per size**, and it is the from-scratch one. Pairing the reference-image count with the from-scratch USD price would invent a rate PixelLab does not publish, so no such row appears above.
- **`generate-8-rotations-v3` published counts (`1`/`1`/`2`/`8` at `32`/`64`/`128`/`256`) are exactly `ceil(s * s * 8 / 65536)`** — the same area term. Its `256` row is the one place the area scaling bites: `8` generations for `$0.0377` collapses it to `$0.0047/gen`, statistically identical to a Pro rung.
- **`animate-with-text-v3` scales on frames and area together** (`1`/`8`/`4` at `32`&#8239;4f / `256`&#8239;8f / `128`&#8239;16f) and has no published formula, but every listed row has a published count. The `256`&#8239;8f row is the only non-tileset route that loses at max discount.
- **`create-map-object` bills `1` generation** (`$0.0099`), resolving a cost this repo's [cost-routing.md](../../skills/pixellab-pip/references/cost-routing.md) still records as unlabeled. It is `2.20x` at Tier 1 bracket 4 — a subscription win, not a hidden tileset.

### Step 3: interpretation

- **Pro Tools land near the subscription rate, and the tenure bracket decides the sign.** Under the assumed rung mapping, all three rungs sit within about `8%` of each other at `$0.0046-$0.0050`. That is close enough to the subscription rate that Pro flips: on first-month Tier 1 a subscription costs about `20-30%` more than credits (`$0.12` vs `$0.095` on the small rung), by Tier 1 bracket 3 (`$0.00475`) it lands on **exact** breakeven with the small rung, and from bracket 4 or any annual plan the subscription wins by `3-36%`. Whether PixelLab set the rung counts deliberately to sit near the subscription rate is **unknown** — the mapping itself is this spike's assumption, so the apparent parity cannot be used as evidence of intent. Pro grids returning many candidates change output density, not `$/generation`, so they are not a reason to prefer either payment method.
- **The subscription's value comes from `v3`, template, and helper routes**, where generation counts stay low or step coarsely while GPU time (and therefore USD) climbs.
- **Tilesets are the worst subscription value among the routes reviewed here**, at `0.44-0.90x` across every plan — the only family where credits win on all of them. This ranking depends on the Pro rung mapping above; at `40` generations per `$0.095`, Pro would be worse.
- **Low generations-per-dollar does not mean poor value.** The table in [Estimated Generation-Unit Range Per 1 Credit](#estimated-generation-unit-range-per-1-credit) reports `10-31` generation-units per `$1` for template animation, its lowest row. Inverted, that is the *best* subscription value reviewed here (`15.9x` at `128`/dir). The two framings point opposite directions; do not read one as the other.

### Every Endpoint At Maximum Discount

Sweeping **all `124` published priced rows** (every endpoint, every size row, using PixelLab's own `credits` and `generations` fields) against the deepest monthly brackets. Reminder: bracket 4 is a month-4-and-later rate, not one a new subscriber can buy.

| Plan | Rate | Subscription wins | Credits win |
|---|---:|---:|---:|
| Tier 1 bracket 1 (`$12`) | `$0.0060` | `63/124` | `61` |
| Tier 1 bracket 4 (`$9.00`) | `$0.0045` | `119/124` | `5` |
| Tier 2 bracket 4 (`$22`) | `$0.0044` | `119/124` | `5` |
| Tier 2 annual (`$220`) | `$0.0037` | `120/124` | `4` |

The first row is the headline the tenure ladder hides: **in the first month, Tier 1 loses on `61` of `124` rows — roughly half the catalog** — because every Pro row (`51` of them) and both background-removal sizes sit below `$0.0060`. The subscription only becomes broadly correct once the ladder has been climbed.

**The losing set at max discount, identical on Tier 1 and Tier 2:**

| Endpoint | Size | Gens | USD | Implied `$/gen` | T1 bracket 4 | T2 bracket 4 |
|---|---|---:|---:|---:|---:|---:|
| `create-tileset` | `16x16` | `3` | `$0.0079` | `$0.0026` | `0.59x` | `0.60x` |
| `create-tileset-sidescroller` | `16x16` | `3` | `$0.0079` | `$0.0026` | `0.59x` | `0.60x` |
| `create-tileset` | `32x32` | `3` | `$0.0099` | `$0.0033` | `0.73x` | `0.75x` |
| `create-tileset-sidescroller` | `32x32` | `3` | `$0.0099` | `$0.0033` | `0.73x` | `0.75x` |
| `animate-with-text-v3` | `256x256`, 8 frames | `8` | `$0.0302` | `$0.0038` | `0.84x` | `0.86x` |

**Tilesets are the only family that loses on every one of the 12 plans**, and they are structurally immune: a `3`-generation call must cost more than `$0.0135` in credits to break even at `$0.0045`, and tilesets cost `$0.0079-$0.0099`. Tier 1 would have to fall to **`$5.27/month`** to reach parity on `16x16` tiles (or `$6.60` on `32x32`) — below the `$9.00` floor. No published bracket closes it.

**`animate-with-text-v3` at `256x256`/8 frames is the one non-tileset loser** at max discount: `8` generations for `$0.0302` is `$0.0038/gen`. It loses on `11` of `12` plans, winning only at Tier 2 annual (`1.03x`). It is the counterexample to "`v3` always favors the subscription" — frame-and-area scaling can push a `v3` route below the subscription rate, and this is the single row where it does.

Two qualifications on the `119` wins:

- **The Pro `40`-generation rung wins by only `1.03x`.** That is the large rung of `generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `inpaint-v3`, `edit-images-v2`, `animate-with-text-v2`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`, and every Pro character/object route. A `3%` margin sits inside the GPU-time variance the source warns about. Treat as break-even, not a win.
- **`generate-8-rotations-v3` `@256` wins by `1.05x`** for the same reason — its published `8`-generation count puts it at `$0.0047/gen`, statistically identical to a Pro rung. At first-month Tier 1 it is `0.79x` and credits win.

Unlike earlier revisions of this document, **none of these counts is inferred** — all `124` rows publish theirs.

### Choosing A Tier: Volume, Not Unit Rate

Tier 2 at max discount (`$0.0044`) has a better unit rate than Tier 1 at max discount (`$0.0045`) — by `2.3%`. That number is close to meaningless, because it costs `$13/month` more and requires spending `3,000` more generations to realize.

All-in monthly cost, Tier 1 at max plus USD credits for anything past its `2,000` cap, overflow priced at a representative `v3` rate (`$0.0205/gen`):

| Generations/month | Tier 1 (`$9` + overflow) | Tier 2 (`$22`) | Cheaper |
|---:|---:|---:|---|
| `500` | `$9.00` | `$22.00` | **Tier 1** |
| `2,000` | `$9.00` | `$22.00` | **Tier 1** |
| `2,500` | `$19.25` | `$22.00` | **Tier 1** |
| `3,000` | `$29.50` | `$22.00` | **Tier 2** |
| `5,000` | `$70.50` | `$22.00` | **Tier 2** |

Crossover is about **`2,634` generations/month** for `v3`-heavy work (overflow at `create-character-v3` `@64`'s `$0.0205/gen`), and it moves with the route mix: about `2,136` for template-animation-heavy (at the `128`/dir rate, `$0.0956`; the `64`/dir rate gives `2,402`), `3,811` for Pixen-heavy (`$0.00718`), `4,737` for Pro-heavy (`$0.00475` — Pro overflow is cheap enough in credits that Tier 2 barely pays off before its own cap).

Effective all-in `$/generation` at real volume:

| Generations used | Tier 1 max (`$9` + overflow) | Tier 2 max (`$22`) | Better |
|---:|---:|---:|---|
| `500` | `$0.0180` | `$0.0440` | **Tier 1** |
| `2,000` | `$0.0045` | `$0.0110` | **Tier 1** |
| `2,500` | `$0.0077` | `$0.0088` | **Tier 1** |
| `3,000` | `$0.0098` | `$0.0073` | **Tier 2** |
| `5,000` | `$0.0141` | `$0.0044` | **Tier 2** |

At `2,000` generations Tier 2 costs `$0.0110/gen` against Tier 1's `$0.0045` — **`2.4x` worse**, despite advertising the better rate. Pick a tier by volume, not by unit rate: below about `2,600` generations/month, Tier 1 at max discount is the cheapest monthly plan on both absolute cost and effective rate. Both rates above are tenured; a first-month comparison is `$12` vs `$24` at the same allowances, and Tier 1 wins there too below the crossover.

What actually moves the bill, in order:

1. **Utilization.** Tier 1 at `25%` use is `$0.0180/gen`, `4x` worse than the same plan at full use, and worse than credits on most routes.
2. **Tenure.** Worth `25%` on Tier 1 (`$0.0060` to `$0.0045`) — but it accrues over consecutive monthly bills and is forfeited on cancellation. It is earned, not chosen, and it is a switching cost once earned.
3. **Billing period.** Tier 2 annual (`$0.0037`) still beats Tier 2 max monthly (`$0.0044`) by `16%` — and annual is excluded from the loyalty ladder, so the two are alternatives, not a stack.
4. **Tier.** Worth `2.3%`, and only above about `2,600` generations/month.
5. **Route.** Only decides anything for tilesets (credits always win) and `animate-with-text-v3` `@256`/8f (credits win on all but Tier 2 annual).

### Worked baskets

Both assume full allowance utilization (see the scope limit above). `create-1-direction-object` publishes exactly `20` generations at its single `$0.095` rung, so there is no range to pick from; an earlier revision hedged against a `40`-generation reading that does not exist.

A `v3`-centric workflow (`10x` `create-character-v3` `@128`, `40x` v3 `animate-character` `@64`, `20x` Pixen `@128`, `3x` `generate-8-rotations-v3` `@64`):

- Credits: about `$1.20`. Subscription: `93` generations, about `$0.56` at first-month Tier 1. Subscription about `2.1x` better. (All four counts are published; `generate-8-rotations-v3` `@64` bills `1`.)

The same basket plus `5x` `create-1-direction-object`:

- Credits: about `$1.67`. Subscription: `193` generations, about `$1.16` at first-month Tier 1. Subscription about `1.4x` better.

Those `5` Pro calls are `28%` of the USD but `52%` of the generations. Pro Tools are what pull a mixed workflow back toward parity. Observed basket range: **`1.4-2.1x`**, first-month Tier 1.

### Utilization Breaks These Rates

Every rate in Step 1 is a **floor**, reachable only by spending the entire allowance. Assuming allowance does not roll over (strongly indicated, not documented — see [Outside the arithmetic](#outside-the-arithmetic)), actual `$/generation` is `price / generations_actually_used`:

| Plan | At 100% use | At 50% use | At 25% use |
|---|---:|---:|---:|
| Tier 1 monthly, bracket 1 | `$0.0060` | `$0.0120` | `$0.0240` |
| Tier 1 monthly, bracket 4 | `$0.0045` | `$0.0090` | `$0.0180` |
| Tier 1 annual | `$0.0041` | `$0.0083` | `$0.0165` |
| Tier 2 annual | `$0.0037` | `$0.0073` | `$0.0147` |

At `50%` utilization Tier 1 annual (`$0.0083`) no longer beats `create-character-v3` `@168` (`$0.0090`) by much and loses to Pro Tools and every base image route. Annual is worse in this respect than monthly: it requires sustaining the allowance for twelve consecutive months to realize `$0.0041`. **Underuse destroys subscription value faster than route choice does** — a half-used plan is a bigger error than picking the wrong tier.

### Outside the arithmetic

- **Raw credits are flexible USD balance that does not expire.** Subscription allowance is **believed** not to roll over: no public source states this directly, but the upgrade modal offers to "wait until your limit resets next month", and a monthly *reset* implies no carry-over. The FAQ is silent. Treat as strongly indicated, not documented.
- **The hosted MCP is believed to spend subscription generations before USD credits.** This is **not corroborated by any public source** — it rests on this repo's own notes plus the MCP server blurb ("Requires PixelLab subscription (with credit fallback support)"), which implies subscription-first. If true, a subscriber on hosted MCP cannot elect to pay credits for a tileset, and the "credits win on tilesets and first-month Pro" conclusions are actionable only for a credits-only account or on direct REST. Verify before advising anyone to restructure spending around it.
- **The loyalty discount is not free.** Tenure brackets are forfeited on cancellation (with roughly a one-week reactivation grace) and do not apply to annual plans. A deep bracket is a switching cost as much as a benefit: leaving resets you to `$0.0060`.
- **Size caps make some rows unreachable for Tier 1.** From the homepage card logic: Tier 0 and Tier 1 cap at **`320x320`**; Tier 2 reaches **`512x512`** (including edits/inpaint) and up to `10` concurrent jobs; Tier 3 inherits those and reaches `20` concurrent. **`12` of the `124` priced rows sit above Tier 1's `320` cap** — including `create-image-pixen` `512x512`, which an earlier revision of this document compared against Tier 1 rates. That comparison was meaningless and has been removed. The caps bite narrowly: only the five *image* Pro routes (`generate-image-v2`, `generate-with-style-v2`, `generate-ui-v2`, `inpaint-v3`, `edit-images-v2`) reach `341`/`512` at `$0.125`/`$0.185`. The Pro character, object, and animation routes top out at `168x168` or `256x256`, under the cap and reachable on Tier 1, so the generic "Pro Tools, large rung" row survives. Caveat: `320`/`512` are the advertised card benefit; the OpenAPI documents only route-level maxima, and whether the API hard-enforces a per-tier cap is unverified.
- **The precision here exceeds the input quality.** The USD side is officially an estimate that varies with GPU processing time; the generation side is what actually bills. Pro spans `0.77-1.14x` across monthly brackets — a window narrow enough that a few percent of GPU-time drift flips the sign. Treat Pro as "roughly break-even, tenure-dependent", not as a computed edge.
- Subscriptions also add tier benefits — concurrency and priority slots, support level, early access — and holding both a subscription and credits is not an either/or. Quality, retry rate, and feature access sit outside this comparison entirely.

## Estimated Generation-Unit Range Per 1 Credit

Based on the documented examples reviewed, the implied generation-unit ratios for `$1` of USD credit are roughly:

| Workflow family | Example documented pricing | Approx spent generation-units per $1 |
|---|---:|---:|
| Low-cost helper endpoint (`estimate-skeleton`) | about `$0.0051` for `0.1` generation | about `19-20` generation-units |
| Character template animation | `$0.0323-$0.0956` for `1` generation per direction | about `10-31` generation-units |
| Prompt enhancement | `$0.002` for `0.05` generation | `25` generation-units |
| `create-character-v3` (from scratch) | `$0.041` for `2`, `$0.042` for `3`, `$0.045` for `5` generations | about `49-111` generation-units |
| Common one-generation tools | about `$0.0055-$0.02` for `1` generation | `50-181` generation-units |
| Common simple image examples | about `$0.01` for `1` generation | `100` generation-units (a datum; **not** the withdrawn benchmark — see [Credits Versus Subscription](#credits-versus-subscription)) |
| Pro tools | `$0.095` for `20`, `$0.125` for `25`, `$0.185` for `40` generations | about `200-216` generation-units |
| Top-down/sidescroller tilesets | `$0.0079-$0.0099` for `3` generations | about `303-380` generation-units |

Read this table only as "what does USD credit buy". It is **not** a value ranking: a low generation-units-per-`$1` row means the route burns GPU time cheaply relative to its generation cost, which makes it a *strong* subscription route and a weak credit route. See [Credits Versus Subscription](#credits-versus-subscription) for the direction-correct comparison.

Estimated overall range from the reviewed examples: about `10-380` generation-units per `$1` of USD credit. Restricting to content endpoints does **not** raise the floor — template animation at `128`/dir is a content route at about `10` per `$1`, below both helper rows.

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

Density cuts both ways. A route that returns many outputs per generation is efficient against a subscription *allowance*, but it is also doing enough GPU work that its USD price stays low relative to its generation count — which is why tilesets are simultaneously the densest route here and the worst subscription value in [Credits Versus Subscription](#credits-versus-subscription). Density argues for using a route; it does not argue for a payment method. (That inversion holds only under the full-utilization assumption; with allowance to spare, density is unambiguously good.)

## Recommended User-Facing Summary

When asked how much 1 PixelLab credit gives:

> When planning around `$1` of PixelLab USD credit, current public examples imply roughly `10-380` generation-units. In literal returned outputs, that is about `5-674` normal image/candidate outputs. If each tileset tile is counted separately, compact 16-tile outputs imply about `1,616-2,025` tile outputs, while locally observed expanded 25-populated-tile cases could imply up to about `3,165` if the same USD examples apply. The exact number depends heavily on the workflow.

When asked whether a subscription beats credits:

> It depends on the route **and on how long you have been subscribed**, and it genuinely flips. Subscription generations cost `$0.0037-$0.0071` each; the pricing page publishes both a USD price and a generation count for every route, so divide one by the other and compare. In a **first month on Tier 1 (`$0.0060`), the subscription loses on about half the catalog** — all `51` Pro rows sit just below that rate. Monthly prices then step down over consecutive bills (Tier 1 to `$0.0045`), which flips Pro positive and takes the subscription to `119` of `124` rows. So the honest answer to "why does my Pro call cost more on subscription": it does, in month one, and that is temporary — but the discount is earned over months and forfeited if you cancel. `v3` characters, template animation, and helper endpoints run `$0.009-$0.096` per generation and favor the subscription `1.5-16x` at any bracket. Tilesets favor credits on **every** plan and no discount fixes them. `animate-with-text-v3` at `256x256`/8 frames also favors credits on all but Tier 2 annual — `v3` is not automatically subscription-friendly; size and frame count decide. Two things matter more than route choice: **spend the allowance** (a half-used plan doubles your real per-generation cost, dwarfing every route difference) and **pick the tier by volume** — below ~`2,600` generations/month Tier 1 beats Tier 2 despite Tier 2's better headline rate.

When the user asks about budget planning, prefer route-specific estimates:

- For simple one-image calls, quote the selected endpoint's price.
- For Pro grids, state both candidate count and generation-unit cost.
- For tilesets, state both the call cost and the number of returned tile cells.
- For animations, state whether counting final animation files, frames, or directional frame sets.
- For retry-heavy work, budget attempts explicitly. Completed jobs can spend credits even if the result is rejected for quality; failed jobs should be reported from actual `usage` or a balance delta instead of assumed.

## Do Not Overclaim

- Do not say `1 credit = 1 generation`.
- Do not say `$1 always buys 100 generations`.
- Do not quote a single subscription-value percentage such as `Tier 1 = 167%`. The withdrawn figures in this doc's history were artifacts of an arbitrary baseline. Value is per route and changes sign.
- Do not assume a subscription always beats credits. Pro Tools in a first month and tilesets on any plan are cheaper with credits.
- Do not treat generations-per-`$1` as a value ranking; it inverts the subscription comparison.
- Do not quote a subscription `$/generation` without stating the utilization assumption. Every rate here is a floor that requires spending the full allowance; at `50%` use it doubles.
- Do not guess a generation count. The pricing page publishes one for all `124` priced rows; read it instead of inferring from a route's family or label.
- Do not treat `v3` as a subscription-favoring family. `animate-with-text-v3` `@256`/8f bills `8` generations and loses to credits on `11` of `12` plans; `generate-8-rotations-v3` `@256` bills `8` and is `0.79x` at first-month Tier 1. Size and frame count decide, not the label.
- Do not claim PixelLab priced Pro Tools to match the subscription rate. The rung mapping is published and confirmed, but nothing documents *why*; near-parity is an observation, not evidence of intent.
- Do not quote a max-discount rate without its condition. Tenure brackets accrue over consecutive monthly bills, are forfeited on cancellation, and do not apply to annual plans. `$0.0045` is a month-4+ rate, not an available price.
- Do not state as fact that hosted MCP spends generations before credits, or that allowance does not roll over. Both are indicated but uncited to any public source.
- Do not compare a Tier 1 rate against a row above `320x320`. Tier 1 caps there; Tier 2 reaches `512x512`. `12` of `124` rows are unreachable on Tier 1.
- Do not recommend a tier by its `$/generation` rate. Tier choice is worth about `2.3%`; below about `2,600` generations/month Tier 1 at max discount beats Tier 2 at max discount on both absolute cost and effective rate. Recommend by expected monthly volume.
- Do not compare routes only by generation-units when the user cares about literal outputs.
- Do not compare routes only by literal output count when the user cares about quality, consistency, editability, or final usable assets.
- Do not promote this research into runtime rules unless a stable agent behavior changes.
