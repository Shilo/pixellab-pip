# Security Policy

PixelLab Pip is an Agent Skill: plain-Markdown routing instructions plus two small local Python helpers (a completion sound and a background-removal check). It ships no compiled binaries and makes no hidden network calls. It uses your PixelLab token only as an auth header for PixelLab's own API and is designed never to read, print, log, or store the token's value.

## Reporting a vulnerability

Report suspected vulnerabilities privately through GitHub's [private vulnerability reporting](https://github.com/Shilo/pixellab-pip/security/advisories/new) (the repository **Security** tab → **Report a vulnerability**). Please do not open a public issue for a security report. We aim to acknowledge reports within a few days.

## How each release is verified

- **Skill audit** — every push and a weekly schedule run [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) over the skill; results are public on the [Code Scanning tab](https://github.com/Shilo/pixellab-pip/security/code-scanning) and a release is blocked if it goes over the risk threshold.
- **Independent registry audit** — every release auto-publishes to [ClawHub](https://clawhub.ai/shilo/skills/pixellab-pip), whose third-party audit (SkillSpector + VirusTotal + ClawScan) posts a public [security audit](https://clawhub.ai/shilo/skills/pixellab-pip/security-audit) verdict.
- **Malware scan** — each release links a public [VirusTotal](https://www.virustotal.com/) report of the exact download in its release notes.
- **Build provenance** — every release zip carries a cryptographic proof-of-origin (a Sigstore build-provenance attestation) that GitHub built it from this repo, unaltered. Verify one: `gh attestation verify pixellab-pip-<version>.zip --repo Shilo/pixellab-pip`.

Some scanner findings are expected and disclosed by design — the skill legitimately documents PixelLab bearer-token handling, `api.pixellab.ai` documentation URLs, and a local sound-playback helper — so instruction scanners report those as informational findings. See the [README Security section](README.md#security) for the line-by-line disclosure.

## Supported versions

The latest release is supported. Older versions are not maintained.
