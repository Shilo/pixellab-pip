# Usage Reporting

Read this before the first credit-spending live PixelLab call when cost may require a before/after balance check, and after live PixelLab calls when preparing the final report. For polling, MCP review state, rate limits, and expiring download URLs, read `job-lifecycle.md`.

After final success verification for a live PixelLab generation, edit, transform, conversion, background-removal, or animation job, apply the bark completion-sound contract in `bark.md`, then give the user a concise Markdown report. Bark must run only for successful live PixelLab generation-style work, not for setup, auth checks, balance/status checks, docs, failures, pending jobs, downloads alone, or local post-processing alone.

## Report Shape

Use this order for successful work. Keep it readable and short; omit sections that truly do not apply. For live generation work that completes but fails verification, still use this report shape and say plainly that verification failed.

```markdown
Done - [one plain sentence saying what was produced and whether it passed verification.]

**Files**
- [Individual PNGs](path-or-url)
- [Spritesheet](path-or-url)
- [Preview sheet](path-or-url)
- [Package](path-or-url)
- [Manifest](path-or-url)

**Route**
- Surface/tool: `MCP create_1_direction_object` or `REST POST /v2/generate-image-v2`
- Output structure: `Atlas image`, `Separate images`, `Single image`, `Animation frames`, or another concise pixel/file-shape label when those do not apply
- Selection state: `Drafts` when generated options still need selection
- Asset lifecycle: `Managed asset` when the result is backed by a PixelLab/MCP asset ID, plus the retrieved output shape when useful
- Delivered package: ZIP, archive, or packaged folder when one was delivered
- Prompt prep: user wording preserved, agent-enhanced, PixelLab inline `enhance_prompt`, or PixelLab enhance endpoint

**Inputs Used**
- `description`: exact final text sent, when used
- `action`: exact final text sent, when animation/action was used
- Required image/frame fields: name each field that materially anchored the result, such as `image`, `first_frame`, `last_frame`, `reference_image`, `style_image`, `init_image`, `mask_image`, or `directions`, and say when an optional paired field was omitted if that changes interpretation, such as `last_frame: omitted`
- Seed: exact seed when one seed was used, `multiple, see Manifest` for multi-seed work, `not supported`, or `not exposed`
- Generation settings: size, view/direction, count, mode/method/product label, `no_background`, frame count/timing, masks, references, palette, outline/detail/shading, reused base asset, or other non-default settings that materially affected the output

**Cost**
- Total: [usage returned by PixelLab, or balance before -> after and delta]

**Verified**
- [short checklist of requested constraints actually checked]
```

Use normal Markdown links for every useful output file, directory, URL, ZIP, manifest, preview, or package. Prefer user-facing labels such as `Individual PNGs`, `Spritesheet`, `Preview`, `ZIP package`, and `Manifest` over raw filenames alone.

Unless the user explicitly states or approves another output location, local PixelLab generation artifacts and derived files should live under the active project/workspace `pixellab-pip-generations/` folder. If an external tool returns a temporary URL or cache path, download or copy the selected final files into that folder before reporting them as local outputs.

## Manifest Persistence Contract

YAGNI rule: do not add persistence machinery outside the manifest/reporting work already needed for a PixelLab generation. When a live PixelLab generation, edit, transform, conversion, background-removal, or animation manifest is created, store the IDs and seeds needed to resume, inspect, reproduce, or audit the result later. PixelLab does not consistently expose seeds later through MCP getters, REST asset getters, downloadable metadata, or documented response schemas.

For every PixelLab call or managed asset in a manifest, include the fields that exist for that route:

- `job_id` or `background_job_id`: the async PixelLab job ID returned by REST or MCP, when present.
- `asset_id`: the persistent PixelLab/MCP asset ID, such as character, object, tileset, tile, UI asset, font, animation, or map-object ID, when present.
- `result_id` or route-specific child IDs: IDs for selected candidates, child tiles, animation groups, frames, or other follow-up handles when the route exposes them.
- `seed`: the exact integer sent to PixelLab when the route accepts a seed.
- `seed`: the exact resolved integer returned by PixelLab when the request used random/default seed and the final response exposes a resolved seed.
- `seed`: `null` only when the selected tool or endpoint has no seed input and no returned seed.
- `seed_provenance`: `user_provided`, `agent_generated`, `pixellab_returned`, `not_supported`, or `not_exposed`.

