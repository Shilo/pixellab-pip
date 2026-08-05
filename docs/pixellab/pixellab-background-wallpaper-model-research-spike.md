# PixelLab Background And Wallpaper Model Research Spike

**Date:** 2026-08-05  
**Status:** directional finding; suitable for routing guidance, not a new blind benchmark  
**Question:** Which PixelLab image model is the best fit for game backgrounds, wallpapers, and wide environmental scenes?

## Executive finding

The four models have distinct practical roles for this category:

| Model | Best current use case for backgrounds/wallpapers | Main trade-off |
|---|---|---|
| **Pro** | Premium hero wallpaper when quality and stylization both matter | Highest cost in this test: 40 generations for one 16:9 candidate |
| **Pixen** | Detail-first full scene: mountains, islands, foreground texture, and a focal subject | Can be visually dense or tighter-framed; less useful when the backdrop should stay simple |
| **PixFlux** | Stylized, atmospheric, subject-light or subjectless backdrop; good value for broad scenery | Low detail at its native ceiling; small focal subjects and reflections may not read |
| **BitForge** | No dependable production-wallpaper role identified; possible thumbnail, rough moodboard, or coverage/style-control route | Maximum 200×200 per the current contract; the tested 192×108 output was too small and did not clearly depict the dragon |

### Recommended routing

- Choose **Pixen** when the wallpaper is a full scene with a prominent subject and the user asks for detail.
- Choose **PixFlux** for a stylized atmospheric backdrop, especially when the focal subject is absent or intentionally simple.
- Choose **Pro** for a premium hero image where a strong mix of finish, readability, and stylized art direction justifies the cost.
- Do not choose **BitForge** as the default for a production 16:9 wallpaper. Use it only when a low-resolution output is acceptable or when its specialized controls—such as coverage or reference-style guidance—are the actual requirement.

This is more useful than a single “best model” ranking: **subjectless backdrop** and **subject-plus-environment scene** are different wallpaper jobs.

## Test setup

The comparison used one shared 16:9 lake scene: an expansive central lake, mountains, a luminous sky, islands on both foreground sides, one flying dragon, and aligned reflections. The original run used seed `1529010282`; PixFlux and BitForge were each retried once with a stronger focal-subject prompt and seed `1546285305` after the dragon was not readable in the first result.

The images were generated at the largest exact 16:9 canvas available for each route in this run:

| Model | Surface / route | Canvas | Usage | Visual result |
|---|---|---:|---:|---|
| Pro | MCP `create_image_pro` | **672×378** | 40 generations; 1 candidate | Passed the full scene brief; strongest balance of polish and stylization |
| Pixen | MCP `create_image_pixen` | **640×360** | 1 generation | Passed the full scene brief; strongest visible scene detail |
| PixFlux | MCP `create_image_pixflux` | **384×216** | 1 generation + 1 retry | Stylized lake and reflections read; retry made the dragon visible, but still small |
| BitForge | REST `POST /v2/create-image-bitforge` | **192×108** | 1 generation + 1 retry | Lake, mountains, islands, sky, and reflections read; dragon remained unclear |

All saved outputs were valid opaque PNGs and exact 16:9. The first attempted PixFlux size, `400×225`, was rejected before generation because the dimensions were not divisible by four; the successful exact-ratio fallback was `384×216`.

The [packed comparison preview](../../pixellab-pip-generations/lake-dragon-16x9-model-comparison/lake-dragon-16x9-spritesheet-preview.png) preserves the native render sizes. The [initial manifest](../../pixellab-pip-generations/lake-dragon-16x9-model-comparison/lake-dragon-16x9-model-comparison.manifest.json) and [retry manifest](../../pixellab-pip-generations/lake-dragon-16x9-model-comparison/lake-dragon-16x9-model-comparison-retry.manifest.json) contain the exact requests, job IDs, usage, and verification notes.

## Findings by model

