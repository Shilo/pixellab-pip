# Aseprite MCP Integration

Read this only when the user explicitly asks for a third-party Aseprite MCP server or MCP-based Aseprite tooling. For ordinary Aseprite CLI/Lua file handling, use `aseprite-cli.md`.

Third-party Aseprite MCP servers are an optional escalation, not the default PixelLab-to-Aseprite route. Use one only when it adds real value beyond documented CLI/Lua — for example many small iterative draw/layer/cel/palette/animation operations, or curated visual-QA tools that are safer or clearer than a custom script. For import/export/package tasks already covered by CLI/Lua, stay with CLI/Lua.

## Safety delta over aseprite-cli.md

Everything in `aseprite-cli.md` still applies — Safety Gates, Original File Safety, and Verification. On top of that:

- Any MCP tool that saves back to a `.aseprite` file is a write operation. Apply the CLI original-file safety first: copy the original before mutation unless the user approved in-place editing of that exact path, show which files are read/written, and ask before overwriting.
- Treat destructive tools (delete, flatten, merge, erase, crop, resize, quantize, save-back) as copy-on-write by default; prefer read-only MCP tools for inspection and QA.
- A raw-Lua MCP tool is unrestricted local host-code execution, exactly like `aseprite --script`. Prefer curated tools or small reviewed scripts.
- Do not use an MCP server to inspect PixelLab credentials, extension request history, or private extension state.
- After a run, verify expected outputs (and, for copy-on-write flows, that the original was unchanged); treat printed `ERROR:` as failure even when the MCP call itself returned success.

For palette clamps, 1-bit output, batch import/export, layer copy, and QA mechanics, follow `aseprite-cli.md` — see its "Patterns Usable Without MCP" and "Palette Quantization" sections.
