# Setup Mode

Use this reference when the user asks natural-language setup questions such as installing PixelLab Pip, connecting PixelLab to an agent, enabling MCP tools, using REST/API v2, fixing authentication, checking readiness, or deciding between MCP and API. This is a reference for the existing PixelLab Pip skill, not a separate skill.

The intended first-run command is one short word after the skill trigger:

```text
/pixellab-pip setup
@pixellab-pip setup
```

Some hosts expose text after a slash command as arguments, while others treat it as normal prompt text. Treat the English word `setup` the same either way. Do not require flags, positional syntax, host-specific argument features, or translated one-word triggers.

## Setup Intent

First classify what the user wants to set up:

- `mcp`: hosted PixelLab MCP tools inside an agent, IDE, desktop app, or MCP host.
- `api`: direct REST v2 usage from scripts, apps, SDKs, curl, or backend code.
- `both`: MCP for agent workflows plus REST/API for code or automation.
- `unknown`: ask one short question, or explain the difference and recommend `both` for users who want agent-generated assets and code integration.

Use user wording to infer intent:

- MCP signals: "agent", "Claude", "Codex", "Cursor", "MCP", "tools", "server", "host config", "desktop app", "connect PixelLab to my assistant".
- API signals: "REST", "API", "curl", "SDK", "Python", "JavaScript", "backend", "endpoint", "batch", "integration", "web app".
- Both signals: "set everything up", "agent and code", "MCP plus API", "use in my app and assistant".

## Readiness Diagnosis

Diagnose before changing anything. Keep checks narrow and relevant to the user's stated environment.

For MCP readiness, check:

- Whether PixelLab MCP tools are currently available in the agent. Match tool names by suffix if they are prefixed.
- Whether the user's MCP host is known and what config path or UI they want to use.
- Whether an MCP config was explicitly provided or the user asked you to inspect a specific file.
- Whether the host can pass `PIXELLAB_SECRET` from an environment variable or secret store.

For API readiness, check:

- Whether the runtime can read `PIXELLAB_SECRET` without printing the value.
- Whether the user wants shell, Python, JavaScript/TypeScript, or another platform example.
- Whether network access to `https://api.pixellab.ai/v2` is available when a live check is requested.
- Whether any installed SDK is actually present before recommending SDK-specific methods.

Do not scan broad home, auth, shell history, keychain, credential, config, project, or repository directories. For credential-bearing config, inspect only exact paths the user named or explicitly approved after you explain why. Do not recursively search for token, secret, auth, or env var names. Non-secret readiness checks may inspect only the active workspace files needed for the stated setup task.

## Safe Credential Setup

PixelLab uses one account-level bearer token for public REST v2 and hosted MCP. The PixelLab UI may call it an API key, API token, secret, or token. For REST/MCP auth, call it a bearer token.

Tell the user to get the token from `https://www.pixellab.ai/account` after signing in, or follow PixelLab's MCP setup page at `https://www.pixellab.ai/mcp`.

Never ask the user to paste the bearer token into chat. Never print, echo, log, summarize, transform, validate, or copy a token value from chat or config output. If a token appears in chat or tool output, do not repeat it.

Preferred storage order:

1. User-scoped OS environment variable or MCP host secret/env config using `PIXELLAB_SECRET`.
2. Hidden local prompt or host UI that writes user-scoped env/keychain/secret config.
3. `.env.local` in a private, gitignored app directory.

Avoid project `.env`, committed MCP config, generated docs, shell history, chat transcripts, copied website session tokens, and literal `Authorization: Bearer ...` values in config files.

Use one canonical env var in new examples:

```text
PIXELLAB_SECRET
```

Use it for REST as:

```text
Authorization: Bearer <PIXELLAB_SECRET value>
```

Do not introduce aliases such as `PIXELLAB_API_KEY`, `PIXELLAB_TOKEN`, or `YOUR_API_TOKEN` in new instructions. If official docs use another placeholder, explain that the same bearer token should be stored in `PIXELLAB_SECRET`.

