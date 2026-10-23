# Spear (spear, pike, bayonet-style thrusts, javelin) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Facing right throughout: right hand, right foot and the near side face the viewer. The point is on the right side of
the image, the butt on the left.

## Contents
- [What every spear pose keeps](#what-every-spear-pose-keeps)
- [Ready and carry poses, what to draw](#ready-and-carry-poses-what-to-draw)
- [Moves as animations (key pose A -> key pose B, trail/effect)](#moves-as-animations-key-pose-a---key-pose-b-traileffect)
- [Throw, frame by frame (Muybridge, read as facing right)](#throw-frame-by-frame-muybridge-read-as-facing-right)
- [Frame rhythm (from the LPC spear sprite, 8 frames per direction)](#frame-rhythm-from-the-lpc-spear-sprite-8-frames-per-direction)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every spear pose keeps
- **Two hands far apart on the shaft.** In every drill plate the hands sit about a forearm-plus apart: the rear
  hand near the butt end at the hip or beside the face, the front hand a third of the way up. Say `rear hand near
  the butt end, front hand far ahead on the shaft, hands well apart`; without it the generator bunches both fists
  together in the middle like a sword hilt.
- **One straight, rigid shaft.** Ask for `one straight rigid wooden shaft, same length as in the original` in every
  pose. The point stays toward the right of the image and the butt toward the left except in the throw wind-up
  and the butt strokes, where you say so explicitly.
- **Canvas width.** Pro Flash stops at 256 px. Tested: a 96x200 hero with a spear as tall as
  she is on a 256x200 canvas, padded at x=40, held every key pose of a lunge thrust and a javelin throw inside the
  image (the thrust point ~10 px from the right edge); only the deepest lunge in-betweens touched the left edge with
  the back foot. Keep the spear as tall as the hero (no taller), place her at x≈40, and say `the spear point fully
  inside the image, not cut off at the right edge`. Pike length (2-3x height) doesn't fit any generated canvas.
- **Long, low stance.** All the thrust figures stand with feet 1.5-2 shoulder widths apart, front knee bent, back
  leg straight; the long thrust drops into a deep lunge with the back leg almost flat. `long low stance, left foot
  forward, front knee bent, back leg straight`.

## Ready and carry poses, what to draw
| Pose | Visible description for the prompt | Use |
|---|---|---|
| Upright rest | `spear standing upright beside him, butt on the ground by his right foot, right hand gripping at shoulder height` | idle, roster portrait |
| Shoulder slope | `spear resting on his right shoulder, point angled up toward the upper right, both hands at his chest` | walk / march |
| Low ready (hip) | `rear hand at his right hip near the butt, front hand ahead, shaft angled from low behind him up to the point at chest height toward the right of the image` | default combat idle, thrust start |
| Guard (bayonet) | `shaft held diagonally across the front of his body, rear hand at the belt, front hand forward, point aimed at chest height toward the right` | alert idle |
| Shoulder-height level | `shaft level at shoulder height, rear hand beside his cheek, other arm stretched back holding the butt end, point far to the right` | overhand thrust wind-up |
| Overhead lift | `both hands raised above his right shoulder, shaft level over his head, point toward the right` | downward stab start |
| Kneeling overhead | `kneeling on his right knee, both hands above his head holding the shaft level, point toward the right` | crouched ambush, downward stab start |
| Low point | `walking forward, shaft slanting down from behind his right shoulder to the point near the ground ahead, toward the lower right` | stalking walk, rising-thrust start |
| Planted upright | `crouching behind the spear, shaft upright in front of him, butt on the ground, both hands high on the shaft` | defensive idle, pole-vault start |
| With shield | `round shield on his left arm in front of his chest, spear in his right hand held underarm at the hip, point forward toward the right` | run, shield idle |

## Moves as animations (key pose A -> key pose B, trail/effect)
- **Thrusts use the 6-frame clip** (the 10-frame one reached the hit by frame 4, then repeated it with flashes).
- **Low forward thrust:** A = low ready (hands at the hip, slight lean back) -> B = `both arms pushed forward, front
  arm straight, shaft level at waist-to-chest height, point far toward the right of the image, torso leaning over
  the bent front knee`. The shaft only translates to the right; it never rotates. Trail: `vfx_workbench`
  `thrust_streak` along the shaft line, `spark_burst` at the point on contact.
- **Long thrust (lunge):** A = guard -> B = `deep lunge, back leg stretched flat behind him, chest low over the
  front knee, both arms fully extended, point level far toward the right`. Add `speed_lines` behind the body.
- **Short thrust:** same as long but the feet barely move; arms extend, body leans. Good for a fast jab loop.
- **High (overhand) thrust:** A = shoulder-height level or overhead lift -> B = `front arm straight, shaft angled
  slightly down, point aimed at head height toward the right, rear hand pushed forward past his chin`.
- **Sliding thrust (pike drill):** the front hand stays near the point while the rear hand travels up the shaft;
  the shaft slides through the hands. Interpolation smears this; use stepped key poses (A, mid with hands
  together, B) and keep each hand's position on the shaft named in every prompt.
- **Brace against a charge:** `crouching low, butt of the spear planted on the ground against his rear foot at the
  lower left, shaft angled up toward the upper right, point at chest height of a rider, left hand holding the
  shaft low, right hand free or on his sword hilt`. Hold pose, no trail.
- **Parry / high port:** high port = `shaft held diagonally across his chest, front hand high near his left
  shoulder, rear hand low at his right hip, point up toward the upper right`. Parry = snap the whole weapon a short
  way up or across in front with the point still upright, arms pushed out; idle -> parry (hold ~200 ms) -> idle,
  `spark_burst` where the blades meet.
- **Butt stroke (a reversal, step it):** A = guard -> B = `rear hand swung forward and up, butt end of the shaft
  driven toward the right at head height, point now dropped low behind him toward the lower left`. Then a smash:
  `shaft held level above his shoulder at head height, both elbows bent, butt end driven straight toward the
  right`. The point is BEHIND here on purpose: say it in the prompt and generate stepped, never interpolate.
- **Mounted thrust:** A = `spear couched level under his right armpit, point forward toward the right, left hand on
  the reins` -> B = `leaning forward out of the saddle, couched spear level, point pushed far to the right`. The
  other mounted variant: `right arm raised above his head holding the spear overhand, point angled down and
  forward toward the lower right`. The horse keeps its gait; only the rider's torso and arm change.
- **Spear and shield (one hand on the spear):** run = the with-shield pose in a leaning stride. Coil = `shield
  held up in front, right arm drawn far back, spear level at the hip, point just past the shield rim`. Block ->
  overhand stab: A = `crouched low behind the shield, shield covering his body, right arm raised above his head
  holding the spear overhand, point aimed forward over the shield rim toward the right` -> B = `right arm driven
  forward and down, point toward the lower right`; trail a short `thrust_streak` angled down. Name the grip every
  pose: `the spear in his right hand only, his left arm holds the shield`.
- **Leaping stab:** `in the air, knees tucked, shield raised high on his left arm, right arm driving the spear
  down, point toward the lower right`. Hit = landing frame; `debris_burst` at the point.
- **Pole-vault kick:** A = planted upright -> B = `swinging sideways around the planted spear, hands high on the
  shaft, body tilted in the air, both feet kicking toward the right`. Stepped key poses; the shaft does not move.
- **Bladed polearm (glaive) cuts:** with a long blade on the shaft the weapon cuts, not just thrusts.
  Rising cut: A = `crouched, shaft low, blade near the ground ahead toward the lower right` -> B = `shaft swung up
  upright in front of him, blade straight above his head`; trail a vertical band from the ground to the top.
  Diagonal slash: B = `very wide low stance, rear hand low at his left hip near the butt, front arm stretched up
  toward the upper right, blade at the upper right end`; trail one long crescent band along the blade path from
  the upper right down to the ground in front. Edge faces the direction of the cut, as on the axe page.
  Keyframe rhythm from the sheet: the full smear lands on the first fast frame, then thins over 3 frames while the
  body barely moves.

## Throw, frame by frame (Muybridge, read as facing right)
1-3 approach/draw: `wide stance, left foot forward toward the right, right hand sliding back along the shaft from
arm's length to beside his face, shaft level above his shoulder, point toward the right`.
4-6 full wind-up: `right arm stretched straight back toward the left at shoulder height, shaft level along the arm
and past his head, chest turned to the viewer, left arm bent across the front, widest stance`.
7 load: `weight on the bent front knee, body leaning back, right elbow bending, hand still behind his head`.
8 release: `right arm whipping forward and up toward the upper right, the spear just leaving the hand, angled up,
lunging onto the front leg, back toe dragging`.
9-10 follow-through: `torso pitched forward over the front leg, back leg kicked up level behind him, empty right
arm hanging down in front`. 11-12 recover: `back leg lowering, stepping through to stand`.
Tested recipe (3 key poses): idle -> 4-frame clip into the full wind-up (4-6) -> release (8, the spear
just out of the hand, angled up-right) -> follow-through (9-10, hand empty). The lift clip swung the point backward
in one frame: drop it, and put `the point stays toward the right the whole time` in the clip's action. Fly the spear
with the free `throw_prop.py` finishing script (step it along the throw angle,
e.g. 40,-17 px per frame), then a thin streak behind it with `blade_trail.py`. From the release on, `no spear in her hands`.

## Frame rhythm (from the LPC spear sprite, 8 frames per direction)
- 1 carry frame (shaft diagonal, point up-right) -> 2 frames pulling to hip level -> 2 frames extending -> 3 frames
  holding the extension -> back. The point travels only a short way; the thrust reads from arms and lean, not
  from a huge reach. The hit is the first extended frame; the hold sells it.
- Same timing as in `key-pose-animation.md`: hold the wind-up, one fast hit frame, longer settle.

## Pitfalls to name in prompts
- Shaft grows or shrinks between poses -> `same length as in the original`, check at 3x beside the idle.
- Shaft bends or kinks at the hands -> `one straight rigid shaft`.
- Point flips to the back of the body in in-betweens -> `point toward the right of the image, butt toward the
  left`; step the poses if it persists.
- Hands bunch together mid-shaft -> name each hand's place: `rear hand near the butt, front hand far ahead`.
- Second spear appears after a throw (or the spear stays in the hand) -> `his right hand empty, no spear in his
  hands` on every frame after the release.
- Point cut off by the canvas edge -> widen the canvas first, then `spear point fully inside the image`.
- Shield dropped or second hand grabs the shaft in spear-and-shield poses -> `spear in his right hand only, shield
  on his left arm` in every pose.
- Glaive blade shrinks into a plain spear point -> `the same long blade on the end of the shaft, same size`.
