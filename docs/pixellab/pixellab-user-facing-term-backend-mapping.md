# PixelLab User-Facing Term To Backend Mapping

Last reviewed: 2026-06-26.

Purpose: map PixelLab user-facing labels to backend surfaces without treating website, editor, or Aseprite integration routes as public API contracts. This production reference is intentionally conservative: public means documented in REST v2 OpenAPI/llms/API pages or MCP docs; observed means visible in first-party website/editor surfaces or Aseprite source and is used only for terminology/surface awareness; inferred means the capability matches but the exact backend branch is not exposed.

## Sources Inspected

Official web and docs:

- `https://www.pixellab.ai/pixellab-api`
- `https://www.pixellab.ai/editor`
- `https://www.pixellab.ai/docs`
- `https://www.pixellab.ai/create-character`
- `https://www.pixellab.ai/create-object`
- `https://www.pixellab.ai/create-ui`
- `https://www.pixellab.ai/maps`
- `https://www.pixellab.ai/create-tiles`
- `https://www.pixellab.ai/create-tileset`
- `https://www.pixellab.ai/mcp`

Official API and MCP:

- `https://api.pixellab.ai/v2/docs`
- `https://api.pixellab.ai/v2/openapi.json`
- `https://api.pixellab.ai/v2/llms.txt`
- `https://api.pixellab.ai/mcp/docs`
- `https://api.pixellab.ai/mcp`

Terminology-only local and repository sources:

- Local Aseprite extension labels and request identifiers, used only as uncited terminology evidence
- Supporting repository research notes on endpoint crosswalks, model terms, website/runtime terms, Aseprite model terms, public API/MCP coverage, website endpoints, and Aseprite extension coverage

Important exclusions:

- Browser-session credentials, browser-only auth, and request-history payloads are not public contracts.
- Root `https://api.pixellab.ai/...` website routes and Aseprite `http://api.pixellab.ai/generate-*` routes are not public REST unless the same operation appears in `https://api.pixellab.ai/v2/openapi.json` or MCP docs.
- Local Aseprite extension source can inform terminology, but filenames, line references, source contents, and source snippets are not cited as documentation evidence.
- `request_history/**` is excluded from local Aseprite conclusions because it contains user generation history rather than stable product terminology.

## Surface Legend

| Surface | Contract status | Evidence notes |
|---|---:|---|
| Public REST v2 | Public | `https://api.pixellab.ai/v2/llms.txt` says base URL is `https://api.pixellab.ai/v2`, bearer auth is required, most generation endpoints are async, and OpenAPI/interactive docs are authoritative. |
| Hosted MCP | Public tool surface, not REST | `https://api.pixellab.ai/mcp/docs` explicitly says MCP tools are not REST endpoints and should be called as tools, not curled as `/v2/...`. |
| Website app pages | First-party/internal unless docs say otherwise | Current chunks expose root `/maps`, `/tiles`, `/tilesets`, `/characters`, `/objects`, `/creator/images`, `/ui-assets`, and `replace-png` routes using website session auth. |
| Pixelorama/editor | First-party/editor integration | `https://www.pixellab.ai/editor` loads a Pixelorama iframe and current editor chunk uses root replacement routes. |
| Aseprite extension | First-party/editor integration | Local Aseprite extension source exposes labels and request identifiers, but this is uncited terminology evidence only, not a public REST/MCP contract. |
| Existing repo research | Secondary evidence | Useful for older website chunks and model term history, but current upstream fetches take precedence when they conflict. |

## Confidence Key

| Confidence | Meaning |
|---|---|
| High | Same label or capability appears in public REST/MCP docs; local/web observations may confirm terminology but do not create a public contract. |
| Medium | Public capability exists, but website/Aseprite terminology points to extra behavior, different transport, or a different label. |
| Low | Observed only in local/web terminology or older repo research; no exact public REST/MCP match found. |

## Public REST Baseline

`https://api.pixellab.ai/v2/openapi.json` currently exposes these generation and management families:

- Images and UI: `/generate-image-v2`, `/generate-with-style-v2`, `/generate-ui-v2`, `/create-ui-asset`, `/ui-assets`, `/create-image-pixflux`, `/create-image-pixflux-background`, `/create-image-pixen`, `/create-image-bitforge`.
- Image operations: `/image-to-pixelart`, `/image-to-pixelart-pro`, `/resize`, `/remove-background`, `/edit-image`, `/edit-images-v2`, `/inpaint`, `/inpaint-v3`.
- Animation and rotation: `/animate-with-text`, `/animate-with-text-v2`, `/animate-with-text-v3`, `/animate-with-skeleton`, `/estimate-skeleton`, `/edit-animation-v2`, `/interpolation-v2`, `/transfer-outfit-v2`, `/rotate`, `/generate-8-rotations-v2`, `/generate-8-rotations-v3`.
- Characters: `/create-character-with-4-directions`, `/create-character-with-8-directions`, `/create-character-pro`, `/create-character-v3`, `/create-character-state`, `/animate-character`, `/characters/animations`, plus character list/get/delete/tag/zip.
- Objects: `/create-1-direction-object`, `/create-8-direction-object`, `/objects/{object_id}/animations`, `/objects/{object_id}/states`, review selection, list/get/delete/tag.
- Maps and tiles: `/create-tileset`, `/tilesets`, `/create-tileset-sidescroller`, `/tilesets-sidescroller`, `/create-isometric-tile`, `/isometric-tiles`, `/create-tiles-pro`, `/tiles-pro/{tile_id}`, `/map-objects`.
- Prompt helpers: `/enhance-pixen-prompt`, `/enhance-character-v3-prompt`, `/enhance-animation-v3-prompt`.
- Account/status/docs: `/balance`, `/background-jobs/{job_id}`, `/llms.txt`.

