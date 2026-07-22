#!/usr/bin/env python3
"""Deterministically evaluate whether an exact reviewed snapshot may merge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

BLOCKING_FINDING_STATES = {"OPEN", "ADDRESSED", "DISPUTED", "STILL_OPEN", "REGRESSED"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def blocker(kind: str, owner: str, action: str, reference: str | None = None, authority: str | None = None) -> dict:
    item = {"type": kind, "owner": owner, "required_action": action}
    if reference:
        item["reference"] = reference
    if authority:
        item["authority_basis"] = authority
    return item


def evaluate(aggregate: dict, state: dict) -> dict:
    blockers: list[dict] = []
    snapshot_id = aggregate.get("snapshot_id")

    if state.get("snapshot_id") != snapshot_id:
        blockers.append(blocker("REVIEW_STALE", "implementer", "capture_and_review_current_snapshot"))
    if aggregate.get("status") != "COMPLETE":
        blockers.append(blocker("AGGREGATION_INCOMPLETE", "review_coordinator", "complete_or_repair_aggregation", aggregate.get("status")))
    if not (aggregate.get("requirement_set") or {}).get("stabilized", False):
        blockers.append(blocker("REQUIREMENTS_NOT_STABILIZED", "review_coordinator", "resolve_escalations"))

    for dimension in (aggregate.get("dimension_coverage") or {}).get("missing", []):
        blockers.append(blocker("MISSING_DIMENSION_REVIEW", "review_coordinator", "assign_and_complete_review", dimension))
    for seam in (aggregate.get("seam_coverage") or {}).get("missing", []):
        blockers.append(blocker("MISSING_SEAM_REVIEW", "review_coordinator", "assign_and_complete_seam_review", seam))

    for scope, result in (aggregate.get("dimension_results") or {}).items():
        verdict = result.get("verdict")
        if verdict == "CHANGES_REQUESTED":
            blockers.append(blocker("REVIEW_CHANGES_REQUESTED", "implementer", "resolve_binding_findings", scope))
        elif verdict == "CANNOT_ASSESS":
            blockers.append(blocker("REVIEW_CANNOT_ASSESS", "review_coordinator", "supply_evidence_or_reassign", scope))
    for seam, result in (aggregate.get("seam_results") or {}).items():
        verdict = result.get("verdict")
        if verdict == "CHANGES_REQUESTED":
            blockers.append(blocker("REVIEW_CHANGES_REQUESTED", "implementer", "resolve_seam_findings", seam))
        elif verdict == "CANNOT_ASSESS":
            blockers.append(blocker("REVIEW_CANNOT_ASSESS", "review_coordinator", "supply_evidence_or_reassign", seam))

    findings = aggregate.get("binding_findings") or {}
    for status in BLOCKING_FINDING_STATES:
        for finding_id in findings.get(status, []):
            kind = {
                "ADDRESSED": "ADDRESSED_FINDING_UNVERIFIED",
                "DISPUTED": "UNRESOLVED_DISPUTE",
                "REGRESSED": "REGRESSED_FINDING",
            }.get(status, "OPEN_BINDING_FINDING")
            owner = "reviewer" if status in {"ADDRESSED", "DISPUTED"} else "implementer"
            action = "adjudicate_finding" if owner == "reviewer" else "resolve_binding_finding"
            blockers.append(blocker(kind, owner, action, finding_id))

    evidence = aggregate.get("evidence") or {}
    if evidence.get("sufficiency") != "SUFFICIENT":
        blockers.append(blocker("UNSATISFIED_EVIDENCE", "implementer", "satisfy_effective_evidence_requirements", evidence.get("sufficiency")))
    if evidence.get("contradictory"):
        blockers.append(blocker("CONTRADICTORY_EVIDENCE", "review_coordinator", "reconcile_evidence"))
    if evidence.get("stale"):
        blockers.append(blocker("EVIDENCE_STALE", "implementer", "rerun_evidence_for_current_snapshot"))

    if not state.get("base_fresh", False):
        blockers.append(blocker("BASE_BRANCH_OUTDATED", "implementer", "update_branch_and_rerun_review"))
    if state.get("merge_conflict", False):
        blockers.append(blocker("MERGE_CONFLICT", "implementer", "resolve_merge_conflict"))
    if not state.get("branch_protection_satisfied", False):
        blockers.append(blocker("BRANCH_PROTECTION_UNSATISFIED", "implementer", "satisfy_branch_protection"))
    if not state.get("dependencies_ready", True):
        blockers.append(blocker("DEPENDENCY_NOT_READY", "release_owner", "satisfy_dependency_sequence"))

    ci = state.get("ci") or {}
    if ci.get("required", False):
        if ci.get("status") == "MISSING":
            blockers.append(blocker("REQUIRED_CI_MISSING", "implementer", "run_required_ci"))
        elif ci.get("status") != "PASSED":
            blockers.append(blocker("REQUIRED_CI_FAILED", "implementer", "fix_or_rerun_ci"))
        if ci.get("snapshot_id") and ci.get("snapshot_id") != snapshot_id:
            blockers.append(blocker("EVIDENCE_STALE", "implementer", "run_ci_for_current_snapshot", "ci"))

    approvals = state.get("approvals") or {}
    required_approvals = set(approvals.get("required") or [])
    present_approvals = set(approvals.get("present") or [])
    for missing in sorted(required_approvals - present_approvals):
        blockers.append(blocker("REQUIRED_APPROVAL_MISSING", "human_authority", "obtain_required_approval", missing))

    exception = state.get("exception") or {}
    decision_basis = "NORMAL_POLICY"
    if blockers and exception.get("valid", False):
        bypasses = set(exception.get("bypasses") or [])
        unbypassed = [item for item in blockers if item["type"] not in bypasses]
        if not unbypassed:
            blockers = []
            decision_basis = exception.get("decision_basis", "APPROVED_EXCEPTION")

    return {
        "schema_version": 1,
        "snapshot_id": snapshot_id,
        "decision": "ALLOW" if not blockers else "BLOCK",
        "decision_basis": decision_basis,
        "blockers": blockers,
        "post_merge_obligations": exception.get("post_merge_obligations") or [],
        "input_hashes": state.get("input_hashes") or {},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aggregate", type=Path, required=True)
    parser.add_argument("--repository-state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = evaluate(load(args.aggregate), load(args.repository_state))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Merge gate decision: {result['decision']}")
    return 0 if result["decision"] == "ALLOW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
