"""The run manifest: one record per run folder (`<run>/manifest.json`), per references/usage-reporting.md.

    python manifest.py spent <run_dir>...       {"spent": <charged generations of finished jobs>}
    python manifest.py committed <run_dir>...   {"committed": <spent + jobs submitted but not yet fetched>}: what a budget
                                             counts; give every run folder of one plan to get the plan's total
    python manifest.py add <run_dir> <job_id> --tool T --generations G     record a paid call right after submitting it
    python manifest.py done <run_dir> <job_id>                       a job saved without fetch.py (a character's rotations)
    python manifest.py outcome <run_dir> <job_id> <outcome> [note]   kept, rejected, redone... with an optional note

Helpers import add_job, set_outcome, jobs and spent. Standard library only.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

NAME = "manifest.json"


def _read(run_dir: str) -> dict[str, Any]:
    path = Path(run_dir) / NAME
    if not path.exists():
        return {"jobs": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) and isinstance(data.get("jobs"), list) else {"jobs": []}


def _write(run_dir: str, data: dict[str, Any]) -> None:
    folder = Path(run_dir)
    folder.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=folder, prefix=".manifest.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        os.replace(tmp, folder / NAME)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def jobs(run_dir: str) -> list[dict[str, Any]]:
    return _read(run_dir)["jobs"]


def add_job(run_dir: str, entry: dict[str, Any]) -> None:
    """Record one PixelLab call; the same job_id again updates its entry (a re-fetch never counts twice and keeps
    what the first record knew, such as the reported usage)."""
    data = _read(run_dir)
    old = next((j for j in data["jobs"] if j.get("job_id") == entry.get("job_id")), {})
    data["jobs"] = [j for j in data["jobs"] if j.get("job_id") != entry.get("job_id")] + [{**old, **entry}]
    _write(run_dir, data)


def set_outcome(run_dir: str, job_id: str, outcome: str, note: str = "") -> None:
    data = _read(run_dir)
    for j in data["jobs"]:
        if j.get("job_id") == job_id:
            j["outcome"] = outcome
            if note:
                j["outcome_note"] = note
    _write(run_dir, data)


def _usage(job: dict[str, Any]) -> float:
    return float((job.get("reported_usage") or {}).get("generations") or 0)


def spent(run_dir: str) -> float:
    """Charged generations of the jobs that finished (a failed job is refunded)."""
    return sum(_usage(j) for j in jobs(run_dir) if j.get("status", "ok") == "ok")


def committed(run_dir: str) -> float:
    """What a budget counts: finished jobs plus jobs submitted but not yet fetched (an interrupted session's)."""
    return sum(_usage(j) for j in jobs(run_dir) if j.get("status", "ok") in ("ok", "submitted"))


def main(argv: list[str]) -> int:
    cmd, args = (argv[0], argv[1:]) if argv else ("", [])
    sizes = {"add": range(2, 7), "done": [2], "outcome": [3, 4], "spent": range(1, 99), "committed": range(1, 99)}
    if len(args) not in sizes.get(cmd, []):
        print(__doc__, file=sys.stderr)
        return 2
    runs = args if cmd in ("spent", "committed") else args[:1]
    missing = [d for d in runs if not (Path(d) / NAME).exists()]
    if cmd != "add" and missing:   # a mistyped run folder must never count as 0 spent
        print("no %s in %s" % (NAME, ", ".join(missing)), file=sys.stderr)
        return 2
    if cmd in ("spent", "committed"):
        out: dict[str, Any] = {cmd: sum((spent if cmd == "spent" else committed)(d) for d in args)}
    elif cmd == "add":
        opts = dict(zip(args[2::2], args[3::2]))
        entry: dict[str, Any] = {"job_id": args[1], "tool": opts.get("--tool", ""), "status": "submitted"}
        if "--generations" in opts:
            entry["reported_usage"] = {"generations": float(opts["--generations"])}
        add_job(args[0], entry)
        out = {"recorded": args[1]}
    elif cmd == "done":
        add_job(args[0], {"job_id": args[1], "status": "ok"})
        out = {"done": args[1]}
    else:
        if not any(j.get("job_id") == args[1] for j in jobs(args[0])):
            print("no job %s in %s" % (args[1], args[0]), file=sys.stderr)
            return 2
        set_outcome(args[0], args[1], args[2], args[3] if len(args) == 4 else "")
        out = {"outcome": args[2]}
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
