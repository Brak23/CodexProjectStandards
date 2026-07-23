#!/usr/bin/env python3
"""Validate planner package contracts, workspaces, gates, graphs, and authorization records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from planning_common import (
    AC_REF,
    DEC_REF,
    EXEC_REF,
    MILESTONE_REF,
    MO_REF,
    PLAN_REF,
    ROOT,
    SKILL,
    PlanningError,
    changed_paths,
    check_integrity,
    content_hash,
    detect_cycle,
    error,
    feature_workspaces,
    file_hash,
    find_json,
    load_json,
    load_records,
    newest_by_id,
    record_ref,
    relative,
    required_role_names,
    workspace_paths,
)
from render_planning_views import build_outputs

RISK = {"low", "moderate", "high", "critical"}
SIZE = {"XS", "S", "M", "L", "XL"}
EXEC_TERMINAL = {"done", "superseded_before_start", "abandoned_in_flight", "stale_before_release", "cancelled_by_intent", "failed"}
EXEC_ACTIVE = {"planned", "in_progress", "implemented", "merged"}
REVERSAL = {"local", "bounded", "coordinated", "irreversible"}
MILESTONE_CLASS = {"behavioral", "enabling", "maintenance"}
OBS_MODES = {"production_observable", "operationally_observable", "repository_verifiable"}
GENERIC_CARRY = re.compile(r"\b(barely changed|should still|probably unaffected|same code|mostly unchanged)\b", re.I)
CALENDAR_ESTIMATE = re.compile(r"\b(?:(?:\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten)\s*(?:hours?|days?|weeks?|months?|person-days?|story points?)|by (?:monday|tuesday|wednesday|thursday|friday|saturday|sunday))\b", re.I)


def package_required() -> list[str]:
    return [
        "SKILL.md",
        "README.md",
        "references/planning-contract.md",
        "references/authority-and-gates.md",
        "references/reversal-classification.md",
        "references/evidence-design.md",
        "references/obligation-execution-model.md",
        "references/milestone-composition.md",
        "references/promotion-semantics.md",
        "references/amendment-propagation.md",
        "config/decision-triggers.json",
        "config/reversal-classes.json",
        "config/size-classes.json",
        "config/approval-roles.example.json",
        "config/milestone-classes.json",
        "config/planning-policy.example.json",
        "scripts/planning_common.py",
        "scripts/render_planning_views.py",
        "scripts/validate_planning_artifacts.py",
        "scripts/init_planning_workspace.py",
        "scripts/assess_plan_impact.py",
        "scripts/collect_planning_context.py",
        "scripts/build_plan_manifest.py",
        "scripts/classify_planning_pr.py",
        "scripts/validate_planning_authority.py",
        "scripts/migrate_legacy_workspace.py",
    ]


def validate_contracts(errors: list[dict[str, Any]]) -> None:
    for relative_path in package_required():
        path = SKILL / relative_path
        if not path.exists():
            errors.append(error("PACKAGE_FILE_MISSING", relative_path, "required planner package file is missing"))
    for path in sorted((SKILL / "config").glob("*.json")) + sorted((SKILL / "schemas").glob("*.json")) + sorted((SKILL / "templates").glob("*.json")):
        try:
            load_json(path)
        except PlanningError as exc:
            errors.append(error("PACKAGE_JSON_INVALID", relative(path), str(exc)))
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8") if (SKILL / "SKILL.md").exists() else ""
    for token in (
        "name: feature-execution-planner",
        "Convert approved product intent",
        "implementation authorization",
        "Every current execution belongs to exactly one milestone",
        "INTENT_AMENDMENT_REQUIRED",
    ):
        if token not in skill:
            errors.append(error("SKILL_CONTRACT_MISSING", "SKILL.md", f"missing required phrase: {token}"))
    try:
        triggers = load_json(SKILL / "config/decision-triggers.json")
        reversal = load_json(SKILL / "config/reversal-classes.json")
        trigger_ids = [item.get("id") for item in triggers.get("triggers", [])]
        if len(trigger_ids) != len(set(trigger_ids)) or not trigger_ids:
            errors.append(error("DECISION_TRIGGER_REGISTRY_INVALID", "decision-triggers.json", "trigger IDs must be unique and non-empty"))
        ranks = [item.get("rank") for item in reversal.get("classes", [])]
        if ranks != sorted(ranks) or {item.get("id") for item in reversal.get("classes", [])} != REVERSAL:
            errors.append(error("REVERSAL_REGISTRY_INVALID", "reversal-classes.json", "reversal classes or rank order are invalid"))
    except PlanningError as exc:
        errors.append(error("PACKAGE_CONFIG_INVALID", "config", str(exc)))


def validate_intent(intent: dict[str, Any], source: str, errors: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
    active_ac: set[str] = set()
    active_mo: set[str] = set()
    if intent.get("schema_version") != 1:
        errors.append(error("INTENT_SCHEMA_VERSION", source, "schema_version must be 1"))
    for item in intent.get("acceptance_criteria", []):
        if not isinstance(item, dict):
            errors.append(error("AC_RECORD_INVALID", source, "acceptance criteria must be objects"))
            continue
        ref = item.get("ref")
        status = item.get("status")
        if not isinstance(ref, str) or not AC_REF.fullmatch(ref):
            errors.append(error("AC_REFERENCE_INVALID", source, f"invalid acceptance criterion reference: {ref}"))
        elif status == "active":
            if ref in active_ac:
                errors.append(error("AC_DUPLICATE_ACTIVE", ref, "acceptance criterion appears more than once"))
            active_ac.add(ref)
        elif status not in {"retired", "superseded"}:
            errors.append(error("AC_STATUS_INVALID", str(ref), f"unsupported acceptance criterion status: {status}"))
    for item in intent.get("maintenance_objectives", []):
        if not isinstance(item, dict):
            errors.append(error("MO_RECORD_INVALID", source, "maintenance objectives must be objects"))
            continue
        ref = item.get("ref")
        status = item.get("status")
        if not isinstance(ref, str) or not MO_REF.fullmatch(ref):
            errors.append(error("MO_REFERENCE_INVALID", source, f"invalid maintenance objective reference: {ref}"))
        elif status == "active":
            active_mo.add(ref)
    check_integrity(intent, source, errors, allow_pending=intent.get("status") == "draft")
    return active_ac, active_mo


def validate_decisions(work: Path, active_ac: set[str], role_names: set[str], errors: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    paths = workspace_paths(work)
    records = load_records(find_json(paths["decisions"], "**/revisions/*.json"), errors)
    all_refs: dict[str, dict[str, Any]] = {}
    active = newest_by_id(records)
    edges: dict[str, set[str]] = defaultdict(set)
    trigger_registry = {item.get("id"): item for item in load_json(SKILL / "config/decision-triggers.json").get("triggers", [])}
    reversal_rank = {item.get("id"): int(item.get("rank", 0)) for item in load_json(SKILL / "config/reversal-classes.json").get("classes", [])}
    for path, record in records:
        source = relative(path)
        ref = record_ref(record)
        if not DEC_REF.fullmatch(ref):
            errors.append(error("DECISION_REFERENCE_INVALID", source, f"invalid decision identity: {ref}"))
        if ref in all_refs:
            errors.append(error("DECISION_REVISION_DUPLICATE", ref, "decision revision is duplicated"))
        all_refs[ref] = record
        check_integrity(record, source, errors, allow_pending=False)
        parts = set(path.parts)
        domain = record.get("domain")
        if domain not in parts:
            errors.append(error("DECISION_OWNER_PATH_MISMATCH", ref, f"decision domain {domain} must match a path segment"))
        options = record.get("options", [])
        if not isinstance(options, list) or not 2 <= len(options) <= 3:
            errors.append(error("DECISION_OPTION_COUNT", ref, "decision must contain two or three options"))
        option_ids = {item.get("id") for item in options if isinstance(item, dict)}
        recommendation = record.get("recommendation", {}).get("option")
        if recommendation not in option_ids:
            errors.append(error("DECISION_RECOMMENDATION_INVALID", ref, "recommended option does not exist"))
        for option in options:
            if not isinstance(option, dict) or not option.get("forecloses") or not option.get("reversal_requirements"):
                errors.append(error("DECISION_OPTION_INCOMPLETE", ref, "every option needs foreclosures and reversal requirements"))
        approval = record.get("approval_requirements", {})
        primary = approval.get("primary_role")
        additional = approval.get("additional_roles", [])
        for role in [primary, *additional]:
            if role not in role_names:
                errors.append(error("APPROVAL_ROLE_UNKNOWN", ref, f"unknown approval role: {role}"))
        triggers = record.get("trigger_ids", [])
        minimum_rank = 0
        for trigger_id in triggers:
            trigger = trigger_registry.get(trigger_id)
            if not trigger:
                errors.append(error("DECISION_TRIGGER_UNKNOWN", ref, f"unknown decision trigger: {trigger_id}"))
                continue
            minimum_rank = max(minimum_rank, reversal_rank.get(trigger.get("minimum_reversal_class"), 0))
            required_roles = set(trigger.get("required_roles", []))
            declared_roles = {primary, *additional}
            missing_roles = sorted(required_roles - declared_roles)
            if missing_roles:
                errors.append(error("DECISION_TRIGGER_APPROVER_MISSING", ref, "trigger-required roles are missing", roles=missing_roles))
        actual_reversal = record.get("reversal", {}).get("class")
        if actual_reversal not in REVERSAL:
            errors.append(error("REVERSAL_CLASS_INVALID", ref, f"unsupported reversal class: {actual_reversal}"))
        elif reversal_rank.get(actual_reversal, 0) < minimum_rank:
            errors.append(error("REVERSAL_CLASS_TOO_LOW", ref, "decision is classified below the trigger minimum"))
        if record.get("default_on_deadline") != "do_not_proceed" and actual_reversal in {"coordinated", "irreversible"}:
            errors.append(error("PROTECTED_DECISION_DEFAULT_UNSAFE", ref, "coordinated or irreversible decisions must default to do_not_proceed"))
        for dependency in record.get("depends_on", []):
            target = dependency.get("decision") if isinstance(dependency, dict) else None
            if target:
                edges[ref].add(target)
    for source, targets in edges.items():
        for target in targets:
            if target not in all_refs:
                errors.append(error("DECISION_DEPENDENCY_MISSING", source, f"dependency does not exist: {target}"))
    cycle = detect_cycle(all_refs, edges)
    if cycle:
        errors.append(error("DECISION_GRAPH_CYCLE", "decision-graph", " -> ".join(cycle)))
    for ref, record in all_refs.items():
        supersedes = record.get("supersedes")
        revision = record.get("revision")
        if revision == 1 and supersedes:
            errors.append(error("DECISION_INITIAL_REVISION_SUPERSEDES", ref, "revision 1 cannot supersede another revision"))
        if isinstance(revision, int) and revision > 1:
            expected_previous = f"{record.get('id')}@{revision - 1}"
            if supersedes != expected_previous or supersedes not in all_refs:
                errors.append(error("DECISION_SUPERSESSION_INVALID", ref, f"revision must supersede {expected_previous}"))
    active_refs = {record_ref(record): record for _, record in active.values()}
    for ref, record in active_refs.items():
        for dependency in record.get("depends_on", []):
            target = dependency.get("decision")
            base = target.split("@", 1)[0] if isinstance(target, str) else None
            newest = active.get(base) if base else None
            if newest and record_ref(newest[1]) != target:
                errors.append(error("ACTIVE_DECISION_DEPENDS_ON_SUPERSEDED", ref, f"active decision depends on superseded revision {target}"))
    return active_refs, edges


def validate_tasks(work: Path, active_ac: set[str], active_decisions: dict[str, dict[str, Any]], errors: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, set[str]]]:
    paths = workspace_paths(work)
    obligations_list = load_records(find_json(paths["tasks"], "**/obligation.json"), errors)
    executions_list = load_records(find_json(paths["tasks"], "**/executions/*.json"), errors)
    obligations: dict[str, dict[str, Any]] = {}
    executions: dict[str, dict[str, Any]] = {}
    coverage: dict[str, set[str]] = defaultdict(set)
    edges: dict[str, set[str]] = defaultdict(set)
    for path, record in obligations_list:
        source = relative(path)
        identity = record.get("id")
        if not isinstance(identity, str) or not re.fullmatch(r"TASK-[0-9]{3,}", identity):
            errors.append(error("OBLIGATION_ID_INVALID", source, f"invalid obligation ID: {identity}"))
            continue
        if identity in obligations:
            errors.append(error("OBLIGATION_DUPLICATE", identity, "obligation is duplicated"))
        obligations[identity] = record
        check_integrity(record, source, errors, allow_pending=False)
        for ac in record.get("intent_basis", []):
            if ac not in active_ac:
                errors.append(error("OBLIGATION_INTENT_INACTIVE", identity, f"obligation references inactive or unknown AC: {ac}"))
            coverage[ac].add(identity)
    for ac in active_ac:
        if not coverage.get(ac):
            errors.append(error("AC_UNCOVERED_BY_OBLIGATION", ac, "active AC has no obligation"))
    for path, record in executions_list:
        source = relative(path)
        identity = record.get("id")
        if not isinstance(identity, str) or not EXEC_REF.fullmatch(identity):
            errors.append(error("EXECUTION_ID_INVALID", source, f"invalid execution ID: {identity}"))
            continue
        if identity in executions:
            errors.append(error("EXECUTION_DUPLICATE", identity, "execution attempt is duplicated"))
        executions[identity] = record
        check_integrity(record, source, errors, allow_pending=False)
        obligation = record.get("obligation")
        if obligation not in obligations:
            errors.append(error("EXECUTION_OBLIGATION_MISSING", identity, f"obligation does not exist: {obligation}"))
        for decision in record.get("decision_basis", []):
            if decision not in active_decisions:
                errors.append(error("EXECUTION_DECISION_INACTIVE", identity, f"execution references inactive decision: {decision}"))
        for dependency in record.get("dependencies", []):
            target = dependency.get("execution") if isinstance(dependency, dict) else None
            if target:
                edges[identity].add(target)
        for carry in record.get("evidence_carries", []):
            rationale = str(carry.get("rationale", "")) if isinstance(carry, dict) else ""
            if len(rationale.strip()) < 30 or GENERIC_CARRY.search(rationale):
                errors.append(error("EVIDENCE_CARRY_RATIONALE_INADEQUATE", identity, "carry rationale must specifically argue non-impact against the named decision"))
            if not isinstance(carry, dict) or not carry.get("affected_decision") or not carry.get("source_execution") or not carry.get("source_evidence_id") or not carry.get("approval_required_from"):
                errors.append(error("EVIDENCE_CARRY_INCOMPLETE", identity, "evidence carry is missing required traceability or approval"))
    for source, targets in edges.items():
        for target in targets:
            if target not in executions:
                errors.append(error("EXECUTION_DEPENDENCY_MISSING", source, f"execution dependency does not exist: {target}"))
    cycle = detect_cycle(executions, edges)
    if cycle:
        errors.append(error("EXECUTION_GRAPH_CYCLE", "task-graph", " -> ".join(cycle)))
    current_counts: dict[str, int] = defaultdict(int)
    for obligation_id, obligation in obligations.items():
        current = obligation.get("current_execution")
        lifecycle = obligation.get("lifecycle")
        if lifecycle == "retired_by_intent":
            if current is not None:
                errors.append(error("RETIRED_OBLIGATION_HAS_CURRENT_EXECUTION", obligation_id, "retired obligation must not have a current execution"))
            continue
        if current not in executions:
            errors.append(error("CURRENT_EXECUTION_MISSING", obligation_id, f"current execution does not exist: {current}"))
            continue
        current_counts[obligation_id] += 1
        execution = executions[current]
        status = execution.get("status")
        if lifecycle == "active" and status not in EXEC_ACTIVE:
            errors.append(error("ACTIVE_OBLIGATION_CURRENT_EXECUTION_TERMINAL", obligation_id, f"active obligation points to terminal execution status {status}"))
        if lifecycle == "satisfied" and status != "done":
            errors.append(error("SATISFIED_OBLIGATION_NOT_DONE", obligation_id, "satisfied obligation must point to a done execution"))
    for execution_id, execution in executions.items():
        obligation_id = execution.get("obligation")
        if obligations.get(obligation_id, {}).get("current_execution") == execution_id:
            continue
        status = execution.get("status")
        if status not in EXEC_TERMINAL:
            errors.append(error("NONCURRENT_EXECUTION_NOT_TERMINAL", execution_id, "a displaced execution must have a terminal status"))
        if status in {"superseded_before_start", "abandoned_in_flight", "stale_before_release"} and not any(candidate.get("replaces") == execution_id for candidate in executions.values()):
            errors.append(error("DISPLACED_EXECUTION_SUCCESSOR_MISSING", execution_id, "displaced execution has no replacement attempt"))
    return obligations, executions, edges


def validate_milestones(work: Path, active_ac: set[str], active_mo: set[str], obligations: dict[str, dict[str, Any]], executions: dict[str, dict[str, Any]], errors: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    paths = workspace_paths(work)
    records = load_records(find_json(paths["milestones"], "**/revisions/*.json"), errors)
    active = newest_by_id(records)
    active_milestones = {record_ref(record): record for _, record in active.values()}
    all_refs = {record_ref(record): record for _, record in records}
    edges: dict[str, set[str]] = defaultdict(set)
    ac_claims: dict[str, list[str]] = defaultdict(list)
    mo_claims: dict[str, list[str]] = defaultdict(list)
    execution_membership: dict[str, list[str]] = defaultdict(list)
    for path, record in records:
        source = relative(path)
        ref = record_ref(record)
        if not MILESTONE_REF.fullmatch(ref):
            errors.append(error("MILESTONE_REFERENCE_INVALID", source, f"invalid milestone identity: {ref}"))
        check_integrity(record, source, errors, allow_pending=False)
        klass = record.get("class")
        if klass not in MILESTONE_CLASS:
            errors.append(error("MILESTONE_CLASS_INVALID", ref, f"unsupported milestone class: {klass}"))
        claims = record.get("claims", {})
        acs = claims.get("acceptance_criteria", [])
        mos = claims.get("maintenance_objectives", [])
        if klass == "behavioral" and not acs:
            errors.append(error("BEHAVIORAL_MILESTONE_HAS_NO_AC", ref, "behavioral milestone must borrow at least one active AC"))
        if klass == "behavioral" and not record.get("joint_evidence"):
            errors.append(error("MILESTONE_JOINT_EVIDENCE_MISSING", ref, "behavioral milestone requires composition-level evidence"))
        if klass != "behavioral" and acs:
            errors.append(error("NONBEHAVIORAL_MILESTONE_CLAIMS_AC", ref, f"{klass} milestone may not claim product ACs"))
        if klass == "maintenance" and not mos:
            errors.append(error("MAINTENANCE_OBJECTIVE_MISSING", ref, "maintenance milestone must claim an approved maintenance objective"))
        if klass != "maintenance" and mos:
            errors.append(error("NONMAINTENANCE_MILESTONE_CLAIMS_MO", ref, "only maintenance milestones may claim maintenance objectives"))
        if klass == "enabling" and not record.get("enables"):
            errors.append(error("ENABLING_CONSUMER_MISSING", ref, "enabling milestone must name downstream consumers"))
        if klass == "enabling" and not record.get("downstream_failure_disposition"):
            errors.append(error("ENABLING_FAILURE_DISPOSITION_MISSING", ref, "enabling milestone must define downstream failure disposition"))
        for evidence in record.get("joint_evidence", []):
            if evidence.get("member_evidence_carry_permitted") is not False:
                errors.append(error("MILESTONE_MEMBER_EVIDENCE_CARRY", ref, "joint milestone evidence cannot be satisfied by member evidence carry"))
        observability = record.get("observability", {})
        mode = observability.get("mode")
        if mode not in OBS_MODES:
            errors.append(error("OBSERVABILITY_MODE_INVALID", ref, f"unsupported observability mode: {mode}"))
        if not observability.get("monitoring_owner") or not observability.get("incident_owner"):
            errors.append(error("OBSERVABILITY_OWNER_MISSING", ref, "monitoring and incident owners are required"))
        rollback = record.get("rollback", {})
        rollback_class = rollback.get("class")
        if rollback_class not in REVERSAL:
            errors.append(error("MILESTONE_ROLLBACK_CLASS_INVALID", ref, f"unsupported rollback class: {rollback_class}"))
        if rollback_class == "irreversible" and not rollback.get("exception_decision"):
            errors.append(error("IRREVERSIBLE_ROLLBACK_DECISION_MISSING", ref, "irreversible milestone requires an approved decision reference"))
        if not rollback.get("owner") or not rollback.get("procedure"):
            errors.append(error("ROLLBACK_CONTRACT_INCOMPLETE", ref, "rollback owner and procedure are required"))
        for dependency in record.get("dependencies", []):
            target = dependency.get("milestone") if isinstance(dependency, dict) else None
            if target:
                edges[ref].add(target)
    for ref, record in active_milestones.items():
        claims = record.get("claims", {})
        for ac in claims.get("acceptance_criteria", []):
            if ac not in active_ac:
                errors.append(error("MILESTONE_AC_INACTIVE", ref, f"milestone claims inactive or unknown AC: {ac}"))
            ac_claims[ac].append(ref)
        for mo in claims.get("maintenance_objectives", []):
            if mo not in active_mo:
                errors.append(error("MILESTONE_MO_INACTIVE", ref, f"milestone claims inactive or unknown maintenance objective: {mo}"))
            mo_claims[mo].append(ref)
        for execution in record.get("executions", []):
            execution_membership[execution].append(ref)
            if execution not in executions:
                errors.append(error("MILESTONE_EXECUTION_MISSING", ref, f"milestone contains unknown execution: {execution}"))
            elif executions[execution].get("milestone") != ref:
                errors.append(error("EXECUTION_MILESTONE_MISMATCH", execution, f"execution declares {executions[execution].get('milestone')} but membership is {ref}"))
        for dependency in record.get("dependencies", []):
            target = dependency.get("milestone")
            if target not in active_milestones:
                errors.append(error("ACTIVE_MILESTONE_DEPENDENCY_INACTIVE", ref, f"dependency is not an active milestone revision: {target}"))
    for ac in active_ac:
        claimants = ac_claims.get(ac, [])
        if len(claimants) != 1:
            errors.append(error("AC_MILESTONE_CLAIM_COUNT", ac, "active AC must be claimed by exactly one behavioral milestone", claimants=claimants))
    for mo in active_mo:
        claimants = mo_claims.get(mo, [])
        if len(claimants) != 1:
            errors.append(error("MO_MILESTONE_CLAIM_COUNT", mo, "active maintenance objective must be claimed by exactly one maintenance milestone", claimants=claimants))
    current_executions = {record.get("current_execution") for record in obligations.values() if record.get("current_execution")}
    for execution in sorted(current_executions):
        membership = execution_membership.get(execution, [])
        if len(membership) != 1:
            errors.append(error("EXECUTION_MILESTONE_MEMBERSHIP_COUNT", execution, "current execution must belong to exactly one active milestone", milestones=membership))
    for execution, memberships in execution_membership.items():
        if execution not in current_executions:
            errors.append(error("HISTORICAL_EXECUTION_IN_CURRENT_MILESTONE", execution, "current milestone composition may contain only current execution attempts", milestones=memberships))
    cycle = detect_cycle(active_milestones, edges)
    if cycle:
        errors.append(error("MILESTONE_GRAPH_CYCLE", "release-graph", " -> ".join(cycle)))
    return active_milestones, edges


def validate_plans(work: Path, intent: dict[str, Any], active_decisions: dict[str, dict[str, Any]], obligations: dict[str, dict[str, Any]], executions: dict[str, dict[str, Any]], milestones: dict[str, dict[str, Any]], role_names: set[str], errors: list[dict[str, Any]]) -> None:
    paths = workspace_paths(work)
    records = load_records(find_json(paths["plans"], "**/revisions/*.json"), errors)
    for path, plan in records:
        source = relative(path)
        ref = record_ref(plan)
        if not PLAN_REF.fullmatch(ref):
            errors.append(error("PLAN_REFERENCE_INVALID", source, f"invalid plan reference: {ref}"))
        check_integrity(plan, source, errors, allow_pending=False)
        classification = plan.get("classification", {})
        if classification.get("risk") not in RISK:
            errors.append(error("PLAN_RISK_INVALID", ref, "risk must be low, moderate, high, or critical"))
        if classification.get("size_class") not in SIZE:
            errors.append(error("PLAN_SIZE_CLASS_INVALID", ref, "size class must be XS, S, M, L, or XL"))
        if classification.get("size_class") in {"L", "XL"} and not classification.get("size_unknowns"):
            errors.append(error("PLAN_SIZE_UNKNOWNS_MISSING", ref, "large plans must name size-changing unknowns"))
        approval = plan.get("approval_requirements", {})
        for role in [approval.get("primary_role"), *approval.get("additional_roles", [])]:
            if role not in role_names:
                errors.append(error("PLAN_APPROVAL_ROLE_UNKNOWN", ref, f"unknown approval role: {role}"))
        records_map = plan.get("records", {})
        expected = {
            "obligations": {identity: content_hash(record) for identity, record in obligations.items()},
            "executions": {identity: content_hash(record) for identity, record in executions.items() if obligations.get(record.get("obligation"), {}).get("current_execution") == identity},
            "milestones": {identity: content_hash(record) for identity, record in milestones.items()},
        }
        for category, actual_records in records_map.items():
            if category not in expected or not isinstance(actual_records, list):
                continue
            actual = {item.get("id"): item.get("content_hash") for item in actual_records if isinstance(item, dict)}
            if actual != expected[category]:
                errors.append(error("PLAN_RECORD_MANIFEST_STALE", ref, f"{category} manifest does not match current normative records", expected=expected[category], actual=actual))
        basis = plan.get("basis", {})
        if basis.get("intent_manifest_hash") != content_hash(intent):
            errors.append(error("PLAN_INTENT_HASH_STALE", ref, "plan does not bind the current intent manifest"))
        generated = plan.get("generated_views", {})
        generated_paths = {"plan_md_hash": paths["plan_view"], "task_graph_hash": paths["task_graph"], "release_graph_hash": paths["release_graph"]}
        for field, generated_path in generated_paths.items():
            if generated_path.exists() and generated.get(field) != file_hash(generated_path.read_bytes()):
                errors.append(error("PLAN_GENERATED_HASH_STALE", ref, f"{field} does not match the generated file"))
        if paths["decision_graph"].exists() and basis.get("decision_graph_hash") != file_hash(paths["decision_graph"].read_bytes()):
            errors.append(error("PLAN_DECISION_GRAPH_HASH_STALE", ref, "plan does not bind the current decision graph"))
        source_text = json.dumps(plan, ensure_ascii=False)
        if CALENDAR_ESTIMATE.search(source_text):
            errors.append(error("CALENDAR_ESTIMATE_PROHIBITED", ref, "plan records may not contain calendar effort estimates"))


def validate_authorizations(work: Path, active_plans: dict[str, dict[str, Any]], active_milestones: dict[str, dict[str, Any]], executions: dict[str, dict[str, Any]], role_names: set[str], errors: list[dict[str, Any]]) -> None:
    paths = workspace_paths(work)
    records = load_records(find_json(paths["authorizations"], "*.json"), errors)
    for path, authorization in records:
        source = relative(path)
        check_integrity(authorization, source, errors, allow_pending=False)
        basis = authorization.get("basis", {})
        plan_ref = basis.get("plan_revision")
        plan = active_plans.get(plan_ref)
        if not plan:
            errors.append(error("AUTHORIZATION_PLAN_INACTIVE", source, f"authorization references inactive plan: {plan_ref}"))
        elif basis.get("plan_manifest_hash") != content_hash(plan):
            errors.append(error("AUTHORIZATION_PLAN_HASH_MISMATCH", source, "authorization plan hash does not match the active plan"))
        scope = authorization.get("scope", {})
        milestones = scope.get("milestones", [])
        scoped_executions = scope.get("executions", [])
        if any(item in {"*", "all", "all_current"} for item in [*milestones, *scoped_executions]):
            errors.append(error("AUTHORIZATION_WILDCARD_PROHIBITED", source, "authorization must name exact milestones and executions"))
        for milestone in milestones:
            if milestone not in active_milestones:
                errors.append(error("AUTHORIZATION_MILESTONE_INACTIVE", source, f"authorization references inactive milestone: {milestone}"))
        for execution in scoped_executions:
            if execution not in executions:
                errors.append(error("AUTHORIZATION_EXECUTION_MISSING", source, f"authorization references missing execution: {execution}"))
        role = authorization.get("authority", {}).get("required_role")
        if role not in role_names:
            errors.append(error("AUTHORIZATION_ROLE_UNKNOWN", source, f"unknown authority role: {role}"))


def validate_generated_views(work: Path, errors: list[dict[str, Any]]) -> None:
    try:
        outputs = build_outputs(work)
    except PlanningError as exc:
        errors.append(error("GENERATED_VIEW_BUILD_FAILED", relative(work), str(exc)))
        return
    for path, expected in outputs.items():
        if not path.exists():
            errors.append(error("GENERATED_VIEW_MISSING", relative(path), "generated planning view is missing"))
        elif path.read_text(encoding="utf-8") != expected:
            errors.append(error("GENERATED_VIEW_STALE", relative(path), "generated planning view does not match source records"))


def validate_workspace(work: Path, require_complete: bool = True) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    paths = workspace_paths(work)
    try:
        model = load_json(paths["model"])
    except PlanningError as exc:
        return [error("PLANNING_MODEL_INVALID", relative(paths["model"]), str(exc))]
    if model.get("planning_model_version") != 2:
        return [error("PLANNING_MODEL_UNSUPPORTED", relative(paths["model"]), "planning_model_version must be 2")]
    try:
        intent = load_json(paths["intent"])
        roles = load_json(ROOT / "planning-approval-roles.json") if (ROOT / "planning-approval-roles.json").exists() else load_json(SKILL / "config/approval-roles.example.json")
    except PlanningError as exc:
        return [error("WORKSPACE_AUTHORITY_INPUT_INVALID", relative(work), str(exc))]
    role_names = required_role_names(roles)
    active_ac, active_mo = validate_intent(intent, relative(paths["intent"]), errors)
    active_decisions, _ = validate_decisions(work, active_ac, role_names, errors)
    obligations, executions, _ = validate_tasks(work, active_ac, active_decisions, errors)
    milestones, _ = validate_milestones(work, active_ac, active_mo, obligations, executions, errors)
    plan_records = load_records(find_json(paths["plans"], "**/revisions/*.json"), errors)
    active_plan_by_id = newest_by_id(plan_records)
    active_plans = {record_ref(record): record for _, record in active_plan_by_id.values()}
    if plan_records and intent.get("status") != "approved":
        errors.append(error("PLAN_INTENT_NOT_APPROVED", relative(paths["intent"]), "Gate 2 requires approved intent"))
    validate_plans(work, intent, active_decisions, obligations, executions, milestones, role_names, errors)
    validate_authorizations(work, active_plans, milestones, executions, role_names, errors)
    if require_complete or plan_records:
        validate_generated_views(work, errors)
    return errors


GATE_PATHS = {
    "GATE_0": ("brief.md", "intent/", "intent-manifest.json"),
    "GATE_1": ("decisions/", "decisions.md", "decision-graph.json"),
    "GATE_2": ("tasks/", "milestones/", "plans/", "plan.md", "task-graph.json", "release-graph.json", "planning-context.json"),
    "AUTHORIZATION": ("authorizations/implementation/",),
}


def classify_changed_paths(paths: list[str]) -> tuple[str, list[dict[str, Any]], list[Path]]:
    gates: set[str] = set()
    works: set[Path] = set()
    errors: list[dict[str, Any]] = []
    for path in paths:
        if path.startswith("docs/work/_template/") or not path.startswith("docs/work/"):
            continue
        parts = Path(path).parts
        if len(parts) < 4:
            continue
        work = ROOT.joinpath(*parts[:3])
        works.add(work)
        relative_to_work = "/".join(parts[3:])
        for gate, prefixes in GATE_PATHS.items():
            if any(relative_to_work == prefix or relative_to_work.startswith(prefix) for prefix in prefixes):
                gates.add(gate)
        if any(segment in path for segment in ("/src/", "/tests/", "/migrations/", "/infrastructure/")):
            gates.add("IMPLEMENTATION")
    if not gates:
        return "NONE", errors, sorted(works)
    if len(gates) > 1:
        errors.append(error("MIXED_AUTHORITY_GATES", "pull-request", "planning PR combines multiple authority gates", gates=sorted(gates)))
        return "MIXED", errors, sorted(works)
    return next(iter(gates)), errors, sorted(works)


def output_result(errors: list[dict[str, Any]], gate: str | None = None) -> int:
    payload = {"status": "FAIL" if errors else "PASS", "gate": gate, "errors": errors}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contracts-only", action="store_true")
    parser.add_argument("--work", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    errors: list[dict[str, Any]] = []
    gate: str | None = None
    validate_contracts(errors)
    if args.contracts_only:
        return output_result(errors, "CONTRACTS")
    works: list[Path] = []
    if args.work:
        works = [args.work.resolve()]
    elif args.all:
        works = feature_workspaces()
    elif args.changed_only:
        try:
            paths = changed_paths(args.base_ref)
        except PlanningError as exc:
            errors.append(error("CHANGED_PATH_DISCOVERY_FAILED", "pull-request", str(exc)))
            return output_result(errors)
        gate, gate_errors, works = classify_changed_paths(paths)
        errors.extend(gate_errors)
    else:
        parser.error("choose --contracts-only, --work, --all, or --changed-only")
    for work in works:
        errors.extend(validate_workspace(work, require_complete=not args.allow_draft))
    return output_result(errors, gate)


if __name__ == "__main__":
    raise SystemExit(main())
