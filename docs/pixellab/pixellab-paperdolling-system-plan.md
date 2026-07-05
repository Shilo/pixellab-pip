# PixelLab Paperdolling System Plan

Generated: 2026-07-04.

Goal: build a high-level PixelLab paperdolling workflow that lets users create reusable RPG equipment layers, especially animated weapons, while staying honest about what PixelLab public APIs return today. The system should start as a Python-assisted wrapper and can later evolve into a visual application.

## Product Target

Create a user-facing workflow that can answer requests like:

```text
Generate a 4-direction RPG character with an 8-frame walk, add an iron sword to the right hand, extract the sword as a reusable paperdoll layer, show me a preview, and export a Godot-ready package.
```

The system should produce:

- Base character frames.
- PixelLab equipment composites.
- Transparent equipment layer frames when extraction passes QA.
- Final composited previews.
- A manifest describing animations, directions, frame order, pivots, slots, draw order, and hardpoints.
- QA reports explaining whether the output is reusable, composite-only, or failed.
- Optional engine export helpers.

## Non-Goals

- Do not claim PixelLab returns native paperdoll layers through REST/MCP unless official docs later expose that feature.
- Do not automate undocumented website/editor/Aseprite internals or private operation URLs.
- Do not locally draw or repaint requested equipment pixels.
- Do not silently "repair" failed PixelLab output and call it final PixelLab art.
- Do not make skeleton anchoring sound deterministic before it is proven.

## Guiding Contract

Every requested visual pixel must come from PixelLab or the user. Local tooling may:

- Compare.
- Mask.
- Extract.
- Copy PixelLab/user pixels.
- Compose.
- Package.
- Preview.
- Verify.
- Export.

Local tooling may not synthesize missing equipment art or repaint broken pixels unless the user explicitly approves a labeled non-PixelLab fallback.

## MVP Workflow

```text
1. Collect or generate base character frame(s).
2. Normalize the frame contract:
   canvas, frame size, animation, direction, frame index, origin, pivot.
3. Ask PixelLab for a same-canvas equipment composite.
4. Extract changed pixels into transparent layer frame(s).
5. Run strict QA.
6. Produce manifest, previews, and final package.
7. If QA fails, recommend retry, mask/inpaint, Aseprite/editor cleanup, or composite-only output.
```

## Route Planner

| User need | First route | Fallbacks | Output label |
|---|---|---|---|
| Fast AI-generated armed/dressed animation | Generate or edit a full character spritesheet with equipment baked in | Asset-combiner workflow; first-frame video-to-sheet; managed state plus animation | `baked equipment composite`, not reusable layer |
| Single-frame fitted weapon/accessory layer | REST `edit-image` or `edit-images-v2`, then diff extraction | `inpaint-v3` with mask; Aseprite changes-only layer; second remove-character edit | `client-extracted layer` if QA passes |
| Short animated equipment layer | REST `edit-animation-v2`, then per-frame diff extraction | Per-frame `edit-images-v2`; masked per-frame inpaint; editor cleanup | `client-extracted animation layer` if temporal QA passes |
| Outfit/armor over animation | REST `transfer-outfit-v2`, then extraction only if needed | `edit-animation-v2`; managed state; composite-only | Usually `composited frames`; layer only if QA passes |
| Dressed preview/state | MCP `create_character_state` or REST `create-character-state` | Image edit routes | `managed character variant` or `composite` |
| Managed base animation | MCP `animate_character`; REST `characters/animations` | REST v3/pro custom animation | `base animation frames` |
| Skeleton/hardpoint metadata | REST `estimate-skeleton` on base frames | Manual hardpoints; Aseprite/editor keypoint workflow | `hardpoint metadata`, not layer |
| User already works in Aseprite | Visible Aseprite image-edit changes-only layer workflow, then verify/export | REST composite + extraction | `editor-verified layer` |

## AI Workflow Planner

Separate "AI-assisted sprite production" from "reusable paperdoll layer production." The first is allowed to bake equipment into a finished animation. The second must pass layer extraction and QA.

AI-assisted composite routes:

