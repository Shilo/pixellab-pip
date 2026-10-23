# War hammer (one-handed hammer, two-handed war hammer and maul, sledgehammer) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Facing right throughout: right hand, right foot and the near side face the viewer. Pollaxe guards and the shared
Mordaxt binds are in [weapon-axe.md](weapon-axe.md); the one-handed raise and the shield are in
[weapon-mace.md](weapon-mace.md).

## What every hammer pose keeps
- **The face points where the blow lands.** On a downward hit the flat striking face points `toward the lower
  right of the image, flat face down on the target`; on a side swing it points `toward the right side of the
  image`. A war hammer has a back spike or pick opposite the face: name both, `flat hammer face forward, pick
  spike pointing back`, or the generator swaps them (or turns the head into an axe blade).
- **The head is a block, not a ball.** Say `a heavy rectangular steel hammer head, same size as in the original`
  in every key pose. In the sketch sheets the head stays a crisp box from every angle; generators round it into a
  mace or shrink it on turned frames.
- **Weight shows in the body, not the arms.** In all three Muybridge plates the sledge falls with the arms nearly
  straight and the torso folds after it; nobody muscles it with bent elbows. Say `arms long and straight, the
  hammer's weight pulling his body forward and down`.
- **Exactly one hammer, straight haft.** `holding one hammer, straight rigid haft, as long as in the original`.

## Grips, what to draw
| Weapon | Visible description for the prompt |
|---|---|
| Hand hammer, one hand | `right hand gripping near the end of the short handle, hammer head above the fist, left arm forward or holding a shield` |
| Sledge / maul, two hands at rest | `both hands near the butt end of the long haft, the hammer head resting on the ground in front of his front foot, haft slanting up to his hands` |
| Maul across the shoulders | `haft lying across the back of his shoulders behind his neck, both wrists hooked over it, hammer head out past his right shoulder` |
| Maul on one shoulder (carry) | `haft resting on his right shoulder, right hand near the butt in front of his chest, hammer head up behind his back` |
| War hammer / Mordaxt, two hands | `hands about a shoulder-width apart on a haft as tall as his chest, hammer head at the top, butt spike at the bottom` |
The sledge photos show the front hand **sliding**: spread up the haft while lifting, slid down to meet the back
hand at the butt for the fall, so the head travels the widest arc. Draw the top of the wind-up and the hit with
the hands together at the end; draw guards and blocks with the hands apart (as on the Mordaxt, [weapon-axe.md](weapon-axe.md)).

## Moves as animations (key pose A -> key pose B, trail and effect in screen terms)
- **Overhead smash (two hands):** A = `both arms straight up, hands together at the butt, haft upright or
  slanting back, hammer head high behind his head`, torso arched, weight on the back foot -> B = `bent forward over
  the front knee, arms straight down in front, hammer head on the ground ahead of his front foot, flat face down`.
  Trail: a tall half-circle from behind the head, over the top, down in front, widest at the top. Impact:
  `crater_dust` + `shockwave_ring` at floor level, `debris_burst` of chips and a short ground crack (the sketch
  sheet sprays rubble both ways from the head), `hit_star` only if it lands on a body. Interpolates if both poses
  name the face direction.
- **Full-circle sledge (the forge swing):** the photos never lift the sledge straight up from rest. It hangs by
  the shins -> swings back low past the back knee -> rises behind at shoulder height, level -> comes up over the
  head -> falls. For a heavy hero use this as a 4-key-pose wind-up (stepped, not interpolated: the generator
  shortcuts the loop through the front of the body). Trail only on the falling half.
- **One-handed hammer blow:** A = `right elbow raised beside his head, forearm up, hammer head above and behind his
  head` -> B = `forearm swung down in front, fist at chest height, hammer head below the fist, face toward the lower
  right`. Short arc from the elbow and wrist, the body barely moves; it rebounds straight back up. Small `hit_star`.
