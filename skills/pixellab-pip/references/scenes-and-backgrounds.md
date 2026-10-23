# Scenes, Backgrounds and Buildings

Read this for a battle or level background, a hub or menu backdrop, a story or cutscene picture, a region map, or a single building sprite with upgrade tiers. The Intent Router picks PixFlux for subject-less backdrops and Pro for full scenes; this page adds the composition decisions. Look words, palette and the anchor image come from the project style (`project-style.md`, examples in `style-examples.md`).

## Shared settings

- `no_background: false` for every scene and background; `true` for a building sprite.
- Match an existing set with MCP `create_image_pro` + `style_image_url` = the approved anchor and `style_copy: ["outline", "detail", "shading"]`; add `reference_images` with usage `scene layout, colors and lighting only` when a layout should carry over. Pro canvases are aspect-gated (512x512 square, 688x384 at 16:9).
- A cheap pass with `create_image_pixflux` keeps the set's palette when `color_image_url` = the matching Pro image.
- Several regions or screens: one call each, the same anchor and seed, and one shared palette sentence, so they read as one place.
- Always negate what creeps in: `no characters, no people, no text, no letters, no numbers, no UI, no frame` (`no labels` for maps).

## Battle and level backgrounds

- Fighters need somewhere to stand: `open flat <ground type> along the bottom third for fighters` naming the ground (street, marble floor, cave floor, stone ledge). Without it they stand on clutter; put clutter in the middle and back.
- 2-4 landmarks and one light story (moonlight, torches, a glowing portal). Keep the palette muted so sprites read on top and the horizon low enough that the ground band stays open.
- Review: ground clear, no figures or text, the canvas edge does not cut a landmark.
- Seams and mirrored artefacts in wide images: prompt `no reflections, no mirrored shapes`; repair a region with MCP `inpaint_image_pro_flash` plus `context_image` (the whole scene) and `bounding_box`, as a paid, approved call.

## Backdrops, story pictures and maps

- **Hub or menu backdrop:** say where the empty space must be and keep UI and button areas calm. For a room with clickable props, generate the furnished room, then edit it (MCP `edit_image`; Pro Flash edits stop at 256 px) to `the same room, empty, without <props>` (or pass the full scene as a `reference_images` entry and ask for `the same scene with every <thing> removed`) to get the clean plate.
- **Story picture:** one moment, one focal subject, foreground/midground/background, warm light against cold shadow.
- **Region map:** `top-down overhead view ... seen directly from above like a game world map`, readable paths, `no text, no labels, no UI`.
- **Several buildings in one panorama merge** however the prompt numbers them. Generate an empty backdrop and each building as its own sprite instead.
- **Dark scenes read as mud.** Add a named light that picks out the main shapes (`pale moonlight through a tall window, a few candles on the table, so the table, chairs and pillars read clearly`).
- **Banners and signs carry fake letters.** Drop them from the prompt (`no banners or flags, no signs with writing`); for a leftover sign, inpaint `blank cloth with no numbers, no letters, no symbols`.
- **Framed vignettes:** `straight-on front view of a room filling the whole frame edge to edge, no borders`.

## Buildings

- One building per call. MCP `create_image_pro` at ≤170 px returns several candidates; pick per `reviewable-candidates.md`.
- Side-view projection drifts to isometric, even with PixFlux `view: "side"`: start with `front view pixel art, flat side elevation, not isometric, sitting on a flat ground line`.
- Isolated means isolated: `single building, nothing behind it, no people, no text`, plus `the whole building fully visible and centred with empty margin on all sides`. A cropped roof: edit `draw this same building a little smaller so it fits with a small transparent margin; keep design, colours and bottom position`.
- Give it materials plus one signature feature (a forge glow, a sign shape without letters).
- **Upgrade tiers** come from the previous tier so the silhouette carries over: MCP `edit_image_pro_flash` on tier N with `grow this <tier N> into <tier N+1>: <changes>, same pixel art style and palette`. Regenerating each tier from text makes unrelated buildings.
- A hard-projection top-down or south-facing building follows `style-reference.md` instead.
