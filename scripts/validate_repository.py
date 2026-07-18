#!/usr/bin/env python3
"""Validate the stack-agnostic template without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "LICENSE",
    "CODEOWNERS",
    "Taskfile.yml",
    ".agent/PLANS.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/template-validation.yml",
    "docs/README.md",
    "docs/architecture/overview.md",
    "docs/engineering/ai-assisted-development.md",
    "docs/security/github-hardening.md",
    "docs/operations/production-readiness.md",
    "docs/work/_template/brief.md",
    "scripts/bootstrap_project.py",
]

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
ACTION = re.compile(r"uses:\s*([^\s@]+)@([^\s#]+)")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def validate_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).exists():
            errors.append(f"missing required file: {relative}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
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
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for action, ref in ACTION.findall(text):
            if action.startswith("./"):
                continue
            if not FULL_SHA.match(ref):
                errors.append(f"GitHub Action is not full-SHA pinned: {path.relative_to(ROOT)} {action}@{ref}")
        if "permissions:" not in text:
            errors.append(f"workflow lacks explicit permissions: {path.relative_to(ROOT)}")


def validate_text(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
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
