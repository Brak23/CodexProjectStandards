#!/usr/bin/env python3
"""Run the repository's stack-agnostic verification contract."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(command))
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> int:
    run([sys.executable, "scripts/validate_repository.py"])

    project_config = ROOT / "project.yml"
    if project_config.exists():
        run([sys.executable, "scripts/bootstrap_project.py", "--config", "project.yml", "--dry-run"])
    else:
        run([sys.executable, "scripts/test_bootstrap.py"])

    reference = ROOT / "examples/reference-project/package.json"
    if reference.exists():
        run(["node", "--test"], reference.parent)

    hooks = ROOT / "scripts/verify.d"
    if hooks.exists():
        for hook in sorted(path for path in hooks.iterdir() if path.is_file() and path.name != "README.md"):
            if hook.suffix == ".py":
                run([sys.executable, str(hook.relative_to(ROOT))])
            elif hook.suffix == ".sh":
                run(["bash", str(hook.relative_to(ROOT))])
            elif os.access(hook, os.X_OK):
                run([str(hook.relative_to(ROOT))])
            else:
                raise SystemExit(f"Verification hook is not executable or supported: {hook.relative_to(ROOT)}")

    print("Repository verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
