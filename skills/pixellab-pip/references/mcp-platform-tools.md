# MCP Platform Tools

Use this reference for PixelLab MCP tools that operate on projects, sandboxes, deployed agents, chat conversations, help, or feedback rather than direct asset generation.

Official MCP docs currently expose platform helpers such as `list_projects`, `add_to_project`, `chat_*`, `sandbox_*`, `agent_help`, `agent_feedback`, `agent_list`, `agent_inspect`, `agent_talk`, `search_knowledge`, `list_jobs`, and `cancel_job`. These are public MCP tools, not REST v2 endpoints. Version 0.4.123 makes Game Builder available to Tier 1+ subscribers; use the visible Game Builder product for that workflow and only use the public project/chat/sandbox helpers when the user requests an approved project-scoped action. Generation tools that accept `project_id` can link results to that Game Builder context, but there is no documented dedicated REST v2 Game Builder endpoint.

## Safety Rules

- Use `agent_help` freely for PixelLab MCP usage questions, because it asks PixelLab's knowledge agent for documentation help. `search_knowledge` is the same kind of free read against a Phaser/game-dev knowledge base — use it only for that subject, not as a general search.
- `list_jobs` is a free read of your active background jobs; use it when a job ID was lost or the user asks what is still running.
- `cancel_job` is destructive: the result is lost and refund behavior is undocumented, so assume the spend is not recovered. Ask before cancelling, naming the job and what it was producing.
- Use `agent_feedback` only when the user wants to report feedback or after you have a concise, non-secret issue report. Do not include bearer tokens, private prompts, raw files, account data, or unrelated local paths.
- Treat `list_projects`, `chat_list_conversations`, `chat_get_messages`, `agent_list`, and `agent_inspect` as account or project data reads. Ask for approval before reading them unless the user directly asked for that exact information.
- Treat `chat_send_message`, `agent_talk`, `add_to_project`, `sandbox_create_session`, `sandbox_bash`, `sandbox_run`, `sandbox_write`, `sandbox_edit`, `sandbox_sync`, `sandbox_read_image`, and `sandbox_destroy_session` as state-changing or potentially sensitive actions. Get explicit approval for the specific target and action before calling them. `sandbox_write` defaults to `force: true` and overwrites silently — read the path first when the file may already exist.
- For `sandbox_destroy_session`, `sandbox_deploy_worker`, `sandbox_undeploy`, `sandbox_playtest`, destructive deletes, git syncs, or any command that may publish, overwrite, delete, or spend credits, clearly name the target and consequence before asking for approval. `sandbox_deploy_worker` and `sandbox_undeploy` are outward-facing publish/delete actions — name the project and branch when asking.
- Do not use PixelLab sandbox tools to bypass the user's local repository, approval, or secret-handling rules. If a task is ordinary local coding work, use the local workspace unless the user explicitly requests a PixelLab sandbox.
- Do not paste secrets, raw environment dumps, private traces, full chat transcripts, or full agent traces into reports. Summarize only the minimum needed to answer or debug the user's request.

## Reporting

Report the MCP tool used, the project/session/conversation/agent identifier only when needed for follow-up, whether the action was read-only or state-changing, and any next step that needs user approval.
