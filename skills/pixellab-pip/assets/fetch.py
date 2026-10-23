"""Wait for a PixelLab MCP image or animation job, download it into the run folder and record it in the manifest.

    python fetch.py <job_id> <out.png> --run <run_dir> [--tool T] [--generations G]
    python fetch.py <job_id> <out_dir> --frames N --run <run_dir> ...      an animation: <out_dir>/0.png ..
    python fetch.py --url <PixelLab file link> <out>      a link a tool returned (rotations, effect exports)

--frames: frames to fetch (frame_count + 1 for animate_image); a clip with fewer is saved as it is.
--generations: the call's usage as PixelLab reported it at submit (Pro Flash's estimated_generations counts), recorded as
reported_usage.generations.
--timeout S (default 100, under a shell tool's usual limit); it polls every 15 s.
Exit 0 downloaded; 2 failed (PixelLab refunds it); 3 still running: run the same command again.
A 404 in the first 60 s means "not registered yet"; after that, and a 410 at any time, the job failed.
Network calls go only to PixelLab's download and file hosts; the job id or link is the key, no token is sent. Stdlib only.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest  # noqa: E402

BASE = "https://api.pixellab.ai/mcp/images/%s/download"
HOSTS = {"api.pixellab.ai", "backblaze.pixellab.ai"}
UA = "pixellab-pip-fetch/1 (+https://github.com/Shilo/pixellab-pip)"   # the file host refuses Python's default (403)
GRACE_404 = 60


def check_host(url: str) -> None:
    parts = urllib.parse.urlparse(url)
    if parts.scheme != "https" or parts.hostname not in HOSTS:
        raise ValueError("not an https PixelLab host: " + url)


class PixelLabOnly(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only to another allow-listed PixelLab https host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_host(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _download(url: str) -> bytes:
    check_host(url)
    with OPENER.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as response:
        return response.read()


OPENER = urllib.request.build_opener(PixelLabOnly)


def get(job: str, index: int | None = None) -> tuple[str, bytes | None]:
    """('ok', bytes) | ('wait', None) | ('notfound', None) on a 404 | ('failed', None) on a 410."""
    url = BASE % urllib.parse.quote(job, safe="") + ("?index=%d" % index if index is not None else "")
    try:
        data = _download(url)
    except urllib.error.HTTPError as exc:
        return ("notfound", None) if exc.code == 404 else ("failed", None) if exc.code == 410 else ("wait", None)
    except OSError:
        return "wait", None
    return ("ok", data) if data[:4] == b"\x89PNG" or data[:3] == b"GIF" else ("wait", None)


def settle(status: str, elapsed: float) -> str:
    if status == "notfound":
        return "wait" if elapsed < GRACE_404 else "failed"
    return status


def try_job(job: str, out: str, frames: int) -> str:
    """Writes the file(s) when the job is done; returns ok, wait, notfound or failed."""
    if not frames:
        status, data = get(job)
        if status == "ok":
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            Path(out).write_bytes(data)
        return status
    got: list[bytes] = []
    for index in range(frames):
        status, data = get(job, index)
        if status == "notfound" and got:   # a shorter clip than asked for: keep what it has
            break
        if status != "ok":
            return status
        got.append(data)
    Path(out).mkdir(parents=True, exist_ok=True)
    for index, data in enumerate(got):
        (Path(out) / ("%d.png" % index)).write_bytes(data)
    return "ok"


def outputs(out: str, run: str) -> list[str]:
    paths = sorted(Path(out).glob("*.png"), key=lambda p: int(p.stem) if p.stem.isdigit() else 0) if Path(out).is_dir() else [Path(out)]
    return [os.path.relpath(p, run).replace(os.sep, "/") for p in paths]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--url"] and len(argv) == 3:
        check_host(argv[1])
        if Path(argv[2]).exists():   # raw PixelLab outputs are never written over
            print("refusing to overwrite " + argv[2], file=sys.stderr)
            return 2
        try:
            data = _download(argv[1])
        except (urllib.error.URLError, OSError) as exc:
            print("download failed: %s" % exc, file=sys.stderr)
            return 2
        Path(argv[2]).parent.mkdir(parents=True, exist_ok=True)
        Path(argv[2]).write_bytes(data)
        print(argv[2])
        return 0
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job")
    ap.add_argument("out")
    ap.add_argument("--run", required=True)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--tool", default="")
    ap.add_argument("--generations", type=float)
    ap.add_argument("--timeout", type=int, default=100)
    a = ap.parse_args(argv)
    started = time.time()
    while True:
        status = settle(try_job(a.job, a.out, a.frames), time.time() - started)
        if status in ("ok", "failed") or time.time() - started >= a.timeout:
            break
        time.sleep(max(0, min(15, a.timeout - (time.time() - started))))
    if status not in ("ok", "failed"):
        print("TIMEOUT %s - still running at PixelLab; run the same command again" % a.job)
        return 3
    entry = {"job_id": a.job, "tool": a.tool, "status": status, "waited_s": round(time.time() - started)}
    if status == "ok":
        entry["outputs"] = outputs(a.out, a.run)
        if a.generations is not None:
            entry["reported_usage"] = {"generations": a.generations}
    manifest.add_job(a.run, entry)
    print(("OK %s %s" % (a.job, a.out)) if status == "ok" else ("FAILED %s (refunded; resubmit)" % a.job))
    return 0 if status == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
