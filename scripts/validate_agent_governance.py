#!/usr/bin/env python3
"""Validate portable agent context, permissions, state, adapters, and eval contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


def validate_evals(errors: list[str]) -> None:
    path = ROOT / "evals/agent-behavior/scenarios.json"
    if not path.exists():
        errors.append("missing required AI governance file: evals/agent-behavior/scenarios.json")
        return
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid agent evaluation JSON: {exc}")
        return

    scenarios = payload.get("scenarios")
    if payload.get("version") != 1:
        errors.append("agent evaluation version must be 1")
    if not isinstance(scenarios, list) or len(scenarios) < 8:
        errors.append("agent evaluation suite must contain at least 8 scenarios")
        return

    required = {
        "id",
        "category",
        "stimulus",
        "required_behavior",
        "prohibited_behavior",
        "expected_workflow",
        "expected_status",
        "expected_escalation",
    }
    ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"agent evaluation scenario {index} must be an object")
            continue
        missing = sorted(required - scenario.keys())
        if missing:
            errors.append(f"agent evaluation scenario {index} missing: {', '.join(missing)}")
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"agent evaluation scenario {index} has invalid id")
        elif scenario_id in ids:
            errors.append(f"duplicate agent evaluation id: {scenario_id}")
        else:
            ids.add(scenario_id)
        for list_key in ("required_behavior", "prohibited_behavior"):
            value = scenario.get(list_key)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{scenario_id or index} {list_key} must be a non-empty string list")


def validate_governance(errors: list[str]) -> None:
    require_tokens(
        "agent-context.yml",
        ["version: 1", "always:", "when:", "user_facing_ui:", "security_or_privacy:", "agent_handoff_or_resume:"],
        errors,
    )
    require_tokens(
        "agent-policy.yml",
        ["default: prohibited", "approval_required", "production_database:", "production_deployment:", "secrets_read_or_output:"],
        errors,
    )
    require_tokens(
        "docs/work/_template/state.yml",
        ["phase: specification", "implementation_authorized: false", "release_authorized: false", "active_agent:", "base_commit:"],
        errors,
    )
    require_tokens("GEMINI.md", ["@./AGENTS.md", "@./agent-context.yml", "@./agent-policy.yml"], errors)
    require_tokens(
        ".cursor/rules/project-standards.mdc",
        ["alwaysApply: true", "@AGENTS.md", "@agent-context.yml", "@agent-policy.yml"],
        errors,
    )
    require_tokens(".aider.conf.yml", ["read:", "AGENTS.md", "agent-context.yml", "agent-policy.yml", "yes-always: false"], errors)

    for path in (
        "docs/engineering/context-loading.md",
        "docs/engineering/tool-permissions.md",
        "docs/engineering/approval-amendments.md",
        "docs/engineering/review-independence.md",
        "docs/engineering/session-recovery.md",
        "docs/engineering/multi-agent-coordination.md",
        "docs/engineering/agent-evaluations.md",
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
        print("No model was invoked; connect scenarios.json to a model-specific harness for behavioral results.")
    else:
        print("AI platform governance validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
