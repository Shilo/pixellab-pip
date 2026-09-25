# PixelLab Image-to-Text Research Spike

## Summary

`POST /v2/image-to-text` is an image-to-text utility, not a replacement for the three `enhance-*` prompt routes. Its default mode reads one image and returns a short, general image-generation prompt; its optional `prompt` asks PixelLab to answer a caller-written question about that image. The Pixen and character enhancers instead rewrite caller-supplied text for a named generation route. The animation enhancer is the closest counterexample: it also takes image context, but requires an action and returns target-specific motion text for an animation route. **Verdict: the overlap is real at the broad “use image content to produce useful words” level, but the documented API contracts are not redundant.**

The endpoint is useful when an agent needs PixelLab to describe an image it cannot otherwise inspect, or needs PixelLab's own image-conditioned caption/answer. Skip it when the image is already visually available to the agent, when the task is only to improve text for one known route, when structured pixel-art inspection is needed from MCP Workbench, or when the user wants the image converted rather than described. The added call may be unnecessary overhead in those cases.

Checked against the current PixelLab sources on **2026-09-25**. No paid endpoint call was made for this research.

## What The Endpoint Does

The current REST OpenAPI describes two modes:

- **Describe (default):** send an image and omit `prompt`. PixelLab returns a 1–3 sentence generation prompt covering visible subject, pose, notable details, style, lighting, camera angle, and background. The stated purpose is to paste it into a create endpoint's `description` field.
- **Ask:** send an image and a custom `prompt` with an instruction or question. This replaces the default instruction, so the caller must include any desired focus, length, or format.

