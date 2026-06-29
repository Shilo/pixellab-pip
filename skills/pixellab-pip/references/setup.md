# Setup

Use this reference when the user asks natural-language setup questions such as installing PixelLab Pip, connecting PixelLab to an assistant/editor/app, enabling MCP tools, using documented REST v2 fallback, fixing authentication, checking readiness, or deciding between MCP and API. In this setup guide, "API" means documented REST v2 fallback, not legacy v1, root website routes, or editor/internal operations. This is a reference for the existing PixelLab Pip skill, not a separate skill.

The intended first-run command is one short word after the skill trigger:

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
```

Some apps expose text after a slash command as arguments, while others treat it as normal prompt text. Treat `setup` the same either way. Do not require flags, positional syntax, or app-specific argument features.

For a standalone `setup` after skill invocation, treat the setup mode as `unknown` unless the user explicitly names an assistant/editor/app target or the prior conversation clearly established one. The current runtime app can be mentioned as the likely MCP target after the user chooses an MCP-bearing mode, but it must not by itself skip the MCP + API/MCP only/API only/Manual choice.

## Setup Wizard Contract

`/pixellab-pip setup` behaves like a beginner-friendly wizard, not a static help page. Start from the next safest action, recommend MCP + API first, and ask only the shortest question needed to continue.

When the assistant app exposes an interactive choice prompt, use it for setup selection instead of a prose-only question. Claude Code may show its `AskUserQuestion` UI. In Codex app, use `request_user_input` only when that tool is actually available, typically in Plan mode. Codex full-access/sandbox settings do not imply `request_user_input` availability. If Codex is in normal chat/default mode or the tool is not exposed, ask in normal chat. Keep this optional so CLI/noninteractive agents still work.

For a bare setup command, mode selection is mandatory before any MCP/API-specific setup. Do not ask yes/no questions such as "Should I prepare a Codex MCP config preview?" before the user chooses MCP + API, MCP only, API only, or Manual. Do not inspect config, prepare write previews, or request write approval until the mode is chosen. A brief readiness note is allowed, but the next user-facing question must be the setup choice.

For setup selection, prefer these choices:

- MCP + API (recommended): Connect PixelLab tools directly to the assistant/editor and configure `PIXELLAB_SECRET` so Pip can use documented REST v2 fallback.
- MCP only: Connect PixelLab tools directly to the assistant/editor. Prefer app secret settings or an env/secret reference; use a literal-token MCP config only as an explicit user-chosen fallback when the app has no token-free option, and warn that REST-only features will not be available through Pip fallback.
- API only: Configure `PIXELLAB_SECRET` for Pip's documented REST v2 fallback without adding MCP.
- Manual: Open or link PixelLab's MCP setup page and stop; include the account/Secret step only when auth/token setup is part of the request.

Use the same four initial choices in Claude Code, Codex app, and prose fallback. Treat user wording such as "both", "everything", or "recommended" as `both` mode. Do not hide API fallback behind a later follow-up when the user chose the recommended path.

If no interactive choice tool is available, ask this exact chat question: "Which setup do you want: MCP + API (recommended), MCP only, API only, or Manual?"

Supported wizard modes:

- `both`: recommended default for AI assistants, editors, and MCP-compatible apps. Configure MCP first, then confirm the same `PIXELLAB_SECRET` source is available for Pip's documented REST v2 fallback.
- `mcp`: MCP-only setup for AI assistants, editors, and MCP-compatible apps.
- `api`: configure `PIXELLAB_SECRET` so PixelLab Pip can use documented REST v2 fallback when MCP tools are unavailable, incomplete, or insufficient for the request.
- `manual`: open or link to `https://www.pixellab.ai/mcp`, tell the user to pick their app there, and stop. If auth/token setup is part of the user's request, also link `https://www.pixellab.ai/account` and tell them to copy the value labeled `Secret` without pasting it into chat. If opening a browser is unavailable, provide the links. Do not inspect, write, verify, or continue setup.
- `unknown`: recommend MCP + API and ask one short choice question: MCP + API, MCP only, API only, or Manual.

Use user wording to infer intent:

