# Setup

Reference for natural-language setup: installing Pip, connecting PixelLab to an assistant/editor/app, enabling MCP, configuring documented REST v2 fallback, fixing auth, or checking readiness. Here "API" means documented REST v2 fallback, not legacy v1, root website routes, or editor/internal operations. This extends the existing Pip skill; it is not a separate skill.

The first-run command is one word after the trigger, such as `/pixellab-pip setup`, `@pixellab-pip setup`, or `$pixellab-pip setup`. Some apps pass it as an argument, others as prose; treat it the same either way and require no flags or app-specific syntax.

## 1. Choose a mode first

For a bare `setup`, the mode is `unknown` unless the user gave an explicit mode signal (see the inference list below). Naming or detecting an assistant/editor/app resolves only which app to target, not the mode — a named app with no mode word still needs the mode question. Already-set-up shortcut (ambient signals only, no config inspection): if PixelLab MCP tools are already visible in this session and a live `PIXELLAB_SECRET` is present, the effective state is already `both` — report that PixelLab is ready, offer the section 5 no-credit verify, and ask the mode question only if the user then wants to add, change, or narrow the setup. Otherwise, mode selection is mandatory before any MCP/API-specific work: do not inspect config, prepare write previews, or request write approval until the user picks a mode. A brief credential-readiness note is expected (see section 5 for how narrow it must be) and doubles as the shortcut check above; when the shortcut does not fire, the next user-facing question must be the mode choice — never a yes/no question such as "Should I prepare a Codex MCP config preview?"

When the app exposes an interactive choice prompt, use it (Claude Code `AskUserQuestion`; Codex `request_user_input` only when actually available, typically Plan mode — full-access/sandbox does not imply it), carrying the plain-language gloss below as each option's description so a non-technical user always sees it. Otherwise ask this exact question paired with the gloss: "Which setup do you want: MCP + API (recommended), MCP only, API only, or Manual?" Gloss — MCP = PixelLab's tools built directly into your app; API = a backup connection PixelLab uses when those tools are missing; MCP + API = PixelLab's tools in your app plus that backup connection (recommended); Manual = you set it up on PixelLab's website yourself.

The four modes:

- **MCP + API (recommended)** — `both`. Connect PixelLab MCP tools to the app, then confirm the same `PIXELLAB_SECRET` source is available for Pip's REST v2 fallback. Recommend this for normal assistant/editor use: full MCP tools plus fallback when MCP tools are unavailable, incomplete, or insufficient. Do not hide the API step behind a later follow-up.
- **MCP only** — `mcp`. Connect PixelLab MCP tools only. Prefer app secret settings or an env/secret reference. A literal-token MCP config is an explicit user-chosen fallback only when the app has no token-free option; warn that REST-only features stay unavailable through Pip fallback.
- **API only** — `api`. Configure `PIXELLAB_SECRET` for REST v2 fallback without adding MCP. This is for Pip's fallback, not the user's frameworks, scripts, backends, SDK projects, or deployment platforms.
- **Manual** — `manual`. Open or link `https://www.pixellab.ai/mcp`, tell the user to follow the instructions there, and stop. Add the account/Secret step only when auth/token setup is part of the request. Do not inspect, write, verify, or continue.

Infer intent from wording. A plain "connect PixelLab to my app/assistant/editor" or a bare app target ("set up for Cursor") resolves only the target, not the mode — ask the mode question (MCP + API recommended); do not silently pick MCP only and do not silently default a mode. Reserve `mcp` for an explicit exclusivity signal ("only MCP", "just MCP", "no API/REST"). API signals ("REST", "API", "fallback", "when MCP is unavailable", "direct PixelLab API") → `api`; both signals ("recommended", "everything", "MCP plus API", "MCP and REST", "full setup") → `both`; manual signals ("manual", "website", "I'll do it myself") → `manual`.

## 2. Credential policy

**The account step** (the canonical credential instruction, reused wherever the Secret is needed): open `https://www.pixellab.ai/account`, sign in, copy the value labeled `Secret`, and store it locally as `PIXELLAB_SECRET` — preferably in app secret settings, an app secret store, or a user-level environment setting — without pasting it into chat. PixelLab uses this one account-level bearer token for both public REST v2 and PixelLab MCP. Full credential policy: `credentials.md`.

In setup mode, apply `credentials.md`'s token-safety rules (safest-default ordering of secret UIs/stores over literal-token commands; never a literal Secret in an agent-run command; `setx`/`export`/`$env:` external-terminal caveats; `.env*` only via a named loader) — do not restate a weaker copy here. One setup-specific rule:

- An MCP-only literal token configures MCP auth but does not make `PIXELLAB_SECRET` available for Pip's REST v2 fallback. In `both` mode reuse the same `PIXELLAB_SECRET` source across MCP and API; if MCP-only used a hardcoded token, do not read or copy it — API fallback still needs `PIXELLAB_SECRET` set separately.

