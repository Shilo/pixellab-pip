PixelLab Pip is an unofficial, agent-agnostic PixelLab workflow router shipped as a portable Agent Skill. It teaches coding agents to choose between documented PixelLab MCP tools, REST v2 endpoints, website/editor fallback, Aseprite, Pixelorama, and local asset assembly. The repository is mostly Markdown because the product is the routing contract itself — task detection, prompt normalization, image-role classification, credential handling, usage reporting, localization, and specialty workflows for sprites, tilesets, layered characters, edits, animation, and completion sounds — plus helper scripts, QA, and packaging manifests.

Refactor rules:
- Functionality, correctness, and efficiency first; KISS second; YAGNI third. Shorter is not automatically better — challenge every cut and every addition.
- Never remove rules protecting routing accuracy, public-vs-private PixelLab endpoint boundaries, secret/auth safety, paid-credit control, output integrity, or user trust. Deduplicate instead: each rule stated once — in SKILL.md if global, in one reference if route-specific.
- Reuse existing structure before adding text. No speculative future-proofing, unused outputs/formats, redundant examples, or wording that does not change agent behavior.
- Human-facing updates are rare and useful (per references/usage-reporting.md). PixelLab-facing prompts describe the visual result and never repeat structured parameters (per SKILL.md Text Preparation).

Structure (progressive discovery):
- skills/pixellab-pip/SKILL.md — agent-facing canonical contract and lean router: triggers, guardrails, surface selection, pointers. Common requests must resolve from SKILL.md alone.
- skills/pixellab-pip/references/*.md — agent-facing operational contracts loaded on demand: durable routing rules, schema mappings, safety constraints, verification. Never restate SKILL.md globals (it is always co-loaded); use a pointer.
- docs/ — human/developer research, evidence, and background; never loaded at runtime. Promote a finding into SKILL.md or references/ only when it changes general agent behavior. (docs/pixellab/ terminology and routing research; docs/tools/ integration background; docs/developer.md repo structure and local install; docs/showcase/README.md showcase rules.)
- .local/ — temporary agent-generated or cache files.

Validate every edit: `python dev-tools/qa.py` and `python -m pytest tests/test_helpers.py` (CI enforces markdown link/reference existence and one exact prompt-limits table row).
Commits: conventional `<type>[optional scope]: <description>`.