- MCP signals: "assistant", "editor", "app", "agent", "Claude", "Claude Code", "Codex", "Gemini CLI", "Cursor", "VS Code", "Copilot", "MCP", "tools", "connect PixelLab to my assistant".
- API signals: "REST", "API", "fallback", "when MCP is unavailable", "when MCP tools are missing", "direct PixelLab API".
- Both signals: "recommended", "set everything up", "MCP plus API", "MCP and REST", "assistant plus fallback", "full setup".
- Manual signals: "manual", "website", "open the PixelLab MCP page", "I'll do it myself".

## Decision Tree

1. Identify the desired mode from the user's words. If unclear, say MCP + API is recommended for normal assistant/editor use because it enables full MCP tools plus Pip's documented REST v2 fallback, then ask which mode they want. A bare `setup` command is unclear even when the current app is detectable. The next question must be MCP + API/MCP only/API only/Manual, not a yes/no MCP preview or config-write question.
   If you include a brief credential readiness note before mode selection, check only whether the live `PIXELLAB_SECRET` environment variable is visible to the current process. Do not inspect project-local secret files, broad config directories, or recursive paths. Project files such as `.env` or `.env.local` do not configure MCP unless an explicit loader or wrapper reads them.
2. If mode is `manual`, link or open `https://www.pixellab.ai/mcp`, tell the user to choose their app there, include the account/Secret step only when auth/token setup is part of the request, and stop.
3. If mode is `mcp` or `both`, detect the current assistant/editor/app when possible. If detection is unclear, ask which app they use or offer the manual website option.
4. For known supported apps, tailor only to the named/detected app: Claude Code, Codex, Gemini CLI, Cursor, VS Code Agent Plugins, GitHub Copilot CLI, or generic MCP-compatible apps.
5. If the user names an unknown app, do not guess config paths or syntax. Link or open `https://www.pixellab.ai/mcp`, tell the user to pick their app there, and stop unless they explicitly provide the exact settings screen, config path, or documented MCP format they want you to use.
6. Explain what exact setting or likely config path would be inspected before inspecting it. Do not scan broad home, auth, shell history, keychain, credential, config, project, or repository directories.
7. Explain the credential model: PixelLab account `Secret` stored locally as `PIXELLAB_SECRET`, preferably in app secret settings, app secret store, or a user-level environment setting. In MCP-only mode, a user-chosen hardcoded MCP config can work for MCP auth, but it does not make `PIXELLAB_SECRET` available for Pip's REST v2 fallback.
8. If a write is needed, show a token-free preview with `PIXELLAB_SECRET` placeholders or secret references only, then get explicit approval before changing anything.
9. Tell the user to restart or reload the assistant/editor/app only when the chosen app requires it or tools do not appear after setup.
10. Verify only after the user approves a no-credit check. For MCP, use exposed PixelLab `get_balance` when available. For API, use REST `GET /balance`.
11. Report outcome briefly: detected mode, readiness, credential location type, write destination if any, reload need, and no-credit verification result.

## Safe Credential Setup

Use `credentials.md` as the credential policy source of truth. In setup mode, apply only this summary:

- PixelLab uses one account-level bearer token for public REST v2 and PixelLab MCP.
- Tell the user to get the value labeled `Secret` from `https://www.pixellab.ai/account` and store it locally as `PIXELLAB_SECRET`; never ask them to paste it into chat.
- Prefer app/editor secret settings, app secret stores, user-scoped OS environment settings, or hidden prompts over literal-token commands.
- Literal-token `setx`, `export`, PowerShell `$env:`, or `ENV=value command` examples are allowed only as user-run external-terminal fallbacks with placeholders and a shell-history/process-history warning.
- Project-local `.env*` files work only when a named loader or wrapper reads them; they are not MCP-ready or Pip-ready by themselves.
- Never read broad credential locations or existing `.env*` files unless the user names the exact file and explicitly approves troubleshooting.

## MCP Wizard

Recommend MCP + API first for normal assistant/editor/app use. MCP connects PixelLab tools directly to the app without requiring the user to write API code, and API fallback lets Pip use documented REST v2 endpoints when MCP tools are unavailable, incomplete, or insufficient.

