"""Past runs from their manifests (references/usage-reporting.md): name, jobs, spent generations, outcomes.

    python history.py [--root pixellab-pip-generations] [--runs N] [--json]

Newest run first. A folder without manifest.json is not a run. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest  # noqa: E402


def history(root: str, runs: int) -> list[dict]:
    found = sorted(Path(root).glob("*/" + manifest.NAME), key=lambda p: p.stat().st_mtime, reverse=True)
    out = []
    for path in found[:runs]:
        jobs = manifest.jobs(str(path.parent))
        out.append({"name": path.parent.name, "jobs": len(jobs), "spent": manifest.spent(str(path.parent)),
                    "outcomes": dict(Counter(j["outcome"] for j in jobs if j.get("outcome")))})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default="pixellab-pip-generations")
    parser.add_argument("--runs", type=int, default=10, help="newest N runs (default 10)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows = history(args.root, args.runs)
    if args.json:
        print(json.dumps(rows, indent=2))
    elif not rows:
        print(f"no runs with {manifest.NAME} under {args.root}")
    for r in [] if args.json else rows:
        outcomes = ", ".join(f"{k} {v}" for k, v in sorted(r["outcomes"].items())) or "not judged"
        print(f"{r['name']}: {r['jobs']} jobs, {r['spent']:g} generations, {outcomes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
