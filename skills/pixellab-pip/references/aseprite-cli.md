# Aseprite CLI Integration

Read this only when the user explicitly asks for Aseprite handling: opening output in Aseprite, creating/updating an `.aseprite` file, importing PixelLab frames as layers/frames/tags, palette/indexed conversion, or exporting via the Aseprite CLI/Lua. Most local preview work belongs in `local-asset-assembly.md` instead.

This is a low-risk pipeline:

```text
PixelLab MCP or documented REST v2
  -> verified local image/frame files
  -> Aseprite CLI or Aseprite Lua script
  -> `.aseprite`, PNG sequence, GIF, spritesheet, metadata, or visible Aseprite workspace
```

Aseprite is a local workspace/import/export tool applied after PixelLab generated the pixels. It arranges PixelLab/user images into layers, frames, tags, cels, and exports; it never authors content (per SKILL.md Asset Integrity — no Lua draw/brush/shape/scripted pixel placement unless the user approves a labeled non-PixelLab fallback).

For explicit Aseprite MCP requests, read `aseprite-mcp.md`; return here when the task also needs direct CLI/Lua file handling.

## Extension Safety

This route never drives or reads the PixelLab Aseprite extension — it is built around interactive editor state, dialogs, plugin prefs, and private first-party communication, not a headless automation API. Do not:

- drive its dialogs or call its modules/operation URLs from Lua;
- run its `generate-*.lua` files through `aseprite --script` to spend credits or call private operations;
- read its credentials, payloads, auth headers, settings, or request history.

Its "reduce-colors" (and unzoom, pixel correction) round-trip the image to a PixelLab server and place the result back — they are not local Aseprite quantization; do not present them as local-only. Treat extension startup errors in batch mode as a diagnostic signal, not something to work around by reading internals. If the user needs exact extension behavior, the stable route is PixelLab MCP/REST plus Aseprite CLI workspace handling, or visible manual Aseprite use.

## Lua Integration Model

Aseprite Lua runs inside Aseprite, not as an external controller. The agent launches the executable and Aseprite runs the script:

```powershell
& $AsepritePath -b --script-param "output=$Output" --script "script.lua"
```

Inside the script Aseprite exposes globals such as `app`, `Sprite`, `Image`, `Point`, `Rectangle`, `ColorMode`. `app.params` receives `--script-param` values, `app.open()` loads sprites, and sprite methods or `app.command.*` modify/export them. This makes Lua the tool for file/workspace automation, not the extension (below).

## Safety Gates

Before running Aseprite:

1. Verify the executable path:

   ```powershell
   $AsepritePath = (Get-Command aseprite -ErrorAction SilentlyContinue).Source
   if (-not $AsepritePath) { throw "Aseprite executable not found; ask the user for the path." }
   ```

   Search common install locations only when appropriate, or ask the user for the path. Do not scan private project folders unless the user points you there.

2. Show which files will be read and written.
3. Ask before launching visible Aseprite.
4. Ask before overwriting existing files.
5. For existing `.aseprite` files, default to writing a copy such as `name-pixellab.aseprite`; modify the original only after explicit approval for that exact path.
6. Keep generated scripts and outputs inside the user's stated or approved output directory; when they did not choose one, use the `pixellab-pip-generations/` output folder (per SKILL.md Asset Integrity).
7. Treat extension startup errors as a diagnostic signal. Do not work around them by reading extension internals.
8. Treat raw Lua as local host-code execution. Generate small, reviewable scripts, pass paths through parameters, and do not run untrusted user-provided Lua.

Use `--batch` for noninteractive file conversion and export. Launch the GUI only when the user wants to continue editing manually.

## Original File Safety

Never write directly into an existing `.aseprite` file unless the user explicitly approves in-place modification of that exact file. A request like "add this to my Aseprite file" is not enough by itself; treat it as permission to create a modified copy.

Default behavior for existing files:

1. Read the original `.aseprite` file.
2. Write a separate output file, such as `name-pixellab.aseprite`.
3. Verify the output copy.
4. Verify the original file was not changed when the workflow was meant to be copy-on-write.

Use `spr:saveCopyAs(output)` for existing-file imports unless the user has explicitly approved overwriting or saving back to the original path. Do not pass the original path as `output` by default. If the user does approve an in-place edit, restate the exact file path and action before writing.

## Fit

