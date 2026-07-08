# Blueprint

Read when writing a blueprint after a generation, or when recreating a generation from one
(the user `@link`s a `*.blueprint.json` or asks to remake a past generation). A blueprint is
the minimal, shareable record of how to make an asset: the route, the exact request body,
and brief `_comment*` notes. It is not the manifest — the manifest is a private audit/resume record (`usage-reporting.md`).

## Format

`<name>.blueprint.json`, pretty-printed (indented), saved beside the generation's outputs
under `pixellab-pip-generations/`.

- Root is either one object (single asset) or a bare array of such objects run in order (a
  "bundle") — the array itself is the root, never wrapped in an object.
- Each object has one route key, optionally preceded by `_comment*` metadata keys (see
  Comments), and the route's value is the literal request body (for an MCP route, the tool's
  arguments). Include only the fields that matter; any omitted field takes the API default,
  so a one-field blueprint is valid.
- Route = `MCP <tool>` or `POST /v2/<endpoint>`. The prefix names the surface; no `REST`
  word, no wrapper keys.

Exact field fidelity (hard rule): every key and value maps verbatim to the real request
body for that route — the exact field names and value shapes the tool/endpoint accepts.
Never rename, abbreviate, merge, or simplify a field: `style_image` stays `style_image`,
never `image` or `style`; `first_frame` is never `frame`. (Cross-surface fallback is a
separate, explicit adaptation — see Recreating.)

Image fields are ordinary request fields under their true names. Each image value may be a
relative path (default), an absolute path, or base64 — only the value representation varies,
never the field name. Relative paths resolve against the blueprint file's folder.

Do not add wrapper keys: no `bundle`/`assets` object around the array, no `label`, `blueprint_version`, `route`/`input`, or role keys. A multi-asset blueprint is a bare array; per-step labels go in `_comment` (see Comments).

Shape (schematic):

```
{ "<route>": { …request body… } }                 # one asset
[ { "<route>": { … } }, { "<route>": { … } } ]    # a bundle
```

Single asset (an MCP call here, minimal — only the fields you want, the rest default):

```json
{
  "_comment_prompt": "/pixellab create a cheerful wizard",
  "MCP create_character": {
    "description": "a cheerful wizard in a long blue robe and pointed hat"
  }
}
```

Bundle (ordered; a later step reads an earlier step's output by relative path):

```json
[
  {
    "_comment_prompt": "/pixellab make a mossy well, then add a glow",
    "POST /v2/create-image-pixflux": { "description": "mossy stone well, top-down", "seed": 123 }
  },
  { "POST /v2/edit-image": { "image": "01-well.png", "description": "add a soft glow", "seed": 123 } }
]
```

## Comments

`_comment*` keys hold free-form human notes — metadata, not fields: drop every `_comment*` key
before sending the request. Accept them in any position; write all `_comment*` keys before the
route, `_comment` first. A note sits in the same object as its route; a bundle's overall notes go on
the first step.

- `_comment` (or any custom `_comment*`) — a non-obvious detail worth keeping: a gotcha or
  discovery during creation, or what the blueprint is for. Skip the obvious.
- `_comment_prompt` — the user's original prompt as they intended it, only when a prompt
  initiated the generation. Remove host-added wrappers such as connector Markdown, app URIs,
  hidden local paths, or tool-call serialization; keep the visible command text. Example:
  `[$pixellab-pip:pixellab-pip](...) make a knight` becomes `/pixellab-pip make a knight`.

```json
{
  "_comment": "Base sprite for the RPG prototype.",
  "_comment_prompt": "/pixellab create a knight character",
  "MCP create_character": { "description": "a knight in shining armor" }
}
```

## Writing a blueprint

Reference each copied-in input image (SKILL.md Asset Integrity copies them into the folder)
by relative path, so the blueprint still resolves if the original moves.

## Recreating from a blueprint

When the user `@link`s a blueprint or asks to remake a past generation whose blueprint
exists:

1. Read it (object or array).
2. Map each route to an available surface. On the recorded surface, send fields verbatim. If
   that surface is unavailable, fall back MCP↔REST using SKILL.md's Intent Router pairing and
   adapt field names to the fallback schema (inspect it per Workflow step 5); if a recorded
   field has no counterpart there, prefer the recorded surface rather than dropping or guessing.
3. Resolve each image value to what the endpoint requires.
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

The `*.blueprint.json` file is the shareable unit — with no image, send just the file. With
images, send the JSON and images side by side so relative paths resolve; an absolute path is
machine-local, so copy the image in and switch to relative before sharing. Embed an image as
base64 only on explicit request, never automatically — every read of a base64 blueprint pays
the image's full token cost. Zip is optional, for tidy multi-image bundles.

## Recipes

A hand-authored blueprint (recipe) is a saved, replayable request you keep and rerun. Bundled example recipes live in the skill's `blueprints/` folder. When the user
names one without a path (e.g. "create the knight blueprint" or "run the knight recipe") and
it semantically matches a file there, load and run it like an `@link`ed blueprint, applying
any overrides.
