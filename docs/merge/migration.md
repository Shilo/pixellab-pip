# Migrating Game Art projects to Pip

Pip keeps one skill and the existing `pixellab.json` project file. Ordinary requests work without a profile. Use `/pixellab-pip panel` for the reworked visual review and `auto plan <budget> [retries] [task]` for one identified bounded run. Auto off asks first; Auto on runs within the stated limits, preserving explicit ask-first or dry-run instructions. The cap blocks calls exceeding it; the retry allowance blocks extra retries, while original approved stages may continue within the cap when their inputs/checkpoints are satisfied. Neither limit increases automatically. The separate Studio package and `level` command are consolidated rather than restored as parallel systems. Changing spending confirmation does not authorize recoloring, new pixels or playback changes.

Prototype global `level`, `budget` and `retries` fields are restrictive unresolved policy. `auto status` exposes them and disables effective Auto until reconciled. Review the old limits, transfer applicable constraints to the identified run, and only after deliberate acceptance use `auto reset` to discard those three legacy fields and leave Auto off. An informed request to discard these limits and enable Auto can run reset then on in one turn without another confirmation. Reset preserves other settings and grants no spending permission. Installation-wide budget defaults do not silently carry over or become unlimited Auto.

## Review the old installation before changing it

1. Identify the installation roots the user names and the current project. Look for the old `pixellab-game-art` core, `pga-*` task skills, optional generated task-agent configurations, and installed project instructions. Do not sweep unrelated home/config folders.
2. Show the exact proposed removals and recognizable copied instruction paragraphs, including old “never ask permission” rules. If a paragraph has user edits or uncertain provenance, ask what should remain. Existing user instructions must not be erased to make the merge pass.
3. After explicit approval, remove only the obsolete identified components or replace the approved block. Keep a user-requested backup outside packaged source when needed. This document is guidance, not an automatic cleanup script.

## Review appearance and restrictive settings

Old projects may combine top-level direction, named styles, implicit dark-fantasy/size/timing defaults and category wording. Pip does not activate those defaults by absence. Display the effective intended direction, palette, view, sizes/timing and per-family anchors before paid work. Offer to save/pin the user's chosen look; no exact output equivalence is promised.

Pip recursively overlays known maps (for example one family's anchor or one sprite size) while lists/scalars/null replace their previous value. This deliberately differs from the source agent's shallow overlay description. Example: a saved icons anchor need not remove a top-level heroes anchor, but that retained heroes anchor must still be the user's intended reference. Show the resolved result during migration instead of assuming it is unchanged.

Legacy `max_cost` or `ask_above` is a restrictive expectation, not discarded unknown data. Preserve it and resolve its units and scope with the user before spending. `0` is a real restriction. Opting out of a project's appearance does not opt out of its limits. Malformed data, unknown selections or unreadable anchors require a clear decision; never overwrite them with an empty profile or generate a replacement reference implicitly.

Temporary named selection and one-job overrides leave active state unchanged. Choosing a character's canonical still is distinct from approving a family style anchor. Explicitly save/replace an anchor under the correct family only when intended.

## Credentials, history and pending work

Do not copy a token from an old config or ask for it in chat. Use the established host secret mechanism or `PIXELLAB_SECRET`; follow Pip setup/credential guidance. Keep old manifests/artifact files intact. Recover pending jobs with their IDs/getters; an expired URL does not prove a failed or refunded job. If an old log cannot establish charge, date, exact request or ownership, report that uncertainty rather than inventing it. A new reroll needs recoverable input plus the usual current-user scope/approval.

## Representative acceptance walkthroughs

- Existing two-style project: inspect/review its effective town direction; request dungeon icons for one job; the next ordinary job still uses town. A per-job override never saves itself.
- Profile with `max_cost: 0`: appearance opt-out leaves the cap visible and prevents unapproved paid work.
- Project `AGENTS.md` has a copied no-ask block plus user notes: preview only the known block, preserve notes, and wait for explicit cleanup approval.
- Saved monster reference exists but heroes reference is absent: a new hero does not silently use the monster or generate an anchor.
- Interrupted job has a download 404: recover the getter/submit result and reservation; do not pay for a replacement merely to get a file.

These walkthroughs define expected decisions. Unit/dry evidence is recorded in the remediation plan; they are not claims of a live engine import or paid migration experiment.
