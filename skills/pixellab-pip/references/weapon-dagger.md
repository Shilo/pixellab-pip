# Dagger and knife (one-handed, forward and reverse grip) as visible poses

Facing right throughout: right hand, right foot and the near side face the viewer. The dagger is in the right hand
unless the prompt says otherwise.

## What every dagger pose keeps
- **Name the grip in every prompt.** Forward (hammer) grip: `dagger held in his right fist with the blade sticking
  out past his thumb, point forward`. Reverse (ice-pick) grip: `dagger held in his right fist with the blade
  sticking out below his little finger, point down`. Every overhand stab in the manuscripts is reverse grip; every
  underhand stab and every modern slash is forward grip. Unnamed, the generator picks one per frame.
- **Low, bent, close.** The modern stance is a crouch: `knees bent, torso leaning forward, weight on the balls of
  the feet`, the knife hand low at the near hip close to the body, the empty left hand open across the chest as a
  shield. The manuscript fighters stand taller but with the same long stride as the sword (`long stride, front knee
  bent, back leg straight`).
- **The empty hand works.** In 12 of 15 images the off hand is doing something: catching a wrist, checking a
  forearm, pushing an elbow. Give it a job in every key pose (`left hand open and raised in front of his chest`),
  or Pro Flash drops it to the side and the pose reads as idle.
- **Sheath at idle, empty after the draw.** Worn idle: `dagger sheathed upright on his belt at his right hip, only
  the hilt showing`. After the draw: `an empty sheath on his right hip, the dagger in his right hand` - say both,
  or the generator draws a second dagger in the sheath.
- **Make it bigger than real.** A real blade is about a hand long, 8-12 px on a ~100x250 sprite: it vanishes.
  The manuscripts draw it forearm length and the sprite set draws it a third of the body width; ask for
  `a long dagger, the blade about as long as his forearm`, a bright edge (`a light steel highlight along the blade`)
  and a dark outline around it.

## Guards and ready poses (what to draw)
| Pose | Visible description for the prompt | Use |
|---|---|---|
| Knife fighter's crouch | `crouched, knees bent, dagger low at his right hip pointing forward, left hand open across his chest` | default idle once drawn |
| Concealed ready | `left forearm held across his belly, the dagger hidden low behind it, point forward` | sneaky idle, feint wind-up |
| Low guard, dagger in hand (Fiore) | `wide stance, both hands low in front of his thighs, dagger pointing forward and down` | defensive ready, rising-stab start |
| Overhand raise | `right arm raised straight up, fist above his head, dagger in reverse grip hanging point down behind his fist` | overhand stab wind-up |
| Underhand chamber | `right fist pulled back to his right hip, dagger in forward grip, point aimed forward and slightly up` | underhand stab / gut thrust wind-up |
| Shoulder chamber (sprite) | `right fist at his chest, blade angled up and forward toward the upper right of the image` | quick jab wind-up |

## Moves as animations (key pose A -> key pose B, trail path in screen terms)
- **Overhand stab (reverse grip):** A = overhand raise, torso leaning back slightly, left hand reaching forward ->
  B = `right fist driven down to chest height in front of him, dagger point down and forward toward the lower right
  of the image, torso bent over the front knee`. Trail: a short steep arc from above the head down in front; thin
  `slash_trail` (low width) or `blade_trail.py`. Needs **3 stepped key poses** (raised, fist at shoulder height,
  finish): the in-betweens flip the grip.
- **Underhand stab / gut thrust (forward grip):** A = underhand chamber -> B = `right arm straight out at belly
  height, dagger level pointing right, lunging onto the right foot`. Trail: a straight line, `thrust_streak`;
  no crescent. 4-6 frame interpolation is usually safe here (the blade stays in line); still check the in-betweens.
- **Quick jab x2 (from the sprite set):** shoulder chamber -> `arm straight out at chest height, blade level
  pointing right` -> chamber -> extended. Two poses alternated, no in-betweens; a tiny `thrust_streak` on each
  extended frame.
