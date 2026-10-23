# Armour and clothing in motion (plate joints, samurai armour, turnarounds, capes, robes, coats, skirts)

Facing right throughout: a cape, train or coat tail that lags lies **toward the left of the image**.

## Contents
- [What every armoured pose keeps](#what-every-armoured-pose-keeps)
- [Joints, what to draw](#joints-what-to-draw)
- [Samurai armour (front/back sheet, two stances, donning sequence)](#samurai-armour-frontback-sheet-two-stances-donning-sequence)
- [Turnarounds (front / side / back, 4 or 8 directions)](#turnarounds-front--side--back-4-or-8-directions)
- [Cloth: rules that make it read](#cloth-rules-that-make-it-read)
- [Wind strength stages (four steps, weak -> strong)](#wind-strength-stages-four-steps-weak---strong)
- [Cycles (frame rhythm and key shapes)](#cycles-frame-rhythm-and-key-shapes)
- [PixelLab steps (side view, facing right)](#pixellab-steps-side-view-facing-right)
- [Pitfalls to name in prompts](#pitfalls-to-name-in-prompts)

## What every armoured pose keeps
- **Rigid tubes, sliding bands, cupped joints.** Every plate limb is a rigid tube (upper arm, forearm, thigh,
  shin) joined at a cup (elbow, knee) with 2-3 narrow overlapping bands above and below it. On a bend the tubes
  stay the same length and shape, the bands slide under each other, and the cup turns with the lower limb. Ask
  for `rigid steel plates on the upper and lower arm, the elbow cop covering the bent elbow, the plates keep their
  shape`. Without it the generator bends the plate like cloth (the "melted armour" look).
- **Same piece list in every pose.** Name the pieces once in the look line and repeat them in every key pose:
  `the same helmet, pauldrons, breastplate, gauntlets, tabard and greaves as in the original`. Pauldrons and the
  helmet crest are what vanish first in wide poses.
- **Plate does not stretch, the gaps open.** When a joint bends, the dark mail or padding underneath shows
  (inside of the elbow, back of the knee, the armpit). One or two dark pixels there sells the bend; ask for
  `dark mail showing at the inside of the bent elbow`.

## Joints, what to draw
| Joint | What moves (sources) | Visible description for the prompt |
|---|---|---|
| Elbow | Upper and lower tube rigid; a rounded cop over the point with a fan-shaped side wing on the outside; the cop rotates with the forearm; mail at the inner crook | `round elbow cop with a side wing on the outside of the bent elbow, straight rigid forearm plate` |
| Shoulder (pauldron) | 3-5 curved bands stacked down the upper arm; raising the arm slides the lower bands up under the top plate; a big pauldron reaches over the chest and wider at the back; a small spaulder leaves the armpit open (a round disc may cover it) | arm raised: `the pauldron bands pushed up together over the shoulder, the pauldron staying on top of the shoulder` · arm down: `layered pauldron covering the shoulder and top of the arm` |
| Gauntlet | Flared bell cuff, rigid; one plate over the back of the hand; 4-6 small overlapping scales over each finger or a single mitten of bands; a fist fans the bands out over the knuckles | `steel gauntlet with a flared cuff and overlapping finger plates, fist closed around the grip` |
| Waist | Breastplate rigid; below it 3-5 horizontal hoop bands (faulds) that telescope up under each other when the torso bends forward; two plates (tassets) hang from them over the front of each thigh and swing with the thigh; one solid crotch plate blocks the stride | bend: `torso bent forward, the waist bands sliding up under the breastplate` · stride: `the thigh plates swinging forward with the front leg` |
| Knee | Thigh and shin plates rigid; a cupped knee cop with a wing on the outer side; 1-3 small bands above and below that slide; bent, the cop stays on the knee point and the bands fan open behind | `round knee cop on the bent knee, the shin plate straight, the thigh plate straight` |
| Feet | Several overlapping bands over the toes, often a long point; flex only at the toe bands | `segmented steel shoes`; drop pointed toes at sprite size (they read as a blade) |

## Samurai armour (front/back sheet, two stances, donning sequence)
- **Layer order (inside -> out, from the donning sequence):** robe and puffy trousers -> shin guards tied at the
  knee -> armoured sleeves on each arm -> a thigh apron of small plates -> the chest box of laced plate rows ->
  two big flat shoulder boards -> a skirt of 4-5 hanging laced panels -> helmet with a wide flared neck guard and
  a tall crest, face mask last. The sword sits through the sash at the left hip.
- **What moves:** the shoulder boards hang flat from the shoulders and **swing out from the arm** when it rises
  (they do not wrap like a pauldron); the skirt panels **split and fan apart** over the front thigh in a lunge;
  the trousers billow at the knee; the chest box stays a rigid rectangle. Prompt: `laced samurai armour, two flat
  rectangular shoulder boards swinging out from the raised arm, the plate skirt panels splitting apart over the
  bent front thigh, puffy trousers, the chest box rigid`.
- **Helmet crest is the first thing to change** between poses: `the same helmet with the same golden crest and
  the same wide neck guard`. The two stances on the sheet are a wide low lunge with the blade forward and a
  sideways guard with the blade held back; the skirt fans in both.

## Turnarounds (front / side / back, 4 or 8 directions)
- **Same heights in every view.** All sheets run horizontal guide lines across the views: helmet top, eye slit,
  shoulder line, belt, hem, knee, sole. Ask for `the same height and proportions in every view`, and check the
  belt and knee lines line up when the frames sit side by side.
- **Things that must survive the turn:** crest or plume side, the side of the body the sword hangs on (left hip,
  or across the back with the hilt over the same shoulder), cape clasp, belt pouches, shield arm. In the 6-view
  sheet every strap and holster stays on the same body side; in the samurai sheet the long hair covers the back
  plates in the back view, so the back view needs its own wording.
- **The back view is different armour.** The Gothic photos show the backs of the knees and thighs **open** (straps
  and padding, no plate) and a long tail on the helmet; the hooded cloak's back view is one big unbroken shape
  with only the hood point and hem. Describe the back explicitly: `back view: plate backplate, the helmet's neck
  tail, the backs of the legs strapped, red cape covering the back down to the knees`.
- **Side views slim down.** Pauldrons become a round shoulder bump, the breastplate a curved profile, the cloak a
  narrow wedge hanging behind. Say `side view, the cape hanging behind his back toward the left of the image`.
- **The cloak opens on the arm side.** The hooded turnaround shows a cloak closed at the throat; an arm reaching
  out lifts the whole side panel like a curtain and shows the lining. Prompt: `left arm reaching out, the cloak
  lifted on that side, its inside visible`.
- **4-direction walk (LPC gold plate, 9 frames each):** frame 1 is the standing pose, frames 2-9 the walk loop.
  Front and back views read the walk only by the feet lifting and a 1 px body bob; the plates do not change.
  Side views swing the legs and arms, the plume rocking a pixel. A stiff armoured walk needs no cloth at all.

## Cloth: rules that make it read
- **Anchored, then lagging.** Cloth is pinned at the shoulders (cape), the waist (skirt, tassets, coat tails)
  or the neck (hood). The anchor moves with the body; the free edge **arrives 1-2 frames later** and
  **overshoots** past the rest position before settling. A body that stops gets one more cloth frame forward.
- **Folds radiate from the anchor.** The flow diagrams draw the hem first as a wavy line, then straight fold lines
  from each anchor point to each wave peak; the lining shows wherever the hem curls over. Prompt: `folds running
  from the shoulders down to a wavy hem, the dark inner lining showing where the hem curls`.
- **Opposite the motion, always.** Moving right: cape, coat tails, scarf, plume and train trail toward the left of
  the image. Falling: cloth rises above the body. Leaping up: cloth streams down and behind. Kneeling or lying:
  cloth pools on the ground around the knees or over the body.
- **Long cloth turns late.** In the trained-dress turn the body turns in 2-3 frames, the train keeps going the old
  way for 2-3 more and then sweeps round in a wide arc behind; stooping pulls it in tight to the feet.

## Wind strength stages (four steps, weak -> strong)
| Stage | Shape | Prompt wording |
|---|---|---|
| 1 still/light | hangs straight, only the bottom corner kicks back | `cape hanging straight down his back, the bottom edge lifting slightly toward the left of the image` |
| 2 breeze | lower third lifts, bottom edge diagonal | `cape swinging back, its lower half lifted toward the left of the image` |
| 3 strong | whole sheet at ~45°, rounded belly, hem rippling | `cape billowing out behind him at a slant toward the upper left of the image, wavy edge` |
| 4 gale | near horizontal or above the shoulders, the far edge curling over, sharp folds back to the clasp | `cape streaming straight out behind him toward the left of the image, nearly horizontal, the edge curling and snapping` |
Pick one stage per clip; mixing stage 1 and 4 in key poses makes the in-betweens flap randomly.

## Cycles (frame rhythm and key shapes)
- **Cape lift and flutter (numbered cycle, ~38 drawings):** hang (1) -> lower edge swings back (9) -> diagonal
  sheet (14) -> horizontal (19) -> flutter loop 19-23-27 (a ripple runs from the clasp to the tip, keys 4 apart,
  the tip up on one key and down on the next) -> drops back diagonal (32) -> hangs (38). At sprite rate: 3 frames
  to lift, a 3-4 frame flutter loop, 2 frames to fall. The S-ripple travelling along the sheet is the loop:
  `cape trailing behind toward the left of the image in an S-curve, the wave halfway along it`.
- **Idle flutter (cloaked archer, 10 frames):** only the bottom 2-4 px of the cloak move, a sideways sway of 1
  px, out of phase with the 1 px body breathing. Prompt for animate_image: `the cloak hem sways slightly, body
  breathes, same pose`. Do not ask for wind in an idle; it turns into a stage-3 flap.
- **Walk with a cape (caped knight, 6 frames; cloaked archer ~10):** the cape hangs behind and swings a little
  opposite to the back leg; at each contact frame the hem kicks back 1-2 px, at each passing frame it drops.
  Plume rocks with the head bob. Plate stays rigid.
- **Run with a cape (caped knight 6 frames; cloak run 6 frames; king leap):** the cape rises to stage 3 and stays
  there, rippling. On the stride (legs apart) frames the cloak streams flat behind and the legs show under it; on
  the contact/passing frames it bunches into a lump on the back and drops a little. Torso leans forward; hood
  leads the body. Key prompt: `running, leaning forward, cape streaming out behind toward the left of the image,
  legs visible below the cape`.
- **Robe or long gown walk (Muybridge, 12 frames per stride pair):** the hem is pressed **forward against the
  front shin** on the contact frame (the leg shape shows through the cloth), the back of the hem lags and bells
  out behind the trailing leg; on the passing frame the robe hangs nearly straight; the hem swings about one
  foot-length front to back across the stride. Feet show below the hem on every frame. Prompt: `long robe, the
  front knee pushing the robe forward, the hem flaring back behind the trailing leg, both feet visible below the
  hem`.
- **Skirt and open coat run (~36 drawings: start, run, stop):** the skirt is a bell that swings **opposite to the
  front leg** (front edge pressed to the forward thigh, back edge flared); on the airborne frames the whole bell
  lifts and opens, on landing the hem compresses and drops; open coat tails fly flat behind the waist on the
  stride and flick up on the push-off. The stop has 2-3 frames of the skirt and tails swinging past the body
  forward before settling.
- **Attack (caped knight, 10 frames; wolf-man; king lunge):** the cloth lags the swing: wind-up = cape swings
  forward around the legs, strike = cape whips back toward the left of the image, 2-3 settle frames it flops back.
  The crescent in the knight's attack is on frame 6 of 10. Loincloths, straps and tails follow the same rule.
- **Death/collapse (cloaked archer, king):** the body drops first, the cloak lands one frame later and covers
  the body as a flat sheet on the ground.

## PixelLab steps (side view, facing right)
- **Look line:** list every armour piece and the cloth with its colour and length once (`steel pauldrons, steel
  gauntlets, deep red tabard to the knees, dark red cape to the calves`); repeat it word for word in every pose
  edit. Cloth length is the thing pose edits shorten.
- **Pose edits:** each key pose names the cloth direction in screen terms and the wind stage, plus one rigid-plate
  line for the bent joint. Keep the clasp point in place: `cape attached at both shoulders`.
- **animate_image in-betweens:** the action states the lag (`the cape follows a moment behind the body`). Keep the
  cape stage the same in both key poses for loops; for a strike, key A = cape forward, key B = cape back.
- **Canvas:** a stage-3/4 cape adds about one body width behind; pad the left side, or the generator folds the cape
  down to fit.

## Pitfalls to name in prompts
- **Armour melts in bends** -> `rigid plates`, `the elbow cop / knee cop on the bent joint`, plus the dark gap.
- **Pieces vanish or change between poses** (pauldron gone, crest swapped, gauntlet becomes a bare hand, tabard
  becomes a skirt) -> repeat the full piece list in every key pose; check each in-between at 3x.
- **Cape flips sides** (appears in front of the body or toward the right while running right) -> `cape behind his
  back, trailing toward the left of the image` in every key pose; the clasp at the shoulders, never at the hip.
- **Cloth frozen in a run** (the idle cape pasted on a running body) -> state stage 3 in the run keys and ask for
  `the cape rippling, its edge rising and falling between frames`.
- **Robe hides the legs and the walk reads as a glide** -> `both feet visible below the hem`, front knee pressing
  the robe forward, and at least 1-2 px of vertical bob.
- **Samurai skirt and shoulder boards stay stiff** -> name the panels splitting over the front thigh and the boards
  swinging out from the raised arm.
- **Back view loses the cape or the sword side** -> describe the back view on its own, with the cape covering the
  back and the sword hilt over the same shoulder as in the front view.
