# PixelArt Workbench

Read this for explicit PixelArt Workbench requests or model-authored pixel operations that fit its command workflow.

Use it for pixel-level repair or recipe drawing, inspecting/measuring/linting art, comparing revisions, and planning motion from source parts. For open-ended image creation, use the normal generation route. It is an MCP-only tool, not a REST route. It accepts PixelLab IDs and supported image references (including character/object/job references, HTTPS URLs, and data URLs), but not local file paths. Pass one command in `argv` per call (string or argument list) and use returned IDs for follow-up operations. Use the user's requested mode; otherwise use `low`. `high` returns fuller evidence and a review checklist, so include the plan and observations in `notes` (required in high mode). On the first call, put the user's request in `notes`. Inspect the resulting art before reporting completion.

For preservation-critical localized edits, compare compatible IDs: two drawing IDs or two still-image IDs. In testing, mixing a drawing ID with the still-image ID returned by `edit` caused a generic `invalid_input`; `inspect` the drawing source to obtain a still-image ID before comparing it with an edited image. Research observed the live tool description label Workbench free for subscribers; check the current tool description and account eligibility before treating a call as free. Responses expose no per-call `usage.generations`, so report the pricing statement as PixelLab's claim, not an account-ledger measurement. Host-model token use is separate. Follow the [usage-reporting guidance](usage-reporting.md).

Start with `argv=["describe", "start"]` in low mode for brief guidance. Use `argv=["describe", "cli"]` when the command list or syntax is needed. Follow the live command description; do not invent flags. `draw --recipe` supports layered art and animation.

For recipes that cut or move source parts, run `parts <drawing-id>` and fix unassigned or double-claimed pixels. An empty `{}` source part passed one small test but failed on a different larger fixture; use an explicit mask when predictable coverage matters and audit either form.

Use the regular image-generation route for open-ended image creation when no direct pixel-operation workflow is requested. The 0.4.125 announcement reports roughly 70% lower token consumption from PixelLab's testing; treat that as an estimate, not a guaranteed result.
