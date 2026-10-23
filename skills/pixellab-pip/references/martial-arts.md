# Martial arts (punches, kicks, blocks, throws, grapples, kata) as visible poses

Facing right throughout: the right hand, right foot and right side are NEAR the viewer.

## Contents
- [What every unarmed pose keeps](#what-every-unarmed-pose-keeps)
- [Stances and guards](#stances-and-guards)
- [Moves as animations (key pose A -> key pose B, effect in screen terms)](#moves-as-animations-key-pose-a---key-pose-b-effect-in-screen-terms)
- [Two-character moves (throws, takedowns) on a single sprite](#two-character-moves-throws-takedowns-on-a-single-sprite)
- [Kata (diagram sheets)](#kata-diagram-sheets)
- [Canvas notes](#canvas-notes)
- [Frame rhythm (photos and sprite sheets)](#frame-rhythm-photos-and-sprite-sheets)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every unarmed pose keeps
- **Near and far limbs, named every time.** A right-facing fighter in an orthodox stance leads with his LEFT foot
  and LEFT hand, which are the FAR limbs: `left foot forward, his left fist forward, partly behind his body`. The
  rear hand and rear leg are near: `his right fist by his chin, nearest to the viewer`. So a jab is the far arm, a
  cross is the near arm crossing in front of his chest, a rear-leg kick is the near leg. Say which, in every pose:
  the generator swaps arms between poses.
- **Fists stay fists.** `both hands closed into tight fists` (or `open hands, fingers together, knife-hand` for
  karate blocks). Wide poses turn fists into open claws or extra fingers.
- **Guard hand home.** Whatever one hand does, the other stays up by the chin: `the other fist stays up guarding
  his chin`. In every photo the non-striking hand is at the face or pulled back to the hip, never dangling.
- **Chin down, eyes on the target.** Muybridge and the boxing guide fighters tuck the chin behind the lead shoulder
  on every blow.
- **Two limbs each.** Kicks and spins grow a third leg or arm: `two legs, two arms`, check every frame at 3x.

## Stances and guards
| Stance | Visible description for the prompt | Use |
|---|---|---|
| Boxing guard | `side-on, left foot forward, knees soft, left fist forward at shoulder height, right fist by his chin, elbows in` | idle, punch start |
| Old-school guard | `left arm almost straight forward at chest height, right fist low across his stomach, upright torso` | vintage boxer idle |
| Cover block | `both forearms up in front of his face, fists at his forehead, elbows together, chin tucked, knees bent` | block hold (the sprite's block row) |
| Open-hand guard | `hands open and raised near his face, palms forward, elbows close to his ribs` | brawler / military idle |
| Front stance | `long stride, front knee bent over the toes, back leg straight, one fist forward, the other fist chambered at his hip, knuckles up` | karate punch start and finish |
| Back stance | `weight on the bent back leg, front leg light and forward, hands in knife-hand guard, the front hand forward, the back hand at his chest` | karate defensive idle |
| Horse stance | `feet very wide, both knees deeply bent, back straight` | kata, rooted pose; in side view it looks narrow, say `seen from the side, feet far apart` |
| Crane stance | `standing on one leg, the other knee raised high, both fists up` | kick chamber, kata pause |
| Wrestling crouch | `low crouch, torso bent forward, both arms reaching forward with open hands, feet wide` | grapple and takedown start |

## Moves as animations (key pose A -> key pose B, effect in screen terms)
- **Jab (far arm):** A = boxing guard -> B = `left arm fully straight forward at chin height, fist knuckles first,
  left shoulder up against his chin, right fist still by his face, small step forward with the left foot`.
  Impact: small `hit_star` at the fist. Interpolates.
- **Cross (near arm):** A = guard, right fist cocked by the ear, right shoulder back -> B = `right arm fully straight
  forward across his chest, hips and shoulders turned toward the right, right heel lifted, left fist back by his
  chin`. Muybridge shows the torso folding forward over the front knee on a full cross. Impact: `hit_star` +
  short streaks behind the fist, never along the arm. Interpolates.
- **Hook:** A = guard, near elbow out at shoulder height -> B = `right arm bent at a right angle, level at head
  height, the fist swinging in from the side, torso twisted toward the right`. The corkscrew version turns the fist
  thumb-down at the end. Stepped: in-betweens straighten the arm into a cross. Trail: short flat arc.
- **Uppercut / body blow:** A = `knees dipped, fist dropped low beside his hip` -> B = `fist driven up in front of
  his chest or chin, elbow bent and below the fist, knees straightening`. The sprite dips for three frames first.
  Interpolates.
- **Front kick / knee kick:** A = guard -> chamber `near knee raised to waist height, foot hanging under the knee`
  -> B = `leg straight forward at waist height, foot flat or heel first, leaning back slightly, arms up`.
  The FM knee kick drives the sole into the shin or knee, the leg angled down. Interpolates from chamber to
  extension, not from the floor: always key the chamber.
- **Side kick:** A = chamber `knee pulled up across his body, foot by the other knee, torso turned side-on` -> B =
  `leg straight out to the right at chest height, heel first, toes pointing down, torso leaning away to the left,
  arms tucked`. The FM version first steps the back foot behind the front one. Stepped (the body turns).
- **Roundhouse kick:** A = guard -> chamber `near knee raised and turned level, pointing at the target, the standing
  foot pivoted, toes pointing back` -> B = `leg straight out to the right at head or rib height, shin and instep
  first, torso leaning back to the left, the far arm thrown down for balance`. The combo sheet holds B for two
  frames and leans further back on the second. Stepped; the in-betweens bend the knee the wrong way.
- **Spin (back) kick:** A = guard -> turn `back turned toward the target, looking over his shoulder` -> B = `leg
  straight out behind him toward the right, heel first, torso low, looking past his shoulder`. Stepped; the
  generator ends the spin facing left. Key the turn pose and end with a pose that states `facing right`.
- **Flying kick:** see `key-pose-animation.md` (takeoff, chamber, kick, land, speed lines behind).
- **Knee strike:** A = `both hands up at head height as if gripping a neck` -> B = `near knee driven up and forward
  to chest height, hands pulled down to meet it, hips forward`. Impact: `hit_star` close to the body. Interpolates.
- **Block / parry / duck (boxing guide):** parry = `open glove pushing sideways across his face`; low parry =
  `forearm swept down and across his stomach`; slip = `head moved to the side outside the incoming arm, torso
  leaning`; duck = `bent forward at the waist, head below shoulder height, fists by his face`. idle -> pose (hold
  ~200 ms) -> idle. Effect: a small pale impact ring on the forearm, not sparks (no metal).
- **Grab:** A = wrestling crouch -> B = `long lunge forward, both arms reaching out at shoulder height, hands
  closed as if gripping cloth, nothing in his hands`. The grab sheet uses the same 4-frame lunge entry for every
  variant, a dust puff at the back foot, and impact ticks on the contact frame.

## Two-character moves (throws, takedowns) on a single sprite
The references always show both bodies; the sprite draws only the thrower. Never describe the enemy in the prompt
(a second figure appears): describe the empty grip, `hands closed at shoulder height in front of him, as if
holding someone`. Move the enemy sprite by code (tween position and rotation) or swap it to its own `knocked
down` pose on the slam frame.
- **Hip / shoulder throw, as drawn:** grip collar and sleeve -> step in and pivot, back against the opponent, hips
  under his -> pull him over the hip or shoulder -> he lands in front. The thrower faces LEFT mid-move, which a
  right-facing sprite can't hold. Cheat that reads in 2D (the grab sheet does it): A = grip pose -> B = `lifting
  with both arms, hands above his near shoulder, back arched, knees bent` -> C = `bent forward low, arms swept down
  to the ground behind him on the left`. The enemy arcs over his head and lands behind him. Stepped, three keys.
  Slam: `crater_dust` or `debris_burst` at ground level where the enemy lands + a short screen shake.
- **Takedown (Muybridge):** collar tie -> arms around the waist -> drive forward and down -> both on the ground,
  top man on his knees. Sprite: A = `low lunge, both arms wrapped around an empty space at waist height` -> B = `down
  on one knee, arms pressed down at ground level in front, head low`. Dust puff at the knee.

## Kata (diagram sheets)
The kata diagrams are numbered held poses joined by a footwork line: stance + block or strike, held, then a fast
change. Use them for skill poses, a charge-up or a victory pose: each step is its own key pose, snap 1-2 frames
between, hold 3-4. Useful kata-only poses: `both open hands raised above his forehead, fingertips and thumbs
touching in a triangle`; `fists crossed at the wrists in front of his chest`; `rising block, forearm angled above
his forehead`; `downward block, fist swept down past his front knee`. Stepped, never interpolated.

## Canvas notes
- A straight punch with a lunge reaches about 0.6 x body height in front; a head-height roundhouse or side kick
  about half a body height in front plus a torso lean behind; a spin kick swings the leg behind first. The grab
  throw lifts the hands a head above the head. Pad more on the right for punches and kicks, above for throws.
- Untested estimate: the 256x256 greataxe canvas in [weapon-axe.md](weapon-axe.md) (hero ~100x200 at x≈72, y=56) fits these too.
  If a foot is clipped at the edge, the generator shortens the leg to fit: pad first.

## Frame rhythm (photos and sprite sheets)
- **Muybridge cross, 12 photos:** 2 guard -> 1 cock (fist by the ear) -> 1 strike -> 4 held at full reach while the
  torso keeps folding forward -> 4 pulling back to guard. The jab plate is the same with one fewer cock frame and a
  deeper overshoot. Fast out, long held reach, slow return.
- **Sprite jab and uppercut, 8 frames:** 3 small anticipation frames (body shifts, fist dips), 1 strike frame, 3
  held, 1 return. Block: 5 frames held with a slight bob, loopable.
- **Kick combo, 9 drawings:** guard -> jab -> closing step -> knee chamber -> kick -> kick held, leaning further ->
  leg drops crossing in front -> turn -> spinning follow-up. The chamber is always its own frame.
- **Spin kick concepts:** 5-7 frames per full turn, the leg extends only on the last third of the turn.
- **Wrestling takedown, 12 photos:** 2 approach, 1 clinch, 1 drive, 2 falling, 6 ground control. For a game
  move keep the first 6 and cut to the enemy's down pose.
- **Grab sheet:** 4-frame lunge -> 1 contact with impact ticks -> 2-3 lift and swing frames -> 1 finish hold.

## Pitfalls to name in prompts
- Jab thrown with the near arm, or arms swapping between poses -> name `his left (far) arm` / `his right (near) arm`.
- Fists open into claws -> `both hands closed into tight fists` in every pose.
- Kick drawn straight from the floor, reading as a sweep -> key the chamber: `knee raised first, foot under the knee`.
- Third leg or arm in kicks and spins -> `two legs, two arms`; check every in-between at 3x.
- Standing leg straight and stiff, or the foot sliding -> `standing knee slightly bent, standing foot flat on the
  ground in the same place`.
- Spin ends facing left -> state `facing right` in the end pose; key the back-turned frame.
- Grip poses grow a weapon or a cloth bundle -> `empty hands, nothing in his hands, as if gripping cloth`.
- Mentioning the opponent adds a second figure -> describe heights (`at chin height in front of him`), never a person.
- Speed lines painted along the limb read as a blade -> streaks behind the fist or body only (as in `key-pose-animation.md`).
