# Eight-Direction Moves

Read this for a top-down or 3/4 character move (attack, shot, cast) that must play in 8 facings. Managed rotation inputs are in `image-input-roles.md` (`create-character-v3`) and `preset-skeleton-template-animation.md`; per-direction smears in `weapon-effects.md`.

## Walkable Top-Down Character

A player that walks in 4 or 8 facings (tested: a 4-direction farmer, 24 generations with candidates and one redo):

1. Ask for the still **front-facing** in the first prompt (`facing the viewer, front view`), so step 1 below is not needed.
2. Rotate it: `create_character(mode="v3", reference_image_url=<still>, n_directions=4 or 8)`. Download the rotation links with `python <skill-dir>/assets/fetch.py --url <link> <out.png>` and check them on one sheet at 3x: the held prop in the same hand in every view.
3. Walk with `animate_character(mode="v3")`, one call per direction, naming every held prop in `action_description` (`walks forward at a relaxed pace, the green watering can stays in the right hand`); pass the same `animation_group_id` and `animation_name` on each call so the directions stay one animation at PixelLab. The cheaper template walk (`walking-8-frames`) has no wording: it dropped a held can, changed colours and baked a flickering shadow.
4. Record the character job with `python <skill-dir>/assets/manifest.py done <run> <job_id>` (`fetch.py` downloads image jobs only), and run the doctor per direction with `--move walk` so a loop is judged as a loop.

## Choose the route

| Route | How | Aim |
|---|---|---|
| Text | `create_character(mode="v3")` rotates the reference, then `animate_character(mode="v3")` animates each direction from `action_description` | Loose: the generator picks the arm angle. |
| Key poses | Per direction: wind-up and hit (or aim and recoil) key poses on that rotation, then interpolate between them (`end_frame_url` on `animate_character`, or `animate_image` with `first_frame_url` + `last_frame_url`) | Exact, at about two and a half times the text route's cost per direction. |

Offer **5 directions** (south, south-east, east, north-east, north) plus mirrored west, south-west and north-west, which saves about 40%. The mirror is a local derivative and the weapon switches hands on the mirrored side; ask, and generate all 8 when the game cannot accept that.

Animation cost is billed on the generated canvas, which the silhouette grows past the sprite, not on the sprite (`cost-routing.md`). Recommend 64-128 px characters for 8-direction games; a tall side-view hero sprite animates on a canvas several times as expensive.

## Steps

1. **Front-facing reference.** Re-pose the still with MCP `edit_image_pro_flash`: `the same <character>, now standing straight-on facing the viewer, front view, symmetric relaxed stance, <weapon> held at the side. Same size, same colours and pixel style, feet in the same place`, `use_color_palette_correction: true`. Whatever the reference faces becomes south.
2. **Rotate.** `create_character(mode="v3", reference_image_url=<front>, n_directions=8, view=<the game's view>)`, then `get_character` for the rotations. Check all 8 on one sheet at 3x (hair, back details, boots, the weapon in hand, `characters.md` look checklist) before animating: a drifted direction is cheapest to fix here.
3. **Animate one direction per call** and name the aim in screen terms. Never write "forward": it is read as screen-right in every direction (south, south-east, north-east and north all fired right).

   | Direction | Wording that worked |
   |---|---|
   | south | `keeps facing the viewer and raises the <weapon> straight toward the viewer, arm extended toward the bottom of the screen` |
   | north | `keeps the back to the viewer and raises the <weapon> straight ahead away from the viewer toward the top of the screen` |
   | south-east | `keeps facing down-right and raises the <weapon> toward the bottom-right of the screen, arm extended diagonally down-right` |
   | north-east | `keeps the back half-turned and raises the <weapon> toward the top-right of the screen, arm extended diagonally up-right away from the viewer` |
   | east | `raises the <weapon> with the arm extended straight to the right` |

   Even with these words text aim stays loose (north aimed up-right, diagonals fairly flat); use the key-pose route for exact angles.
4. **Finish as labelled derivatives**, listed in the plan: the generator paints its own wrong-coloured flash at the muzzle or blade; clear it, and replace a frame where the flash covers the body with the previous frame (a hold reads as weight) rather than erasing. Lay one `vfx_workbench` flash rotated to each direction, anchored on the muzzle. Pad every direction to the same frame count by holding the last pose, and keep the same smear frame count in all 8.
5. **Compare** all directions in one compass-grid preview before handing over, and build one sheet per direction (`assets/make_sheet.py`).
