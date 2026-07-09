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


class MarkdownLinkScanTests(unittest.TestCase):
    """The link checker must ignore link *syntax* inside code, but keep real
    prose links — otherwise doc examples (connector wrappers, blueprints) trip
    CI, and on Windows Path.resolve() silently strips trailing dots so a bad
    `[x](...)` example passes locally yet fails on Linux CI (issue: run #51)."""

    def _has_link(self, text: str) -> bool:
        return bool(qa.MD_LINK.search(qa.CODE_REGION.sub("", text)))

    def test_inline_code_example_ignored(self):
        self.assertFalse(self._has_link("`[$pip:pip](...) make a knight`"))

    def test_fenced_code_example_ignored(self):
        self.assertFalse(self._has_link("x\n```\n[x](nope.md)\n```\ny"))

    def test_real_prose_link_kept(self):
        self.assertTrue(self._has_link("See [guide](docs/developer.md)."))


if __name__ == "__main__":
    unittest.main()
