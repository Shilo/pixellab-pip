# Local Asset Assembly

Read this for atlas or spritesheet grid inspection previews and when creating local preview or assembled artifacts from PixelLab-generated frames.

For Aseprite-specific opening, import/export, layers, frames, tags, `.aseprite` workspace creation, or Aseprite CLI/Lua behavior, read `aseprite-cli.md` instead.

Local assembly only assembles, previews, format-converts, or verifies existing PixelLab-generated or user-supplied pixels — it never creates or alters requested art. Preserve frame order, write outputs to the run's `pixellab-pip-generations/` tree, and record manifest fields per `usage-reporting.md` (SKILL.md holds the asset-integrity, frame-order, and output-folder rules).

## Atlas And Spritesheet Grid Inspection

For every atlas or spritesheet request with known or requested cell dimensions, create a separate, clearly labeled inspection preview showing the expected cell grid. Keep the preview separate from final deliverables, never bake it into the requested asset, and never treat a correctly drawn grid as proof that the underlying content follows it.

When the cell size is known, derive the expected column and row counts from the actual canvas dimensions. Require each canvas dimension to divide evenly by its corresponding cell dimension; if either does not, report the mismatch rather than rounding or drawing a misleading grid.

Create the required inspection preview as a copy with a contrasting one-pixel grid overlay at every cell boundary. Use local tooling such as ImageMagick only on the preview copy; do not alter the source or final deliverable. Name it explicitly, for example `<name>-inspection-grid.png`, and label it `Inspection aid — expected grid overlay` wherever it is shown or reported.

For a canvas `W` by `H` and cells `CW` by `CH`, draw vertical lines at `x = CW, 2*CW, ... < W` and horizontal lines at `y = CH, 2*CH, ... < H`. Keep the overlay visually legible without obscuring cell-scale content; a contrasting color or two-tone line may be used on the inspection copy.

Inspect the underlying art against the overlay for scale, containment, boundaries, and alignment. The overlay visualizes the requested geometry only: its presence and correct arithmetic do not prove that the generated content follows that layout. Validate the original asset independently and report any mismatch.

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
