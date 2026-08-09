# PixelLab Traditional Top-Down South-Facing Building Prompt Test Plan

Status: complete. Last reviewed: 2026-08-08.

## Goal

Find the smallest prompt and lowest-cost route that reliably produces one traditional 2D game
building sprite: shallow top-down, screen-aligned, whole building visible, and the front facade and
entrance facing south (down on the screen). The visual target is a classic handheld RPG town
building, not an isometric or three-quarter architectural illustration.

“Reliable” means the candidate passes the hard structural checks on every confirmation output in
this small operational test. It is not a guarantee about future PixelLab model versions.

## What the repository already tells us

The existing [Top-Down House Generation Routing Spike](../pixellab/pixellab-top-down-house-generation-routing-spike.md)
is the required research spike for this problem. It reports:

- 24 reviewed Pixen house outputs failed the projection check, including attempts using `high
  top-down`, `low top-down`, `south`, overhead/map/floor-plan wording, anti-isometric wording, and
  both background settings.
- User-run raw Pro text generation also failed to preserve the required house projection.
- Init-image guidance either copied the supplied geometry too literally or reverted to an
  isometric-like house.
- Pro style-reference generation was the only reported success, but its exact reference, prompt,
  seed, and outputs were not captured, so it is not yet reproducible.

Adjacent evidence narrows the test:

- [SKILL.md](../../skills/pixellab-pip/SKILL.md) treats Pixen/v3/new view and direction controls as
  weak and distinguishes raw-image generation from the structured building-kit route.
- The model benchmark rates PixFlux as the best-value model for standalone objects and Pixen as
  the weakest model for standalone objects.
- [Tilesets](../../skills/pixellab-pip/references/tileset.md) and the MCP verification results show
  `create_building_kit` produces architectural floor/wall/doorway/pillar/stair pieces in isometric
  or oblique layouts. That is a building kit, not the requested single south-facing sprite, so it
  is out of the MVP path.
- [Style Reference Generation](../../skills/pixellab-pip/references/style-reference.md) says the
  REST style-reference route derives output size from the reference and must not receive a separate
  `image_size` control.

## Hypothesis

Prompt-only generation may produce an occasional acceptable house, but it is not the leading
reliability hypothesis because the prior house sweep established a repeated projection failure.
The smallest useful experiment is therefore:

1. Run a cheap PixFlux prompt ladder to determine whether a prompt-only solution is still viable.
2. Confirm the shortest passing prompt across new seeds.
3. If prompt-only generation fails, test one neutral top-down style reference with a short prompt.
   The reference supplies the missing projection example; the prompt supplies the new building
   design and south-facing entrance.

## Fixed target and controls

Use one neutral `128x128` standalone town house for the first experiment. Keep the target constant
across prompt variants:

- one building only;
- transparent background;
- low/shallow top-down game-map view;
- front facade and entrance on the south/bottom edge, facing the camera/player;
- whole building centered and uncropped;
- readable 2D pixel-art silhouette;
- no text, labels, adjacent buildings, scene, or ground-plane composition.

Use the current route schema as the source of truth. Send `no_background: true`, `128x128`, and a
seed only when the selected route exposes those fields. Use any view, direction, isometric, or
projection control only when the current schema declares it; do not invent a field to force a route.
Hold other style controls at their defaults during the prompt test. If MCP does not expose a seed
needed for paired comparisons, use the documented REST equivalent for the experiment.

## Prompt ladder

Test the shortest structural wording first. The variants differ by one composition idea at a time;
do not add roof materials, palette, age, or decorative detail until the projection passes.

| ID | Prompt | Purpose |
|---|---|---|
| P0 | `one traditional 2D top-down game building with a south-facing entrance.` | Minimal baseline. |
| P1 | `one centered standalone traditional 2D handheld RPG town-house sprite, low top-down game-map view; whole building visible, front facade and entrance on the south side at the bottom of the image, facing the camera/player.` | Add single-subject framing, shallow camera, and an explicit screen-space south definition. |
| P2 | `one centered standalone traditional 2D handheld RPG town-house sprite, low top-down game-map view; whole building visible, roof visible from a shallow angle, screen-aligned rectangular footprint, front facade and entrance on the south side at the bottom of the image, facing the camera/player. No isometric, axonometric, diamond-grid, three-quarter perspective, horizon, or receding side walls.` | Add the anti-isometric clause and the Pokémon-like roof/front composition as a controlled final variant. |

P1 is the initial MVP candidate. P2 is a diagnostic, not an assumption that negative wording is
effective. If P1 and P2 tie, prefer P1 because it is shorter.

## Execution plan

### Phase 0: current-model sentinel

Run one current Pixen text-only sentinel with the existing house-spike target and a current route
schema. This is only a model-drift check; do not repeat the prior 24-attempt sweep. A sentinel miss
does not need another Pixen retry.

### Phase 1: cheap prompt ladder

Use MCP `create_image_pixflux` when visible, otherwise REST `POST /create-image-pixflux`.

