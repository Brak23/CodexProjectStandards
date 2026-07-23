#!/usr/bin/env python3
"""Validate current-head planning approvals without executing untrusted PR code."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
import base64
from urllib.parse import quote
from collections import defaultdict
from pathlib import Path
from typing import Any

from planning_common import ROOT, PlanningError, load_json


def api(path: str, token: str) -> Any:
    request = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "feature-execution-planner-authority-check",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise PlanningError(f"GitHub API request failed for {path}: {exc}") from exc


def paged(path: str, token: str) -> list[dict[str, Any]]:
    page = 1
    result: list[dict[str, Any]] = []
    while True:
        separator = "&" if "?" in path else "?"
        payload = api(f"{path}{separator}per_page=100&page={page}", token)
        if not isinstance(payload, list):
            raise PlanningError(f"expected list from GitHub API path {path}")
        result.extend(item for item in payload if isinstance(item, dict))
        if len(payload) < 100:
            return result
        page += 1


def planning_gate(paths: list[str]) -> str:
    gates: set[str] = set()
    for path in paths:
        if path.startswith("docs/work/_template/") or not path.startswith("docs/work/"):
            continue
        relative = "/".join(Path(path).parts[3:])
        if relative == "brief.md" or relative == "intent-manifest.json" or relative.startswith("intent/"):
            gates.add("GATE_0")
        if relative.startswith("decisions/") or relative in {"decisions.md", "decision-graph.json"}:
            gates.add("GATE_1")
        if relative.startswith(("tasks/", "milestones/", "plans/")) or relative in {"plan.md", "task-graph.json", "release-graph.json", "planning-context.json", "impact-assessment.json"}:
            gates.add("GATE_2")
        if relative.startswith("authorizations/implementation/"):
            gates.add("AUTHORIZATION")
    if not gates:
        return "NONE"
    if len(gates) > 1:
        return "MIXED"
    return next(iter(gates))


def fetch_pr_json(repository: str, path: str, head_sha: str, token: str) -> dict[str, Any] | None:
    encoded = quote(path, safe="")
    payload = api(f"/repos/{repository}/contents/{encoded}?ref={head_sha}", token)
    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        return None
    try:
        value = json.loads(base64.b64decode(payload.get("content", "")).decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    return value if isinstance(value, dict) else None


def latest_reviews(reviews: list[dict[str, Any]], head_sha: str) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for review in sorted(reviews, key=lambda item: str(item.get("submitted_at") or "")):
        user = review.get("user", {}).get("login")
        if user:
            latest[user] = review
    return {
        user: review
        for user, review in latest.items()
        if review.get("state") == "APPROVED" and review.get("commit_id") == head_sha
    }


def main() -> int:
    repository = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")
    if not repository or not pr_number or not token:
        print("planning authority check skipped: GITHUB_REPOSITORY, PR_NUMBER, and GITHUB_TOKEN are required")
        return 0
    try:
        pr = api(f"/repos/{repository}/pulls/{pr_number}", token)
        files = paged(f"/repos/{repository}/pulls/{pr_number}/files", token)
        reviews = paged(f"/repos/{repository}/pulls/{pr_number}/reviews", token)
        registry_path = ROOT / "planning-approval-roles.json"
        registry = load_json(registry_path)
    except PlanningError as exc:
        print(f"planning authority check failed: {exc}", file=sys.stderr)
        return 1
    paths = [str(item.get("filename")) for item in files]
    gate = planning_gate(paths)
    if gate == "NONE":
        print("No feature planning authority gate detected; CODEOWNERS and normal repository protections apply.")
        return 0
    if gate == "MIXED":
        print("planning authority check failed: MIXED_AUTHORITY_GATES", file=sys.stderr)
        return 1
    if pr.get("draft"):
        print(f"Planning authority pending for {gate}: draft PRs are not approval-effective.")
        return 0
    head_sha = pr.get("head", {}).get("sha")
    author = pr.get("user", {}).get("login")
    approved = latest_reviews(reviews, head_sha)
    mode = registry.get("mode", "team")
    require_non_author = bool(registry.get("require_non_author_approval", mode == "team"))
    required_roles = {
        "GATE_0": {"product"},
        "GATE_1": set(),
        "GATE_2": set(),
        "AUTHORIZATION": set(),
    }[gate]
    for path in paths:
        record = None
        if gate == "GATE_1" and "/decisions/" in path and path.endswith(".json"):
            record = fetch_pr_json(repository, path, head_sha, token)
            approval = record.get("approval_requirements", {}) if record else {}
            required_roles.update([approval.get("primary_role"), *approval.get("additional_roles", [])])
        elif gate == "GATE_2" and "/plans/" in path and path.endswith(".json"):
            record = fetch_pr_json(repository, path, head_sha, token)
            approval = record.get("approval_requirements", {}) if record else {}
            required_roles.update([approval.get("primary_role"), *approval.get("additional_roles", [])])
        elif gate == "AUTHORIZATION" and "/authorizations/implementation/" in path and path.endswith(".json"):
            record = fetch_pr_json(repository, path, head_sha, token)
            required_roles.add(record.get("authority", {}).get("required_role") if record else None)
    required_roles.discard(None)
    if not required_roles:
        required_roles.add("architecture" if gate == "GATE_1" else "engineering_owner")
    # Path-level CODEOWNERS remains primary. The registry check verifies exact individual
    # owners when configured and reports team-owned roles as externally enforced.
    unsatisfied: list[str] = []
    external_roles: list[str] = []
    roles = registry.get("roles", {})
    for role in sorted(required_roles):
        definition = roles.get(role, {}) if isinstance(roles, dict) else {}
        owners = {str(item).lstrip("@") for item in definition.get("github_owners", [])}
        teams = definition.get("github_teams", [])
        if teams:
            external_roles.append(role)
        if owners and not (owners & set(approved)):
            if mode == "solo" and not require_non_author and author in owners:
                continue
            unsatisfied.append(role)
    if require_non_author and not any(user != author for user in approved):
        unsatisfied.append("non_author_current_head_approval")
    if unsatisfied:
        print(json.dumps({"status": "FAIL", "gate": gate, "head_sha": head_sha, "unsatisfied": sorted(set(unsatisfied)), "current_head_approvers": sorted(approved), "externally_enforced_team_roles": external_roles}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps({"status": "PASS", "gate": gate, "head_sha": head_sha, "current_head_approvers": sorted(approved), "externally_enforced_team_roles": external_roles, "mode": mode}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
