#!/usr/bin/env python3
"""Dependency-free integration tests for the Feature Execution Planner package."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = ROOT / ".agents/skills/feature-execution-planner/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from planning_common import dump_json, load_json, set_integrity  # noqa: E402
from validate_planning_artifacts import validate_workspace  # noqa: E402


def write_record(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_json(set_integrity(value)), encoding="utf-8")


def codes(errors: list[dict]) -> set[str]:
    return {str(item.get("code")) for item in errors}


def assert_code(work: Path, expected: str) -> None:
    found = codes(validate_workspace(work))
    if expected not in found:
        raise AssertionError(f"expected {expected}; found {sorted(found)}")


def run(*args: str) -> None:
    completed = subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise AssertionError(f"command failed: {' '.join(args)}\n{completed.stdout}\n{completed.stderr}")


def valid_workspace(root: Path) -> Path:
    work = root / "APP-104-order-events"
    run(str(SKILL_SCRIPTS / "init_planning_workspace.py"), "--work", str(work), "--feature-id", "APP-104", "--feature-name", "Order Events")
    intent = load_json(work / "intent-manifest.json")
    intent.update({"status": "approved", "acceptance_criteria": [{"ref": "AC-001@1", "status": "active", "title": "Accepted orders remain durable during publication failure"}]})
    (work / "intent-manifest.json").write_text(dump_json(set_integrity(intent)), encoding="utf-8")
    decision = {"schema_version": 1, "id": "DEC-001", "revision": 1, "title": "Select order publication boundary", "domain": "architecture", "lifecycle_action": "create", "supersedes": None, "trigger_ids": ["service_boundary_crossing"], "depends_on": [], "reversal": {"class": "coordinated", "reasons": ["Undo requires consumer coordination"]}, "options": [{"id": "outbox", "summary": "Use an outbox", "forecloses": ["Synchronous-only publication"], "reversal_requirements": ["Consumer migration"]}, {"id": "direct", "summary": "Publish directly", "forecloses": ["Independent recovery"], "reversal_requirements": ["Request-path redesign"]}], "recommendation": {"option": "outbox", "rationale": "The outbox preserves accepted orders when publication is unavailable."}, "approval_requirements": {"primary_role": "architecture", "additional_roles": []}, "deadline": "2026-08-01", "default_on_deadline": "do_not_proceed", "provides": [], "requires": []}
    write_record(work / "decisions/architecture/DEC-001-order-publication/revisions/1.json", decision)
    obligation = {"schema_version": 1, "id": "TASK-001", "title": "Accepted orders remain durable during publication failure", "intent_basis": ["AC-001@1"], "lifecycle": "active", "current_execution": "TASK-001/1", "accountability": {"owner": "order-platform"}}
    write_record(work / "tasks/TASK-001-durable-order/obligation.json", obligation)
    execution = {"schema_version": 1, "id": "TASK-001/1", "obligation": "TASK-001", "attempt": 1, "kind": "initial_execution", "status": "planned", "replaces": None, "corrects": None, "decision_basis": ["DEC-001@1"], "local_choices": [], "implementation": {"summary": "Persist the order and outbox entry atomically.", "allowed_modules": ["services/orders"], "prohibited_modules": ["services/notifications"]}, "dependencies": [], "assignee": {"owner": "order-platform", "inherited_from": None}, "evidence_requirements": [{"predicate": "test.targeted"}, {"predicate": "test.integration"}], "evidence_carries": [], "milestone": "MILESTONE-001/1"}
    write_record(work / "tasks/TASK-001-durable-order/executions/1.json", execution)
    milestone = {"schema_version": 1, "id": "MILESTONE-001", "revision": 1, "class": "behavioral", "claims": {"acceptance_criteria": ["AC-001@1"], "maintenance_objectives": []}, "supports": {"acceptance_criteria": []}, "enables": [], "executions": ["TASK-001/1"], "dependencies": [], "provides": [], "joint_evidence": [{"predicate": "test.integration", "scenarios": ["accepted_order_survives_publication_failure"], "member_evidence_carry_permitted": False}], "observability": {"mode": "production_observable", "success_signals": ["orders.accepted"], "failure_signals": ["accepted_order_without_event"], "monitoring_owner": "order-platform", "incident_owner": "commerce-on-call"}, "rollback": {"class": "coordinated", "owner": "commerce-on-call", "procedure": ["Disable publication and preserve pending orders"], "data_disposition": "preserve_and_reconcile"}, "downstream_failure_disposition": None, "corrects": None, "release_owner": "commerce-release-owner"}
    write_record(work / "milestones/MILESTONE-001-order-publication/revisions/1.json", milestone)
    run(str(SKILL_SCRIPTS / "build_plan_manifest.py"), "--work", str(work), "--revision", "1", "--risk", "high", "--size", "M")
    errors = validate_workspace(work)
    if errors:
        raise AssertionError("valid workspace failed:\n" + json.dumps(errors, indent=2))
    return work


def clone(source: Path, root: Path, name: str) -> Path:
    destination = root / name
    shutil.copytree(source, destination)
    return destination


def mutate_json(path: Path, mutate) -> None:
    value = load_json(path)
    mutate(value)
    path.write_text(dump_json(set_integrity(value)), encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="feature-planner-") as temporary:
        root = Path(temporary)
        valid = valid_workspace(root)
        stale = clone(valid, root, "stale-view")
        (stale / "plan.md").write_text("hand edited\n", encoding="utf-8")
        assert_code(stale, "GENERATED_VIEW_STALE")
        double_claim = clone(valid, root, "double-claim")
        original = load_json(double_claim / "milestones/MILESTONE-001-order-publication/revisions/1.json")
        second = copy.deepcopy(original)
        second["id"] = "MILESTONE-002"
        second["executions"] = ["TASK-001/1"]
        write_record(double_claim / "milestones/MILESTONE-002-duplicate/revisions/1.json", second)
        assert_code(double_claim, "AC_MILESTONE_CLAIM_COUNT")
        enabling = clone(valid, root, "enabling-claims-ac")
        milestone_path = enabling / "milestones/MILESTONE-001-order-publication/revisions/1.json"
        mutate_json(milestone_path, lambda value: value.update({"class": "enabling", "enables": ["MILESTONE-002"], "downstream_failure_disposition": {"default": "retain_for_retry", "owner": "order-platform", "deadline": "2026-08-15"}}))
        assert_code(enabling, "NONBEHAVIORAL_MILESTONE_CLAIMS_AC")
        floating = clone(valid, root, "floating-execution")
        milestone_path = floating / "milestones/MILESTONE-001-order-publication/revisions/1.json"
        mutate_json(milestone_path, lambda value: value.update({"executions": []}))
        assert_code(floating, "EXECUTION_MILESTONE_MEMBERSHIP_COUNT")
        generic_carry = clone(valid, root, "generic-carry")
        execution_path = generic_carry / "tasks/TASK-001-durable-order/executions/1.json"
        def add_carry(value):
            value["evidence_carries"] = [{"requirement": "test.targeted", "source_execution": "TASK-001/0", "source_evidence_id": "EV-1", "affected_decision": "DEC-001@1", "rationale": "The code barely changed and should still be valid.", "approval_required_from": ["plan_reviewer"]}]
        mutate_json(execution_path, add_carry)
        assert_code(generic_carry, "EVIDENCE_CARRY_RATIONALE_INADEQUATE")
        low_reversal = clone(valid, root, "low-reversal")
        decision_path = low_reversal / "decisions/architecture/DEC-001-order-publication/revisions/1.json"
        mutate_json(decision_path, lambda value: value["reversal"].update({"class": "local"}))
        assert_code(low_reversal, "REVERSAL_CLASS_TOO_LOW")
        cycle = clone(valid, root, "execution-cycle")
        execution_path = cycle / "tasks/TASK-001-durable-order/executions/1.json"
        mutate_json(execution_path, lambda value: value.update({"dependencies": [{"execution": "TASK-001/1", "consumes": []}]}))
        assert_code(cycle, "EXECUTION_GRAPH_CYCLE")
        bad_rollback = clone(valid, root, "bad-rollback")
        milestone_path = bad_rollback / "milestones/MILESTONE-001-order-publication/revisions/1.json"
        mutate_json(milestone_path, lambda value: value["rollback"].update({"procedure": []}))
        assert_code(bad_rollback, "ROLLBACK_CONTRACT_INCOMPLETE")
        estimate = clone(valid, root, "calendar-estimate")
        plan_path = estimate / "plans/PLAN-001/revisions/1.json"
        mutate_json(plan_path, lambda value: value["classification"].update({"size_unknowns": ["This should take three weeks"]}))
        assert_code(estimate, "CALENDAR_ESTIMATE_PROHIBITED")
        wildcard = clone(valid, root, "wildcard-auth")
        plan = load_json(wildcard / "plans/PLAN-001/revisions/1.json")
        authorization = {"schema_version": 1, "id": "AUTH-IMP-001", "type": "grant", "feature_id": "APP-104", "basis": {"plan_revision": "PLAN-001/1", "plan_manifest_hash": plan["integrity"]["content_hash"], "repository_base_commit": "UNKNOWN"}, "scope": {"milestones": ["all_current"], "executions": ["all_current"]}, "authority": {"required_role": "engineering_owner"}, "validity": {"not_before": "2026-08-01", "expires_at": "2026-09-01"}, "branch": {"required_prefix": "agent/APP-104-implementation"}}
        write_record(wildcard / "authorizations/implementation/AUTH-IMP-001.json", authorization)
        assert_code(wildcard, "AUTHORIZATION_WILDCARD_PROHIBITED")
        irreversible = clone(valid, root, "irreversible")
        milestone_path = irreversible / "milestones/MILESTONE-001-order-publication/revisions/1.json"
        mutate_json(milestone_path, lambda value: value["rollback"].update({"class": "irreversible"}))
        assert_code(irreversible, "IRREVERSIBLE_ROLLBACK_DECISION_MISSING")
    print("Feature Execution Planner integration tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
