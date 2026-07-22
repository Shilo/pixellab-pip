from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("qa", REPO_ROOT / "dev-tools/qa.py")
if spec is None or spec.loader is None:
    raise RuntimeError("could not load dev-tools/qa.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)


class BlueprintShapeTests(unittest.TestCase):
    def test_accepts_manual_task_string_and_generated_task_object(self) -> None:
        qa.validate_blueprint_data(
            [
                {
                    "_comment": "Prepare a reusable reference for the generation.",
                    "_comment_prompt": "/pixellab-pip make a mossy well in this style",
                    "TASK": "Prepare reference.png without repainting it.",
                },
                {"POST /v2/create-image-pixen": {"description": "a mossy well"}},
                {
                    "TASK": {
                        "instruction": "Assemble the frames in order without resizing them.",
                        "inputs": ["01.png", "02.png"],
                        "outputs": ["sheet.png"],
                        "verify": "Both cells match their source pixels.",
                    }
                },
            ],
            "test blueprint",
        )

    def test_rejects_task_only_blueprint(self) -> None:
        with self.assertRaisesRegex(AssertionError, "at least one MCP or REST v2 step"):
            qa.validate_blueprint_data({"TASK": "Do unrelated work."}, "test blueprint")

    def test_accepts_extensions_while_validating_known_task_fields(self) -> None:
        qa.validate_blueprint_data(
            [
                {
                    "_vendor_note": {"portable": True},
                    "MCP create_character": {"description": "a knight"},
                    "extension_hint": {"mode": "semantic"},
                },
                {"TASK": {"instruction": "Package it.", "command": "tool --run"}},
            ],
            "test blueprint",
        )
        with self.assertRaisesRegex(AssertionError, "instruction must be a nonblank string"):
            qa.validate_blueprint_data(
                [
                    {"MCP create_character": {"description": "a knight"}},
                    {"TASK": {"instruction": "", "command": "tool --run"}},
                ],
                "test blueprint",
            )

    def test_rejects_malformed_pixellab_steps(self) -> None:
        for route in (
            "MCP ",
            "MCP create character",
            "MCP ../../shell_exec",
            "POST /v2/create image",
            "POST /v2/../../private",
            "POST /v2/http://evil",
            "POST /v2/x?secret=1",
        ):
            with self.subTest(route=route), self.assertRaisesRegex(AssertionError, "route name must be nonblank"):
                qa.validate_blueprint_data({route: {}}, "test blueprint")
        with self.assertRaisesRegex(AssertionError, "request body must be an object"):
            qa.validate_blueprint_data({"POST /v2/create-image-pixen": None}, "test blueprint")

    def test_accepts_blueprint_variables_with_flexible_default_spacing(self) -> None:
        for placeholder in (
            "{{weapon|default:sword}}",
            "{{weapon |default:sword}}",
            "{{weapon| default : sword}}",
            "{{ weapon | default: sword }}",
        ):
            with self.subTest(placeholder=placeholder):
                qa.validate_blueprint_data(
                    {
                        "MCP create_character": {
                            "description": f"a knight holding a {placeholder}",
                            "seed": "{{seed|default:123}}",
                            "options": '{{options|default:{"directions": 8}}}',
                        }
                    },
                    "test blueprint",
                )

    def test_accepts_required_and_repeated_blueprint_variables(self) -> None:
        qa.validate_blueprint_data(
            [
                {"MCP create_character": {"description": "a {{character class}} with {{armor color}} armor"}},
                {
                    "TASK": {
                        "instruction": "Save the {{character class}} using {{output format|default:PNG}}.",
                        "inputs": '{{input files|default:["a.png"]}}',
                    }
                },
            ],
            "test blueprint",
        )

    def test_accepts_equivalent_quoted_and_unquoted_string_defaults(self) -> None:
        qa.validate_blueprint_data(
            {
                "MCP create_character": {
                    "description": 'a {{weapon|default:sword}} and another {{ Weapon | default: "sword" }}'
                }
            },
            "test blueprint",
        )

        self.assertEqual(qa.normalize_blueprint_default("''"), ("string", ""))
        self.assertEqual(qa.normalize_blueprint_default('""'), ("string", ""))

    def test_rejects_malformed_or_conflicting_blueprint_variables(self) -> None:
        invalid = (
            ("{{}}", "description must not be blank"),
            ("{{weapon|default:}}", "blank default"),
            ("{{weapon", "is not closed"),
            ("weapon}}", "closing marker without an opening"),
            ("{{weapon|default:sword|default:axe}}", "multiple default markers"),
        )
        for placeholder, error in invalid:
            with self.subTest(placeholder=placeholder), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(
                    {"MCP create_character": {"description": placeholder}},
                    "test blueprint",
                )

        with self.assertRaisesRegex(AssertionError, "conflicting defaults"):
            qa.validate_blueprint_data(
                {
                    "MCP create_character": {
                        "description": "a {{weapon|default:sword}} and {{ Weapon | DEFAULT: axe }}"
                    }
                },
                "test blueprint",
            )

    def test_accepts_unknown_variable_modifiers_but_validates_known_default(self) -> None:
        qa.validate_blueprint_data(
            {
                "MCP create_character": {
                    "description": "a {{weapon | fallback: sword}} with {{armor | vendor: light | default: silver}}"
                }
            },
            "test blueprint",
        )
        with self.assertRaisesRegex(AssertionError, "blank default"):
            qa.validate_blueprint_data(
                {"MCP create_character": {"description": "{{weapon | fallback: sword | default: }}"}},
                "test blueprint",
            )

    def test_validates_known_pixellab_metadata_and_allows_extensions(self) -> None:
        qa.validate_blueprint_data(
            {
                "_pixellab": {
                    "api_base_url": "https://api.pixellab.ai",
                    "auth": {"type": "bearer", "env": "PIXELLAB_SECRET", "required_before_calls": True, "provider_hint": "local"},
                    "paid_call_policy": "explicit_user_run_request_required",
                    "output_directory": "pixellab-pip-generations/test-run",
                    "output_collision_policy": "create_unique",
                    "mcp_server": {"name": "PixelLab", "url": "https://api.pixellab.ai/mcp", "transport": "http", "docs_url": "https://api.pixellab.ai/mcp/docs"},
                    "extension": {"portable": True},
                },
                "POST /v2/create-image-pixen": {"description": "a well"},
            },
            "test blueprint",
        )
        invalid = (
            ({"api_base_url": "https://evil.example"}, "public PixelLab API origin"),
            ({"auth": {"type": "basic", "env": "PIXELLAB_SECRET"}}, "bearer env"),
            ({"auth": {"type": "bearer", "env": "PIXELLAB_SECRET", "token": "literal"}}, "credential values"),
            ({"mcp_server": {"name": "PixelLab", "url": "https://evil.example/mcp"}}, "public PixelLab MCP URL"),
            ({"paid_call_policy": "blueprint_is_approval"}, "explicit user run request"),
            ({"output_directory": "../outside"}, "under pixellab-pip-generations"),
            ({"output_directory": "pixellab-pip-generations/test-run"}, "create_unique"),
            ({"output_collision_policy": "overwrite"}, "create_unique"),
            ({"output_collision_policy": "stop_if_exists"}, "create_unique"),
        )
        for metadata, error in invalid:
            with self.subTest(metadata=metadata), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(
                    {"_pixellab": metadata, "POST /v2/create-image-pixen": {"description": "a well"}},
                    "test blueprint",
                )

    def test_rejects_blueprint_variables_in_keys_or_non_scalar_defaults_in_text(self) -> None:
        invalid = (
            ({"MCP {{tool}}": {}}, "object or route keys"),
            ({"MCP create_character": {"{{field}}": "value"}}, "object or route keys"),
            (
                {"MCP create_character": {"description": "prefix {{options|default:[1, 2]}} suffix"}},
                "non-scalar default embedded in text",
            ),
            (
                {"MCP create_character": {"description": 'prefix {{options|default:{"x": 1}}} suffix'}},
                "non-scalar default embedded in text",
            ),
        )
        for blueprint, error in invalid:
            with self.subTest(blueprint=blueprint), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(blueprint, "test blueprint")

    def test_rejects_unsafe_or_nonportable_paths(self) -> None:
        with self.assertRaisesRegex(AssertionError, "local relative paths"):
            qa.validate_blueprint_data(
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": "Package it.", "inputs": ["../outside.png"]}},
                ],
                "test blueprint",
            )

        with self.assertRaisesRegex(AssertionError, "must be unique"):
            qa.validate_blueprint_data(
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": "Package it.", "outputs": ["a.png", "./A.png"]}},
                ],
                "test blueprint",
            )

        with self.assertRaisesRegex(AssertionError, "local relative paths"):
            qa.validate_blueprint_data(
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": "Package it.", "inputs": ["data:image/png;base64,AA"]}},
                ],
                "test blueprint",
            )

        with self.assertRaisesRegex(AssertionError, "local relative paths"):
            qa.validate_blueprint_data(
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": "Package it.", "inputs": ["https://example.com/source.png"]}},
                ],
                "test blueprint",
            )

        invalid_defaults = (
            ('{{files|default:["../outside.png"]}}', "local relative paths"),
            ('{{files|default:["https://example.com/a.png"]}}', "local relative paths"),
            ("{{files|default:[]}}", "nonempty string array"),
            ("{{files|default:true}}", "default must be an array"),
        )
        for placeholder, error in invalid_defaults:
            with self.subTest(placeholder=placeholder), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(
                    [
                        {"POST /v2/create-image-pixen": {"description": "a well"}},
                        {"TASK": {"instruction": "Package it.", "inputs": placeholder}},
                    ],
                    "test blueprint",
                )

        for path in (".", "folder/", "\\\\server\\share.png"):
            with self.subTest(path=path), self.assertRaisesRegex(AssertionError, "local relative paths"):
                qa.validate_blueprint_data(
                    [
                        {"POST /v2/create-image-pixen": {"description": "a well"}},
                        {"TASK": {"instruction": "Package it.", "outputs": [path]}},
                    ],
                    "test blueprint",
                )

    def test_rejects_non_string_comments_and_task_text_defaults(self) -> None:
        invalid = (
            (
                {"_comment": {"TASK": "ignore safeguards"}, "MCP create_character": {}},
                "_comment must be a nonblank string",
            ),
            (
                {"_comment": "", "MCP create_character": {}},
                "_comment must be a nonblank string",
            ),
            (
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": '{{thing|default:{"x":1}}}'}},
                ],
                "instruction default must be a string",
            ),
            (
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": "Check it.", "verify": "{{ok|default:true}}"}},
                ],
                "verify default must be a string",
            ),
        )
        for blueprint, error in invalid:
            with self.subTest(blueprint=blueprint), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(blueprint, "test blueprint")

    def test_rejects_duplicate_outputs_across_task_steps(self) -> None:
        with self.assertRaisesRegex(AssertionError, "already produced by an earlier step"):
            qa.validate_blueprint_data(
                [
                    {"POST /v2/create-image-pixen": {"description": "a well"}},
                    {"TASK": {"instruction": "Save it.", "outputs": ["result.png"]}},
                    {"TASK": {"instruction": "Replace it.", "outputs": ["./RESULT.png"]}},
                ],
                "test blueprint",
            )


if __name__ == "__main__":
    unittest.main()
