from __future__ import annotations

import json
import subprocess
import unittest

from test_helpers import REPO_ROOT

EDITION = REPO_ROOT / "editions" / "claude"
BANNED_WORDS = ("never ask", "without asking", "don't ask", "do not ask")


class ClaudeEditionTests(unittest.TestCase):
    def test_no_never_ask_wording(self) -> None:
        for f in EDITION.rglob("*.md"):
            low = f.read_text(encoding="utf-8").lower()
            for word in BANNED_WORDS:
                self.assertNotIn(word, low, f"{f.name}: {word}")

    def test_one_entry_point_no_pga_commands(self) -> None:
        # one /pixellab-pip entry (Shilo's design): requests are routed by SKILL.md, not by per-task commands
        self.assertFalse((EDITION / "commands").exists())
        for f in (REPO_ROOT / "skills" / "pixellab-pip").rglob("*"):
            if f.suffix in (".md", ".py", ".json"):
                self.assertNotIn("/pga-", f.read_text(encoding="utf-8"), f.name)

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


if __name__ == "__main__":
    unittest.main()
