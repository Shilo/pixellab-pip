# PixelLab Pip — Blueprint System Design

Status: approved design, pre-implementation. Date: 2026-07-05.

Human/developer design doc (docs/ is never loaded at runtime). Runtime behavior
will live in `skills/pixellab-pip/references/blueprint.md` plus small pointers in
`SKILL.md` and `references/usage-reporting.md`.

## Problem

Nothing durable on disk captures *how* a generation was made in a form that can be
replayed or shared. Today two JSON files land next to outputs, and neither fills the gap:

- **`*-manifest.json`** — agent-authored, freeform (shape varies per run), and *private
  by nature*: it carries local absolute paths, job UUIDs, account balance, plan tier, and
  cost deltas. Its purpose is a private audit/resume note. It is not shareable and has no
  stable schema.
- **`*.metadata.json`** — PixelLab's own API response blob. It embeds the inputs but
  buries them under response data (tile structure, `spritesheet_url`, `base_tile_ids`),
  does **not** record which tool/endpoint was used, is shaped differently per endpoint,
  and includes account-scoped URLs.

So a user who wants to recreate a past generation (with tweaks), hand it to someone else,
or reproduce it manually in the website/Aseprite has no clean artifact to work from. The
tool/endpoint + exact inputs exist only in the ephemeral chat report.

## Goals

- A minimal, uniform, human-readable, shareable file that records exactly **tool/endpoint
  + request inputs** — enough to regenerate an asset, or read by hand and reproduce it in
  the website/Aseprite.
- Agent can replay it (via `@link` or semantic recall) and apply natural-language
  **overrides** to any value, without rewriting the source file.
- Supports single-asset and ordered multi-asset bundles.
- Doubles as the format for hand-authored presets (none bundled yet).

## Non-goals

- **Not pixel-exact reproduction.** PixelLab states same-seed regeneration does not
  guarantee identical pixels. A blueprint reproduces *inputs*; PixelLab does its best.
- **Not a batch-runner pipeline.** No `{{var}}` templating, no CLI, no placeholder-repair
  machinery. Pip's runtime is the agent, which reasons about ordering and dependencies
  itself.
- **No bundled preset packs yet.** The format supports them; ship none until each is
  showcase-validated (repo policy against unverified tuning values).
- **No strict manifest schema.** The manifest stays freeform; it only gains a pointer.
- **No repo-wide reference rename.** The existing 21 references are already mixed
  singular/plural; renaming them is unrelated churn.

## The blueprint format

A `<name>.blueprint.json` file, **pretty-printed** (indented) because it is meant to be
read by humans and shared.

Shape: the route is the key, the request body is the value.

- **Route** = `"MCP <tool>"` or `"POST /v2/<endpoint>"`. (The verb/prefix already signals
  the surface; no separate "REST" word, no wrapper keys.)
- **Value** = the literal request body for that route. Include only the fields you want;
  any field left out uses the API's own default. So a one-field blueprint is valid.
- **Exact field fidelity (hard rule).** Every key and value must map verbatim to the real
  request body for that route — the exact field names and value shapes the MCP tool or REST
  endpoint accepts. Never rename, abbreviate, merge, or "simplify" a field: `style_image`
  is always `style_image`, never `image` or `style`; `first_frame` is never `frame`. A
  blueprint must be replayable by sending its value as the request body with no key
  translation. Image fields are just normal request fields under their true names; the field
  name already encodes the role, so no separate role wrapper is needed.
- **Image field values** may hold a **relative path** (default), an **absolute path**
  (opt-in), or **base64** (opt-in) — all three are distinguishable on read and resolved to
  whatever the endpoint needs at replay time. Only the *value representation* varies; the
  *field name* never does.
- **No** `blueprint_version`, `assets` wrapper, `images` wrapper, `route`/`input` keys, or
  `notes`.

**Single asset** — root object, one route key:

```json
{
  "MCP create_topdown_tileset": {
    "lower_description": "1-bit black and white black floor, solid black tile surface with no gray colors",
    "upper_description": "1-bit black and white upper black dirt surface with sparse white dirt texture speckles, no gray colors",
    "transition_description": "1-bit black and white dithered wall transition, black and white pixels only",
    "tile_size": { "width": 16, "height": 16 },
    "view": "low top-down",
    "detail": "low detail",
    "outline": "lineless",
    "shading": "flat shading",
    "transition_size": 0.5,
    "text_guidance_scale": 12,
    "seed": 1747915334
  }
}
```

**Minimal blueprint** — only the fields you care about; the rest default:

```json
{
  "POST /v2/create-image-pixflux": {
    "description": "a small mossy stone well, top-down"
  }
}
```

**Bundle** — an array of single-route objects, run in order. Order is preserved and there
are no duplicate-key collisions. A later step may reference an earlier step's output by
relative path:

