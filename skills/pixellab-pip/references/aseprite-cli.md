# Aseprite CLI Integration

Read this only when the user explicitly asks for Aseprite handling, such as opening output in Aseprite, creating or updating an `.aseprite` file, importing PixelLab frames into Aseprite, making layers/frames/tags, exporting from Aseprite, or using the Aseprite CLI.

This reference describes a low-risk integration path:

```text
PixelLab MCP or documented REST v2
  -> verified local image/frame files
  -> Aseprite CLI or Aseprite Lua script
  -> `.aseprite`, PNG sequence, GIF, spritesheet, metadata, or visible Aseprite workspace
```

Do not use this route to automate the PixelLab Aseprite extension itself.

For explicit Aseprite MCP requests, read `aseprite-mcp.md` instead. Return here only when the task also needs direct Aseprite CLI/Lua file handling.

## Lua Integration Model

Aseprite Lua is not a separate Lua runtime that controls Aseprite from the outside. The agent launches the Aseprite executable, and Aseprite runs the Lua script inside its own scripting environment.

Use this shape:

```powershell
& $AsepritePath -b --script-param "output=$Output" --script "script.lua"
```

In that script, Aseprite exposes globals such as `app`, `Sprite`, `Image`, `Point`, `Rectangle`, and `ColorMode`. `app.params` receives `--script-param` values, `app.open()` loads sprites, and sprite methods or `app.command.*` modify/export them.

This means Lua is useful for file/workspace automation:

- Create a new `.aseprite` file.
- Open a source image, GIF, sprite sheet, or `.aseprite` file.
- Add layers, groups, frames, cels, tags, and frame durations.
- Export PNG sequences, GIFs, sprite sheets, metadata, or copies.
- Save a modified copy of an existing `.aseprite` file.

This does not make the PixelLab Aseprite extension a stable headless automation API. Extension commands are designed around interactive Aseprite state, dialogs, active sprite/layer/frame, plugin preferences, editor placement behavior, and private first-party communication. Do not call extension modules directly, drive extension dialogs through Lua, or invoke extension commands to spend credits unless a future bridge explicitly exposes a supported command contract with approval gates.

The extension's Aseprite commands are dialog launchers and editor actions, not stable script-callable generation commands. Do not run PixelLab extension files such as `generate-*.lua` through `aseprite --script` to spend PixelLab credits, call private operations, or bypass the visible editor workflow.

## Positioning

Use Aseprite as a local file and workspace tool after PixelLab has generated files through public automation surfaces.

Aseprite CLI/Lua is workspace automation, not a PixelLab substitute. It may arrange PixelLab/user images into layers, frames, tags, cels, and exports, but must not author content: no Lua draw, brush, shape primitives, or scripted pixel placement unless the user explicitly requests or approves a labeled non-PixelLab fallback.

Good fit:

- Open a generated PNG, GIF, sprite sheet, or frame sequence in Aseprite.
- Create an `.aseprite` workspace from generated frames.
- Open an existing `.aseprite` file and save a modified copy with generated assets added.
- Put generated variants into named layers.
- Put generated animation frames into numbered frames with tags and durations.
- Export an `.aseprite` file to PNG frames, GIF, sprite sheet, or JSON metadata.
- Inspect layers, tags, slices, or export metadata from an Aseprite file.
- Convert palette/color mode when Aseprite's documented CLI supports the needed conversion.
- Quantize or reduce local image colors with explicit Aseprite CLI/Lua palette handling after PixelLab/user images already exist.
- Clamp visible pixels to a supplied or named palette, such as "only #000000 and #ffffff", and optionally replace the `.aseprite` document palette when the user asks for palette replacement too.

Poor fit:

- Driving the PixelLab Aseprite extension UI.
- Calling undocumented operation URLs used by the extension.
- Reading extension credentials, request payloads, auth headers, private settings, or request history.
- Controlling an already-open Aseprite document without a user-approved bridge.
- Spending PixelLab credits from inside Aseprite through hidden automation.
- Mouse, screenshot, or OCR automation as the default workflow.
- Claiming PixelLab extension reduce-colors is local-only Aseprite quantization. The observed extension workflow sends the image to a PixelLab quantize operation, then places the returned image in Aseprite.

