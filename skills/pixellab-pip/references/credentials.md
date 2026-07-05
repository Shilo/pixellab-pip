# Credentials

Read this for PixelLab bearer-token handling, UI naming, and reusing MCP auth for Pip's REST v2 fallback. For where the Secret comes from and how to store it, follow SKILL.md's Auth And Execution and `setup.md`; this file adds the security rules and lookup order.

PixelLab uses one account-level bearer token for both public REST v2 and PixelLab MCP; store it in `PIXELLAB_SECRET`. Use one canonical env var — do not create aliases. Official examples may say `YOUR_API_TOKEN` or `YOUR_SECRET`; put that same token in `PIXELLAB_SECRET`.

Use it as:

```text
Authorization: Bearer <PIXELLAB_SECRET>
```

In previews, `<PIXELLAB_SECRET>` is a private local secret reference — never a cue to paste the real Secret into chat, a shared config file, or a generated doc.

## Token handling

- Never print, echo, log, summarize, measure, transform, validate, or reuse a token value from chat or config output. Never ask the user to paste it into chat. If a token appears in chat or tool output, do not repeat it; tell the user to treat it as exposed and replace it before continuing.
- Never put the token in an agent-run or assistant-shell command, including Claude Code or Codex CLI shell escapes and Codex-readable integrated-terminal commands. Even when the user's local shell runs the command from inside an assistant session, the command text may be visible to the session, saved in transcripts/logs, or kept in command history.
- A user-run command with a literal token is allowed only as an explicit manual fallback in a normal external terminal, after warning that the token may be stored in local config or shell history. Show placeholders only; never run it, never put the real token in generated text, and never ask the user to paste it into chat.
- `setx`, `export`, PowerShell `$env:`, and `ENV=value command` are not inherently forbidden — the risk is the literal Secret appearing in command text. Show placeholder-based commands for a normal external terminal, explain the shell-history/process-history tradeoff, and list secret UIs, secret stores, or hidden prompts first as the safest default.
- Never use website/Supabase/browser session tokens for REST or MCP; they are never the bearer token.

## MCP reuse

If PixelLab MCP is already configured, reuse its credential source when safe:

- MCP config using `PIXELLAB_SECRET`: Pip's REST v2 fallback can use the same env var.
- MCP config using an app secret setting or store named `PIXELLAB_SECRET`: tell the user to make that same source visible to the assistant/editor/app session where Pip runs.
- MCP config with a literal `Authorization: Bearer ...` value: do not extract, print, or copy it. It supports MCP-only auth but does not make the token available to Pip's REST v2 fallback; suggest moving it to env/secret config for MCP + API or API-only readiness.

## Where to look, and where not to

Inspect only the specific config paths the user names or approves after a token-free explanation. Do not scan broad home/auth/config directories, shell history, keychains, project trees, or existing `.env*` files — tool output can leak secrets. Do not recursively search for token/secret/auth/env names.

Before writing environment settings, keychain/secret-store entries, MCP app config, shell profiles, or loader-backed project-local secret files, follow `setup.md`: explain the destination, show a token-free preview or secret reference, and get explicit approval.

`.env`/`.env.local` do not auto-inject variables into Codex, Claude, Pip, MCP clients, terminals, or the OS; they work only when a specific helper, dotenv loader, or wrapper reads them. Do not present them as MCP-ready or Pip-ready by themselves. ClawHub `pixellab-ai` reads such a file only when its helper gets an explicit `--env-file` flag; Pip ships no loader at all, so copying the file pattern alone is not enough. Before writing `PIXELLAB_SECRET` to any project-local file, explain the loader or wrapper that will read it, show a token-free preview, and get approval. Inspect an existing `.env`/`.env.local` only to troubleshoot when the user names that exact file, approves inspection, and confirms the purpose; if unclear, ask first. Never print or copy values from it.

Fallback order:

1. Assistant/editor/app secret settings, app secret store, or user-scoped OS environment variable named `PIXELLAB_SECRET`.
2. Hidden local prompt that writes user-scoped env/keychain config.
3. A project-local `.env`/`.env.local`, only when a specific loader or wrapper explicitly loads it — not a default MCP or Pip path.
4. Avoid existing `.env*` files, committed MCP config, generated docs, shell history, chat transcript, and copied browser session tokens. Do not read existing `.env*` files unless the user names the exact file, approves inspection, and confirms the purpose is troubleshooting.
