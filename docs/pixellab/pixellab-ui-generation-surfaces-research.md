# PixelLab UI generation surfaces research

Generated at UTC: 2026-06-28T11:04:28Z

Scope: focused research on PixelLab UI generation after an outdated routing claim that shape pieces were not available through public API or MCP surfaces. Sources were current official REST v2 OpenAPI, current MCP docs, the active MCP tool schema exposed through an MCP-capable agent host, and existing repository research. No credit-spending generation was run.

## Verdict

The previous shape-piece limitation is outdated for the current public surface.

- REST v2 `POST /create-ui-asset` supports shape pieces through `pieces`.
- MCP `create_ui_asset` also supports `pieces` when the tool is exposed by the agent host.
- REST v2 `POST /generate-ui-v2` does not support shape pieces; it is the simpler freeform UI image generator.

For an agent skill that can choose either MCP or REST, prefer REST `POST /create-ui-asset` for structured UI assets when REST calls are available. Use MCP `create_ui_asset` when the user is already working through MCP and the request only needs the overlapping fields. These two routes appear to target the same UI asset workflow family, but they should not be treated as perfectly identical contracts: REST currently exposes more fields and the exact OpenAPI schema.

The practical split is:

| Option | Surface | Shape pieces? | Best use |
|---|---|---:|---|
| 1 | REST `POST /create-ui-asset` | Yes | Best default for an agent skill that can call either surface; most complete structured UI asset endpoint. |
| 2 | MCP `create_ui_asset` | Yes | Convenient managed-asset route for MCP-first agent workflows using overlapping fields. |
| 3 | REST `POST /generate-ui-v2` | No | Raw UI element/image generation from text, with optional concept-image guidance. |

Website/UI Creator is a fourth, human/editor surface. It can expose UI library, presets, and editor workflows, but internal website routes should not be treated as public automation unless they appear in REST OpenAPI or MCP docs.

## Sources

| Source | What it proves |
|---|---|
| `https://api.pixellab.ai/v2/openapi.json` | Exact REST endpoint inventory, request fields, response fields, shape-piece schemas, and lifecycle endpoints. |
| `https://api.pixellab.ai/v2/docs` | Interactive REST docs backed by the OpenAPI schema. |
| `https://api.pixellab.ai/mcp/docs` | Current MCP docs, including `create_ui_asset`, `get_ui_asset`, `list_ui_assets`, and `delete_ui_asset`. |
| Active MCP tool schema for `create_ui_asset` | Confirms the exposed MCP tool accepts typed `pieces` and lists the supported piece object shapes. |
| Existing repository website/editor research | Historical context for UI Creator, UI library, shape presets, and why undocumented website routes are treated as editor/internal surfaces. |

## Option 1: MCP `create_ui_asset`

Current MCP docs describe `create_ui_asset` as:

- Queues a pixel-art UI panel.
- Returns a `ui_asset_id` immediately.
- Omits `pieces` for a default rounded-rect panel.
- Uses `get_ui_asset` to check status.

Current MCP fields from the live tool schema:

| Field | Meaning |
|---|---|
| `description` | Required style prompt, e.g. wooden RPG panel with gold trim. |
| `width`, `height` | Output size in px. Live schema says 192-688, with aspect-dependent max. |
| `color_palette` | Optional text palette hint, e.g. `brown and gold`. |
| `no_background` | Remove background after generation. |
| `seed` | Reproducibility control. |
| `name` | Friendly saved asset name. |
| `elements` | Named scaffold elements such as `button`, `icon_button`, `toolbar`, `tab`, `panel`, `window`, `health_bar`, `avatar`, `triangle`, `pentagon`, `hexagon`, `octagon`. |
| `pieces` | Advanced shape template. Supports `rounded_rect`, `circle`, and `polygon` objects. |

MCP lifecycle tools:

- `get_ui_asset(ui_asset_id, include_preview?)`
- `list_ui_assets(limit?, offset?)`
- `delete_ui_asset(ui_asset_id, confirm?)`

MCP gaps relative to REST `POST /create-ui-asset`:

- Current MCP schema does not expose `style_image`.
- Current MCP schema does not expose `project_id`.
- MCP docs list `pieces` but do not describe the piece schema in detail; the live tool schema and REST OpenAPI do.

Use MCP when the agent is already working through PixelLab MCP and the request can be satisfied by the overlapping fields. It is the convenient route, not the most complete route.

## Option 2: REST `POST /create-ui-asset`

This is the structured UI asset endpoint. It is the clearest public API answer to "can I shape pieces?"

