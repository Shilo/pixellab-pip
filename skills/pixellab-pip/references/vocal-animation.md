# Talking Portraits And Lip Sync

Read this for stored character portraits, mouth/viseme generation, talking GIFs, or a frame-by-frame lip-sync plan.

## Route Choice

| Need | MCP | REST v2 | Cost and lifecycle |
|---|---|---|---|
| Attach/replace a character portrait | `set_character_portrait(character_id, image=...)`, or `from_job_id` from a completed portrait-character conversion | `POST /characters/{character_id}/portrait` with `image` | Free and synchronous. Replacing an existing portrait is destructive; get explicit approval first. |
| Generate mouth visemes | `create_vocal_animation` then `get_vocal_animation` | `POST /vocal-animation` then dedicated `GET /vocal-animation/{job_id}` | Paid-plan async generation; this is the only credit-spending step in this workflow. |
| Render a talking GIF | `create_talking_gif` | `POST /talking-gif` | Free and synchronous; no polling. |
| Return a lip-sync frame plan | `get_lip_sync` | `POST /lip-sync` | Free and synchronous. MCP requires a managed character; REST also supports stateless `viseme_count`. |

Use either a managed `character_id` with a stored portrait or a raw portrait image for vocal generation, never both. Attached portraits may be 16–256 px; attachment centers a non-square image on a transparent square canvas. Raw vocal input has a documented maximum of 256×256 with no published minimum. Managed generation stores the visemes on the character. Raw generation returns them in the completed result without creating a managed character.

## Vocal Generation

- Supported moods: `neutral`, `happy`, `angry`, `sad`, `surprised`; default `neutral`. Generate one mood per call.
- `viseme_count` is 3, 5, 7, or 12; default 7. Keep the same count across every mood stored on one character.
- `no_background` defaults to `true`. Preserve transparency unless the user requests a background.
- Ask for paid-call approval under the normal cost rules. Setting a portrait, rendering the GIF, and requesting the lip-sync plan are free.
- Poll the dedicated vocal getter every 10–15 seconds. Do not use the generic background-job route. `completed_visemes` may be partial progress; wait for the terminal result and all expected frames.

## Talking Output

Preserve `text` / `text_to_speak` exactly: it is dialogue content, not a visual prompt. Do not enhance or translate it. PixelLab documents Latin-alphabet language support; when the dialogue uses another script, ask the user to approve a transliteration.

Talking GIF timing uses `frame_ms` 20–500 (default 90) and `hold_ms` 0–5000 (default 600); GIF timing is rounded to 10 ms. REST accepts either a managed character or inline visemes; MCP accepts a managed character or `from_job_id` from raw portrait generation. The synchronous response is the final GIF, so save and verify it directly. An MCP `from_job_id` remains available for 8 hours after completion; persist needed output before it expires.

The lip-sync plan returns ordered frames with `viseme`, `column`, `duration_ms`, and `text_offset`. With a managed character it also includes the grid URL and row metadata. REST stateless mode takes `viseme_count`; MCP intentionally has no stateless form. REST timing bounds are `frame_ms` 1–5000 and `hold_ms` 0–10000; both default to 90/600.

Verify portrait dimensions and centering, transparency, requested mood, expected viseme count, full completion, frame order and duration, and the dialogue offsets before reporting success.
