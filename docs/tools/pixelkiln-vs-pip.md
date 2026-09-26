# PixelKiln vs PixelLab Pip

Last reviewed: 2026-09-26, against PixelKiln v0.80.0 at Git commit [`f6d478aec1424f5f6d6d924f465e670f557259e7`](https://github.com/gfargo/pixelkiln/tree/f6d478aec1424f5f6d6d924f465e670f557259e7) and PixelLab Pip at repository commit `b0a93b6d9f61866c8b4e6bdbd9f6b694cd54ff94`.

Terminology: the subject here is **PixelKiln** (`gfargo/pixelkiln`), which ships a `pixelkiln` CLI. This is not a comparison with the separate `pixellab-cli` repository.

Sources reviewed:

- PixelKiln [README](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/README.md), [provider comparison](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/PROVIDERS.md), [agent workflow docs](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/docs/AGENTS.md), bundled [PixelKiln Agent Skill](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/skills/pixelkiln/SKILL.md), [CLI reference](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/docs/CLI.md), [PixelLab adapter guide](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/docs/PIXELLAB.md), and [architecture](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/docs/ARCHITECTURE.md).
- PixelKiln implementation at the same commit: [CLI entry point](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/src/cli.ts), [PixelLab REST client](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/src/client.ts), [PixelLab provider](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/src/providers/pixellab.ts), [offline plan](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/src/pipeline/plan.ts), and [lockfile](https://github.com/gfargo/pixelkiln/blob/f6d478aec1424f5f6d6d924f465e670f557259e7/src/lock.ts).
- PixelLab Pip [SKILL.md](../../skills/pixellab-pip/SKILL.md), [usage reporting](../../skills/pixellab-pip/references/usage-reporting.md), [blueprints](../../skills/pixellab-pip/references/blueprint.md), [candidate review](../../skills/pixellab-pip/references/reviewable-candidates.md), and [local assembly](../../skills/pixellab-pip/references/local-asset-assembly.md).

This is a repository and documentation review, not an install, runtime, or paid-generation comparison. PixelKiln's provider maturity statements are its documented status; no comparative output-quality or cost benchmark was run here. PixelKiln's `main` branch and pre-1.0 releases move quickly, so the findings are pinned to the revision above.

## Summary

PixelKiln is a project-level asset build pipeline. Its Node.js CLI and TypeScript library read a committed manifest, compare it with a lockfile and files on disk, run budgeted PixelLab REST requests, guide human candidate selection, recover paid jobs and downloads, and package accepted outputs with provenance.

PixelLab Pip is an agent skill and routing contract. It helps an agent choose among visible PixelLab MCP tools, documented REST v2, and PixelLab's website/editor and supported local-editor workflows. Pip prepares inputs, sets credit and credential boundaries, handles task-specific PixelLab guidance, and reports and verifies results. Its per-flow manifest and replayable blueprint support a generation workflow; they are not a project-wide manifest/lock state machine.

These operate at different layers. Use PixelKiln when a game repository needs a repeatable, reviewable asset pipeline. Use Pip when an agent needs to choose and use the right PixelLab surface for a one-off request, an MCP task, or work outside PixelKiln's adapter. PixelKiln's own guide describes the official PixelLab MCP server as a complementary direct-generation surface.

## What Each Project Provides

| Area | PixelKiln v0.80.0 | PixelLab Pip |
|---|---|---|
| Product layer | Node.js CLI plus a public TypeScript library; requires Node.js 22 or newer. | Portable Agent Skill with `SKILL.md`, on-demand references, blueprints, and small Python helpers; no Pip CLI product. |
| PixelLab execution | Its PixelLab adapter calls public REST v2 directly. The client uses `PIXELLAB_API_KEY`; it does not call PixelLab MCP. | Prefers visible PixelLab MCP tools for supported work, with documented REST v2 fallback and other surface routing. |
| Project model | Committed `pixelkiln.manifest.json` expresses desired assets; `pixelkiln.lock.json` tracks provider jobs, files, hashes, history, and available billing data. Offline `plan` diffs manifest, lock, and disk. | Writes a private manifest per live generation flow and a separate shareable blueprint. It records call inputs and IDs, supports resuming from saved IDs, and does not diff the entire project against a persistent generation lock. |
| Cost handling | Plans estimated work and checks `--budget` ceilings in provider-specific units. The lock distinguishes estimated `cost` from provider-reported `billed` when available. The wave budget still uses estimates; a reported charge may be absent or differ. | Explains route costs, requests approval before paid work and extra attempts, and reports returned per-call usage or a carefully labeled balance observation. The manifest contract currently records IDs and seeds, not the actual per-call usage amount. |
| Human review | Built-in local picker and provenance gallery; selection stays with the person, and unresolved candidates remain pending. | Agent presents candidate choices and waits for the user's selection. A temporary indexed contact sheet is allowed, but Pip does not ship a full project gallery or review application. |
| Recovery and provenance | Resumable submit/poll/pick/fetch stages, content-addressed cache, hash-based file ownership, restore/history, and durable project records. | Keeps job/asset IDs, polls the matching getter, and records per-flow call details; no project-wide stale-file detection, lock reconciliation, or cache restore pipeline. |
| Quality and packaging | Selected styles can define grid/palette checks and named approval. Commands package and export sprite sheets, engine metadata, and tilesets with provenance. | Provides task-specific verification guidance, pixel-preserving local assembly, and Aseprite/editor handoffs. It does not define a general project-level quality gate or engine-export pipeline. |
| Providers | PixelLab is documented as the production adapter. Retro Diffusion, ComfyUI, and Scenario are experimental, with limits and live-test coverage documented per adapter. | PixelLab-specific. It routes among PixelLab's MCP, REST, website/editor, Pixelorama, Aseprite, and legacy v1 surfaces rather than abstracting multiple image providers. |
| PixelLab product coverage | Selected REST workflows only. PixelKiln documents Game Builder, editor plugins/Pixelorama, Map Workshop, and vocal/lip-sync workflows as outside its adapter. | Broader PixelLab surface routing and task guidance, including MCP-only and editor/manual workflows, subject to the documented public-vs-private boundaries. |

## PixelKiln Strengths And Tradeoffs

### Strengths over Pip

- A committed asset manifest plus lockfile gives a team a durable view of missing, stale, current, failed, recoverable, and manually changed outputs before a provider call.
- `plan`, per-run provider-unit ceilings, and explicit user approval make a batch's intended spend inspectable. The ceiling applies to PixelKiln's computed estimate; it is not a guarantee that every provider's final charge will equal that estimate.
- Remote job IDs are saved as work progresses. A failed download can be resumed without buying the image again, and exact output hashes help protect hand edits and identify drift.
- Built-in candidate picking and a provenance gallery put review, previous generations, prompt/cost history, and comparison in one project workflow.
- Deterministic packing, engine exports, quality profiles, and approval checks suit game repositories that need committed outputs with a verifiable source trail.
- The provider interface can route one manifest across providers, but maturity varies. PixelLab is the production adapter; the others remain experimental as of the reviewed revision.

### Tradeoffs compared with Pip

- The project takes on a Node.js dependency, manifest and lockfile conventions, provider credentials, and an opinionated asset lifecycle. That setup is valuable for recurring project work, but unnecessary overhead for a one-off PixelLab request.
- PixelKiln uses REST v2 instead of visible MCP tools. Its own PixelLab guide says the adapter does not cover all PixelLab product surfaces, including Game Builder, editor plugins/Pixelorama, Map Workshop, and vocal/lip-sync workflows.
- Its useful route choices are generators and workflows inside its project pipeline. Pip provides broader agent-side routing, prompt and input-role rules, setup guidance, and cost/safety decisions for PixelLab tasks that are not part of a PixelKiln manifest.
- The project is pre-1.0 and fast-moving. Provider capabilities and live confidence must be read at the pinned revision rather than assumed from the generic provider interface.

## When To Use PixelKiln Instead Of Pip

Choose PixelKiln when:

- The assets belong to a persistent game project and should be declared, versioned, reviewed, and regenerated as a set.
- The user needs an offline manifest/lock/disk plan before generation, project-level change detection, or multi-provider budgets kept in separate units.
- The task needs safe recovery of interrupted paid work, provider-job history, output hashes, hand-edit protection, or a durable record for later collaborators.
- The deliverable needs a human candidate-selection workflow followed by repeatable sheet, atlas, tileset, or engine packaging.
- The project has a PixelKiln manifest and the user explicitly wants that manifest-driven workflow. Use PixelKiln's own agent skill for those assets so direct calls do not bypass its plan, budget, or lockfile.

Prefer Pip when:

- The user wants direct PixelLab MCP work, or needs an agent to decide between MCP and documented REST v2.
- The request is a one-off generation, edit, animation, setup, troubleshooting, or PixelLab capability question without a project-pipeline requirement.
- The right path is a PixelLab surface that PixelKiln does not model, such as a supported MCP platform tool, website/editor workflow, Aseprite/Pixelorama handoff, or another documented PixelLab route.
- The agent needs Pip's prompt preparation, supplied-image role classification, route-specific cost guidance, auth boundaries, or result-verification/reporting contract.
- The user does not want a Node-based project dependency or a committed manifest/lockfile.

Use both when a project uses PixelKiln for manifest-owned generation and a separate task needs Pip's PixelLab guidance. Keep the work boundaries explicit: PixelKiln owns assets declared in its manifest; Pip handles independent PixelLab questions or tasks the user intentionally keeps outside that pipeline. Do not make direct Pip calls for a manifest-owned asset in a way that leaves its lockfile out of date.

## Pip Implications

PixelKiln does not justify copying its project pipeline into Pip. Pip already has per-flow manifests, resumable PixelLab IDs, blueprints, candidate-selection rules, local assembly, and Aseprite/editor handoffs. A project-wide manifest/lock, cache, candidate gallery, provider abstraction, CI package gate, or engine-export system would change Pip's purpose and duplicate substantial machinery.

There is one smaller reporting gap worth considering: Pip tells the agent to report actual `usage.generations` or `usage.usd` in chat, but the canonical per-flow manifest fields explicitly retain IDs and seeds rather than returned usage. An optional per-call `reported_usage` record with only the `generations` and/or `usd` fields actually returned by PixelLab would make later continuation and budget recalculation more reliable. Omit it when usage is unavailable. Never persist estimates, account balances, or before/after balance deltas. This is a small extension to the existing manifest contract, not a new ledger or execution interface. No runtime changes are made in this research spike.
