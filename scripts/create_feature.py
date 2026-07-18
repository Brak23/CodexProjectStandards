#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    feature = re.sub(r"[^A-Za-z0-9._-]+", "-", args.feature).strip("-")
    name = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-")
    destination = ROOT / "docs/work" / f"{feature}-{name}"
    if destination.exists():
        raise SystemExit(f"Feature workspace already exists: {destination.relative_to(ROOT)}")
    shutil.copytree(ROOT / "docs/work/_template", destination)
    for path in destination.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        text = text.replace("[Feature]", args.name.replace("-", " ").title())
        text = text.replace("[Name]", args.name.replace("-", " ").title())
        text = text.replace("[ID]", feature)
        path.write_text(text, encoding="utf-8")
    print(destination.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
