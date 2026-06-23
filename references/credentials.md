# Credentials

Read this for PixelLab bearer-token setup, PixelLab UI naming, or reusing MCP auth for REST API calls.

PixelLab uses one account-level bearer token for public REST v2 and hosted MCP. End-user setup should store that token in `PIXELLAB_SECRET`. PixelLab UI and examples may call the same value an API key, API token, or secret; when discussing REST/MCP authentication, use the technical term `bearer token`.

User-facing setup wording:

- Store your PixelLab token in `PIXELLAB_SECRET`.
- The PixelLab API/account UI may label this value as an API key, API token, or secret.
- Do not paste the value into chat.

Use the bearer token as:

```text
Authorization: Bearer <PIXELLAB_SECRET value>
```

Use one canonical local env var for new agent/API examples:

```text
PIXELLAB_SECRET
```

Do not create additional env var aliases. Official examples may say `YOUR_API_TOKEN` or `YOUR_SECRET`; put that same bearer token in `PIXELLAB_SECRET`.

## MCP Reuse

If PixelLab MCP is already configured, reuse its credential source when safe:

- If the MCP config uses `PIXELLAB_SECRET`, REST code can read the same env var.
- If the MCP config uses a host secret reference, tell the user to configure REST/API code to use that same secret mechanism when the host supports it.
- If the MCP config contains a literal `Authorization: Bearer ...` value, do not extract, print, or copy it. Suggest moving it to env/secret config.

Never ask the user to paste the bearer token into chat. Never use website/Supabase session tokens for REST or MCP.

Inspect only named config paths and redact secret-like values. Do not scan broad home/auth/config directories because tool output can leak secrets.

Fallback order:

1. User-scoped OS environment variable or MCP host secret/env config.
2. Hidden local prompt that writes user-scoped env/keychain config.
3. `.env.local` in a private, gitignored app directory.
4. Avoid project `.env`, committed MCP config, generated docs, shell history, chat transcript, and copied browser session tokens.
