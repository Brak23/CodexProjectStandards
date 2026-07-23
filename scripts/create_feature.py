#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    feature = re.sub(r"[^A-Za-z0-9._-]+", "-", args.feature).strip("-")
    name = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-")
    display_name = args.name.replace("-", " ").title()
    destination = ROOT / "docs" / "work" / f"{feature}-{name}"
    if destination.exists():
        raise SystemExit(f"Feature workspace already exists: {destination.relative_to(ROOT)}")
    shutil.copytree(ROOT / "docs/work/_template", destination)
    for path in destination.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".yml", ".yaml", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("[Feature]", display_name)
        text = text.replace("[Name]", display_name)
        text = text.replace("[ID]", feature)
        path.write_text(text, encoding="utf-8")
    command = [
        sys.executable,
        ".agents/skills/feature-execution-planner/scripts/init_planning_workspace.py",
        "--work",
        str(destination),
        "--feature-id",
        feature,
        "--feature-name",
        display_name,
    ]
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode:
        shutil.rmtree(destination, ignore_errors=True)
        return completed.returncode
    print(destination.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
