# Security And Trust

PixelLab Pip is a Markdown Agent Skill with local Python helpers for sound, asset processing, accounting and restricted downloads. It contains no compiled binaries. Guidance, routing, prompt preparation, and setup planning work without a PixelLab token.

The ordinary Claude plugin registers an optional native review adapter at session startup; its user-clicked full-review button invokes the bundled `panel.py open` through local Python to validate and open a private standalone review in the host's browser, without paid work or settings changes.

## What Pip Can Access

For live PixelLab work, Pip uses a bearer token only as an authentication header for documented PixelLab MCP or REST v2 requests. The MCP client passes it, or REST fallback references `PIXELLAB_SECRET` by name.

Pip is designed not to:

- read the token value into the conversation, print it, log it, or store it;
- scan `.env` files, shell history, keychains, browser sessions, or unrelated secrets;
- use copied website session tokens or undocumented private PixelLab endpoints for automation;
- delete, clear, or overwrite remote PixelLab assets without explicit approval;
- present locally drawn or modified pixels as untouched PixelLab output.

Local helpers make no network calls of their own, except `assets/fetch.py`, which downloads only links a PixelLab tool returned, from PixelLab's download and file hosts (`api.pixellab.ai`, `backblaze.pixellab.ai`) and refuses any other host; it sends no token. Pip writes generated work to the project's `pixellab-pip-generations/` directory and preferences to its own config file or documented fallback location.

Setup can edit the selected app's PixelLab connection after a token-free preview and explicit approval. On macOS and Linux, completion sound playback can launch an installed audio player with an argument list and a timeout. These are intentional capabilities to review when choosing to install Pip.

For detailed auth and service-boundary guidance, see [PixelLab auth and security](pixellab/pixellab-auth-and-security.md).

## Public Checks

- **Skill audit:** [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) scans the skill on every push and weekly. Results appear in the repository's [Code Scanning tab](https://github.com/Shilo/pixellab-pip/security/code-scanning), and releases are blocked above the configured risk threshold of this repository's pinned SkillSpector version.
- **Independent registry audit:** [ClawHub](https://clawhub.ai/shilo/skills/pixellab-pip) publishes its SkillSpector, VirusTotal, and ClawScan verdict in the [public security audit](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit).
- **Malware scan:** each release links a VirusTotal report for the exact release download in the [latest release notes](https://github.com/Shilo/pixellab-pip/releases/latest).
- **Build provenance:** each release zip has a Sigstore build-provenance attestation showing that GitHub built the file from this public repository.

Verify a downloaded release zip with GitHub CLI:

```bash
gh attestation verify pixellab-pip-<version>.zip --repo Shilo/pixellab-pip
```

These checks are independently inspectable layers, not a guarantee that any instruction file is risk-free.

Registry audits and malware reports apply to the published version or exact archive they inspected. A local scan of unreleased changes does not update those public reports or establish a fresh hosted verdict. The release workflow submits and verifies the new version before promoting it; a GitHub-only release explicitly leaves the ClawHub audit pending until it can be completed.

## Expected Scanner Disclosures

Instruction scanners can flag Pip because it legitimately documents bearer-token handling, official `api.pixellab.ai` URLs, and local sound playback. Dismissed findings include a public, per-finding rationale in the [closed Code Scanning results](https://github.com/Shilo/pixellab-pip/security/code-scanning?query=is%3Aclosed).

CI and ClawHub can run different SkillSpector releases, and ClawHub's ClawScan runtime applies additional parser fixes and runs model-based checks. Compare results only with their scanner commit, patch revision, scan mode, and inspected artifact identified. An unpatched local run can report parsing failures that the hosted runtime has already fixed.

SkillSpector's aggregate score is confidence-weighted and capped, with diminishing contributions from repeated occurrences of the same rule and additional weight for executable-file findings. It can therefore read `CRITICAL` / `DO_NOT_INSTALL` even when no individual finding is critical. That aggregate label warrants reviewing the actual findings; it does not identify a particular exploit. ClawHub's final ClawScan review is a separate verdict, and the release workflow requires a benign review with high confidence before promotion. Expected findings include:

- **Incomplete referenced-artifact analysis (`AE1`):** a scanner coverage notice. Local reproductions show bounded parsers stopping on ordinary Markdown and code spans; ClawScan carries fixes for several such limits. A partial report still needs its coverage caveats explained and is not interchangeable with a complete hosted verdict.
- **MCP config access (`AS2`):** the setup wizard adds the PixelLab entry to an app's MCP config only when the user names that app, after a token-free preview and explicit approval. Broad config and secret scans are forbidden.
- **Sound playback (`AST4`) and external URLs (`E1`):** local audio-player execution and documented PixelLab service URLs are real capabilities. Their presence alone does not establish command injection or secret exfiltration; inspect the fixed command arguments and intended destinations.
- **License wording (`EA3`):** the standard MIT disclaimer can match a scope-expansion phrase. The standalone skill ships the adopted source's complete notice in `THIRD_PARTY_NOTICES.md`, because the repository-root license does not travel with a raw-skill archive. The [MIT license](https://opensource.org/license/mit) requires preserving the copyright and permission notice when distributing copies or substantial portions of the software.
- **Autonomous decision making (`EA2`):** phrase matches on safety rules that tell the agent when it must, or need not, ask before acting.
- **Description mismatch (`TP4`) and language policy (`SQP-3`):** model checks that compare one local helper script with the whole skill description, or flag English prompt preparation that already shows the translation and asks for approval before any non-English request is sent.

## Report A Concern

Read [SECURITY.md](../SECURITY.md) for supported versions and private vulnerability reporting.
