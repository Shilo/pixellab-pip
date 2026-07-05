# Editor-Only Utilities

Read this when the user wants an exact PixelLab editor utility that has no documented public REST v2 or MCP route. Map each request to the closest public route or a clearly labeled non-PixelLab local fallback; the routing boundary and the "do not invent `/v2/...` routes" rule are stated in SKILL.md.

| User wording | Route | Warning |
|---|---|---|
| Canny, sketch-guided, pose-guided, depth/image-to-image | Visible website/editor/Aseprite flow for exact behavior; REST v2 only for approximate documented init/reference/skeleton workflows after explaining the difference. | No exact public REST v2/MCP Canny/Pose/Depth route was documented. Do not call internal editor operation URLs. |
| Reduce colors / quantize palette | Visible PixelLab website/editor, Aseprite, or Pixelorama workflow when the user wants exact PixelLab editor behavior. For direct file-level palette quantization, source-derived N-color reduction, bit-depth conversion, indexed conversion, strict palette clamps, or document palette replacement, read `aseprite-cli.md` even when the user did not explicitly say Aseprite. | Do not invent `/v2/quantize-image`. Distinguish PixelLab editor reduce-colors behavior from documented Aseprite CLI/Lua file handling. |
| Unzoom pixel art / remove upscaling | Aseprite or Pixelorama extension when the user is actively in that editor; otherwise local image tooling as a labeled fallback. | Do not invent `/v2/unzoom-pixelart`. |
| Pixel correction / clean-up | Visible Aseprite/editor workflow for exact PixelLab behavior, or closest documented REST edit/convert route after checking docs. | Do not invent `/v2/correct-pixelart`. |
| Reshape character proportions | Website/editor Reshape, or closest documented edit/character route after verifying docs. | Website docs have fixed-size expectations; no public REST v2/MCP reshape route was documented. |
| Single-image Try on garment/accessory | Website Try on for a composited experimental output. | REST `transfer-outfit-v2` is animation-frame outfit transfer, not the same single-image try-on output and not isolated paperdoll layers. |

If future official REST/MCP docs expose a matching public route, prefer the documented route and update this reference.
