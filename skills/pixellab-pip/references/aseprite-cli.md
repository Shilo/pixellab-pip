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

Good fit:

- Open a generated PNG, GIF, sprite sheet, or frame sequence in Aseprite.
- Create an `.aseprite` workspace from generated frames.
- Open an existing `.aseprite` file and save a modified copy with generated assets added.
- Put generated variants into named layers.
- Put generated animation frames into numbered frames with tags and durations.
- Export an `.aseprite` file to PNG frames, GIF, sprite sheet, or JSON metadata.
- Inspect layers, tags, slices, or export metadata from an Aseprite file.
- Convert palette/color mode when Aseprite's documented CLI supports the needed conversion.

Poor fit:

- Driving the PixelLab Aseprite extension UI.
- Calling undocumented operation URLs used by the extension.
- Reading extension credentials, request payloads, auth headers, private settings, or request history.
- Controlling an already-open Aseprite document without a user-approved bridge.
- Spending PixelLab credits from inside Aseprite through hidden automation.
- Mouse, screenshot, or OCR automation as the default workflow.

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
6. Keep generated scripts and outputs inside the user's chosen output directory unless they approve another path.
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

## Optional Aseprite MCP Tools

Third-party Aseprite MCP servers can be useful when the user explicitly asks to use one, or when an installed MCP exposes curated tools for iterative Aseprite work. Keep this separate from the default PixelLab route.

Use an Aseprite MCP only when it adds real value beyond direct CLI/Lua, such as:

- Iterative pixel drawing where the agent needs many small canvas/layer/cel operations.
- Visual feedback loops such as scaled frame exports, onion-skin renders, frame diffs, or color statistics.
- Structured scene operations such as copying layers between `.aseprite` files, validating missing layers/cels, or auditing animation coverage.
- A curated tool is safer and clearer than a custom raw Lua script.

Do not use an Aseprite MCP to automate the PixelLab Aseprite extension, call private PixelLab operations, or bypass approval for credit-spending/editor actions. Many Aseprite MCP tools save back to the file they receive; apply the same original-file safety rule: copy first unless the user explicitly approved in-place edits for that exact file.

If an Aseprite MCP exposes a raw Lua escape hatch, treat it like `aseprite --script`: it can run unrestricted local code. Prefer curated MCP tools or small reviewed scripts, and verify expected files/status afterward.

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

For multi-frame sprites, use filename formatting such as `{frame}` or expect Aseprite to number the output files:

```powershell
& $AsepritePath -b "source.aseprite" --color-mode indexed --save-as "indexed-{frame}.png"
```

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
2. Download or write the verified output file.
3. Ask before launching GUI Aseprite.
4. Open the file visibly:

   ```powershell
   & $AsepritePath "output.png"
   ```

### Generate Frames Then Create `.aseprite`

1. Generate or collect frames locally.
2. Verify dimensions and frame order.
3. Write a small Lua assembly script or reuse one from the project if present.
4. Reuse the new sprite's default layer and first frame for the first generated frame, then create additional frames with explicit positions.
5. Run Aseprite in batch mode with `--script` and `--script-param`.
6. Verify the `.aseprite` file exists and the layer/frame counts match the inputs.
7. Optionally export a GIF or sheet for preview.

### Generated Variants As Layers

1. Put each generated variant in a stable local path.
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
