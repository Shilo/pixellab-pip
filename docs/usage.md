# Usage And Setup

Use this guide after [installing PixelLab Pip](install.md). The product capability overview stays front-facing in the [README](../README.md#features).

## Invoke Pip

Use the prefix supported by your agent:

```text
/pixellab-pip <prompt>
@pixellab-pip <prompt>
$pixellab-pip <prompt>
pip <prompt>
```

The plain `pip` form can work through automatic skill discovery when the surrounding request clearly concerns PixelLab or Pip. Explicit invocation is more reliable.

Examples:

```text
/pixellab-pip make a cute knight character sprite
pip animate this idle character
@pixellab-pip edit this image into cleaner 32px pixel art
@pixellab-pip create a tiny potion sprite, then make an Aseprite workspace with frames, a tag, a GIF preview, and a sprite sheet
@pixellab-pip create a mossy top-down tileset, then clamp it to 1-bit black and white
@pixellab-pip make a small item icon sheet and reduce it to a Game Boy green palette
```

Implicit invocation can work for requests such as “setup PixelLab,” “configure PixelLab MCP,” “make a sprite,” “generate a tileset,” “animate this,” “edit this image,” “call the REST API,” or “check PixelLab docs.” Explicit invocation is still recommended when you want Pip used for sure.

## Commands

### Setup

```text
/pixellab-pip setup
@pixellab-pip setup
$pixellab-pip setup
```

Runs the PixelLab setup wizard. Pip detects what is missing, presents a token-free configuration preview, and changes settings only after approval.

### Auto

```text
/pixellab-pip auto
/pixellab-pip auto on
/pixellab-pip auto off
```

Controls the confirmation before paid PixelLab calls. Auto is **off by default**. Before the first paid call in a job, Pip shows every planned call, exact wording, and rough total cost, then asks once for approval. Auto mode never overrides an explicit “ask me first” instruction or confirmation before deleting or overwriting remote assets.

With Auto on, Pip skips approval but still shows the planned paid calls, rough total cost, and how to turn Auto off.

The preference persists in `pixellab-pip.json` beside the installed `SKILL.md` when that directory is writable, with a user-config fallback otherwise.

### Bark

```text
/pixellab-pip bark
/pixellab-pip bark on
/pixellab-pip bark off
```

Controls the completion sound. Bark is **on by default**. `bark on` also tests the sound. It runs after successful live generation, edit, transform, conversion, background removal, or animation—not after setup, status checks, documentation, failures, downloads alone, or local post-processing alone.

Because bark starts on, a first-run `bark` command usually toggles it off without playing. Use `bark on` to test the sound.

The Bark preference persists in `pixellab-pip.json` beside the installed `SKILL.md` when that directory is writable, with the same user-config fallback as Auto.

The bundled sound is `assets/bark.wav` inside the installed skill. Pip falls back to a native success or alert sound if the helper cannot play it.

### Update

```text
/pixellab-pip update
```

Updates Pip through its current marketplace, plugin, extension, or copied-skill install route. Platform-specific commands are in [Installation](install.md).

### Uninstall

```text
/pixellab-pip uninstall
```

Shows what will be removed and asks first. Pip keeps the PixelLab Secret and `pixellab-pip-generations/` outputs unless you explicitly ask to remove them.

Manual alternative: use your agent's plugin or extension uninstall command, or delete the copied `pixellab-pip` skill folder.

## Connect PixelLab MCP And API

For most users, run `/pixellab-pip setup` and choose **MCP + API**. MCP connects PixelLab tools directly to the assistant; API fallback lets Pip use documented REST v2 routes when MCP is unavailable or does not expose the needed capability.

Bundled local helpers require Python 3.10 or newer.

| Wizard mode | Use it when | What Pip does |
|---|---|---|
| MCP + API | Recommended for direct tools plus complete documented fallback coverage. | Sets up MCP, then checks that the same `PIXELLAB_SECRET` source is visible where Pip runs. |
| MCP only | You want only PixelLab tools exposed by MCP. | Detects or asks which app you use, previews the client configuration, and applies it after confirmation. Pip prefers app secret settings or an environment/secret reference; a hardcoded MCP config is only an explicit user-chosen fallback when the app has no token-free option. REST-only fallback routes remain unavailable. |
| API only | You want documented REST v2 fallback without adding MCP. | Configures or verifies `PIXELLAB_SECRET` for Pip. |
| Manual | You want to follow PixelLab's instructions yourself. | Opens or links to [PixelLab's MCP setup page](https://www.pixellab.ai/mcp) and stops. |

## Token Safety

Open the PixelLab [account page](https://www.pixellab.ai/account) after signing in and copy the value labeled `Secret`. PixelLab may describe it as an API key, API token, secret, or token. Pip uses it as a bearer token for documented MCP and REST v2 authentication.

For local REST fallback, the recommended secret name is:

```text
PIXELLAB_SECRET
```

Store the value outside chat. Never paste it into a conversation, commit it, print it in logs, copy a browser session token, or ask an agent to scan `.env*`, shell history, home directories, keychains, or environment dumps. Pip does not need those actions.

For the complete service boundary and threat model, read [Security and trust](security.md) and [PixelLab auth and security](pixellab/pixellab-auth-and-security.md).
