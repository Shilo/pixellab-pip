# PixelLab MCP Tileset Simulator

Agent bootstrap: use this tool when you need a cheap local PNG preflight for PixelLab MCP `create_sidescroller_tileset` or `create_topdown_tileset` JSON. Run it from the `pixellab-pip/` repository root.

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/sidescroller-request.json --draw-grid
```

The simulator accepts the same JSON object an agent would pass to the MCP create tool and writes local PNGs. Its purpose is cheap prompt/request experimentation before spending PixelLab generations.

Pass the same JSON object you would send to the MCP tool. If no request JSON is provided and stdin is empty, the simulator uses `{}` and fails when required MCP fields are missing.

For realistic testing, create a session-local request under `.local/` and pass it as the second argument:

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_topdown_tileset .local/topdown-request.json --draw-grid
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/sidescroller-request.json --draw-grid
```

You can also pipe JSON through stdin:

```powershell
Get-Content .local/topdown-request.json | python dev-tools/pixellab_mcp_tileset_sim.py create_topdown_tileset
```

Minimal sidescroller request:

```json
{
  "lower_description": "stone brick",
  "transition_description": "moss"
}
```

Minimal top-down request:

```json
{
  "lower_description": "ocean water",
  "upper_description": "sandy beach"
}
```

Omitted optional fields use the documented MCP defaults for simulation only. The simulator does not inject style defaults such as `low detail`, `flat shading`, or `lineless`; include those fields explicitly in the JSON when you want to test them.

By default, it writes to:

```text
.local/mcp-tileset-sim-output/latest/
```

Use `--output NAME` to compare multiple attempts:

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/a.json --output attempt-a
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/b.json --output attempt-b
```

Generated files:

- `corner-key-preview.png`
- `corner-key-preview-x8.png`
- `tileset.png`
- `tileset-x8.png`
- `sim-report.json`

Use `tileset.png` as the output under test. `corner-key-preview.png` is a schematic for checking the source corner classes. `sim-report.json` records the exact request, omitted MCP defaults used internally, native 15-tileset source cells, and exported cell placements; it is not a PixelLab MCP response.

## Export Layouts

Use PixelLab's native compact export:

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/request.json --layout 15-tileset
```

Use the website Wang export geometry:

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/request.json --layout wang
```

Use the website Godot 3x3 export geometry:

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/request.json --layout godot-3x3
```

The native 15-tileset uses PixelLab bit weights `NW=8, NE=4, SW=2, SE=1` and lower/filled terrain as bit value `0`. `wang` and `godot-3x3` repack the native simulated tiles into observed PixelLab website export dimensions.

## Options

- `--draw-grid`: draw magenta tile boundaries in preview PNGs.
- `--scale N`: set the nearest-neighbor preview scale. Default is `8`.
- `--renderer deterministic`: use the local deterministic renderer. This is the only renderer currently implemented.
- `--layout NAME`: choose `15-tileset`, `wang`, or `godot-3x3`.
- `--output NAME`: write under `.local/mcp-tileset-sim-output/NAME`.
- `--template-sheet PATH`: reuse alpha masks from an existing compact 4x4 PixelLab sheet.

## Caveats

This is an MCP-shape simulator, not PixelLab. The deterministic renderer uses simple keyword colors and texture rules, so it can compare request wording cheaply but does not predict PixelLab's generated texture, palette, prompt adherence, or exact compositing.

The simulator validates only the MCP-facing request shape that matters for local simulation. It does not call PixelLab, spend credits, poll jobs, download assets, or reproduce expanded top-down transition sheets.

Unsupported compact simulation cases fail intentionally, including top-down `transition_size: 1.0` and Pro top-down `transition_size >= 0.5`.

Future agent renderers such as `--renderer codex` or `--renderer claude` should be added as explicitly experimental modes. They must write labeled non-PixelLab outputs and must not be described as PixelLab predictions.

`expected_pattern_4x4` in the JSON report is derived from tile corners. Do not assume downloaded PixelLab `pattern_4x4` fields are authoritative; local fixtures show they can disagree with `wang_N`, corners, and visual sheet position.

The platform preview is per-tile schematic. It can draw boundary pixels on edges that would be internal seams in a composed map. Template-sheet mode treats any opaque pixel as occupied, including decorative top or transition pixels.
