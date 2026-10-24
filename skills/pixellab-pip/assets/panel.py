"""Build a private, interactive project-review snapshot without spending or changing settings.

    python panel.py PROJECT [--run PROJECT_RELATIVE_RUN]
                    [--image ROLE PROJECT_RELATIVE_IMAGE]... [--out PROJECT_RELATIVE_DIRECTORY]
                    [--labels PROJECT_RELATIVE_JSON] [--lang LANGUAGE_TAG] [--fragment]
    python panel.py verify SNAPSHOT_JSON
    python panel.py open SNAPSHOT_JSON

Select the run and images explicitly; there is no newest-file discovery. Outputs are
fresh panel.json/panel.html files. The HTML composes requests for return to chat;
neither a snapshot nor a composed request grants execution authority.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import html
import io
import json
import os
from pathlib import Path, PureWindowsPath
import re
import sys
import warnings
import webbrowser

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _assembly import load_pillow, preflight_outputs  # noqa: E402
import manifest  # noqa: E402
import project_style  # noqa: E402

MAX_IMAGES = 12
MAX_IMAGE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_IMAGE_BYTES = 5 * 1024 * 1024
MAX_IMAGE_PIXELS = 4_000_000
MAX_FRAMES = 256
MAX_JSON_BYTES = 2 * 1024 * 1024
MAX_JOBS = 200
DEFAULT_LABELS = {
    "title": "PixelLab Pip review panel", "project": "Project", "run": "Run", "style": "Saved appearance",
    "none": "none selected", "snapshot": "Snapshot",
    "snapshot_help": "Not live. Run /pixellab-pip panel again in a fresh output directory to refresh.",
    "charged": "charged generations", "committed": "committed generations", "unknown": "unknown",
    "preview_alt": "Selected preview", "preview_unavailable": "Preview could not be displayed. Open the original and rebuild the panel.",
    "no_images": "No previews selected. Ask the agent to open the panel with explicit image roles and paths.",
    "note": "Request or correction notes", "request": "Compose request", "redo": "Request redo",
    "animate": "Request animation", "setup": "Request project setup",
    "open_review": "Open full review", "open_failed": "Could not open the full review. Ask the agent for the HTML path.",
    "opened_review": "Opened the full review in your browser.",
    "welcome": "Start with a request, guided help, or project setup. No generation runs from this panel.",
    "guide": "Guided help", "guide_prompt": "Help me choose the next PixelLab Pip step for this project.",
    "feedback_intro": "PixelLab Pip request", "policy_short": "Compose in chat. Pip verifies the files and applies normal approval rules.",
    "input_unavailable": "This surface cannot edit notes. Compose in the full review or agent chat.",
    "native_image_unavailable": "Open full review for this preview.",
    "native_preview_unavailable": "This native surface or selection cannot show every preview. Open the sibling panel.html in a browser; redo and animation requests are unavailable here until every selected image can be reviewed.",
    "empty_note": "Enter a request first.", "draft_ready": "Request composed. Send it in chat; no work has been submitted.",
    "draft_unavailable": "Could not place the request in chat. Copy it manually.",
    "usage_scope": "Selected run only", "cost_explanation": "reported charges or unresolved estimates",
    "previews": "Selected previews", "scale": "Shared pixel scale", "jobs": "Selected run jobs",
    "job": "Job", "tool": "Tool", "status": "Status", "outcome": "Outcome", "not_recorded": "not recorded",
    "compose_heading": "Compose a request", "new_character": "New character", "new_attack": "New attack", "new_skill": "New skill",
    "character_prompt": "Make a new character: ", "attack_prompt": "Make an attack animation: ", "skill_prompt": "Make a skill animation: ",
    "note_placeholder": "Describe what you want or what should change.", "feedback_label": "Request to send in chat",
    "copy_request": "Copy request", "review_blocked": "Redo/animation composition requires an identifiable selected run and every selected preview. Resolve unavailable previews in chat first.",
    "send_request": "Send request to chat", "send_title": "Send this PixelLab Pip request to chat?",
    "host_handoff": "Request handed to the host for confirmation. It may be canceled; this panel has not approved or run a generation.",
    "send_unavailable": "The host could not receive the request. Copy it and send it in chat instead.",
    "copy_empty": "Compose a request first.", "copied": "Copied. Paste and send it in chat.",
    "copy_unavailable": "Clipboard access unavailable. Copy the selected request manually and send it in chat.",
    "style_none": "No saved style", "style_project": "Project appearance", "style_unavailable": "Style unavailable",
}


def contained(root: Path, relative: str) -> Path:
    """Resolve only an explicitly project-relative path, including existing symlinks."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() \
            or PureWindowsPath(relative).drive or relative.startswith(("/", "\\")):
        raise ValueError("expected a project-relative path")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes the selected project: " + relative)
    return path


