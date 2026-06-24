# Setup Mode

Use this reference when the user asks natural-language setup questions such as installing PixelLab Pip, connecting PixelLab to an assistant/editor/app, enabling MCP tools, using REST/API v2, fixing authentication, checking readiness, or deciding between MCP and API. This is a reference for the existing PixelLab Pip skill, not a separate skill.

The intended first-run command is one short word after the skill trigger:

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
```

Some apps expose text after a slash command as arguments, while others treat it as normal prompt text. Treat `setup` the same either way. Do not require flags, positional syntax, or app-specific argument features.

For a standalone `setup` after skill invocation, treat the setup mode as `unknown` unless the user explicitly names an assistant/editor/app target or the prior conversation clearly established one. The current runtime app can be mentioned as the likely MCP target after the user chooses MCP, but it must not by itself skip the MCP/API/Manual choice.

## Setup Wizard Contract

`/pixellab-pip setup` behaves like a beginner-friendly wizard, not a static help page. Start from the next safest action, recommend MCP first, and ask only the shortest question needed to continue.

When the assistant app exposes an interactive choice prompt, use it for setup-mode selection instead of a prose-only question. Claude Code may show its `AskUserQuestion` UI. In Codex app, use `request_user_input` only when that tool is actually available, typically in Plan mode. Codex full-access/sandbox settings do not imply `request_user_input` availability. If Codex is in normal chat/default mode or the tool is not exposed, ask in normal chat. Keep this optional so CLI/noninteractive agents still work.

For a bare setup command, mode selection is mandatory before any MCP/API-specific setup. Do not ask yes/no questions such as "Should I prepare a Codex MCP config preview?" before the user chooses MCP, API, or Manual. Do not inspect config, prepare write previews, or request write approval until the mode is chosen. A brief readiness note is allowed, but the next user-facing question must be the setup-mode choice.

For setup-mode selection, prefer these choices:

- MCP (recommended): Connect PixelLab tools directly to the assistant/editor.
- API: Set up REST v2/API access for scripts, apps, backends, SDKs, or deployments.
- Manual: Open or link PixelLab's MCP setup page and stop.

Use the same three initial choices in Claude Code, Codex app, and prose fallback. Do not show a different fourth "Both" button in agents that support more choices. If the user explicitly types or asks for "both", support `both` mode directly. Otherwise, after MCP or API setup is chosen, mention that the same `PIXELLAB_SECRET` can be reused for the other path if they want it later.

If no interactive choice tool is available, ask this exact chat question: "Which setup do you want: MCP, API, or Manual?"

Supported wizard modes:

- `mcp`: recommended default for AI assistants, editors, and MCP-compatible apps.
- `api`: only for users writing their own scripts, apps, SDK integrations, backends, batch jobs, runtimes, or deployments.
- `both`: MCP first, then API reuse of the same `PIXELLAB_SECRET` source.
- `manual`: open or link to `https://www.pixellab.ai/mcp`, tell the user to pick their app there, and stop. If opening a browser is unavailable, provide the link. Do not inspect, write, verify, or continue setup.
- `unknown`: recommend MCP and ask one short choice question: MCP, API, or manual website setup.

Use user wording to infer intent:

- MCP signals: "assistant", "editor", "app", "agent", "Claude", "Claude Code", "Codex", "Gemini CLI", "Cursor", "VS Code", "Copilot", "MCP", "tools", "connect PixelLab to my assistant".
- API signals: "REST", "API", "curl", "SDK", "Python", "JavaScript", "TypeScript", "backend", "endpoint", "batch", "integration", "web app", "script".
- Both signals: "set everything up", "agent and code", "MCP plus API", "use in my app and assistant".
- Manual signals: "manual", "website", "open the PixelLab MCP page", "I'll do it myself".

## Decision Tree

