#!/usr/bin/env python3
"""Report standards adoption health without requiring third-party packages."""

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
    return [
        Check("Foundation", "Project README", 5, exists("README.md"), "Add README.md."),
        Check("Foundation", "Canonical agent contract", 7, exists("AGENTS.md"), "Add AGENTS.md."),
        Check("Foundation", "Project configuration", 4, exists("project.yml") or exists("project.config.example.yml"), "Add project.yml or the example configuration."),
        Check("AI governance", "Conditional context manifest", 5, exists("agent-context.yml"), "Add agent-context.yml."),
        Check("AI governance", "Tool permission policy", 6, exists("agent-policy.yml"), "Add agent-policy.yml."),
        Check("AI governance", "Machine-readable feature state", 5, exists("docs/work/_template/state.yml"), "Add the feature state template."),
        Check("AI governance", "Behavior evaluation contracts", 5, exists("evals/agent-behavior/scenarios.json"), "Add agent behavior evaluation scenarios."),
        Check("AI governance", "Agent governance validator", 5, exists("scripts/validate_agent_governance.py"), "Add the agent governance validator."),
        Check("Adapters", "Claude Code adapter", 2, exists("CLAUDE.md"), "Add CLAUDE.md."),
        Check("Adapters", "Gemini CLI adapter", 2, exists("GEMINI.md"), "Add GEMINI.md."),
        Check("Adapters", "Cursor adapter", 2, exists(".cursor/rules/project-standards.mdc"), "Add a Cursor project rule."),
        Check("Adapters", "Aider adapter", 2, exists(".aider.conf.yml"), "Add an Aider configuration."),
        Check("Documentation", "Architecture overview", 4, exists("docs/architecture/overview.md"), "Document the current architecture."),
        Check("Documentation", "Workflow decision guide", 3, exists("docs/getting-started/workflow-decision-tree.md"), "Add the workflow decision tree."),
        Check("Documentation", "Operations guidance", 3, exists("docs/operations/README.md"), "Add operations guidance."),
        Check("Documentation", "Design standards", 3, exists("docs/design/README.md"), "Add UX/UI standards."),
        Check("Verification", "Stable verify command", 8, contains(taskfile, "  verify:"), "Add task verify."),
        Check("Verification", "Repository validator", 5, exists("scripts/validate_repository.py"), "Add repository validation."),
        Check("Verification", "Shared verification script", 6, exists("scripts/verify_project.py"), "Add the shared local and CI verifier."),
        Check("Verification", "Stack verification extension point", 2, exists("scripts/verify.d/README.md"), "Add scripts/verify.d/README.md."),
        Check("CI", "Pull-request validation workflow", 6, exists(".github/workflows/project-validation.yml") or exists(".github/workflows/template-validation.yml"), "Add a validation workflow."),
        Check("CI", "Dependency review workflow", 4, exists(".github/workflows/dependency-review.yml"), "Add dependency review."),
        Check("Security", "Security policy", 4, exists("SECURITY.md"), "Add SECURITY.md."),
        Check("Security", "CODEOWNERS", 3, exists("CODEOWNERS"), "Add CODEOWNERS."),
        Check("Security", "Dependabot configuration", 3, exists(".github/dependabot.yml"), "Add Dependabot configuration."),
        Check("Delivery", "Pull request template", 3, exists(".github/PULL_REQUEST_TEMPLATE.md"), "Add a pull request template."),
        Check("Delivery", "Release policy", 2, exists("docs/engineering/release-management.md"), "Document release management."),
        Check("Delivery", "Rollback guidance", 3, exists("docs/operations/rollback.md"), "Document rollback."),
        Check("Usability", "Workflow recommender", 3, contains(taskfile, "  recommend:"), "Add task recommend."),
        Check("Usability", "Doctor command", 3, contains(taskfile, "  doctor:"), "Add task doctor."),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Report standards adoption health.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when the adoption score is below 80.")
    args = parser.parse_args()

    checks = collect_checks()
    earned = sum(check.points for check in checks if check.passed)
    possible = sum(check.points for check in checks)
    score = round(earned * 100 / possible)

    print("Standards adoption health\n")
    for category in sorted({check.category for check in checks}):
        print(category)
        for check in [item for item in checks if item.category == category]:
            marker = "PASS" if check.passed else "MISS"
            print(f"  [{marker}] {check.label}")
        print()

    print(f"Adoption score: {score}/100")
    if score >= 90:
        print("Status: strong standards adoption baseline")
    elif score >= 80:
        print("Status: usable standards baseline with a few gaps")
    elif score >= 60:
        print("Status: partial standards adoption")
    else:
        print("Status: foundational standards missing")

    print("\nImportant")
    print("- This score measures the presence of governance and delivery controls, not whether the application is secure, usable, production-ready, or correctly configured in external systems.")

    missing = [check for check in checks if not check.passed]
    if missing:
        print("\nNext actions")
        for check in sorted(missing, key=lambda item: item.points, reverse=True)[:5]:
            print(f"- {check.action}")

    print("\nManual and evidence checks")
    print("- Confirm GitHub rulesets, required checks, secret scanning, CodeQL, Actions token permissions, and protected environments.")
    print("- Confirm project-specific tests, deployment, accessibility, observability, recovery, and security evidence are real rather than placeholders.")

    if args.strict and score < 80:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
