# Animation Prompting Reference Review

Reviewed: 2026-10-05.

**Decision:** retain the existing animation contract and make two small additions: distinguish a textual storyboard from actual per-frame controls, and explicitly preserve opaque scene backdrops on PixMiniMax. Do not import the supplied reference wholesale or create another runtime prompting guide.

## Scope and evidence

The supplied document, *Pixel Lab Animation Prompting: PixMiniMax and Animate with Text V3*, is a user's workflow reference rather than a skill or an authoritative API contract. Its instruction to output only a prompt belongs to that document's intended workflow; it did not govern this review.

The review checked the complete document against fresh public [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json), the [MCP tool guide](https://api.pixellab.ai/mcp/docs), the connected raw-animation tool descriptors, the [Pro website tool page](https://www.pixellab.ai/docs/tools/animate-with-text-pro), and the repository's canonical animation, prompt-length, image-role, cost, and text-preparation rules. An independent read-only agent challenged the prompting and experimental claims.

Local checks inspected both request schemas, measured every fenced prompt example, parsed the JSON examples, and recomputed the v3 pixel-budget table. All six schema assertions passed. These are schema and text checks, not new server-validation or generation experiments. Existing paid studies supplied the visual counterexamples; no new paid calls were necessary. **Spend: 0 of the authorized 2,000 units.**

The document's `[tested]` tags are self-reported observations. No fixtures, request logs, model versions, seeds, attempt counts, output frames, scoring method, or comparisons accompany them. They can suggest hypotheses but do not establish general fixes or failure causes.

## Concrete contract errors and omissions

| Claim or omission | Finding | Consequence |
|---|---|---|
| Raw PixMiniMax takes required `action` | REST and MCP use required `description`. | The advertised REST request would omit a required field and include an unsupported one. |
| V3 requires `image_size` | The raw REST request has no such field; dimensions come from the supplied image. Both raw request schemas disallow additional properties. | Adding this field makes the request invalid against the published schema. |
| PixMiniMax `view` examples are `top-down` and `side view` | The enum is `low top-down`, `high top-down`, or `side`. | Those examples are not valid field values. |
| V3 allows 4–16 frames, without an even-number rule | Even counts are required. | Values such as 5 or 15 are invalid despite falling within the stated range. |
| Structured JSON gives direct pacing control | Neither text-animation request exposes `frames`, `loop`, `theme`, `animation_type`, or `style_constraints`. | As a request body, that JSON lacks required inputs and has unsupported fields. Serialized inside the motion string, it is descriptive text with no documented frame-by-frame binding. |
| Ambient-scene examples omit background handling | PixMiniMax defaults to cutting out opaque backdrops. | Use `no_background=false` when the opaque scene composition must remain. Prose asking buildings and sky to stay fixed does not replace this control. |
| End-frame and correction controls are omitted | Both REST routes support `last_frame` and `drift_threshold`; current v3 REST also supports enhancement. | A prompt-only troubleshooting method overlooks existing controls. Their canonical behavior and risks are already documented in the skill. |

These findings follow the refreshed REST schema and MCP guide above. MCP and REST use different image-input field shapes; the supplied REST-oriented table should not be copied directly into an MCP call.

### Ready-to-paste examples fail the length check

Both raw REST motion fields permit at most 1,000 characters. Character counts below exclude surrounding fences and leading/trailing whitespace; JSON compact counts use serialization without indentation.

| Complete PixMiniMax example | Characters | Compact JSON characters | Fits REST limit? |
|---|---:|---:|---|
| 16-frame ambient prose | 1,058 | — | No |
| 24-frame two-sword prose | 2,001 | — | No |
| 8-frame ambient JSON | 1,512 | 1,400 | No |
| 12-frame projectile JSON | 2,077 | 1,925 | No |
| 16-frame rotation prose | 749 | — | Yes |

The generic JSON skeleton is a template, not a complete example: it declares 16 frames but contains one placeholder entry. It should not be evaluated as a ready request. No length guarantee is inferred for MCP from REST's bound; see [Prompt Limits](../../skills/pixellab-pip/references/prompt-limits.md).

The v3 pixel-budget table is correct: at square sizes 64, 128, 192, and 256, the usable maxima are 16, 16, 14, and 8 even frames. PixMiniMax's 4–40 multiples-of-four range and Tier 1+ beta requirement also agree with the current public contract.

## Challenge of the behavioral advice

| Advice | Assessment |
|---|---|
| Prefer PixMiniMax whenever a precise loop seam matters | Unsupported as a general default. The [paired study](pixellab-pixminimax-vs-v3-animation-spike.md) found v3 reached a distinct end anchor exactly while PixMiniMax differed in 15,471 pixels. In a same-anchor case, PixMiniMax differed in 956 visible pixels while v3's differences were confined to invisible RGB. These limited samples challenge a blanket preference; they do not establish a universal v3 winner. |
| Identically worded first/last descriptions fix seams | Text equality is not pixel equality or smooth approach to the endpoint. Inspect the middle frames, last-to-first transition, and actual playback. The paired study's same-anchor request also had a prompt/frame-count mismatch, so its exact outcome cannot isolate the cause. |
| Frame zero is always unchanged; drop a duplicate to fix loops | The documented echo convention needs verification. The [tiny-flame study](pixellab-inline-negative-prompting-new-tool-results.md) found no pixel-exact first-frame echo in 50 PixMiniMax calls. Dropping a frame changes playback and can introduce a jump; preserve raw output and follow the skill's existing approval and duplicate-verification rules. |
| Palette, pose, and camera sentences are reliable locks | They are guidance, not enforced constraints. The tiny-flame study found detached components in all three baseline, direct-exclusion, and positive-comparator clips. That tests effect suppression, not every palette lock, but it does not support treating lock sentences as guaranteed fixes. |
| Enhancement should be off for a complete prompt | Sensible for explicit text, already covered by Text Preparation. Enhancement can alter constraints: the tiny-flame study's enhancer dropped exclusions in 3/3 tested requests. Do not infer it preserves every intended restriction. |
| Stating a grid preserves independent cells | V3's [atlas risk](../../skills/pixellab-pip/references/animation.md#atlas-animation-risk) is already characterized. No reproducible PixMiniMax atlas evidence accompanies this claim. Synchronized motion does not establish independent cell identity or boundary preservation. |
| Speed comes only from allocating fewer frames to a beat | Generated phase allocation remains soft guidance. Displayed speed also depends on playback duration/FPS. The 25/15/10/25/25 percentage recipe is a heuristic, not an API timeline. |
| V3 wants 5–12 words and no more than two qualifiers | A useful concision preference, not a documented word-count limit. Its own dual-sword example contains ordered choreography and several qualifiers. V3 REST can enhance a short phrase into richer motion text. |
| Every seamless loop needs at least 16 frames | Unsupported as a universal requirement and inconsistent with the supplied 8-frame loop example. Preserve requested/default counts; more frames alone do not close a seam. |
| Flash effects are superior to fluids; holds cannot work; black frames must never be used | Unverified preferences or absolutes. They need task-specific comparisons before becoming runtime policy. An intentionally black frame or a fluid effect can be a valid user requirement. |
| Generate several times and keep the best | A possible approved experiment, not permission for unbounded rerolls. Existing [cost rules](../../skills/pixellab-pip/references/cost-routing.md) retain budget and attempt control. |

Other inconsistencies reduce confidence in the prescriptions: JSON is recommended for 24–40 frames but demonstrated at 8 and 12; the one-mover rule is followed by a three-layer ambient example; and the ambient prose forbids lighting changes while brightening a star. Some can be reconciled as context-dependent preferences, which is precisely why they should not be global rules.

## What is useful, and where it belongs

Concrete paths and destinations, ordered motion phases, an explicit in-place requirement, reference-grounded captions, and inspection of the middle frames are useful advice. They substantially overlap existing [Animation](../../skills/pixellab-pip/references/animation.md), [Image Input Roles](../../skills/pixellab-pip/references/image-input-roles.md), and [Text Preparation](../../skills/pixellab-pip/SKILL.md#text-preparation). Longer multi-phase motion is a reasonable PixMiniMax candidate; neither choreography nor an ambient scene guarantees better loop closure. The Pro website page describes a separate tool configuration and does not redefine raw v3 limits.

Two changes were made in the canonical animation reference:

1. Explain that a textual or JSON storyboard is not a documented per-frame control, and point to Skeleton v3 for actual caller-supplied pose inputs when appropriate. This does not promise exact rendered pixels from a skeleton.
2. State PixMiniMax's background-removal default and the explicit setting needed to retain an opaque scene backdrop.

No word-count policy, frame-allocation recipe, generic lock library, JSON format, automatic reroll workflow, or new route preference was added. A controlled compact-prose-versus-compact-JSON study, or a visible-part-versus-ambiguous-limb study, could investigate the remaining hypotheses. The current evidence does not require spending the user's allowance on either experiment to make these contract corrections.
