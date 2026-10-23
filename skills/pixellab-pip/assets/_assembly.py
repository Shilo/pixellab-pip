"""Shared by the assembly helpers: the Pillow skip contract and frame-path expansion."""

from __future__ import annotations

import glob
import json
import re
import sys


def require_pillow():
    """Return PIL.Image, or print a skipped report and exit 3 (unavailable verification, never a pass)."""
    try:
        from PIL import Image
    except (ImportError, OSError):
        print(json.dumps({"status": "skipped", "reason": "Pillow is unavailable"}))
        sys.exit(3)
    return Image


def expand(paths: list[str]) -> list[str]:
    """Expand * and ? that cmd/PowerShell pass literally, in natural order (2.png before 10.png)."""
    out = []
    for path in paths:
        hits = glob.glob(path) if ("*" in path or "?" in path) else []
        out += sorted(hits, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]) or [path]
    return out