Good fit: open a generated PNG/GIF/sheet/frame-sequence in Aseprite; create an `.aseprite` workspace from generated frames; open an existing `.aseprite` and save a modified copy with assets added as named layers/groups or numbered frames+tags+durations; export to PNG frames/GIF/sheet/JSON and inspect layers/tags/slices; convert color mode, quantize/reduce colors, or clamp pixels to a named palette after PixelLab/user images exist.

Poor fit: anything touching the PixelLab Aseprite extension (see Extension Safety); controlling an already-open document without a user-approved bridge (an agent workflow may have no live "current layer/frame", and an existing project file stays copy-on-write); mouse/screenshot/OCR automation as the default.

Map live-editor intents to file operations: "make an Aseprite file" -> new `.aseprite` workspace; "put each result on a layer" -> one named layer/group per result on a new sprite/copy; "put this animation in frames" -> frames + durations + a tag when the action is named; "add to my existing file" -> open + `saveCopyAs` (see Original File Safety).

## CLI Patterns

Prefer direct CLI when no custom sprite construction is needed; use `--save-as` placeholders, `--tag`, `--layer`, `--ignore-layer`, `--split-layers/-tags/-slices`, `--sheet-type`, `--scale`, `--crop`, `--color-mode`, `--palette`, and padding options instead of scripts when they cover the request.

**Option order matters.** Export filters (`--tag`, `--frame-range`, `--layer`, `--ignore-layer`, `--all-layers`, `--split-layers`, `--split-tags`, `--split-slices`) apply to the next sprite opened on the command line, so put them **before** the `.aseprite` file. Put `--script-param name=value` **before** `--script script.lua`. Pass each `--script-param` as one `name=value` argument; in PowerShell, build the path into a variable or quote the whole `name=$Value` string so it does not split.

```powershell
& $AsepritePath --version
& $AsepritePath "asset.png"                                             # open visibly (after approval)
& $AsepritePath -b "source.aseprite" --save-as "frame-{frame}.png"      # PNG frames
& $AsepritePath -b --tag "Walk" "source.aseprite" --save-as "walk.gif"  # tagged GIF
& $AsepritePath -b "source.aseprite" --sheet "sheet.png" --data "sheet.json" --sheet-type rows
& $AsepritePath -b --list-layers "source.aseprite"                      # also --list-tags/--list-slices/--list-layer-hierarchy
& $AsepritePath -b --split-layers "source.aseprite" --save-as "layer-{layer}-{frame}.png"
& $AsepritePath -b "source.png" --palette "palette.png" --color-mode indexed --save-as "out-indexed.png"
```

Set `--data ""` to print sheet metadata to stdout for verification. Run a script with params:

```powershell
& $AsepritePath -b --script-param "output=$Output" --script-param "frames=$Frames" --script "make-workspace.lua"
```

**Frame-preserving exports:** when exporting PixelLab animation frames, do not use frame-count/order-changing options — `--frame-range`, `--trim`, `--ignore-empty`, `--merge-duplicates` — unless the user explicitly asks for that playback/export behavior (per SKILL.md frame-order preservation). Packed sheets are fine when they preserve every frame plus the metadata needed to reconstruct order.

### Built-In FX Outline

For an outline, prefer the built-in command over hand-rolled pixel logic. There is no `--outline` CLI flag; use `app.command.Outline` in a script:

```lua
app.command.Outline{ ui=false, place="inside", matrix=170,
  color=Color{ r=255, g=255, b=255, a=255 }, bgColor=Color{ r=0, g=0, b=0, a=0 }, tiledMode="none" }
```

`place="inside"` keeps the outline in the alpha silhouette (preserves transparency), `"outside"` expands into transparent pixels; `matrix=170` = 4 sides, `matrix="square"` = 8 sides; `tiledMode="none"` unless tiled wrapping is asked. Write to a copy, verify, and report it as an Aseprite derivative, not a raw PixelLab generation.

## Palette Quantization

Use for: reduce/quantize colors, force a limited palette, convert to indexed color, or bit-depth results like "1-bit black and white."

### Intent Mapping

Distinguish the pixel transform from the document palette:

| User wording | Pixel transform | Document palette |
|---|---|---|
| "reduce to N colors" | Use Aseprite `ColorQuantization` to derive up to N colors from the source, then convert pixels to indexed or export a constrained RGB copy. | Leave the existing `.aseprite` palette alone only for RGB/exported-image output. Indexed `.aseprite` output necessarily has a palette; replace it only when the user asked for indexed/palette output. |
| "use only these colors", "clamp to #..." | Map visible pixels to the listed colors. | Replace the palette only when the user also says "palette", "indexed", "no stray palette colors", "only these palette entries", or similar. |
| "replace/set/limit the palette to these colors" | Map visible pixels to the listed colors unless the user asks only for a palette setup. | Set the `.aseprite` palette to exactly the requested color entries, subject to transparency handling below. |
| "1-bit", "black and white only", "#000000 and #ffffff only" | Treat as the explicit palette `#000000`, `#ffffff`; use no dithering unless requested. | Replace palette only when the wording asks for palette replacement or indexed output. |
| "make monochrome" | Ask whether the user means black/white 1-bit, grayscale, or a single-hue palette unless the surrounding wording makes it obvious. | Replace palette only when requested. |
| "make every visible pixel #000000" or another one-color clamp | Clamp all visible pixels to that one color. For indexed `.aseprite` output, warn that Aseprite may still need a transparent/index-management entry; RGB PNG output is the cleanest exact one-color result. | Replace palette only when requested and verify no extra visible colors. |
| "2-bit grayscale" | Use the explicit four-color ramp `#000000`, `#555555`, `#AAAAAA`, `#FFFFFF` unless the user supplies different levels. | Replace palette only when requested. |
| "Game Boy palette" | Use `#0F380F`, `#306230`, `#8BAC0F`, `#9BBC0F` unless the user names a different Game Boy palette. | Replace palette only when requested. |
| "PICO-8", "DB16", "DB32", or another Aseprite resource palette | Use the named Aseprite palette resource when available; otherwise ask for a palette file or explicit colors. | Replace palette only when requested. |
| "current palette", "source palette", or "use this sprite's palette" | Use the source sprite's current palette when it has meaningful palette entries; otherwise use source-derived `ColorQuantization` or ask for a palette. | Preserve the current/source palette unless the user asks for indexed output or replacement. |
| Supplied `.gpl/.pal/.png` palette | Load the supplied palette file, then convert or clamp to it. | Replace palette only when requested. |

If the request says only "2-bit color" / "reduce to 4 colors" without naming colors, infer `2^bits` or N visible colors via `ColorQuantization`; do not invent a named art palette when exact palette identity matters. "1-bit" without colors = black and white. "1-bit transparency" = alpha-only binary transparency; do not change RGB colors unless color reduction is also asked.

### Scope And Output

Default PNG inputs to a new PNG copy unless the user asks for `.aseprite`, indexed color, palette replacement, or editor workspace output; default `.aseprite` inputs to a new `.aseprite` copy. Process all frames only when the user says all/whole/every/complete; if they name a current/selected/frame N/active cel/layer, scope to that and verify only the touched frame plus source preservation. If scope is ambiguous on a multi-frame `.aseprite`, ask before writing.

### Transparency

Visible color limits exclude fully transparent pixels by default; preserve alpha unless the user explicitly asks to flatten. For indexed `.aseprite` output the transparent color is a palette index — commonly index `0`. Reserve index `0` for transparency and put visible colors at later indices; do not place a requested visible color such as `#000000` at the transparent index while transparency is preserved. If the user insists the palette hold only visible entries, ask whether to flatten instead.

Flatten only when the user names the matte/background color or clearly accepts one; for a strict clamp the matte must be one of the requested colors unless the user approves adding another. Do not silently flatten transparent pixels to black or white to satisfy an exact palette-size request.

### Dithering

Default to no dithering for strict palette clamps, binary/1-bit output, UI masks, collision masks, silhouettes, and any request that says "only", "exact", "no stray colors", or "hard threshold." Enable ordered dithering only when the user asks for dithering, smoother gradients, retro dither, or Bayer. In Lua, pass the algorithm and matrix as separate `ChangePixelFormat` fields: `dithering="ordered"` and `["dithering-matrix"]="bayer4x4"`.

### Lua Patterns

Use Lua when the palette must be built from hex colors, source-derived N-color quantization is needed, or the output `.aseprite` palette must be replaced. Keep original-file safety: write a copy by default and verify the original did not change. **Every script must reject `output == input`** unless the user approved in-place modification of that exact path — resolve paths before launch (`Resolve-Path -LiteralPath`) and also compare normalized paths in Lua (a launcher-side absolute-path check is safer on Windows, where case, slashes, relative paths, and aliases hide same-file writes).

