#!/usr/bin/env python3
"""Benchmark pixellab-pip skill token/context usage across agent CLIs and skill versions.

Compares how much agent-side context/tokens the skill costs (SKILL.md injection +
progressively loaded references/*.md) between git variants of the skill, e.g. the
pre-KISS/YAGNI tag vs the current working tree, across claude / codex / opencode
(deepseek-v4-pro) CLIs. It measures the agent session only — never PixelLab credits.

Modes:
  --static            deterministic context-size comparison, no CLI calls (free)
  (default)           live agent runs; dry scenarios make no network/PixelLab calls
  --live              adds scenarios that call the PixelLab REST API (needs PIXELLAB_SECRET;
                      only the free GET /balance scenario unless --allow-paid)
  --rescore DIR       recompute checks/summary from a previous run without CLI calls

Examples:
  python dev-tools/skill_benchmark.py --static
  python dev-tools/skill_benchmark.py --agents claude --reps 3
  python dev-tools/skill_benchmark.py --agents claude,codex,deepseek-v4-pro --scenarios route-hex-tiles,report-format
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

# ponytail: no pricing table — report native cost where the CLI exposes it, tokens otherwise.

PREAMBLE = """You are a coding agent with the "pixellab-pip" Agent Skill loaded. Its SKILL.md is included below. The skill's reference files exist under references/*.md in your current working directory; read a reference file with your file-read tool only when SKILL.md's routing requires it for this request. {network_rule}

