# MCP Platform Tools

Use this reference for PixelLab MCP tools that operate on projects, sandboxes, deployed agents, chat conversations, help, or feedback rather than direct asset generation.

Official MCP docs currently expose platform helpers such as `list_projects`, `chat_*`, `sandbox_*`, `agent_help`, `agent_feedback`, `agent_list`, `agent_inspect`, and `agent_talk`. These are public MCP tools, not REST v2 endpoints.

## Safety Rules

- Use `agent_help` freely for PixelLab MCP usage questions, because it asks PixelLab's knowledge agent for documentation help.
- Use `agent_feedback` only when the user wants to report feedback or after you have a concise, non-secret issue report. Do not include bearer tokens, private prompts, raw files, account data, or unrelated local paths.
- Treat `list_projects`, `chat_list_conversations`, `chat_get_messages`, `agent_list`, and `agent_inspect` as account or project data reads. Ask for approval before reading them unless the user directly asked for that exact information.
- Treat `chat_send_message`, `agent_talk`, `sandbox_bash`, `sandbox_run`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`, and `sandbox_destroy_session` as state-changing or potentially sensitive actions. Get explicit approval for the specific target and action before calling them.
- For `sandbox_destroy_session`, destructive deletes, git syncs, deployments, or any command that may publish, overwrite, delete, or spend credits, clearly name the target and consequence before asking for approval.
- Do not use PixelLab sandbox tools to bypass the user's local repository, approval, or secret-handling rules. If a task is ordinary local coding work, use the local workspace unless the user explicitly requests a PixelLab sandbox.
- Do not paste secrets, raw environment dumps, private traces, full chat transcripts, or full agent traces into reports. Summarize only the minimum needed to answer or debug the user's request.

## Reporting

Report the MCP tool used, the project/session/conversation/agent identifier only when needed for follow-up, whether the action was read-only or state-changing, and any next step that needs user approval.
