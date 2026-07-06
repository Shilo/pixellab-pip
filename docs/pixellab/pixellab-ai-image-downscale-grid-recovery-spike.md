# AI-Image Downscale / Pixel-Grid Recovery Spike

Last reviewed: 2026-07-06.

Purpose: capture research findings on reliably downscaling AI-generated "pixel art" (from GPT-image, Gemini/Imagen, etc.) back to a crisp low-resolution grid, so `pixellab-pip` can honestly route "downscale", "unzoom", "remove upscaling", and "fix mixels" requests through the local-tooling fallback slot in [`editor-only-utilities.md`](../../skills/pixellab-pip/references/editor-only-utilities.md) — or decline when recovery is impossible.

This is a code-and-literature spike, not a live-generation spike. It reads the full source of the two dominant open-source tools, identifies why they fail on a representative image, and proposes what a genuinely more reliable system would do. No helper was built.

## The Problem

An LLM asked for "pixel art" typically returns a large canvas (e.g. 1024x1024) *styled* to look pixelated. The apparent "pixels" are blocks of many screen pixels, and the block size is often non-integer and **drifts** across the image (7.9px here, 8.3px there). That drift is what users call "mixels." The goal is to recover a clean NxM indexed-color image where each logical pixel is exactly 1x1, on a uniform grid, with a small palette — without paying generation credits.

## Current Recommendation

**There is no universal reliable downscaler, because "downscale AI pixel art" is two different problems, and every existing tool conflates them.**

| Case | What it is | Reliably recoverable? |
|------|-----------|-----------------------|
| **A** | A true low-res sprite that was nearest-neighbor upscaled (sharp, uniform blocks) | Yes — grid recovery works |
| **B** | An illustration in a pixel-art *style* (anti-aliasing, gradient shading, glow, sub-pixel detail) | No — no consistent grid exists to snap to |

The reliable move is therefore **not a better snapper**. It is a **griddiness gate that classifies A vs. B first**, then routes:

- **Case A** → recover the grid, snap, quantize, done.
- **Case B** → stop and say so. Snapping a non-gridded illustration can only over-downscale or add color noise. Honest alternatives are re-generation through an actual pixel-art model (PixelLab's paid path is *synthesis*, not snapping — which is why it appears to succeed where snappers fail) or an explicitly-labeled approximate downscale to a user-chosen target size.

Do not present any local snapper as a reliable general fix. Do not claim a Case-B image can be made crisp — nothing can, short of re-drawing it.

## What the Existing Tools Actually Do

Both dominant tools use the **same core algorithm**, and it is the fragile part.

### Astropulse `pixeldetector` (the Stable-Diffusion community standard)

[`pixeldetector.py`](https://github.com/Astropulse/pixeldetector):

1. Color-difference projection per axis (`hsum`, `vsum` of adjacent-pixel RGB distance).
2. `scipy.signal.find_peaks` on each projection.
3. **`np.median(np.diff(peaks))`** = the downscale factor.
4. `kCentroid`: crop each output tile, quantize it to **2 colors**, keep the most common.
5. Optional final palette reduction via an elbow-method `determine_best_k`.

### SpriteFusion `pixel-snapper` (Rust/WASM)

[`src/main.rs`](https://github.com/Hugo-Dz/spritefusion-pixel-snapper):

1. k-means quantize the whole image to **16 colors first** (`quantize_image`).
2. Edge-gradient projection (`compute_profiles`, a `[-1,0,1]` derivative summed per axis).
3. Peaks above `0.2*max`, then the **median spacing between peaks** = step size (`estimate_step_size`).
4. An elastic "walker" snaps each cut to a local edge maximum within `±0.35*step` (`walk`), with a uniform-grid fallback (`snap_uniform_cuts`) and cross-axis stabilization (`stabilize_both_axes`).
5. Per cell, take the **mode** (most common color) (`resample`).

### The shared weakness

Both reduce grid detection to **median peak-spacing**: edge projection → peaks → median gap. This assumes edge peaks land on cell boundaries. It holds for Case A (sharp NN-upscaled sprites) and breaks for Case B:

- **"Downscales too much":** anti-aliased gradients create spurious local maxima and smear true seams, so the median gap lands on a wrong (often larger) multiple → too few, too-big output pixels.
- **"Tons of noise, no longer crisp":** the quantize step (pixel-snapper's global k=16, pixeldetector's **2 colors per tile**) coin-flips between similar colors across a smoothly-shaded region → speckle. This is quantization noise, not grid noise.

Pixel-snapper additionally quantizes *before* detecting, which destroys the subtle edges the detector depends on.

## Representative Failure

A user's AI-generated necromancer (heavy anti-aliasing, gradient robe shading, glowing green flame, fine facial detail) came out over-downscaled and speckled from pixel-snapper. Both symptoms are explained by the analysis above: the image is **Case B** — it was never rendered on a consistent integer grid, so there is no grid to recover, and both failure modes are the inevitable result of forcing a grid recovery onto it.

## What a More Reliable System Would Do

Only two changes are defensible reliability wins; neither turns a Case-B image into crisp pixel art.

1. **Replace median peak-spacing with autocorrelation (or FFT) of the edge-projection profile.** Autocorrelation aggregates evidence from *all* seams simultaneously, so missing low-contrast boundaries does not shift the estimate. A sharp, periodic autocorrelation peak also *is* the griddiness signal: sharp/consistent → Case A; flat/ambiguous → Case B. This both fixes the estimator and provides the gate every existing tool lacks.
2. **Quantize last, on the cell grid, in full color until then.** Detect on the full-color image (truer edges). Sample each cell as the **mode of its eroded interior** (erode inward a few px to drop the AA halo). Quantize the resulting ~128x128 cell grid, not the original ~1M pixels — far more stable, and `k` chosen from the actual distinct cell colors (or user-set), never a hardcoded 16 or 2.

Supporting refinements: per-seam local refinement around the autocorrelation-predicted position (pixel-snapper's walker already does this competently) and a **one-number manual factor override** for the ~10% of Case-A images the detector still misjudges. A single human confirmation of one integer is the cheapest route from ~90% to ~99% on Case A.

## Open Questions / Next Steps

- **Measure, don't assert.** For any specific image, run the autocorrelation griddiness test and inspect the profile before claiming a grid exists. The necromancer above is asserted Case B on visual evidence; that should be confirmed empirically on the file, not assumed.
- Decide packaging: a local helper wired into the `editor-only-utilities` unzoom fallback vs. a standalone script. Undecided.
- Confirm whether PixelLab's own unzoom is snapping or re-synthesis; if the latter, it is not comparable to a local snapper and should not be benchmarked as one.

## Sources

- [Astropulse/pixeldetector](https://github.com/Astropulse/pixeldetector) — source read in full.
- [Hugo-Dz/spritefusion-pixel-snapper](https://github.com/Hugo-Dz/spritefusion-pixel-snapper) — `src/main.rs` read in full.
- [Structure-Aware Pixel Art Scaling via Block Size Detection (MDPI, Applied Sciences)](https://www.mdpi.com/2076-3417/16/5/2314).
- [Pixelera — How to Scale Down Pixel Art](https://pixelera.art/blog/how-to-scale-down-pixel-art).
