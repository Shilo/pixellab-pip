# Reviewable Candidates

Read this when any static image-style MCP tool or REST endpoint returns multiple alternatives for a single requested result. Examples include candidates, review frames, grid cells, image batches, or small-image/object review packs.

Do not use this for ordered outputs where every frame/member is part of the requested structure, such as animation frames, directional rotations, tileset members, or spritesheet frames.

## Rule

- Show every user-facing candidate label starting at `1`.
- Never expose `0`-based candidate numbers to the user.
- Stop before saving, selecting, approving, dismissing, editing, animating, converting, or continuing from a candidate unless the user explicitly delegated selection.
- After parsing the user's reply, convert selected labels to `0`-based indices for tool/API calls.
- Apply this even when there is only one job or one requested asset; the trigger is multiple alternatives, not batch size.

## Display

Show candidates in a compact indexed form. Prefer an indexed contact sheet, inline previews with labels, or links with labels. Keep any local preview honest: it is for selection only, and final pixels still come from PixelLab or the user.

Use stable labels from `1..N` in the same order the tool/API returned alternatives. If the tool returns `0`-based frame IDs, add `1` for display.

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

For object review candidates, also say:

```markdown
To save/accept more varieties in PixelLab, open https://www.pixellab.ai/create-object.
```

## Handling Replies

- Single number: convert to `index - 1`, then continue with that selected candidate.
- Multiple numbers: convert each to `index - 1`, then save/keep those candidates.
- `all`: select every candidate.
- `dismiss`: discard/dismiss when the route supports it; otherwise leave candidates unsaved and report that nothing was selected.
- Invalid or out-of-range labels: ask again with the valid range, such as `1-16`.

If multiple candidates are kept but the next step needs exactly one base, keep the selected candidates first, then ask which kept result to use as the base.

## Continuing

After selection, continue the user's original task if enough information is available. For example, create the requested state/edit/animation from the chosen base, or finalize/download the chosen static result. If there is no follow-up action, report the selected output paths or managed asset IDs.
