# Sword and shield (buckler, targe, rotella, dueling shield) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

The two basic buckler wards are in [weapon-sword.md](weapon-sword.md) -> "Sword and buckler". Facing right throughout:
sword in the right (near) hand, shield on the left (far) arm. No source shows a clear shield punch; the push below is
built from the presses.

## Contents
- [Shield types, what to draw](#shield-types-what-to-draw)
- [What every sword-and-shield pose keeps](#what-every-sword-and-shield-pose-keeps)
- [Guards to draw (visible description for the prompt)](#guards-to-draw-visible-description-for-the-prompt)
- [Moves (key pose A -> key pose B, trail/effect in screen terms)](#moves-key-pose-a---key-pose-b-traileffect-in-screen-terms)
- [Interpolate or step](#interpolate-or-step)
- [Frame rhythm (CC0 knight sprite, character ~22-24 px)](#frame-rhythm-cc0-knight-sprite-character-22-24-px)
- [Canvas](#canvas)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## Shield types, what to draw
| Shield | Visible description for the prompt | Notes |
|---|---|---|
| Buckler | `small round buckler with a domed boss, gripped in his left fist` | about head-sized; centre grip, no strap |
| Square targe | `square targe held by a grip in his left hand at arm's length, one corner pointing up` | torso-wide; Di Grassi holds it at head height |
| Round targe / rotella | `large round shield strapped to his left forearm, covering him from chin to thigh` | elbow bent, held close, can tilt to cover the face |
| Dueling shield | `tall wooden shield, taller than him, pointed spikes at top and bottom, held upright by a pole grip down its middle in his left hand` | Talhoffer; stands on or near the ground |
Never just `shield`: the generator then picks a size per frame.

## What every sword-and-shield pose keeps
- **The shield arm reaches across.** The left arm is behind the torso, so the shield shows only when pushed
  forward: in front of the chest or past it toward the right. Say `shield on his far left arm, pushed forward in
  front of his chest`.
- **Face or edge.** Held at the chest and turned to the viewer = a full disc with its boss. Pushed out at arm's
  length toward the enemy (Di Grassi, Marozzo, I.33 opening) = edge-on, a thin upright oval or a cone with the boss
  pointing right. Name which; without it Pro Flash switches between frames.
- **Two schools of hand placement.** Medieval buckler (I.33): `sword hand tucked right behind the buckler`, the two
  fists move together at the same height. Renaissance (Marozzo, Di Grassi): shield high, sword low:
  `shield arm out at head height, sword hand at his right hip, blade level pointing forward under the shield`.
  Pick one per character and keep it in every frame.
- **Arms move in opposition** (gesture strip, sprite): sword back = shield forward; on a big committed cut the
  shield swings out to the side or behind, and it returns in front for the settle.
- **Long low stance.** Feet far apart, front knee bent, torso leaning forward, head behind the shield.

## Guards to draw (visible description for the prompt)
| Guard | Visible description | Use |
|---|---|---|
| Low cover | `sword low behind him, blade pointing back toward the lower left; buckler held at his chest, disc facing the viewer; crouched in a long stride` | idle / ready |
| Paired forward (I.33) | `both arms straight out at chest height, sword hand just behind the buckler, blade level pointing right` | end of a thrust, bind / clash frame |
| High, shield out (I.33) | `sword raised above his head, blade pointing up and back; left arm straight out at head height, buckler edge-on toward the right` | overhead-cut wind-up |
| Cocked thrust (I.33) | `sword hand drawn back at shoulder height, blade level pointing forward; buckler edge-on at arm's length in front` | thrust wind-up |
| Buckler at the face (Marozzo) | `buckler held beside his face at cheek height, elbow bent; sword low in front, point forward and up; crouched` | defensive idle |
| Open high (Marozzo) | `sword raised high above his head, blade up; shield arm out to the side at chest height; upright stance` | big overhead wind-up, taunt |
| Shield high, sword low (Di Grassi) | `shield arm straight out at head height; sword hand at his right hip, blade level forward beneath the shield` | Renaissance idle, thrust start |
| Rotella cover | `large round shield on his forearm, tilted to cover his face and chest; sword hand low at his hip, point forward under the shield's lower edge` | heavy-shield idle |
| Behind the dueling shield | `standing behind the tall shield, left hand on its pole grip at chest height, sword raised over its top edge or held beside its side` | Talhoffer idle |
| Shield-high idle (sprite) | `shield held forward at chest height, disc facing the viewer, sword level at the waist behind it, blade pointing back` | game idle; small vertical bob |

## Moves (key pose A -> key pose B, trail/effect in screen terms)
- **Cut over the shield:** A = high, shield out -> B = sword arm extended forward at head height over the top of the
  buckler, blade level toward the right, buckler still at the chest below it. Trail: from above the head, over the
  top, forward; `swing_slash` or `slash_trail`. The shield stays low and in front in B.
- **Thrust from behind the buckler:** A = low cover or cocked thrust -> B = sword arm level at chest height, point
  passing beside the buckler toward the right, buckler next to the fist, deep lunge. `thrust_streak` from the shield
  edge forward; no crescent. Interpolates if both poses state the buckler's place.
- **High thrust over the hand (I.33):** B = `sword hand at head height, blade level forward at the enemy's face;
  buckler held low at his belly`. Same streak, one row higher.
- **Hanging strike (I.33):** `torso bent far forward, both fists together at face height, blade hanging down and
  forward`. Works as a cut that ends low or as a catch against a rising blow.
- **Cut with the body opening (sprite slash):** the shield swings back behind the body (an edge-on ring at the left
  of the figure) as the torso turns and the sword sweeps. A = idle -> B1 = shield swung back to the left, sword
  overhead -> B2 = low level follow-through -> idle. Use for a big hit where the guard drops.
- **Shield block (snap):** idle -> `shield raised to face height, disc facing the viewer, head ducked behind it,
  knees bent lower` (hold ~200 ms) -> idle. The sprite's raise is only a few pixels plus a crouch and still reads.
  `spark_burst` or `hit_star` on the shield face, not on the body.
- **Buckler press (I.33 binds):** with the blades crossed, `buckler and forearm laid over the enemy's sword arm,
  pressing it down, sword raised to cut from above`. Two separate arm motions: step it.
- **Shield push / bash (built from the presses):** A = shield pulled in at the chest, elbow bent, weight back ->
  B = `left arm thrust straight forward, shield face pushed toward the right, shoulder behind it, front foot stepped
  forward`. Stepped (2-3 frames), `shockwave_ring` or `hit_star` at the shield's front edge.
- **Dueling shield (Talhoffer):** the shield stays upright and planted; the fighter leans out past its edge. Thrust
  around it: `leaning out past the shield's right edge, sword arm thrust low toward the enemy's leg`. Lever: the
  shield's lower spike hooks the enemy shield and turns it flat, then a thrust over it. Strike over the top: sword
  arm raised above the shield's upper spike, cut down over it.

## Interpolate or step
- A far-arm shield in in-betweens vanishes, doubles (one at the chest, one behind) or jumps to the near arm.
  Interpolate only when A and B keep the shield in the same place (thrusts, sprite slash recovery).
- Any move where the shield moves a lot (push, block, swing back, press) = stepped key poses, each edited from the
  idle with the shield described in that frame. Check every frame at 3x.

## Frame rhythm (CC0 knight sprite, character ~22-24 px)
- **Idle, 5 frames:** shield in front, sword behind; 1-2 px bob only.
- **Shield raise, 5 frames:** shield up a step and crouch, held; loops as a guard.
- **Slash, 12 frames:** idle -> 1 frame turning (shield goes back) -> 1 frame rising crescent over the top ->
  2 frames sword overhead -> 1 frame low level crescent -> 2 frames follow-through with a small streak ->
  1 frame shield returning -> 3 frames settle. Two smear frames carry the hit.
- **Stab, 8 frames:** 2 frames pull back -> 3 frames arm extended with a growing streak (shield swung back) ->
  2 frames retract -> shield back in front. Matches `key-pose-animation.md`.

## Canvas
- A forward shield adds ~20-25% width to the right of the body; a swung-back shield adds about as much on the left.
  Size the canvas from the widest key pose, not the idle, or the shield gets clipped or shrunk.
- A dueling shield is taller than the fighter: canvas height about 1.3 x the sprite height, spikes included.

## Pitfalls to name in prompts
- Shield jumps to the near (right) arm -> `shield on his far LEFT arm, sword in his near RIGHT hand` in every edit.
- Shield vanishes in wide poses -> describe where it is in that frame (`shield still held at his chest`).
- Size drifts (round shield shrinks to a buckler, square targe turns round) -> name type and size every pose:
  `same size square targe as in the original`.
- Sword hand and shield hand merge into one blob -> `two separate hands: the sword hilt in his right hand behind
  the shield, the shield grip in his left fist`.
- Shield turned the wrong way (inside toward the viewer on a far-arm shield) -> `outer face of the shield with its
  boss facing the viewer`.
