# Animation Model Routing Review

Reviewed: 2026-11-01.

## Finding

The reviewed instructions did not make Skeleton v3 the default. They did make ordinary text animation default to v3, while a competing “named motion” router and preset-label mappings could send ordinary idle, walk, run, hurt, or cast requests to skeleton-guided **template** mode. PixMiniMax was generally an explicit opt-in, except when raw frame/canvas requirements exceeded v3's limits.

The connected `animate_character` descriptor also auto-detects template mode when a template ID is supplied and v3 otherwise. Omitting `mode` therefore does not select PixMiniMax. Template and Skeleton v3 are different modes; both can use named template clips. Without the reported user's actual request and tool-call log, this review cannot establish which mode produced their rigid animation.

The preset reference compounded the problem by directing agents to raise template `ai_freedom` before switching engines when motion looked rigid. That control applies to template mode, not Skeleton v3.

## Evidence and decision

The review checked the runtime router, animation, preset/skeleton, cinematic, cost, paperdolling, and eight-direction references against the current public [MCP guide](https://api.pixellab.ai/mcp/docs), [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json), and connected tool descriptions. The baseline revision was `9af2fb899bcf4aea1f785ca43c5b51d4c745baa6`.

PixelLab still advertises v3 as its general API starting point. The change to prefer PixMiniMax is **Pip's routing policy**, following the requested preference, rather than a claim that PixelLab has changed its default or that PixMiniMax always produces better motion. The existing [paired comparison](pixellab-pixminimax-vs-v3-animation-spike.md) found clearer multistage actions in some PixMiniMax samples, but also stronger unwanted effects and less exact end-anchor matching. It did not compare Skeleton v3 and does not establish a universal quality ranking.

The canonical engine policy now lives in [Animation → Route Choice](../../skills/pixellab-pip/references/animation.md#route-choice):

- Ordinary managed-character animation explicitly sends `mode="pixminimax"` and action text without a template ID. Ordinary raw-image motion uses `animate_image_pixminimax` or REST `animate-pixminimax`, including creatures, props, scenes, and tweens.
- Explicit engine, template, and skeleton/keypoint requests retain their requested route. Character creation can still use v3; that does not select the animation engine.
- Exact counts such as six or ten generated frames use v3 when no engine was named and v3's limits fit. Explicit PixMiniMax plus six frames is a constraint conflict, not permission to round or switch.
- Cost-sensitive routing can choose a cheaper suitable engine after explaining the motion/cost tradeoff. A template is no longer selected just because an action has a catalog mapping.
- Stored object animation remains `animate_object(mode="v3")`: that tool exposes only v3 and Pro. Explicit PixMiniMax object requests can animate a fetched object frame through the raw route, with disclosure that the clip is separate from the managed animation library.

The change retains backdrop handling, input-echo checks, frame-order protection, end-anchor verification, direction scope, and paid-retry gates. A rigid template result can lead directly to an offered free-form animation; another template attempt is no longer mandatory.

## Offline subagent smoke tests

Two subagents first consumed the original skill and required runtime references, then repeated their cases against the revised files with additional edge cases. They selected tools and arguments using placeholder inputs; they did not execute calls, access credentials, or evaluate generated art.

The original 12 cases reproduced ordinary character template selection and raw/custom v3 defaults. None selected Skeleton v3 without an explicit skeleton request. The revised suite covered 22 prompt cases:

| Prompt family | Before | After |
|---|---|---|
| Wizard idle/walk; managed dog running | Template IDs inferred from ordinary action words | Explicit managed PixMiniMax, action text, no template ID |
| Managed knight sword attack; ordinary hurt/cast | v3 custom or catalog-template discovery | Explicit managed PixMiniMax |
| Loose slime jumping; two-pose tween | Raw v3 | Raw PixMiniMax with supplied frame anchors |
| Raw 24-frame animation | PixMiniMax capacity exception | PixMiniMax default |
| Exact six generated frames | v3 | v3; ten-frame case also verified |
| Explicit Walk template; explicit v3; explicit PixMiniMax | Requested engine or template | Requested engine or template retained |
| Cheapest managed walk with tied documented costs | Template favored by cost table | PixMiniMax retained; no cheaper-route reason to switch |
| Managed chest opening | Managed v3 | Managed v3; explicit PixMiniMax uses a disclosed separate raw clip |
| Supplied Skeleton v3 keypoints | Raw Skeleton v3 | Raw Skeleton v3 retained |
| Looping scene with five-generation cap | v3 | PixMiniMax within cap; reject a six-generation clip |
| Opaque scene animation | Route-dependent background default | PixMiniMax with explicit `no_background=false` |
| Explicit PixMiniMax plus six frames | Not in baseline suite | Block before spending; explain incompatible count |
| Explicit legacy interpolation-v2 | Not in baseline suite | Documented REST interpolation-v2 retained |

A third, independent reviewer checked the final diff and five additional offline cases: equipped managed-character movement through the eight-direction reference, raw paperdoll animation, MCP-unavailable REST routing, an explicit managed Skeleton v3 template, and the explicit PixMiniMax/six-frame conflict. All five retained the intended route or blocker. Duplicate engine-policy wording in the preset reference was removed after review.

These 27 checks are model instruction-following smoke tests, not an automated router implementation or live quality benchmark. Missing motion, invalid inputs, and explicit engine/count conflicts remain legitimate blockers. No new generations were requested and no PixelLab credits were spent.

## Fresh public-contract audit (2026-11-02 UTC)

Rechecked commits `ec262db` and `6bf62b0` against the complete seven-source refresh, with `e89ed59` as the synchronized checkout baseline. The [parity guide](pixellab-mcp-vs-rest-route-parity.md) records the full upstream inventory and unrelated room/pricing/validation changes. The recent paperdoll rollback follow-up is retained; this refresh changes documentation, not those helper implementations.

The central custom-animation distinction in `6bf62b0` is correct: both REST aliases reference `CreateCharacterAnimationRequest`, which forbids additional properties and has no `poses`, `scale`, or `move`. Its current mode description explicitly generates one shared 3D motion from action text. The public MCP guide independently documents those three fields and a free instruction-discovery call before paid rendering. The generic REST endpoint descriptions still omit Skeleton v3 and contain older defaults; the exact shared schema controls this conclusion. Managed and raw skeleton price bands are also supported by the guide, rather than inferred from the archive's reported spend.

The gap was in discovery and selection: SKILL.md and animation.md still led a managed Skeleton v3 request through `template_animation_id`, and custom guidance described a multi-direction use case as though that were necessary. A single direction is a valid custom use case. The new canonical choice is custom for an explicit Skeleton v3 request on a managed humanoid, with requested presets and raw keypoints preserved. Another body plan, unsupported count, or an unregistered raw sprite needs a supported plan before generation; none authorizes an implicit engine switch or extra character-import charge.

This accepts the proposed preference as **Pip policy**, not a conclusion that custom Skeleton v3 wins a quality benchmark. The public contract establishes control and shared-direction reuse. The older raw-keypoint/preset trials and archive contact sheet do not establish superiority of the new managed custom workflow. No paid experiment was needed to verify schemas or repair routing; visual quality, exact authored-pose adherence, loop closure, gear preservation and cross-surface pixel equivalence remain output checks.

The review also keeps the existing boundaries: character v3 creation does not choose its animation engine; ordinary motion remains PixMiniMax when constraints fit; managed objects retain their own supported modes; exact-count conflicts cannot be rounded away; anatomy cannot be inferred from screen-side crossings; independently generated paperdoll frames cannot be assumed to align. Detailed authoring rules remain in the [single operational reference](../../skills/pixellab-pip/references/preset-skeleton-template-animation.md#skeleton-v3-custom-motion-managed).


An independent read-only reviewer reconstructed the refreshed contracts, challenged the recent animation commits and current diff, and ran 19 additional model instruction-following dry runs with placeholder inputs. Cases covered ordinary managed/raw motion, custom Skeleton v3 at 3/15/16 frames, explicit presets, quadrupeds, raw keypoints, missing poses/client support, REST exact-pose requests, group reuse, managed objects, six-frame conflicts, and room view/piece constraints. The selected routes or blockers preserved the intended scope; these were not executed requests or a quality benchmark. Review found stale template-only current research and an MCP-only Pro Flash context ceiling stated too broadly; both were source-checked, narrowed, and independently rechecked. No actionable defect remained in the refresh-owned changes.