def read_bounded(path: Path, limit: int) -> bytes:
    if not path.is_file():
        raise ValueError("missing regular file: " + str(path))
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError("file exceeds the panel size limit: " + str(path))
    return data


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _labels(root: Path, path: str | None) -> dict:
    labels = dict(DEFAULT_LABELS)
    if path is not None:
        data = json.loads(read_bounded(contained(root, path), 128 * 1024).decode("utf-8-sig"))
        if not isinstance(data, dict) or any(k not in labels for k in data):
            raise ValueError("panel labels must be an object containing only known label keys")
        if any(not isinstance(v, str) or not v.strip() or len(v) > 2000 for v in data.values()):
            raise ValueError("panel labels must be nonempty strings of at most 2000 characters")
        labels.update(data)
    return labels


def _style(root: Path, diagnostics: list[str], labels: dict) -> str:
    profile = contained(root, "pixellab-pip-style.json")
    if not profile.exists():
        return labels["style_none"]
    try:
        read_bounded(profile, MAX_JSON_BYTES)
        data = project_style.load(str(profile))
        project_style.validate_profile(data)
        active = data.get("active_style")
        if active:
            if len(active) > 256:
                diagnostics.append("Style name exceeds the panel display limit; inspect the profile directly.")
                return active[:256] + "…"
            return active
        return labels["style_project"] if any(k in data for k in project_style.STYLE_KEYS) else labels["style_none"]
    except (OSError, ValueError) as exc:
        diagnostics.append("Project style could not be read: " + str(exc))
        return labels["style_unavailable"]


def language_tag(value: str) -> str:
    if not isinstance(value, str) or len(value) > 63 or not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", value):
        raise ValueError("lang must be a language tag such as en, ja, or zh-Hant")
    return value


def build_snapshot(project: str, run: str | None = None, images=(), labels: str | None = None, lang: str = "en") -> dict:
    root = Path(project).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project must be an existing directory")
    if len(images) > MAX_IMAGES:
        raise ValueError(f"select at most {MAX_IMAGES} images per panel")
    label_map = _labels(root, labels)
    diagnostics: list[str] = []
    snapshot = {
        "version": 1, "project": str(root), "run": None, "lang": language_tag(lang),
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "style": _style(root, diagnostics, label_map), "labels": label_map,
        "usage": {"charged": None, "committed": None},
        "jobs": [], "images": [], "manifest_sha256": None, "warnings": diagnostics,
    }
    if run is not None:
        selected = contained(root, run)
        if not selected.is_dir():
            raise ValueError("selected run must be an existing directory")
        snapshot["run"] = selected.relative_to(root).as_posix()
        ledger = contained(root, snapshot["run"] + "/" + manifest.NAME)
        try:
            before = read_bounded(ledger, MAX_JSON_BYTES)
            entries = manifest.jobs(str(selected))
            for key, reader in (("charged", manifest.spent), ("committed", manifest.committed)):
                try:
                    snapshot["usage"][key] = reader(str(selected))
                except ValueError:
                    diagnostics.append(key.capitalize() + " generations are unknown for this selected run.")
            if before != read_bounded(ledger, MAX_JSON_BYTES):
                raise ValueError("manifest changed while reading; rebuild the panel")
            snapshot["manifest_sha256"] = digest(before)
            snapshot["jobs"] = [{"job_id": entry["job_id"], "tool": entry.get("tool", label_map["not_recorded"]),
                                 "status": entry.get("status", label_map["not_recorded"]),
                                 **({"outcome": entry["outcome"]} if "outcome" in entry else {})}
                                for entry in entries[:MAX_JOBS]]
            if len(entries) > MAX_JOBS:
                diagnostics.append(f"Showing the first {MAX_JOBS} of {len(entries)} selected run jobs; usage covers all its jobs.")
        except (OSError, ValueError) as exc:
            snapshot["usage"] = {"charged": None, "committed": None}
            diagnostics.append("Selected run accounting is unavailable: " + str(exc))
    else:
        diagnostics.append("No run selected. Usage and jobs are not project lifetime totals.")
    total_bytes = 0
    for role, relative in images:
        if not isinstance(role, str) or not role.strip() or len(role) > 100:
            raise ValueError("image role must be a nonempty label of at most 100 characters")
        image_path = contained(root, relative)
        try:
            data = read_bounded(image_path, MAX_IMAGE_BYTES)
            if total_bytes + len(data) > MAX_TOTAL_IMAGE_BYTES:
                raise ValueError("selected images exceed the combined panel size limit")
            Image = load_pillow()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error", Image.DecompressionBombWarning)
                    with Image.open(io.BytesIO(data)) as image:
                        image_format = image.format
                        if image_format not in ("PNG", "GIF"):
                            raise ValueError("only PNG and GIF previews are supported")
                        width, height = image.size
                        count = getattr(image, "n_frames", 1)
                        if width * height * count > MAX_IMAGE_PIXELS or count > MAX_FRAMES:
                            raise ValueError("image dimensions/frame count exceed the panel limit")
                        for frame in range(count):
                            image.seek(frame)
                            image.load()
            except Image.DecompressionBombError as exc:
                raise ValueError("image exceeds the safe decoding limit") from exc
            total_bytes += len(data)
            snapshot["images"].append({
                "role": role, "path": image_path.relative_to(root).as_posix(), "sha256": digest(data),
                "data_url": "data:image/" + image_format.lower() + ";base64," + base64.b64encode(data).decode("ascii"),
                "width": width, "height": height,
            })
        except (ImportError, OSError, ValueError, Warning) as exc:
            diagnostics.append("Preview unavailable for " + role + " (" + relative + "): " + str(exc))
    snapshot["review_ready"] = bool(snapshot["run"] and snapshot["manifest_sha256"]
                                    and snapshot["images"] and len(snapshot["images"]) == len(images))
    return snapshot


