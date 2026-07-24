#!/usr/bin/env python3

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    canonical = Path(__file__).resolve().parents[1] / "apply.py"
    sys.argv[0] = str(canonical)
    runpy.run_path(str(canonical), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
