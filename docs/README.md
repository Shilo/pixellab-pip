# More Documentation

Last reviewed: 2026-08-06.

These docs contain PixelLab Pip's user guides, developer material, research, and technical background. The repository README is the short front door; detailed installation, usage, and security material lives here.

Research and developer sections are maintainer-facing. Do not treat `docs/` files as the canonical agent instruction contract.

Agent-facing routing and operational instructions belong in `../skills/pixellab-pip/references/`, with `../skills/pixellab-pip/SKILL.md` as the core router. When research here changes agent behavior, update the matching reference file instead of expecting agents to load developer notes.

## User Guides

- [Installation](install.md) - marketplaces, extensions, cross-agent and manual installs, upgrades, migration, and Claude Code cloud sessions.
- [Usage And Setup](usage.md) - invocation, commands, PixelLab MCP/API modes, and token safety.
- [Security And Trust](security.md) - access boundaries, public audits, release provenance, and scanner disclosures.
- [Blueprints](blueprint.md) - create, validate, share, and replay reusable workflows.
- [Resources](resources.md) - official PixelLab, Agent Skill, and project links.

## Showcase

- [Showcase](showcase/README.md) - examples of using Pip to route PixelLab requests, enhance prompts, generate assets, and document results.

## Examples

- [Minimal PixelLab Router Skill](minimal-pixellab-router.md) - compact standalone example that routes a PixelLab request to an exposed MCP tool or the documented REST v2 fallback.

## Benchmark

- [PixelLab Pip Skill Benchmark](pixellab-pip-benchmark.md) - reproducible agent-side context/token and routing-correctness comparison of the skill vs no skill vs the official mcp/docs injection.
- [PixelLab Static-Image Model Benchmark](pixellab-image-model-benchmark-results.md) - blind quality comparison and current routing summary for Pixen, PixFlux, Create Image Pro, and BitForge, supplemented by focused evidence that Pro is reliable for isolated reusable VFX while Pixen is not.
- [PixelLab Static-Image Model Style Fingerprint](pixellab-image-model-style-fingerprint.md) - blind style/failure-mode tagging of the benchmark's existing seed-7 outputs, used to validate the per-model profiles rather than re-rank them.

## Research

