# PixelLab Oversized Background Animation Spike

Last reviewed: 2026-07-15.

Purpose: record live findings for animating a background image far larger than `animate-with-text-v3`'s `256x256` input cap, by looping selected regions independently and compositing them back at their exact source offsets. Covers region selection, the chunk-boundary seam problem, loop closure via `first_frame`/`last_frame`, prompt failure modes, GIF palette handling, and the Aseprite layer/composition build. This is developer research, not the canonical runtime contract.

Source case: one `1672x941` flat pixel-art forest title screen (characters, foliage, waterfall, glowing mushrooms, a magic orb), animated as a subtle ambient loop. Ten regions, 14 paid jobs.

Local run outputs (not committed showcase assets) are in the `pixellab-pip-generations/forest-survivors-title-loop/` run folder: the source image, the ten `256x256` crops sent as `first_frame`/`last_frame`, every returned frame per region, the eight composited `1672x941` frames, the looping GIF, per-region and composite spritesheets, ten per-region `.aseprite` files plus the layered composition, the four rejected orb iterations, the plan, and the run blueprint and manifest.

## Bottom Line

A background larger than `256x256` can be animated by **looping regions, not the image**. The pattern that worked:

1. Measure each candidate subject's bounding box in the source. Only animate subjects that **fit inside `256x256`**.
2. Crop each region at an **integer offset**; never resize.
3. Send the crop as **both `first_frame` and `last_frame`** — this closed the loop exactly on 10 of 10 jobs.
4. Composite each region back at that same offset **through a feathered mask covering only its moving subject**, never as a raw rectangle.
5. Assert that compositing the unmodified crops reproduces the source byte-for-byte before spending anything.

The single most important finding: **`animate-with-text-v3` re-renders the entire chunk, so pasting the returned rectangle back produces a visible breathing box** wherever the model drifts the palette. Masked compositing is what makes this technique viable, not an optional polish step.

| Question | Finding |
|---|---:|
| Does `first_frame == last_frame` close a loop? | Yes — mean difference `0.00` from frame 0 on 10/10 jobs |
| Can the returned rectangle be pasted back directly? | No — palette drift reads as a rectangle |
| Can regions overlap? | Chunks yes; **paste masks no** |
| Frames available at `256x256` | `8` (API-enforced) |
| Cost per `256x256` 8-frame job | ~`$0.022`–`$0.081` (≈4x spread) |

## Verified Constraints

Read from raw `https://api.pixellab.ai/v2/openapi.json` and confirmed with a live probe.

| Field | Value | Source |
|---|---|---|
| `first_frame` | Base64Image, **"max 256x256 pixels"** | schema field description |
| `last_frame` | Base64Image or null, same cap | schema field description |
| `action` | string, **maxLength `1000`** | schema |
| `frame_count` | integer, min `4`, max `16`, **must be even**, default `8` | schema |
| `seed` | integer ≥ 0, default `0` (random) | schema |
| `enhance_prompt` | bool, default `false`, costs ~`0.05` generations | schema |

**The `256x256` cap is stated in prose, not as a field constraint.** This matches the warning in [`pixellab-image-size-limits.md`](pixellab-image-size-limits.md) that several endpoints (`animate-with-text-v3` among them) declare real bounds only in their descriptions while the field schema stays loose. Reading field schemas alone under-reports this limit.

**`frame_count` is coupled to canvas area.** The documented budget is `width x height x frame_count <= 524,288`; `256 x 256 x 8 = 524,288` exactly. A live probe requesting `16` frames at `256x256` was rejected before any charge:

```text
422 {"detail": "frame_count 16 too high for 256x256 image. Max frame_count: 8"}
```

So at a full `256x256` region, **8 frames is the hard ceiling**, and the error message states the maximum directly — a cheap, non-billable way to confirm the ceiling for any canvas.

**Return shape:** `frame_count + 1` images. Image 0 is the submitted `first_frame` echoed back verbatim (verified: `maxdiff 0` against the sent crop on all 10 regions). With `last_frame` set to the same crop, the final image lands back on it and duplicates image 0, leaving `frame_count` unique frames.

## Loop Closure Is Reliable; Artifacts Are The Real Risk

