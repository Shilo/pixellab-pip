# Prompt Limits

Read this when a PixelLab REST v2 call rejects a natural-language field for length, when writing exact API code, or when preparing unusually long prompts.

These limits were checked against `https://api.pixellab.ai/v2/openapi.json` on 2026-07-01. OpenAPI is the source of truth for exact current REST v2 schemas; refresh it when failures or exact code depend on current limits.

## Pattern

Do not globally cap every prompt at 500 characters. `maxLength` follows a rough tier by field kind:

- 2000 for most primary `description` fields.
- 1000 for the managed state/edit-description family: character/object state `edit_description` and object `animation_description`, and `animate-with-text-v3` `action`.
- 500 for the other raw-animation `action` fields, single-image edit descriptions, and some style/reference descriptions.
- 200 for some UI/font fields (`color_palette`, `font_name`).

## Non-Obvious Limits

These are the rows that do not follow the tier you would guess from the field name. Verify against OpenAPI before exact integrations.

| Endpoint | Field | Max chars |
|---|---|---:|
| `POST /animate-with-text-v2` | `action` | 500 |
| `POST /animate-with-text-v3` | `action` | 1000 |
| `POST /edit-image` | `description` | 500 |
| `POST /enhance-animation-v3-prompt` | `action` | 500 |
| `POST /generate-8-rotations-v2` | `style_description` | 500 |
| `POST /generate-image-v2` | `reference_images[].usage_description` | 500 |
| `POST /generate-image-v2` | `style_image.usage_description` | 500 |
| `POST /generate-with-style-v2` | `style_description` | 500 |
| `POST /interpolation-v2` | `action` | 500 |
| `POST /remove-background` | `text` | 500 |
| `POST /create-ui-asset` | `color_palette` | 200 |
| `POST /generate-ui-v2` | `color_palette` | 200 |
| `POST /generate-font-pro` | `font_name` | 200 |

## No Declared Max Length

Some REST v2 request schemas include natural-language string fields without a declared `maxLength` in OpenAPI, including older image, tileset, tile, base animation, and base inpaint routes (for example `create-image-pixen`/`pixflux`/`bitforge.description`, `create-isometric-tile.description`, `create-tiles-pro.description`, `create-tileset.*_description`, `create-tileset-sidescroller.*_description`, `animate-with-text.action`/`description`/`negative_description`, `inpaint.description`/`negative_description`). Do not infer that these are unlimited; keep them concise and refresh OpenAPI or interactive docs before exact integrations.

MCP tool schemas may expose different parameter descriptions or validation. When using visible MCP tools, follow the tool schema shown by the host and keep prompts concise unless the tool declares a larger limit.