If the user wants exact PixelLab extension behavior such as extension-specific reduce-colors, unzoom, pixel correction, or in-editor placement, explain that the stable agent route is PixelLab MCP/REST plus Aseprite CLI workspace handling. Offer visible manual Aseprite use or a separately designed bridge only if they really need live editor behavior.

## Output Mode Mapping

The PixelLab Aseprite extension has live-editor output concepts such as creating a new frame, creating a new layer, or modifying the current layer. In this CLI integration, map those concepts to safer file-level operations:

| User-facing intent | CLI/Lua behavior |
|---|---|
| "Make an Aseprite file" | Create a new `.aseprite` workspace from generated files. |
| "Put each result on a layer" | Create a new sprite or output copy, then add one named layer or group per result. |
| "Put this animation in frames" | Add generated images across frames, set durations, and add a tag when the action has a name. |
| "Add this to my existing Aseprite file" | Open the existing file and save a modified copy by default. |
| "Modify the current/original file" | Only write in place after explicit approval for that exact file path. |
| "Open it in Aseprite so I can continue" | Create or export the file first, verify it, then ask before launching visible Aseprite. |

Do not treat "modify current layer" as safe by default. In an agent workflow there may be no live current layer, and an existing project file must remain copy-on-write unless the user explicitly approved an in-place edit.

## Trigger Conditions

Use this reference only when Aseprite is part of the requested outcome. Examples:

- "open this in Aseprite"
- "make an Aseprite file"
- "create an .aseprite workspace"
- "add this to my existing .aseprite file"
- "import these into this .aseprite project"
- "import these frames into Aseprite"
- "put each output on a layer"
- "make frames/tags/durations"
- "export this .aseprite as a sprite sheet"
- "I prefer working in Aseprite"
- "use Aseprite CLI"
- "apply/create an Aseprite outline"
- "use Edit > FX > Outline"
- "inside outline", "outside outline", "4-side outline", or "8-side outline"
- "reduce colors in Aseprite"
- "quantize this with Aseprite"
- "convert this to indexed color"
- "limit this sprite to these colors"
- "make it 1-bit black and white"
- "replace the Aseprite palette with only these colors"

Do not trigger just because PixelLab generated local images. Most local preview work belongs in `local-asset-assembly.md`.

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
6. Keep generated scripts and outputs inside the user's stated or approved output directory; when they did not choose one, use the active project/workspace `pixellab-pip-generations/` output folder. Use another path only after explicit approval.
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

## CLI Patterns

Prefer direct CLI commands when no custom sprite construction is needed.

Option order matters. Aseprite processes many export filters against the next sprite opened on the command line. Put filters such as `--tag`, `--frame-range`, `--layer`, `--ignore-layer`, `--all-layers`, `--split-layers`, `--split-tags`, and `--split-slices` before the `.aseprite` file they apply to. Put `--script-param name=value` before `--script script.lua` so the script can read `app.params`.

Check version:

```powershell
& $AsepritePath --version
```

Open a file visibly after user approval:

```powershell
& $AsepritePath "asset.png"
```

Export an `.aseprite` file as PNG frames:

```powershell
& $AsepritePath -b "source.aseprite" --save-as "frame-{frame}.png"
```

Export a tagged animation as a GIF:

```powershell
& $AsepritePath -b --tag "Walk" "source.aseprite" --save-as "walk.gif"
```

Export a sprite sheet plus JSON metadata:

```powershell
& $AsepritePath -b "source.aseprite" --sheet "sheet.png" --data "sheet.json" --sheet-type rows
```

Write sprite sheet metadata to stdout for verification:

```powershell
& $AsepritePath -b "source.aseprite" --sheet "sheet.png" --data "" --sheet-type rows
```

Export layers separately:

```powershell
& $AsepritePath -b --split-layers "source.aseprite" --save-as "layer-{layer}-{frame}.png"
```

List layers, tags, or slices for inspection:

```powershell
& $AsepritePath -b --list-layers "source.aseprite"
& $AsepritePath -b --list-layer-hierarchy "source.aseprite"
& $AsepritePath -b --list-tags "source.aseprite"
& $AsepritePath -b --list-slices "source.aseprite"
```

Preview a command without writing files:

```powershell
& $AsepritePath -b --preview --tag "Walk" "source.aseprite" --save-as "walk.gif"
```

Export a single layer or exclude a guide layer:

```powershell
& $AsepritePath -b --layer "Body" "source.aseprite" --save-as "body-{frame}.png"
& $AsepritePath -b --ignore-layer "Guides" "source.aseprite" --save-as "clean-{frame}.png"
```

Export a frame range:

```powershell
& $AsepritePath -b --frame-range 1,6 "source.aseprite" --save-as "walk-{frame}.png"
```

Scale, crop, or trim output:

```powershell
& $AsepritePath -b "source.aseprite" --scale 2 --save-as "source-2x.png"
& $AsepritePath -b "source.aseprite" --crop 0,0,32,32 --save-as "source-crop.png"
& $AsepritePath -b "source.aseprite" --trim --save-as "source-trimmed.png"
```

Convert to indexed color with optional dithering:

```powershell
& $AsepritePath -b "source.png" --dithering-algorithm none --color-mode indexed --save-as "source-indexed.png"
& $AsepritePath -b "source.png" --palette "palette.png" --color-mode indexed --save-as "source-paletted.png"
```

### Built-In FX Outline

When the user asks for an outline through Aseprite, prefer Aseprite's built-in `Edit > FX > Outline` command through batch Lua. Do not hand-roll pixel outline logic unless the built-in command cannot express the requested behavior.

The direct CLI has no standalone `--outline` flag. Use `app.command.Outline` in a script:

```lua
app.command.Outline{
  ui=false,
  place="inside", -- or "outside"
  matrix=170, -- 4 sides only: top, left, right, bottom
  color=Color{ r=255, g=255, b=255, a=255 },
  bgColor=Color{ r=0, g=0, b=0, a=0 },
  tiledMode="none"
}
```

Use these settings:

- `place="inside"`: keeps the outline inside the existing alpha silhouette and preserves transparency.
- `place="outside"`: expands the outline into transparent pixels.
- `matrix=170`: 4 sides only, matching top/left/right/bottom.
- `matrix="square"`: 8 sides, including diagonals/corners.
- `tiledMode="none"` unless the user explicitly asks for tiled wrapping.

Write to a copy, verify the output file exists, and compare alpha/visible colors against the request. If this modifies PixelLab art locally, report it as an Aseprite derivative rather than a raw PixelLab generation.

For palette-constrained output, prefer a supplied palette file or a Lua-created palette when the user names exact colors. The CLI documents `--palette`, `--dithering-algorithm`, `--dithering-matrix`, and `--color-mode indexed`, but it does not document a standalone `--num-colors` option. For broad source-derived requests such as "reduce to 12 colors", use Lua `app.command.ColorQuantization{ ui=false, maxColors=12, ... }` followed by indexed conversion and verification.

For multi-frame sprites, use filename formatting such as `{frame}` or expect Aseprite to number the output files:

```powershell
& $AsepritePath -b "source.aseprite" --color-mode indexed --save-as "indexed-{frame}.png"
```

When exporting PixelLab-generated animation frames, preserve frame count and order by default. Do not use frame-count/order-changing options such as `--frame-range`, `--trim`, `--ignore-empty`, or `--merge-duplicates` unless the user explicitly asks for that playback/export behavior. Packed sheets are okay when they preserve every frame and include metadata needed to reconstruct the original order.

Export a packed or padded sprite sheet:

```powershell
& $AsepritePath -b --tag "Walk" "source.aseprite" --sheet "walk-sheet.png" --data "walk-sheet.json" --sheet-type packed --shape-padding 1 --border-padding 1 --trim --ignore-empty
```

Use fixed sheet dimensions or duplicate merging when engine import rules require them:

```powershell
& $AsepritePath -b "source.aseprite" --sheet "sheet.png" --data "sheet.json" --sheet-type rows --sheet-columns 4 --inner-padding 1 --merge-duplicates
```