1. Choose three positive, nonzero seeds once and use the same three seeds for P0, P1, and P2.
2. Generate `3 prompts × 3 seeds = 9` candidates.
3. Review all nine candidates in a blinded order. Record prompt ID, seed, route, dimensions,
   transparency, and each acceptance flag; do not select by aesthetic quality before projection.
4. Keep the shortest prompt whose three outputs all pass the hard structural checks. If none does,
   stop prompt-only exploration and go to Phase 2.

### Phase 1b: confirmation

If a prompt passes all three discovery seeds, run that prompt with five new, independent seeds.
Promote prompt-only generation only if all five confirmation outputs pass the hard structural
checks. A 4/5 result is promising but not reliable; do not hide the miss by selecting the best
candidate.

### Phase 2: projection-anchored style reference

Use the leading route from the existing house spike: REST `POST /generate-with-style-v2`.

1. Use one original, neutral `128x128` top-down house reference with a shallow roof, a visible
   south/bottom front facade and entrance, screen-aligned geometry, and no distinctive subject that
   must be copied. Use a user-owned, PixelLab-generated, or locally authored fixture; a locally
   authored guide is acceptable when it is declared as a projection/style control and is not
   treated as final art. Do not use a copyrighted game screenshot as the fixture.
2. Treat the image as a style/projection reference, not an init/source image. Do not use the failed
   isometric house output as the reference.
3. Because this route derives its square output from the largest style image, use a `128x128`
   reference and do not send `image_size`.
4. Test this short prompt:

   ```text
   one new town-house sprite with a different roof, windows, and facade materials; preserve the
   reference's shallow top-down, screen-aligned game-map projection, with the front facade and
   entrance on the south/bottom edge facing the camera/player; do not copy the reference's exact
   building geometry.
   ```

5. Run two independent style-reference calls. At the documented `128`-sized bucket this should
   yield eight reviewable candidates if the route returns four candidates per call. Promote the
   route only if every candidate passes the projection and south-facing checks; record any
   candidate-level miss.

The MCP `create_image_pro` style-image input is a narrower single-image alternative if REST is not
available. Do not describe it as equivalent to the REST multi-image style-reference route; record
the surface used.

### Phase 3: reserve routes

Do not spend these routes in the MVP matrix unless Phase 2 fails and the user approves the added
cost:

- Raw Pro text generation (`generate-image-v2` / `create_image_pro`) is an expensive control, not
  the first fix; the existing house spike already reports the same projection failure.
- `create_1_direction_object` is a possible managed-object comparator only if the current schema
  exposes a genuine top-down/south-facing control. It is a Pro object route and needs its own
  schema-and-cost check.
- `create_building_kit` is for connectable architectural pieces and its observed isometric/oblique
  layout is a hard mismatch for this target.

## Acceptance rubric

Score hard gates before style:

| Gate | Pass condition | Hard failure |
|---|---|---|
| Projection | Shallow top-down game-map read; roof/front relationship is readable. | Isometric diamond grid, axonometric block, or three-quarter perspective dominates. |
| South-facing front | Front facade and entrance are on the bottom/south side and face the camera/player. | Door is on a side/back edge, direction is ambiguous, or the building faces left/right. |
| Screen alignment | Main footprint and facade align to the image's horizontal/vertical axes. | Strong diagonal axes or receding side walls imply isometric/3D construction. |
| Single whole asset | One centered building is fully visible and uncropped. | Multiple buildings, scene composition, crop, or large unrelated ground plane. |
| Output integrity | Requested dimensions and transparent background are present; no text or watermark. | Wrong dimensions, opaque matte, text-like marks, or unreadable output. |

Secondary notes are palette, outline, roof/facade material, architectural charm, and variation from
the style reference. A visually attractive candidate that fails a hard gate is rejected.

## Budget and stop rules

The current pricing notes estimate roughly `$0.008` for a transparent `128x128` PixFlux image and
`$0.095` for a Pro style-reference call up to `256x256`; verify live pricing and balance before
generation.

| Phase | Calls | Approximate spend |
|---|---:|---:|
| Pixen sentinel | 1 | `$0.01` |
| PixFlux ladder | 9 | `$0.08` |
| PixFlux confirmation | up to 5 | `$0.04` |
| Pro style reference | 2 | `$0.19` |
| Planned maximum | 17 | about `$0.32` |

Stop prompt-only retries after the nine-call ladder if projection keeps failing. Do not add more
adjectives, larger prompts, or repeated negative wording after a route-level failure. Any extra raw
Pro or managed-object comparison requires a new approval because it changes the budget materially.

## Artifacts and reporting

Store the run in a named gitignored generation folder. Preserve every raw PixelLab output and the
exact request/seed metadata. Add a small review table and a contact sheet only as inspection aids;
never crop, repaint, rotate, or repair a candidate and call it a pass. If a later route succeeds,
capture the reference fixture, exact prompt, route body, seeds, candidate-level scores, and the
reason the route was selected so the existing research spike becomes reproducible.

