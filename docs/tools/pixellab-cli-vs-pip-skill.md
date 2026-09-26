# PixelLab CLI vs Pip Skill

Last reviewed: 2026-09-26, against `protonspy/pixellab-cli` `main` at commit [`6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2`](https://github.com/protonspy/pixellab-cli/commit/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2) (2026-09-22) and PixelLab Pip at repository commit `b0a93b6d9f61866c8b4e6bdbd9f6b694cd54ff94`.

This compares PixelLab Pip with the **whole** [`pixellab-cli`](https://github.com/protonspy/pixellab-cli) project: a Python command-line application and its companion, task-specific agent skills. It is not just a skill-to-skill comparison. The projects overlap in helping agents produce PixelLab assets, but the CLI is an execution product and Pip is an agent-facing router that augments the PixelLab MCP service. The goal is to describe the real tradeoffs and decide whether any CLI behavior belongs in Pip, not to rank or copy the projects.

## Sources reviewed

- The CLI [README](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/README.md), [`pyproject.toml`](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/pyproject.toml), and current source for [paid-call gating and execution](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/src/pixellab_cli/run.py), [ledger](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/src/pixellab_cli/ledger.py), [recipes](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/src/pixellab_cli/commands/recipe_command.py), [credential resolution](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/src/pixellab_cli/config.py), and [agent setup](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/src/pixellab_cli/commands/setup.py).
- The CLI's [main asset skill](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/src/pixellab_cli/skill/pixellab-cli-assets/SKILL.md), [generation-record guide](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/docs/wiki/pages/generation-record.md), and [CLI-vs-MCP decision](https://github.com/protonspy/pixellab-cli/blob/6fe32ba3d341fcec44d42cdb3f1710f8e4a131c2/docs/adr/0003-a-cli-and-a-skill-rather-than-an-mcp-server.md).
- Pip's [`SKILL.md`](../../skills/pixellab-pip/SKILL.md), plus its references for [cost approval](../../skills/pixellab-pip/references/auto.md), [cost routing](../../skills/pixellab-pip/references/cost-routing.md), [job lifecycle](../../skills/pixellab-pip/references/job-lifecycle.md), [usage reporting](../../skills/pixellab-pip/references/usage-reporting.md), [animation](../../skills/pixellab-pip/references/animation.md), and [blueprints](../../skills/pixellab-pip/references/blueprint.md).
- The [piwheels package-history mirror](https://www.piwheels.org/project/pixellab-cli/) was last updated 2026-09-15 and showed only `0.1.0` at that snapshot. This is not a live PyPI check on the review date.

No paid PixelLab or fal calls were made, and the CLI test suite was not run. This review assesses documented and implemented workflow behavior, not generated-image quality or runtime reliability.

## Summary

`pixellab-cli` ships a real local execution path: typed commands over a curated REST v2 surface, a companion skill that teaches those commands, persistent output records, and recipe resume. It also includes optional fal-backed concept-art workflows. It does **not** expose an MCP server.

Pip is a portable skill contract for deciding how an agent should use PixelLab: prefer configured MCP for normal managed-asset work, fall back to documented REST v2 for code/exact control or missing MCP capabilities, and route to website/editor or Aseprite/Pixelorama workflows where appropriate. Pip does not ship an execution client or recipe runner.

Use the CLI when a user wants its repeatable terminal workflow, persistent transaction history, resumable recipes, or local engine export. Use Pip when the user wants PixelLab MCP augmented with cross-surface routing, task-specific guidance, cost approval, and output verification without installing a separate Python application. The two can coexist as tools in a shell-capable environment, but they have overlapping agent instructions; there is no need to install both skill sets merely to use PixelLab MCP.

## Feature comparison

| Area | `pixellab-cli` project | PixelLab Pip skill |
|---|---|---|
| Product contract | Python CLI plus companion skills; the same command implementation serves people and agents. | Agent instructions that route the host's available tools; no Pip-owned PixelLab execution binary. |
| Default PixelLab surface | Direct calls to PixelLab REST v2 from the CLI. The repository's decision record explicitly chooses a CLI plus skill and no MCP server. | MCP first when a suitable tool is visible; documented REST v2 for code, exact control, or MCP gaps; other documented PixelLab surfaces remain available when relevant. |
| Capability boundary | A substantial but curated command set for image, character, animation, tiles, object, UI/font, edit, and asset workflows. Its command/schema implementation is not the entire PixelLab product surface. | Cross-surface route selection, including MCP platform tools, REST-only operations, website/editor workflows, Aseprite and Pixelorama boundaries, and legacy v1 constraints. Exact parameters are refreshed from current official schemas. |
| Agent integration | `setup` installs its skill/instructions into the harnesses it currently targets (Claude Code, Codex, and opencode). The agent must be able to invoke the installed command through a shell. No MCP tool list is added. | Portable skill content for skill-capable agents; uses MCP tools already exposed by the host when configured. It can still answer setup/routing questions when MCP is absent. |
| Paid-call gate | The runner refuses a paid invocation without `--yes`; `--dry-run` shows the request without sending it. Unknown cost is treated as unknown, not free. `PIXELLAB_ASSUME_YES` is an explicit headless bypass, and the companion skill says the person must set it. | An agent-facing gate plans the full paid chain and asks once before the first call when `auto` is off (the default); it shows the exact material inputs and rough costs. The agent must follow that contract. Unapproved extra paid work needs separate approval. |
| Usage record | Writes an append-only per-call ledger intent before the call and records outcome, estimate, reported cost when available, IDs and files afterward. A call that may have been charged can remain visible as unresolved. | Requires a private generation manifest with per-call IDs and seeds, accurate cost reporting in chat, and persistence/polling of returned jobs. It does not currently prescribe a separate append-only ledger or require actual usage in the manifest. |
| Multi-step work | Ships recipes such as concept-to-sprite and character workflows. Recipe state is saved and `resume` skips completed steps; default workflow pauses so a person can correct an intermediate image. | Blueprints capture exact MCP/REST calls and material local tasks for later replay, but the host agent executes them; there is no Pip runner that owns recipe state. |
| Cost and provider coverage | PixelLab estimate and reported usage are distinct in the ledger. fal is optional, but its calls have no published/provider-reported cost in this project; the ledger labels that cost unknown. fal can produce concept art that PixelLab cannot. | PixelLab route/cost guidance and balance snapshots; report returned usage or an observed balance delta without inferring a conversion. Pip is scoped to PixelLab and does not add fal as a second provider. |
| Local files | Includes Pillow-based local image operations and export commands for a TexturePacker atlas and a Tiled tileset. The latter is not a Tiled map. | Uses the host's local tools for allowed inspection, verification, assembly, and packaging, with explicit pixel-integrity rules. It does not ship an image CLI or engine adapter. |
| Credentials | Resolves `PIXELLAB_SECRET` and optional `FAL_KEY` from environment/config sources; supports a home-file password-manager command, redacts credential values from records, and prevents commands in a project config file from executing. | Uses host secret settings or a user-scoped `PIXELLAB_SECRET`; never asks users to paste bearer tokens in chat and avoids broad `.env*` inspection. |
| Runtime requirements | Python 3.12+, `uv` for the documented install, a shell, and the CLI's Python dependencies. The fal account is optional, but `fal-client` is a declared package dependency. | Skill installation and a host that can expose the required MCP tools or perform documented REST/local actions. Pip itself has no Python package requirement. |

## Pros and cons

### Where the CLI is stronger

- The paid-call boundary is enforced in the runner rather than being only an instruction to an agent. Each CLI invocation needs its own `--yes`; a user-configured headless environment variable can intentionally replace that interaction.
- The ledger and recipe manifest are durable, machine-written state. This is useful when a long workflow spans terminals or agent sessions: actual outcomes, failed/unresolved calls, route IDs, output paths, and completed recipe steps are not reconstructed from chat history.
- Its recipes encode a particular production sequence and stop at human-edit checkpoints. Its local image helpers and engine exports cover work after PixelLab returns files.
- Optional fal integration makes the CLI useful for flows that intentionally start with non-pixel concept art or produce non-pixel deliverables. That introduces another account/provider and unknown fal spend, and is outside Pip's PixelLab-only routing scope.

### Where Pip is stronger

- Pip works with PixelLab MCP instead of replacing it. It can use managed-asset tools and can choose REST or manual/editor surfaces where an MCP tool does not fit.
- Its route contract is broader than one executable command tree and applies in hosts where Python installation or shell execution is unavailable, provided the relevant PixelLab tool is exposed.
- It carries cross-surface behavior around image-role classification, request ambiguity, setup and credential safety, localization, cost choice, asset integrity, and result verification. The host agent performs the actions rather than inheriting a second route client and schema copy.
- Its blueprints are shareable exact-call records and can include ordered `TASK` steps; the distinction is that replay is performed by the agent, not by a Pip runner.

### Costs of each approach

The CLI's strongest benefit—controlling and recording the call path in code—has a matching maintenance cost: it owns command behavior, route validation, a vendored API schema, output conventions, credential resolution, and package release state. The reviewed source and installable package may not be at the same feature level: `main` declares version `0.7.0`; its README says `0.1.0` was the manual PyPI release and that the next tagged release would start at `0.2.0`; the piwheels snapshot last updated 2026-09-15 showed only `0.1.0`. The mirror is not a live PyPI check for 2026-09-26, so verify the current published artifact before assuming `uv tool install pixellab-cli` provides the reviewed `main` features.

Pip has the inverse tradeoff. It avoids a second runtime and can route into the configured MCP service, but it cannot make its prose rules an unconditional runtime enforcement boundary. It also does not give the user the CLI's append-only per-call ledger or automatic recipe runner. Existing Pip job-persistence rules and manifests cover common continuation needs, but the host agent must actually follow them.

## When to use `pixellab-cli` over Pip

Prefer the CLI when the user explicitly wants a local, repeatable terminal tool and one or more of these matter:

- They want to run or automate supported PixelLab workflows from a Python game repository or CI job, and can provide Python 3.12+, shell access, and the required credential safely.
- They want the CLI's hard `--yes` invocation gate, local ledger, output manifests, and resumable built-in recipes as one product.
- They need its local image utilities or TexturePacker/Tiled export for files the user or PixelLab already produced.
- They deliberately want a fal-backed concept-art step as part of a PixelLab pipeline and accept the separate provider/account and its unreported spend.

Prefer Pip and PixelLab MCP when tools are already configured and the request is ordinary interactive asset work, needs a managed PixelLab object, needs the broader PixelLab surface router, or must run in an agent host without installing and launching the CLI. Pip is also the better fit for PixelLab website/editor, Aseprite, and Pixelorama assistance, which the CLI does not provide.

The CLI's presence is not a reason to add it as Pip's default backend. If a user explicitly asks to use the CLI, Pip can describe the tradeoff and the user can invoke it; Pip should not silently switch from MCP to an external executable.

## Pip gaps and verdicts

These judgments assess the current need in Pip, not whether the feature is useful in the CLI.

- **Adopt, narrowly: preserve exact reported PixelLab usage in the existing private manifest.** Pip already reports exposed actual usage in chat, while the private manifest's written contract names call/result IDs and seeds but does not require the returned usage values. A later continuation can use its existing audit/resume file to see what the earlier call actually reported. Extend only `references/usage-reporting.md`; store exposed `usage.generations` and/or `usage.usd` per call under clearly named units, preserve both when present, and omit either when absent. Never put estimates or account-balance values in the manifest, and never convert USD to generations. This is a small proposed follow-up, not implemented here.
- **Already covered: pre-call cost approval, budget-sensitive routing, actual usage reporting, and async job resumption.** Keep Pip's current full-chain approval gate, per-retry approval rules, and job-ID polling contract; a second confirmation scheme would duplicate these decisions.
- **Defer: an append-only attempt ledger.** The CLI's crash-recovery ledger is a genuine advantage, but Pip already requires writing the returned job/asset ID as each response arrives and resuming through the matching getter. Do not add a second record format until a verified Pip-compliant run demonstrates the existing manifest/poll contract cannot preserve a returned job ID or actual usage across a host interruption. A helper or ledger should follow that evidence, not precede it.
- **Skip: a Pip CLI, `pixellab-cli` wrapper, or second REST client.** This is a separate execution product, not a small skill enhancement. It would duplicate the external CLI and its maintained route/schema/auth layers, narrow Pip to shell-capable hosts, and create another path beside PixelLab MCP.
- **Skip: vendoring the CLI's entire route schema or command catalog into Pip.** Exact fields belong to connected MCP schemas or current official REST docs; copying them into runtime text would make two freshness surfaces to maintain.
- **Skip: multiple Pip skills to mirror the CLI's command-specific skill split or a bundled recipe runner.** Pip already loads task-specific references on demand and supports agent-executed blueprints. Add a distinct runtime file or helper only after a repeated workflow cannot fit the existing canonical reference.
- **Reject for Pip: fal integration.** It adds a separate provider, credential, billing model, and product scope. PixelLab MCP augmentation does not require it.
- **Defer: a small Python helper for local image work.** Consider only a narrow, deterministic script when repeated user tasks show the same local inspection/assembly step is error-prone or unavailable in common host tools. It should supplement one existing reference, not become a public command tree, API client, package, installer, or separate skill.

## Freshness and evidence limits

The comparison uses the exact upstream commit above; later `main` changes may change command behavior. The CLI's documented package-install route and checked-out source version differ as noted. The CLI suite was inspected but not run. No claims here compare generated art quality, speed, or billed outcome; those require separate controlled work. Pip feature claims describe the checked-out repository at review time and should be refreshed against current official PixelLab docs when exact endpoints, schemas, costs, or host setup are the decision.