Export slices separately when the user organized hitboxes, UI pieces, or sub-assets as slices:

```powershell
& $AsepritePath -b --split-slices "source.aseprite" --save-as "slice-{slice}-{frame}.png"
```

Run a Lua script with explicit parameters:

```powershell
$Output = "character.aseprite"
$Frames = "frames.json"
& $AsepritePath -b --script-param "output=$Output" --script-param "frames=$Frames" --script "make-workspace.lua"
```

Pass each `--script-param` value as a single `name=value` argument. In PowerShell, build paths into variables first or quote the whole `name=$Value` string so expressions do not split the key and value into separate arguments.

Use Aseprite's `--save-as` filename placeholders, `--tag`, `--frame-range`, `--layer`, `--ignore-layer`, `--split-layers`, `--split-tags`, `--sheet-type`, `--trim`, `--crop`, `--scale`, `--color-mode`, and padding options instead of writing custom scripts when they cover the request.

## Palette Quantization

Use this workflow when the user asks to reduce colors, quantize colors, force a limited palette, convert to indexed color, or make a bit-depth-style result such as "1-bit black and white."

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

If the request says only "2-bit color" or "reduce to 4 colors" without naming the colors, infer `2^bits` or N visible colors and use Aseprite `ColorQuantization`. Do not invent a specific named art palette when exact palette identity matters.

When the user says "1-bit" without naming colors, infer black and white. When they say "1-bit transparency", treat that as alpha-only binary transparency and do not change RGB colors unless they also ask for color reduction.

### Scope And Output

Default still-image inputs such as PNGs to a new PNG copy unless the user asks for `.aseprite`, indexed color, palette replacement, or editor workspace output. Default `.aseprite` inputs to a new `.aseprite` copy. Export extra PNG previews only when needed for verification or when requested.

For multi-frame sprites, process all frames only when the user says all frames, whole animation, every frame, the whole sprite, the complete sheet/sequence, or equivalent. If the user says current frame, selected frame, frame N, or active cel/layer, scope the Lua script or CLI export to that frame/cel/layer and verify only the touched frame plus unchanged source preservation. If the scope is ambiguous on a multi-frame `.aseprite`, ask before writing.

### Transparency

Visible color limits exclude fully transparent pixels by default. Preserve alpha unless the user explicitly asks to flatten transparency.

For indexed `.aseprite` output, transparent layers use a palette index as the transparent color. In Aseprite indexed sprites this is commonly index `0`; do not put a visible requested color such as `#000000` at that transparent index when transparency is preserved. Reserve index `0` for transparency and put visible colors at later indices, or ask whether to flatten transparency when the user insists the document palette contain only visible entries such as `#000000` and `#ffffff`.

Flatten transparency only when the user names the matte/background color or clearly accepts one. For a strict palette clamp, the matte must be one of the requested colors unless the user approves adding another color. Do not silently flatten transparent pixels to black or white just to satisfy an exact palette-size request.

### Dithering

Default to no dithering for strict palette clamps, binary/1-bit output, UI masks, collision masks, silhouettes, and any request that says "only", "exact", "no stray colors", or "hard threshold." Enable ordered dithering only when the user asks for dithering, smoother gradients, retro dither, Bayer, or similar. In Lua, pass the algorithm and matrix as separate `ChangePixelFormat` fields: `dithering="ordered"` and `["dithering-matrix"]="bayer4x4"`.

### Lua Patterns

Use Lua when the palette must be created from hex colors, source-derived N-color quantization is needed, or the output `.aseprite` palette must be replaced. This is file/workspace automation, so keep the original-file safety rules: write a copy by default and verify the original did not change. Always reject `output == input` unless the user explicitly approved in-place modification of that exact path.

Resolve input and output paths before launching Aseprite when possible, such as with PowerShell `Resolve-Path -LiteralPath`. Lua scripts should also compare normalized paths, but a launcher-side absolute-path check is safer on Windows because case, slashes, relative paths, and aliases can hide same-file writes.

Source-derived N-color reduction:

