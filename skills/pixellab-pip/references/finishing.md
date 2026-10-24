# Finishing

Read this before cleaning up or finishing generated frames locally: stray pixels, flashes, floating poses, colour drift, colour variants, swing trails, thrown props, and baked effects.

## Contents

- [Contract](#contract)
- [Approval](#approval)
- [Order](#order)
- [Clean-up helpers](#clean-up-helpers): ground_snap, scrub, despeckle, colormatch, apply_palette, recolor_trail, recolor_groups, recolor_like, dir8_finish
- [New-pixel helpers](#new-pixel-helpers): slash_layer, throw_prop, bake_fx, blade_trail

## Contract

Quote frame wildcards (`"raw/*.png"`) so the helper sorts `0.png .. 10.png` in number order; a shell that expands them first puts `10.png` before `2.png`.

The helpers live in `assets/finish/`; resolve them to the installed skill's absolute path as in `local-asset-assembly.md`. They need Pillow and numpy (some also scipy); when unavailable they print a JSON `status: skipped` with the missing dependency and exit 3 — report the step as not done, never as passed. Do not install packages to run them unless the user asks.

- Every helper requires `--out <dir>` and writes copies only; it preflights collisions with inputs and existing outputs. Raw PixelLab outputs stay untouched beside the finished copies. Give each step its own folder inside the run, e.g. `pixellab-pip-generations/<run>/finish/1-ground-snap/`.
- Each run writes `<out>/derivative.json`: `helper`, `category` (`cleanup` or `new_pixels`), `inputs`, and per-frame `changes`. Use a fresh output folder for each step or revised attempt; previous copies/records remain untouched. Report every derivative as a local derivative, name the helper and its changes, and record the step as a `TASK` in the blueprint (`blueprint.md`).
- The `new_pixels` category describes a helper's capabilities, not the provenance of every operation. Compositing generated VFX or a supplied prop is a local derivative; procedural painting creates non-PixelLab content. Apply the Approval rule below to the actual transformation. Prefer a supported PixelLab route when it fits — `vfx_workbench` for effects, `pixelart_workbench` for pixel repairs.
- Look at every output frame before calling it finished; a helper's exit 0 means it ran, not that the art is right.

## Approval

Apply SKILL.md Asset Integrity to the actual operations, not the helper category. Run only requested/accepted transformations, report their changes and keep the originals. A named accepted plan can cover its listed local derivatives/fallbacks; a cost toggle or saved style cannot. New locally painted content requires the explicit labeled non-PixelLab fallback scope. Timing substitutions/mirroring/holds also require the requested playback scope.

## Order

Ground-snap → clean (scrub, despeckle, colormatch, palette and recolour) → trails and effects. Snapping first keeps feet-line measurements on the raw silhouettes; effects go last so the clean-up never eats them. Build sheets and GIFs from the last folder.

## Clean-up helpers

### ground_snap

Moves floating frames down so their lowest pixel sits on the standing sprite's feet line (pad offset + the sprite's lowest row); `--out` gets every frame, moved or not. Frames already below the line are copied unchanged and flagged "below the feet line" — look at them (a robe or an effect hangs lower). `--fx 5,6` leaves feetless frames (smoke-only) alone, counted from 1 in the list given. `--check` prints the gaps and writes nothing. Only for grounded moves, never jumps or flyers. It trusts the lowest opaque pixel: when that is not the anchor (sparks or a burst under the body, a body rising out of a crack), run `--check`, look, and leave those frames out with `--fx` or don't snap.

```bash
python ground_snap.py hero.png 24,56 "raw/*.png" --out finish/1-ground-snap [--fx 5,6] [--check]
```

### scrub

Clears flashes and streaks the generator painted in. Clip mode: in a raw `0.png..N.png` folder, pixels far from every colour of the first and last frame (the key poses) and specks under 12 px go; `--tol 20`–`25` also catches trails in the character's own hues; `--clear-right X` / `--clear-left X` clear past a barrel tip. Pose mode: one `.png`, only the `--box` or side you name is cleared. Writes `<frame>_s.png`. Clip mode misses a flash or streak close to the character's own colours (a frost glow on blue robes): look at its output and clear what is left per frame in pose mode; set `--clear-right X` past the fingertips, or it cuts the hand.

```bash
python scrub.py raw 1 2 3 4 5 --out finish/2-scrub [--tol 40] [--keep-main]
python scrub.py pose.png --box 29,10,47,16 --out finish/2-scrub
```

### despeckle

Gives each pixel unlike all 8 neighbours their median colour and makes opaque pixels with no opaque neighbour transparent; two or more alike pixels (highlights, eye glints) stay. A one-pixel eye or rune looks exactly like a speck, so pass the clean still the frames came from as `--ref` whenever one exists: lone pixels in the still's own lone-pixel colours are kept (`kept_as_detail`). Without a reference, check the per-frame counts in `derivative.json`: dozens of changes on a clean frame mean it is eating detail, so add `--ref`, raise `--tol` or skip it.

```bash
python despeckle.py "frames/*.png" --out finish/3-despeckle [--ref still.png] [--tol 90]
```

### colormatch

Scales each frame's brightness to the standing sprite's, then snaps every pixel to the sprite's own colours. Use when key poses or in-betweens drifted in colour.

```bash
python colormatch.py hero.png "frames/*.png" --out finish/4-colormatch
```

### apply_palette

Snaps every opaque pixel to the nearest colour of a fixed palette (hex list, `.hex`/`.txt`, swatch `.png`, or `auto --colors N`). For PixelLab-side reduction prefer `reduce_colors` (SKILL.md router).

```bash
python apply_palette.py "#1a1c2c,#5d275d,#b13e53" "frames/*.png" --out finish/4-palette
```

### recolor_trail

Finds a swing trail painted in the character's own hue (thin strokes away from the body) and recolours it into an effect ramp (`--to air|fire|arcane|holy|shadow`) or deletes it (`--to none`: where it crosses the body the pixels stay, so no hole, and its thin outline goes with it). `--ref` with the standing sprite separates trail from costume best; `--from-scrub DIR` takes what scrub cleared as the trail. Writes `<frame>_t.png`.

```bash
python recolor_trail.py raw 3 4 5 --hue red --to none --ref hero.png --out finish/2-trail
```

### recolor_groups

A colour variant: colour groups (skin, neutrals, hue families) move to named colours or `#rrggbb` while each pixel keeps its place on the ramp; the still and every frame get the same mapping; skin stays unless named. `--groups` lists the groups and writes nothing.

```bash
python recolor_groups.py hero.png "frames/*.png" --swap red=indigo --out variant
```

### recolor_like

Recolours frames drawn in an old still's colours into a new still's (same pose), keeping the old contrast; reports repeated frames. `--keep-thin REDRAWN_DIR` pastes the recoloured thin parts (blades, staffs) over a redraw.

```bash
python recolor_like.py old/still.png new/still.png "old/attack_*.png" --out new-colours
```

### dir8_finish

For multi-direction shots: clears named boxes, drops detached specks, puts a `vfx_workbench` export at each direction's muzzle (rotated), and mirrors the other side, from one `spec.json` (format in the helper's `--help`). Its `total` (hold frames) and `replace` (copy a frame) keys change frame count or order — use them only when the user asked.

```bash
python dir8_finish.py spec.json --out finish/dirs
```

To fill each direction's `shot`, `muzzle` and `clear`, `find_muzzle.py <frames_dir>` (read-only) guesses them from the generator's own flash and prints a spec line; check it on the frame, and read the muzzle by eye when the flash covers the body or the gun.

## New-pixel helpers

### slash_layer

`extract`: turns what scrub cleared from one frame into a shaded effect-only image (`<frame>_fx.png`). `apply`: lays that effect on a frame of another clip with the same canvas and key poses (`--behind`, `--fade`, `--offset dx,dy`).

```bash
python slash_layer.py extract raw/3.png finish/2-scrub/3_s.png --out fx [--to air]
python slash_layer.py apply clip/3.png fx/3_fx.png --out finish/5-slash [--offset 3,2]
```

### throw_prop

Lifts the weapon already apart from the body in the release pose and flies it across the following frames, `--step dx,dy` per frame, `--turn` quarter turns per frame; it is pasted on empty pixels only. Ground-snap the frames first.

```bash
python throw_prop.py release.png --onto f4.png f5.png f6.png --step 40,-17 [--turn 1] --out finish/5-throw
```

### bake_fx

Composites a `vfx_workbench` export onto the body frames from frame `--from N`, centred on `--at x,y`, or with the effect's own pixel `--anchor x,y` (the projectile's start inside the effect image, not the export's origin field) placed there; `--widen W` adds room on the right. When the effect outlasts the body, the last body frame is held and `held_frames` is reported — say so.

```bash
python bake_fx.py "body/*.png" --fx burst.png --at 250,70 --from 9 [--anchor 3,14] [--widen 320] --out finish/5-fx
```

### blade_trail

Paints a tapered trail along a path through the blade tips for stepped key poses, with an optional dithered afterimage (`--ghost`). A locally painted fallback — offer a `vfx_workbench` trail first.

```bash
python blade_trail.py --frames idle.png draw.png ext.png --path "70,91 124,93 185,75" --spans "x,0:1,0.55:1" --thick "0,8,5" --out finish/5-trail
```
