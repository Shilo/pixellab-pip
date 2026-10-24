# Animation doctor: checking frames, asking, re-rolling

`python <skill-dir>/assets/fix.py <frames|folder|sheet|gif> --check-only --out <dir>` inspects frames for heuristic anomalies (motion, colour drift, dots/gaps, identity changes and pixel scale), and writes `fix_report.json` + `fix_report.txt` only. Inspect the supplied images with available host tools. Omit `--check-only` only when the user requests/accepts the local repair scope; repairs write labeled copies, an inspection sheet and a verified preview into a fresh output location. Originals are never written; every fixed frame is a local derivative of PixelLab's output, and the final report says so. Same frame count and names out as in. Frame numbers in the report count
from 1, like the file names, and each finding, change and plan lists its `files`.

## Look before "ready"

The checks are pixel measures. They can't see an extra hand, a scabbard that vanished while the sword is drawn,
a shortened blade, or a weapon missing in a fast-swing frame. When produced, `fix_sheet.png` puts the reference first; otherwise compare the original frames and reference with host tools. Answer the report's `look` list. A failed item overrides the verdict; plan its re-roll by hand,
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
broken, and the doctor planned a paid redraw). The report says so under `skipped`.

## Verdict

- `ready`: no significant measured anomaly; not a visual-quality certification.
- `ready after free fixes`: everything that mattered was fixed locally (0 generations).
- `needs re-rolls`: something still fails; each failure has a plan (tool, frames, the change, cost).

Calibration comes from the source project's animation corpus, not every art style or size. Single-pixel details, intentional lighting and effects can be misclassified. Inspect before/after and reject a harmful suggested repair; no heuristic verdict supersedes visual checks or the requested output.

## Changes

Every change is listed with `fixed` or `still failing` (re-measured after fixing). Timing changes (dropping a frame
by holding its neighbour, reordering frames) are proposals like effect changes, since they repeat or move frames
PixelLab returned; with `--accept` they are applied and listed; `timing.json` has the order and per-frame durations
(a 0 ms frame is a dropped one kept as a copy, for engines that load a fixed frame count).
Input GIF zero-delay frames remain unchanged in `--check-only` reports. Repair output is refused before writing because its verified preview requires positive durations; choose playback timing explicitly through `local-asset-assembly.md` rather than treating a source zero delay as an accepted drop or inventing a delay.

## Proposals: ask before touching effects

Effects (slashes, glows, smoke) and soft effect edges are never changed on their own. They come back as `proposed`
changes. Ask the user **one** question listing each proposal with its recommended fix, e.g.
"Frame 3 has a flash that appears in no other frame - remove it? (recommended) / keep it". Then re-run `fix.py`
with the same unchanged inputs, one animation only, a fresh output location and `--accept c2,c5`. Acceptance IDs are local to that animation; never apply them to a batch. A lasting effect (2+ frames) is reported as information only: keep it.
For intentionally airborne moves, use the appropriate explicit inspection options and visual review; a ground-line heuristic cannot prove a defect. When the selected project profile says soft edges are intended, pass `--profile <selected-root>/pixellab.json`; the helper does not search the process working directory. Without this explicit path it uses no saved style facts.

## Re-roll plans

The helper groups repair suggestions for affected frames. It may propose one `whole clip` plan only for exact known raw-v3 ownership when the current conservative clip estimate is cheaper than individual repairs and no approved keys or excluded effect frames would be swept into that retry. This compares estimates, not historical charges.

A plan names the frames to redo (only those), the tool, the change to make and its cost (Pro Flash costs are measured size tiers, not quotes: get the live estimate per `pro-flash.md` before approval); `job` is the original
generation from the run's `manifest.json` when it records one. A re-roll is paid: follow `auto.md` and the current approved scope. Treat reported repair costs as estimates and validate the selected tool/size/frame controls against its current schema before approval; a diagnostic plan never authorizes payment.

## Defect guidance

Run `python <skill-dir>/assets/fix.py --table` for the helper's current defect → likely cause → tool → prompt-change suggestions. These are diagnostic suggestions; validate the live tool schema and visually inspect the affected frames before choosing a repair.
