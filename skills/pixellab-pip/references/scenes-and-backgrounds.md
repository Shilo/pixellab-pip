# Scenes, Backgrounds and Buildings

Read this for a battle/level background, hub/menu backdrop, story picture, region map, furnished room with a floor plan, or building with upgrade tiers. The Intent Router selects the surface/model; this page supplies composition decisions. Apply saved appearance only under `project-style.md`.

## Furnished rooms

Use MCP `create_room` for a room asset with planned floor cells and doorways. It requires Tier 2 (Pixel Artisan) or higher and has no public REST v2 counterpart. A normal room backdrop remains an image request. Room tools choose their own transparency: rock outside the walls is transparent, so the image-route `no_background` settings below do not apply. Use `list_rooms` only when the user asks to find or choose an existing room; it lists rooms newest first, and `get_room` returns the selected room's image, door anchors, and walkable rectangles.

- Supply a concise `theme` and 1–8 `doors`: each has `side` (`n`, `e`, `s`, `w`), `col` 0–6 and `row` 0–5. Doors must lie on the floor boundary. East/west doors are two cells tall (`row` is the upper cell) and need two wall cells before an inner corner below them.
- Optional `cells` is six strings of seven characters: `#` floor, `.` solid rock, with one connected floor region. Omit for the full 7×6 floor. Each floor cell is 32px; top-down output is 256×256. Confirm door positions against the actual plan.
- `view` defaults to `top-down`. `isometric` uses the same plan in 2:1 projection, about 248×176 for a full room; north/west walls are tall and south/east walls are low curbs. `oblique` uses a tilted square floor grid, the same wall-height layout, and is about 272×240 for a full room; it draws only walls, doors, and floor, so `pieces` must be false.
- `style_room_id` can reuse the walls, wall tops, doors, lights/hangings and, by default, floor from a completed room in the same view. The new room keeps its own shape and furniture; `style_room_floor=false` lets its theme choose a different floor. For an existing room, use the id returned by `list_rooms`/`get_room`, not a guessed id.
- A completed painted room costs 20 generations (documented estimate ~4 minutes; about 1 in 10 takes over 8); movable furniture pieces cost another 10 and ~5–8 minutes. Leave `pieces=false` unless movable furniture is requested. Pieces can be requested at creation or later with `cut_out_room_furniture(room_id=...)`; do not request both for the same work.
- Optional `project_id` files the finished room in the selected project; if omitted, PixelLab uses the account's auto-add setting. Pass a project only when the user requested that context.
- Poll `get_room(room_id=...)` through completion. It returns progress, painted art/downloads and, after extraction, named movable pieces and a website room-editor link. Verify requested floor shape, doors, view and output stage; a painted room does not prove cutouts are ready. Use the returned links rather than constructing room/map endpoints or promising automated map placement of room pieces.

## Shared settings

- `no_background: false` for every scene and background; `true` for a building sprite.
- Match a set using the selected route's supported style/reference fields (`style-reference.md`); distinguish appearance from layout references. For Pro sizes/candidate bands see `create-image-pro.md` rather than assuming every canvas is supported.
- For an approved PixFlux pass matching a set's palette, use its approved palette image in `color_image_url` (or `color_image_base64` for a local image). A Pro output can supply that palette when Pro was already selected; creating one is not required.
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
