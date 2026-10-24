"""Exercise the existing release bump and the raw-skill notice payload."""
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile

from test_helpers import REPO_ROOT


class MergePackagingTests(unittest.TestCase):
    def test_release_bump_updates_every_shipped_plugin(self):
        if not shutil.which("node"):
            self.skipTest("Node unavailable")
        workflow = (REPO_ROOT / ".github/workflows/release-skill.yml").read_text(encoding="utf-8")
        block = workflow.split("node <<'NODE'", 1)[1].split("\n          NODE", 1)[0]
        script = "\n".join(line[10:] if line.startswith(" " * 10) else line for line in block.splitlines())
        paths = re.findall(r'file: "([^"]+\.json)"', script)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in [*paths, "README.md"]:
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO_ROOT / name, dest)
            (root / "skills/pixellab-pip").mkdir(parents=True)
            env = dict(os.environ, INPUT_VERSION="99.0.1", RESUME_VERSION="", GITHUB_OUTPUT=str(root / "output.txt"))
            result = subprocess.run(["node", "-"], input=script, cwd=root, env=env,
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
            for plugin in market["plugins"]:
                self.assertEqual(plugin["version"], "99.0.1")
            for name in paths:
                data = json.loads((root / name).read_text())
                if "version" in data:
                    self.assertEqual(data["version"], "99.0.1", name)

    def test_skill_package_preserves_adopted_notice(self):
        payload = io.BytesIO()
        prefix = "skills/pixellab-pip/"
        names = subprocess.check_output(["git", "ls-files", prefix], cwd=REPO_ROOT, text=True).splitlines()
        with zipfile.ZipFile(payload, "w") as archive:
            for name in names:
                archive.write(REPO_ROOT / name, "pixellab-pip/" + name.removeprefix(prefix))
        with zipfile.ZipFile(payload) as archive:
            notice = archive.read("pixellab-pip/THIRD_PARTY_NOTICES.md").decode("utf-8")
        self.assertIn("Copyright (c) 2026 Shilo", notice)
        self.assertIn("Copyright (c) 2026 lexingel", notice)
        self.assertIn("Permission is hereby granted, free of charge", notice)
        self.assertIn("THE SOFTWARE IS PROVIDED", notice)


if __name__ == "__main__":
    unittest.main()
