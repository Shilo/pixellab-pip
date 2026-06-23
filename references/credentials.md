# Credentials

Read this for PixelLab credential setup, credential-name labels, or reusing MCP auth for REST API calls.

PixelLab uses one account credential for public REST v2 and hosted MCP. Different surfaces call that same value an API key, API token, bearer token, or secret. Treat those as labels for one credential, not different token types.

User-facing examples:

- The PixelLab API page/account UI may call it an API key.
- The account page may call it a secret.
- REST and MCP docs call it an API token or bearer token.

Use the credential as:

```text
Authorization: Bearer <PixelLab account credential>
```

Use one canonical local env var for new agent/API examples:

```text
PIXELLAB_SECRET
```

Do not create additional env var aliases. Official examples may say `YOUR_API_TOKEN` or `YOUR_SECRET`; put that same account credential in `PIXELLAB_SECRET`.

## MCP Reuse

If PixelLab MCP is already configured, reuse its credential source when safe:

- If the MCP config uses `PIXELLAB_SECRET`, REST code can read the same env var.
- If the MCP config uses a host secret reference, tell the user to configure REST/API code to use that same secret mechanism when the host supports it.
- If the MCP config contains a literal `Authorization: Bearer ...` value, do not extract, print, or copy it. Suggest moving it to env/secret config.

Never ask the user to paste the credential into chat. Never use website/Supabase session tokens for REST or MCP.

Inspect only named config paths and redact secret-like values. Do not scan broad home/auth/config directories because tool output can leak secrets.

Fallback order:

1. User-scoped OS environment variable or MCP host secret/env config.
2. Hidden local prompt that writes user-scoped env/keychain config.
3. `.env.local` in a private, gitignored app directory.
4. Avoid project `.env`, committed MCP config, generated docs, shell history, chat transcript, and copied browser session tokens.
