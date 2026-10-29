# PixelLab Font Generation Spike

Last reviewed: 2026-10-29 (UTC REST/MCP snapshot); live test 2026-07-11.

Purpose: capture live findings for PixelLab font generation via REST `generate-font-pro`, starting with the first `glyph_px: 8` test. This is a research spike for route behavior, response shape, and quality expectations. It is not a canonical agent instruction contract.

## Route And Request

- REST `POST /v2/generate-font-pro` (Pro). **Asynchronous** — the create call returns HTTP `202` with a `background_job_id`; poll `GET /v2/background-jobs/{id}` until `status: completed`.
- Required fields: `description`, `weight` (`enum ["Bold", "Regular"]`).
- Optional fields:
  - `glyph_px` (`enum [8, 12, 16, 24, 32, 64]`, default 16) — the **real bitmap size per glyph** in the output atlas/TTF.
  - `seed`, `font_name` (defaults to `"{description} {weight}"`).

The former `image_size: "1K" | "2K"` field has been removed from both REST and MCP. Current pricing is fixed at 15 subscription generations, or at least `$0.115` when billed to credits.

## Response Shape

The completed job's `last_response` holds:

- `ttf_base64` — **the actual deliverable: a TrueType font file.** Decode and use this; a font is judged by rendering text with the TTF.
- `images[0]` — a glyph-**atlas** preview (`{type, width, height, base64}`): every glyph laid out in a grid. This is the character map, not sample text, so it never "reads" as words. Do not treat it as the output or as a legibility test.
- Current MCP `create_font` docs describe this atlas as 10×8 row-major cells for `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?:;'"-+()0123456789/%*=_$`; cell `i` represents character `i`, and there is no space glyph.
- `font_name`, `glyph_px`, `weight`, `seed`.
- `suspect_glyphs` — a list of glyph indices the model self-flagged as low quality.
- `billing_usage` / `usage`, `billing_charged`, `progress`.

Key lesson learned the hard way: **judge a generated font by rendering strings with the TTF**, not by eyeballing the atlas grid.

## Historical First Test: glyph_px 8, Regular, 1K

This request records the 2026-07-11 live probe. It includes the now-retired `image_size` field and must not be copied into a current request.

Request:

```json
{
  "description": "clean pixel arcade font",
  "weight": "Regular",
  "image_size": "1K",
  "glyph_px": 8,
  "seed": 20260713
}
```

Result:

- Completed after roughly two minutes (async). Cost `$0.095`.
- Returned a `64x64` glyph-atlas preview and a ~5.5 KB TTF.
- `suspect_glyphs: [56, 60]` — the model self-flagged two glyphs.
- Rendered as actual text, the `8px` font is **partially legible but rough**: some words read (for example `THE QUICK BROWN`, and `RSTUVWXYZ`), but several glyphs are broken or malformed — notably `L` and `E`, and several digits. Not production-clean.

Interpretation: `8px` is at the edge of legibility for a full glyph set; a single generation can land on the rough side, and the API's own `suspect_glyphs` signal confirms it. `glyph_px: 8` is a native 8px glyph-creation path in the PixelLab API (see [`pixellab-image-size-limits.md`](pixellab-image-size-limits.md)); it produces a usable-but-experimental tiny font, not a clean one.

Local run outputs (not committed showcase assets) are in the `pixellab-pip-generations/autonomous-final-tests/` run folder: the TTF, the atlas preview, and a rendered-text sample.

## Open / Untested

- `weight: "Bold"` — thicker strokes may survive `8px` better.
- `glyph_px: 12`, `16`, `24`, `32`, and `64` — valid in the current REST/MCP contracts; quality has not been tested here.
- MCP `create_font` versus REST output parity — not live-compared; current docs agree on `glyph_px` and omit `image_size`, and MCP now documents the 10×8 glyph order above.
- Whether re-rolling the `seed` or adjusting the description reduces `suspect_glyphs` at `8px`.

## Verification Guidance

- Extract and decode `ttf_base64`; render representative strings — uppercase, lowercase, digits, punctuation — at the target `glyph_px` and at integer multiples for inspection.
- Check the `suspect_glyphs` indices and visually confirm those plus high-frequency letters (E, A, O, S, R, L).
- Do not accept the atlas preview as the output or as proof of legibility.

## Related

- [`pixellab-image-size-limits.md`](pixellab-image-size-limits.md) — per-tool size limits, including native 8px/12px glyph sizes and the separate image-processing limits.
- [Resources](../resources.md#official-pixellab) — official documentation entry points.
