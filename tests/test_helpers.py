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

    def test_prompt_limits_include_font_name(self) -> None:
        text = (REPO_ROOT / "skills/pixellab-pip/references/prompt-limits.md").read_text(encoding="utf-8")
        self.assertIn("| `POST /generate-font-pro` | `font_name` | 200 |", text)


if __name__ == "__main__":
    unittest.main()
