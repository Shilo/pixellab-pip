# Key-Pose Animation

Read this to animate an attack, skill, or signature move from a standing sprite: pad the canvas, paint key poses with `edit_image_pro_flash`, colour-match them, interpolate in-betweens with `animate_image`, then finish, add effects, check, and export. Route limits, frame echo, and the generic padding rule live in `animation.md`; weapon-specific poses, trails, and rhythm live in the `weapon-*.md`, `martial-arts.md`, `armor-clothing.md`, and `weapon-effects.md` pages. Dated measurements behind these rules: `../../../docs/pixellab/key-pose-animation-evidence.md`.

**Facing convention.** Every pose and action below is written for a sprite facing right: the near side is the figure's right, so right hand, right foot, and right-hip gear face the viewer, and left-hip gear sits on the far side. For a left-facing sprite, mirror every side and direction word, including screen-term sides.

## Contents

- [Run Folder](#run-folder)
- [Pipeline](#pipeline)
- [Canvas And Padding](#canvas-and-padding)
- [Key Poses](#key-poses)
- [The Dynamic Layer](#the-dynamic-layer)
- [Pose Review Checkpoint](#pose-review-checkpoint)
- [In-Betweens](#in-betweens)
- [Picking Frames](#picking-frames)
- [Multi-Stage Moves](#multi-stage-moves)
- [Carried And Worn Props](#carried-and-worn-props)
- [Shots, Beams, And Projectile Skills](#shots-beams-and-projectile-skills)
- [Two-Handed Sword Stances](#two-handed-sword-stances)
- [Pistol Draw And Flying Kick](#pistol-draw-and-flying-kick)
- [Hurt, Death, And Telegraphs](#hurt-death-and-telegraphs)
- [Clean-Up Order And Effects](#clean-up-order-and-effects)
- [Timing](#timing)
- [Look Checklist](#look-checklist)
- [Example Values: Side-View Dark Fantasy](#example-values-side-view-dark-fantasy)

## Run Folder

One run folder per move, `pixellab-pip-generations/<character>-<move>/`: `raw/` every key pose and clip as fetched,
`keys/` the checked, colour-matched key poses the clips are made from (`A.png`, `B.png`, ... in stage order),
`clean/<n>-<step>/` the labelled finishing copies in order, `fx/` effect exports, and `final/` the sheet, its JSON and
GIF (`<character>_<move>.png/.json/.gif`), beside `manifest.json` and the blueprint. The still gets its own run folder
(`<character>-still/`). A move built from two clips is joined first: copy both into one `clean/<n>-join/` folder
numbered `0.png..N.png` in play order, so `scrub`, `slash_layer` and `ground_snap` see one clip.
Review tools (the Claude edition's panel) read `keys/` and `final/`, so keep these names.

## Pipeline

1. Check and fix the standing sprite first, per `characters.md` (look checklist at 3x, and how a fault is fixed); every pose and in-between inherits its faults. Use one canonical still per character (every prop on) for padding, colour matching, and ground lines.
2. Pad a copy of the sprite (`assets/pad_sprite.py`, see [Canvas And Padding](#canvas-and-padding)) and upload it (`get_upload_url`, see `image-input-roles.md`).
3. Paint the key poses with `edit_image_pro_flash`, `no_background: true`, `use_color_palette_correction: true` ([Key Poses](#key-poses), [The Dynamic Layer](#the-dynamic-layer)).
4. Colour-match the key poses to the standing sprite (`colormatch`, `finishing.md`) before any in-between: clips made from matched keys inherit the right colours; matching only at the end left visible drift.
5. Pause at the [Pose Review Checkpoint](#pose-review-checkpoint).
6. Interpolate with `animate_image` (`first_frame_url` = pose A, `last_frame_url` = pose B, `no_background: true`, motion-only `action`) ([In-Betweens](#in-betweens)).
7. Pick frames ([Picking Frames](#picking-frames)), then finish in the [Clean-Up Order](#clean-up-order-and-effects) with the helpers in `finishing.md`; effects come from `vfx-workbench.md`.
8. Check with the doctor (`animation-doctor.md`; `--stepped` for moves stepped through key poses, `--fx` for frames with baked effects, `--ref` the padded sprite).
9. Export the sheet and preview with `local-asset-assembly.md` (`make_sheet.py` with `--pad`, `--facing`, `--hit`, `--durations` from [Timing](#timing)).

The plan shown at the approval gate (`auto.md`) lists the canvas, every pose prompt, every clip with its `frame_count`, and every locally painted layer (trails, baked effects, a flown prop), so `plan` and `auto` levels can run those steps without another ask.

## Canvas And Padding

A standing sprite is tight to its silhouette; on that canvas a big swing has nowhere to go and the body barely moves. Pad with room on the facing side, plus room above only when the weapon, arms, or body rise above the head.

| Move | Room |
|---|---|
| Overhead swing, slam, leap, upward cast, raised long bow | in front and above |
| Long two-handed weapon swung over the shoulder (greataxe, maul, halberd) | behind, in front, and above |
| Thrust, lunge, throw, shot, bash, waist-high sweep | in front only |
| Lunge | also behind: the cape and back leg travel back |

- Size the pad from the sprite: about 2× its width, plus about 28% height when the move rises above the head. A style may fix exact canvases ([Example Values](#example-values-side-view-dark-fantasy)).
- Pro Flash edit cost steps up when the longest side passes 200 px (measured 6 vs 9 generations per pose): pick the shorter canvas whenever nothing rises above the head. Confirm with `get_pro_flash_capabilities` per `pro-flash.md`.
- The canvas also caps the clip: `animate_image` needs `width × height × frame_count ≤ 524,288` (`animation.md`). A 256×256 pad allows `frame_count` 8 at most; to get more frames there, splice ([In-Betweens](#in-betweens)). When a wider canvas would not fit the frames, crop the poses to their joint bounding box first; otherwise accept fewer frames.
- Record the pad offset per character and move; the engine grows the sprite rect by `offset × scale` (mirrored when flipped) so the feet stay put, and `make_sheet.py --pad` stores it.
- A pose that touches the canvas edge bakes the cut into every in-between. Before animating, check pose B's borders; more than about 15 opaque pixels on a side means re-pose on a canvas with more room on that side.
- Front-facing giant bosses fought from both sides: draw them waist-up rising out of something (a crack, water) with about 20 px margin, since 256×256 cannot be padded further.

## Key Poses

Template:
```
The same <look line>, <pose core>, <facing>. Exactly the same body size as the original, same colours and pixel style, <anchor> in the same place, no background.
```

- **Look line**: who plus 2–3 identifying colours or props, from looking at the sprite once. For armoured or caped characters list every armour piece and each cloth's colour and length, word for word in every pose; pauldrons, crests, and cloth length drift first (`armor-clothing.md`).
- **Anchor**: `feet`; for lunges `back foot`; for floating bodies `base of the robes`; for serpents `coils resting`. Deep lunges still float, so ground-snap later.
- **Pose A (wind-up)** is a real coil: name where the weapon or fist ends up and how far the torso turns. A weak wind-up is the most common failure: "arm drawn back" returns an idle stance; "fist cocked high beside the far shoulder, torso rotated hard" works. Try two candidates for wind-ups.
- **Pose B (hit)** is the follow-through at the end of the blow.
- **Directions in screen terms**: say `toward the right of the image`, never "his right" or "forward", in every pose, and again in the `action`.
- **Held props**: name each prop's SIDE in screen terms in every pose (`the staff upright on the left side of the image, close against his robe, staff arm bent with the fist at waist height`), never a fixed POSITION (`exactly where it was` freezes the prop while the body moves and stretches the arm to reach it). Say the gripping hand is joined to the body at normal arm length. One-handed weapon or mismatched arms: name which arm holds it by its look and say the other hand is empty.
- **Worn props**: describe what is visible, not where it is worn (`characters.md`). After a draw, say `the EMPTY scabbard` / `the EMPTY holster` in every later pose, or a second weapon appears.
- **Props in colours the sprite lacks**: palette correction and colour matching turn them into the sprite's colours. Pose without the prop and lay it on afterwards (a locally painted layer, named in the plan), or recolour the prop region afterwards.
- **One weapon, one tip**: `one clean straight steel blade with a single sharp tip` fixes forked tips; give lengths in body terms (`hilt as long as his forearm`). For the weapon the generator tends to swap to, end with `the weapon is clearly a <weapon>, never a <the other>`.
- **Raised-arm end poses** drop the weapon in about half the casters: write it into the pose (`raising the staff high in both hands`).
- **Start every sword move the way idle holds the weapon**: reuse one sheathed wind-up as pose A of every move, then animate the draw into each move's own pose B.
- Tool: Pro Flash plus [The Dynamic Layer](#the-dynamic-layer) is the default. Offer Pro `edit_image` (same text, about 10 per pose) for showpiece moves or a move that still flashes after one re-roll; its in-betweens came out cleaner. PixFlux cannot pose-edit (it keeps the standing pose and returns an opaque background).

## The Dynamic Layer

Plain pose wording gives stiff Pro Flash poses. For fast moves add all four to every key pose; it matched Pro's dynamism at Pro Flash cost:

1. `dynamic exaggerated pose`, said outright.
2. Stance depth: wind-up `deep low stance, knees bent, weight on the back foot, back arched`; hit `extremely deep lunge, front knee bent low, back leg stretched straight`.
3. Torso: `body twisted away` (wind-up), `torso leaning far forward` (hit).
4. Secondary motion of the character's own soft parts (cape, tabard, robe, hair), with its direction in screen terms in each pose (`cape trailing toward the left of the image`), or it flips sides. One wind strength per clip, named in both poses.

```
The same <look>, <pose core>, dynamic exaggerated pose: <stance depth>, <torso>, <secondary motion>, <facing>. Exactly the same body size as the original, same colours and pixel style, <anchor> in the same place, no background.
```

Calm moves (a kyudo shot, a spell focus, a bow to the opponent) skip the layer: upright posture, feet still. More dramatic poses bring more generator flashes in the in-betweens; handle them in clean-up, not in the prompt.

## Pose Review Checkpoint

Stop here before any in-between. Show the sprite and the key poses side by side at 3× (several stages: one strip, in order) and run the [Look Checklist](#look-checklist). At `plan` level this is one of the content pauses inside an approved plan (`auto.md`): the user chooses Approve or Redo per pose; a Redo uses the plan's redo allowance. At `auto`, approve the poses yourself only when the level says so, and report what you approved.

- Re-roll a pose once for a hard defect: it reads as standing, a prop changed hand or side, a prop appeared, vanished, or doubled, or the body changed size.
- Colour drift is not a re-roll: colour-match instead.
- Small exact defects (a missing bowstring, a nock off the hand) are free: `pixelart_workbench` (`brush`, `copy_region`, `patch_pixels`) on the key pose. A wrong hand or prop: masked inpaint. An inpaint cannot add a prop where another part already is.
- When you fix one pose, re-check the poses you keep.

## In-Betweens

`animate_image` returns `frame_count + 1` images with pose A echoed at index 0 (`animation.md`); `frame_count` must be even. It costs `ceil(width × height × frame_count / 65536)` generations (`cost-routing.md`): quote that in the plan, not a guess.

```
action = "<verb> <weapon or limb> <path> in one fast <heavy|wide> <blow>, <body lean>, <one secondary motion>"
```

- **Motion only**, one short line; never re-describe the character, and never name the fire or glow of a burning weapon (it re-lights the whole body; the key poses already carry it). Never add "no effects / no white lines / no motion trails": naming the flashes invites more.
- **Pin the path** when a take wanders: where the weapon stays and the one direction of travel (`stays low and drives the shield straight forward, the shield kept at chest height the whole time`; `the point stays toward the right the whole time`; `never standing up`).
- **Frame counts**: the more drawings in the fast part, the smoother; low counts freeze on screen. Keep every move of one character at the same count; a short move next to a long one looks choppy. If a long take invents a pose in neither key pose, re-roll once with the path pinned, then fall back to a shorter count for all of that character's moves.
- **Thrusts and snaps** (sword, spear, dagger thrust; a kick extension): use a 6-frame clip alone; longer clips reached the hit early and repeated it with flashes.
Two different splices; pick by the problem. **Heavy chops** repairs the frames after the hit; **Splice** adds frames inside a take.

- **Heavy chops**: when the flash replaces the weapon head on fast frames, keep frames up to the first hit and splice a 6-frame clip from there with `the same <weapon head> stays solid and fully visible in every frame`.
- **Splice** to exceed a canvas's frame cap: in a good take, find the fastest two-frame span (most pixels changed) and run `animate_image` between the frames on either side with `frame_count` 4; its 3 new frames replace the 1 in the middle. If a splice smears, re-roll once, then try the next span along.
- One re-roll for a swing with fewer than 4 usable frames; never pay for a third take — see [Picking Frames](#picking-frames).

## Picking Frames

- Keep every good frame; clean rather than drop. Drop only a smear or blob that cannot be cleaned, a frame whose colours shifted (the body turns lighter or oranger), or a white-washed frame (colour matching turns it muddy grey). Frame drops are proposals unless the approval level allows them (`auto.md`).
- Takes from the same key poses line up: build one clip from the good frames of several takes instead of paying for a third.
- A white swoosh joined to a body that already holds white cannot be scrubbed: drop the frame, copy its neighbour in, or recolour the smear into the effect colour.
- Watch faces for skin-tone flicker across in-betweens and remap the odd frames to the kept frames' tones.
- Find the contact frame by eye and pass it as `make_sheet.py --hit N`; cut or shorten repeats when a clip lands early and holds.

## Multi-Stage Moves

For moves with more than wind-up and hit (a kyudo shot: ready → raise → draw → full draw → release; a draw-then-cut; a combo), write the stages down in order and paint one key pose per stage.

- **The move goes one way**: each pose continues the last; a step done in one pose is never undone in the next. Check the poses as one strip, in order. When a pose undoes a step, drop it and interpolate across the gap.
- One 4-frame clip per neighbouring pair; keep instant cuts where the motion is instant (a release) or a prop changes place (bow from the back to the hands).
- When in-betweens cannot do a stage (a far-hip sword draw came back reversed, crossed, or doubled), step through checked key poses instead and carry the speed with a trail or afterimage ([Carried And Worn Props](#carried-and-worn-props)).
- Vanish or teleport strikes: crouch → crouch with smoke frames → smoke alone → the first cut pose emerging from the smoke → the other cuts with trails; keep the body on one spot (the engine moves the sprite). Smoke comes from `vfx-workbench.md` in the character's own colour ramp.

## Carried And Worn Props

The generator's in-betweens do not keep a carried prop on its side: a sheathed sword flipped, rotated, reversed, or doubled in most clips even when both key poses were right. Decide per move:

| Prop during the move | Method |
|---|---|
| A worn prop that moves (sword drawn from its scabbard, pistol from its holster) | step through checked key poses; show the swing with a trail through the blade tips (`blade_trail`, `--ghost` for a flash-step afterimage) |
| Held in both hands the whole move (a bow being drawn, a staff) | interpolate between checked poses with 4-frame clips; check string and nock in every frame |
| Stays put (idle, death) | interpolate; say `no step`, `the sword stays sheathed` |
| Held in one hand while the other works (staff during a throw or cast) | name its side in every pose ([Key Poses](#key-poses)); check the grip in every frame |

- Check every in-between at 3× next to the sprite: the gripping hand touches the prop at normal arm length, joined to the body with no background gap.
- Never paste a prop region from one frame into another; the body moved.
- A slash cannot be stepped as one finished pose plus a trail (it reads as a thrust): paint the cut's middle as its own key poses (blade cocked back → level across the chest → finish), then one trail along one path through the blade tips, each frame's trail ending at that frame's tip.
- Hurt for a prop-carrier is a snap ([Hurt, Death, And Telegraphs](#hurt-death-and-telegraphs)).

## Shots, Beams, And Projectile Skills

**Shots** (guns, bows, wands) reach forward only: canvas with room in front, pose A = the aim (`rifle shouldered, barrel levelled toward the right, braced stance`), pose B = the recoil (`shoulder and rifle jolted back, barrel kicked up, torso rocked back onto the braced back foot`). No crescent. The damage fires on the first motion frame (`--hit 1`). Name an energy weapon's flash colour, or the generator paints an orange gunpowder flash. A big recoil from a kneel needs the path pinned (`stays low on bent legs, never falls over`). A take that drops the gun mid-shot: re-roll once with `the gun never drops below shoulder height`. A light recoil can be a 2 px lift of the arm band only (rows where arms and gun stick out past the body), checking the rows below stay identical.

**Gear-mounted launchers** (a shoulder pod, a back cannon): the launcher moves with the recoil, so take the muzzle point per frame from the pose, not from the first frame, and start the exhaust after the recoil peak; otherwise the smoke lands on the head. Use these Shots poses, not the thrown-prop recipe.

**Generator flashes on shots and beams**: shot, beam, and projectile poses come back with the effect painted in, even the charge pose. Clear it from each key pose before animating (`scrub --box` or `--clear-right <tip x>`), clear the in-betweens' own flash at the barrel tip only (a colour scrub strips hair and skin the flash lit), or reuse the previous frame where the flash sits on the body (a short hold reads as weight). Then paint the real flash or beam in `vfx-workbench.md` and bake it on at the muzzle or eye (`bake_fx`).

**Thrown props and projectile skills** (javelin, dagger, a bomb, a cast bolt):
1. Key poses: wind-up (prop in hand) → release (hand open, the prop just out of it or not drawn) → follow-through (hand empty). Clips: 6 frames wind-up → release, 4 frames release → follow-through. A conjured projectile the still does not carry (an ice shard, a fire bolt): name it in the wind-up pose, crop the one the generator draws there as the prop, or draw it in `vfx_workbench` and fly it with the effect's own projectile instead of `throw_prop`.
2. Remove every generator-drawn copy of the prop after the release (keep the largest piece, or scrub).
3. Ground-snap, then fly the prop along the throw (`throw_prop`, `--turn` to tumble it); paste it on the release frame first if the release pose does not hold it.
4. Impact: a `vfx-workbench.md` strike, baked on with the canvas widened on the facing side (`bake_fx --widen`), holding the last body frame until the effect ends.
5. Export with body timing then the effect's own timing; pass the flight frames to the doctor as `--fx`. Also ship the body-only sheet, the prop, and the effect for engines that spawn projectiles themselves.

## Two-Handed Sword Stances

Use a stance name only with its visible description; the generator draws the description, not the term. Grip: right hand just below the guard, left hand near the pommel. Feet shoulder width, one forward, knees slightly bent. A katana is worn through the sash on the left hip (the far side) and drawn by the right hand. More guards, kendo cuts, and katana rhythm: `weapon-katana.md`, `weapon-sword.md`.

| Kamae | Use | Visible description |
|---|---|---|
| Chudan (middle) | ready, start of a thrust | `both hands on the hilt a fist in front of his navel, blade angled up, tip at the opponent's eye or throat height, near right foot forward` (not "pointing straight forward": that draws it flat) |
| Jodan (high) | overhead-cut wind-up | `both hands raised above his head, left hand about a fist from his forehead, blade angled up and back behind him, far left foot forward` |
| Gedan (low) | counter, wary ready | `blade lowered, tip pointing at the ground ahead, both hands at the hips, near right foot forward` |
| Waki (side) | sideways or rising cut wind-up | `turned side-on, hilt at his right hip, far left arm crossing his body, blade pointing down and back behind him, far left foot forward` |
| Kasumi | parry, counter-thrust | `deep knee bend, hilt raised beside his right temple, far left arm across his chest, blade level and pointing forward, edge up` |
| Hasso | diagonal-cut wind-up | `left shoulder toward the enemy, hilt beside his right cheek and shoulder, blade tilted back 30-45 degrees from upright, far left foot forward` |

| Longsword guard | Visible description |
|---|---|
| Fool's (Alber) | tip lowered toward the enemy's feet |
| Roof (Vom Tag) | hilt at or above the right shoulder, tip up and behind (overhead wind-up) |
| Ox (Ochs) | hands beside the head, blade level, pointing at the enemy's face |
| Plow (Pflug) | hilt at the right hip, tip angled up at the enemy's face |
| Side / Tail (Nebenhut) | hilt at the right hip, left arm across the body, tip low and behind |
| Longpoint (Langort) | arms fully extended at chest height, tip at the throat (end of a thrust) |
| Wrath (Zornhut) | hilt at the right shoulder, blade back and down behind the body, core coiled |

Moves as stance pairs:
- Overhead cut: jodan or Vom Tag → follow-through low in front. Heavy diagonal: hasso or Zornhut → low on the far side. Thrust: chudan → Langort. Counter: kasumi or Ochs → Langort.
- **Iai draw-cut**: sheathed, right hand on the hilt → the blade slides out forward, level across the CHEST at about shoulder height, right elbow high → the right arm straight out in front at chest height, one hand, scabbard end still behind. The blade is never cocked back behind the body. Paint the middle stance as its own pose. Facing left, the left-hip scabbard is on the near side and the left hand pulls it back along the hip during the draw; its trail is a level arc in front at chest height.
- **Complete cut** (game form: draw → raise → one cut): after the draw the raise starts ONE-handed (the right hand lifts the blade overhead while the left stays at the scabbard mouth and joins at the top) → two-handed cut down and forward, ending at waist height for a light cut or tip toward the ground with the torso over the front knee for a finisher.
- **Thrust from a sheathed idle**: show the draw first (blade out level, its own frame), then the dash; the afterimage is the draw stance, not the idle. One draw pose can serve every iai move of a character.
- **Resheathe (noto)**: in the middle, the right hand draws the hilt back across the chest and the blade runs forward and down into the scabbard mouth at the front of the hip, the scabbard `running back toward the lower left, mouth at the front of the hip`; that bent angle is correct and only for the middle. The last frame has blade and scabbard back on one line, scabbard end raised slightly behind (the idle). Hold about 280 ms, then idle.
- **Three-hit combo**: horizontal cut → rising cut (both hands, blade swept up and back overhead) → downward diagonal finish (blade low toward the lower front, torso over the front knee). Avoid a spinning slash: it turned the figure to a front view and dropped the scabbard.

## Pistol Draw And Flying Kick

**Pistol draw and shot** (holster on the near right hip): ready → grip (right hand on the holstered pistol, left hand flat at the chest centre) → clear (muzzle turns forward at chest height, left hand joins, finger along the frame) → push (both arms extend, sights just under the eyes, never above the eye line) → recoil plus a `vfx-workbench.md` muzzle flash → aim hold. The pistol moves between poses: step, do not interpolate. Say `the EMPTY holster` in every pose after the draw.

**Flying side kick**: takeoff (crouched run-up, arms back) → chamber (airborne, kicking knee to the chest, torso leaning back) → kick (leg snapped out, heel first at head height, other leg folded, torso nearly horizontal, arms back) → land (low crouch, guard up). Needs room above and in front. Speed lines go behind the body, never along the leg (that reads as a blade) and never as in-betweens of a flying body (they smear). Ground-snap only the frames on the ground. For a kick between two poses use a 6-frame clip with `the raised knee stays up, then the lower leg snaps out; the foot never goes back to the ground`.

## Hurt, Death, And Telegraphs

- **Hurt**: paint only the peak recoil on the attack's padded canvas (`thrown backward, head snapped back, staggering onto the back foot, arms flung out, <weapon> still gripped in his hand, still facing <side>`; unarmed: name the hands). Interpolate stand → peak with a motion-only action (`head and torso jerk back and away`; "knocked back by a heavy blow" paints impact bursts), then play it there and back. For a carried-prop character or a sheathed swordsman, play a snap: idle → recoil (hold about 300 ms) → idle, no in-betweens, and describe the sword exactly as in idle (never `hand goes to the hilt`). Colour-match hurt frames; they drift brighter or darker.
- **Death**: paint the defeated pose as the last key; say `no step` or the body walks forward first. A sheathed swordsman sinks onto one knee in place, hand still on the hilt, hilt and scabbard on one line. When a death clip paints clouds, build it from clean hurt frames plus the clean collapse frames.
- **Telegraph wind-up** for a monster: a 4-frame clip padded still → the attack's pose A (`slowly gathers itself and draws back into the wind-up`); its last frame is pose A, so the engine can hold it until the blow lands.

## Clean-Up Order And Effects

Per move, in the order and with the helpers in `finishing.md`. For key-pose moves: poses drift up to about 20 px, so snap every grounded frame; for waist-up bosses match a body band, and do not snap a slam that lowers the body on purpose. Check the weapon at 3× after cleaning.

Effects choice: blades get a crescent slash (harvested from a 6-frame take of the same poses, or recoloured from the generator's own streaks), shown on the mid-cleave frame and faded on the next, never with the full blade and full crescent on one frame; blunt weapons get a line smear, dust at the head, and a one-frame rebound; spells may keep the generator's streaks recoloured to an element. Shapes, frame counts, and fades per effect: `weapon-effects.md`. A weapon that already trails its own glow gives no crescent: skip it. Animated effects themselves: `vfx-workbench.md`.

## Timing

Hold the wind-up, swing fast, hold the hit, settle. Calm multi-stage moves ease into each key, hold the key stages longer, make the release instant, and give a long follow-through. Fire the impact (damage, hit flash, projectile release) on the contact frame, not after the animation; shots fire on the first motion frame. Pass the values as `make_sheet.py --durations` and `preview_gif.py --durations`; the user's style or request sets them ([Example Values](#example-values-side-view-dark-fantasy) for one tested set).

## Look Checklist

Run at 3× beside the standing sprite on the sprite, every key pose, and every kept in-between:

- Same arm count and hands; no extra or missing hand.
- Every prop still there, on the same side, pointing the same way (hilt forward, scabbard back), full length, one tip; a drawn weapon leaves an empty scabbard or holster, not a second weapon.
- Gripping hand touches the prop, arm at normal length, joined to the body.
- Same armour piece by piece and cloth colour and length; same body size.
- Colours held (no lighter, oranger, or washed frame); facing kept.
- Feet on the line (or deliberately airborne); nothing cut at the canvas edge.
- No generator flash, burst, or ghost left on body frames.

## Example Values: Side-View Dark Fantasy

These are the values of the "Side-view dark fantasy" example style (`style-examples.md`), not defaults; apply them only when the project's chosen style is that one, and say so in the plan.

| Setting | Value |
|---|---|
| Hero sprite | 96×200, facing right |
| Overhead pad | 192×256, sprite at (24, 56); poses 9 each |
| Front-only pad | 192×200, sprite at (24, 0); poses 6 each |
| Boss pad | 256×256, feet on the bottom edge |
| Swing | `frame_count` 10 (11 frames) on 192×256, plus a 6-frame take for the crescent |
| Light timing (heroes) | 60 ms per frame, wind-up 160 ms, hit 140 ms, settle 120 ms |
| Heavy timing (bosses) | beats × a 50–70 ms step: stand 0.6, wind-up 4.0, in-betweens 0.8, hit 3.2, settle 1.4 |
| Calm timing | in-betweens 100–140 ms, key stages 220–450 ms, release 60 ms, follow-through about 450 ms |
| Hurt snap | peak 300 ms, then idle |
| Crescent | pale "air" ramp behind the character |
| Cost per melee move | 31 generations at 192×256, 22 at 192×200; a shot 18 |
