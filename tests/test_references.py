from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_helpers import REPO_ROOT  # noqa: E402

SKILL_DIR = REPO_ROOT / "skills/pixellab-pip"
WEAPON_PAGES = sorted(p.name for p in (SKILL_DIR / "references").glob("weapon-*.md")) + ["martial-arts.md", "armor-clothing.md"]


class ReferencePagesTests(unittest.TestCase):
    def test_weapon_pages_linked_and_have_toc(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for name in WEAPON_PAGES:
            with self.subTest(page=name):
                path = SKILL_DIR / "references" / name
                self.assertIn(f"`references/{name}`", skill)
                lines = path.read_text(encoding="utf-8").splitlines()
                if len(lines) > 100:
                    self.assertIn("## Contents", lines)

    def test_portable_description_and_metadata(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        description = next(line.split(":", 1)[1].strip() for line in skill.splitlines()
                           if line.startswith("description:"))
        self.assertTrue(description)
        self.assertLessEqual(len(description), 1024)


if __name__ == "__main__":
    unittest.main()
