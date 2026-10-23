# Style Examples

Optional named starting points when the user wants style setup (`project-style.md`). Each name says what it is for. They
are offers, never defaults: write one only when the user picks it, with
`python assets/project_style.py example "<name>" --use` (add `--as <name>` to rename). `project_style.py` holds the
exact field values.

| Example | Made for | Evidence scope |
|---|---|---|
| Side-view dark fantasy | side-view action and RPG fights; ~96x200 heroes; padded key-pose attacks and skills (`key-pose-animation.md`), muted dark palette | reported source examples; not a cross-style benchmark |
| Top-down cozy | top-down farming and life sims; 48 px canvas (a ~24x32 chibi figure), 4-direction walk, pastel palette, soft outline | one walkable farmer demonstration |
| Top-down 8-direction | top-down 3/4 RPGs needing eight facings; ~64 px characters (`eight-direction.md`) | written, not yet proven |
| Side-view sci-fi | side-view shooters and action; 96x200 canvas, padded key-pose attacks like dark fantasy, hard-surface shapes, glowing accents | one armoured marine, two moves |

Sizes are canvases (the sprite's image size), not the figure: the figure inside is smaller and its shape decides how much.
A style's negative never overrides what the user asked for: drop a negative that names a requested item (a chain-axe
under "no medieval weapons") from that call.

After picking, the user can change any field; the saved style is theirs from then on.

## Side-view dark fantasy production example


Optional production values reported for the selected "Side-view dark fantasy" example, not defaults or an automatic full recipe. Pose/animation charges are dated observations; current route pricing and the requested count govern the paid plan.

| Setting | Value |
|---|---|
| Hero sprite | 96×200, facing right |
| Overhead pad | 192×256, sprite at (24, 56); poses 9 each |
| Front-only pad | 192×200, sprite at (24, 0); poses 6 each |
| Boss pad | 256×256, feet on the bottom edge |
| Swing example | `frame_count` 10 (11 returned frames) on 192×256; an extra six-frame crescent source is optional separately approved work |
| Light timing (heroes) | 60 ms per frame, wind-up 160 ms, hit 140 ms, settle 120 ms |
| Heavy timing (bosses) | beats × a 50–70 ms step: stand 0.6, wind-up 4.0, in-betweens 0.8, hit 3.2, settle 1.4 |
| Calm timing | in-betweens 100–140 ms, key stages 220–450 ms, release 60 ms, follow-through about 450 ms |
| Hurt snap | peak 300 ms, then idle |
| Crescent | pale "air" ramp behind the character |
| Historical recipe costs | Reported 31 generations at 192×256, 22 at 192×200; a shot 18. Not current price quotes or budget authority. |
