#!/usr/bin/env python3
"""Validate portable agent context, permissions, state, skills, and eval contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_PERMISSION_STATUSES = {"allowed", "approval_required", "prohibited"}


def read(path: str, errors: list[str]) -> str:
    target = ROOT / path
    if not target.exists():
        errors.append(f"missing required AI governance file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def require_tokens(path: str, tokens: list[str], errors: list[str]) -> None:
    text = read(path, errors)
    for token in tokens:
        if token not in text:
            errors.append(f"{path} missing required token: {token}")


def validate_context_manifest(errors: list[str]) -> None:
    text = read("agent-context.yml", errors)
    for token in (
        "version: 4",
        "always:",
        "when:",
        "repository_orientation:",
        "independent_review:",
        "security_or_privacy:",
        "agent_handoff_or_resume:",
    ):
        if token not in text:
            errors.append(f"agent-context.yml missing required token: {token}")

    before_rules = text.split("\nrules:\n", 1)[0]
    for raw in before_rules.splitlines():
        stripped = raw.strip()
        if not stripped.startswith("- "):
            continue
        relative = stripped[2:].strip()
        if relative == "project.yml" and not (ROOT / relative).exists() and (ROOT / "project.config.example.yml").exists():
            continue
        if not (ROOT / relative).exists():
            errors.append(f"agent-context.yml references missing path: {relative}")


def validate_tool_policy(errors: list[str]) -> None:
    text = read("agent-policy.yml", errors)
    for token in ("version: 1", "default: prohibited", "production_database:", "production_deployment:", "secrets_read_or_output:"):
        if token not in text:
            errors.append(f"agent-policy.yml missing required token: {token}")
    statuses = [line.split(":", 1)[1].strip() for line in text.splitlines() if line.strip().startswith("status:")]
    if not statuses:
        errors.append("agent-policy.yml contains no permission statuses")
    for status in statuses:
        if status not in ALLOWED_PERMISSION_STATUSES:
            errors.append(f"agent-policy.yml contains invalid permission status: {status}")


def validate_scenarios(path: str, minimum: int, required: set[str], errors: list[str]) -> None:
    target = ROOT / path
    if not target.exists():
        errors.append(f"missing evaluation file: {path}")
        return
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid evaluation JSON {path}: {exc}")
        return

    scenarios = payload.get("scenarios")
    if payload.get("version") != 1:
        errors.append(f"{path} version must be 1")
    if not isinstance(scenarios, list) or len(scenarios) < minimum:
        errors.append(f"{path} must contain at least {minimum} scenarios")
        return

    ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"{path} scenario {index} must be an object")
            continue
        missing = sorted(required - scenario.keys())
        if missing:
            errors.append(f"{path} scenario {index} missing: {', '.join(missing)}")
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"{path} scenario {index} has invalid id")
        elif scenario_id in ids:
            errors.append(f"duplicate evaluation id in {path}: {scenario_id}")
        else:
            ids.add(scenario_id)
        for list_key in ("required_behavior", "prohibited_behavior"):
            value = scenario.get(list_key)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{path} {scenario_id or index} {list_key} must be a non-empty string list")


def validate_evals(errors: list[str]) -> None:
    validate_scenarios(
        "evals/agent-behavior/scenarios.json",
        8,
        {
            "id",
            "category",
            "stimulus",
            "required_behavior",
            "prohibited_behavior",
            "expected_workflow",
            "expected_status",
            "expected_escalation",
        },
        errors,
    )
    validate_scenarios(
        "evals/code-review/scenarios.json",
        10,
        {"id", "category", "stimulus", "required_behavior", "prohibited_behavior"},
        errors,
    )


def validate_governance(errors: list[str]) -> None:
    validate_context_manifest(errors)
    validate_tool_policy(errors)
    require_tokens(
        "docs/work/_template/state.yml",
        ["phase: specification", "implementation_authorized: false", "release_authorized: false", "active_agent:", "base_commit:", "independent_review_level:"],
        errors,
    )
    require_tokens("GEMINI.md", ["@./AGENTS.md", "@./agent-context.yml", "@./agent-policy.yml"], errors)
    require_tokens(
        ".cursor/rules/project-standards.mdc",
        ["alwaysApply: true", "@AGENTS.md", "@agent-context.yml", "@agent-policy.yml"],
        errors,
    )
    require_tokens(".aider.conf.yml", ["read:", "AGENTS.md", "agent-context.yml", "agent-policy.yml", "yes-always: false"], errors)
    require_tokens(
        ".agents/skills/code-review/SKILL.md",
        ["name: code-review", "refs/reviews/snapshots", "Every binding finding includes a written acceptance criterion", "The merge gate"],
        errors,
    )
    require_tokens(
        "docs/engineering/review-system.md",
        ["Evidence requirements", "Scoped dimensions", "Seams", "Persistent ledger", "Merge gate"],
        errors,
    )

    for path in (
        "docs/engineering/context-loading.md",
        "docs/engineering/tool-permissions.md",
        "docs/engineering/approval-amendments.md",
        "docs/engineering/review-independence.md",
        "docs/engineering/review-system.md",
        "docs/engineering/session-recovery.md",
        "docs/engineering/multi-agent-coordination.md",
        "docs/engineering/agent-evaluations.md",
        "evals/agent-behavior/README.md",
        "evals/code-review/README.md",
    ):
        read(path, errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI platform governance contracts.")
    parser.add_argument("--evals-only", action="store_true", help="Validate only agent behavior evaluation scenarios.")
    args = parser.parse_args()

    errors: list[str] = []
    if not args.evals_only:
        validate_governance(errors)
    validate_evals(errors)

    if errors:
        print("AI governance validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.evals_only:
        print("Agent behavior evaluation contracts passed structural validation.")
        print("No model was invoked; connect scenario files to a model-specific harness for behavioral results.")
    else:
        print("AI platform governance validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
