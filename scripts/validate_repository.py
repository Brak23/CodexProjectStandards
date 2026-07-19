#!/usr/bin/env python3
"""Validate the stack-agnostic template or a generated project."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
COMMON_REQUIRED = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
    "CODEOWNERS",
    "Taskfile.yml",
    "agent-context.yml",
    "agent-policy.yml",
    ".agent/PLANS.md",
    ".cursor/rules/project-standards.mdc",
    ".aider.conf.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/reusable-verify.yml",
    ".github/workflows/dependency-review.yml",
    "docs/README.md",
    "docs/architecture/overview.md",
    "docs/design/README.md",
    "docs/design/ux-ui-development.md",
    "docs/design/design-system.md",
    "docs/design/accessibility.md",
    "docs/design/responsive-design.md",
    "docs/design/content-design.md",
    "docs/design/usability-validation.md",
    "docs/design/ui-review-checklist.md",
    "docs/engineering/ai-assisted-development.md",
    "docs/engineering/agent-compatibility.md",
    "docs/engineering/context-loading.md",
    "docs/engineering/tool-permissions.md",
    "docs/engineering/approval-amendments.md",
    "docs/engineering/review-independence.md",
    "docs/engineering/session-recovery.md",
    "docs/engineering/multi-agent-coordination.md",
    "docs/engineering/agent-evaluations.md",
    "docs/engineering/enforcement-matrix.md",
    "docs/security/github-hardening.md",
    "docs/operations/production-readiness.md",
    "docs/work/_template/brief.md",
    "docs/work/_template/state.yml",
    "docs/work/_template/ux-requirements.md",
    "docs/work/_template/ui-verification.md",
    "evals/agent-behavior/scenarios.json",
    "scripts/bootstrap_project.py",
    "scripts/verify_project.py",
    "scripts/validate_agent_governance.py",
    "scripts/verify.d/README.md",
    "templates/licenses/MIT.txt",
    "templates/licenses/Apache-2.0.txt",
    "templates/licenses/Proprietary.txt",
]
TEMPLATE_REQUIRED = [
    ".github/workflows/template-validation.yml",
    "project.config.example.yml",
    "scripts/test_bootstrap.py",
    "examples/reference-project/package.json",
    "templates/github-actions/project-validation.yml",
    "templates/github-actions/semantic-release.yml.example",
]
PROJECT_REQUIRED = [
    "project.yml",
    ".github/workflows/project-validation.yml",
    "docs/getting-started/template-origin.md",
]

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ACTION = re.compile(r"uses:\s*([^\s@]+)@([^\s#]+)")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"}


def is_generated_project() -> bool:
    return (ROOT / "project.yml").exists()


def validate_required(errors: list[str]) -> None:
    required = COMMON_REQUIRED + (PROJECT_REQUIRED if is_generated_project() else TEMPLATE_REQUIRED)
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"missing required file: {relative}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            destination = (path.parent / unquote(target)).resolve()
            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not destination.exists():
                errors.append(f"broken local link: {path.relative_to(ROOT)} -> {target}")


def validate_actions(errors: list[str]) -> None:
    workflows = ROOT / ".github/workflows"
    if not workflows.exists():
        return
    for path in workflows.glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for action, ref in ACTION.findall(text):
            if action.startswith("./"):
                continue
            if not FULL_SHA.match(ref):
                errors.append(f"GitHub Action is not full-SHA pinned: {path.relative_to(ROOT)} {action}@{ref}")
        if "permissions:" not in text:
            errors.append(f"workflow lacks explicit permissions: {path.relative_to(ROOT)}")


def validate_generated_configuration(errors: list[str]) -> None:
    if not is_generated_project():
        return
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    if re.search(r"(?m)^/?project\.yml$", gitignore):
        errors.append("project.yml is canonical project metadata and must not be ignored")
    if (ROOT / ".github/workflows/template-validation.yml").exists():
        errors.append("generated project still contains template-only validation workflow")


def validate_text(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if not text.endswith("\n"):
            errors.append(f"missing final newline: {path.relative_to(ROOT)}")
        if "\t" in text and path.name != "Makefile":
            errors.append(f"tab character found: {path.relative_to(ROOT)}")
        if re.search(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][A-Za-z0-9_\-]{16,}", text):
            errors.append(f"possible committed secret: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_markdown_links(errors)
    validate_actions(errors)
    validate_generated_configuration(errors)
    validate_text(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
