# PixelArt Workbench

Read this for explicit PixelArt Workbench requests or model-authored pixel operations that fit its command workflow.

Use MCP `pixelart_workbench`; this is an MCP-only tool, not a REST route. It accepts PixelLab IDs and supported image references (including character/object/job references, HTTPS URLs, and data URLs), but not local file paths. Pass one command in `argv` per call (string or argument list), use low mode by default, and use returned IDs for follow-up operations. Optional `notes` are stored with the step; include them on each call where they are needed. Inspect the resulting art before reporting completion. For preservation-critical localized edits, compare the source and returned IDs to confirm changes stay inside the requested region. The live tool description says Workbench is free for subscribers, but a 2026-09-25 Workbench-only test window coincided with a +6 account generation delta and no per-call usage field; billing remains unverified. Apply the normal paid-call gate when usage matters and record before/after balance deltas.

Start with `argv=["describe", "start"]` in low mode for brief guidance. Use `argv=["describe", "cli"]` when the command list or syntax is needed. Follow the live command description; do not invent flags. `draw --recipe` supports layered art and animation. See the [Workbench research spike](../../../docs/pixellab/pixellab-pixelart-workbench-research-spike.md) for current measured results.

For recipes that cut or move source parts, run `parts <drawing-id>` and fix unassigned or double-claimed pixels. Use an explicit mask when the `{}` shorthand does not produce an auditable partition.

Use the regular image-generation route for open-ended image creation when no direct pixel-operation workflow is requested. The 0.4.125 announcement reports roughly 70% lower token consumption from PixelLab's testing; treat that as an estimate, not a guaranteed result.
