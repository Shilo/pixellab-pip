# Safe Background Removal After `no_background`

Use this reference when a PixelLab generation request set `no_background: true`, but the returned image still has a visible or opaque background.

## Default Behavior

Attempt background removal when the generated image otherwise satisfies the request and the background is safely separable from the requested art. This is an approved exception to the general no-post-processing rule because the structured request already asked PixelLab for a backgroundless result.

For flat exterior backgrounds, a conservative local edge-connected removal pass is acceptable when it preserves the requested art. If that pass leaves enclosed background inside holes, loops, handles, straps, or similar negative spaces, do not globally remove the color when it may also appear in the art. Prefer PixelLab `POST /remove-background` with the original failed generation as the image input, not a locally altered derivative, unless the user explicitly approves a different source.

For PixelLab `/remove-background`, set `background_removal_task` to `remove_simple_background` for flat/simple backgrounds. Use `remove_complex_background` only when the background is actually complex or intertwined. Include a concise foreground/text hint when it helps preserve art pixels or remove enclosed negative spaces.

If safe background removal cannot be achieved, report the output as a failed candidate and ask how to proceed. Do not spend credits on another generation or edit unless the user approves the retry.

## Safe Cases

Background removal is usually safe when the unwanted background is:

- A flat or near-flat exterior fill.
- Connected whitespace or simple canvas color around the subject.
- A simple sheet background that does not share important colors with the art.
- Clearly outside item, character, object, icon, effect, or UI pixels.

Prefer a conservative connected-background removal from image edges for flat backgrounds. Avoid global color removal when that color may appear inside the art.

## Unsafe Cases

Do not use background removal to fix:

- Wrong layout, size, scale, framing, direction, or cell math.
- Borders, UI slots, dividers, text, labels, glyphs, watermarks, or checkerboards baked into the art.
- Merged objects, cropped subjects, missing subjects, or low readability.
- Noisy, smeared, downscaled-looking, or semantically wrong output.
- Backgrounds intertwined with glow, shadow, hair, fur, cloth, glass, particles, or other important art pixels.

If removal would erase outlines, interior colors, shadows needed for readability, or effect pixels, treat it as unsafe.

## Verification

Before calling the post-processed asset final:

- Preserve the original PixelLab output alongside the post-processed file.
- Track the method and source image used for background removal.
- When using PixelLab `/remove-background`, confirm the input was the original failed generation unless the user explicitly approved a different source.
- Confirm output dimensions and requested sheet/cell math still match.
- Confirm alpha exists and the unwanted background is transparent.
- Confirm subject silhouettes, outlines, interior colors, shadows/effects, and readability are preserved.
- Confirm local crops or packages are derived from the post-processed transparent file.
- When using PixelLab `/remove-background`, include the call cost in the final report.
- Report the result as PixelLab output with background-removal post-processing.

Include the method, source image, and a concise preservation check in the final report, such as `connected edge background removal from original generation; preserved non-background pixels` or `PixelLab /remove-background with background_removal_task=remove_simple_background on original generation; preserved readable item pixels`.
