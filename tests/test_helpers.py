from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


background_removal = load_module(
    "background_removal",
    REPO_ROOT / "skills/pixellab-pip/assets/background_removal.py",
)
bark = load_module("bark", REPO_ROOT / "skills/pixellab-pip/assets/bark.py")
tileset_sim = load_module(
    "pixellab_mcp_tileset_sim",
    REPO_ROOT / "dev-tools/pixellab_mcp_tileset_sim.py",
)
skill_benchmark = load_module(
    "skill_benchmark",
    REPO_ROOT / "dev-tools/skill_benchmark.py",
)


class BackgroundRemovalTests(unittest.TestCase):
    def test_edge_background_removed_without_repainting_sprite(self) -> None:
        Image = background_removal.Image
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.png"
            target = Path(tmp) / "target.png"
            image = Image.new("RGBA", (5, 5), (255, 255, 255, 255))
            for y in range(1, 4):
                for x in range(1, 4):
                    image.putpixel((x, y), (10, 20, 30, 255))
            image.save(source)

            args = background_removal.build_parser().parse_args([str(source), str(target)])
            report = background_removal.remove_background(args)

            out = Image.open(target).convert("RGBA")
            self.assertEqual(report["local_result_status"], "passed_conservative_checks")
            self.assertEqual(out.getpixel((0, 0)), (255, 255, 255, 0))
            self.assertEqual(out.getpixel((2, 2)), (10, 20, 30, 255))

    def test_enclosed_background_like_pixels_require_fallback(self) -> None:
        Image = background_removal.Image
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.png"
            target = Path(tmp) / "target.png"
            image = Image.new("RGBA", (7, 7), (255, 255, 255, 255))
            for y in range(1, 6):
                for x in range(1, 6):
                    image.putpixel((x, y), (0, 0, 0, 255))
            for y in range(2, 5):
                for x in range(2, 5):
                    image.putpixel((x, y), (255, 255, 255, 255))
            image.save(source)

            args = background_removal.build_parser().parse_args([str(source), str(target)])
            report = background_removal.remove_background(args)

            self.assertEqual(report["local_result_status"], "needs_pixellab_fallback")
            self.assertIn("remaining_background_like_pixels", report["fallback_reasons"])
            self.assertGreater(report["significant_unresolved_enclosed_component_count"], 0)


class BarkConfigTests(unittest.TestCase):
    def test_write_config_uses_skill_config_first_and_preserves_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            original_skill_config = bark.SKILL_CONFIG
            try:
                bark.SKILL_CONFIG = Path(tmp) / "pixellab-pip.json"
                bark.SKILL_CONFIG.write_text('{"other": 7, "bark": true}\n', encoding="utf-8")

                written = bark.write_config(False)
                data = json.loads(written.read_text(encoding="utf-8"))

                self.assertEqual(written, bark.SKILL_CONFIG)
                self.assertEqual(data, {"bark": False, "other": 7})
            finally:
                bark.SKILL_CONFIG = original_skill_config

    def test_non_bool_skill_config_falls_back_to_valid_user_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            original_skill_config = bark.SKILL_CONFIG
            original_user_config_path = bark.user_config_path
            try:
                root = Path(tmp)
                bark.SKILL_CONFIG = root / "skill" / "pixellab-pip.json"
                user_config = root / "user" / "pixellab-pip.json"
                bark.SKILL_CONFIG.parent.mkdir()
                user_config.parent.mkdir()
                bark.SKILL_CONFIG.write_text('{"bark": "false"}\n', encoding="utf-8")
                user_config.write_text('{"bark": false}\n', encoding="utf-8")
                bark.user_config_path = lambda: user_config

                data, source, invalid_source = bark.read_config()

                self.assertEqual(data["bark"], False)
                self.assertEqual(source, user_config)
                self.assertEqual(invalid_source, bark.SKILL_CONFIG)
                self.assertFalse(bark.bark_enabled())
            finally:
                bark.SKILL_CONFIG = original_skill_config
                bark.user_config_path = original_user_config_path


