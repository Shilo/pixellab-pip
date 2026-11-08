# Audit improvement handoff

Improve PixelLab Pip's security and audit reliability independently of releasing it. Preserve useful behavior and every existing security boundary. Start with [AGENTS.md](../AGENTS.md), [Scanner Maintenance](../docs/developer/scanner-maintenance.md), [Security And Trust](../docs/security.md), and the canonical runtime text before proposing a runtime edit. Publication is a separate task; this handoff does not instruct an agent to bump versions, upload candidates or open upstream issues.

## Verified starting point: 3.2.5

The [3.2.5 release](https://github.com/Shilo/pixellab-pip/releases/tag/v3.2.5) completed through [release run 42472613035](https://github.com/Shilo/pixellab-pip/actions/runs/42472613035). It became the default on GitHub and ClawHub; skipping unsuccessful intermediate versions worked. The tagged source commit is `4be8933b3f4343cc75c106f6c38955caf17c9519`.

| Evidence | Observed result | What it establishes |
| --- | --- | --- |
| Production final ClawScan | Benign / MEDIUM confidence | Passed the explicitly approved benign + medium/high policy at that time |
| Production SkillSpector | 46 / MEDIUM / CAUTION; 49 findings | Supporting advisory, **not** a clean LOW result |
| Production review of those 49 findings | All `evidence.llm_review_outcome = disagreed`; all MEDIUM | The meta-review disagreed; findings and the aggregate score still exist |
| Production coverage | 127/127 supported components fully inspected; four missing-reference caveats; WAV excluded from applicable text analyzers | Raw completeness remains `partial`, not complete |
| Reviewed static mode | 17 / LOW / CAUTION | Static regression evidence only |
| Offline TP4 planner | 64/64 batches; zero headroom; no partial events, at 128,000 assumed input tokens | Planning fits at that assumption; no model assessment |
| Release checks | 434 QA tests, mandatory security checks and malware scan passed; zero open GitHub code-scanning alerts | Observed release state, not a perpetual guarantee |
| Public downloads | All 128 ClawHub source files matched; GitHub ZIP matched tagged source and attestation | The audited/released source identity was checked |

GitHub ZIP SHA-256: `8890e3f7fcd19acf4f7d3b6d85397d9200befcdbc7a97ba6d84919c1dd3d6fe8`.

The optional generated `skill-card.md` was absent. Consequently standalone `skill verify` reported `card.missing` despite `security.passed = true`. Do not describe the entire CLI verification as passing or manufacture a card requirement the release does not have.

The initial evidence is in ignored `.local/release-3.2.5/`: `hosted-skillspector-final-full.json`, `verify-monitored.json`, `latest-monitored.json`, `source-archive.json`, `public-download/verification.json`, `workflow.log`, and `outcome.json`. This scratch data may not exist in a fresh checkout. Download the exact version's stored reports rather than substituting the current default:

```powershell
npx --yes clawhub@0.23.3 --no-input scan download @Shilo/pixellab-pip --version 3.2.5 --output .local/clawhub-3.2.5-reports.zip
npx --yes clawhub@0.23.3 --no-input inspect @Shilo/pixellab-pip --version 3.2.5 --json
```

The report download requires the publisher's existing native authentication. It retrieves evidence, not a new scan. Archive the complete raw reports, scan/check timestamps, input hashes, scanner/patch provenance, observed model settings and coverage. Reports can change after a rescan of unchanged bytes; never merge findings from different scan times into one purported result.

## Why local and live results differ

Our ordinary CI scanners use `--no-llm`. That omits semantic analysis, model-based review and the final ClawScan judge. Scanner revisions and ClawScan's integration patches also differ across lanes. The hosted scan therefore assesses substantially more than a local score of 17. Neither identical version numbers nor a static LOW rating establish equivalent execution.

Use the [full model preflight procedure](../docs/developer/scanner-maintenance.md#full-model-preflight-separate-from-release), not another static-only run, to test semantic improvements before selecting a release version. The new manual workflow builds the binary and Docker image from ClawScan `80d11a34a97a9181213c806fc3013123360f9012`, the [ClawHub reviewed worker source pin inspected on 2026-11-08](https://github.com/openclaw/clawhub/blob/547b484e29fa55eedb22449e8a47749989fda21e/scripts/security/clawscan-source-commit.txt). Its [bundled profile](https://github.com/openclaw/clawscan/blob/80d11a34a97a9181213c806fc3013123360f9012/internal/profiles/clawhub/clawscan.yml) selects model-enabled SkillSpector and A.I.G, then the final judge. Do not replace the image with a moving `latest` tag or run an unpatched scanner with just a different model name.

At handoff, repository secret `OPENAI_API_KEY` and local model credentials are absent. Only the offline planner and static checks have been exercised here; the new full workflow is prepared, **not yet validated with real inference**. Configure the API credential through native secret settings; never paste it into chat, commit it, write it to scratch files or put its value in CLI arguments. Dispatch manually because the full audit costs model usage. A missing credential must remain a clear failure, not a silent static fallback.

The same pinned source can be built and run locally using upstream's [matched binary/image recipe](https://github.com/openclaw/clawscan/blob/80d11a34a97a9181213c806fc3013123360f9012/docs/scanner-runtime.md#consume-without-a-public-release). Keep model credentials in the environment and the default Docker sandbox enabled. Run outside the project checkout to avoid loading a local profile. The repo workflow is the canonical implementation here; do not create a second diverging runner.

Full preflight is the closest available developer test, not the registry's result. Different model responses, deployment versions, resolved dependencies and registry/publisher context can still change it. Record those differences explicitly. The actual hosted verdict remains mandatory when eventually releasing.

ClawHub's [CLI rejects local folder scans](https://github.com/openclaw/clawhub/blob/547b484e29fa55eedb22449e8a47749989fda21e/packages/clawhub/src/cli/commands/scan.ts#L111). `publish --dry-run` previews packaging; it does not request a live audit. A registry scan requires a submitted version, and `--tags candidate` is not private staging: the [server automatically promotes higher semver versions](https://github.com/openclaw/clawhub/blob/547b484e29fa55eedb22449e8a47749989fda21e/convex/skills.ts#L11236). Do not implement that workaround on the live skill. A true unpublished registry preview would need ClawHub support; no upstream issue has been authorized or is needed for the independent model workflow.

## Findings to challenge, not blindly remove

All paths below are relative to `skills/pixellab-pip/`. Counts are findings in the stored 3.2.5 report, not occurrences in every report or proof of exploits. Re-read each exact location and its surrounding canonical rules before deciding.

| Group | Count | Files | Review direction |
| --- | --- | --- | --- |
| `AST4`: subprocess execution | 1 | `assets/bark.py` | Preserve completion sounds. Inspect fixed argument lists, `shell=False` behavior, bounded timeout, executable selection and hostile filenames. Change only a demonstrated weakness; do not remove playback to erase the finding. |
| `E1`: external URLs in blueprints | 18 | Nine bundled blueprints, two findings each | Verify intended official PixelLab endpoints and token-free examples. Preserve working URLs and portable recipes. |
| `E1`: external URLs in references | 19 | `blueprint.md` (2), `official-pixellab-documentation.md` (7), `preset-skeleton-template-animation.md` (4), `setup.md` (5), `prompt-limits.md` (1) | Trace the destination and data actually sent. Public documentation links are not themselves secret exfiltration. No string splitting or URL hiding. |
| `SQP-3`: language/choice | 2 | `blueprints/rpg-maker-character.blueprint.json`, `references/auto.md` | Challenge whether the literal English review menu can be localized without changing checkpoint semantics. Keep exact provider-bound English values, translations, user choices and paid-call approval. A reviewer disagreement is evidence, not a reason to skip this UX review. |
| `SQP-2`: image transfer disclosure | 9 | `cinematic.md`, `eight-direction.md`, `image-input-roles.md`, `normal-maps.md`, `paperdolling.md`, `preset-skeleton-template-animation.md`, `pro-flash.md`, `scenes-and-backgrounds.md`, `style-reference.md` | Trace first-transfer disclosure, selected images and authorization using SKILL.md's global Auth And Execution rule. Fix a specific bypass if one exists. Do not duplicate the global rule in nine references just to satisfy isolated file review. |

The nine blueprint names are `character-candidates`, `knight`, `overhead-axe-chop`, `portrait-head-shoulders-mvp`, `projectile-skill`, `rpg-maker-character`, `vfx-eruption-per-target`, `vfx-strike-single-target` and `vfx-wave-across-party` (each ending `.blueprint.json`). Counts sum to 49. A.I.G's stored 3.2.5 report contained no findings; still inspect its execution status and provenance on a new scan.

The four coverage notices point to `SKILL.md` lines 32, 167, 232 and 239 **at v3.2.5**. Inspect the referenced paths before classifying them: runtime-created outputs, unresolved mentions and genuinely missing bundled files require different remedies. Preserve necessary dynamic filenames and official links; never add dummy files merely to make references resolve. `assets/bark.wav` remains an explicit binary/text-analysis exclusion, not uninspected Python code. Keep those distinctions in comparisons.

## Priorities and iteration procedure

1. **Validate full model preflight first.** Once the credential exists, run the unchanged 3.2.5 export as a control, then a fixed candidate with the same runtime. The committed workflow scans the dispatch commit on `main`; for the historical control, use the same upstream local recipe on a clean `v3.2.5` export. Do not alter the production default. Review actual scanner completion, model controls, coverage, findings and the final verdict—not just process exit status. Retain the control and every candidate report, including adverse ones.
2. **Create scan-capacity headroom.** The pinned offline planner currently fits exactly 64 batches. Trace which real executable blocks consume batches and consolidate genuinely redundant examples only when their routing/verification value is already preserved canonically. Do not reclassify, hide, move or obscure executable code, remove capabilities, or raise scanner limits. Measure before/after; target real headroom rather than a fabricated universal safe batch count. Newer full-runtime patches may plan differently; keep that separate from the reviewed static lane.
3. **Review the semantic groups above.** Start with plausible disclosure or localization gaps, not deletion of required URLs, MIT notices or sound functionality. For each finding record: real capability, canonical rule, evidence, classification (valid / expected capability / false positive / uncertain), proposed minimal fix or no-change rationale, and meaningful behavior tests.
4. **Apply small coherent changes.** Preserve the original artifact, change one concern at a time, then follow Scanner Maintenance for identical before/after static scans, offline planning and independent review. Run `python dev-tools/qa.py`; check source diffs for duplicated runtime rules. For helpers, test valid/edge/failure inputs and compare outputs, cleanup and accounting. For prose, trace decisions and permissions; a prose diff is not a live agent behavior test.
5. **Re-run full model preflight for the finished candidate.** Record full input hashes, source/image identity, configured and observed models, risk score, findings, coverage and verdict. A changed skill needs fresh evidence. Don't repeatedly rescan unchanged bytes until the model happens to return benign. A later adverse result is evidence to investigate, not something to discard.
6. **Stop at a reviewed improvement.** Deliver a concise findings ledger, before/after evidence, behavior/test results and remaining uncertainty. Update `[Unreleased]` and commit conventionally. A lower score alone is not acceptance. Leave version choice, actual registry scan and release promotion to a separately requested release.

For durable notes, maintain the reviewed state here and canonical procedures in Scanner Maintenance; keep large raw results and environment-specific paths in ignored `.local/` evidence. A future handoff must be recoverable from the exact version/source links even when scratch data is gone.

## Boundaries already decided

- Benign + MEDIUM or HIGH confidence is the approved release policy. Low/unknown/missing confidence and suspicious/malicious verdicts remain blocked. Keep static regression, direct malware scan, publisher/version identity, exact-file checks, provenance, current stored verdict and latest-pointer protection.
- Do not remove functionality, add suppressions, rewrite licensing, mangle strings, loosen a baseline automatically or switch to an easier model to improve a score. An accepted static reduction should tighten its baseline only after measurement and independent review.
- The 3.2.2–3.2.5 fixes clarified existing protections: first-transfer disclosure, blueprint external-sharing scope, palette-reference scope, and concise Workbench task notes. Preserve those behaviors and canonical placement. The old HIGH-only policy is obsolete; do not restore it accidentally.
- No paid PixelLab generation is needed for audit maintenance. Model-audit API usage is separate from PixelLab credits.
- Do not contact maintainers or publish new versions as part of this improvement task. Existing resume/skip functionality already worked; a blocked new candidate does not mean the public 3.2.5 release must be removed.
