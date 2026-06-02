#!/usr/bin/env python
"""Legacy entry point — runs minimal_blis_reproducer level ``pytest``."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    script = Path(__file__).resolve().parent / "minimal_blis_reproducer.py"
    cmd = [sys.executable, str(script), "--level", "pytest"]
    print("Running:", " ".join(cmd), flush=True)
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
