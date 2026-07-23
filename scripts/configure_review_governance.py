#!/usr/bin/env python3
"""Add review and planning governance to generated-project ownership configuration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEOWNERS = ROOT / "CODEOWNERS"
ROLE_REGISTRY = ROOT / "planning-approval-roles.json"
SENSITIVE_PATHS = (
    "/.agents/skills/",
    "/.github/workflows/",
    "/docs/engineering/review-system.md",
    "/docs/engineering/feature-planning.md",
    "/docs/work/**/brief.md",
    "/docs/work/**/intent-manifest.json",
    "/docs/work/**/decisions/",
    "/docs/work/**/tasks/",
    "/docs/work/**/milestones/",
    "/docs/work/**/plans/",
    "/docs/work/**/authorizations/",
    "/planning-approval-roles.json",
    "/agent-context.yml",
    "/agent-policy.yml",
)
ROLES = ("product", "architecture", "security", "privacy", "data", "operations", "engineering_owner")


def main() -> int:
    if not CODEOWNERS.exists():
        print("governance configuration failed: CODEOWNERS is missing", file=sys.stderr)
        return 1
    text = CODEOWNERS.read_text(encoding="utf-8")
    owners = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("* "):
            owners = stripped[2:].strip()
            break
    if not owners:
        print("governance configuration failed: CODEOWNERS has no wildcard owner", file=sys.stderr)
        return 1
    existing_paths = {
        raw.strip().split(maxsplit=1)[0]
        for raw in text.splitlines()
        if raw.strip() and not raw.lstrip().startswith("#") and len(raw.strip().split(maxsplit=1)) == 2
    }
    additions = [f"{path} {owners}" for path in SENSITIVE_PATHS if path not in existing_paths]
    if additions:
        updated = text.rstrip() + "\n\n# Review, planning, and project-local skill governance.\n" + "\n".join(additions) + "\n"
        CODEOWNERS.write_text(updated, encoding="utf-8")
        print(f"Added {len(additions)} governance CODEOWNERS entries.")
    else:
        print("Review and planning CODEOWNERS entries already configured.")
    logins = [item.lstrip("@") for item in owners.split()]
    payload = None
    if ROLE_REGISTRY.exists():
        try:
            existing = json.loads(ROLE_REGISTRY.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"governance configuration failed: invalid planning approval role registry: {exc}", file=sys.stderr)
            return 1
        if existing.get("generated_from_codeowners"):
            payload = existing
    else:
        payload = {"schema_version": 1, "generated_from_codeowners": True, "roles": {}}
    if payload is not None:
        payload["mode"] = "solo" if len(logins) == 1 else "team"
        payload["require_non_author_approval"] = len(logins) > 1
        payload["roles"] = {role: {"github_owners": logins} for role in ROLES}
        ROLE_REGISTRY.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("Configured planning approval role registry from CODEOWNERS.")
    else:
        print("Custom planning approval role registry preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
