"""Runs the animation doctor's test cases (tests/doctor_cases/test_*.py, plain functions with assert) under
unittest: each function becomes one test; a `tmp_path` parameter gets a fresh temporary folder.
The doctor needs numpy and scipy; without them these tests are skipped, as the helper itself skips."""
from __future__ import annotations

import importlib
import inspect
import sys
import tempfile
import unittest
from pathlib import Path

CASES = Path(__file__).resolve().parent / "doctor_cases"


def _case(module, name, func):
    def run() -> None:
        if "tmp_path" in inspect.signature(func).parameters:
            with tempfile.TemporaryDirectory() as tmp:
                func(Path(tmp))
        else:
            func()
    run.__name__ = f"{module.__name__}.{name}"
    return unittest.FunctionTestCase(run)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    try:
        import numpy  # noqa: F401
        import scipy  # noqa: F401
    except ImportError:
        suite.addTest(unittest.FunctionTestCase(lambda: (_ for _ in ()).throw(unittest.SkipTest("numpy/scipy missing"))))
        return suite
    sys.path.insert(0, str(CASES))
    import conftest  # noqa: F401  (puts the doctor's folder on the path)
    for path in sorted(CASES.glob("test_*.py")):
        module = importlib.import_module(path.stem)
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("test_") and func.__module__ == module.__name__:
                suite.addTest(_case(module, name, func))
    return suite
