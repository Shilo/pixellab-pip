"""Exercise the release bump and the actual standalone-skill ZIP builder."""
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

from test_helpers import REPO_ROOT


class MergePackagingTests(unittest.TestCase):
    def _git(self, root, *args, **kwargs):
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", *args],
                                       cwd=root, text=True, **kwargs).strip()

    def _commit_fixture(self, root):
        tree = self._git(root, "write-tree")
        commit = self._git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                           "-c", "commit.gpgSign=false", "commit-tree", tree, input="fixture\n")
        self._git(root, "update-ref", "HEAD", commit)
        return commit

    def _prepare_release_tree(self, root):
        names = subprocess.check_output(["git", "ls-files", "skills/pixellab-pip/"],
                                        cwd=REPO_ROOT, text=True).splitlines()
        for name in [*names, ".gitignore", "plugin.json"]:
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO_ROOT / name, dest)
        self._git(root, "init", "--quiet")
        self._git(root, "add", "--all")
        self._commit_fixture(root)
        return names

    def _build_release(self, root, source="HEAD"):
        workflow = (REPO_ROOT / ".github/workflows/release-skill.yml").read_text(encoding="utf-8")
        step = workflow.split("      - name: Build skill archive\n", 1)[1].split("      - name: ", 1)[0]
        block = step.split("<<'PY'\n", 1)[1].split("\n          PY", 1)[0]
        script = "\n".join(line[10:] for line in block.splitlines())
        output = root / "release.zip"
        output.unlink(missing_ok=True)
        result = subprocess.run([sys.executable, "-c", script, "pixellab-pip", str(output)],
                                cwd=root, env=dict(os.environ, RELEASE_SOURCE=source),
                                capture_output=True, text=True)
        return result, output

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

    def test_skill_package_preserves_complete_license(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            names = self._prepare_release_tree(root)
            # The version bump intentionally changes root manifests before the ZIP is built.
            (root / "plugin.json").write_text('{"version":"99.0.1"}\n', encoding="utf-8")
            result, output = self._build_release(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = output.read_bytes()
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                expected = sorted(name.removeprefix("skills/") for name in names)
                self.assertEqual(archive.namelist(), expected)
                for name in names:
                    self.assertEqual(archive.read(name.removeprefix("skills/")), (root / name).read_bytes())
                for info in archive.infolist():
                    self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                notice = archive.read("pixellab-pip/LICENSE.md").decode("utf-8").replace("\r\n", "\n")
            for name in names:
                (root / name).touch()
            result, output = self._build_release(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_bytes(), payload)
        project_license = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
        copyrights = [line.partition(" (adopted ")[0]
                      for line in project_license.splitlines() if line.startswith("Copyright ")]
        self.assertGreaterEqual(len(copyrights), 2)
        for copyright_notice in copyrights:
            self.assertIn(copyright_notice + "\n", notice)
        grant_start = "Permission is hereby granted"
        full_mit_body = grant_start + project_license.split(grant_start, 1)[1]
        self.assertIn(full_mit_body.strip(), notice)
        self.assertEqual(notice.count(grant_start), 1)
        self.assertIn("https://github.com/lexingel/pixellab-game-art", notice)

    def test_release_builder_rejects_ignored_untracked_and_missing_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self._prepare_release_tree(root)
            for name in ("pixellab-pip.json", "untracked.txt"):
                with self.subTest(name=name):
                    extra = root / "skills/pixellab-pip" / name
                    extra.write_text("synthetic private-file canary\n", encoding="utf-8")
                    result, output = self._build_release(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("selected source tree", result.stderr)
                    self.assertFalse(output.exists())
                    extra.unlink()
            (root / "skills/pixellab-pip/LICENSE.md").unlink()
            result, output = self._build_release(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())

    def test_release_builder_rejects_file_and_directory_symlinks(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self._prepare_release_tree(root)
            target = root / "outside.txt"
            target.write_text("synthetic outside canary\n", encoding="utf-8")
            for directory in (False, True):
                with self.subTest(directory=directory):
                    link = root / "skills/pixellab-pip/link"
                    try:
                        link.symlink_to(root if directory else target, target_is_directory=directory)
                    except OSError:
                        self.skipTest("Symbolic links unavailable")
                    result, output = self._build_release(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("symbolic link", result.stderr)
                    self.assertFalse(output.exists())
                    link.unlink()

    def test_release_builder_resumes_tagged_paths_without_using_the_main_index(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            names = self._prepare_release_tree(root)
            self._git(root, "update-ref", "refs/tags/v0.0.1", "HEAD")
            old = root / "skills/pixellab-pip/blueprints/aura.blueprint.json"
            new = old.with_name("newer-main.blueprint.json")
            old.rename(new)
            self._git(root, "add", "--all")
            self._commit_fixture(root)
            self._git(root, "restore", "--source=v0.0.1", "--worktree", "--", "skills/pixellab-pip")
            self.assertNotIn(old.relative_to(root).as_posix(), self._git(root, "ls-files").splitlines())
            result, output = self._build_release(root, "v0.0.1")
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.namelist(), sorted(name.removeprefix("skills/") for name in names))
            extra = root / "skills/pixellab-pip/pixellab-pip.json"
            extra.write_text("synthetic private-file canary\n", encoding="utf-8")
            result, output = self._build_release(root, "v0.0.1")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
