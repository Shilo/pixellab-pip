from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest

from test_helpers import REPO_ROOT

EDITION = REPO_ROOT / "editions" / "claude"
COMMANDS = EDITION / "commands"
GEN = REPO_ROOT / "dev-tools" / "gen_claude_commands.py"
BANNED_WORDS = ("never ask", "without asking", "don't ask", "do not ask")
DESTRUCTIVE = re.compile(r"mcp__[a-z_-]+__(delete_|cancel_|remove_|edit_map|place_)")


def frontmatter(text: str) -> dict[str, str]:
    head = text.split("---", 2)[1]
    return {k.strip(): v.strip() for k, v in (line.split(":", 1) for line in head.strip().splitlines())}


class ClaudeEditionTests(unittest.TestCase):
    def test_generated_commands_are_current(self) -> None:
        r = subprocess.run([sys.executable, str(GEN), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_frontmatter_values_are_quoted(self) -> None:
        # a colon in a description or a [..] hint broke the YAML, so the command loaded with no metadata
        for path in (REPO_ROOT / "editions/claude/commands").glob("pga-*.md"):
            for line in path.read_text(encoding="utf-8").split("---")[1].strip().splitlines():
                key, _, value = line.partition(": ")
                if key in ("description", "argument-hint"):
                    self.assertTrue(value.startswith('"') and value.endswith('"'), (path.name, line))

    def test_every_command_names_a_core_intent(self) -> None:
        files = sorted(COMMANDS.glob("pga-*.md"))
        self.assertGreaterEqual(len(files), 18)
        for f in files:
            text = f.read_text(encoding="utf-8")
            self.assertIn("pixellab-pip skill", text, f.name)
            self.assertIn("$ARGUMENTS", text, f.name)
            self.assertIn("description", frontmatter(text), f.name)

    def test_no_never_ask_wording(self) -> None:
        for f in EDITION.rglob("*.md"):
            low = f.read_text(encoding="utf-8").lower()
            for word in BANNED_WORDS:
                self.assertNotIn(word, low, f"{f.name}: {word}")

    def test_no_destructive_tools_preapproved(self) -> None:
        for f in COMMANDS.glob("*.md"):
            tools = frontmatter(f.read_text(encoding="utf-8")).get("allowed-tools", "")
            self.assertIsNone(DESTRUCTIVE.search(tools), f.name)
            self.assertNotIn("mcp__pixellab__*", tools, f.name)   # paid calls keep their normal approval

    def test_edition_version_matches_core(self) -> None:
        market = json.loads((REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        versions = {p["name"]: p.get("version") for p in market["plugins"]}
        self.assertEqual(versions.get("pixellab-pip-studio"), versions.get("pixellab-pip"))

    def test_connector_file_is_tracked(self) -> None:
        # final review: the root .gitignore hid editions/claude/.mcp.json, so the connector never shipped
        r = subprocess.run(["git", "check-ignore", "-q", "editions/claude/.mcp.json"], cwd=REPO_ROOT)
        self.assertEqual(r.returncode, 1)
        server = json.loads((EDITION / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["pixellab"]
        self.assertIn("${user_config.pixellab_key}", server["headers"]["Authorization"])

    def test_read_tools_preapproved_under_both_namings(self) -> None:
        tools = frontmatter((COMMANDS / "pga-anim.md").read_text(encoding="utf-8"))["allowed-tools"]
        self.assertIn("mcp__pixellab__get_balance", tools)                              # a user's own server
        self.assertIn("mcp__plugin_pixellab-pip-studio_pixellab__get_balance", tools)  # the bundled one


if __name__ == "__main__":
    unittest.main()
