# Whip (bullwhip, chain whip, energy lash) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

From one whip test (an overhead crack, Pro Flash key poses + `animate_image`); no reference sheet yet, so the
side lash and wrap are untested. Facing right.

## What every pose keeps
- **Name the holding arm by its look** in every pose (rule: `characters.md`; e.g. `her black-gloved right arm holds
  the whip handle`). A character with one arm that differs (a chrome cyber arm, a gauntlet) swapped the whip into
  that arm until both poses named it.
- **The handle stays in the fist; the lash is the moving prop.** Name the lash's length and its tip
  (`a long black leather lash, about her height, ending in a glowing magenta tip`) in every pose, or it shortens.
- **One lash, one tip.** Wide poses grow a second lash or a loop.

## Canvas
- The lash at full stretch runs about 1.3 x the body height in front of the hand. 256x200 with the sprite at x≈40
  (~125 px in front) held a shoulder-height crack for a ~95 px wide hero; the overhead wind-up curls the lash behind the
  head, so keep ~30 px above the hair. Widen afterwards (`bake_fx.py --widen`) for a tip spark past the edge.

## Moves as key poses (A -> B, effect in screen terms)
- **Overhead crack (forward):** A = `whip hand raised high behind her head, the lash trailing behind her in a loose
  S-curve toward the left of the image` -> B = `deep lunge, whip arm thrust straight forward at shoulder height, the
  lash snapped out straight toward the right of the image, the tip at the far end`. `animate_image` 10 frames between
  them rolled the lash over her head convincingly on the first try once the poses were right.
- **Side lash (waist height):** A = whip hand pulled back past the hip, lash trailing low behind -> B = arm swept
  across in front, lash out level at waist height. Untested.
- **Wrap / grab:** B with the lash coiled around a point ahead (`the lash's end wound twice around a post at the
  right of the image`), held, then a pull-back pose. Untested.
- **No crescent slash.** The effect is a **crack spark at the tip on the hit frame**: a small `vfx_workbench` burst (a
  ring is enough; a white ring on a bright core can read as an eye icon at 2x - use a star or rays instead), placed at
  the tip with `bake_fx.py --at <tip>`. A faint line along the lash on the frame before the hit sells the speed.

## Frame rhythm
- The hit is the first frame where the lash is straight; the 10-frame clip held that pose 3 frames in a row (8-10) -
  propose keeping one at 140 ms and giving the others 60, or cutting them (only if the user agrees).
- Wind-up hold 160 ms, the roll over the head 60 ms a frame, crack 140, settle 120.

## Pitfalls to name in prompts / check at 3x
- **The tip drifts back to the hand** in the mid in-betweens, so the lash reads as a loop from the hand back to the
  hand (frames 4-6 of the test). Put the path in the action: `the lash rolls forward over her head in one wave, the
  tip always the farthest point from her hand`; if it still loops, propose re-rolling that span as a short splice (4 frames), a paid call under `auto.md`.
- **The whip changes hands** for a frame (the cyber arm held it in frame 7): name the arm in the action as well.
- **Face goes grey in wide poses**: `the same pale face` in both poses.