MCP setup must be agent-agnostic and OS-agnostic until the assistant/editor/app is detected or named. Do not assume a specific assistant/editor, operating system, shell, language runtime, package manager, or config path.

For automatic MCP setup:

- Detect the current assistant/editor/app when possible. Otherwise ask one short question or offer Manual.
- Detect OS/shell only when needed to choose a local write method.
- Locate likely config paths only for known supported apps and only after explaining what will be inspected.
- Use PixelLab MCP URL `https://api.pixellab.ai/mcp`.
- Use `Authorization: Bearer <PIXELLAB_SECRET>` or the app's documented env/secret syntax. Never use or preview a real literal token.
- Prefer app secret settings or a secret store named `PIXELLAB_SECRET`.
- Patch or create MCP config only after confirmation.
- In MCP-only mode, a literal bearer token in MCP config is allowed only when the app has no token-free secret reference and the user explicitly chooses that tradeoff. Show placeholders only, warn that the raw Secret may be stored in local MCP config or shell history, and never run literal-token commands for the user.
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

Use API setup only when the user chooses API only, MCP + API, or clearly asks to enable PixelLab Pip's REST v2 fallback. Say this configures the same PixelLab Secret so Pip can call documented REST v2 endpoints when MCP tools are unavailable, incomplete, or insufficient. It is not a setup path for the user's frameworks, scripts, backends, SDK projects, deployment platforms, or app code.

If MCP is unavailable for the user's assistant/editor/app and they did not ask for API fallback, offer Manual, a user-run hardcoded-token command when the app supports it, or ask for a different MCP-compatible app/config path.

For automatic API setup:

- Configure or recommend a `PIXELLAB_SECRET` source visible to the assistant/editor/app session where Pip runs.
- Do not provide language, framework, SDK, backend, deployment, package-manager, or app-code examples in setup mode.
- Do not assume shell, OS, package manager, SDK, framework, backend, deployment platform, or user runtime availability.
- Do not hard-code token literals or generate commands that echo the secret.
- Do not say `setx`, `export`, PowerShell `$env:`, or `ENV=value command` are forbidden; explain they are acceptable only in a normal external terminal when the user accepts shell-history/process-history tradeoffs.
- Avoid literal-token command examples. Use placeholders and safer hidden-prompt or UI options first.
- Do not prefix secret-setting commands with assistant shell escapes; the command text can become part of the assistant session.
- Reuse the same `PIXELLAB_SECRET` source as MCP when mode is `both`. If MCP-only used a hardcoded token in MCP config, do not read or copy it; tell the user API fallback still needs `PIXELLAB_SECRET` configured separately.
- Verify with REST `GET /balance` only after user approval, without printing auth headers or full JSON.

Before writing API-related files or settings, report:

- Target surface: API only or MCP + API.
- Exact destination: assistant/editor/app secret setting, user-level environment setting, hidden prompt, or a specific loader-backed project file only if the user explicitly chose that route.
- Secret handling: `PIXELLAB_SECRET` only.
- Token-free preview: configuration references `PIXELLAB_SECRET`, not a literal value.
- Reload step: whether the assistant/editor/app or terminal must restart.

## Readiness Diagnosis

Diagnose before changing anything. Keep checks narrow and relevant to the user's stated environment.

For MCP readiness, check:

- Whether PixelLab MCP tools are currently available in the agent. Match tool names by suffix if they are prefixed.
- Whether the user's assistant/editor/app is known and what settings screen or config file they want to use.
- Whether an MCP config was explicitly provided or the user approved inspection of a specific likely path.
- Whether the assistant/editor/app can pass `PIXELLAB_SECRET` from an environment variable or secret setting.

For API readiness, check:

- Whether `PIXELLAB_SECRET` is present and non-empty without outputting, logging, measuring, or inspecting the value; only pass it directly to an approved no-credit auth check.
- Whether network access to `https://api.pixellab.ai/v2` is available when a live check is requested.
- Whether the assistant/editor/app session where Pip runs can see the same `PIXELLAB_SECRET` source.

Do not scan broad home, auth, shell history, keychain, credential, config, project, or repository directories. For credential-bearing config, inspect only exact paths the user named or explicitly approved after you explain why. Do not recursively search for token, secret, auth, or env var names. Non-secret readiness checks may inspect only the active workspace files needed for the stated setup task.

