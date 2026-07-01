# Aseprite CLI Integration Testing

Last reviewed: 2026-07-01.

This note is for maintainers validating PixelLab Pip's Aseprite CLI integration. Agent-facing task instructions live in `skills/pixellab-pip/references/aseprite-cli.md`; this file covers developer QA policy.

## Scope

The Aseprite CLI integration should prove that generated or fixture image files can move through a useful Aseprite workflow without automating the PixelLab Aseprite extension:

- Create a new `.aseprite` workspace from PNG frames.
- Reuse the default layer and frame instead of leaving blank content.
- Create layers, cels, frames, tags, and frame durations.
- Import generated art into a copy of an existing `.aseprite` file.
- Export PNG sequences, GIFs, sprite sheets, and JSON metadata.
- Import grid sprite sheets and GIFs back into `.aseprite` files.
- Verify output files, metadata, layer names, tag names, frame counts, and original-file preservation.
- Quantize or reduce fixture images to source-derived N-color palettes and explicit palettes, including strict `#000000`/`#ffffff` 1-bit output, and verify both visible pixel colors and optional `.aseprite` palette replacement.

## PixelLab Service Stability

Prefer deterministic local fixtures for Aseprite integration tests. PixelLab service availability can fluctuate; if live PixelLab generation is slow, failing, rate-limited, or otherwise unstable, skip live generation and simulate generated assets locally with small PNG frames. Label those results as local fixtures, not PixelLab outputs.

When a live PixelLab smoke test is useful and the service is healthy, keep it small and non-destructive:

- Generate or download one tiny asset.
- Import it into a temporary `.aseprite` file or a copy of a test fixture.
- Verify exports and metadata.
- Do not test against a user's real project file.

## Original File Safety

Tests should verify the agent-facing contract: Pip must never write directly into an existing `.aseprite` original unless the user explicitly approves in-place modification of that exact file.

During automated testing, create a new temporary `.aseprite` file or copy an input file first, then write only to the copy.

If a test uses an existing source file:

- Hash it before the run.
- Hash it after the run.
- Fail the test if the hash changed.

In-place writes require explicit user approval for that exact file and should not be part of routine verification. Routine E2E coverage should prove copy-on-write behavior and original-file preservation.

## Verification Notes

Aseprite launcher-based installs may return before output files are visible on disk. Test harnesses should wait briefly for expected files before declaring failure.

Do not rely on unverified examples just because an option exists in documentation. Keep examples in the agent-facing reference only when they are either directly verified or simple documented patterns with clear verification steps.

Palette quantization tests should cover both halves of the contract:

- Pixel-only clamp: output visible pixels use only the requested colors, while the document palette is not asserted unless the output is indexed.
- Palette replacement: output visible pixels use only the requested colors and the `.aseprite` palette entries match the requested list, allowing only an explicitly approved transparent entry when the source has transparency.

For strict 1-bit tests, use fixtures with near-black, near-white, mid-gray, and colored pixels so the test catches accidental grayscale ramps or unverified palette entries. Default dithering should be disabled; add a separate fixture only when testing a requested dither mode.

For transparent indexed tests, include black visible pixels and transparent pixels in the same fixture. Fail if `#000000` is assigned to the transparent index or exports as transparency. Palette-replacement tests should verify the requested visible colors plus only an explicitly approved transparent index.

Do not publish local machine paths, account data, tokens, extension credentials, copied request payloads, or private extension internals in test output or public docs.
