# HD Region Edit / Animate Spike (Selection-Scoped Editing Above Tool Max Size)

Last reviewed: 2026-07-19. Status: **research spike / future decision — not adopted into the runtime skill.**

Purpose: decide whether Pip should gain a workflow for **editing or animating a region of an image that is larger than the target tool's maximum input size** — the capability the official PixelLab Aseprite extension exposes as its **"Use selection tool to select painting area"** checkbox. Records the size gap, how the reference implementation works, what a headless (REST/MCP) equivalent would look like, the correctness caveats, and a recommendation.

This is background/evidence, not an agent instruction contract. Nothing here changes routing today. See [`pixellab-image-size-limits.md`](pixellab-image-size-limits.md) for the underlying size ceilings.

## The Gap

Generation can produce canvases well above 256×256, but the **edit / animate** endpoints cap much lower — and Pip has no documented way to edit or animate content past those caps. The mismatch (Tier-2 numbers, from the size-limits spike):

| Operation | Endpoint | Max input size | Can it touch a 640×360 background? |
|---|---|---|---|
| Generate scene/background | `generate-image-v2` | up to 792×688 (aspect buckets; 640×360 fine) | — |
| Generate backdrop | `create-image-pixflux(-background)` | 400×400 | — |
| Edit image | `edit-image` | 400×400 | **No** (over 400 wide) |
| Edit image (Pro) | `edit-images-v2` | 512×512 | **No** (over 512 wide) |
| Inpaint / Inpaint Pro | `inpaint` / `inpaint-v3` | 200×200 / 512×512 | **No** |
| Animate with text | `animate-with-text-v3` | 256×256 (and `w·h·frames ≤ 524,288`) | **No** |
| Interpolate | `interpolation-v2` | 128×128 | **No** |

So a user can generate a 640×360 pixel-art screen (the canonical background size) and then **cannot edit or animate it at all** through any single public call. Whole-image HD editing/animation is genuinely unsupported. The extension's answer is not a bigger endpoint — it is to operate on a **max-size sub-region**.

## How The Reference Implementation Works

The official PixelLab Aseprite extension's "Use selection tool to select painting area" toggle appears on Edit Image (Pro), Animate with Text, and Interpolate. Observed UI behavior (the extension talks over its own internal transport, not the public REST v2 contract, so this is a technique, not a public API — same caveat as the client-side section of the size-limits spike):

1. Read the user's marquee selection (origin + bounds) on a canvas larger than the tool max.
2. **Clamp the selection to the tool's valid window** — Edit Image Pro fixes it to a square (256², or 512² on Tier 2+); Animate with Text clamps each dimension to `[32, 256]` (rectangular allowed). If the whole canvas already fits the max, the selection step is skipped and the whole canvas is used.
3. **Crop that region out** and send only the crop to the same endpoint (`edit-images-v2` / `animate-with-text-v3` / `interpolation-v2`). The canvas is *not* resized when a selection is used — resizing would destroy content outside the region.
4. **Paste the result back at the stored selection origin** — a single edited image for edits, or the generated frames placed into the selected region for animation. For animation, `frame_count` is first clamped to the `w·h·frames ≤ 524,288` budget for the cropped size.

