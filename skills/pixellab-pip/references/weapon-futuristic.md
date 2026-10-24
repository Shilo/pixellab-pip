# Futuristic weapons (arm cannons, energy rifles, energy blades, cyborg and robot limbs) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Read this for sci-fi shooters and energy-blade fighters: arm-cannon aims, run-and-shoot, rifle recoil, glowing
blades and their trails, and mechanical arms that turn into weapons. Facing right throughout:
muzzle and blade tip toward the right of the image. Basic shot/recoil, generator flashes and gear-mounted launchers
are in `weapon-firearms.md`; smear shapes and hit sparks are in
`weapon-effects.md`. This page adds only what is new for sci-fi gear.

## Contents
- [What every futuristic pose keeps](#what-every-futuristic-pose-keeps)
- [Glow and energy colour, what to say](#glow-and-energy-colour-what-to-say)
- [Arm cannons and forearm guns](#arm-cannons-and-forearm-guns)
- [Energy rifles and pistols: aim, run-and-shoot, recoil](#energy-rifles-and-pistols-aim-run-and-shoot-recoil)
- [Energy blades vs steel blades](#energy-blades-vs-steel-blades)
- [Cyborg and robot limbs](#cyborg-and-robot-limbs)
- [Frame rhythm](#frame-rhythm)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every futuristic pose keeps
- **Name the weapon arm by its look in every pose** (`characters.md`: `his chrome right forearm ends in a thick teal
  cannon`). A mismatched arm is the first thing in-betweens swap (as on `weapon-whip.md`).
- **The gun or cannon is rigid and keeps its size.** `same cannon, same length and thickness as in the original`.
  Big sci-fi guns grow or shrink more than swords because they have no clear silhouette edge; check at 3x.
- **The aim line is level unless you say otherwise.** Good shooting frames hold the barrel at chest or
  shoulder height, dead level toward the right; diagonal aims are separate named poses (`barrel angled up toward
  the upper right, 45 degrees`), never something the clip drifts into.
- **Canvas:** an arm cannon or rifle sticks out ~0.5-0.7 x body height in front of the chest; pad the sprite at
  x≈40 on the style's forward canvas (192x200 for the sci-fi example; wider when the gun is long) so the muzzle plus a beam start fits, then widen for the beam itself (`bake_fx --widen`).

## Glow and energy colour, what to say
- **Name the energy colour and the core in every prompt that has light in it:** `a cyan energy bolt with a white
  core`, `a magenta plasma blade, white-hot centre line, thin pink glow edge`. Without it the generator paints an
  orange-yellow gunpowder flash with smoke.
- **Also say what is NOT there:** `no smoke, no fire, no orange muzzle flash, no shell casings`.
- **Light the muzzle, not the body.** A shot often tints the whole figure orange;
  in pixel art that reads as the hero catching fire. Say `only the muzzle glows, the body keeps its normal colours`,
  and bake the flash on afterwards instead of letting the key pose carry it.
- **Glow parts on the gear stay one fixed colour:** visor, chest light, vents and cannon rings. `the visor and the
  cannon rings glow the same teal in every pose`. Pick one accent hue per character and reuse it for shots and trails.
- **Pixel glow = 2-3 flat tones, no blur:** white core, saturated rim, at most a darker outer edge. `flat pixel glow,
  hard edges, no soft blur`. Same rule as the flat outlined clips in `weapon-effects.md`.

## Arm cannons and forearm guns
| Pose | Visible description for the prompt | Use |
|---|---|---|
| Ready | `right forearm raised level at chest height, the cannon pointing straight toward the right, elbow bent and tucked at his side, left fist at his hip` | idle, shoot start |
| Braced shot | `feet shoulder width, left foot forward, knees soft, cannon arm locked straight out level at chest height toward the right, left hand gripping the cannon arm just behind the barrel` | heavy shot, charge |
| Run aim | `running stride, legs mid-cycle, cannon arm held level and steady at chest height toward the right` | run-and-shoot |
| Jump aim | `in the air, knees tucked, cannon arm level toward the right` | jump-shoot |
| Up / down aim | `cannon angled up toward the upper right` / `angled down toward the lower right`, body leaning the other way | 8-way aim |
- **The cannon is the forearm.** `no hand on the right arm, the forearm ends in the cannon barrel`; otherwise the
  generator draws a fist holding a gun.
- **Recoil is tiny on a body-mounted cannon:** the arm kicks back ~2-3 px and the shoulder dips, legs stay
  planted. Use the optional 2 px arm-band lift from `weapon-firearms.md`, not a full recoil pose.
- **Charge shot:** A = braced, B = `cannon arm pulled back to the shoulder, glowing cyan ball forming at the
  muzzle` (scrub the generator ball, paint it in `vfx_workbench` with `ring` + growing `dot`) -> release B' =
  `arm thrust forward, torso rocked back onto the rear foot`. Hold the charge ~300 ms, fire on the first motion frame.

## Energy rifles and pistols: aim, run-and-shoot, recoil
- **Run-and-shoot is legs plus a steady upper body.** Build it from two halves split at the belt: the run legs
  cycle while the aiming torso is the same few frames, sunk 1 px on the low steps. In prompts: `running, upper body
  upright and steady, rifle held level at shoulder height toward the right, only the legs move`. When a clip bobs the
  gun, composite: keep one checked upper half, paste it on each leg frame at the same cut row, +1 px down on the
  frames where the feet are passing.
- **Lean-in shot (one-handed pistol):** `torso leaning forward, right arm stretched straight toward the right at
  shoulder height, pistol level, left arm swung back for balance, back leg trailing`. Reads fast; good for a dash shot.
- **Rifle recoil frame:** aim = `rifle stock against the right shoulder, left hand under the barrel, cheek on the
  stock, barrel level toward the right`; recoil = `shoulder pushed back 2-3 px, barrel kicked up slightly, head
  stays level`. Two frames, then back to aim. Auto-fire loops these two, the flash alternating on and off.
- **Diagonal aim while running or crouched** is its own key pose (`crouched low, rifle angled up toward the upper
  right`); do not let `animate_image` rotate the gun between aims, step it.
- **Bolts:** small pill or arrow shapes, 2-3 tones of the accent hue, ~1/6 body height long, flown in
  `vfx_workbench` (a `streak` with a white head). The hit flash is a white star burst, not a fireball.

## Energy blades vs steel blades
- **The blade is a light, not metal.** `a thin straight beam of red light from a short metal hilt, white core line,
  thin red glow edge, no metal shine, no edge bevel`. Keep it the same length in every pose (`blade as long as
  his arm`); beam blades shrink to a stick in fast frames.
- **Twin blades:** one hilt in each fist, both blades named with their direction in every pose (`right blade
  pointing up toward the upper right, left blade pointing down toward the lower left`). An idle crosses them
  low in an X in front of the hips; say that, or one blade vanishes.
- **The trail is the blade's colour, not white air.** Unlike the steel smears on `weapon-effects.md`, an energy
  slash trail is a solid saturated crescent of the blade hue, brightest at the leading end, its tail breaking into
  lighter dithered streaks. Make it with `slash_layer.py` or a workbench `arc` in the blade colour; keep white only
  as a thin inner line. Same grow-full-erode rhythm as steel.
- **Energy-blade moves (A -> B, trail):**
  - Horizontal spin cut: A = `blades drawn back past the left hip, body coiled` -> B = `body turned through, both
    arms swept out to the right at waist height`; trail = a flat red ellipse band around the waist.
  - Rising cut: A = `blade low behind toward the lower left` -> B = `blade swept up to the upper right above the
    head`; trail a crescent from lower left to upper right in front of the body.
  - Lunge stab: B = `deep lunge, blade arm straight toward the right, blade level`; trail a straight `thrust_streak`
    of the blade colour, no crescent.
- **Elemental energy edge (crackling blue variant):** big pale-blue arc with jagged lightning ticks on its rim for the
  overhead cut; a straight icy spear of light for the thrust; spirals wrapping the whole body for a whirl. Ask
  `vfx_workbench` for `arc` + small `rays`/`streak` ticks along the rim, never the key pose: the generator paints
  the swirl over the face.

## Cyborg and robot limbs
- **Mechanical parts change shape in in-betweens** (plates merge, joints vanish). Name the parts: `round silver
  shoulder joint, segmented black forearm, three-finger metal hand`, and the visor (`one horizontal red visor slit`).
- **Robot arm blade:** the robot's melee shows a short glowing blade extending straight out of the forearm. Swing:
  A = `forearm blade pointing down toward the lower left, arm low behind the hip, knees bent` -> mid = `blade
  level toward the right at chest height` -> B = `arm raised, blade pointing up toward the upper right above the head`.
  Paint the mid as its own pose (a slash needs three poses), then the arm folds back into the gun pose.
- **Oversized cyborg blade (taller than the body):** held one-handed at the hilt end, the far end resting
  on the shoulder in idle (`huge segmented blade resting on his right shoulder, tip up toward the upper left`); attack
  B = `blade swung down and level, pointing far toward the right at hip height, body leaning forward over a bent front
  leg`. It does not fit 256 px swinging: keep it at body height and say `blade fully inside the image`.
- **Robots move stiffly:** fewer in-betweens, hard stops, no follow-through wobble. `stiff mechanical movement,
  no cloth, no bending in the arm plates`.

## Frame rhythm
- Shot: aim hold 120 ms -> recoil 1 frame 60-80 ms (flash on this frame only) -> recover 2 frames. Auto-fire
  loop: 2 frames x 60 ms.
- Run-and-shoot: the run's own timing (6-8 frames); the flash lands on every second or fourth leg frame.
- Arm-cannon idle: a slow 2 px bob of the whole body, the cannon rides with the torso, ~150 ms a frame.
- Energy slash: wind-up hold 160 ms, the full crescent frame 120-140 ms, 2-3 fade frames at 60 ms.

## Pitfalls to name in prompts
- Orange gunpowder flash, smoke or a fireball -> name the energy colour + `no smoke, no fire`.
- The whole body glows the flash colour -> `only the muzzle glows`; bake the flash on afterwards.
- A hand appears holding the arm cannon -> `the forearm ends in the cannon, no hand`.
- The gun bobs or tilts while running -> `upper body steady`; composite a fixed upper half if it persists.
- Energy blade turns into grey steel or a stick -> `beam of light, white core, same length as in the original`.
- One twin blade drops out -> name both blades and their directions in every pose.
- Energy trail painted white like a steel smear -> `the trail is the same red as the blade`.
- Robot plates melt together -> name each joint and plate; step stiff moves instead of interpolating.
