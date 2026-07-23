#!/usr/bin/env python3
"""Exercise the real bootstrap and governance configuration twice in an isolated copy."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_NAMES = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"}


def ignore(directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in EXCLUDED_NAMES or name.endswith(".pyc")}


def run(command: list[str], cwd: Path) -> None:
    print("+", " ".join(command))
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def snapshot(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED_NAMES for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def assert_generated(root: Path) -> None:
    required = ["project.yml", "README.md", "LICENSE", "CODEOWNERS", "planning-approval-roles.json", ".github/workflows/project-validation.yml", ".github/workflows/planning-structure.yml", ".github/workflows/planning-authority.yml", ".github/workflows/release.yml", "docs/getting-started/template-origin.md"]
    missing = [path for path in required if not (root / path).exists()]
    if missing:
        raise AssertionError("bootstrap did not create: " + ", ".join(missing))
    if (root / ".github/workflows/template-validation.yml").exists():
        raise AssertionError("template-only validation workflow remained after bootstrap")
    if (root / "examples/reference-project").exists():
        raise AssertionError("reference project should be removed by the default configuration")
    if "project.yml" in (root / ".gitignore").read_text(encoding="utf-8"):
        raise AssertionError("project.yml must be committed")
    readme = (root / "README.md").read_text(encoding="utf-8")
    if "Example Project" not in readme or "project.yml" not in readme:
        raise AssertionError("generated README is incomplete")
    codeowners = (root / "CODEOWNERS").read_text(encoding="utf-8")
    for token in ("@Brak23", "/.agents/skills/", "/docs/work/**/decisions/", "/planning-approval-roles.json"):
        if token not in codeowners:
            raise AssertionError(f"generated CODEOWNERS is incomplete: {token}")
    roles = json.loads((root / "planning-approval-roles.json").read_text(encoding="utf-8"))
    if "Brak23" not in roles["roles"]["engineering_owner"]["github_owners"]:
        raise AssertionError("planning approval roles were not configured from CODEOWNERS")
    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    if "Copyright (c) 2026 Example Owner" not in license_text:
        raise AssertionError("generated license did not use configured ownership")
    origin = (root / "docs/getting-started/template-origin.md").read_text(encoding="utf-8")
    if "https://github.com/Brak23/CodexProjectStandards" not in origin:
        raise AssertionError("template provenance is missing")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="codex-template-") as temporary:
        copy = Path(temporary) / "project"
        shutil.copytree(ROOT, copy, ignore=ignore)
        bootstrap = [sys.executable, "scripts/bootstrap_project.py", "--config", "project.config.example.yml"]
        governance = [sys.executable, "scripts/configure_review_governance.py"]
        run(bootstrap, copy)
        run(governance, copy)
        assert_generated(copy)
        first = snapshot(copy)
        run(bootstrap, copy)
        run(governance, copy)
        second = snapshot(copy)
        if first != second:
            changed = sorted(set(first) ^ set(second) | {path for path in first.keys() & second.keys() if first[path] != second[path]})
            raise AssertionError("bootstrap is not idempotent; changed on second run: " + ", ".join(changed))
        run([sys.executable, "scripts/validate_repository.py"], copy)
    print("Bootstrap integration test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
