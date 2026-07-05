# PixelLab MCP Docs vs Pip Skill (Session Context)

Last reviewed: 2026-07-05.

This is a decision guide for one specific choice: what PixelLab context to give a coding agent for a session. The two options are PixelLab's official MCP documentation, injected as a prompt link, versus installing the PixelLab Pip Agent Skill. It is a session-context question, not a service question; for the execution-layer comparison (MCP service vs the skill) see [Official PixelLab MCP Service Comparison](official-pixellab-mcp-service-comparison.md).

Sources reviewed:

- [PixelLab MCP tool guide](https://api.pixellab.ai/mcp/docs).
- [PixelLab MCP setup page](https://www.pixellab.ai/mcp).
- [PixelLab Pip `SKILL.md`](../../skills/pixellab-pip/SKILL.md) and its `references/`.

## What Each Option Is

**Official MCP docs as context.** The setup page tells users: "Include this link in your prompts for a complete overview of all PixelLab tools: `@https://api.pixellab.ai/mcp/docs`." That URL is one flat document listing the hosted MCP tool inventory (~65 tools across characters, tilesets, isometric tiles, objects, UI, fonts, chat/agent/sandbox helpers, and balance), the return-ID-then-poll `get_*` job model, UUID download links, bearer-token auth, and six engine implementation guides (Godot, Unity, Python) exposed as `pixellab://` resources. First-party, always current, no install.

**Pip Agent Skill.** A skill installed into agents that support skills. `SKILL.md` (the always-loaded router) plus 22 on-demand `references/*.md` cover surface selection across MCP, REST v2, website/Pixelorama editor, Aseprite, and legacy v1, plus cost routing, prompt preparation, secret-handling guardrails, and an output verification/reporting contract. The two are complementary, not rivals: Pip itself treats `https://api.pixellab.ai/mcp/docs` as the authoritative MCP tool inventory and refreshes from it when a tool, field, or schema is missing or unclear.

## Scope

| Area | Official MCP docs | Pip Skill |
|---|---|---|
| MCP tool inventory | Yes — full ~65-tool list, authoritative | Partial — routing tables; defers to mcp/docs for exact schemas |
| REST v2 coverage | No — named only as an alternative | Yes — full endpoint router and fallback policy |
| Non-PixelLab surfaces (Aseprite / Pixelorama / website) | No | Yes |
| Engine integration guides (Godot / Unity / Python) | Yes — via `pixellab://` resources | No |
| Cost / credit control | No | Yes — `references/cost-routing.md` |
| Prompt preparation | Partial — parameter examples | Yes — enhancement and text-prep rules |
| Auth / secret handling | Partial — bearer header setup | Yes — `PIXELLAB_SECRET`, no-paste guardrails |
| Output verification / reporting | No | Yes — `references/usage-reporting.md` contract |
| Setup | Partial — per-client config snippets | Yes — interactive setup wizard |
| Image-role classification | No — lists image params only | Yes — edit / identity / style / mask / palette / frame roles |
| Localization (non-English requests) | No | Yes — normalize to English, reply in the user's language |
| Output integrity | No | Yes — "every pixel from PixelLab"; local processing labeled, not passed off as generated |
| Token footprint | ~31k chars (~7.8k est tokens), one flat all-or-nothing document | `SKILL.md` ~28.9k chars (~7.2k est tokens) always, + `references/` ~158k chars (~39.6k est tokens) loaded on demand |

Token counts are estimated as chars/4. The footprints are not directly comparable: mcp/docs loads in full whenever the link is fetched, while Pip loads `SKILL.md` every time and pulls only the references a task needs. Pip's always-on floor (~7.2k) is comparable to mcp/docs (~7.8k); a task that opens a reference can exceed the flat mcp/docs injection — that extra load is the cost of the more specific, correct routing.

## Use the Official MCP Docs When

- You are doing pure MCP work in a client where PixelLab MCP tools are already configured and visible.
- You want no install and the smallest possible setup — one prompt link.
- You prefer first-party, always-current guidance over a maintained skill.
- You need the engine integration guides (Godot / Unity / Python tilemaps).
- You are using platform features the skill does not document — chat, deployed agents, or the sandbox.
- You want an authoritative dump of every MCP tool and its parameters in one place.

## Use the Agent Skill When

- You need REST v2 fallback or exact endpoint control (batch jobs, backends, scripts, edits, resize, background removal, style references).
- Cost matters — cheap-vs-Pro routing and per-attempt approval before paid retries.
- You want icon, tileset, animation, or paperdoll know-how that mcp/docs does not carry.
- You want a fixed reporting and verification contract after each live call.
- You route across multiple surfaces (MCP, REST, website, Aseprite, Pixelorama, v1).
- You want secret-handling guardrails: `PIXELLAB_SECRET`, never pasting tokens into chat, no session-token scraping.

## Use Both When

The skill is installed and the agent refreshes mcp/docs on demand — Pip's own model. Pip routes, prepares parameters, and enforces safety, then fetches `https://api.pixellab.ai/mcp/docs` (or `v2/openapi.json` for REST) only when an exact tool, field, price, or schema is missing or unclear. Installing the skill does not replace the docs link; it decides when to consult it.

## Measuring the Choice

`dev-tools/skill_benchmark.py` can measure both context strategies directly. Alongside the current skill (always benchmarked) and git-ref skill variants, it defines two context-strategy arms: `vanilla` (agent knowledge only) and `mcp-docs` (the pixellab.ai/mcp pro-tip docs injected, no skill). Running the current skill against `mcp-docs` compares the two context strategies described here on the same tasks.

A recent dry, credit-free 13-scenario snapshot (`claude`) found the skill routed every deterministic check correctly, while the injected docs and no-skill each passed roughly half: the docs alone missed REST-only routes, local post-processing, and the skill's setup and background-removal fallback policies. Numbers vary per run; see [PixelLab Pip Skill Benchmark](../pixellab-pip-benchmark.md) for the current tables and [`dev-tools/skill_benchmark.py`](../../dev-tools/skill_benchmark.py) to reproduce.
