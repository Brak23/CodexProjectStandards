#!/usr/bin/env python3
"""Recommend evidence and review from consequences, not keyword matches."""

from __future__ import annotations

import argparse

HINTS = {
    "trust boundary": ("auth", "authentication", "authorization", "permission", "secret", "crypto", "tenant"),
    "sensitive or regulated data": ("pii", "phi", "sensitive", "regulated"),
    "external or irreversible effect": ("payment", "billing", "delete", "migration", "production", "infrastructure", "iam"),
}


def yes_no(question: str) -> bool:
    while True:
        answer = input(f"{question} [y/N]: ").strip().lower()
        if answer in {"", "n", "no"}:
            return False
        if answer in {"y", "yes"}:
            return True
        print("Please answer y or n.")


def classify(description: str, facts: dict[str, bool]) -> tuple[str, list[str], list[str]]:
    reasons: list[str] = []
    unknowns: list[str] = []
    lowered = description.lower()
    hints = [name for name, terms in HINTS.items() if any(term in lowered for term in terms)]

    if facts["production_or_irreversible"]:
        reasons.append("The requested action affects production or has an irreversible external effect.")
    if facts["trust_or_sensitive"]:
        reasons.append("The changed behavior affects a trust boundary or sensitive data.")
    if facts["production_or_irreversible"] or facts["trust_or_sensitive"]:
        return "HIGH_RISK", reasons, unknowns

    if facts["cross_boundary"]:
        reasons.append("The change spans a shared boundary, introduces meaningful behavior, or needs a tradeoff.")
    if facts["hard_to_reverse"]:
        reasons.append("Rollback would be difficult or operationally risky.")
    if facts["material_unknown"]:
        unknowns.append("A material requirement, environment, or verification path is still unknown.")
    if facts["cross_boundary"] or facts["hard_to_reverse"] or facts["material_unknown"]:
        return "MEANINGFUL", reasons, unknowns

    if hints:
        reasons.append("Terms worth inspecting: " + ", ".join(hints) + ". They are not a risk classification by themselves.")
    reasons.append("The change appears localized, reversible, and well understood.")
    return "ROUTINE", reasons, unknowns


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend routine, meaningful, or high-risk workflow evidence.")
    parser.add_argument("description", nargs="*", help="Optional change description.")
    parser.add_argument("--trust-or-sensitive", action="store_true")
    parser.add_argument("--production-or-irreversible", action="store_true")
    parser.add_argument("--cross-boundary", action="store_true")
    parser.add_argument("--hard-to-reverse", action="store_true")
    parser.add_argument("--material-unknown", action="store_true")
    args = parser.parse_args()

    interactive = not args.description
    description = " ".join(args.description).strip()
    if interactive:
        description = input("Describe the change in one sentence: ").strip()
    if not description:
        print("A change description is required.")
        return 2

    facts = {
        "trust_or_sensitive": args.trust_or_sensitive,
        "production_or_irreversible": args.production_or_irreversible,
        "cross_boundary": args.cross_boundary,
        "hard_to_reverse": args.hard_to_reverse,
        "material_unknown": args.material_unknown,
    }
    if interactive:
        facts["trust_or_sensitive"] = yes_no("Does executable behavior affect a trust boundary, permissions, secrets, sensitive, or regulated data?")
        facts["production_or_irreversible"] = yes_no("Does the requested action affect production or create an irreversible external effect?")
        facts["cross_boundary"] = yes_no("Does it add meaningful behavior, span shared modules, add a dependency, or need an architecture/design tradeoff?")
        facts["hard_to_reverse"] = yes_no("Would rollback be difficult, incomplete, or operationally risky?")
        facts["material_unknown"] = yes_no("Is a material requirement, environment, or verification path unknown?")

    workflow, reasons, unknowns = classify(description, facts)
    print(f"\nRecommended workflow: {workflow}\n")
    for reason in reasons:
        print(f"- {reason}")
    for unknown in unknowns:
        print(f"- Unknown: {unknown}")

    if workflow == "ROUTINE":
        print("\nConfirm current behavior, implement the coherent change, run focused checks, and demonstrate the result.")
    elif workflow == "MEANINGFUL":
        print("\nCreate or update work.md, inspect the affected boundaries, plan verification and review, then implement.")
    else:
        print("\nRecord the consequential surface, use the required security/data/recovery evidence, and obtain any missing environment or release authorization.")

    print("\nThis is advisory. Inspect code and the requested action before deciding; words in a description are evidence hints, not proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
