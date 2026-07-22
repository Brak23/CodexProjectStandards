#!/usr/bin/env python3
"""Validate code-review skill contracts and review JSON artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / ".agents/skills/code-review"
VALID_VERDICTS = {"APPROVE", "APPROVE_WITH_COMMENTS", "CHANGES_REQUESTED", "CANNOT_ASSESS"}
OWNER_ONLY_ACTIONS = {"RESOLVED", "STILL_OPEN", "WITHDRAWN", "SUPERSEDED"}
HUMAN_ONLY_ACTIONS = {"WAIVED", "AUTHORITY_OVERRIDE"}


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path}: {exc}")
        return None


def require_files(errors: list[str]) -> None:
    required = [
        "SKILL.md",
        "references/record-model.md",
        "references/review-storage.md",
        "references/aggregation-and-gate.md",
        "config/review-policy.example.json",
        "config/dimension-registry.example.json",
        "config/seam-registry.example.json",
        "config/evidence-requirements.example.json",
        "config/review-triggers.example.json",
        "schemas/snapshot.schema.json",
        "schemas/finding.schema.json",
        "schemas/review-result.schema.json",
        "schemas/coordination.schema.json",
        "schemas/evidence-manifest.schema.json",
        "schemas/finding-ledger.schema.json",
        "schemas/aggregate-review.schema.json",
        "schemas/merge-gate.schema.json",
        "scripts/capture_review_snapshot.py",
        "scripts/compose_requirements.py",
        "scripts/review_store.py",
        "scripts/reconcile_findings.py",
        "scripts/aggregate_reviews.py",
        "scripts/evaluate_merge_gate.py",
        "templates/review-request.json",
        "templates/coordination.json",
        "templates/evidence-manifest.json",
        "templates/repository-state.json",
    ]
    for relative in required:
        if not (SKILL / relative).exists():
            errors.append(f"missing code-review skill file: {relative}")


def validate_finding(record: dict, label: str, errors: list[str]) -> None:
    if record.get("authority") != "BLOCKING":
        return
    if record.get("record_type") not in {"dimension_finding", "seam_finding"}:
        errors.append(f"{label}: only dimension or seam findings may be blocking")
    criterion = record.get("acceptance_criterion")
    if not isinstance(criterion, dict) or not criterion.get("statement"):
        errors.append(f"{label}: binding finding lacks acceptance criterion")
    if not record.get("closure_authority"):
        errors.append(f"{label}: binding finding lacks closure authority")
    if not record.get("fingerprint") and not record.get("fingerprint_sha256"):
        errors.append(f"{label}: binding finding lacks stable fingerprint")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{label}: binding finding lacks evidence")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict) or not item.get("decision_excerpt"):
                errors.append(f"{label}: evidence {index} lacks decision_excerpt")
            if isinstance(item, dict) and item.get("external_locator") and "retention_until" not in item:
                errors.append(f"{label}: external evidence {index} lacks explicit retention_until")


def validate_review(payload: dict, label: str, errors: list[str]) -> None:
    owned = payload.get("owned_scope")
    verdicts = payload.get("verdicts")
    if not isinstance(owned, list) or not owned:
        errors.append(f"{label}: review lacks owned_scope")
        return
    if not isinstance(verdicts, dict):
        errors.append(f"{label}: review lacks verdicts")
        return
    for scope, result in verdicts.items():
        if scope not in owned:
            errors.append(f"{label}: verdict outside owned scope: {scope}")
        if not isinstance(result, dict) or result.get("verdict") not in VALID_VERDICTS:
            errors.append(f"{label}: invalid verdict for {scope}")


def validate_events(payload: object, label: str, errors: list[str]) -> None:
    if not isinstance(payload, list):
        errors.append(f"{label}: ledger events must be a list")
        return
    for index, event in enumerate(payload):
        if not isinstance(event, dict):
            errors.append(f"{label}: event {index} must be an object")
            continue
        action = event.get("action")
        role = event.get("actor_role")
        if role == "implementer" and action in OWNER_ONLY_ACTIONS | HUMAN_ONLY_ACTIONS:
            errors.append(f"{label}: implementer may not perform {action}")
        if role not in {"human_authority", "incident_commander"} and action in HUMAN_ONLY_ACTIONS:
            errors.append(f"{label}: {action} requires authenticated human authority")


def validate_artifact(path: Path, errors: list[str]) -> None:
    payload = load_json(path, errors)
    if not isinstance(payload, dict):
        return
    if payload.get("schema_version") != 1:
        errors.append(f"{path}: schema_version must be 1")
    if "record_type" in payload:
        validate_finding(payload, str(path), errors)
    if "owned_scope" in payload or "verdicts" in payload:
        validate_review(payload, str(path), errors)
    if isinstance(payload.get("findings"), list):
        for index, finding in enumerate(payload["findings"]):
            if isinstance(finding, dict):
                validate_finding(finding, f"{path} finding {index}", errors)
    if isinstance(payload.get("events"), list):
        validate_events(payload["events"], str(path), errors)


def validate_contracts(errors: list[str]) -> None:
    require_files(errors)
    for path in (SKILL / "schemas").glob("*.json"):
        load_json(path, errors)
    policy = load_json(SKILL / "config/review-policy.example.json", errors)
    registry = load_json(SKILL / "config/evidence-requirements.example.json", errors)
    if isinstance(policy, dict):
        retention = policy.get("retention") or {}
        if "external_routine_evidence_days" not in retention or "external_high_risk_evidence_days" not in retention:
            errors.append("review policy must set explicit external evidence retention")
        if isinstance(registry, dict):
            known = set((registry.get("requirements") or {}).keys())
            for class_name, class_policy in (policy.get("change_classes") or {}).items():
                for requirement in (class_policy.get("requirements") or []) + (class_policy.get("deferred_requirements") or []):
                    requirement_id = requirement if isinstance(requirement, str) else requirement.get("id")
                    if requirement_id not in known:
                        errors.append(f"review policy {class_name} references unknown requirement: {requirement_id}")
    scenarios_path = ROOT / "evals/code-review/scenarios.json"
    scenarios = load_json(scenarios_path, errors)
    if isinstance(scenarios, dict):
        items = scenarios.get("scenarios")
        if not isinstance(items, list) or len(items) < 10:
            errors.append("code-review eval suite must contain at least 10 scenarios")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="optional review JSON artifacts to validate")
    parser.add_argument("--contracts-only", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    validate_contracts(errors)
    if not args.contracts_only:
        for path in args.paths:
            validate_artifact(path, errors)

    if errors:
        print("Code review artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Code review contracts and artifacts passed structural validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
