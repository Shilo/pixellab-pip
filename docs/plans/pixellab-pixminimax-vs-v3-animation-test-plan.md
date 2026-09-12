# PixelLab PixMiniMax vs v3 Animation Test Plan

Status: planned 2026-09-12. Results will be recorded in
`../pixellab/pixellab-pixminimax-vs-v3-animation-spike.md` and the git-ignored
`pixellab-pip-generations/` run folder.

## Goal

Measure the practical difference between PixelLab's public
`POST /v2/animate-pixminimax` route (PixMiniMax, powered by MiniMax H3) and
`POST /v2/animate-with-text-v3` (v3) on the same supplied pixel-art frames.
The comparison is about usable sprite animation, not a claim that the two
routes expose the same model, prompt language, or price. It must cover the
common first-frame workflow, end-frame interpolation, motion families, prompt
enhancement, frame-count scaling, transparency, and output integrity while
staying comfortably below the explicit 3,000-generation ceiling.

## Guardrails

- Use only the documented public REST v2 routes and `GET /v2/background-jobs/{job_id}`.
  Do not call the private website or editor operation URLs observed during research.
- Reuse existing PixelLab/user source frames from prior runs. Do not create or
  repaint test art locally; local processing is limited to copying inputs,
  decoding returned images, making labeled contact sheets/GIF previews, and
  calculating verification metrics.
- Use one fixed seed per paired comparison where the route accepts it, but treat
  same-seed output as comparable rather than deterministic.
- The route's `frame_count` is the number of generated frames; validate the
  documented `frame_count + 1` response convention and identify the echoed
  input frame before comparing motion.
- Keep `no_background=true` unless a test explicitly exercises background
  retention. Compare alpha and composition separately from semantic motion.
- Never retry a paid create request because a poll timed out. Re-poll the saved
  job ID. A new attempt requires a new budget entry and an explicit reason.
- Stop all paid testing immediately if cumulative reported generations reaches
  2,700, leaving 300 generations for an approved correction or one necessary
  rerun; never cross 3,000.

## Fixtures

Use two existing, representative source families so the result is not tied to
one subject:

1. **Robot character** — a small south-facing futuristic robot with a helmet,
   blue armor, yellow accents, outline, and transparent background. Use the
   same source PNG for paired first-frame tests and a previously recorded
   matching walking pose as the end anchor where available.
2. **Fireplace/flame effect** — a tiny front-facing fireplace with a stationary
   ember base and a transparent background. Use the existing source frame and
   a matching end frame for cyclic-fire and endpoint tests.

For each fixture, record dimensions, color mode, alpha coverage, non-transparent
bounding box, and a SHA-256 digest before the first call. Copy the exact source
files into the run folder. If an older output is used as an end anchor, label it
as a PixelLab-generated anchor and record its provenance; do not silently use a
locally repaired composite as a model input.

## Test matrix

Each numbered case is a planned comparison unit. A “pair” means one v3 call and
one PixMiniMax call with the same fixture, action, frame count, seed, and
background setting wherever the two schemas permit. `P` means the public
PixMiniMax route; `V` means the public v3 route.

### A. Common baseline and prompt-shape cases

| ID | Fixture | Inputs | Purpose |
|---|---|---|---|
| A1 | robot | first frame only, 8 frames, neutral walk prompt | Direct baseline at the default frame count. |
| A2 | robot | matching first/end anchors, 8 frames, same prompt | Measures endpoint anchoring and loop closure. |
| A3 | flame | first frame only, 8 frames, in-place fire prompt | Tests tiny effect motion and stationary-base preservation. |
| A4 | flame | matching first/end anchors, 8 frames, same prompt | Tests a cyclic effect with an explicit endpoint. |
| A5 | robot | first frame only, 8 frames, short prompt with `enhance_prompt=false` | Separates prompt brevity from server enhancement. |
| A6 | robot | first frame only, 8 frames, same short prompt with inline `enhance_prompt=true` on each route | Measures whether enhancement improves motion structure enough to justify its extra charge. |

The baseline prompt is:

