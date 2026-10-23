from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_helpers import REPO_ROOT  # noqa: E402

SKILL_DIR = REPO_ROOT / "skills/pixellab-pip"
WEAPON_PAGES = [
    "weapon-sword.md",
    "weapon-katana.md",
    "weapon-dagger.md",
    "weapon-staff.md",
    "weapon-bow.md",
    "weapon-mace.md",
    "weapon-spear.md",
    "weapon-axe.md",
    "weapon-sword-and-shield.md",
    "weapon-war-hammer.md",
    "weapon-whip.md",
    "martial-arts.md",
    "armor-clothing.md",
    "weapon-effects.md",
    "weapon-firearms.md",
    "weapon-futuristic.md",
    "weapon-anime.md",
]


class ReferencePagesTests(unittest.TestCase):
    def test_weapon_pages_linked_and_have_toc(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for name in WEAPON_PAGES:
            with self.subTest(page=name):
                path = SKILL_DIR / "references" / name
                self.assertTrue(path.exists(), f"missing {name}")
                self.assertIn(f"`references/{name}`", skill)
                lines = path.read_text(encoding="utf-8").splitlines()
                if len(lines) > 100:
                    self.assertIn("## Contents", lines)

    def test_plan_level_always_posts_the_cost_card(self) -> None:
        # e2e runs 2 and 3: at plan level the agent approved its own plan silently and never showed the cost card
        auto = (SKILL_DIR / "references/auto.md").read_text(encoding="utf-8")
        self.assertIn("even when it is approved at once", auto)
        self.assertIn("plan · budget {B} · {R} redos", auto)
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("the approval or auto-on card", skill)

    def test_plan_never_approves_itself(self) -> None:
        # review: "approved by the level's own budget" read as plan approving itself
        auto = (SKILL_DIR / "references/auto.md").read_text(encoding="utf-8")
        self.assertNotIn("the level's own budget", auto)
        self.assertNotIn("python assets/", auto)

    def test_router_rows_point_to_existing_references(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        rows = {
            "| Attack, skill or signature move from a sprite (key poses, then in-betweens) |": "key-pose-animation.md",
        }
        for row, name in rows.items():
            with self.subTest(page=name):
                line = next((ln for ln in skill.splitlines() if ln.startswith(row)), "")
                self.assertIn(f"`references/{name}`", line, f"router row missing for {name}")
                path = SKILL_DIR / "references" / name
                self.assertTrue(path.exists(), f"missing {name}")
                self.assertIn("## Contents", path.read_text(encoding="utf-8").splitlines())


if __name__ == "__main__":
    unittest.main()
