# PixelLab API Pricing and Model List

Last reviewed: 2026-07-06.

This is a quick reference for public PixelLab API endpoint labels, plugin labels, model/tool families, and official estimated USD prices. Treat prices as estimates: PixelLab states that prices vary with GPU processing time. For exact schemas, verify against the live REST v2 docs or OpenAPI.

Primary sources:

- [PixelLab API catalog](https://www.pixellab.ai/pixellab-api)
- [REST v2 docs](https://api.pixellab.ai/v2/docs)
- [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)

## Billing Notes

- Public REST/MCP auth uses the PixelLab bearer token.
- PixelLab account balance can include subscription generations and USD credits.
- Hosted MCP help reports that billing uses subscription generations first, then USD credits.
- Official USD estimates and API `usage.generations` / credit deltas are distinct reporting units unless PixelLab documents a conversion for the selected route.
- The pricing page shows the same estimate two ways: **generations** (the subscription-spend unit, its default view) and the USD values recorded below. Baselines: most base/`new`/`v3` routes ~1 generation; enhancers ~0.05; `estimate-skeleton` ~0.1; top-down and sidescroller tilesets ~3; Pro Tools ~20-40. Size- and frame-driven routes (`create-character-v3`, `generate-8-rotations-v3`, `animate-with-text-v3`) scale with output area — see [cost-routing.md](../../skills/pixellab-pip/references/cost-routing.md) for the formulas.
- Prompt-enhancement endpoints are separately priced when called or enabled through an endpoint option.

## Concurrency and Priority Slots

The `pixellab-api` page lists **Concurrent jobs** and **priority slots** per account. Confirmed: **sustained, consistent API usage automatically raises an account's concurrency** — how many generation jobs it can run in parallel (stated by PixelLab, 2026).

Unconfirmed — do not state as fact: the exact concurrency limit for any account, whether a paid membership tier raises it, and how priority slots are earned or applied. If an exact limit matters, verify on the live page or with PixelLab support rather than quoting a number.

Agent behavior on the ceiling (`429`/`529`, batch pacing): see [job-lifecycle.md](../../skills/pixellab-pip/references/job-lifecycle.md).

## Image Generation

| Tool label | Endpoint | Model/tool family | Useful for | Estimated price |
|---|---|---|---|---|
| Create M-XL image (new) | `POST /v2/create-image-pixflux` | Pixflux | General image generation, larger image understanding, init images, forced palettes, transparent background | `64x64 $0.00793`; `128x128 $0.00793`; `320x320 $0.0101`; `400x400 $0.0132`; transparent `64x64 $0.0084`; transparent `128x128 $0.00848` |
| Create image S-XL (new) | `POST /v2/create-image-pixen` | Pixen | Text-to-image sprites, outline/detail controls, view/direction, transparent background | `32x32 $0.007`; `64x64 $0.00718`; `128x128 $0.00793`; `256x256 $0.0089`; `512x512 $0.0169` |
| Generate S-M image (style) | `POST /v2/create-image-bitforge` | Bitforge | Small/medium text-to-image, style image, inpainting, init image, forced palette, transparent background | `32x32 $0.0071`; `64x64 $0.00716`; `128x128 $0.00797`; `200x200 $0.01122`; transparent `32x32 $0.00734`; transparent `64x64 $0.00738`; transparent `128x128 $0.00821`; transparent `200x200 $0.01285` |
| Create S-XL image (Pro) | `POST /v2/generate-image-v2` | Pro image generation | Multiple candidates, reference images, style image, higher-cost candidate selection | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Generate with style (Pro) | `POST /v2/generate-with-style-v2` | Pro style generation | Matching a reference style across new images | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Create UI elements (Pro) | `POST /v2/generate-ui-v2` | Pro UI generation | Buttons, health bars, slots, menus | up to `256x256 $0.095`; up to `341x341 $0.125`; up to `512x512 $0.185` |
| Create UI asset (Pro) | `POST /v2/create-ui-asset` | Structured UI asset generation | Saved UI panels with `pieces`, `elements`, style image, project assignment, and polling | current public pricing page has no USD row; local cost docs treat this as Pro / `20-40` generations |

## Image Operations

| Tool label | Endpoint | Useful for | Estimated price |
|---|---|---|---|
| Convert image to pixel art | `POST /v2/image-to-pixelart` | Regular image to pixel art | `64x64 $0.006`; `128x128 $0.00666`; `256x256 $0.01164` |
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
| Animate with text (Pro) | `POST /v2/animate-with-text-v2` | Pro text animation | Reference-image animation, 4/9/16 frames, view and direction controls | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Animate with skeleton | `POST /v2/animate-with-skeleton` | Skeleton-guided animation | Pose/skeleton-driven animation up to 128x128 | `32x32 $0.0136`; `64x64 $0.01433`; `128x128 $0.01572` |
| Estimate skeleton | `POST /v2/estimate-skeleton` | Skeleton helper | Skeleton extraction for skeleton animation | `16x16 $0.00511`; `64x64 $0.00513`; `256x256 $0.00516` |
| Edit animation (Pro) | `POST /v2/edit-animation-v2` | Pro animation editing | Apply edits consistently across 2-16 frames | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Interpolate (Pro) | `POST /v2/interpolation-v2` | Pro interpolation | Generate in-between frames | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |
| Transfer outfit (Pro) | `POST /v2/transfer-outfit-v2` | Pro animation transfer | Apply outfit/appearance to animation frames | up to `128x128 $0.095`; up to `170x170 $0.125`; up to `256x256 $0.185` |

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
| Animate character | `POST /v2/animate-character` | Character animation, per direction | template `64x64 $0.0323`, `128x128 $0.0956`; v3 4 frames `64x64 $0.0129`, `128x128 $0.0145`; Pro up to `128x128 $0.095`, up to `168x168 $0.185` |
| Create character state | `POST /v2/create-character-state` | Character state/variant | up to `84x84 $0.095`; up to `112x112 $0.125`; up to `168x168 $0.185` |
| Create single direction objects | `POST /v2/create-1-direction-object` | Style-consistent object candidates | up to `168x168 $0.095` |
| Create 8 directional objects | `POST /v2/create-8-direction-object` | 8-direction object | up to `84x84 $0.095`; up to `112x112 $0.125`; up to `168x168 $0.185` |
| Animate object | `POST /v2/objects/{object_id}/animations` | Object animation, per direction | v3 4 frames `64x64 $0.0129`, `128x128 $0.0144`; Pro up to `128x128 $0.095`, up to `168x168 $0.185` |
| Create object state | `POST /v2/objects/{object_id}/states` | Object variant/state | single-direction up to `168x168 $0.095`; 8-direction up to `84x84 $0.095`, up to `112x112 $0.125`, up to `168x168 $0.185` |
| Create tiles (Pro) | `POST /v2/create-tiles-pro` | Multiple tile variations | tile up to `42x42 $0.095`; up to `56x56 $0.125`; up to `85x85 $0.185` |
| Generate pixel font (Pro) | `POST /v2/generate-font-pro` | Pro bitmap font generation | Generate a font atlas / pixel font from description and font controls | current public pricing page has no USD row; verify current usage before cost-sensitive calls |

## Prompt Enhancement

| Tool label | Endpoint | Useful for | Estimated price |
|---|---|---|---|
| Enhance Pixen prompt | `POST /v2/enhance-pixen-prompt` | Expand a Pixen image prompt | official estimate per call `$0.002`; live check observed `usage.generations: 0.05` |
| Enhance character v3 prompt | `POST /v2/enhance-character-v3-prompt` | Expand a v3 character prompt | official estimate per call `$0.002`; treat reported usage/credits as a separate unit |
| Enhance animation v3 prompt | `POST /v2/enhance-animation-v3-prompt` | Expand an action for `animate-with-text-v3` using frames as context | official estimate per call `$0.002`; treat reported usage/credits as a separate unit |

## Practical Routing Notes

- For cheap image prompt iteration, start with Pixflux or Pixen.
- For multiple image candidates from one call, use Pro image generation.
- For first-frame animation or chained VFX animation, prefer `animate-with-text-v3`.
- For Pro text animation with view/direction fields and a reference image, use `animate-with-text-v2`.
- For managed character/object assets, prefer the resource-specific character/object endpoints or MCP tools instead of raw image animation endpoints.
