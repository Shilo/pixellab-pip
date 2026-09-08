# Editor-Only Utilities

Read this when the user wants an exact PixelLab editor utility that has no documented public REST v2 or MCP route. Map each request to the closest public route or a clearly labeled non-PixelLab local fallback; the routing boundary and the "do not invent `/v2/...` routes" rule are stated in SKILL.md.

Reduce colors, unzoom, and pixel correction are not in this file: they have public REST v2 endpoints and MCP tools. Route them from SKILL.md's cleanup row.

| User wording | Route | Warning |
|---|---|---|
| Canny, sketch-guided, pose-guided, depth/image-to-image | Visible website/editor/Aseprite flow for exact behavior; REST v2 only for approximate documented init/reference/skeleton workflows after explaining the difference. | No exact public REST v2/MCP Canny/Pose/Depth route was documented. Do not call internal editor operation URLs. |
| Reshape character proportions | Website/editor Reshape, or closest documented edit/character route after verifying docs. | Website docs have fixed-size expectations; no public REST v2/MCP reshape route was documented. |
| Single-image Try on garment/accessory | Website Try on for a composited experimental output. | REST `transfer-outfit-v2` is animation-frame outfit transfer, not the same single-image try-on output and not isolated paperdoll layers. |

If future official REST/MCP docs expose a matching public route, prefer the documented route and update this reference.
