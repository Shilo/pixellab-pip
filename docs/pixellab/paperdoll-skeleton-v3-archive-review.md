# Paperdoll and Skeleton v3 archive review

Reviewed 2026-11-01 against the current skill, the supplied archive, current public PixelLab documentation, and the connected MCP tool declaration. Three specialist reviewers covered animation contracts, paperdoll extraction, and finishing/diagnostics; the coordinating reviewer inspected the contact sheet, compared the changes with canonical guidance, and checked the combined result. No paid PixelLab calls were made.

## What the archive contains

The outer archive contains two Git patches, a nested ZIP with 18 replacement source/reference/test files, a review note, a three-row animation contact sheet, and an eight-pose JSON sequence. The patches target an older branch. Replacement files therefore served as proposals to inspect, not files to copy over current work. Patch author headers and local archive paths are not part of the shipped material.

The material covers managed Skeleton v3 custom motion, paperdoll layer extraction, two cleanup helpers, an experimental missing-prop diagnostic, and reported generation trials. The pose JSON uses managed pose fields such as pelvis, chest, and hand targets; it is not the raw Skeleton v3 endpoint's normalized COCO-18 joint sequence.

## Decisions

| Proposal / supplied files | Review outcome |
|---|---|
| Preset/skeleton reference and animation routing | Accept custom managed Skeleton v3 as an explicit option. Separate MCP written poses from REST text-generated motion; retain the ordinary PixMiniMax default. |
| Cost reference | Refresh managed Skeleton v3 frame bands from current public docs. The free MCP instruction response is distinct from the paid submission and from REST generation. |
| Key-pose reference | Add inspection of behind-body blade paths and a stepped-pose option when interpolation repeatedly invents an incorrect path. No automatic retry or mandatory engine switch. |
| Eight-direction reference | Keep existing guidance. Three tested directions do not establish eight-direction reliability or a generally safe mirroring rule. |
| Paperdoll reference and `paperdoll.py` | Replace heuristic extraction guidance with a smaller exact-overlay helper. Preserve RGBA, require matching registration, reject unreproducible alpha changes and edits outside an explicit region, and retain semantic visual review. |
| Paperdoll tests | Replace the archive's tests with meaningful roundtrip, alpha, registration, region, overwrite, dependency, animated-input, and failed-write checks for the accepted helper. |
| `outline_gaps.py`, finishing reference/tests | Do not add the helper. Two dark neighbors can sit on the same side of a bright edge tip; the algorithm still erases the highlight. Preserved alpha alone does not prove an outline repair. |
| `painterly_clean.py`, finishing reference/tests | Do not add the helper. It overlaps existing cleanup operations and has independently reproduced alpha, pixel-provenance, reporting, and overwrite defects. |
| `prop_gone` in measurement/planning/threshold files and its test | Do not add the diagnostic. Synthetic positives do not overcome its reported failure to detect the actual missing swords. Existing visual inspection remains necessary. |
| Animation-doctor reference | Correct hand-continuity guidance, including the existing report checklist: a cross-body swing can change screen side while retaining the same anatomical hand; an occluded grip is unverified. |
| Supplied evidence page, review note, image and pose JSON | Retain findings and limitations here. Do not install trial outputs as templates or treat reported charges and measurements as verified API guarantees. |

## Official contract checks

The [public MCP guide](https://api.pixellab.ai/mcp/docs) documents managed custom Skeleton v3, its free instruction call, subsequent pose submission, character-specific instructions, and shared motion across directions. The connected `animate_character` declaration exposes `poses`, `scale`, and `move`.

The raw [REST OpenAPI](https://api.pixellab.ai/v2/openapi.json) maps both `/animate-character` and `/characters/animations` to `CreateCharacterAnimationRequest`, whose properties lack those three controls. Its field descriptions specify action-text motion generation. Treating a REST submission without poses as the free MCP discovery step would risk unintended paid generation and would not preserve caller-authored poses. The [REST endpoint index](https://api.pixellab.ai/v2/llms.txt) confirms the public paths; MCP tool names are not REST paths.

Exact operational guidance lives in the [preset/skeleton reference](../../skills/pixellab-pip/references/preset-skeleton-template-animation.md); pricing lives in [cost routing](../../skills/pixellab-pip/references/cost-routing.md). Discovery instructions provide character-specific pose semantics; the archive's example coordinates are not a universal contract.

## Evidence strength and reproduced problems

The research note reports trials on 64px and 96px bases, including failed layer extractions, expensive key-pose attempts, and one custom slash rendered in east, north-west, and north. The contact sheet visibly supports missing sword sections in two east frames and one north-west frame. It does not establish whether a temporarily hidden grip changed hands. Raw frames, job receipts, run manifests, and before/after layer pairs were not supplied, so reported costs, palette counts, timing, pixel measurements, and comparative success rates remain third-party observations.

Local synthetic probes independently established these archive implementation problems:

- `painterly_clean --holes-only` changed nine alpha values from 128 to 255 while reporting zero hole repairs and marking no changes.
- Its median repair created RGB `(5, 5, 0)` from neighboring `(10, 0, 0)` and `(0, 10, 0)` pixels, contradicting a copied-source-pixels interpretation.
- Its marks-output path could overwrite another source image: a 5×5 input became a 45×15 inspection image and the command exited successfully.
- `outline_gaps` replaced an intentional bright edge tip even when its two dark neighbors did not bracket a gap.
- The proposed paperdoll helper hardened alpha, used replacement rather than source-over composition, and allowed filters or recoloring to exempt changed pixels from faithful reconstruction checks. Its output handling also lacked the current shared collision and image-input guards.

The accepted extractor deliberately does not guess equipment from color, remove drift or slivers, realign independently generated poses, or reconstruct hidden back layers. Exact recomposition proves an overlay reproduces the edit; it cannot prove that changed pixels depict only the requested equipment. A full-body redraw can also recompose exactly and must fail visual review.

## Validation boundary

The accepted changes require repository QA and the pinned static scanner comparison described in [scanner maintenance](../developer/scanner-maintenance.md). Focused extraction tests exercise the new helper's actual CLI and failure paths. Archive probes run only on local synthetic copies. These checks do not establish live generation quality, eight-direction reliability, or a hosted security-audit result. Ignored `.local/friend-pack-review/` contains the source snapshots, specialist reviews, probe results, and validation logs for this review session.