def _read_snapshot(snapshot_path: str) -> tuple[Path, dict, Path]:
    snapshot_file = Path(snapshot_path).resolve(strict=True)
    data = json.loads(read_bounded(snapshot_file, MAX_TOTAL_IMAGE_BYTES * 2).decode("utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("unsupported panel snapshot")
    if not isinstance(data.get("project"), str):
        raise ValueError("invalid panel project")
    root = Path(data["project"])
    if not root.is_absolute() or not root.is_dir() or root.resolve() != root:
        raise ValueError("snapshot project must be an existing canonical absolute directory")
    if not snapshot_file.is_relative_to(root):
        raise ValueError("snapshot is outside its selected project")
    return snapshot_file, data, root


def verify(snapshot_path: str) -> dict:
    """Check the selected content identity; never interpret this as spending approval."""
    _, data, root = _read_snapshot(snapshot_path)
    if data.get("run") is not None:
        run = contained(root, data["run"])
        expected = data.get("manifest_sha256")
        if not isinstance(expected, str) or digest(read_bounded(contained(root, str(run.relative_to(root) / manifest.NAME)), MAX_JSON_BYTES)) != expected:
            raise ValueError("selected manifest is unavailable or changed; rebuild the panel")
    entries = data.get("images")
    if not isinstance(entries, list) or len(entries) > MAX_IMAGES:
        raise ValueError("invalid panel images")
    for image in entries:
        if not isinstance(image, dict) or not isinstance(image.get("sha256"), str):
            raise ValueError("invalid panel image identity")
        display = image.get("data_url")
        if not isinstance(display, str) or not display.startswith(("data:image/png;base64,", "data:image/gif;base64,")):
            raise ValueError("invalid panel image preview")
        try:
            displayed_bytes = base64.b64decode(display.partition(",")[2], validate=True)
        except ValueError as exc:
            raise ValueError("invalid panel image preview encoding") from exc
        if digest(displayed_bytes) != image["sha256"]:
            raise ValueError("displayed image does not match its recorded identity; rebuild the panel")
        if digest(read_bounded(contained(root, image.get("path")), MAX_IMAGE_BYTES)) != image["sha256"]:
            raise ValueError("selected image changed; rebuild the panel: " + image["path"])
    return {"verified": True, "project": str(root), "run": data.get("run"),
            "created_at": data.get("created_at"), "manifest_sha256": data.get("manifest_sha256"),
            "review_ready": data.get("review_ready") is True and bool(data.get("run") and entries),
            "images": [{k: image[k] for k in ("role", "path", "sha256")} for image in entries]}


def render(snapshot: dict, snapshot_path: Path, fragment: bool = False) -> str:
    template = Path(__file__).with_suffix(".html").read_text(encoding="utf-8")
    payload = json.dumps({"snapshot": snapshot, "snapshot_path": str(snapshot_path), "inline": fragment}, ensure_ascii=True, allow_nan=False)
    # JSON in an HTML script element must not be able to close the element.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    body = template.replace("__PANEL_DATA__", payload)
    if fragment:
        if len(body.encode("utf-8")) >= 1_000_000:
            raise ValueError("inline panel exceeds the 1 MB renderer limit; use standalone HTML or fewer/smaller previews")
        return body
    return '<!doctype html><html lang="' + html.escape(language_tag(snapshot.get("lang", "en")), quote=True) + '"><head><meta charset="utf-8">' \
        '<meta name="viewport" content="width=device-width,initial-scale=1">' \
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; ' \
        'style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; connect-src \'none\'; ' \
        'base-uri \'none\'; form-action \'none\'">' \
        '<title>' + html.escape(snapshot["labels"]["title"]) + '</title></head><body>' + body + '</body></html>\n'


def open_review(snapshot_path: str) -> dict:
    """Open only an unchanged standalone review produced by this helper."""
    selected = Path(snapshot_path).absolute()
    snapshot_file = selected.resolve(strict=True)
    if selected != snapshot_file or snapshot_file.name != "panel.json":
        raise ValueError("select an unredirected panel.json snapshot")
    _, snapshot, root = _read_snapshot(str(snapshot_file))
    private = root / "pixellab-pip-generations"
    if private.resolve() != private or not snapshot_file.is_relative_to(private):
        raise ValueError("panel must be in the project's unredirected private generations directory")
    panel_file = snapshot_file.with_name("panel.html")
    if panel_file.resolve(strict=True) != panel_file:
        raise ValueError("panel HTML must not redirect to another file")
    expected = render(snapshot, snapshot_file)
    actual = read_bounded(panel_file, MAX_TOTAL_IMAGE_BYTES * 3).decode("utf-8").replace("\r\n", "\n")
    if actual != expected:
        raise ValueError("panel HTML differs from its standalone snapshot; rebuild the panel")
    if not webbrowser.open(panel_file.as_uri(), new=2):
        raise ValueError("browser could not open the panel; open panel.html manually")
    return {"opened": True, "panel": str(panel_file)}


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] in ("verify", "open"):
        parser = argparse.ArgumentParser(description="Verify a panel snapshot against the current selected files.")
        parser.add_argument("command", choices=["verify", "open"])
        parser.add_argument("snapshot")
        args = parser.parse_args(argv)
        try:
            print(json.dumps((verify if args.command == "verify" else open_review)(args.snapshot)))
            return 0
        except (OSError, ValueError, TypeError, KeyError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project")
    parser.add_argument("--run")
    parser.add_argument("--image", nargs=2, action="append", default=[], metavar=("ROLE", "PROJECT_RELATIVE_PATH"))
    parser.add_argument("--out")
    parser.add_argument("--labels", help="explicit project-relative JSON overrides for known UI labels; defaults are in DEFAULT_LABELS")
    parser.add_argument("--lang", default="en", help="language tag for the supplied UI labels, e.g. en or ja")
    parser.add_argument("--fragment", action="store_true", help="HTML fragment for a verified inline renderer; not a live bridge")
    args = parser.parse_args(argv)
    try:
        snapshot = build_snapshot(args.project, args.run, args.image, args.labels, args.lang)
        root = Path(snapshot["project"])
        private_root = contained(root, "pixellab-pip-generations")
        if private_root != root / "pixellab-pip-generations":
            raise ValueError("private generations directory must not redirect snapshots to another project folder")
        run_in_private = snapshot["run"] and contained(root, snapshot["run"]).is_relative_to(private_root)
        default_out = (snapshot["run"] + "/panel") if run_in_private else "pixellab-pip-generations/panel"
        out = contained(root, args.out or default_out)
        if out == private_root or not out.is_relative_to(private_root):
            raise ValueError("private panel outputs must use a subdirectory of pixellab-pip-generations/")
        if out.exists() and any(out.iterdir()):
            raise ValueError("panel output directory must be fresh or empty; existing files left unchanged")
        paths = [out / "panel.json", out / "panel.html"]
        sources = [contained(root, "pixellab-pip-style.json"), *(contained(root, path) for _, path in args.image)]
        if snapshot["run"]:
            sources.append(contained(root, snapshot["run"] + "/" + manifest.NAME))
        if args.labels:
            sources.append(contained(root, args.labels))
        ignore = out / ".gitignore"
        preflight_outputs([ignore, *paths], sources)
        html = render(snapshot, paths[0], args.fragment)
        out.mkdir(parents=True, exist_ok=True)
        if out.resolve() != out or not out.is_relative_to(root):
            raise ValueError("output directory changed; choose a safe project directory")
        contents = [json.dumps(snapshot, indent=2, ensure_ascii=False, allow_nan=False) + "\n", html]
        for path, content in zip([ignore, *paths], ["*\n", *contents]):
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(content)
        print(json.dumps({"snapshot": str(paths[0]), "panel": str(paths[1])}))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
