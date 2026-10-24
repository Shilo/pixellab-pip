# Katana (kendo cuts, iai draw details, katana sprite rhythm) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Key-pose production is optional under `key-pose-animation.md`; the basic kamae and draw cycles are below. Facing right throughout:
right hand, right foot and the near side face the viewer. The scabbard is on the LEFT (far) hip, its end sticking out
behind toward the left of the image.

## Contents
- [What every katana pose keeps](#what-every-katana-pose-keeps)
- [Kendo cuts as animations (key pose A -> key pose B, trail path in screen terms)](#kendo-cuts-as-animations-key-pose-a---key-pose-b-trail-path-in-screen-terms)
- [Other moves the sources show](#other-moves-the-sources-show)
- [More kamae from the 15-pose chart (additional guards)](#more-kamae-from-the-15-pose-chart-additional-guards)
- [Combo strips (ink-silhouette sheet, read as game key poses)](#combo-strips-ink-silhouette-sheet-read-as-game-key-poses)
- [Frame rhythm from three katana sprite sets](#frame-rhythm-from-three-katana-sprite-sets)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every katana pose keeps
- **Right hand at the guard, left hand at the pommel end**, a gap between them, in every two-handed frame. Both
  manuals show the left fist low and centred; the right hand does the steering. Say `right hand just below the
  guard, left hand at the end of the hilt`.
- **Short, sliding feet.** Kendo and kata fighters keep the near right foot forward, feet a little over shoulder
  width, back heel lifted. The cut lands with a stamp-step of the front foot and the back foot dragged after it,
  not a passing step: `steps in on the near right foot, far left foot slides up behind`.
- **Scabbard stays in the sash** in every bare-blade frame: `empty scabbard still through the sash at his far left
  hip, end pointing back toward the left of the image`. The generator deletes it once the blade is out.
- **Curve:** `curved single-edged blade, edge facing forward and down`; at the hit frame the edge faces the target.

## Kendo cuts as animations (key pose A -> key pose B, trail path in screen terms)
All four start from chudan and step in on the hit. Canvas: the raise puts the blade above the head (192x256 or
256x256); the extended hit frames reach far forward (256 wide).
- **Men (head cut):** A = full raise, `both arms straight up above his head, blade level behind his head pointing
  back toward the left of the image` (the school manual's big practice raise; jodan's 45-degree tilt is the short
  version) -> B = `both arms straight out at shoulder height, blade pointing forward and slightly down, tip at head
  height in front of him, near right foot stamped forward`. Trail: a half circle from behind the head, over the top,
  down to head height in front. Left/right men: same, but B ends with `blade slanting 45 degrees down toward the
  lower right`, the trail a shorter diagonal arc.
- **Kote (wrist cut):** A = chudan with the hands lifted only to chin height, `blade raised to about 45 degrees` ->
  B = `arms extended at chest height, blade level and pointing forward, tip slightly down`. The smallest arc of the
  four; trail: a short arc in front of the chest. Don't let it become a full overhead cut: say `small lift, hands
  never above his head`.
- **Do (side cut):** A = full raise as for men -> B = `arms extended in front of his belly, wrists turned, blade
  level at waist height sweeping across in front of him toward the left of the image`. Trail: a curve from above
  the head down to waist height, then flattening into a level line (flattened `blade_trail.py` path or
  `vfx_workbench` `swing_slash`). Torso leans slightly forward, no deep lunge.
- **Tsuki (throat thrust):** A = chudan -> B = `both arms pushed straight forward at chest height, hands turned
  inward with the knuckles on top, blade level, tip forward at throat height, weight on the near right foot`. No
  wind-up arc; trail = `thrust_streak`. Name `no raise` or the in-betweens lift the blade overhead.

## Other moves the sources show
- **Chudan -> jodan, the long way (kata salute / charge-up skill):** the hands open, the arms swing out to both
  sides in a wide circle and rejoin above the head, ending `both hands above his head, blade level over his head`.
  One hand holds the sword out low to the side mid-circle: generate that frame as its own pose, the interpolator
  drops the sword. Read it as a 3-key-pose flourish: chudan -> arms spread -> overhead.
- **Hasso from jodan:** `hilt lowered to beside his right cheek, blade tilted back about 30 degrees from upright,
  far left forearm across in front of his chin`. The kata show it as the answer to an opponent who drops to a low
  side guard (`hilt at his right hip, blade pointing forward and down at the ground`).
- **Standing draw:** the right hand crosses to the far hip, then `right elbow raised to shoulder height, blade
  sliding out horizontally across his chest`; next key pose = one-armed raise (below). Stepped key poses: the blade
  leaves the scabbard, so never interpolate idle -> drawn.
- **Defence against a head cut:** `both hands raised above his head, blade slanting down and forward across the
  top of his head toward the attacker`, the attacker's blade sliding off it near the guard; feet step to one side.
  Follow-up key pose: `blade straight up above his head, both hands at the forehead` (counter-raise), then a men cut.
  The kendo receiver's simpler block: `hands at chest height, blade held upright beside his head`.
- **Iai photo sequence (rear view, 15 frames):** sit -> rise to one knee as the arm shoots out sideways at shoulder
  height (held across 4 frames: the draw-cut is the longest pose) -> arm back, blade at the side -> second draw ->
  both hands straight up, blade vertical -> kneel, blade down at the side -> arm out (the flick) -> sheathe. For a
  game: draw-cut hold 3-4 frames, raise 1, cut 1, settle 2.

## More kamae from the 15-pose chart (additional guards)
| Guard | Visible description for the prompt | Use |
|---|---|---|
| In (upright at the shoulder) | `blade straight up in front of his near right shoulder, hilt at chest height, both elbows down` | calm ready idle, a narrower hasso |
| Low left / low right | `hilt at his far left hip, blade pointing forward and down across the front` (or the same at the near right hip) | wary counter idle, start of a rising cut |
| Kneeling low right | the low right guard with `deep stance, back knee almost on the ground` | counter crouch, ambush idle |
| Overhead bar (standing or crouched) | `both hands above his head far apart, blade level over his head, pointing back` | catch-block of a head cut, charge-up |
| Hip carry | `hilt at his near right hip, blade level pointing back toward the left of the image, upright stance` | relaxed walk-in, a quieter waki |
| Low trailing | `wide low stance, hilt at his waist, blade pointing down and back behind him near the ground` | dash start, sweeping rising cut wind-up |
| Kasumi variants | high: `wrists crossed above his forehead, blade level over his head pointing forward`; face height: `hands beside his temple, blade level at head height pointing at the enemy` | parry, thrust from the face |
| Angled across (shin) | `hands at the near hip, blade angled up across the front of his body toward the upper right` | between-cuts ready pose |

## Combo strips (ink-silhouette sheet, read as game key poses)
- **Draw-lunge combo (7 keys):** one-hand low carry -> `deep crouch, blade raised upright behind his head, hands at
  his face` -> `low crouch, blade level at chest height pointing back` (chamber) -> long low lunge, `blade extended
  forward and slightly up` (thrust) -> rise, `blade straight up overhead` -> step-in, blade level beside the head
  pointing back -> `low crouch, blade down near the ground ahead`. Trail only on the last cut: a tall crescent from
  above his head sweeping down in front to the ground. A small dust curl at the front foot marks each stamp-step.
- **Dash -> leap -> plunge (5 keys):** `low crouch, blade back over the far shoulder` with a big dust swirl behind
  -> long horizontal dash lunge, blade trailing behind -> landing crouch -> airborne, `knees tucked, both hands above
  his head, blade level pointing back` under a crescent arcing over his head -> `kneeling low, blade driven down in
  front`, a vertical crescent ending in a ground spark spray. Hit = the kneeling frame; give it the impact VFX.
- **Spin chain (6 keys):** horizontal cut, arm extended at shoulder height (flat elliptical trail in front) ->
  rising cut, near hand high to the upper right (upward crescent) -> full turn, `blade level at waist height
  circling around his body` (a ring trail around the hips, passing behind him) -> overhead circle (tall loop trail)
  -> low diagonal finish (trail from upper left down to the lower right) -> hop back away, a splash under the feet.
  Each trail lives on ONE key frame; the poses between have no trail.
- Lesson: big moves read from silhouette alone; the trail is a thick white crescent, tapered at both ends, fattest
  where the blade moves fastest (mid-swing), drawn on the hit frame and gone the next.

## Frame rhythm from three katana sprite sets
- **Cartoon samurai (Segel, large frames, faces left):** idle 10 (breathing only). Attack1, 8 frames: idle -> 2
  wind-up frames lifting the blade upright beside the head -> 1 diagonal down -> 2 frames blade level low across
  the front with a pale smear along the edge -> 2 recovery. Attack2, 8: blade dropped low -> point down in front
  -> 2 rising frames with smear (low to upright) -> 3 recovery. Smear = a faint ghost blade, 1-2 frames.
- **Pixel samurai (cyanglaz, ~64 px, faces right, deep wide crouch):** block 4 = frame 1 a full cyan fan from low
  to upright, the blade then held vertical in front with the guard at chest height, frames 2-3 the fan breaking into
  sparks, frame 4 clean hold. Attack 5 = frame 1 a big pink crescent from low to the raised point, arm extended,
  blade angled up toward the upper right; frames 2-5 hold that pose while the crescent dissolves. No wind-up: the
  smear frame IS the swing. Good model for snappy, low-frame attacks.
- **Tiny 4-direction samurai (sebshady, ~16 px):** 3 attack frames per direction: arms up, blade back over the head
  -> mid swing with a one-pixel ghost line -> blade level forward at waist height. At this size the line is the trail.
- Rule of thumb across all three: wind-up 0-2 frames, hit 1 frame (often the smear frame), hold or recovery 2-4.

## Pitfalls to name in prompts
- Men raise tilts only slightly -> `blade level behind his head` for the big raise.
- Kote and tsuki in-betweens raise the blade overhead -> `small lift` / `no raise`, or stepped key poses.
- Empty scabbard vanishes or ends up on the near hip -> describe it in every bare-blade pose.
- One-handed frames (draw, one-arm raise, salute circle) lose the sword -> generate each as its own key pose.
- Spin cuts: the blade passes behind the body and vanishes or doubles -> step the turn key poses; the trail ring
  passes behind the hips, so draw its back half under the body.
- Kendo armour and bamboo swords in the manuals are props of practice: ask for `steel katana`, never `bamboo sword`.

## Basic kamae and draw cycles

Use a stance name only with its visible description; the generator draws the description, not the term. Grip: right hand just below the guard, left hand near the pommel. Feet shoulder width, one forward, knees slightly bent. A katana is worn through the sash on the left hip (the far side) and drawn by the right hand. Shared sword rhythm: `weapon-sword.md`.

| Kamae | Use | Visible description |
|---|---|---|
| Chudan (middle) | ready, start of a thrust | `both hands on the hilt a fist in front of his navel, blade angled up, tip at the opponent's eye or throat height, near right foot forward` (not "pointing straight forward": that draws it flat) |
| Jodan (high) | overhead-cut wind-up | `both hands raised above his head, left hand about a fist from his forehead, blade angled up and back behind him, far left foot forward` |
| Gedan (low) | counter, wary ready | `blade lowered, tip pointing at the ground ahead, both hands at the hips, near right foot forward` |
| Waki (side) | sideways or rising cut wind-up | `turned side-on, hilt at his right hip, far left arm crossing his body, blade pointing down and back behind him, far left foot forward` |
| Kasumi | parry, counter-thrust | `deep knee bend, hilt raised beside his right temple, far left arm across his chest, blade level and pointing forward, edge up` |
| Hasso | diagonal-cut wind-up | `left shoulder toward the enemy, hilt beside his right cheek and shoulder, blade tilted back 30-45 degrees from upright, far left foot forward` |



Moves as stance pairs:
- Overhead cut: jodan or Vom Tag → follow-through low in front. Heavy diagonal: hasso or Zornhut → low on the far side. Thrust: chudan → Langort. Counter: kasumi or Ochs → Langort.
- **Iai draw-cut**: sheathed, right hand on the hilt → the blade slides out forward, level across the CHEST at about shoulder height, right elbow high → the right arm straight out in front at chest height, one hand, scabbard end still behind. The blade is never cocked back behind the body. Paint the middle stance as its own pose. Facing left, the left-hip scabbard is on the near side and the left hand pulls it back along the hip during the draw; its trail is a level arc in front at chest height.
- **Complete cut** (game form: draw → raise → one cut): after the draw the raise starts ONE-handed (the right hand lifts the blade overhead while the left stays at the scabbard mouth and joins at the top) → two-handed cut down and forward, ending at waist height for a light cut or tip toward the ground with the torso over the front knee for a finisher.
- **Thrust from a sheathed idle**: show the draw first (blade out level, its own frame), then the dash; the afterimage is the draw stance, not the idle. One draw pose can serve every iai move of a character.
- **Resheathe (noto)**: in the middle, the right hand draws the hilt back across the chest and the blade runs forward and down into the scabbard mouth at the front of the hip, the scabbard `running back toward the lower left, mouth at the front of the hip`; that bent angle is correct and only for the middle. The last frame has blade and scabbard back on one line, scabbard end raised slightly behind (the idle). Hold about 280 ms, then idle.
- **Three-hit combo**: horizontal cut → rising cut (both hands, blade swept up and back overhead) → downward diagonal finish (blade low toward the lower front, torso over the front knee). Avoid a spinning slash: it turned the figure to a front view and dropped the scabbard.