OpenAPI summary: `Create UI panel (Pro)`.

Request fields:

| Field | Required | Notes |
|---|---:|---|
| `description` | Yes | Style description for the UI panel. |
| `image_size` | No | Output size, 192-688 px with aspect-dependent max. |
| `pieces` | No | Validated shape template; defaults to a full-canvas rounded-rect panel when omitted. |
| `elements` | No | Auto-positioned named UI element types; can combine with `pieces`. |
| `style_image` | No | Optional PNG/JPEG base64 style reference. |
| `color_palette` | No | Optional text palette hint. |
| `no_background` | No | Default `true`. |
| `seed` | No | Reproducibility control. |
| `name` | No | Friendly saved asset name. |
| `project_id` | No | Assigns finished asset to a project when set. |

Response fields:

| Field | Meaning |
|---|---|
| `background_job_id` | Background job ID for polling status. |
| `ui_asset_id` | UI asset ID available immediately; poll the asset until ready. |
| `status` | Defaults to `processing`. |
| `usage` | Usage object when exposed. |

Lifecycle endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /ui-assets/{ui_asset_id}` | Get status/detail. Completed assets expose `image_url`. |
| `GET /ui-assets` | List UI assets with pagination. |
| `DELETE /ui-assets/{ui_asset_id}` | Delete a UI asset. |
| `GET /background-jobs/{job_id}` | Generic background job status. Useful because the create response includes `background_job_id`. |

Use REST `create-ui-asset` as the default structured UI route for an agent skill that can call either MCP or REST. It has the most complete documented control surface, including `style_image`, `project_id`, exact request/response schemas, and standard REST polling.

## Option 3: REST `POST /generate-ui-v2`

This is the simpler raw UI generation endpoint.

OpenAPI summary: `Generate UI (Pro)`.

Request fields:

| Field | Required | Notes |
|---|---:|---|
| `description` | Yes | Description of the UI element to generate, e.g. `medieval stone button`, `sci-fi health bar`. |
| `image_size` | No | Output image size, 16 px minimum with aspect-ratio max. |
| `seed` | No | Reproducibility control. |
| `no_background` | No | Default `true`. |
| `concept_image` | No | Optional concept image to guide the UI design. |
| `color_palette` | No | Optional text palette hint. |

Response fields:

| Field | Meaning |
|---|---|
| `background_job_id` | Poll `GET /background-jobs/{job_id}`. |
| `status` | Defaults to `processing`. |
| `usage` | Usage object when exposed. |

Use `generate-ui-v2` for loose UI image generation: buttons, bars, panels, slots, dialogue boxes, and other interface components where a text prompt plus optional concept image is enough.

Do not use `generate-ui-v2` when the requirement is "place these exact shapes." It has no `pieces` or `elements` field.

## Shape pieces

REST `CreateUIAssetRequest.pieces` and the active MCP tool schema both support the same conceptual shape template. The REST docs describe a virtual editor coordinate space:

- The longer side spans `0-512`.
- The shorter side is aspect-scaled.
- A 16:9 panel uses a `512x288` coordinate grid.
- Coordinates are not output pixels; they are editor-space coordinates.

Supported piece kinds:

```json
[
  {
    "id": "main_panel",
    "kind": "rounded_rect",
    "label": "Main panel",
    "x": 24,
    "y": 24,
    "w": 464,
    "h": 240,
    "radius": 16
  },
  {
    "id": "portrait",
    "kind": "circle",
    "label": "Avatar frame",
    "x": 84,
    "y": 144,
    "r": 48
  },
  {
    "id": "badge",
    "kind": "polygon",
    "label": "Hex badge",
    "x": 430,
    "y": 64,
    "r": 28,
    "sides": 6,
    "phase": 0
  }
]
```

REST schema names:

| Schema | Required fields |
|---|---|
| `UiPieceRect` | `id`, `kind`, `x`, `y`, `w`, `h`; optional `label`, `radius`. |
| `UiPieceCircle` | `id`, `kind`, `x`, `y`, `r`; optional `label`. |
| `UiPiecePolygon` | `id`, `kind`, `x`, `y`, `r`, `sides`; optional `label`, `phase`. |

In the active MCP schema, the rectangle kind is named `rounded_rect`. The REST field description also says allowed kinds include `rounded_rect`. Use `rounded_rect`, `circle`, and `polygon`.

## Elements

`elements` is a higher-level scaffold list. Current documented values:

- `button`
- `icon_button`
- `toolbar`
- `tab`
- `panel`
- `window`
- `health_bar`
- `avatar`
- `triangle`
- `pentagon`
- `hexagon`
- `octagon`

Use `elements` when rough structure is enough. Use `pieces` when layout geometry matters. Combine both when a known UI type needs custom shape guidance.

## Feature matrix

| Capability | REST `/create-ui-asset` | MCP `create_ui_asset` | REST `/generate-ui-v2` |
|---|---:|---:|---:|
| Text prompt | Yes | Yes | Yes |
| Saved UI asset ID | Yes | Yes | No documented `ui_asset_id`; returns background job. |
| Poll asset by UI asset ID | Yes, `GET /ui-assets/{id}` | Yes, `get_ui_asset` | No, poll background job. |
| List saved UI assets | Yes | Yes | Not applicable. |
| Delete saved UI assets | Yes | Yes | Not applicable. |
| Shape `pieces` | Yes | Yes | No |
| Named `elements` | Yes | Yes | No |
| Default full-panel shape | Yes | Yes | No |
| `style_image` | Yes | Not in current MCP schema | No |
| `concept_image` | No | No | Yes |
| `color_palette` text hint | Yes | Yes | Yes |
| `seed` | Yes | Yes | Yes |
| `no_background` | Yes | Yes | Yes |
| `name` | Yes | Yes | No |
| `project_id` | Yes | Not in current MCP schema | No |
| Small raw UI element generation | Possible, but structured-panel oriented | Possible, but structured-panel oriented | Best fit |
| Exact API/server integration | Best fit | Possible only through MCP host | Best fit for raw generation |

## Behavior and selection rule

REST `POST /create-ui-asset` and MCP `create_ui_asset` should be treated as the same UI asset workflow family, not as identical APIs.

Use REST `POST /create-ui-asset` as the better default when an agent skill can call both because:

- REST exposes the fuller documented field set: `pieces`, `elements`, `style_image`, `color_palette`, `no_background`, `seed`, `name`, and `project_id`.
- REST has explicit OpenAPI request and response schemas.
- REST integrates cleanly into backend code, batch scripts, tests, and logs.
- REST gives both `background_job_id` and `ui_asset_id`, with documented asset polling through `GET /ui-assets/{ui_asset_id}`.

Use MCP `create_ui_asset` when:

- The user is explicitly working in an MCP/vibe-coding agent context.
- The request only needs overlapping controls such as `description`, size, `pieces`, `elements`, `color_palette`, `no_background`, `seed`, and `name`.
- The agent benefits from MCP-managed tool calls and resource helpers instead of writing REST request code.

Do not assume pixel-identical results between MCP and REST for the same prompt and seed unless that has been verified by a live generation. Public docs show overlapping controls, not an identity guarantee.

## Website/UI Creator boundary

Existing website research shows a PixelLab `/create-ui` page, UI asset library labels, UI shape presets, and internal website routes such as UI asset generation and shape-preset CRUD. Treat these as website/editor implementation details, not public automation contracts.

Use the website when a human wants to visually design UI, browse libraries, or use editor-only workflows. Use REST/MCP when an agent or backend needs supported automation.

## Guidance for agents

When a user asks whether UI shapes can be controlled:

1. Say yes, through `create_ui_asset` or REST `/create-ui-asset`.
2. Do not route shape-piece requests to `/generate-ui-v2`.
3. Prefer REST `/create-ui-asset` by default when the agent can call both MCP and REST for structured UI assets.
4. Prefer MCP `create_ui_asset` when the user is in an MCP-first workflow and the request does not need REST-only fields such as `style_image` or `project_id`.
5. Treat website/editor endpoints as manual/editor surfaces unless official REST/MCP docs expose the same capability.

## Superseded documentation notes

Older repository docs may contain now-superseded statements such as "No direct hosted MCP UI tool found" or "no public layout-template endpoint found." As of this research pass, current MCP exposes `create_ui_asset`, and current REST OpenAPI exposes `/create-ui-asset` with `pieces`.

Keep older generated research docs as historical snapshots unless updating their generated date/scope. For current routing, this file should supersede older UI gap notes.

## Open questions

- Whether the generated UI asset preserves separate piece metadata for downstream editing is not established by the public response schema; `UIAssetDetail` exposes asset metadata and `image_url`, not a full editable piece graph.
- Exact credit cost for each UI option was not verified in a live generation.
- The current MCP docs list `pieces` but do not print the full shape schema; agent hosts should inspect the active MCP tool schema before constructing complex piece payloads.
