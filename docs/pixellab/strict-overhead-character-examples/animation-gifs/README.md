# One-direction overhead animation attempts

All 38 attempts are preserved, including failures.

Each model/path folder is flat and contains GIFs only. Names are motion + attempt number; attempts 01 and 02 are the initial and controlled rounds. Shooting attempts 03â€“05 are the final targeted variants.

GIFs are faithful 4x nearest-neighbour inspection previews at 10 fps. V3/PixMiniMax retain the input echo plus 8 generated frames (9 total); Skeleton v3 returns 8 generated frames. Original 64x64 PNGs, input copies, exact requests and blueprints remain in the local run's original per-call folders. The portable [validation record](../follow-up-validation.json) contains every review; the [research report](../../pixellab-strict-overhead-characters-spike.md) records the requests and findings.

## Result

No fully verified production-ready idle/walk/run/shoot pack emerged. PixMiniMax is the strongest tested workflow: walk-02 is a provisional pass; idle-02, run-02 and shoot-05 are uncertain candidates. Review them visually before using them in a game. Raw Skeleton v3 authored keypoints removed extra limbs but often produced weak or static motion. Managed Skeleton v3 and v3 often lost grip/anatomy consistency.

The base-sprite text generator needs no guide. Animation needs its selected starting sprite. Character Creator is not required for the recommended raw PixMiniMax path.

## Every attempt

### pixminimax

| GIF | Review verdict |
|---|---|
| [idle-01.gif](pixminimax/idle-01.gif) | uncertain (best idle candidate; amplitude may be too low to read at 1x) |
| [idle-02.gif](pixminimax/idle-02.gif) | uncertain (best idle again; comparable to the initial PixMiniMax idle, with slightly more movement) |
| [walk-01.gif](pixminimax/walk-01.gif) | pass (provisional; GIF playback not directly viewed) |
| [walk-02.gif](pixminimax/walk-02.gif) | pass (provisional; strongest clip so far; GIF not directly viewed) |
| [run-01.gif](pixminimax/run-01.gif) | uncertain (clean but weak run read) |
| [run-02.gif](pixminimax/run-02.gif) | uncertain-leaning-pass (clean; distinctness from the walk is the open question) |
| [shoot-01.gif](pixminimax/shoot-01.gif) | fail (flash clipping); body animation is otherwise the best shoot |
| [shoot-02.gif](pixminimax/shoot-02.gif) | fail (the parent's 'better, needs grip/crop check' is not upheld: crop and speck failures are confirmed) |
| [shoot-03.gif](pixminimax/shoot-03.gif) | fail (repeats the PixMiniMax clipped-flame failure) |
| [shoot-04.gif](pixminimax/shoot-04.gif) | fail (the negative prompt was ignored) |
| [shoot-05.gif](pixminimax/shoot-05.gif) | uncertain (best shoot of all 38). The only defect is the f3 specks. Removing the 7 single-pixel components locally is a trivial non-paid cleanup, but the cleaned clip has not been re-reviewed, so this is not a production pass. |

### v3

| GIF | Review verdict |
|---|---|
| [idle-01.gif](v3/idle-01.gif) | fail |
| [idle-02.gif](v3/idle-02.gif) | fail (the same failure mode as the initial v3 idle; the controlled wording did not fix it) |
| [walk-01.gif](v3/walk-01.gif) | fail |
| [walk-02.gif](v3/walk-02.gif) | fail (grip) |
| [run-01.gif](v3/run-01.gif) | fail |
| [run-02.gif](v3/run-02.gif) | fail |
| [shoot-01.gif](v3/shoot-01.gif) | fail |
| [shoot-02.gif](v3/shoot-02.gif) | fail |
| [shoot-03.gif](v3/shoot-03.gif) | fail (repeats the v3 grip-break failure) |
| [shoot-04.gif](v3/shoot-04.gif) | fail as delivered. Best v3 shoot ever: f1-f8 are the first v3 frames that keep one pistol in both hands. Trimming f9 would leave a short subtle double-tap, but that is uncertain, not a pass. |
| [shoot-05.gif](v3/shoot-05.gif) | fail |

### skeleton-v3-raw

| GIF | Review verdict |
|---|---|
| [idle-01.gif](skeleton-v3-raw/idle-01.gif) | fail (static duplicate) |
| [idle-02.gif](skeleton-v3-raw/idle-02.gif) | fail (static still; do not promote) |
| [walk-01.gif](skeleton-v3-raw/walk-01.gif) | fail |
| [walk-02.gif](skeleton-v3-raw/walk-02.gif) | uncertain (clean but weak gait) |
| [run-01.gif](skeleton-v3-raw/run-01.gif) | fail |
| [run-02.gif](skeleton-v3-raw/run-02.gif) | uncertain (clean and coherent, but the run read is weak) |
| [shoot-01.gif](skeleton-v3-raw/shoot-01.gif) | fail |
| [shoot-02.gif](skeleton-v3-raw/shoot-02.gif) | fail (clean body and grip, but ring artifacts, a double flash and a near-static recoil) |

### skeleton-v3-character-creator

| GIF | Review verdict |
|---|---|
| [idle-01.gif](skeleton-v3-character-creator/idle-01.gif) | fail (near-static still plus pop; do not promote as an 8-frame idle) |
| [idle-02.gif](skeleton-v3-character-creator/idle-02.gif) | fail |
| [walk-01.gif](skeleton-v3-character-creator/walk-01.gif) | fail |
| [walk-02.gif](skeleton-v3-character-creator/walk-02.gif) | fail |
| [run-01.gif](skeleton-v3-character-creator/run-01.gif) | uncertain-leaning-fail (camera ok, motion unreadable) |
| [run-02.gif](skeleton-v3-character-creator/run-02.gif) | fail |
| [shoot-01.gif](skeleton-v3-character-creator/shoot-01.gif) | fail |
| [shoot-02.gif](skeleton-v3-character-creator/shoot-02.gif) | fail |

Full per-frame observations are in the sibling `animation-comparison.json`. Subjective naturalness was assessed from frame sequences and measurements; live GIF playback was not directly watched by the agent reviewers. No automatic generator can certify that a viewer will find a clip non-uncanny.
