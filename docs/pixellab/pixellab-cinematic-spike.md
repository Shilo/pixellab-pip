# PixelLab Multi-Shot Cinematic Spike

Last reviewed: 2026-07-12.

Purpose: record live-generation findings from building a ~60-second, seamless-looping cinematic by chaining many PixelLab REST v2 `animate-with-text-v3` jobs, each continuing from the previous job's last frame. This note is the evidence base behind `skills/pixellab-pip/references/cinematic.md`. It extends the single-clip findings in `pixellab-idle-animation-artifact-research.md` to the multi-job case.

This note does not link to the generated candidate frames; they live in the gitignored `pixellab-pip-generations/` folder and are disposable. The durable artifact is the method and the failure/mitigation catalog.

## What was built (evidence)

- Goal: a 1-minute virtual-pet cinematic — a subject that reacts to and faces the camera (its "owner"), a single secondary object (a ball) thrown, chased, caught, returned, and handed back, looping seamlessly, with only two things ever on screen.
- Result: 600 frames at 100 ms = 60.0 s, transparent background, verified seamless loop.
- Cost: 37 chained 16-frame jobs, ~$0.035–0.083 each; **~$2.28 total** including every re-roll and discard, against a $10 budget.
- Input: one supplied 128×128 transparent start frame; a managed PixelLab character supplied the identity description.

## Endpoint mechanics (confirmed against the live API and OpenAPI)

- **Async.** `POST /v2/animate-with-text-v3` returns a `background_job_id`; poll `GET /v2/background-jobs/{job_id}` until `completed`. Cost appears as `usage`/`billing_usage` (`{"type":"usd","usd":…}`) on the completed job.
- **Frame count.** `frame_count` is 4–16, must be even, default 8. `frame_count=16` returned **17 images**: image 0 is the input `first_frame` echoed back (pixel-identical or a negligible re-encode difference — see the testing note), images 1–16 are the generated motion. Budget on 16 to minimize job count.
- **Image fields are objects, not raw strings.** `first_frame`/`last_frame` are `Base64Image` = `{"type":"base64","base64":"…","format":"png"}`. Passing a bare base64 string 422s (before any charge).
- **No `image_size`.** Output canvas equals the `first_frame` canvas (max 256×256). A 128×128 canvas left room for the subject plus a second object to move around; the subject was kept small on purpose.
- **`action` caps at 500 characters** (hard). Over-length 422s before charge; still cheaper to check length locally before POST.
- **`no_background: true`** preserved transparency when the input frame was already transparent; every output frame kept a real alpha channel (extrema 0–255).
- **`seed`.** `0` = random; a fixed non-zero seed per job made runs reproducible and gave a lever for re-rolls.
- **`enhance_prompt`** was not used; hand-authored near-max actions already carried the intended motion, and enabling it would expand/rewrite the action text.

## Chaining and timing

- **Handoff.** Job N+1's `first_frame` = a chosen frame from job N (the "handoff"). Because job N+1's image 0 is a duplicate of the handoff (the frame you fed it, echoed back — pixel-identical or nearly so), the smooth stitch is: keep job 1's frames 0–16, and for each later job drop its image 0 and keep 1..handoff. The transition handoff→(next) image 1 is one clean motion step.
- **Timing math.** Playback delay (100 ms/frame) is an assembly choice; the endpoint sets no timing. Unique frames = 1 (initial) + Σ(new frames per job). 60 s = 600 frames ≈ 37–40 jobs at ~16 new frames each, fewer when a handoff is taken before frame 16.
- **Adaptive authoring.** Each next action was written *after* viewing the previous result, because the "current state" (subject pose, object position) is whatever the model actually produced, not what was requested.

## Failure modes and mitigations (the core findings)

1. **A free secondary object fades out in a job's final frames.** The thrown object was solid mid-job then vanished by frame 16 in most chase jobs. Mitigation: after each job, detect the object (colour/shape) across all frames and pick the **latest frame that still contains it** as the handoff — not blindly frame 16. This made object continuity reliable across the chain.
2. **Describing an off-screen actor makes the model draw a person.** "The owner throws the ball" rendered a human hand/arm — a third object that broke "only two things on screen." Mitigation: describe the object's **physics** ("a ball flies in from the lower-right and arcs up-left") and explicitly forbid hands/arms/people. The camera-as-owner stays implied and off-screen.
3. **A small held object merges with the subject at small canvas.** A red ball "in the mouth" at 128×128 read as a red mouth and confused colour detection. On-ground / free objects rendered as distinct shapes reliably. Mitigation: prefer distinct on-surface object states; keep "held" spans short; when a held object matters, place it below/outside the silhouette and accept the limitation. Compositing a cleaner object is possible but is post-processing.
4. **Identity, scale, and palette drift over a long chain.** Each job re-renders from the prior frame, so small biases compound: the subject's bounding box grew from roughly 30×53 px to 79×99 px (about double) and warmed in hue across 37 jobs. Mitigations: restate identity + a size/framing cue ("keep small, whole body visible, centred") in every action; expect gradual drift and plan a correction at the loop point. Drift is the dominant long-chain risk.
5. **Copying a stored character prompt can fight the actual render.** The managed character's saved prompt said "floppy ears," which pushed the model to droop ears that the reference frame actually drew erect. Mitigation: describe the **desired visible traits, verified against the reference frame**, rather than pasting a stored description; confirm ambiguous identity traits with the user.
6. **Large orientation changes are unreliable in one job.** A full side→front turn often did not complete in 16 frames. Mitigation: spread big turns over ≥2 jobs, or accept a 3/4 view — "facing the camera" reads fine at front or 3/4 front.
7. **Motion-mark artifacts appear on some energetic/idle frames** (stray sparkles/marks near the head), consistent with `pixellab-idle-animation-artifact-research.md`. Watch for them in validation; they are removable in post if strict "only these objects" matters.
8. **Energetic beats can briefly show the subject's back** (e.g., a spin). Acceptable as play, but note it against any "always face the camera" requirement — the rule usually means "when looking at the viewer," not every frame.

