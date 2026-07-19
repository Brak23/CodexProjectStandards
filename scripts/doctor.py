#!/usr/bin/env python3
"""Report repository adoption health without requiring third-party packages."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    category: str
    label: str
    points: int
    passed: bool
    action: str


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def contains(path: str, text: str) -> bool:
    target = ROOT / path
    return target.exists() and text in target.read_text(encoding="utf-8")


def collect_checks() -> list[Check]:
    taskfile = "Taskfile.yml"
    checks = [
        Check("Foundation", "Project README", 6, exists("README.md"), "Add README.md."),
        Check("Foundation", "Canonical agent contract", 8, exists("AGENTS.md"), "Add AGENTS.md."),
        Check("Foundation", "Project configuration", 5, exists("project.yml") or exists("project.config.example.yml"), "Add project.yml or the example configuration."),
        Check("Documentation", "Architecture overview", 5, exists("docs/architecture/overview.md"), "Document the current architecture."),
        Check("Documentation", "Workflow decision guide", 4, exists("docs/getting-started/workflow-decision-tree.md"), "Add the workflow decision tree."),
        Check("Documentation", "Operations guidance", 4, exists("docs/operations/README.md"), "Add operations guidance."),
        Check("Verification", "Stable verify command", 10, contains(taskfile, "  verify:"), "Add task verify."),
        Check("Verification", "Repository validator", 6, exists("scripts/validate_repository.py"), "Add repository validation."),
        Check("Verification", "Shared verification script", 8, exists("scripts/verify_project.py"), "Add the shared local and CI verifier."),
        Check("Verification", "Stack verification extension point", 3, exists("scripts/verify.d/README.md"), "Add scripts/verify.d/README.md."),
        Check("CI", "Pull-request validation workflow", 8, exists(".github/workflows/project-validation.yml") or exists(".github/workflows/template-validation.yml"), "Add a validation workflow."),
        Check("CI", "Dependency review workflow", 5, exists(".github/workflows/dependency-review.yml"), "Add dependency review."),
        Check("Security", "Security policy", 5, exists("SECURITY.md"), "Add SECURITY.md."),
        Check("Security", "CODEOWNERS", 4, exists("CODEOWNERS"), "Add CODEOWNERS."),
        Check("Security", "Dependabot configuration", 4, exists(".github/dependabot.yml"), "Add Dependabot configuration."),
        Check("Delivery", "Pull request template", 4, exists(".github/PULL_REQUEST_TEMPLATE.md"), "Add a pull request template."),
        Check("Delivery", "Release policy", 3, exists("docs/engineering/release-management.md"), "Document release management."),
        Check("Delivery", "Rollback guidance", 4, exists("docs/operations/rollback.md"), "Document rollback."),
        Check("Usability", "Workflow recommender", 4, contains(taskfile, "  recommend:"), "Add task recommend."),
        Check("Usability", "Doctor command", 4, contains(taskfile, "  doctor:"), "Add task doctor."),
    ]
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Report repository adoption health.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when the score is below 80.")
    args = parser.parse_args()

    checks = collect_checks()
    earned = sum(check.points for check in checks if check.passed)
    possible = sum(check.points for check in checks)
    score = round(earned * 100 / possible)

    print("Repository health\n")
    categories = sorted({check.category for check in checks})
    for category in categories:
        print(category)
        for check in [item for item in checks if item.category == category]:
            marker = "PASS" if check.passed else "MISS"
            print(f"  [{marker}] {check.label}")
        print()

    print(f"Overall: {score}/100")
    if score >= 90:
        print("Status: strong maintained-project baseline")
    elif score >= 80:
        print("Status: usable baseline with a few gaps")
    elif score >= 60:
        print("Status: partial adoption")
    else:
        print("Status: foundational controls missing")

    missing = [check for check in checks if not check.passed]
    if missing:
        print("\nNext actions")
        for check in sorted(missing, key=lambda item: item.points, reverse=True)[:5]:
            print(f"- {check.action}")

    print("\nManual GitHub check")
    print("- Confirm rulesets, required checks, secret scanning, CodeQL, Actions token permissions, and protected environments in GitHub Settings.")

    if args.strict and score < 80:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
