# Official PixelLab MCP Service Comparison

Last reviewed: 2026-07-01.

This compares PixelLab Pip with the official [PixelLab MCP service](https://api.pixellab.ai/mcp/docs). The goal is to define the technical boundary between the service that executes PixelLab work and the skill that helps an agent choose, configure, and use the right PixelLab surface.

Sources reviewed:

- [PixelLab MCP tool guide](https://api.pixellab.ai/mcp/docs).
- [PixelLab MCP setup page](https://www.pixellab.ai/mcp).
- PixelLab Pip `README.md`, `SKILL.md`, and runtime references.

## Summary

The official PixelLab MCP service is the execution layer. It exposes MCP tools for creating, polling, listing, downloading, and deleting managed PixelLab assets from MCP-capable assistants and editors.

PixelLab Pip is the agent-side routing and safety layer. It helps an agent decide whether to use MCP, REST v2, website/editor workflows, Aseprite, Pixelorama, SDK/API docs, or legacy v1. Pip does not replace the MCP service; when MCP is configured and fits the request, Pip should use MCP.

Use the official MCP service when the assistant already has PixelLab MCP tools and the user wants managed PixelLab assets. Use Pip when the assistant needs setup guidance, route selection, credential safety, unsupported-flow warnings, prompt preparation, or a fallback decision between MCP and documented REST v2.

## Feature Comparison

| Area | Official PixelLab MCP service | PixelLab Pip skill |
|---|---|---|
| Technical layer | Hosted MCP server at `https://api.pixellab.ai/mcp`. | Agent skill/instruction layer installed in supported assistants. |
| Primary goal | Provide callable PixelLab tools to MCP-capable assistants. | Help agents choose and use the correct PixelLab surface safely. |
| Best default use | Direct asset generation and management inside an MCP-enabled coding assistant. | Setup, routing, explanation, workflow selection, and guardrails before or around live calls. |
| Execution capability | Actually creates, polls, lists, downloads, and deletes PixelLab assets. | Does not provide compute by itself; it routes to MCP, REST v2, website/editor, or another documented surface. |
| Setup model | User configures an MCP client with the PixelLab MCP URL and bearer auth header. | Recommends MCP first, then guides MCP/API/manual setup where API means documented REST v2 fallback, with token-free previews and explicit approval before writes. |
| Supported apps | The setup page lists multiple MCP clients such as Claude Code, VS Code, Cursor, Gemini CLI, Codex CLI, and other MCP clients. | Distributed as a plugin/skill intended to work across agents that support skills, plugin invocation, or explicit prompt instructions. |
| Invocation | User asks their MCP-enabled assistant for PixelLab work; the assistant calls visible MCP tools. | User invokes `/pixellab-pip`, `@pixellab-pip`, `$pixellab-pip`, or asks a PixelLab-specific question/task that triggers the skill. |
| Tool schema | MCP tools expose structured tool parameters when the assistant has the server configured. | Maintains routing tables and warnings; refreshes official docs when exact current schemas matter. |
| Main asset coverage | Characters, portrait-character conversion, fonts, character states, animations, top-down tilesets, sidescroller tilesets, isometric tiles, tile variants, UI assets, objects, map objects, balance, projects, chat, sandbox, and agent helper tools documented by MCP. | Covers MCP assets plus REST v2, website/editor-only flows, Aseprite, Pixelorama, SDK/API questions, and legacy v1 compatibility. |
| Async workflow | Creation tools return IDs immediately; corresponding `get_*` tools poll status and provide result/download data. | Teaches the same non-blocking pattern, reports IDs/status/output details, and routes REST async jobs separately from MCP managed assets. |
| REST v2 fallback | MCP docs point users to REST v2 when writing code or needing API surfaces not exposed through MCP. | Explicitly chooses REST v2 for scripts, batch jobs, exact endpoint control, generic images, UI, edits, resizing, background removal, and other REST-only tasks. |
| Website/editor boundary | Notes that web interfaces, editor plugins, API v1, and API v2 are different PixelLab interfaces. | Adds stricter boundaries for website/editor automation, Aseprite, Pixelorama, copied session tokens, and undocumented endpoints. |
| Credential handling | Requires bearer auth in MCP client configuration. Official examples use generic bearer-token placeholders. | Standardizes user-facing setup on `PIXELLAB_SECRET`, avoids asking for tokens in chat, avoids broad `.env*` inspection, and previews config without literal secrets. |
| Beginner setup experience | Official setup page provides app-specific commands/config snippets and links to external client docs. | Adds a beginner-oriented setup wizard contract: recommend MCP first, ask MCP/API/both/manual, explain the next step, and write only after approval. |
| Prompt preparation | Tool docs include examples and parameter descriptions. | Rewrites vague natural-language parameters into PixelLab-ready English values unless the user opts out. |
| Image input handling | Tool parameters define what each MCP tool can accept. | Classifies supplied images by role before choosing a surface: identity, style, target, mask, palette, source frame, reference, and related endpoint-specific roles. |
| Unsupported requests | If tools are unavailable, MCP docs tell the agent not to pretend MCP is configured. | Adds route warnings for ambiguous terms, missing tools, REST-only features, website-only flows, SDK parity, and unsupported automation. |
| Output policy | MCP returns managed asset IDs, statuses, result URLs, previews, and download links according to the tool. | Requires final reporting of surface, tool/endpoint, prompt prep, final parameters, IDs, paths/URLs, polling/status, usage when exposed, and verification status. |
| Security posture | Uses normal MCP client auth and PixelLab-managed tools. | Adds agent behavior rules: no pasted secrets, no token printing, no session-token scraping, no calls to undocumented internal endpoints used by first-party surfaces, no credit-spending setup checks. |
| Dependency | Requires an MCP-capable client with the PixelLab server configured. | Can still answer route/setup/API questions without MCP tools, but live MCP generation requires the official MCP service to be configured. |

## Pip-Only Capabilities

These are capabilities Pip provides that the official MCP service does not try to provide. They are not replacements for MCP tools; they are decision, setup, and safety behavior around those tools.

| Pip capability | Why MCP does not cover it | Practical effect |
|---|---|---|
| Cross-surface routing | MCP exposes one official tool surface. It does not decide between MCP, REST v2, website/editor workflows, Aseprite, Pixelorama, SDKs, or legacy v1. | The agent can choose MCP for managed assets, REST v2 for code and batch jobs, and website/editor flows for manual-only product surfaces. |
| Beginner setup wizard | MCP setup pages provide client-specific snippets. They do not act as an interactive, agent-agnostic installer. | Pip can recommend MCP first, offer MCP/API/both/manual modes, preview changes, and ask before writing config. |
| `PIXELLAB_SECRET` setup convention | MCP only requires a bearer auth header. It does not define a cross-agent user-facing secret name. | Pip gives users one stable secret name and avoids token values in chat, docs, and committed config. |
| Credential safety policy | MCP clients decide how they store and pass secrets. | Pip instructs agents not to ask for pasted tokens, not to print token values, not to scan `.env*` broadly, and not to scrape website session tokens. |
| Ambiguity handling | MCP tools execute structured calls; they do not resolve broad natural-language collisions by themselves. | Pip asks only for blocking distinctions such as tileset vs tile variant, whole map vs map object, or static effect vs animation. |
| Prompt and parameter preparation | MCP docs describe parameters and examples. They do not standardize how agents rewrite rough user text. | Pip converts vague asset requests into PixelLab-ready English parameter values unless the user opts out. |
| Supplied-image role classification | MCP tools accept tool-specific image inputs. | Pip classifies attachments as identity, style, target, mask, palette, source frame, reference, or other endpoint-specific roles before choosing a route. |
| Unsupported-flow warnings | MCP docs warn not to treat MCP tools as REST endpoints. | Pip also warns against undocumented internal endpoints used by first-party surfaces, copied browser/session tokens, SDK parity assumptions, and website-only/editor-only flows. |
| REST v2 fallback policy | MCP docs mention REST v2 as another interface. | Pip defines when to leave MCP for REST v2: scripts, backends, batch jobs, exact endpoint control, generic image/UI/edit/remove-background tasks, and SDK/API integration. |
| Output reporting contract | MCP returns tool results. | Pip tells the agent what to report after live calls: surface, tool/endpoint, final parameters, IDs, URLs/paths, polling status, usage when exposed, and verification state. |

## Recommended Relationship

PixelLab Pip should treat the official MCP service as the preferred execution path for normal assistant/editor asset work. Pip adds value before and around the service call:

1. Decide whether MCP is the right surface for the user's request.
2. Help the user configure MCP safely if tools are not visible.
3. Convert the user's request into route-appropriate PixelLab parameters.
4. Use MCP tools when they are available and documented for the task.
5. Fall back to REST v2 only when the user needs direct API/code control or the requested capability is not exposed through MCP.
6. Refuse or reroute website/session-token automation and automation of undocumented internal endpoints used by first-party surfaces.

This means "MCP versus Pip" is usually the wrong framing. MCP is the service that performs supported PixelLab work; Pip is the guidance layer that helps an agent use MCP correctly and choose another official surface when MCP is not the right fit.

## Without Pip

An assistant can still use PixelLab MCP without Pip if:

1. The user configures `https://api.pixellab.ai/mcp` in an MCP-capable app.
2. The app sends `Authorization: Bearer <PixelLab bearer token>` from a private local secret or secret setting.
3. PixelLab MCP tools appear to the assistant.
4. The assistant reads the exposed tool schemas or the [MCP tool guide](https://api.pixellab.ai/mcp/docs).
5. The assistant calls the appropriate MCP tool and polls with the matching `get_*` tool.

The MCP docs' prompt tip, `@https://api.pixellab.ai/mcp/docs`, is helpful for assistants that can fetch URL context. It is not a substitute for MCP configuration. If MCP tools are not visible, an agent should say MCP is not configured instead of inventing tool calls.

## When To Prefer Each

Prefer official MCP directly when:

- PixelLab MCP tools are already visible in the assistant.
- The request maps cleanly to an MCP tool such as character, object, tileset, tile variant, project, sandbox, chat, or balance.
- The user wants assets inside a coding-agent workflow, not a custom API integration.

Prefer Pip-assisted routing when:

- The user is setting up PixelLab for the first time.
- The assistant needs to decide between MCP, REST v2, website/editor, Aseprite, Pixelorama, SDKs, or legacy v1.
- The request is ambiguous, such as "tiles", "map", "object", "effect", "paperdoll", or supplied images with unclear roles.
- The user asks about tokens, API setup, command prefixes, unsupported endpoints, or how to verify readiness.
- The task may spend credits and needs parameter confirmation, route explanation, or output reporting.

Prefer REST v2 guidance instead of MCP when:

- The user is writing a backend, script, batch job, SDK integration, or deployment.
- The task needs exact endpoint control or a REST-only capability.
- The user needs code that runs outside an MCP-enabled assistant.

## Ideas Not Adopted

- Do not present Pip as an alternative execution service to official MCP.
- Do not duplicate the full MCP tool schema into Pip docs; refresh the official MCP docs when exact tool parameters matter.
- Do not teach users to curl MCP tool names as REST endpoints.
- Do not require Pip for users who only need official MCP and already have MCP tools configured.
- Do not claim MCP covers every PixelLab product surface; route REST v2 and website/editor-only requests separately.