- **Side swing (level):** A = `haft held level behind him at shoulder height, hammer head far behind his back,
  torso twisted away, long lunge` -> B = `both arms straight out to the right at chest height, haft level, hammer
  head at full reach, face toward the right side of the image, back heel lifted`. Trail: one flat ellipse at
  chest height, `swing_slash`; `hit_star` + a `debris_burst` of armour bits at the head on contact. A rising
  variant ends with the head up in front; a low variant drags the head along the floor first (sketch sheet).
- **Leap smash:** A = coiled lunge, hammer level behind at shoulder height -> B = take-off, front knee up, hammer
  rising behind the head -> C = apex, back arched, `hammer horizontal behind his head, head behind his left
  shoulder` -> D = falling, hammer coming over the top -> E = landing crouch, `hammer head on the ground in front,
  flat face down` -> F = settle low, free arm out. Five or six stepped key poses; never A -> E in one clip. Impact
  on E: `crater_dust` + `shockwave_ring` + `debris_burst`, the biggest of the set; a one-frame screen shake suits.
  Same take-off pitfall as [weapon-axe.md](weapon-axe.md) -> "Jump take-off".
- **Hook / takedown (Mordaxt pick):** A = `haft reaching forward, the back spike hooked behind the enemy's neck or
  knee` -> B = `haft pulled back to his right hip, leaning back`. The 1467 plates finish by stepping in and throwing
  the enemy over the hip, and push an elbow from behind with the haft upright. Hold A 2 frames, snap to B; no trail.
- **Haft block:** `haft held level above his head, hands wide apart, hammer head to the left` (Thott 148/151) or
  `haft upright in front of him`. idle -> block (hold ~200 ms) -> idle, `spark_burst` where the weapons meet.
- **Spike thrust:** A = haft drawn back at the hip, hands apart -> B = `deep lunge, both arms forward, haft level at
  waist or face height, top spike aimed straight ahead toward the right`. Trail: `thrust_streak`, no crescent. In
  Thott 149/151 the thrust goes at the face from the high hold too: A = haft overhead -> B = haft driven down and
  forward. Stepped; the generator turns it into a smash otherwise.

## Canvas notes
- A maul at the top of the wind-up reaches about a full haft-length above the head; the leap apex reaches higher
  still and the low drag reaches past the front foot. Pad top and both sides before posing; a clipped head makes
  the generator shorten the haft. Starting point: the greataxe canvas in [weapon-axe.md](weapon-axe.md) (256x256 for a ~100x200 hero),
  plus more top room for the leap. Hand hammers need little padding.

## Frame rhythm (Muybridge plates and the leap sketches)
- **Two-handed sledge, 12 photos (376):** 1 cocked over the shoulder, 2 frames held at the top with arms straight
  up, 1 frame starting the fall, 1 frame mid-fall, ONE contact frame bent forward with the head low, 2 frames still
  pressed on the target, then 4 slow recovery frames with the head sinking to hang by the shins.
- **Sledge loop, 6 photos (377):** hanging -> swung back low -> level behind -> over the head -> top -> fall. The
  hand hammer beside it lands two to three quick taps per sledge blow: light hammer = fast, short, repeated.
- **One-handed hammer, 6 photos (374):** 2 frames rising, 1 at the top, 1 fast falling, 1 contact, 1 rebound up.
- **Leap smash, 6 sketches:** coil, take-off, apex, fall, impact, settle. For game timing: hold the apex 2 frames,
  one fall frame, hold the impact 2-3 frames with the effect (the timing in `key-pose-animation.md`).

## Pitfalls to name in prompts
- Head turns into an axe blade or a mace ball -> `rectangular steel hammer head, flat striking face` every pose.
- Face and spike swap sides between poses -> state the face direction in screen terms in each key pose.
- Head shrinks on turned frames -> `same size as in the original`; check each in-between at 3x.
- Bent-elbow chopping instead of a heavy fall -> `arms straight, the hammer's weight pulling him down`.
- Wind-up loop cut through the front of the body -> stepped key poses with the hammer behind him named.
- Haft bends on wide arcs -> `straight rigid haft`. Back hand drops off a maul -> `both hands on the haft`.
- Impact effect painted over the head so the hammer vanishes on the hit frame -> see [weapon-axe.md](weapon-axe.md) "fast frames".
