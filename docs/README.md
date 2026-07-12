# More Documentation

Last reviewed: 2026-07-02.

These docs explain PixelLab tools, workflows, terminology, SDK boundaries, and auth rules that Pip needs in order to automate PixelLab correctly. They supplement the repository README; install, update, and plugin metadata stay there.

This folder is developer-facing. Use it for research spikes, test notes, findings, audits, comparisons, terminology background, and maintainer QA policy. Do not treat `docs/` files as the canonical agent instruction contract.

Agent-facing routing and operational instructions belong in `../skills/pixellab-pip/references/`, with `../skills/pixellab-pip/SKILL.md` as the core router. When research here changes agent behavior, update the matching reference file instead of expecting agents to load developer notes.

## Showcase

- [Showcase](showcase/README.md) - examples of using Pip to route PixelLab requests, enhance prompts, generate assets, and document results.

## Benchmark

- [PixelLab Pip Skill Benchmark](pixellab-pip-benchmark.md) - reproducible agent-side context/token and routing-correctness comparison of the skill vs no skill vs the official mcp/docs injection.

## Research

- [PixelLab Surfaces And Services](pixellab/pixellab-surfaces-and-services.md) - where MCP, REST v2, website/editor, Aseprite, Pixelorama, SDKs, and legacy v1 fit.
- [PixelLab Asset Routing](pixellab/pixellab-asset-routing.md) - how common requests map to PixelLab tools, endpoints, and workflows.
- [PixelLab UI Generation Surfaces Research](pixellab/pixellab-ui-generation-surfaces-research.md) - current UI-specific matrix for MCP `create_ui_asset`, REST `/create-ui-asset`, REST `/generate-ui-v2`, shape pieces, elements, and website/editor boundaries.
- [PixelLab User-Facing Term To Backend Mapping](pixellab/pixellab-user-facing-term-backend-mapping.md) - production mapping of user-facing labels across REST v2, MCP, website/editor, Pixelorama, and Aseprite to endpoints, tools, and model/product terms.
- [PixelLab MCP vs REST v2 Route Parity](pixellab/pixellab-mcp-vs-rest-route-parity.md) - endpoint-level MCP/REST coverage matrix and the full inventory of missing features both ways: REST v2 endpoints with no MCP tool, and MCP tools with no REST v2 endpoint.
- [Pixel-Art GIF-Friendly Disappearance](pixellab/pixel-art-gif-friendly-disappearance.md) - prompt and QA guidance for GIF-friendly disappearance effects, 1-bit transparency, dithered cutout dissolves, particle dissipation, and export checks.
- [PixelLab Chibi Base Character Findings](pixellab/pixellab-chibi-base-character-findings.md) - live-generation findings for a reusable chibi avatar base character, including closest candidates, failed prompt/model patterns, and unresolved next tests.
- [PixelLab 16px Item Sprite Generation Spike](pixellab/pixellab-16px-item-sprite-generation-spike.md) - findings on why `16x16` full-cell tiles work better than strict `16x16` non-tile item sprites, including prompt comparisons, Aseprite style-reference observations, a pixen single-subject icon test (coins read well at 16px; the hollow-center background-removal artifact and its edge-flood fix), and verification guidance.
- [PixelLab 32px VFX Atlas Density Spike](pixellab/pixellab-32px-vfx-atlas-density-spike.md) - controlled prompt findings for strict `16x16` atlases of transparent `32x32` explosion effects, including density failure analysis and safer assembly experiments.
- [PixelLab Image Size Limits (Min And Max)](pixellab/pixellab-image-size-limits.md) - per-tool minimum and maximum size limits from the raw OpenAPI schema, why the Aseprite `32x32` minimum is a client-side editor limit, the schema-enforced `16px` floor (and the `8px`-only `glyph_px` exception), and per-endpoint max/area/aspect rules across REST v2 and MCP.
- [PixelLab API Pricing Model List](pixellab/pixellab-api-pricing-model-list.md) - current API pricing and model/tool list from PixelLab's official API catalog.
- [PixelLab Documentation Watch Cache](pixellab/pixellab-doc-watch-cache.md) - local-only watcher workflow for caching upstream PixelLab docs, detecting REST/MCP drift, and deciding when the Agent Skill needs updates.
- [PixelLab Changelog 2026-07-01](pixellab/pixellab-changelog-2026-07-01.md) - dated summary of the July 1 public-doc drift and corresponding PixelLab Pip routing/reference updates.
- [PixelLab Top-Down Tileset Transition Findings](pixellab/pixellab-topdown-tileset-transition-findings.md) - live-generation findings for `create_topdown_tileset` transition sizes, compact 4x4 graybox exports, and the `transition_size: 1.0` expanded-layout caveat.
- [PixelLab DualGrid Tileset Export System](pixellab/pixellab-dualgrid-tileset-export-system.md) - reverse-engineering notes for PixelLab's compact DualGrid/Wang tileset metadata, layout order, public tileset surfaces, and local simulator scope.
- [PixelLab 1-Bit Tileset Prompt Testing](pixellab/pixellab-1bit-tileset-prompt-testing.md) - simulator and live MCP findings for black-and-white top-down and sidescroller prompt tests.
- [PixelLab 1-Bit Tileset Optimization Workflow](pixellab/pixellab-1bit-tileset-optimization-workflow.md) - practical workflow for using simulator and live MCP tests to place white 1-bit edge, rim, ledge, and boundary pixels in top-down and sidescroller tilesets.
- [PixelLab Skeleton And Template Animation Research](pixellab/pixellab-skeleton-template-animation-research.md) - managed template animations, raw skeleton keypoint routes, Aseprite skeleton workflow parity, and MCP/REST boundaries.
- [PixelLab Paperdolling Research Spike](pixellab/pixellab-paperdolling-research-spike.md) - research on RPG equipment layers, PixelLab composite/edit boundaries, layer extraction, skeleton hardpoints, and paperdoll QA.
- [PixelLab Paperdolling System Plan](pixellab/pixellab-paperdolling-system-plan.md) - staged implementation plan for a PixelLab-backed paperdoll package workflow, Python extraction prototype, previews, manifests, and engine exports.
- [PixelLab Auth And Security](pixellab/pixellab-auth-and-security.md) - bearer-token handling and automation boundaries.
- [PixelLab SDK Compatibility](pixellab/pixellab-sdk-compatibility.md) - official SDK guidance and when to call REST v2 directly.
- [PixelLab Terminology](pixellab/pixellab-terminology.md) - product labels, endpoint labels, and terms agents should not over-interpret.
- [Official PixelLab MCP Service Comparison](tools/official-pixellab-mcp-service-comparison.md) - technical comparison between Pip and the official hosted MCP service.
- [PixelLab MCP Docs vs Pip Skill (Session Context)](tools/pixellab-mcp-docs-vs-pip-skill.md) - decision guide for choosing session context: the official mcp/docs link vs installing the Agent Skill.
- [PixelLab Aseprite Extension Coverage Audit](tools/aseprite-extension-coverage-audit.md) - comparison of official Aseprite editor workflows with Pip's MCP/REST/editor routing.
- [Aseprite CLI Integration Testing](tools/aseprite-cli-integration-testing.md) - maintainer QA policy for local Aseprite CLI workflow tests.
- [PixelLab AI Skill vs Pip Skill](tools/pixellab-ai-skill-vs-pip-skill.md) - feature comparison between Pip and the unofficial PixelLab AI Skill.

## Official PixelLab

For exact current endpoint schemas, tool lists, model/mode availability, pricing, and authentication behavior, verify against [Resources](resources.md#official-pixellab).

## Publication Rules

These docs intentionally avoid:

- Copied credentials, session tokens, cookies, JWTs, or private account data.
- Instructions for automating undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension.
- Direct citations of local Aseprite extension filenames, line references, source contents, or source snippets; use source only as uncited terminology evidence, and route code/automation to REST v2, MCP, or visible editor workflows.
- Local machine paths or user-specific filesystem details.
- Provider/internal model claims not documented in public PixelLab sources.
- Informal, mocking, or critical language about PixelLab.

PixelLab Pip can document caveats when they matter for correct implementation, but the tone should stay neutral and technical.
