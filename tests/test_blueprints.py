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

    def test_accepts_nested_defaults_and_the_rpg_numeric_size_fallback(self) -> None:
        placeholders = (
            "{{size | default: {{base size | default: 48}}}}",
            "{{size|default:{{base|default:{{minimum|default:32}}}}}}",
            '{{size | default: {{base | vendor: {"note": "| default: literal"} | default: 48}}}}',
        )
        for placeholder in placeholders:
            with self.subTest(placeholder=placeholder):
                qa.validate_blueprint_data(
                    {"MCP create_character": {"description": f"Use {placeholder} cells."}},
                    "test blueprint",
                )
                parsed = qa.iter_blueprint_placeholders(placeholder, "test blueprint")
                self.assertEqual(len(parsed), 1)
                self.assertEqual(qa.normalize_blueprint_default(parsed[0][1])[0], "placeholder")

        qa.validate_blueprint_data(
            {
                "MCP create_character": {
                    "size": '{{character size | default: {{RPG Maker version | map: '
                    '{"XP": 48, "VX": 32, "VX Ace": 32, "MV": 48, "MZ": 48}}}}}'
                }
            },
            "test blueprint",
        )
        qa.validate_blueprint_data(
            {
                "MCP create_character": {
                    "description": '{{size | default: {{base size | default: sword}}}} and '
                    '{{ SIZE | DEFAULT: {{ Base   Size | default: "sword" }} }}'
                }
            },
            "test blueprint",
        )

    def test_nested_defaults_preserve_quoted_and_json_literals(self) -> None:
        literals = (
            ('"{{invalid|default:}}"', "string", "{{invalid|default:}}"),
            ('{"note":"{{}} | default: literal"}', "object", {"note": "{{}} | default: literal"}),
            ('["{{}}", "| default: literal"]', "array", ["{{}}", "| default: literal"]),
            ('"| default: literal"', "string", "| default: literal"),
        )
        for literal, kind, expected in literals:
            with self.subTest(literal=literal):
                qa.validate_blueprint_data(
                    {"MCP create_character": {"options": "{{value | default: " + literal + "}}"}},
                    "test blueprint",
                )
                self.assertEqual(qa.normalize_blueprint_default(literal), (kind, expected))
        self.assertNotEqual(
            qa.normalize_blueprint_default("{{fallback}}"),
            qa.normalize_blueprint_default('"{{fallback}}"'),
        )

    def test_nonwhole_defaults_keep_placeholder_like_text_literal(self) -> None:
        for literal in (
            "{{}} suffix",
            "prefix {{}}",
            "{{base | default:}} suffix",
            "prefix {{base | default:}}",
            "{{}} {{other}}",
        ):
            with self.subTest(literal=literal):
                qa.validate_blueprint_data(
                    {"MCP create_character": {"description": "{{value | default: " + literal + "}}"}},
                    "test blueprint",
                )
                self.assertEqual(qa.normalize_blueprint_default(literal), ("string", literal))
                self.assertEqual(qa.blueprint_default_literal(literal), ("string", literal))

    def test_rejects_malformed_nested_defaults_and_nested_conflicts(self) -> None:
        invalid = (
            ("{{size | default: {{}}}}", "description must not be blank"),
            ("{{size | default: {{base | default:}}}}", "blank default"),
            ("{{size | default: {{base}}", "is not closed"),
            ("{{size | default: {{base}}}}}}", "closing marker without an opening"),
            ("{{size | default: {{base}}}} }} {{other}}", "closing marker without an opening"),
            ("{{size | default: {{base}} | default: 48}}", "multiple default markers"),
            ('{{size | default: {{base}}}} {{size | default: "{{base}}"}}', "conflicting defaults"),
            ("{{size | default: {{base | default: 32}}}} {{base | default: 48}}", "conflicting defaults"),
            (
                '{{size | default: {{version | map: {"MZ":32}}}}} '
                '{{size | default: {{version | map: {"MZ":48}}}}}',
                "conflicting defaults",
            ),
        )
        for placeholder, error in invalid:
            with self.subTest(placeholder=placeholder), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(
                    {"MCP create_character": {"description": placeholder}}, "test blueprint"
                )

    def test_nested_terminal_literals_keep_task_type_and_path_checks(self) -> None:
        invalid = (
            ({"instruction": "{{text | default: {{base | default: true}}}}"}, "instruction default must be a string"),
            (
                {"instruction": "Check.", "verify": "{{text | default: {{base | default: []}}}}"},
                "verify default must be a string",
            ),
            (
                {"instruction": "Package.", "inputs": '{{files | default: {{base | default: ["../outside.png"]}}}}'},
                "local relative paths",
            ),
            (
                {"instruction": "Package.", "inputs": "{{files | default: {{base | default: []}}}}"},
                "nonempty string array",
            ),
            (
                {"instruction": "Package.", "inputs": "{{files | default: {{base | default: false}}}}"},
                "default must be an array",
            ),
            (
                {"instruction": "Package.", "outputs": ["{{file | default: {{base | default: ../outside.png}}}}"]},
                "local relative paths",
            ),
            (
                {"instruction": "Package.", "outputs": ["{{file | default: {{base | default: true}}}}"]},
                "nonempty string array",
            ),
        )
        for task, error in invalid:
            with self.subTest(task=task), self.assertRaisesRegex(AssertionError, error):
                qa.validate_blueprint_data(
                    [{"MCP create_character": {}}, {"TASK": task}], "test blueprint"
                )

        for default in ('[1, 2]', '{"x":1}'):
            with self.subTest(default=default), self.assertRaisesRegex(AssertionError, "non-scalar default embedded"):
                qa.validate_blueprint_data(
                    {"MCP create_character": {"description": "Use {{size | default: {{base | default: " + default + "}}}} cells."}},
                    "test blueprint",
                )
        qa.validate_blueprint_data(
            [
                {"MCP create_character": {}},
                {
                    "TASK": {
                        "instruction": "Package.",
                        "inputs": '{{files | default: {{base | default: ["{{}}.png"]}}}}',
                    }
                },
            ],
            "test blueprint",
        )

    def test_unknown_nested_modifiers_do_not_imply_a_terminal_result_type(self) -> None:
        fallback = '{{name | map: {"x": "a.png"} | default: [1]}}'
        self.assertIsNone(qa.blueprint_default_literal(fallback))
        qa.validate_blueprint_data(
            [
                {"MCP create_character": {"description": "Use {{value | default: " + fallback + "}} cells."}},
                {"TASK": {"instruction": "{{text | default: " + fallback + "}}"}},
            ],
            "test blueprint",
        )
        with self.assertRaisesRegex(AssertionError, "conflicting defaults"):
            qa.validate_blueprint_data(
                {"MCP create_character": {"description": "{{value | default: " + fallback + "}} {{name | default: 48}}"}},
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


BUNDLED = REPO_ROOT / "skills/pixellab-pip/blueprints"
PRODUCTION_BLUEPRINTS = (
    "overhead-axe-chop",
    "character-candidates",
    "projectile-skill",
    "vfx-strike-single-target",
    "vfx-wave-across-party",
    "vfx-eruption-per-target",
)
FORBIDDEN_KEYS = {
    "cost", "costs", "est_cost", "generations", "spent", "reported_usage",
    "balance", "job_id", "job_ids", "background_job_id",
}


def iter_keys(value: object):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from iter_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_keys(item)


class ProductionBlueprintTests(unittest.TestCase):
    def test_production_blueprints_validate_and_stay_portable(self) -> None:
        import json
        import re

        for name in PRODUCTION_BLUEPRINTS:
            with self.subTest(blueprint=name):
                path = BUNDLED / f"{name}.blueprint.json"
                self.assertTrue(path.exists(), f"missing {path.name}")
                text = path.read_text(encoding="utf-8")
                data = json.loads(text)
                qa.validate_blueprint_data(data, path.name)
                steps = data if isinstance(data, list) else [data]
                calls = [k for step in steps for k in step if k.startswith(("MCP ", "POST /v2/"))]
                self.assertTrue(calls, "needs at least one PixelLab call")
                bad = {k for k in iter_keys(data) if k.casefold() in FORBIDDEN_KEYS}
                self.assertFalse(bad, f"cost/job keys: {bad}")
                self.assertIsNone(re.search(r"(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/", text), "machine path")


if __name__ == "__main__":
    unittest.main()
