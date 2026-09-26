# PixelArt Workbench

Read this for explicit PixelArt Workbench requests or model-authored pixel operations that fit its command workflow.

Use MCP `pixelart_workbench`; this is an MCP-only tool, not a REST route. It accepts PixelLab IDs and supported image references (including character/object/job references, HTTPS URLs, and data URLs), but not local file paths. Pass one command in `argv` per call (string or argument list), use low mode by default, and use returned IDs for follow-up operations. Optional `notes` are stored with the step; include them on each call where they are needed. Inspect the resulting art before reporting completion.

For preservation-critical localized edits, compare compatible IDs: two drawing IDs or two still-image IDs. In testing, mixing a drawing ID with the still-image ID returned by `edit` caused a generic `invalid_input`; `inspect` the drawing source to obtain a still-image ID before comparing it with an edited image. The live tool description labels Workbench free for subscribers, but responses expose no per-call `usage.generations`; report that as PixelLab's published claim, not an account-ledger measurement. Host-model token use is separate. Follow the [usage-reporting guidance](usage-reporting.md).

Start with `argv=["describe", "start"]` in low mode for brief guidance. Use `argv=["describe", "cli"]` when the command list or syntax is needed. Follow the live command description; do not invent flags. `draw --recipe` supports layered art and animation.

For recipes that cut or move source parts, run `parts <drawing-id>` and fix unassigned or double-claimed pixels. An empty `{}` source part passed one small test but failed on a different larger fixture; use an explicit mask when predictable coverage matters and audit either form.

Use the regular image-generation route for open-ended image creation when no direct pixel-operation workflow is requested. The 0.4.125 announcement reports roughly 70% lower token consumption from PixelLab's testing; treat that as an estimate, not a guaranteed result.
