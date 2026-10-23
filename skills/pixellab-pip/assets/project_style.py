"""Named art styles for a project, kept in `pixellab.json` at the project root. Standard library only.

    python project_style.py show [--style NAME | --no-style]   effective appearance and unresolved legacy limits
    python project_style.py list                      saved styles (active marked) and the example styles on offer
    python project_style.py save <name> --from <style.json> [--use] [--replace]
    python project_style.py example "<example name>" [--as <name>] [--use]   copy an example style, only when picked
    python project_style.py use <name> | rename <old> <new> | delete <name>
    python project_style.py anchor <family> <image.png> [--style <name>]   approved reference art for an asset family
Options: --profile <path> (default ./pixellab.json).

No profile means an ordinary one-off request, not required setup. Temporary selection never writes.
Appearance maps merge recursively; lists/scalars/null replace. Legacy limits remain restrictions
requiring reconciliation before spending. Anchor paths are relative to the profile's folder.
"""
from __future__ import annotations

import argparse
import json
import math
import copy
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
    if not isinstance(data, dict):
        raise ValueError("profile/style JSON must be an object")
    return data


MAP_KEYS = {"sizes", "facing", "anim", "anchors"}
LIMIT_KEYS = ("max_cost", "ask_above")


def validate_style(style: dict) -> None:
    if not isinstance(style, dict):
        raise ValueError("each style must be an object")
    for key in MAP_KEYS:
        if key in style and style[key] is not None and not isinstance(style[key], dict):
            raise ValueError(key + " must be an object or null")
        if isinstance(style.get(key), dict) and any(not isinstance(k, str) or not k for k in style[key]):
            raise ValueError(key + " keys must be nonempty strings")
    def positive_number(value):
        return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value) and value > 0
    for size in (style.get("sizes") or {}).values():
        if size is not None and not (isinstance(size, list) and len(size) == 2 and all(isinstance(v, int) and positive_number(v) for v in size)):
            raise ValueError("sizes entries must be [width, height] positive integers or null")
    anchors = style.get("anchors") or {}
    for family, image in anchors.items():
        if family not in FAMILIES or not (image is None or isinstance(image, str) and image.strip()):
            raise ValueError("anchors need a known family and a nonempty image path or null")
    value = (style.get("anim") or {}).get("timing_ms")
    if value is not None and not isinstance(value, dict):
        raise ValueError("anim.timing_ms must be an object or null")
    if isinstance(value, dict) and any(v is not None and not positive_number(v) for v in value.values()):
        raise ValueError("animation durations must be positive numbers or null")
    for key in ("frames", "directions"):
        value = (style.get("anim") or {}).get(key)
        if value is not None and not (isinstance(value, int) and positive_number(value)):
            raise ValueError("anim." + key + " must be a positive integer or null")
    reference = style.get("reference")
    if reference is not None and not (isinstance(reference, str) and reference.strip()):
        raise ValueError("reference must be a nonempty local image path or null")


def validate_profile(prof: dict) -> dict:
    validate_style(prof)
    styles = prof.get("styles", {})
    if not isinstance(styles, dict) or any(not isinstance(n, str) or not n.strip() for n in styles):
        raise ValueError("styles must be an object with nonempty names")
    for style in styles.values():
        validate_style(style)
    active = prof.get("active_style")
    if active is not None and (not isinstance(active, str) or active not in styles):
        raise ValueError("active_style does not name a saved style; select a valid style explicitly")
    for key in LIMIT_KEYS:
        value = prof.get(key)
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))
                                  or not math.isfinite(value) or value < 0):
            raise ValueError(key + " is an unresolved invalid legacy limit; reconcile before spending")
    return styles


