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
        self.assertNotIn("unrelated", output)
        self.assertNotIn("private value", json.dumps(output))
        self.assertEqual(self.config.read_bytes(), original)

    def test_utf8_bom_config_stays_authoritative(self) -> None:
        data = {"auto": False, "bark": False, "other": {"keep": 7}}
        original = b"\xef\xbb\xbf" + json.dumps(data).encode("utf-8")
        self.config.write_bytes(original)
        fallback = self.config.with_name("fallback.json")
        fallback.write_text('{"auto": true}', encoding="utf-8")
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            status = self.run_command("status")[1]
            self.assertEqual(status["config"], str(self.config))
            self.assertIsNone(status["invalid_config"])
            self.assertIs(status["auto"], False)
            self.assertIs(status["bark"], False)
            self.assertEqual(self.config.read_bytes(), original)
            self.assertEqual(self.run_command("off")[0], 0)
        self.assertEqual(json.loads(self.config.read_text()), data)
        self.assertEqual(fallback.read_text(), '{"auto": true}')

    def test_transient_windows_replace_denial_reuses_prepared_toggle(self) -> None:
        self.write({"auto": False, "other": {"keep": 7}})
        real_replace = Path.replace
        attempts = []
        denied = PermissionError("temporarily held by a Windows reader")
        denied.winerror = 5

        def replace(source, target):
            attempts.append((source, source.read_bytes()))
            if len(attempts) == 1:
                raise denied
            return real_replace(source, target)

        with patch.object(Path, "replace", new=replace), patch.object(bark.time, "sleep"):
            result, output = self.run_command("auto")
        self.assertEqual(result, 0, output)
        self.assertIs(output["auto"], True)
        self.assertEqual(len(attempts), 2)
        self.assertEqual(attempts[0], attempts[1])
        self.assertEqual(json.loads(self.config.read_text()), {"auto": True, "other": {"keep": 7}})
        self.assertFalse(list(self.config.parent.glob("*.tmp")))

    def test_failed_replacement_preserves_config_and_cleans_prepared_file(self) -> None:
        for winerror, expected_attempts in ((5, 2), (None, 1)):
            with self.subTest(winerror=winerror):
                original = self.write({"auto": False, "other": 7})
                denied = PermissionError("replacement denied")
                if winerror is not None:
                    denied.winerror = winerror
                with patch.object(Path, "replace", side_effect=denied) as replace, \
                        patch.object(bark.time, "monotonic", side_effect=[0, 0, 1]), \
                        patch.object(bark.time, "sleep"):
                    with self.assertRaises(PermissionError):
                        bark.write_text_atomic(self.config, '{"auto":true}')
                self.assertEqual(replace.call_count, expected_attempts)
                self.assertEqual(self.config.read_bytes(), original)
                self.assertFalse(list(self.config.parent.glob("*.tmp")))

    def test_invalid_auto_with_malformed_bark_stays_authoritative(self) -> None:
        fallback = self.config.with_name("fallback.json")
        fallback.write_text('{"auto": true, "bark": true}', encoding="utf-8")
        for value in (None, 0, "false", []):
            with self.subTest(value=value):
                original = self.write({"auto": value, "bark": "invalid"})
                with patch.object(bark, "safe_user_config_path", return_value=fallback):
                    output = self.run_command("status")[1]
                    self.assertIs(output["auto"], False)
                    self.assertEqual(output["config"], str(self.config))
                    self.assertIsNone(output["invalid_config"])
                self.assertEqual(self.config.read_bytes(), original)

    def test_corrupt_primary_blocks_auto_and_all_settings_writes_without_data_loss(self) -> None:
        original = b'{"auto": false, "other": 45,'
        self.config.write_bytes(original)
        fallback = self.config.with_name("fallback.json")
        fallback_original = b'{"auto": true, "bark": true}'
        fallback.write_bytes(fallback_original)
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            status = self.run_command("status")[1]
            self.assertIs(status["auto"], False)
            self.assertEqual(status["invalid_config"], str(self.config))
            for command in ("auto-on", "auto", "auto-off", "off", "on", "bark"):
                with self.subTest(command=command):
                    result, output = self.run_command(command)
                    self.assertEqual(result, 1)
                    self.assertNotIn("auto", output)
                    self.assertIsNone(output["config"])
                    self.assertEqual(self.config.read_bytes(), original)
                    self.assertEqual(fallback.read_bytes(), fallback_original)

    def test_malformed_bark_object_remains_active_and_explicit_repair_preserves_data(self) -> None:
        original = self.write({"bark": "invalid", "other": {"keep": 7}})
        fallback = self.config.with_name("fallback.json")
        fallback_original = b'{"auto": true, "bark": true}'
        fallback.write_bytes(fallback_original)
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            status = self.run_command("status")[1]
            self.assertIs(status["auto"], False)
            self.assertIs(status["bark"], True)
            self.assertIsNone(status["invalid_config"])
            self.assertEqual(status["config"], str(self.config))
            self.assertEqual(self.config.read_bytes(), original)
            self.assertEqual(self.run_command("off")[0], 0)
            self.assertEqual(json.loads(self.config.read_text()), {"bark": False, "other": {"keep": 7}})
            self.assertEqual(fallback.read_bytes(), fallback_original)

    def test_nonstandard_json_or_nonobject_config_cannot_enable_auto_or_be_overwritten(self) -> None:
        for raw in ('{"auto":true,"budget":NaN}', '{"auto":true,"other":Infinity}',
                    '{"auto":true,"other":-Infinity}', '{"auto":false,"other":1e999}',
                    '{"auto":true,"budget":-1e999}', '[]', 'true', 'null'):
            with self.subTest(raw=raw):
                self.config.write_text(raw, encoding="utf-8")
                status = self.run_command("status")[1]
                self.assertIs(status["auto"], False)
                self.assertEqual(status["invalid_config"], str(self.config))
                self.assertNotIn("NaN", json.dumps(status, allow_nan=False))
                self.assertEqual(self.run_command("auto-on")[0], 1)
                self.assertEqual(self.config.read_text(encoding="utf-8"), raw)

    def test_invalid_user_fallback_error_does_not_claim_a_priority(self) -> None:
        fallback = self.config.with_name("user.json")
        fallback.write_text("[]", encoding="utf-8")
        with patch.object(bark, "safe_user_config_path", return_value=fallback):
            result, output = self.run_command("off")
        self.assertEqual(result, 1)
        self.assertIn("invalid config", output["error"])
        self.assertNotIn("higher-priority", output["error"])
        self.assertFalse(self.config.exists())
        self.assertEqual(fallback.read_text(encoding="utf-8"), "[]")

    def test_explicit_bark_repair_preserves_parsed_authoritative_settings(self) -> None:
        policy = {"auto": False, "other": {"keep": 7}}
        self.write({"bark": "invalid", **policy})
        result, output = self.run_command("off")
        self.assertEqual(result, 0, output)
        self.assertEqual(json.loads(self.config.read_text()), {"bark": False, **policy})
        status = self.run_command("status")[1]
        self.assertIsNone(status["invalid_config"])
        self.assertIs(status["auto"], False)

    def test_failed_enable_does_not_claim_changed_auto(self) -> None:
        original = self.write({"auto": False})
        with patch.object(bark, "write_text_atomic", side_effect=PermissionError("read-only")):
            result, output = self.run_command("auto-on")
        self.assertEqual(result, 1)
        self.assertIs(output["ok"], False)
        self.assertNotIn("auto", output)
        self.assertIsNone(output["config"])
        self.assertEqual(self.config.read_bytes(), original)

    def test_sound_typo_does_not_change_valid_auto(self) -> None:
        for auto in (True, False):
            with self.subTest(auto=auto):
                original = self.write({"bark": "x", "auto": auto})
                status = self.run_command("status")[1]
                self.assertIsNone(status["invalid_config"])
                self.assertIs(status["auto"], auto)
                self.assertEqual(self.config.read_bytes(), original)

    def test_read_only_authoritative_config_cannot_report_shadowed_fallback_success(self) -> None:
        fallback = self.config.with_name("user.json")
        for command, data in (("auto-off", {"auto": True}),
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