When the selected MCP tool or REST endpoint exposes a `seed` input and the user did not provide one, choose a non-zero integer seed before the first paid call, send it in the request, and record `seed_provenance: agent_generated`. Do not pass `0`, `null`, or omit `seed` merely to ask PixelLab for a random seed unless the user specifically wants PixelLab-random output or the endpoint only documents that behavior. If a legacy/random run already used `0`, `null`, or an omitted seed and the final job/status response exposes a resolved seed, update the final manifest to the resolved value with `seed_provenance: pixellab_returned`; otherwise record the original request value and `seed_provenance: not_exposed`.

For multi-call outputs such as batches, candidates, per-direction animations, tilesets plus chained child tilesets, or retry attempts, record job IDs, asset IDs, child/result IDs, seed, and seed provenance per call or per result item, not only once at the top level. Also preserve raw request and final job/status JSON when available, because undocumented `last_response.seed` fields may be the only later evidence of PixelLab's resolved random seed.

Put route and inputs in bullets instead of burying them in prose. Do not lead with internal job IDs. Include job, asset, or result IDs only when the result is pending/review, when the user needs the ID for a follow-up action, or when debugging exact status/schema behavior.

For REST routes, report the exact public v2 HTTP path that was actually used, such as `REST POST /v2/create-tileset` for top-down tileset creation, `REST POST /v2/create-tileset-sidescroller` for sidescroller creation, or `GET /v2/tilesets/{tileset_id}` for top-down retrieval. Do not omit the `/v2` prefix or collapse create and retrieval routes into one shorthand.

Output structure describes the pixel/file shape, not the lifecycle or selection state. Use `Atlas image` for a single PixelLab output image that already contains the full grid/sheet/atlas. Use `Separate images` for multiple PixelLab output images delivered individually, whether or not they are later arranged or packaged. Use `Single image` for one non-atlas still image. Use `Animation frames` for frame sequences. Use `Selection state: Drafts` for generated options that still need selection; after selection, report the selected output structure and note the selection step.

Report managed assets and packages separately from output structure. If an MCP/REST asset ID is involved, add `Asset lifecycle: Managed asset` and explain the retrieved shape, such as `Managed asset; retrieved as separate directional PNGs`, `Managed tileset; retrieved tile PNGs assembled locally into a 4x4 sheet`, or `Managed character; retrieved animation frames`. If a ZIP, archive, or packaged folder is delivered, add `Delivered package` and describe whether it contains original PixelLab outputs, locally assembled sheets, frames, or metadata.

When the output is a grid, sheet, atlas, spritesheet, or package assembled locally, state how PixelLab produced the underlying images. If local assembly was used, report it as local processing and make clear the assembly preserved original PixelLab pixels.

Always include every final user-facing natural-language value that was sent to PixelLab or otherwise affected generation, especially `description`, `action`, `edit_description`, `animation_description`, `style_description`, `negative_description`, `item_descriptions`, `text`, and `color_palette`. This is mandatory for both successful reports and completed-but-failed-verification reports. If a `description` field was used, the report must display `description` under `Inputs Used`; do not omit it because the output failed, because the report is short, or because the field seems obvious from the request. If prompt enhancement or agent enhancement changed the user's wording, show the final value used. Show the exact value for `description` unless it is too large for the chat response; when truncation is unavoidable, label it as truncated and include the saved local request/manifest file that contains the full exact value.

Always name image, mask, reference, and frame input fields by their actual API/tool field names when they define the result. Do this even when the field is required by the selected route, because required inputs can still carry the subject identity, edit target, style, direction, or animation anchor. For animation, explicitly state `first_frame` and whether `last_frame` was used or omitted.

Report only generation settings that materially affected the output. Do not dump every schema default. In user-facing reports, include a concise `Seed` line: the exact seed when one seed was used, `multiple, see Manifest` for multi-seed work, `not supported`, or `not exposed`.

For cost, report total generation cost for the whole generate/promote/edit flow when exposed. Prefer exact per-call `usage` totals when available. If only balance is available, report `before -> after` and the delta. If other PixelLab jobs may have run concurrently, do not present a balance delta as the cost of one specific job; label it as an overlapping balance observation and prefer the job's own `usage` when available. If usage and balance are both unavailable, say `Cost: not exposed by the tool/API`.

Use `get_balance` or REST `GET /balance` before and after nontrivial generation when available. If only balance is available, report the delta. If neither per-call usage nor balance is exposed, say usage was not exposed. Label estimates as estimates.

If an async call times out or remains pending, keep the job or asset ID and use the matching status/get route or MCP getter. Do not resubmit a paid generation unless the user explicitly wants a fresh run. If a managed object returns `review` status, report the selection step instead of treating the job as incomplete.

For REST error handling, rate limits, MCP review states, stale download URLs, and map-object expiry, use `job-lifecycle.md`.
