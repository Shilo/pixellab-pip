# PixelLab 1-Bit Tileset Optimization Workflow

Last reviewed: 2026-07-03.

Purpose: explain how to test PixelLab top-down and sidescroller tileset prompts when the target is a beautiful 1-bit style: black terrain masses with intentional white edge, rim, ledge, or boundary pixels.

This is a practical workflow for humans and agents. It documents what is known from PixelLab public docs, MCP docs, REST schema checks, DualGrid references, and local live tests. It does not claim to know PixelLab's private model internals.

## Source Summary

PixelLab publicly documents `Create Tileset` as a tool that generates tilesets from textures or text descriptions and can export to Wang, dual-grid 15-tileset, and 3x3 layouts. Its top-down mode asks for inner/outer terrain descriptions, while sidescroller mode uses center/top tile descriptions.

Current MCP docs describe top-down tilesets as 16 corner-combination Wang tilesets, with `transition_size` values such as `0`, `0.25`, and `0.5`. They describe sidescroller tilesets as 16 transparent platform tiles, where `lower_description` is the platform material and `transition_description` is the decorative top layer.

Current REST v2 schema exposes the same core fields and also exposes reference and palette controls that MCP may not expose: `lower_reference_image`, `upper_reference_image`, `transition_reference_image`, and `color_image`. Those controls are useful later, but they change the experiment from text-only MCP prompt testing.

DualGrid references agree on the important structural idea: the visible tile samples four neighboring terrain cells. A compact 16-tile sheet covers all corner combinations. PixelLab's observed compact 15-tileset order is documented in `pixellab-dualgrid-tileset-export-system.md`.

The visual style references for this project, such as Monochrome Caves, CanariPack 1BIT TopDown, and Kenney's 1-Bit Pack, are artist-made 1-bit assets. They are useful for taste: strong silhouettes, sparse highlights, readable edges, and exact black/white contrast. They are not evidence that PixelLab text-only generation can obey exact palette or exact edge placement.

## Mental Model

Think of PixelLab tileset generation as two layers of behavior:

1. Model generation: PixelLab interprets `lower_description`, `upper_description` or sidescroller `transition_description`, style controls, and optional references to create image content.
2. Tileset structure: the result is packed into a corner-based tileset where each output tile corresponds to a different terrain-corner combination.

The simulator can help with the second layer and with coarse semantic placement in the first layer. It cannot predict the exact live model drawing.

For prompt optimization, the useful question is:

```text
Did this wording put light pixels in the intended semantic place?
```

For 1-bit tilesets, the intended semantic place is usually one of:

- top-down wall/floor boundary
- top-down wall rim or contour
- sidescroller exposed top surface
- sidescroller exposed outside end caps
- sparse non-seam detail inside a dark body

Avoid asking whether the simulator image is beautiful. That is a live PixelLab/art review question.

## Why "White Border Around The Tile" Fails

`White border around the tile` is ambiguous and often harmful.

In a connected tileset, the output tile is not one standalone icon. It is one case in a set of corner combinations. A white border around every individual tile can create white seams between repeatable middle tiles. For a 1-bit terrain set, the useful wording is usually:

```text
white pixels only on exposed terrain boundaries, never on repeatable seams
```

Top-down and sidescroller routes need different wording because the fields mean different things.

## Top-Down Prompt Placement

Use top-down when the target is a wall/floor, room, cave, island, water/land, or other overhead terrain transition.

Field roles:

| Field | Meaning for 1-bit tests | What to put there |
|---|---|---|
| `lower_description` | lower/base terrain class | black floor, void, water, walkable space, or inside terrain |
| `upper_description` | upper/elevated terrain class | black wall, solid mass, raised terrain, rock, or outer terrain |
| `transition_description` | boundary between lower and upper | white rim, white wall edge, white contour pixels, ledge highlight |
| `transition_size` | width/height of the boundary band | start with `0.5` for top-down wall/floor tests; use `0.25` if the rim is too heavy |

For a black floor and black wall with white edges, both lower and upper can be black. Put the white wording in `transition_description`, not in the base terrain descriptions.

Expected composition behavior:

- Fully lower tiles should mostly look like lower terrain.
- Fully upper tiles should mostly look like upper terrain.
- Mixed-corner tiles should carry the transition/edge/rim information.
- A white outline should not appear on every side of every source tile. It should appear where lower and upper terrain meet in the corner pattern.

Recommended first top-down JSON:

```json
{
  "lower_description": "1-bit black floor void, flat solid black fill, no gray",
  "upper_description": "1-bit black wall mass, flat solid black interior, no gray",
  "transition_description": "one-pixel pure white rim pixels on the boundary where wall meets floor, white only on exposed contour edges, black interior, no gray",
  "transition_size": 0.5,
  "detail": "low detail",
  "shading": "flat shading",
  "outline": "lineless",
  "mode": "standard",
  "view": "high top-down",
  "tile_size": {
    "width": 16,
    "height": 16
  },
  "text_guidance_scale": 12
}
```

Test variants by changing one thing at a time:

- `transition_size: 0.25` vs `0.5`
- `white rim pixels` vs `white edge highlights` vs `white contour outline`
- `wall mass` vs `cave wall mass` vs `solid raised wall`
- `text_guidance_scale: 8` vs `12` vs `20`

## Sidescroller Prompt Placement

