#!/usr/bin/env python3
"""PixelLab Pip bark helper.

This helper is intentionally small and dependency-free. It keeps the bark and
auto configuration portable with the skill first, then falls back to a user
config directory only when the installed skill directory is not writable.
Config writes are atomic and key-preserving so agents never hand-edit the JSON.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import shutil
import subprocess
import tempfile
import time
import wave
from pathlib import Path
from typing import Any


ASSETS_DIR = Path(__file__).resolve().parent
SKILL_DIR = ASSETS_DIR.parent
SKILL_CONFIG = SKILL_DIR / "pixellab-pip.json"
BARK_WAV = ASSETS_DIR / "bark.wav"


def user_config_path() -> Path:
    system = platform.system().lower()
    home = Path.home()

    if system == "windows":
        root = os.environ.get("APPDATA")
        base = Path(root) if root else home / "AppData" / "Roaming"
    elif system == "darwin":
        base = home / "Library" / "Application Support"
    else:
        root = os.environ.get("XDG_CONFIG_HOME")
        base = Path(root) if root else home / ".config"

    return base / "pixellab-pip" / "pixellab-pip.json"


def safe_user_config_path() -> Path | None:
    try:
        return user_config_path()
    except RuntimeError:
        return None


def reject_constant(value: str) -> None:
    raise ValueError("nonstandard JSON constant: " + value)


def finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("JSON number is outside the finite numeric range")
    return result


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), parse_constant=reject_constant, parse_float=finite_float)
    except (OSError, ValueError):
        # ValueError covers json.JSONDecodeError and UnicodeDecodeError (a config
        # re-saved as UTF-16), so a malformed file degrades to the
        # graceful invalid-config path instead of an uncaught traceback.
        return None


def normalize_bark(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return True


def read_config() -> tuple[dict[str, Any], Path | None, Path | None]:
    invalid_source: Path | None = None
    user_config = safe_user_config_path()
    paths = [SKILL_CONFIG]
    if user_config is not None:
        paths.append(user_config)

    for path in paths:
        if path.exists():
            data = read_json(path)
            if isinstance(data, dict):
                return data, path, invalid_source
            if invalid_source is None:
                invalid_source = path
    return {"bark": True}, None, invalid_source


def bark_enabled() -> bool:
    data, _, _ = read_config()
    return normalize_bark(data.get("bark", True))


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=str(path.parent),
            delete=False,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(content)
        deadline = time.monotonic() + 1
        while True:
            try:
                temp_path.replace(path)
                break
            except PermissionError as exc:
                # Windows readers/scanners may briefly deny replacement. Retry
                # only this prepared file, never the setting mutation or toggle.
                if getattr(exc, "winerror", None) not in (5, 32, 33) or time.monotonic() >= deadline:
                    raise
                time.sleep(0.05)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def auto_enabled(data: dict[str, Any], invalid_source: Path | None = None) -> bool:
    return invalid_source is None and data.get("auto") is True


def write_config(key: str, enabled: bool) -> Path:
    existing, _, invalid_source = read_config()
    if invalid_source is not None:
        # An explicit command replaces the unreadable file; a fallback's `auto` must never carry over into it.
        existing.pop("auto", None)
    existing[key] = bool(enabled)
    path = save_config(existing)
    if key == "auto":
        data, _, still_invalid = read_config()
        if auto_enabled(data, still_invalid) is not bool(enabled):
            raise RuntimeError("an unreadable config still keeps Auto off; repair " + str(still_invalid))
    return path


def save_config(data: dict[str, Any]) -> Path:
    content = json.dumps(data, indent=2, sort_keys=True) + "\n"

    candidates = [SKILL_CONFIG]
    user_config = safe_user_config_path()
    if user_config is not None:
        candidates.append(user_config)

    errors: list[str] = []
    for path in candidates:
        if path != SKILL_CONFIG and read_config()[1] == SKILL_CONFIG:
            raise RuntimeError("skill config remains authoritative but could not be updated; "
                               "a user-config fallback would be ignored; inspect status and resolve the read-only skill config")
        try:
            write_text_atomic(path, content)
        except OSError as exc:
            errors.append(f"{path}: {exc}")
            continue
        actual, source, _ = read_config()
        if source != path or json.dumps(actual, indent=2, sort_keys=True) + "\n" != content:
            raise RuntimeError("config write did not become the verified active setting; inspect status before continuing")
        return path

    raise RuntimeError("; ".join(errors) or "could not write config")


def playable_wav(path: Path) -> bool:
    try:
        with wave.open(str(path), "rb"):
            return True
    except (OSError, wave.Error):
        return False


def play_sound() -> bool:
    if not BARK_WAV.exists() or not playable_wav(BARK_WAV):
        return False

    system = platform.system().lower()

    if system == "windows":
        try:
            import winsound

            winsound.PlaySound(str(BARK_WAV), winsound.SND_FILENAME)
            return True
        except Exception:
            return False

    commands = []
    if system == "darwin":
        commands.append(["afplay", str(BARK_WAV)])
    else:
        commands.extend(
            [
                ["paplay", str(BARK_WAV)],
                ["pw-play", str(BARK_WAV)],
                ["aplay", "-q", str(BARK_WAV)],
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(BARK_WAV)],
            ]
        )

    for command in commands:
        if shutil.which(command[0]) is None:
            continue
        try:
            completed = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=3,
            )
            if completed.returncode == 0:
                return True
        except (OSError, subprocess.TimeoutExpired):
            continue

    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="PixelLab Pip bark helper")
    parser.add_argument("command", choices=["status", "bark", "on", "off", "play", "auto", "auto-on", "auto-off"])
    args = parser.parse_args()

    result: dict[str, Any] = {
        "ok": True,
        "bark": bark_enabled(),
        "config": None,
        "played": False,
        "sound": str(BARK_WAV),
    }

    try:
        if args.command == "bark":
            enabled = not bark_enabled()
            result["config"] = str(write_config("bark", enabled))
            result["bark"] = enabled
            if result["bark"]:
                result["played"] = play_sound()
        elif args.command == "on":
            result["config"] = str(write_config("bark", True))
            result["bark"] = True
            result["played"] = play_sound()
        elif args.command == "off":
            result["config"] = str(write_config("bark", False))
            result["bark"] = False
        elif args.command == "play":
            if bark_enabled():
                result["played"] = play_sound()
            result["bark"] = bark_enabled()
        elif args.command == "auto":
            data, _, invalid_source = read_config()
            if invalid_source is not None:
                # Its intended value is unknown, so a toggle could turn Auto on by accident.
                raise ValueError("config is unreadable; say auto on or auto off instead of toggling")
            enabled = not auto_enabled(data, invalid_source)
            result["config"] = str(write_config("auto", enabled))
            result["auto"] = enabled
        elif args.command == "auto-on":
            result["config"] = str(write_config("auto", True))
            result["auto"] = True
        elif args.command == "auto-off":
            result["config"] = str(write_config("auto", False))
            result["auto"] = False
        elif args.command == "status":
            data, source, invalid_source = read_config()
            result["bark"] = normalize_bark(data.get("bark", True))
            result["auto"] = auto_enabled(data, invalid_source)
            result["bark_value_ignored"] = "bark" in data and not isinstance(data["bark"], bool)
            result["config"] = str(source) if source else None
            result["invalid_config"] = str(invalid_source) if invalid_source else None
    except Exception as exc:
        result["ok"] = False
        result["error"] = str(exc)

    print(json.dumps(result, sort_keys=True))

    if not result["ok"]:
        return 1
    if args.command == "play" and result["bark"] and not result["played"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