- Reference-to-spritesheet: start from a base/reference character and generate the full armed/dressed animation. Use when the user wants a finished character state quickly.
- Asset-combiner bake-in: generate or import a weapon, place it onto a representative frame, then animate the combined character+weapon image. Use when the weapon should move naturally with the body and layer reuse is not required.
- First-frame video-to-sheet: generate guided video from a character frame, extract key poses, and assemble a spritesheet. Use for motion exploration, not for reusable paperdoll layers.
- Managed state plus animation: create a dressed/armed managed character state, then animate that state. Use when PixelLab managed character consistency matters more than layer reuse.

AI-assisted reusable-layer routes:

- Same-canvas edit plus extraction: default when a reusable layer is required.
- Masked inpaint/edit plus extraction: preferred when the target region is small or body preservation matters.
- Editor changes-only layer: preferred when the user is already in Aseprite/Pixelorama and can verify the layer visually.
- Two-pass add/remove: fallback only; label as AI-extracted candidate until QA proves it is clean.

Workflow decision:

```text
Does the user need equipment to be swappable at runtime?
  yes -> reusable-layer route with extraction, manifest, and QA
  no  -> baked composite route is acceptable and often faster

Does the equipment need to animate with hands/limbs?
  yes -> use animation edit, asset-combiner bake-in, or hardpoint-assisted extraction
  no  -> single-frame edit/extraction may be enough

Does the user need hidden/behind-body equipment pixels?
  yes -> require front/back masks, editor layer workflow, or manual art; diff extraction cannot recover invisible pixels
  no  -> same-canvas extraction can work when QA passes
```

## Aseprite-Parity Changes-Only Workflow

Use the Aseprite extension's `New layer with changes` behavior as the product benchmark, but implement the portable route from public PixelLab outputs.

Current evidence:

- PixelLab's public docs list `New layer with changes` as an editor output method.
- The installed Aseprite extension sends `output_method` through its extension request JSON and prepares a dedicated PixelLab generation layer/cel for `New layer with changes`.
- The installed extension appears to place returned bytes into Aseprite cels; local per-pixel base-vs-result subtraction was not found in the Lua placement path.
- Public REST v2 schemas for the relevant edit routes do not expose `output_method`.

Portable implementation:

```text
1. Call a documented PixelLab route and save the returned composite.
2. Load base and composite as same-size RGBA arrays.
3. Run exact-diff extraction as the fast path.
4. Run tolerant alpha-aware extraction when minor AI drift is present.
5. Reject if body drift, palette drift, unrelated redraw, or full-sprite changes exceed limits.
6. Copy accepted pixels from the PixelLab composite into a transparent layer PNG.
7. Recompose base + layer and compare against the composite.
8. Generate preview artifacts and a manifest entry that names the output `client-extracted`.
9. Optionally assemble an `.aseprite` review file with base, composite, extracted layer, mask, and heatmap layers.
```

Do not:

- Send `output_method` to public REST unless official REST documentation later exposes it.
- Automate the Aseprite extension's private operation URL.
- Depend on the user's Aseprite preferences or request history.
- Use `Modify current layer, only changes` as an automated route because it is editor-specific and in-place.

The optional Aseprite workspace exporter should use only documented Aseprite CLI/Lua APIs: open or create sprites, create transparent layers, create cels, draw the PNG layers, add frame tags, save a copy, and leave the user's source files untouched.

## CLI Prototype

Start with a small Python CLI under `dev-tools/` after the docs are approved.

Possible commands:

```powershell
python dev-tools/paperdoll.py init `
  --base "base/frame-000.png" `
  --animation idle `
  --direction south `
  --slot weapon `
  --item iron_sword

python dev-tools/paperdoll.py extract `
  --base "base/frame-000.png" `
  --composite "composites/iron-sword/frame-000.png" `
  --slot weapon_front `
  --expected-region hand_r `
  --out "paperdoll-pack"

python dev-tools/paperdoll.py preview `
  --pack "paperdoll-pack" `
  --checkerboard-inspection

python dev-tools/paperdoll.py verify `
  --pack "paperdoll-pack"

python dev-tools/paperdoll.py assemble-aseprite `
  --pack "paperdoll-pack" `
  --out "paperdoll-pack\\exports\\aseprite\\iron-sword-review.aseprite"
```

Generation calls can be added after the local extraction/QA is proven:

```powershell
python dev-tools/paperdoll.py generate-composite `
  --route edit-image `
  --base "base/frame-000.png" `
  --prompt "add an iron sword held in the right hand" `
  --out "paperdoll-pack"
