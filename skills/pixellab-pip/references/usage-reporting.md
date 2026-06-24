# Usage Reporting

Read this before or after live PixelLab calls, especially credit-spending generation or async jobs.

After every live PixelLab call, report:

- Surface: MCP, REST v2, website/manual, Aseprite, or Pixelorama.
- Tool or endpoint.
- Text-prep method: user text unchanged, agent-enhanced, or PixelLab enhance endpoint.
- Final text fields used, summarized when long.
- Product/mode/model label requested by the user or returned by PixelLab, if any; do not infer provider internals.
- Job, asset, or result IDs.
- Output paths or URLs.
- Async polling/status when relevant.
- Balance/credit delta when exposed.
- Candidate/final status. Call an output final only after the selected file exists locally or at the returned URL and any requested dimensions, transparency, frame count, or layer contract has been checked.

Use `get_balance` or REST `GET /balance` before and after nontrivial generation when available. If only balance is available, report the delta. If neither per-call usage nor balance is exposed, say usage was not exposed. Label estimates as estimates.

If an async call times out or remains pending, keep the job or asset ID and use the matching status/get route or MCP getter. Do not resubmit a paid generation unless the user explicitly wants a fresh run.

Common REST status handling:

- `401`/`403`: auth or permission problem; point back to bearer-token setup, never ask for the token in chat.
- `402`: credits or billing issue; tell the user PixelLab rejected the paid operation.
- `400`/`422`: request validation issue; summarize the field/error and fix the payload before retrying.
- `409`/`423`: conflict, duplicate, or locked/in-progress state; inspect status before retrying.
- `429`/`529`: rate/overload response; wait or retry later instead of immediate loops.

MCP download URLs are unauthenticated; the asset UUID acts as the access key, so treat returned download links as shareable but sensitive.