[`../../skills/pixellab-pip/references/animation.md`](../../skills/pixellab-pip/references/animation.md) flags identical `first_frame`/`last_frame` on low-motion loops as high-risk. This spike refines that:

- **Loop closure itself was not the risk.** All 10 regions returned a final frame with mean difference `0.00` from frame 0. Closure was exact, not approximate.
- **Artifact generation was the risk**, and it materialised in 1 of 10 regions (the magic orb, below).

A likely reason the documented idle-loop failures did not appear: those findings concern **idle character loops**, where the model reads the request as needing a walk/idle cycle from a neutral stance. This spike's subjects were **ambient environmental motion** (foliage sway, falling water, glow pulse, breathing) where "return to the starting state" is physically natural. **Ambient background motion appears to be a materially better fit for identical start/end anchors than character idle loops.**

## Region Selection

Ten `256x256` regions covered characters, lighting, foliage, and water. Rules that emerged:

- **Measure the subject's bounding box before choosing an offset.** A subject that does not fit inside `256x256` cannot be fully contained by any chunk, and motion will tear at the crop line.
- **A subject larger than the cap has no clean route.** One character measured `240x355`. No chunk can hold him. The workaround was to animate only a sub-region (the cloak) and word the `action` to pin everything else ("legs, boots, belt and torso stay completely still"). It held acceptably, but the bow still shifted slightly. Treat oversized subjects as a known compromise, not a solved case.
- **Static regions are a legitimate choice.** The title lettering was deliberately excluded; animating text was not attempted and is not recommended without its own test.
- **Chunks may overlap; masks may not.** Several chunks overlapped because their subjects were adjacent (a wolf's rump sat under a staff). This is fine as long as the paste masks stay disjoint, which lets each chunk keep useful surrounding context for the model.

## The Seam Problem And Masked Compositing

`animate-with-text-v3` re-renders the whole `256x256` region, including parts the prompt asked to hold still. Pasting that rectangle onto an otherwise-static background makes any palette drift read as a rectangular box that breathes with the loop.

The fix is to composite each region through a **feathered alpha mask that covers only its moving subject**, landing the mask edges in visually quiet areas. Properties that make this sound:

- **Frame 0 is a pixel-exact echo of the crop, so a masked paste of frame 0 is an identity operation.** That makes the whole pipeline assertable: recompositing the unmodified crops must reproduce the source with `maxdiff 0`. This ran before any paid call and is the alignment proof.
- Outside the mask, original pixels are untouched.
- Every pixel still originates from PixelLab or the source. Masking and compositing are permitted local operations under Asset Integrity, and were reported as such.

**Feather geometry matters.** Building the mask as a rectangle inset by `f` then blurred with sigma `f/2` let the gaussian tail reach roughly `1.5f` **beyond** the declared rectangle, silently overlapping a neighbouring mask. Using **sigma `f/3`** puts the ~3-sigma tail at the declared edge:

```python
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).rectangle([x0 + f, y0 + f, x1 - f, y1 - f], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(f / 3.0))   # tail dies at the rect edge
```

**Two mask defects were caught by assertions, not by eye:** the blur overspill above, and a mask whose top edge reached into a static neighbouring character's robe hem — which would have animated the hem while the body above it stayed frozen. A pairwise disjointness check over the full-size masks (`min(a, b).max() == 0`) plus an `alpha_sum <= 255` check found both.

## Prompt Findings

### Additive brightness is subject-dependent

The same wording produced opposite results:

| Subject | Wording | Result |
|---|---|---|
| Bioluminescent mushrooms | "glow pulses slowly brighter and dimmer" | Smooth, correct breathing glow, first attempt |
| Magic orb on a staff | "pulses gently brighter and dimmer" | Blew out to a **white flash with a light beam** |

The orb already contained a small white core at high intensity; the mushrooms are a soft area glow. **A small, high-intensity light source with an existing white core amplifies brightness wording into a strobe; a diffuse area glow does not.** For concentrated light sources, drive motion with something other than brightness (rotation, drift) and pin brightness and size explicitly as constants.

### Negative wording alone did not fix it; the seed did

The orb took five attempts. Rewriting the `action` to make rotation the only motion, pinning size and colour, and explicitly banning white/flash/bloom/beams/glare **reduced but did not eliminate** the blowout. `animate-with-text-v3` exposes **no guidance, strength, or adherence control** — after wording, the seed is the only remaining lever. Three candidate seeds were run in parallel and selected by measurement.

### Selecting candidates by measurement, then by eye

Per-frame mean luminance spread separated the candidates cleanly:

| Seed | Mean-luminance spread | Outcome |
|---|---:|---|
| `4242` | 24.40 | Rejected — strobed white |
| `7` | **9.54** | Rejected — smoothest luminance but the orb **changed size** erratically |
| `99` | 14.71 | **Shipped** — constant size and hue, rings swirl consistently |
| `3131` | 28.09 | Rejected — largest swing |

**The metric alone was not sufficient.** The lowest-spread candidate (`7`) was rejected on a failure the luminance metric cannot see. A cheap numeric filter narrows the field; a visual check still decides. Note also that peak-white was `255` in *every* candidate including frame 0 — the source orb already contains white, so "peak white present" is not a defect signal here. Metrics need a baseline from the input frame.

## GIF Assembly

The source held **293,193 unique colours**; GIF allows 256. Quantisation is unavoidable and is the main quality loss in the deliverable.

**Use one palette built from all frames together.** A per-frame palette makes the palette flicker across the loop. When PIL reads back a correctly-built GIF, only frame 0 carries a palette and later frames return `None` — that indicates a shared global palette and is not a defect.

Quantisers measured against the composited frames (same image, 256 colours, no dither):

| Quantiser | Mean err | Max err | Pixels off by >32 | Note |
|---|---:|---:|---:|---|
| PIL `MEDIANCUT` | 2.56 | 136 | 0.671% | Visible mottling in lettering |
| PIL `MAXCOVERAGE` | 5.94 | **22** | 0.000% | Strong olive colour cast |
| PIL `FASTOCTREE` | 3.45 | 52 | 0.118% | Closest of the PIL options |
| ImageMagick default (sRGB) | **2.35** | 90 | 0.048% | Best mean |
| ImageMagick `-quantize LAB` | 2.62 | **59** | **0.077%** | Best balance |

**For flat pixel art, peak error predicts visible damage better than mean error.** `MEDIANCUT` had a good mean but its localised outliers produced obvious blotching; `MAXCOVERAGE` had an excellent max but shifted every colour. LAB gave the best combination.

**`-layers optimize` costs quality.** It reserves a palette slot for transparency, taking it from the image:

| Build | Size | Mean err | Max err |
|---|---:|---:|---:|
| LAB 256, no optimisation | 7.92 MB | 2.67 | 81 |
| LAB 256, `-layers optimize` | 1.90 MB | 3.71 | 96 |
| **LAB 255, `-layers OptimizeTransparency`** | **2.02 MB** | **2.84** | **66** |

Quantising to **255** colours and letting the 256th slot be transparency gives ~4x smaller output **and** lower error than the unoptimised 256-colour build. Final recipe:

```bash
magick frames/frame_*.png -append -quantize LAB -dither None -colors 255 -unique-colors palette.png
magick -delay 20 -loop 0 frames/frame_*.png -dither None -remap palette.png \
  -layers OptimizeTransparency out.gif
```

**Always decode the finished GIF and diff every frame against the composited source frames.** Frame differencing is where an encoder can silently corrupt output.

## Aseprite Build

Two CLI behaviours forced a Lua script instead of plain CLI flags:

- **The CLI auto-expands numbered sequences.** Passing exactly `00.png`–`07.png` produced a **9-frame** sprite, because Aseprite detected the sequence and pulled in `08.png` from the same folder. Verify the frame count in the written header; do not assume the file list is the frame list.
- **The CLI cannot set frame duration.** `Frame.duration` is Lua-only, and is expressed in **seconds** (`0.2`, not `200`).

The composition build (one background layer plus one layer per region, each cel at that region's exact source offset, layer alpha carrying the paste mask):

```lua
local spr = Sprite(1672, 941, ColorMode.RGB)
while #spr.frames < N do spr:newEmptyFrame(#spr.frames + 1) end
for i = 1, N do spr.frames[i].duration = 0.2 end          -- seconds
local lay = spr:newLayer(); lay.name = id
spr:newCel(lay, f, Image{ fromFile = path }, Point(x0, y0))  -- cel pos == source offset
spr:saveAs(out)
```

Aseprite's cel-position model maps directly onto the offsets, so no coordinate translation is needed. Verify by exporting the composition back out (`--save-as frame_{frame}.png`) and diffing against the externally composited frames. Result here: **`maxdiff 0` on frame 0 and `maxdiff 1` on the rest** — the 1-level difference is Aseprite/PIL alpha-blend rounding, not misalignment.

Note: an installed PixelLab Aseprite extension may print unrelated Lua errors on `-b` startup. They did not affect scripted runs here.

## Verification Harness

The assertions that earned their place, in the order they should run:

| Check | Catches |
|---|---|
| Recomposite unmodified crops == source, `maxdiff 0` | Any offset/alignment error — **run before spending** |
| Pairwise mask disjointness + `alpha_sum <= 255` | Masks fighting over shared pixels |
| Image 0 == sent crop (`maxdiff 0`) | Wrong frame order or a mismatched echo |
| Final image vs image 0 mean diff | Whether the loop actually closes |
| Per-frame mean delta vs the crop | A job that returned no motion |
| Decoded GIF frames vs composited frames | Encoder/optimiser corruption |
| Aseprite re-export vs composited frames | Cel offset or layer alpha errors |

The first two ran before any paid call and caught two real defects at zero cost.

## Job Lifecycle Note

A session ended between submitting a paid job and polling it. Because the `background_job_id` was persisted to disk immediately after submit and before polling, the charged job was recovered by re-polling the saved id, with no resubmission and no double charge. This validates the rule in [`../../skills/pixellab-pip/references/job-lifecycle.md`](../../skills/pixellab-pip/references/job-lifecycle.md); the write-before-poll ordering is what made recovery possible.

## Cost

Per-job cost for a `256x256`, 8-frame job ranged **`$0.022`–`$0.081`** — an ~4x spread across identical request shapes, consistent with compute-time-based pricing rather than a flat per-call fee. Fourteen jobs (10 kept, 4 rejected orb iterations) billed `$0.5018` by their own `usage.usd` records.

Budget a region-composited background at roughly **`$0.03` per region per attempt**, plus re-rolls. Re-rolls are concentrated on whichever regions have the failure modes above, so a fixed per-region budget under-estimates.

## Open Questions

- **Smaller regions buy frames.** `frame_count 16` needs `width x height <= 32,768` (~`181x181`; `128x128` is a safe choice). Whether 16 frames at ~`181px` reads as a smoother ambient loop than 8 frames at `256px` — trading region coverage for temporal resolution — was not tested.
- **Region-count scaling.** Ten regions held without neighbouring palette drift. Whether 20+ regions on one canvas stay coherent is untested.
- **Subjects larger than `256x256`** have no clean route. Splitting one subject across two chunks with a shared mask boundary was not attempted and would need the two jobs' motion to agree at the seam — likely difficult without an anchor they both share.
- **Animated lettering** was avoided by design, not tested.
- **`interpolation-v2`** (Pro, `128x128` cap, no frame-count control) was not compared against the `first_frame`+`last_frame` tween for this use case.
- **Billing reconciliation.** Per-call `usage.usd` summed ~`$0.19` below the observed balance delta. Concurrent PixelLab work in the same account is the likely cause, but the v2 API exposes no usage-history endpoint (`llms.txt` lists only `GET /balance`), so it could not be attributed. Treat a balance delta as an overlapping observation whenever other work may be running.

## Candidate Promotions

Findings here that change agent behaviour and belong in the runtime contract if adopted:

- `animation.md`: the identical-anchor risk is **artifact generation, not loop closure**, and ambient/environmental motion is a materially safer fit for identical anchors than character idle loops.
- `animation.md` or a new reference: **`animate-with-text-v3` re-renders the whole chunk**, so any composite of a sub-region back onto a static background requires a mask, not a rectangle paste.
- `local-asset-assembly.md`: the GIF global-palette rule, the LAB/255-colour + `OptimizeTransparency` recipe, and peak-vs-mean error guidance for quantising flat pixel art.
- `aseprite-cli.md`: the CLI numbered-sequence auto-expansion, and that frame duration is Lua-only and in seconds.
