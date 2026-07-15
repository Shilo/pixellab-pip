# PixelLab Image Size Limits (Minimum And Maximum)

Last reviewed: 2026-07-11 (background/widescreen size breakpoints + tier-gating added 2026-07-13).

> **All maxima in this document were measured on a Tier 2 ("Pixel Artisan") subscription.** PixelLab gates max image *size* by plan tier (a soft limit under the hard schema caps). See [Tier / Plan Size Gating](#tier--plan-size-gating-soft-limits) — lower tiers cap several endpoints below the numbers below.

Purpose: document the true minimum and maximum image-size hard limits for every PixelLab REST v2 / MCP tool, separate client-side Aseprite-extension limits from the actual API limits, and record what the schema enforces versus what the server enforces at generation time. This is a research spike for routing and verification. It is not the canonical agent instruction contract.

Motivating goal: support `8px` and `16px` icons, items, and tilesets if the tools allow it. The `32x32` minimum seen in some workflows prompted this review; that floor turned out to be a client-side editor limit, not an API limit.

Source: raw `https://api.pixellab.ai/v2/openapi.json` (parsed field-by-field) plus `https://api.pixellab.ai/mcp/docs`, checked 2026-07-11. Numbers below are quoted from the schema, not inferred. Refresh before exact integrations.

## How To Read These Limits

Most generation endpoints enforce size in up to two layers, and the effective allowed size is the intersection of both:

1. **Per-axis schema bounds** — the request JSON schema puts a `minimum`/`maximum` (or `enum`) on the `image_size.width` / `image_size.height` (or `size` / `tile_size`) fields. These are validated on the request; a value outside them is rejected before generation (FastAPI/Pydantic `422`).
2. **Prose rules layered on top** — total **area** caps, **aspect-ratio**-dependent maxima, **divisibility** requirements, and **padding** behavior, described in the endpoint/field descriptions and enforced during generation. Example of generation-time enforcement: a top-down `color_image` of the wrong size passes request validation but the background job fails with an internal `Expected image of size 64x64`.

So "max 512×512" can mean a per-axis cap, a square-area cap, or an aspect-specific cap depending on the endpoint. The tables call out which.

## Tier / Plan Size Gating (Soft Limits)

Reviewed 2026-07-13. PixelLab gates maximum image **size** by subscription tier — a soft limit that sits *under* the hard per-request schema caps and is a **distinct axis from the monthly generation quota**. **Every other maximum in this document was measured on Tier 2, so it is a Tier-2 ceiling, not a universal one.**

Every image endpoint, with its per-tier max size. `?` = **genuinely undocumented** — no tier-size language exists for it in the raw schema (only edit-image carries one) or on any tool docs page (checked `create-image-flux`, `edit-image`, `text2animation`, `rotate`, `create-image-pro`, `consistent-style`, `create-ui-elements-pro`; only the first three publish a size ladder). The Tier-2 column is what this account measured; `?` cells can be filled **only** by re-probing on a Free/Tier-1 account.

| Endpoint | Free | Tier 1 (Apprentice) | Tier 2+ (tested here) | Status |
|---|---|---|---|---|
| `create-image-pixflux` / `-background` | 200×200 | 320×320 | 400×400 | documented (docs) |
| `edit-image` / `edit-images-v2` | **200×200** | 320×320 | 400×400 | documented (docs **+ raw schema**) |
| `animate-with-text*` | — (T1+ only) | 256×256 | 256×256 | documented (docs) |
| `rotate` | 16/32/64/128 | 16/32/64/128 | 16/32/64/128 | no tier gate |
| `generate-image-v2` | `?` | `?` | 792×688 aspect buckets (16:9 688×384, sq 512×512) | **tier undocumented — untested** |
| `create-image-pixen` | `?` | `?` | 512×512 area | **tier undocumented — untested** |
| `create-image-bitforge` | `?` | `?` | 200×200 | **tier undocumented — untested** |
| `generate-with-style-v2` | `?` | `?` | 512×512 | **tier undocumented — untested** |
| `create-ui-asset` | `?` | `?` | 688×688 | **tier undocumented — untested** |
| `create-character-*` | `?` | `?` | per Characters table | **tier undocumented** |
| tilesets / tiles | `?` | `?` | per Tilesets table | feature needs Apprentice+; size tier undocumented |

The **only** tier-size gate encoded in the raw OpenAPI JSON is edit-image's Free-tier 200×200; the pixflux and animation ladders live on per-tool docs pages, enforced server-side (verified: no other `tier`/`Requires Tier` size language in the schema). For the `?` rows, the priority test is `generate-image-v2`: on a Free/Tier-1 account, does it still accept 688×384 and 512×512, or clamp toward ~320/200 like pixflux does?

Tiers map Apprentice = 1, Artisan = 2, Architect = 3 (docs gate Map Workshop behind "Requires Pixel Apprentice or higher"), matching the `Tier 2: Pixel Artisan` label the balance endpoint returns in `subscription.plan`. Prices are medium-confidence (pricing page is a JS SPA). Sources: `https://www.pixellab.ai/docs/tools/create-image-flux`, `.../edit-image`, `.../text2animation`, `.../rotate`; raw `https://api.pixellab.ai/v2/openapi.json`.

## Empirical Verification (2026-07-11)

The per-axis minimums and maximums below were not just read from the schema — they were live-probed and confirmed as hard rejections. Method: send an out-of-range size (below the minimum or above the maximum) to each endpoint whose size field is schema-constrained, which returns `422` at request validation before any job is created. This is safe (no generation, no credits) and proves the limit is a **reject**, not a silent clamp.

- **74 out-of-range probes (42 below-minimum + 32 above-maximum) across all size-constrained endpoints returned `422`.** Every error was a Pydantic `greater_than_equal` / `less_than_equal` / `enum` violation naming the exact bound (e.g. `Input should be greater than or equal to 16`, `Input should be less than or equal to 792`, `Input should be 16, 32 or 64`).
- **Zero cost, confirmed by a before/after balance snapshot.** The two balance readings were byte-identical across both runs (`$0.00` delta). No background jobs were created.
- `8px` was rejected by every image/tile/icon/character/object endpoint. `16px` was additionally rejected by every `ge 32` / `ge 64` / `ge 192` endpoint. Every per-axis maximum in the tables was confirmed by an over-max rejection.
- **These validation probes cover the per-axis min/max and enum bounds only.** They do not exercise the *generation-time* area/aspect/divisibility rules (e.g. a square-vs-16:9 max, a "min area 32×32", or a `÷4` requirement) — those are enforced after acceptance and can only be confirmed with a paid call. See "What Is Still Uncertain".
- **There is no way to cancel a job to avoid a charge.** The API exposes only `GET /background-jobs/{job_id}` (status) — no cancel endpoint. The `DELETE` routes remove *finished* managed assets (character/object/ui-asset) and do not refund the generation. Once a valid request is accepted, the credit is committed. "Submit then cancel" is not possible.

Not live-tested (would cost credits, because the value is valid and starts a real generation): valid `16px`+ sizes, `remove-background` at ≤`8px` (its min is `1`), and `generate-font-pro` with `glyph_px: 8`. Their limits are taken from the schema. `16px` *success* for icons/items/tilesets is already evidenced by committed showcase assets.

## Bottom Line

- **Minimum is `16` almost everywhere; several routes floor at `32`.** No image/tile/icon endpoint accepts a dimension below `16`. The only exceptions are `remove-background` (per-axis min `1`) and font `glyph_px` (`enum` includes `8`).
- **`8px` icons, items, and tilesets are not supported** (empirically confirmed — see verification section). Every relevant field has a schema minimum of `16` (or an `enum` of `[16, 32, 64]`), so an `8px` request is rejected with a `422` at validation, not padded up. The only place `8` is a legal value anywhere in the API is `generate-font-pro.glyph_px` (`enum [8, 16, 32, 64]`).
- **`16px` icons, items, and tilesets are supported at the API level.** The remaining `16px` risk is semantic quality for non-tile item sprites (they drift larger), already characterized in the 16px spike — not a hard-limit problem.
- **The `32x32` minimum users hit in the PixelLab Aseprite extension is a client-side editor limit,** not an API floor. Different editor tools apply different local minimums.
- Maxima vary widely and are often larger than the product wording implies (for example `generate-image-v2` per-axis max is `792×688`, not `512`; `create-tiles-pro` goes to `256`, not `128`).

## Client-Side (Aseprite Extension) vs API

Review of the official PixelLab Aseprite extension shows its size floors are enforced locally, in the editor, before any request is sent; the `32x32` message is produced client-side, not returned by the server. The extension communicates over its own internal transport rather than the public REST v2 contract, so its minimums are the extension author's choices and do not define the public API limits.

Observed editor behavior (not the API contract):

| Editor tool family | Local minimum enforced in-editor |
|---|---|
| Inpainting v3, Pixen, edit, pose, general images, Canny | `32x32` |
| General image (new), base inpainting, isometric tile | `16x16` |
| Image-to-pixelart output clamp | `4x4` |
| Fixed-size validators (rotation/pose/animation helpers) | one of `256`, `128`, `64`, `32`, `16` |
| Interpolation, movement, base tiles | exact `64x64` |

The extension also shows soft warnings (a "smaller than 48×48" caution, an "above 80×80 is experimental" note) and applies local tier gating for larger sizes. None of these are server-returned floors. **Do not treat any Aseprite-extension size minimum as the API minimum.**

### Editor Floors That Block API-Valid Sizes

Some editor tools hardcode a size floor stricter than the confirmed API, so certain sizes are reachable through REST/MCP but blocked in the Aseprite UI. Tools below are named by their plugin menu label.

Fake blocks — the editor rejects a size the matching REST endpoint accepts:

| Tool (menu label) | Editor block | API allows | Blocked |
|---|---|---|---|
| Edit image ▸ `Edit image` | selection ≥ 32×32 | `edit-image` ≥ 16 | 16–31px |
| Animate ▸ `Interpolate` | exactly 64×64 | `interpolation-v2` 16–128 | everything but 64 |
| Rotate ▸ `Rotate` | only 16/32/64/128 | `rotate` 16–200 | 48, 100, 150, 200, all 129–200 |
| Animate ▸ `Animate with skeleton` | only 16/32/64/128/256 | `animate-with-skeleton` 16–256 | in-between (48, 96, 100…) |
| Animate ▸ `Re-pose (skeleton)` | only 16/32/64/128/256 | skeleton family 16–256 | in-between |
| Create image ▸ `Create S-M image (old)` | 16/32/64, square-only | `create-image-bitforge` 16–200, any ratio | 48, 100, non-square |

Not fake — these match the real API floor, so prefer them for small sizes:

- Create image ▸ `Create S-XL image (pro)` — allows 16×16, matching `generate-image-v2` (confirmed min 16, with a committed 16×16 showcase atlas). This is the editor's genuine 16px path; 16px is **not** REST-only.
- Inpaint ▸ `Inpaint` — min 16; Map ▸ `Create isometric tile` — min 16×16.
- Create image ▸ `Create Image S-XL (New)` (Pixen) — min 32, but that matches `create-image-pixen`'s documented min area 32×32, so it is an honest floor, not a fake block.

Blocked with an unverified backend limit (caveated, not confirmed fake): `Create character with same style` (< 128×128), `Create M-XL image` (modifier ≤ 150×150), Map ▸ `Extend map (old)` (exactly 64×64), Inpaint ▸ `Inpaint M-L (pixpatch v2)` (selection ≥ 32×32). On the max side, some editor tools cap at 200×200 or 128×128, below the `generate-image-v2` API max of 792×688.

Mapping caveat: the editor tools communicate over the extension's internal transport, so a tool may not call the identically named public REST endpoint; treat these as same-family comparisons. The one mismatch backed by a committed asset rather than inference is 16×16 on `generate-image-v2`. `8px` stays blocked on both surfaces.

## REST v2 Limits — Image Generation

| Endpoint | Field | Min (per axis) | Max (per axis) | Additional prose rules |
|---|---|---|---|---|
| `generate-image-v2` | `image_size` | 16×16 | width 792, height 688 | Effective max is aspect-dependent: square 512×512, 16:9 688×384; long axis up to 792 at extreme ratios. `style_image` sets pixel size. **`no_background` defaults to `true` → transparent sky + side bars unless you set `no_background: false` (then opaque full-bleed; verified 0 bars at 688×384).** See empirical subsection below. |
| `create-image-pixen` | `image_size` | 16×16 | 768×768 | Area 32×32 to **512×512**; width and height **divisible by 4**. (768 per axis only reachable at extreme aspect where area ≤ 512×512.) |
| `create-image-pixflux` | `image_size` | 16×16 | 400×400 | Area 32×32 to 400×400. Transparent background blanks area over 200×200. |
| `create-image-pixflux-background` | `image_size` | 16×16 | 400×400 | Area 32×32 to 400×400. `no_background` defaults to `false` (keeps the scene); alternative for opaque edge-to-edge backgrounds ≤400×400 (verified 0px bars, 0% transparency at 400×224, ~$0.0065). |
| `create-image-bitforge` | `image_size` | 16×16 | 200×200 | Max area 200×200. Skeleton keypoints best at 16/32/64. |
| `generate-with-style-v2` | `image_size` | 16×16 | 512×512 | Square; non-standard sizes padded to nearest of {16, 32, 64, 128, 256, 512}. |

### `generate-image-v2` Effective Max Size By Aspect Ratio (Empirical, 2026-07-13)

The raw schema caps each axis (`width ≤ 792`, `height ≤ 688`, both documented "16 to aspect-ratio max") but does **not** publish the aspect formula. The effective per-ratio max is only exposed by the generation-time `400` message, e.g. `image_size must be between 16x16 and 688x384 for this aspect ratio` (free to probe — no job created). Swept across ratios 0.5→2.6 with one identical prompt, the maxima form a fixed set of ~262k–269k-pixel buckets (dims multiples of 8). They are symmetric under transpose (9:16↔16:9, 3:4↔4:3, …) except the wide extreme 792×336, whose transpose 336×792 would need height 792 > the 688 cap. Each bucket labelled by its own dimensions' ratio:

| Bucket ratio | Effective max W×H | Pixels |
|---|---|---|
| 9:16 (0.56, height-capped) | 384×688 | 264,192 |
| 2:3 (0.67) | 424×632 | 267,968 |
| 3:4 (0.75) | 448×600 | 268,800 |
| 4:5 (0.81) | 464×576 | 267,264 |
| 1:1 (1.00) | 512×512 | 262,144 |
| 5:4 (1.24) | 576×464 | 267,264 |
| 4:3 (1.34) | 600×448 | 268,800 |
| 3:2 (1.49) | 632×424 | 267,968 |
| 16:9 (1.79) | 688×384 | 264,192 |
| 21:9 (2.36, width-capped) | 792×336 | 266,112 |

- **Single largest values:** widest **792** (ratio ≥~2.15 → 792×336); tallest **688** (ratio ≤~0.58 → 384×688); most pixels **268,800** (4:3 / 2:3); largest square **512×512**. **`792×688` together never generates** — near-square caps at ≤576×464.
- Requested ratios **snap to the nearest bucket** (16:10 and 3:2 both → 632×424; 16:9/1.85/2:1 all → 688×384); the `400` returns the bucket, not your exact ratio. Bucket *boundary* ratios are approximate (each tested ratio fell inside the range shown), but the max at every standard ratio above is confirmed.
- Any size **≤ its ratio's bucket** generates. Confirmed real generations (paid): 640×360, 634×360 (16:9), 792×300, 792×336 (wide), 344×688 / 360×688 / 380×688 (portrait). Rejected: over per-axis → `422` (1920×1080, 1280×720, 960×540, 793×793, 792×792); over the bucket → `400` (792×688, 400×688, 600×600, …). Isolated before/after balance checks proved every `400`/`422` probe costs **$0.00**; each accepted size costs ~$0.185.

**16:9 widescreen ladder (menus, parallax) — absolute max = `688×384`.** Confirmed: 688×384 generates; every larger 16:9 request (690×388, 696×392, 704×396, 712×400, 768×432 — including exact 16:9 = 1.7778) returns `400 "must be between 16x16 and 688x384 for this aspect ratio"` (free). 688×384 is itself 1.79:1; the largest *mathematically exact* 16:9 (16k×9k) that fits is **672×378** (k=43 → 688×387 exceeds the 384 height cap).

| 16:9 resolution | Works? |
|---|---|
| 1080p 1920×1080 · 720p 1280×720 · 540p 960×540 · 480p 854×480 | ❌ width > 792 (`422`) |
| 432p 768×432 | ❌ passes per-axis, area over the 16:9 max → `400` |
| **max 688×384** | ✅ the ceiling |
| 360p 640×360 · 288p 512×288 · 270p 480×270 · 216p 384×216 · 180p 320×180 · 144p 256×144 · 90p 160×90 · 36p 64×36 · 18p 32×18 | ✅ |
| 9p 16×9 | ❌ height < 16 min (`422`) |

The break sits between 360p (✅ largest standard "p") and 432p (❌); 432p is the telling case — small enough per-axis (768 ≤ 792) but its 331k area exceeds the ~262k budget, so it fails at the aspect layer, not per-axis.

**Most common pixel-art sizes** (all comfortably within limits): **320×180** and **640×360** are the canonical 16:9 pixel-art screen resolutions — both integer-upscale to 1080p (×6 / ×3) and 720p, so they are the usual authoring targets; **640×360** is the default for a full-screen pixel-art background. Also common: 480×270 (16:9), 256×224 / 256×240 (SNES-era), 320×240 (4:3), and square icons 16/32/64/128/256. Note the 16:9 ceiling 688×384 does **not** integer-scale to 1080p (1920/688, 1080/384 are non-integer), so for pixel-perfect upscaling prefer 640×360 or 320×180 and scale up; reserve 688×384 for when raw canvas size matters more than clean scaling.

**Background default gotcha:** `no_background` **defaults to `true`** on `generate-image-v2` (raw schema; "Remove background from generated images"). Omitting it removes the background, so a full-scene landscape loses its sky (~31–39% transparent) and wide canvases gain transparent side bars (634×360 → 5px/side … 792×300 → 38px/side). **Set `no_background: false` for an opaque full-bleed scene** — verified at 688×384 → 0px bars, 0% transparency (this is the Aseprite "Create S-XL image (pro)" "Remove background" checkbox). Per-endpoint `no_background` defaults (raw schema): `generate-image-v2` = **`true`** (removes); `create-image-pixflux` and `create-image-pixflux-background` = **`false`** (keep) — the latter is opaque-by-default but caps at 400×400. Saved outputs under `pixellab-pip-generations/size-probe-2026-07-13/`.

> Correction (2026-07-13): an earlier draft claimed `generate-image-v2` had *no* `no_background` field and forced removal. Wrong — that came from a WebFetch summary, not the raw schema. The field exists and defaults to `true`. Read field existence/defaults from `openapi.json` directly.

## REST v2 Limits — Tilesets And Tiles

| Endpoint | Field | Allowed values | Notes |
|---|---|---|---|
| `create-tileset` / `tilesets` (top-down) | `tile_size` (w/h) | `enum [16, 32, 64]`, default 16 | `standard` mode: 16/32. `pro` mode: 16/32/64 plus shape controls. |
| `create-tileset-sidescroller` / `tilesets-sidescroller` | `tile_size` (w/h) | `enum [16, 32]`, default 16 | No 64 option. |
| `create-tiles-pro` | `tile_size` (int) | 16 to **256**, default 32 | 32 recommended. `tile_height` for non-square; `style_images` override shape/size. |
| `create-isometric-tile` | `image_size` | 16×16 to 64×64 | Sizes above 24×24 documented as better. `isometric_tile_size` default 16 (recommended 16 or 32). |

## REST v2 Limits — Characters And Objects

| Endpoint | Field | Min | Max | Notes |
|---|---|---|---|---|
| `create-character-v3` | `image_size` | **32** (schema-enforced; prose says 16) | 256 | Live probe rejected 8 and 16 with `ge 32`. Reference mode advisory (model picks). `reference_image` max 256×256. Canvas padded ~2×. |
| `create-character-with-4-directions` | `image_size` | 16×16 | 128×128 | Per-direction reference images must match `image_size`. |
| `create-character-with-8-directions` | `image_size` | 16×16 | 128×128 | `standard` (1 gen) vs `pro` (20–40 gens). |
| `create-character-pro` | `image_size` | 32×32 | 168×168 | `reference_image` max 168×168; `concept_image` max 1024×1024. Canvas padded ~2×. |
| `create-1-direction-object` | `size` | 32 | 256 | Default 64. Mutually exclusive with `style_images` (max 256×256 each); size drives object count. |
| `create-8-direction-object` | `size` | 32 | 168 | Default 64; the 8-rotation pipeline rejects anything larger than 168. |
| `portrait-character-pro` | `result_size` | `enum [16, 32, 48, 64, 128, 160]`, default 64 | | 128/160 render at 2K (cost more). |

## REST v2 Limits — Animation And Rotation

| Endpoint | Field | Min | Max | Notes |
|---|---|---|---|---|
| `animate-with-text` (v1) | `image_size` | fixed 64×64 | fixed 64×64 | Only 64×64. |
| `animate-with-text-v2` | `image_size`, `reference_image_size` | 32×32 | 256×256 | |
| `animate-with-text-v3` | `first_frame` / `last_frame` | — | 256×256 | v3 max 256×256. |
| `animate-with-skeleton` | `image_size` | 16×16 | 256×256 | |
| `animate-character` / `characters/animations` | frames | — | 256×256 | v3 mode subject to 256×256. |
| `objects/{object_id}/animations` | frames | — | 256×256 | v3 mode subject to 256×256. |
| `edit-animation-v2` | `image_size` | 16×16 | 256×256 | |
| `interpolation-v2` | `image_size` | 16×16 | 128×128 | |
| `transfer-outfit-v2` | `image_size` | 32×32 | 256×256 | |
| `generate-8-rotations-v2` | `image_size` | 32×32 | 168×168 | |
| `generate-8-rotations-v3` | `first_frame` | — | 256×256 | |
| `rotate` | `image_size` | 16×16 | 200×200 | |

## REST v2 Limits — Edit / Convert / Utility

| Endpoint | Field | Min | Max | Notes |
|---|---|---|---|---|
| `edit-image` | `image_size`, `width`, `height` | 16×16 | 400×400 | Reference and target both 16–400. |
| `edit-images-v2` | `image_size` | 32×32 | 512×512 | 1–16 input images depending on size. |
| `inpaint` | `image_size` | 16×16 | 200×200 | Max area 200×200. |
| `inpaint-v3` | `inpainting_image` | 32×32 | 512×512 | Mask must match dimensions. |
| `image-to-pixelart` | `image_size` (input) | 16×16 | 1280×1280 | Output `output_size` 16×16 to 320×320; recommended output ≈ ¼ input. |
| `image-to-pixelart-pro` | (auto) | — | — | No output-size field; native pixel scale detected and downscaled automatically. |
| `resize` | `reference_image_size`, `target_size` | 16×16 | 200×200 | Both source and target, area 16×16 to 200×200. |
| `remove-background` | `image_size` | **1×1** | 400×400 | Lowest minimum in the API; max area 400×400. |

## REST v2 Limits — UI, Fonts, Maps

| Endpoint | Field | Min | Max | Notes |
|---|---|---|---|---|
| `create-ui-asset` | `image_size` | **192×192** | 688×688 | Default 256×256; max per axis aspect-dependent (square 512, tall/wide 688). Highest minimum in the API. |
| `generate-ui-v2` | `image_size` | 16×16 | width 792, height 688 | Default 256×256; 16 to aspect-ratio max. |
| `generate-font-pro` | `image_size` | `enum ['1K', '2K']` | | Resolution/pricing tier, not pixel dims. |
| `generate-font-pro` | `glyph_px` | `enum [8, 16, 32, 64]`, default 16 | | **Only field in the API that accepts `8`** — 8px generates a rough-but-usable glyph atlas (tested). Native bitmap size per glyph. |
| `map-objects` | `image_size` | 32×32 | 400×400 | Default 128×128. Basic mode max area 400×400; inpainting mode max area 192×192. |

## MCP Tools

MCP tool docs expose defaults but not explicit min/max; the underlying routes map to the REST limits above, so treat the REST bounds as authoritative.

| MCP tool | Size parameter | Default | Effective limit (from REST route) |
|---|---|---|---|
| `create_character` | `size` | 48 | v3: 16–256 |
| `create_topdown_tileset` | `tile_size` | `{16, 16}` | enum 16/32/64 |
| `create_sidescroller_tileset` | `tile_size` | `{16, 16}` | enum 16/32 |
| `create_isometric_tile` | `size` | 32 | 16–64 |
| `create_tiles_pro` | `tile_size` | 32 | 16–256 |
| `create_ui_asset` | `width` / `height` | 256 | 192–688 |
| `create_portrait_character` | `result_size` | 64 | enum 16/32/48/64/128/160 |
| `create_font` | `image_size` / `glyph_px` | `1K` / 16 | glyph_px enum 8/16/32/64 |
| `create_1_direction_object` / `create_8_direction_object` | `size` | 64 | 32–256 / 32–168 |
| `create_map_object` | `width` / `height` | 128 | 32–400 |

## For The Goal: 8px And 16px Icons, Items, Tilesets

| Target | Supported? | Basis |
|---|---|---|
| `16px` top-down / sidescroller tileset | Yes | `tile_size` enum includes 16. |
| `16px` tile variants (`create-tiles-pro`) | Yes | `tile_size` min 16. |
| `16px` isometric tile | Yes | `image_size` min 16×16. |
| `16px` icons/items canvas (`generate-image-v2`) | Yes | `image_size` min 16×16. |
| `16px` standalone item/icon **semantics** | Partial | Item sprites drift larger; full-cell tiles/textures reliable, transparent item sprites experimental. See [`pixellab-16px-item-sprite-generation-spike.md`](pixellab-16px-item-sprite-generation-spike.md). |
| `8px` icons / items | **No** | `generate-image-v2` and all image routes have schema min 16 → request rejected. |
| `8px` tilesets | **No** | Top-down/sidescroller `tile_size` enum is `[16,32,64]`/`[16,32]`; `create-tiles-pro` min 16; isometric min 16×16. All reject 8. |
| `8px` font glyphs | Yes | `generate-font-pro.glyph_px` enum includes 8 — the only 8px-native path in the API. |

Conclusion for the goal:

- **`16px` is fully achievable** for icons, items, and tilesets at the API level; the only open question is `16px` semantic quality for non-tile item sprites, already researched.
- **`8px` is not achievable** for icons, items, or tilesets through any documented endpoint — the hard minimum is `16`, enforced at request validation. If `8px` game assets are required, the paths are: (a) generate at `16px`+ and downscale locally with honest post-processing reporting, or (b) use `generate-font-pro` with `glyph_px: 8` when the assets are genuinely glyph-like.

## Follow-Up Tests (All Resolved 2026-07-11)

Every generation-time rule left open was probed; all resolved, almost all via free validation errors.

- **`create-image-pixen` generation-time rules (validation-enforced, free `422`):** width/height must be a **multiple of 4** (`18×18` → `multiple_of 4`), and total **area `32×32` to `512×512`** (`600×600` → "Canvas must be size 512x512 area or smaller"). It *does* generate at `16×16` (HTTP 200, ~$0.0082) — `16` clears the area floor and is ÷4. So pixen's valid range is per-axis 16–768, **÷4**, area 32×32–512×512. (In the 16×16 test `no_background` worked with a short single-subject prompt; the earlier ~91%-opaque came from overloading the canvas with a 64-item list. Coins can hollow out when their center matches the removed background color — a background-removal artifact fixed by local edge-flood removal, not a limit. See the Pixen Single-Subject section of the [16px item spike](pixellab-16px-item-sprite-generation-spike.md).)
- **`create-image-pixflux` at `16×16`: rejected** — `422` "Canvas must be size 32x32 area or larger". Pixflux's real floor is a **32×32 area**, *unlike* pixen (16); the per-axis schema min 16 is overridden by the area rule at validation.
- **`generate-image-v2` aspect max is enforced:** `600×600` → `400` "image_size must be between 16x16 and 512x512 for this aspect ratio". The square max is `512×512` (the per-axis `792`/`688` apply only at extreme aspect ratios).
- **`glyph_px: 8` fonts: generate** (HTTP 200, ~$0.095) a real **TTF font** (`ttf_base64`) plus a glyph-atlas preview image. Rendered as actual text, the 8px font is **partially legible but rough** — some words read, but several glyphs are broken/malformed and the API flagged 2 as `suspect_glyphs`. Experimental, not production-clean; judge a font by rendering text with the TTF, not by the atlas grid. This is the only 8px-native path in the API. (`weight: Bold` or `image_size: 2K` may improve small-glyph legibility; untested.)
- **`remove-background` at `8×8`: works** (HTTP 200, ~$0.005) — cleanly removed a solid background and kept the foreground at 8×8; the `1×1` floor is real.
- **`16px` non-tile item/icon semantic quality** is a quality question (not a limit), characterized in the [16px item spike](pixellab-16px-item-sprite-generation-spike.md), which also has a palette-clamp demo (over-shaded pixel art clamps cleanly to ~16–24 colors while keeping shape).

Nothing about the size limits themselves remains untested. Do not promote an `8px` icon/item/tileset claim — it is confirmed rejected; the only 8px-native path is font `glyph_px: 8`.

## Related

- [`pixellab-16px-item-sprite-generation-spike.md`](pixellab-16px-item-sprite-generation-spike.md) — why 16px full-cell tiles work better than strict 16px non-tile item sprites.
- [`pixellab-32px-vfx-atlas-density-spike.md`](pixellab-32px-vfx-atlas-density-spike.md) — semantic scale drift at small cell sizes.
- [`../../skills/pixellab-pip/references/create-image-pro.md`](../../skills/pixellab-pip/references/create-image-pro.md) — sub-32px cell request handling.
- [`../../skills/pixellab-pip/references/tileset.md`](../../skills/pixellab-pip/references/tileset.md) — tile_size routing.
- [`../../skills/pixellab-pip/references/prompt-limits.md`](../../skills/pixellab-pip/references/prompt-limits.md) — prompt/field character limits (same OpenAPI source).
- [Resources](../resources.md#official-pixellab) — official documentation entry points.
