# Minimal PixelLab Router Skill

Last reviewed: 2026-07-12.

This minimal Agent Skill is for agents that need one PixelLab decision: use a matching callable MCP tool, or fall back to the documented REST v2 API. It intentionally omits setup, prompt enhancement, cost controls, asset packaging, and other workflow features.

## SKILL.md

```markdown
---
name: pixellab-router
description: Route PixelLab tasks through a matching callable PixelLab MCP tool, falling back to documented PixelLab REST v2 when no matching MCP tool is callable.
---

1. Infer the intended operation and required inputs. Ask only when ambiguity prevents selecting the route or resolving required inputs.
2. If the user requires REST or API, use REST. Otherwise use a matching callable PixelLab MCP tool exposed by the host, matching bare or prefixed names by suffix. Use its host-visible schema; consult `https://api.pixellab.ai/mcp/docs` only when behavior is unclear. If the user requires MCP and no matching tool is callable, report that instead of falling back.
3. For a queued MCP job, poll its matching `get_*` tool until `completed`, `failed`, or an actionable state such as `review`; at `review`, stop for user selection.
4. Otherwise resolve the matching operation from `https://api.pixellab.ai/v2/openapi.json`, including its method, path, parameters, request and response schemas, and content types. If no callable MCP tool or documented REST v2 operation supports the request, report it as unsupported. Call it at `https://api.pixellab.ai/v2` using only documented fields. Require `PIXELLAB_SECRET` in the process environment and use it only as `Authorization: Bearer <token>`; never ask for or expose it in command text, output, logs, or files. If it is absent, stop without performing authentication setup.
5. For every background job ID returned by REST, poll authenticated `GET https://api.pixellab.ai/v2/background-jobs/{job_id}` every 5–10 seconds until `completed` or `failed`. On `completed`, the result is in `last_response`.
```

For full PixelLab functionality—including setup, asset-specific routing, prompt preparation, cost controls, and output handling—use the [PixelLab Pip skill](../skills/pixellab-pip/SKILL.md).

## Setup

### 1. Connect MCP

- Open [PixelLab MCP setup](https://www.pixellab.ai/mcp).
- Follow the instructions for your app.
- Prefer an app secret setting or token-free `PIXELLAB_SECRET` reference; never put the Secret in an assistant-visible command.

### 2. Enable REST fallback

- Sign in to your [PixelLab account](https://www.pixellab.ai/account) and copy the value labeled `Secret`.
- Make it available as `PIXELLAB_SECRET` to the process running the skill, preferably through compatible app secret settings.
- Restart or reload the app only if needed.

### 3. OS fallback

| OS | If the app has no secret settings |
|---|---|
| Windows | Open **Edit environment variables for your account**, add the user variable `PIXELLAB_SECRET`, then fully restart the app. |
| macOS | Follow the app's documented environment-variable method. A shell profile applies only when the app is launched from that shell. |
| Linux | Follow the app's documented environment-variable method. A shell profile applies only when the app is launched from that shell. |

> Never paste the Secret into chat, an assistant-visible command, or the repository.
