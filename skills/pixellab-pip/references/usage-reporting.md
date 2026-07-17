# Usage Reporting

Read this after live PixelLab calls when preparing the final user report or a generation manifest. For polling, MCP review state, rate limits, and expiring download URLs, read `job-lifecycle.md`. Once the job returns image(s), apply the bark contract per SKILL.md, then give this report.

## Report Shape

Use this order for completed work, including work that completed but failed verification — then say plainly that verification failed. Omit sections and lines that do not apply; list only files that were actually produced. Do not narrate the process that led here.

```markdown
Done - [one plain sentence: what was produced and whether it passed verification.]

**Files**
- [Frames / image](path-or-url)
- [Spritesheet](path-or-url)
- [other artifacts only if actually produced, e.g. ZIP package, Manifest]

**Route**
- Surface/tool: `MCP create_1_direction_object` or `REST POST /v2/generate-image-v2`
- Output structure: `Atlas image` (one image containing the grid/sheet), `Separate images`, `Single image`, or `Animation frames`; add `Selection state: Drafts` when candidates still need selection
- Asset lifecycle: `Managed asset` when backed by a PixelLab/MCP asset ID, plus the retrieved shape when useful, e.g. `Managed tileset; tile PNGs assembled locally into a 4x4 sheet`
- Prompt prep: user wording preserved, agent-enhanced, inline `enhance_prompt`, or enhance endpoint

**Inputs Used**
- `description` / `action` / other natural-language fields: the exact final text sent
- Image/frame fields that anchored the result, by API field name: `image`, `first_frame`, `last_frame`, `reference_image`, `style_image`, `init_image`, `mask_image`; note omissions that change interpretation, e.g. `last_frame: omitted`
- Seed: the seed sent, the resolved seed returned, `multiple, see Manifest`, or `not exposed` when neither
- Non-default settings that materially affected the output: size, view/direction, count, mode/product label, `no_background`, frame count/timing, palette, reused base asset

**Cost**
- Total: [per-call usage from PixelLab, or the observed cost delta]

**Verified**
- [short checklist of the constraints the user actually asked for]
```

Two rules that always apply:

- Every final natural-language value sent to PixelLab (`description`, `action`, `edit_description`, `style_description`, `negative_description`, `item_descriptions`, `text`, `color_palette`) must appear in Inputs Used, even when the output failed verification or the field seems obvious. If a value is too large for chat, label it truncated and link the manifest/request file holding the full text.
- Report settings that materially affected the output; do not dump schema defaults.

Use Markdown links with user-facing labels (`Spritesheet`, `ZIP package`) for every listed file. Files live under the project `pixellab-pip-generations/` folder per SKILL.md; copy temporary URLs or cache paths there before reporting them as local outputs.

OpenCode does not render inline images in chat. Open the output folder.

For REST routes, report the exact public path used, with the `/v2` prefix and without collapsing create and retrieval routes: `REST POST /v2/create-tileset`, `GET /v2/tilesets/{tileset_id}`.

If local assembly produced a sheet/GIF/package, state that PixelLab produced the underlying images and that assembly preserved original pixels.

For cost, prefer per-call `usage` totals for the whole flow. If only balance is available, use `get_balance` / `GET /balance` before and after (no extra permission needed once live work is approved) and report the delta — but if other PixelLab jobs may have run concurrently, label the delta as an overlapping observation rather than the cost of this job. If neither is exposed, say `Cost: not exposed by the tool/API`. Label estimates as estimates.

Report cost as the delta. Never write a balance figure (`credits.usd`, `subscription.generations`, `subscription.total`) or a `before -> after` pair into a blueprint, manifest, or repo file; chat is fine. `usage.generations` is charged, `subscription.generations` is remaining: the parent key decides, not the magnitude.

## Manifest

Write a manifest for every live generation flow. Record per call or per result item (not just top-level):

- `job_id` / `background_job_id`, `asset_id`, and route-specific result/child IDs when present — enough to resume, inspect, or reproduce later.
- `seed`: the seed sent, or the resolved seed from the job/status response when the route returns one. Leave `seed` at its default (`0`, random) unless the user asks for one or another rule directs otherwise. Reuse a recorded seed when the user wants a near-variant of an approved result.

## Pending Jobs

If an async call times out or stays pending, keep the job or asset ID and poll the matching status route or MCP getter; do not resubmit a paid generation unless the user explicitly wants a fresh run. If a managed object returns `review` status, report the selection step instead of treating the job as incomplete. Details: `job-lifecycle.md`.
