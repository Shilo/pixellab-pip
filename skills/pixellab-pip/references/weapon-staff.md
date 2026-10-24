# Staff (quarterstaff, bo, short stick, mage's staff) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Left-facing sources are mirrored: facing right, the right hand, right foot and near side face the viewer, and
"forward" is toward the right of the image.

## Contents
- [What every staff pose keeps](#what-every-staff-pose-keeps)
- [Guards, what to draw](#guards-what-to-draw)
- [Moves as animations (key pose A -> key pose B, trail path in screen terms)](#moves-as-animations-key-pose-a---key-pose-b-trail-path-in-screen-terms)
- [Stepped vs interpolated](#stepped-vs-interpolated)
- [Frame rhythm](#frame-rhythm)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every staff pose keeps
- **Two grips, name the one you want.** Fighting staff in the sources is held either *wide* (`hands about a
  shoulder width apart, splitting the staff into thirds`, Hokusai, Allanson-Winn guards, Riboni's horizontal
  hold) or *at one end like a long club* (`both hands close together near the back end of the staff, the long
  part reaching forward`, Riboni's cuts and thrusts, the "new guard"). The generator slides hands to the middle
  unless told; say where each hand is in thirds or ends.
- **Same length, straight, one staff.** A staff is as tall as the hero or taller (~1.1-1.3x body height); say
  `one straight wooden staff, the same length as in the original, both ends visible` in every pose.
- **Both ends visible means canvas width.** A staff held level forward sticks out ~0.8 body height past the
  front hand and ~0.3 behind the back hand. For a ~100x250 hero pad the canvas to at least 2x the sprite width
  before the edit and add `the whole staff fits inside the canvas with a margin`; cut-off tips
  are read as a shorter staff on the next edit.
- **Stance is wide and low.** Every fighting figure stands with feet 1.5-2 shoulder widths apart, knees bent,
  weight over the front foot on hits; the guards are almost square to the viewer with the staff diagonal in front.

## Guards, what to draw
| Guard | Visible description for the prompt | Use |
|---|---|---|
| High diagonal | `staff held diagonally across the body, the top end high above his head toward the upper right, the lower end near his front foot, near right hand at chest height, left hand low by the hip` | idle / on guard |
| Upright | `staff held almost vertical in front of his near shoulder, right hand at face height, left hand at the belt` | block-ready idle, start of a side swing |
| Level forward (end grip) | `both hands together near the back end of the staff at chest height, staff level, pointing forward at the enemy's chest` | thrust wind-up, duel stance |
| Horizontal low | `staff held level across his hips, hands wide apart near both ends, palms down` | ready for spin, start of a sweep |
| Planted | `one end of the staff resting on the ground beside his front foot, staff upright, one hand on top` | idle / taunt (also a mage's rest) |
| One-hand trail (running) | `staff held level at chest height in his near right hand at the middle, far arm flung out behind for balance, running` | dash / approach |
| Behind the back | `staff held level behind his lower back in one hand, the ends sticking out on both sides` | taunt idle, start of a spin |
| Overhead bar (running) | `staff held level above his head in both hands spread wide, mid-stride` | leap-in wind-up, charge |
| Shoulder rest (wind-up) | `staff over the near shoulder, both hands near the lower end beside the right ear, the long end pointing back and up behind him` | overhead smash wind-up |

## Moves as animations (key pose A -> key pose B, trail path in screen terms)
- **Thrust (point):** A = level forward, hands pulled back to the hip, front knee bent -> B = deep lunge, back
  leg straight, `back hand pushing the rear end of the staff past the belly, front hand slid forward, staff level
  at chest height, the forward end far toward the right side of the image`. Hokusai's bo thrust slides the front
  hand; the end-grip thrust keeps both hands together. Effect: `thrust_streak` from the forward tip, no crescent.
- **Overhead strike (head hit):** A = shoulder rest or `staff raised level above his head in both hands` ->
  B = `arms extended forward and down, the forward end at the enemy's head height toward the right, torso leaning
  over the front knee`. Trail: a big arc from behind and above the head, over the top, down in front; only the
  forward tip draws it (`blade_trail.py` on the tip, or `swing_slash`).
- **Side swing (flank / leg hit):** A = upright guard with the staff pulled back past the far hip -> B = `staff
  swung level in front at waist or knee height, the forward end toward the right of the image, hips turned`.
  Trail: a flat ellipse at that height; for a leg sweep keep it low and short.
- **Horizontal swing + spin (around the head):** A = horizontal low (hands wide) -> step through ->
  `both hands together near one end, staff level, swinging around above his head` -> back to level forward.
  Riboni draws it as three stations: level hold, stepping front moulinet, full turn. Use stepped key poses for
  each station; the trail is a full flat ring at head height (`slash_trail` or a closed `blade_trail.py` path).
- **Twirl (moulinet):** the staff spins in front of the body in one or both hands. Do NOT interpolate one A -> B;
  draw 4 stepped key poses at 45-degree turns (diagonal, upright, diagonal the other way, level) and repeat them.
  Trail: short white arcs at BOTH tips only (both ends travel), never a filled disc.
- **Block (staff as a bar):** high block = `staff held level above his head, hands wide apart, catching a
  downward blow on the middle`; side block = `staff upright in front of his near side, hands wide`. The parries in
  Riboni and Allanson-Winn meet the attack between the hands. Snap idle -> block (hold ~200 ms) -> idle, with a
  `spark_burst` where the staffs cross.
- **Disarm (one-hand cut):** A = staff diagonal, `right hand at the middle, left hand low on the rear end` ->
  B = `left hand off, near arm stretched forward at shoulder height, staff held in one hand at the rear end,
  reaching far forward`. A flick: one-frame `swing_slash` on the tip, then the enemy weapon flies off (separate).
- **Choke / throat thrust (short stick):** the army stick is ~half a staff, `held level in both fists, one at
  each end`. Throat thrust = push both fists forward at neck height; choke = `standing behind the enemy, the stick
  across the front of his neck, both fists pulling back toward his own chest`. A grapple: two-figure frames are a
  composite job, not a single-hero edit.

- **Vault -> whirl -> sweep (signature skill, 4 keys):** A = `staff planted in the ground ahead at an angle, both
  hands high on it, body leaning in, back foot pushing off` (a red ground burst at the planted tip) -> `body arched
  over the top of the upright staff, hands on its top end, legs swinging over` (pole vault, NOT a free leap) ->
  airborne, `staff whirled level above his head in both hands` (a flat grey ellipse plus 2-3 ghost staffs at
  different angles = the spin) -> landing, `deep low lunge, staff swung level at waist height out to the right,
  torso twisted`. Trail on the last key: a wide flat ellipse around him at waist height, read as a radial sweep,
  not a downward slam; ground ring under it. The sheet's own note: one flip at most, keep it readable.
- **Acrobatic staff poses (sketch page):** handstand on the planted staff (`body upside down above the upright
  staff, both hands on its top end`), lunging dive with the staff diagonal in one hand, one-hand end twirl (the
  far end blurred into a fan). Good single key poses for flourishes; the inverted ones need a tall canvas and
  should be stepped, never interpolated from standing.

## Stepped vs interpolated
- Interpolate (4 frames, `first_frame_url` + `last_frame_url`) when the hands keep their grip and the staff
  turns less than ~90 degrees: thrust, overhead strike, side swing, block.
- Step (one edited key pose per frame) when the staff swaps ends, passes behind the body, or turns more than
  ~90 degrees: twirl, around-the-head spin, disarm flick, the vault (body goes over the staff). Interpolation there gives two staffs, a vanished staff,
  or a staff that shrinks to a stub at the edge-on frame.

## Frame rhythm
- **Bo attack set (Athrix, 60 px frames, 28 frames):** idle -> 6 twirl frames (staff at a new 45-degree angle
  each frame, tip arcs only) -> 3-frame crouch -> 1 smash frame on the jump with one big filled crescent down the
  front -> 3 airborne frames, staff angled down-forward -> landing -> 4 frames vaulting on the planted staff with
  a forward kick -> the twirl reversed (6 frames) -> idle. The hit is ONE frame; the twirl is even-paced.
- **Staff cast (Movicx wizard, 7 frames per direction):** `staff held upright in the near hand beside the body`
  rises a few pixels until the head is above the hat, the whole staff wrapped in a soft glow for 3 frames, then
  4 frames lowering while the glow fades. For a facing-right cast: A = `staff upright at his near side, head at
  shoulder height` -> B = `staff raised so the crystal head is above his head`; keep the body still and put the
  light in `charge_up` + `magic_orb` at the head, never painted by the animation (it flickers).
- Timing: `key-pose-animation.md`.

## Pitfalls to name in prompts
- Staff length changes between poses -> `the same length as in the original, both ends visible` + wider canvas.
- Staff bends or kinks at the hands -> `one straight rigid wooden pole, no bend`.
- Two staffs, or a second stub behind the body -> `holding only one staff`; step the poses where it swaps ends.
- Hands slide off or merge at the middle -> name each hand's place (`right hand a third from the front end`).
- The staff turns into a spear or gets a blade or crystal -> `plain wooden staff, blunt rounded ends` (fighter)
  or `the same crystal head at the top end` (mage); a mage's raised-arms cast drops the staff unless pose B names it.
- Vault reads as a plain jump -> name `staff planted in the ground, his weight on it`, and put the tip burst on
  the planted frame; the staff must stay touching the ground until the body is over it.
- Glow painted into the frames flickers -> keep the staff unlit in the animation, add the VFX after.
