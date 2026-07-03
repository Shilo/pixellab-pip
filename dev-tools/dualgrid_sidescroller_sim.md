# DualGrid Sidescroller Simulator

Use this developer tool from the `pixellab-pip/` repository root.

```powershell
python dev-tools/dualgrid_sidescroller_sim.py --draw-grid --layout pixellab
```

The simulator renders a schematic 16-tile DualGrid/Wang sheet using a minimal built-in sidescroller request:

- empty `lower_description`
- empty `transition_description`
- `tile_size: 16x16`
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
- `dualgrid-platform-preview.png`
- `dualgrid-platform-preview-x8.png`
- `dualgrid-patterns.json`

## Layouts

Use PixelLab's observed compact sheet order:

```powershell
python dev-tools/dualgrid_sidescroller_sim.py --layout pixellab
```

Use the Lexaloffle row order alias:

```powershell
python dev-tools/dualgrid_sidescroller_sim.py --layout lexaloffle-row
```

Use the TileMapDual standard atlas/key convention:

```powershell
python dev-tools/dualgrid_sidescroller_sim.py --layout tilemapdual-standard
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

`expected_pattern_4x4` in the JSON report is derived from tile corners. Do not assume downloaded PixelLab `pattern_4x4` fields are authoritative; local fixtures show they can disagree with `wang_N`, corners, and visual sheet position.

The platform preview is per-tile schematic. It can draw boundary pixels on edges that would be internal seams in a composed map. Template-sheet mode treats any opaque pixel as occupied, including decorative top or transition pixels.
