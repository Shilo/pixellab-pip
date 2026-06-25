# PixelLab Aseprite Extension Coverage Audit

Last investigated: 2026-06-25.

Review basis: local compatibility review of the official PixelLab Aseprite editor integration.

Documentation policy: public docs may describe observed editor workflows and operation names, but must not reference internal source filenames, source layout, source contents, request payloads, credentials, or account-specific values.

## Summary

PixelLab Pip can cover Aseprite workflows, but it should not implement them by calling the same undocumented internal endpoints used by first-party surfaces. The official Aseprite extension is a first-party editor integration. Public agent/code surfaces are different:

- Hosted MCP tools for managed characters, objects, tilesets, tile variants, map objects, chat/sandbox helpers, projects, and balance.
- REST v2 endpoints under `https://api.pixellab.ai/v2` for code/API work.
- Aseprite/Pixelorama/website for editor-only workflows.

Pip should cover every Aseprite workflow by routing to the closest documented surface, not by treating the extension's private first-party editor integration protocol as a public REST or MCP contract.

## Agent Automation Finding

The current public PixelLab surfaces do not expose a clean MCP or headless control surface for driving Aseprite itself.

Observed editor behavior, described without publishing internal source details:

- Workflows are designed for interactive use inside Aseprite, with user-visible dialogs and editor placement behavior.
- Generation and editing flows depend on the active document, selected images, and editor-side state.
- Public docs must not copy credentials, account values, internal request payloads, or private integration metadata from a local installation.
- Request history and previews are editor workflow concepts; a future bridge should expose only curated, non-sensitive status/result data.

Practical implication: an agent such as Codex or Claude can already automate PixelLab through official MCP/REST and then import files into Aseprite, but it cannot reliably drive the current Aseprite extension directly without either UI automation or an added bridge.

## Efficient Near-Term Path: Aseprite CLI Integration

The most efficient near-term integration is not direct control of the PixelLab Aseprite extension. It is a constrained Aseprite CLI integration:

```text
MCP-capable agent
  -> PixelLab MCP or documented REST v2 generation
  -> verified local image/frame files
  -> Aseprite CLI or Lua script workspace/import/export step
  -> `.aseprite`, PNG sequence, GIF, sprite sheet, metadata, or visible Aseprite workspace
```

This has practical value for users who prefer Aseprite over the website because it gets generated assets into their normal workspace without depending on private extension internals. It also has lower maintenance risk than a full Aseprite MCP bridge because the moving parts are public PixelLab MCP/REST behavior and documented Aseprite CLI/scripting behavior.

Official Aseprite docs support this shape:

- Aseprite CLI can convert/export sprites, run in batch mode, save files, export sprite sheets, list layers/tags/slices, and execute Lua scripts with `--script` and `--script-param`.
- Aseprite's Lua API can open files, create new sprites, modify the active sprite, save modified sprites, show dialogs, and add plugin/menu options.

Recommended scope for Pip:

- Generate with PixelLab MCP/REST first.
- Save generated PNGs, frame sequences, GIF previews, ZIPs, or sprite sheets locally.
- Use Aseprite only for file/workspace handling: open/import, create or update `.aseprite` files, arrange frames/layers, set tags/durations, export sprite sheets/metadata, or launch the result for manual editing.
- Trigger this route only when the user explicitly asks for Aseprite handling, such as creating or updating an `.aseprite` file, importing frames into an existing project, arranging layers/tags, exporting through Aseprite, or continuing work in Aseprite.
- Ask before launching visible Aseprite, overwriting files, or running a local script that writes outside the generated output folder.
- For existing `.aseprite` projects, prefer writing a modified copy and require explicit approval before editing the original file in place.
- Useful Aseprite CLI coverage should include export filters, frame ranges, layer/tag/slice listing, sprite-sheet metadata, preview mode, scale/crop/trim, color-mode/palette conversion, and Lua scripts for creating layers, frames, cels, tags, durations, and imports from existing sheets or GIFs.

This route is not a replacement for an Aseprite MCP bridge. It does not solve live control of an already-open document, extension-only PixelLab operations, or interactive plugin dialogs. It is still worth adding to the agent skill because it answers the common user request "I want to work in Aseprite, not the website" with a stable, low-maintenance workflow.

Implementation guidance for the agent skill:

- Keep the main skill file as a router only. It should point explicit Aseprite requests to an Aseprite-specific reference file.
- Put Aseprite mechanics in the reference file, including CLI command patterns, script patterns, safety gates, and verification.
- Do not route every local asset assembly task through Aseprite. Generic GIF previews and spritesheet assembly can remain local image tooling unless the user asked for Aseprite.
- Treat the phrase "handoff" as a user-experience description, not the integration architecture. The actual architecture is PixelLab generation followed by Aseprite CLI/Lua workspace integration.

