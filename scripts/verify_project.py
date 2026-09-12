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
    run([sys.executable, "scripts/validate_agent_governance.py"])
    run([sys.executable, ".agents/skills/code-review/scripts/validate_review_artifacts.py", "--contracts-only"])
    run([sys.executable, "scripts/test_code_review_skill.py"])
    run([sys.executable, ".agents/skills/feature-execution-planner/scripts/validate_planning_artifacts.py", "--contracts-only"])
    run([sys.executable, "scripts/test_feature_planner_skill.py"])
    run([sys.executable, "scripts/doctor.py", "--strict"])
    run([sys.executable, "scripts/recommend_workflow.py", "add", "a", "new", "API", "endpoint"])
    project_config = ROOT / "project.yml"
    if project_config.exists():
        run([sys.executable, "scripts/bootstrap_project.py", "--config", "project.yml", "--dry-run"])
    else:
        run([sys.executable, "scripts/test_bootstrap.py"])
    run([sys.executable, "scripts/test_governance_modes.py"])
    reference = ROOT / "examples/reference-project/package.json"
    if reference.exists():
        run(["node", "--test"], reference.parent)
    run([sys.executable, "scripts/verify_app.py"])
    print("Repository verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
