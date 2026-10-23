# Panel and Auto: challenged restoration plan

This decision supersedes the panel/level deletion recommendation in the earlier PR #11 implementation plan. The user explicitly values visual interaction and intended useful level controls to be consolidated into Auto. Safety defects justified replacing those internals; they did not establish that the features were redundant. Preserve the earlier evidence as history, not as the current product decision.

## Goals and boundaries

Keep Pip's portable routing contract, one cost gate, documented PixelLab surfaces, original-pixel integrity, localization, deliberate project/style saves and truthful accounting. Preserve useful Game Art interaction. Apply KISS/YAGNI/DRY to cuts as well as additions. A small host-specific view can serve an agent-agnostic core; agent agnosticism does not require identical host APIs.

Do not restore the second Studio package, install-time credential connector, separate slash-command family, global Plan presets, automatic project creation, regex usage totals, optimistic permission state or heuristically selected newest poses. Opening a view must not spend, choose art, change Auto or save a style.

## Current primary-source research

The following documentation was fetched during this reconsideration. Support must be checked in the running session, not inferred from a product name.

| Surface | Evidence and implementation consequence |
|---|---|
| Claude Code native mods | [Overview](https://code.claude.com/docs/en/plugins/mods) and [reference](https://code.claude.com/docs/en/plugins/mods/reference) document modules, panes, buttons, inputs and reactive state. A native presentation adapter is justified. |
| Claude tool entry point | [Mods API](https://code.claude.com/docs/en/plugins/mods/api) documents registering a callable tool in `session.start`. The existing skill command can call that tool; registering another `/pixellab-pip` command risks a collision. |
| Claude visual surfaces | [Interface guide](https://code.claude.com/docs/en/plugins/mods/interface) distinguishes terminal from Desktop/VS Code elements. SVG is not a terminal capability. Headless/SDK/cloud sessions do not display native drawings; Desktop WSL plugins have additional restrictions. Report unsupported previews instead of approving unseen art. |
| Codex desktop browser | [Official browser documentation](https://learn.chatgpt.com/docs/browser?surface=app) establishes local browser review in supported desktop sessions. It does not establish a universally available Claude-style mod API. CLI/IDE sessions require another available renderer or external browser. |
| Codex inline presentation | The available bundled visualization capability in this session accepts interactive local HTML fragments and prohibits network calls. It is a session capability, not a repository-provided bridge or a public promise for every Codex installation. Use its actual rendering contract only when present. |
| MCP Apps | [Overview](https://modelcontextprotocol.io/extensions/apps/overview) and [client matrix](https://modelcontextprotocol.io/extensions/client-matrix) establish a real portable UI standard and capability negotiation. Tool support alone does not establish UI support. |
| OpenAI shared plugins | [UI documentation](https://developers.openai.com/plugins/build/chatgpt-ui) and [troubleshooting](https://developers.openai.com/plugins/deploy/troubleshooting) distinguish tools in ChatGPT/Codex from the documented ChatGPT component renderer. Do not equate ChatGPT UI support with Codex UI support. |

No new MCP server is required for this change: it adds dependencies, lifecycle, file-serving and authorization work without establishing the specific Claude Code/Codex support requested. Reconsider it only for a concrete workflow on verified MCP Apps clients.

## Auto decision

Retain the persistent boolean toggle. Ask and Plan already share Pip's whole-chain approval; their useful distinction is an explicit run budget and finite additional attempts, not a new permission hierarchy.

| Command | Scope |
|---|---|
| `auto`, `auto on`, `auto off` | Existing persistent cost-confirmation setting. |
| `auto status` | Read-only actual settings and unresolved legacy-policy notice. |
| `auto plan B [R]` | One identified requested run: generation ceiling B, at most R additional paid attempts across the chain, default zero, whole-plan approval even if standing Auto is on. No persistent mutation. |
| `auto reset` | Explicit migration: discard exactly the prototype `level`, `budget`, `retries` fields and disable Auto, preserving unrelated configuration. Never grants spending permission. |

Budget B is finite/nonnegative, including fractional generations; R is a nonnegative integer. A cap does not authorize unspecified attempts, scopes, visual delegation, locally drawn pixels or playback changes. Without an identified task, clarify the target instead of saving a latent future permission. Reuse the existing cost card, manifest evidence and conservative `committed` admission. No runner, scheduler or second plan store.

Legacy policy must not silently become unlimited Auto. Status exposes those three fields separately; effective Auto remains off until reconciliation. Off remains available, enabling is blocked while legacy fields remain, and reset requires an explicit accepted discard. This deliberately consolidates the useful interface without preserving cross-project installation-wide budget defaults. Existing project restrictions remain independently applicable.

## Panel decision

One `/pixellab-pip panel` route loads one reference. Prefer a visible supported native panel tool. Otherwise render the shared HTML review in an available browser or supported inline surface. Warn when native UI or direct feedback submission is unavailable; retain ordinary chat/files when no interactive renderer exists.

One on-demand Python snapshot helper reads the explicit selected project/run and exact selected images. It reuses existing style/manifest readers and accounting. No recursive project index, database, guessed latest run, second ledger or tool-output cost parsing. The snapshot is private review material, not permission or a new canonical audit source.

Snapshot fields include project/run, capture time, effective style label, selected-run known/unknown charged and committed usage, job observations, explicit image roles/paths/content hashes, manifest hash and visible warnings. Content is bounded, image decoding uses the existing patched-decoder guard, and resolved input/output paths stay inside the selected project. Original art/config/ledgers are never replaced by review output.

The shared HTML offers equal pixel-scale image comparison, GIF viewing, zoom, notes and scoped request composition. It works without network, services, credentials or build dependencies. Ordinary browser feedback is explicitly copied back to chat; a copy button does not claim that an action was submitted. A host-specific inline fragment is generated only for a renderer that requires one. When that renderer exposes its documented follow-up-message bridge, a user-clicked send control hands the scoped request to the host and respects confirmation/cancellation; it never claims to approve or complete paid work.

The ordinary Claude plugin adds a thin native tool/view, not another Studio edition. It reads the same snapshot and routes button requests back to Pip with selected project/run and content identities. It never writes config/manifests or calls PixelLab. Unsupported SVG/oversized preview states are visible and cannot approve unseen art. Native GIF playback is not promised; the HTML view supplies it.

Before acting on review feedback, verify the snapshot's selected files and manifest still match. A same-length replacement invalidates old review identity. Requests to animate/redo remain subject to normal scope, route and cost approval; local UI state cannot grant authority. Preview readiness is separate from cost/style warnings: unknown accounting does not prevent inspecting art or composing a request, while the cost gate still blocks unbounded admissions. Both views consume one bounded label dictionary, with agent-supplied translations rather than a separate translation service.

## Deliberate differences from the original panel

| Original feature | Revised disposition |
|---|---|
| Visual pose comparison and correction notes | Preserve in shared HTML and supported native view, with content identity. |
| Animation/redo buttons | Preserve as scoped requests, followed by verification and the canonical gate. |
| GIF/sheet access | Preserve through explicit selected review assets; no filename-based final-status claim. |
| Project/style context and onboarding | Preserve visible context and scoped requests; no silent folder/style/policy creation. |
| Request shortcuts | Preserve through request composition routed to the existing skill. |
| Usage/activity | Show recorded selected-run observations and uncertainty. Remove invented live/session accounting. |
| Auto-opening and four-second scan | Replace with deliberate opening and snapshot refresh; no hidden project scanning or live-state claim. |
| Ask/Plan/Auto presets | Consolidate into Auto; no hardcoded 50-generation/two-redo permission. |
| Install-time key/MCP setup | Keep canonical Pip setup, not a second credential/connector configuration. |

This is useful feature preservation with explicit behavior changes, not a claim of exact prototype parity.

## Independent challenges before implementation

Three reviewers independently researched Auto, Claude's native API and portable presentation. Their objections changed the plan: preserve actual UI rather than text-only links; keep run-scoped structured budgets; block legacy-policy widening; expose a native tool rather than a colliding command; distinguish Claude Code from Claude chat; never infer Codex MCP Apps UI; keep snapshots truthful and selected; bind feedback to content; avoid a new server and separate policy framework.

All three accepted this architecture subject to the safeguards above. They will cross-review changes rather than solely approve their own implementation. Prior green CI does not validate the new panel or settle remaining product tradeoffs.

## Verification and delivery

Require meaningful regressions for legacy-policy migration/preservation, wrong-project actions, changed same-length art, failed/unknown charges, path/symlink/alias protection, malformed data, HTML injection, unsupported surfaces and no settings/spending during view operations. Exercise the actual Claude plugin validator/test runner and browser interactions; distinguish mocks from live-host tests. Run `python dev-tools/qa.py` after integration and re-review accepted fixes. No paid PixelLab calls are needed.

The Claude handoff must explicitly prohibit edits, commits, pushes, installs, paid calls and external messages. Claude supplies findings and proposed fixes to the user, who returns them to Codex. Earlier removal decisions and these restoration choices are both review targets.

## Findings during implementation and cross-review

- Shared Python UTC timestamps and optional historical job fields initially disagreed with native parsing. Corrected the interface and added a native fixture captured from the actual Python builder, not a separately invented schema.
- Verification initially needed stronger binding between embedded preview bytes, disk files and returned feedback identities. Both hashes are now checked; changed content cannot inherit a prior review.
- A single warning flag unnecessarily blocked art requests when only cost/style data was uncertain. Separated explicit preview readiness from those observations, while retaining the canonical paid-admission boundary.
- Fixed English labels conflicted with Pip localization. Added a finite shared label map with validated, literal translated overrides; no translation engine or duplicate defaults.
- Private snapshots could escape ignored output through arbitrary output folders or a redirected generations root. Restricted private output to the unredirected generations tree and retained explicit alternate source-run locations with a safe default output.
- Native module-variable note changes needed explicit invalidation. Corrected controlled input updates and preserved literal feedback instead of silently truncating it.
- An existing settings fallback could report success without becoming active. Writes now verify active read-back and reject a fallback shadowed by an immutable authoritative config. This preserves honest failure instead of inventing an override system.
- Further malformed-setting cases could hide restrictions behind a permissive fallback. Those cases are explicit repair boundaries, not permission to spend or replace corrupt config bytes with a clean template.
- Shared sound/Auto persistence prose was challenged for duplication; it is consolidated into one existing reference rather than another settings layer.
- Cross-host packaging research found that Codex also discovers root `hooks/hooks.json`. Claude's ordinary manifest explicitly selects `hooks/claude/hooks.json` instead; no default hook file leaks Claude modules into other hosts. This uses [documented OpenAI discovery behavior](https://developers.openai.com/plugins/build/plugins) and [Claude's custom hook path](https://code.claude.com/docs/en/plugins/manifest-reference#hooks), verified by the actual Claude validator/test runner. It adds no second package or Codex override.

Initial integrated QA passed 330 tests without skips before the last malformed-config and alternate-output corrections. Final validation must cover those corrections; historical/passing earlier-head checks do not substitute for it.

The reopened original findings now close through preserved behavior rather than deleting the UI:

| Finding | Replacement evidence |
|---|---|
| R02 hidden global policy change | Opening and setup requests read a snapshot/compose a draft; no settings writer, connector or default budget exists in the adapter. |
| R08 wrong project | Every request carries the displayed root, run and exact image identities; current-file verification and the selected root remain required in the core. |
| R23 stale panel authority | Timestamped, hash-bound observations; canonical ledger accounting; no optimistic permission state or cached approval. Unsupported previews cannot approve unseen content. |
| R24 edition release drift | One ordinary plugin/version owns the native adapter; no separately versioned Studio distribution. Existing real release-bump checks remain applicable. |

## Current acceptance evidence and limits

- Integrated `python dev-tools/qa.py`: **337 tests passed, no skips**, all repository checks passed with patched Pillow 13 and the image/scientific dependencies available. This includes the malformed-config, alternate-run, private-root and cross-host packaging regressions, plus existing release-bump/raw-skill packaging checks.
- Actual Claude Code 2.1.303: `claude plugin validate . --json` succeeds and recognizes the explicitly selected nested module; `claude plugin test .` passes **14 native tests**. Unsupported terminal/GIF selections explicitly return the generated HTML's path to the agent, which cannot read its own rendered pane. The existing root contributor `CLAUDE.md` context warning is unrelated to the adapter. The native fixture was captured from the Python builder, with its project root anonymized.
- Actual headless Edge: four image previews, including the original GIF, decoded; shared zoom changed the displayed scale; composed animation feedback retained selected project/run/digests and literal script-looking notes; no page network requests or runtime exceptions occurred. Desktop and narrow-screen screenshots were inspected.
- The actual HTML template's JavaScript DOM smoke exercises translated labels/notes, click-only inline bridge handoff, standalone/missing-bridge fallback and failed-image invalidation. This is simulated host-bridge evidence, not a live Codex confirmation test.
- Three independent reviewers cross-audited the changed files and reopened prior closures, exchanged reproductions/counterarguments, and accepted the fixes above. Their final audit identified no remaining concrete actionable finding in that scope. Agreement is not proof that no future defect can exist.
- A fresh evaluator with no prior design discussion applied the skill to four offline requests: bounded planning with standing Auto on, a plan without a task, project B from project A on a host without a renderer, and same-length stale art with Auto on. All four chose the intended approval/scope/fallback/identity boundaries. Two minor wording concerns led to removing a duplicated global Auto summary and clarifying that chat-only fallback need not generate unused HTML.
- No paid PixelLab calls, real engine imports or live Claude Desktop/VS Code painting were performed. Native element-tree tests do not prove final SVG painting. Actual inline-host confirmation/cancellation remains a live-host verification limit. Unsupported surfaces and oversized selections retain explicit HTML/chat alternatives.
- Historical CI links in the original record apply to their pinned commits. New published checks must be verified against the new head after push; local QA output is not evidence of new remote CI success.
- The private Claude handoff is findings-only, validated separately, and includes both source skills, research, all 29 findings, the removal inventory, the new design and these limitations. The user will return Claude's findings to Codex before any merge decision.
