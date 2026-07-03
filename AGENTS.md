PixelLab Pip is an unofficial, agent-agnostic PixelLab workflow router implemented as a portable Agent Skill. It teaches coding agents how to choose between documented PixelLab MCP tools, REST v2 endpoints, website/editor fallback, Aseprite, Pixelorama, and local asset assembly workflows with differing capabilities. The repository is mostly Markdown because the product is the routing contract itself: task detection, progressive reference loading, prompt normalization, image-role classification, credential handling, usage reporting, localization, and specialty workflows for sprites, tilesets, layered characters, edits, animation, and completion sounds.

Design goal: Treat YAGNI and KISS as requirements. Keep the routing contract no larger than today's need; reuse existing structure before adding new text, while preserving safety, correctness, clarity, and verification.

Keep skills/pixellab-pip/SKILL.md limited to the core routing contract: common triggers, guardrails, surface selection rules, and pointers to deeper references. Move uncommon workflows, procedures, tool-specific edge cases, and specialty QA checklists into topic files under skills/pixellab-pip/references/. Common requests should resolve from SKILL.md alone; specialized requests should route predictably to the relevant topic reference.

Treat skills/pixellab-pip/references/*.md as agent-facing operational contracts loaded by progressive discovery. Keep them YAGNI: include durable routing rules, schema mappings, safety constraints, verification requirements, and broadly reusable failure-mode guidance. Do not add niche prompt recipes, one user's experimental preferences, project-specific taste notes, or exploratory research unless they change how agents should generally route, verify, or avoid mistakes. Put those narrower findings in docs/pixellab/, docs/tools/, docs/showcase/, or .local/ as appropriate, and only promote them into references/ when they become general agent behavior.

Treat docs/*.md files as human-facing and developer-facing learning material. They may be much more detailed than references/ when the detail is useful for research, future audits, product understanding, examples, or fallback evidence. Use docs/ as source material when a task needs deeper context, but do not rely on docs/ alone to change agent behavior; promote only the durable operational rule into SKILL.md or the matching references/ file.

Canonical skill contract and routing source of truth: skills/pixellab-pip/SKILL.md
Topic reference files loaded on demand by the skill: skills/pixellab-pip/references/
PixelLab terminology and surface-model background: docs/pixellab/ only when changing product terminology or routing claims
Tool comparison and integration background: docs/tools/ only when changing Aseprite, MCP, REST, or editor-routing claims
Developer context: docs/developer.md only when changing repository structure or local install guidance
Showcase rules: docs/showcase/README.md only when adding or editing showcase pages or showcase assets
Temporary agent-facing generated or cache files belong inside: .local/
Git conventional commits: <type>[optional scope]: <description>