- **Diagonal slash, high to low (angle 1 / 2 on the chart):** A = `dagger raised beside his right ear, point back`
  -> B = `arm swept across his body, dagger low near his left hip, point toward the lower left of the image`.
  Trail: a diagonal from the upper right to the lower left in front of the body. Rising version reverses it.
- **Level slash (angle 3 / 4):** A = `right hand drawn back behind his right hip, blade level` -> B = `arm swept
  across his belly, blade level pointing toward the left of the image`. Trail: a flat thin line at belly height.
  Slashes need **stepped** key poses (cocked, across the belly, finish) and one trail through the tips.
- **Thrust-slash combo (FM sequence):** gut thrust -> slash back across at belly height -> rising diagonal.
  Three finishes, each its own key pose; join the trails with `zigzag_slash` or use `cross_slash` for an X.
  A fast flurry on the target: `claw_marks` (3 thin parallel cuts) over the foe instead of trails on the hero.
- **Canvas:** the gut thrust and jab reach forward (give the right side ~40% extra width); the overhand raise adds
  ~15% above the head. Keep `both feet inside the canvas with a margin`.

## Defence and grapple poses (skill / counter material)
- **Wrist catch:** `left hand gripping the attacker's raised wrist above his head, right fist cocked back`. The
  most drawn pose in the folder (Fiore, Talhoffer, Meyer, FM). As a counter: catch -> hold ~200 ms -> strike.
- **Crossed-forearm catch:** `both forearms crossed in an X above his head, catching a downward stab where they
  cross`. A two-dagger fighter does the same with both blades crossed: add `spark_burst` where they meet.
- **Check:** `left forearm pressed against the attacker's knife arm at the elbow, stopping a level slash`.
- **Low parry:** `left hand sweeping down and outward across his body, knocking a low thrust toward the lower
  left of the image, hips turned`.
- **Lock / disarm:** `the attacker's knife arm bent and trapped under his left armpit, his right hand twisting the
  dagger out of the attacker's fist`. Two-character poses don't generate well as one sprite; use it as a solo
  `seize and twist` pose with the foe off-sprite, or as a hit-reaction on the foe.
- A parry is a snap like a hurt: idle -> parry pose (hold ~200 ms) -> idle, one `spark_burst` at the contact.

## Frame rhythm (from a CC0 knife sprite set, ~25 px frames)
- **Attack, 5 frames:** neutral (knife not shown) -> chamber at the chest, blade up-forward, hair flicking back ->
  arm extended, blade level -> chamber -> extended. Hit = the extended frame, held as long as the others: a dagger
  hit is fast and repeats rather than one heavy frame.
- The blade is two tones (a light edge and a mid body) and always outlined; that is what keeps it readable.
- The run frames hold the knife level forward at the waist the whole cycle: in a held-prop loop, keep the blade
  angle fixed and let the body move.
- For skill moves use the timing in `key-pose-animation.md` (wind-up hold, one fast hit frame, settle);
  for basic attacks the sprite set's quicker two-hit jab reads better for a dagger.

## Pitfalls to name in prompts
- Blade vanishes in mid-swing or shrinks to a fist -> `a long dagger, blade as long as his forearm, light steel
  highlight, dark outline`, and step key poses instead of interpolating.
- Grip flips between frames -> name forward or reverse grip in every key pose and in-between prompt.
- A second knife appears (in the sheath or the empty hand) -> `ONE dagger, in his right hand only; an empty sheath
  on his right hip; left hand empty and open`.
- The empty hand hangs and the pose reads as idle -> give the left hand a job (raised, catching, across the chest).
- The thrust's in-betweens raise the blade overhead -> 6-frame swing or stepped poses + `thrust_streak`.
- Dagger throw: no reference in this folder; see `key-pose-animation.md` (wind-up behind the head, arm extended after).
