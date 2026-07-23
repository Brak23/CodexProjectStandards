#!/usr/bin/env python3
"""Render deterministic decisions, plan, task graph, and release graph views."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from planning_common import (
    PlanningError,
    dump_json,
    file_hash,
    find_json,
    graph_payload,
    load_json,
    load_records,
    newest_by_id,
    record_ref,
    relative,
    workspace_paths,
)

GENERATED = "<!-- GENERATED FILE. DO NOT EDIT. -->\n<!-- Source model: planning-model-v2 -->\n"


def collect(work: Path) -> dict[str, Any]:
    paths = workspace_paths(work)
    errors: list[dict[str, Any]] = []
    decisions = load_records(find_json(paths["decisions"], "**/revisions/*.json"), errors)
    obligations = load_records(find_json(paths["tasks"], "**/obligation.json"), errors)
    executions = load_records(find_json(paths["tasks"], "**/executions/*.json"), errors)
    milestones = load_records(find_json(paths["milestones"], "**/revisions/*.json"), errors)
    plans = load_records(find_json(paths["plans"], "**/revisions/*.json"), errors)
    if errors:
        raise PlanningError("cannot render invalid JSON records: " + json.dumps(errors))
    return {
        "decisions": decisions,
        "active_decisions": newest_by_id(decisions),
        "obligations": obligations,
        "executions": executions,
        "milestones": milestones,
        "active_milestones": newest_by_id(milestones),
        "plans": plans,
    }


def render_decisions(data: dict[str, Any], feature: str) -> str:
    lines = [GENERATED.rstrip(), "", f"# Decisions: {feature}", ""]
    active = data["active_decisions"]
    if not active:
        lines.extend(["No decision revisions have been recorded.", ""])
    for identity, (_, record) in sorted(active.items()):
        ref = record_ref(record)
        lines.extend([
            f"## {ref}: {record.get('title', identity)}",
            "",
            f"- Domain: `{record.get('domain', 'unknown')}`",
            f"- Reversal: `{record.get('reversal', {}).get('class', 'unknown')}`",
            f"- Primary approval role: `{record.get('approval_requirements', {}).get('primary_role', 'unknown')}`",
            f"- Deadline: `{record.get('deadline', 'unknown')}`",
            f"- Default: `{record.get('default_on_deadline', 'unknown')}`",
        ])
        dependencies = record.get("depends_on", [])
        if dependencies:
            lines.append("- Depends on: " + ", ".join(f"`{item.get('decision')}`" for item in dependencies))
        recommendation = record.get("recommendation", {})
        lines.extend([f"- Recommendation: `{recommendation.get('option', 'none')}`", "", str(recommendation.get("rationale", "")), "", "### Options", ""])
        for option in record.get("options", []):
            lines.extend([f"- **{option.get('id')}**: {option.get('summary')}", f"  - Forecloses: {', '.join(option.get('forecloses', [])) or 'None recorded'}", f"  - Reversal requirements: {', '.join(option.get('reversal_requirements', [])) or 'None recorded'}"])
        lines.append("")
    lines.extend(["## Revision history", ""])
    for _, record in sorted(data["decisions"], key=lambda item: (str(item[1].get("id")), int(item[1].get("revision", 0)))):
        lines.append(f"- `{record_ref(record)}` supersedes `{record.get('supersedes') or 'none'}`")
    return "\n".join(lines).rstrip() + "\n"


def render_plan(data: dict[str, Any], feature: str) -> str:
    lines = [GENERATED.rstrip(), "", f"# Execution plan: {feature}", ""]
    plan_records = sorted(data["plans"], key=lambda item: int(item[1].get("revision", 0)))
    if plan_records:
        plan = plan_records[-1][1]
        lines.extend([f"- Current plan: `{record_ref(plan)}`", f"- Risk: `{plan.get('classification', {}).get('risk', 'unknown')}`", f"- Size class: `{plan.get('classification', {}).get('size_class', 'unknown')}`", ""])
        unknowns = plan.get("classification", {}).get("size_unknowns", [])
        if unknowns:
            lines.extend(["## Size-changing unknowns", ""] + [f"- {item}" for item in unknowns] + [""])
    else:
        lines.extend(["No plan revision has been recorded.", ""])

    lines.extend(["## Milestone release compositions", ""])
    if not data["active_milestones"]:
        lines.extend(["No milestone revisions have been recorded.", ""])
    for _, (_, milestone) in sorted(data["active_milestones"].items()):
        ref = record_ref(milestone)
        claims = milestone.get("claims", {})
        lines.extend([
            f"### {ref}", "",
            f"- Class: `{milestone.get('class')}`",
            f"- Borrowed ACs: {', '.join(f'`{item}`' for item in claims.get('acceptance_criteria', [])) or 'None'}",
            f"- Maintenance objectives: {', '.join(f'`{item}`' for item in claims.get('maintenance_objectives', [])) or 'None'}",
            f"- Executions: {', '.join(f'`{item}`' for item in milestone.get('executions', []))}",
            f"- Observability mode: `{milestone.get('observability', {}).get('mode', 'unknown')}`",
            f"- Rollback class: `{milestone.get('rollback', {}).get('class', 'unknown')}`",
            f"- Release owner: `{milestone.get('release_owner', 'unknown')}`",
            "",
        ])

    lines.extend(["## Obligations and current executions", ""])
    execution_map = {record.get("id"): record for _, record in data["executions"]}
    for _, obligation in sorted(data["obligations"], key=lambda item: str(item[1].get("id"))):
        execution = execution_map.get(obligation.get("current_execution"), {})
        lines.extend([
            f"### {obligation.get('id')}: {obligation.get('title')}", "",
            f"- Intent basis: {', '.join(f'`{item}`' for item in obligation.get('intent_basis', []))}",
            f"- Current execution: `{obligation.get('current_execution')}`",
            f"- Decision basis: {', '.join(f'`{item}`' for item in execution.get('decision_basis', [])) or 'None'}",
            f"- Milestone: `{execution.get('milestone', 'unassigned')}`",
            f"- Allowed modules: {', '.join(f'`{item}`' for item in execution.get('implementation', {}).get('allowed_modules', [])) or 'None declared'}",
            "",
        ])

    lines.extend(["## Evidence design", ""])
    for _, execution in sorted(data["executions"], key=lambda item: str(item[1].get("id"))):
        requirements = [item.get("predicate", "unknown") for item in execution.get("evidence_requirements", [])]
        lines.append(f"- `{execution.get('id')}`: {', '.join(f'`{item}`' for item in requirements) or 'No predicates declared'}")
    lines.extend(["", "## Replanning and authorization", "", "Implementation requires a current immutable authorization event naming the exact plan, milestone revisions, and execution attempts. Plan approval alone does not authorize implementation.", ""])
    return "\n".join(lines).rstrip() + "\n"


def graphs(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision_nodes, decision_edges = [], []
    for _, record in data["decisions"]:
        ref = record_ref(record)
        decision_nodes.append({"id": ref, "base_id": record.get("id"), "revision": record.get("revision")})
        for dependency in record.get("depends_on", []):
            decision_edges.append({"from": ref, "to": dependency.get("decision"), "type": "depends_on"})

    task_nodes, task_edges = [], []
    for _, obligation in data["obligations"]:
        task_nodes.append({"id": obligation.get("id"), "type": "obligation", "intent_basis": obligation.get("intent_basis", []), "current_execution": obligation.get("current_execution")})
        for ac in obligation.get("intent_basis", []):
            task_edges.append({"from": obligation.get("id"), "to": ac, "type": "traces_to"})
    for _, execution in data["executions"]:
        task_nodes.append({"id": execution.get("id"), "type": "execution", "obligation": execution.get("obligation"), "milestone": execution.get("milestone")})
        task_edges.append({"from": execution.get("id"), "to": execution.get("obligation"), "type": "executes"})
        for dependency in execution.get("dependencies", []):
            task_edges.append({"from": execution.get("id"), "to": dependency.get("execution"), "type": "depends_on"})

    release_nodes, release_edges = [], []
    for _, milestone in data["milestones"]:
        ref = record_ref(milestone)
        release_nodes.append({"id": ref, "class": milestone.get("class"), "claims": milestone.get("claims", {})})
        for execution in milestone.get("executions", []):
            release_edges.append({"from": ref, "to": execution, "type": "contains"})
        for dependency in milestone.get("dependencies", []):
            release_edges.append({"from": ref, "to": dependency.get("milestone"), "type": dependency.get("type", "depends_on")})
    return graph_payload(decision_nodes, decision_edges), graph_payload(task_nodes, task_edges), graph_payload(release_nodes, release_edges)


def build_outputs(work: Path) -> dict[Path, str]:
    model = load_json(work / "planning-model.json")
    feature = str(model.get("feature_name") or model.get("feature_id") or work.name)
    data = collect(work)
    decision_graph, task_graph, release_graph = graphs(data)
    paths = workspace_paths(work)
    return {
        paths["decisions_view"]: render_decisions(data, feature),
        paths["plan_view"]: render_plan(data, feature),
        paths["decision_graph"]: dump_json(decision_graph),
        paths["task_graph"]: dump_json(task_graph),
        paths["release_graph"]: dump_json(release_graph),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    try:
        outputs = build_outputs(work)
    except PlanningError as exc:
        print(f"planning render failed: {exc}", file=sys.stderr)
        return 1
    stale: list[str] = []
    for path, content in outputs.items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        elif not path.exists() or path.read_text(encoding="utf-8") != content:
            stale.append(relative(path))
    if stale:
        print("generated planning views are stale:", file=sys.stderr)
        for path in stale:
            print(f"- {path}", file=sys.stderr)
        return 1
    if args.write:
        for path in outputs:
            print(relative(path))
    else:
        print("Generated planning views are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
