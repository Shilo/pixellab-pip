from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_helpers import bark


class AutoPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.config = Path(temporary.name) / "pixellab-pip.json"
        self.real_write = bark.write_text_atomic
        for replacement in (patch.object(bark, "SKILL_CONFIG", self.config),
                            patch.object(bark, "safe_user_config_path", return_value=None)):
            replacement.start()
            self.addCleanup(replacement.stop)

    def write(self, data: dict) -> bytes:
        self.config.write_text(json.dumps(data), encoding="utf-8")
        return self.config.read_bytes()

    def run_command(self, command: str) -> tuple[int, dict]:
        output = io.StringIO()
        with patch.object(sys, "argv", ["bark.py", command]), redirect_stdout(output):
            result = bark.main()
        return result, json.loads(output.getvalue())

    def write_fallback_only(self, path: Path, content: str) -> None:
        if path == self.config:
            raise PermissionError("read-only skill config")
        self.real_write(path, content)

    def test_status_is_read_only_and_does_not_expose_unrelated_config(self) -> None:
        original = self.write({"auto": True, "bark": False, "unrelated": "private value"})
        result, output = self.run_command("status")
        self.assertEqual(result, 0)
        self.assertIs(output["auto"], True)
        self.assertIs(output["bark"], False)
        self.assertEqual(output["legacy_policy"], {})
        self.assertIs(output["requires_reconciliation"], False)
        self.assertNotIn("unrelated", output)
        self.assertNotIn("private value", json.dumps(output))
        self.assertEqual(self.config.read_bytes(), original)

    def test_any_legacy_key_requires_reconciliation_including_invalid_values(self) -> None:
        for policy in ({"level": "auto"}, {"level": "unknown"}, {"budget": 45},
                       {"budget": None}, {"budget": -1}, {"retries": 0},
                       {"retries": True}, {"retries": {"invalid": "shape"}}):
            with self.subTest(policy=policy):
                original = self.write({"auto": True, **policy})
                result, output = self.run_command("status")
                self.assertEqual(result, 0)
                self.assertIs(output["auto"], False)
                self.assertIs(output["requires_reconciliation"], True)
                self.assertEqual(output["legacy_policy"], policy)
                self.assertEqual(self.config.read_bytes(), original)

    def test_enabling_and_toggling_do_not_discard_legacy_restrictions(self) -> None:
        for enabled in (False, True):
            for command in ("auto-on", "auto"):
                with self.subTest(enabled=enabled, command=command):
                    original = self.write({"auto": enabled, "level": "plan", "budget": 45, "retries": 2})
                    result, output = self.run_command(command)
                    self.assertEqual(result, 1)
                    self.assertIs(output["ok"], False)
                    self.assertIn("reconciliation", output["error"])
                    self.assertNotIn("auto", output)
                    self.assertIsNone(output["config"])
                    self.assertEqual(self.config.read_bytes(), original)

    def test_invalid_bark_cannot_hide_legacy_limits_behind_fallback_auto(self) -> None:
        self.write({"auto": True, "bark": "invalid", "budget": 45})
        fallback = self.config.with_name("fallback.json")
        fallback.write_text('{"auto": true, "bark": true}', encoding="utf-8")
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            result, output = self.run_command("status")
            self.assertEqual(result, 0)
            self.assertIs(output["auto"], False)
            self.assertEqual(output["legacy_policy"], {"budget": 45})
            self.assertEqual(output["invalid_config"], str(self.config))
            self.assertEqual(self.run_command("auto-on")[0], 1)
            self.assertEqual(self.run_command("auto-reset")[0], 0)
            status = self.run_command("status")[1]
            self.assertIs(status["auto"], False)
            self.assertEqual(status["config"], str(self.config))
            self.assertEqual(json.loads(self.config.read_text()), {"auto": False, "bark": "invalid"})

    def test_invalid_auto_with_malformed_bark_stays_authoritative(self) -> None:
        fallback = self.config.with_name("fallback.json")
        fallback.write_text('{"auto": true, "bark": true}', encoding="utf-8")
        for value in (None, 0, "false", []):
            with self.subTest(value=value):
                original = self.write({"auto": value, "bark": "invalid"})
                with patch.object(bark, "safe_user_config_path", return_value=fallback):
                    output = self.run_command("status")[1]
                    self.assertIs(output["auto"], False)
                    self.assertIs(output["requires_reconciliation"], True)
                    self.assertEqual(output["config"], str(self.config))
                    self.assertEqual(self.run_command("auto-on")[0], 1)
                self.assertEqual(self.config.read_bytes(), original)

    def test_corrupt_primary_blocks_auto_and_all_settings_writes_without_data_loss(self) -> None:
        original = b'{"auto": false, "budget": 45,'
        self.config.write_bytes(original)
        fallback = self.config.with_name("fallback.json")
        fallback_original = b'{"auto": true, "bark": true}'
        fallback.write_bytes(fallback_original)
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            status = self.run_command("status")[1]
            self.assertIs(status["auto"], False)
            self.assertIs(status["requires_reconciliation"], True)
            self.assertEqual(status["invalid_config"], str(self.config))
            for command in ("auto-on", "auto", "auto-off", "auto-reset", "off", "on", "bark"):
                with self.subTest(command=command):
                    result, output = self.run_command(command)
                    self.assertEqual(result, 1)
                    self.assertNotIn("auto", output)
                    self.assertIsNone(output["config"])
                    self.assertEqual(self.config.read_bytes(), original)
                    self.assertEqual(fallback.read_bytes(), fallback_original)

    def test_shadowed_invalid_object_is_not_replaced_with_fallback_policy(self) -> None:
        original = self.write({"bark": "invalid", "other": {"keep": 7}})
        fallback = self.config.with_name("fallback.json")
        fallback_original = b'{"auto": true, "bark": true}'
        fallback.write_bytes(fallback_original)
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            self.assertIs(self.run_command("status")[1]["auto"], False)
            for command in ("off", "auto-off", "auto-reset"):
                with self.subTest(command=command):
                    self.assertEqual(self.run_command(command)[0], 1)
                    self.assertEqual(self.config.read_bytes(), original)
                    self.assertEqual(fallback.read_bytes(), fallback_original)

    def test_explicit_bark_repair_preserves_parsed_authoritative_policy(self) -> None:
        policy = {"auto": False, "level": "plan", "budget": 0, "other": {"keep": 7}}
        self.write({"bark": "invalid", **policy})
        result, output = self.run_command("off")
        self.assertEqual(result, 0, output)
        self.assertEqual(json.loads(self.config.read_text()), {"bark": False, **policy})
        status = self.run_command("status")[1]
        self.assertIsNone(status["invalid_config"])
        self.assertIs(status["auto"], False)
        self.assertEqual(status["legacy_policy"], {"level": "plan", "budget": 0})

    def test_off_preserves_legacy_policy_and_other_settings(self) -> None:
        policy = {"level": "auto", "budget": 45, "retries": 2, "bark": False, "other": 7}
        self.write({"auto": True, **policy})
        result, output = self.run_command("auto-off")
        self.assertEqual(result, 0, output)
        self.assertIs(output["auto"], False)
        self.assertEqual(json.loads(self.config.read_text()), {"auto": False, **policy})
        self.assertIs(self.run_command("status")[1]["requires_reconciliation"], True)

    def test_reset_removes_only_legacy_policy_and_disables_auto(self) -> None:
        retained = {"bark": False, "other": {"budget": 9}, "auto_budget": 8}
        self.write({"auto": True, "level": "plan", "budget": 45, "retries": 2, **retained})
        result, output = self.run_command("auto-reset")
        self.assertEqual(result, 0)
        self.assertIs(output["auto"], False)
        self.assertEqual(json.loads(self.config.read_text()), {"auto": False, **retained})
        self.assertIs(self.run_command("status")[1]["requires_reconciliation"], False)
        self.assertIs(self.run_command("auto-on")[1]["auto"], True)

    def test_failed_reset_or_enable_does_not_claim_changed_auto(self) -> None:
        for command, data in (("auto-reset", {"auto": True, "budget": 45}),
                              ("auto-on", {"auto": False})):
            with self.subTest(command=command):
                original = self.write(data)
                with patch.object(bark, "write_text_atomic", side_effect=PermissionError("read-only")):
                    result, output = self.run_command(command)
                self.assertEqual(result, 1)
                self.assertIs(output["ok"], False)
                self.assertNotIn("auto", output)
                self.assertIsNone(output["config"])
                self.assertEqual(self.config.read_bytes(), original)

    def test_bark_change_never_resets_legacy_policy(self) -> None:
        policy = {"auto": True, "level": "plan", "budget": 45, "retries": 2}
        self.write({"bark": True, **policy})
        result, output = self.run_command("off")
        self.assertEqual(result, 0)
        self.assertIs(output["bark"], False)
        self.assertEqual(json.loads(self.config.read_text()), {"bark": False, **policy})
        self.assertIs(self.run_command("status")[1]["auto"], False)

    def test_read_only_authoritative_config_cannot_report_shadowed_fallback_success(self) -> None:
        fallback = self.config.with_name("user.json")
        for command, data in (("auto-off", {"auto": True}),
                              ("auto-reset", {"auto": True, "budget": 45}),
                              ("off", {"bark": True})):
            with self.subTest(command=command):
                original = self.write(data)
                with patch.object(bark, "safe_user_config_path", return_value=fallback), \
                        patch.object(bark, "write_text_atomic", side_effect=self.write_fallback_only):
                    result, output = self.run_command(command)
                    self.assertEqual(result, 1)
                    self.assertIs(output["ok"], False)
                    self.assertIn("fallback would be ignored", output["error"])
                    self.assertNotIn("auto", output)
                    self.assertIsNone(output["config"])
                    if command == "auto-off":
                        self.assertIs(self.run_command("status")[1]["auto"], True)
                    if command == "off":
                        self.assertIs(output["bark"], True)
                self.assertEqual(self.config.read_bytes(), original)
                self.assertFalse(fallback.exists())

    def test_read_only_install_without_primary_config_can_use_user_fallback(self) -> None:
        fallback = self.config.with_name("user.json")
        with patch.object(bark, "safe_user_config_path", return_value=fallback), \
                patch.object(bark, "write_text_atomic", side_effect=self.write_fallback_only):
            result, output = self.run_command("auto-on")
            self.assertEqual(result, 0)
            self.assertEqual(output["config"], str(fallback))
            self.assertIs(output["auto"], True)
            status = self.run_command("status")[1]
            self.assertIs(status["auto"], True)
            self.assertEqual(status["config"], str(fallback))
        self.assertFalse(self.config.exists())

    def test_write_must_become_active_before_success_is_reported(self) -> None:
        original = self.write({"auto": False})
        with patch.object(bark, "write_text_atomic", return_value=None):
            result, output = self.run_command("auto-on")
        self.assertEqual(result, 1)
        self.assertIn("verified active", output["error"])
        self.assertNotIn("auto", output)
        self.assertIsNone(output["config"])
        self.assertEqual(self.config.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
