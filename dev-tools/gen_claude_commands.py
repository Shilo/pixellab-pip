"""Writes the Claude edition's short commands (editions/claude/commands/pga-*.md) from one table.

Each command is a thin alias into the one core skill: it names the intent and passes the user's words on.
Pre-approved tools are read-only (the skill's local helpers and PixelLab status reads); paid PixelLab calls keep
Claude Code's normal permission and the skill's approval levels.

    python dev-tools/gen_claude_commands.py           write the files
    python dev-tools/gen_claude_commands.py --check   exit 1 when a file is missing or out of date
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "editions" / "claude" / "commands"
READS = ("get_balance", "get_image", "get_upload_url", "wait_for_jobs")
# a user's own `pixellab` server, and the server this plugin bundles (plugin servers are namespaced)
TOOLS = " ".join(["Bash(python *skills/pixellab-pip/assets/*)"]
                 + [f"mcp__{server}__{tool}" for server in ("pixellab", "plugin_pixellab-pip-studio_pixellab") for tool in READS])

# name: (description, argument hint, the intent handed to the skill)
COMMANDS = {
    "pga-start": ("A guided first project: plain steps, a style, then a character and a move",
                  "", "a guided first project for someone new: explain each step in plain words, help them choose an art style, then make one character and one move"),
    "pga-init": ("Set up this project: art style, engine and output folder", "",
                 "project setup: art style (always the user's choice), engine, output folder and approval level"),
    "pga-style": ("List, pick, change or save art styles", "[list | use <name> | new | example <name>]",
                  "manage the project's art styles"),
    "pga-analyze": ("Match art you show: measure it and save it as a style", "<image | gif | folder>",
                    "match the art the user shows and save it as a project style"),
    "pga-char": ("Make a character in the project style", "<description> [--n 3]",
                 "make a character: a few candidates in the project style, checked at 3x"),
    "pga-anim": ("Make an attack, skill or other move from a sprite", "<sprite.png> <move>",
                 "an attack, skill or signature move from a standing sprite: key poses, review, in-betweens, finishing, doctor, sheet"),
    "pga-vfx": ("Make a painted effect (slash, burst, beam, smoke)", "<effect>",
                "a painted effect with vfx_workbench"),
    "pga-fix": ("Check animation frames and fix what's free; plan re-rolls for the rest", "<frames | folder | sheet | gif>",
                "check and fix animation frames with the animation doctor"),
    "pga-reroll": ("Redo the frames a check found bad", "<fix_report.json> [plan number]",
                   "re-roll the planned frames from an animation doctor report, through the approval level"),
    "pga-bg": ("Make a background or backdrop", "<description>", "a background or backdrop in the project style"),
    "pga-scene": ("Make a scene or location art", "<description>", "a scene in the project style"),
    "pga-building": ("Make a building sprite", "<description>", "a building in the project style"),
    "pga-icon": ("Make icons or UI art", "<description>", "icons or UI art in the project style"),
    "pga-tiles": ("Make a tileset", "<description>", "a tileset in the project style"),
    "pga-normal": ("Make normal maps so an engine can light sprites", "<sprite or sheet>", "normal maps for sprites or sheets"),
    "pga-batch": ("Make several assets in one approved plan", "<list>", "a batch of assets planned and approved together"),
    "pga-history": ("Show past runs and what they spent", "[--runs N]", "the project's run history and spend"),
    "pga-prompt": ("Improve a prompt without generating anything", "<prompt>", "prompt improvement only, no generation"),
    "pga-level": ("Show or set the approval level: ask, plan or auto", "[ask | plan <budget> <redos> | auto <budget> <redos>]",
                  "the approval level command"),
    "pga-help": ("Every command and what it does", "", "help: list the commands and what each does"),
}


def render(name: str) -> str:
    desc, hint, intent = COMMANDS[name]
    head = ["---", "description: " + json.dumps(desc)]   # quoted: a colon or [..] would break the YAML
    if hint:
        head.append("argument-hint: " + json.dumps(hint))
    head += ["allowed-tools: " + TOOLS, "---"]
    return "\n".join(head) + f"\n\nUse the pixellab-pip skill for: {intent}.\n\nRequest: $ARGUMENTS\n"


def main(argv: list[str]) -> int:
    check = "--check" in argv
    stale = []
    for name in COMMANDS:
        path = OUT / f"{name}.md"
        text = render(name)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path.name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    extra = sorted(p.name for p in OUT.glob("pga-*.md") if p.stem not in COMMANDS) if OUT.exists() else []
    if check and (stale or extra):
        print("out of date: " + ", ".join(stale + extra) + " (run dev-tools/gen_claude_commands.py)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
