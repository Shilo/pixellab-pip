# Credentials

Read this for PixelLab bearer-token setup, PixelLab UI naming, or reusing MCP auth for PixelLab Pip REST/API fallback.

PixelLab uses one account-level bearer token for public REST v2 and PixelLab MCP. End-user setup should store that token in `PIXELLAB_SECRET`. PixelLab UI and examples may call the same value an API key, API token, or secret; when discussing REST/MCP authentication, use the technical term `bearer token`.

User-facing setup wording:

- Open `https://www.pixellab.ai/account` after signing in and copy the value labeled `Secret`.
- Store that Secret value locally as `PIXELLAB_SECRET`, preferably in the assistant/editor/app secret settings, an app secret store, or a user-level environment setting.
- If the user chooses Manual setup, open or link to `https://www.pixellab.ai/mcp`, tell them to pick their app there, and stop.
- The PixelLab API/account UI may label this value as an API key, API token, or secret.
- Do not paste the value into chat.
- Do not put the value in an assistant shell escape, including Claude Code or Codex CLI shell commands, or in a Codex app integrated terminal command that Codex can read.
- Prefer app/OS secret settings, environment-variable UI, secret stores, or hidden prompts over literal-token shell commands that can be saved in shell history.
- If the user wants a CLI option such as `setx`, `export`, PowerShell `$env:`, or `ENV=value command`, explain that the command itself is allowed in a normal external terminal, but the literal Secret in command text may be saved or exposed. Use placeholders in examples.

Use the bearer token as:

```text
Authorization: Bearer <PIXELLAB_SECRET>
```

Use one canonical local env var for new agent/API setup examples:

```text
PIXELLAB_SECRET
```

Do not create additional env var aliases. Official examples may say `YOUR_API_TOKEN` or `YOUR_SECRET`; put that same bearer token in `PIXELLAB_SECRET`.

In setup previews, `<PIXELLAB_SECRET>` means a private local secret reference. It does not mean the user should paste the real Secret into chat, a shared config file, or a generated doc.

## MCP Reuse

If PixelLab MCP is already configured, reuse its credential source when safe:

- If the MCP config uses `PIXELLAB_SECRET`, Pip's REST/API fallback can use the same env var.
- If the MCP config uses an app secret setting or secret store named `PIXELLAB_SECRET`, tell the user to make that same `PIXELLAB_SECRET` source visible to the assistant/editor/app session where Pip runs.
- If the MCP config contains a literal `Authorization: Bearer ...` value, do not extract, print, or copy it. It can support MCP-only auth, but it does not configure Pip REST/API fallback. Suggest moving it to env/secret config when the user wants MCP + API or API-only readiness.

Never ask the user to paste the bearer token into chat. Never print, echo, log, summarize, measure, transform, validate, or use token values from chat or config output. If a token appears in chat or tool output, do not repeat it; tell the user to treat it as exposed and replace it before continuing setup. Never use website/Supabase session tokens for REST or MCP.

Never suggest agent-run or assistant-shell commands that include a literal token. This includes Claude Code and Codex CLI shell escapes. Even when a command is executed by the user's local shell from inside an assistant session, the command text may still be visible to the assistant session, saved in transcripts/logs, visible in Codex-readable terminal output, or preserved in command history.

A user-run external-terminal command with a literal token is allowed only as an explicit manual fallback after warning that the token may be stored in local config or shell history. Show placeholders only; never run it, never put the real token in generated text, and never ask the user to paste the real token into chat.

Do not describe `setx`, `export`, PowerShell `$env:`, or `ENV=value command` as inherently forbidden. The risk is the literal Secret appearing in command text. If users ask for CLI setup, show a placeholder-based command for a normal external terminal and explain the shell-history/process-history tradeoff. For the safest default, list secret UIs, secret stores, or hidden prompts first.

Project-local files such as `.env` or `.env.local` do not automatically inject environment variables into Codex, Claude, Pip, MCP clients, terminals, or the OS. They work only when a specific helper, dotenv loader, or wrapper reads them. Do not present project-local files as MCP-ready or Pip-ready by themselves.

When checking MCP config files for credential setup, inspect only the specific config paths referenced by the user or approved after a token-free explanation. Do not scan broad home/auth/config directories, shell history, keychains, project trees, or existing `.env*` files because tool output can leak secrets.

Before writing environment settings, keychain/secret-store entries, MCP app config, shell profiles, or loader-backed project-local secret files, follow `references/setup.md`: explain the destination, show a token-free preview or secret reference, and get explicit approval.

Fallback order:

1. Assistant/editor/app secret settings, app secret store, or user-scoped OS environment variable named `PIXELLAB_SECRET`.
2. Hidden local prompt that writes user-scoped env/keychain config.
3. A project-local file such as `.env` or `.env.local`, only when a specific loader or wrapper explicitly loads it. This is not a default MCP or Pip setup path.
4. Avoid existing `.env*` files, committed MCP config, generated docs, shell history, chat transcript, and copied browser session tokens. Do not read existing `.env*` files unless the user names the exact file, explicitly approves inspection, and confirms the purpose is troubleshooting.

Pip does not use `.env` or `.env.local` for MCP setup or REST/API fallback unless an explicit loader or wrapper is configured. ClawHub `pixellab-ai` uses `.env.local` because its helper auto-loads it; Pip does not currently include that helper loader, so copying the file pattern alone is not enough. If the user asks for `.env` or `.env.local`, explain that it works only when a helper, dotenv loader, or wrapper reads it, and it does not configure MCP or Pip by itself. Before writing `PIXELLAB_SECRET` to any project-local file, explain the loader or wrapper that will read it, show a token-free preview, and get explicit approval. Inspect an existing `.env` or `.env.local` only for troubleshooting when the user names that exact file, explicitly approves inspection, and confirms the purpose is troubleshooting an existing setup. If the purpose is unclear, ask before inspecting. Never print or copy values from it.
