# PR #11: challenged response to Claude's review

Review input: Claude's independent review of `9ee2e8bb97ebc6dd5cd5ddf322b2e36915af9f0a`. The complete supplied review remains a private attachment; this response deliberately omits its machine paths. The PR must remain unmerged.

Three independent reviewers challenged the Auto/config, panel/host and helper/routing findings before implementation. A finding's defect, severity and proposed fix are separate judgments. This record supersedes affected decisions in the earlier panel/Auto reconsideration; earlier validation remains historical evidence for its pinned revision.

## Plan and finding dispositions

| Finding | Challenged conclusion and implemented resolution |
|---|---|
| F1 | Accept discovery gap. Offer the panel at the pose-review checkpoint when an actual presentation is available; preserve normal image review and avoid unused files. |
| F2 | Accept all-or-nothing rendering defect. Render bounded PNG strips at a shared pixel scale, preserve supported images when others are GIF/oversize, and diagnose missing previews individually. Native review requests require all selected review images visible. |
| F3 | Accept demonstrated sound/config regression. Any parsed JSON object is authoritative; normalize only the sound value. Preserve Auto, unrelated fields and restrictive policy. Truly malformed/non-object JSON still fails closed. |
| F4 | Accept useful capability loss, refine proposed behavior. A run cap narrows enabled Auto; Auto off still asks, and explicit ask-first/plan-only/content checkpoints remain authoritative. Stop at cap/retry limits rather than silently increasing them. Permit an explicit task with the structured command without making ambiguous numeric arguments permissive. |
| F5 | Accept truncated HTTP failure in both job and direct-URL paths. Catch protocol exceptions and retain recovery/no-resubmit guidance. A double charge is an indirect agent risk, not a demonstrated charge. |
| F6 | Accept missing full-view access. One button opens only the validated helper-generated standalone HTML through a fixed, shell-free helper call. No arbitrary file launcher or project scan. Unsupported environments retain the exact manual path. |
| F7 | Partially accept complexity concern; reject silent restriction deletion on ordinary on/off commands. Unreleased status does not erase current users' saved budget expectations. Keep a narrow explicit reset and fail-closed legacy notice; simplify configuration handling/prose without a new migration framework. |
| F8 | Accept native presentation clutter. Show meaningful project/style/usage/image-role information and concise requests. Hide raw identifiers from the view but retain full project/content identities in a compact draft context block. |
| F9 | Accept misleading reload control. Remove it; rebuild a snapshot to refresh. Retain independent stale-content verification and tests. |
| F10 | Accept private-output gap. Write an exclusive per-panel `.gitignore` containing `*` before private payloads, with collision/alias protection. Do not change the generations root or overwrite user ignore rules. |
| F11 | Reject blanket bridge/fragment deletion. The available official bundled visualization contract documents the exact follow-up bridge, confirmation and fragment limit; the user requested Codex interaction. Retain actual-capability checks and click-only behavior, and distinguish documented/simulated support from an unperformed live-host check. |
| F12 | Accept automated native-test gap. Add a pinned real Claude validator/test invocation to existing CI, without a new Node project, account sign-in or model calls. |
| F13 | Accept defensive missing-element handling. Guard an absent native input and disclose the host limitation; simulated missing-input tests do not establish live mobile support. |
| F14 | Accept inconsistent native bound. Align with the host's 4 MiB limit in UTF-8 bytes while retaining larger portable HTML selections and explicit fallback. |
| F15 | Partially accept claims/onboarding gap. Clarify native stills versus full HTML GIF/zoom support; restore a short empty welcome with guided-project/setup drafts. Do not restore automatic project/policy writes. |
| F16 | Accept missing locked writer, reject removing audit requirements. Charged/committed sums do not record approved scope, retry consumption or resume context. Add one small transaction-backed plan-metadata operation to the existing manifest helper, not another store or runner. |
| F17 | Accept missing explicit dry intent. `--dry`, dry-run or a free preview/plan-only request spends nothing, regardless of Auto. |
| F18 | Partially accept discoverability concern. Existing blueprint intent already exposes matching recipes; add direct optional links from the relevant workflows, retaining schema validation and the distinction between replay and visual references. No new paid route or claim of live recipe-schema validation. |
| F19 | Accept inaccurate error wording. Report an invalid config without assuming it is always higher priority. Preserve damaged bytes. |
| F20 | Accept small routing ambiguity and duplication. Palette/reference advice must not imply mandatory Pro generation. Keep operation-specific reference pointers and remove repeated global opt-in rules. |
| F21 | Accept CLI error boundary. Handle bad dimensions and indivisible sheets in `fix.py`'s argument/error handling, not by invoking an unavailable parser from the frames library. Preserve sources and avoid partial outputs. |
| F22 | Accept small packaging/language improvements. Move native-only DTOs into the Claude adapter; use explicit validated language metadata rather than inferring a locale from translated strings. |

