# Reviewable Candidates

Read this when any static image-style MCP tool or REST endpoint returns multiple alternatives for a single requested result. Examples include candidate arrays, review frames, grid cells that are alternative choices for one requested asset, or small-image/object review packs.

Do not treat a requested multi-asset batch as alternatives unless each requested asset has multiple candidates.

Do not use this for ordered outputs where every frame/member is part of the requested structure, such as animation frames, directional rotations, tileset members, or spritesheet frames.

## Rule

- Show every user-facing candidate label starting at `1`.
- Never expose `0`-based candidate numbers to the user.
- Stop before finalizing, accepting, reporting, editing, animating, converting, or continuing from a candidate unless the user explicitly delegated selection.
- Keep an internal mapping from each displayed label to the route-specific selector. After parsing the user's reply, use that mapping for tool/API calls. When the route expects `0`-based positional indices, pass `label - 1`; when it expects returned IDs, URLs, or frame IDs, pass the mapped value.
- Apply this even when there is only one job or one requested asset; the trigger is multiple alternatives, not batch size.

## Display

Show candidates in a compact indexed form. Prefer an indexed contact sheet, inline previews with labels, or links with labels. Temporary preview downloads/contact sheets are allowed when clearly treated as selection previews. Keep any local preview honest: it is for selection only, and final pixels still come from PixelLab or the user.

Use stable labels from `1..N` in the same order the tool/API returned alternatives. Never expose route-native `0`-based positions as user-facing labels.

## Prompt

For keep/save selection:

```markdown
**Choose Results**
Which result(s) do you want to keep?

Reply with: `3`, `1, 3, 6`, `all`, or `dismiss`.
```

For one base result before a follow-up:

```markdown
**Choose Base**
Pick the base before I continue.

Reply with one index, like `3`.
```

For PixelLab object review candidates, also say:

```markdown
To save/accept more varieties in PixelLab, open https://www.pixellab.ai/create-object.
```

## Handling Replies

- Single number: look up the mapped selector, then continue with that selected candidate.
- Multiple numbers: look up each mapped selector, then save/keep those candidates.
- `all`: select every candidate.
- `dismiss`: discard/dismiss when the route supports it; otherwise leave candidates unsaved and report that nothing was selected.
- Invalid or out-of-range labels: ask again with the valid range, such as `1-16`.

If multiple candidates are kept but the next step needs exactly one base, keep the selected candidates first, then ask which kept result to use as the base.

## Continuing

After selection, continue the user's original task if enough information is available. For example, create the requested state/edit/animation from the chosen base, or finalize/download the chosen static result. If there is no follow-up action, report the selected output paths or managed asset IDs.