### Pro: the quality/stylization balance

The Pro result is the strongest all-around wallpaper candidate from this four-image run. It combines a polished environment, strong atmospheric color, readable silhouettes, and a stylized pixel-art finish. The dragon and its mirrored reflection remain legible while the lake, mountain range, side islands, and sky still have enough structure to feel like a finished scene.

That matches the broader static-image benchmark's description of Pro as a high-quality route and its finding that Pro edges the other models on subjectless backgrounds. The cost matters, though: this run consumed 40 generations for one candidate, so Pro is best reserved for a final hero background, a premium title-screen image, or a wallpaper that will be seen large and often—not every exploratory backdrop.

**Use Pro when:** the request emphasizes a finished-looking, stylized wallpaper and the budget allows a quality-first choice.

**Avoid defaulting to Pro when:** the request is a subject-plus-environment scene that Pixen can cover well, or when the background is only a low-attention decorative layer.

### Pixen: the detail-first full scene

Pixen produced the most detailed-looking environmental scene in the comparison. Mountain layers, island silhouettes, foreground vegetation, water reflections, and the dragon all have strong pixel-level texture. It reads like a detailed in-game scene rather than a loose mood painting.

This is the best fit when “background” really means **a full illustrated scene with a subject inside it**. The broader benchmark also found Pixen strongest for scenes containing both a subject and an environment, even though it was not the best-value choice for a subjectless backdrop.

The cost is not the issue here—Pixen used one generation in this run—but composition can become dense or tight. Prompt for open water, readable negative space, and an uncropped wide composition when the image is meant to sit behind gameplay or UI.

**Use Pixen when:** detail, environmental texture, and a complete scene matter more than minimalism.

**Avoid defaulting to Pixen when:** the user wants a quiet, low-detail background or a simple atmospheric color field.

### PixFlux: stylized, broad, and low detail

PixFlux produced the most simplified and stylized reading of the scene. The lake, mountain masses, sky, and mirrored color fields are clear and attractive, but the low-detail treatment does not hold small focal subjects well. Even after a retry that explicitly enlarged and centered the dragon, the dragon and reflection remained much smaller and less detailed than requested.

That makes PixFlux a strong **background layer** model when the backdrop should establish mood, color, and depth without competing with gameplay. It is also the best-value choice for broad scenery in the existing static-image benchmark. Its loose, painterly/stylized tendency is a feature for atmospheric wallpapers, not a defect to eliminate in every prompt.

**Use PixFlux when:** the scene is primarily a sky, lake, mountain, forest, or parallax backdrop; the subject is absent, distant, or intentionally low-detail; and one low-cost generation is preferable.

**Avoid defaulting to PixFlux when:** a small dragon, character, architecture detail, or reflection must be immediately readable at the native canvas size.

### BitForge: no established wallpaper role yet

BitForge is the unresolved model in this category. Both its initial and retry outputs established the lake, mountains, sky, islands, and reflections, but neither showed a clearly recognizable dragon. At `192×108`, the output is also materially smaller than the other renders, and its ceiling prevents it from serving as a like-for-like production wallpaper route.

The current evidence does not justify a general BitForge wallpaper use case. The most plausible narrow uses are:

- low-resolution thumbnails or moodboard tiles where semantic detail is not important;
- rough composition or color exploration before paying for a larger final render;
- jobs that specifically require BitForge's coverage control or reference-style inputs, if the downstream asset can remain small.

Those are **candidate uses**, not validated strengths from this spike. For a normal 16:9 production background, BitForge should be treated as a fallback of last resort or skipped.

## Background versus wallpaper routing matrix

