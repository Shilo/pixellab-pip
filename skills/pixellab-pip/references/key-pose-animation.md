# Key-Pose Animation

Read this when the user requests key-pose choreography/anchors, a multi-stage signature move, or accepts this advanced route after an ordinary animation fails. A simple attack stays on the main animation route. This recipe adds paid pose edits and optional finishing; choosing it does not imply every optional step. Generic routes, canvas/frame limits and input echo are canonical in `animation.md`; approval and review authority are in `auto.md` and `reviewable-candidates.md`.

Specialty poses belong in `weapon-*.md`, `martial-arts.md` and `armor-clothing.md`; effect shapes/rhythms in `weapon-effects.md`; selected example values in `style-examples.md`. Dated successes and failures in `../../../docs/pixellab/key-pose-animation-evidence.md` are scoped observations, not universal model guarantees.

## Plan and files

Plan the stages, chosen supported edit/animation routes, canvas, requested count, every paid call and any proposed local transformation before execution. For selected Pro Flash edits, read `pro-flash.md`. Use the request/style's look, scale and facing rather than a house aesthetic. Optional starting recipes are `../blueprints/overhead-axe-chop.blueprint.json` and `../blueprints/projectile-skill.blueprint.json`; read `blueprint.md` before adapting either to the actual request.

Within the normal run folder, `raw/` can hold unchanged returned poses/clips, `keys/` reviewed pose copies, `clean/<step>/` accepted derivatives, and `final/` requested sheets/metadata/preview. Create only directories/artifacts actually needed. A joined clip must record each source index and junction handling; its derived playback is not an unchanged provider clip. No host panel depends on this layout.

## Pipeline

1. Inspect the canonical still using `characters.md` before multiplying a defect across poses.
2. If the motion needs room, pad a copy without scaling (`assets/pad_sprite.py`). Keep each pose on the same canvas and record the placement offset for any requested export. Honor fixed dimensions; explain conflicting canvas/count limits instead of silently cropping, lowering counts or adding clips.
3. Generate the agreed pose stages using the selected supported edit route and actual source image. A two-stage move uses a genuine wind-up A and follow-through/contact B; multi-stage moves list their stages first.
4. Inspect the poses together and apply the content checkpoint below. Propose a scoped correction for observed drift; colour matching, painting or cleanup is an optional accepted operation under `finishing.md`.
5. Interpolate approved neighbours with the selected raw animation route and motion-only action, or use accepted stepped key poses when interpolation breaks the intended grip/prop transfer.
6. Save all returned frames in returned order and inspect them, optionally running the doctor with `--check-only` (`animation-doctor.md`). Apply only the requested/accepted repair scope.
7. Assemble requested outputs with `local-asset-assembly.md`; finishing, effect composition and custom timing are selected options, not automatic recipe consequences.

## Canvas and pose wording

- Overhead swings/slams/leaps need room above and in front; long weapons swung over a shoulder may also need room behind. Thrusts/shots mainly need forward room; lunges may need rear room for cape/back leg. Size from the actual silhouette and motion, not a fixed multiple for every sprite.
- Check current operation sizes/costs using `pro-flash.md`; a capability response is not a cost quote. The animation route's canvas/frame budget also applies after padding. Inspect pose borders for clipping; padding cannot guarantee containment.
- Pose template: `The same <identity and visible gear>, <pose core>, <screen facing>. Same body size, colours and pixel style, <anchor> in the same place, no background` when transparent art is requested.
- Name a physical anchor suited to the move: feet/back foot for grounded stances, robe base for a floating body, grounded coils for a serpent, the crack for a boss rising out of one. Do not later snap intentionally airborne/lowered parts to an inferred footline.
- Wind-up: name where weapon/fist ends and how the torso coils (`fist cocked high beside the far shoulder, torso rotated away`); a vague arm-back phrase can return idle. Contact/follow-through: name the end of the motion and body lean.
- Name carried gear by visible hand/side, not an assumed anatomy convention (`staff on the left side of the image, fist at waist height`). A fixed prop POSITION can freeze it and stretch the arm; describe grip and path instead. Worn props describe what is visible; a drawn weapon leaves an EMPTY scabbard/holster.
- Name every armor piece and cloth colour/length when continuity matters (`armor-clothing.md`). New prop colours may be lost by palette correction; preserve them in the request or propose a separately accepted correction instead of silently normalizing them away.
- Use screen directions (`toward the right of the image`) when relative words such as forward/his right proved ambiguous. Adapt all example directions to the actual facing/visible side.

## Optional dynamic layer

For exaggerated fast moves, useful pose components are an explicit dynamic pose, deep stance, torso coil/lean, and one direction of cape/hair motion. Example wind-up: `deep low stance, weight on the back foot, torso twisted away, cape trailing left`. Example hit: `deep lunge, front knee low, back leg straight, torso leaning forward`. Calm focus/bow poses may remain upright. These are creative choices; do not apply them to every movement or promise Pro quality from wording alone.

## Pose review checkpoint

Apply `SKILL.md` → Auth And Execution's first-candidate checkpoint before expanding pose generation, with approved wider scope handled by `auto.md` → The cost-approval gate. The joint review here is the checkpoint before interpolation, not a substitute for that earlier checkpoint.

Show the still and the exact pose files proposed for interpolation together at a useful inspection scale and run the look checklist below. Apply the content checkpoint/delegation rule in `auto.md` → Bounded plans and resuming. Any changed pose must be reviewed again before it is used. A redo is paid work within the expressly approved retry scope, or needs additional approval.

