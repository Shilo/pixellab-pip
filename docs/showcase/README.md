# Showcase

Last reviewed: 2026-06-25.

Real PixelLab Pip example workflows, including prompts, selected routes, outputs, and validation notes.

## Generated Assets

| Asset | Preview | Initial prompt |
|---|---|---|
| [Pip Mascot](pip-mascot.md) | ![Pip mascot idle animation](pip/pip.gif) | <pre><code>pip create a 64px character based on .pip-mascot.md</code></pre> |
| [Gameplay GUI](gameplay-gui.md) | ![Fantasy MMORPG GUI kit](gameplay-gui/gameplay-gui-fantasy-mmo-688x384.png) | <pre><code>pip create a complete world of warcraft gui</code></pre> |

## Showcase Format

Each showcase should include:

- The generated result first, including the lead image and the request that produced it.
- Source inputs or brief summaries.
- Final prompts or natural-language parameters sent to PixelLab.
- Route, PixelLab surface, tool, endpoint, and key controls.
- Reproducibility controls that were intentionally set, such as image size, transparency, palette, direction, frame count, and seed. Do not imply every PixelLab endpoint always returns a seed; record a seed when the request explicitly sent one.
- Output files and showcase asset locations.
- Local processing notes for cropping, spritesheets, GIFs, or other assembled files.
- Validation notes that are useful to readers, such as image size, transparency, frame count, and display caveats.

Prefer direct prose that names the subject of each paragraph. Avoid starting explanatory paragraphs with placeholders such as "This example", "This pass", or "This result" when a concrete subject would be clearer.

For showcase pages with multiple related outputs, put the primary result first and make the `## Request` prompt subheaders match the order of the showcased images. Use descriptive headers such as `### Short MMO Prompt`, `### Mood-Only Prompt`, or `### Component-Specific Prompt (Follow-up)` instead of vague labels when prompts came from separate sessions or follow-ups.

Do not store PixelLab tokens, cookies, private account data, background job IDs, or unpublished third-party assets here.