The endpoint accepts one required PNG/JPEG image as base64 or a data URI, up to 4096×4096. The optional custom `prompt` is 1–2000 characters. It returns a `text` string plus optional `usage`, in a synchronous `200` response. It does not generate an image or return a background job ID. PixelLab documents `401` for an invalid token, `402` for insufficient credits, `422` for validation/unreadable/oversized images, and `503` for a temporary upstream failure. PixelLab says small pixel art is enlarged with whole-number nearest-neighbour scaling before analysis and transparency is communicated to the model, so transparent sprites should be described as transparent rather than against white. The default instruction also says to avoid speculation about sensitive attributes. [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) · [Image-to-text operation](https://api.pixellab.ai/v2/redoc#operation/image_to_text_endpoint_image_to_text_post)

The default caption is deliberately **general-purpose**. The schema has no target model, output size, view, direction, outline, or detail controls. A returned caption can be used as text for a downstream generation call, but the API does not promise that it is optimized for Pixen, Character v3, or a particular animation model.

## Comparison With Prompt Enhancers

| Route | What goes in | What comes out | Image-conditioned? | Documented target |
|---|---|---|---|---|
| `POST /v2/image-to-text` | One image; optional question/instruction | General image prompt or answer text | Yes | No single route; default text is suitable for a create endpoint's `description` |
| `POST /v2/enhance-pixen-prompt` | User's text description, required output size, optional Pixen style/view/direction/background controls | `enhanced_prompt` | No image field | `/v2/create-image-pixen` |
| `POST /v2/enhance-character-v3-prompt` | User's text description, required output size, optional view/outline/detail | `enhanced_prompt` | No image field | `/v2/create-character-v3` |
| `POST /v2/enhance-animation-v3-prompt` | Required first frame and action; optional last frame, engine, direction, and frame count | `enhanced_prompt` describing motion | Yes | Text animation v3 by default; supports PixMiniMax and Skeleton v3 engine-specific action wording |

The Pixen enhancer expands text while respecting size, outline, detail, view, direction, and background settings. The character-v3 enhancer expands text for that character route; PixelLab says its output does not mention facing direction because v3 rotates the south-facing image into eight directions, and does not describe a background because the route renders transparent. Neither accepts the source image itself.

The animation enhancer is the closest overlap and deserves a careful distinction. It receives the animation's first frame plus the caller's requested action, and can optionally receive a last frame for interpolation. PixelLab says it grounds the requested motion in visible pose, props, orientation, and clothing, and avoids introducing new objects or camera changes unless requested. It does **not** return a general caption or arbitrary visual Q&A; it returns an action description intended for an animation endpoint. In other words, image-to-text asks “what is in this image, or what do I want to know about it?”, while the animation enhancer asks “given this frame and this requested action, what motion prompt fits the animation route?” [Pixen enhancer](https://api.pixellab.ai/v2/redoc#operation/enhance_pixen_prompt_enhance_pixen_prompt_post) · [Character v3 enhancer](https://api.pixellab.ai/v2/redoc#operation/enhance_character_v3_prompt_enhance_character_v3_prompt_post) · [Animation enhancer](https://api.pixellab.ai/v2/redoc#operation/enhance_animation_v3_prompt_enhance_animation_v3_prompt_post)

### Verdict On Redundancy

The criticism is partly right: all four routes can yield useful text related to visual generation, and the image-to-text default can be followed by an enhancer. That makes image-to-text optional in a generation pipeline, not a required preparation step. Its broader question mode and general image-to-prompt output are distinct from the three enhancers' narrow text-rewriting contracts. The image-aware animation enhancer overlaps most in its use of visual evidence, but its action input and motion-specific output make it a different operation.

This is a contract-level conclusion, not a measured quality comparison. The current docs do not publish comparative accuracy, model identity, or benchmark results for image-to-text versus an agent's own vision model or the enhancers.

## MCP And Workbench Comparison

The current public MCP tool guide has no `image_to_text` tool and documents none of the three REST `enhance-*` routes as MCP tools. MCP `agent_help` and `search_knowledge` answer questions about PixelLab's tools and documentation; they do not accept a source image for visual Q&A. [MCP tool guide](https://api.pixellab.ai/mcp/docs)

`pixelart_workbench` is the closest MCP-side adjacent capability, not a one-for-one equivalent. Its tool contract accepts an image reference and its commands can inspect or analyze pixel art: `inspect` returns frame sheets or exact-color crops; `score` reports pixel-art discipline; `extract-palette` proposes colors and ramps; `lint`, `measure`, `clusters`, `silhouette`, and `motion` report specialized findings. Those outputs serve concrete pixel-art review and editing workflows. The documented command list does not offer a generic “describe this image as a generation prompt” or arbitrary image-question endpoint. This command distinction was checked through the live, read-only Workbench `describe cli` and command help on 2026-09-25; the public MCP guide describes Workbench as a tool that checks, explains, and improves drawings. [MCP tool guide](https://api.pixellab.ai/mcp/docs)

If the caller's own model can already inspect the image, that model can write a caption or answer without calling image-to-text. That is an inference about agent workflow, not a claim that all host models have vision access or match PixelLab's results. The REST route's remaining value is a PixelLab-hosted image-to-text pass with a documented prompt format and metered `usage`.

## Cost And Practical Tradeoffs

The current OpenAPI describes image-to-text as typically about **0.09 generations** for a sprite or screenshot, with higher cost for longer answers; the exact amount is returned in `usage`. This is an estimate, not a fixed tariff. The public PixelLab API catalog currently lists the three prompt enhancers at **$0.002 per call**. A prior recorded live check in this repository observed `usage.generations: 0.05` for `enhance-pixen-prompt` only; it did not establish that value for all enhancers or recheck it on this date. These are different reporting units and sources, so do not treat `0.09` and `$0.002` (or the historical `0.05`) as a direct price comparison. For an actual call, prefer its returned `usage`; for an estimate, confirm the current account's billing view. [REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) · [PixelLab API pricing catalog](https://www.pixellab.ai/pixellab-api) · [Prior enhancer observation](../../skills/pixellab-pip/references/official-pixellab-documentation.md#prompt-enhancement-pricing)

Calling image-to-text and then an enhancer spends for both operations. That chain is reasonable when the source image is the source of truth and a route-specific version is still needed, but the current docs do not say the chain reliably improves image quality. Keep it to one route-specific enhancer at most, and skip that too if PixelLab-ready wording can be produced directly or the user opts out.

## Route-Selection Examples

| Need | Better route | Why |
|---|---|---|
| “I have this sprite but don't know how to describe it. Give me a short prompt I can reuse.” | `image-to-text` | The input is an image and the output is a general prompt. Use the default mode. |
| “What colors are used, where are the pixels, and which outline gaps are wrong?” | MCP Workbench `extract-palette`, `measure`, or `lint` | The need is pixel-specific evidence; use the structured command for that question. |
| “Make my text prompt stronger for a 64×64 transparent Pixen icon.” | `enhance-pixen-prompt` | This is text-in, route-specific prompt preparation; image-to-text would needlessly require an image. |
| “Improve this character description for Character v3.” | `enhance-character-v3-prompt` | The target is a specific character route, and the enhancer's fields match it. |
| “Animate this frame as a sword swing; keep the current character's facing.” | `enhance-animation-v3-prompt` or `/animate-pixminimax` with its inline `enhance_prompt: true` option | The requested action and frame are known; use the motion-specific enhancer rather than first captioning the image. |
| “Tell me what is in this screenshot / answer a question about this sprite.” | `image-to-text` with a self-contained `prompt`, if PixelLab's answer is needed | Custom visual Q&A is the distinctive documented mode among the compared REST routes. |
| “Convert this source image into pixel art.” | REST `image-to-pixelart` or MCP `image_to_pixelart` | This transforms the image; image-to-text would only return words. |
| “The agent can already see the image and just needs a concise generation prompt.” | Usually skip PixelLab image-to-text | The host model can inspect and describe it directly; call PixelLab only if a vendor-side answer or its cost/behavior is specifically desired. |

When asking a custom question, give a clear format and scope, and remember that it fully replaces the default instruction. Treat free-form answers as model-generated descriptions, not measured pixel facts. For objective palette, geometry, or animation diagnostics, use Workbench commands where available and verify the evidence they return.

## Evidence And Limitations

- **REST contract facts:** current OpenAPI defines the request/response fields, accepted image type/size, synchronous response and error codes, default/ask modes, image preprocessing notes, and variable typical cost. The endpoint is not marked deprecated in that spec.
- **MCP facts and live observation:** the public MCP guide lists no image-to-text or prompt-enhancer equivalent. Workbench's relevant command names and help text were checked with non-mutating `describe`/`-h` calls.
- **Product pricing fact:** the public API catalog lists $0.002 per call for each of the three enhancers. Its visible catalog does not list the image-to-text route; the current cost description for that endpoint is in OpenAPI.
- **Inference:** an open-ended answer can omit or misidentify details; the response is a model-generated text string without a structured confidence or pixel-coordinate schema. For high-stakes or exact visual facts, independently inspect the image or use a specialist tool.
- **Unverified:** no live paid image-to-text/enhancer request was made, and no model provider, retention period, quality benchmark, or comparison against host-model vision is specified in the sources checked.

## Sources

Checked 2026-09-25:

- [PixelLab REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json) — authoritative request/response schema and the most complete current descriptions.
- [PixelLab REST v2 machine-readable endpoint index](https://api.pixellab.ai/v2/llms.txt) — confirms the four operations are distinct public REST endpoints.
- [Image-to-text operation](https://api.pixellab.ai/v2/redoc#operation/image_to_text_endpoint_image_to_text_post).
- [Enhance Pixen prompt](https://api.pixellab.ai/v2/redoc#operation/enhance_pixen_prompt_enhance_pixen_prompt_post).
- [Enhance Character v3 prompt](https://api.pixellab.ai/v2/redoc#operation/enhance_character_v3_prompt_enhance_character_v3_prompt_post).
- [Enhance animation v3 prompt](https://api.pixellab.ai/v2/redoc#operation/enhance_animation_v3_prompt_enhance_animation_v3_prompt_post).
- [PixelLab MCP tool guide](https://api.pixellab.ai/mcp/docs) — MCP tools and Workbench contract.
- [PixelLab API pricing catalog](https://www.pixellab.ai/pixellab-api) — public USD estimates for the prompt enhancers.
- [Repository's prior enhancer pricing observation](../../skills/pixellab-pip/references/official-pixellab-documentation.md#prompt-enhancement-pricing) — a dated live check of `enhance-pixen-prompt`, not a current universal price contract.

The MCP documentation assistant returned no endpoint details when queried about these REST routes and pointed to the REST `llms.txt` index. The OpenAPI and REST docs were used as the endpoint authority; the MCP answer was treated only as evidence that MCP help does not currently explain this REST family.