Not found in public v2 OpenAPI: map CRUD, website map export/import, Pixelorama/editor `replace-png`, reduce colors/quantize, unzoom, pixel correction, try-on image, reshape, create texture, raw website `/tilesets/create`, raw website `/tiles/create`, or Aseprite root `generate-*` operation paths.

## MCP Baseline

`https://api.pixellab.ai/mcp/docs` documents MCP as a coding-agent surface for non-blocking asset generation. Tool names may be bare or prefixed by the host, and MCP download URLs are special direct HTTP endpoints.

Current MCP tool families:

- Character: `create_character`, `create_character_state`, `animate_character`, `get_character`, `list_characters`, `delete_character`, `delete_animation`.
- Tilesets: `create_topdown_tileset`, `get_topdown_tileset`, `list_topdown_tilesets`, `delete_topdown_tileset`, `create_sidescroller_tileset`, `get_sidescroller_tileset`, `list_sidescroller_tilesets`, `delete_sidescroller_tileset`.
- Isometric/tile variants: `create_isometric_tile`, `get_isometric_tile`, `list_isometric_tiles`, `delete_isometric_tile`, `create_tiles_pro`, `get_tiles_pro`, `list_tiles_pro`, `delete_tiles_pro`.
- Objects and map objects: `create_map_object`, `get_map_object`, `create_1_direction_object`, `create_8_direction_object`, `get_object`, `list_objects`, `animate_object`, `create_object_state`, `delete_object`, `select_object_frames`, `dismiss_review`.
- UI assets: `create_ui_asset`, `get_ui_asset`, `list_ui_assets`, `delete_ui_asset`.
- Platform helpers: `get_balance`, `list_projects`, `chat_*`, `sandbox_*`, `agent_*`, `agent_feedback`, `agent_help`.

MCP does not currently document raw image-editing equivalents for every REST v2 image route, such as `edit-image`, `edit-images-v2`, `inpaint`, `resize`, or `remove-background`. Route those to REST v2 unless actual MCP tools are visible in a client.

## Term Matrix

Public REST paths below are relative to `https://api.pixellab.ai/v2`. Website/internal and Aseprite operation names are listed only to explain first-party labels and routing caveats; they are not public contracts unless the same operation appears in REST v2 OpenAPI or MCP docs.

### Create Image And Style Labels

