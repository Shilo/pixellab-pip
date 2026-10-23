"""Named art styles for a project, kept in `pixellab.json` at the project root. Standard library only.

    python project_style.py show                      the active style as JSON; exit 4 {"status":"no_style"} when none
    python project_style.py list                      saved styles (active marked) and the example styles on offer
    python project_style.py save <name> --from <style.json> [--use]
    python project_style.py example "<example name>" [--as <name>] [--use]   copy an example style, only when picked
    python project_style.py use <name> | rename <old> <new> | delete <name>
    python project_style.py anchor <family> <image.png> [--style <name>]   approved reference art for an asset family
Options: --profile <path> (default ./pixellab.json).

A style is never assumed: with no saved, active style the project has none, and the agent asks the user
(references/project-style.md). Anchor paths are stored relative to the profile's folder.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

STYLE_KEYS = ("setting", "density", "look", "palette", "palette_hex", "colors", "outline", "shading", "dither",
              "light", "view", "facing", "sizes", "negatives", "rules", "anim", "anchors", "seed", "reference",
              "analysed_from", "notes")
FAMILIES = ("heroes", "monsters", "backgrounds", "scenes", "buildings", "icons", "ui")

# Starting points offered by name; written into a project only when the user picks one.
EXAMPLES = {
    "Side-view dark fantasy": {
        "setting": "dark-fantasy", "density": "high", "view": "side", "facing": {"heroes": "right", "foes": "left"},
        "look": "dark fantasy pixel art, muted colours, gritty, dark outline, light from above, detailed shading",
        "palette": "deep violet, ember orange, cold blue, worn steel", "outline": "dark", "shading": "detailed",
        "light": "top", "dither": False, "negatives": ["no modern objects", "no guns"],
        "sizes": {"hero": [96, 200]},
        "anim": {"canvas_overhead": [192, 256], "canvas_forward": [192, 200], "frames": 10,
                 "timing_ms": {"wind_up": 160, "frame": 60, "hit": 140, "settle": 120}},
        "notes": "the tested recipe: padded key-pose attacks for ~96x200 heroes (references/key-pose-animation.md)",
    },
    "Top-down cozy": {
        "setting": "cozy", "density": "low", "view": "top-down",
        "look": "cute cozy pixel art, chibi proportions, big head, rounded shapes, soft outline",
        "palette": "soft pastels, warm cream, sage green", "outline": "soft", "shading": "simple",
        "negatives": ["no blood", "no gore", "no realistic weapons"], "sizes": {"hero": [48, 48]},
        "notes": "a 48 canvas draws a ~24x32 figure; a walkable player: references/eight-direction.md (Walkable Top-Down Character)",
    },
    "Top-down 8-direction": {
        "setting": "rpg", "density": "mid", "view": "top-down 3/4", "anim": {"directions": 8},
        "look": "top-down 3/4 view pixel art, clear silhouettes readable from all eight directions",
        "outline": "dark", "shading": "simple", "sizes": {"hero": [64, 64]},
        "notes": "8 facings: references/eight-direction.md",
    },
    "Side-view sci-fi": {
        "setting": "scifi", "density": "high", "view": "side", "facing": {"heroes": "right", "foes": "left"},
        "look": "sci-fi pixel art, clean hard-surface shapes, glowing accents",
        "palette": "gunmetal, teal, cyan glow, warning orange", "outline": "dark", "shading": "detailed",
        "negatives": ["no wooden bows"], "sizes": {"hero": [96, 200]},
        "anim": {"canvas_overhead": [256, 256], "canvas_forward": [192, 200], "frames": 8,
                 "timing_ms": {"wind_up": 160, "frame": 60, "hit": 140, "settle": 120}},
        "notes": "sizes are canvases; a bulky armoured figure fills less of it (tested 2026-10-23: a 91x136 marine)",
    },
}


def load(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8-sig") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def save(path: str, prof: dict) -> None:
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".pixellab.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(prof, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def fail(message: str, code: int = 1) -> int:
    print(message, file=sys.stderr)
    return code


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=("show", "list", "save", "example", "use", "rename", "delete", "anchor"))
    ap.add_argument("args", nargs="*")
    ap.add_argument("--profile", default="pixellab.json")
    ap.add_argument("--from", dest="source")
    ap.add_argument("--use", action="store_true")
    ap.add_argument("--as", dest="as_name")
    ap.add_argument("--style")
    a = ap.parse_args(argv)
    prof = load(a.profile)
    styles = prof.get("styles") if isinstance(prof.get("styles"), dict) else {}
    active = prof.get("active_style") if prof.get("active_style") in styles else None

    if a.command == "show":
        if not active:
            print(json.dumps({"status": "no_style", "examples": list(EXAMPLES)}))
            return 4
        print(json.dumps({"name": active, "style": styles[active]}, indent=2, ensure_ascii=False))
        return 0
    if a.command == "list":
        for name in sorted(styles):
            print("%s %s" % ("*" if name == active else " ", name))
        print("examples (pick one, or describe your own): " + "; ".join(EXAMPLES))
        return 0

    def need(name: str) -> bool:
        return name in styles

    if a.command in ("save", "example"):
        if not a.args:
            return fail("give a name")
        if a.command == "save":
            if not a.source:
                return fail("save needs --from <style.json>")
            src = load(a.source)
            style = {k: src[k] for k in STYLE_KEYS if k in src}
            name = a.args[0]
        else:
            if a.args[0] not in EXAMPLES:
                return fail("no example named %r; examples: %s" % (a.args[0], "; ".join(EXAMPLES)))
            style = json.loads(json.dumps(EXAMPLES[a.args[0]]))
            name = a.as_name or a.args[0]
        if not style:
            return fail("nothing to save: no style fields found")
        styles[name] = style
        prof["styles"] = styles
        if a.use or not active:
            prof["active_style"] = name
        save(a.profile, prof)
        print("saved style %r%s" % (name, ", active" if prof.get("active_style") == name else ""))
        return 0
    if a.command == "use":
        if not a.args or not need(a.args[0]):
            return fail("no such style")
        prof["active_style"] = a.args[0]
        save(a.profile, prof)
        print("active style: %s" % a.args[0])
        return 0
    if a.command == "rename":
        if len(a.args) != 2 or not need(a.args[0]):
            return fail("usage: rename <old> <new> (the old style must exist)")
        old, new = a.args
        if new in styles:
            return fail("a style named %r already exists" % new)
        styles[new] = styles.pop(old)
        if prof.get("active_style") == old:
            prof["active_style"] = new
        save(a.profile, prof)
        print("renamed %s -> %s" % (old, new))
        return 0
    if a.command == "delete":
        if not a.args or not need(a.args[0]):
            return fail("no such style")
        del styles[a.args[0]]
        if prof.get("active_style") == a.args[0]:
            prof["active_style"] = None   # never fall back to another style silently
        save(a.profile, prof)
        print("deleted %s" % a.args[0])
        return 0
    # anchor
    if len(a.args) != 2 or a.args[0] not in FAMILIES:
        return fail("usage: anchor <%s> <image.png>" % "|".join(FAMILIES))
    family, image = a.args
    name = a.style or active
    if not name or not need(name):
        return fail("no active style: save or pick one first")
    if not os.path.isfile(image):
        return fail("no such image: " + image)
    rel = os.path.relpath(os.path.abspath(image), os.path.dirname(os.path.abspath(a.profile))).replace(os.sep, "/")
    styles[name].setdefault("anchors", {})[family] = rel
    save(a.profile, prof)
    print("anchor for %s in style %r: %s" % (family, name, rel))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
