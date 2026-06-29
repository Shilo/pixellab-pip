# Editor-Only Utilities

Read this when the user asks for exact PixelLab editor utilities that do not have a documented public REST v2 or MCP route.

The stable automation rule is: use public MCP or REST v2 when a documented route exists; use visible website/editor/Aseprite/Pixelorama assistance for exact editor-only behavior; use local tooling only as a labeled non-PixelLab fallback after explaining the difference.

## Known Editor-Only Or Partial-Public Cases

| User wording | Route | Warning |
|---|---|---|
| Canny, sketch-guided, pose-guided, depth/image-to-image | Visible website/editor/Aseprite flow for exact behavior; REST v2 only for approximate documented init/reference/skeleton workflows after explaining the difference. | No exact public REST v2/MCP Canny/Pose/Depth route was documented. Do not call internal editor operation URLs. |
| Reduce colors / quantize palette | Visible PixelLab website/editor, Aseprite, or Pixelorama workflow when the user wants PixelLab behavior; otherwise local quantization as a labeled fallback. | Do not invent `/v2/quantize-image`. |
| Unzoom pixel art / remove upscaling | Aseprite or Pixelorama extension when the user is actively in that editor; otherwise local image tooling as a labeled fallback. | Do not invent `/v2/unzoom-pixelart`. |
| Pixel correction / clean-up | Visible Aseprite/editor workflow for exact PixelLab behavior, or closest documented REST edit/convert route after checking docs. | Do not invent `/v2/correct-pixelart`. |
| Reshape character proportions | Website/editor Reshape or closest documented edit/character route after verifying docs. | Website docs have fixed-size expectations; no public REST v2/MCP reshape route was documented. |
| Single-image Try on garment/accessory | Website Try on for a composited experimental output. | REST `transfer-outfit-v2` is animation-frame outfit transfer, not the same single-image try-on output and not isolated paperdoll layers. |

Do not expose, scrape, or automate browser/session tokens, extension-private request payloads, or first-party internal endpoints. If future official REST/MCP docs expose a matching public route, prefer the documented route and update this reference.
