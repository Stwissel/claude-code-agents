"""Test configuration for test-design-reviewer tests.

Adds the lib directory to sys.path at import time so test modules
can import core, scoring directly.
"""

import sys
from pathlib import Path


_lib_dir = str(Path(__file__).resolve().parents[2] / "skills" / "test-design-reviewer" / "lib")
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)
