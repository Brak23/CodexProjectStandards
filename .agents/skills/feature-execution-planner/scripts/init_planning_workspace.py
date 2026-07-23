#!/usr/bin/env python3
"""Initialize or normalize a model-v2 feature planning workspace."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from planning_common import dump_json, set_integrity
from render_planning_views import build_outputs


def placeholder_feature(work: Path) -> tuple[str, str]:
    match = re.match(r"(?P<id>[^-]+)-(?P<name>.+)", work.name)
    if not match:
        return work.name, work.name.replace("-", " ").title()
    return match.group("id"), match.group("name").replace("-", " ").title()


def initialize(work: Path, feature_id: str | None = None, feature_name: str | None = None) -> None:
    work.mkdir(parents=True, exist_ok=True)
    inferred_id, inferred_name = placeholder_feature(work)
    feature_id = feature_id or inferred_id
    feature_name = feature_name or inferred_name
    for directory in (
        work / "decisions" / "architecture",
        work / "decisions" / "security",
        work / "decisions" / "privacy",
        work / "decisions" / "data",
        work / "decisions" / "operations",
        work / "tasks",
        work / "milestones",
        work / "plans",
        work / "authorizations" / "implementation",
    ):
        directory.mkdir(parents=True, exist_ok=True)
    model = {"schema_version": 1, "planning_model_version": 2, "feature_id": feature_id, "feature_name": feature_name, "status": "draft"}
    intent = set_integrity({
        "schema_version": 1,
        "id": "INTENT-001",
        "revision": 1,
        "feature_id": feature_id,
        "status": "draft",
        "acceptance_criteria": [],
        "maintenance_objectives": [],
        "non_goals": [],
        "constraints": [],
        "approval_basis": {"required_role": "product", "source": "brief.md"},
    })
    context = {"schema_version": 1, "feature_id": feature_id, "base_commit": None, "loaded_sources": [], "relevant_modules": [], "contracts": [], "existing_patterns": [], "rejected_paths": [], "limitations": []}
    impact = {"schema_version": 1, "feature_id": feature_id, "trigger": {}, "affected_decisions": [], "affected_obligations": [], "affected_executions": [], "affected_milestones": [], "affected_authorizations": [], "uncertain_impact": False}
    for path, value in ((work / "planning-model.json", model), (work / "intent-manifest.json", intent), (work / "planning-context.json", context), (work / "impact-assessment.json", impact)):
        if not path.exists():
            path.write_text(dump_json(value), encoding="utf-8")
    for path, content in build_outputs(work).items():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--feature-id")
    parser.add_argument("--feature-name")
    args = parser.parse_args()
    initialize(args.work.resolve(), args.feature_id, args.feature_name)
    print(args.work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
