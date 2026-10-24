"""Read project run history from its existing manifests; never guess old dates/costs.

    python history.py [--root pixellab-pip-generations] [--runs N] [--json]
                      [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--job ID] [--tool TEXT]

Date bounds include both UTC calendar dates and select recorded job creation times.
Unknown dates do not match a date query. Filters apply before the newest-N limit;
counts/costs describe matching calls. Historical manifests without dates remain
searchable by job/tool, with dates and unavailable costs labeled unknown.
Manifests that are not run ledgers (older Pip manifests or unreadable files) are listed
after the runs and never count toward --runs; their calls are not searched or totalled.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timezone
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest  # noqa: E402


def _date(value):
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo is not None else None
    except ValueError:
        return None


def history(root: str, runs: int, *, since: date | None = None, until: date | None = None,
            job: str | None = None, tool: str | None = None) -> list[dict]:
    if runs <= 0:
        raise ValueError("--runs must be positive")
    if since and until and since > until:
        raise ValueError("--since must be on or before --until")
    out, skipped = [], []
    for path in Path(root).glob("*/" + manifest.NAME):
        try:
            entries = manifest.jobs(str(path.parent))
        except (ValueError, OSError) as exc:
            skipped.append({"name": path.parent.name, "error": str(exc), "created_at": None})
            continue
        matches = []
        for entry in entries:
            dt = _date(entry.get("created_at"))
            if (job and entry["job_id"] != job) or (tool and tool.casefold() not in str(entry.get("tool", "")).casefold()):
                continue
            if (since or until) and (dt is None or (since and dt.date() < since) or (until and dt.date() > until)):
                continue
            matches.append(entry)
        if not matches and (job or tool or since or until):
            continue
        stamps = [_date(j.get("created_at")) for j in matches]
        latest = max((d for d in stamps if d is not None), default=None)
        totals = {}
        for key, estimate in (("spent", False), ("committed", True)):
            try:
                totals[key] = sum(manifest._usage(j, estimate=estimate) for j in matches)
            except ValueError:
                totals[key] = None
        out.append({"name": path.parent.name, "jobs": len(matches), **totals,
                    "created_at": latest.isoformat() if latest else None,
                    "unknown_dates": sum(d is None for d in stamps),
                    "outcomes": dict(Counter(j["outcome"] for j in matches if j.get("outcome"))),
                    "entries": [{k: j[k] for k in ("job_id", "tool", "status", "created_at", "outcome", "outputs") if k in j}
                                for j in matches]})
    runs_out = sorted(out, key=lambda r: (r["created_at"] or "", r["name"]), reverse=True)[:runs]
    return runs_out + sorted(skipped, key=lambda r: r["name"])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default="pixellab-pip-generations")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--since", type=date.fromisoformat)
    parser.add_argument("--until", type=date.fromisoformat)
    parser.add_argument("--job")
    parser.add_argument("--tool")
    args = parser.parse_args(argv)
    try:
        rows = history(args.root, args.runs, since=args.since, until=args.until, job=args.job, tool=args.tool)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(rows, indent=2))
    elif not rows:
        print("no matching runs with %s under %s" % (manifest.NAME, args.root))
    else:
        skipped = [row["name"] for row in rows if "error" in row]
        for row in rows:
            if "error" in row:
                continue
            cost = "unknown charged generations" if row["spent"] is None else "%g charged generations" % row["spent"]
            outcomes = ", ".join("%s %s" % (v, k) for k, v in sorted(row["outcomes"].items())) or "not judged"
            print("%s: %s jobs, %s, %s; date %s%s" %
                  (row["name"], row["jobs"], cost, outcomes, row["created_at"] or "unknown",
                   "; %s undated jobs" % row["unknown_dates"] if row["unknown_dates"] else ""))
        older = [r["name"] for r in rows if "jobs list" in r.get("error", "")]   # a manifest from before the ledger
        broken = [n for n in skipped if n not in older]
        for names, text in ((older, "are older Pip manifests, not run ledgers"),
                            (broken, "are unreadable run ledgers that need checking")):
            if names:
                print("%d manifests %s; their calls are not searched or counted: %s%s"
                      % (len(names), text, ", ".join(names[:5]), ", +%d more" % (len(names) - 5) if len(names) > 5 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
