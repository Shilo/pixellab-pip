# Blueprints

A **blueprint** is a small JSON file that records exactly how one PixelLab asset was made —
the tool/route used and the inputs sent — so you (or anyone you send it to) can recreate that
asset later, with or without changes. Think of it as a recipe card for a generation.

It is deliberately minimal and human-readable: just the route, the request values, and short
human notes — no account or cost metadata. That makes a blueprint easy to share; the notes do
carry the wording of the request that created it, so skim them first if that matters.

## What's inside

A blueprint file is named `<name>.blueprint.json` and comes in two shapes.

**One generation** — a single object with one route key holding the exact request as its value,
plus `_comment*` notes (see Comments below):

```json
{
  "_comment_prompt": "/pixellab create a knight character",
  "MCP create_character": {
    "description": "a knight in shining armor holding a sword and shield"
  }
}
```

Only the fields that matter are included — anything left out uses PixelLab's default, so a
one-line blueprint is perfectly valid. Image inputs (a source, reference, style, or mask image)
are referenced by a relative filename kept next to the blueprint.

**Multiple generations** — a JSON **array** of those objects, run top to bottom. A later step
can use an earlier step's output by referencing its filename, so you can chain steps — for
example, "make an image, then edit it":

```json
[
  {
    "_comment_prompt": "/pixellab make a mossy stone well, then add a magical glow",
    "POST /v2/create-image-pixen": { "description": "a small mossy stone well, top-down", "seed": 123 }
  },
  { "POST /v2/edit-image": { "image": "01-well.png", "description": "add a soft magical glow", "seed": 123 } }
]
```

Here the second step edits the well the first step produced (saved as `01-well.png`). Each step
spends credits, so the assistant confirms the plan before running a multi-step bundle.

## Comments

A blueprint can carry short human notes as keys starting with `_comment`. They are only for
people reading the file — the assistant ignores them when it runs the blueprint.

```json
{
  "_comment": "base sprite for the RPG prototype",
  "_comment_prompt": "/pixellab create a knight character",
  "MCP create_character": { "description": "a knight in shining armor" }
}
```

When both are present, `_comment` (the summary) comes first, then `_comment_prompt` — like a
doc-comment. `_comment_prompt` holds your originating prompt (in a bundle, on the first step);
a `_comment` is added only for something non-obvious worth sharing — an issue, discovery, or
important detail found during creation, or what the blueprint is for.

## Creating a blueprint

You don't have to do anything special: after a successful generation, the assistant writes the
blueprint next to the asset's output files (under your project's `pixellab-pip-generations/`
folder). If the generation used an image you supplied, a copy of that image is saved alongside
so the blueprint stays reproducible even if your original moves.

## Recreating from a blueprint

Two ways to trigger it:

- **Point at the file:** `@`-link or mention the `.blueprint.json` and ask to run it.
- **Just describe it:** if the blueprint lives in the bundled presets (below), name it — e.g.
  *"create the knight blueprint"* — and the assistant finds and runs it.

**Overrides.** You can change any value in plain language when recreating; the original file is
never modified. For example:

- *"Recreate that knight blueprint but make the armor red."*
- *"Same blueprint, keep the seed but change the description to a dark wizard."*
- *"Run it again with a random seed."*

> **Note:** reusing the same seed reproduces the same *inputs*, but PixelLab does not guarantee
> pixel-identical art from a repeated seed. A blueprint reliably reproduces the recipe, not an
> exact copy of the pixels.

## Presets (blueprints you can run by name)

Ready-made example blueprints ship in the skill's `blueprints/` folder — currently a minimal
`knight.blueprint.json`. Name one without a path and, if it matches, the assistant loads and
runs it. For your own blueprints, point at the file (see Recreating, above) — the skill's
`blueprints/` folder holds bundled examples and may be overwritten when the plugin updates.

## Sharing

A blueprint is meant to be shared:

- **No image:** just send the single `.blueprint.json` file. This is the common case.
- **With an image input:** send the JSON and its image together; the relative path resolves
  when they sit side by side.
- **One self-contained file:** on request, an image can be embedded directly in the JSON as
  base64 (larger file, but nothing else to send).

Whoever receives it can recreate the asset the same way — point their assistant at the file, or
drop it into their `blueprints/` folder to run it by name.

## MCP vs REST

Blueprints record whichever surface produced the asset — an `MCP <tool>` route or a
`POST /v2/<endpoint>` route. On recreation the assistant maps it to whatever you have available,
falling back between MCP and REST when needed. MCP routes are handy for sharing because they run
through your assistant's existing PixelLab connection without a separate API key.
