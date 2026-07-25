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

The helper writes `bark` to `pixellab-pip.json` beside `SKILL.md` atomically, preserving the other key (notably `auto`). Do not hand-edit the JSON — the read-modify-write is what a short-turn agent corrupts (misreading the current value flips the toggle backwards). If Python is unavailable, hand-write `bark` as a boolean in that file, preserving `auto`; if the skill directory is read-only, write instead to `pixellab-pip/pixellab-pip.json` inside the OS user-config dir (`%APPDATA%` on Windows, `~/Library/Application Support` on macOS, `${XDG_CONFIG_HOME:-~/.config}` on Linux) — where the helper also reads it. Do not scan other config, home, shell, credential, or project directories for it. Do not rewrite config except when the user runs an explicit `bark` command. If persistence fails everywhere, say the setting could not be saved and do not claim it changed.

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
