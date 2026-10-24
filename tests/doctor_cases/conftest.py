"""Shared paths for the animation doctor's test cases (run through tests/test_doctor.py)."""
import os
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'skills', 'pixellab-pip', 'assets')
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
