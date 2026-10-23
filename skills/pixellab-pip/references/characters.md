# Characters

Read this for an explicitly requested standalone still character, candidates, colour variant or fitted prop edit. SKILL.md chooses managed character versus standalone-image routing; this page does not change that choice. A saved style supplies applicable gaps per `project-style.md`; without one follow the current request and selected route.

## Route

| Need | Route | Notes |
|---|---|---|
| Explicit Pro Flash standalone still | MCP `create_image_pro_flash` with the appropriate approved family anchor as `style_image`, when available | See `pro-flash.md` for supported sizes, costs and limits; observed detail/facing successes are scoped examples, not a new default. |
| Many candidates at once, sprite ≤170 px | MCP `create_image_pro` (4 candidates at 86-170 px) | Ignores facing; a mirrored copy is a local derivative, so ask before mirroring. |
| Cheap standalone still/draft or palette reference | MCP `create_image_pixflux` with `color_image_url` when appropriate | A palette reference influences colour; use the canonical palette routes for a hard constraint. |
| Detailed redraw of an existing sprite | MCP `create_image_pro` with `reference_images` = the old sprite and `style_copy` | Keeps the subject, sharpens the art. |
| Managed character or multiple facings | Main router and `preset-skeleton-template-animation.md`; `eight-direction.md` for requested multi-direction moves | v3 supports quadrupeds with a matching south-facing reference/template; text-only creation is humanoid-only. |

`style_image.usage_description` that worked: `match this sprite's outline weight, pixel detail, shading and palette`.

## Description

- Describe a creature, not a concept: name the body plan and the material (`a hunched giant whose whole body is a window into a starry night sky`, not `a shape made of a shattered night sky`). A robed or wrapped figure needs its body named (`two human legs hidden by the robe`).
- Name every carried prop and which hand holds it **by its look** in every prompt and every later pose: `the sword in her black-gloved hand, not the chrome arm`, and say the other hand is empty. Unnamed, the prop can change hands between poses. If candidates ignore the required hand, report the failed constraint and propose a scoped correction or an explicitly accepted alternative. Carry the approved hand consistently into later poses.
- Worn-side gear in what the viewer sees: a figure facing right shows its right side, so left-hip gear sits on the far side: `worn on the far hip: only the hilt shows in front of the sash, the scabbard end pokes out behind his back, not across the front of the legs`. Facing left, the left hip faces the viewer.
- Name every armour piece and each cloth's colour and length; they drift first in later poses (`armor-clothing.md`).
- For a full-body still add `whole body fits inside the canvas with a small margin`; omit it for requested portraits/crops.
- A bow on a front-facing figure: `held upright and vertical at the side, lower limb outside the leg`, or it crosses the thighs.
- Add a negative only when it does not contradict the request: a ranged fighter with no firearm asked for → `medieval, no guns`; stone → `no metal, no armour plates`; a bird → `not a dragon`.
- A named firearm stays a firearm: drop `medieval` and `no guns`, give it an era word that fits the look (`long black-powder rifle`, `flintlock musket`), hold it so it fits (`held diagonally across the chest in both hands, barrel pointing up, whole rifle inside the canvas`), name the rest of the kit, and add `no sword, no bow, no crossbow`. Aiming belongs to the attack's key pose, not the still.

## Candidates

Start with one candidate unless the user requested/approved a batch; `blueprints/character-candidates.blueprint.json` is an optional explicit three-candidate plan. A Pro call may itself return several. Save every returned candidate unchanged, build a numbered contact sheet (`assets/contact_sheet.py`), run the look checklist, and apply `reviewable-candidates.md`. The chosen image is this character's **canonical still** for later poses and checks. Registering/replacing a project family anchor is a separate deliberate save under `project-style.md`, using `monsters` for monsters/bosses and `heroes` for appropriate playable/NPC subjects.

## Look checklist at 3x

Pixel checks pass every fault below. Look at the sprite at 3x beside its base (the anchor, or the sprite it was edited from) and answer each item; do this again after **every** edit or inpaint of the still (recolour, added prop, fixed hand):

- Arm and hand count; each hand joined to an arm.
- Each carried prop is one piece and reads right (a sword in one straight scabbard, not a stub; one axe, not two).
- Worn props on the side they are worn; held props in the hand the description names.
- Nothing touches or is cut by the canvas edge.
- Same face, hair, armour pieces and colours as the base.

Offer a supported PixelLab fix for a failed check before deriving more poses. A localized defect can use a masked inpaint on the selected route; a figure-level defect may need a broader edit or reroll. Name the exact defect and cost in the existing approval plan. Pro Flash edit/inpaint are explicit choices under `pro-flash.md`, not universal repair upgrades. A helper pass does not establish visual approval.

## Variants

For an explicitly requested/accepted local colour variant, whole-colour-group swaps can retain shading; use `finishing.md`. Match the requested number of variants and scope of any animation recolour. Near-white may read too bright on dark armour: a muted bone/parchment option is useful when it fits the chosen look. Check for stray pixels and intentional material/effect colours.

## Add a prop

1. Pad the still unscaled so the prop fits (a long bow on the back needs room above the head; `assets/pad_sprite.py`).
2. Make a same-size mask PNG, pure white where the prop goes and black elsewhere. For a prop worn on the back, the mask is the strip behind the body, never the body itself.
3. Use the supported inpaint route with the padded still, mask and a description naming placement (`a long yumi bow carried upright on his back behind the shoulder, a quiver of white-fletched arrows`). Inspect the actual schema for input/mask fields; verify unmasked pixels rather than promising preservation from the tool name.
4. Run the look checklist. The new sprite replaces the canonical still from here on; tell the animation doctor about the taller figure by passing it as the reference.