1. Identify the desired mode from the user's words. If unclear, say MCP is recommended for normal assistant/editor use and ask which mode they want. A bare `setup` command is unclear even when the current app is detectable. The next question must be MCP/API/Manual, not a yes/no MCP preview or config-write question.
2. If mode is `manual`, link or open `https://www.pixellab.ai/mcp`, tell the user to choose their app there, and stop.
3. If mode is `mcp` or `both`, detect the current assistant/editor/app when possible. If detection is unclear, ask which app they use or offer the manual website option.
4. For known supported apps, tailor only to the named/detected app: Claude Code, Codex, Gemini CLI, Cursor, VS Code Agent Plugins, GitHub Copilot CLI, or generic MCP-compatible apps.
5. If the user names an unknown app, do not guess config paths or syntax. Link or open `https://www.pixellab.ai/mcp`, tell the user to pick their app there, and stop unless they explicitly provide the exact settings screen, config path, or documented MCP format they want you to use.
6. Explain what exact setting or likely config path would be inspected before inspecting it. Do not scan broad home, auth, shell history, keychain, credential, config, project, or repository directories.
7. Explain the credential model: PixelLab account `Secret` stored locally as `PIXELLAB_SECRET`, preferably in app secret settings, app secret store, or a user-level environment setting.
8. If a write is needed, show a token-free preview with `PIXELLAB_SECRET` placeholders or secret references only, then get explicit approval before changing anything.
9. Tell the user to restart or reload the assistant/editor/app only when the chosen app requires it or tools do not appear after setup.
10. Verify only after the user approves a no-credit check. For MCP, use exposed PixelLab `get_balance` when available. For API, use REST `GET /balance`.
11. Report outcome briefly: detected mode, readiness, credential location type, write destination if any, reload need, and no-credit verification result.

## Safe Credential Setup

PixelLab uses one account-level bearer token for public REST v2 and PixelLab MCP. The PixelLab UI may call it an API key, API token, secret, or token. For REST/MCP auth, call it a bearer token.

Tell the user to open `https://www.pixellab.ai/account` after signing in and copy the value labeled `Secret`. Never ask the user to paste the bearer token into chat. Never print, echo, log, summarize, transform, validate, measure, use, or copy a token value from chat or config output. If a token appears in chat or tool output, do not repeat it; tell the user to treat it as exposed and replace it before continuing setup.

Do not tell users to run secret-setting commands through an assistant chat, slash-command argument, Claude/Codex shell escape, or a Codex app integrated terminal with the literal Secret value. Commands typed into assistant UIs can appear in chat history, transcripts, debug logs, command history, terminal output, or tool output. Codex app terminal output can be read by Codex, so it is not a secret-entry UI.

`setx`, `export`, PowerShell `$env:`, and `ENV=value command` are not forbidden. They are just lower-safety options when the command contains the literal Secret because shell history or process details may preserve it. When token setup is needed, list the options concisely in this order:

1. App/editor secret settings or app secret store named `PIXELLAB_SECRET`.
2. OS environment-variable UI for a user-scoped `PIXELLAB_SECRET`.
3. Hidden local prompt or secret-store command that does not place the token in command text.
4. Private PixelLab-only `.pixellab` file containing only `PIXELLAB_SECRET`, only if the user explicitly wants a project-local file.
5. Normal external terminal command, only if the user chooses it; show placeholders such as `<PIXELLAB_SECRET>` and warn not to run it inside an assistant prompt, assistant shell escape, or Codex-readable integrated terminal.

Preferred storage order:

1. Assistant/editor/app secret settings, app secret store, or user-scoped OS environment variable named `PIXELLAB_SECRET`.
2. Hidden local prompt or app UI that writes user-scoped env/keychain/secret config.
3. A private `.pixellab` file, gitignored, containing only `PIXELLAB_SECRET`, only if the user explicitly chooses that option.

Avoid existing `.env*` files, committed MCP config, generated docs, shell history, chat transcripts, copied website session tokens, and literal token values in config files unless the user explicitly chooses a manual fallback that requires one. Do not read existing `.env*` files unless the user names the exact file and explicitly approves inspection.

If the user asks for `.env.local`, explain that Pip does not use `.env.local` for PixelLab secret setup because `.env*` files often contain unrelated private secrets. Do not write `PIXELLAB_SECRET` to `.env.local`. If the user wants a project-local file, use a private PixelLab-only `.pixellab` file containing only `PIXELLAB_SECRET` after a token-free preview and explicit approval. Inspect an existing `.env.local` only for troubleshooting when the user names that exact file, explicitly approves inspection, and confirms the purpose is troubleshooting an existing setup. If the purpose is unclear, ask before inspecting. Never print or copy values from it.

Use one canonical env var in new examples:

```text
PIXELLAB_SECRET
```