```lua
local input = app.params["input"]
local output = app.params["output"]
local maxColors = tonumber(app.params["max_colors"] or "16")
local outputMode = app.params["output_mode"] or "rgb" -- "rgb" or "indexed"
local dithering = app.params["dithering"] or "none"
local matrix = app.params["dithering_matrix"]

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

app.command.ColorQuantization{
  ui=false,
  withAlpha=false,
  maxColors=maxColors,
  algorithm="octree",
}

local changePixelFormatArgs = { format="indexed" }
if dithering ~= "none" then
  changePixelFormatArgs.dithering = dithering
  if matrix and matrix ~= "" then
    changePixelFormatArgs["dithering-matrix"] = matrix
  end
end
app.command.ChangePixelFormat(changePixelFormatArgs)

if outputMode == "indexed" and app.params["has_transparency"] == "true" then
  error("Source-derived indexed output with transparency needs an explicit transparent-index QA path; use RGB output or an exact palette clamp with preserve_transparency=true")
end

if outputMode == "rgb" then
  app.command.ChangePixelFormat{ format="rgb" }
  if originalPalette then
    spr:setPalette(originalPalette)
  end
end
spr:saveCopyAs(output)
print("OK:color-quantized")
```

Exact palette clamp with optional palette replacement:

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

Launch shape:

```powershell
& $AsepritePath -b --script-param "input=$Input" --script-param "output=$Output" --script-param "colors=#000000,#ffffff" --script-param "replace_palette=true" --script-param "preserve_transparency=true" --script-param "dithering=none" --script "palette-clamp.lua"
```

Palette-only replacement, when the user explicitly asks to change the document palette without changing pixel indices/colors, should not call `ChangePixelFormat`:

```lua
local input = app.params["input"]
local output = app.params["output"]
local paletteFile = app.params["palette"]

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
spr:setPalette(Palette{ fromFile=paletteFile })
spr:saveCopyAs(output)
print("OK:palette-only")
```

Use palette-only replacement carefully: on indexed sprites it changes the meaning of existing color indices without remapping pixels, and on RGB sprites it changes palette metadata rather than visible RGB pixels. Verify that this is what the user asked for.

For named palettes or palette files, use `Sprite:loadPalette()`, `Sprite:setPalette(Palette{ fromFile=... })`, `Palette{ fromResource=... }`, or `app.command.LoadPalette{ ui=false, filename=... }` in Lua, then convert to indexed. Built-in resource names such as `PICO-8`, `DB16`, and `DB32` are acceptable only after verifying Aseprite can load them or the user accepts the closest installed palette. If the user did not ask for indexed or palette replacement, convert back to RGB and restore the original palette before saving so the output is a pixel-clamped image rather than a document palette replacement.

### Verification

After palette quantization:

1. Verify the output file exists. Installed Aseprite extensions can print unrelated startup warnings in batch mode, and output-file visibility can lag briefly; judge success by the saved output plus color/palette checks, not clean stdout alone.
2. Count visible colors in exported PNGs or cels and fail if any opaque/semitransparent pixel uses a color outside the requested palette.
3. If palette replacement was requested, inspect the `.aseprite` palette and verify it contains exactly the requested visible entries, plus only an approved transparent index when needed.
4. For multi-frame sprites, verify every frame, not only the active frame.
5. Report the output type: RGB PNG copy, RGB `.aseprite` copy, indexed `.aseprite` copy, palette-replaced `.aseprite`, or exported verification preview. These are different outcomes.
6. For "1-bit black and white", verify visible RGB values are exactly `#000000` and/or `#ffffff`; do not accept near-black, near-white, grayscale ramps, antialias colors, black pixels exported as transparent, or unused stray palette entries when the user asked for strict output.
7. A simple verification script may export PNG frames and count nonzero-alpha RGB tuples, or use Aseprite Lua to print palette entries, `transparentColor`, frame count, and per-frame used visible colors as JSON-like status lines.

## Lua Script Patterns

Use Lua when the task requires opening an existing `.aseprite` file, creating layers, frames, cels, tags, durations, or a new `.aseprite` workspace from generated images.