## Loop closure

- The final job used `last_frame` = the movie's first frame. The end frame matched the start almost exactly (mean abs diff **1.16/255**), so the loop seam is effectively invisible.
- But interpolation loaded the size/palette correction into the **last 1–2 frames**, producing an abrupt "snap back" (the drift from finding 4 surfacing all at once). Options, in order of preference: (a) steer the chain back toward the opening size/pose over the last few beats so the anchor has little to correct; (b) accept the raw snap; (c) smooth it in post (a scale/position/colour morph between real frames — post-processing, must be disclosed).
- The movie's frame 0 is the first job's image 0, which is the supplied start image echoed back. Anchor the loop to whichever frame you actually display first.

## Validation methodology

- **Per job, every job.** Programmatic: frame count, canvas size, alpha preserved, motion present (frame-to-frame diff), object present (colour detection), handoff extracted. Visual: a contact sheet on a neutral checkerboard to confirm identity, pose, orientation, and absence of unwanted elements. Re-roll below confidence by varying the seed and tightening the wording at the specific failure (hands, missing object, wrong orientation). Re-rolls spend budget.
- **Plan before spending.** A full beat sheet (one job per beat) was written and documented before any paid call. One calibration job then fixed the real per-job cost and confirmed output shape.
- **Budget gating.** Capture balance first; track cumulative cost with a hard stop; report per-job and total usage.

## Assembly and integrity

- Standard deliverables: one stitched GIF at 100 ms, a spritesheet, and the individual frames, plus a blueprint and a manifest. Keep checkerboard inspection aids separate from final deliverables.
- **Post-processing is a distinct, disclosable act.** Stitching and format conversion preserve pixels. Speck removal, object compositing/interpolation, and loop-smoothing morphs alter content — they are legitimate only when reported and, for content repair, approved. Offer a **zero-post cut** (raw stitched PixelLab frames) alongside any processed cut.
- **Zero-post is verifiable.** Decoding the base64 straight from the saved job responses and comparing to the delivered frames proved 0-pixel difference end to end; a processed cut differed in a large fraction of frames — so "unprocessed" is a checkable claim, not a promise.

## Cost and scale guidance

- ~$0.05/job average at 16 frames; a 60 s single-subject loop landed near $2 including re-rolls. Budget scales roughly linearly with duration and re-roll rate. Always gate on a user-specified budget and stop when reached.

## Confirmed and extended by later testing

A follow-up round ran many from-scratch cinematics as independent assistant instances (short public write-up in `../pixellab-cinematic-testing.md`). Three durable additions came out of it and are now in the runtime references:

- **Cyclic vs evolving — the loop-one-cycle shortcut.** Periodic motion (flicker, spin, bob, sway, flow, rain, a breathing idle) does not need chaining: generate one clean cycle as a single ≤16-frame clip and loop it at playback, tuning the per-frame delay to the requested duration. Multiple instances reached this independently; it is far cheaper than chaining and closes cleanly (measured pixel-identical endpoints with a `last_frame`=first anchor, or within-normal seam distance for a self-closing field). Reserve chaining for scenes that genuinely evolve (the 60 s build above, or a seed→flower growth arc).
- **Robust async polling.** The outer background-job `status` can lag behind the finished, already-billed result; key completion on `last_response`'s own completed/`done` status — not merely the first image, since some endpoints stream partial progress images. Tolerate transient timeouts/5xx by re-polling the same saved job id, never resubmit a paid job on a transient error, and persist each paid response so a poller crash cannot orphan a charge. Read per-call cost from the job's top-level `usage.usd`.
- **De-duplication is not trimming.** Dropping the duplicate frame at each seam (the echoed-back input; and a loop-close frame identical to frame 0) is expected de-duplication for a clean stitch — distinct from the ping-pong/reverse/trim playback manipulation the global rules forbid. Keep the raw frames alongside for integrity.

## Open questions / follow-ups

- Whether periodically re-anchoring to the original reference frame (or a fixed-size crop) mid-chain reduces scale/palette drift without hurting motion continuity.
- Whether `last_frame` mid-chain (not just at the loop) can hold a specific pose without importing endpoint artifacts.
- Whether a lower per-job frame count with more jobs trades cost for less drift, or the reverse.

## Conclusion

Multi-job cinematics are reliably achievable within a small budget, but quality is governed by continuity management, not any single prompt: pick object-preserving handoffs, describe physics instead of off-screen actors, restate identity to fight drift, validate and re-roll every job, and close the loop with a `last_frame` anchor after steering back toward the opening state. The technique is subject-agnostic; nothing here is specific to any one scene.
