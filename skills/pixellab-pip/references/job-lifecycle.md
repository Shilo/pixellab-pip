# Job Lifecycle

Read this for live PixelLab calls that return a job, asset ID, managed MCP asset, pending status, review status, rate-limit response, or download URL.

## Polling

REST v2 async jobs use `GET /background-jobs/{job_id}` when the create response returns a background job ID. MCP managed assets use the matching `get_*` tool, not REST background-job polling.

For REST `POST /v2/tilesets`, the create response can contain both `background_job_id` and `tileset_id` while the status is still `processing`. Poll `GET /background-jobs/{background_job_id}` first. `GET /tilesets/{tileset_id}` may return `423` while the tileset is still being generated, or `404` until the background job has completed and the tileset object has been persisted; treat those as early lifecycle lookups while the background job is still processing.

Poll gently. Start with a short delay, then back off instead of tight loops. Stop polling in the current turn when the job is still pending after a reasonable wait, report the job or asset ID, and tell the user which status route or getter can resume the check.

Do not resubmit a paid job because a poll timed out or a `423`/`404`/`review`/stale-URL lookup came back — poll again or re-fetch with the matching getter instead.

Handle statuses as:

- Success: completed asset/result is available and the returned URL or local download verifies.
- Review: user or agent selection is required before finalizing; do not call it completed.
- Failed: report the failed status and error summary; do not retry paid work unless the user approves.
- Pending/processing: keep the ID and continue polling later.

## MCP Managed Assets

MCP creation tools return asset IDs quickly. Use the matching getter to inspect status, previews, downloads, and results:

- Characters: `get_character`.
- Character animations: `get_character` or animation-specific tool output when available.
- Objects: `get_object`.
- Map objects: `get_map_object`.
- Fonts: `get_font`.
- Portrait-character conversions: `get_portrait_character`.
- UI assets, tilesets, tiles, projects, or helpers: use the visible matching MCP getter when exposed.

State tools such as `create_character_state` and `create_object_state` auto-wait only briefly for the source asset to finish. If a state call fails because the source is still pending, poll the source with its getter first, then retry the state call only when the source is ready.

Animation tools such as `animate_character` and `animate_object` may expose `confirm_cost`. If the first call requests confirmation or refuses without it, report the cost gate and ask before retrying with confirmation. Do not guess that a failed confirmation gate means the animation endpoint is broken.

## Object Review State

PixelLab object generation can return `review` status when multiple candidate frames are produced. Credits may already be spent, but the object is not finalized.

When an object is in review:

- Report that it needs selection, not that it is stuck.
- Show or summarize candidate frame URLs/indices when available.
- Use `select_object_frames` or REST `POST /objects/{object_id}/select-frames` only after the user chooses candidates or the request clearly authorized automatic selection.
- Use `dismiss_review` only when the user approves discarding the candidates.

## Expiring And Sensitive Outputs

MCP download URLs may be unauthenticated and should be treated as shareable but sensitive. If a URL is stale, call the matching getter again for a fresh result.

MCP map objects auto-delete after 8 hours. After a successful map-object result, download or persist needed files promptly and warn the user about the expiry.

## REST Error Handling

- `401`/`403`: auth or permission problem. If auth worked earlier in the same session, say it may be expired, rotated, or unavailable to the current process; point back to bearer-token setup and never ask for the token in chat.
- `402`: credits or billing issue. Stop paid work and tell the user PixelLab rejected the operation.
- `400`/`422`: request validation problem. Summarize the field/error, fix the payload, and retry only if the corrected request preserves user intent.
- `409`/`423`: conflict, duplicate, or locked/in-progress state. Inspect the job or asset status before retrying.
- `429`/`529`: rate or overload response. Honor a `Retry-After` header when visible; otherwise wait/back off. Do not immediate-loop or fan out more paid calls.
- Concurrency: an account runs a limited number of jobs in parallel. Dispatch an approved batch up to that limit — full parallelism finishes fastest; back off only on `429`/`529` (honor `Retry-After`). PixelLab grants queue-skipping **priority slots** for sustained high utilization over a rolling 30-minute window, but that is a user-level concern — do not artificially throttle or inflate paid work to farm slots. Limits vary by tier and are not fully published; no public endpoint reports your slot count, utilization, or active-job list — only per-job `GET /background-jobs/{job_id}` and `GET /balance` (generations/credits). Do not assume a specific number or invent a slots route.