Use sidescroller when the target is platformer ground, ledges, blocks, cave platforms, or side-view terrain.

Field roles:

| Field | Meaning for 1-bit tests | What to put there |
|---|---|---|
| `lower_description` | center/platform body | solid black tileable body, black interior, no seam highlights |
| `transition_description` | top/surface decoration | white top rim, broken ledge pixels, exposed cap highlights |
| `transition_size` | amount of top/surface coverage | start with `0.25`; use `0.5` if the top band is too thin |

The sidescroller route has no separate end-cap prompt. End caps are generated as part of the 16 corner-combination tiles. This means the body prompt must avoid white seam language, and the transition prompt must explicitly say exposed top/end-cap edges only.

Recommended first sidescroller JSON:

```json
{
  "lower_description": "1-bit solid black platform center body, flat rectangular black terrain fill, horizontally tileable, black touches left and right edges, no white on repeatable seams, no gray",
  "transition_description": "pure white broken rim pixels only on exposed top surface and outside end-cap edges, never on middle tile seams, black interior, no gray",
  "transition_size": 0.25,
  "detail": "low detail",
  "shading": "flat shading",
  "outline": "lineless",
  "tile_size": {
    "width": 16,
    "height": 16
  },
  "text_guidance_scale": 12
}
```

Test variants by changing one thing at a time:

- `transition_size: 0.25` vs `0.5`
- `broken rim pixels` vs `top ledge highlights` vs `white cap edge pixels`
- with and without `outside end-cap edges`
- with and without `never on middle tile seams`
- `text_guidance_scale: 8` vs `12` vs `20`

## Simulator Workflow

Use `dev-tools/pixellab_mcp_tileset_sim.py` before live MCP spending.

The simulator is useful for:

- checking MCP request shape
- checking compact 16-tile layout and export layout
- checking whether text points light pixels toward lower, upper, top, transition, boundary, body, or seams
- inspecting component previews before the packed sheet

The simulator is not useful for:

- judging final beauty
- predicting exact PixelLab silhouettes
- predicting exact dithering
- predicting exact black/white palette compliance
- deciding whether a prompt will overcome PixelLab model priors

Recommended local loop:

1. Write 3-8 request JSON files under `.local/`.
2. Change only one prompt/control at a time.
3. Run deterministic first for structural sanity.
4. Run `--renderer deepseek-v4-pro` only when wording interpretation matters.
5. Inspect `sim-report.json` and `components/` before `tileset.png`.
6. Reject candidates where light pixels land in the wrong semantic class.
7. Promote the best 1-3 to live MCP tests.
8. Compare live outputs using the rubric below.
9. Update prompt wording from live behavior.

Example:

```powershell
python dev-tools/pixellab_mcp_tileset_sim.py create_topdown_tileset .local/topdown-rim-a.json --renderer deterministic --output topdown-rim-a
python dev-tools/pixellab_mcp_tileset_sim.py create_sidescroller_tileset .local/side-rim-a.json --renderer deepseek-v4-pro --output side-rim-a
```

## Live Result Rubric

Judge live PixelLab outputs in this order:

1. Topology: are the terrain masses usable?
2. Tileability: do repeatable center/body tiles avoid unwanted seams?
3. White placement: are white/light pixels on boundaries, rims, top surfaces, or exposed caps?
4. Interior control: are interiors mostly black when requested?
5. Transition control: do mixed tiles carry edge information while full tiles stay clean?
6. Native-scale readability: does it read at `16x16`?
7. Palette: how many non-black/non-white colors appeared?

Palette is last because exact black/white can be clamped after the fact if the PixelLab shape is good. A wrong silhouette, wrong seam, or wrong white-pixel placement cannot be fixed without locally repainting the actual art.

## Prompt Anti-Patterns

Avoid these for first-pass 1-bit tests:

- `white border around every tile`
- `black and white texture` without placement
- `sparse white speckles` when you actually mean edge highlights
- putting white wording in `lower_description` for sidescroller bodies
- making `upper_description` white in top-down when the desired wall mass should be black
- relying on `outline: "single color outline"` to place gameplay edges
- spending large live batches before simulator and component review

Prefer:

- `white rim pixels`
- `white edge highlights`
- `white contour pixels`
- `white only on exposed boundaries`
- `black interior`
- `never on repeatable seams`
- `exposed top surface`
- `outside end-cap edges only`

## When Prompt-Only Is Not Enough

Live tests already show that PixelLab may add gray, purple, blue, cream, or off-white drift despite strict `1-bit`, `pure black`, `pure white`, or `no gray` wording.

If text-only MCP keeps missing edge placement, the next controlled route is REST v2 with reference inputs:

- `color_image` for palette anchoring
- `transition_reference_image` for transition style anchoring
- `lower_reference_image` or `upper_reference_image` for terrain style anchoring

Treat those as production controls, not as text-only prompt tests. Keep the untouched PixelLab output separate from any palette-clamped derivative.

Do not assume `color_image` is always the safest first fix. In 2026-07-03 top-down REST tests with black lower terrain, black upper terrain, and white boundary pixels, both a mostly black palette image and a balanced black/white checker palette image collapsed the result to all black. The same prompt with `transition_reference_image` and no `color_image` restored visible near-white contour pixels on the wall/floor boundary. For black-on-black 1-bit terrain, test placement with `transition_reference_image` first; add `color_image` only as its own controlled follow-up after verifying it does not erase the transition.