## User-Facing Setup Output

Keep setup wording friendly, action-oriented, agent-agnostic, and OS-agnostic by default. Prefer "Next step" language over long diagnostic inventories. Avoid jargon such as "host"; say "assistant", "editor", "app", or the named product.

Required setup output:

- If `PIXELLAB_SECRET` is missing, unknown, or mentioned as something the user must configure, always include the PixelLab account link: `https://www.pixellab.ai/account`.
- In the same sentence or bullet as that link, tell the user to sign in and copy the value labeled `Secret`.
- Tell the user to store that Secret locally as `PIXELLAB_SECRET`, without pasting it into chat.
- If a Secret was pasted into chat/tool output, or the response says to replace/rotate/treat a Secret as exposed, include the same account link and tell the user to copy a new value labeled `Secret`.
- If the response proposes or reports MCP config while `PIXELLAB_SECRET` is still missing, include both next steps: configure/register MCP and separately set `PIXELLAB_SECRET` from the account page. Exception: if the user explicitly chose MCP-only with a literal-token MCP config, say that MCP can work but Pip REST v2 fallback remains unavailable until `PIXELLAB_SECRET` is configured.
- If setup writes or registers MCP successfully but the Secret is still missing from the current session, say PixelLab is registered but not ready for live use until `PIXELLAB_SECRET` is set and the app is reloaded.
- If refusing an unsafe secret-discovery path such as scanning home directories, scanning `.env*`, using browser/session tokens, or entering secrets in an assistant-visible command, include the account link as the safe alternative for getting the value labeled `Secret`.
- If the user asks for no writes and setup/auth is still incomplete, keep the response instruction-only but still include the account link and `PIXELLAB_SECRET` storage step.

Good user-facing setup output:

- "I recommend MCP + API because it lets your assistant/editor use PixelLab tools directly and gives Pip a documented REST v2 fallback."
- "Which setup do you want: MCP + API (recommended), MCP only, API only, or Manual?"
- "Manual means I will open PixelLab's MCP setup page, you pick your app there, and I stop."
- "Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`. Do not paste it here."
- "Token setup options are app secret settings, OS environment-variable UI, a hidden prompt, or a normal external terminal command if you accept shell-history tradeoffs. Project-local files only work when a helper, dotenv loader, or wrapper explicitly loads them."
- "Before I write anything, I will show a preview that uses `PIXELLAB_SECRET` instead of your token."
- "I can verify with a no-credit balance check if you approve."

Client-specific output notes:

- Codex MCP preview: include the token-free `codex mcp add ... --bearer-token-env-var PIXELLAB_SECRET` command, then immediately include the account page step for getting the `Secret` if `PIXELLAB_SECRET` is missing or unknown.
- Codex MCP registered: report the registered MCP endpoint, then say whether `PIXELLAB_SECRET` is visible in this session. If it is missing, link `https://www.pixellab.ai/account` and tell the user to copy `Secret`, store it as `PIXELLAB_SECRET`, and restart/reload Codex before live use.
- Claude Code MCP blocked fallback: include the account page step before any user-run hardcoded-token command option, because the user must copy `Secret` from the account page to use that option.
- API-only and MCP + API setup: include the account page step unless `PIXELLAB_SECRET` is already present.
- MCP-only setup: if a token-free env/secret reference is available, prefer it. If the user chooses a literal-token MCP config, warn that it only configures MCP and does not make `PIXELLAB_SECRET` available for Pip REST v2 fallback.
- Manual setup: link `https://www.pixellab.ai/mcp` for app instructions and also link `https://www.pixellab.ai/account` for the `Secret` if auth/token setup is part of the user's request.

Compact output templates:

- Codex MCP preview with missing Secret: "Codex can register PixelLab MCP with a token-free config that references `PIXELLAB_SECRET`: [command]. Before live use, open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`. Do not paste it here. Should I run the MCP registration command?"
- Codex MCP registered but missing Secret: "PixelLab MCP is registered in Codex, but it is not ready for live use because `PIXELLAB_SECRET` is not visible in this session. Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, store it locally as `PIXELLAB_SECRET`, then restart/reload Codex."
- Claude Code token-free MCP blocked: "I cannot safely auto-write Claude Code HTTP MCP auth without a verified token-free header path. Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET` if you want token-free options later. Your choices are: open `https://www.pixellab.ai/mcp`, run the placeholder command yourself in an external terminal, or discuss a wrapper workaround."
- API-only or MCP + API setup with missing Secret: "Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`. Then Pip can use the same Secret for documented REST v2 fallback when MCP tools are unavailable or insufficient."
- MCP-only with user-chosen hardcoded token: "This can make MCP work, but it stores the raw Secret in local MCP config or shell history and does not configure `PIXELLAB_SECRET` for Pip REST v2 fallback. Replace `<paste-your-Secret-here>` yourself in an external terminal; do not paste it here."
- Pasted Secret: "I cannot use a Secret pasted here. Treat it as exposed and replace it. Open `https://www.pixellab.ai/account`, sign in, copy a new value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`; do not paste it into chat."
- Unsafe secret scan or session token: "I will not scan broad secret locations or use browser/session tokens. Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`; do not paste it here."
- No writes while auth is incomplete: "I will not write anything. Open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET`; I can show token-free setup previews only."
- Manual setup: "Open `https://www.pixellab.ai/mcp`, pick your app there, and follow PixelLab's instructions. I will stop here."
- Manual setup when the user explicitly asks about auth: "Open `https://www.pixellab.ai/mcp`, pick your app there, and follow PixelLab's instructions. If it asks for auth, get the value labeled `Secret` from `https://www.pixellab.ai/account`; do not paste it here. I will stop here."

Avoid config-first output for beginners. Do not show OS-specific, shell-specific, package-manager, SDK, framework, backend, deployment, or programming-language setup commands in setup mode unless the user asks for a specific manual secret-storage path.

## Prompt Before Writes

Any setup action that writes files, environment settings, MCP app config, shell profiles, or loader-backed project-local secret files needs explicit confirmation first. In setup mode, avoid user project files unless the user explicitly chooses a loader-backed secret-storage path.

Before asking, report:

- Target surface: MCP + API, MCP only, API only, or Manual. Recommend MCP + API unless the user explicitly chooses a narrower path.
- Exact destination: config file, app setting, env var, app secret store, app file, or loader-backed project-local secret file.
- Secret handling: token-free placeholder, `PIXELLAB_SECRET` env var, or app secret setting named `PIXELLAB_SECRET`.
- Preview: token-free and using placeholders or secret references only.
- Reload step: whether a terminal, app, or assistant/editor must restart.

If the user only wants instructions, do not write anything.

## No-Credit Live Auth Check

Use live checks only when the user asks to verify readiness or when a setup flow would benefit from confirmation. Never spend credits during setup verification.

Preferred checks:

- MCP: use `get_balance` if available, because it verifies MCP auth without generating assets.
- REST v2: call `GET /balance` with `Authorization: Bearer <env value>` if the user approves a live API check.
- Tool availability: list or identify PixelLab MCP tools without making generation calls.

Before a live check:

- Confirm it should use the locally configured credential.
- State that the token value will not be printed.
- State that no generation or edit will be run.

After a live check:

- Report success/failure, surface checked, and whether credentials were found.
- If balance/usage is returned, summarize it without exposing raw auth headers or full response JSON.
- If failed, report the likely layer: missing env var, assistant/editor/app not reloaded, auth rejected, network failure, endpoint unavailable, or tool mismatch.

## What To Report

For setup help, report only what helps the user proceed:

- Detected intent: MCP + API, MCP only, API only, manual, or unknown.
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
- Do not call undocumented internal endpoints used by first-party surfaces such as the website or Aseprite extension as setup verification.
- Do not run credit-spending generation/edit endpoints during setup checks.
- Do not write MCP config, env files, shell profiles, package files, project code, or deployment settings without explicit confirmation. In setup mode, avoid user project files unless a named loader or wrapper will read them.
- Do not scan broad credential/config directories.
- Do not claim SDK support, MCP tool availability, pricing, limits, or current endpoint behavior without checking when those facts matter.
- Do not require PixelLab Pip-specific assistant behavior from apps that only support generic MCP or REST.