class HelperCliSmokeTests(unittest.TestCase):
    def run_help(self, script: Path) -> str:
        completed = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return completed.stdout

    def test_doc_watch_help(self) -> None:
        output = self.run_help(REPO_ROOT / "dev-tools/pixellab-doc-watch.py")
        self.assertIn("usage:", output.lower())
        self.assertIn("refresh", output)

    def test_tileset_simulator_help(self) -> None:
        output = self.run_help(REPO_ROOT / "dev-tools/pixellab_mcp_tileset_sim.py")
        self.assertIn("usage:", output.lower())
        self.assertIn("create_topdown_tileset", output)
        self.assertIn("claude", output.lower())

    def test_skill_benchmark_help(self) -> None:
        output = self.run_help(REPO_ROOT / "dev-tools/skill_benchmark.py")
        self.assertIn("usage:", output.lower())
        self.assertIn("--static", output)
        self.assertIn("--live", output)

    def test_skill_benchmark_cells_run_in_workspace_with_valid_commands(self) -> None:
        import argparse

        scenario = skill_benchmark.SCENARIOS[0]  # route-hex-tiles; check expects create_tiles_pro
        fake_stdout = {
            "claude": json.dumps(
                {
                    "result": "Use create_tiles_pro.\nREFERENCES_READ: none",
                    "usage": {
                        "input_tokens": 100,
                        "output_tokens": 10,
                        "cache_read_input_tokens": 5,
                        "cache_creation_input_tokens": 2,
                    },
                    "total_cost_usd": 0.01,
                    "num_turns": 1,
                    "modelUsage": {"claude-test": {}},
                }
            ),
            "codex": "\n".join(
                [
                    json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "create_tiles_pro"}}),
                    json.dumps(
                        {
                            "type": "turn.completed",
                            "usage": {
                                "input_tokens": 100,
                                "cached_input_tokens": 50,
                                "output_tokens": 10,
                                "reasoning_output_tokens": 0,
                            },
                        }
                    ),
                ]
            ),
            "deepseek-v4-pro": "\n".join(
                [
                    json.dumps({"type": "text", "part": {"text": "create_tiles_pro"}}),
                    json.dumps(
                        {
                            "type": "step_finish",
                            "part": {
                                "type": "step-finish",
                                "tokens": {"input": 100, "output": 10, "reasoning": 0, "cache": {"read": 1, "write": 2}},
                                "cost": 0.001,
                            },
                        }
                    ),
                ]
            ),
        }
        captured: dict[str, dict] = {}

        def fake_run_cli(command, stdin_text, timeout, cell_dir, cwd):
            agent = captured["current"]
            captured[agent] = {"command": command, "cwd": Path(cwd), "stdin": stdin_text}
            return 0, fake_stdout[agent], "", 7

        args = argparse.Namespace(dry_run=False, timeout=5, model_claude=None, model_codex=None)
        original_which = skill_benchmark.shutil.which
        original_run_cli = skill_benchmark.run_cli
        try:
            skill_benchmark.shutil.which = lambda name: f"C:/fake/{name}.cmd"
            skill_benchmark.run_cli = fake_run_cli
            with tempfile.TemporaryDirectory() as tmp:
                skill_dir = Path(tmp) / "skill"
                skill_dir.mkdir()
                (skill_dir / "SKILL.md").write_text("skill body", encoding="utf-8")
                ctx = {"kind": "skill", "dir": skill_dir, "context_text": "skill body", "files": {}}
                cells_dir = Path(tmp) / "cells"
                cells: dict[str, dict] = {}
                for agent in ("claude", "codex", "deepseek-v4-pro"):
                    captured["current"] = agent
                    cells[agent] = skill_benchmark.run_cell(agent, scenario, "worktree", ctx, 1, args, cells_dir)
                    self.assertNotIn("error", cells[agent], msg=str(cells[agent]))
                    self.assertEqual(cells[agent]["checks_passed"], cells[agent]["checks_total"])
                self.assertIn("skill body", captured["claude"]["stdin"])
                # vanilla arm: no skill text injected
                captured["current"] = "claude"
                vanilla_ctx = {"kind": "vanilla", "dir": skill_dir, "context_text": "", "files": {}}
                vanilla_cell = skill_benchmark.run_cell("claude", scenario, "vanilla", vanilla_ctx, 1, args, cells_dir)
                self.assertNotIn("error", vanilla_cell, msg=str(vanilla_cell))
                self.assertNotIn("skill body", captured["claude"]["stdin"])
                self.assertNotIn("SKILL.md", captured["claude"]["stdin"])
                # regression: codex 0.142.5 rejects --ask-for-approval
                self.assertNotIn("--ask-for-approval", captured["codex"]["command"])
                # regression: every agent must run inside the variant workspace to read references/*.md
                for agent in ("claude", "codex", "deepseek-v4-pro"):
                    self.assertEqual(captured[agent]["cwd"], skill_dir)
                # regression: opencode per-cell files must not leak into later cells
                self.assertFalse((skill_dir / "PROMPT.txt").exists())
                self.assertFalse((skill_dir / "opencode.json").exists())
                # token accounting: claude adds cache tokens; codex cached is a subset of input_tokens
                self.assertEqual(cells["claude"]["total_input_tokens"], 107)
                self.assertEqual(cells["codex"]["total_input_tokens"], 100)
                self.assertEqual(cells["deepseek-v4-pro"]["total_input_tokens"], 103)
                self.assertTrue((cells_dir / "route-hex-tiles__claude__worktree__r1" / "response.txt").is_file())
        finally:
            skill_benchmark.shutil.which = original_which
            skill_benchmark.run_cli = original_run_cli

    def test_skill_benchmark_static_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as out_base:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "dev-tools/skill_benchmark.py"),
                    "--static",
                    "--variants",
                    "worktree",
                    "--out",
                    out_base,
                ],
                cwd=REPO_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            run_dirs = list(Path(out_base).iterdir())
            self.assertEqual(len(run_dirs), 1)
            summary = (run_dirs[0] / "SUMMARY.md").read_text(encoding="utf-8")
            self.assertIn("Injected context", summary)
            static = json.loads((run_dirs[0] / "static.json").read_text(encoding="utf-8"))
            self.assertGreater(static["variants"]["worktree"]["context_est_tokens"], 0)
            self.assertIn("Results:", completed.stdout)

    def test_claude_renderer_uses_safe_no_tools_print_mode(self) -> None:
        captured: dict[str, object] = {}
        original_which = tileset_sim.shutil.which
        original_run = tileset_sim.subprocess.run
        try:
            tileset_sim.shutil.which = lambda name: "claude" if name == "claude" else None

            def fake_run(command, **kwargs):
                captured["command"] = command
                captured["kwargs"] = kwargs
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout=json.dumps(
                        {
                            "summary": "stone with moss",
                            "lower": {
                                "label": "stone",
                                "color": "#777777",
                                "accent_color": "#999999",
                                "texture": "solid",
                                "placement": "all",
                            },
                            "transition": {
                                "label": "moss",
                                "color": "#227733",
                                "accent_color": "#55AA66",
                                "texture": "sparse",
                                "placement": "top",
                            },
                        }
                    ),
                    stderr="",
                )

            tileset_sim.subprocess.run = fake_run
            recipe = tileset_sim.run_ai_renderer(
                "claude",
                "create_sidescroller_tileset",
                {"lower_description": "stone", "transition_description": "moss"},
                16,
                16,
                1,
            )
        finally:
            tileset_sim.shutil.which = original_which
            tileset_sim.subprocess.run = original_run

        command = captured["command"]
        self.assertEqual(recipe["renderer"], "claude")
        self.assertIn("-p", command)
        self.assertIn("--safe-mode", command)
        self.assertIn("--no-session-persistence", command)
        self.assertIn("--permission-mode", command)
        self.assertIn("dontAsk", command)
        self.assertIn("--tools=", command)
        self.assertIn("--json-schema", command)

    def test_ai_renderer_preserves_valid_topdown_recipe_without_text_overrides(self) -> None:
        original_which = tileset_sim.shutil.which
        original_run = tileset_sim.subprocess.run
        try:
            tileset_sim.shutil.which = lambda name: "claude" if name == "claude" else None

            def fake_run(command, **kwargs):
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout=json.dumps(
                        {
                            "summary": "light flooring with white speckles",
                            "lower": {
                                "label": "light flooring",
                                "color": "#EEEEEE",
                                "accent_color": "#FFFFFF",
                                "texture": "speckle",
                                "placement": "all",
                            },
                            "upper": {
                                "label": "pale grass",
                                "color": "#AADD88",
                                "accent_color": "#CCEEAA",
                                "texture": "solid",
                                "placement": "all",
                            },
                            "transition": {
                                "label": "soft edge",
                                "color": "#DDEECC",
                                "accent_color": "#FFFFFF",
                                "texture": "sparse",
                                "placement": "boundary",
                            },
                        }
                    ),
                    stderr="",
                )

            tileset_sim.subprocess.run = fake_run
            recipe = tileset_sim.run_ai_renderer(
                "claude",
                "create_topdown_tileset",
                {
                    "lower_description": "1-bit white speckles on light flooring",
                    "upper_description": "pale grass",
                    "transition_description": "soft edge",
                },
                16,
                16,
                1,
            )
        finally:
            tileset_sim.shutil.which = original_which
            tileset_sim.subprocess.run = original_run

        self.assertEqual(recipe["lower"]["color"], "#EEEEEE")
        self.assertEqual(recipe["lower"]["accent_color"], "#FFFFFF")
        self.assertEqual(recipe["lower"]["texture"], "speckle")

    def test_prompt_limits_include_font_name(self) -> None:
        text = (REPO_ROOT / "skills/pixellab-pip/references/prompt-limits.md").read_text(encoding="utf-8")
        self.assertIn("| `POST /generate-font-pro` | `font_name` | 200 |", text)


if __name__ == "__main__":
    unittest.main()
