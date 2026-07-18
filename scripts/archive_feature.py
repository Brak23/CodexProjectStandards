#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True)
    args = parser.parse_args()
    source = (ROOT / args.work).resolve()
    work_root = (ROOT / "docs/work").resolve()
    if source.parent != work_root or source.name.startswith("_") or not source.is_dir():
        raise SystemExit("WORK must be a direct feature directory under docs/work/")
    destination_root = work_root / "archive"
    destination_root.mkdir(exist_ok=True)
    destination = destination_root / source.name
    if destination.exists():
        raise SystemExit(f"Archive already exists: {destination.relative_to(ROOT)}")
    shutil.move(str(source), destination)
    print(destination.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
