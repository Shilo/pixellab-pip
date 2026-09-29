# Inline Negative Prompting on PixMiniMax and Pro Flash: Results

**Study date:** 2026-09-28 to 2026-09-29

**Status:** all registered generation calls completed; visual/statistical conclusions are preliminary because the planned independent rating process was not completed.

## Decision

The study found **no validated general benefit** from inline exclusions on PixMiniMax or the five tested Pro Flash operations. The registered thresholds classify all 54 negative-involving contrasts as inconclusive:

| Registered contrast verdict | Count | Share |
|---|---:|---:|
| Beneficial | 0 | 0% |
| Harmful | 0 | 0% |
| Proven no meaningful effect | 0 | 0% |
| Inconclusive | 54 | 100% |

These are evidence classifications, not outcome frequencies. The sample has only three matched blocks for most contrasts and two for the induction checks. The data cannot establish equivalence or reliably distinguish modest benefit from harm. In particular, **100% inconclusive does not mean 100% no effect**.

Two task-specific observations show why a blanket recommendation would be premature:

- In the PixMiniMax flame task, the registered no-sparks wording and baseline both failed in all 3/3 clips. A warm-color connected-component screen flagged detached components in every core arm; it is a supporting heuristic, not a semantic spark detector.
- In one Pro Flash edit task, visible `OX7` remnants occurred in 2/3 baseline outputs and 3/3 outputs with an inline exclusion. Across the three paired blocks, the exclusion was better in 0/3, worse in 1/3, and tied in 2/3. This is a small directional regression, not statistically established harm.

**Practical recommendation:** do not add negative boilerplate by default. Describe the desired result positively, and try one short exclusion only when addressing a specific, reproducible failure. Inspect the output. For PixMiniMax, leave prompt enhancement off when a constraint must survive, or inspect the returned expanded prompt.

## What Was Tested

The experiment covered six public operations. REST was the primary surface; MCP received one matched baseline and negative call per operation as a forwarding and output-shape check.

| ID | Operation | REST calls | MCP calls | REST reported units | MCP estimated units | REST coverage |
|---|---|---:|---:|---:|---:|---|
| PM | PixMiniMax animation | 50 | 2 | 50.45 | 2 | Flame core, robot-walk secondary task, forbidden-noun sentinel, enhancement-on comparison |
| PF-I | Pro Flash image creation | 41 | 2 | 205 | 10 | Pictogram sign core, crossed-swords secondary task, forbidden-noun sentinel |
| PF-C | Pro Flash character creation | 41 | 2 | 287 | 14 | Ranger core, two-pouch secondary task, forbidden-noun sentinel |
| PF-O | Pro Flash object creation | 32 | 2 | 160 | 10 | Signpost core and forbidden-noun sentinel; no secondary task |
| PF-E | Pro Flash edit | 41 | 2 | 205 | 10 | Sign restoration core, clean-sky secondary task, forbidden-noun sentinel |
| PF-P | Pro Flash inpaint | 41 | 2 | 205 | 10 | Masked sign restoration core, pictogram secondary task, forbidden-noun sentinel |
| **Total** |  | **246** | **12** | **1,112.45** | **56 estimated** |  |

The run returned 975 images or animation frames: 933 from REST and 42 from MCP. All outputs are present in the ignored run archive. The REST amount is provider-reported, including 0.45 units for PixMiniMax prompt enhancement. MCP completion responses did not return usage; its 56 units are estimates from the frozen cost forecast. The combined budget-accounting basis is **1,168.45/2,000 units**, leaving **831.55 units**. This is not an account-balance delta.

The PF-O secondary task was omitted because its frozen route cap was 200 units. The completed core, sentinel, and MCP calls used or reserved 170 units; its three-arm, three-block secondary task was estimated at another 45, which would exceed the route cap. The global remaining allowance does not override a route cap.

## Results by Question

### Core exclusions and wording variants

The frozen core compared baseline (`B0`) against direct `No X` (`N0`), `without X` (`NW`), `Avoid X` (`NA`), `Exclude: X` (`NE`), a longer exclusion list (`L1`), a positive replacement (`P1`), and a combined positive-plus-negative instruction (`CP`). Calls were matched by seed/block where supported. Frames and character directions were treated as nested outputs, not independent samples.

The Pro Flash contact-sheet screen showed few baseline failures on several tasks, leaving limited room for an exclusion to improve them. No negative form met the preregistered benefit threshold on any route. The one legible adverse direction was the PF-E secondary task described below. Because the numeric rating template was not completed and each comparison has only three blocks, there is no defensible route-wide percentage for which wording “works.”

### PixMiniMax flame and enhancement

The primary task asked PixMiniMax to animate an irregular flame in place without detached sparks, smoke, symbols, or duplicate flames. For the no-sparks target, baseline and `N0` each failed in 3/3 clips; the positive comparator and the other core arms also showed detached warm-color components in all three clips. No reduction was observed for inline exclusions.

When prompt enhancement was enabled, the returned expanded text dropped the negative clauses in **3/3** `N0` requests. This establishes a preservation risk in the enhancer output, not that it made the rendered result worse. Keep `enhance_prompt=False` when the exclusion must be carried through, or review the returned prompt before relying on it.

The PixMiniMax operation returned nine frames per call across 50 REST calls. In **0/50** calls was output frame zero pixel-identical to the fixed input; the measured difference was 293–512 of 512 pixels (mean 332.42). Treat the returned frame sequence as output and preserve the source separately; do not assume the first returned frame is an exact source echo.

### Pro Flash edit: small adverse direction

