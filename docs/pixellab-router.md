# Minimal PixelLab Router Skill

Last reviewed: 2026-07-12.

This minimal Agent Skill is for agents that need one PixelLab decision: use a matching callable MCP tool, or fall back to the documented REST v2 API. It intentionally omits setup, prompt enhancement, cost controls, asset packaging, and other workflow features.

## Embedded Skill

```markdown
---
name: pixellab-router
description: Route PixelLab tasks to a matching visible PixelLab MCP tool, falling back to the documented PixelLab REST v2 API when no matching MCP tool exists.
---

Route PixelLab requests only through PixelLab MCP or REST v2.

1. Infer the intended operation and inputs. Ask one concise question only when ambiguity changes the route or required fields.
2. If the user explicitly requests REST or API, use REST. Otherwise discover callable PixelLab MCP tools from the host, matching prefixed names by suffix; documentation does not expose tools. If an exposed tool's behavior is unclear, consult `https://api.pixellab.ai/mcp/docs`, then call it using its host-visible schema. For asynchronous work, use the corresponding exposed status tool until completion, failure, or an actionable state such as `review`. If that status tool is unavailable, report that completion cannot be checked; do not resubmit through REST.
3. If no MCP tool fits and the user did not require MCP, inspect `https://api.pixellab.ai/v2/openapi.json`. Select the matching operation and resolve its exact method, path, parameters, request content type and body schema. Send only documented fields.
4. For REST, require `PIXELLAB_SECRET` in the process environment and use it only as `Authorization: Bearer <token>`. Never print the value. If it is absent, stop; do not perform authentication setup.
5. Execute the resolved REST request against `https://api.pixellab.ai/v2`, then handle the response according to its documented schema and content type.
6. If the REST response contains one or more background job IDs, poll each through authenticated `GET https://api.pixellab.ai/v2/background-jobs/{job_id}` every 5–10 seconds until `completed` or `failed`; use each `last_response` when completed.
7. If neither surface documents the operation, say it is unsupported. Do not invent a tool, path, field, or response.

MCP tool names are not REST paths. If the user explicitly requires MCP and no matching MCP tool is exposed, report that instead of falling back.
```

The embedded skill is a compact example, not the repository's canonical agent contract. PixelLab Pip's maintained routing instructions remain in [`../skills/pixellab-pip/SKILL.md`](../skills/pixellab-pip/SKILL.md).
