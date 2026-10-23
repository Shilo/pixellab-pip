# Characters

Read this for a single still character sprite (hero, NPC, monster, boss, portrait), picking among candidates, a colour variant of a sprite, or adding a prop to one. Managed 8-direction characters and animation live in their own references; this page covers the still that every pose and move inherits. Look words, sprite size and anchor sprite come from the project style (`project-style.md`, examples in `style-examples.md`), never from this page.

## Route

| Need | Route | Notes |
|---|---|---|
| Side-view hero, NPC, monster or boss still (default) | MCP `create_image_pro_flash` with `style_image` = the project's anchor sprite and `no_background: true`; a new project with no anchor yet sends text only, then registers the picked still (`project_style.py anchor heroes <still.png>`) | Tested best on detail, brief and facing; it follows "facing left/right" in the text. Width and height are multiples of 4, 16-256. |
| Many candidates at once, sprite ≤170 px | MCP `create_image_pro` (4 candidates at 86-170 px) | Ignores facing; a mirrored copy is a local derivative, so ask before mirroring. |
| Cheap draft or a forced palette from an image | MCP `create_image_pixflux` with `color_image_url` | Flat; the palette image changes colours. Drafts only. |
| Detailed redraw of an existing sprite | MCP `create_image_pro` with `reference_images` = the old sprite and `style_copy` | Keeps the subject, sharpens the art. |
| A game that needs 8 facings | `eight-direction.md` | `create_character(mode="v3")` from text is humanoid-only and draws a thin side profile. |

`style_image.usage_description` that worked: `match this sprite's outline weight, pixel detail, shading and palette`.

## Description

- Describe a creature, not a concept: name the body plan and the material (`a hunched giant whose whole body is a window into a starry night sky`, not `a shape made of a shattered night sky`). A robed or wrapped figure needs its body named (`two human legs hidden by the robe`).
- Name every carried prop and which hand holds it **by its look** in every prompt and every later pose: `the sword in her black-gloved hand, not the chrome arm`, and say the other hand is empty. Unnamed, the prop changes hands between poses. Side-view generators favour the near hand for a long prop: when every candidate ignores the named hand, keep the hand they drew and name that hand in every later pose.
- Worn-side gear in what the viewer sees: a figure facing right shows its right side, so left-hip gear sits on the far side: `worn on the far hip: only the hilt shows in front of the sash, the scabbard end pokes out behind his back, not across the front of the legs`. Facing left, the left hip faces the viewer.
- Name every armour piece and each cloth's colour and length; they drift first in later poses (`armor-clothing.md`).
- Always add `whole body fits inside the canvas with a small margin`; without it limbs and weapons are cut.
- A bow on a front-facing figure: `held upright and vertical at the side, lower limb outside the leg`, or it crosses the thighs.
- Add a negative only when it does not contradict the request: a ranged fighter with no firearm asked for → `medieval, no guns`; stone → `no metal, no armour plates`; a bird → `not a dragon`.
- A named firearm stays a firearm: drop `medieval` and `no guns`, give it an era word that fits the look (`long black-powder rifle`, `flintlock musket`), hold it so it fits (`held diagonally across the chest in both hands, barrel pointing up, whole rifle inside the canvas`), name the rest of the kit, and add `no sword, no bow, no crossbow`. Aiming belongs to the attack's key pose, not the still.

## Candidates

Submit a few seeds of one description as one approved batch (`blueprints/character-candidates.blueprint.json`), or one Pro call when it returns several. Save every candidate unchanged, build a numbered contact sheet at 3x (`assets/contact_sheet.py`), run the look checklist on each, and let the user pick per `reviewable-candidates.md`. The pick is the **canonical still**: pads, colour matching, ground lines and the animation doctor's reference all use it.

## Look checklist at 3x

Pixel checks pass every fault below. Look at the sprite at 3x beside its base (the anchor, or the sprite it was edited from) and answer each item; do this again after **every** edit or inpaint of the still (recolour, added prop, fixed hand):

- Arm and hand count; each hand joined to an arm.
- Each carried prop is one piece and reads right (a sword in one straight scabbard, not a stub; one axe, not two).
- Worn props on the side they are worn; held props in the hand the description names.
- Nothing touches or is cut by the canvas edge.
- Same face, hair, armour pieces and colours as the base.

A fail is fixed by PixelLab, never by a local repaint, and it is a paid call under the approval gate. A wrong detail (a hand, a strap, a prop) is a masked inpaint (`inpaint_image_pro_flash`) over that area: text edits fix one part and break another. A wrong figure (extra limb, wrong proportions, wrong pose) is a re-roll with MCP `edit_image_pro_flash` naming the fix (`exactly two arms, left hand on the hilt`, `one long straight scabbard at the far hip`). A fault in the still is inherited by every move, so fix it before any pose.

## Variants

A colour variant swaps whole colour groups of the still locally, shading kept; it is a labelled derivative, not new PixelLab art. Offer 3-5 variants side by side at 3x and let the user pick; recolour animation frames with the same swaps so a whole set matches. Near-white reads too bright on dark armour: offer a muted bone or parchment tone instead. Check at 3x for stray pixels the swap missed.

## Add a prop

1. Pad the still unscaled so the prop fits (a long bow on the back needs room above the head; `assets/pad_sprite.py`).
2. Make a same-size mask PNG, pure white where the prop goes and black elsewhere. For a prop worn on the back, the mask is the strip behind the body, never the body itself.
3. MCP `inpaint_image_pro_flash` with the padded still, the mask (`mask_image_url` or `mask_image_base64`) and a description naming the prop, where it sits and how it is worn (`a long yumi bow carried upright on his back behind the shoulder, a quiver of white-fletched arrows`). Unmasked pixels come back unchanged.
4. Run the look checklist. The new sprite replaces the canonical still from here on; tell the animation doctor about the taller figure by passing it as the reference.
