# Scanner Maintenance

Use this procedure when changing the shipped skill or investigating scanner findings. It is maintainer guidance, outside the installed skill. The objective is to reduce avoidable risk while preserving behavior, safety, stability and efficiency; a lower score never overrides the project rules in [AGENTS.md](../../AGENTS.md).

## Automated checks

The existing [Skill Security Audit](../../.github/workflows/security-scan.yml) retains its CI/release scanner and adds **SkillSpector risk regression** on pull requests, main pushes, weekly runs and manual dispatch. The additional job uses the exact reviewed SkillSpector commit and the original, hash-verified ClawScan patch recorded in [scanner-baseline.json](../../dev-tools/scanner-baseline.json). It installs in an isolated environment and runs static analysis without a model, credentials or paid generation. This is ClawHub-compatible static evidence, not the complete hosted audit.

[check_scanner.py](../../dev-tools/check_scanner.py) checks the JSON report against that baseline: risk must not increase, findings must not introduce new or increased rule/path/severity groups, and errors or worse analysis coverage fail the check. It checks the current skill's file inventory so a report of an empty or different directory cannot pass. Reduced findings are allowed; the full report remains visible as a CI artifact. The baseline does not suppress or modify scanner findings.

The existing QA security-trigger guard, unit tests, HOL scan, Code Scanning, release checks and Scorecard remain in place. Dependabot merges also wait for the new check. Requiring it for every human merge is a separate repository branch-rule setting; this change does not modify GitHub settings.

## Reviewed baseline

The baseline records the reviewed source commit and scanner provenance. It starts at **17 / LOW / CAUTION** for the pinned ClawScan-compatible static scan. Do not compare numbers across different scanner revisions, patches, modes or artifacts as if they were interchangeable.

Accepted findings are local sound-player execution (`AST4`, `assets/bark.py`) and documented PixelLab service URLs (`E1`, in the paths listed in the baseline). Sound playback is a required feature; the URLs provide working, portable setup and documented service access. Their continued presence is not proof of an exploit. See [Expected Scanner Disclosures](../security.md#expected-scanner-disclosures) for the capability boundaries and other scanners' findings, including required MIT text.

Coverage is explicitly partial: the pinned scan reports four unresolved runtime/reference notices in `SKILL.md` and unsupported WAV analysis for `assets/bark.wav`. The validator permits only the reviewed exception groups and counts; it does not call this complete coverage. A new parser failure, analyzer failure, uninspected supported file or additional exclusion requires investigation.

## Review a change

1. Preserve the before revision and scan clean exported before/after artifacts with the same exact scanner, upstream patch and static mode. Local test caches are not release payloads; export the tracked skill rather than scanning a development folder with ignored artifacts. Record provenance, input identity, score, finding changes and coverage limits in ignored `.local/` evidence. Use throwaway scanner environments outside the repo for local work. The CI workflow is the canonical setup recipe; redirect JSON stdout rather than using the pinned scanner's unreliable Windows `--output` option.
2. Challenge each finding against the actual capability and canonical rule. Apply only a concrete safety improvement or equally clear wording/formatting. Keep required notices, URLs and features. Do not split strings, mangle URLs, hide files, add suppressions, or weaken safety instructions to lower a score.
3. For helper changes, exercise old and new versions on representative valid, edge and failure inputs with mocks/dry runs. Compare outputs, accounting, cleanup and meaningful resource use. For prose, trace each old/new decision, permission and safety obligation with the canonical context loaded. Static reasoning is not native execution in every host; a planned dry run is not a model behavior test. No paid or hosted audit call is implied by these checks.
4. Have an independent reviewer challenge the final diff, test evidence and efficiency claims. Resolve concrete findings, then run `python dev-tools/qa.py`. Record user-facing changes under `[Unreleased]`; commit conventionally. CI must pass before treating the change as accepted.

To check an existing raw report locally, name the same clean artifact directory that the report scanned:

```powershell
python dev-tools/check_scanner.py .local/scanner-results/report.json --skill-dir .local/scanner-input/pixellab-pip
```

A failed check means investigate; it does not authorize removing functionality. If an intentional capability change legitimately increases findings, review its benefit, protections and before/after tests before updating the baseline with a written rationale. After an accepted reduction, tighten the baseline and record the new source revision so old allowances do not mask a later increase. Never regenerate the baseline automatically from a failing report. Changes to scanner pins or the upstream patch require fresh measurements and review before changing the baseline, and matching schema changes if necessary. Keep the original reports.

These checks detect known regressions; they cannot guarantee zero regressions, permanently LOW ratings, or a ClawHub recommendation. Local scans and GitHub pushes do not refresh the audit of a published ClawHub version. See [Security And Trust](../security.md) and [Publishing](publishing.md) for those separate release checks.
