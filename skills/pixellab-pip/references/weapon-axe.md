# Axe (one-handed hatchet, two-handed pollaxe, halberd) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Facing right throughout: right hand, right foot and the near side face the viewer. Axe throws are not covered here.

## Contents
- [What every axe pose keeps](#what-every-axe-pose-keeps)
- [Grips, what to draw](#grips-what-to-draw)
- [Pollaxe guards (Fiore's six, plus Talhoffer)](#pollaxe-guards-fiores-six-plus-talhoffer)
- [Moves as animations (key pose A -> key pose B, effect in screen terms)](#moves-as-animations-key-pose-a---key-pose-b-effect-in-screen-terms)
- [Canvas notes](#canvas-notes)
- [Frame rhythm (Muybridge photos and the axe sprite)](#frame-rhythm-muybridge-photos-and-the-axe-sprite)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every axe pose keeps
- **The edge faces where the blow goes.** On the hit frame of a downward chop the edge faces `toward the lower right
  of the image`; on a side swing it faces `toward the right side of the image`. At the top of a wind-up the edge
  points up and back (`edge facing up, toward the upper left`). The hammer or back spike is always on the opposite
  side of the head from the edge. Name it in every key pose: the generator flips the head between poses.
- **Same head size, same haft length as the idle.** Ask for `the same axe head, same size, the haft as long as in
  the original` in every pose. Pollaxe hafts in the manuscripts run from the ground to about the fighter's eyes;
  a halberd is taller than the fighter.
- **Exactly one axe.** Wide poses and smears grow a second head or a second weapon: say `holding one axe`.
- **Long stride for the pollaxe.** Talhoffer and Fiore fighters stand very wide, front knee bent, back leg straight,
  the back heel lifting on the blow; say `very long stride, feet far apart, front knee bent, back leg straight`.

## Grips, what to draw
| Weapon | Visible description for the prompt |
|---|---|
| Hatchet, one hand | `right hand gripping the end of the short handle, axe head beyond the fist, left arm free and forward for balance` |
| Pollaxe, two hands | `both hands on the long haft about a shoulder-width apart, the right hand in the middle of the haft toward the head, the left hand near the butt end` |
| Pollaxe, raised | `both hands above his head, the haft level or slanting above his head, the axe head behind him and up` |
| Halberd | `both hands wide apart on the long shaft, the left hand forward, the right hand back at his right hip` |
| Halberd, shoulder carry | `shaft sloped over his right shoulder, blade high behind him, butt end down in front, right hand at his chest` |
| Hatchet, at rest | `right arm hanging, axe held low beside his thigh, head down` |
| Two hands at the end (max reach) | `both hands together at the butt end of the haft` for full-reach side swings and ground smashes |
The pick swing photos show the forward hand **sliding** along the haft: near the head during the lift, down next
to the back hand at the top, back up the haft on the impact. Draw the top of the wind-up with hands together.

## Pollaxe guards (Fiore's six, plus Talhoffer)
| Guard | Visible description for the prompt | Use |
|---|---|---|
| Short / low forward | `haft angled down in front, axe head low ahead near his front knee, butt spike up behind his back hand` | defensive ready, rising-blow start |
| Haft across the hips | `haft level at hip height across his body, axe head behind him, butt spike pointing forward` | butt-thrust start, idle |
| High forward | `both hands at head height, haft slanting up and forward, axe head above and in front of him` | top-spike thrust down, overhead start |
| Low tail | `haft slanting across his body, axe head low behind him near the ground` | rising or sweeping blow wind-up |
| Over the shoulder | `haft resting on his right shoulder, axe head up behind his head, butt spike forward and down` | heavy overhead wind-up |
| Overhead roof | `both arms raised, haft level above his head, axe head behind him` | overhead chop wind-up, high block start |
| Planted rest | `axe head resting on the ground beside his right foot, haft upright, his hand on the butt end` | idle, roster portrait |
| Hanging behind the back | `axe over his right shoulder, head hanging down behind his back near his hip, both hands at his shoulder` | deepest overhead wind-up |

## Moves as animations (key pose A -> key pose B, effect in screen terms)
- **Overhead chop (two hands):** A = over the shoulder or roof, torso arched back, head looking at the target ->
  B = torso folded forward over the front knee, arms extended low in front, axe head at knee height, `edge facing
  toward the lower right of the image`. Trail: from above and behind the head, over the top, down in front.
  Impact: `crater_dust` or `debris_burst` at the head + `hit_star`. Interpolates if A and B both state the edge.
- **One-handed chop (hatchet):** A = `right arm raised, elbow up beside his head, axe head above and behind his
  head` -> B = `right arm straight down in front, axe head at waist height, edge toward the lower right`. Short
  stride, left arm forward. Interpolation works; it is a short arc.
- **Diagonal chop:** A = axe head high behind the right shoulder -> B = head low on the far side, `axe head ending
  low toward the lower left of the image, haft across his body`. Step key poses: the in-betweens tend to turn the
  head over. Trail: one diagonal crescent from upper left of the body to lower front.
- **Side swing (level or rising):** A = low tail or haft across the hips, head behind -> B = arms out in front,
  haft level at chest height, `edge facing toward the right side of the image`. Trail: `swing_slash` or
  `slash_trail`, a flat ellipse in front. A rising variant (from the sprite) ends with the head pointing up in front.
- **Spike thrust:** A = haft across the hips or high forward, hands pulled back -> B = both arms forward, haft level
  at chest or neck height, `top spike aimed straight ahead toward the right`, deep lunge. Trail: straight line
  (`thrust_streak`), no crescent. Stepped: the generator likes to lift the head into a chop between them.
- **Hook / pull:** A = haft reaching forward at the neck or leg height of the enemy, `axe head hooked beyond the target`
  -> B = `pulling the haft back to his right hip, leaning back, front knee bent`. Hold A for 2 frames, then snap.
  The references show the haft behind a leg and hafts locked at the heads; no crisp edge-hook was drawn.
- **Haft block:** `haft held upright in front of him, hands far apart, axe head at the top` or `haft level above
  his head, hands wide`. The enemy blow meets the haft between the hands. idle -> block (hold ~200 ms) -> idle,
  `spark_burst` where the weapons meet.
- **Stand -> raise -> smash -> recover (4 keys, two hands):** A = `axe held upright in front of him, head up by
  his left shoulder` -> B = `axe lifted high, the head turned so the edge faces forward, back foot stepping wider`
  -> C = `leaning forward, axe swung down to the ground in front, head at foot level, edge toward the lower right`
  -> D = `crouched, haft pulled back up upright in front of his right shoulder`. D doubles as the next ready, so it
  loops. Name the edge turn in B; it is where the head flips.
- **Full-reach side swing:** A = `torso twisted away, both hands at the butt end over his back shoulder, axe head
  behind his head` -> B = `arms straight out in front at shoulder height, arms and haft in one straight line, axe
  head far toward the right, edge facing right`. Trail: a wide flat ellipse; needs the most room on the right.
- **Ground smash with follow-through:** after the hit frame the body keeps going: `folded low over the haft, axe
  head on the ground ahead, back heel lifted`, hold 3 frames. A one-handed side swing ends the same way with the
  axe trailing low behind him.
- **Halberd over-the-top arc:** A = `shaft upright, blade straight above his head` -> B = `shaft level far in front
  at waist height, blade toward the right` -> C = `blade on the ground a full shaft length ahead`. Trail: a quarter
  circle from the top over to the ground on the right. Untested on canvas: a halberd at hero size likely overflows
  256 px here, so shorten the shaft or end the clip at B.
- **Halberd raise -> thrust:** A = `both hands high, shaft slanting up behind him, blade far above and behind` ->
  B = level forward thrust (as the spike thrust). Straight `thrust_streak`, stepped.

## Canvas notes
- A raised pollaxe reaches about one haft-length above the shoulders; the low tail reaches behind the heels. Pad
  to roughly 2.0 x the sprite width and 1.4 x its height for a 100x250 hero, more room on the
  left for wind-ups and on the right for thrusts and side swings. A hatchet needs only modest padding above.
- If the head is clipped at the canvas edge in a pose, the generator shortens the haft to fit: pad first.
- Tested canvas for a two-handed greataxe on a ~100x200 hero (tested): **256x256, sprite at
  x≈72, y=56** - room behind for the over-the-shoulder wind-up and in front for the hit. A 192x256 canvas leaves
  24 px behind: too little. 256x256 takes at most 8 generated frames per clip (`frame_count` 8 = 9 frames with
  the key poses); for more, splice two clips that share a frame.

## Frame rhythm (Muybridge photos and the axe sprite)
- **Hatchet chop, 10 photos:** 6 frames lifting (slow, the head rising past the ear to behind the head) -> ONE
  strike frame -> 3 frames held on contact. Heavy weapon = long lift, one hit, a held landing.
- **Two-handed pick, 12 photos:** 4 frames lift, 2-3 frames at the top with the torso arched back (the hold), 1
  frame mid-fall, 1 impact frame bent double, 2 frames pulling the head back out.
- **Sprite swing, 6 frames:** ready (axe trailing behind the hip) -> 2 coil frames low -> low sweep with the trail
  at foot level -> hit with the arm straight forward and a full crescent -> overshoot upward. Fast; for a heavy
  feel add 2 wind-up hold frames and 2-3 settle frames (the timing in `key-pose-animation.md`).
## Pitfalls to name in prompts
- Head flips so the edge faces backward -> state the edge direction in screen terms in every key pose.
- Head shrinks or turns into a spear point in wide poses -> `the same large axe head, same size as in the original`.
- Haft length changes between poses -> `the haft as long as in the original`; pad the canvas before posing.
- A second axe or a second head appears -> `holding one axe`, check every in-between at 3x.
- Left hand drops off a pollaxe -> `both hands on the haft`; for the hatchet say the left hand is empty.
- **The fast frames lose the head** (8-frame chop): the generator painted its flash over the axe head on frames
  2-4, so `scrub.py` left a bare haft; the clip also reached the hit by frame 5 and repeated it four times. Fix
  that worked: keep frames 1 to the first hit, splice a 6-frame clip from there with the action `the same large
  steel axe head stays solid and fully visible in every frame`, and set `--hit` to the real contact frame.
- **Jump take-off**: crouch (axe low behind) -> apex (axe overhead) swung the axe through the front of the body in
  two takes, even with the path in the action. Pick frames across the takes, or add a key pose with the axe
  behind the back at shoulder height between them.
