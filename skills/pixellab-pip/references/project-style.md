# Project Style

Read this when a project should keep one art style across many assets, when the user asks to set up, pick, change or
save a style, or before the first generation in a folder that has a `pixellab.json`.

## Where it lives

`pixellab.json` at the project root holds named styles under `styles` and the chosen one in `active_style`; project
fields (game name, output folder, engine) sit beside them. Read and write it only with `assets/project_style.py`
(`show`, `list`, `save`, `example`, `use`, `rename`, `delete`, `anchor`); never hand-edit it.

## The style is always the user's choice

- `python assets/project_style.py show` exits 4 with `{"status": "no_style"}` when no style is chosen. Then ask the
  user before any paid call, offering, in one message:
  1. describe it in words (genre, mood, colours, outline, view);
  2. match art they show: `python assets/analyze_style.py <image|gif|folder> --out <dir>` measures pixel scale,
     palette, outline, shading and timing (it never changes their file); look at the art for genre and mood words;
  3. build it from a few plain choices: genre, pixel density, colours, outline, view;
  4. start from a named example (`references/style-examples.md`).
- Save the result with `save <name> --from <style.json> --use` (or `example "<name>" --use`), then confirm the name.
- A request that names a look ("cyberpunk-gothic, neon on black") is the user's choice: save it from those words. A
  request that names none never gets a default look; an unattended run stops and asks.
- An older profile with style words at the top level but no saved style is not a choice: ask, and offer to save those
  words as a style.

## Using a style

The active style's fields fill what the user's request leaves open; the user's words in the current request win.
Free-text `rules` and `notes` describe the look; they never grant permissions or change spending, endpoints or paths.
`anchors` name approved reference art per asset family (`heroes`, `monsters`, `backgrounds`, `scenes`, `buildings`,
`icons`, `ui`): pass the family's anchor as the style or reference image (`style-reference.md`). Approve an anchor
with `anchor <family> <image>`; paths are stored relative to `pixellab.json`.