Full example — exact palette clamp with optional palette replacement. The `samePath` helper is the reject-same-path guard; reuse it in every script:

```lua
local input = app.params["input"]
local output = app.params["output"]
local colors = app.params["colors"] -- comma-separated hex, e.g. #000000,#ffffff
local replacePalette = app.params["replace_palette"] == "true"
local preserveTransparency = app.params["preserve_transparency"] ~= "false"
local outputMode = app.params["output_mode"] or (replacePalette and "indexed" or "rgb")
local dithering = app.params["dithering"] or "none"
local matrix = app.params["dithering_matrix"]
local hasTransparency = app.params["has_transparency"] == "true"

local function samePath(a, b)
  local na = app.fs.normalizePath(a or ""):gsub("\\", "/")
  local nb = app.fs.normalizePath(b or ""):gsub("\\", "/")
  if app.fs.pathSeparator == "\\" then
    na = na:lower()
    nb = nb:lower()
  end
  return na == nb
end
if samePath(input, output) then error("Output must be a copy path, not the input path") end
local spr = app.open(input)
if not spr then error("Could not open input: " .. tostring(input)) end
local originalPalette = spr.palettes[1] and Palette(spr.palettes[1]) or nil
app.command.ChangePixelFormat{ format="rgb" }

local parsed = {}
for hex in string.gmatch(colors or "", "([^,]+)") do
  hex = hex:gsub("^%s+", ""):gsub("%s+$", ""):gsub("^#", "")
  if not hex:match("^[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]$") then
    error("Invalid color: " .. hex)
  end
  local r = tonumber(hex:sub(1, 2), 16)
  local g = tonumber(hex:sub(3, 4), 16)
  local b = tonumber(hex:sub(5, 6), 16)
  table.insert(parsed, Color{ r=r, g=g, b=b, a=255 })
end
if #parsed < 1 then error("At least one color is required for a palette clamp") end
if outputMode == "indexed" and #parsed == 1 and not hasTransparency then
  error("One-color indexed output can collide with Aseprite's transparent index; use output_mode=rgb or approve an extra transparent/index-management entry")
end

local transparentOffset = (preserveTransparency and hasTransparency) and 1 or 0
local pal = Palette(#parsed + transparentOffset)
if transparentOffset == 1 then
  pal:setColor(0, Color{ r=0, g=0, b=0, a=0 })
  spr.transparentColor = 0
end
for i, color in ipairs(parsed) do
  pal:setColor(i - 1 + transparentOffset, color)
end

local pc = app.pixelColor
local function nearestPaletteColor(pixel)
  local alpha = pc.rgbaA(pixel)
  if preserveTransparency and alpha == 0 then return pixel end
  local r = pc.rgbaR(pixel)
  local g = pc.rgbaG(pixel)
  local b = pc.rgbaB(pixel)
  local best = parsed[1]
  local bestDistance = math.huge
  for _, color in ipairs(parsed) do
    local dr = r - color.red
    local dg = g - color.green
    local db = b - color.blue
    local distance = dr * dr + dg * dg + db * db
    if distance < bestDistance then
      bestDistance = distance
      best = color
    end
  end
  return pc.rgba(best.red, best.green, best.blue, alpha)
end

for _, cel in ipairs(spr.cels) do
  local image = cel.image
  for y = 0, image.height - 1 do
    for x = 0, image.width - 1 do
      image:putPixel(x, y, nearestPaletteColor(image:getPixel(x, y)))
    end
  end
end

local changePixelFormatArgs = { format="indexed" }
if dithering ~= "none" then
  changePixelFormatArgs.dithering = dithering
  if matrix and matrix ~= "" then
    changePixelFormatArgs["dithering-matrix"] = matrix
  end
end

if outputMode == "rgb" then
  if originalPalette then
    spr:setPalette(originalPalette)
  end
else
  spr:setPalette(pal)
  app.command.ChangePixelFormat(changePixelFormatArgs)
  if replacePalette then
    spr:setPalette(pal)
  end
end
spr:saveCopyAs(output)
print("OK:palette-clamped")
```

Launch:

```powershell
& $AsepritePath -b --script-param "input=$Input" --script-param "output=$Output" --script-param "colors=#000000,#ffffff" --script-param "replace_palette=true" --script-param "preserve_transparency=true" --script-param "dithering=none" --script "palette-clamp.lua"
```

