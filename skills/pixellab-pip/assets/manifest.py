"""Private run ledger: exact charges and conservative reservations are separate.

    python manifest.py add RUN JOB --tool T [--generations ACTUAL] [--estimate RESERVED]
    python manifest.py done RUN JOB
    python manifest.py outcome RUN JOB OUTCOME [NOTE]
    python manifest.py spent RUN...       exact reported charges; unknown exits 2
    python manifest.py committed RUN...   actual charge, otherwise estimate; unknown exits 2

Failure is not evidence of a refund. Record a provider-confirmed zero charge as
reported_usage.generations = 0. No balance or credential values belong here.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time
from typing import Any

NAME = "manifest.json"
LOCK_TIMEOUT = 5.0


def number(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValueError("usage must be a finite nonnegative number, not a boolean")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("usage is outside the supported numeric range") from exc
    if not math.isfinite(result):
        raise ValueError("usage must be finite")
    return result


def _validate(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        raise ValueError("invalid manifest: expected an object with a jobs list; existing data left unchanged")
    seen = set()
    for entry in data["jobs"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("job_id"), str) or not entry["job_id"]:
            raise ValueError("invalid manifest job_id")
        if entry["job_id"] in seen:
            raise ValueError("duplicate manifest job_id: " + entry["job_id"])
        seen.add(entry["job_id"])
        for key in ("tool", "status", "outcome", "outcome_note", "created_at"):
            if key in entry and not isinstance(entry[key], str):
                raise ValueError("invalid manifest " + key)
        if "waited_s" in entry:
            number(entry["waited_s"])
        for key in ("reported_usage", "estimated_usage"):
            usage = entry.get(key)
            if usage is not None:
                if not isinstance(usage, dict):
                    raise ValueError("invalid " + key)
                for unit in ("generations", "usd"):
                    if unit in usage:
                        number(usage[unit])
        if "outputs" in entry and (not isinstance(entry["outputs"], list)
                                   or any(not isinstance(p, str) for p in entry["outputs"])):
            raise ValueError("invalid manifest outputs")
    return data


def _read(run_dir: str, *, missing_ok: bool = False) -> dict[str, Any]:
    path = Path(run_dir) / NAME
    if not path.exists() and missing_ok:
        return {"jobs": []}
    if not path.exists():
        raise ValueError("no manifest.json in " + str(run_dir))
    return _validate(json.loads(path.read_text(encoding="utf-8-sig")))


def _write(run_dir: str, data: dict[str, Any]) -> None:
    _validate(data)
    fd, tmp = tempfile.mkstemp(dir=run_dir, prefix=".manifest.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, allow_nan=False)
            handle.write("\n")
        os.replace(tmp, Path(run_dir) / NAME)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def _transaction(run_dir: str):
    """Protect the whole mutation. Never steal a possibly live/stale lock."""
    Path(run_dir).mkdir(parents=True, exist_ok=True)
    lock = Path(run_dir) / ".manifest.lock"
    deadline = time.monotonic() + LOCK_TIMEOUT
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            break
        except (FileExistsError, PermissionError) as exc:
            # Windows can deny exclusive creation briefly while another process releases the lock.
            # A persistent access problem must also fail closed; never remove a lock we do not own.
            if time.monotonic() >= deadline:
                raise ValueError("cannot acquire manifest lock; check directory permissions and verify no writer "
                                 "is running before manually removing an existing " + str(lock)) from exc
            time.sleep(0.05)
    try:
        yield
    finally:
        lock.unlink()


def jobs(run_dir: str) -> list[dict[str, Any]]:
    return _read(run_dir)["jobs"]


def add_job(run_dir: str, entry: dict[str, Any]) -> None:
    """Merge one call under the transaction lock; never double-count a job ID."""
    _validate({"jobs": [entry]})
    with _transaction(run_dir):
        data = _read(run_dir, missing_ok=True)
        old = next((j for j in data["jobs"] if j["job_id"] == entry["job_id"]), None)
        merged = {**(old or {}), **entry}
        if old is not None:
            if entry.get("status") == "submitted" and old.get("status"):
                merged["status"] = old["status"]
            if "outputs" in entry:
                merged["outputs"] = list(dict.fromkeys(old.get("outputs", []) + entry["outputs"]))
        for key in ("reported_usage", "estimated_usage"):
            if isinstance((old or {}).get(key), dict) and isinstance(entry.get(key), dict):
                merged[key] = {**old[key], **entry[key]}
        if old is None:
            merged.setdefault("created_at", datetime.now(timezone.utc).isoformat())
            data["jobs"].append(merged)
        else:
            data["jobs"][data["jobs"].index(old)] = merged
        _write(run_dir, data)


def _update_existing(run_dir: str, job_id: str, updates: dict[str, Any]) -> None:
    if not (Path(run_dir) / NAME).exists():
        raise ValueError("no manifest.json in " + str(run_dir))
    with _transaction(run_dir):
        data = _read(run_dir)
        entry = next((j for j in data["jobs"] if j["job_id"] == job_id), None)
        if entry is None:
            raise ValueError("no job " + job_id)
        entry.update(updates)
        _write(run_dir, data)


def set_outcome(run_dir: str, job_id: str, outcome: str, note: str = "") -> None:
    _update_existing(run_dir, job_id, {"outcome": outcome, **({"outcome_note": note} if note else {})})


def _usage(job: dict[str, Any], *, estimate: bool = False) -> float:
    for key in (("reported_usage", "estimated_usage") if estimate else ("reported_usage",)):
        usage = job.get(key)
        if isinstance(usage, dict) and "generations" in usage:
            return number(usage["generations"])
    raise ValueError("unknown generations for job " + job["job_id"])


def spent(run_dir: str) -> float:
    """Exact reported charges across every status; unknown is never zero."""
    return sum(_usage(j) for j in jobs(run_dir))


def committed(run_dir: str) -> float:
    """Actual charges, otherwise reserved estimates, including failed/uncertain jobs."""
    return sum(_usage(j, estimate=True) for j in jobs(run_dir))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("run")
    add.add_argument("job")
    add.add_argument("--tool", default="")
    add.add_argument("--generations", type=float, help="exact charge reported by PixelLab")
    add.add_argument("--estimate", type=float, help="conservative reservation, never a reported charge")
    for command in ("spent", "committed"):
        commands.add_parser(command).add_argument("runs", nargs="+")
    done = commands.add_parser("done")
    done.add_argument("run")
    done.add_argument("job")
    outcome = commands.add_parser("outcome")
    outcome.add_argument("run")
    outcome.add_argument("job")
    outcome.add_argument("outcome")
    outcome.add_argument("note", nargs="?", default="")
    args = parser.parse_args(argv)
    try:
        if args.command in ("spent", "committed"):
            fn = spent if args.command == "spent" else committed
            out = {args.command: sum(fn(run) for run in dict.fromkeys(args.runs))}
        elif args.command == "add":
            entry = {"job_id": args.job, "tool": args.tool, "status": "submitted"}
            for field, value in (("reported_usage", args.generations), ("estimated_usage", args.estimate)):
                if value is not None:
                    entry[field] = {"generations": number(value)}
            add_job(args.run, entry)
            out = {"recorded": args.job}
        elif args.command == "done":
            _update_existing(args.run, args.job, {"status": "ok"})
            out = {"done": args.job}
        else:
            set_outcome(args.run, args.job, args.outcome, args.note)
            out = {"outcome": args.outcome}
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
