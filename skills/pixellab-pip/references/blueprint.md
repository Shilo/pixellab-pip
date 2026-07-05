# Blueprint

Read when writing a blueprint after a generation, or when recreating a generation from one
(the user `@link`s a `*.blueprint.json` or asks to remake a past generation). A blueprint is
the minimal, shareable record of how to make an asset: the route plus the exact request
body. It is not the manifest — the manifest is a private audit/resume record (`usage-reporting.md`).

## Format

`<name>.blueprint.json`, pretty-printed (indented), saved beside the generation's outputs
under `pixellab-pip-generations/`.

- Root is either one object (single asset) or an array of such objects (a bundle, run in
  order).
- Each object has exactly one key: the route. Its value is the request body (for an MCP
  route, the tool's arguments).
- Route = `MCP <tool>` or `POST /v2/<endpoint>`. The prefix names the surface; no `REST`
  word, no wrapper keys.
- Value = the literal request body. Include only the fields that matter; any omitted field
  takes the API default, so a one-field blueprint is valid.

Exact field fidelity (hard rule): every key and value maps verbatim to the real request
body for that route — the exact field names and value shapes the tool/endpoint accepts.
Never rename, abbreviate, merge, or simplify a field: `style_image` stays `style_image`,
never `image` or `style`; `first_frame` is never `frame`. The value must be sendable as the
recorded route's request body with no key translation. (Cross-surface fallback is a separate,
explicit adaptation — see Recreating.)

Image fields are ordinary request fields under their true names. Each image value may be a
relative path (default), an absolute path, or base64 — only the value representation varies,
never the field name. Relative paths resolve against the blueprint file's folder.

Do not add `blueprint_version`, wrapper keys, `route`/`input` keys, role tags, or notes.

Single asset:

```json
{
  "POST /v2/create-image-pixflux": {
    "description": "a small mossy stone well, top-down"
  }
}
```

Bundle (ordered; a later step reads an earlier step's output by relative path):

```json
[
  { "POST /v2/create-image-pixflux": { "description": "mossy stone well, top-down", "seed": 123 } },
  { "POST /v2/edit-image": { "image": "01-well.png", "description": "add a soft glow", "seed": 123 } }
]
```

## Writing a blueprint

The blueprint is written after a successful generation, and input images are copied into the
folder, per SKILL.md Asset Integrity. Reference each copied image by relative path, so the
blueprint stays reproducible if the original later moves or is deleted.

## Recreating from a blueprint

When the user `@link`s a blueprint or asks to remake a past generation whose blueprint
exists:

1. Read it (object or array).
2. Map each route to an available surface. On the recorded surface, send fields verbatim. If
   that surface is unavailable, fall back MCP↔REST using SKILL.md's Intent Router pairing and
   adapt field names to the fallback schema (inspect it per Workflow step 5); if a recorded
   field has no counterpart there, prefer the recorded surface rather than dropping or guessing.
3. Resolve image values (relative path from the blueprint's folder, absolute path, or
   base64) to what the endpoint requires.
4. Apply the user's natural-language overrides to any value — e.g. keep the seed but change
   `description`, or use every value with a random seed. Overrides are temporary; never
   rewrite the source blueprint.
5. Generate, report per `usage-reporting.md`, and write a new blueprint + manifest for the
   new run; copy any input image the new blueprint references into the new folder so it stays
   self-contained.

For a bundle, run steps in order, and save each produced image to the exact relative
filename a later step references (e.g. `01-well.png`) so the next step consumes it. A bundle
replay spends credits per step — apply SKILL.md's multi-asset batch approval first.

Same seed does not guarantee identical pixels (`official-pixellab-documentation.md`); a
blueprint reproduces inputs, not exact art. Say so when reusing a seed.

## Sharing

The single `*.blueprint.json` file is the shareable unit; most have no image, so send the one
file. With an image, send the JSON and the image together — the relative path resolves when
they sit side by side. A blueprint carrying an absolute image path is machine-local — copy
the image in and switch to a relative path before sharing. For a self-contained single file
on explicit request, embed the image
as base64; never do this automatically, because every read of a base64 blueprint pays the
image's full token cost. Zip is optional, only for tidy multi-image bundles.

## Presets

A hand-authored blueprint is a preset. Do not bundle preset packs until each is
showcase-validated (standing policy against unverified tuning values).