Variants — same skeleton, same `samePath` guard, `saveCopyAs` + printed status:

- **Source-derived N-color reduction:** drop the color-parsing/clamp loop; run `app.command.ColorQuantization{ ui=false, withAlpha=false, maxColors=N, algorithm="octree" }` then `ChangePixelFormat`. For RGB output, convert back to `rgb` and restore the saved original palette. Refuse source-derived *indexed* output with transparency unless an explicit transparent-index QA path is set — use RGB output, or an exact clamp with `preserve_transparency=true`, instead. The CLI has no documented `--num-colors`; `ColorQuantization` is the source-derived route.
- **Palette-only replacement** (change the document palette without remapping pixel indices/colors): open, `spr:setPalette(Palette{ fromFile=paletteFile })`, `saveCopyAs` — do **not** call `ChangePixelFormat`. On indexed sprites this changes what existing indices mean; on RGB sprites it changes palette metadata rather than visible pixels. Verify this is what the user asked. For named palettes/files use `spr:loadPalette()`, `Palette{ fromResource=... }`, or `app.command.LoadPalette{ ui=false, filename=... }`; resource names like `PICO-8`, `DB16`, `DB32` are acceptable only after verifying Aseprite can load them or the user accepts the closest installed palette. If the user did not ask for indexed/palette output, convert back to RGB and restore the original palette so the result is a pixel-clamped image, not a document-palette swap.

### Verification

After palette quantization:

1. Verify the output file exists. Installed extensions can print unrelated startup warnings in batch mode and output-file visibility can lag briefly; judge success by the saved output plus color/palette checks, not clean stdout alone.
2. Count visible colors in exported PNGs or cels and fail if any opaque/semitransparent pixel uses a color outside the requested palette.
3. If palette replacement was requested, inspect the `.aseprite` palette and verify it contains exactly the requested visible entries, plus only an approved transparent index when needed.
4. For multi-frame sprites, verify every frame, not only the active frame.
5. Report the output type: RGB PNG copy, RGB `.aseprite` copy, indexed `.aseprite` copy, palette-replaced `.aseprite`, or exported verification preview — these are different outcomes.
6. For "1-bit black and white", verify visible RGB values are exactly `#000000` and/or `#ffffff`; do not accept near-black, near-white, grayscale ramps, antialias colors, black pixels exported as transparent, or unused stray palette entries when the user asked for strict output.
7. A simple check exports PNG frames and counts nonzero-alpha RGB tuples, or uses Lua to print palette entries, `transparentColor`, frame count, and per-frame used visible colors as status lines.

## Lua Script Patterns

For opening an existing `.aseprite`, or building one from generated images with layers/frames/cels/tags/durations, use Lua — but only these non-obvious points matter; the rest is the public Aseprite Lua API (`Sprite`, `newLayer`/`newGroup`/`newEmptyFrame`/`newCel`/`newTag`, `ExportSpriteSheet`/`ImportSpriteSheet`, `saveAs`/`saveCopyAs`, `app.open` on images/GIFs).

- **Parameterize user strings** via `--script-param` + `app.params`; never embed user paths, layer names, tag names, or labels into the generated Lua file.
- **Reuse the default layer and frame.** A new `Sprite(w, h, ColorMode.RGB)` already has one layer and one frame. Use them for the first imported item (rename `spr.layers[1]`, fill `spr.frames[1]`), then create the rest with explicit positions (`spr:newEmptyFrame(#spr.frames + 1)`, `spr:newLayer()`, `spr:newGroup()`). Do not blindly add a fresh layer+frame before the first import — that leaves stray blank content. Delete an unused default (`spr:deleteFrame`/`spr:deleteLayer`) only after replacement content exists.
- **Print explicit status.** Lua return values are not a reliable agent result channel. Print `OK` / `ERROR:<message>` / `INFO:<json>` / `MISSING:<name>` and parse after the run. A clean process exit is not proof; verify the printed status and the expected files.

### Frame Manifest Contract

For multi-frame imports, drive the script from a small JSON manifest (local paths and non-sensitive metadata only):

