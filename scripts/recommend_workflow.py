#!/usr/bin/env python3
"""Recommend a workflow level from explicit risk questions."""

from __future__ import annotations

import argparse

HIGH_RISK_TERMS = {
    "auth", "authentication", "authorization", "permission", "payment", "billing",
    "financial", "sensitive", "regulated", "pii", "phi", "migration", "database",
    "infrastructure", "iam", "secret", "breaking", "encryption", "production data",
}
FEATURE_TERMS = {
    "feature", "api", "endpoint", "integration", "dependency", "refactor", "module",
    "background job", "queue", "schema", "workflow", "new screen", "new page",
}
LIGHT_TERMS = {"typo", "docs", "documentation", "copy", "small bug", "css", "display", "label"}


def yes_no(question: str) -> bool:
    while True:
        answer = input(f"{question} [y/N]: ").strip().lower()
        if answer in {"", "n", "no"}:
            return False
        if answer in {"y", "yes"}:
            return True
        print("Please answer y or n.")


def classify(description: str, interactive: bool) -> tuple[str, list[str]]:
    lowered = description.lower()
    reasons: list[str] = []

    matched_high = sorted(term for term in HIGH_RISK_TERMS if term in lowered)
    matched_feature = sorted(term for term in FEATURE_TERMS if term in lowered)
    matched_light = sorted(term for term in LIGHT_TERMS if term in lowered)

    high = bool(matched_high)
    feature = bool(matched_feature)

    if matched_high:
        reasons.append("High-risk topic detected: " + ", ".join(matched_high))
    if matched_feature:
        reasons.append("Meaningful feature/change topic detected: " + ", ".join(matched_feature))

    if interactive:
        if yes_no("Does this affect authentication, permissions, payments, sensitive data, production migrations, infrastructure access, secrets, or a breaking public contract?"):
            high = True
            reasons.append("You identified a high-risk surface.")
        if yes_no("Does this add meaningful behavior, span modules, add an API/integration/dependency, or require design tradeoffs?"):
            feature = True
            reasons.append("You identified a meaningful feature or cross-boundary change.")
        localized = yes_no("Is it localized, well understood, reversible, and low blast radius?")
    else:
        localized = bool(matched_light) and not feature and not high

    if high:
        return "HIGH-RISK", reasons
    if feature or not localized:
        if not reasons:
            reasons.append("The change is not clearly a tiny localized edit.")
        return "FULL FEATURE", reasons
    reasons.append("The change appears localized, reversible, and low risk.")
    return "LIGHT", reasons


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend Light, Full Feature, or High-Risk workflow.")
    parser.add_argument("description", nargs="*", help="Optional change description. Omit for interactive mode.")
    args = parser.parse_args()

    interactive = not args.description
    description = " ".join(args.description).strip()
    if interactive:
        description = input("Describe the change in one sentence: ").strip()
    if not description:
        print("A change description is required.")
        return 2

    workflow, reasons = classify(description, interactive)
    print(f"\nRecommended workflow: {workflow}\n")
    for reason in reasons:
        print(f"- {reason}")

    if workflow == "LIGHT":
        print("\nConfirm current behavior, make the smallest change, run focused tests and task verify, then open a PR.")
    elif workflow == "FULL FEATURE":
        print("\nCreate a feature workspace, approve the brief and plan, implement on a branch, independently review, and record verification evidence.")
    else:
        print("\nUse the full feature workflow plus the applicable threat model, migration, rollback, security review, staged rollout, and explicit human approvals.")

    print("\nGuide: docs/getting-started/workflow-decision-tree.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
