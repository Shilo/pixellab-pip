from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_qa():
    path = REPO_ROOT / "dev-tools" / "qa.py"
    spec = importlib.util.spec_from_file_location("qa", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


qa = _load_qa()


class SecurityTriggerPatternTests(unittest.TestCase):
    """Locks the SkillSpector-trigger guard both ways: known avoidable IOCs must
    match, and the phrasing the shipped setup docs rely on (bare
    `.codex/config.toml`, prose `~/.bashrc` with no redirection) must stay clean —
    so a careless loosening of a pattern fails loudly here instead of silently
    red-ing every release or silently ceasing to guard."""

    def _hit(self, text: str) -> bool:
        return any(rx.search(text) for rx, _ in qa.SECURITY_TRIGGER_REGEXES)

    def test_flags_real_triggers(self):
        for bad in (
            "echo x >> ~/.bashrc",
            "cat key >> ~/.ssh/authorized_keys",
            "export LD_PRELOAD=/tmp/x.so",
            "a crontab entry that runs curl",
            "Codex config lives at ~/.codex/config.toml",
        ):
            self.assertTrue(self._hit(bad), f"should flag: {bad!r}")

    def test_allows_current_doc_style(self):
        # The phrasing the shipped docs actually use — must never be flagged.
        for ok in (
            "put the same block in a project `.codex/config.toml`",
            "add the export line to your shell profile (`~/.zshrc` on macOS, `~/.bashrc` on Linux)",
            "Never print, echo, log a token value",
            "Codex writes a global user `config.toml`",
        ):
            self.assertFalse(self._hit(ok), f"should NOT flag: {ok!r}")


if __name__ == "__main__":
    unittest.main()
