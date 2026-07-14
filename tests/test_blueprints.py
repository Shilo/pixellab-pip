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

    def test_rejects_unknown_task_field(self) -> None:
        with self.assertRaisesRegex(AssertionError, "unknown fields"):
            qa.validate_blueprint_data(
                [
                    {"MCP create_character": {"description": "a knight"}},
                    {"TASK": {"instruction": "Package it.", "command": "tool --run"}},
                ],
                "test blueprint",
            )

    def test_rejects_malformed_pixellab_steps(self) -> None:
        for route in ("MCP ", "MCP create character", "POST /v2/create image"):
            with self.subTest(route=route), self.assertRaisesRegex(AssertionError, "route name must be nonblank"):
                qa.validate_blueprint_data({route: {}}, "test blueprint")
        with self.assertRaisesRegex(AssertionError, "request body must be an object"):
            qa.validate_blueprint_data({"POST /v2/create-image-pixen": None}, "test blueprint")

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


if __name__ == "__main__":
    unittest.main()