## MCP Configuration Guidance

For MCP setup, stay host- and platform-agnostic unless the user named a host.

Good guidance:

- Use the host's MCP settings UI or documented MCP config file.
- Configure PixelLab MCP to read `PIXELLAB_SECRET` from the host environment or secret store.
- If the host supports secret references, use the host secret reference instead of a literal token.
- If a config file already contains a literal bearer token, suggest moving it into env/secret config; do not extract or print it.
- After config changes, tell the user to restart or reload the MCP host when that host requires it.

Before writing config:

- Explain the exact file or setting you intend to change.
- Show a token-free preview using placeholders or secret references only.
- Ask for confirmation.
- Write only after explicit approval.

If the user asks for a generic MCP snippet, provide a token-free template and note that field names vary by host. Prefer the official PixelLab MCP setup page for host-specific details.

## API Configuration Guidance

For REST/API setup, tailor examples to the user's platform but keep the credential pattern stable.

Safe examples may show:

- Reading `PIXELLAB_SECRET` from the process environment.
- Passing `Authorization: Bearer ...` from that environment value.
- A no-credit check against balance or an official lightweight endpoint when the user approves a live check.
- How MCP and API can reuse the same credential source.

Do not hard-code token literals. Do not generate commands that would echo the secret. Avoid commands that persist secrets in shell history. When platform-specific persistent env setup is needed, prefer OS or host settings UI, documented secret stores, or user-scoped environment configuration over project files.

## Prompt Before Writes

Any setup action that writes files, environment settings, MCP host config, shell profiles, `.env.local`, package files, or project scripts needs confirmation first.

Before asking, report:

- Target surface: MCP, API, or both.
- Exact destination: config file, host setting, env var, app file, or project file.
- Secret handling: token-free placeholder, env var reference, or host secret reference.
- Reload step: whether a terminal, app, server, or MCP host must restart.

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
- If failed, report the likely layer: missing env var, MCP host not loaded, auth rejected, network failure, endpoint unavailable, or SDK/tool mismatch.

## What To Report

For setup help, report only what helps the user proceed:

- Detected intent: MCP, API, both, or unknown.
- Current readiness: ready, partially ready, not configured, blocked, or unknown.
- Credential location type: env var, host secret, literal config value found, or not found. Never report the credential value.
- Next safest step.
- Any write you propose, with destination and token-handling approach.
- Whether a restart/reload is needed.
- Whether a live auth check was no-credit and what it verified.

## What Not To Do

- Do not ask for, paste, print, echo, log, or quote the bearer token.
- Do not use website/Supabase/browser session tokens for REST or MCP.
- Do not scrape browser storage or session cookies.
- Do not call undocumented website endpoints as setup verification.
- Do not run credit-spending generation/edit endpoints during setup checks.
- Do not write MCP config, env files, shell profiles, package files, or project code without explicit confirmation.
- Do not scan broad credential/config directories.
- Do not claim SDK support, MCP tool availability, pricing, limits, or current endpoint behavior without checking when those facts matter.
- Do not require PixelLab Pip-specific agent behavior from hosts that only support generic MCP or REST.

## Agent- and Platform-Agnostic Flow

Use this default flow for natural-language setup mode:

1. Identify whether the user wants MCP, API, or both.
2. Diagnose current readiness using available tools and only user-approved/specific config paths.
3. Explain the safe credential model: one PixelLab bearer token stored as `PIXELLAB_SECRET` or host secret config.
4. Offer token-free setup steps for the user's host/platform.
5. Ask before writing config or changing environment.
6. Run only no-credit readiness checks after approval.
7. Report outcome and the next concrete step.

If host-specific details are unknown, give a generic MCP/REST pattern and route the user to `https://www.pixellab.ai/mcp` or `https://api.pixellab.ai/v2/docs` for the host- or endpoint-specific fields.
