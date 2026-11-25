# Game Music And Sound Effects

Read this for game music, seamless loops, lyrics/vocals, or sound effects. This is generated game audio, not Pip's completion chime (`bark.md`).

## Route Choice

| Need | MCP | REST v2 | Cost and notes |
|---|---|---|---|
| Music from a style description | `create_music` | `POST /music` | Two takes per request. 10 generations or $0.08 credits, charged when made. Tier 2+; ~20–60 s, up to 2.5 min. |
| Restyle an existing song | `create_music(restyle_song_id=...)` | `POST /music` with `restyle_song_id` | Same price and tier as a new song. Keeps the melody, vocals and lyrics; send no `lyrics`, `auto_lyrics` or `about`. |
| Seamless game loop | `make_music_loop` | `POST /music/{song_id}/loop` | Two takes with `loop_start_s`/`loop_end_s`. 4 generations or $0.033. Completed instrumental only; not a loop already. MCP states Tier 2+, REST Tier 1+. |
| Expand a short music idea | `improve_music_style` | `POST /music/improve-style` | 0.05 generations, synchronous. Then send the expanded `style` with the same `instrumental` and `bpm`. |
| Write lyrics | `write_music_lyrics` | `POST /music/lyrics` | 0.05 generations, synchronous. Returns two versions with section tags. |
| List/get music | `list_music`, `get_music` | `GET /music`, `GET /music/{song_id}` | Free. `list_music` is newest first. |
| Rename music | `rename_music` | `PATCH /music/{song_id}` | Free; renames it in the library and in games. |
| Delete music | `delete_music` | HTTP DELETE on `/music/{song_id}` | Destructive; see below. |
| Sound effect | `create_sound_effect` | `POST /sound-effects` | One clip per request. Priced by length. MCP states Tier 2+, REST Tier 1+. |
| List/get sound effects | `list_sound_effects`, `get_sound_effect` | `GET /sound-effects`, `GET /sound-effects/{sound_effect_id}` | Free. |
| Rename sound effect | `rename_sound_effect` | `PATCH /sound-effects/{sound_effect_id}` | Free. |
| Delete sound effect | `delete_sound_effect` | HTTP DELETE on `/sound-effects/{sound_effect_id}` | Destructive; see below. |

Sound-effect cost is charged only when the clip is made: 1 generation up to 1.6 s, 2 up to 3.2 s, 4 at 6 s, 7 at 10 s, 19 at 30 s (0.614 per second, rounded up; $0.0027 per second in credits). `seconds` is 0.5–30, default 2.

## Music Inputs

- `style` (required, 1–1000 chars) is a sentence or two that gives each instrument a role, plus mood and how the song ends. A tag list comes out flat, and artist names are refused. Keep sounds to exclude in `exclude`, not as “no …” in `style`.
- `instrumental` defaults to true. For vocals, set it false and supply `lyrics` or `auto_lyrics`. With `auto_lyrics`, send no `lyrics`, `length_s` or `style_weight`; `about` (≤200 chars) says what the song is about.
- Supplied `lyrics` (≤5000 chars): one line per line, with section tags on their own lines (`[Intro]`, `[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Instrumental Break]`, `[Outro]`, `[End]`). A tag may carry one direction, such as `[Chorus: full band, doubled vocals]`. Preserve the user's lyrics exactly; do not rewrite or translate them unless asked.
- `length_s` is 10–360 (omit for auto), `bpm` 60–180 (omit for auto), `voice` ≤100 chars (vocals only), `exclude` ≤1000, `style_weight` 0–1 (default 0.5), `name` ≤120.
- `create_music` also accepts `project_id` for Game Builder project context; REST `POST /music` has no such field.
- For a short idea such as “spooky swamp level”, use the style improver first rather than padding it by hand.

## Sound-Effect Inputs

`prompt` (required, 1–1000 chars) describes the sound in plain words, including material and action: “a heavy sword slash hitting metal armor”. `seconds` sets clip length; a hit or shot is about 1 s, an explosion or growl about 3 s, ambience 10–30 s. `name` ≤120 chars. `create_sound_effect` also accepts `project_id`; REST does not.

## Lifecycle And Output

- Music returns two takes; `get_music`/`GET /music/{song_id}` reports status, and a completed take exposes `audio_url` (MP3, no auth) and `duration_ms`. With `auto_lyrics`, `lyrics` shows what it sings. Poll every 10 s until terminal; the generic background-job route also works.
- A loop take adds `loop_start_s` and `loop_end_s`; play to the end then jump back to the start. The intro plays once.
- Sound effects return one WAV per request with `audio_url` and `duration_ms`; poll every few seconds.
- Every new paid request usually makes a new take; asking again is another paid call. For another sound-effect take, submit again.
- Save the downloaded MP3/WAV in the generation folder with the other deliverables, and verify terminal status and expected duration before reporting completion. Download links are unauthenticated, so treat them as sensitive.
- Do not quote an audio file, duration, or lyric that the returned result does not contain.

## Destructive Actions

Deleting a song or sound effect removes it from the library and from games, and cannot be undone. A pending song is stopped together with its other take and is charged if it had already started. Follow SKILL.md's Destructive Remote Actions gate; renaming is not destructive.

## Prompt Preparation

Write music style and SFX prompts as natural-language descriptions, not tool instructions. Keep music `exclude` for sounds to keep out and SFX prompts for the sound itself.