| User-facing label | Public REST v2 | MCP tool | First-party label/operation note | Product/model label | Public/internal status | Confidence and evidence |
|---|---|---|---|---|---|---|
| `Create image S-XL (new)` / `Create Image S-XL (New)` | `POST /create-image-pixen`; `POST /enhance-pixen-prompt` for prompts | None documented | Aseprite menu and request identifiers include `generate_pixen`, `model_name = "pixen"`, and root label `generate-image-pixen` | Pixen; `new` is UI/status; `S-XL` is size/tool label | Public REST plus editor wrapper | High. API page lists `Create image (Pixen)` at `/v2/create-image-pixen` and plugin tool `Create image S-XL (new)`. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create M-XL image` / `Create M-XL image (new)` | `POST /create-image-pixflux`; background variant `POST /create-image-pixflux-background` | None documented | Aseprite menu and request identifiers include `flux`, `model_name = "generate_pixelart_flux"`, and root label `generate-pixelart-flux`; website/API page says plugin tool `Create M-XL image (new)` | PixFlux/Pixflux; `M-XL` is size/tool label | Public REST plus editor wrapper | High for PixFlux. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create S-XL image (Pro)` / Aseprite `Create S-XL image (pro)` | `POST /generate-image-v2` | None documented | Aseprite request identifiers include `model_name = "generate_image_new"` and root label `generate-image-new` | Pro image workflow; provider undisclosed | Public REST plus editor wrapper | High for REST mapping, medium for exact website backend. API page lists `/v2/generate-image-v2` and plugin tool `Create S-XL image (Pro)`. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| Docs nav `Create S-L image (Pro)` | Same as above by current link target: `/docs/tools/create-sl-image-pro`, API page labels S-XL | None documented | No distinct Aseprite `S-L` tool found | Likely docs/navigation mismatch | Ambiguous public docs label | Medium. `https://www.pixellab.ai/docs` nav says `Create S-L image (Pro)`, while the API page and Aseprite label say S-XL. Treat `S-L` as alias only after verifying page contents. |
| `Create S-M image` / `Create S-M image (style)` | `POST /create-image-bitforge` | None documented | Aseprite `generate-style` family: `model_name = "generate_style"`, root `generate-style`; old variant root `generate-style-old` | BitForge/Bitforge; `S-M` is size/tool label | Public REST for current BitForge; old route internal/legacy | High for current, low for old. API page lists `/v2/create-image-bitforge` and plugin tool `Generate S-M image (style)`. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create images from style references (Pro)` / `Generate with style (Pro)` | `POST /generate-with-style-v2` | None documented | Aseprite request identifiers include `model_name = "generate_consistent_style"` and root label `generate-consistent-style` | Pro style-reference workflow | Public REST plus editor wrapper | High for public route, medium for exact wrapper parity. Evidence: API page `/v2/generate-with-style-v2`; docs nav. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Image to image (depth)` | No exact public depth endpoint found; closest documented image/init/reference routes are PixFlux/Pro image routes | None documented | Aseprite request identifiers include root label `generate-pixelart-flux` with depth behavior | PixFlux-endpoint editor workflow; depth is not public v2 field observed | Internal/editor-specific | Low. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Image to pixel art` | `POST /image-to-pixelart` | None documented | Aseprite root `generate-image-to-pixelart` | Converter | Public REST plus editor wrapper | High. Evidence: API page `/v2/image-to-pixelart`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Image to pixel art (Pro)` | `POST /image-to-pixelart-pro` | None documented | Aseprite root `generate-image-to-pixelart-pro` | Pro converter | Public REST plus editor wrapper | High. Evidence: API page `/v2/image-to-pixelart-pro`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create UI elements` | `POST /generate-ui-v2` for loose UI images; `POST /create-ui-asset` for structured/saved UI assets | `create_ui_asset` for MCP-first managed UI assets | Aseprite menu exposes a matching UI-generation action; website `/create-ui` is a human UI page | UI generation and UI asset workflows | Public REST/MCP for documented routes; website/editor internals remain internal | Medium. When both REST and MCP are available, REST `/create-ui-asset` is the fuller structured UI asset route. See `pixellab-ui-generation-surfaces-research.md`. |
| `Create UI elements (Pro)` | `POST /generate-ui-v2`; `POST /create-ui-asset` when saved asset, elements, or shape pieces matter | `create_ui_asset` for MCP-first workflows | Aseprite root `generate-ui`, `model_name = "generate_ui"` | Pro UI workflow | Public REST/MCP plus editor wrapper | High for public REST/MCP routes; Aseprite terminology evidence informs labels only. See `pixellab-ui-generation-surfaces-research.md`. |
| `Create UI from layout (Pro)` | Prefer `POST /create-ui-asset` with `pieces` and/or `elements` | `create_ui_asset` with `pieces` and/or `elements` when MCP-first | Aseprite root `generate-ui-template`, `model_name = "generate_ui_template"` | Pro UI template/layout workflow | Public REST/MCP for shape-piece asset creation; editor-specific wrappers remain internal | High for current public shape-piece capability. REST has the more complete schema. See `pixellab-ui-generation-surfaces-research.md`. |

### Animation, Rotation, And Prompt Labels

| User-facing label | Public REST v2 | MCP tool | First-party label/operation note | Product/model label | Public/internal status | Confidence and evidence |
|---|---|---|---|---|---|---|
| `Animate with text (new)` | `POST /animate-with-text-v3`; helper `POST /enhance-animation-v3-prompt` | Use `animate_character`/`animate_object` only for managed assets, not raw image v3 parity | Aseprite root `animate-with-text-v3`, `model_name = "generate_animate_with_text_v3"` | v3 animation workflow; `new` is UI label | Public REST plus editor wrapper | High. Evidence: API page lists `/v2/animate-with-text-v3`; docs nav says `Animate with text (New)`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Animate with text (Pro)` | `POST /animate-with-text-v2` | Managed character/object animation only | Aseprite root `generate-animate-with-text`, `model_name = "generate_animate_with_text"` | Pro/v2 animation workflow | Public REST plus editor wrapper | High. Evidence: API page `/v2/animate-with-text-v2` and plugin tool `Animate with text (Pro)`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Animate with text` | `POST /animate-with-text` | Managed character/object animation only | Aseprite older root `generate-movement` | Base/legacy text animation | Public REST plus legacy editor wrapper | Medium. Evidence: API page `/v2/animate-with-text`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Animate with skeleton` | `POST /animate-with-skeleton`; `POST /estimate-skeleton` for pose utility | None as raw tool in current hosted MCP docs; MCP character/object animation may use templates/modes | Aseprite root `generate-pose-animation` or `generate-animation`; newer menu label `Animate with skeleton (new)` appears in the extension | Skeleton animation workflow | Public REST plus editor wrappers | Medium. Evidence: API llms lists both endpoints; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Interpolate (new)` | No exact public v3 interpolation endpoint found; closest is `POST /interpolation-v2` | None documented | Aseprite root `animate-with-text-v3`, `model_name = "generate_interpolation_v3"` | New/v3 editor workflow | Editor-specific wrapper with public partial | Low/medium. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Interpolate (Pro)` | `POST /interpolation-v2` | None documented | Aseprite root `generate-interpolation-pro`, `model_name = "interpolation"` | Pro interpolation | Public REST plus editor wrapper | High. Evidence: API page `/v2/interpolation-v2`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Edit animation (Pro)` | `POST /edit-animation-v2` | None documented | Aseprite root `generate-edit-animation-pro`, `model_name = "edit_animation_pro"` | Pro animation edit | Public REST plus editor wrapper | High. Evidence: API page `/v2/edit-animation-v2`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Transfer outfit to animation (Pro)` | `POST /transfer-outfit-v2` | None documented | Aseprite root `generate-transfer-outfit-pro`, `model_name = "transfer_outfit_pro"` | Pro outfit transfer | Public REST plus editor wrapper | High. Evidence: API page `/v2/transfer-outfit-v2`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Rotate to 8 directions (new)` | `POST /generate-8-rotations-v3` | None documented for raw rotate-to-8; character/object creation can output directions | Aseprite root `animate-with-text-v3`, `model_name = "generate_8_rotations_v3"` | v3 rotation workflow | Public REST plus editor wrapper | Medium/high. Evidence: API page `/v2/generate-8-rotations-v3`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Rotate to 8 directions (Pro)` / `Create 8-directional sprite (Pro)` | `POST /generate-8-rotations-v2` | None documented for raw rotate-to-8 | Aseprite root `generate-reference-to-8-rotations`, `model_name = "reference_to_8_rotations"` | Pro rotation workflow | Public REST plus editor wrapper | Medium/high. Evidence: API page `/v2/generate-8-rotations-v2`; docs nav `Create 8-directional sprite (Pro)`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Rotate` | `POST /rotate` | None documented | Aseprite root `generate-rotate-single` | Base rotate utility | Public REST plus editor wrapper | High. Evidence: API llms `/rotate`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Prompt enhancement` | `POST /enhance-pixen-prompt`, `/enhance-character-v3-prompt`, `/enhance-animation-v3-prompt` | No direct prompt helper tools documented except `agent_help` | Aseprite observes WS helper paths such as `enhance-animation-prompt-ws` and `enhance-pixen-prompt-ws` in local dialog code | Prompt helper, provider undisclosed | Public REST for HTTP helpers; editor helper paths internal | High for public helpers, low for WS paths. Evidence: API page prompt helper section; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |

### Characters, Objects, And Managed Assets

| User-facing label | Public REST v2 | MCP tool | First-party label/operation note | Product/model label | Public/internal status | Confidence and evidence |
|---|---|---|---|---|---|---|
| `Create Character` website page | `POST /create-character-with-4-directions`, `/create-character-with-8-directions`, `/create-character-pro`, `/create-character-v3`; management `/characters*` | `create_character`, `get_character`, `list_characters`, `delete_character` | Website `/create-character` chunk uses root `/characters/zip`, `/characters/delete-batch`, `/characters/tags`; page button says `Create Character` | Character workflows; Pro/v3 are modes, not providers | Public REST/MCP for generation and management; website batch routes internal | High for public, medium for website batch helpers. Evidence: API page character section; MCP docs character tools; website chunk `create-character-3b48e01d98147a51.js` route snippets. |
| `Character with 4 rotations` | `POST /create-character-with-4-directions` | `create_character(n_directions=4)` | Aseprite root `generate-4-rotations`, `model_name = "generate_4_rotations"` | Character rotation workflow | Public REST/MCP plus editor wrapper | High. Evidence: API page `/v2/create-character-with-4-directions`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Character with 8 rotations` | `POST /create-character-with-8-directions`; v3/pro alternatives exist | `create_character(n_directions=8)` | Aseprite root `generate-8-rotations` | Character rotation workflow | Public REST/MCP plus editor wrapper | High. Evidence: API page `/v2/create-character-with-8-directions`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create character (Pro)` | `POST /create-character-pro` | `create_character(mode=...)` may map, exact internal route hidden | Website/REST docs only; Aseprite Pro sprite rotate is not necessarily this endpoint | Pro character workflow | Public REST; MCP capability mapping inferred | Medium/high. Evidence: API page `/v2/create-character-pro`; MCP `create_character` has `mode`. |
| `Create character v3` | `POST /create-character-v3`; helper `/enhance-character-v3-prompt` | `create_character` may map by mode, exact internal route hidden | Website docs; no exact Aseprite label found besides v3-adjacent rotation/animation | v3 character model/workflow | Public REST; MCP capability mapping inferred | High for REST, medium for MCP exact route. Evidence: API page says create an 8-direction character using v3 model. |
| `Create Object` website page | `POST /create-1-direction-object`, `/create-8-direction-object`, object state/animation/review endpoints | `create_1_direction_object`, `create_8_direction_object`, `get_object`, `list_objects`, `animate_object`, `create_object_state`, `select_object_frames`, `dismiss_review`, `delete_object` | Website `/create-object` chunk uses root `/objects/zip`, `/objects/delete-batch`; page button says `Create Object` | Object workflow | Public REST/MCP for core; website batch routes internal | High for public, medium for website batch helpers. Evidence: API llms object section; MCP docs object tools; website chunk `create-object-94d4405f1f185485.js` route snippets. |
| `Create 8-directional object/character (Pro)` | Partial: `/generate-8-rotations-v2`, `/create-8-direction-object`, character endpoints depending intent | `create_8_direction_object` or `create_character` depending asset | Aseprite root `generate-reference-to-8-rotations` | Pro rotation/object-character wrapper | Collision-prone editor wrapper | Medium. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create animated object/character (Pro)` | Partial: object animation endpoints, character animation endpoints, or `/animate-with-text-v2` depending source asset | `animate_object` or `animate_character` for managed assets | Aseprite root `generate-animate-with-text` as an extension wrapper | Pro animation wrapper | Collision-prone editor wrapper | Medium. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create map object` / `Map Objects` | `POST /map-objects` | `create_map_object`, `get_map_object` | Website Map Workshop object flows are root map/editor routes | Map object generation | Public REST/MCP for generated map object; website map editing internal | High. Evidence: API page `/v2/map-objects`; MCP docs say map objects auto-delete after 8 hours. |

### Maps, Tiles, Map Workshop, And Pixelorama