| Request shape | Default | Why |
|---|---|---|
| Quiet sky, lake, mountains, mist, or abstract scenery with no focal subject | **PixFlux** | Broad stylization, low detail, low cost, and good value for backdrop work |
| Full scene with a dragon, character, vehicle, or other focal subject | **Pixen** | Strongest subject-plus-environment scene read and highest environmental detail |
| Premium title screen, splash art, or hero wallpaper | **Pro** | Best balance of finish, readability, atmospheric treatment, and stylization in this test |
| Small thumbnail, rough moodboard, or coverage-driven experiment | **BitForge only conditionally** | The only plausible role found, but the 200×200 ceiling makes it unsuitable for normal wallpaper delivery |

## Prompt and controls

The initial shared prompt was:

```text
Wide fantasy pixel-art lake panorama, fixed eye-level side-on landscape composition. A calm expansive lake fills the center; layered blue, partly snow-capped mountains sit on the horizon beneath a luminous sky of peach, gold, lavender, and deep-blue clouds. Forested islands frame both foreground sides, leaving open water in the middle. One majestic dragon flies above the central water with wings spread. Mirror-like ripples reflect the sky, mountains, islands, and a clearly aligned dragon reflection. Full-bleed opaque scene, atmospheric depth, crisp readable pixel art, no text.
```

The retry prompt used for PixFlux and BitForge was:

```text
Wide fantasy pixel-art lake panorama, fixed eye-level side-on landscape composition. A calm expansive lake fills the center; layered blue, partly snow-capped mountains sit on the horizon beneath a luminous peach-gold-lavender sky. Forested islands frame both foreground sides. Make one large, unmistakable majestic dragon the main focal subject in the upper center, fully visible in profile with wings spread; place a clear full-body mirrored dragon reflection directly below it on the water. Also reflect the sky, mountains, and islands across the lake. Full-bleed opaque scene, strong silhouette contrast, readable dragon and reflection at small resolution, crisp pixel art, no text.
```

All routes used opaque full-bleed output (`no_background: false`) and a side view where supported. PixFlux and BitForge used highly detailed detail/shading settings; BitForge also used `coverage_percentage: 100`. The BitForge retry negative description was:

```text
text, logos, borders, blank margins, tiny or hidden dragon, missing dragon, unclear dragon reflection, duplicate dragons, people, boats, buildings
```

## Limitations

- This is a four-image applied test, not a blind benchmark. The initial run held the prompt and seed constant, but the two retries used a revised prompt and a new seed.
- The models did not share the same maximum canvas. Pro and Pixen therefore had more pixels available than PixFlux and BitForge; that is part of the real routing decision, but it makes pure visual ranking less fair.
- Visual review was human inspection of static outputs. No game-engine UI-overlap, integer-upscale, scrolling, tiling, or multi-monitor wallpaper test was performed.
- BitForge's possible thumbnail/coverage/reference-style uses need a separate controlled test. This spike only establishes that it is a poor fit for the tested production-style 16:9 scene.
- The existing [static-image benchmark](../pixellab-image-model-benchmark-results.md) is broader and should remain the source for general model routing. This spike narrows that evidence to backgrounds and wallpapers.

## Next research step

If BitForge needs a useful role, the next test should stop asking it to compete as a wallpaper generator. Run a small controlled matrix for `coverage_percentage`, style-reference transfer, and thumbnail readability at `64×36`, `128×72`, and `192×108`; compare it against PixFlux at the same sizes. If it does not win a clearly defined small-asset task, remove it from background/wallpaper routing defaults.

## Sources

- [PixelLab v2 LLM API reference](https://api.pixellab.ai/v2/llms.txt) — current endpoint inventory, including Pro, PixFlux, Pixen, and BitForge image routes.
- [PixelLab v2 OpenAPI specification](https://api.pixellab.ai/v2/openapi.json) — current request fields and documented route capabilities.
- [PixelLab image size limits research](pixellab-image-size-limits.md) — repository evidence for per-route aspect, area, grid, and maximum-size behavior.
- [PixelLab static-image model benchmark](../pixellab-image-model-benchmark-results.md) — broader blind comparison and model-routing context.
