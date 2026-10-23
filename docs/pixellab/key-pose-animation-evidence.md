# Key-pose animation: test evidence

Dated measurements behind `skills/pixellab-pip/references/key-pose-animation.md`. They come from the pixellab-game-art
production runs (a side-view dark-fantasy game, 96×200 heroes, ~200 px bosses) between 2026-10-13 and 2026-10-22,
ported with the key-pose recipe. Costs are PixelLab generations as reported by the jobs at the time; check current
prices before relying on them.

## Costs

| Item | Measured cost | Date |
|---|---|---|
| `edit_image_pro_flash` key pose, longest side ≤ 200 px | 6 | 2026-10-13 |
| `edit_image_pro_flash` key pose, longest side > 200 px (192×256, 256×256) | 9 | 2026-10-13 |
| Pro `edit_image` key pose, same text | ~10 | 2026-10-13 |
| `animate_image` 10 generated frames at 192×256 | 8 (6 frames: 5) | 2026-10-13 |
| `animate_image` 10 generated frames at 192×200 | 6 (6 frames: 4) | 2026-10-13 |
| `animate_image` 4-frame splice at 256×256 | 4 | 2026-10-13 |
| `animate_image` 4-frame clip at 192×256 | 3 | 2026-10-22 |
| Overhead melee move (2 poses + 10-frame swing + 6-frame crescent take) | 31 at 192×256, 22 at 192×200 | 2026-10-13 |
| Shot (aim + recoil + 10-frame clip) at 192×200 | 18 | 2026-10-13 |
| Hero hurt (one peak pose + two 6-frame clips) | ~33 with the base sprite | 2026-10-15 |
| Foe hurt (one peak pose + one 4-frame clip, played there and back) | ~13 | 2026-10-16 |
| Front-facing 256² raid boss: still + 3 moves + idle, hurt, death, one re-roll | 136 | 2026-10-16 |
| Named champion on a shared body: attack + skill + hurt | ~20 (≈6 per 11-frame take) | 2026-10-17 |
| Smoothed kick from a cartoon reference, 19 frames, three clips | ~55 | 2026-10-15 |
| Ninja gunslinger draw-and-shoot + flying kick, with fixes | ~110 | 2026-10-22 |
| Fire-sword boss splices: 3 moves, 5 segments | 20 | 2026-10-13 |

## Frame caps

- `animate_image` (raw v3) requires an even `frame_count` and `width × height × frame_count ≤ 524,288`
  (hit 2026-10-17). Measured consequences:
  - 256×256 → `frame_count` 8 at most (9 frames with the echoed first frame).
  - 192×256 → 10 (11 frames).
  - 240×256 → 8 (9 frames).
  - 208×252 → 10 (fits when a lunge needs more room behind).
- The returned set is `frame_count + 1` images; image 0 is the first frame.
- Splicing a 4-frame clip into the fastest span of a 9-frame 256² take gives 11 frames (front-facing boss: 8 + 4
  splice = 12, one settle frame dropped → 11, 30 generations a move).

## What worked

- **Dynamic layer** (2026-10-13, one warrior attack + skill): plain Pro Flash pose wording was stiff; Pro `edit_image`
  was clearly more dynamic; Pro Flash with the four additions (dynamic exaggerated pose, stance depth, torso, secondary
  motion) matched Pro at 6–9 per pose.
- **Wind-ups**: "arm drawn back" returned an idle stance three times; naming the fist's end position and the torso
  rotation fixed it (cosmic brute backhand, three rewrites).
- **Pinned paths**: the warrior's 10-frame shield bash stood up and lifted the shield overhead halfway; re-rolling with
  "stays low and drives the shield straight forward, the shield kept at chest height the whole time" fixed it.
- **Thrusts**: the 6-frame clip between the same key poses was clean where the 10-frame one invented an overhead raise
  and three flash frames (samurai, 2026-10-21).
- **Kick**: the 10-frame chamber → kick clip retracted the leg and kicked twice and painted a white swipe; a 6-frame clip
  with "the foot never goes back to the ground" was clean (2026-10-15).
