"""Shared contract for the finishing helpers: numpy/scipy skip, frame lists, copy-only output, derivative label.

Every helper writes into its own `--out` folder, never over an input, and ends with `<out>/derivative.json`:
{"helper": name, "category": "cleanup" | "new_pixels", "inputs": [paths as given], "changes": {...}}; a re-run into
the same folder moves the earlier records to "previous".
"""
import glob
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):   # Windows consoles: never crash on non-ASCII text
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def require_numpy(scipy: bool = False) -> None:
    """Exit 3 with a JSON skip report when numpy (and scipy, if asked) cannot be imported."""
    try:
        import numpy  # noqa: F401
        if scipy:
            import scipy.ndimage  # noqa: F401
    except (ImportError, OSError):
        print(json.dumps({"status": "skipped", "reason": "numpy/scipy not installed"}))
        sys.exit(3)


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _assembly import expand  # noqa: E402,F401  (cmd/PowerShell pass *.png literally; natural order)


def _natural(s: str) -> list:
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def frames(d: str, names: list) -> list:
    """Frame names like 3 or 0* inside folder d (no .png); a plain * means the raw numbered frames only."""
    out = []
    for n in names:
        n = n[:-4] if n.endswith(".png") else n
        if "*" in n or "?" in n:
            hits = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(d, n + ".png"))]
            keep = [h for h in hits if h.isdigit() or n.endswith(("_s", "_t"))]
            out += sorted(keep, key=_natural) or [n]
        else:
            out.append(n)
    return out


class Run:
    """One helper run: the --out folder, the inputs it must never overwrite, and the changes it reports."""

    def __init__(self, helper: str, category: str, out: str, inputs: list):
        assert category in ("cleanup", "new_pixels")
        self.helper, self.category, self.out = helper, category, out
        self.inputs = [str(p) for p in inputs]
        self._guard = {os.path.normcase(os.path.realpath(p)) for p in self.inputs}
        self.changes: dict = {}
        os.makedirs(out, exist_ok=True)

    def path(self, name: str) -> str:
        p = os.path.join(self.out, name)
        if os.path.normcase(os.path.realpath(p)) in self._guard:
            sys.exit("refusing to overwrite the input %s: give another --out folder" % p)
        return p

    def save(self, img, name: str, **change) -> str:
        """Save a PIL image as <out>/<name>; keyword arguments go into changes.frames[name]."""
        p = self.path(name)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        img.save(p)
        self.changes.setdefault("frames", {})[name] = change
        return p

    def done(self, **extra) -> None:
        self.changes.update(extra)
        label = {"helper": self.helper, "category": self.category, "inputs": self.inputs, "changes": self.changes}
        dest = self.path("derivative.json")
        if os.path.exists(dest):   # a re-run into the same folder keeps the earlier records
            with open(dest, encoding="utf-8") as fh:
                old = json.load(fh)
            label["previous"] = old.pop("previous", []) + [old]
        with open(dest, "w", encoding="utf-8") as fh:
            json.dump(label, fh, indent=2)
        print("derivative ->", os.path.join(self.out, "derivative.json"))
