#!/usr/bin/env python3
"""Exercise delegated defaults, formal compatibility, and application verification states."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"}


def ignore(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED or name.endswith(".pyc")}


def run(command: list[str], cwd: Path, expected: int = 0) -> None:
    result = subprocess.run(command, cwd=cwd, check=False, text=True, capture_output=True)
    if result.returncode != expected:
        raise AssertionError(f"expected {expected}, got {result.returncode}: {' '.join(command)}\n{result.stdout}\n{result.stderr}")


def set_mode(path: Path, mode: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("governance_mode: delegated", f"governance_mode: {mode}")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    authority_path = ROOT / ".agents/skills/feature-execution-planner/scripts/validate_planning_authority.py"
    sys.path.insert(0, str(authority_path.parent))
    spec = importlib.util.spec_from_file_location("planning_authority", authority_path)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load planning authority validator")
    authority = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(authority)
    if authority.planning_gate(["project.yml"]) != "MODE_TRANSITION":
        raise AssertionError("project mode transition was not detected")
    if authority.planning_gate(["project.yml", "docs/work/APP-001/brief.md"]) != "MIXED":
        raise AssertionError("mode transition may bypass a formal planning change")
    with tempfile.TemporaryDirectory(prefix="codex-governance-") as temporary:
        copy = Path(temporary) / "project"
        shutil.copytree(ROOT, copy, ignore=ignore)
        config = copy / "project.config.example.yml"
        set_mode(config, "formal")
        run([sys.executable, "scripts/bootstrap_project.py", "--config", "project.config.example.yml"], copy)
        run([sys.executable, "scripts/configure_review_governance.py"], copy)
        for required in ("planning-approval-roles.json", ".github/workflows/planning-structure.yml", ".github/workflows/planning-authority.yml"):
            if not (copy / required).exists():
                raise AssertionError(f"formal bootstrap removed {required}")
        run([sys.executable, "scripts/create_feature.py", "--feature", "APP-002", "--name", "formal-feature"], copy)
        if not (copy / "docs/work/APP-002-formal-feature/planning-model.json").exists():
            raise AssertionError("formal feature creation did not use model-v2 workspace")

        (copy / "project.yml").write_text((copy / "project.yml").read_text(encoding="utf-8").replace('governance_mode: "formal"\n', ""), encoding="utf-8")
        run([sys.executable, "scripts/create_feature.py", "--feature", "APP-003", "--name", "legacy-feature"], copy)
        if not (copy / "docs/work/APP-003-legacy-feature/planning-model.json").exists():
            raise AssertionError("project without governance mode did not retain formal behavior")

        # The template source may itself contain application verification hooks.
        # Isolate this fixture before asserting the generated project's
        # NOT_CONFIGURED state.
        hooks = copy / "scripts/verify.d"
        inherited_hooks = [
            path for path in hooks.iterdir()
            if path.is_file() and path.name != "README.md"
        ] if hooks.exists() else []
        for path in inherited_hooks:
            path.unlink()

        run([sys.executable, "scripts/verify_app.py"], copy, expected=2)
        hook = hooks / "application.py"
        hook.write_text("print('application check passed')\n", encoding="utf-8")
        run([sys.executable, "scripts/verify_app.py"], copy)

        # Regression: configured application checks must survive full project
        # verification instead of breaking this governance fixture.
        run([sys.executable, "scripts/verify_project.py"], copy)
    print("Governance mode integration test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
