# Normal Maps

Read this for sprite/animation normal maps and optional preparation, splitting or lighting inspection. Canonical input roles, per-frame limits and convention are in `image-input-roles.md`; public MCP `create_normal_map` and REST `POST /normal-map` are distinct transports.

## Route and representation

- MCP accepts documented PixelLab image/animation references, PNG/GIF URLs/base64 and animation strips. Prefer an existing reference/URL; do not force download/re-upload or GIF conversion. A managed animation reference already identifies its frames. The descriptor documents strips, but how an arbitrary MCP strip's frame count is detected has not been empirically verified here; do not invent a `frames` parameter.
- REST uses an encoded image: one sprite, or an equal-cell horizontal PNG strip plus explicit `frames`. Verify dimensions/frame count before sending it.
- Set `kind` when known (`character`, `object`, `topdown`, `side`, `iso`, `ui`). The current MCP default is `mode="lite"` (documented 0.1 generation); `pro` plans parts (documented 0.5 generation). Mode prices are estimates until actual usage is exposed. Do not silently upgrade modes or assume Pro is always necessary.
- Use OpenGL convention for engines expecting green-up and DirectX for engines expecting green-down, such as Unreal; preserve an explicit user convention. Tune strength/shape/detail only for a stated problem, using controls the selected schema actually exposes.

## Optional preparation and inspection

Local helpers are conveniences for the requested representation, not mandatory deliverables. `assets/normal_map.py gif <out.gif> <frames...>` prepares a GIF only when wanted; GIF palette/alpha limits may lose source information, so keep originals and verify decoded correspondence. Prefer supported lossless/reference inputs when that matters. `normal_map.py split` can split an equal-width returned strip into frame maps; check count, dimensions and original frame order.

One earlier Pro-mode lunge showed bands on late frames; processing the affected poses separately helped that example. This is scoped evidence, not a universal limitation of Lite, all attacks or MCP strips. If an actual result bands, propose a separately approved smaller segment or mode/control experiment rather than automatically increasing calls. Describe every segment and added cost before spending.

When requested or needed to diagnose a defect, `normal_map.py preview` renders a separate labeled lighting simulation (`--directx` for that convention). It is an inspection aid with a synthetic light, not provider art or proof of engine integration. Check source correspondence, visible coverage, silhouette and lighting response; binary normal-map alpha need not equal fractional source alpha.

For engine integration, pair diffuse and normal textures using the engine's supported normal-map material/texture path and actual project version. Godot uses `CanvasTexture`; Phaser uses the Light2D pipeline; Unreal typically expects DirectX convention. Verify animation-frame pairing and import settings in that engine before promising an engine-ready result; local light previews do not establish import fidelity.