## Ownership and implementation sequence

1. Auto worker owns `bark.py`, config tests and Auto/Bark references. Helper worker owns downloader/doctor fixes, manifest metadata/tests, usage reference and recipe/routing pointers. Native worker owns Claude adapter/types/tests and the pose checkpoint. Parent owns shared panel Python/HTML/labels/tests, CI, README and decision records. No worker reverts another's edits.
2. Agree the small manifest metadata contract and panel opener/label interface before implementation. No paid PixelLab calls or modifications to real user settings.
3. Add regressions from demonstrated failures, run focused tests and inspect real browser interactions. Use a real patched image dependency; never substitute a version-string shim for dependency validation.
4. Cross-review the integrated changes, debate counterexamples, fix accepted material defects, and repeat affected verification. Run full repository QA, actual native tests and published checks for the exact final head. Keep live-host gaps explicit and leave the PR unmerged.

## Evidence corrections and limitations

- Claude disclosed that its own full-suite run used an installed-Pillow version shim. That does not establish that Codex's earlier run did. The existing isolated dependency reports Pillow 13 through package metadata, the Python module and the compiled imaging extension, and decodes a real image. Earlier Codex QA logs record the actual 337-test runs.
- Per-host native painting, browser launch and inline confirmation are distinct from element-tree/DOM simulation. Do not turn either successful mocks or absent live evidence into a universal support claim.
- Current public PixelLab docs establish the VFX recipe family and palette input; no new concrete live recipe-field claim is justified by an unauthenticated help failure. Runtime replay must still validate current schemas.
- There is no mathematical guarantee of zero future defects. Acceptance requires closed material findings in the reviewed scope, preserved user goals and safeguards, and applicable verification on the final change set.

## Implementation and repeated-review results

All 22 findings were challenged individually. Accepted defects and the useful parts of partial findings are implemented; the rejected cuts preserve restrictive policy, resume evidence and the documented optional host bridge. Three specialist reviewers cross-reviewed the changes, and a fourth reviewer without the design history rechecked the complete PR and sibling workflow coverage.

That review produced further corrections rather than treating agreement as automatic acceptance:

- Restrict private panel output to fresh/empty subdirectories. A generations-root output or an existing art folder must never receive the panel's `*` ignore policy. Existing files and ignore rules stay unchanged.
- Separate inspection from action verification. Missing accounting or stale captured art does not prevent opening the unchanged standalone snapshot. Acting on feedback still requires strict current manifest, embedded-byte and source-image verification.
- Clarify retry exhaustion: it blocks additional retries, not original approved stages that still fit the cap and have valid inputs/checkpoints. Zero retries does not cancel the initial run.
- Recover the demonstrated Windows atomic-replacement denial by retrying the same prepared manifest replacement under the existing transaction lock. Persistent failure preserves the old ledger and cleans owned temporary files; neither the mutation nor remote work is replayed.

Focused verification used genuine Pillow 13: 23 Auto/Bark tests, 28 manifest tests, 17 downloader tests, six doctor-rule tests and 22 panel tests passed. The manifest scenario that failed in the first integrated run then passed ten repetitions; the mixed nine-process update scenario passed three repetitions. The published Claude Code 2.1.303 CLI validates the plugin and passes 20 native tests; CI now pins and runs those commands without account sign-in or model calls. The pre-existing root contributor-context warning remains unrelated to the adapter.

Real headless Edge decoded four previews including GIF, changed shared zoom, composed identity-bound feedback with literal script-looking notes, and made no page network requests or runtime exceptions. Desktop and narrow screenshots were inspected. The actual HTML-template DOM test passed localized notes, explicit bridge click, missing-bridge/standalone fallback and failed-preview invalidation. These browser/DOM checks do not claim live native painting or live inline confirmation.

The first integrated QA's Windows replacement failure is retained as diagnostic evidence, not reported as a pass. Full repository QA and the published checks on the final commit are the final acceptance gates; their exact-head results are recorded on [PR #11](https://github.com/Shilo/pixellab-pip/pull/11). The PR remains unmerged, and no paid PixelLab call or real user-settings edit was made for this review.
