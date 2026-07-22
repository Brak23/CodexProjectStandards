#!/usr/bin/env python3
"""Compose policy, plan, and content-triggered review requirements."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path


class RequirementError(RuntimeError):
    pass


def load(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RequirementError(f"cannot read {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RequirementError(f"artifact must be a JSON object: {path}")
    return payload


def merge_value(definition: dict, current, incoming, requirement_id: str, parameter: str):
    kind = definition.get("type")
    if current is None:
        return deepcopy(incoming)
    if kind == "set":
        return sorted(set(current or []) | set(incoming or []))
    if kind == "number":
        direction = definition.get("stronger")
        if direction == "higher":
            return max(current, incoming)
        if direction == "lower":
            return min(current, incoming)
    if kind == "boolean":
        stronger = definition.get("stronger", True)
        return bool(current) or bool(incoming) if stronger else bool(current) and bool(incoming)
    if kind == "enum":
        order = definition.get("order") or []
        if current not in order or incoming not in order:
            raise RequirementError(f"unknown enum value for {requirement_id}.{parameter}")
        return current if order.index(current) >= order.index(incoming) else incoming
    if current != incoming:
        raise RequirementError(f"ambiguous parameter composition for {requirement_id}.{parameter}")
    return current


def add_requirement(effective: dict, registry: dict, item, source: dict) -> None:
    if isinstance(item, str):
        requirement_id, parameters = item, {}
    elif isinstance(item, dict):
        requirement_id = item.get("id")
        parameters = item.get("parameters") or {}
    else:
        raise RequirementError(f"invalid requirement entry: {item!r}")
    definitions = registry.get("requirements") or {}
    if requirement_id not in definitions:
        raise RequirementError(f"requirement is not in controlled vocabulary: {requirement_id}")
    record = effective.setdefault(requirement_id, {"id": requirement_id, "parameters": {}, "imposed_by": []})
    parameter_definitions = definitions[requirement_id].get("parameters") or {}
    for name, value in parameters.items():
        if name not in parameter_definitions:
            raise RequirementError(f"unknown parameter for {requirement_id}: {name}")
        record["parameters"][name] = merge_value(
            parameter_definitions[name], record["parameters"].get(name), value, requirement_id, name
        )
    record["imposed_by"].append(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--change-class", required=True)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--detected", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        policy = load(args.policy)
        registry = load(args.registry)
        classes = policy.get("change_classes") or {}
        if args.change_class not in classes:
            raise RequirementError(f"unknown change class: {args.change_class}")
        effective: dict[str, dict] = {}
        for item in classes[args.change_class].get("requirements") or []:
            add_requirement(
                effective,
                registry,
                item,
                {"source": "policy", "change_class": args.change_class, "policy_version": policy.get("policy_version")},
            )

        dimensions = {"general_engineering"}
        seams: list[dict] = []
        if args.plan:
            plan = load(args.plan)
            for item in plan.get("additional_requirements") or []:
                add_requirement(effective, registry, item, {"source": "plan", "reference": str(args.plan)})
            dimensions.update(plan.get("required_dimensions") or [])
            seams.extend(plan.get("required_seams") or [])
        if args.detected:
            detected = load(args.detected)
            for item in detected.get("requirements") or []:
                add_requirement(
                    effective,
                    registry,
                    item,
                    {"source": "diff_trigger", "trigger": detected.get("trigger_id", "detected-content")},
                )
            dimensions.update(detected.get("dimensions") or [])
            seams.extend(detected.get("seams") or [])
            for seam in seams:
                if isinstance(seam, dict):
                    dimensions.update(seam.get("participant_dimensions") or seam.get("dimensions") or [])

        result = {
            "schema_version": 1,
            "policy_version": policy.get("policy_version"),
            "change_class": args.change_class,
            "requirements": [effective[key] for key in sorted(effective)],
            "required_dimensions": sorted(dimensions),
            "required_seams": seams,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Composed {len(result['requirements'])} effective requirements.")
        return 0
    except RequirementError as exc:
        print(f"requirement composition error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
