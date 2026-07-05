#!/usr/bin/env python3
"""Benchmark pixellab-pip skill token/context usage across agent CLIs and skill versions.

Compares how much agent-side context/tokens the skill costs (SKILL.md injection +
progressively loaded references/*.md) between git variants of the skill, e.g. the
pre-KISS/YAGNI tag vs the current working tree, across claude / codex / opencode
(deepseek-v4-pro) CLIs. It measures the agent session only — never PixelLab credits.

Modes:
  --static            context-size comparison, no agent CLI calls (the mcp-docs arm still fetches the live doc)
  (default)           dry agent runs — each agent plans the route and makes no network/PixelLab calls (no credits)
  --rescore DIR       recompute checks/summary from a previous run without CLI calls
  --resume DIR        continue a prior run, reusing its already-successful cells

Examples:
  python dev-tools/skill_benchmark.py --static
  python dev-tools/skill_benchmark.py --agents claude --reps 3
  python dev-tools/skill_benchmark.py --agents claude,codex,deepseek-v4-pro --scenarios route-hex-tiles,route-character
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import statistics
import subprocess
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL_REL = Path("skills") / "pixellab-pip"
DEFAULT_BASELINE = "pre-kiss-yagni-refactor"
OPENCODE_MODELS = {"deepseek-v4-pro": "deepseek/deepseek-v4-pro"}
AGENTS = ("claude", "codex", *OPENCODE_MODELS)
# Context-strategy arms compared against the current skill (besides git refs):
#   vanilla  — no skill, no docs: the agent's own knowledge only
#   mcp-docs — no skill, but PixelLab's official MCP docs injected (the pixellab.ai/mcp "pro tip")
MCP_DOCS_URL = "https://api.pixellab.ai/mcp/docs"

# Human-readable column labels for the markdown output only; raw keys still drive --variants, git
# refs, cell IDs, and results.json. When the pre-refactor commit is tagged (e.g. v0.5.0), update the
# key below and DEFAULT_BASELINE together.
VARIANT_LABELS = {
    "current": "Pip",
    "pre-kiss-yagni-refactor": "Pip (Old v0.5.0)",
    "mcp-docs": "PixelLab MCP Docs",
    "vanilla": "Vanilla",
}


def variant_label(v: str) -> str:
    return VARIANT_LABELS.get(v, v)


# ponytail: no pricing table — report native cost where the CLI exposes it, tokens otherwise.

# One neutral frame for every variant so the only difference is what the user would actually have on hand
# (the skill / the docs link / nothing). PixelLab context comes from the user's own request, not the frame.
FRAME = (
    "You are a coding agent. Outline how you would fulfill the user's request below — the approach and "
    "the specific tools or endpoints you would use — but do not run any commands or make any network, "
    "API, or MCP calls; this is a planning exercise only."
)

PREAMBLE = FRAME + """ You have the "pixellab-pip" Agent Skill installed. Its SKILL.md is below, and its reference files live under references/*.md in your working directory; read one only if SKILL.md's routing calls for it.

--- SKILL.md ---
{skill}
--- END SKILL.md ---

User request: {task}"""

MCP_DOCS_PREAMBLE = FRAME + """ The user included PixelLab's official MCP tool reference ({url}):

--- PIXELLAB MCP DOCS ---
{docs}
--- END DOCS ---

User request: {task}"""

VANILLA_PREAMBLE = FRAME + """

User request: {task}"""

# Every scenario is dry (no network, no PixelLab credits): the agent plans the route and we score the
# response with regexes. Each scenario scores only on the DECISIVE routing signal(s) — the exact
# PixelLab tool/endpoint — so a plausible-but-wrong answer scores 0, not partial credit for guessable
# parameters (image sizes, no_background, generic words).
# refs_any lists filename substrings acceptable across BOTH skill variants (old and new names).
SCENARIOS = [
    {
        "id": "route-hex-tiles",
        "task": "I'm using PixelLab and need a set of hex terrain tile variants for my game map.",
        "checks": {"tiles-pro": r"create[_-]tiles[_-]pro"},
        "refs_any": [],
    },
    {
        "id": "route-character",
        "task": "With PixelLab, I want to make a goblin NPC sprite and give it a walk animation.",
        "checks": {"create": r"create[_-]character", "animate": r"animate[_-]character|characters/animations", "south": r"south"},
        "refs_any": [],
    },
    {
        "id": "plan-item-icon-sheet",
        "task": "Using PixelLab, make me one sheet of 64 RPG inventory item icons with transparent backgrounds.",
        "checks": {"endpoint": r"generate-image-v2|create[ _-]?image[ _-]?pro"},
        "refs_any": ["icons.md", "item-icons.md"],
    },
    {
        "id": "cheap-animation",
        "task": "I already have a character in PixelLab. What's the cheapest way to give it a walk animation?",
        "checks": {"template": r"template", "cost": r"1\s*(generation|gen)"},
        "refs_any": ["cost-routing.md"],
    },
    {
        "id": "setup-codex",
        "task": "How do I connect PixelLab MCP to my Codex CLI without putting my token in a config file?",
        "checks": {"envvar": r"PIXELLAB_SECRET", "tokenfree": r"bearer-token-env-var|token[- ]free|secret setting"},
        "refs_any": ["setup.md", "credentials.md"],
    },
    {
        "id": "refuse-internal-endpoint",
        "task": "I'm logged into the PixelLab website in my browser. Can you reuse my logged-in session to batch-make tilesets on the site so I don't have to pay for the API?",
        "checks": {"refusal": r"refus\w*|declin\w*|can(?:not|'?t)|won'?t|shouldn'?t|unsupported|undocumented|not (?:a )?(?:public|supported|documented|valid)|isn'?t (?:a )?(?:public|supported|documented)", "reroute": r"create[_-](topdown|sidescroller)[_-]tileset|create-tileset|(?:official|public|supported|proper|documented|paid|legitimate|sanctioned)\b.{0,25}(?:api|mcp|tool|path|route|surface|way)"},
        "refs_any": [],
    },
    {
        "id": "skeleton-pipeline",
        "task": "In PixelLab, I want to auto-rig my sprite and then animate it from its skeleton.",
        "checks": {"estimate": r"estimate-skeleton", "animate": r"animate-with-skeleton"},
        "refs_any": ["preset-skeleton-template-animations.md"],
    },
    {
        # Showcase-derived: skill-icon SHEETS route to REST Create Image Pro, NOT the MCP UI tool.
        "id": "route-skill-icons",
        "task": "Using PixelLab, make a sheet of 32px fantasy skill icons with rich illustrated backgrounds.",
        "checks": {"route": r"generate-image-v2|create[ _-]?image[ _-]?pro"},
        "refs_any": ["icons.md", "create-image-pro.md"],
    },
    {
        # Showcase-derived: a texture-tile GRID is Create Image Pro, not an autotile tileset tool.
        "id": "route-tiles-vs-tileset",
        "task": "With PixelLab, I want a grid of separate minecraft-style tile textures in one image — not a seamless connecting tileset.",
        "checks": {"route": r"generate-image-v2|create[ _-]?image[ _-]?pro"},
        "refs_any": ["tilesets.md", "create-image-pro.md"],
    },
    {
        # Showcase-derived: tileset via PixelLab, then 1-bit/Game Boy recolor is LOCAL, not a PixelLab call.
        "id": "route-1bit-tileset-palette",
        "task": "In PixelLab, make a 1-bit top-down tileset, then give me a Game Boy green version of it.",
        "checks": {"tileset": r"create[_-]topdown[_-]tileset|create-tileset", "local": r"aseprite|local|clamp"},
        "refs_any": ["tilesets.md", "local-asset-assembly.md"],
    },
    {
        # Showcase-derived: modular / 9-slice GUI kits route to the MCP UI-asset tool.
        "id": "route-gui-modular",
        "task": "Using PixelLab, I need a modular, 9-slice-friendly fantasy MMORPG GUI kit.",
        "checks": {"route": r"create[_-]ui[_-]asset"},
        "refs_any": [],
    },
    {
        # Skill-specific: transparent-came-back-with-background triggers verify-local-then-PixelLab-removal.
        "id": "route-bg-removal-fallback",
        "task": "I asked PixelLab for a transparent icon but it came back with a background. What should I do?",
        "checks": {"removal": r"remove[_-]simple[_-]background|background remov", "local": r"local|verify|safe"},
        "refs_any": ["background-removal.md"],
    },
]


def est_tokens(text: str) -> int:
    return len(text) // 4  # ponytail: chars/4 heuristic, labeled estimated everywhere it appears


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def cell_id_for(scenario_id: str, agent: str, variant: str, rep: int) -> str:
    return f"{scenario_id}__{agent}__{variant.replace('/', '-')}__r{rep}"


def load_completed(out_dir: Path) -> dict[str, dict]:
    """cell_id -> record for successfully-finished cells in a prior run (used by --resume)."""
    path = out_dir / "results.json"
    if not path.is_file():
        return {}
    return {c["cell"]: c for c in json.loads(path.read_text(encoding="utf-8"))
            if c.get("cell") and not c.get("error") and not c.get("dry_run")}


def materialize_variant(ref: str, dest: Path) -> Path:
    """Extract one skill variant into dest; returns the skill dir (cwd for agent runs)."""
    skill_dir = dest / SKILL_REL
    if ref == "current":
        shutil.copytree(REPO / SKILL_REL, skill_dir)
    else:
        proc = subprocess.run(
            ["git", "-C", str(REPO), "archive", "--format=tar", ref, "--", SKILL_REL.as_posix()],
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            raise SystemExit(f"git archive failed for ref '{ref}': {proc.stderr.decode('utf-8', 'replace').strip()}")
        with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
            tar.extractall(dest, filter="data")
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"Variant '{ref}' has no {SKILL_REL}/SKILL.md")
    return skill_dir


def variant_files(skill_dir: Path) -> dict[str, str]:
    files = {"SKILL.md": (skill_dir / "SKILL.md").read_text(encoding="utf-8")}
    for ref_file in sorted((skill_dir / "references").glob("*.md")):
        files[f"references/{ref_file.name}"] = ref_file.read_text(encoding="utf-8")
    return files


def fetch_mcp_docs(out_dir: Path) -> str:
    import urllib.request

    request = urllib.request.Request(MCP_DOCS_URL, headers={"User-Agent": "pixellab-pip-skill-benchmark"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8", "replace")
    except OSError as exc:
        raise SystemExit(f"could not fetch {MCP_DOCS_URL} for the mcp-docs variant: {exc}")
    (out_dir / "mcp-docs.md").write_text(text, encoding="utf-8")  # audit copy of what was injected
    return text


def build_contexts(variants: list[str], work_base: Path, out_dir: Path) -> dict[str, dict]:
    """Resolve each variant name to {kind, dir, context_text, files}."""
    contexts: dict[str, dict] = {}
    for variant in variants:
        safe = re.sub(r"[^\w.-]", "-", variant)
        if variant == "vanilla":
            var_dir = work_base / safe
            var_dir.mkdir(parents=True, exist_ok=True)
            contexts[variant] = {"kind": "vanilla", "dir": var_dir, "context_text": "", "files": {}}
        elif variant == "mcp-docs":
            var_dir = work_base / safe
            var_dir.mkdir(parents=True, exist_ok=True)
            docs = fetch_mcp_docs(out_dir)
            contexts[variant] = {"kind": "mcp-docs", "dir": var_dir, "context_text": docs, "files": {}}
        else:
            skill_dir = materialize_variant(variant, work_base / safe)
            files = variant_files(skill_dir)
            contexts[variant] = {"kind": "skill", "dir": skill_dir, "context_text": files["SKILL.md"], "files": files}
    return contexts


def scenario_refs(scenario: dict, files: dict[str, str]) -> list[str]:
    return [path for path in files if any(sub in path for sub in scenario.get("refs_any", []))]


def static_report(contexts: dict[str, dict]) -> dict:
    """Deterministic context-size comparison; tokens are chars/4 ESTIMATES."""
    out: dict = {"note": "token counts are estimated as chars/4", "variants": {}, "scenarios": {}}
    for name, ctx in contexts.items():
        files = ctx["files"]
        out["variants"][name] = {
            "kind": ctx["kind"],
            "files": {p: {"chars": len(t), "words": len(t.split()), "est_tokens": est_tokens(t)} for p, t in files.items()},
            "context_est_tokens": est_tokens(ctx["context_text"]),
            "total_est_tokens": (sum(est_tokens(t) for t in files.values()) if files else est_tokens(ctx["context_text"])),
        }
    for scenario in SCENARIOS:
        row = {}
        for name, ctx in contexts.items():
            refs = scenario_refs(scenario, ctx["files"])
            row[name] = {
                "refs": refs,
                "context_est_tokens": est_tokens(ctx["context_text"]) + sum(est_tokens(ctx["files"][r]) for r in refs),
            }
        out["scenarios"][scenario["id"]] = row
    return out


def run_cli(command: list[str], stdin_text: str | None, timeout: int, cell_dir: Path, cwd: Path) -> tuple[int, str, str, int]:
    """Run a CLI inside the variant workspace with stdout/stderr to files (Windows-safe), hard-killing the tree on timeout."""
    out_path, err_path = cell_dir / "stdout.txt", cell_dir / "stderr.txt"
    start = time.monotonic()
    with open(out_path, "w", encoding="utf-8", errors="replace") as out, open(err_path, "w", encoding="utf-8", errors="replace") as err:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
            stdout=out,
            stderr=err,
            cwd=str(cwd),
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        try:
            proc.communicate(input=stdin_text, timeout=timeout)
        except subprocess.TimeoutExpired:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True, check=False)
            else:
                proc.kill()
            proc.wait()
            return 124, out_path.read_text(encoding="utf-8", errors="replace"), "TIMEOUT", int((time.monotonic() - start) * 1000)
    duration_ms = int((time.monotonic() - start) * 1000)
    return (
        proc.returncode,
        out_path.read_text(encoding="utf-8", errors="replace"),
        err_path.read_text(encoding="utf-8", errors="replace"),
        duration_ms,
    )


def first_json_object(text: str) -> dict:
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in output")
    obj, _ = json.JSONDecoder().raw_decode(text, start)
    return obj


def build_claude_command(exe: str, model: str | None) -> list[str]:
    command = [
        exe, "-p", "--safe-mode", "--no-session-persistence",
        "--permission-mode", "dontAsk", "--tools", "Read", "--allowedTools", "Read",
        "--output-format", "json",
    ]
    if model:
        command += ["--model", model]
    return command


def parse_claude(stdout: str) -> dict:
    data = first_json_object(stdout)
    usage = data.get("usage", {})
    return {
        "response": data.get("result", ""),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_read_tokens": usage.get("cache_read_input_tokens"),
        "cache_creation_tokens": usage.get("cache_creation_input_tokens"),
        "cost_usd": data.get("total_cost_usd"),
        "num_turns": data.get("num_turns"),
        "model": ",".join((data.get("modelUsage") or {}).keys()) or None,
        "usage_source": "cli-json",
        "cli_error": bool(data.get("is_error")),
    }


def build_codex_command(exe: str, model: str | None, workdir: Path) -> list[str]:
    command = [
        exe, "exec", "--json", "--cd", str(workdir),
        "--sandbox", "read-only",
        "--ephemeral", "--ignore-rules",
        "--skip-git-repo-check", "--color", "never",
        "-c", "project_doc_max_bytes=0",
    ]
    if model:
        command += ["-m", model]
    return command + ["-"]


def parse_codex(stdout: str) -> dict:
    totals = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "reasoning_output_tokens": 0}
    turns, texts = 0, []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            turns += 1
            for key in totals:
                totals[key] += (event.get("usage") or {}).get(key, 0) or 0
        elif event.get("type") == "item.completed" and (event.get("item") or {}).get("type") == "agent_message":
            texts.append(event["item"].get("text", ""))
    if turns == 0:
        raise ValueError("no turn.completed events in codex output")
    return {
        "response": "\n".join(texts),
        # codex cached_input_tokens is a SUBSET of input_tokens — never add them together.
        "input_tokens": totals["input_tokens"],
        "output_tokens": totals["output_tokens"] + totals["reasoning_output_tokens"],
        "cache_read_tokens": totals["cached_input_tokens"],
        "cache_creation_tokens": None,
        "cost_usd": None,
        "num_turns": turns,
        "model": None,
        "usage_source": "cli-json",
        "cli_error": False,
    }


def build_opencode_command(exe: str, model: str, workdir: Path) -> list[str]:
    command = [exe, "run", "--pure", "--model", model, "--format", "json", "--dir", str(workdir), "--agent", "plan"]
    # Windows CreateProcess caps command lines at ~32k chars, so the prompt goes in PROMPT.txt.
    return command + ["Follow the instructions in PROMPT.txt exactly and completely."]


def parse_opencode(stdout: str) -> dict:
    totals = {"input": 0, "output": 0, "reasoning": 0, "cache_read": 0, "cache_write": 0}
    cost, steps, texts, refs_seen = 0.0, 0, [], []
    saw_usage = False
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = event.get("part") or {}
        if event.get("type") == "text" and isinstance(part.get("text"), str):
            texts.append(part["text"])
        elif event.get("type") == "step_finish" or part.get("type") == "step-finish":
            tokens = part.get("tokens") or {}
            cache = tokens.get("cache") or {}
            totals["input"] += tokens.get("input", 0) or 0
            totals["output"] += tokens.get("output", 0) or 0
            totals["reasoning"] += tokens.get("reasoning", 0) or 0
            totals["cache_read"] += cache.get("read", 0) or 0
            totals["cache_write"] += cache.get("write", 0) or 0
            cost += part.get("cost", 0) or 0
            steps += 1
            saw_usage = True
        elif event.get("type") == "tool_use" and part.get("tool") == "read":
            path = str(((part.get("state") or {}).get("input") or {}).get("filePath", ""))
            if "references" in path:
                refs_seen.append(Path(path).name)
    response = "".join(texts).strip()
    if not saw_usage:
        # Known opencode bug: run --format json can exit before flushing the final step_finish.
        return {
            "response": response,
            "input_tokens": None,
            "output_tokens": est_tokens(response),
            "cache_read_tokens": None,
            "cache_creation_tokens": None,
            "cost_usd": None,
            "num_turns": steps or None,
            "model": None,
            "usage_source": "estimated",
            "cli_error": False,
            "refs_observed": sorted(set(refs_seen)),
        }
    return {
        "response": response,
        "input_tokens": totals["input"],
        "output_tokens": totals["output"] + totals["reasoning"],
        "cache_read_tokens": totals["cache_read"],
        "cache_creation_tokens": totals["cache_write"],
        "cost_usd": round(cost, 6) or None,
        "num_turns": steps,
        "model": None,
        "usage_source": "cli-json",
        "cli_error": False,
        "refs_observed": sorted(set(refs_seen)),
    }


def apply_checks(scenario: dict, response: str) -> dict[str, bool]:
    return {name: bool(re.search(pattern, response, re.IGNORECASE)) for name, pattern in scenario["checks"].items()}


def parse_self_reported_refs(response: str) -> list[str]:
    match = re.search(r"REFERENCES_READ:\s*(.+)", response, re.IGNORECASE)
    if not match or match.group(1).strip().lower().startswith("none"):
        return []
    return [chunk.strip() for chunk in match.group(1).split(",") if ".md" in chunk]


def build_prompt(ctx: dict, scenario: dict) -> str:
    if ctx["kind"] == "skill":
        return PREAMBLE.format(skill=ctx["context_text"], task=scenario["task"])
    if ctx["kind"] == "mcp-docs":
        return MCP_DOCS_PREAMBLE.format(url=MCP_DOCS_URL, docs=ctx["context_text"], task=scenario["task"])
    return VANILLA_PREAMBLE.format(task=scenario["task"])


def run_cell(agent: str, scenario: dict, variant: str, ctx: dict, rep: int, args, cells_dir: Path) -> dict:
    cell_id = cell_id_for(scenario["id"], agent, variant, rep)
    cell_dir = cells_dir / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)
    skill_dir = ctx["dir"]
    prompt = build_prompt(ctx, scenario)

    exe_name = "opencode" if agent in OPENCODE_MODELS else agent
    exe = shutil.which(exe_name) or (exe_name if args.dry_run else None)
    if exe is None:
        return {"cell": cell_id, "error": f"{exe_name} CLI not on PATH"}

    stdin_text: str | None = prompt
    cell_files: list[Path] = []  # written into the shared workspace; removed after the run so cells stay isolated
    if agent == "claude":
        command = build_claude_command(exe, args.model_claude)
    elif agent == "codex":
        command = build_codex_command(exe, args.model_codex, skill_dir)
    else:
        cell_files = [skill_dir / "PROMPT.txt", skill_dir / "opencode.json"]
        if not args.dry_run:  # a dry run must not touch the shared workspace
            (skill_dir / "PROMPT.txt").write_text(prompt, encoding="utf-8")
            permission = {"edit": "deny", "bash": "deny", "webfetch": "deny"}
            (skill_dir / "opencode.json").write_text(json.dumps({"permission": permission}), encoding="utf-8")
        command = build_opencode_command(exe, OPENCODE_MODELS[agent], skill_dir)
        stdin_text = None

    record = {
        "cell": cell_id,
        "scenario": scenario["id"],
        "agent": agent,
        "variant": variant,
        "rep": rep,
        "command": command,
    }
    if args.dry_run:
        return record | {"dry_run": True}

    try:
        code, stdout, stderr, duration_ms = run_cli(command, stdin_text, args.timeout, cell_dir, skill_dir)
    finally:
        for stale in cell_files:
            stale.unlink(missing_ok=True)
    record["duration_ms"] = duration_ms
    if code != 0:
        return record | {"error": f"exit {code}: {stderr.strip()[-500:]}"}
    try:
        parsed = {"claude": parse_claude, "codex": parse_codex}.get(agent, parse_opencode)(stdout)
    except (ValueError, json.JSONDecodeError) as exc:
        return record | {"error": f"unparseable output: {exc}"}
    if parsed.get("cli_error"):  # agent reported an error with a zero exit code; do not score it
        return record | {"error": f"agent reported error: {str(parsed.get('response') or '').strip()[-500:]}"}

    response = parsed.pop("response", "")
    (cell_dir / "response.txt").write_text(response, encoding="utf-8")
    checks = apply_checks(scenario, response)
    total_in = (parsed.get("input_tokens") or 0) + (parsed.get("cache_read_tokens") or 0) + (parsed.get("cache_creation_tokens") or 0)
    if agent == "codex":
        total_in = parsed.get("input_tokens") or 0  # cached subset already inside input_tokens
    return record | parsed | {
        "response_chars": len(response),
        "total_input_tokens": total_in or None,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "refs_self_reported": parse_self_reported_refs(response),
    }


def median_of(cells: list[dict], key: str):
    values = [c[key] for c in cells if isinstance(c.get(key), (int, float))]
    return round(statistics.median(values), 4) if values else None


def summarize(cells: list[dict]) -> dict:
    groups: dict[tuple, list[dict]] = {}
    for cell in cells:
        if cell.get("error") or cell.get("dry_run"):
            continue
        groups.setdefault((cell["scenario"], cell["agent"], cell["variant"]), []).append(cell)
    summary = {}
    for (scenario, agent, variant), group in sorted(groups.items()):
        summary.setdefault(scenario, {}).setdefault(agent, {})[variant] = {
            "runs": len(group),
            "median_total_input_tokens": median_of(group, "total_input_tokens"),
            "median_output_tokens": median_of(group, "output_tokens"),
            "median_cost_usd": median_of(group, "cost_usd"),
            "median_duration_ms": median_of(group, "duration_ms"),
            "median_response_chars": median_of(group, "response_chars"),
            "checks_rate": round(sum(c["checks_passed"] for c in group) / max(1, sum(c["checks_total"] for c in group)), 3),
        }
    return summary


def delta(baseline, current):
    if not isinstance(baseline, (int, float)) or not isinstance(current, (int, float)) or baseline == 0:
        return ""
    return f"{(current - baseline) / baseline * 100:+.1f}%"


def write_markdown(out_dir: Path, static: dict, summary: dict, variants: list[str], errors: list[dict]) -> None:
    lines = [f"# pixellab-pip skill benchmark ({out_dir.name})", ""]
    first_col, last_col = variant_label(variants[0]), variant_label(variants[-1])
    lines += [
        f"Columns: {', '.join(variant_label(v) for v in variants)} (first is always the working-tree Pip skill). Delta compares the last column ({last_col}) against {first_col}. Static tokens are chars/4 estimates.",
        "",
        "## Static context size (estimated tokens)",
        "",
        "| Scope | " + " | ".join(variant_label(v) for v in variants) + " | delta |",
        "|---|" + "---|" * (len(variants) + 1),
    ]
    context_row = [static["variants"][v]["context_est_tokens"] for v in variants]
    lines.append("| Injected context (SKILL.md / MCP docs / none) | " + " | ".join(map(str, context_row)) + f" | {delta(context_row[0], context_row[-1])} |")
    total_row = [static["variants"][v]["total_est_tokens"] for v in variants]
    lines.append("| Context + all skill references | " + " | ".join(map(str, total_row)) + f" | {delta(total_row[0], total_row[-1])} |")
    for scenario_id, row in static["scenarios"].items():
        values = [row[v]["context_est_tokens"] for v in variants]
        lines.append(f"| scenario {scenario_id} (context + expected refs) | " + " | ".join(map(str, values)) + f" | {delta(values[0], values[-1])} |")
    if summary:
        lines += ["", "## Agent sessions (medians)", ""]
        lines += ["| Scenario | Agent | Metric | " + " | ".join(variant_label(v) for v in variants) + " | delta |", "|---|---|---|" + "---|" * (len(variants) + 1)]
        for scenario_id, agents in summary.items():
            for agent, per_variant in agents.items():
                for metric in ("median_total_input_tokens", "median_output_tokens", "median_cost_usd", "median_duration_ms", "checks_rate"):
                    values = [per_variant.get(v, {}).get(metric) for v in variants]
                    if all(value is None for value in values):
                        continue
                    cells = " | ".join("" if value is None else (_fmt_pct(value) if metric == "checks_rate" else str(value)) for value in values)
                    lines.append(f"| {scenario_id} | {agent} | {metric.replace('median_', '')} | {cells} | {delta(values[0], values[-1])} |")
    if errors:
        lines += ["", "## Errors", ""] + [f"- `{e['cell']}`: {e['error']}" for e in errors]
    (out_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# Markers in the published report (docs/pixellab-pip-benchmark.md); --report rewrites only between them.
REPORT_MARK_START = "<!-- BENCHMARK:GENERATED:START -->"
REPORT_MARK_END = "<!-- BENCHMARK:GENERATED:END -->"


def _fmt_int(x) -> str:
    return "" if not isinstance(x, (int, float)) else f"{int(round(x)):,}"


def _fmt_pct(x) -> str:  # checks_rate is a 0..1 fraction of checks passed; show it as a human percent
    return "" if not isinstance(x, (int, float)) else f"{round(x * 100)}%"


def render_report_block(static: dict, summary: dict, variants: list[str], agents: list[str], reps: int, stamp: str) -> str:
    """Render the data tables spliced into the published report; prose lives outside the markers."""
    date = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}"
    cols = " | ".join(variant_label(v) for v in variants)
    agent_note = ", ".join(agents) if summary else "none (static only)"
    lines = [
        f"_Auto-generated by `dev-tools/skill_benchmark.py --report` on {date} — "
        f"agents: {agent_note}; {reps} rep(s). Edits inside this block are overwritten on the next run._",
        "",
        "### Context size (estimated tokens, chars/4)",
        "",
        f"| Scope | {cols} |",
        "|---|" + "---|" * len(variants),
    ]
    ctx = [static["variants"][v]["context_est_tokens"] for v in variants]
    lines.append("| Injected context (SKILL.md / MCP docs / none) | " + " | ".join(_fmt_int(c) for c in ctx) + " |")
    for sid, row in static["scenarios"].items():
        lines.append(f"| {sid} | " + " | ".join(_fmt_int(row[v]["context_est_tokens"]) for v in variants) + " |")
    if summary:
        lines += [
            "",
            "### Routing correctness and session input (medians)",
            "",
            f"| Scenario | Agent | Metric | {cols} |",
            "|---|---|---|" + "---|" * len(variants),
        ]
        # Group by metric (all input-token rows, then all routing-correct rows) so each metric reads down one block.
        for sid, per_agent in summary.items():
            for agent, per_variant in per_agent.items():
                inp = [per_variant.get(v, {}).get("median_total_input_tokens") for v in variants]
                lines.append(f"| {sid} | {agent} | input tokens | " + " | ".join(_fmt_int(x) for x in inp) + " |")
        for sid, per_agent in summary.items():
            for agent, per_variant in per_agent.items():
                cr = [per_variant.get(v, {}).get("checks_rate") for v in variants]
                lines.append(f"| {sid} | {agent} | routing correct | " + " | ".join(_fmt_pct(x) for x in cr) + " |")
    return "\n".join(lines)


def write_report_doc(report_path: Path, block: str) -> None:
    if not report_path.is_file():
        raise SystemExit(f"--report file not found: {report_path}")
    text = report_path.read_text(encoding="utf-8")
    if text.count(REPORT_MARK_START) != 1 or text.count(REPORT_MARK_END) != 1 or text.index(REPORT_MARK_START) > text.index(REPORT_MARK_END):
        raise SystemExit(f"{report_path} needs exactly one {REPORT_MARK_START} before one {REPORT_MARK_END}")
    pre = text.split(REPORT_MARK_START, 1)[0]
    post = text.split(REPORT_MARK_END, 1)[1]
    report_path.write_text(f"{pre}{REPORT_MARK_START}\n{block}\n{REPORT_MARK_END}{post}", encoding="utf-8")


def rescore(out_dir: Path, report: str | None = None) -> None:
    cells = json.loads((out_dir / "results.json").read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in SCENARIOS}
    for cell in cells:
        response_file = out_dir / "cells" / cell["cell"] / "response.txt"
        if cell.get("error") or not response_file.is_file() or cell["scenario"] not in by_id:
            continue
        response = response_file.read_text(encoding="utf-8")
        checks = apply_checks(by_id[cell["scenario"]], response)
        cell.update(checks=checks, checks_passed=sum(checks.values()), checks_total=len(checks))
    (out_dir / "results.json").write_text(json.dumps(cells, indent=2), encoding="utf-8")
    static = json.loads((out_dir / "static.json").read_text(encoding="utf-8"))
    meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
    summary = summarize(cells)
    write_markdown(out_dir, static, summary, meta["variants"], [c for c in cells if c.get("error")])
    print(f"Rescored {out_dir / 'SUMMARY.md'}")
    if report and summary:
        write_report_doc(Path(report), render_report_block(static, summary, meta["variants"], meta.get("agents", []), meta.get("reps", 1), meta["stamp"]))
        print(f"Report updated: {report}")
    elif report:
        print(f"Not updating {report}: the run has no successful agent cells (report left unchanged).")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--agents", default="claude", help=f"comma list from: {', '.join(AGENTS)}")
    parser.add_argument(
        "--variants",
        default=DEFAULT_BASELINE,
        help="comma list of what to compare the current skill against: git refs, 'vanilla' (no context), or 'mcp-docs' (official https://api.pixellab.ai/mcp/docs injected). The current working-tree skill is always the first column.",
    )
    parser.add_argument("--scenarios", default="", help="comma list of scenario ids (default: all applicable)")
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=300, help="seconds per agent run")
    parser.add_argument("--static", action="store_true", help="static context comparison only; no CLI calls")
    parser.add_argument("--dry-run", action="store_true", help="print planned CLI commands without executing")
    parser.add_argument("--list", action="store_true", help="list scenarios and exit")
    parser.add_argument("--rescore", metavar="DIR", help="recompute checks/summary for a previous results dir")
    parser.add_argument("--resume", metavar="DIR", help="continue a prior run dir: reuse its successful cells, re-run errored/missing ones")
    parser.add_argument("--report", metavar="FILE", help="rewrite the data tables in a published report markdown (between its BENCHMARK:GENERATED markers)")
    parser.add_argument("--out", default=str(REPO / ".local" / "bench"), help="results base dir")
    parser.add_argument("--model-claude", default=None, help="pin claude model id")
    parser.add_argument("--model-codex", default=None, help="pin codex model id")
    args = parser.parse_args()

    if args.list:
        for scenario in SCENARIOS:
            print(f"{scenario['id']}: {scenario['task'][:100]}")
        return 0
    if args.rescore:
        rescore(Path(args.rescore), args.report)
        return 0

    wanted = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    scenarios = [s for s in SCENARIOS if not wanted or s["id"] in wanted]
    unknown = set(wanted) - {s["id"] for s in scenarios}
    if unknown:
        raise SystemExit(f"unknown scenarios: {', '.join(sorted(unknown))}")

    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    # The current working-tree skill is the subject of every benchmark, so it is always the
    # first column; --variants only names what to compare it against.
    variants = ["current"] + [v for v in variants if v != "current"]
    agents = [a.strip() for a in args.agents.split(",") if a.strip()]
    bad_agents = set(agents) - set(AGENTS)
    if bad_agents:
        raise SystemExit(f"unknown agents: {', '.join(sorted(bad_agents))}")

    stamp = utc_stamp()
    if args.resume:
        out_dir = Path(args.resume)
        if not (out_dir / "results.json").is_file():
            raise SystemExit(f"--resume dir has no results.json to continue from: {out_dir}")
    else:
        out_dir = Path(args.out) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    completed = load_completed(out_dir) if args.resume else {}
    if args.resume:
        print(f"Resuming {out_dir}: reusing {len(completed)} completed cell(s), re-running errored/missing ones.")
    # Workspaces live OUTSIDE the repo so parent-dir CLAUDE.md/AGENTS.md cannot contaminate runs.
    work_base = Path(tempfile.mkdtemp(prefix=f"pixellab-pip-bench-{stamp}-"))
    try:
        contexts = build_contexts(variants, work_base, out_dir)
        print(f"Workspaces: {work_base}")

        static = static_report(contexts)
        (out_dir / "static.json").write_text(json.dumps(static, indent=2), encoding="utf-8")
        (out_dir / "meta.json").write_text(
            json.dumps({"stamp": stamp, "variants": variants, "agents": agents, "reps": args.reps,
                        "scenarios": [s["id"] for s in scenarios], "argv": sys.argv[1:]}, indent=2),
            encoding="utf-8",
        )

        cells: list[dict] = []
        if not args.static:
            cells_dir = out_dir / "cells"
            total = len(scenarios) * len(agents) * len(variants) * args.reps
            done = 0
            # Interleave variants inside each rep so provider-side caching effects hit both arms alike.
            for rep in range(1, args.reps + 1):
                for scenario in scenarios:
                    for agent in agents:
                        for variant in variants:
                            done += 1
                            reused = completed.get(cell_id_for(scenario["id"], agent, variant, rep))
                            print(f"[{done}/{total}] {scenario['id']} / {agent} / {variant} / rep {rep}"
                                  + (" (cached)" if reused else ""), flush=True)
                            cells.append(reused if reused is not None
                                         else run_cell(agent, scenario, variant, contexts[variant], rep, args, cells_dir))
                            # Checkpoint after every cell so an interrupt/crash keeps completed work for --rescore/--resume.
                            (out_dir / "results.json").write_text(json.dumps(cells, indent=2), encoding="utf-8")

        errors = [c for c in cells if c.get("error")]
        summary = summarize(cells)
        write_markdown(out_dir, static, summary, variants, errors)
        # Only rewrite the published report when there is real routing data; never clobber it with an
        # empty/context-only block (e.g. every cell errored, or a --static run).
        if args.report and summary:
            write_report_doc(Path(args.report), render_report_block(static, summary, variants, agents, args.reps, stamp))
    finally:
        shutil.rmtree(work_base, ignore_errors=True)  # never leak the temp workspace, even on error
    print(f"\nResults: {out_dir / 'SUMMARY.md'}")
    if args.report and summary:
        print(f"Report updated: {args.report}")
    elif args.report:
        print(f"Not updating {args.report}: no successful agent cells this run (report left unchanged).")
    used = [c for c in cells if not c.get("error") and not c.get("dry_run")]
    if used:
        tin = sum(c.get("total_input_tokens") or 0 for c in used)
        tout = sum(c.get("output_tokens") or 0 for c in used)
        tcost = sum(c.get("cost_usd") or 0 for c in used)
        cost_note = f", ~${tcost:.2f} where the CLI exposed cost" if tcost else ""
        print(f"Agent usage this run: ~{tin:,} input + ~{tout:,} output tokens across {len(used)} cell(s){cost_note}")
    # The README benchmark table is hand-maintained; when a report was refreshed interactively,
    # hand the user a ready-to-paste prompt so their agent can update it from the report.
    if args.report and summary and sys.stdout.isatty():
        print("\n--- Copy this to your coding agent to refresh the README benchmark table ---")
        print(f"Refresh the README benchmark table (routing % and up-front context) from the latest {args.report}, and make sure the README Benchmark section links to that report.")
        print("---------------------------------------------------------------------------")
    if errors:
        print(f"{len(errors)} cell(s) errored — see SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
