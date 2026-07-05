# Bark

Use this reference when the user runs a bark command, or when a live PixelLab job finishes successfully.

## Commands

One short word after the skill trigger. Any of the `/`, `@`, `$` prefixes work, and `on`/`off` variants set state explicitly:

```text
/pixellab-pip bark
@pixellab-pip bark on
$pixellab-pip bark off
```

Some apps expose post-trigger text as structured arguments, others as normal prompt text; treat `bark`, `bark on`, and `bark off` the same either way.

- `bark`: read the persisted state, toggle it, write the new state.
- `bark on`: write `"bark": true`.
- `bark off`: write `"bark": false`.

With the bundled helper, pass the same intent:

```text
python assets/bark.py bark
python assets/bark.py on
python assets/bark.py off
```

After a successful write, respond `Bark is on.` or `Bark is off.` If the command enables bark, immediately play the sound so it also tests audio; if it disables bark, do not play.

Bark is on by default: no `pixellab-pip.json` — or invalid JSON with no valid fallback config — means bark is enabled for the current command. So a bare first-run `bark` usually toggles bark off and plays nothing; use `bark on` to test the sound without risking an off toggle.

## Config

Persist bark state in `pixellab-pip.json` next to this skill's `SKILL.md`:

```json
{
  "bark": true
}
```

Precedence: skill-local `pixellab-pip.json` is authoritative whenever it can be written. If the skill directory is read-only, fall back to the exact user-config path for the current OS:

- Windows: `%APPDATA%\pixellab-pip\pixellab-pip.json`
- macOS: `~/Library/Application Support/pixellab-pip/pixellab-pip.json`
- Linux: `${XDG_CONFIG_HOME:-~/.config}/pixellab-pip/pixellab-pip.json`

The user-config path is only a read fallback when no valid skill-local config exists, and a write fallback when skill-local persistence fails. Do not scan broad config, home, shell, credential, or project directories. An update or reinstall that replaces the skill directory may reset skill-local config to default-on.

When the user runs `bark`, `bark on`, or `bark off`, write the valid shape above to skill-local config first; if that write fails, write the exact user-config fallback path. If both writes fail, say the setting could not be saved persistently and do not claim it changed. Do not rewrite config during normal generation completion. Preserve any extra fields when changing `bark` if the available file-editing tools make that practical; otherwise keep only `bark`.

## When To Play

When bark is enabled, play the configured sound only after a live PixelLab generation, edit, transform, conversion, background-removal, or animation job or task finishes successfully and passes verification. Eligible completions:

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

The bark sound path is not configurable: the bundled helper resolves it as `assets/bark.wav` inside the same skill directory as `SKILL.md`. Missing config must not prevent resolving the bark sound path.

Run the bundled helper from the skill directory first; it always prints JSON:

```text
python assets/bark.py play
```

If `python` is unavailable, try `python3 assets/bark.py play`, or `py -3 assets/bark.py play` on Windows only. Do not install Python or audio tools. The helper output includes `bark` and `played`, and `status` may include `config` or `invalid_config`. If `bark` is `true` and `played` is `false`, or the helper exits with code `2`, use the native fallback below.

If the helper cannot load or run, fall back to a native success or alert sound that needs no bundled WAV, other audio file, MCP, or install step:

- If a host/app notification primitive clearly supports a native `success`, `done`, or `alert` sound, use it without passing a file path.
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

Do not pass `assets/bark.wav` to host/app fallback tools. Do not install audio tools or sound servers during generation reporting. If neither the helper nor a native fallback can play sound, fail quietly and continue the normal PixelLab report — never block on sound. After a full helper-plus-native-fallback failure, do not keep retrying sound for later completions in the same conversation/session; only try again if the user explicitly runs `bark` or `bark on` as a sound test, or in a new conversation/session.
