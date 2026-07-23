#!/usr/bin/env python3
"""Classify a pull-request diff into one planning authority gate."""

from __future__ import annotations

import argparse
import json

from planning_common import changed_paths
from validate_planning_artifacts import classify_changed_paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default="origin/main")
    args = parser.parse_args()
    gate, errors, works = classify_changed_paths(changed_paths(args.base_ref))
    print(json.dumps({"gate": gate, "workspaces": [str(path) for path in works], "errors": errors}, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
