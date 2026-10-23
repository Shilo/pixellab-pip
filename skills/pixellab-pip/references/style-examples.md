# Style Examples

Named starting points to offer when a project has no style (`project-style.md`). Each name says what it is for. They
are offers, never defaults: write one only when the user picks it, with
`python assets/project_style.py example "<name>" --use` (add `--as <name>` to rename). `project_style.py` holds the
exact field values.

| Example | Made for | Tested |
|---|---|---|
| Side-view dark fantasy | side-view action and RPG fights; ~96x200 heroes; padded key-pose attacks and skills (`key-pose-animation.md`), muted dark palette | yes: many characters and moves |
| Top-down cozy | top-down farming and life sims; 48 px canvas (a ~24x32 chibi figure), 4-direction walk, pastel palette, soft outline | yes: one walkable farmer |
| Top-down 8-direction | top-down 3/4 RPGs needing eight facings; ~64 px characters (`eight-direction.md`) | written, not yet proven |
| Side-view sci-fi | side-view shooters and action; 96x200 canvas, padded key-pose attacks like dark fantasy, hard-surface shapes, glowing accents | yes: one armoured marine, two moves |

Sizes are canvases (the sprite's image size), not the figure: the figure inside is smaller and its shape decides how much.
A style's negative never overrides what the user asked for: drop a negative that names a requested item (a chain-axe
under "no medieval weapons") from that call.

After picking, the user can change any field; the saved style is theirs from then on.