> A natural 8-frame walk cycle facing south toward the viewer. Start moving on
> the first frame; alternate arms and legs with clear contact and passing poses,
> a relaxed weight shift, and a subtle torso bob. Keep the character in place;
> preserve the helmet, blue armor, yellow accents, outline, scale, palette, and
> transparent background.

The short prompt is:

> An energetic walk cycle facing south, in place.

The flame prompt is:

> Start the fire moving on the first frame. Animate an irregular flame in place:
> tongues rise, curl, split, merge, contract, and swell with varied timing.
> Keep the stone hearth and ember base stationary; preserve the pixel-art scale,
> palette, placement, and transparency.

### B. Motion-family cases

Run these on the robot unless noted otherwise. The same action wording is sent
to both routes; controls such as `direction` are recorded separately because
PixMiniMax uses it only with prompt enhancement.

| ID | Action | Frames | Purpose |
|---|---|---:|---|
| B1 | idle breathing with a small shoulder and torso shift, facing south, in place | 4 | Minimum legal clip and low-motion artifact risk. |
| B2 | relaxed walk cycle facing south, in place | 8 | Locomotion quality and foot contacts. |
| B3 | energetic run cycle facing south, in place | 16 | Faster locomotion and longer temporal planning. |
| B4 | raise a sword overhead, strike once, and recover to the starting stance, facing south | 8 | Multi-phase attack and silhouette continuity. |
| B5 | draw a bow, aim toward the viewer, release one arrow, and return, facing south | 16 | Direction/facing and a discrete event. |
| B6 | jump in place, reach a clear apex, land, and settle, facing south | 8 | Vertical trajectory and contact timing. |
| B7 | spin a gold coin once in place with a stable center and return to the starting orientation | 16 | Rigid-object rotation and center drift. |
| B8 | fireplace flame rises and curls in place around a stationary hearth | 16 | Non-character effect motion; flame fixture only. |

### C. Endpoint, drift, and scale cases

These cases probe controls that are materially different between the routes.

| ID | Fixture | Inputs | Purpose |
|---|---|---|---|
| C1 | robot | distinct first/end walking poses, 4 frames | Shortest start-to-end transition. |
| C2 | robot | distinct first/end walking poses, 16 frames | Longer transition and endpoint convergence. |
| C3 | flame | same first/end frame, 8 frames, PixMiniMax `drift_threshold` omitted | Documented/default de-flicker behavior. |
| C4 | flame | same first/end frame, 8 frames, PixMiniMax `drift_threshold=0` | Aggressive de-flicker comparison; only run if C3 completes. |
| C5 | robot | 32×32 source, 4 frames | Lowest published PixMiniMax cost example and small-canvas behavior. |
| C6 | robot | 64×64 source, 8 frames | Main quality/cost reference. |
| C7 | robot | 80×80 source, 8 frames | Boundary behavior around the documented upscaling buckets. |
| C8 | robot | 128×128 source, 16 frames | Larger canvas and long clip within the public route limits. |
| C9 | robot | 256×256 source, 40 frames | Maximum-duration stress case; run once per model only if the running ledger remains below the reserve. |

Cases C5–C9 may use a nearest-neighbor-preserved copy of the same supplied
source only when a correctly sized source already exists in the archive. Do not
invent a resized/generated input during the experiment. If an exact-size source
is unavailable, mark the case “not run” rather than making test art.

### D. Reproducibility and failure cases

| ID | Inputs | Purpose |
|---|---|---|
| D1 | Repeat A1 once per route with the same seed | Estimate within-route variance; do not interpret pixel differences as regressions. |
| D2 | Repeat A2 once per route with the same seed | Check whether endpoint behavior is stable across a second sample. |
| D3 | One legal request with `last_frame` but no `enhance_prompt` | Confirms the PixMiniMax end-frame path independently of prompt enhancement. |
| D4 | One malformed/illegal request per route in a separate non-paid validation attempt where possible; otherwise use schema inspection only | Records validation boundaries without intentionally charging a job. |

D4 is not a request to force a paid server-side failure. Prefer local payload
validation or a rejected request that the server confirms before a background
job is accepted; record any unexpected charge and stop the branch.

## Per-case procedure

