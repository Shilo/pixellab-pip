# Scenes, Backgrounds and Buildings

Read this for a battle/level background, hub/menu backdrop, story picture, region map or building with upgrade tiers. The Intent Router selects the surface/model; this page supplies composition decisions. Apply saved appearance only under `project-style.md`.

## Shared settings

- `no_background: false` for every scene and background; `true` for a building sprite.
- Match a set using the selected route's supported style/reference fields (`style-reference.md`); distinguish appearance from layout references. For Pro sizes/candidate bands see `create-image-pro.md` rather than assuming every canvas is supported.
- A cheap pass with `create_image_pixflux` keeps the set's palette when `color_image_url` = the matching Pro image.
- Several requested regions/screens may share their approved anchor and palette. Seed selection remains the global workflow's decision.
- Add only exclusions that fit the request: a subjectless game backdrop may exclude figures/UI/text; a story scene containing a party keeps that party; a requested sign, labeled map or framed vignette keeps those elements.

## Battle and level backgrounds

- Fighters need somewhere to stand: `open flat <ground type> along the bottom third for fighters` naming the ground (street, marble floor, cave floor, stone ledge). Without it they stand on clutter; put clutter in the middle and back.
- A few landmarks and one light story (moonlight, torches, a portal) help readability. Palette contrast and horizon height should fit the requested foreground/game view.
- Review requested standing space, subjects/text, and landmark edges against the actual brief.
- For unwanted seams or mirrored artefacts in wide images, propose a supported scoped inpaint on the selected surface. Use `no reflections, no mirrored shapes` only when the scene does not require them. If Pro Flash was selected, its `context_image` and `bounding_box` requirements are in `pro-flash.md`.

## Backdrops, story pictures and maps

- **Hub or menu backdrop:** say where the empty space must be and keep UI and button areas calm. If separately clickable props require a clean plate, propose that additional output and its cost. A supported edit of the approved furnished room can request `the same room, empty, without <props>` while preserving its layout; use the selected route's actual image/reference fields.
- **Story picture:** one moment, one focal subject, foreground/midground/background, warm light against cold shadow.
- **Region map:** name the requested projection and readable paths; exclude labels/UI only when an unlabeled map is wanted.
- **Independently placeable buildings:** a shared panorama can merge their silhouettes. If separate sprites are required, plan an empty backdrop and individual building outputs; a requested city panorama remains one scene.
- **Dark scenes read as mud.** Add a named light that picks out the main shapes (`pale moonlight through a tall window, a few candles on the table, so the table, chairs and pillars read clearly`).
- **Unwanted fake letters on banners/signs:** for an unlabeled backdrop, offer blank cloth/signs; preserve requested writing and disclose failures to render it accurately.
- **Framed vignettes:** `straight-on front view of a room filling the whole frame edge to edge, no borders`.

## Buildings

- For independently placeable buildings use one building per call; candidate behavior/review follows `create-image-pro.md` and `reviewable-candidates.md`.
- Side-view projection drifts to isometric, even with PixFlux `view: "side"`: start with `front view pixel art, flat side elevation, not isometric, sitting on a flat ground line`.
- For an isolated building ask for transparent empty margins, excluding people/text only when absent from the brief. A cropped roof can be corrected with a supported edit naming a smaller fit and preserved design/ground position.
- Give it materials plus one signature feature (a forge glow, a sign shape without letters).
- **Requested upgrade tiers** can use the previous approved tier as the selected supported edit's source so the silhouette carries over: `grow this <tier N> into <tier N+1>: <changes>, same pixel art style and palette`. Independent text-only generations risk unrelated buildings; inspect continuity before using a tier as the next source.
- A hard-projection top-down or south-facing building follows `style-reference.md` instead.