Net: it is a **local crop → generate-at-max-size → composite-back** wrapper around the *same* endpoints. No mask, no new API surface, no inpaint. (The extension's separate Inpaint tools are the only ones that build a real mask; these three do not.)

## Headless (Pip) Equivalent

Everything the technique needs is already permitted by SKILL.md **Asset Integrity** — local crop/mask/composite of PixelLab-origin pixels is allowed as long as the generated pixels come from PixelLab and the local steps are reported honestly. A REST/MCP flow would be:

1. Take a user-supplied bounding box (headless has no marquee — the region must be given as coordinates, or the user works in the editor).
2. Crop the region to a size ≤ the endpoint max (square for `edit-images-v2` per its own sizing; ≤256 rectangular for `animate-with-text-v3`; ≤128 for `interpolation-v2`).
3. Call the public endpoint on the crop.
4. Composite the returned image / frames back into the original at the region origin, and report it as a **region-scoped, locally-composited** result.

No new endpoint or credit path is involved — it reuses documented routes at their documented sizes.

## Correctness Caveats (Why This Is Not "HD Editing")

The technique is real but narrow. A general agent adopting it blindly would over-promise:

- **Seams.** These three endpoints regenerate the *whole crop* from a text prompt (+ frames); they are not seam-aware like a masked inpaint. Pasting a regenerated square back into a larger image can leave a visible boundary where the crop edge meets untouched neighbors. It suits **localized, self-contained** edits (add an object in an open area, animate a torch, a glowing orb) far better than blending into dense surrounding art. The API's seam-aware tool is `inpaint-v3` (mask + context) — but it also caps at 512, so it does not solve whole-HD either.
- **Animation is region-only.** Animating a crop yields frames of *that region*; the rest of the HD image is static. Compositing animated region-frames over a static background works for **localized motion/VFX**, not whole-scene animation, and breaks if the motion crosses the crop boundary.
- **No headless selection.** The editor's value comes from the marquee. Headless, the region must arrive as explicit coordinates — an extra required input and a new ambiguity (which region?) to resolve before spending credits.
- **Whole-HD ≠ one crop.** Editing/animating an *entire* >max image coherently would require tiling with overlap and blending across tiles — a materially harder problem with real cross-tile seam and consistency costs, not covered by the single-region technique.

## Recommendation

**Worth adding later as a narrow, opt-in, region-scoped edit / localized-VFX workflow. Not worth adding to the runtime skill now.**

- **Now:** leave it out (YAGNI). There is no current user demand, the technique is reusable ad hoc from existing Asset Integrity permissions when a specific case arises, and the seam / place-back caveats make it error-prone to automate as a default. If a user hits the wall today, the honest answer is already available: generate at ≤max, or edit/animate a region and composite locally with clear reporting.
- **When to promote it into a reference:** if HD backgrounds/scenes become a common Pip target *and* users repeatedly want to edit or add localized motion to them. At that point add a small `references/` entry (not a new endpoint) that:
  - requires an explicit user-provided region (bounding box) — never guesses one,
  - restricts scope to **localized** edits / VFX and says so, refusing to claim seamless whole-image results,
  - reuses `edit-images-v2` / `animate-with-text-v3` / `interpolation-v2` at documented sizes, composites back locally, and reports the crop-and-place as a labeled local step per Asset Integrity,
  - points at `inpaint-v3` (masked, ≤512) when the edit needs to blend into surrounding art rather than fill an open region.
- **Do not** frame it as "HD image editing/animation." It is region-scoped operation on an oversized canvas; the whole-image and cross-tile-seam cases remain unsolved by public endpoints.

## Open Questions / Follow-Ups

- Seam quality of paste-back on dense backgrounds is unmeasured (would cost a paid edit to characterize). Worth a small paid probe before promotion.
- Whether `edit-images-v2`'s `reference_image` can reduce boundary mismatch by feeding surrounding context is untested.
- Tiling-with-overlap for true whole-image HD editing is a separate, larger spike if ever needed.

## Related

- [`pixellab-image-size-limits.md`](pixellab-image-size-limits.md) — the edit/animate/interpolate size ceilings this spike works around, and the client-side-vs-API framing.
- [`../../skills/pixellab-pip/references/local-asset-assembly.md`](../../skills/pixellab-pip/references/local-asset-assembly.md) — permitted local crop/composite/preview operations on PixelLab pixels.
- [`../../skills/pixellab-pip/references/paperdolling.md`](../../skills/pixellab-pip/references/paperdolling.md) — the existing region-scoped edit workflow (body-region selection / masked layer), the closest current analog.
- [`../../skills/pixellab-pip/references/animation.md`](../../skills/pixellab-pip/references/animation.md) — `animate-with-text-v3` frame/pixel budget.
- [`../../skills/pixellab-pip/references/create-image-pro.md`](../../skills/pixellab-pip/references/create-image-pro.md) — large-canvas generation and grid/sheet handling.