| User-facing label | Public REST v2 | MCP tool | First-party label/operation note | Product/model label | Public/internal status | Confidence and evidence |
|---|---|---|---|---|---|---|
| `Map Workshop` / `Maps` | No public map CRUD found; public map-adjacent endpoints are tilesets, tiles pro, isometric tiles, map objects | No full map CRUD; MCP covers tilesets and map objects | Website `/maps` chunk uses `/maps/save`, `/maps/list`, `/maps`, `/maps/tiles`, imports, exports; page says Map Workshop | Website map editor | Internal website surface | High. Evidence: `https://www.pixellab.ai/maps` says Map Workshop requires subscription; current maps chunk exposes `/maps/save` and `/maps/list`. |
| `Create top-down tileset` / `Create tileset (high top-down)` | `POST /create-tileset`; async resource `POST /tilesets`; list/get `/tilesets`, `/tilesets/{tileset_id}` | `create_topdown_tileset`, `get_topdown_tileset`, `list_topdown_tilesets`, `delete_topdown_tileset` | Aseprite root `generate-tileset`; website create-tileset root `POST /tilesets/create` | Top-down/Wang tileset | Public REST/MCP plus internal web/editor wrappers | High for public route, medium for web parity. Evidence: API page `/v2/create-tileset`; MCP docs `create_topdown_tileset`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| Website `Generate Pro` tileset / Create Tileset Pro | No exact public v2 route. Closest public top-down route is `/create-tileset`; `create-tiles-pro` is a different individual-tile variation route | `create_topdown_tileset` has some parameters resembling Pro controls, but exact web Pro route hidden | Website create-tileset chunk sends root `/tilesets/create` with `use_pro`, `spread_x`, `slope_size`, `raggedness` | Pro tileset mode; current chunk did not contain `Gemini` string | Internal website mode with partial public analogs | Medium/low. Fresh evidence confirms `use_pro` and root route. Existing repo research says older chunk mentioned Gemini, but the older chunk now 404s and current chunk did not include `Gemini`. |
| `Create sidescroller tileset` | `POST /create-tileset-sidescroller`; async `POST /tilesets-sidescroller` | `create_sidescroller_tileset`, `get_sidescroller_tileset`, `list_sidescroller_tilesets`, `delete_sidescroller_tileset` | Aseprite root `generate-tileset-sidescroller` | Sidescroller/platformer tileset | Public REST/MCP plus editor wrapper | High. Evidence: API page `/v2/create-tileset-sidescroller`; MCP docs; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create isometric tile` | `POST /create-isometric-tile`; list/get `/isometric-tiles` | `create_isometric_tile`, `get_isometric_tile`, `list_isometric_tiles`, `delete_isometric_tile` | Aseprite request identifiers use root label `generate-pixelart-flux` for isometric tile behavior | Isometric tile workflow; not a full isometric tileset | Public REST/MCP plus editor wrapper | High for public route, medium for exact Aseprite route. Evidence: API page `/v2/create-isometric-tile`; MCP docs; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create tiles (Pro)` / `Tiles pro` | `POST /create-tiles-pro`; `GET /tiles-pro/{tile_id}` | `create_tiles_pro`, `get_tiles_pro`, `list_tiles_pro`, `delete_tiles_pro` | Aseprite root `generate-tiles-pro` | Tiles Pro variants: hex, isometric, square top-down, etc. | Public REST/MCP plus editor wrapper | High. Evidence: API page `/v2/create-tiles-pro`; MCP docs `create_tiles_pro`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| Website `Create tiles` | Public `/create-tiles-pro` is related but not necessarily identical | `create_tiles_pro` likely closest | Website create-tiles/maps chunks use root `/tiles/create`, `/tiles/list`, `/tiles/import` | Website tile workshop | Internal website surface with public partial | Medium. Evidence: maps chunk route snippets `/tiles/create`, `/tiles/list`; API has no root `/tiles/create`. |
| `Create map (pixflux)` | Partial: closest public image route `POST /create-image-pixflux` | None documented | Aseprite root `generate-pixelart-flux`, `model_name = "generate_map_flux"` | PixFlux map-image editor workflow | Editor-specific, public image partial only | Medium/low. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Extend map (v2)` / `Extend map` / `Extend map (old)` | Partial: `/inpaint`, `/inpaint-v3`, or `/map-objects` depending intent; no exact map-extend endpoint | None documented | Aseprite root `generate-pixelart-flux`, `generate-inpainting`, or `generate-tiles` depending tool | Map/editor inpainting workflow | Editor-specific | Low/medium. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Create texture` | No exact public REST v2 route found | None documented | Aseprite root `generate-texture` | Texture editor workflow | Internal/editor-specific | Low. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Pixelorama` / web editor actions | No public v2 replacement endpoints found | None documented | `https://www.pixellab.ai/editor` loads Pixelorama; current editor chunk uses `/creator/images/{id}/replace-png`, `/character/{id}/rotations/replace-png`, `/object-animation/{id}/direction/{dir}/replace-png`, `/ui-assets/{id}/replace-png`, `/maps/{id}/inpainting/replace-png` | Editor save-back actions | Internal website/editor routes | High. Evidence: current editor chunk `editor-654881b385de4277.js`; official docs nav includes `Introduction to Pixelorama`. |

### Inpaint, Edit, And Utility Labels

