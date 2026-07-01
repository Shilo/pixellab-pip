# Aseprite MCP Integration

Read this when the user explicitly asks for an Aseprite MCP server, an installed third-party Aseprite MCP, MCP-based Aseprite drawing tools, or MCP visual QA tooling. Read `aseprite-cli.md` only when the same task also needs direct Aseprite CLI/Lua file handling.

Do not read this for ordinary Aseprite CLI/Lua file handling.

## Positioning

Aseprite MCP tools are optional escalation tools, not the default PixelLab-to-Aseprite route.

Default route stays:

```text
PixelLab MCP or documented REST v2
  -> verified local image/frame files
  -> Aseprite CLI or Aseprite Lua script
  -> `.aseprite`, PNG sequence, GIF, spritesheet, metadata, or visible Aseprite workspace
```

Use Aseprite MCP only when it adds real value beyond direct CLI/Lua.

Good fit:

- The user explicitly asks to use an Aseprite MCP.
- An installed Aseprite MCP exposes curated tools that are safer or clearer than a custom script.
- The task needs many small iterative drawing, layer, cel, palette, or animation operations.
- The task needs visual QA tools such as scaled frame exports, onion-skin renders, frame diffs, color statistics, or scene validation.
- The task needs structured operations such as copying layers between `.aseprite` files, validating missing layers/cels, or auditing animation coverage.

Poor fit:

- Ordinary import/export/package tasks already covered by CLI/Lua.
- Automating the PixelLab Aseprite extension.
- Calling private PixelLab operations.
- Bypassing approval for credit-spending or editor actions.
- Treating a broad MCP toolset as safe to run against a user's original `.aseprite` file.

## Safety Rules

Many Aseprite MCP tools are wrappers around Aseprite batch/Lua and may save back to the file they receive. Apply the same original-file safety rules from `aseprite-cli.md`:

- Copy an existing `.aseprite` original before MCP mutation unless the user explicitly approved in-place editing for that exact file path.
- Show which files will be read and written.
- Ask before overwriting files.
- Prefer read-only MCP tools for inspection and QA.
- Treat destructive tools such as delete, flatten, merge, erase, crop, resize, quantize, and save-back as write operations requiring copy-on-write by default.
- Do not use MCP tools to inspect credentials, extension request history, or private PixelLab extension state.

If an Aseprite MCP exposes a raw Lua escape hatch, treat it like `aseprite --script`: it can run unrestricted local host code. Prefer curated MCP tools or small reviewed scripts, and verify expected files/status afterward.

## Useful MCP-Inspired Patterns

Even when no Aseprite MCP is used, these patterns are useful for CLI/Lua workflows:

- Export one frame at 4x, 8x, or 10x for review before changing more files.
- Render onion-skin-style previews when animation continuity matters.
- Compare neighboring frames to detect duplicate or near-duplicate animation frames.
- Count colors or inspect color histograms when the user asked for palette discipline.
- For exact palette clamps, 1-bit black/white output, or "replace the palette with only these colors" requests, follow `aseprite-cli.md`'s palette quantization contract even if an MCP tool performs the mechanics: distinguish visible pixel colors from document palette entries, preserve or explicitly resolve transparency, and verify every touched frame.
- Validate expected layers/cels/tags before and after imports.
- Copy layers between a staging `.aseprite` file and a copy of the target `.aseprite` file.
- Require explicit printed script status such as `OK` or `ERROR:<message>` when running generated Lua.

## Verification

After using Aseprite MCP tools:

1. Verify expected output files exist.
2. Verify exact outputs or acceptable numbered frame outputs, because Aseprite may write frame-numbered sibling files.
3. For `.aseprite` changes, inspect metadata such as layers, tags, frames, and durations.
4. If the task touched an existing file through a copy-on-write workflow, verify the original file was unchanged.
5. Treat raw Lua output containing `ERROR:` as failure even when the process or MCP call itself returned successfully.
