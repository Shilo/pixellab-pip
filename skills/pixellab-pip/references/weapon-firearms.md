# Firearms (pistol, rifle, shotgun, sniper rifle) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Read this for gun grips, stances, reload, pump and draw cycles, run-and-gun, prone and kneeling shots, top-down
facings and dual pistols. Optional key-pose production uses `key-pose-animation.md`. Facing right throughout: the muzzle points toward the right of the image, the stock or grip toward the left.

## Contents
- [Which hand is which (facing right)](#which-hand-is-which-facing-right)
- [What every gun pose keeps](#what-every-gun-pose-keeps)
- [Stances, what to draw](#stances-what-to-draw)
- [Cycles as key poses (reload, pump, bolt, draw)](#cycles-as-key-poses-reload-pump-bolt-draw)
- [Run-and-gun and aim angles](#run-and-gun-and-aim-angles)
- [Top-down facings](#top-down-facings)
- [Frame rhythm](#frame-rhythm)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## Which hand is which (facing right)
- **Long gun:** the near RIGHT hand holds the pistol grip with the stock pressed into the near right shoulder; the
  far LEFT hand reaches forward under the barrel to the forend. The right elbow sticks out back-left at about
  shoulder height, the left elbow sits low under the gun. Say `stock tucked into his right shoulder, cheek resting on
  the stock, right hand on the grip, left hand forward under the barrel`.
- **Pistol, two hands:** the right hand grips high on the handle, the left hand wraps over the right fingers from
  below, both thumbs pointing forward along the left side of the frame. At sprite size this reads as one fist
  cluster at the end of two arms: `both hands wrapped together around the pistol grip`.
- **Pistol, one hand:** body turned side-on, gun arm straight out at shoulder height toward the right, the free hand
  at the hip or flat on the chest. A side-on one-hand pose is the clearest silhouette at small sizes.
- Generators mirror long guns (stock on the far shoulder, barrel sprouting from the back). Name both hands and the
  shoulder in every pose.

## What every gun pose keeps
- **Gun line = eye line.** Aimed long guns sit with the sights just below the eye, head tipped down onto the stock,
  never upright above it. Pistols in an aim sit at chin-to-eye height, arms not raised above the face.
- **Same gun every pose.** Name length relative to the body: `pistol about the size of his hand`, `rifle as long as
  from his shoulder to his knee`, `long sniper rifle with a scope, longer than his arm span`. Guns shrink in wide
  poses like blades do; check at 3x beside the idle.
- **Forward lean.** Every standing shot leans the torso slightly forward over the front foot, weight on the balls of
  the feet: `slight forward lean, nose over the front toes, left foot forward`. An upright or backward-leaning
  shooter reads as startled, not firing.
- **Canvas.** Pistol aims need ~arm length of room in front; a rifle ~1.2x the figure's width; a sniper rifle in prone
  is about as long as the figure is tall, so prone needs a wide, short canvas.

## Stances, what to draw
| Stance | Visible description for the prompt | Use |
|---|---|---|
| Low ready | `rifle shouldered, muzzle angled down toward the ground ahead at the lower right, eyes up over the sights` | alert idle, walk |
| High ready | `rifle shouldered, muzzle tipped up just under his eye line toward the upper right` | alert idle, before a shot |
| Hip carry | `rifle held low across his hips in both hands, barrel level toward the right` | relaxed idle, run |
| Pistol ready (up) | `pistol held upright beside his right cheek, muzzle pointing at the sky, elbow bent low` | wary idle, draw end |
| Pistol low | `both arms angled down, pistol pointing at the ground ahead of his feet` | sneak, patrol |
| Square two-hand aim | `chest square, both arms straight forming a triangle, pistol at chin height toward the right, feet shoulder width` | default pistol shot |
| Bladed two-hand aim | `body turned side-on, right arm nearly straight, left elbow bent and pointing down, pistol at eye level` | duelist, cop |
| Standing rifle aim | `feet shoulder width, left foot forward, rifle shouldered and level toward the right, slight forward lean` | default rifle shot |
| Kneeling | `kneeling on his right knee, sitting back on his right heel, left knee up in front, left elbow resting just past the left knee, gun level toward the right` | cover shot, steady shot |
| Crouch | `knees deeply bent, feet apart, torso leaning forward, arms straight out, pistol toward the right` | quick low shot |
| Prone | `lying flat on his belly, body angled slightly behind the gun, legs spread, toes turned out, both elbows on the ground, rifle level just above the ground toward the right` | sniper, crawl stop |
| Prone with bipod | `lying flat, the rifle's two short legs resting on the ground under the barrel, his left hand under the rear of the stock` | sniper idle and shot |
| Rested on cover | `kneeling behind a low crate, forend resting on the crate top, left forearm along the crate, muzzle past its edge` | cover shooter |
| Wall cover | `standing beside a wall at the right, the side of his left hand pressed against the wall edge, only the gun and one eye past it` | peek-and-shoot |

Swap legs only for kneel/crouch/prone variants: `arms, hands and gun exactly as in the original, only the legs
change` gives 3-4 shot poses from one base, like the bow page's kneeling draw.

## Cycles as key poses (reload, pump, bolt, draw)
The gun stays in the hands through most of these, so interpolate with 4-frame clips between checked poses; step
(don't interpolate) any frame where a magazine, shell or the gun itself changes hands
([Carried And Worn Props](key-pose-animation.md#props-projectiles-and-effects)).
- **Pump-action (shotgun):** A = shouldered aim -> B = `left hand pulled back along the barrel to just in front of
  the trigger, a spent red shell popping out of the side, flying up and toward the left` -> A again (left hand slid
  forward to the barrel end). The stock, cheek and right hand never move; only the left forearm slides along the
  barrel line. Say `the stock stays in his shoulder, only his left hand slides`.
- **Lever or bolt action:** same as the pump but the right hand moves: lever = `right hand pushed down and forward
  under the gun, the lever swung open below the grip`; bolt = `right hand lifted to a small knob at the back of the
  gun beside his cheek, pulled back toward the left`. Muzzle stays on line.
- **Magazine reload (rifle or pistol, side view):** A = `gun tilted, muzzle angled up toward the upper right, held in
  his right hand at chest height, left hand dropping an empty magazine from under the gun` -> B = `left hand at a
  pouch on his belt` -> C = `left hand pushing a fresh magazine up into the bottom of the gun` -> D = `left hand
  slapping the top of the gun` (pistol: pulling the slide back) -> back to aim. Name the empty magazine falling
  toward the lower left on A only; scrub any extra copies afterward.
- **Shell-by-shell reload (shotgun):** a loop of `left hand at the belt picking up a red shell` -> `left thumb
  pushing the shell into the bottom of the gun just in front of the trigger`, the gun held tilted across his chest.
  Generate the pair once and repeat it per shell, then one pump.
- **Draw from holster:** order and the empty-holster rule are below. Add, for a jacketed
  figure: `right hand sweeping the jacket back behind the hip` on the grip pose, and `finger straight along the
  side of the gun, off the trigger` until the push pose.
- **Holster (reverse draw):** lower to pistol-low, eyes still forward, then step the gun into the holster;
  `the pistol back in the holster on his right hip, right hand resting on it`.

## Run-and-gun and aim angles
- **Run with long gun:** legs run, the upper body stays locked: `running, torso upright and square, rifle held at
  chest height in both hands, barrel level toward the right`. The gun only bobs up and down with the body; if the
  in-betweens swing it, add `arms and rifle locked, only the legs move`.
- **Run with pistol:** either one arm locked straight out aiming while the other pumps, or both arms pumping with
  the gun hand low; pick one and say it.
- **Aim angles (side-scroller):** reuse the run cycle and edit only the arms: `barrel pointing straight up`,
  `toward the upper right at 45 degrees`, `level`, `toward the lower right at 45 degrees`. Rifle from the shoulder
  rotates around the shoulder; for straight up the stock drops to the chest.
- **Duck / dash shot:** duck = crouch with the gun level at the hip; dash = `low forward lean, legs in a long
  stride, rifle level`, speed smoke behind the feet, never along the gun (speed-line rules in `key-pose-animation.md`).
- **Turning while aimed:** the arms-and-gun triangle stays fixed to the chest like a turret; the feet step and the
  hips turn. For a turn-to-aim, key the feet, not the arms.
- **Dual pistols:** `one pistol in each hand`. Parallel = `both arms straight out toward the right, the near gun
  slightly lower`. Crossed = `near right arm crossed over his chest pointing left, far left arm out to the right`
  (two targets). Name `two pistols, one in each hand` on every frame; generators merge them into one.

## Top-down facings
- The gun comes out from the right-hand side of the body, not the centre: facing right, that is the lower side of
  the sprite. Say `gun held at his right side, barrel pointing toward the right, offset below the centre line`. The
  muzzle point (flash and bullet origin) is that offset tip, not the head.
- Pistol: one or both hands at the end of straight arms just past the head. Rifle and shotgun: `stock at his right
  shoulder, gun running forward along his right side, left hand reaching across to the barrel`.
- Reload top-down reads from the free arm only: the left hand leaves the gun, travels to the chest or belt and
  back while the gun stays roughly on line, or the gun swings to point upward across the chest for the swap.
- Shot top-down: the gun and shoulders jolt back a few pixels toward the left, then return; no muzzle rise.
- Facing-down (toward the viewer) long gun reads best angled diagonally across the body toward the lower right.

## Frame rhythm
- Pistol shot, small side sprite, 5 frames: flash on 1, muzzle flipped up 30-50 degrees from the wrist for 3, back
  level on 5. Pistols kick UP at the wrist; long guns kick BACK into the shoulder with only a few degrees of rise.
- Rifle shot, 10 frames: the rock-back lands in 2-3 frames, the settle takes the other 7. Top-down: 3 frames.
- Raise-to-aim from a holstered idle: ~2 frames up, hold while firing, ~2 frames down.
- Reloads are long: 15-20 frames on a 3-frame shot. Hold the magazine-in frame; it is the read.
- Pump: back and forward 2 frames each, the shell ejecting on the back frame.

## Pitfalls to name in prompts
- Stock on the wrong shoulder / barrel from the back -> `stock in his near right shoulder, barrel toward the right`.
- Gun floats in front of the hands -> `both hands touching the gun: right on the grip, left on the forend`.
- Barrel bends or grows -> `one straight rigid barrel, same length as in the original`.
- Sights raised above the eyes -> `gun just below his eye line, head down on the stock`.
- Dual pistols merge -> `two pistols, one in each hand` on every frame.
- Ejected shell or magazine copied into later frames -> say it only on its own frame, scrub copies afterward.
- Generator flash baked into the aim or reload pose -> clear it per `key-pose-animation.md`, paint the real flash.
- Kneel or prone variants change the arms -> `arms and gun exactly as in the original, only the legs change`.

## Aim, recoil and mounted launchers

**Shots** (guns, bows, wands) reach forward only: canvas with room in front, pose A = the aim (`rifle shouldered, barrel levelled toward the right, braced stance`), pose B = the recoil (`shoulder and rifle jolted back, barrel kicked up, torso rocked back onto the braced back foot`). No crescent. For a requested instant shot, the first motion frame may be the event; identify the actual contact/release before setting `--hit`. Name an energy weapon's flash colour, or the generator paints an orange gunpowder flash. A big recoil from a kneel needs the path pinned (`stays low on bent legs, never falls over`). For a take that drops the gun, propose a scoped redo with `the gun never drops below shoulder height`. An explicitly accepted local recoil derivative can be a 2 px lift of the arm band only (rows where arms and gun stick out past the body), checking the rows below stay identical.

**Gear-mounted launchers** (a shoulder pod, a back cannon): the launcher moves with the recoil, so take the muzzle point per frame from the pose, not from the first frame, and start the exhaust after the recoil peak; otherwise the smoke lands on the head. Use these Shots poses, not the thrown-prop recipe.

**Generator flashes on shots and beams**: shot, beam, and projectile poses come back with the effect painted in, even the charge pose. For an unwanted flash, propose removing it from the affected key pose before animating (`scrub --box` or `--clear-right <tip x>`), clear the in-betweens' own flash at the barrel tip only (a colour scrub strips hair and skin the flash lit), or reuse the previous frame where the flash sits on the body (a short hold reads as weight). An agreed replacement flash/beam can use `vfx-workbench.md` and accepted composition at the muzzle or eye (`bake_fx`).

## Pistol draw

**Pistol draw and shot** (holster on the near right hip): ready → grip (right hand on the holstered pistol, left hand flat at the chest centre) → clear (muzzle turns forward at chest height, left hand joins, finger along the frame) → push (both arms extend, sights just under the eyes, never above the eye line) → recoil plus a `vfx-workbench.md` muzzle flash → aim hold. The pistol moves between poses: step, do not interpolate. Say `the EMPTY holster` in every pose after the draw.