def overlay(base: dict, override: dict) -> dict:
    """Appearance maps inherit by key; arrays, scalars and null replace."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = overlay(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def check_image(path: str, *, require_decode: bool = False) -> bool:
    """Validate local anchor art; ordinary profile reads need no image dependency."""
    if not os.path.isfile(path):
        raise ValueError("missing anchor image: " + path)
    try:
        from PIL import Image
    except ImportError:
        if require_decode:
            raise ValueError("Pillow is needed to verify a new anchor; use an equivalent host image check instead")
        return False
    try:
        with Image.open(path) as image:
            image.verify()
    except (OSError, ValueError) as exc:
        raise ValueError("unreadable anchor image: " + path) from exc
    return True


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
    selection = ap.add_mutually_exclusive_group()
    selection.add_argument("--style")
    selection.add_argument("--no-style", action="store_true")
    ap.add_argument("--replace", action="store_true", help="explicitly replace an existing saved style/anchor")
    a = ap.parse_args(argv)
    prof = load(a.profile)
    styles = validate_profile(prof)
    active = prof.get("active_style")
    if a.style is not None and a.style not in styles:
        return fail("no such style: " + a.style)
    if a.no_style and a.command != "show" or a.style is not None and a.command not in ("show", "anchor"):
        return fail("temporary selection is only for show or anchor; use changes the active style")

    if a.command == "show":
        if a.args:
            return fail("usage: show [--style NAME | --no-style]")
        selected = a.style if a.style is not None else active
        style = {} if a.no_style else {k: prof[k] for k in STYLE_KEYS if k in prof}
        if selected and not a.no_style:
            style = overlay(style, {k: v for k, v in styles[selected].items() if k in STYLE_KEYS})
        result = {"name": None if a.no_style else selected, "style": style,
                  "legacy_limits": {k: prof[k] for k in LIMIT_KEYS if k in prof}}
        folder = os.path.dirname(os.path.abspath(a.profile))
        unverified = []
        invalid = {}
        for family, image in (style.get("anchors") or {}).items():
            if image is not None:
                try:
                    if not check_image(os.path.join(folder, image)):
                        unverified.append(family)
                except ValueError as exc:
                    invalid[family] = str(exc)
        if style.get("reference") is not None and not check_image(os.path.join(folder, style["reference"])):
            unverified.append("reference")
        if unverified:
            result["unverified_anchors"] = unverified
        if invalid:
            result["invalid_anchors"] = invalid
        if not style:
            result["status"] = "no_style"
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 4
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if a.command == "list":
        for name in sorted(styles):
            print("%s %s" % ("*" if name == active else " ", name))
        print("examples (pick one, or describe your own): " + "; ".join(EXAMPLES))
        return 0

    def need(name: str) -> bool:
        return name in styles

    if a.command in ("save", "example"):
        if len(a.args) != 1 or not a.args[0].strip():
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
        validate_style(style)
        if name in styles and not a.replace:
            return fail("style already exists; replacement needs --replace")
        # Paths in a source style file are relative to that file, not the caller's cwd.
        if a.command == "save":
            for key in ("anchors",):
                for family, image in (style.get(key) or {}).items():
                    if image is not None:
                        source_path = os.path.join(os.path.dirname(os.path.abspath(a.source)), image)
                        check_image(source_path, require_decode=True)
                        style[key][family] = os.path.relpath(source_path, os.path.dirname(os.path.abspath(a.profile))).replace(os.sep, "/")
            if style.get("reference") is not None:
                source_path = os.path.join(os.path.dirname(os.path.abspath(a.source)), style["reference"])
                check_image(source_path, require_decode=True)
                style["reference"] = os.path.relpath(source_path, os.path.dirname(os.path.abspath(a.profile))).replace(os.sep, "/")
        styles[name] = style
        prof["styles"] = styles
        if a.use:
            prof["active_style"] = name
        save(a.profile, prof)
        print("saved style %r%s" % (name, ", active" if prof.get("active_style") == name else ""))
        return 0
    if a.command == "use":
        if len(a.args) != 1 or not need(a.args[0]):
            return fail("no such style")
        prof["active_style"] = a.args[0]
        save(a.profile, prof)
        print("active style: %s" % a.args[0])
        return 0
    if a.command == "rename":
        if len(a.args) != 2 or not need(a.args[0]) or not a.args[1].strip():
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
        if len(a.args) != 1 or not need(a.args[0]):
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
    check_image(image, require_decode=True)
    if family in (styles[name].get("anchors") or {}) and not a.replace:
        return fail("anchor already exists; replacement needs --replace")
    rel = os.path.relpath(os.path.abspath(image), os.path.dirname(os.path.abspath(a.profile))).replace(os.sep, "/")
    if styles[name].get("anchors") is None:
        styles[name]["anchors"] = {}
    styles[name].setdefault("anchors", {})[family] = rel
    save(a.profile, prof)
    print("anchor for %s in style %r: %s" % (family, name, rel))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError) as exc:
        raise SystemExit(fail(str(exc)))
