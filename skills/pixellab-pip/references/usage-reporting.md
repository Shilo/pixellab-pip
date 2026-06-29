# Usage Reporting

Read this before the first credit-spending live PixelLab call when cost may require a before/after balance check, and after live PixelLab calls when preparing the final report. For polling, MCP review state, rate limits, and expiring download URLs, read `job-lifecycle.md`.

After final success verification for a live PixelLab generation, edit, transform, conversion, background-removal, or animation job, apply the bark completion-sound contract in `bark.md`, then give the user a concise Markdown report. Bark must run only for successful live PixelLab generation-style work, not for setup, auth checks, balance/status checks, docs, failures, pending jobs, downloads alone, or local post-processing alone.

## Report Shape

Use this order for successful work. Keep it readable and short; omit sections that truly do not apply.

```markdown
Done - [one plain sentence saying what was produced and whether it passed verification.]

**Files**
- [Individual PNGs](path-or-url)
- [Spritesheet](path-or-url)
- [Preview sheet](path-or-url)
- [Package](path-or-url)

**Route**
- Surface/tool: `MCP create_1_direction_object` or `REST POST /generate-image-v2`
- Prompt prep: user wording preserved, agent-enhanced, PixelLab inline `enhance_prompt`, or PixelLab enhance endpoint

**Inputs Used**
- `description`: exact final text sent, or concise excerpt if very long
- `action`: exact final text sent, when animation/action was used
- Non-default controls: size, view/direction, seed, count, mode/method/product label, `no_background`, frame count/timing, image roles, masks, references, palette, outline/detail/shading, or reused base asset

**Cost**
- Total: [usage returned by PixelLab, or balance before -> after and delta]

**Verified**
- [short checklist of requested constraints actually checked]
```

Use normal Markdown links for every useful output file, directory, URL, ZIP, manifest, preview, or package. Prefer user-facing labels such as `Individual PNGs`, `Spritesheet`, `Preview`, `ZIP package`, and `Manifest` over raw filenames alone.

Unless the user explicitly states or approves another output location, local PixelLab generation artifacts and derived files should live under the active project/workspace `pixellab-pip/` folder. If an external tool returns a temporary URL or cache path, download or copy the selected final files into that folder before reporting them as local outputs.

Put route and inputs in bullets instead of burying them in prose. Do not lead with internal job IDs. Include job, asset, or result IDs only when the result is pending/review, when the user needs the ID for a follow-up action, or when debugging exact status/schema behavior.

Always include the final user-facing natural-language values that affected generation, especially `description`, `action`, `edit_description`, `animation_description`, `style_description`, `negative_description`, `item_descriptions`, `text`, and `color_palette`. If prompt enhancement or agent enhancement changed the user's wording, show the final value used. If a value is too long, include the most useful excerpt and say it was truncated for readability.

Report only non-default controls that materially affected the output. Do not dump every schema default. Mention seed when set or returned; otherwise say `seed: random/not exposed` only if reproducibility matters.

For cost, report total generation cost for the whole generate/promote/edit flow when exposed. Prefer exact per-call `usage` totals when available. If only balance is available, report `before -> after` and the delta. If usage and balance are both unavailable, say `Cost: not exposed by the tool/API`.

Use `get_balance` or REST `GET /balance` before and after nontrivial generation when available. If only balance is available, report the delta. If neither per-call usage nor balance is exposed, say usage was not exposed. Label estimates as estimates.

If an async call times out or remains pending, keep the job or asset ID and use the matching status/get route or MCP getter. Do not resubmit a paid generation unless the user explicitly wants a fresh run. If a managed object returns `review` status, report the candidate-selection step instead of treating the job as incomplete.

For REST error handling, rate limits, MCP review states, stale download URLs, and map-object expiry, use `job-lifecycle.md`.
