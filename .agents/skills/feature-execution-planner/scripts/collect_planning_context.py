#!/usr/bin/env python3
"""Collect deterministic repository planning context without modifying implementation files."""

from __future__ import annotations

import argparse
from pathlib import Path

from planning_common import PlanningError, dump_json, git, load_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--module", action="append", default=[])
    parser.add_argument("--contract", action="append", default=[])
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--limitation", action="append", default=[])
    args = parser.parse_args()
    work = args.work.resolve()
    model = load_json(work / "planning-model.json")
    try:
        base_commit = git("rev-parse", "HEAD")
    except PlanningError:
        base_commit = None
    loaded_sources = []
    for raw in args.source:
        path = Path(raw)
        loaded_sources.append({"path": raw, "status": "loaded" if path.exists() else "missing"})
    payload = {
        "schema_version": 1,
        "feature_id": model.get("feature_id"),
        "base_commit": base_commit,
        "loaded_sources": loaded_sources,
        "relevant_modules": [{"path": value, "reason": "Declared planning context"} for value in args.module],
        "contracts": [{"path": value, "type": "declared"} for value in args.contract],
        "existing_patterns": [],
        "rejected_paths": [],
        "limitations": args.limitation,
    }
    (work / "planning-context.json").write_text(dump_json(payload), encoding="utf-8")
    print(work / "planning-context.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
