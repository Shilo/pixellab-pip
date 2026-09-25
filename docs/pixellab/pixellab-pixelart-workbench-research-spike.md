# PixelLab PixelArt Workbench Research Spike

## Summary

`pixelart_workbench` is a PixelLab MCP-only, command-driven way for an agent's chosen model to inspect, edit, draw, and animate pixel art using structured operations. It runs PixelLab commands against an image reference and returns a new image ID for follow-up work. The exposed interface accepts PixelLab IDs and supported image references such as URLs; it does not accept a local filesystem path. It is useful when the requested work is specific enough to express as pixel operations, a layered drawing, or frame-by-frame scene recipe. For open-ended image creation and prompt-led model edits, PixelLab's normal generation and edit routes remain the better fit.

PixelLab's live MCP tool description calls the Workbench commands free for subscribers. The public MCP guide and REST API catalog do not publish that billing detail, so this spike treats it as a vendor statement from the exposed tool metadata. PixelLab's 0.4.125 announcement also reports about 70% lower token use in its own testing; this repository has not benchmarked that estimate, and it does not mean the caller's preferred AI model uses no tokens.

## Scope And Evidence

This spike documents the public-facing PixelArt Workbench contract and the richer behavior returned by the live hosted MCP tool's help commands. It does not claim access to PixelLab's implementation or private editor transport.

Sources checked on 2026-09-25:

