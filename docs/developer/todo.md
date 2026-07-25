# Developer TODO

Tracked future work. Not runtime routing; see `../../AGENTS.md` for placement rules.

## Ship a generic async poll-and-download helper (brainstorm)

**Problem.** `references/job-lifecycle.md` requires agents to retrieve every paid async result —
"poll to a bounded deadline, or … a bounded background poll-and-download so the asset is saved even
after the turn ends." But the skill ships **no helper to do this**. Agents with short turns (observed
on Antigravity, ~1-minute turns) submit an async job, can't wait it out in-turn, and abandon it — the
job completes on PixelLab's side but never lands on disk unless the user manually resumes. Claude Code
and Codex tolerate this (longer turns / background-task notifications); Antigravity does not.

During testing this was worked around with a gitignored `.local/poll_download.py` crutch. That is not
shipped, so real users hit the gap.

**Task.** Design and ship a small, generic "works for every case" poll-and-download helper in the
skill (alongside `assets/bark.py`, `assets/background_removal.py`), plus a no-Python fallback.

**Requirements to brainstorm/validate:**

- **Covers every async surface:** REST `background-jobs/{id}` and every MCP-managed getter
  (character, object, tileset, sidescroller, isometric, font, portrait, map-object, edit/inpaint,
  style, animate-with-text, etc.). Verified during testing that recorded IDs may be *asset* IDs
  (poll `/v2/<kind>/{id}`) or *job* IDs (poll `/v2/background-jobs/{id}`) — the helper must try the
  right getter per kind.
- **Auto-register jobs so a sloppy agent can't drop one (highest-value fix).** The prototype
  required the agent to manually register each job (`poll_download.py job <id> <dir>`). In clean-room
  testing Antigravity registered dozens of junk `dummy` entries and *forgot to register the two
  chained-edit jobs it actually needed* — so 2/8 outputs never downloaded while the agent reported
  8/8. The shipped helper must not depend on the agent registering jobs by hand. Options: have the
  submit call itself write the job to the registry; or derive the pending set from the manifests the
  skill already writes per job (`usage-reporting.md`); or scan a run directory for jobs with no saved
  image yet. Whatever the source, the "download everything pending" pass must be driven by real data,
  not by whatever the agent remembered to type. This is the class of failure that made an otherwise
  correct run report a false pass — treat it as a first-class requirement, not a nicety.
- **Correct image extraction:** decode base64 AND fetch image URLs (character `rotation_urls`,
  object `frame_urls`/`storage_urls` — these 403 the default urllib UA, need a browser UA);
  verify PNG magic and prefer the PNG-encoded field when a response exposes raw RGBA in one field
  and the real PNG in another (e.g. `quantized_image`). See the raw-RGBA note now in SKILL.md.
- **Survives a short turn:** a detached/background mode that keeps polling+downloading after the
  agent's turn ends (the `.local` prototype used Windows `DETACHED_PROCESS` + `CREATE_NEW_PROCESS_GROUP`;
  POSIX `start_new_session`). Confirm it survives each harness's turn-end cleanup — unverified whether
  aggressive sandboxes kill detached children.
- **Resumable & idempotent:** skip a job whose output already exists; support a `--retry` pass so a
  later turn (or the user) finishes stragglers. Never re-spend credits on a completed job.
- **Secret-safe:** read `PIXELLAB_SECRET` from env; never print it.

**No-Python fallback (the harder open question).** `bark.py`/`background_removal.py` already assume
Python; the skill declares Python 3.10+. But a robust "never abandon a paid job" guarantee should
degrade when Python is absent. Brainstorm options:
- A shell/`curl`-based poller (bash + PowerShell variants) — cross-platform pain, but no Python dep.
- Let the agent run its own bounded in-turn poll loop via its native tool calls when it *can* wait
  (Claude/Codex), and only fall to the helper/background path for short-turn agents.
- Emit a clear, one-command resume the user can run later (the current SKILL.md fallback), and make
  that command Python-optional.
- Decide whether "no Python + short turn + async job" is a case we truly support or one we honestly
  refuse with a clear "your asset is ready at job <id>, run <X> to fetch it" handoff.

**Acceptance:** on a short-turn harness, an async generation lands its real asset on disk without the
user babysitting; on a no-Python environment, the user is never left charged with an unretrievable
asset. Validate on Antigravity (the failing harness) and confirm no regression on Claude/Codex/OpenCode.

**Prereqs:** run `superpowers:brainstorming` before building — this needs design exploration, not a
rushed script. Then QA (`python dev-tools/qa.py`) and, if shipped as a skill asset, the media/security
scan gates apply.