## 3. Per-app MCP setup

MCP setup stays agent-agnostic and OS-agnostic until the app is named or detected; do not assume an app, OS, shell, runtime, package manager, or config path. Use PixelLab MCP URL `https://api.pixellab.ai/mcp` and `Authorization: Bearer <PIXELLAB_SECRET>` or the app's documented env/secret syntax. Never preview or run a real literal token. Explain the exact setting or likely config path before inspecting it, and only for a named/detected app. Patch or create config only after confirmation, and tell the user to restart or reload only when the app requires it or tools do not appear.

Scope is agent-specific: default to a global/user install so PixelLab works in every project — the friendly default — and use a project scope only when the user wants one project or a team-committed config, through the app's own mechanism. `.mcp.json` is Claude Code's config format, not a cross-app standard: never write it for another app. Each app differs — Codex uses a TOML config file (global `config.toml`, or a project `.codex/config.toml` in a trusted project), Cursor uses `.cursor/mcp.json`, and others have their own — so use only the named/detected app's documented format.

- **Codex CLI**: `codex mcp add --help` supports HTTP MCP auth via `--bearer-token-env-var`. Token-free preview (ask before running; it stores the URL and env var name, not the Secret):

  ```text
  codex mcp add pixellab --url https://api.pixellab.ai/mcp --bearer-token-env-var PIXELLAB_SECRET
  ```

  Scope: `codex mcp add` writes Codex's global user `config.toml` (all projects). For one repo only, put the same `[mcp_servers.pixellab]` block in a project `.codex/config.toml` instead — Codex reads that only after the project is trusted (it prompts to trust a folder the first time you open it there).

