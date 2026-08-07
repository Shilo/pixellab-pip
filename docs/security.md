# Security And Trust

PixelLab Pip is a Markdown Agent Skill with small local Python helpers for completion sound and conservative background-removal validation. It contains no compiled binaries. Guidance, routing, prompt preparation, and setup planning work without a PixelLab token.

## What Pip Can Access

For live PixelLab work, Pip uses a bearer token only as an authentication header for documented PixelLab MCP or REST v2 requests. The MCP client passes it, or REST fallback references `PIXELLAB_SECRET` by name.

Pip is designed not to:

- read the token value into the conversation, print it, log it, or store it;
- scan `.env` files, shell history, keychains, browser sessions, or unrelated secrets;
- use copied website session tokens or undocumented private PixelLab endpoints for automation;
- delete, clear, or overwrite remote PixelLab assets without explicit approval;
- present locally drawn or modified pixels as untouched PixelLab output.

Local helpers make no network calls of their own. Pip writes generated work to the project's `pixellab-pip-generations/` directory and preferences to its own config file or documented fallback location.

For detailed auth and service-boundary guidance, see [PixelLab auth and security](pixellab/pixellab-auth-and-security.md).

## Public Checks

- **Skill audit:** [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) scans the skill on every push and weekly. Results appear in the repository's [Code Scanning tab](https://github.com/Shilo/pixellab-pip/security/code-scanning), and releases are blocked above the configured risk threshold.
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

## Report A Concern

Read [SECURITY.md](../SECURITY.md) for supported versions and private vulnerability reporting.