| User-facing label | Public REST v2 | MCP tool | First-party label/operation note | Product/model label | Public/internal status | Confidence and evidence |
|---|---|---|---|---|---|---|
| `Inpaint` | `POST /inpaint` | None documented | Aseprite root `generate-inpainting` | Base inpaint | Public REST plus editor wrapper | High. Evidence: API llms `/inpaint`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Inpaint (v3)` / `Inpaint (Pro)` | `POST /inpaint-v3` | None documented | Aseprite root `generate-inpainting-v3`; file title says `Inpaint (pro)`, menu says `Inpaint (v3)` | v3/Pro inpaint workflow | Public REST plus editor wrapper | High, with label collision. Evidence: API page calls `/v2/inpaint-v3` `Inpaint (Pro)`; docs nav says `Inpaint v3`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Inpaint M-L (pixpatch v2)` | No exact public v2 `pixpatch` or `M-L` route found; closest public inpaint routes are `/inpaint` and `/inpaint-v3` | None documented | Aseprite root `generate-pixelart-flux`, `model_name = "generate_inpainting_pixpatch_v2"` | PixPatch v2 / M-L inpaint label | Editor/docs label, internal exact route | Low/medium. Evidence: docs nav label; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Edit image` | `POST /edit-image` | None documented | Aseprite root `generate-edit`, `model_name = "generate_edit"` | Base edit | Public REST plus editor wrapper | High. Evidence: API page `/v2/edit-image`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Edit image (Pro)` / `Edit images (Pro)` | `POST /edit-images-v2` | None documented | Aseprite root `generate-edit-image-pro`, `model_name = "edit_image_pro"` | Pro image edit, multi/reference-capable | Public REST plus editor wrapper | High. Evidence: API page `/v2/edit-images-v2`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Multi-image edit` / docs `Multi image` | Partial: closest public route `POST /edit-images-v2` | None documented | Aseprite root `generate-multi-edit`, `model_name = "generate_multi_edit"` | Multi-image editor workflow | Editor-specific wrapper with public partial | Medium. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Resize` | `POST /resize` | None documented | Aseprite root `generate-resize`, `model_name = "generate_resize"` | Resize utility | Public REST plus editor wrapper | High. Evidence: API page `/v2/resize`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Remove background` | `POST /remove-background` | None documented | Aseprite root `remove-background`, `model_name = "generate_remove_background"` | Background removal utility | Public REST plus editor wrapper | High. Evidence: API page `/v2/remove-background`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Reduce colors` / `Quantize Colors` | No public v2 endpoint found | None documented | Aseprite root `quantize-image`; dialog title `Quantize Colors | Reduce colors` | Quantization utility | Editor/internal only | Low. Evidence: docs nav `Reduce colors`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Unzoom pixel art` | No public v2 endpoint found | None documented | Aseprite root `unzoom-pixelart`, `model_name = "unzoom_pixelart"` | Unzoom editor utility | Editor/internal only | Low. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Pixel correction` | No public v2 endpoint found | None documented | Aseprite root `correct-pixelart`, `model_name = "generate_correct_pixelart"` | Pixel correction utility | Editor/internal only | Low. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Try-on image` / docs `Try on` | No exact public v2 single-image try-on endpoint found; `POST /transfer-outfit-v2` is animation outfit transfer, not same output | None documented | Aseprite root `generate-try-on`, `model_name = "generate_try_on"` | Try-on editor workflow | Editor/internal only | Low. Evidence: docs nav `Try on`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Reshape` | No exact public v2 endpoint found | None documented | Aseprite exposes a deprecated or extra reshape action; website docs nav includes `Reshape` | Editor reshape workflow | Editor/internal only | Low. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Canny`, `Pose to image`, `Depth` | No exact public v2 Canny/Pose/Depth routes found, except `estimate-skeleton` for skeleton estimation | None documented | Aseprite root `generate-general-canny`, `generate-style` pose, `generate-pixelart-flux` depth | Editor-guided image workflows | Editor/internal with partial public alternatives | Low/medium. Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |

### Auth, Account, And Platform Labels

| User-facing label | Public REST v2 | MCP tool | First-party label/operation note | Product/model label | Public/internal status | Confidence and evidence |
|---|---|---|---|---|---|---|
| `Secret`, `API token`, `API key`, bearer token | Public REST uses `Authorization: Bearer YOUR_API_TOKEN` | MCP config uses `Authorization: Bearer YOUR_API_TOKEN` | Aseprite menu has `Secret`; website account exposes account token/secret label | Auth credential label, not model/tool | Public auth concept, labels differ by surface | High. Evidence: `https://api.pixellab.ai/v2/llms.txt`; `https://api.pixellab.ai/mcp/docs`; Aseprite terminology evidence informs this row; source filenames are intentionally omitted. |
| `Balance` | `GET /balance` | `get_balance` | Website account data routes are separate; Aseprite no direct balance tool found | Account utility | Public REST/MCP | High. Evidence: OpenAPI `/balance`; MCP docs `get_balance`. |
| `Background job status` | `GET /background-jobs/{job_id}` | MCP uses resource-specific `get_*` tools instead | Website/editor use their own status and replacement flows | Async status | Public REST | High. Evidence: llms/OpenAPI. |
| `Vibe Coding` / `MCP` | Not a REST path; REST fallback is v2 API | Hosted server URL `https://api.pixellab.ai/mcp` with tools | Website setup page `https://www.pixellab.ai/mcp` lists tool examples | MCP product surface | Public MCP setup and docs | High. Evidence: `https://www.pixellab.ai/mcp`, `https://api.pixellab.ai/mcp/docs`. |
| `Agent`, `Sandbox`, `Projects`, `Chat` | No public art REST endpoint found | `list_projects`, `chat_*`, `sandbox_*`, `agent_*`, `agent_feedback`, `agent_help` | Website agent/platform pages not deeply mapped in this reference | MCP platform helpers | MCP-public, not REST v2 art API | High for tool availability, low for backend implementation. Evidence: MCP docs lines for chat/sandbox/agent tools. |