- **Claude Code**: `claude mcp add --help` supports HTTP MCP headers, and Claude Code expands `${VAR}` in `url` and `headers` at load, so the Secret stays referenced by name. Token-free preview (ask before running; `-s user` registers it for all projects, and single quotes keep `${PIXELLAB_SECRET}` literal instead of expanding it):

  ```text
  claude mcp add -s user pixellab -t http https://api.pixellab.ai/mcp -H 'Authorization: Bearer ${PIXELLAB_SECRET}'
  ```

  Scope (Claude Code's own flags): `-s user` = global default; `-s local` = this project only (private); `-s project` = a committed `.mcp.json` shared with the team (Claude Code marks a newly added project config as pending approval — approve it before the tools load).

- **Cursor, VS Code Agent Plugins, Gemini CLI, GitHub Copilot CLI, or any other named MCP-capable app**: do not invent config syntax. Use the app's settings UI/docs, PixelLab's MCP page, or an exact path/format the user provides. Always show a token-free preview and ask before writing. A named app not listed here (e.g. Zed, Windsurf, an in-house agent) still gets this generic handling — do not route it to Manual just because it is unlisted.
- **No app named or identifiable**: route to Manual — open or link `https://www.pixellab.ai/mcp` and stop unless the user returns with a known app name, exact settings screen, config path, or documented MCP format. Do not guess config paths or syntax.

## 4. Before any write

Any write — MCP config, env settings, shell profiles, or a loader-backed project-local secret file — needs explicit confirmation first. Avoid user project files unless the user explicitly chose a loader-backed path. If the user only wants instructions, write nothing. Before asking, report:

- **Mode**: MCP + API, MCP only, API only, or Manual.
- **Exact destination**: config file, app setting, env var, app secret store, or loader-backed project-local secret file.
- **Secret handling**: token-free placeholder or `PIXELLAB_SECRET` reference only — never a literal value.
- **Preview**: endpoint, transport/header shape, and secret reference, with no literal token.
- **Reload**: whether a terminal, app, or assistant/editor must restart.

Then get explicit approval before changing anything.

## 5. Verify without spending credits

Diagnose before changing anything, keeping checks narrow to the user's stated environment. The broad diagnostics in this paragraph apply only after a mode is chosen; before mode selection, limit any readiness note to the ambient signals in this section's last paragraph. For MCP readiness: whether PixelLab MCP tools are already available (match by suffix if prefixed), whether the app and its target settings screen or config file are known, whether a config path was explicitly provided or a specific likely path approved, and whether the app can pass `PIXELLAB_SECRET` from an env var or secret setting. For API readiness: whether `PIXELLAB_SECRET` is present and non-empty (checked as below), whether network access to `https://api.pixellab.ai/v2` is available when a live check is requested, and whether the session where Pip runs can see the same `PIXELLAB_SECRET` source.

Verify only after the user approves a no-credit check; never spend credits during setup. Before it, confirm it uses the locally configured credential, and state that the token value will not be printed and that no generation or edit will run.

- **MCP**: `get_balance` when tools are exposed — verifies MCP auth without generating.
- **REST v2**: `GET /balance` with `Authorization: Bearer <PIXELLAB_SECRET>` — never print auth headers or full JSON.
- **Tool availability**: list or identify PixelLab MCP tools (match by suffix if prefixed) without generation calls.

Check `PIXELLAB_SECRET` presence without outputting, logging, measuring, transforming, or inspecting the value — test only whether it is non-empty and emit a status word such as `set`/`not set`, never the value, and pass the value only to the approved check. For a readiness note before mode selection, check only whether the live `PIXELLAB_SECRET` environment variable is visible to the current process and whether PixelLab MCP tools are already visible in this session (already-loaded tools only — no config inspection); do not inspect project-local secret files, broad config directories, or recursive paths.

After the check, report success/failure, the surface checked, and whether credentials were found; summarize any balance without raw headers or full JSON. On failure, name the likely layer: missing env var, app not reloaded, auth rejected, network failure, endpoint unavailable, or tool mismatch.

**Never scan broad locations.** Do not scan home, auth, shell history, keychain, credential, config, project, or repository directories, and do not recursively search for token/secret/auth/env names. Inspect credential-bearing config only at exact paths the user named or approved after you explain why. Non-secret readiness checks may inspect only active-workspace files needed for the task.

## 6. Output

Keep wording friendly, action-oriented, agent-agnostic, OS-agnostic, and in the user's language (for non-English requests follow `localization.md`); prefer "Next step" over long diagnostics; say "assistant", "editor", "app", or the product name, not "host". Do not show OS/shell/package-manager/SDK/framework/language setup commands unless the user asks for a specific manual secret-storage path. When the app has no secret-settings UI (many CLIs and generic agents), storing `PIXELLAB_SECRET` as a user-level environment variable is itself the manual secret-storage path: offer the user both ways per `credentials.md` — the OS settings dialog where one exists (Windows; friendliest, history-safe) and a placeholder terminal command — never a literal token, and include the new-shell-inheritance caveat so the user does not verify from a stale session.

Include the account step (defined in section 2) whenever `PIXELLAB_SECRET` is missing or unknown, a Secret was pasted or must be rotated, a write or MCP registration is proposed while the Secret is still missing, or an unsafe path is refused (broad scans, `.env*` scans, session tokens, assistant-visible commands). If MCP registers but the Secret is still missing from the session, say PixelLab is registered but not ready for live use until `PIXELLAB_SECRET` is set and the app is reloaded. If the user asks for no writes, stay instruction-only but still include the account step.

Compact templates (`[account step]` = the account-step sentence from section 2; `[command]` = the app's token-free MCP preview from section 3):

- **Already configured**: "PixelLab is ready — MCP tools are connected and `PIXELLAB_SECRET` is available for REST v2 fallback. I can run a no-credit balance check to confirm (no token printed, no credits spent), or leave it as is."
- **Codex preview, Secret missing**: "Codex can register PixelLab MCP with a token-free config that references `PIXELLAB_SECRET`: [command]. Before live use, [account step] Should I run the registration command?"
- **Codex registered, Secret missing**: "PixelLab MCP is registered in Codex but not ready for live use — `PIXELLAB_SECRET` is not visible in this session. [account step] Then restart/reload Codex."
- **API-only / MCP + API, Secret missing**: "[account step] Then Pip can use the same Secret for documented REST v2 fallback when MCP tools are unavailable or insufficient."
- **MCP-only, user-chosen hardcoded token**: "This can make MCP work, but it stores the raw Secret in local MCP config or shell history and does not configure `PIXELLAB_SECRET` for Pip's REST v2 fallback. Replace the placeholder yourself in an external terminal; do not paste it here."
- **Pasted Secret**: "I cannot use a Secret pasted here — treat it as exposed and replace it. Repeat the account step for a fresh Secret; do not paste it here."
- **Unsafe scan or session token**: "I will not scan broad secret locations or use browser/session tokens. If you pasted a session token here, treat it as exposed and sign out or rotate it. [account step]"
- **No writes while auth incomplete**: "I will not write anything. [account step] I can show token-free setup previews only."
- **Manual**: "Open `https://www.pixellab.ai/mcp` and follow PixelLab's instructions. I will stop here."
- **Manual with auth**: "Open `https://www.pixellab.ai/mcp` and follow PixelLab's instructions. If it asks for auth, [account step] I will stop here."

Report outcome briefly: detected mode; readiness (ready, partially ready, not configured, blocked, unknown); credential location type (env var, app secret setting, secret store, literal config value, or not found — never the value); next safe step; any proposed write with destination and token handling; reload need; and what the no-credit check verified.

## Setup guardrails

- Do not scrape browser storage or session cookies, or use website/Supabase/browser session tokens for REST or MCP.
- Do not call undocumented internal endpoints (website or Aseprite extension) as setup verification.
- Do not claim SDK support, MCP tool availability, pricing, limits, or endpoint behavior without checking when those facts matter.
- Do not require Pip-specific behavior from apps that only support generic MCP or REST.