```

## Package Layout

```text
paperdoll-pack/
  paperdoll.json
  base/
    walk/south/frame-000.png
    walk/south/frame-001.png
  composites/
    weapon_iron_sword/walk/south/frame-000.png
  layers/
    weapon_iron_sword/front/walk/south/frame-000.png
    weapon_iron_sword/back/walk/south/frame-000.png
  previews/
    final-contact-sheet.png
    layer-contact-sheet.png
    blink.gif
    mask-overlay.png
  qa/
    report.json
    diff-heatmap-frame-000.png
    rejected-components-frame-000.png
  exports/
    godot/
    unity/
    phaser/
    pixi/
```

## Manifest Sketch

```json
{
  "version": 1,
  "created_at": "2026-07-04",
  "character": {
    "name": "rpg_player",
    "source": "pixellab",
    "canvas": { "width": 92, "height": 92 },
    "pivot": { "x": 46, "y": 74 },
    "view": "low top-down"
  },
  "animations": [
    {
      "name": "walk",
      "fps": 8,
      "directions": ["south", "east", "north", "west"],
      "frame_count": 8,
      "frame_order": "source"
    }
  ],
  "slots": [
    { "name": "weapon_back", "z": -10 },
    { "name": "body", "z": 0 },
    { "name": "weapon_front", "z": 20 }
  ],
  "items": [
    {
      "id": "weapon_iron_sword",
      "slot": "weapon_front",
      "source_route": "rest.edit-image",
      "layer_type": "client-extracted",
      "qa": "passed"
    }
  ],
  "hardpoints": {
    "walk/south/frame-000": {
      "hand_r": { "x": 53, "y": 51, "angle": 30 },
      "weapon_tip": { "x": 69, "y": 38 }
    }
  }
}
```

## Python Extraction Module

Suggested modules:

```text
dev-tools/paperdoll/
  __init__.py
  cli.py
  image_io.py
  extract.py
  drift.py
  components.py
  temporal.py
  preview.py
  manifest.py
  report.py