- **Colour-matching key poses first** (kyudo bow shot, 2026-10-22): clips from matched keys inherited the colours;
  matching only at the end left 10–14% drift.
- **Masked inpaint for sprite fixes** (samurai, 2026-10-21): three full text edits each fixed one thing and broke
  another; an inpaint box over the waist fixed arm, hilt and scabbard in 2 tries.
- **Lunges**: "back knee slightly bent with the back foot close under the body" + "both feet inside the canvas with a
  margin" stopped the back leg being cut (2 of 2).
- **Weapon naming**: posing from an existing frame with "the weapon is clearly a <weapon>" kept 21 of 24; adding "never
  a <the guide's other weapon>" with a guide holding the same kind of weapon kept 106 of 108 (2026-10-19).
- **Front-facing boss swipes**: naming arms by the side of the image gave all six key poses right first try (2026-10-16).
- **Recoil prompts**: adding "<weapon> still gripped in its hand" and "still facing <side>" fixed a flung bow and a
  turned beak (2 of 10 foes, 2026-10-16).

## What failed, and why

- **"No effects / no white lines / no motion trails" in the action** made flashes worse (2026-10-13): naming them invites them.
- **Naming the fire in the action** ("flames streaking along the blade") lit the whole body pale pink then white-hot,
  two re-rolls in a row (fire-sword boss, 256², 9 frames). A motion-only action kept the colours and still drew the fire
  arc. A palette snap did not help: the pale colours were the fire's own.
- **PixFlux pose edits** kept the standing pose and returned an opaque background.
- **Carried props in in-betweens** (samurai, 2026-10-21/22, 8 clips): a sheathed sword flipped to the near hip, rotated,
  reversed, or doubled in 6 of 8 clips even with correct key poses. Four tries at a far-hip sword draw put the scabbard
  across the front, reversed it, or drew 2–3 swords.
- **Pinning a prop's position** ("exactly where it was", necromancer) froze the staff while the body lunged; the arm
  stretched to twice its length to reach it.
- **Props in colours the sprite lacks**: a pink lollipop on a violet necromancer came back lavender after palette
  correction and colour matching.
- **"At the left hip"** on a right-facing samurai drew the katana across the front of the legs (the right hip).
- **Multi-stage moves undoing a step** (kyudo, 2026-10-22): the raise came back already drawn overhead and the next pose
  had the string slack at the chest, so the clip drew the bow twice.
- **Raised-arms end poses** dropped the staff or mace in about half the casters (797-sequence audit, 2026-10-17).
- **Spinning slash** turned the figure to a front view, drew the bow across the chest, and dropped the scabbard.
- **Hurt wording** "right hand goes to the hilt" twisted the torso and pulled the hilt to the near side.
- **Generated hurt in-betweens** painted a burst or darkened the body on frames 1–2 in about half the takes; 40% of
  champions' hurt takes painted smoke, a ghost, or a spark on in-betweens 1–3.
- **Washed frames**: colour matching fixes a 10–20% glow but turns a white-washed frame muddy grey.
- **White swoosh joined to a body that holds white**: no script cleared it (necromancer test).
- **Deep lunges** ignored "back foot in the same place"; one pose floated 21 px (smoke-vanish katana combo, 2026-10-22).
  On 192-wide canvases the blade tip and back foot were cut off; 256×256 was needed.
- **Front-facing boss ground snap by lowest pixel** was fooled by sparks below the crack (frames shifted 8–14 px).
- **Light timing on calm moves**: 60 ms per frame made a kyudo shot read as rushed; boss holds (4× wind-up, 3.2× hit)
  read as freezing on heroes.
- **Energy weapons** without a named flash colour got an orange-yellow gunpowder flash (laser pistol).
- **Colour-scrubbing a lit frame** stripped a pink-haired shooter's hair grey.
- **Beam and shot poses** came back with the effect painted in, even the charge pose (laser eyes, 2026-10-22).