## Product And Model Term Dictionary

| Term | Meaning in user-facing docs | Public selector or terminology note | Provider disclosure | Confidence |
|---|---|---|---|---|
| Pixen | New/S-XL image generation label | REST `/create-image-pixen`; Aseprite terminology evidence includes `model_name = "pixen"` and root label `generate-image-pixen` | PixelLab-branded, provider undisclosed | High |
| PixFlux / Pixflux | M-XL image generation label; also reused in several editor workflows through `generate-pixelart-flux` | REST `/create-image-pixflux`, `/create-image-pixflux-background`; Aseprite terminology evidence includes root label `generate-pixelart-flux` | PixelLab-branded, provider undisclosed | High |
| BitForge / Bitforge | S-M image/style generation label | REST `/create-image-bitforge`; Aseprite terminology evidence includes the `generate-style` family | PixelLab-branded, provider undisclosed | High |
| Pro | Quality/tier/mode label across many unrelated tools | Endpoint suffixes and paths such as `/generate-image-v2`, `/animate-with-text-v2`, `/edit-images-v2`, `/create-character-pro`, `/create-tiles-pro`; website `use_pro` | Product/mode, provider undisclosed | High |
| v3 | Version/workflow label | REST `/create-character-v3`, `/animate-with-text-v3`, `/generate-8-rotations-v3`, `/inpaint-v3`; Aseprite v3 source terminology is evidence only | Product/version, provider undisclosed | High |
| new | UI/status label, not a backend selector | Maps to Pixen for S-XL images and v3 for animation/rotation/interpolation | Product/status, provider undisclosed | High |
| S-XL, M-XL, S-M, M-L | Size/tool labels, not endpoint names | Must map to a concrete public endpoint, documented tool, or first-party terminology note | Not provider terms | High |
| PixPatch v2 | M-L inpaint label in docs/Aseprite | Aseprite terminology evidence includes `generate_inpainting_pixpatch_v2` and root label `generate-pixelart-flux`; no exact public v2 PixPatch path found | PixelLab-branded/workflow label, provider undisclosed | Low/medium |
| Gemini | Existing repo research observed Gemini text in an older create-tileset website chunk | Current 2026-06-26 create-tileset chunk did not contain `Gemini`; older chunk URL now 404s | External provider named only in prior observed website copy | Low until reverified |

## Confusing Collisions

1. `new` vs `Pro`
   - `Create image S-XL (new)` maps to Pixen and `/v2/create-image-pixen`.
   - `Create S-XL image (Pro)` maps to `/v2/generate-image-v2`.
   - `Animate with text (new)` maps to `/v2/animate-with-text-v3`.
   - `Animate with text (Pro)` maps to `/v2/animate-with-text-v2`.
   - Do not route by `new` or `Pro` alone. Route by the full label and asset intent.

2. `S-XL`, `M-XL`, `S-M`, `M-L`
   - These are user-facing size/tool labels.
   - They do not appear as public REST endpoint slugs.
   - `S-XL` collides between Pixen/new and Pro image generation.
   - `M-L` currently points to PixPatch v2 inpaint in docs/Aseprite but has no exact public v2 path found.

3. Website root routes vs public REST v2 paths
   - Website Map Workshop uses root `/maps/save`, `/maps/list`, `/tiles/create`, `/tilesets/create`, etc.
   - Public REST uses `/v2/create-tileset`, `/v2/tilesets`, `/v2/create-tiles-pro`, etc.
   - Same host does not imply same auth, schema, or support contract.

4. MCP tool names vs REST paths
   - MCP docs warn that tools like `create_character` are not REST endpoints.
   - A REST fallback should use `https://api.pixellab.ai/v2/...`, not guessed `/mcp/...` or `/v2/create_character` paths.

5. Pixelorama/editor labels vs API endpoints
   - Pixelorama save-back routes such as `/creator/images/{id}/replace-png` and `/ui-assets/{id}/replace-png` are website/editor integration routes.
   - No public v2 `replace-png` equivalents were found.

6. `Create tiles (Pro)` vs website Create Tileset Pro
   - Public `/v2/create-tiles-pro` and MCP `create_tiles_pro` generate individual tile variants.
   - Website create-tileset Pro uses root `/tilesets/create` with `use_pro` and Pro controls. It is not the same public contract.

7. Character/object/rotation wrappers
   - Aseprite `Create 8-directional object/character (pro)` can be a raw rotation workflow, object workflow, or character workflow depending the source image and user intent.
   - Public REST splits these into `/generate-8-rotations-v2`, `/create-8-direction-object`, and character create endpoints.

8. `Inpaint (v3)` vs `Inpaint (Pro)`
   - Public REST summary for `/inpaint-v3` says `Inpaint image (Pro)`.
   - Docs/Aseprite menu also label it `Inpaint v3`.
   - Treat v3/Pro as labels on the same public endpoint here, but do not generalize that equivalence to other tools.

9. Local `model_name` vs product model
   - Aseprite `model_name` values such as `generate_image_new`, `generate_pixelart_flux`, `generate_style`, and `generate_inpainting_v3` are local request identifiers.
   - They are not guaranteed provider/model names.

