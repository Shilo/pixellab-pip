# Eight-Direction Moves

Read this for a top-down or 3/4 character move (attack, shot, cast) that must play in 8 facings. Managed rotation inputs are in `image-input-roles.md` (`create-character-v3`) and `preset-skeleton-template-animation.md`; per-direction smears in `weapon-effects.md`.

## Walkable Top-Down Character

A requested player walk in 4 or 8 facings (one 4-direction farmer demonstration cost 24 generations with candidates and a redo; this is not a price quote):

1. Front-facing reference and rotation as in [Steps](#steps) 1-2, with `n_directions` 4 or 8; asking for the still `facing the viewer, front view` in its first prompt skips the re-pose. Download the rotation links with `python <skill-dir>/assets/fetch.py --url <link> <out.png>`.
2. Use the requested supported animation mode/template and agreed direction scope; custom v3 motion can name held props in `action_description` (`walks at a relaxed pace, the green watering can stays in the right hand`). Group the calls with supported `animation_group_id`/`animation_name`. One template-walk example dropped a held can and changed colours; inspect held gear rather than treating that single result as a universal template failure.
3. Record completion/actual exposed usage under `usage-reporting.md`; do not mark a job finished merely because a download was attempted. Optional doctor inspection runs per direction with `--check-only --move walk`.

## Choose the route

| Route | How | Aim |
|---|---|---|
| Text | `create_character(mode="v3")` rotates the reference, then `animate_character(mode="v3")` animates each direction from `action_description` | Loose: the generator picks the arm angle. |
| Requested key poses | Per direction: reviewed wind-up/hit or aim/recoil anchors, then supported interpolation; see `animation.md` for the matching raw/managed frame fields | More explicit anchors, extra paid edits; no guarantee of exact motion or fixed cost ratio. |

When useful, offer **5 generated directions** (south, south-east, east, north-east, north) plus accepted mirrors for the other three. Mirroring switches hands/asymmetric gear; disclose that and generate the requested facings when unacceptable. It reduces direction calls, not necessarily total cost by a fixed percentage.

Animation cost is billed on the generated canvas, which the silhouette grows past the sprite, not on the sprite (`cost-routing.md`). Recommend 64-128 px characters for 8-direction games; a tall side-view hero sprite animates on a canvas several times as expensive.

## Steps

1. **Front-facing reference.** Reuse a suitable supplied/approved south-facing still. If a re-pose is actually needed, propose the supported edit route and its cost; example wording: `the same <character>, standing facing the viewer, relaxed stance, <weapon> held at the side, same size, colours and pixel style`. Do not insert a paid Pro Flash edit into every rotation request.
2. **Rotate.** `create_character(mode="v3", reference_image_url=<front>, n_directions=<agreed 4 or 8>, view=<the game's view>)`, then `get_character` for the rotations. Check every returned facing together (hair, back details, boots, the weapon in hand, `characters.md` look checklist) before animating: a drifted direction is cheapest to fix here.
3. **Animate one direction per call** and name the aim in screen terms. Never write "forward": it is read as screen-right in every direction (south, south-east, north-east and north all fired right).

   | Direction | Wording that worked |
   |---|---|
   | south | `keeps facing the viewer and raises the <weapon> straight toward the viewer, arm extended toward the bottom of the screen` |
   | north | `keeps the back to the viewer and raises the <weapon> straight ahead away from the viewer toward the top of the screen` |
   | south-east | `keeps facing down-right and raises the <weapon> toward the bottom-right of the screen, arm extended diagonally down-right` |
   | north-east | `keeps the back half-turned and raises the <weapon> toward the top-right of the screen, arm extended diagonally up-right away from the viewer` |
   | east | `raises the <weapon> with the arm extended straight to the right` |

   In the observed test, text aim stayed loose (north aimed up-right, diagonals fairly flat). For a strict angle, offer reviewed key-pose anchors as a more explicit route; verify the result rather than promising exact motion.
4. **Inspect all returned directions.** Wrong-coloured flashes may justify proposed scoped cleanup or a separately generated workbench effect. Any replacement hold, mirror, rotated effect or equal-count padding is an optional accepted derivative under `finishing.md`; keep the original direction count/order/timing when no such treatment was requested. A flash over the body is not permission to erase the body or copy a neighbour automatically.
5. **Compare** every requested direction with an appropriate standard preview; a compass grid is one useful inspection layout. Build per-direction sheets (`assets/make_sheet.py`) only when requested/required by the agreed export.
