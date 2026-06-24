# Local Asset Assembly

Read this only when creating local preview files from generated PixelLab frames, such as animated GIFs, spritesheets, or other assembled animation artifacts.

## Transparent GIF Previews

Transparent pixel art GIFs are disposal-sensitive: if each frame does not say how the previous frame should be cleared, some viewers accumulate old transparent-frame pixels and show trails.

When using ImageMagick `magick`, put animation settings before the input frames so they apply to every frame:

```powershell
magick -delay 12 -dispose Previous -loop 0 "frame-*.png" "preview.gif"
```

Use `-dispose Previous` by default for transparent sprite previews. Use `-dispose Background` only after verifying the rendered output does not leave trails.

Avoid this anti-pattern:

```powershell
magick "frame-*.png" -delay 12 -dispose Background -loop 0 "preview.gif"
```

Putting `-delay`, `-dispose`, or `-loop` only after the input frames can produce frames with `Dispose: Undefined`, which is exactly the condition that causes past frames to remain visible in transparent GIF previews.

## Verification

Before reporting a GIF preview as complete:

1. Inspect metadata and confirm each frame has the intended delay and a non-undefined disposal method.

   ```powershell
   magick identify -verbose "preview.gif"
   ```

2. Coalesce the GIF back into rendered frames.

   ```powershell
   magick "preview.gif" -coalesce "check-%02d.png"
   ```

3. Compare the coalesced frames to the source PNG frames. Unexpected nonzero differences mean the preview is not faithfully rendering the source frames.

   ```powershell
   magick compare -metric AE "frame-00.png" "check-00.png" null:
   ```

If the preview is only for chat display, still run the verification. A preview that looks wrong can make a good PixelLab generation look broken.
