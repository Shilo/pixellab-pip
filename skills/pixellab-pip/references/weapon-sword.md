# Sword (one-handed, longsword, sword and buckler) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Key-pose production is optional under `key-pose-animation.md`; katana kamae live in `weapon-katana.md`. Facing right throughout: right hand,
right foot and the near side face the viewer.

## Contents
- [What every sword pose keeps](#what-every-sword-pose-keeps)
- [More guards (Fiore's poste), what to draw](#more-guards-fiores-poste-what-to-draw)
- [More guards (German chart), what to draw](#more-guards-german-chart-what-to-draw)
- [The four cuts as animations (key pose A -> key pose B, trail path in screen terms)](#the-four-cuts-as-animations-key-pose-a---key-pose-b-trail-path-in-screen-terms)
- [Defence poses (block / parry / hurt-adjacent)](#defence-poses-block--parry--hurt-adjacent)
- [Sword and buckler (one-handed sword)](#sword-and-buckler-one-handed-sword)
- [Frame rhythm (from a CC0 knight sprite set, ~28 px frames)](#frame-rhythm-from-a-cc0-knight-sprite-set-28-px-frames)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every sword pose keeps
- **Long stride.** Every manuscript fighter stands with the feet about 1.5 shoulder widths apart, front knee bent
  over the foot, back leg nearly straight, back heel lifting on the cut. The generator keeps the idle's feet
  unless told: say `long stride, feet far apart, front knee bent, back leg straight`.
- **The cut lands with a step.** Cuts are thrown while passing forward (the back foot steps through); the hit pose
  has the other foot in front from the wind-up. For an in-place game attack keep the step short: `steps forward
  onto the near right foot` and `back foot in the same place`.
- **Both hands on a longsword.** Right hand under the cross, left hand at the pommel, in every pose including the
  follow-through. Say `both hands on the hilt`; Pro Flash often drops the left hand on wide poses.
- **Same blade length as the idle.** Ask for the full-length blade in every pose (`full-length blade, as long as
  in the original`); short blades were the most common fault in testing.

## More guards (Fiore's poste), what to draw
| Guard | Visible description for the prompt | Use |
|---|---|---|
| Woman's guard (posta di donna) | `the sword resting on his right shoulder, hilt at the shoulder, blade pointing back and up behind him` | heavy-cut wind-up, cocky idle |
| Window (posta di finestra) | `hilt raised beside his right temple, blade level, point aimed forward at the enemy's face` | thrust wind-up (= Ochs) |
| Iron door (porta di ferro) | `both hands low in front of his belly, blade pointing forward and down at the ground ahead` | defensive ready, rising-cut start |
| Boar's tooth (dente di zenghiaro) | `hands at his right hip, point angled forward and up` | rising thrust / rising cut start |
| Long tail (coda longa) | `blade trailing low behind him at his right side, point near the ground` | sweeping rising cut wind-up |
| Two-horned (bicorno) | `hands pulled in to his chest, blade straight forward and level` | close thrust |
| Crown (frontale / corona) | `blade held upright in front of his face, hilt at chest height` | block / salute pose |
| Long guard (posta longa) | `arms straight out in front, blade level` | end of a thrust (= Langort) |
| Short guard (posta breve) | `hands in front of his belly, elbows bent, blade pointing forward and a little down` | close ready, short thrust |

## More guards (German chart), what to draw
| Guard | Visible description for the prompt | Use |
|---|---|---|
| Crown (Krone) | `hands raised beside his head, blade straight up, cross-guard above his face` | high block against a downward cut |
| Hanging point (Hangetort) | `hands high in front of his forehead, blade hanging forward and down, point at chest height` | high-to-low thrust, hanging parry |
| Unicorn (Einhorn) | `hands above his forehead, arms extended, blade pointing up and forward at 45 degrees` | rising thrust at the face, end of a rising cut |
| Middle guard (Mittelhut) | `hilt at his right shoulder, blade level pointing straight back toward the left of the image` | level-cut wind-up |
| Key (Schlussel) | `hands pulled in at his chest, forearms crossed, blade level forward at shoulder height` | close thrust (like bicorno) |
| Barrier (Schrankhut) | `arms crossed and extended to his left, blade slanting down to the ground ahead of his front foot` | low parry, rising-cut start |
| Change (Wechsel) | `hands at his right hip, blade pointing steeply down at the ground beside his front foot` | low ready, rising-cut start |
The chart's one-handed guards (drawn with a curved short sword, good for any one-handed blade) all park the free
hand: `left fist on his hip` or `left fist at his chest`, never hanging. Watch (Wacht) = `sword hand above his head,
blade level over his head pointing back`; Bull (Stier) = `sword hand high beside his head, blade pointing forward
and down`; Straight parry (gerade Versatzung) = `sword arm straight out at shoulder height, blade angled up`;
Boar (Eber) = `sword hand low at his near hip, blade level across the front of his hips`; Bastion (Bastey) =
`sword arm reaching low forward, blade slanting down at the ground ahead`.

## The four cuts as animations (key pose A -> key pose B, trail path in screen terms)
Fiore draws them as one diagram: descending cuts, rising cuts, level cuts and thrusts.
- **Descending (fendente / Oberhau):** A = roof or woman's guard (hilt above the right shoulder, blade back) ->
  B = arms extended low in front, blade pointing forward and down at knee height, torso leaning over the front
  knee. Trail: from above and behind the head, over the top, down in front to knee height (a big arc on the near
  side). The diagonal version (Zornhau, from Zornhut) ends low on the far side: `blade ending low toward the lower
  left of the image`.
- **Rising (sottano / Unterhau):** A = long tail or iron door (blade low behind or low in front) -> B = hands high
  in front of the face, blade pointing up and forward. Trail: from low behind the hip, under and up in front to
  above the head.
- **Level (mezano / Mittelhau):** A = side guard with the blade back at waist height -> B = arms across the body,
  blade level pointing toward the left of the image after crossing in front. Trail: a flat ellipse at chest/waist
  height in front of the body; use `blade_trail.py` with a flattened path or `vfx_workbench` `swing_slash`.
- **Thrust (punta):** A = window / Ochs or bicorno (point forward, hands pulled back) -> B = long guard, both arms
  straight, blade level at chest height, deep lunge. Trail: a straight line, `vfx_workbench` `thrust_streak`; no
  crescent. The generator likes to raise the blade overhead between these two poses - check the in-betweens or
  use the 6-frame swing (`key-pose-animation.md`).
- **Body leads, blade follows** (keyframe sheet notes): the shoulder rolls up before the arm lifts; the hips turn
  and the front foot plants a frame before the blade comes down; the body stops moving forward on the hit frame.
  In key poses write the torso, not only the arms: A = `shoulders turned away, back toward the viewer, weight on
  the back foot`, B = `chest turned toward the viewer, weight on the front foot`.
- **Charged ground slam (greatsword):** A = `blade raised up and back over his right shoulder at 45 degrees, both
  hands above his head, leaning back, weight on the back foot` -> B = `blade driven diagonally down, tip striking
  the ground one body length ahead, deep lunge, back leg straight`. Trail: a big arc from behind the head to the
  ground in front; `crater_dust` or `debris_burst` at the tip. The front foot slides forward between A and B.
- **Low sweep:** `crouched almost to the ground, front knee deeply bent, blade sweeping level at ankle height`.
  Trail: a flat low ellipse at foot level. Step it from the idle; interpolation stands the figure up mid-swing.

## Defence poses (block / parry / hurt-adjacent)
- **High block (Krone / hanging parry):** `both hands raised above his head, blade held level or tilted down
  across the top of his head to catch a downward cut, knees bent`. Talhoffer's parries all meet the enemy blade
  near the hilt (the strong of the blade), never at the tip.
- **Hanging guard parry:** `hilt high beside his head, blade hanging down and forward across his body, point low`.
- **Bind:** two blades crossed at mid-length in front, both fighters' arms half extended; good for a clash or a
  block-reaction frame.
- **Block angle:** the blocking blade crosses the incoming blow's path at a right angle: upright beside the body
  for a level cut, level overhead for a downward cut, slanting across the front for a diagonal. Name the attacker's
  direction and the blade angle together.
- A block animation is a snap like a hurt: idle -> block pose (hold ~200 ms) -> idle; add a `spark_burst` or
  `sparks_shower` from `vfx_workbench` where the blades meet.

## Sword and buckler (one-handed sword)
- The buckler is held at the left fist with the left arm pushed forward, and it **covers the sword hand**: in
  guards and cuts the buckler moves with the sword hand, close in front of it.
- First ward (under the arm): `sword held under his left armpit, blade pointing back, buckler held out in front`.
- High ward: `sword raised above his head pointing back, buckler held forward in front of his face`.
- The shield or buckler stays on its arm in every frame (the generator drops or doubles it in wide poses); check
  each key pose and in-between at 3x.

## Frame rhythm (from a CC0 knight sprite set, ~28 px frames)
- **Overhead slam, 10 frames:** guard -> 4 frames of wind-up with the blade trailing back behind -> 1 smear frame
  (a full crescent over the top) -> 4 frames of follow-through and settle -> guard. The hit is ONE frame.
- **Two-hit slash, 12 + 5 frames:** a rising crescent, then a low horizontal crescent, then a 5-frame recovery
  back to guard. Alternate high and low crescents for combos.
- **Stab, 8 frames:** 2 frames pulling back, 3 frames holding the extended thrust with a short streak, 2-3 back.
- The shield stays on the front arm in every frame; the trail is the only effect.
- Same timing as in `key-pose-animation.md`: hold the wind-up, one fast hit frame, longer settle.
- **Keyframe sheet (frame numbers at film rate):** swing = ready hold 6 -> raise 4 -> held at the top 3 (a "moving
  hold": body still drifting, blade still) -> down 5-8 -> hit, body stops. Chop = hit key -> swung back across with
  a step back (7) -> raised with a hop back (8) -> overhead, heel up (7) -> down to level (4). About two thirds of
  each move is wind-up and hold, the fall is short. For 8-10 game frames: 2 raise, 1-2 top hold, 1 fall, 1 hit,
  2-3 settle.
- **Draw from the back/hip into a two-hand hold** (same sheet): one hand lifts the sword up past the shoulder, it
  swings down low in front, the second hand grabs the hilt, the body sinks into the guard. Hand-swap frames lose
  the sword: generate the grab as its own key pose.

## Pitfalls to name in prompts
- Feet stay at idle width -> say the long stride. Left hand vanishes -> `both hands on the hilt`.
- Blade shortens in wide poses -> `full-length blade, as long as in the original`.
- A thrust's in-betweens raise the blade overhead -> 6-frame swing or stepped poses + `thrust_streak`.
- **Wrist bent at the hilt** -> in a thrust the blade continues the line of the forearm (`blade in line with his
  arm`); a blade sticking up at 90 degrees from the fist reads wrong. A relaxed idle holds the blade pointing forward
  and down from the hip, not hanging straight down like a dropped stick.
- **Greatsword reach:** a blade as long as the fighter reaches about one body length ahead on a thrust or slam;
  pad the canvas in front first or the generator shortens it.
- A one-handed sword plus a buckler: name which hand holds which, and that the buckler stays in front of the sword hand.

## Core longsword guards

| Longsword guard | Visible description |
|---|---|
| Fool's (Alber) | tip lowered toward the enemy's feet |
| Roof (Vom Tag) | hilt at or above the right shoulder, tip up and behind (overhead wind-up) |
| Ox (Ochs) | hands beside the head, blade level, pointing at the enemy's face |
| Plow (Pflug) | hilt at the right hip, tip angled up at the enemy's face |
| Side / Tail (Nebenhut) | hilt at the right hip, left arm across the body, tip low and behind |
| Longpoint (Langort) | arms fully extended at chest height, tip at the throat (end of a thrust) |
| Wrath (Zornhut) | hilt at the right shoulder, blade back and down behind the body, core coiled |
