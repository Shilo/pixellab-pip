PixelLab Pip is an unofficial, agent-agnostic PixelLab workflow router shipped as a portable Agent Skill. It teaches coding agents to choose between documented PixelLab MCP tools, REST v2 endpoints, website/editor fallback, Aseprite, Pixelorama, and local asset assembly. The repository is mostly Markdown because the product is the routing contract itself — task detection, prompt normalization, image-role classification, credential handling, usage reporting, localization, and specialty workflows for sprites, tilesets, layered characters, edits, animation, and completion sounds — plus helper scripts, QA, and packaging manifests.

Project rules:
- Apply KISS and YAGNI to agent-facing/runtime and implementation work: additions, fixes, tests, tooling, manifests, and refactors. Make the smallest complete change that satisfies the current requirement without weakening functionality, correctness, safety, or efficiency. Shorter is not automatically better — challenge every cut and every addition.
- Add only what the current task requires, using verified PixelLab behavior where relevant and preserving applicable safety/correctness constraints. No speculative future-proofing, unused outputs/formats, compatibility paths without a current requirement, redundant examples, or optional machinery.
- Keep runtime content only when it changes an agent decision, action, safety boundary, or verification step. Retain only the rationale needed to apply it; move research, evidence, and background explanation to docs/.
- Keep each runtime rule in one canonical place: SKILL.md if global, or one reference if specific to a task or route. Search for an existing rule or section before adding another; elsewhere, use a pointer.
- Reuse and simplify existing structure before creating a file, section, workflow, example, schema mapping, or helper. When new guidance replaces old guidance, remove the obsolete text in the same change.
- The KISS/YAGNI, runtime-content, canonical-placement, and reuse/consolidation rules above do not apply to docs/. docs/ is user-facing; follow the user's request and the document's own requirements.
- Never weaken protections for routing accuracy, public-vs-private PixelLab endpoint boundaries, secret/auth safety, paid-credit control, output integrity, or user trust. Simplify them through consolidation.

Content placement (progressive discovery):
- skills/pixellab-pip/SKILL.md — agent-facing canonical contract and lean router: triggers, guardrails, surface selection, pointers. It must classify common requests and point directly to any required reference.
- skills/pixellab-pip/references/*.md — agent-facing operational contracts loaded on demand: durable routing rules, schema mappings, safety constraints, verification. Never restate SKILL.md globals (it is always co-loaded); use a pointer.
- docs/ — human/developer research, evidence, and background; not required for normal runtime routing. Promote a finding into SKILL.md or references/ only when it changes agent behavior. (docs/pixellab/ terminology and routing research; docs/tools/ integration background; docs/developer.md repo structure and local install; docs/showcase/README.md showcase rules.)
- .local/ — temporary agent-generated or cache files.

Validate every edit: `python dev-tools/qa.py` (includes the unit tests).
Commits: conventional `<type>[optional scope]: <description>`.