```

Core responsibilities:

- `image_io.py`: load/save RGBA, assert same size, preserve transparency.
- `drift.py`: alpha/luma drift checks; fail before extraction when body moves.
- `extract.py`: alpha-aware diff mask and layer copy.
- `components.py`: connected component filtering and expected-region scoring.
- `temporal.py`: frame-to-frame bbox, centroid, area, IoU, and component stability.
- `preview.py`: contact sheets, blink GIFs, mask overlays, diff heatmaps.
- `manifest.py`: package metadata and engine export hints.
- `report.py`: machine-readable and human-readable QA summaries.

Extraction modes:

- `exact`: copy pixels where premultiplied RGBA differs exactly; useful for synthetic fixtures and editor-clean composites.
- `tolerant`: seed from high-confidence RGB/alpha differences, grow into nearby low-confidence differences, then filter components.
- `masked`: constrain extraction to a user/provided or skeleton-derived region with configurable padding.
- `review`: keep uncertain components in a rejected/needs-review overlay instead of silently discarding them.

Aseprite parity output:

- Transparent equipment PNGs remain the canonical portable assets.
- `.aseprite` files are review workspaces, not the only source of truth.
- The exporter should be copy-on-write and should never modify the artist's open source file in-place.

## QA Gates

Gate 1: Input contract

- Same dimensions.
- Same frame count/order.
- Same direction names/order.
- Same origin/pivot or explicit correction.
- Transparent background preserved.

Gate 2: Base preservation

- No whole-body shift.
- No subpixel drift.
- No unrelated body/face/limb redraw outside expected region.
- No global palette or shadow drift.

Gate 3: Layer plausibility

- Nontransparent bounds overlap expected region or hardpoint.
- Component count plausible for item type.
- Area is neither tiny noise nor full-body duplicate.
- No edge-connected background junk.
- No loose unregistered prop unless user asked for detached prop.

Gate 4: Round-trip

- `base + layer` matches PixelLab composite within threshold.
- Outside-mask pixels match the base.
- Final preview reads as the requested equipment attached to the character.

Gate 5: Animation

- Frame count/order unchanged.
- Layer does not flicker or disappear.
- Bbox/centroid movement follows base motion.
- Component count changes only when expected by the animation.
- Preview GIF preserves frame order and transparency.

Gate 6: Aseprite parity

- Exported layer PNGs align to the same canvas origin as the base.
- Optional `.aseprite` workspace contains separate base, composite, extracted layer, and QA layers.
- Re-exporting the Aseprite review layer produces the same transparent PNG bytes or an explicitly documented equivalent.
- Editor-only outputs are labeled `editor-verified`, not `client-extracted`.

## Prompting Strategy

For same-canvas extraction, prompts should be strict and body-preserving:

```text
Edit this south-facing RPG character sprite. Add only an iron sword held in the right hand, angled slightly down and forward, with the handle overlapping the hand. Keep every existing body, face, limb, outline, pose, canvas pixel, and transparent background unchanged except where the sword naturally covers the hand. Do not redraw the character, do not move any body parts, and do not create a loose detached sword.
```

For animation:

```text
Add the same iron sword to the right hand in every frame. The sword follows the hand motion and keeps the same scale, palette, and outline style. Preserve frame count, frame order, canvas size, transparent background, body pose, face, limbs, and all base pixels except where the sword naturally occludes the hand.
```

Prompt builder inputs:

- Base identity.
- Direction.
- Animation name and frame count.
- Target equipment.
- Body side and region.
- Occlusion rule.
- Placement/angle/scale.
- Preservation rule.
- Negative constraints for duplicate body, loose parts, body redraw, background, and palette drift.

For baked AI composite workflows, prompts can prioritize the final animation instead of base-pixel preservation:

```text
Create an 8-frame south-facing RPG walk cycle of this character holding the same iron sword in the right hand. The sword moves naturally with the hand, keeps the same scale and outline in every frame, and remains readable at sprite size. Keep the character identity, palette, transparent background, and frame grid consistent.
```

For masked AI workflows, prompts should explicitly honor the mask:

```text
Modify only the masked hand-and-weapon area. Add an iron sword held in the right hand, with the handle under the hand and blade angled down-forward. Keep unmasked pixels unchanged. Keep transparent background, original pose, and original character silhouette.
```

## Skeleton And Hardpoint Phase

Add skeleton support after the base extraction CLI works.

Phase behavior:

1. Run `estimate-skeleton` on base frames or representative frames.
2. Normalize returned keypoints into manifest hardpoints.
3. Map labels to practical anchors such as hands, head, torso, feet, and weapon direction.
4. Use anchors to:
   - generate better prompts,
   - build expected-region masks,
   - reject components far from the intended attachment,
   - export engine hardpoints,
   - preview weapon alignment.

Risks:

- Keypoint labels may not map cleanly to tiny/chibi sprites.
- One estimated pose is not a full motion sequence.
- Top-down hand positions may be ambiguous.
- Hardpoint data helps validation, but the art layer still comes from PixelLab composites and extraction.

## Engine Export Plan

Generic export first:

- Transparent PNG frames.
- Composited PNG frames.
- `paperdoll.json`.
- Contact sheets and QA report.

Atlas packing discipline (when the exporter packs frames into a sheet):

- Trim transparent borders only if `source_size` and `sprite_source_size` are stored so the runtime can reconstruct untrimmed placement; store pivots in untrimmed frame space.
- Add 1-2 px border padding and 1 px extrude to stop neighbor bleed and edge flicker.
- Leave atlas rotation off unless the target loader supports rotated regions.
- Keep atlas max size conservative (2048; 4096 only when the target is validated); use duplicate-frame detection to save area.
- These are starting points; a project overrides them once its target platform, texture budget, and loader are known. GPU texture compression (KTX2/Basis, ASTC/ETC2/BC) is a per-target concern left to the specific adapter, not the generic export.

Then add engine adapters:

- Godot: JSON manifest plus folder layout for layered `AnimatedSprite2D`/`Sprite2D` children; optional GDScript sample that drives all layers from one animation state.
- Unity: sliced PNG/atlas metadata plus Sprite Library category/label mapping; document Sorting Group/root sorting assumptions.
- Phaser: atlas JSON and animation config for synchronized layer sprites in a container/layer.
- PixiJS: spritesheet JSON and animation arrays for one `AnimatedSprite` per layer or manual shared-frame driving.
- Aseprite: `.aseprite` workspace assembly only after existing Aseprite CLI contract is followed and output is copy-on-write.

## Implementation Phases

### Phase 0: Documentation And Contract

- Keep research in `docs/pixellab/`.
- Keep `paperdolling.md` as the current agent contract until the workflow is implemented.
- Add a short future update to `paperdolling.md` only after the prototype proves exact QA language.

Exit criteria:

- Research doc and plan doc exist.
- Open questions and route boundaries are explicit.

### Phase 1: Local Extraction Prototype

- Build `dev-tools/paperdoll.py` or `dev-tools/paperdoll/`.
- Inputs are local base/composite PNG files only.
- Output transparent layer, composite preview, diff heatmap, mask overlay, and QA JSON.

Exit criteria:

- Passing sample extracts a layer without altering pixels.
- Failing sample reports why it is not reusable.
- Unit tests cover dimension mismatch, no-change, body drift, noisy diff, and successful extraction.

### Phase 2: Paperdoll Package Manifest

- Add `paperdoll.json` creation.
- Support multiple frames and directions from local files.
- Add contact sheets and blink GIF previews.

Exit criteria:

- Package is self-describing.
- Preview artifacts are generated and clearly labeled.
- Checkerboards never appear in final assets.

### Phase 3: PixelLab REST Integration

- Add optional generation calls for `edit-image`, `edit-images-v2`, `inpaint-v3`, and `edit-animation-v2`.
- Require `PIXELLAB_SECRET` from local env/app settings, never chat.
- Save job IDs, route, prompts, seed, and usage details when available.
- Keep one candidate first unless the user approves batch spending.

Exit criteria:

- The tool can generate a composite, poll, extract, and package.
- Failed QA recommends route-specific retry/mask/editor options.

### Phase 4: Animated Equipment

- Support 2-16 frame sequences.
- Add temporal QA.
- Add frame-grid import/export and source-order preservation.
- Experiment with `edit-animation-v2` versus per-frame edit routes.
- Compare reusable-layer extraction against baked AI composite routes so the tool can recommend the honest cheaper/faster option when layer reuse is unnecessary.

Exit criteria:

- A short walk/idle equipment layer can pass or fail with clear evidence.
- Temporal jitter is detected before a layer is called reusable.
- Baked composite outputs are labeled separately from reusable layer packages.

### Phase 5: Hardpoints And Skeleton Metadata

- Add optional `estimate-skeleton`.
- Store keypoints and derived hardpoints in the manifest.
- Use hardpoints to create expected-region masks and QA bounds.

Exit criteria:

- Hardpoints improve rejection of loose equipment and wrong-hand placement.
- The docs clearly state hardpoints are metadata, not a deterministic layer renderer.

### Phase 6: Engine Exporters

- Implement generic export first.
- Add Godot, Unity, Phaser, and Pixi adapters one at a time.
- Keep exporters data-only and sample-code-oriented.

Exit criteria:

- Each exporter has a minimal working sample or import guide.
- Sorting/layer-order assumptions are documented.

### Phase 7: Visual App Spike

- Build only if the CLI proves useful but QA needs human visual decisions.
- Candidate UI: local browser app or desktop editor helper.
- Include mask editing, component accept/reject, blink previews, timeline, layer order, and hardpoints.

Exit criteria:

- Manual correction points are faster and clearer than CLI-only iteration.

## Test Plan

Unit tests:

- RGBA load/save preserves dimensions and alpha.
- Base/composite size mismatch fails.
- Empty diff fails with "no equipment detected."
- Simple known pixel addition extracts exactly those pixels.
- Exact-diff extraction preserves only changed pixels.
- Tolerant extraction removes similar body pixels while keeping real equipment edge pixels.
- Masked extraction rejects components outside the intended hand/head/torso region.
- Body drift fails before extraction.
- Tiny noise components are rejected.
- Full-body redraw is rejected by area/body-overlap heuristics.
- Round-trip composite matches expected output.

Animation tests:

- Frame count mismatch fails.
- Reordered frame names fail unless manifest order overrides.
- One-frame missing equipment fails temporal QA.
- Jittering equipment bbox fails temporal QA.
- Stable multi-frame layer passes.

Golden fixtures:

- Synthetic RGBA squares for deterministic masks.
- User/PixelLab sample frames stored under `.local/` or a dedicated test fixture folder only when licensing permits.
- Aseprite parity fixture with base, composite, expected changes-only layer, and optional `.aseprite` review export.

## Agent Skill Update Criteria

Update `skills/pixellab-pip/references/paperdolling.md` only after Phase 1 or Phase 3 proves the language. Candidate durable additions:

- Name "client-extracted layer" as the output label for same-canvas diff workflows.
- Name "baked equipment composite" as the output label for AI-generated armed/dressed spritesheets that are not reusable layers.
- Require drift detection before layer extraction.
- Require temporal QA before calling animated equipment reusable.
- Treat skeleton hardpoints as metadata/QA, not native layer generation.
- Prefer one PixelLab edit plus extraction over a second remove-character edit when layer extraction passes.
- Keep two-edit remove-character as an explicit fallback, not the default.

## Prior Art: PixelLab AI Skill

Reviewed 2026-07-05 (v1.5.5). See the research spike's "PixelLab AI Skill Paperdolling Approach (Reference)" section for the full inventory. Mapping their shipped artifacts onto this plan's phases:

| Their artifact | Maps to this plan | Notes |
|---|---|---|
| `validate-sprites` file-checker (frame set/order match vs reference layer, per-frame PNG-header size) | A subset of Gate 1 (Input contract), runnable in Phase 1 / Phase 2 QA and manifest checks | Validates already-separated layer files by filename and header size only. Does not read pixels, so it is not Gate 2-4 and does not replace extraction. |
| `transfer-outfit-v2` → `edit-animation-v2` "remove the body" pipeline | Route Planner "composite routes" and the AI Workflow Planner two-pass add/remove fallback | A second generative pass, not the reusable-layer extraction route. Keep it labeled fallback, not default. |
| `modular-rpg-character` recipe `sprite_contract` / `qa` fields | Phase 2 manifest shape (`paperdoll.json`) and Gate 1 input contract | A compact machine-readable contract worth mirroring; their `qa` entries are prose, not executable gates. |
| `estimate-skeleton` / `animate-with-skeleton` example payloads | Phase 5 skeleton/hardpoint inputs | Example payloads only; no hardpoint derivation or manifest on their side. |

Smallest safe first borrow: a `validate-sprites`-style checker. It is a few lines of deterministic file/header checks, maps directly onto Phase 1's exit criteria (dimension-mismatch and frame-order tests over local PNGs), and needs no PixelLab calls. It validates already-separated layer files, so it complements — it does not replace — the Phase 1 extraction core, the drift/temporal/round-trip QA (Gates 2-5), or the reusable-vs-composite labeling. Adopting it early gives a shipped, testable QA surface while the extraction algorithm is still being proven.

## Provenance And Licensing

Shipped AI-generated art carries provenance and licensing weight this plan should surface, not resolve:

- The operative license for Pip output is PixelLab's own terms of service. The wrapper must not assert copyright ownership or licensing guarantees on the user's behalf.
- Keep a provenance log per item: route, prompt, seed, model/mode, job/asset IDs, and usage. The manifest already records `source_route`; Phase 3 already saves prompt/seed/usage, so extend the item entry with those when available.
- If the user ships to a platform with AI-content rules (for example Steam's pre-generated and live-generated AI disclosure), that disclosure is the user's responsibility; the tool can note it but does not file it.
- General AI-copyright guidance (e.g., the 2025 U.S. Copyright Office position that AI output is protectable only with sufficient human authorship, not from prompts alone) is context for users, not a gate the wrapper enforces.

Keep this as user-facing context and provenance hygiene, not a compliance engine.

## Main Risks

- PixelLab edits may redraw the base body too often for reliable extraction without masks.
- Held weapons can cross in front of and behind body parts, requiring front/back split layers or manual masks.
- Tiny sprites make hand anchors and skeleton estimates ambiguous.
- Some equipment is partially occluded in the composite, so the invisible part cannot be recovered by differencing.
- Animation edits can keep style consistency but still produce frame-to-frame jitter.
- Engine-specific import expectations can consume more work than the extraction prototype.

## Recommended Immediate Next Step

Build Phase 1 as a local, no-PixelLab-call prototype using hand-picked base/composite PNG pairs. This proves the deterministic core before spending credits or expanding the agent contract.
