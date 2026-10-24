# Mace, club and flail (one-handed mace, mace and shield, two-handed flails) as visible poses

Optional pose/rhythm examples for selected choreography; execution scope follows `key-pose-animation.md`, and local operations follow `finishing.md`.

Left-facing plates are mirrored. Facing right throughout: right hand, right foot and the near side face the viewer.
The horizontal swing comes from the sprite sheet only; no historical source shows it frame by frame.

## What every mace pose keeps
- **The head is the weight.** In every raise the head of the club sits above and behind the hand, never level
  with it; the hand leads into the strike, the head arrives last. Say `the mace head above and behind his fist`.
- **Wide, low stance, and it gets wider on the hit.** Talhoffer's club fighters stand with the feet nearly two
  shoulder widths apart, knees bent, and lunge further on the blow: `very wide stance, front knee deeply bent over
  the right foot, back leg straight, body weight thrown forward`.
- **Same head size as the idle.** Name it every pose: `the same large flanged mace head as in the original,
  full size`. Interpolated frames shrink it first when it turns toward or away from the viewer.
- **Straight handle.** `straight rigid wooden handle`; wide arcs make the generator bow it like a whip.

## Stances and wind-ups (visible description for the prompt)
| Pose | Visible description | Use |
|---|---|---|
| Shield-up stance | `tall shield held upright in front of his body by the left hand, mace held short and upright behind the shield edge, crouched behind it` | idle / guard with shield |
| Low trailing club | `mace hanging low behind him at his right side, head near the back knee, shield pushed forward` | rising or swinging strike wind-up |
| High raise | `right arm straight up, fist above the head, mace head pointing up and back toward the upper left` | overhead wind-up (the common one) |
| Cocked over the shield | `fist beside the right ear, elbow high, mace head pointing forward over the top of the shield` | short chop over a shield |
| Flail high guard | `both hands on a long staff raised diagonally above his head, front hand higher, the spiked head hanging straight down from the far end of the staff behind him` | two-handed flail idle / wind-up |

## Moves as animations (key pose A -> key pose B, trail and effect)
- **Overhead strike (mace):** A = high raise -> B = `arm extended forward and down, mace head at the enemy's head
  height or lower, toward the right side of the image, torso leaning over the front knee`. Trail: a tall crescent
  from above and behind the head, over the top, down in front (`swing_slash` or `blade_trail.py` with the head as
  the tracked point). Impact: `hit_star` on contact, `crater_dust` + `shockwave_ring` if it reaches the ground.
  Interpolation is fine for this one; hold A 2-3 frames.
- **Raise-strike with shield:** A = shield-up stance -> B = high raise with the shield pushed forward -> C = the
  overhead strike over the shield's top edge. Keep three key poses (stepped), the shield in the same spot in all
  three: `shield stays in his left hand, upright in front of his chest, same size and place in every frame`.
- **Horizontal swing (sprite rhythm):** A = mace pulled back behind the hip, head hidden behind the body ->
  B = `right arm fully extended toward the right side of the image at shoulder height, mace head level with the
  shoulder`. The middle frames turn the head toward the viewer (foreshortened); generate those as stepped key
  poses, not interpolation, or the head vanishes. Trail: a flat ellipse at waist-to-shoulder height,
  `slash_trail`; one `hit_star` at the tip in B.
- **Low sweep (flail):** A = flail high guard -> B = `bent forward over the front knee, staff angled down toward
  the lower right, the spiked head skidding along the ground ahead of his front foot`. Trail: a low arc ending at
  floor level; `crater_dust` + `debris_burst` where the head scrapes. Stepped key poses.
- **Forward flail strike:** A = staff pulled back to the right shoulder -> B = `both arms straight out, staff level
  at chest height, the striking bar swinging past the end of the staff toward the right side of the image`.
- **Block-catch (shield):** idle -> `shield pushed forward to the right, catching a blow near its top, mace held low
  behind him` (hold ~200 ms) -> idle; `spark_burst` (or a dull `debris_burst` for wood) on the shield face. The
  close-in catch (Talhoffer pl.126) is `left hand grabbing the enemy's mace near its head, own mace raised` - a
  grapple frame, no trail.
- **Cross-block (two-handed flail or staff):** `staff held in both hands and angled up across the front of his
  face, crossing the enemy's staff in an X at head height` - one held pose, `spark_burst` at the cross. The
  overhead block is `both hands above the head, staff horizontal, the flail head hanging straight down behind`.

## The flail chain (the hard case)
- The striking part always **lags behind the handle**: on the wind-up it hangs down from the staff end; during the
  swing it trails the staff's path; it catches up and passes the staff only at B. The weighted veil in Talhoffer
  behaves the same way: `cloth stretched taut from her raised fist, the stone hanging out behind it to the right`.
- Interpolation straightens the chain or deletes it. Use stepped key poses for every frame where the head changes
  side relative to the staff, and name it: `a short chain links the staff end to the spiked head; the chain and
  the head are visible`.
- Or draw the staff only in the animation and add the head and chain as an overlay with `pixelart_workbench`
  (rigid handle, the head trailing one frame behind the staff tip).

## Frame rhythm (from the LPC mace slash, 6 frames per direction)
- Rest (head hanging low in front) -> pulled back behind the body -> crossing the belly -> coming forward
  (foreshortened) -> arm straight out, head at the tip (the hit) -> recover with the arm lifting.
- For heavier weapons stretch it: hold the wind-up 2-3 frames, ONE fast swing frame, hold the impact 2 frames
  (with the effect), then 3-4 slow recovery frames with the head sinking low before returning to idle. Heavy
  follow-through ends lower than the hit: `mace head dropping below the waist after the blow`.

## Canvas notes
- The high raise adds about a third of the body height above the head; the flail high guard and the low sweep
  need room above and to the right. Pad the canvas before the edit (top and right) so the head isn't clipped.

## Pitfalls to name in prompts
- Head shrinks in turned or interpolated frames -> `same large mace head as in the original, full size`.
- Chain or flail head vanishes -> stepped key poses + `the chain and the spiked head are visible`.
- Handle bends on wide arcs -> `straight rigid wooden handle`.
- Shield drops, shrinks or moves to the other arm -> `shield stays on his left arm, in front of his chest, every
  frame`; check each key pose and in-between at 3x.
- Two-handed flail loses the back hand -> `both hands on the staff`.
