# PixelLab Terminology

Last reviewed: 2026-09-13.

Purpose: prevent agents from over-interpreting PixelLab labels such as `Pro`, `v3`, `new`, `Pixen`, `PixFlux`, `BitForge`, `tiles`, and `tileset`.

PixelLab product labels, endpoint names, editor labels, and SDK method names can use related but different terms. Pip should map the user's plain-language request to the concrete documented surface instead of treating labels as universal model selectors.

## Product And Endpoint Labels

| Term | Public handling |
|---|---|
| `Pro` | Treat as a product/mode label scoped to a specific tool or endpoint. Do not treat it as one global model. |
| `Pro Flash` | A separate beta image/character/object/edit/inpaint family, not a faster alias for the older Pro endpoints. The single-image option is advertised at 4–6 generations with a maximum size of `256x256`; current REST describes a provisional five-generation first-image estimate. Creation gives one image; character views are always eight. Its speed, visual quality, and price advantage have not been independently tested here. |
| `v3` | Treat as a workflow/version label scoped to endpoints such as character creation, animation, rotation, or inpainting. |
| `new` | Treat as a UI or workflow label. Map to the concrete endpoint/tool before giving technical advice. |
| `Pixen` | Public image-generation product/endpoint label. Verify exact endpoint fields in REST v2 docs. |
| `PixFlux` | Public image/background-generation product/endpoint label. Verify exact endpoint fields in REST v2 docs. |
| `PixMiniMax` | PixelLab's public raw-animation product label for REST `/animate-pixminimax` and MCP `animate_image_pixminimax`; the REST operation says it is powered by MiniMax H3 and is available to Tier 1+ subscribers. Version 0.4.123 also surfaces it in Character Creator, Creator, Aseprite, and Pixelorama. This wrapper is not the full standalone H3 prompt or audio contract. |
| `BitForge` | Public image-generation product/endpoint label. Verify exact endpoint fields in REST v2 docs. |
| `S-XL`, `M-XL`, `S-M`, `M-L` | User-facing size/tool labels. Do not use them as standalone technical route selectors. |
| `create tiles` | Usually individual tile variants or tile-pro workflows. Clarify when the user might mean a full terrain tileset. |
| `create tileset` | Usually terrain/platformer tileset workflows. Clarify when the user might mean individual tile variants. |
| `map` | Could mean a generated map image, map object, tilemap, terrain tileset, an MCP-managed tile map (`create_map`/`edit_map`/`view_map`), or a website Map Workshop project. Map Workshop also exports for Godot and Unity. Ask only when context is insufficient. |
| `Game Builder` | A Tier 1+ first-party product workflow. Keep it separate from the public REST v2 API: visible Game Builder may use project/chat/sandbox context, but no dedicated public REST Game Builder endpoint is documented. |
| `object` vs `character` | Infer character for people, NPCs, creatures, body templates, or identity/state animation. Infer object for props, items, furniture, and weapons. |

## Provider Claims

Do not infer provider identity, proprietary model details, or backend ownership from product labels. PixelLab's current public REST description specifically discloses MiniMax H3 for `animate-pixminimax`; scope that claim to the operation and do not generalize it to other PixelLab routes or to undocumented editor operations. If PixelLab public REST/MCP docs do not disclose a provider or backend model, say that the provider is not disclosed in the public docs.

## Recommended Agent Behavior

- Classify the asset intent first.
- Choose MCP, REST v2, or a visible editor workflow second.
- Refresh official docs before exact schema, enum, pricing, model/mode, or SDK claims.
- Avoid repeating internal or observed website strings as official API terminology unless they appear in PixelLab's public REST v2 docs/OpenAPI or MCP docs as supported programmatic endpoints/tools.