On the secondary sign-restoration task, baseline left visible `OX7` marks in 2/3 outputs. Adding the unrelated clause `No red balloon in the upper-left sky` left visible marks in 3/3 outputs. By paired block, the negative-clause version was better in 0/3, worse in 1/3, and tied in 2/3. The positive rewrite was clean in 1/3, ambiguous in 1/3, and failed in 1/3. Since the negative clause concerned the empty sky rather than the sign lettering, this is a small incidental adverse direction, not direct evidence that a “no letters” exclusion harms text removal.

This is a directional signal that the exclusion did not help this edit, with one extra residual-mark failure. It is too small to classify as reliable harm, and it does not establish that inline exclusions generally impair Pro Flash.

### Forbidden-noun induction sentinel

The registered absent target was a red balloon, with a different absent noun as the unrelated negative control. Each of six operations received two calls per condition, for 12 call-level observations per condition. Results were:

| Condition | Red balloon present | Decoy target present |
|---|---:|---:|
| Baseline (`B0`) | 0/12 | — |
| Inline `No red balloon` (`I1`) | 0/12 | — |
| Unrelated negative (`Q1`) | — | 0/12 |
| Positive balloon request (`Pcap`) | 12/12 | — |

The negative wording did not induce the named target in this sample, and the positive controls show all six operations could produce it. These call counts include animations and multi-view character outputs as one call each; their frames/directions are not additional independent observations.

### Inpaint integrity

All **43** PF-P REST and MCP results preserved every pixel outside the 798-pixel white mask exactly: zero changed pixels among the 8,418 outside-mask pixels in every result. This verifies the operation’s preservation behavior; it does not show that negative wording improved the patch.

## Percentage Method

The denominator of 54 includes the registered negative-involving comparisons most relevant to “does adding negative wording help?”: 30 core pure-exclusion comparisons (`N0`, `NW`, `NA`, `NE`, and `L1` versus `B0` over six operations), six core combined-strategy comparisons (`CP` versus its positive-only counterpart `P1`), five secondary `N0` versus `B0` comparisons, 12 induction comparisons (`I1` and `Q1` versus `B0` over six operations), and one PixMiniMax enhanced-`N0` versus `B0` comparison. Positive-only comparisons to baseline, the other registered wording-to-wording comparisons, and MCP parity calls are not counted in these four shares; MCP checks forwarding, not efficacy.

The frozen rule required at least a 20-point reduction in target failures with an interval excluding zero and no material quality loss to label a contrast beneficial. Harm required a corresponding statistically supported increase or a quality loss confirmed across blocks. “No meaningful effect” required the full interval to fit inside ±10 points and quality within ±0.5. Every other case is inconclusive. With three matched blocks (two for induction), and without the planned independent numerical ratings, no contrast could meet the evidence threshold. Observed ties are reported separately; they are not equivalence findings.

## Interface and Model Identity

The current public REST and MCP schemas for these operations accept a `description` field but do not expose a dedicated `negative_prompt` or equivalent field. No unsupported property was sent. Therefore there is no explicit-field generation result; the finding is that this feature is absent from the tested documented interfaces.

PixelLab's hosted tool guide defines PixMiniMax's `description` as motion-only and documents an optional prompt enhancer. The study followed that wrapper contract; MiniMax H3's general video-prompt advice was not treated as a separate PixelLab field or capability. PixelLab's live MCP tool metadata calls PixMiniMax “Powered by MiniMax H3.” The Pro Flash capabilities response recorded in the run archive reports `provider_model=gpt-image-2.5-flare`. These are service-provided labels, not independent verification of the underlying models. The available metadata gives no support for the claim that Pro Flash is secretly MiniMax; the experiment cannot inspect hidden routing or internal prompts.

## Limits and Deviations

- The plan called for two independent reviewers and adjudication. In practice, one AI reviewer inspected the randomized opaque-ID contact sheets; the second review and adjudication were not performed. The per-call ratings template remains blank, so the visual review is not a reproducible double-rated dataset.
- Most treatment arms have only three matched calls, and the induction has two. Outputs are diverse even under matched seeds; these results do not support broad claims about all prompts, dimensions, or future model versions.
- The PF-O secondary task was not run because it exceeded the frozen route cap, as described above.
- Four initial read-only character/object polling attempts lacked required IDs and were rejected before a generation call. The corrected reads succeeded; there was no generation retry or usage from those attempts.
- The live preflight and exact requests are preserved, but there was no final account-balance snapshot. MCP usage remains estimated.

## Reproduction and Sources

The ignored archive `pixellab-pip-generations/negative-prompting-new-tools-20260928/` contains the frozen protocol and prompt matrix, REST and MCP requests/results, responses, output images, fixture files and hashes, blinded contact sheets, and `run-summary.json`. The main per-call files are `completed-results.jsonl` and `mcp-results.jsonl`; signed download URLs were removed. The research and plan remain in ignored `.local/negative-prompting-new-tools-plan-2026-09-28.md`.

Sources checked against the public interface:

- [PixelLab API catalog](https://www.pixellab.ai/pixellab-api) — names PixMiniMax and labels its plugin tool “Powered by MiniMax H3.”
- [PixelLab REST v2 OpenAPI](https://api.pixellab.ai/v2/openapi.json)
- [PixelLab hosted MCP tool guide](https://api.pixellab.ai/mcp/docs) — documents the PixMiniMax motion `description`, `enhance_prompt`, and Pro Flash operation parameters.
- [MiniMax H3 official video prompt guide](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md) — consulted as background; PixelLab's exposed PixMiniMax motion field remains the operative prompt contract.
- [Project Pro Flash route reference](../../skills/pixellab-pip/references/pro-flash.md)
- [Project animation route reference](../../skills/pixellab-pip/references/animation.md)