- PixelLab's [public MCP guide](https://api.pixellab.ai/mcp/docs), with the refreshed snapshot at `.local/pixellab-doc-watch/snapshots/20260925T145051Z/raw/mcp-docs.md` and refresh report at `.local/pixellab-doc-watch/reports/20260925T145051Z.md`.
- The [public REST v2 OpenAPI document](https://api.pixellab.ai/v2/openapi.json), cached at `.local/pixellab-doc-watch/latest/raw/rest-openapi.json`. The current OpenAPI inventory has no `pixelart_workbench` path or REST operation.
- The official [REST v2 documentation](https://api.pixellab.ai/v2/docs) and PixelLab's [product documentation introduction](https://www.pixellab.ai/docs) for comparisons with normal API and editor workflows.
- The live PixelLab MCP tool declaration and read-only `describe start`, `describe cli`, `describe draw`, `describe edits`, `describe lint_rules`, `draw -h`, `edit -h`, and `inspect -h` responses. These are runtime help returned by the configured official MCP server, not a versioned section in the static public MCP guide. The static guide currently documents the tool parameters, one-command convention, ID-or-image-reference input, output ID, modes, and notes; the runtime help exposes further command and recipe detail.
- The Version 0.4.125 announcement supplied with the request. Its token-reduction figure is an attributed product claim, not an independent measurement.

The cache refresh at 2026-09-25T14:50:51Z completed all seven configured sources without fetch failures. The MCP guide had a raw update but no normalized summary drift; its meaningful Workbench change from the prior snapshot is that a subject may now be an ID **or** image reference (`character:<id>:south`, a data URL, or an HTTPS link), while local file paths remain excluded. Website-page raw changes had no normalized text change. REST OpenAPI and REST index sources were unchanged in that refresh.

## What The Tool Is

The tool is exposed through the hosted PixelLab MCP server as `pixelart_workbench`. Its public MCP guide describes a command-line-like interface to the Workbench engine: the agent sends one command, and PixelLab runs it on an existing drawing or image. The agent's model is the operator that chooses and composes the command; the command contract is structured and pixel-specific. This is distinct from giving a text prompt to a PixelLab image-generation model and asking that model to redraw the image.

The MCP call has three parameters:

| Parameter | Documented behavior |
|---|---|
| `argv` | Optional string or list of strings containing one Workbench command. Omit it to request the playbook. Prefer the command syntax returned by live `describe` help. |
| `mode` | `low` by default, for direct action and fewer tokens; `high` for fuller evidence and a review checklist. In high mode, put the plan and observations in `notes`. |
| `notes` | Optional observations and step objective, stored with the step. The first call should include the user's request; high mode always uses notes, while low mode may omit them. |

`argv` is a Workbench command, not a shell command. For example, a JSON change list or draw recipe is passed as an argument to one command. One MCP call can batch multiple edits inside that command's JSON payload, but the MCP tool itself is invoked once per Workbench command. Do not infer flags from shell conventions: `describe cli` lists commands, and `<command> -h` lists that command's arguments.

## Inputs, Identity, And Results

The refreshed public MCP guide says the subject is an ID or supported image reference, never a local file path. Live `describe start` help listed these image forms:

- `character:<id>:<direction>` and `character:<id>:<direction>:<animation>`.
- `object:<id>`.
- `job:<id>` or `job:<id>:<index>` for image-generation job output.
- An ID returned by a pixel-art tool.
- A URL; the public guide explicitly calls out HTTPS and data URLs.

This permits a workflow to continue from an existing PixelLab asset, from a generated job result, or from user artwork reachable at a supported URL. It does not create filesystem access: a local path is explicitly unsupported. The sources checked do not document a Workbench upload step; if the source artwork exists only as a local file, use another documented workflow to obtain a supported image reference or choose a PixelLab route with its own documented image input.

The public tool declaration says the server writes the output and returns a new ID. Keep that ID for subsequent Workbench calls instead of passing image bytes between steps. The static docs do not specify a public REST getter, file-export contract, or stable download lifetime for Workbench results; verify any desired download/export through the visible result or a documented MCP tool rather than inventing a path.

The `notes` field is stored with the step to improve the tools. This is a documented retention behavior. As a prudent consequence, do not put bearer tokens, credentials, or unrelated private information in notes.

## Discovery And Command Model

Use the live help rather than memorizing a presumed complete CLI:

```text
pixelart_workbench(argv=["describe", "cli"], mode="low")
pixelart_workbench(argv=["<command>", "-h"], mode="low")
```

The `describe cli` response grouped commands into these families:

| Family | Commands documented by live help | What they do |
|---|---|---|
| Author, edit, inspect | `inspect`, `edit`, `draw`, `describe` | Inspect image/frame sheets or zoomed crops; apply guarded pixel operations; build layered drawings or animations from a recipe; read the current command contracts. |
| Check and explain | `lint`, `measure`, `explain`, `clusters`, `parts`, `silhouette`, `motion`, `storyboard`, `reveal`, `crop`, `score`, `compare` | Report visual structure, colors, provenance, frame changes, silhouette, motion, or defects. `explain` reports resolved geometry and per-command footprints; `lint` findings can name the node and command responsible. |
| Palette and repair | `extract-palette`, `palette`, `repair` | Extract colors and ramp proposals, make hue-shifted ramps, or run the named cleanup operations. The exposed description calls repair deterministic cleanup for regridding, defringing, snapping, strays, holes, and flicker. |
| Drawing craft | `shade`, `selout`, `reoutline`, `clean-lines`, `aa`, `mirror`, `cluster`, `paste` | Apply focused drawing operations such as ramp shading, selective outlining, cluster edits, and guarded region replacement. Ramp-dependent work may require `extract-palette` first. |
| Candidate sweep | `sweep` | Render variations of a craft operation as candidates with a comparison sheet. |

This is the command set shown by `describe cli` on the checked date, not a compatibility guarantee for future versions. Each command's help is the authority for its exact flags and operation schema.

## The Two Main Workflows

### Inspect And Edit An Existing Image

For a localized pixel correction, the simplest pattern is:

1. Inspect the source once for the relevant frame, region, scale, and exact colors.
2. Send one `edit` command with all observed changes batched in its structured change list.
3. Inspect the returned result and correct only visible remaining defects.

Live help gives this shape:

```text
inspect <image> [--frames 1,2,3] [--region x0,y0,x1,y1] [--scale 1-24]
edit <image> --changes '[…]'
```

The documented edit family includes guarded pixel assignment, color mapping, region copying, outline operations, masks, flood fill, and brush edits. Guards can check expected colors or a fingerprint before applying a targeted operation; failed validation prevents an unsafe guessed edit. Inspect exact colors first instead of inferring pixel coordinates from a small preview. The Workbench's exact operation names and fields can change, so retrieve them with `describe edits` and command help.

### Draw Or Animate With A Recipe

`draw` accepts a structured recipe, and can be used for a layered still drawing or animation. The live recipe contract has a `job` section for canvas, frame count, timing, and views, plus a `scene` section for palette, ordered layers, source parts, drawing nodes, and per-view timing. It supports either pose/frame sequences or node property tracks. A `--sources` map associates a view (for example, `south`) with an image reference.

```text
draw --recipe '<JSON recipe>' --sources '{"south":"character:<id>:south"}'
```

The recipe command can:

- Divide an input sprite into selected parts, preserve the remainder, and draw parts on named layers.
- Place and attach nodes, then move, rotate, show, or hide them per frame.
- Draw with pixel, brush, shape, path, and grid commands; use the source palette or explicitly declared palette colors.
- Set per-frame durations and named events.
- Use body-only layers, exact bookend checks, clear-border checks, or protected regions where the recipe contract supports them.
- Inspect, revise, and render comparisons against a prior drawing ID.

The recipe is detailed scene authoring. The model must choose where parts and joints are, which pixels form each region, and how motion changes between frames. Moving a cutout can reveal pixels that the source did not contain (for example, the torso behind an arm); a recipe must account for such gaps. The tool does not claim to infer correct anatomy or hidden pixels automatically. Use the live `describe draw` contract for the full schema and limitations.

## Analysis And Verification

The Workbench has more than paint operations. It can produce structured diagnostics and review aids:

- `inspect` returns frame sheets or enlarged crops with exact colors.
- `measure` can report a pixel's location/owner and image geometry such as bounding box, centroid, widths, and colors.
- `explain` reports geometry and command footprints without rendering.
- `lint` reports named pixel-art issues such as outline gaps, orphan pixels/clusters, jaggies, banding, pillow shading, palette mismatch, dead commands, or symmetry; some are explicitly informational.
- `motion`, `storyboard`, `silhouette`, `reveal`, `parts`, `clusters`, `score`, and `compare` summarize different aspects of the image or animation.

These reports help an agent decide what to inspect or edit; they are not an artistic acceptance guarantee. Some lint outputs are heuristics or explicitly informational. A successful command does not prove that the character remains recognizable, the motion reads well, an outline is intentional, or an animation loop is seamless. Review the actual returned art and adjacent frames before reporting completion.

## Billing And Token Claims

| Claim | Evidence and limit |
|---|---|
| Workbench commands are free for subscribers | Present in the live PixelLab MCP tool description inspected on 2026-09-25. The static [public MCP guide](https://api.pixellab.ai/mcp/docs) and [REST API catalog](https://api.pixellab.ai/v2/docs) do not publish this detail. Treat it as the vendor's tool-metadata claim; no separate usage test or plan-by-plan billing contract was available. |
| The tool uses fewer LLM tokens | The live tool description calls low mode a fewest-token mode; the 0.4.125 announcement reports roughly 70% lower consumption in PixelLab's testing. The repository has not reproduced the benchmark, and no baseline/model, prompt set, or measurement method was supplied in the announcement. |
| No token cost at all | Not established. Workbench may avoid sending image bytes between calls by referring to IDs, but the agent's chosen AI model still consumes context and produces tool arguments. Its cost depends on that model and the size of the discussion. |
| Same billing as PixelLab generation | Not established. The Workbench tool metadata says its commands are free for subscribers; ordinary image-generation/edit/animation routes may consume PixelLab generations or credits. Do not apply a generation price estimate to Workbench or assume an edit/animation recipe is free solely because it uses the same MCP server. |

The tool description's free-for-subscribers claim is stronger than the public static billing documentation. Until PixelLab publishes a plan-specific billing statement, regard the availability/cost distinction as exposed runtime metadata and confirm the account/subscription terms if it is material to a purchasing decision.

## Comparison With Other PixelLab And Local Workflows

| Workflow | Input-to-output model | Best fit | Main tradeoff compared with Workbench |
|---|---|---|---|
| PixelLab image generation: MCP `create_image_pixen`/`create_image_pro`; REST `POST /create-image-pixen`/`POST /generate-image-v2` | A text description and optional image references are sent to a PixelLab image-generation route; an asynchronous job returns generated art. | New, open-ended image creation and multiple generated alternatives. | The model chooses the pixel-level result, so it requires less coordinate/recipe authoring. It gives less command-level control over exact pixels than a guarded Workbench edit. Workbench can instead construct simple art, but it needs a structured recipe. |
| PixelLab AI edit: MCP `edit_image_pixen`/`edit_image`; REST `POST /edit-image-pixen`/`POST /edit-images-v2` | A source image and text instruction ask an image model to alter the image. | Broad semantic change such as changing an outfit, adding a detail, or regenerating a region. | Less recipe authoring, more model judgment. Workbench is the closer fit when the requested change is a specific cluster, pixel, outline, or repeatable frame operation; it does not provide the same natural-language regeneration behavior. |
| PixelLab text animation: MCP `animate_image`; REST `POST /animate-with-text-v3` | An image and a motion description are sent to an animation model. | Descriptive, open-ended motion such as walking, waving, or flickering. | The model invents intermediate pixels and poses. Workbench can animate authored layers/nodes with explicit frame timing and positions, which offers a more specified construction path but takes more planning and recipe detail. |
| PixelLab Skeleton v3: MCP `animate_with_skeleton_v3`; REST `POST /animate-with-skeleton-v3` | A reference sprite plus a sequence of keypoint poses guides model-rendered animation. | Animation when explicit pose placement matters but generated pixel rendering is still desired. | Skeleton v3 supplies pose constraints to a generative animation route. Workbench draws/edits through explicit pixel operations and layered scene data; the approaches differ in who creates the frame pixels and are not interchangeable. |
| Website/editor workflows (Creator, Pixelorama, Aseprite) | A person works in PixelLab's web/editor surfaces or a supported editor integration. | Direct visual authoring, hands-on correction, and existing editor-centered workflows. | A visible editor lets the artist judge and manipulate pixels directly; Workbench keeps interaction in an MCP command loop and needs a reachable image reference. The public docs do not promise automatic synchronization between Workbench IDs and an open editor document. |
| Local pixel-art editors or scripts | Artwork is opened and changed as local files in a local editor/toolchain. | Local file access, manual drawing, custom scripting, and project-specific export. | Local tools operate on local files, while Workbench explicitly rejects file paths and runs through PixelLab MCP. There is no documented Workbench REST endpoint or local CLI package in the sources checked. |

The comparison follows the official descriptions of [REST v2 operations](https://api.pixellab.ai/v2/docs), the current [MCP tool catalog](https://api.pixellab.ai/mcp/docs), and PixelLab's overview of its [website/editor/API surfaces](https://www.pixellab.ai/docs). “More exact” here means that a command can specify pixels, colors, regions, or frame transforms directly; it does not mean every operation is safe, artistically correct, or identical to an editor's rasterizer.

## Strengths, Costs, And Limits

### Strengths

- **Pixel-level intent can be made explicit.** Guarded changes can name coordinates, colors, frames, regions, masks, and reasons rather than asking an image model to infer them.
- **A single command surface covers inspect, editing, drawing, animation, and analysis.** The agent can examine a result, apply a bounded operation, and inspect the returned ID without handing raw image bytes back through every step.
- **Recipes can preserve structure.** Layer names, source parts, node anchors, pose tracks, frame timing, and safety checks can make an authored animation easier to inspect and revise than an opaque prompt-only result.
- **Diagnostics expose useful evidence.** Exact color crops, command footprints, pixel ownership, comparisons, and motion summaries can reduce blind edits.
- **Model choice is flexible at the orchestration layer.** PixelLab's release announcement explicitly presents Workbench as usable by a preferred AI model through its MCP server; this does not imply that PixelLab exposes a REST API or its own LLM for the workflow.

### Tradeoffs And Unknowns

- **More reasoning shifts to the calling agent.** The model needs to translate visual intent into coordinates, color values, source masks, layers, and timing; poor observations can produce a precisely executed wrong edit.
- **The workflow is command- and JSON-oriented.** A small correction can be concise, but layered animation recipes can become substantially more involved than a text prompt or direct visual editor action.
- **There is no REST fallback.** The tool is MCP-only. If the PixelLab MCP tool is not configured, the Workbench-specific command system is unavailable; use ordinary REST image routes, a visible editor, or a local editor according to the user's intent.
- **No local path contract exists.** Files must be made available as a PixelLab ID or supported image reference before Workbench can act on them.
- **Static documentation trails the live command description.** The public MCP guide provides the wrapper fields but not the complete `describe` contracts. Discover commands and syntax at runtime; do not copy undocumented flags into an integration.
- **Several integration details remain undocumented in public sources.** They do not set a comprehensive size/frame ceiling, a stable command-error schema, a REST or SDK equivalent, or a public local-file export contract for Workbench. Ask the live tool for supported command help and report a limit as unknown when no help states it.
- **PixelLab's token reduction is not independently verified.** It should not be presented as a guaranteed 70% reduction or as a claim that the workflow eliminates LLM cost.

## Practical Selection Rule

Choose `pixelart_workbench` when the user asks for exact pixel-level work, analysis of a PixelLab image/drawing, layered pixel art, or a hand-authored frame recipe that fits its command language. Begin with `describe cli` or a task-relevant `describe` topic, inspect the source, batch a bounded command, and inspect the returned art and ID. Use regular PixelLab generation for open-ended new art, natural-language editing for semantic redraws, text animation for generative motion, and Skeleton v3 when a model should render from supplied pose keypoints. Use a visible website/editor or local tool when direct visual/file workflows are the required interaction.

Do not route a task to Workbench just because it mentions “pixel art,” and do not promise that it will achieve a better-looking result or a fixed token saving. Confirm that the exact operation, source reference, and desired result can be expressed by current live help before relying on it.

## Unresolved Questions

The public guide and live help checked here do not settle:

- Which subscription plans qualify for the free-command claim, or whether access/limits differ by plan.
- The exact accounting boundary for “free” when a subscriber supplies a preferred model through a separate AI product.
- Maximum dimensions, frame counts, accepted URL restrictions, command timeouts, or output-retention periods for every command family.
- Whether each analysis command is strictly read-only, what schemas all commands accept, and the stable error/result schema beyond the command help observed.
- A supported REST, SDK, local CLI, or editor-session equivalent.
- A reproducible basis for the announcement's roughly 70% token reduction.

## Source Notes

- Official static MCP source: [`https://api.pixellab.ai/mcp/docs`](https://api.pixellab.ai/mcp/docs); refreshed snapshot `.local/pixellab-doc-watch/snapshots/20260925T145051Z/raw/mcp-docs.md`.
- Official REST v2 source: [`https://api.pixellab.ai/v2/openapi.json`](https://api.pixellab.ai/v2/openapi.json); refreshed snapshot `.local/pixellab-doc-watch/latest/raw/rest-openapi.json`.
- Official REST v2 interactive documentation: [`https://api.pixellab.ai/v2/docs`](https://api.pixellab.ai/v2/docs).
- Official product documentation overview: [`https://www.pixellab.ai/docs`](https://www.pixellab.ai/docs).
- Refresh manifest/report/changes: `.local/pixellab-doc-watch/manifest.json`, `.local/pixellab-doc-watch/reports/20260925T145051Z.md`, and `.local/pixellab-doc-watch/changes/20260925T145051Z.json`.
- Live read-only help checked on 2026-09-25: `describe start`, `describe cli`, `describe draw`, `describe edits`, `describe lint_rules`, `draw -h`, `edit -h`, `inspect -h`, and the `pixelart_workbench` MCP tool metadata. Help output is dynamic runtime evidence; record another snapshot if the exact command contract must be reproduced later.
