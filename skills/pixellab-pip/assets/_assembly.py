"""Shared by the local helpers: a UTF-8-safe console, the Pillow/numpy skip contract and frame-path expansion."""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path


for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def require_numpy(scipy: bool = False) -> None:
    """Print a skipped report and exit 3 when numpy or Pillow cannot be imported (never a pass)."""
    require_pillow()
    try:
        import numpy  # noqa: F401
        if scipy:
            import scipy.ndimage  # noqa: F401
    except (ImportError, OSError) as exc:
        print(json.dumps({"status": "skipped", "reason": f"needs numpy, Pillow{', scipy' if scipy else ''}: {exc}"}))
        sys.exit(3)


def load_pillow():
    """Return a patched stable PIL.Image, or raise without printing/decoding any input."""
    import PIL
    version = str(getattr(PIL, "__version__", "unknown"))
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:\.post\d+)?", version)
    if match is None or tuple(map(int, match.groups())) < (13, 0, 0):
        raise ImportError(f"Pillow 13.0.0+ stable is required for patched image decoding; installed {version}")
    from PIL import Image
    return Image


def require_pillow():
    """Return patched PIL.Image, or print an unavailable-verification skip and exit 3."""
    try:
        return load_pillow()
    except (ImportError, OSError) as exc:
        print(json.dumps({"status": "skipped", "reason": f"Pillow is unavailable: {exc}"}))
        sys.exit(3)


def open_still(path: str):
    """One RGBA image; an animated input would silently lose every frame after the first, so refuse it."""
    with require_pillow().open(path) as im:
        if getattr(im, "n_frames", 1) > 1:
            sys.exit("%s has %d frames; pass its frames as separate images" % (path, im.n_frames))
        return im.convert("RGBA")


def expand(paths: list[str]) -> list[str]:
    """Expand * and ? that cmd/PowerShell pass literally, in natural order (2.png before 10.png)."""
    out = []
    for path in paths:
        hits = glob.glob(path) if ("*" in path or "?" in path) else []
        out += sorted(hits, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]) or [path]
    return out


def preflight_outputs(outputs, inputs=()) -> None:
    """Reject collisions before any write, including symlink/hardlink aliases and duplicate names."""
    destinations = [Path(p) for p in outputs]
    sources = [Path(p) for p in inputs]
    seen = set()
    for dest in destinations:
        key = os.path.normcase(str(dest.resolve()))
        if key in seen:
            raise ValueError(f"duplicate output destination: {dest}")
        seen.add(key)
        for source in sources:
            same = key == os.path.normcase(str(source.resolve()))
            if not same and dest.exists() and source.exists():
                same = os.path.samefile(dest, source)
            if same:
                raise ValueError(f"refusing to overwrite input: {dest}")
        if dest.exists() or dest.is_symlink():
            raise ValueError(f"output already exists; choose a fresh destination: {dest}")