Use it for REST/MCP auth as:

```text
Authorization: Bearer <PIXELLAB_SECRET>
```

In setup previews, `<PIXELLAB_SECRET>` means a private local secret reference, not a real value to paste into chat. Do not introduce aliases such as `PIXELLAB_API_KEY`, `PIXELLAB_TOKEN`, or `YOUR_API_TOKEN` in new instructions. If official docs use another placeholder, explain that the same bearer token should be stored in `PIXELLAB_SECRET`.

## MCP Wizard

Recommend MCP first for normal assistant/editor/app use. MCP connects PixelLab tools directly to the app without requiring the user to write API code.

MCP setup must be agent-agnostic and OS-agnostic until the assistant/editor/app is detected or named. Do not assume a specific assistant/editor, operating system, shell, language runtime, package manager, or config path.

For automatic MCP setup:

- Detect the current assistant/editor/app when possible. Otherwise ask one short question or offer Manual.
- Detect OS/shell only when needed to choose a local write method.
- Locate likely config paths only for known supported apps and only after explaining what will be inspected.
- Use PixelLab MCP URL `https://api.pixellab.ai/mcp`.
- Use `Authorization: Bearer <PIXELLAB_SECRET>` or the app's documented env/secret syntax. Never use or preview a real literal token.
- Prefer app secret settings or a secret store named `PIXELLAB_SECRET`.
- Patch or create MCP config only after confirmation.
- Tell the user to restart/reload the assistant/editor/app only if needed.
- Verify with no-credit MCP `get_balance` only when MCP tools are exposed and the user approves.

Before writing MCP config, report:

- Target surface: MCP.
- Exact destination: app setting, app secret setting, MCP config path, or user-level environment setting.
- Secret handling: `PIXELLAB_SECRET` secret reference only.
- Token-free preview: endpoint, transport/header shape, and secret reference without a literal token.
- Reload step: whether the assistant/editor/app must restart or reload.

Known app preview rules:

- Codex CLI: current `codex mcp add --help` supports HTTP MCP auth through `--bearer-token-env-var`. A safe token-free preview is:

  ```text
  codex mcp add pixellab --url https://api.pixellab.ai/mcp --bearer-token-env-var PIXELLAB_SECRET
  ```

  Ask before running it. It stores the server URL and env var name, not the Secret value.
- Claude Code: current `claude mcp add --help` supports HTTP MCP headers, but header examples can expand or store literal values if used carelessly. First try to find a verified token-free path. Preview only the token-free destination and shape: Claude Code MCP config, HTTP transport, URL `https://api.pixellab.ai/mcp`, and `Authorization: Bearer <PIXELLAB_SECRET>` as a private env/secret reference. Verify current Claude secret-reference syntax or ask for the exact settings/config path before writing.
  If no token-free secret-reference path is available, do not write the config automatically. Offer the user explicit options:
  1. Open or link PixelLab's MCP setup page and let the user follow it.
  2. Manually run a Claude Code command in their own external terminal that hardcodes the Secret, after warning that Claude Code may store the raw Secret in its MCP config.
  3. Discuss a token-free wrapper workaround if they prefer not to store the raw Secret.
  For the hardcoded-token option, show only a placeholder command and tell the user to replace `<paste-your-Secret-here>` themselves outside chat:

  ```text
  claude mcp add --transport http pixellab https://api.pixellab.ai/mcp --header "Authorization: Bearer <paste-your-Secret-here>"
  ```

  Never run that command for the user, and never ask them to paste the real Secret into chat.
- Cursor, VS Code Agent Plugins, Gemini CLI, GitHub Copilot CLI, and generic MCP-compatible apps: do not invent exact config syntax. Use the app's settings UI/docs, PixelLab's MCP page, or an exact path/format the user provides. Always show a token-free preview and ask before writing.

If the app is unknown, route to Manual: open or link `https://www.pixellab.ai/mcp`, tell the user to pick their app there, and stop unless they come back with a known supported app name, exact settings screen, config path, or documented MCP format.

## API Wizard

Use API setup only when the user chooses API/both or clearly asks for code/backend/script setup. Say this is the backup/advanced path for direct code. If MCP is unavailable for the user's assistant/editor/app and they did not ask to write code, offer Manual, a user-run hardcoded-token command when the app supports it, or ask for a different MCP-compatible app/config path.