1. Snapshot the account balance and the cumulative generation ledger.
2. Save the exact request body with the route, fixture digest, prompt, seed,
   dimensions, frame count, and chosen controls. Omit credentials.
3. Submit v3 and PixMiniMax sequentially with a short delay if the service is
   rate-limited. Save the returned job IDs immediately.
4. Poll each job at a gentle backoff until the documented result is complete
   or failed. Persist the latest response after every meaningful poll.
5. Decode and save each returned frame, preserving the input frame separately.
   Create a clearly labeled contact sheet and preview GIF as QA derivatives;
   do not present them as untouched PixelLab originals.
6. Verify dimensions, frame count, frame ordering, input-frame echo, alpha,
   transparency, color stability, bounding-box drift, and endpoint equality.
7. Visually review the first, middle, event, and final frames for identity,
   silhouette, action readability, cadence, detached artifacts, palette drift,
   camera/background motion, and unwanted symbols/particles.
8. Record cost, wall time, poll count, transient errors, and a verdict for
   technical validity and visual usefulness separately.

## Scoring

Score each completed output on a 0–4 scale, with “not applicable” allowed:

| Dimension | 0 | 4 |
|---|---|---|
| Identity/style retention | Subject is lost or redesigned | Subject, palette, outline, scale, and transparent composition remain usable |
| Motion fidelity | No intended motion or wrong action | Action is clear, coherent, and starts on frame 1 |
| Temporal cadence | Frozen, duplicated, or chaotic | Readable timing with distinct purposeful phases |
| Spatial stability | Severe drift, crop, or background movement | Stable placement and silhouette with acceptable motion |
| Artifact cleanliness | Detached marks, symbols, body fusion, or severe flicker | No material artifacts for the requested use |
| Endpoint/loop behavior | Anchor ignored or loop visibly breaks | Required endpoint is reached and/or loop is visually clean |
| Editor readiness | Wrong dimensions/alpha/order or unusable export | Ready for an Aseprite frame sequence after ordinary import/export |

Report mean scores only with the case-level table still available. A higher
score does not override a hard failure such as wrong dimensions, missing alpha,
or an ignored required end frame.

## Budget ledger

The hard ceiling is **3,000 PixelLab generation units** across this plan,
including enhancement calls and any approved reruns. The expected run is much
smaller; reserve is intentional.

| Group | Planned calls | Conservative allowance |
|---|---:|---:|
| A common baselines | 12–14 | 120 generations |
| B motion families | 16 | 240 generations |
| C endpoint/drift/scale | 18 | 700 generations |
| D repeats/validation | 8–10 | 180 generations |
| Prompt enhancement overhead | ≤4 | 1 generation |
| One correction/rerun reserve | — | 300 generations |
| **Expected ceiling for the planned matrix** | **≤58 paid calls** | **1,541 generations** |

The allowance intentionally exceeds the current published PixMiniMax examples
(1 generation at 32×32/4 frames, 2 at 64×64/4, 3 at 64×64/8, 5 at 64×64/16,
and 12 at 64×64/40) and treats v3 costs conservatively. The live response's
`usage` value is authoritative for the ledger. Do not spend the unused balance
just to make the sample larger.

Before the first paid call, show the complete approved call list and exact
prompts under the normal cost gate. Any addition outside this plan, including a
third candidate or an unplanned retry, needs a new approval. The user’s
explicit 3,000-unit ceiling authorizes this planned comparison but does not
authorize exceeding it.

## Deliverables

- This plan, updated with execution status and any cases not run.
- A detailed research Spike in `docs/pixellab/` covering the refreshed public
  REST/MCP contract, MiniMax H3 evidence and adaptation limits, website and
  Aseprite findings, prompt guidance, test results, and unresolved conflicts.
- One git-ignored run folder under `pixellab-pip-generations/` containing exact
  requests, sanitized responses, source copies, returned original frames,
  labeled QA derivatives, per-case manifests, a usage ledger, and blueprints
  that replay only the successful paid calls.
- Updated canonical routing/parity/prompt-limit references and index entries.
- QA output from `python dev-tools/qa.py`, diff checks, and a conventional
  commit containing the documentation and routing changes.