Batch-mode Lua should print explicit status because Lua return values are not a reliable agent result channel. Prefer lines such as `OK`, `ERROR:<message>`, `INFO:<json>`, or `MISSING:<name>` and parse them after the command finishes. A clean Aseprite process exit is not enough; verify the printed status and the expected files.

Escape or parameterize all user-provided paths, layer names, tag names, and labels. Prefer `--script-param` plus `app.params` over embedding user strings directly into a generated Lua file.

Parameter access:

```lua
local output = app.params["output"]
local first_frame = app.params["first_frame"]
```

Open an existing image:

```lua
local spr = app.open(first_frame)
if not spr then
  error("Could not open first frame: " .. tostring(first_frame))
end
```

Open an existing `.aseprite` file:

```lua
local input = app.params["input"]
local spr = app.open(input)
if not spr then
  error("Could not open Aseprite file: " .. tostring(input))
end
```

Create a new sprite:

```lua
local spr = Sprite(64, 64, ColorMode.RGB)
spr.filename = output
```

A new sprite already contains one layer and one frame. Reuse them for the first imported item, or explicitly delete them after creating replacement layers/frames. Do not blindly add a new layer and a new frame before importing the first asset, because that creates stray blank content.

Use the default layer for the first imported item:

```lua
local layer = spr.layers[1]
layer.name = "PixelLab"
```

Create an additional named layer:

```lua
local layer = spr:newLayer()
layer.name = "PixelLab Extra"
```

Create a group for imported output:

```lua
local group = spr:newGroup()
group.name = "PixelLab Import"
```

Use the first existing frame, then create additional frames with explicit positions:

```lua
local frame = spr.frames[1]
local nextFrame = spr:newEmptyFrame(#spr.frames + 1)
```

Create a cel from an image:

```lua
local image = Image{ fromFile="frame-001.png" }
spr:newCel(layer, frame, image, Point(0, 0))
```

Delete an unused default frame or layer only after replacement content exists:

```lua
spr:deleteFrame(1)
spr:deleteLayer(layer)
```

Create an animation tag:

```lua
local tag = spr:newTag(1, #spr.frames)
tag.name = "walk"
```

Set frame duration:

```lua
spr.frames[1].duration = 0.12
```

Save the workspace:

```lua
spr:saveAs(output)
```

Save a modified copy of an existing workspace:

```lua
spr:saveCopyAs(output)
```

Convert color mode or load a palette when the user asks for palette/indexed-color handling:

```lua
app.command.ChangePixelFormat{
  format="indexed",
}

app.command.LoadPalette{
  ui=false,
  filename="palette.png",
}
```

Export a sprite sheet from a script:

```lua
app.command.ExportSpriteSheet{
  ui=false,
  askOverwrite=false,
  type=SpriteSheetType.ROWS,
  textureFilename="sheet.png",
  dataFilename="sheet.json",
  dataFormat=SpriteSheetDataFormat.JSON_HASH,
}
```

Save a copy without changing the active sprite filename:

```lua
app.command.SaveFileCopyAs{
  ui=false,
  filename="preview.gif",
}
```

Import a grid sprite sheet into frames when PixelLab or another source returned a sheet instead of separate frame files:

```lua
local spr = app.open("sheet.png")
if not spr then
  error("Could not open sprite sheet")
end

app.command.ImportSpriteSheet{
  ui=false,
  type=SpriteSheetType.ROWS,
  frameBounds=Rectangle(0, 0, 32, 32),
  padding=Size(0, 0),
  partialTiles=false,
}
```

Open a GIF directly when the source is already animated:

```lua
local spr = app.open("preview.gif")
if not spr then
  error("Could not open GIF")
end
```

Prefer script parameters over hard-coded paths so generated scripts are reusable and safe to review.

### Frame Manifest Contract

For multi-frame imports, prefer a small JSON manifest instead of inventing arguments per script. Include only local paths and non-sensitive metadata:

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

The script should sort by explicit `frame` value, verify each file exists, verify image dimensions before adding cels, set frame duration when provided, and create tags only from explicit manifest data or clear user intent.

## Example Use Cases

