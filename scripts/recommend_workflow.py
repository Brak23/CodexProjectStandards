#!/usr/bin/env python3
"""Recommend a workflow level from impact, reversibility, and risk questions."""

from __future__ import annotations

import argparse

HIGH_RISK_TERMS = {
    "auth", "authentication", "authorization", "permission", "payment", "billing",
    "financial", "sensitive", "regulated", "pii", "phi", "migration", "production data",
    "infrastructure", "iam", "secret", "breaking", "encryption", "tenant isolation",
}
FEATURE_TERMS = {
    "feature", "api", "endpoint", "integration", "dependency", "refactor", "module",
    "background job", "queue", "schema", "workflow", "new screen", "new page",
    "global css", "theme token", "design system", "shared component",
}
LIGHT_TERMS = {"typo", "docs", "documentation", "copy edit", "small bug", "display issue", "label text"}


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
    localized = bool(matched_light) and not high and not feature

    if matched_high:
        reasons.append("High-risk surface detected: " + ", ".join(matched_high))
    if matched_feature:
        reasons.append("Meaningful or cross-boundary change detected: " + ", ".join(matched_feature))

    if interactive:
        trust_or_sensitive = yes_no("Does this affect trust boundaries, permissions, payments, sensitive data, secrets, or regulated behavior?")
        production_or_contract = yes_no("Does this affect production data, migrations, infrastructure, or a breaking public contract?")
        cross_boundary = yes_no("Does this add behavior, span modules, change shared UI, add a dependency, or require architecture/design tradeoffs?")
        low_reversibility = yes_no("Would rollback be difficult, incomplete, or operationally risky?")
        meaningful_unknowns = yes_no("Are important requirements, failure modes, environments, or verification paths still uncertain?")
        localized = yes_no("Is the change localized, well understood, easily reversible, and low blast radius?")

        if trust_or_sensitive or production_or_contract or low_reversibility:
            high = True
            reasons.append("Impact or reversibility requires the high-risk workflow.")
        if cross_boundary or meaningful_unknowns:
            feature = True
            reasons.append("Scope or uncertainty requires specification and planning.")

    if high:
        return "HIGH-RISK", reasons
    if feature or not localized:
        if not reasons:
            reasons.append("The change is not clearly localized, reversible, and low blast radius.")
        return "FULL FEATURE", reasons
    reasons.append("The change appears localized, reversible, well understood, and low risk.")
    return "LIGHT", reasons


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend Light, Full Feature, or High-Risk workflow.")
    parser.add_argument("description", nargs="*", help="Optional change description. Omit for interactive impact questions.")
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
        print("\nUse the full feature workflow plus applicable specialist review, threat model, migration, rollback, staged rollout, and explicit human approvals.")

    print("\nAdvisory only: classify upward when discovery reveals greater blast radius, lower reversibility, new trust boundaries, public contracts, or material unknowns.")
    print("Guide: docs/getting-started/workflow-decision-tree.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