After a successful live run, follow the normal manifest and blueprint requirements in
[SKILL.md](../../skills/pixellab-pip/SKILL.md) and its usage-reporting/blueprint references.

## Execution record (2026-08-08)

The plan was executed against the current PixelLab surfaces and model state:

| Phase | Result |
|---|---|
| Pixen sentinel | 1/1 failed; the house remained visibly angled/isometric. |
| PixFlux prompt ladder | 0/9 hard passes; P0, P1, and P2 all remained angled/isometric even with isometric: false. |
| PixFlux confirmation | Not run because no discovery prompt passed all three seeds. |
| REST style reference | 8/8 hard passes across two independent calls using a neutral locally authored 128x128 projection guide. |

The smallest reliable MVP is therefore the style-reference route plus the short variation prompt
in the [live review](../../pixellab-pip-generations/top-down-south-building-mvp-20260808/review.md).
The style-reference route produced four candidates per 128x128 call; every candidate had a
screen-aligned shallow top-down read and a south/bottom-facing front entrance. The reference
changed projection behavior without being used as an init/source image.

The run used 12 live calls and recorded 50 charged generations: 1 Pixen call and 9 PixFlux calls
at the current one-generation route pricing, plus two REST style-reference calls reporting 20
generations each. No additional raw Pro or managed-object comparison was needed.

## Follow-up execution (2026-08-08)

The follow-up isolated the projection reference from the wording:

| Test | Result |
|---|---|
| Full description, no style_description | 4/4 hard passes. |
| Short description with style_description | 4/4 hard passes. |
| Short description with projection wording and style_description | 4/4 hard passes. |
| Previously generated house used as reference | 4/4 structural passes, but 0/4 novelty passes; the outputs converged on the reference-specific architecture. |
| Minimal description, no style_description | 4/4 hard passes. |
| MCP create_image_pro style-image fallback | 4/4 hard passes in one call; useful fallback, not a new reliability sweep. |

The final MVP prompt is:

    a new traditional 2D town-house sprite with a south-facing entrance and different geometry.

Use it with a neutral screen-aligned 128x128 projection guide, REST
POST /generate-with-style-v2, no_background: true, and no image_size or style_description field.
Keep the hard structural review. The projection guide is the essential control; the prompt should
describe the desired variation without trying to force the camera through repeated negative wording.

## Reliability suite (2026-08-08)

The autonomous repeat suite tested whether the MVP generalized beyond one successful batch:

| Test | Strict passes |
|---|---:|
| Town house, base neutral guide across three new seeds | 11/12 |
| Town house, alternate neutral guide | 2/4 |
| Shop, minimal wording | 2/4 |
| Shop, explicit front-facade wording | 3/4 |
| Shop, strict front/side-wall wording | 3/4 |
| Inn, minimal wording | 2/4 |
| Inn, explicit front-facade wording | 0/4 |
| Inn, strict front/side-wall wording | 0/4 |

The suite retained 40 candidates from 10 REST calls and recorded 200 charged generations. The
base neutral guide plus the minimal prompt remains the strongest MVP, but the evidence bounds
reliability to town-house-like buildings. Shop and inn category nouns can reintroduce depth,
three-quarter views, or signage even after positive projection wording. Do not generalize this
route to arbitrary building categories without a category-specific reference and test.

See the [reliability review](../../pixellab-pip-generations/top-down-south-building-mvp-reliability-20260808/review.md)
and [run manifest](../../pixellab-pip-generations/top-down-south-building-mvp-reliability-20260808/run-manifest.json)
for the exact requests, seeds, outputs, and candidate-level notes.

## Decision after the spike

- **Prompt-only passes 5/5:** use the shortest passing prompt for this narrow building class, and
  promote it to a single canonical reference only after documenting the live evidence.
- **Prompt-only fails, style reference passes:** route hard-projection building requests through a
  projection-anchored style reference and keep the prompt short; update the existing house spike
  with the exact fixture and reproduction.
- **Both fail:** report that no reliable prompt-only solution was found for the current model state;
  test the schema-qualified managed object route or move to a user-owned reference/editor or
  approved local assembly workflow. Do not claim that more prompt wording will solve the route.

## Related documentation

- [Top-Down House Generation Routing Spike](../pixellab/pixellab-top-down-house-generation-routing-spike.md)
- [PixelLab Static-Image Model Benchmark](../pixellab-image-model-benchmark-results.md)
- [PixelLab Pixen Character Prompt Research Spike](../pixellab/pixellab-pixen-character-prompt-research-spike.md)
- [Style Reference Generation](../../skills/pixellab-pip/references/style-reference.md)
- [Image Input Roles](../../skills/pixellab-pip/references/image-input-roles.md)
- [Create Image Pro](../../skills/pixellab-pip/references/create-image-pro.md)
- [Tilesets and Building Kits](../../skills/pixellab-pip/references/tileset.md)
