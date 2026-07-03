# DualGrid Tileset Simulator

Use this developer tool from the `pixellab-pip/` repository root.

```powershell
python dev-tools/dualgrid_tileset_sim.py create_sidescroller_tileset --draw-grid --layout pixellab
```

The simulator renders a schematic compact 16-tile DualGrid/Wang sheet for MCP-style `create_sidescroller_tileset` and `create_topdown_tileset` request JSON.

If no request JSON is provided, it uses a minimal built-in request for the selected tool. For realistic testing, create a session-local request under `.local/` and pass it as the second argument:

```powershell
python dev-tools/dualgrid_tileset_sim.py create_topdown_tileset .local/topdown-request.json --draw-grid
python dev-tools/dualgrid_tileset_sim.py create_sidescroller_tileset .local/sidescroller-request.json --draw-grid
```

You can also pipe JSON through stdin:

```powershell
Get-Content .local/topdown-request.json | python dev-tools/dualgrid_tileset_sim.py create_topdown_tileset
```

Minimal sidescroller request:

- empty `lower_description`
- empty `transition_description`
- `tile_size: 16x16`
- `detail: low detail`
- `shading: flat shading`
- `outline: lineless`

Minimal top-down request:

- empty `lower_description`
- empty `upper_description`
- empty `transition_description`
- `tile_size: 16x16`
- `mode: standard`
- `view: high top-down`
- `detail: low detail`
- `shading: flat shading`
- `outline: lineless`

It always writes to:

```text
.local/dualgrid-sim-output/
```

Generated files:

- `dualgrid-corner-preview.png`
- `dualgrid-corner-preview-x8.png`
- `dualgrid-tileset-preview.png`
- `dualgrid-tileset-preview-x8.png`
- `dualgrid-patterns.json`

## Layouts

Use PixelLab's observed compact sheet order:

```powershell
python dev-tools/dualgrid_tileset_sim.py create_sidescroller_tileset --layout pixellab
```

Use the Lexaloffle row order alias:

```powershell
python dev-tools/dualgrid_tileset_sim.py create_topdown_tileset --layout lexaloffle-row
```

Use the TileMapDual standard atlas/key convention:

```powershell
python dev-tools/dualgrid_tileset_sim.py create_topdown_tileset --layout tilemapdual-standard
```

PixelLab/Lexaloffle uses bit weights `NW=8, NE=4, SW=2, SE=1` and defaults lower/filled terrain to bit value `0`.

TileMapDual uses bit weights `NW=1, NE=4, SW=2, SE=8` and defaults lower/filled terrain to bit value `1`.

## Options

- `--draw-grid`: draw magenta tile boundaries in preview PNGs.
- `--scale N`: set the nearest-neighbor preview scale. Default is `8`.
- `--layout NAME`: choose `pixellab`, `lexaloffle-row`, or `tilemapdual-standard`.
- `--filled-bit 0|1`: override which bit value maps to lower terrain.
- `--template-sheet PATH`: reuse alpha masks from an existing compact 4x4 PixelLab sheet.

## Caveats

This is a structure simulator, not a PixelLab art simulator. It does not predict PixelLab's generated texture, palette, prompt adherence, or exact compositing.

The simulator validates only the MCP-facing request shape that matters for structure. It does not call PixelLab, spend credits, poll jobs, download assets, or reproduce expanded top-down transition sheets.

`expected_pattern_4x4` in the JSON report is derived from tile corners. Do not assume downloaded PixelLab `pattern_4x4` fields are authoritative; local fixtures show they can disagree with `wang_N`, corners, and visual sheet position.

The platform preview is per-tile schematic. It can draw boundary pixels on edges that would be internal seams in a composed map. Template-sheet mode treats any opaque pixel as occupied, including decorative top or transition pixels.
