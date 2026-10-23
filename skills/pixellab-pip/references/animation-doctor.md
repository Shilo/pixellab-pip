# Animation doctor: checking frames, asking, re-rolling

`python assets/fix.py <frames|folder|sheet|gif> --out <dir>` measures every frame against "game ready" (smooth motion, clean transitions, colour match, no
dots or gaps, no artifacts between frames, no weird changes, crisp pixels at one scale), fixes for free what it can
from pixels the set already has, and writes `fix_report.json` + `fix_report.txt` + `fix_sheet.png` next to the fixed
frames. Originals are never written; every fixed frame is a local derivative of PixelLab's output, and the final report says so. Same frame count and names out as in. Frame numbers in the report count
from 1, like the file names, and each finding, change and plan lists its `files`.

## Look before "ready"

The checks are pixel measures. They can't see an extra hand, a scabbard that vanished while the sword is drawn,
a shortened blade, or a weapon missing in a fast-swing frame. `fix_sheet.png` puts the reference first: always
look at it and answer the report's `look` list. A failed item overrides the verdict; plan its re-roll by hand,
naming the fix in the prompt ("exactly two arms", "the empty black scabbard stays at the left hip", "the whole
blade from hilt to tip"). When the fault is in the reference sprite itself, every move inherits it: fix the sprite
first, then redo the poses.

`prop_drift` (low, a warning): in a one-shot, a held staff or blade leaves the span of the body side it holds in the
first and last frames (drifts to the centre line, changes hands). Look at those frames: a swing that crosses the body
is fine; a prop that should stay put is a re-roll of those frames naming the hand and side ("the staff stays upright in
her near right hand beside the robe").

## Stepped animations (`--stepped`)

Moves built from checked key poses on purpose, with no generated in-betweens (`key-pose-animation.md`): a draw-and-shoot, an iai cut, a flying kick, a snap hurt. Without the flag the motion checks read
the steps as jumps, a pose change as a vanished weapon and an airborne pose as off the ground, then drop frames or
pull a kick down to the floor. `--stepped` turns off `jump`, `missing_inbetween`, `loop_seam`, `size_pop`,
`weird_change`, `weapon_lost`, `broken_thin` and `ground`, keeps every clean, colour and crispness check (specks,
holes, edges, palette, brightness, flashes, pixel grid) and never drops, reorders or moves a frame. The report
says so under `skipped`. The look checklist matters more here: the steps are judged by eye.

## Effect frames (`--fx`)

Frames with an effect drawn in on purpose (a smoke vanish, a flash baked into the frame): `--fx 3,4,5` (the report's
1-based numbers). Nothing on them is judged, fixed or re-rolled - a smoke poof otherwise reads as a washed-out frame
and its loose puffs as detached pieces, and gets paid re-roll plans. The report lists them under `skipped`; judge
them by eye. A prop added on purpose (a bow on the back) makes the figure taller and reads as `size`: pass the new
sprite as `--ref`.

A thrown or held prop flying apart from the body (a lollipop in flight) reads as a one-frame effect or a detached
piece: pass those frames as `--fx` too.

## Approved key poses (`--keys`)

The first and last frame of a clip are usually the key poses you already checked at 3x. `--keys 1,11` keeps their
findings in the report but plans no paid re-roll for them (a slam pose with the ground debris asked for read as
broken, and the doctor planned 9 generations to redraw it). The report says so under `skipped`.

## Verdict

- `ready`: nothing to fix.
- `ready after free fixes`: everything that mattered was fixed locally (0 generations).
- `needs re-rolls`: something still fails; each failure has a plan (tool, frames, the change, cost).

## Changes

Every change is listed with `fixed` or `still failing` (re-measured after fixing). Timing changes (dropping a frame
by holding its neighbour, reordering a hurt) are proposals like effect changes, since they repeat or move frames
PixelLab returned; with `--accept` they are applied and listed; `timing.json` has the order and per-frame durations
(a 0 ms frame is a dropped one kept as a copy, for engines that load a fixed frame count).

## Proposals: ask before touching effects

Effects (slashes, glows, smoke) and soft effect edges are never changed on their own. They come back as `proposed`
changes. Ask the user **one** question listing each proposal with its recommended fix, e.g.
"Frame 3 has a flash that appears in no other frame - remove it? (recommended) / keep it". Then re-run `fix.py`
with the same inputs and `--accept c2,c5`. A lasting effect (2+ frames) is reported as information only: keep it.
When the project style (`project-style.md`) says soft edges are intended, soft edges aren't flagged.

## Re-roll plans

One plan per frame, whatever number of checks failed on it. When two or more frames of a generated clip fail and
their plans cost more than the clip did, the report gives one `whole clip` plan instead (same key frames, new seed).

A plan names the frames to redo (only those), the tool, the change to make and its cost; `job` is the original
generation from the run's `manifest.json` when it records one. A re-roll is paid: it goes through the approval level
in `auto.md` (at `plan` and `auto`, inside the redo allowance and budget; otherwise its own approval).

## Defect -> cause -> the change to make

| check | likely cause | tool | the change to make |
|---|---|---|---|
| `weapon_lost` | the pose prompt left the weapon out, so the generator dropped it | `edit_image_pro_flash` | write the weapon into the pose ("... raising the staff high in both hands") |
| `broken_thin` | thin parts (blades, staffs) break when a pose is redrawn | `edit_image_pro_flash` | name the weapon and its whole length in the pose; the reference as style image |
| `flash` | the action words invited a painted effect (burst, swipe) | `animate_image` | motion only, no burst, no swipe arc ("... in one fast snap") |
| `weird_change` | the in-between redrew part of the character | `edit_image_pro_flash` | same face, same outfit as the reference; the reference as style image |
| `head_change` | the in-between redrew the head: turned it away or toward the viewer, or changed the skin colour | `edit_image_pro_flash` | the same face, facing the same way as the frames around it, the same skin colour; the reference as style image |
| `jump` | an in-between left the motion path | `animate_image` | pin the path in the action ("the same arc, smoothly") |
| `missing_inbetween` | too few frames for that span of the move | `animate_image` | animate between these two frames (first_frame + last_frame), 2-4 frames |
| `size_pop` | a frame was drawn at another size | `edit_image_pro_flash` | the same size as the reference; the reference as style image |
| `loop_seam` | the loop's last frame doesn't lead back to its first | `animate_image` | animate from the last frame back to the first (last_frame = frame 0) |
| `return_to_stand` | the move ends away from the standing pose | `animate_image` | animate from the last frame back to the standing pose |
| `edge` | the pose touches the canvas border, so every in-between is cut | `edit_image_pro_flash` | re-pose on a canvas with more room on that side |
| `detached` | a piece came off the body (a thrown weapon or a floating bit) | `edit_image_pro_flash` | write the weapon into the pose, held in the hand |
| `grid` | the frame was drawn at another pixel size than the set | `edit_image_pro_flash` | re-draw the frame at the set's pixel size (no upscaling) |
| `mixels` | mixed pixel sizes in one frame (an upscale painted over) | `edit_image_pro_flash` | re-draw the frame at the set's pixel size (no upscaling) |
| `size` | the character is drawn bigger or smaller than the reference (a prop added on purpose, like a bow on the back, makes it taller: pass the new sprite as --ref) | `edit_image_pro_flash` | the same size as the reference; the reference as style image |
| `brightness` | a washed-out frame (colour matching would turn it muddy) | `edit_image_pro_flash` | the reference as style image, colour palette correction on |
| `palette` | the frame was drawn in other colours | `edit_image_pro_flash` | the reference as style image, colour palette correction on |
| `empty` | the generator returned an empty frame | `animate_image` | re-run the same span |
