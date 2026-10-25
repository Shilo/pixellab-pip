# Bark

Use this reference when the user runs a bark command, or when a live PixelLab job returns image(s).

## Commands

One short word after the skill trigger; the `/`, `@`, `$` prefixes and the `on`/`off` variants all work, whether the app passes it as an argument or as prose:

```text
/pixellab-pip bark
@pixellab-pip bark on
$pixellab-pip bark off
```

- `bark`: run `python assets/bark.py bark` (reads, flips, and persists the value).
- `bark on`: run `python assets/bark.py on`.
- `bark off`: run `python assets/bark.py off`.

`bark` is on by default: no config, no `bark` key, or a non-boolean value all mean on. After a successful write, reply `Bark is on.` or `Bark is off.` If the command enables bark, immediately play the sound so it also tests audio; if it disables bark, do not play.

A bare first-run `bark` usually toggles bark off and plays nothing; use `bark on` to test the sound without risking an off toggle.

## Config

`pixellab-pip.json` holds a boolean per setting:

```json
{
  "bark": true
}
```

Use the helper for ordinary Bark writes; it preserves other settings and verifies persistence. For manual/no-Python handling or a persistence/config error, read only [Auto → Config](auto.md#config) for the shared storage, precedence, repair and fallback procedure. A Bark command changes only `bark`, never Auto. On failure, do not claim the setting changed.

## When To Play

When bark is enabled, play the configured sound only after a live PixelLab generation, edit, transform, conversion, background-removal, or animation job or task returns image(s). Eligible completions:

- PixelLab asset generation.
- PixelLab image edit, transform, conversion, or background-removal job that produces a new generated result.
- PixelLab animation or animation-edit job.
- MCP managed asset task once the final asset/result exists.
- REST async job once polling reaches a final success state.

Do not bark for:

- Setup, auth, readiness, or no-credit balance checks.
- Status checks for jobs that were already completed earlier.
- Docs lookups, endpoint selection, prompt enhancement alone, or normal chat answers.
- Failed, canceled, rejected, timed-out, still-pending, or unknown-status jobs — job status, not a returned result that fails verification.
- Downloads, local file assembly, local previews, spritesheet/GIF assembly, or validation when no live PixelLab generation/edit/animation job finished in this turn.
- Manual website instructions unless the assistant directly observed a PixelLab generation finish in the visible website flow and the user had approved that action.

## Sound

The bark sound path is not configurable: the bundled helper resolves it as `assets/bark.wav` inside the same skill directory as `SKILL.md`. Missing config must not prevent resolving the bark sound path.

Run the bundled helper from the skill directory first; it always prints JSON:

```text
python assets/bark.py play
```

The helper output includes `bark` and `played`, and `status` may include `config` or `invalid_config`. If `bark` is `true` and `played` is `false`, or the helper exits with code `2`, use the native fallback below.

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