## Possible Aseprite MCP Bridge

The safest design is a companion local MCP server plus a small extension bridge, not making the Aseprite extension itself host MCP.

Recommended shape:

```text
MCP-capable agent
  -> local Aseprite bridge MCP server
  -> localhost WebSocket or file-command queue
  -> Aseprite PixelLab extension bridge script
  -> existing editor-approved generation and placement logic
```

Two bridge options are plausible:

- Local WebSocket bridge: the extension connects outward to a localhost service and receives commands such as `generate_image`, `animate_with_text`, `reduce_colors`, or `export_active_sprite`.
- File-command queue: the MCP server writes command JSON into an extension-owned queue folder; the extension polls on an Aseprite timer, executes approved commands, and writes result/status JSON back.

The file-command queue is simpler and more crash-tolerant. The WebSocket bridge is better for interactive status updates, cancellation, and live result streaming.

An MCP bridge should expose editor operations, not PixelLab's undocumented internal endpoint protocol. Example tool concepts:

| MCP tool concept | Aseprite-side behavior |
|---|---|
| `list_pixellab_aseprite_tools` | Return supported extension tool names and required parameters from curated bridge metadata. |
| `open_pixellab_tool` | Open the existing PixelLab dialog for a named tool. |
| `run_pixellab_tool_preview` | Populate a model and ask the user to approve generation in Aseprite before spending credits. |
| `run_pixellab_tool` | Execute an approved generation through the extension's supported editor workflow. |
| `get_active_sprite_context` | Return non-sensitive canvas metadata such as size, color mode, frame count, selected layer, and whether a sprite is open. |
| `export_active_sprite` | Export the active sprite or selected frames to a user-approved local path. |

Bridge guardrails:

- Do not expose or return the extension's stored secret, bearer token, session data, request auth fields, or full request JSON when it contains credentials.
- Require explicit user approval before credit-spending generation, destructive edits, downloads, deletes, or session/auth actions.
- Treat the private first-party editor integration protocol as editor behavior, not public REST v2 endpoints.
- Prefer official PixelLab MCP/REST for pure agent asset generation when the user does not need the result placed into the live Aseprite document.
- Keep Aseprite-specific commands scoped to the active editor session and visible user workflow.

Efficiency judgment: build the lightweight Aseprite CLI integration into Pip first. Consider a dedicated Aseprite MCP bridge only if users need repeated live-document operations that cannot be handled by opening/importing generated files or by simple Aseprite CLI/scripts.

## Evidence

- The official Aseprite integration provides interactive editor workflows for generation, editing, progress/status updates, and placing results back into Aseprite.
- Local compatibility review observed editor workflows including generation tools plus helpers such as reduce-colors, unzoom, skeleton editing, image placement, request history, and update checks.
- Observed extension operation names include image generation, style/reference generation, multi-image edit, quantize/reduce-colors, unzoom, pixel correction, map-extension, rotation, animation, tileset, UI, update, and review workflows.
- Official Aseprite CLI docs document batch mode, save/export options, sprite-sheet export, and `--script` / `--script-param` for Lua automation: <https://www.aseprite.org/docs/cli/>.
- Official Aseprite scripting docs and API docs document Lua scripting, `app.open`, `Sprite()`, `Sprite:saveCopyAs()`, dialogs, and plugin/menu extension points: <https://www.aseprite.org/docs/scripting/> and <https://www.aseprite.org/api/>.
- Official REST v2 docs list public paths under `/v2`, such as `/generate-image-v2`, `/edit-images-v2`, `/inpaint-v3`, `/animate-with-text-v3`, `/create-tileset`, `/create-tiles-pro`, `/resize`, and `/remove-background`.
- Official MCP docs explicitly distinguish MCP, REST v2, web interfaces, editor plugins, and legacy v1.

## Public Coverage Map