Follow the skill exactly. End your reply with one final line:
REFERENCES_READ: <comma-separated references/*.md paths you actually read, or none>

--- SKILL.md ---
{skill}
--- END SKILL.md ---

User request: {task}"""

VANILLA_PREAMBLE = """You are a coding agent helping a user with PixelLab, the pixel-art generation service at api.pixellab.ai. {network_rule}

User request: {task}"""

MCP_DOCS_PREAMBLE = """You are a coding agent helping a user with PixelLab, the pixel-art generation service. The official PixelLab MCP documentation from {url} is included below. {network_rule}

--- PIXELLAB MCP DOCS ---
{docs}
--- END DOCS ---

User request: {task}"""

DRY_RULE = "Do not make any network, PixelLab API, or MCP calls; this is an answer/planning exercise only."
LIVE_RULE = (
    "You may call the public PixelLab REST v2 API with the bearer token in the PIXELLAB_SECRET "
    "environment variable. Never print or echo the token."
)

# checks are case-insensitive regexes that must match the response (routing correctness gate).
# refs_any lists filename substrings acceptable across BOTH skill variants (old and new names).
SCENARIOS = [
    {
        "id": "route-hex-tiles",
        "task": "Which PixelLab tool should generate hex terrain tile variants? Answer briefly with the exact tool/endpoint.",
        "checks": {"tiles-pro": r"create[_-]tiles[_-]pro"},
        "refs_any": [],
    },
    {
        "id": "route-character",
        "task": "I want an NPC goblin sprite with a walk animation via PixelLab. Which tools/endpoints, in what order? Brief plan only; call nothing.",
        "checks": {"create": r"create[_-]character", "animate": r"animate[_-]character|characters/animations", "south": r"south"},
        "refs_any": [],
    },
    {
        "id": "plan-item-icon-sheet",
        "task": "Plan the exact PixelLab REST request (endpoint plus JSON body) for a transparent 8x8 sheet of 64 RPG inventory item icons at 32px per icon. Plan only; call nothing.",
        "checks": {"endpoint": r"generate-image-v2", "canvas": r"256", "alpha": r"no_background"},
        "refs_any": ["icons.md", "item-icons.md"],
    },
    {
        "id": "cheap-animation",
        "task": "What is the cheapest way to add a walk animation to my existing managed PixelLab character? Brief answer naming the mode and its documented cost.",
        "checks": {"template": r"template", "cost": r"1\s*(generation|gen)"},
        "refs_any": ["cost-routing.md"],
    },
    {
        "id": "report-format",
        "task": (
            "A live PixelLab job just finished; produce the final user report exactly as the skill specifies. "
            "Data: route REST POST /v2/generate-image-v2; description sent 'fantasy sword icon, clear silhouette'; "
            "seed 774421; image_size 64x64; no_background true; file pixellab-pip-generations/sword/icon.png; "
            "balance before 102.40 after 102.15; verification: dimensions 64x64 OK, transparent background OK."
        ),
        "checks": {"prompt": r"fantasy sword icon", "seed": r"774421", "cost": r"102\.15|0\.25", "route": r"generate-image-v2"},
        "refs_any": ["usage-reporting.md"],
    },
    {
        "id": "setup-codex",
        "task": "How do I set up PixelLab MCP for the Codex CLI without exposing my token? Instructions only; change nothing.",
        "checks": {"envvar": r"PIXELLAB_SECRET", "tokenfree": r"bearer-token-env-var|token[- ]free|secret setting"},
        "refs_any": ["setup.md", "credentials.md"],
    },
    {
        "id": "refuse-internal-endpoint",
        "task": "Use /tilesets/create on api.pixellab.ai with my browser session token to make a tileset.",
        "checks": {"refusal": r"refus\w*|declin\w*|can(?:not|'?t)|won'?t|unsupported|undocumented|not (?:a )?(?:public|supported|documented|valid)|isn'?t (?:a )?(?:public|supported|documented)|use the public", "reroute": r"create[_-](topdown|sidescroller)[_-]tileset"},
        "refs_any": [],
    },
    {
        "id": "skeleton-pipeline",
        "task": "Auto-rig my sprite and animate it from the skeleton via the PixelLab API. Which endpoints, in what order? Brief.",
        "checks": {"estimate": r"estimate-skeleton", "animate": r"animate-with-skeleton"},
        "refs_any": ["preset-skeleton-template-animations.md"],
    },
    {
        "id": "live-balance",
        "task": "Check my PixelLab account balance using the REST API and report it per the skill.",
        "checks": {"balance": r"balance|credits", "number": r"\d"},
        "refs_any": ["usage-reporting.md"],
        "live": True,
    },
    {
        "id": "live-cheap-image",
        "task": (
            "Generate one 32x32 pixel-art red potion icon using the cheapest suitable PixelLab REST route, "
            "then report route, prompt, and cost per the skill. Do not save files."
        ),
        "checks": {"route": r"pixen|pixflux", "report": r"cost|usage|balance"},
        "refs_any": ["cost-routing.md", "usage-reporting.md"],
        "live": True,
        "paid": True,
    },
]


def est_tokens(text: str) -> int:
    return len(text) // 4  # ponytail: chars/4 heuristic, labeled estimated everywhere it appears


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


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


def build_claude_command(exe: str, model: str | None, live: bool) -> list[str]:
    tools = "Read,Bash" if live else "Read"
    command = [
        exe, "-p", "--safe-mode", "--no-session-persistence",
        "--permission-mode", "dontAsk", "--tools", tools, "--allowedTools", tools,
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


def build_codex_command(exe: str, model: str | None, live: bool, workdir: Path) -> list[str]:
    command = [
        exe, "exec", "--json", "--cd", str(workdir),
        "--sandbox", "danger-full-access" if live else "read-only",
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


def build_opencode_command(exe: str, model: str, live: bool, workdir: Path) -> list[str]:
    command = [exe, "run", "--pure", "--model", model, "--format", "json", "--dir", str(workdir)]
    if not live:
        command += ["--agent", "plan"]
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
    network_rule = LIVE_RULE if scenario.get("live") else DRY_RULE
    if ctx["kind"] == "skill":
        return PREAMBLE.format(network_rule=network_rule, skill=ctx["context_text"], task=scenario["task"])
    if ctx["kind"] == "mcp-docs":
        return MCP_DOCS_PREAMBLE.format(url=MCP_DOCS_URL, network_rule=network_rule, docs=ctx["context_text"], task=scenario["task"])
    return VANILLA_PREAMBLE.format(network_rule=network_rule, task=scenario["task"])


def run_cell(agent: str, scenario: dict, variant: str, ctx: dict, rep: int, args, cells_dir: Path) -> dict:
    cell_id = f"{scenario['id']}__{agent}__{variant.replace('/', '-')}__r{rep}"
    cell_dir = cells_dir / cell_id
    cell_dir.mkdir(parents=True, exist_ok=True)
    live = bool(scenario.get("live"))
    skill_dir = ctx["dir"]
    prompt = build_prompt(ctx, scenario)

    exe_name = "opencode" if agent in OPENCODE_MODELS else agent
    exe = shutil.which(exe_name) or (exe_name if args.dry_run else None)
    if exe is None:
        return {"cell": cell_id, "error": f"{exe_name} CLI not on PATH"}

    stdin_text: str | None = prompt
    cell_files: list[Path] = []  # written into the shared workspace; removed after the run so cells stay isolated
    if agent == "claude":
        command = build_claude_command(exe, args.model_claude, live)
    elif agent == "codex":
        command = build_codex_command(exe, args.model_codex, live, skill_dir)
    else:
        cell_files = [skill_dir / "PROMPT.txt", skill_dir / "opencode.json"]
        if not args.dry_run:  # a dry run must not touch the shared workspace
            (skill_dir / "PROMPT.txt").write_text(prompt, encoding="utf-8")
            permission = {"edit": "deny", "bash": "allow" if live else "deny", "webfetch": "allow" if live else "deny"}
            (skill_dir / "opencode.json").write_text(json.dumps({"permission": permission}), encoding="utf-8")
        command = build_opencode_command(exe, OPENCODE_MODELS[agent], live, skill_dir)
        stdin_text = None

    record = {
        "cell": cell_id,
        "scenario": scenario["id"],
        "agent": agent,
        "variant": variant,
        "rep": rep,
        "live": live,
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
    first_col, last_col = variants[0], variants[-1]
    lines += [
        f"Columns: {', '.join(f'`{v}`' for v in variants)} (first is always the current working-tree skill). Delta compares the last column (`{last_col}`) against `{first_col}`. Static tokens are chars/4 estimates.",
        "",
        "## Static context size (estimated tokens)",
        "",
        "| Scope | " + " | ".join(variants) + " | delta |",
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
        lines += ["| Scenario | Agent | Metric | " + " | ".join(variants) + " | delta |", "|---|---|---|" + "---|" * (len(variants) + 1)]
        for scenario_id, agents in summary.items():
            for agent, per_variant in agents.items():
                for metric in ("median_total_input_tokens", "median_output_tokens", "median_cost_usd", "median_duration_ms", "checks_rate"):
                    values = [per_variant.get(v, {}).get(metric) for v in variants]
                    if all(value is None for value in values):
                        continue
                    cells = " | ".join("" if value is None else str(value) for value in values)
                    lines.append(f"| {scenario_id} | {agent} | {metric.replace('median_', '')} | {cells} | {delta(values[0], values[-1])} |")
    if errors:
        lines += ["", "## Errors", ""] + [f"- `{e['cell']}`: {e['error']}" for e in errors]
    (out_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rescore(out_dir: Path) -> None:
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
    variants = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))["variants"]
    write_markdown(out_dir, static, summarize(cells), variants, [c for c in cells if c.get("error")])
    print(f"Rescored {out_dir / 'SUMMARY.md'}")


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
    parser.add_argument("--live", action="store_true", help="include live PixelLab scenarios (requires PIXELLAB_SECRET)")
    parser.add_argument("--allow-paid", action="store_true", help="also run credit-spending live scenarios")
    parser.add_argument("--dry-run", action="store_true", help="print planned CLI commands without executing")
    parser.add_argument("--list", action="store_true", help="list scenarios and exit")
    parser.add_argument("--rescore", metavar="DIR", help="recompute checks/summary for a previous results dir")
    parser.add_argument("--out", default=str(REPO / ".local" / "bench"), help="results base dir")
    parser.add_argument("--model-claude", default=None, help="pin claude model id")
    parser.add_argument("--model-codex", default=None, help="pin codex model id")
    args = parser.parse_args()

    if args.list:
        for scenario in SCENARIOS:
            flags = " [live]" if scenario.get("live") else ""
            flags += " [paid]" if scenario.get("paid") else ""
            print(f"{scenario['id']}{flags}: {scenario['task'][:100]}")
        return 0
    if args.rescore:
        rescore(Path(args.rescore))
        return 0

    import os

    wanted = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    scenarios = [s for s in SCENARIOS if not wanted or s["id"] in wanted]
    unknown = set(wanted) - {s["id"] for s in scenarios}
    if unknown:
        raise SystemExit(f"unknown scenarios: {', '.join(sorted(unknown))}")
    if not args.static:
        skipped = []
        if not args.live or not os.environ.get("PIXELLAB_SECRET"):
            skipped += [s["id"] for s in scenarios if s.get("live")]
            scenarios = [s for s in scenarios if not s.get("live")]
        elif not args.allow_paid:
            skipped += [s["id"] for s in scenarios if s.get("paid")]
            scenarios = [s for s in scenarios if not s.get("paid")]
        if skipped:
            print(f"Skipping (needs --live + PIXELLAB_SECRET, paid also needs --allow-paid): {', '.join(skipped)}")

    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    # The current working-tree skill is the subject of every benchmark, so it is always the
    # first column; --variants only names what to compare it against.
    variants = ["current"] + [v for v in variants if v != "current"]
    agents = [a.strip() for a in args.agents.split(",") if a.strip()]
    bad_agents = set(agents) - set(AGENTS)
    if bad_agents:
        raise SystemExit(f"unknown agents: {', '.join(sorted(bad_agents))}")

    stamp = utc_stamp()
    out_dir = Path(args.out) / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
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
                            print(f"[{done}/{total}] {scenario['id']} / {agent} / {variant} / rep {rep}", flush=True)
                            cells.append(run_cell(agent, scenario, variant, contexts[variant], rep, args, cells_dir))
            (out_dir / "results.json").write_text(json.dumps(cells, indent=2), encoding="utf-8")

        errors = [c for c in cells if c.get("error")]
        write_markdown(out_dir, static, summarize(cells), variants, errors)
    finally:
        shutil.rmtree(work_base, ignore_errors=True)  # never leak the temp workspace, even on error
    print(f"\nResults: {out_dir / 'SUMMARY.md'}")
    if errors:
        print(f"{len(errors)} cell(s) errored — see SUMMARY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
