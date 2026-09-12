# PixelLab MCP Docs vs Pip Skill (Session Context)

Last reviewed: 2026-09-12.

This is a decision guide for one specific choice: what PixelLab context to give a coding agent for a session. The two options are PixelLab's official MCP documentation, injected as a prompt link, versus installing the PixelLab Pip Agent Skill. It is a session-context question, not a service question; for the execution-layer comparison (MCP service vs the skill) see [Official PixelLab MCP Service Comparison](official-pixellab-mcp-service-comparison.md).

Sources reviewed:

- [PixelLab MCP tool guide](https://api.pixellab.ai/mcp/docs).
- [PixelLab MCP setup page](https://www.pixellab.ai/mcp).
- [PixelLab Pip `SKILL.md`](../../skills/pixellab-pip/SKILL.md) and its `references/`.

## What Each Option Is

**Official MCP docs as context.** The setup page tells users: "Include this link in your prompts for a complete overview of all PixelLab tools: `@https://api.pixellab.ai/mcp/docs`." That URL is one flat document listing the hosted MCP tool inventory (106 tools in the latest 2026-09-12 snapshot, including six new Pro Fast tools), the return-ID-then-poll `get_*` job model, UUID download links, bearer-token auth, and engine implementation guides exposed as `pixellab://` resources. It is first-party and live, but its generated examples and prose can disagree with its own parameters; no install is needed to read it.

**Pip Agent Skill.** A skill installed into agents that support skills. `SKILL.md` (the always-loaded router) plus 32 on-demand `references/*.md` cover surface selection across MCP, REST v2, website/Pixelorama editor, Aseprite, and legacy v1, plus cost routing, prompt preparation, secret-handling guardrails, and output verification/reporting. The two are complementary, not rivals.

## Scope

| Area | Official MCP docs | Pip Skill |
|---|---|---|
| MCP tool inventory | Yes — full 106-tool list, authoritative for documented tool names | Partial — routing tables; defers to mcp/docs and visible tool schemas for exact calls |
| REST v2 coverage | Linked and described as an alternative, but no route inventory | Yes — endpoint router and fallback policy |
| Other PixelLab surfaces (Aseprite / Pixelorama / website) | Names them, but gives no operating workflow | Yes |
| Engine integration guides (Godot / Unity / Python) | Yes — via `pixellab://` resources | No |
| Cost / credit control | Per-tool estimates, but no cross-route approval or retry policy | Yes — `references/cost-routing.md` and the paid-call gate |
| Prompt preparation | Partial — parameter examples | Yes — enhancement and text-prep rules |
| Auth / secret handling | Partial — bearer header setup | Yes — `PIXELLAB_SECRET`, no-paste guardrails |
| Output verification / reporting | No | Yes — `references/usage-reporting.md` contract |
| Setup | Partial — per-client config snippets | Yes — interactive setup wizard |
| Image-role classification | No — lists image params only | Yes — edit / identity / style / mask / palette / frame roles |
| Localization (non-English requests) | No | Yes — normalize to English, reply in the user's language |
| Output integrity | No | Yes — "every pixel from PixelLab"; local processing labeled, not passed off as generated |
| Token footprint | ~104.9k chars (~26.2k est tokens), one flat all-or-nothing document | `SKILL.md` ~49.5k chars (~12.4k est tokens) always, plus 32 `references/*.md` files loaded on demand |

Token counts are estimated as chars/4 and re-measured after the Pro Fast refresh. The footprints are not directly comparable: mcp/docs loads in full whenever the link is fetched, while Pip loads `SKILL.md` every time and pulls only the references a task needs. Pip's always-on floor remains below the flat MCP document.

## What The Current Official Guide Gets Wrong Or Leaves Unsettled

- Its opening says that if MCP tools are absent, an agent should not try REST v2, yet its own “Other PixelLab Interfaces” section says REST v2 can be called directly and is useful when MCP lacks an endpoint. It also calls the two surfaces the “same functionality,” which the current parity map disproves: 25 asset REST routes lack a fully equivalent MCP tool, and 35 MCP platform tools lack REST counterparts. The opening is advice for a pure-MCP session, not a ban on Pip's documented, bearer-authenticated REST fallback. Never curl an MCP tool name as though it were a REST path.
- It calls unauthenticated download links freely shareable because their UUID is the access key. Pip treats those URLs as sensitive: anyone with the link may reach the asset, and stale links should be refreshed through the getter. Do not paste one indiscriminately.
- Its new `create_character_pro_fast` examples actually call older `create_character` with unsupported fields; its “4 directions” hint contradicts `n_directions: Literal[8]`. Both the REST OpenAPI and the MCP guide's declared parameter support eight-direction Pro Fast characters; a connected agent should still check its visible tool schema. Treat generated examples as illustrations, not executable payloads.
- The `get_image` description says it accepts any raw-image job, but its parenthetical tool list was not updated for the new Pro Fast tools (or the prior PixMiniMax tool). Pip uses the returned job ID and checks the connected getter/result rather than treating that list as a closed inventory.
- Its “all creation tools return immediately with job IDs” overview is too broad for non-generating helpers and renderers. For example, `set_character_portrait` attaches a portrait without generation, and `create_talking_gif` renders from an existing mouth-position set rather than queuing new artwork. Follow each tool's actual result shape; do not poll when it already returned a final result.
- The Pro Fast name does not prove better quality, speed, lower total cost, or byte-perfect inpainting in a live run. The official REST schema says seed is recorded but the provider does not promise deterministic output; creation pricing is provisional. Pip uses the new routes only when requested or after a cost/quality tradeoff is made explicit, and verifies the actual image and billed usage.

The complete six-tool/seven-REST-path mapping, including the REST-only provisional cost lookup, is in [MCP vs REST Route Parity](../pixellab/pixellab-mcp-vs-rest-route-parity.md). The operational contract is [Pro Fast](../../skills/pixellab-pip/references/pro-fast.md). No paid generations were used in this documentation review.

Intentionally not copied into the runtime skill: the 106-tool signature dump, general setup JSON, engine-specific examples, and marketing prose. Those remain available from the official guide when a task needs them; Pip keeps only routing, cost/safety, input-role, and verification decisions.

## Use the Official MCP Docs When

- You are doing pure MCP work in a client where PixelLab MCP tools are already configured and visible.
- You want no install and the smallest possible setup — one prompt link.
- You prefer a live first-party tool inventory over a maintained skill, while still checking its examples against the visible schemas.
- You need the engine integration guides (Godot / Unity / Python tilemaps).
- You need exact platform-tool parameters for chat, deployed agents, or the sandbox; Pip supplies only their routing and safety boundaries.
- You want an authoritative dump of every MCP tool and its parameters in one place.

## Use the Agent Skill When

- You need REST v2 fallback or exact endpoint control (batch jobs, backends, scripts, base-tier non-Pro edits/inpaints, resize, background removal, multi-image style references).
- Cost matters — cheap-vs-Pro routing and per-attempt approval before paid retries.
- You want icon, tileset, animation, or paperdoll know-how that mcp/docs does not carry.
- You want a fixed reporting and verification contract after each live call.
- You route across multiple surfaces (MCP, REST, website, Aseprite, Pixelorama, v1).
- You want secret-handling guardrails: `PIXELLAB_SECRET`, never pasting tokens into chat, no session-token scraping.

## Use Both When

The skill is installed and the agent refreshes mcp/docs on demand — Pip's own model. Pip routes, prepares parameters, and enforces safety, then fetches `https://api.pixellab.ai/mcp/docs` (or `v2/openapi.json` for REST) only when an exact tool, field, price, or schema is missing or unclear. Installing the skill does not replace the docs link; it decides when to consult it.

## Measuring the Choice

`dev-tools/skill_benchmark.py` can measure both context strategies directly. Alongside the current skill (always benchmarked) and git-ref skill variants, it defines two context-strategy arms: `vanilla` (agent knowledge only) and `mcp-docs` (the pixellab.ai/mcp pro-tip docs injected, no skill). Running the current skill against `mcp-docs` compares the two context strategies described here on the same tasks.

A recent dry, credit-free 20-scenario snapshot across three agents (`claude`, `codex`, `deepseek-v4-pro`) found the skill routed the large majority of deterministic checks correctly, while the injected docs landed around the middle — strong on pure MCP tool-selection, zero on REST-only routes and near-zero on setup — and no context at all was mostly lost. Exact percentages vary per run and go stale, so this file does not repeat them; see the Summary table in [PixelLab Pip Skill Benchmark](../pixellab-pip-benchmark.md) for the current numbers and [`dev-tools/skill_benchmark.py`](../../dev-tools/skill_benchmark.py) to reproduce.
