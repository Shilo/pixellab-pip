# Weapon effects (smears, slash arcs, trails, hit flashes, bursts, shockwaves, arrow trails)

The sources give frame counts, not times: the ms below are play timing for ~12 fps clips. How to make them: a crescent
harvested from a 6-frame swing with the `slash_layer.py` finishing script (see `key-pose-animation.md`), a trail drawn
through the blade tips with `blade_trail.py`, or a painted clip in `vfx_workbench`
([vfx-workbench.md](vfx-workbench.md)). This page says which, per effect.

## Contents
- [What every weapon effect keeps](#what-every-weapon-effect-keeps)
- [Smear / slash arc (sword, axe, katana)](#smear--slash-arc-sword-axe-katana)
- [Thrust smear (spear, rapier, dagger stab)](#thrust-smear-spear-rapier-dagger-stab)
- [Blunt smash smear (hammer, mace, club)](#blunt-smash-smear-hammer-mace-club)
- [Trail / afterimage (fast cuts, flash steps, combos)](#trail--afterimage-fast-cuts-flash-steps-combos)
- [Hit flash / spark](#hit-flash--spark)
- [Blood burst](#blood-burst)
- [Impact burst + shockwave ring](#impact-burst--shockwave-ring)
- [Ground impact (hammer slam, landing, earth strike)](#ground-impact-hammer-slam-landing-earth-strike)
- [Arrow trail](#arrow-trail)
- [Cartoon burst](#cartoon-burst)
- [Frame rhythms (counts from the sources, ms ours)](#frame-rhythms-counts-from-the-sources-ms-ours)
- [8-direction smears (top-down)](#8-direction-smears-top-down)
- [Pitfalls](#pitfalls)

## What every weapon effect keeps
- **The smear replaces the blade for one frame, it does not decorate it.** In all three character sheets the
  biggest smear frame has the weapon drawn short or not at all; the arc *is* the weapon on that frame. The next
  frames show the real blade again and the smear shrinks behind it.
- **Grow from the tip side, die from the tail side.** Every arc (pixel and painted) is born at the leading edge,
  is full for one frame, then erodes from where the swing started toward where it ended. The last thing left is a
  thin sliver at the end of the path.
- **Thickest where the blade moves fastest.** Crescents are fat in the middle of the swing or at the leading end
  and taper to a point at both ends. Never a constant-width band (reads as a pipe or a ring).
- **Flat, light, few tones.** The pixel sources use 1 colour (white or pale cyan) for the smear, at most 2-3
  (bright rim + white core + dithered inner edge). A pale `air` ramp with a dark outline works
  (`slash_layer.py --to air`); keep it in the project style's family or the character's own colours, never a new saturated hue.
- **Effects sit outside the body's silhouette.** The smear wraps around the side the weapon passes; it goes behind
  the body (`--behind`) where the blade passes behind, in front only on the far side of the arc.

## Smear / slash arc (sword, axe, katana)
- **Looks like:** a crescent, fat in the middle, both ends pointed, its outer edge following the blade tip's path
  and its inner edge cut along the hand's path (so the hollow is the arm's reach). Size: on the top-down dummy the
  sword smear runs ~1.3x the character's height and ~0.5x its height thick; on the side-view sword combo the big
  crescent is about the character's full height and wraps half the body. The painted trail sheet's full circle
  swing is a closed C, ~1.5x the body.
- **Frames:** top-down sword: 1 anticipation, then smear 4 frames - full crescent -> half thickness -> hairline arc
  -> one thin line on the blade - then recover. The pixel slash arc: 9 frames - a tiny sliver, 2 frames growing
  along the path with a fat head, 1 frame full and pure white (the flash), 1 frame the same shape in the pale grey
  ramp, then 3 frames where the body splits into 3-4 parallel thin strands that shorten toward the end, last a
  single line. Dithered crescents: 3 frames per size - full, inner half dithered away, only the outer rim.
- **Colour:** white flash frame -> pale blue-grey; dithered version: saturated dark outer rim, white body, the inner
  edge broken into scattered single pixels (fading by dither, not by opacity).
- **Make it:** the key-pose route, `slash_layer.py extract` the crescent from the 6-frame swing's mid-cleave frame,
  `apply --behind` full on that frame, `--fade 0.3` on the next, the small follow-through arc on the one after. In
  `vfx_workbench` (a strike over the victim or a hero-side clip): `arc` with `profile:"slash"`, radius ~30 at 112 px,
  sweep 150-200, thickness 6-7, `life [0, 0.4]` so it grows then erodes; a strand phase = 2-3 thin `arc`s
  (thickness 1-2) at radius ±3 with life [0.25, 0.5]. `mirror:"x"` for left-facing.
- **Timing:** grow 1-2 frames x 60 ms, full 1 frame (the hit, 140 ms), erode 2-3 frames x 60 ms. Total 4-6 frames.

## Thrust smear (spear, rapier, dagger stab)
- **Looks like:** a long narrow wedge along the shaft line, point at the weapon tip, widest a little behind the
  tip, tapering to a hair behind the hand. Top-down spear: ~1.2x the body length on the full frame, ~3-4 px wide at
  sprite scale. Not a crescent: any curve reads as a slash.
- **Frames:** full wedge (tip at full reach) -> wedge half as long, pulled toward the tip -> 2-3 px tick at the tip
  -> gone; the spear slides back over 2 more frames. Painted version (trail sheet row 4): a small line, then a
  feathered spearhead flare 3 frames, then 2 frames of sparks drifting off the tip.
- **Make it:** `blade_trail.py` with a 2-point straight `--path` from the hand to the tip, `--spans` 0:1 -> 0.5:1 ->
  0.85:1, thick 5 -> 3 -> 2. Workbench: `arc` with `points` + `corners:"smooth"`, or the `thrust_streak` part
  (size ~2 at hero scale), plus 4-6 `streak` particles at the tip from life 0.5.
- **Timing:** 1 frame full on the hit, 2 frames shrink at 60 ms. 3 frames total.

## Blunt smash smear (hammer, mace, club)
- **Looks like:** not a filled crescent. A hollow arc: two thin lines (the head's path and the haft's path) closed
  at the head end, or one bold bent line, ending at the impact point. The head itself is drawn at the end of the
  smear, on the ground. Sized like the sword smear but narrower.
- **Frames (top-down hammer):** anticipation (head high) -> smear frame with the head already down -> **rebound**: the
  head lifts a few pixels while a short tick of smear remains -> follow-through (head flat on the ground, 2 frames) ->
  recover. Impact dust: 2-3 small grey puffs and 2-4 single-pixel debris dots either side of the head on the smear
  and rebound frames, then the dots drift outward.
- **Make it:** `blade_trail.py` with the head as the path end, `--thick 3` (a line, not a crescent), no `--dither`;
  impact = workbench `puffs` (radius 8-10, count 3, low throw) + `chunk` particles (count 6, floor, bounce 0.3).
  If the 6-frame swing drew no crescent, skip `slash_layer` (blunt weapons get a line smear, not a crescent).
- **Timing:** smear 1 frame (hit, 140 ms), rebound 1 frame 60 ms, follow-through hold 2 frames 120 ms.

## Trail / afterimage (fast cuts, flash steps, combos)
- **Looks like:** the draw-and-double-slash and two-cut combo both alternate **one big smear frame, then the bare
  blade drawn as a straight line** for 1-2 frames, then the next smear. The double slash's smears are jagged stepped
  wedges (one long horizontal, then a thinner one going the other way), pale cyan, no outline, ~1 sword length ahead
  of the hand. The two-cut combo's crescents are solid flat white. A second cut's smear starts where the first ended.
- **Painted variant (trail sheet rows 1-3):** a crescent that rotates as it moves (full spin: 6 frames, brightest on
  frames 3-5), a half arc that grows from its head and loses its tail, and a soft smoky arc that loses its core
  first. Row 5: a diagonal slit that widens into an eye shape with a dark core and closes again (a slash through
  the air / a cut in space, 6 frames).
- **Make it:** stepped key poses + `blade_trail.py` (`--spans` per frame, `--ghost` for the 50% dithered stance left
  behind in a flash step). Rotating spin: workbench `arc` with sweep 300+ animated over its life, or a `ribbon` on
  a circular path. The slit: a `shape` lens with a dark core, width keyed 0 -> max -> 0.
- **Timing:** smear 1 frame each, blade-line frames 60 ms each, between cuts no hold. A 2-cut combo is ~10-13
  frames total (draw 2-3, cut A 1 + 2, cut B 1 + 2, settle/sheathe 3-5).

## Hit flash / spark
- **Looks like (spark hit, 16 frames):** 2 empty frames (the delay to contact) -> a thin white ring alone -> ring +
  a small yellow core + one long thin diagonal streak through it along the blow's line -> 3 frames the ring grows ~1.3x
  and fades while a jagged yellow burst grows **one-sidedly, away from the attacker** -> ring gone -> 8 frames the
  shards shrink and scatter into specks. **Ray impact (32 frames):** a long faint build (a grey wisp, 7 frames) ->
  glowing ball -> 4-6 rays in a cross grow to ~3x the ball -> rays retract, the core goes grey -> 12+ frames of
  grey smoke and specks.
- **Make it:** workbench strike: `ring` (radius 6 -> 10, thin, life [0, 0.3]) + `rays` (count 4-6, length 8 -> 24,
  life [0.05, 0.3]) + `streak` particles in a cone pointing away from the attacker (count 10-14, life [0.15, 1.0]) +
  `dot` embers to finish. Or the `spark_burst` / `hit_star` parts as a start. For a block/parry: the same, half
  size, at the contact point.
- **Timing:** flash peak 1-2 frames (the hit frame), scatter 4-6 frames at 60-80 ms. Drop the source's long tail.

## Blood burst
- **Looks like (16 frames):** two short dark diagonal blade cuts close in from outside (2 frames) -> a white star
  flash with a red glow at the cross (1 frame) -> the X of two long thin cuts at full size + a red splash (2 frames)
  -> the flash fades, the X retracts, the splash becomes a ragged ring with droplets thrown outward (2 frames) -> the
  ring and droplets hang and erode for ~9 frames. Cut lines ~2x the splash size.
- **Make it:** workbench strike, crimson ramp: two thin `arc`s (`points`, straight) crossing, life [0, 0.35]; a small
  `rays` or ring flash at the cross, life [0.1, 0.3]; `puffs` burst (radius 14, thin, lump high) for the splash,
  life [0.25, 1.0]; `droplet` particles (gravity 70-110, count 10-14, outline). Gore setting off -> swap the ramp for
  the air or spark ramp and keep the shapes.
- **Timing:** cuts 2 x 60 ms, flash 1 x 140 ms, splash 2 x 80 ms, hang 4-6 x 80 ms (not 9: it slows the fight).

## Impact burst + shockwave ring
- **Burst (~40 frames, pixel):** a speck grows into a jagged flame crescent on one side, wraps into a full ring of
  shards, then shifts colour (yellow -> pink -> violet) as it breaks into slivers. Long and decorative; take the
  shape, not the length.
- **Ring (31 frames, pixel):** a filled white dot grows (5 frames) -> a thick donut with a pinhole -> the hole opens
  while the outer radius grows ~5x and the line thins to 1 px -> 2 frames flicker yellow mid-way -> the last frame is
  a broken dotted circle. Constant colour; it fades by **thinning**, not by opacity.
- **Make it:** `ring` (radius 3 -> 30, width keyed 6 -> 1, life [0.1, 0.7]); for side-view games `squash 0.35` so it
  lies on the floor plane, or a ring of puffs (`closed:false` curve, `fill:"cartoon"`). Burst = `rays`
  + `streak` particles, the ramp walking warm -> cool through the life.
- **Timing:** ring 5-7 frames at 60 ms, hidden behind the burst for the first 1-2.

## Ground impact (hammer slam, landing, earth strike)
- **Looks like (5 rows x 5):** a cross flash with a faint ring (row 1); a 4-point star that sprouts a cracked stone
  ring which expands to ~3x (row 2); radial spikes that collapse into rubble around a dark centre (row 3); rocks
  thrown outward that **grow** as they fly (toward the camera, row 4); a ring of pebbles and dust balls that widens
  (row 5). Brown/earth ramp, lit from above, dark undersides.
- **Make it:** eruption-style ground pieces: ground-plane `ring` (keep the width low - it balloons), `chunk`
  particles (floor 30, bounce 0.3, size up to 8), dust `puffs` low and wide (rise 0.2), optional `rays` flash at
  life [0, 0.2]; or `crater_dust` / `debris_burst` parts as a start. Use a stone/earth ramp.
- **Timing:** flash 1 frame on the hit, ring + rocks 3-4 frames at 60-80 ms, dust settle 2-3 frames at 100 ms.

## Arrow trail
- **Looks like (30 frames):** the arrowhead (a chevron) stays still in the frame while 2-3 ghost copies of it trail
  behind at ~0.5 head length spacing; over the loop the copies stretch farther back and fade, the last frames leave
  one dim ghost 1.5 head lengths behind. The trail is copies of the head, not a line.
- **Make it:** a looping 48x16 comet tail on a pivot at the shot's centre, or workbench:
  a `glow` head + `ribbon` trail on a straight `paths` line; for the copy look, the head `shape` repeated with life
  offsets. The projectile's hit is a separate strike (see "Projectile skills" in `key-pose-animation.md`).
- **Timing:** loop it in flight (4-6 frames, 60-80 ms); don't play all 30.

## Cartoon burst
- **Looks like (4 sparks, 4-8 frames each):** flat white fill with a thick black outline, no gradient: an 8-point
  star -> a ring of small circles around a small ring -> the same circles turned into scruffy clouds -> scattered
  clouds; a vertical slit -> a line -> a speck shower + a star with a speed streak; shards flying up in pairs; motion
  lines (CCC) + a crescent + a dust cloud.
- **Make it:** keep it outlined and flat: `rays` star (or `sparkle` particles) at life [0, 0.2],
  then `puffs` with `fill:"cartoon"`, `tones` 3. Good for comic or child-friendly styles; next to a painted, darker
  set it reads as another game - keep it per style.
- **Timing:** 1 frame each, 80-100 ms, no hold except the star (2 frames).

## Frame rhythms (counts from the sources, ms ours)
| Effect | Frames in source | Game frames | Hold | Fade |
|---|---|---|---|---|
| Sword smear (top-down) | 4 smear + 1 antic + 1 recover | 4 | full frame on the hit 140 ms | erode 3 x 60 ms |
| Pixel slash arc | 9 | 5-6 | flash frame 1 | strands 2-3 x 60 ms |
| Thrust smear | 3 + slide back | 3 | tip frame 140 ms | 2 x 60 ms |
| Hammer smear + rebound | smear 1, rebound 1, follow 2 | 4 | follow-through 2 x 60 ms | dust drifts 2 frames |
| Double slash combo | 16 | 11-13 | none between cuts | sheathe 3-5 x 80 ms |
| Spark hit | 16 (2 empty) | 6-8 | peak 1-2 | scatter 4-6 x 70 ms |
| Ray impact | 32 | 8-10 | rays at max 2 | smoke 4 x 80 ms |
| Blood burst | 16 | 10-12 | flash 1 x 140 ms | hang 4-6 x 80 ms |
| Shockwave ring | 31 | 6-7 | none | thins out, 60 ms each |
| Ground impact | 5 per row | 7-9 | flash 1 | dust 2-3 x 100 ms |
| Arrow trail | 30 | 4-6 loop | n/a | n/a |
| Cartoon spark | 4-8 | 4-6 | star 2 | 1 frame each |
Rule seen everywhere: **appear in 1-2 frames, peak 1 frame, take 2-4x as long to disappear.** The sources' long
tails (9-20 fade frames) are for showcase sheets; a fight cuts them to 3-6.

## 8-direction smears (top-down)
- The top-down sheets keep the **same crescent shape and size** in all 8 directions, rotated, always on the facing
  side and wrapping toward the off hand. On north-facing frames the smear sits mostly beyond the head (the body
  overlaps its root); on south it hangs below the feet with the root over the body.
- Make one crescent (E), rotate it for SE/NE/S/N in 45 degree steps, mirror for the west side, like
  `dir8_finish.py` does for flashes. Rotating a pixel crescent by 45 degrees breaks its edges: snap the rotated
  result back to the ramp (or rebuild the diagonal in the workbench with `start` angles ±45) and check at 3x.
- Thrust smears just rotate (a straight wedge survives rotation). Hammer smears keep the head end on the ground
  point in every direction; for north the head lands above the body and the smear is mostly hidden by it.
- Top-down cuts the smear to 4 frames in every direction; keep the frame count equal across all 8.

## Pitfalls
- **A constant-width arc reads as a ring or a pipe** -> taper both ends, fat at the leading third.
- **Smear plus full blade on the same frame** reads as two weapons -> the smear frame uses the generator's smeared
  blade or the scrubbed body; the bare blade comes back on the next frame.
- **Fading by opacity** turns pixel arcs into muddy half-tones -> fade by thinning, splitting into strands, or
  dither (`--fade`), as every pixel source does.
- **Long showcase tails** (the 32-frame ray impact, the 40-frame burst) make the fight drag -> 3-6 fade frames.
- **Symmetric hit sparks** look like explosions -> throw the shards away from the attacker (a cone, not a circle).
- **A slash crescent on a blunt weapon** reads as a blade -> hollow line smear + dust at the head instead.
- **Additive glow on painted, outlined clips** washes them out: the soft-glow sources here are a
  shape reference, rebuild them flat with an outline.
- **Effect hue far from the attacker's** (the saturated red and green crescents) reads as elemental magic ->
  the `air` ramp or the attacker's own family for plain weapons.
