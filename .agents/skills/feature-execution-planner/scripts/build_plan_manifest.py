#!/usr/bin/env python3
"""Build an immutable plan manifest over current normative planning records."""

from __future__ import annotations

import argparse
from pathlib import Path

from planning_common import content_hash, dump_json, file_hash, find_json, git, load_json, load_records, newest_by_id, record_ref, set_integrity, workspace_paths
from render_planning_views import build_outputs


def refs(records):
    return {record_ref(record): record for _, record in records}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--plan-id", default="PLAN-001")
    parser.add_argument("--revision", type=int, required=True)
    parser.add_argument("--risk", choices=["low", "moderate", "high", "critical"], required=True)
    parser.add_argument("--size", choices=["XS", "S", "M", "L", "XL"], required=True)
    parser.add_argument("--unknown", action="append", default=[])
    parser.add_argument("--primary-role", default="engineering_owner")
    parser.add_argument("--additional-role", action="append", default=[])
    parser.add_argument("--base-commit")
    args = parser.parse_args()
    work = args.work.resolve()
    paths = workspace_paths(work)
    intent = load_json(paths["intent"])
    decision_records = load_records(find_json(paths["decisions"], "**/revisions/*.json"), [])
    obligations = load_records(find_json(paths["tasks"], "**/obligation.json"), [])
    executions = load_records(find_json(paths["tasks"], "**/executions/*.json"), [])
    milestones = load_records(find_json(paths["milestones"], "**/revisions/*.json"), [])
    active_milestones = refs(newest_by_id(milestones).values())
    obligation_map = {record.get("id"): record for _, record in obligations}
    current_execution_map = {
        record.get("id"): record
        for _, record in executions
        if obligation_map.get(record.get("obligation"), {}).get("current_execution") == record.get("id")
    }
    plans_dir = paths["plans"] / args.plan_id / "revisions"
    plans_dir.mkdir(parents=True, exist_ok=True)
    destination = plans_dir / f"{args.revision}.json"
    base_commit = args.base_commit
    if not base_commit:
        try:
            base_commit = git("rev-parse", "HEAD")
        except Exception:
            base_commit = "UNKNOWN"
    provisional = {
        "schema_version": 1,
        "id": args.plan_id,
        "revision": args.revision,
        "basis": {
            "intent_manifest_hash": content_hash(intent),
            "decision_graph_hash": "PENDING",
            "repository_base_commit": base_commit,
            "policy_version": 1,
        },
        "records": {
            "obligations": [{"id": identity, "content_hash": content_hash(record)} for identity, record in sorted(obligation_map.items())],
            "executions": [{"id": identity, "content_hash": content_hash(record)} for identity, record in sorted(current_execution_map.items())],
            "milestones": [{"id": identity, "content_hash": content_hash(record)} for identity, record in sorted(active_milestones.items())],
        },
        "classification": {"risk": args.risk, "size_class": args.size, "size_unknowns": args.unknown},
        "replan_when": [
            "active intent revision changes",
            "active decision revision changes",
            "an unplanned service boundary is crossed",
            "a new production dependency or migration is required",
            "risk classification increases",
            "approved implementation scope is exceeded",
            "rollback becomes coordinated or irreversible",
            "two implementation attempts fail for the same underlying symptom",
        ],
        "generated_views": {"plan_md_hash": "PENDING", "task_graph_hash": "PENDING", "release_graph_hash": "PENDING"},
        "approval_requirements": {"primary_role": args.primary_role, "additional_roles": args.additional_role},
        "integrity": {"algorithm": "planning-canonical-json-v1", "content_hash": "PENDING"},
    }
    destination.write_text(dump_json(provisional), encoding="utf-8")
    outputs = build_outputs(work)
    provisional["basis"]["decision_graph_hash"] = file_hash(outputs[paths["decision_graph"]])
    provisional["generated_views"] = {
        "plan_md_hash": file_hash(outputs[paths["plan_view"]]),
        "task_graph_hash": file_hash(outputs[paths["task_graph"]]),
        "release_graph_hash": file_hash(outputs[paths["release_graph"]]),
    }
    destination.write_text(dump_json(set_integrity(provisional)), encoding="utf-8")
    for path, content in build_outputs(work).items():
        path.write_text(content, encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