```json
[
  {
    "POST /v2/create-image-pixflux": {
      "description": "a small mossy stone well, top-down",
      "seed": 123
    }
  },
  {
    "POST /v2/edit-image": {
      "image": "01-well.png",
      "description": "add a soft magical glow around the water",
      "seed": 123
    }
  }
]
```

## Behavior at generation time

After a successful generation, the agent writes `<name>.blueprint.json` next to the
outputs in the run's `pixellab-pip-generations/` folder.

If a generation used a **user-supplied source/reference/style/mask/frame image**, the agent
**copies that file** into the generation folder (a filesystem copy — it must not read the
image and re-write it) and references it by **relative path** inside the request body. This
guarantees the blueprint is reproducible and forensically complete even if the user's
original input is later moved or deleted, and it keeps relative-path sharing working (send
the JSON and the copied image together).

## Relationship to the manifest

The manifest is unchanged and stays freeform (private audit/resume record). It gains a
single line in `usage-reporting.md`: reference the blueprint file instead of restating the
inputs. Inputs are defined once (in the blueprint); the manifest points to it. No manifest
schema is introduced.

## Replay and override

Triggered when the user `@link`s a `.blueprint.json` or semantically refers to a past
generation whose blueprint exists in the folder. The agent:

1. Reads the blueprint (single object or array).
2. Maps each route to an available surface, falling back MCP↔REST per the existing Surface
   Rules if the recorded surface is unavailable.
3. Resolves image fields (relative path is relative to the blueprint file's location;
   absolute path and base64 as-is) to what the endpoint schema requires.
4. Applies any natural-language **overrides** the user requested ("same seed, new
   description", "everything but a random seed" → drop/replace `seed`). Overrides are
   temporary; the source blueprint is **never rewritten**.
5. Generates, reports normally, and writes a **new** blueprint + manifest for the new run.

For a bundle, steps run in order; a later step consumes an earlier step's output by relative
path (produced images never need re-supplying or base64).

## Sharing

- **The single `.blueprint.json` file (primary).** Most blueprints have no source image
  (text-only generations), so the JSON *is* the shareable unit — send the one file. When
  there is a source image, sending the JSON plus the image as two files also works: the
  recipient drops both together and the relative path resolves.
- **Base64 embed (self-contained single file):** on explicit request, embed the image as
  base64 so one JSON file carries everything. Only sensible for small images. Never written
  automatically — every read of a base64 blueprint pays the full image token cost, which is
  prohibitive across a folder of auto-saved blueprints.
- **Zip (optional, only if wanted):** blueprint + relative-path images zipped together.
  Tidy for multi-image bundles, but overkill for the common case — it adds pack/unpack work
  on both ends, so it is not the default.

## Caveats to state honestly (in the reference and in reports)

- Same-seed does not guarantee identical pixels; a blueprint reproduces inputs, not art.
- A blueprint that references an external image is only reproducible if that image travels
  with it (hence copy-into-folder + zip). Internally-produced images in a bundle are always
  available.

## Files changed

- **New** `skills/pixellab-pip/references/blueprint.md` — the runtime contract: format,
  the one convention (key = route, value = request body), minimal/partial inputs, image
  path/base64 modes, generation-time write + copy-not-rewrite, replay + override, bundles,
  sharing, caveats.
- **`skills/pixellab-pip/SKILL.md`** — a short blueprint trigger + Intent-Router pointer
  ("recreate a generation / `@link` a blueprint"), and one Asset-Integrity line (write a
  blueprint; copy user-supplied source images into the folder by copying, not rewriting).
- **`skills/pixellab-pip/references/usage-reporting.md`** — one line: the manifest
  references the blueprint instead of restating inputs.

## QA / CI

- Real blueprints live in the gitignored `pixellab-pip-generations/` tree — untouched by
  `qa.py` and by the "no tracked generated artifacts" check.
- If `SKILL.md` links `references/blueprint.md`, the file must exist
  (`check_skill_reference_files`) — created by this change.
- Any example blueprint JSON committed under docs would need to be valid JSON
  (`check_json_files`); examples in this doc are fenced markdown, not tracked `.json`, so no
  new JSON file is introduced.
- No change to `tests/test_helpers.py`.

## Rejected alternatives

- **Merge blueprint into the manifest.** Rejected: the only overlap is `input` (the whole
  blueprint), and merging forces the shareable half to inherit the manifest's private leak
  surface (paths, balance, job IDs). Separate files, manifest points to blueprint.
- **Verbose `{ "route": …, "input": … }` shape.** Rejected: after deleting version/notes/
  images there is no future field to justify the extra keys; route-as-key is more concise
  and still self-evident.
- **Competitor-style templating/CLI pipeline.** Rejected: rebuilds a product shape the repo
  already declined; the agent supplies the intelligence a script would need.
- **Repo-wide singular reference rename.** Rejected: churn with zero behavior change.
