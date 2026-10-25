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

For detailed auth and service-boundary guidance, see [PixelLab auth and security](pixellab/pixellab-auth-and-security.md).

## Public Checks

- **Skill audit:** [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) scans the skill on every push and weekly. Results appear in the repository's [Code Scanning tab](https://github.com/Shilo/pixellab-pip/security/code-scanning), and releases are blocked above the configured risk threshold of this repository's pinned SkillSpector version.
- **Independent registry audit:** [ClawHub](https://clawhub.ai/shilo/skills/pixellab-pip) publishes its SkillSpector, VirusTotal, and ClawScan verdict in the [public security audit](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit).
- **Malware scan:** each release links a VirusTotal report for the exact release download in the [latest release notes](https://github.com/Shilo/pixellab-pip/releases/latest).
- **Build provenance:** each release zip includes a Sigstore build-provenance attestation showing that GitHub built the file from this public repository.

Verify a downloaded release zip with GitHub CLI:

```bash
gh attestation verify pixellab-pip-<version>.zip --repo Shilo/pixellab-pip
```

These checks are independently inspectable layers, not a guarantee that any instruction file is risk-free.

## Expected Scanner Disclosures

Instruction scanners can flag Pip because it legitimately documents bearer-token handling, official `api.pixellab.ai` URLs, and local sound playback. Dismissed findings include a public, per-finding rationale in the [closed Code Scanning results](https://github.com/Shilo/pixellab-pip/security/code-scanning?query=is%3Aclosed).

ClawHub's registry audit runs a newer SkillSpector with model-based checks. Its score is a capped aggregate of every finding, so it can read `CRITICAL` / `DO_NOT_INSTALL` even though no single finding is critical; ClawHub's final ClawScan review rates the same version benign with high confidence, and the release workflow promotes a version and creates its GitHub release only after that verdict. The one exception is a GitHub-only release, used when ClawHub's own scanning is stuck: its notes say the ClawHub audit is pending, and the same version goes to ClawHub later only after that audit passes. Expected findings there:

- **Incomplete referenced-artifact analysis (`AE1`):** a scanner coverage notice, not detected hidden content. Ordinary prose trips it, such as the `${XDG_CONFIG_HOME:-~/.config}` settings path or the words "remove" and "DELETE" beside code spans. Every referenced file ships as readable Markdown with no hidden characters, comments, or encoded content.
- **MCP config access (`AS2`):** the setup wizard adds the PixelLab entry to an app's MCP config only when the user names that app, after a token-free preview and explicit approval. Broad config and secret scans are forbidden.
- **Autonomous decision making (`EA2`):** phrase matches on safety rules that tell the agent when it must, or need not, ask before acting.
- **Description mismatch (`TP4`) and language policy (`SQP-3`):** model checks that compare one local helper script with the whole skill description, or flag English prompt preparation that already shows the translation and asks for approval before any non-English request is sent.

## Report A Concern

Read [SECURITY.md](../SECURITY.md) for supported versions and private vulnerability reporting.
