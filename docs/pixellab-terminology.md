# PixelLab Terminology

Last reviewed: 2026-06-23.

PixelLab product labels, endpoint names, editor labels, and SDK method names can use related but different terms. Pip should map the user's plain-language request to the concrete documented surface instead of treating labels as universal model selectors.

## Product And Endpoint Labels

| Term | Public handling |
|---|---|
| `Pro` | Treat as a product/mode label scoped to a specific tool or endpoint. Do not treat it as one global model. |
| `v3` | Treat as a workflow/version label scoped to endpoints such as character creation, animation, rotation, or inpainting. |
| `new` | Treat as a UI or workflow label. Map to the concrete endpoint/tool before giving technical advice. |
| `Pixen` | Public image-generation product/endpoint label. Verify exact endpoint fields in REST v2 docs. |
| `PixFlux` | Public image/background-generation product/endpoint label. Verify exact endpoint fields in REST v2 docs. |
| `BitForge` | Public image-generation product/endpoint label. Verify exact endpoint fields in REST v2 docs. |
| `S-XL`, `M-XL`, `S-M`, `M-L` | User-facing size/tool labels. Do not use them as standalone technical route selectors. |
| `create tiles` | Usually individual tile variants or tile-pro workflows. Clarify when the user might mean a full terrain tileset. |
| `create tileset` | Usually terrain/platformer tileset workflows. Clarify when the user might mean individual tile variants. |
| `map` | Could mean a generated map image, map object, tilemap, terrain tileset, or website Map Workshop project. Ask only when context is insufficient. |
| `object` vs `character` | Infer character for people, NPCs, creatures, body templates, or identity/state animation. Infer object for props, items, furniture, and weapons. |

## Provider Claims

Do not infer provider identity, proprietary model details, or backend ownership from product labels. If PixelLab public REST/MCP docs do not disclose a provider or backend model, say that the provider is not disclosed in the public docs.

## Recommended Agent Behavior

- Classify the asset intent first.
- Choose MCP, REST v2, or a visible editor workflow second.
- Refresh official docs before exact schema, enum, pricing, model/mode, or SDK claims.
- Avoid repeating internal or observed website strings as official API terminology unless PixelLab documents them publicly.
