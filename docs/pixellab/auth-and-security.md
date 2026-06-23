# PixelLab Auth And Security

Last reviewed: 2026-06-23.

Purpose: document the safe credential and session boundaries agents need before calling PixelLab MCP, REST v2, website/editor workflows, or generated asset links.

PixelLab REST v2 and hosted MCP use bearer-token authentication. Pip should guide users toward local secret configuration and avoid exposing credentials in chat or generated docs.

## Bearer Token Handling

- Get the PixelLab token from the [PixelLab account page](https://www.pixellab.ai/account) after signing in.
- Store the token locally as `PIXELLAB_SECRET` or in the agent app's secret configuration.
- Send it to REST v2 or MCP as `Authorization: Bearer <token>`.
- Do not paste the token into chat.
- Do not commit tokens to source control.
- Do not print tokens in logs, generated docs, examples, or error output.
- When checking auth setup, inspect only user-specified config paths. Do not broadly scan home, auth, or shell-history directories, and never print literal `Authorization` values.

PixelLab UI/docs may use terms such as API key, API token, bearer token, or secret for the account credential. For technical REST/MCP authentication, call it a bearer token. For local environment examples, use `PIXELLAB_SECRET`.

## Website Session Boundary

Website login sessions and public REST/MCP bearer tokens are separate auth contexts. Do not copy browser session tokens into scripts or use them for automation.

When a requested workflow appears to require a website-only action, route to:

1. A documented REST v2 endpoint, if available.
2. A documented MCP tool, if available.
3. A visible website/editor workflow with explicit user permission.

## Download URLs

Some generated asset download URLs may be unauthenticated/shareable, with an unguessable identifier acting as the access key. Treat them as intentional-share output links:

- Share only with the user who requested the generation.
- Avoid committing them to public repos.
- Avoid including them in logs when not necessary.

## Public Docs Rule

Public docs may include placeholders such as `YOUR_API_TOKEN` or `<PIXELLAB_SECRET value>`. They must not include real credentials, session tokens, cookies, JWTs, or account-specific values.
