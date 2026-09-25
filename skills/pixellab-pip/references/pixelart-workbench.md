# PixelArt Workbench

Read this for explicit PixelArt Workbench requests or model-authored pixel operations that fit its command workflow.

Use MCP `pixelart_workbench`; this is an MCP-only tool, not a REST route. It accepts PixelLab IDs and supported image references (including character/object/job references, HTTPS URLs, and data URLs), but not local file paths. Pass one command in `argv` per call (string or argument list), use low mode by default, and use returned IDs for follow-up operations. Optional `notes` are stored with the step; include them on each call where they are needed. Inspect the resulting art before reporting completion. The MCP tool description says PixelLab's Workbench commands are free for subscribers; this does not cover the preferred AI model's token cost.

Start with `argv=["describe", "start"]` in low mode for brief guidance. Use `argv=["describe", "cli"]` when the command list or syntax is needed. Follow the live command description; do not invent flags. `draw --recipe` supports layered art and animation.

Use the regular image-generation route for open-ended image creation when no direct pixel-operation workflow is requested. The 0.4.125 announcement reports roughly 70% lower token consumption from PixelLab's testing; treat that as an estimate, not a guaranteed result.
