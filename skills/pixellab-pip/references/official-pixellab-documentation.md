# Official PixelLab Documentation

Read this when a needed endpoint, tool, field, price, limit, SDK detail, or exact request/response schema is missing or unclear in the skill. Official docs can change after this skill ships; prefer the skill for routing and refresh docs only for the gap. Refresh triggers and the URL shortlist are in SKILL.md (Current Docs Refresh) — this file adds the annotated link table and the surface boundaries below.

## Links

| Link | Use for | Limits |
|---|---|---|
| `https://www.pixellab.ai/docs` | Human API guides and conceptual docs. | Not a complete machine-readable schema. |
| `https://api.pixellab.ai/v2/docs` | Interactive REST v2 API docs. | Good for exact endpoint parameters; less useful for high-level agent routing. |
| `https://api.pixellab.ai/v2/redoc` | REST v2 ReDoc reference pages linked from `llms.txt`. | Browseable operation docs; still use OpenAPI for machine-readable schemas. |
| `https://api.pixellab.ai/v2/llms.txt` | LLM-friendly REST v2 endpoint index and auth summary. | Curated index only; it intentionally points to OpenAPI/interactive docs for full endpoint parameters, enum values, and request/response shapes. |
| `https://api.pixellab.ai/v2/openapi.json` | Machine-readable REST v2 schema. | Requires parsing; current skill summarizes only stable routing. |
| `https://www.pixellab.ai/mcp` | Human Vibe Coding setup page for MCP clients. | Setup-oriented; its "Available Tools" list can be abbreviated and should not be treated as the full tool inventory. |
| `https://api.pixellab.ai/mcp` | Hosted MCP server URL. | This is a service endpoint, not documentation. Use through an MCP-capable client. |
| `https://api.pixellab.ai/mcp/docs` | LLM-readable MCP tool guide and authoritative public MCP tool inventory. | MCP tools are not REST endpoints; do not curl tool names. |
| `https://github.com/pixellab-code/pixellab-python` | Official Python SDK linked from `llms.txt`. | Check installed package/docs before assuming endpoint coverage. |
| `https://github.com/pixellab-code/pixellab-js` | Official JavaScript/TypeScript SDK linked from `llms.txt`. | Check installed package/docs before assuming endpoint coverage. |
| `https://github.com/pixellab-code/pixellab-mcp` | Official MCP server repository linked from `llms.txt`. | Hosted MCP tool availability can still vary by client/tool schema. |

## Authoritative MCP Inventory

- `https://api.pixellab.ai/mcp/docs` is the authoritative public MCP tool inventory. It explains available tools, non-blocking jobs, polling, downloads, and warns that MCP tools are not REST endpoints. Do not rely on the abbreviated "Available Tools" list at `https://www.pixellab.ai/mcp` to decide whether a current MCP tool exists.
- The MCP tool set can change between sessions as PixelLab ships server updates. A client's connected tool list can also lag a very recent server change until the client reconnects — if a documented tool is unexpectedly missing, do not conclude it was removed from a single stale check; note the discrepancy and prefer a fresh connection or `mcp/docs` before routing around it.
- An MCP-capable client may also expose `pixellab://docs/...` documentation resources (engine/framework guides such as Godot, Unity, Python, Wang tilesets, sidescroller tilesets, isometric tiles, and platform overview). Use those resources when visible; otherwise fall back to the public docs URLs above.

## Prompt Enhancement Pricing

`enhance-pixen-prompt`, `enhance-character-v3-prompt`, and `enhance-animation-v3-prompt` are public REST v2. A live check on 2026-06-25 returned `usage.generations: 0.05` with a matching balance delta for `enhance-pixen-prompt` — treat prompt enhancement as low-cost prompt prep, not a generation job. These are not root website/editor endpoints. Ask first for bulk or unusually cost-sensitive enhancement, and honor opt-out.

## Boundaries Beyond The Intent Router

SKILL.md's Intent Router already states MCP-vs-REST routing per asset type. These are the extra facts it does not:

- Beyond managed assets, MCP documents raw-image primitives needing no managed asset: `create_image_pixflux`/`create_image_pixen`/`create_image_pro` (+ `get_image` as their shared getter, matching REST `create-image-pixflux`/`create-image-pixen`/`generate-image-v2` on core fields — REST PixFlux additionally exposes deprecated `negative_description` and `background_removal_task`, REST Pixen exposes `enhance_prompt`, and Pro exposes no negative field; `create_image_pixflux` also covers `create-image-pixflux-background`, a byte-identical schema), `edit_image` (**Pro tier** — matches `edit-images-v2`, not base `edit-image`, which has `color_image`/`text_guidance_scale` that `edit_image` lacks), `inpaint_image` (**Pro tier** — matches `inpaint-v3`, which has `crop_to_mask` unique to v3, not base `inpaint`, whose extra weak-guidance controls `inpaint_image` can't reach: `direction`/`isometric`/`shading`/`outline`/`detail`/`text_guidance_scale`/`init_image`/`color_image`/`negative_description`), and `animate_image` (matches `animate-with-text-v3`, partially `interpolation-v2` via `last_frame_base64`; neither modern route exposes a negative field). Current REST v2 also exposes nondeprecated `negative_description` on `create-image-bitforge`, legacy `animate-with-text`, and base `inpaint`; no public MCP tool exposes it.
- MCP has no tool for REST `create-image-bitforge` (`coverage_percentage`), `generate-with-style-v2`, `generate-ui-v2`, base-tier `edit-image`/`inpaint`, `image-to-pixelart`(`-pro`), `resize`, `remove-background`, or `rotate` (single arbitrary rotation). Legacy `animate-with-text`/`-v2` (`reference_image` is a subject/style role, not a frame anchor) is only partially covered via managed `animate_character`/`animate_object` `mode="v3"`; `generate-8-rotations-v2` is only partially covered via `create_8_direction_object` (whose own tool docs warn identity transfer is unreliable for character sprites); `generate-8-rotations-v3` via `create_character(mode="v3", reference_image_base64=…)`, which does reproduce the input sprite but returns a managed character with animation padding, not raw rotations. Route the REST-only ones to REST v2; do not assume a REST endpoint has an MCP equivalent just because MCP is configured.
- MCP `create_map_object` may expose `background_image` or `inpainting` parameters. These are map-object generation controls, not generic replacements for REST v2 `inpaint`/`inpaint-v3`.
- MCP and REST versions of the same workflow (for example `create_ui_asset` vs `create-ui-asset`) are not guaranteed pixel-identical for the same prompt and seed; treat them as one workflow family with overlapping controls, while REST currently exposes the fuller documented schema. More generally, same-seed regeneration is not guaranteed to reproduce pixels exactly.
- Font and portrait-character conversion have dedicated Pro routes on both REST and MCP (see the Intent Router). Do not fall back to generic image/icon or text-to-character generation for them; portrait-to-character is an image-conversion workflow with `image` as the source input. Talking portraits, vocal-animation visemes, talking GIFs, and lip-sync plans also have dedicated routes; read `vocal-animation.md` rather than treating them as generic sprite animation.
- Aseprite extension operation names (observed: `generate-image-new`, `generate-pixelart-flux`, `generate-multi-edit`, `quantize-image`, `unzoom-pixelart`, `correct-pixelart`) are undocumented internal endpoints unless they appear in public REST v2/OpenAPI or MCP docs. Do not cite extension source filenames, source layout, source contents, or internal request payloads as public documentation. When an Aseprite workflow maps to a documented public route, use that route instead.
