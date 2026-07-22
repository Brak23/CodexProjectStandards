#!/usr/bin/env python3
"""Add code-review governance paths to generated-project CODEOWNERS."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEOWNERS = ROOT / "CODEOWNERS"
SENSITIVE_PATHS = (
    "/.agents/skills/",
    "/docs/engineering/review-system.md",
    "/agent-context.yml",
    "/agent-policy.yml",
)


def main() -> int:
    if not CODEOWNERS.exists():
        print("review governance configuration failed: CODEOWNERS is missing", file=sys.stderr)
        return 1

    text = CODEOWNERS.read_text(encoding="utf-8")
    owners = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("* "):
            owners = stripped[2:].strip()
            break
    if not owners:
        print("review governance configuration failed: CODEOWNERS has no wildcard owner", file=sys.stderr)
        return 1

    existing_paths = {
        raw.strip().split(maxsplit=1)[0]
        for raw in text.splitlines()
        if raw.strip() and not raw.lstrip().startswith("#") and len(raw.strip().split(maxsplit=1)) == 2
    }
    additions = [f"{path} {owners}" for path in SENSITIVE_PATHS if path not in existing_paths]
    if additions:
        updated = text.rstrip() + "\n\n# Review governance and project-local skills.\n" + "\n".join(additions) + "\n"
        CODEOWNERS.write_text(updated, encoding="utf-8")
        print(f"Added {len(additions)} review governance CODEOWNERS entries.")
    else:
        print("Review governance CODEOWNERS entries already configured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