For automatic API setup:

- Configure or recommend reading `PIXELLAB_SECRET` from the runtime environment or deployment secret store.
- Provide language/platform examples only after the user names the language, framework, deployment platform, SDK, or runtime.
- Do not assume shell, OS, package manager, or SDK availability.
- Do not hard-code token literals or generate commands that echo the secret.
- Do not say `setx`, `export`, PowerShell `$env:`, or `ENV=value command` are forbidden; explain they are acceptable only in a normal external terminal when the user accepts shell-history/process-history tradeoffs.
- Avoid literal-token command examples. Use placeholders and safer hidden-prompt or UI options first.
- Do not prefix secret-setting commands with assistant shell escapes; the command text can become part of the assistant session.
- Reuse the same `PIXELLAB_SECRET` source as MCP when mode is `both`.
- Verify with REST `GET /balance` only after user approval, without printing auth headers or full JSON.

Before writing API-related files or settings, report:

- Target surface: API or both.
- Exact destination: runtime secret, deployment secret, app setting, user-level environment setting, or project file.
- Secret handling: `PIXELLAB_SECRET` only.
- Token-free preview: code/config uses an environment or secret-store read, not a literal value.
- Reload step: whether a terminal, app, server, or deployment must restart.

## Readiness Diagnosis

Diagnose before changing anything. Keep checks narrow and relevant to the user's stated environment.

For MCP readiness, check:

- Whether PixelLab MCP tools are currently available in the agent. Match tool names by suffix if they are prefixed.
- Whether the user's assistant/editor/app is known and what settings screen or config file they want to use.
- Whether an MCP config was explicitly provided or the user approved inspection of a specific likely path.
- Whether the assistant/editor/app can pass `PIXELLAB_SECRET` from an environment variable or secret setting.

For API readiness, check:

- Whether `PIXELLAB_SECRET` is present and non-empty without outputting, logging, measuring, or inspecting the value; only pass it directly to an approved no-credit auth check.
- Whether the user named a shell, language, SDK, framework, deployment platform, or another runtime.
- Whether network access to `https://api.pixellab.ai/v2` is available when a live check is requested.
- Whether any installed SDK is actually present before recommending SDK-specific methods.

Do not scan broad home, auth, shell history, keychain, credential, config, project, or repository directories. For credential-bearing config, inspect only exact paths the user named or explicitly approved after you explain why. Do not recursively search for token, secret, auth, or env var names. Non-secret readiness checks may inspect only the active workspace files needed for the stated setup task.

## User-Facing Setup Output

Keep setup wording friendly, action-oriented, agent-agnostic, and OS-agnostic by default. Prefer "Next step" language over long diagnostic inventories. Avoid jargon such as "host"; say "assistant", "editor", "app", or the named product.

Required setup output:

- If `PIXELLAB_SECRET` is missing, unknown, or mentioned as something the user must configure, always include the PixelLab account link: `https://www.pixellab.ai/account`.
- In the same sentence or bullet as that link, tell the user to sign in and copy the value labeled `Secret`.
- Tell the user to store that Secret locally as `PIXELLAB_SECRET`, without pasting it into chat.
- If the response proposes or reports MCP config while the Secret is still missing, include both next steps: configure/register MCP and separately set `PIXELLAB_SECRET` from the account page.
- If setup writes or registers MCP successfully but the Secret is still missing from the current session, say PixelLab is registered but not ready for live use until `PIXELLAB_SECRET` is set and the app is reloaded.

Good user-facing setup output:

- "I recommend MCP first because it lets your assistant/editor use PixelLab tools directly."
- "Which setup do you want: MCP, API, or Manual?"
- "Manual means I will open PixelLab's MCP setup page, you pick your app there, and I stop."
- "Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`. Do not paste it here."
- "Token setup options are app secret settings, OS environment-variable UI, a hidden prompt, a private `.pixellab` file, or a normal external terminal command if you accept shell-history tradeoffs."
- "Before I write anything, I will show a preview that uses `PIXELLAB_SECRET` instead of your token."
- "I can verify with a no-credit balance check if you approve."

Client-specific output notes:

- Codex MCP preview: include the token-free `codex mcp add ... --bearer-token-env-var PIXELLAB_SECRET` command, then immediately include the account page step for getting the `Secret` if `PIXELLAB_SECRET` is missing or unknown.
- Codex MCP registered: report the registered MCP endpoint, then say whether `PIXELLAB_SECRET` is visible in this session. If it is missing, link `https://www.pixellab.ai/account` and tell the user to copy `Secret`, store it as `PIXELLAB_SECRET`, and restart/reload Codex before live use.
- Claude Code MCP blocked fallback: include the account page step before any user-run hardcoded-token command option, because the user must copy `Secret` from the account page to use that option.
- API setup: include the account page step before language/runtime examples unless `PIXELLAB_SECRET` is already present.
- Manual setup: link `https://www.pixellab.ai/mcp` for app instructions and also link `https://www.pixellab.ai/account` for the `Secret` if auth/token setup is part of the user's request.

Avoid config-first output for beginners. Do not show OS-specific, shell-specific, package-manager, SDK, or programming-language setup commands unless the user named that platform or asked for that manual path.

## Prompt Before Writes

Any setup action that writes files, environment settings, MCP app config, shell profiles, private PixelLab-only env files, package files, project scripts, or deployment settings needs explicit confirmation first.

Before asking, report:

- Target surface: MCP, API, or both. Recommend MCP first unless the user is writing direct API code.
- Exact destination: config file, app setting, env var, app secret store, deployment secret, app file, or project file.
- Secret handling: token-free placeholder, `PIXELLAB_SECRET` env var, or app secret setting named `PIXELLAB_SECRET`.
- Preview: token-free and using placeholders or secret references only.
- Reload step: whether a terminal, app, server, deployment, or assistant/editor must restart.

If the user only wants instructions, do not write anything.

## No-Credit Live Auth Check

Use live checks only when the user asks to verify readiness or when a setup flow would benefit from confirmation. Never spend credits during setup verification.

Preferred checks:

- MCP: use `get_balance` if available, because it verifies MCP auth without generating assets.
- REST/API: call `GET /balance` with `Authorization: Bearer <env value>` if the user approves a live API check.
- Tool availability: list or identify PixelLab MCP tools without making generation calls.

Before a live check:

- Confirm it should use the locally configured credential.
- State that the token value will not be printed.
- State that no generation or edit will be run.

After a live check:

- Report success/failure, surface checked, and whether credentials were found.
- If balance/usage is returned, summarize it without exposing raw auth headers or full response JSON.
- If failed, report the likely layer: missing env var, assistant/editor/app not reloaded, auth rejected, network failure, endpoint unavailable, or SDK/tool mismatch.

## What To Report

For setup help, report only what helps the user proceed:

- Detected intent: MCP, API, both, manual, or unknown.
- Current readiness: ready, partially ready, not configured, blocked, or unknown.
- Credential location type: env var, app secret setting, secret store, literal config value found, or not found. Never report the credential value.
- Next safest step.
- Any write you propose, with destination and token-handling approach.
- Whether a restart/reload is needed.
- Whether a live auth check was no-credit and what it verified.

## What Not To Do

- Do not ask for, paste, print, echo, log, quote, summarize, measure, or transform the bearer token.
- Do not suggest any agent-run or assistant-shell command that includes the literal Secret value, including Claude Code or Codex CLI shell escapes.
- A user-run external-terminal command with a literal Secret is allowed only as an explicit manual fallback after warning that the token may be stored in local config or shell history. Show placeholders only; never run it or ask the user to paste the real Secret into chat.
- Do not describe `setx` or `export` as inherently unsafe or forbidden; describe the risk as literal-token command text being stored or exposed.
- Do not present literal-token shell commands as the safest default for manual setup; list safer secret UIs, secret stores, or hidden prompts first.
- Do not use website/Supabase/browser session tokens for REST or MCP.
- Do not scrape browser storage or session cookies.
- Do not call undocumented website endpoints as setup verification.
- Do not run credit-spending generation/edit endpoints during setup checks.
- Do not write MCP config, env files, shell profiles, package files, project code, or deployment settings without explicit confirmation.
- Do not scan broad credential/config directories.
- Do not claim SDK support, MCP tool availability, pricing, limits, or current endpoint behavior without checking when those facts matter.
- Do not require PixelLab Pip-specific assistant behavior from apps that only support generic MCP or REST.
