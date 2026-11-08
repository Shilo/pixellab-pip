from __future__ import annotations

import importlib.util
import json
import os
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch


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
            "loop forever, and explicit disposal",
            "The cancellation route is `DELETE /background-jobs/{job_id}`:",
            "remove '/path/to/file'",
        ):
            self.assertTrue(self._hit(bad), f"should flag: {bad!r}")

    def test_allows_current_doc_style(self):
        # The phrasing the shipped docs actually use — must never be flagged.
        for ok in (
            "put the same block in a project `.codex/config.toml`",
            "add the export line to your shell profile (`~/.zshrc` on macOS, `~/.bashrc` on Linux)",
            "Never print, echo, log a token value",
            "Codex writes a global user `config.toml`",
            "infinite looping, and explicit disposal",
            "Never request the PixelLab bearer token in chat",
            "The cancellation route uses HTTP `DELETE` on `/background-jobs/{job_id}`:",
            "Poll `GET /background-jobs/{job_id}`.",
        ):
            self.assertFalse(self._hit(ok), f"should NOT flag: {ok!r}")


class ReleaseSecurityGateTests(unittest.TestCase):
    def test_static_evidence_cannot_be_skipped_or_allowed_to_fail(self):
        read = Path.read_text
        mutations = (
            (".github/workflows/release-skill.yml", "        uses: ./.github/actions/scanner-regression",
             "        if: false\n        uses: ./.github/actions/scanner-regression"),
            (".github/workflows/security-scan.yml", "        uses: ./.github/actions/scanner-regression", ""),
            (".github/workflows/release-skill.yml", "        uses: ./.github/actions/scanner-regression",
             "        uses: ./.github/actions/scanner-regression\n        continue-on-error: true"),
            (".github/actions/scanner-regression/action.yml", "    - name: Read reviewed scanner pins",
             "    - name: Read reviewed scanner pins\n      continue-on-error: true"),
            (".github/actions/scanner-regression/action.yml",
             'python dev-tools/check_scanner.py .local/scanner-results/report.json', "true"),
            (".github/actions/scanner-regression/action.yml",
             'hashlib.sha256(patch).hexdigest() != os.environ["PATCH_SHA256"]', "False"),
        )
        qa.check_workflows()
        for name, before, after in mutations:
            target = REPO_ROOT / name

            def changed(path, *args, **kwargs):
                text = read(path, *args, **kwargs)
                return text.replace(before, after) if path == target else text

            with self.subTest(path=name, mutation=before), patch.object(Path, "read_text", changed):
                with self.assertRaises(AssertionError):
                    qa.check_workflows()

    def test_hosted_verdict_stays_fail_closed_after_retired_static_section(self):
        workflow = (REPO_ROOT / ".github/workflows/release-skill.yml").read_text(encoding="utf-8")
        step = workflow.split("      - name: Scan the published ClawHub version\n", 1)[1]
        source = textwrap.dedent(step.split("python - <<'PY'\n", 1)[1].split("\n          PY", 1)[0])
        valid = {"status": "succeeded", "sourceKind": "published", "writtenBack": True,
                 "artifact": {"version": "3.2.0"},
                 "report": {"clawscan": {"verdict": "benign", "confidence": "high"}}}

        def check(data):
            with patch.dict(os.environ, {"EXPECTED_VERSION": "3.2.0"}), \
                    patch.object(Path, "read_text", return_value=json.dumps(data)), patch("builtins.print"):
                exec(compile(source, "release hosted audit gate", "exec"), {})

        check(valid)
        for section, key, value in (
            (None, "status", "failed"), (None, "sourceKind", "local"),
            (None, "writtenBack", False), ("artifact", "version", "3.1.0"),
            ("clawscan", "verdict", "suspicious"), ("clawscan", "confidence", "medium"),
        ):
            data = json.loads(json.dumps(valid))
            target = data["report"]["clawscan"] if section == "clawscan" else data[section] if section else data
            target[key] = value
            with self.subTest(section=section, key=key), self.assertRaises(SystemExit):
                check(data)
        for key in ("malicious", "suspicious"):
            data = json.loads(json.dumps(valid))
            data["report"]["virustotal"] = {key: 1}
            with self.subTest(detection=key), self.assertRaises(SystemExit):
                check(data)


if __name__ == "__main__":
    unittest.main()
