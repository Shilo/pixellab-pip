# Local Asset Assembly

Read this only when creating local preview files from generated PixelLab frames, such as animated GIFs, spritesheets, or other assembled animation artifacts.

For Aseprite-specific opening, import/export, layers, frames, tags, `.aseprite` workspace creation, or Aseprite CLI/Lua behavior, read `aseprite-cli.md` instead.

Local assembly is not art generation or editing. Use it only to assemble, preview, format-convert, or verify PixelLab-generated or user-supplied files; do not create or alter requested visual content locally.

Preserve animation frame order by default. Do not create ping-pong, reversed, duplicated, trimmed, interpolated, or otherwise reordered playback variants unless the user explicitly asks for that style. If the direct sequence does not loop cleanly, report that verification result instead of silently packaging a repaired-looking derivative as the final animation.

Write local previews, spritesheets, manifests, ZIPs, and verification scratch files under the same project/workspace `pixellab-pip-generations/` output tree as the source PixelLab generation unless the user explicitly states or approves another directory. For PixelLab generation manifests, follow `usage-reporting.md` and store the route's job IDs, asset IDs, child/result IDs, seeds, and seed provenance when those fields exist. Do not scatter derived files into the repository root, generic `outputs/`, or temp folders except for short-lived tool scratch that is not reported as a final output.

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
   New-Item -ItemType Directory -Force "check-frames" | Out-Null
   magick "preview.gif" -coalesce "check-frames/check-%04d.png"
   ```

3. Compare every coalesced frame to the matching source PNG frame by sorted order. Unexpected nonzero differences mean the preview is not faithfully rendering the source frames.

   ```powershell
   $sourceFrames = @(Get-ChildItem "frame-*.png" | Sort-Object Name)
   $checkFrames = @(Get-ChildItem "check-frames/check-*.png" | Sort-Object Name)
   if ($sourceFrames.Count -ne $checkFrames.Count) { throw "Frame count mismatch" }
   for ($i = 0; $i -lt $sourceFrames.Count; $i++) {
     magick compare -metric AE $sourceFrames[$i].FullName $checkFrames[$i].FullName null:
   }
   ```

If the preview is only for chat display, still run the verification. A preview that looks wrong can make a good PixelLab generation look broken.
