#!/usr/bin/env python3
"""Aggregate scoped review artifacts without inventing a scalar approval."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

VALID_VERDICTS = {"APPROVE", "APPROVE_WITH_COMMENTS", "CHANGES_REQUESTED", "CANNOT_ASSESS"}
BLOCKING_FINDING_STATES = {"OPEN", "ADDRESSED", "DISPUTED", "STILL_OPEN", "REGRESSED"}


class AggregateError(RuntimeError):
    pass


def load(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AggregateError(f"cannot read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AggregateError(f"artifact must be a JSON object: {path}")
    return payload


def collect(paths: list[Path]) -> list[dict]:
    return [load(path) for path in paths]


def validate_review(review: dict, expected_snapshot: str, errors: list[str]) -> None:
    if review.get("snapshot_id") != expected_snapshot:
        errors.append(f"review {review.get('review_id')} targets a different snapshot")
    owned = review.get("owned_scope")
    verdicts = review.get("verdicts")
    if not isinstance(owned, list) or not owned:
        errors.append(f"review {review.get('review_id')} has no owned scope")
        return
    if not isinstance(verdicts, dict):
        errors.append(f"review {review.get('review_id')} has invalid verdicts")
        return
    for scope, result in verdicts.items():
        if scope not in owned:
            errors.append(f"review {review.get('review_id')} issued verdict outside owned scope: {scope}")
        verdict = result.get("verdict") if isinstance(result, dict) else None
        if verdict not in VALID_VERDICTS:
            errors.append(f"review {review.get('review_id')} has invalid verdict for {scope}: {verdict}")


def coverage(required: list[str], results: dict[str, dict]) -> dict:
    received = sorted(scope for scope in required if scope in results)
    missing = sorted(set(required) - set(received))
    cannot_assess = sorted(scope for scope in received if results[scope]["verdict"] == "CANNOT_ASSESS")
    return {
        "required": sorted(required),
        "received": received,
        "missing": missing,
        "cannot_assess": cannot_assess,
        "status": "COMPLETE" if not missing else "INCOMPLETE",
    }


def aggregate(
    coordination: dict,
    dimension_reviews: list[dict],
    seam_reviews: list[dict],
    ledger: dict,
    evidence: dict,
) -> dict:
    snapshot_id = coordination.get("snapshot_id")
    if not snapshot_id:
        raise AggregateError("coordination is missing snapshot_id")

    errors: list[str] = []
    dimension_results: dict[str, dict] = {}
    seam_results: dict[str, dict] = {}

    for review in dimension_reviews:
        validate_review(review, snapshot_id, errors)
        for scope, result in (review.get("verdicts") or {}).items():
            if scope in dimension_results:
                errors.append(f"multiple binding dimension verdicts: {scope}")
            else:
                dimension_results[scope] = {
                    "verdict": result.get("verdict"),
                    "confidence": result.get("confidence"),
                    "review_id": review.get("review_id"),
                }

    for review in seam_reviews:
        validate_review(review, snapshot_id, errors)
        for scope, result in (review.get("verdicts") or {}).items():
            if scope in seam_results:
                errors.append(f"multiple binding seam verdicts: {scope}")
            else:
                seam_results[scope] = {
                    "verdict": result.get("verdict"),
                    "confidence": result.get("confidence"),
                    "review_id": review.get("review_id"),
                }

    dimensions_cfg = coordination.get("dimensions") or {}
    seams_cfg = coordination.get("seams") or {}
    required_dimensions = dimensions_cfg.get("required") or []
    required_seams_raw = seams_cfg.get("required") or []
    required_seams = [item.get("seam_id") if isinstance(item, dict) else item for item in required_seams_raw]
    required_seams = [item for item in required_seams if item]

    dimension_coverage = coverage(required_dimensions, dimension_results)
    seam_coverage = coverage(required_seams, seam_results)

    findings = ledger.get("findings") or []
    findings_by_state: dict[str, list[str]] = defaultdict(list)
    blocking_work: dict[str, list[dict]] = defaultdict(list)
    for finding in findings:
        status = finding.get("status", "OPEN")
        record_id = finding.get("record_id", "UNKNOWN")
        findings_by_state[status].append(record_id)
        if finding.get("authority") == "BLOCKING" and status in BLOCKING_FINDING_STATES:
            owner = finding.get("resolution_owner") or "unassigned"
            blocking_work[owner].append(
                {
                    "type": "binding_finding",
                    "reference": record_id,
                    "action": "satisfy_acceptance_criterion" if status != "DISPUTED" else "adjudicate_dispute",
                }
            )

    open_escalations = (coordination.get("escalations") or {}).get("open") or []
    requirement_set = coordination.get("requirement_set") or {}
    stabilized = bool(requirement_set.get("stabilized", not open_escalations)) and not open_escalations

    stale_evidence = evidence.get("stale") or []
    contradictory_evidence = evidence.get("contradictory") or []

    if errors:
        status = "CONTRADICTORY" if any("multiple binding" in item or "different snapshot" in item for item in errors) else "INVALID"
    elif stale_evidence:
        status = "STALE"
    elif dimension_coverage["missing"] or seam_coverage["missing"] or not stabilized:
        status = "INCOMPLETE"
    elif contradictory_evidence:
        status = "CONTRADICTORY"
    else:
        status = "COMPLETE"

    for dimension in dimension_coverage["missing"]:
        blocking_work["review_coordinator"].append(
            {"type": "missing_dimension_review", "reference": dimension, "action": "assign_and_complete_review"}
        )
    for seam in seam_coverage["missing"]:
        blocking_work["review_coordinator"].append(
            {"type": "missing_seam_review", "reference": seam, "action": "assign_and_complete_seam_review"}
        )
    for escalation in open_escalations:
        reference = escalation.get("record_id") if isinstance(escalation, dict) else str(escalation)
        blocking_work["review_coordinator"].append(
            {"type": "open_escalation", "reference": reference, "action": "resolve_escalation"}
        )
    for gap in evidence.get("unsatisfied") or []:
        owner = gap.get("owner", "implementer") if isinstance(gap, dict) else "implementer"
        reference = gap.get("requirement_id", "unknown") if isinstance(gap, dict) else str(gap)
        blocking_work[owner].append(
            {"type": "evidence_requirement", "reference": reference, "action": "satisfy_requirement"}
        )

    return {
        "schema_version": 1,
        "snapshot_id": snapshot_id,
        "status": status,
        "errors": errors,
        "requirement_set": {
            "stabilized": stabilized,
            "escalation_rounds_used": requirement_set.get("escalation_rounds_used", 0),
        },
        "dimension_coverage": dimension_coverage,
        "seam_coverage": seam_coverage,
        "dimension_results": dimension_results,
        "seam_results": seam_results,
        "binding_findings": {key: sorted(value) for key, value in sorted(findings_by_state.items())},
        "evidence": {
            "sufficiency": evidence.get("sufficiency", "INSUFFICIENT"),
            "satisfied": evidence.get("satisfied") or [],
            "partially_satisfied": evidence.get("partially_satisfied") or [],
            "unsatisfied": evidence.get("unsatisfied") or [],
            "stale": stale_evidence,
            "contradictory": contradictory_evidence,
        },
        "escalations": {"open": open_escalations, "resolved": (coordination.get("escalations") or {}).get("resolved") or []},
        "blocking_work": {owner: items for owner, items in sorted(blocking_work.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coordination", type=Path, required=True)
    parser.add_argument("--dimension-review", type=Path, action="append", default=[])
    parser.add_argument("--seam-review", type=Path, action="append", default=[])
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        result = aggregate(
            load(args.coordination),
            collect(args.dimension_review),
            collect(args.seam_review),
            load(args.ledger),
            load(args.evidence),
        )
    except AggregateError as exc:
        print(f"aggregation error: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Aggregate review status: {result['status']}")
    return 0 if result["status"] not in {"INVALID", "CONTRADICTORY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