10. Root API redirect
   - `https://api.pixellab.ai/` redirecting to v1 docs is not evidence that website root routes are v1 REST endpoints.
   - Website and Aseprite root operations are separate first-party runtime surfaces.

## Recommended Progressive-Disclosure References

Create small, task-routed references under `skills/pixellab-pip/references/` rather than one giant mapping file. Suggested split:

1. `user-facing-term-router.md`
   - Purpose: one-page alias table from common labels to the correct reference file.
   - Contents: `Create image S-XL (new)` -> Pixen REST; `Create S-XL image (Pro)` -> Pro image REST; `Map` -> clarify whole map vs tileset vs map object; `Tiles` -> clarify terrain tileset vs tile variants.

2. `image-model-labels.md`
   - Purpose: image/user-size labels only.
   - Contents: Pixen/PixFlux/BitForge, S-XL/M-XL/S-M, Pro image, style reference, image-to-pixel-art, prompt enhancement.
   - Rule: never infer provider internals from label alone.

3. `animation-rotation-labels.md`
   - Purpose: text animation, skeleton, interpolation, rotation, outfit transfer.
   - Contents: `new` -> v3 where documented, `Pro` -> v2/pro routes, Aseprite terminology crosswalk, MCP managed-asset alternatives.

4. `character-object-labels.md`
   - Purpose: route character/object/map-object requests.
   - Contents: character v3/pro/4/8 directions, object 1/8 directions, managed MCP asset lifecycle, review-state object tools, state/animation follow-ups.

5. `map-tiles-editor-labels.md`
   - Purpose: separate Map Workshop/editor from public map/tile APIs.
   - Contents: top-down tileset, sidescroller tileset, isometric tile, tiles pro, map object, whole-map Map Workshop, Pixelorama/editor replace routes.
   - Warning block: root `/tilesets/create` and `/tiles/create` are website routes, not public REST v2.

6. `editor-only-utilities.md`
   - Purpose: document unsupported public API utilities.
   - Contents: reduce colors/quantize, unzoom, pixel correction, try-on, reshape, create texture, Canny/pose/depth distinctions.
   - Recommended response: route to visible Aseprite/Pixelorama flow or local fallback only after explaining it is not PixelLab public REST/MCP.

7. `auth-token-terminology.md`
   - Purpose: normalize `Secret`, `API token`, `API key`, bearer token, and website browser-auth context.
   - Contents: REST/MCP bearer token from account/MCP setup; website browser auth is not an API token; Aseprite Secret label.

8. `surface-boundaries.md`
   - Purpose: short guardrails for public, internal, and observed surfaces.
   - Contents: MCP tools are not REST; website routes are not REST v2; Aseprite root operations are internal; public OpenAPI wins when endpoint names conflict.

Recommended lookup flow:

1. Match the full user phrase against `user-facing-term-router.md`.
2. If it contains image size/model terms, load only `image-model-labels.md`.
3. If it contains map/tiles/editor words, load only `map-tiles-editor-labels.md`.
4. If it contains unsupported utilities, load `editor-only-utilities.md`.
5. Only fetch current upstream OpenAPI/MCP docs when a route, field, model/mode, or support status is missing or could have changed.

## Open Questions And Uncertainties

- `Gemini`: existing repo research observed the word in an older website create-tileset Pro chunk, but the current chunk fetched on 2026-06-26 did not include it and the old chunk URL returned 404. Treat `Gemini` as stale/low-confidence unless a current page or bundle reintroduces it.
- Website Create Tileset Pro: current chunk confirms `use_pro`, `spread_x`, `slope_size`, `raggedness`, and root `/tilesets/create`; public REST does not expose an exact equivalent. MCP `create_topdown_tileset` has similar controls, but exact backend mapping is not public.
- UI labels still collide: `generate-ui-v2` is loose/raw UI image generation, while `create-ui-asset` and MCP `create_ui_asset` are structured saved UI asset workflows with `pieces`/`elements`. See `pixellab-ui-generation-surfaces-research.md`.
- `M-L PixPatch v2`: docs/Aseprite expose the term, but public v2 has only base/pro inpaint endpoints. Do not invent `/v2/pixpatch` or `/v2/inpaint-pixpatch-v2`.
- Pixelorama/editor replacement routes: observed in the current editor chunk, but they are website-session routes and may change independently of public REST/MCP.
- Aseprite local source is rich but not a public API contract. It is excellent terminology evidence, but routing should prefer REST v2 or MCP when building code.

## Bottom Line

For automation and code, route to REST v2 or MCP first:

- Pixen/new S-XL image -> `POST /v2/create-image-pixen`.
- PixFlux/M-XL image -> `POST /v2/create-image-pixflux`.
- Pro S-XL image -> `POST /v2/generate-image-v2`.
- BitForge/S-M image -> `POST /v2/create-image-bitforge`.
- UI Pro/raw image -> `POST /v2/generate-ui-v2`; UI asset/layout/pieces -> prefer `POST /v2/create-ui-asset`, or use MCP `create_ui_asset` for MCP-first workflows.
- Animation new/v3 -> `POST /v2/animate-with-text-v3`.
- Animation Pro -> `POST /v2/animate-with-text-v2`.
- Character/object/tileset managed workflows -> MCP tools when available, otherwise corresponding REST v2 endpoints.
- Whole Map Workshop, Pixelorama save-back, quantize/reduce colors, unzoom, pixel correction, try-on, reshape, and root website routes -> visible editor/website surfaces or explicitly labeled unsupported/internal paths, not public REST contracts.