```json
{
  "canvas": { "width": 32, "height": 32 },
  "placement": "origin",
  "layers": [
    {
      "name": "PixelLab - walk",
      "frames": [
        { "path": "frame-001.png", "frame": 1, "duration": 0.12, "x": 0, "y": 0 },
        { "path": "frame-002.png", "frame": 2, "duration": 0.12, "x": 0, "y": 0 }
      ],
      "tag": { "name": "walk", "from": 1, "to": 2 }
    }
  ]
}
```

The script sorts by explicit `frame`, verifies each file exists, checks image dimensions before adding cels, sets duration when provided, and creates tags only from explicit manifest data or clear user intent.

## Patterns Usable Without MCP

These QA/structure patterns need only the CLI/Lua — no MCP server:

- **Batch import/export:** import a grid sheet with `app.command.ImportSpriteSheet{ ui=false, type=..., frameBounds=Rectangle(...), padding=Size(...) }`; open a GIF with `app.open` to load its frames; export via `--sheet`/`--save-as` or `app.command.ExportSpriteSheet`.
- **Visual QA:** export one frame at 4x/8x/10x for readable inspection; render onion-skin previews when continuity matters; compare neighboring frames to catch duplicate/near-duplicate frames.
- **Palette ops / metadata reads:** count colors or inspect histograms when a limited palette was requested; read layers/tags/slices/frame counts with `--list-*` or by printing from Lua. Treat QA as read-only; any fix to an existing `.aseprite` still follows copy-on-write.
- **Copy layers between files:** open the source and a *copy* of the target; resolve layers by name (error out if missing, don't create placeholders); copy each source cel image + position into the matching target layer/frame; save and verify the copy plus that the original was unchanged.
- **Validate** expected layers/cels/tags before and after imports; require a printed `OK`/`ERROR:` status from generated Lua.

## Common Workflows

Shared checklist for every workflow:

1. Generate/collect assets through PixelLab MCP or documented REST v2; write verified files under `pixellab-pip-generations/` (per SKILL.md) unless another path is approved.
2. Verify dimensions and, for animations, frame order.
3. Reuse the new sprite's default layer/frame for the first item; add explicit frames/layers for the rest (see Lua Script Patterns). Set durations from PixelLab metadata, else the user's requested FPS; add tags (`idle`/`walk`/`attack` or the user's action name) when the import is a named animation.
4. Run Aseprite in `--batch` with `--script`/`--script-param`, or a direct CLI command for simple exports.
5. Verify output files exist, layer/frame/tag counts match inputs, and — for existing-file work — the original is unchanged. Optionally export a GIF/sheet preview. Ask before launching GUI Aseprite.

### Import Into Existing `.aseprite` (unique guidance)

1. Confirm the input file, files to import, and placement. Default to a new output file; never write the input path without explicit per-path approval.
2. Open with `app.open(input)`; inspect existing layer names, frame count, tags, canvas size, and color mode when placement depends on them.
3. Compare generated image dimensions against the existing canvas before creating cels. If they differ, **do not silently crop/resize/expand** — ask the user to choose: preserve origin and allow clipping, center on the canvas, expand the canvas, resize the art, or abort.
4. Keep color mode unchanged unless the user asked for conversion or approved it after seeing the source and target modes.
5. Add imported output on a clearly named layer/group (e.g. `PixelLab - walk`); add/update tags only when requested or when the import is a named animation.
6. Save with `spr:saveCopyAs(output)`; verify the copy with `--list-layers`/`--list-tags` and confirm the original was unchanged.

This is a file-level edit — it can modify a project file on disk, but it is not live control of an already-open Aseprite session.

## Verification

After Aseprite CLI work, verify before reporting success:

- Check expected output files exist. Aseprite can exit 0 without writing the expected file, write numbered sibling files for frame sequences, or (on launcher installs) return before files are visible — check exact and acceptable numbered outputs, and wait briefly before declaring failure.
- For sprite sheets, check both image and JSON metadata when requested.
- For GIFs, inspect frame count/delay/disposal if transparency matters; see `local-asset-assembly.md`.
- For `.aseprite` files, run `--list-layers`/`--list-tags` when the task created layers/tags.
- For existing-file imports, verify the output copy exists and the original was not changed unless in-place was approved.
- For exported PNG frames, count the outputs against the requested frame count.
- For Lua scripts, require an explicit printed success/status line and treat printed `ERROR:` lines as failures even if Aseprite exits 0. If Aseprite prints extension startup errors, report that it ran but an extension emitted errors; do not print credentials or extension internals.
