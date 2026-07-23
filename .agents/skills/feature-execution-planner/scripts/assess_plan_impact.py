#!/usr/bin/env python3
"""Compute decision-to-task-to-milestone impact closure for a feature workspace."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from planning_common import dump_json, find_json, load_json, load_records, newest_by_id, record_ref, transitive_dependents, workspace_paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--decision")
    parser.add_argument("--acceptance-criterion")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    paths = workspace_paths(work)
    errors: list[dict] = []
    decisions = load_records(find_json(paths["decisions"], "**/revisions/*.json"), errors)
    obligations = load_records(find_json(paths["tasks"], "**/obligation.json"), errors)
    executions = load_records(find_json(paths["tasks"], "**/executions/*.json"), errors)
    milestones = load_records(find_json(paths["milestones"], "**/revisions/*.json"), errors)
    if errors:
        raise SystemExit(json.dumps(errors, indent=2))
    active_decisions = {record_ref(record): record for _, record in newest_by_id(decisions).values()}
    reverse_decisions: dict[str, set[str]] = defaultdict(set)
    for ref, record in active_decisions.items():
        for dependency in record.get("depends_on", []):
            reverse_decisions[dependency.get("decision")].add(ref)
    affected_decisions = transitive_dependents([args.decision], reverse_decisions) if args.decision else set()
    affected_obligations: set[str] = set()
    for _, obligation in obligations:
        if args.acceptance_criterion and args.acceptance_criterion in obligation.get("intent_basis", []):
            affected_obligations.add(obligation.get("id"))
    affected_executions: set[str] = set()
    execution_map = {record.get("id"): record for _, record in executions}
    for identity, execution in execution_map.items():
        if set(execution.get("decision_basis", [])) & affected_decisions or execution.get("obligation") in affected_obligations:
            affected_executions.add(identity)
    reverse_execution: dict[str, set[str]] = defaultdict(set)
    for identity, execution in execution_map.items():
        for dependency in execution.get("dependencies", []):
            reverse_execution[dependency.get("execution")].add(identity)
    affected_executions = transitive_dependents(affected_executions, reverse_execution)
    affected_milestones: set[str] = set()
    for _, milestone in milestones:
        ref = record_ref(milestone)
        if set(milestone.get("executions", [])) & affected_executions:
            affected_milestones.add(ref)
        if args.acceptance_criterion and args.acceptance_criterion in milestone.get("claims", {}).get("acceptance_criteria", []):
            affected_milestones.add(ref)
    model = load_json(paths["model"])
    payload = {
        "schema_version": 1,
        "feature_id": model.get("feature_id"),
        "trigger": {"decision": args.decision, "acceptance_criterion": args.acceptance_criterion},
        "affected_decisions": sorted(item for item in affected_decisions if item),
        "affected_obligations": sorted(item for item in affected_obligations if item),
        "affected_executions": sorted(item for item in affected_executions if item),
        "affected_milestones": sorted(item for item in affected_milestones if item),
        "affected_authorizations": [],
        "uncertain_impact": False,
    }
    text = dump_json(payload)
    if args.write:
        (work / "impact-assessment.json").write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
