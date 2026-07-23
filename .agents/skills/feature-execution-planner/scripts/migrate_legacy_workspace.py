#!/usr/bin/env python3
"""Preserve a legacy feature workspace and initialize model-v2 draft records."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from init_planning_workspace import initialize


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    if (work / "planning-model.json").exists():
        raise SystemExit("workspace already has a planning model; migration is not applicable")
    legacy = work / "legacy"
    legacy.mkdir(parents=True, exist_ok=True)
    for name in ("plan.md", "decisions.md", "state.yml"):
        source = work / name
        if source.exists():
            shutil.copy2(source, legacy / name)
    initialize(work)
    marker = work / "migration-review-required.md"
    marker.write_text(
        "# Migration review required\n\n"
        "Legacy artifacts were preserved under `legacy/`. Model-v2 records are draft only. "
        "They create no approval or implementation authorization and require normal Gate 1 and Gate 2 review.\n",
        encoding="utf-8",
    )
    print(work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
