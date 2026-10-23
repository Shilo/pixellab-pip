# Bow (longbow, yumi, short recurve) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Facing right throughout.

## Contents
- [Which hand is which (facing right)](#which-hand-is-which-facing-right)
- [What every bow pose keeps](#what-every-bow-pose-keeps)
- [Stages, what to draw](#stages-what-to-draw)
- [Moves as key poses (A -> B, trail in screen terms)](#moves-as-key-poses-a---b-trail-in-screen-terms)
- [Frame rhythm (from the two CC0 sprite sets)](#frame-rhythm-from-the-two-cc0-sprite-sets)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## Which hand is which (facing right)
- The **bow is in the LEFT hand, the far arm**. It reaches out toward the right of the image at shoulder height;
  in a 3/4 view it comes out from behind the chest. The **RIGHT hand draws: the near arm**, folded in front of the
  near shoulder with the hand at the face and the elbow pointing back toward the left of the image.
- Shooting side-on opens the chest to the viewer and turns the head to look right along the arrow. Every source shows
  this: `chest turned toward the viewer, head turned to look right along the arrow`.
- Generators often mirror the archer (bow in the near hand). Say it outright: `the bow in his far left hand
  stretched out to the right, his near right hand pulling the string`.

## What every bow pose keeps
- **Bow shape and side.** The bow bulges toward the right (the grip is its rightmost point) and its tips curve back
  toward him; the string runs on the body side. A recurve's very tips curl forward again toward the right. Say
  `the bow bulges toward the right, its tips curving back toward him, the string on the body side`.
- **Bow length.** The longbow is about as tall as the archer, the yumi taller than the archer with the grip in its
  lower third (the top limb about twice the bottom), the Persian recurve about half his height. Name it in every
  pose (`a longbow as tall as he is`). Bows shrink in wide poses, same as blades.
- **Feet.** European: side-on, feet about shoulder width, legs straight, upright, no lean. Kyudo: wider, toes out,
  hips low and level. A quick game shot keeps the idle's feet: `feet planted as in the original, no step`.
- **The arrow's length decides the draw.** At full draw the arrowhead sits at the bow hand or a few pixels past it
  toward the right. Much further out means the draw is short; behind the bow means a too-short arrow or a mirror.

## Stages, what to draw
| Stage | Visible description for the prompt | Seen in |
|---|---|---|
| Ready | `bow held upright in his far left hand beside him, lower tip near his foot, string slack and straight` | Hansard |
| Nock | `bow lowered and tilted across the front of his hips, near right hand fitting the back end of an arrow onto the string, head bowed to look at it` | Pope, Hokusai |
| Set (European) | `arrow on the string, both arms lowered and angled down toward the lower right, bow tilted about 45 degrees in front of his hips, head already turned right` | stages diagram |
| Raise (kyudo) | `both fists lifted above his head, arrow level above his head pointing right, bow upright in front of him` | Hokusai |
| Draw | `bow arm straight out to the right, string hand pulled back to the middle of his chest, arrow level at chest height` | Hansard, Pope |
| Full draw, European | `string hand under the jaw, the string touching his chin and the tip of his nose, drawing elbow level with the arrow, pointing back left` | Badminton, Hansard |
| Full draw, kyudo | `arrow level with his mouth, string hand just behind his cheek, both arms spread wide and level, string crossing the chest` | Hokusai |
| Full draw, thumb | `string hand pulled past his ear to behind his head, drawing elbow raised to head height, short curved bow tilted slightly` | Hansard (Persian) |
| Release | `the string snapped straight and the bow upright, no arrow on the bow, string hand opened just behind the jaw` | Badminton, sprites |
| Follow-through | `bow arm still pointing right and steady, string hand slid back along the jaw to below the ear, fingers relaxed` | Badminton |
| Follow-through, loose bow | `bow hand opened, the bow tipped forward and down to nearly level, hanging from a strap around his wrist, string hand flung back to his near shoulder` | stages diagram |

Bow hand and arrow (hand sketches): the arrow rests on top of the bow fist and passes on the far side of the bow,
with the nock between the first two string fingers; the bow arm's elbow is turned out so the string clears the
forearm (`a leather guard on his far forearm`). At sprite size only the guard and a straight bow arm read.

Grips at sprite size (~8 px hand): three-finger draw = `fingers hooked over the string, back of the hand toward the
viewer`; thumb draw = `closed fist with the thumb hooked around the string, a thumb ring`. Morse's finer grips
(pinch, secondary, tertiary) don't read at 100x250; pick one of these two and keep it in every pose.

## Moves as key poses (A -> B, trail in screen terms)
- **Quick game shot (heroes).** A = full draw (the aim), B = follow-through (string straight, no arrow, hand back
  at the ear), like the rifle's aim/recoil in `weapon-firearms.md`. Draw from idle is one 4-frame clip (bow held
  in both hands). A -> B is an **instant cut**: in-betweens there slide the arrow forward on the string or leave it
  half-released. Damage and the streak fire on B (mark that frame as the hit).
- **Ceremonial / kyudo.** Ready -> nock -> raise -> draw -> full draw (long hold) -> release -> follow-through, with
  the optional calm timing from `style-examples.md`. Hokusai's kneeling shot is the same stages with `kneeling on his back knee,
  front knee up` held in every key pose.
- **Reload loop (repeated shots).** Follow-through -> nock pose -> full draw. The arrow moves from the quiver to the
  string, so step that frame (`key-pose-animation.md`); don't interpolate it.
- **Upward shot (at a flyer).** `leaning back from the hips, bow arm raised up and to the right at 45 degrees,
  arrow pointing to the upper right`. Needs head room: add ~60 px above the 192x256 canvas or shrink the hero.
- **Downward shot (from a ledge).** `leaning forward over the front knee, bow arm angled down and to the right,
  arrow pointing to the lower right`; the streak runs diagonally down. Needs room below the feet.
- **Action variants (silhouette and action-pose sheets), all the same draw with a changed body:** kneeling draw
  (`back knee on the ground, front knee up`), low crouch draw, running draw (mid-stride, torso still square to the
  aim), airborne draw (`knees tucked, both feet off the ground`, bow upright), canted bow (`bow tilted about 30
  degrees off vertical, top tip leaning right`, a quick-shot look). Keep the arms and arrow line identical to the
  standing full draw and only edit the legs; that is a cheap way to get 4 shot poses from one base.
- **Sky raise -> draw (flourish).** `bow arm straight up, arrow pointing straight up, string hand at his chin` ->
  lower the bow arm to the right into the full draw. Two stepped key poses; a charge-up shot or a volley skill.
- **Foot draw (cartoon flourish only).** Standing on one leg, the bow held by the raised foot and the string drawn
  with both hands, arrow pointing up. Fun for a jester or monk archer; stepped key poses, tall canvas.
- **Mounted.** Forward: the horse runs right and the rider draws as standing, bow tilted a little. Backward shot:
  `horse galloping right while he twists his torso back over its rump, bow arm reaching to the left, drawing elbow
  pointing right`. That flips the shot direction: the streak runs left and the trail script needs a mirrored path.
- **The arrow streak.** Start it at the arrowhead's full-draw position (the bow hand), never at the string hand, and
  run it straight right at arrow height to the canvas edge: `blade_trail.py` with a 2-point `--path`, thin
  `--thick` (2-3), on the release frame only. No muzzle flash for a plain bow; a magic bow gets a small
  `vfx_workbench` flash at the bow hand, colour named. The arrow's hit on the target is a separate strike.
- **Canvas.** A European full draw reaches ~50-60 px right of the chest on a 100 px hero; 192x200 holds it. The
  kyudo raise and the upward shot need the tall canvas; a thumb draw needs ~20 px more on the LEFT for the elbow.

## Frame rhythm (from the two CC0 sprite sets)
- **Tiny pixel archer, 5 frames:** idle -> bow raised with an arrow -> 2 frames of draw -> release. No hold frame;
  on release the arrow is already a long streak in front of the bow hand and the bow tips over. Draw = 2 of 5.
- **Painted archer, 22 frames (11 shown):** ~3 shown frames reaching to the hip quiver and nocking with the bow low,
  a fast raise-and-draw, full draw held 2, **one** release frame (string straight, bow upright, hand flung open
  back), then ~3 lowering back to idle. The arrow is never visible (front view): the string carries the read.
- Takeaway: the draw is short, the full draw is held, the release is one frame, the settle is the longest part.
  A hero shot: idle 60 ms, draw clip 4 x 60-80 ms, full draw 220-260 ms, release 60 ms, follow-through 200 ms, back.

## Pitfalls to name in prompts
- **String vanishes or goes slack mid-draw**: `a taut thin bowstring from the top tip to his hand and down to the
  bottom tip` in every drawn pose; `string straight between the tips` in ready and release poses.
- **Arrow on the wrong side**: `the arrowhead just past his bow hand on the right, the shaft running back to his
  jaw`. Fix a small miss with `pixelart_workbench` lines, not a re-roll.
- **Arrow floats off the string**: `the back end of the arrow sits on the string between his fingers`.
- **Bow flips** (string on the right, limbs bending toward him): `the bow bulges toward the right, the string on the
  body side`. Check each in-between at 3x; a flip in one frame reads as a flicker.
- **Second arrow**: after the release the generator keeps an arrow on the string, and with the streak that makes two.
  Say `no arrow on the bow, his string hand empty and open`, and `the quiver arrows stay in the quiver`.
- **Follow-through bow flies away**: if the loose-bow follow-through is used, name the wrist strap, or the bow is
  read as dropped.
- **Kneeling / airborne variants change the arms**: say `arms and arrow exactly as in the original, only the legs
  change`.
- **Mirrored archer** (bow in the near hand): name the far left hand for the bow (see top).
- **Bottom limb through the leg**: `lower limb curving down in front of his thigh, never crossing the leg`; prevent it
  in the base sprite (`key-pose-animation.md`).
