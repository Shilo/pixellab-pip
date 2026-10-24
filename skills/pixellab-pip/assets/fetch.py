"""Bounded download of an MCP raw-image job, with validated, preserved raw files.

    python fetch.py JOB out.png --run RUN --url LINK [--tool T] [--generations ACTUAL] [--estimate RESERVED]
    python fetch.py JOB out_dir --run RUN --url LINK0 --url LINK1 ...
    python fetch.py --url RETURNED_PIXELLAB_URL out.png

Pass exactly the download links the job's getter (e.g. `get_image`) returned, in order;
two or more links save 0.png onward into the new out_dir (the finishing helpers' frame names).
Existing destinations are refused. Exit 0: downloaded; 2: blocked/invalid/unavailable
(check the matching getter); 3: download not ready or dependency unavailable. HTTP
file errors establish neither job failure nor refund. Never resubmit from this result.
"""
from __future__ import annotations

import argparse
import contextlib
from http.client import HTTPException
import io
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import warnings

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _assembly import require_pillow  # noqa: E402
import manifest  # noqa: E402

HOSTS = {"api.pixellab.ai", "backblaze.pixellab.ai"}
UA = "pixellab-pip-fetch/1 (+https://github.com/Shilo/pixellab-pip)"
MAX_BYTES = 32 * 1024 * 1024


def check_host(url: str) -> None:
    parts = urllib.parse.urlparse(url)
    if parts.scheme != "https" or parts.hostname not in HOSTS or parts.username or parts.password:
        raise ValueError("requires an HTTPS PixelLab file URL without embedded credentials")


class PixelLabOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_host(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = urllib.request.build_opener(PixelLabOnly)


def _download(url: str, *, timeout: float = 30) -> bytes:
    check_host(url)
    with OPENER.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=timeout) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("download exceeds %d MiB" % (MAX_BYTES // (1024 * 1024)))
    return data


def validate_image(data: bytes, suffix: str | None = None) -> None:
    Image = require_pillow()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            _validate(Image, data, suffix)
    except (OSError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError("download is not a complete readable image") from exc


def _validate(Image, data: bytes, suffix: str | None) -> None:
    with Image.open(io.BytesIO(data)) as image:
        fmt = image.format
        if fmt not in ("PNG", "GIF"):
            raise ValueError("expected a PNG or GIF result")
        if suffix and fmt != {".png": "PNG", ".gif": "GIF"}.get(suffix.lower()):
            raise ValueError("downloaded image format does not match output extension")
        image.verify()
    with Image.open(io.BytesIO(data)) as image:
        for index in range(getattr(image, "n_frames", 1)):
            image.seek(index)
            image.load()


def get(url: str, *, timeout: float = 30) -> tuple[str, bytes | None]:
    try:
        data = _download(url, timeout=timeout)
    except urllib.error.HTTPError as exc:
        # Not found yet, timeouts, rate limits and server errors can clear; other client errors never do.
        return ("wait", None) if exc.code in (404, 408, 429) or exc.code >= 500 else ("unavailable", None)
    except (OSError, HTTPException):
        return "wait", None
    return "ok", data


def preflight(out: str, frames: int) -> None:
    path = Path(out)
    if path.exists() or path.is_symlink():
        raise ValueError("refusing existing output; inspect the saved result or choose a new destination")
    if not frames and path.suffix.lower() not in (".png", ".gif"):
        raise ValueError("output must use .png or .gif")
    if frames and path.suffix.lower() in (".png", ".gif"):
        raise ValueError("several links save frames into a new folder; give a folder path, not an image name")


def try_job(urls: list[str], out: str, *, deadline: float | None = None) -> str:
    """Save nothing until every returned link is decoded. Never overwrite a path."""
    require_pillow()
    frames = len(urls) if len(urls) > 1 else 0
    preflight(out, frames)
    got = []
    for url in urls:
        remaining = 30 if deadline is None else min(30, deadline - time.monotonic())
        if remaining <= 0:
            return "wait"
        status, data = get(url, timeout=remaining)
        if status != "ok":
            return status
        validate_image(data, ".png" if frames else Path(out).suffix)
        got.append(data)
    write(Path(out), got, frames)
    return "ok"


def write(path: Path, got: list[bytes], frames: int = 0) -> None:
    """Write new files only; a failed write leaves nothing behind that would block a retry."""
    path.parent.mkdir(parents=True, exist_ok=True)
    paths = frame_paths(path, frames) if frames else [path]
    created: list[Path] = []
    try:
        if frames:
            path.mkdir()  # exclusive directory creation prevents concurrent result mixing
            created.append(path)
        for dest, data in zip(paths, got):
            with dest.open("xb") as handle:
                created.insert(0, dest)
                handle.write(data)
    except OSError:
        for item in created:   # disk full, locked file: remove what this call made
            with contextlib.suppress(OSError):
                item.rmdir() if item.is_dir() else item.unlink()
        raise


def frame_paths(folder: Path, frames: int) -> list[Path]:
    return [folder / ("%d.png" % index) for index in range(frames)]


def outputs(out: str, run: str, frames: int = 0) -> list[str]:
    paths = frame_paths(Path(out), frames) if frames else [Path(out)]
    return [p.resolve().relative_to(Path(run).resolve()).as_posix() for p in paths]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    require_pillow()  # skip before HTTP, manifests, or output changes
    try:
        if argv[:1] == ["--url"] and len(argv) == 3:
            check_host(argv[1])
            preflight(argv[2], 0)
            data = _download(argv[1])
            validate_image(data, Path(argv[2]).suffix)
            write(Path(argv[2]), [data])
            print(argv[2])
            return 0
        ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
        ap.add_argument("job")
        ap.add_argument("out")
        ap.add_argument("--run", required=True)
        ap.add_argument("--url", action="append", required=True)
        ap.add_argument("--tool", default="")
        ap.add_argument("--generations", type=float)
        ap.add_argument("--estimate", type=float)
        ap.add_argument("--timeout", type=float, default=100)
        a = ap.parse_args(argv)
        for url in a.url:
            check_host(url)
        frames = len(a.url) if len(a.url) > 1 else 0
        manifest.number(a.timeout)
        if a.timeout <= 0:
            raise ValueError("--timeout must be positive")
        preflight(a.out, frames)
        expected = outputs(a.out, a.run, frames)  # also reject outputs outside this run
        if frames and Path(a.out).resolve() == Path(a.run).resolve():
            raise ValueError("frame destination must be a new subdirectory of the run")
        if not frames and Path(a.out).resolve() == (Path(a.run) / manifest.NAME).resolve():
            raise ValueError("output conflicts with the manifest")
        entry = {"job_id": a.job, "status": "submitted"}
        if a.tool:
            entry["tool"] = a.tool
        for field, value in (("reported_usage", a.generations), ("estimated_usage", a.estimate)):
            if value is not None:
                entry[field] = {"generations": manifest.number(value)}
        # Record identity/charge or reservation before a bounded wait can be interrupted.
        # The locked ledger merge preserves an already recorded status and earlier saved paths.
        manifest.add_job(a.run, entry)
        started = time.monotonic()
        while True:
            status = try_job(a.url, a.out, deadline=started + a.timeout)
            elapsed = time.monotonic() - started
            if status in ("ok", "unavailable") or elapsed >= a.timeout:
                break
            time.sleep(max(0, min(15, a.timeout - elapsed)))
        update = {"job_id": a.job, "waited_s": round(elapsed), "download_status": status}
        if status == "ok":
            update.update(status="ok", outputs=expected)
        manifest.add_job(a.run, update)
        if status == "ok":
            print("OK %s %s" % (a.job, a.out))
            return 0
        print("DOWNLOAD %s for %s; inspect the matching getter before continuing; do not resubmit or infer a refund"
              % ("unavailable" if status == "unavailable" else "not ready", a.job))
        return 2 if status == "unavailable" else 3
    except HTTPException:
        print("DOWNLOAD not ready; inspect the matching getter before continuing; do not resubmit or infer a refund")
        return 3
    except (ValueError, OSError) as exc:
        print("download blocked: %s; inspect the matching getter and any saved outputs; "
              "do not resubmit or infer a refund" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
