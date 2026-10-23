# Pip × Game Art integration

One agent-agnostic Pip skill preserves selected Game Art capabilities: named project styles and approved family references, optional advanced key-pose production, animation inspection and accepted repairs, motion references, local assembly/exports, and history over one private manifest. Existing MCP/REST/editor routing and safety boundaries remain authoritative.

The optional Claude Studio prototype and its panel command are removed from this PR. All supported hosts use the same core; describe the task after the normal skill invocation. Settings remain `setup`, `update`, `uninstall`, `auto` and `bark`. There is no second `level` permission system. Specify budget/retry constraints in the current run request; cost permission does not authorize visual changes.

## Task access

| Source task family | Pip access |
|---|---|
| Characters, icons, backgrounds, scenes, buildings, tiles, VFX, normal maps | Describe the requested asset; the existing router chooses its surface/reference. |
| Animation and custom key poses | Ordinary animation stays on normal raw/managed routes. Ask explicitly for custom reviewed pose stages when wanted. |
| Check/fix | “Inspect these frames” is read-only diagnosis; “fix these defects” authorizes only the identified repair scope, with proposals for playback/effects. |
| Init/style/analyze | Optional guided project setup, saved/temporary named styles, approved family anchors and advisory analysis. |
| Start/batch | Optional first-project choices or a mixed CSV/text/group list, using existing routes and one approved chain. |
| History/reroll | Query the canonical manifests; unknown old dates/charges remain unknown. Repeat a recoverable historical call/blueprint step with the requested change under normal approval. |
| Setup/update/tech/help | Existing core setup/update and direct explanation. |
| Feedback/model dispatch/installer | Author telemetry, automatic task-model dispatch and a second installer/updater are intentionally excluded. |

[Migration](migration.md) covers old instructions, appearance drift, restrictive caps and pending work. [Original prototype evidence](demo/README.md) is historical, not validation of the revised head. [Review and remediation plan](../tools/pixellab-game-art-skill/pixellab-game-art-pr-11-implementation-plan.md) records current acceptance evidence and remaining empirical limits.

Credit: PixelLab Pip by Shilo; pixellab-game-art by lexingel. The shipped skill includes the complete adopted MIT notice and pinned provenance in `THIRD_PARTY_NOTICES.md`.