Use these examples to recognize valuable Aseprite handling. The exact PixelLab generation route still comes first; Aseprite is the local workspace/import/export step.

| Use case | Example user prompt |
|---|---|
| Create an editable workspace from generated frames | "Generate a 32x32 idle potion sparkle animation and make an `.aseprite` file with frames, durations, and an `idle` tag." |
| Import generated variants as layers | "Make three sword pickup variants, then put them as named layers in an Aseprite file so I can compare them." |
| Add generated frames to an existing project copy | "Use this existing `.aseprite` character file as the base and add a PixelLab walk animation as a new layer group in a copy." |
| Export an existing Aseprite project for a game engine | "Export this `.aseprite` as a packed sprite sheet with JSON metadata, only the `Attack` tag, and ignore the `Guides` layer." |
| Build a preview package | "Generate a small torch flame animation, create an Aseprite workspace, then export a GIF preview and sprite sheet." |
| Convert/palette-check local output in Aseprite | "Convert these generated PNG frames to indexed color with this palette and save the converted copies." |
| Open a verified result for manual editing | "Generate a chest sprite, save it locally, then open it in Aseprite after you verify the file exists." |
| Inspect an Aseprite file before deciding | "List the layers, tags, and frame count in this `.aseprite` file before importing anything." |
| Run visual QA on an animation | "Export frame 3 at 8x, compare frames 2 and 3, and check the color count before I review the animation." |
| Copy layers between workspaces | "Copy the `PixelLab - effects` layer group from this staging file into a copy of my character `.aseprite` file." |

## Common Workflows

### Generate Then Open

1. Generate the asset through PixelLab MCP or documented REST v2.
2. Download or write the verified output file under the active project/workspace `pixellab-pip-generations/` folder unless the user explicitly states or approves another output path.
3. Ask before launching GUI Aseprite.
4. Open the file visibly:

   ```powershell
   & $AsepritePath "output.png"
   ```

### Generate Frames Then Create `.aseprite`

1. Generate or collect frames locally under the active project/workspace `pixellab-pip-generations/` folder unless the user explicitly states or approves another output path.
2. Verify dimensions and frame order.
3. Write a small Lua assembly script or reuse one from the project if present.
4. Reuse the new sprite's default layer and first frame for the first generated frame, then create additional frames with explicit positions.
5. Run Aseprite in batch mode with `--script` and `--script-param`.
6. Verify the `.aseprite` file exists and the layer/frame counts match the inputs.
7. Optionally export a GIF or sheet for preview.

### Generated Variants As Layers

1. Put each generated variant in a stable local path under the active project/workspace `pixellab-pip-generations/` folder unless the user explicitly states or approves another output path.
2. Create one sprite sized to the largest accepted canvas.
3. Reuse and rename the default layer for the first variant, then create one named layer per additional variant.
4. Add one cel per layer at frame 1.
5. Save as `.aseprite`.

### Generated Animation As Frames

1. Sort frames by numeric filename or explicit metadata.
2. Create a new sprite from the first frame dimensions.
3. Reuse and rename the default layer for the animation.
4. Add the first image to frame 1, then create explicit new empty frames for subsequent images.
5. Set duration from PixelLab metadata when available, otherwise use the user's requested FPS.
6. Add tags such as `idle`, `walk`, `attack`, or the user's action name.
7. Save `.aseprite`, then export GIF/sheet if requested.

### Import Sprite Sheet Or GIF

1. Confirm whether the source is a grid sheet, packed sheet with JSON metadata, or GIF.
2. For a grid sheet, open the sheet image and use `app.command.ImportSpriteSheet{ ui=false, type=..., frameBounds=Rectangle(...), padding=Size(...) }`.
3. For a GIF, open the GIF with `app.open`; Aseprite should load its frames as an animation.
4. Apply frame durations and tags when metadata or the user's request provides them.
5. Save a new `.aseprite` file or import the frames into an existing-copy workflow.

### Import Into Existing `.aseprite`

