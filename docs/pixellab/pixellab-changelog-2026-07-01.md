# PixelLab Changelog 2026-07-01

Purpose: record the PixelLab public-doc changes reviewed on 2026-07-01 and the corresponding PixelLab Pip documentation updates.

This changelog summarizes repository-facing updates only. The local upstream cache report that triggered the work is intentionally kept under `.local/pixellab-doc-watch/` and is not committed.

## Upstream Drift Reviewed

Source report:

- `.local/pixellab-doc-watch/reports/20260701T132334Z.md`

PixelLab public docs added:

- REST v2 `POST /generate-font-pro`.
- REST v2 `POST /portrait-character-pro`.
- REST schemas `GenerateFontProRequest`, `GenerateFontProResponse`, `PortraitCharacterProRequest`, and `PortraitCharacterProResponse`.
- MCP tools `create_font`, `get_font`, `create_portrait_character`, and `get_portrait_character`.
- Managed character animation fields `custom_start_frame` and `end_frame` on `CreateCharacterAnimationRequest`.

The follow-up refresh report `.local/pixellab-doc-watch/reports/20260701T132735Z.md` found no additional upstream changes after the local docs were updated.

## Local Skill Updates

Updated `skills/pixellab-pip/SKILL.md` to recognize:

- `font` as a target asset class.
- `portrait_character` as a target asset class.
- MCP-first routes for `create_font` and `create_portrait_character` when visible.
- REST v2 fallbacks `generate-font-pro` and `portrait-character-pro` for code, exact schema control, or MCP-unavailable workflows.

The core router intentionally keeps only the common routing facts. Detailed field and image-role guidance lives in reference files.

## Local Reference Updates

Updated `skills/pixellab-pip/references/image-input-roles.md`:

- Added portrait-to-character and character-to-portrait image roles.
- Clarified that `portrait-character-pro.image` is the source conversion image, not a style reference.

Updated `skills/pixellab-pip/references/prompt-limits.md`:

- Bumped the OpenAPI check date to 2026-07-01.
- Added `generate-font-pro.description` at 2000 characters.

Updated `skills/pixellab-pip/references/animation.md` and `preset-skeleton-template-animation.md`:

- Documented v3-only `custom_start_frame` and `end_frame` for managed character animation.
- Noted their one-direction requirement and incompatibility with template/pro modes.

Updated `skills/pixellab-pip/references/job-lifecycle.md`:

- Added MCP polling getters for fonts and portrait-character conversions.

Updated `skills/pixellab-pip/references/usage-reporting.md`:

- Clarified that REST live-call reports should include the exact public `/v2` HTTP path actually used, not only shorthand operation labels.

Updated `skills/pixellab-pip/references/official-pixellab-documentation.md`:

- Added the public REST/MCP boundary for Pro font generation and portrait-character conversion.
- Clarified that font generation should not be treated as generic lettering image generation.
- Clarified that portrait-character conversion should not be routed through normal text-to-character generation.

## Local Research Doc Updates

Updated `docs/pixellab/pixellab-asset-routing.md`:

- Added rows for portrait-character conversion and pixel font generation.

Updated `docs/pixellab/pixellab-user-facing-term-backend-mapping.md`:

- Added REST/MCP mappings for `generate-font-pro`, `portrait-character-pro`, `create_font`, `get_font`, `create_portrait_character`, and `get_portrait_character`.

Updated `docs/pixellab/pixellab-surfaces-and-services.md` and `docs/tools/official-pixellab-mcp-service-comparison.md`:

- Refreshed MCP/REST asset coverage language to include fonts and portrait-character conversion.

## Verification

Commands run:

```powershell
py dev-tools/pixellab-doc-watch.py status
py dev-tools/pixellab-doc-watch.py refresh
py dev-tools/pixellab-doc-watch.py status
rg -n "font|portrait-character|portrait_character|generate-font-pro|custom_start_frame|end_frame|2026-07-01" skills/pixellab-pip docs/pixellab docs/tools
git status --short
git diff --stat
```

Result:

- The final doc-watch refresh reported no further upstream changes.
- The final doc-watch status reported `last_change_detected: false`, `last_refresh_had_failures: false`, and `latest_complete: true`.
- Only Markdown skill/docs files were modified; `.local/` cache files remain local-only.
