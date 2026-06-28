# Prompt Limits

Read this when a PixelLab REST v2 call rejects a natural-language field for length, when writing exact API code, or when preparing unusually long prompts.

These limits were checked against `https://api.pixellab.ai/v2/openapi.json` on 2026-06-28. OpenAPI is the source of truth for exact current REST v2 schemas; refresh it when failures or exact code depend on current limits.

## Rule

Keep natural-language fields concise and within the endpoint's documented `maxLength`.

Do not globally cap every prompt at 500 characters. The common pattern is:

- 2000 characters for many primary `description` fields.
- 1000 characters for managed character/object state edit descriptions and object animation descriptions.
- 500 characters for raw animation `action` fields, single-image edit descriptions, some style/reference descriptions, and remove-background text.
- 200 characters for UI `color_palette` fields such as `generate-ui-v2.color_palette` and `create-ui-asset.color_palette`.

If a call fails because a natural-language field is too long, trim that field without changing intent, mention the trim, and retry the same route.

## Documented REST v2 Limits

| Endpoint | Field | Max chars |
|---|---|---:|
| `POST /animate-with-text-v2` | `action` | 500 |
| `POST /animate-with-text-v3` | `action` | 500 |
| `POST /animate-character` | `description` | 2000 |
| `POST /characters/animations` | `description` | 2000 |
| `POST /create-1-direction-object` | `description` | 2000 |
| `POST /create-8-direction-object` | `description` | 2000 |
| `POST /create-character-pro` | `description` | 2000 |
| `POST /create-character-pro` | `style_description` | 2000 |
| `POST /create-character-state` | `edit_description` | 1000 |
| `POST /create-character-v3` | `description` | 2000 |
| `POST /create-character-with-4-directions` | `description` | 2000 |
| `POST /create-character-with-8-directions` | `description` | 2000 |
| `POST /create-ui-asset` | `color_palette` | 200 |
| `POST /create-ui-asset` | `description` | 2000 |
| `POST /edit-animation-v2` | `description` | 2000 |
| `POST /edit-image` | `description` | 500 |
| `POST /edit-images-v2` | `description` | 2000 |
| `POST /enhance-animation-v3-prompt` | `action` | 500 |
| `POST /enhance-character-v3-prompt` | `description` | 2000 |
| `POST /enhance-pixen-prompt` | `description` | 2000 |
| `POST /generate-8-rotations-v2` | `description` | 2000 |
| `POST /generate-8-rotations-v2` | `style_description` | 500 |
| `POST /generate-image-v2` | `description` | 2000 |
| `POST /generate-image-v2` | `reference_images[].usage_description` | 500 |
| `POST /generate-ui-v2` | `color_palette` | 200 |
| `POST /generate-ui-v2` | `description` | 2000 |
| `POST /generate-with-style-v2` | `description` | 2000 |
| `POST /generate-with-style-v2` | `style_description` | 500 |
| `POST /image-to-pixelart-pro` | `description` | 2000 |
| `POST /inpaint-v3` | `description` | 2000 |
| `POST /interpolation-v2` | `action` | 500 |
| `POST /map-objects` | `description` | 2000 |
| `POST /objects/{object_id}/animations` | `animation_description` | 1000 |
| `POST /objects/{object_id}/states` | `edit_description` | 1000 |
| `POST /remove-background` | `text` | 500 |
| `POST /resize` | `description` | 2000 |
| `POST /transfer-outfit-v2` | `additional_instructions` | 2000 |

## No Declared Max Length

Some REST v2 request schemas include natural-language string fields without a declared `maxLength` in OpenAPI, including older image, tileset, tile, base animation, and base inpaint routes. Do not infer that these are unlimited; keep them concise and refresh OpenAPI or interactive docs before exact integrations.

Prompt-like fields without a declared `maxLength` include:

- `create-image-pixen.description`
- `create-image-pixflux.description`
- `create-image-bitforge.description`
- `create-isometric-tile.description`
- `create-tiles-pro.description`
- `create-tileset.lower_description`, `upper_description`, and `transition_description`
- `create-tileset-sidescroller.lower_description` and `transition_description`
- `animate-with-text.action`, `description`, and `negative_description`
- `inpaint.description` and `negative_description`

MCP tool schemas may expose different parameter descriptions or validation. When using visible MCP tools, follow the tool schema shown by the host and keep prompts concise unless the tool declares a larger limit.
