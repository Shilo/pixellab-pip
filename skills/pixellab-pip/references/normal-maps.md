# Normal Maps

Read this before MCP `create_normal_map` or REST `POST /normal-map` on a sprite or an animation, so an engine can light it. Input roles and size limits are in `image-input-roles.md`; preview helpers in `local-asset-assembly.md`.

## Input

- A PixelLab asset passes straight in by reference (`character:<id>:<direction>[:<animation>]`, `object:<id>`, `job:<id>`, `gallery:<id>`); no download or upload.
- Local animation frames on MCP: pack them into one GIF (`assets/normal_map.py gif <out.gif> <frames...>`) and send that. A PNG strip on MCP is read as one image (and refused over 1024 px); REST takes an equal-frame horizontal strip with `frames`.
- `convention`: `directx` for Unreal, `opengl` for every other engine. Set `kind` when known (above all sidescroller, isometric and UI art).

## Split clips at big pose changes

One call plans the shapes on the first frame and carries them to the rest. Idles and walks are fine whole; an attack whose silhouette changes a lot gets horizontal bands on the frames far from frame 1 (an 11-frame lunge banded its last 4 frames; the same 4 frames sent alone came out clean). Cut the clip where the silhouette changes (wind-up, strike, recover) and send one GIF per segment, submitted together. List the segments and calls in the plan before spending.

## Check

1. Split each returned strip back into per-frame maps beside their frames (`normal_map.py split`).
2. Preview with a light circling the sprite (`normal_map.py preview`, `--directx` for DirectX maps) and look at `<out>_lights.png` once: every part should get brighter on the lit side. Bands or flat patches → re-run that segment with fewer frames (a new paid call).

## Engine wiring (tell the user the steps for theirs)

- Godot 4: a `CanvasTexture` with the sprite as Diffuse and the map as Normal (per frame in `SpriteFrames` for animations), plus a `PointLight2D` or `DirectionalLight2D`.
- Unity (URP 2D): Sprite Editor → Secondary Textures → `_NormalMap` = the map; a Sprite-Lit material and 2D lights.
- Phaser 3: `this.load.image('k', ['k.png', 'k_n.png'])`, `sprite.setPipeline('Light2D')`, `this.lights.enable()`.
- Unreal (Paper2D): `directx` maps and a lit sprite material.
