# Anime weapons (giant swords, scythes, kunai, chibi attacks, stylish guns) as visible poses

Read this for anime-style weapon moves: oversized blades and their weight, scythe grips and reaping arcs, kunai throws,
chibi bodies in motion, exaggerated smear frames, and stylish gun poses.
Basic katana and sword cuts: `weapon-katana.md`, `weapon-sword.md`; trail shapes: `weapon-effects.md`; the thrown-prop
recipe, Shots and the pistol draw: `key-pose-animation.md`. Facing right throughout: right hand, right foot and the
near side face the viewer.

## Contents
- [What every anime weapon pose keeps](#what-every-anime-weapon-pose-keeps)
- [Giant sword: carry, weight, swing](#giant-sword-carry-weight-swing)
- [Scythe: grips, carry, reaping arcs](#scythe-grips-carry-reaping-arcs)
- [Kunai: grip and throw](#kunai-grip-and-throw)
- [Chibi bodies in motion](#chibi-bodies-in-motion)
- [Anime exaggeration and smear frames](#anime-exaggeration-and-smear-frames)
- [Stylish gun poses](#stylish-gun-poses)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every anime weapon pose keeps
- **Silhouette first.** Every key pose should read as a black shape: weapon clear of the body, limbs spread, no
  blade crossing the face. Push poses further than a realistic page would: deeper crouch, longer lunge.
- **Hair and cloth lag the body.** On the hit frame hair, scarf and coat tails stream back toward the left of the
  image; on the settle they swing past and fall. Say `hair and coat tails streaming back behind him`.
- **Free hand is posed, never hanging.** Open palm pushed forward, fist at the hip, or arm flung out back for
  balance: `free left hand open, palm forward toward the right of the image`.

## Giant sword: carry, weight, swing
A giant sword is as long as the figure (or longer) with a blade as wide as the torso. Every pose shows its weight:
the body leans away from the blade or braces under it. Pad the canvas: a blade-length in front and above.
| Pose | Visible description for the prompt | Use |
|---|---|---|
| Shoulder carry | `huge sword resting flat on his near right shoulder, blade pointing back and up behind him toward the upper left, right hand on the hilt in front of his chest` | idle, walk, taunt |
| Back-of-neck carry | `huge sword laid across the back of his shoulders, both wrists draped over it` | cocky idle, victory |
| Low drag | `one hand on the hilt at his hip, huge blade trailing behind him, tip scraping the ground toward the left of the image` | run, dash start |
| Wall block | `crouched behind the huge sword, blade upright in front of him like a wall, both hands on the hilt, far shoulder pressed to the flat` | guard |
| Planted lean | `huge sword stabbed point-down into the ground beside him, one hand resting on the pommel` | idle, out of breath, intro |
| Overhead bar | `both arms straight up, huge blade level above his head pointing back toward the left of the image, knees bent under it` | slam wind-up |
| Low two-hand | `wide stance, both hands at his hip, huge blade angled down in front, tip near the ground ahead` | ready, rising-cut start |
- **Overhead slam:** overhead bar (`leaning back, weight on the back foot`) -> `blade crashed down, flat of the tip
  on the ground one body length ahead, torso bent almost level over the front knee, back leg straight`. The body
  follows the blade down; it doesn't stay upright. Ground dust/crack at the tip.
- **Horizontal cleave:** shoulder carry with `torso twisted away, shoulders turned toward the left of the image` ->
  `arms swung through, blade level at waist height pointing toward the left of the image, torso turned fully past
  the front, front foot pivoted`. Trail: a wide flat ellipse, fattest in front of the body.
- **Rising launcher:** low drag -> `huge blade swept up overhead, both arms high toward the upper right, up on the
  toes of the front foot`. Trail: a tall crescent from the ground behind up to above the head.
- **Momentum:** after a big swing the body keeps turning: a recovery frame with `back turned toward the viewer,
  blade dragged around behind` sells the weight better than a snap back to idle.

## Scythe: grips, carry, reaping arcs
The scythe is taller than the figure; the blade sits at the top of the shaft at a right angle, curving down, sharp
edge on the INNER curve (facing back toward the shaft and the wielder). It cuts by pulling, not pushing.
- **Two-hand grip:** hands far apart, about a forearm and a half: `right hand high on the shaft just below the
  blade, left hand low near the end of the shaft`. Name both hands; the generator slides them together like a staff.
- **Shoulder carry:** `middle of the shaft resting on his near right shoulder, blade up behind his head hooking
  down toward the left of the image, right hand holding the lower shaft in front of his hip`.
- **Planted:** `scythe standing upright beside him, butt on the ground, one hand high on the shaft, blade curving
  out over his head`.
- **Reaping sweep (signature):** A = `torso twisted away, scythe held low behind him, blade near the ground toward
  the left of the image` -> B = `torso swivelled round to the front, shaft swung level across his waist, blade
  hooked forward around in front of him at knee height, inner edge facing back toward him`. Trail: a low flat ring
  around the hips. A follow-up key pulls the blade back toward the body (the cut).
- **Overhead chop:** `both arms raised, shaft upright, blade high above his head pointing forward` -> `shaft driven
  down diagonally, blade tip hooked into the ground ahead, low crouch`. For a vertical swing the low hand pulls in
  toward the belly while the high hand pushes out.
- **Spin:** step every quarter turn as its own key pose (shaft in front, behind the back, overhead); the blade
  passes behind the body and the interpolator loses it. Trail: a full ring, back half drawn behind the body.
- **One-hand flourish:** `scythe held at the end of the shaft in his right hand, arm straight out, blade sweeping
  wide` - generate it alone, never as an in-between.

## Kunai: grip and throw
- **Grip:** `kunai held reverse grip, ring pommel at the top of his fist, short leaf blade pointing down below his
  little finger`; for a volley, `three kunai fanned out between the fingers of his right hand`.
- **Throw, about 10 frames:** cock (`right hand pulled back past his far hip, kunai pointing down`, body coiled)
  -> 1 frame neutral -> forward snap (`right arm whipped straight out toward the right of the image at chest height,
  hand flat, fingers pointing at the target`) = release -> 5-6 frames hand empty, arm still out, slowly returning.
  The follow-through is longer than the wind-up; the release is one frame.
- **Sidearm flick:** from `right hand at his far shoulder, forearm across his chest` -> `arm swept straight across
  to the right, wrist flicked`. Faster read than an overhand throw; good for multiple kunai.
- Fly the kunai with the thrown-prop recipe in `key-pose-animation.md`; it travels point-first, no tumble (skip `--turn`).

## Chibi bodies in motion
Chibi = head about as big as the rest of the body, short stubby arms and legs, weapon often head-sized or bigger.
- **The head barely moves.** In attacks the head stays put or bobs 1-2 px; the arms and the weapon do all the
  travel. Say `head stays in the same place, only the arms and sword move`.
- **Short limbs can't reach:** the weapon carries the reach. Swing from the shoulder with the arm near straight;
  `stubby arm extended, the sword reaching far beyond it`.
- **Few poses, big arc:** a chibi swing is 4-5 key poses: low ready -> `sword raised upright beside his head` ->
  smear frame -> `blade level low in front` -> settle. Feet stay planted; a small hop or squash is enough.
- Keep `chibi proportions, same short arms and legs as the original` in every pose; action poses grow the limbs.

## Anime exaggeration and smear frames
- **Crescent that lingers:** a pale crescent appears on the swing frame and holds 3-5 frames, fading and thinning
  from the tail, while the blade sits at the end pose. Cheaper and punchier than more in-betweens.
- **Fan of lines:** a fast cut drawn as 4-6 thin parallel arcs fanning out from the hilt, like a paper fan; good
  at small sizes where a filled crescent blobs.
- **Energy crescent:** a coloured crescent with a dark core and bright rim (`vfx_workbench` `swing_slash`
  recoloured); can tear into horizontal streaks as it fades. Name the colour; never let it cover the face.
- **Afterimage finisher:** a faded copy of an earlier pose trailing behind a dash, the solid figure in front
  (`blade_trail --ghost` in `finishing.md` draws one at 50% dither; run it once per earlier pose for 2-3).
- **Smear frames are painted, not interpolated:** ask the generator for the end pose, then add the smear locally
  (`weapon-effects.md`). `animate_image` turns a requested smear into mush.
- Frame budget that reads anime: wind-up 1-2 (held), swing 0-1, hit + fading trail 3-5, recovery 2-3.

## Stylish gun poses
Aim/recoil keys are in Shots and the pistol draw (`key-pose-animation.md`); these are the poses between and around them.
| Pose | Visible description for the prompt | Use |
|---|---|---|
| Muzzle-up ready | `pistol held up beside his cheek in both hands, muzzle pointing at the sky, elbows tucked` | idle, before a shot, reload end |
| Two-hand aim | `both arms straight out toward the right, hands cupped around the pistol, head dipped to the sights` | shot |
| Side-on one hand | `body side-on, right arm straight out with the pistol, left arm thrown back for balance` | cool shot, walk-and-fire |
| Kneel aim | the kneeling stance in `weapon-firearms.md`, with the stylish two-hand aim toward the right | low cover shot |
| Slide / dive | `body low and stretched toward the right, one hand on the ground, pistol aimed forward in the other` | dodge-shot |
| Prone | `lying flat on the belly, both arms stretched forward, pistol level toward the right` | sniper, cover |
| Shotgun rest | `shotgun propped on his near shoulder, muzzle up behind his head, hand on the grip` | idle, taunt |
| Lunge shot | `wide lunge toward the right, shotgun held out level in one hand, free fist clenched` | heavy shot |
- Keep the gun out of the face: the muzzle sits below the eye line on aims, beside the cheek (not in front) when up.
- On the recoil frame long hair and coat tails flick back toward the left of the image; that sells the shot.

## Pitfalls to name in prompts
- Giant blade shrinks to a normal sword -> `huge blade as long as his whole body and as wide as his torso, same
  size as in the original`, and pad the canvas first.
- Body stands straight under a giant blade -> name the lean and the bent knees in every pose.
- Scythe blade flipped (edge outward, or on the wrong side of the shaft) -> `blade curving down from the top of the
  shaft toward the right, sharp inner edge facing back toward him`.
- Scythe hands slide together -> name `right hand high, left hand low, far apart` each pose.
- Kunai in a forward grip or extra kunai left in the hand after release -> name the reverse grip; scrub copies after release.
- Chibi limbs lengthen and the head shrinks in big poses -> repeat the proportions; keep the head still.
- Smear in-betweens blur the weapon away -> stepped key poses, paint the smear locally.
- Generator paints its own flashes or energy on gun and sword poses -> scrub, then bake a `vfx_workbench` effect.
