# Safe Background Removal After `no_background`

Use this reference when a PixelLab generation request set `no_background: true`, but the returned image still has a visible or opaque background.

## Default Behavior

Attempt background removal when the generated image otherwise satisfies the request and the background is safely separable from the requested art. This is an approved exception to the general no-post-processing rule because the structured request already asked PixelLab for a backgroundless result.

For flat exterior backgrounds, first try the bundled deterministic helper:

```bash
python assets/background_removal.py input.png output.png --report report.json
```

Run it on the original failed generation. The helper removes only edge-connected background, then analyzes enclosed background-colored components as uncertainty signals. Use the output only when its JSON report says `local_result_status: passed_conservative_checks` and visual verification confirms it preserved the requested art. If the report says `needs_pixellab_fallback`, continue to PixelLab `/remove-background` with the original failed generation.

For non-default flat backgrounds, pass `--bg-color R,G,B` instead of auto-sampling. Use `--tolerance` only for near-flat compression or anti-alias variation, kept conservative so art pixels sharing the background color survive. Run `--help` for the full tuning surface before changing enclosed-component or outline thresholds.

If the helper cannot execute, such as missing Python, missing Pillow, a file error, or an ambiguous background-sampling error, skip further local guessing and use PixelLab `POST /remove-background` with the original failed generation as the image input. If local removal leaves enclosed background inside holes, loops, handles, straps, or similar negative spaces, do not globally remove the color when it may also appear in the art; use PixelLab fallback unless the user explicitly approves a different source or repair path.

For PixelLab `/remove-background`, always set `background_removal_task` to `remove_simple_background` for PixelLab Pip background-failure recovery.

If safe background removal cannot be achieved, report the output as a failed candidate and ask how to proceed. Do not spend credits on another generation or edit unless the user approves the retry.

## Safe Cases

Background removal is usually safe when the unwanted background is:

- A flat or near-flat exterior fill or connected canvas color around the subject that does not share important colors with the art.
- Clearly outside item, character, object, icon, effect, or UI pixels.

Prefer a conservative connected-background removal from the image edges. Avoid global color removal when that color may also appear inside the art.

## Unsafe Cases

Do not use background removal to fix:

- Content problems it cannot repair: wrong layout, size, scale, framing, direction, cell math, merged/cropped/missing subjects, or noisy, smeared, downscaled-looking, or low-readability output.
- Backgrounds intertwined with important art pixels (glow, shadow, hair, fur, cloth, glass, particles), or borders, UI slots, dividers, text, labels, glyphs, watermarks, or checkerboards baked into the art.

## Verification

Before calling the post-processed asset final:

- Preserve the original PixelLab output alongside the post-processed file.
- Track the method and source image used for background removal.
- If the bundled helper was used, keep or summarize its JSON report, including `local_result_status`, `fallback_reasons`, `remaining_background_like_pixels`, and any significant unresolved enclosed components.
- When using PixelLab `/remove-background`, confirm the input was the original failed generation unless the user explicitly approved a different source.
- Confirm output dimensions and requested sheet/cell math still match.
- Confirm alpha exists and the unwanted background is transparent.
- Confirm subject silhouettes, outlines, interior colors, shadows/effects, and readability are preserved.
- Confirm local crops or packages are derived from the post-processed transparent file.
- When using PixelLab `/remove-background`, include the call cost in the final report.
- Report the result as PixelLab output with background-removal post-processing, and include the method, source image, and a concise preservation check.