| Aseprite workflow family | Extension behavior | Pip route |
|---|---|---|
| General image, Pixen, style reference, Flux-like image generation | In-editor image generation with optional references and style controls; observed operation names include `generate-image-new`, `generate-image-pixen`, `generate-pixelart-flux`, `generate-consistent-style`, `generate-flux-same-style`, and `generate-style`. | REST v2 image endpoints such as `generate-image-v2`, `create-image-pixen`, `create-image-pixflux`, `create-image-bitforge`, `generate-with-style-v2`; Aseprite for exact in-editor behavior. |
| UI generation | In-editor UI element and layout-assisted generation; observed operation names include `generate-ui` and `generate-ui-template`. | REST v2 `generate-ui-v2`; website/editor for visual UI-library flows. |
| Image edit, inpaint, conversion, resize, remove background | In-editor editing, mask/inpaint, conversion, resize, and background removal; observed operation names include `generate-edit`, `generate-edit-image-pro`, `generate-inpainting`, `generate-inpainting-v3`, `generate-image-to-pixelart`, `generate-image-to-pixelart-pro`, `generate-resize`, and `remove-background`. | REST v2 `edit-image`, `edit-images-v2`, `inpaint`, `inpaint-v3`, `image-to-pixelart`, `image-to-pixelart-pro`, `resize`, `remove-background`. |
| Multi-image edit | In-editor edit using multiple supplied images; observed operation name `generate-multi-edit`. | REST v2 `edit-images-v2` when the task is a multi-source image edit; website/editor for visual experimental flows. |
| Animation, interpolation, skeleton, outfit transfer | In-editor animation generation/editing, skeleton-guided workflows, interpolation, and outfit transfer; observed operation names include `animate-with-text-v3`, `generate-animate-with-text`, `generate-animation`, `generate-edit-animation-pro`, `generate-interpolation-pro`, `generate-transfer-outfit-pro`, and `estimate-skeleton`. | REST v2 `animate-with-text*`, `animate-with-skeleton`, `estimate-skeleton`, `edit-animation-v2`, `interpolation-v2`, `transfer-outfit-v2`; MCP animation tools for managed characters/objects. |
| Rotation and directional assets | In-editor rotation and directional-sprite workflows; observed operation names include `generate-4-rotations`, `generate-8-rotations`, `generate-reference-to-8-rotations`, `generate-8-rotations-v3`, and `generate-rotate-single`. | REST v2 `rotate`, `generate-8-rotations-v2`, `generate-8-rotations-v3`; MCP character/object workflows when managed assets fit. No public REST v2 4-rotation route was documented. |
| Characters and objects | In-editor workflows that combine generation, style, rotation, and animation steps; observed operation names include `generate-spritesheet` and `generate-complete-character`. | MCP character/object tools by default; REST v2 character/object endpoints for exact API control. |
| Tiles, tilesets, isometric tiles | In-editor tile, tileset, sidescroller, isometric, and tile-variant workflows; observed operation names include `generate-tiles`, `generate-tiles-style`, `generate-tileset`, `generate-tileset-sidescroller`, `generate-isometric-tile`, and `generate-tiles-pro`. | MCP tileset/tile tools by default; REST v2 `create-tileset`, `create-tileset-sidescroller`, `create-isometric-tile`, `create-tiles-pro`. |
| Map image, map extension, texture | In-editor map image, map-extension, and texture workflows; observed operation names include `generate-map-flux`, `generate-inpainting-map`, `generate-inpainting-map-v2`, and `generate-texture`. | REST v2 image/background or tileset routes for generated assets; website/Aseprite for exact map-extension or texture editor workflows. No full public REST/MCP map CRUD or map-extension surface was documented. |
| Try-on and reshape | In-editor single-image compositing and reshape workflows; observed operation names include `generate-try-on` and `generate-reshape`. | Website/editor for single-image try-on/reshape behavior; REST v2 `transfer-outfit-v2` only for animation-frame outfit transfer. No public REST v2/MCP reshape endpoint was documented. |
| Quantize/reduce colors, unzoom, pixel correction | In-editor color reduction, unzooming, and pixel-art correction workflows; observed operation names include `quantize-image`, `unzoom-pixelart`, and `correct-pixelart`. | Aseprite/Pixelorama editor workflow. Use local fallback only when clearly labeled as non-PixelLab. No public REST v2/MCP route was documented for these exact tools. |

## Gaps Fixed In Pip

- Multi-image routing now points to REST v2 `edit-images-v2` instead of saying no public route exists.
- Quantize and unzoom are now described as extension-only PixelLab editor workflows, not simply local tooling.
- Canny/sketch, pose/depth/style-reference, pixel correction, 4-rotation, map-extension, and texture workflows are explicitly labeled as either closest documented REST routes or Aseprite/editor-only behavior.

## Rule

If a PixelLab capability appears only through undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension, Pip must not expose it as a public REST/MCP endpoint. It should route to Aseprite/Pixelorama/website when the user wants that exact editor behavior, or choose the closest documented REST v2/MCP path when the user wants code/agent execution. Treat internal endpoints as unsupported for automation unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools.

If a future Aseprite MCP bridge is added, document it as a local editor-control bridge. Do not describe it as PixelLab's public REST API, and do not include user-specific paths, credentials, or private account data in public documentation.