- [PixelLab Surfaces And Services](pixellab/pixellab-surfaces-and-services.md) - where MCP, REST v2, website/editor, Aseprite, Pixelorama, SDKs, and legacy v1 fit.
- [PixelLab Asset Routing](pixellab/pixellab-asset-routing.md) - how common requests map to PixelLab tools, endpoints, and workflows.
- [PixelLab Background And Wallpaper Model Research Spike](pixellab/pixellab-background-wallpaper-model-research-spike.md) - applied comparison of Pro, Pixen, PixFlux, and BitForge for wide environmental backgrounds and wallpapers, including the conditional BitForge finding.
- [PixelLab UI Generation Surfaces Research](pixellab/pixellab-ui-generation-surfaces-research.md) - current UI-specific matrix for MCP `create_ui_asset`, REST `/create-ui-asset`, REST `/generate-ui-v2`, shape pieces, elements, and website/editor boundaries.
- [PixelLab User-Facing Term To Backend Mapping](pixellab/pixellab-user-facing-term-backend-mapping.md) - production mapping of user-facing labels across REST v2, MCP, website/editor, Pixelorama, and Aseprite to endpoints, tools, and model/product terms.
- [PixelLab MCP vs REST v2 Route Parity](pixellab/pixellab-mcp-vs-rest-route-parity.md) - endpoint-level MCP/REST coverage matrix and the full inventory of missing features both ways: REST v2 endpoints with no MCP tool, and MCP tools with no REST v2 endpoint.
- [Pixel-Art GIF-Friendly Disappearance](pixellab/pixel-art-gif-friendly-disappearance.md) - prompt and QA guidance for GIF-friendly disappearance effects, 1-bit transparency, dithered cutout dissolves, particle dissipation, and export checks.
- [PixelLab Chibi Base Character Findings](pixellab/pixellab-chibi-base-character-findings.md) - live-generation findings for a reusable chibi avatar base character, including closest candidates, failed prompt/model patterns, and unresolved next tests.
- [PixelLab Pixen 128x128 Head-and-Shoulders Portrait Prompt Spike](pixellab/pixellab-pixen-portrait-prompt-research-spike.md) - terminology, 128x128 southwest-facing Pixen prompt comparisons, scale-anchor validation across three subject classes, and the reusable MVP blueprint.
- [PixelLab 16px Item Sprite Generation Spike](pixellab/pixellab-16px-item-sprite-generation-spike.md) - findings on why `16x16` full-cell tiles work better than strict `16x16` non-tile item sprites, including prompt comparisons, Aseprite style-reference observations, a pixen single-subject icon test (coins read well at 16px; the hollow-center background-removal artifact and its edge-flood fix), a Pro-vs-pixen 16px quality comparison (the missing detail/outline controls that make pixen cleaner at 16px while Pro wins at 32px+), and verification guidance.
- [PixelLab 32px VFX Atlas Density Spike](pixellab/pixellab-32px-vfx-atlas-density-spike.md) - controlled prompt findings for strict `16x16` atlases of transparent `32x32` explosion effects, including density failure analysis and safer assembly experiments.
- [PixelLab Character Aura Prompt Research Spike](pixellab/pixellab-character-aura-prompt-research-spike.md) - live `64x64` Pro and Pixen comparisons for modular front-facing character auras, including the reliable Pro prompt hierarchy and forty-three Pixen batches showing that occasional good outputs do not form a dependable effect-only workflow.
- [PixelLab Font Generation Spike](pixellab/pixellab-font-generation-spike.md) - live findings for REST `generate-font-pro`: async job shape, the TTF-vs-atlas distinction (`ttf_base64` is the real deliverable), current `glyph_px` controls and fixed pricing, `suspect_glyphs`, and the historical first `glyph_px: 8` test.
- [PixelLab Image Size Limits (Min And Max)](pixellab/pixellab-image-size-limits.md) - per-tool minimum and maximum size limits from the raw OpenAPI schema, why the Aseprite `32x32` minimum is a client-side editor limit, the schema-enforced `16px` floor (and the `8px`-only `glyph_px` exception), and per-endpoint max/area/aspect rules across REST v2 and MCP.
- [PixelLab API Pricing Model List](pixellab/pixellab-api-pricing-model-list.md) - current API pricing and model/tool list from PixelLab's official API catalog.
- [PixelLab Documentation Watch Cache](pixellab/pixellab-doc-watch-cache.md) - local-only watcher workflow for caching upstream PixelLab docs, detecting REST/MCP drift, and deciding when the Agent Skill needs updates.
- [PixelLab Changelog 2026-07-01](pixellab/pixellab-changelog-2026-07-01.md) - dated summary of the July 1 public-doc drift and corresponding PixelLab Pip routing/reference updates.
- [PixelLab Top-Down Tileset Transition Findings](pixellab/pixellab-topdown-tileset-transition-findings.md) - live-generation findings for `create_topdown_tileset` transition sizes, compact 4x4 graybox exports, and the `transition_size: 1.0` expanded-layout caveat.
- [PixelLab DualGrid Tileset Export System](pixellab/pixellab-dualgrid-tileset-export-system.md) - reverse-engineering notes for PixelLab's compact DualGrid/Wang tileset metadata, layout order, public tileset surfaces, and local simulator scope.
- [PixelLab 1-Bit Tileset Prompt Testing](pixellab/pixellab-1bit-tileset-prompt-testing.md) - simulator and live MCP findings for black-and-white top-down and sidescroller prompt tests.
- [PixelLab 1-Bit Tileset Optimization Workflow](pixellab/pixellab-1bit-tileset-optimization-workflow.md) - practical workflow for using simulator and live MCP tests to place white 1-bit edge, rim, ledge, and boundary pixels in top-down and sidescroller tilesets.
- [PixelLab Skeleton And Template Animation Research](pixellab/pixellab-skeleton-template-animation-research.md) - managed template animations, raw skeleton keypoint routes, Aseprite skeleton workflow parity, and MCP/REST boundaries.
- [PixelLab Oversized Background Animation Spike](pixellab/pixellab-oversized-background-animation-spike.md) - animating a background larger than the `animate-with-text-v3` `256x256` cap by looping regions and compositing them back at exact offsets: the chunk-boundary seam and why masked compositing is required, exact loop closure from identical `first_frame`/`last_frame`, subject-dependent brightness blowout, seed-only candidate selection, GIF global-palette and LAB/255-colour quantisation findings, and the Aseprite layer/composition build.
- [PixelLab Paperdolling Research Spike](pixellab/pixellab-paperdolling-research-spike.md) - research on RPG equipment layers, PixelLab composite/edit boundaries, layer extraction, skeleton hardpoints, and paperdoll QA.
- [PixelLab Paperdolling System Plan](pixellab/pixellab-paperdolling-system-plan.md) - staged implementation plan for a PixelLab-backed paperdoll package workflow, Python extraction prototype, previews, manifests, and engine exports.
- [Bark Sound Design Spike](bark-sound-design-spike.md) - how the bundled `bark.wav` is actually built (three partials at `f0 x [1, 2.1, 3.4]`, a descending perfect fourth, recovered by curve fit), the notification-sound and dog-bioacoustics research behind a possible replacement, the F0-vs-dominant-frequency conflict in the literature and its reconciliation, seven local candidate sounds with loudness-matched measurements and a provisional ranking, and the measurement methodology.
- [PixelLab Auth And Security](pixellab/pixellab-auth-and-security.md) - bearer-token handling and automation boundaries.
- [PixelLab SDK Compatibility](pixellab/pixellab-sdk-compatibility.md) - official SDK guidance and when to call REST v2 directly.
- [PixelLab Terminology](pixellab/pixellab-terminology.md) - product labels, endpoint labels, and terms agents should not over-interpret.
- [Official PixelLab MCP Service Comparison](tools/official-pixellab-mcp-service-comparison.md) - technical comparison between Pip and the official hosted MCP service.
- [PixelLab MCP Docs vs Pip Skill (Session Context)](tools/pixellab-mcp-docs-vs-pip-skill.md) - decision guide for choosing session context: the official mcp/docs link vs installing the Agent Skill.
- [PixelLab Aseprite Extension Coverage Audit](tools/aseprite-extension-coverage-audit.md) - comparison of official Aseprite editor workflows with Pip's MCP/REST/editor routing.
- [Aseprite CLI Integration Testing](tools/aseprite-cli-integration-testing.md) - maintainer QA policy for local Aseprite CLI workflow tests.
- [PixelLab AI Skill vs Pip Skill](tools/pixellab-ai-skill-vs-pip-skill.md) - feature comparison between Pip and the unofficial PixelLab AI Skill.
- [PixelLab 16px Chibi Character Generation Spike](pixellab/pixellab-16px-character-generation-spike.md) - smallest reliable prompt and route for a flat, low-detail 16px character with a cozy chibi read.
- [PixelLab Pixen Full-Body Character Prompt Spike](pixellab/pixellab-pixen-character-prompt-research-spike.md) - smallest description that reliably makes Pixen produce a 64px south-facing full-body idle character at default settings.
- [PixelLab Armless Character Prompt Research Spike](pixellab/pixellab-armless-character-prompt-research-spike.md) - whether `create_character` can produce a genuinely armless humanoid at 32px/eight directions, across long-to-minimal descriptions.
- [PixelLab 360 Rotation Spike](pixellab/pixellab-360-rotation-spike.md) - shortest `animate-with-text-v3` action phrase that yields a clean, seamless, constant-speed turntable with a stiff body.
- [PixelLab Idle Animation Artifact Research](pixellab/pixellab-idle-animation-artifact-research.md) - live findings on 9-frame idle loops from a small transparent frame, including the external effect marks that appear when `last_frame` is supplied.
- [PixelLab Multi-Shot Cinematic Spike](pixellab/pixellab-cinematic-spike.md) - live findings from chaining many `animate-with-text-v3` jobs into a seamless-looping minute-long cinematic, with the failure/mitigation catalog.
- [PixelLab Cinematic Inspiration And Technique](pixellab/pixellab-cinematic-inspiration.md) - composition and motion techniques for fixed-camera pixel-art cinematics, informing opening-frame prompts and per-shot action text.
- [PixelLab Cinematic Support Test Plan And Results](pixellab-cinematic-testing.md) - smoke and live test coverage for the multi-shot cinematic workflow, with the scoring rubric and results.
- [HD Region Edit / Animate Spike](pixellab/pixellab-hd-region-edit-animate-spike.md) - whether Pip should gain a selection-scoped workflow for editing or animating regions of images larger than the edit/animate size caps.
- [AI-Image Downscale And Pixel-Grid Recovery Spike](pixellab/pixellab-ai-image-downscale-grid-recovery-spike.md) - code-and-literature findings on recovering a crisp low-resolution grid from upscaled AI "pixel art", and when to decline.
- [PixelLab Skill Icon Generation Spike](pixellab/pixellab-skill-icon-generation-spike.md) - live findings and tested defaults for fantasy skill/ability/item icon sheet requests.
- [PixelLab Top-Down House Generation Routing Spike](pixellab/pixellab-top-down-house-generation-routing-spike.md) - observed failures and the successful fallback for a south-facing, genuinely top-down building asset.
- [PixelLab Credit Output Estimation Spike](pixellab/pixellab-credit-output-estimation-spike.md) - estimate of how many outputs 1 USD of credit buys per route, with the caveats that keep it an estimate.
- [PixelLab MCP New-Tools Verification Results](pixellab/pixellab-mcp-new-tools-test-results.md) - live verification run over the newly exposed MCP tools against the REST OpenAPI document.
- [Inline Negative Prompting Best Practices](pixellab/pixellab-inline-negative-prompting-best-practices.md) - current-model framing of negative prompting as anything telling the model what not to draw, whether in a dedicated field or the main description.
- [Inline Negative Prompting Current-Model Results](pixellab/pixellab-inline-negative-prompting-current-model-results.md) - Stage A results for Pixen and Create Image Pro, blind-reviewed with adjudication.
- [PixelLab Negative Prompting Research Spike](pixellab/pixellab-negative-prompting-research-spike.md) - what the repo, public docs, and the local generation archive actually establish about negative prompting.
- [PixelLab Negative Prompting Calibration Results](pixellab/pixellab-negative-prompting-calibration-results.md) - Phase 0 calibration for the historical dedicated-field study.
- [PixelLab Negative Prompting Phase 0B Results](pixellab/pixellab-negative-prompting-phase0b-results.md) - replacement-family calibration following Phase 0.
- [PixelLab Negative Prompting Phase 1 Confirmation Results](pixellab/pixellab-negative-prompting-confirmation-results.md) - historical dedicated-field confirmation on BitForge and deprecated PixFlux; zero weight in the current-model study.
- [RPG Maker Map-Character Sheet Formats](pixellab/rpg-maker-character-sheet-formats.md) - verified cell geometry, direction layout, and image-format rules from RPG Maker 2000 through MZ and Unite.
- [PixelLab Pip Preview App Research Spike](pixellab-preview-app-research-spike.md) - evidence and rejected options behind the proposed folder-scoped pixel-art preview app.
- [Pip Mascot](pip-mascot.md) - source design note for the Pip mascot's identity, silhouette, and production direction.

## Plans

- [Inline Negative Prompting Current-Model Test Plan](plans/pixellab-inline-negative-prompting-current-model-test-plan.md) - frozen protocol for the primary Pixen and Create Image Pro inline-prompt study.
- [Negative Prompting Controlled Test Plan](plans/pixellab-negative-prompting-controlled-test-plan.md) - frozen protocol for the historical dedicated-field study on BitForge and deprecated PixFlux.
- [MCP New-Tools Verification Plan](plans/pixellab-mcp-new-tools-test-plan.md) - scope and method for verifying newly exposed MCP tools against REST parity.
- [PixelLab Pip Preview App Plan](plans/pixellab-preview-app-plan.md) - design proposal for the standalone browser-based, folder-scoped preview app.
- [Top-Down South-Facing Building Prompt Plan](plans/pixellab-top-down-south-facing-building-prompt-plan.md) - protocol for finding the smallest prompt and lowest-cost route for a screen-aligned south-facing building sprite.

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