1. Confirm the input `.aseprite` file, generated files to import, and intended placement.
2. Default to a new output file instead of modifying the original. Do not write to the input path unless the user explicitly approved in-place modification of that exact file.
3. Open the existing file in a Lua script with `app.open(input)`.
4. Inspect existing layer names, frame count, tags, canvas size, and color mode if placement depends on them.
5. Compare generated image dimensions against the existing canvas before creating cels.
6. If dimensions differ, do not silently crop, resize, or expand the canvas. Ask the user to choose: preserve origin and allow clipping, center on the current canvas, expand the canvas, resize generated art, or abort.
7. Keep color mode unchanged unless the user asked for conversion or approved it after seeing the source and target modes.
8. Create a clearly named layer or group for imported PixelLab output, such as `PixelLab - walk` or the user's requested name.
9. Add generated stills as cels on a new layer at the requested frame, or add generated animation frames across new/existing frames.
10. Add or update tags only when the user requested them or when the import represents a named animation.
11. Save with `spr:saveCopyAs(output)` unless the user explicitly approved modifying the original.
12. Verify the output copy with `--list-layers` and `--list-tags`.
13. If the workflow was copy-on-write, verify the original file was not changed.

Use this workflow for file-level edits only. It can modify an existing project file on disk, but it is not live control of the already-open Aseprite editor session.

### Copy Layers Between `.aseprite` Files

1. Confirm the source `.aseprite`, target `.aseprite`, requested layer or group names, frame handling, and output copy path.
2. Never write into the target original by default. Copy the target to a new output file first, then modify only the copy.
3. Use Lua to open both source and output copy with `app.open`.
4. Resolve requested layers by name. If none exist, stop with a clear error instead of creating empty placeholders.
5. Create missing target frames only when the user asked to preserve the source frame range or the import requires it.
6. Copy each source cel image and cel position into the matching target layer/frame. Preserve layer names unless the user asked for renamed layers.
7. Save the target copy, then verify target layers/tags/frame counts and verify the original target hash did not change.

### Existing `.aseprite` Export

1. Confirm input file and requested output format.
2. Use direct CLI for simple exports.
3. Use script export only when layer/tag/frame selection needs custom logic.
4. Verify output files and metadata exist.

### Visual Feedback And QA

Use visual feedback when the user wants to review, iterate, or quality-check an animation/workspace:

1. Export one or more frames at an integer scale such as 4x, 8x, or 10x for human-readable inspection.
2. For animation continuity, render an onion-skin-style preview or export neighboring frames together when a local script or installed MCP supports it.
3. Compare neighboring frames when the user asks whether motion changed enough or when a generated animation may have duplicate/near-duplicate frames.
4. Check color statistics or palette conformance when the user asked for a limited palette or indexed-color output.
5. Treat these as read-only QA unless the user asks for fixes; any fixes to an existing `.aseprite` still follow copy-on-write by default.

## Verification

After Aseprite CLI work, verify the result before reporting success:

- Check the expected output files exist.
- Aseprite can sometimes exit successfully without writing the expected file or while writing numbered sibling files for frame sequences. Check exact outputs and acceptable numbered outputs before reporting success.
- On launcher-based installs, the command can return before output files are fully visible on disk; wait briefly for expected files before declaring failure.
- For sprite sheets, check both image and JSON metadata when requested.
- For GIFs, inspect frame count/delay/disposal if transparency matters; see `local-asset-assembly.md`.
- For `.aseprite` files, run `--list-layers` and `--list-tags` when the task created layers or tags.
- For existing-file imports, verify the output copy exists and the original was not changed unless the user approved in-place modification.
- For exported PNG frames, count the output frames and compare against the requested frame count.
- For Lua scripts, require an explicit printed success/status line when possible and treat printed `ERROR:` lines as failures even if Aseprite exits with code 0.
- If Aseprite prints extension errors, report that Aseprite ran but an installed extension emitted startup errors. Do not print credentials or local extension internals.

## Bridge Escalation

Escalate beyond CLI integration only when the user needs repeated live-document operations that cannot be solved by file creation/open/import/export.

A future bridge should be designed as a local editor-control MCP or command queue with explicit approval gates. It should expose curated Aseprite/editor actions, not PixelLab extension private endpoints, credentials, or raw request payloads.