When a presentation is available, offer the interactive review in `panel.md` for this checkpoint; build its private snapshot only if that review is wanted.

A localized hand/prop defect may suit masked inpaint; a missing exact line may suit supported PixelArt Workbench edits. Both require the accepted art-change scope and actual schema. Failed helper measurements are observations, not automatic authority to fix pixels or generate another take.

## In-betweens and optional alternatives

Use `animation.md` for exact frame controls, default count, echo and limits. Action template: `<verb> <weapon or limb> <path> in one <fast/heavy/wide> blow, <body lean>, <secondary motion>`. Keep it about motion; the poses carry appearance. If motion wanders, pin where the prop stays and its direction (`shield stays at chest height and drives right`). Avoid naming unwanted flashes repeatedly when observations showed that wording worsened them.

Preserve the requested generated count and returned order. The following are proposals for a specifically accepted derivative/paid extension, not automatic repairs or changes to other moves:

- A short thrust/snap can use a six-generated-frame clip when no other count is required; longer observed takes sometimes reached contact early.
- For a heavy chop whose flash replaces the head, a new six-frame continuation can name `the same weapon head stays solid and fully visible`. For a count-limited canvas, a four-generated-frame interpolation across a fast span can add interior drawings. Show calls, count/order and junction changes before spending/assembling.
- Keep an unmodified source clip. Proposed drop, replacement, splice, holds, there-and-back playback or palette changes identify exact indices, rationale and output timing; apply the accepted version only. Do not retroactively shorten every move to match a failed take.
- For multistage choreography, write each key stage in order and inspect the strip for a reversed step. An instant release/prop hand-off may work better as a stepped pose than interpolation. Propose removing an undoing stage or adding a transition; do not silently drop it.

## Props, projectiles and effects

A moving worn prop can flip/double in interpolation. Checked stepped stages may suit sword draws or magazine hand-offs; a held bow/staff may interpolate between close stages. Inspect hand-to-prop contact and arm length, and avoid pasting a static prop region over a body that moved. Sword/katana cycles are in `weapon-sword.md`/`weapon-katana.md`; aim/recoil and mounted launchers in `weapon-firearms.md`; flying kicks in `martial-arts.md`.

For an explicitly requested thrown-prop skill: wind-up holding it → release with open hand → empty-hand follow-through. Interpolation does not let go of a held prop: animating from the hold kept the blade in hand in every live test, however the action was worded. Make the open-hand release pose first (an edit of the wind-up, the prop already clear of the hand), review it, then interpolate to it. A six-frame then four-frame interpolation is one optional example. Use PixelLab/workbench effect generation or a verified source prop; `throw_prop`/`bake_fx` can compose an accepted derivative. A largest-connected-piece filter does not identify a prop semantically: review its exact extraction/mask, placement, flight path, timing and any removed generator copies. Extending the canvas or holding a body until impact changes the derivative timeline and must be agreed. Separate body/prop/effect exports are useful only when requested by engine delivery needs.

For source flashes, ground drift or colour drift, choose only relevant operations from `finishing.md`. Ground snapping is for agreed grounded frames, not jumps/flyers or deliberate body lowering. Effects are optional: a blade crescent, blunt smear/dust or elemental streak depends on the requested look (`weapon-effects.md`, `vfx-workbench.md`). New locally drawn trails require the global explicit non-PixelLab fallback approval.

## Hurt, death and telegraphs

- Hurt example: peak recoil with head/torso back, arms away, named weapon still gripped. Motion-only `head and torso jerk back and away` avoids a prompt that requests an impact burst. There-and-back or idle→recoil hold→idle are optional playback treatments; a roughly 300 ms peak is one example, not an automatic reorder/hold. Preserve deliberate carried-gear posture.
- Death example: a defeated last pose; `no step` if the body must collapse in place. A sheathed swordsman can sink to one knee with hand still on the hilt. Joining clean hurt/collapse frames is an accepted derivative, not a replacement raw take.
- Telegraph example: an approved four-generated-frame transition from still to the attack's wind-up; the engine can hold that pose when requested.

## Front-facing giant bosses

A boss fought from both sides faces the viewer, so its blows go sideways and down: left swipe, right swipe and two-handed slam, each a wind-up and a hit pose (still: `characters.md`). Ground: lowest-pixel snapping failed here (`finishing.md` → ground_snap); for swipes, an accepted hand-measured offset that matches the crack's colour band to the still worked. Don't snap slams: fists and burst cover the crack. Idle: motion words only (`shoulders lift and lower by a few pixels, hands don't move`); `breathes, glow pulsing` washed the frames white. On screen, a 256 px boss beside ~150 px heroes needed about 1.4× to read as a giant; with whole-pixel engine scaling, show 1× and a fractional boss-only scale before choosing.

## Timing and look checklist

Custom rhythm may hold wind-up, make contact fast and settle longer. The user's requested/source timing wins; selected style examples are suggestions. Confirm the actual contact/release index before supplying `make_sheet.py --hit`; non-damage animations omit hit metadata. Pass accepted durations through the shared assembly/preview helpers without duplicating physical frames merely for a hold.

Inspect the still, exact keys and all returned frames beside their source: arm/hand count, grip contact and normal arm length, gear side/length/tip, empty scabbards after a draw, armour/cloth/body scale, colour/facing continuity, intended footline/airborne state and canvas containment. An intended effect is not an automatic defect. Report failures and unperformed visual checks honestly.
