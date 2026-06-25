# Bark

Use this reference when the user runs a bark command or when a live PixelLab generation, edit, transform, conversion, background-removal, or animation job finishes successfully.

The intended command is one short word after the skill trigger:

```text
/pixellab-pip bark
@pixellab-pip bark
$pixellab-pip bark
```

Explicit state commands are also supported:

```text
/pixellab-pip bark on
/pixellab-pip bark off
```

Some apps expose text after a slash command as arguments, while others treat it as normal prompt text. Treat `bark`, `bark on`, and `bark off` the same either way.

## Config

Persist bark state in `pixellab-pip.json` next to this skill's `SKILL.md`:

```json
{
  "bark": true
}
```

No `pixellab-pip.json` means bark is enabled.

Read and write only this skill-local `pixellab-pip.json` for bark state. If the skill directory is read-only, fall back to the exact user config path for the current OS:

- Windows: `%APPDATA%\pixellab-pip\pixellab-pip.json`
- macOS: `~/Library/Application Support/pixellab-pip/pixellab-pip.json`
- Linux: `${XDG_CONFIG_HOME:-~/.config}/pixellab-pip/pixellab-pip.json`

Do not scan broad config, home, shell, credential, or project directories.

Skill-local config is authoritative whenever it can be written. The user config path is only a read fallback when no valid skill-local config exists, and a write fallback when skill-local persistence fails.

Because skill-local config lives inside the installed skill directory, an update or reinstall that replaces that directory may reset bark to the default-on state. If the skill directory is not writable, the exact user-config fallback path is used instead.

If `pixellab-pip.json` exists but is invalid JSON and no valid fallback config exists, treat bark as enabled for the current command. When the user explicitly runs `bark`, `bark on`, or `bark off`, write the valid shape above to the skill-local config first; if that write fails, write the exact user-config fallback path. Do not rewrite config during normal generation completion.

If `pixellab-pip.json` exists and contains extra fields, preserve them when changing `bark` if the available file editing tools make that practical. If preserving extra fields is not practical, keep only `bark`.

## Bark Commands

- `bark`: read the persisted state, toggle it, and write the new state.
- `bark on`: write `"bark": true`.
- `bark off`: write `"bark": false`.

When using the bundled helper to execute bark commands, pass the same command intent:

```text
python assets/bark.py bark
python assets/bark.py on
python assets/bark.py off
```

After a successful write, respond briefly with the new state:

- `Bark is on.`
- `Bark is off.`

If `bark` toggles bark on, or if `bark on` enables bark, immediately play the bark sound so the command also tests audio. If `bark` toggles bark off, or if `bark off` disables bark, do not play a bark sound.

Because bark is on by default, a bare first-run `bark` command usually toggles bark off and does not play sound. Use `bark on` when the user only wants to test the sound without risking an off toggle.

If both skill-local and user-config fallback writes fail, say that bark could not be saved persistently. Do not claim the setting changed.

## When To Play

When bark is enabled, play the configured sound only after a live PixelLab generation, edit, transform, conversion, background-removal, or animation job or task finishes successfully.

Eligible completions:

- Successful PixelLab asset generation.
- Successful PixelLab image edit, transform, conversion, or background-removal job that produces a new generated result.
- Successful PixelLab animation or animation-edit job.
- Successful MCP managed asset task after the final asset/result existence and requested constraints are verified.
- Successful REST async job after polling reaches a final success state and the result is verified.

Do not bark for:

- Setup, auth, readiness, or no-credit balance checks.
- Status checks for jobs that were already completed earlier.
- Docs lookups, endpoint selection, prompt enhancement alone, or normal chat answers.
- Failed, canceled, rejected, timed-out, still-pending, or unknown-status jobs.
- Downloads, local file assembly, local previews, spritesheet/GIF assembly, or validation when no live PixelLab generation/edit/animation job finished in this turn.
- Manual website instructions unless the assistant directly observed a PixelLab generation finish in the visible website flow and the user had approved that action.

## Sound

The bark sound path is not configurable. The bundled helper resolves it as `assets/bark.wav` inside the same skill directory as `SKILL.md`. Missing config must not prevent resolving the bark sound path.

Run the bundled helper from the skill directory first. The helper always prints JSON:

```text
python assets/bark.py play
```

If `python` is unavailable, try:

```text
python3 assets/bark.py play
py -3 assets/bark.py play
```

Use `py -3` only on Windows. Do not install Python or audio tools. The helper uses only standard library code and always prints JSON. Its output includes `bark` and `played`, and `status` may include `config` or `invalid_config`; if `bark` is `true` and `played` is `false`, or if the helper exits with code `2`, use the native fallback below.

If the helper cannot load or run, fall back to a native success or alert sound that does not require the bundled WAV, another audio file, MCP, or any install step:

- If an available host/app notification primitive clearly supports a native `success`, `done`, or `alert` sound, use that without passing a file path.
- On Windows, an agent with shell access may run PowerShell's native system sound:

  ```powershell
  [System.Media.SystemSounds]::Asterisk.Play(); Start-Sleep -Milliseconds 500
  ```

- On macOS, an agent with shell access may use the native alert sound:

  ```bash
  osascript -e 'beep 1'
  ```

- On Linux or other POSIX-like shells, an agent with shell access may try the terminal bell:

  ```bash
  printf '\a'
  ```

Do not pass `assets/bark.wav` to host/app fallback tools. Do not install audio tools or sound servers during generation reporting. If neither the helper nor a native fallback can play sound, fail quietly and continue the normal PixelLab report. For later generation completions in the same conversation/session, do not keep retrying sound after a full helper-plus-native-fallback failure. Only try again if the user explicitly runs `bark` or `bark on` as a sound test, or in a new conversation/session.

Future audio formats may include `.wav`, `.wave`, or `.mp4`, but the current deterministic bundled sound is `assets/bark.wav`.
