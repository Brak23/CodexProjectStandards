#!/usr/bin/env python3
"""Dependency-free tests for the project-local code-review skill tooling."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPTS = ROOT / ".agents/skills/code-review/scripts"


def run(*args: str, cwd: Path | None = None, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != expect:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expect}: {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_snapshot_and_requirements(temporary: Path) -> None:
    repo = temporary / "capture-repo"
    repo.mkdir()
    run("git", "init", "-q", cwd=repo)
    run("git", "config", "user.name", "Test Reviewer", cwd=repo)
    run("git", "config", "user.email", "reviewer@example.invalid", cwd=repo)
    (repo / "app.py").write_text("print('one')\n", encoding="utf-8")
    run("git", "add", "app.py", cwd=repo)
    run("git", "commit", "-q", "-m", "initial", cwd=repo)
    (repo / "app.py").write_text("print('two')\n", encoding="utf-8")
    run("git", "add", "app.py", cwd=repo)
    snapshot_dir = temporary / "captured-snapshot"
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "capture_review_snapshot.py"),
        "--target",
        "staged",
        "--output",
        str(snapshot_dir),
        cwd=repo,
    )
    manifest = json.loads((snapshot_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["target"]["type"] == "staged"
    assert manifest["scope"]["included_paths"] == ["app.py"]
    assert manifest["snapshot_id"].startswith("snapshot-")
    assert (snapshot_dir / "diff.patch").exists()

    policy = ROOT / ".agents/skills/code-review/config/review-policy.example.json"
    registry = ROOT / ".agents/skills/code-review/config/evidence-requirements.example.json"
    plan = temporary / "plan-requirements.json"
    detected = temporary / "detected-requirements.json"
    composed = temporary / "effective-requirements.json"
    write_json(
        plan,
        {
            "additional_requirements": [
                {
                    "id": "test.integration",
                    "parameters": {"scenarios": ["downstream_timeout"], "required_status": "PASSED"},
                }
            ],
            "required_dimensions": ["data"],
        },
    )
    write_json(
        detected,
        {
            "trigger_id": "authorization-boundary",
            "requirements": [{"id": "review.security", "parameters": {"minimum_level": "specialist"}}],
            "dimensions": ["security"],
            "seams": [],
        },
    )
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "compose_requirements.py"),
        "--policy",
        str(policy),
        "--registry",
        str(registry),
        "--change-class",
        "standard_change",
        "--plan",
        str(plan),
        "--detected",
        str(detected),
        "--output",
        str(composed),
        cwd=ROOT,
    )
    requirements = json.loads(composed.read_text(encoding="utf-8"))
    ids = {item["id"] for item in requirements["requirements"]}
    assert {"test.targeted", "test.integration", "review.security"} <= ids
    assert {"general_engineering", "data", "security"} <= set(requirements["required_dimensions"])


def test_review_store(temporary: Path) -> None:
    repo = temporary / "repo"
    repo.mkdir()
    run("git", "init", "-q", cwd=repo)
    run("git", "config", "user.name", "Test Reviewer", cwd=repo)
    run("git", "config", "user.email", "reviewer@example.invalid", cwd=repo)
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    run("git", "add", "README.md", cwd=repo)
    run("git", "commit", "-q", "-m", "initial", cwd=repo)
    run("git", "remote", "add", "origin", "https://example.invalid/repo.git", cwd=repo)

    store = SKILL_SCRIPTS / "review_store.py"
    run(sys.executable, str(store), "init", cwd=repo)
    fetch_specs = run("git", "config", "--get-all", "remote.origin.fetch", cwd=repo).stdout
    assert "+refs/reviews/*:refs/reviews/*" in fetch_specs

    snapshot = temporary / "snapshot"
    write_json(snapshot / "manifest.json", {"schema_version": 1, "snapshot_id": "snap-1"})
    run(sys.executable, str(store), "put-snapshot", "--snapshot-id", "snap-1", "--bundle", str(snapshot), cwd=repo)
    run("git", "rev-parse", "refs/reviews/snapshots/snap-1", cwd=repo)
    run(sys.executable, str(store), "put-snapshot", "--snapshot-id", "snap-1", "--bundle", str(snapshot), cwd=repo, expect=1)

    ledger1 = temporary / "ledger1"
    write_json(ledger1 / "findings.json", {"schema_version": 1, "findings": []})
    first = json.loads(run(sys.executable, str(store), "append-ledger", "--work-id", "WORK-1", "--bundle", str(ledger1), cwd=repo).stdout)["commit"]
    ledger2 = temporary / "ledger2"
    write_json(ledger2 / "findings.json", {"schema_version": 1, "findings": [{"record_id": "GEN-1"}]})
    second = json.loads(run(sys.executable, str(store), "append-ledger", "--work-id", "WORK-1", "--bundle", str(ledger2), cwd=repo).stdout)["commit"]
    parent = run("git", "rev-parse", f"{second}^", cwd=repo).stdout.strip()
    assert parent == first

    merge_sha = run("git", "rev-parse", "HEAD", cwd=repo).stdout.strip()
    run(
        sys.executable,
        str(store),
        "put-merge-alias",
        "--merge-commit",
        merge_sha,
        "--merge-method",
        "squash",
        "--reviewed-head",
        merge_sha,
        "--base-commit",
        merge_sha,
        "--snapshot-id",
        "snap-1",
        cwd=repo,
    )
    run(sys.executable, str(store), "verify", cwd=repo)


def test_reconciliation(temporary: Path) -> None:
    candidates = temporary / "candidates.json"
    ledger = temporary / "ledger.json"
    output = temporary / "reconcile.json"
    common = {
        "record_type": "dimension_finding",
        "dimension": "security",
        "defect_class": "authorization_after_disclosure",
        "affected_contract": "resource_confidentiality",
        "location": {"path": "api/resource.py", "symbol": "get_resource"},
        "acceptance_criterion": {"statement": "Authorize before data access."},
    }
    write_json(candidates, {"records": [{"record_id": "NEW", **common}]})
    write_json(ledger, {"findings": [{"record_id": "SEC-1", "status": "RESOLVED", **common}]})
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "reconcile_findings.py"),
        "--candidates",
        str(candidates),
        "--ledger",
        str(ledger),
        "--output",
        str(output),
    )
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["results"][0]["outcome"] == "REGRESSION"


def test_aggregation_and_gate(temporary: Path) -> None:
    coordination = temporary / "coordination.json"
    dimension = temporary / "dimension.json"
    ledger = temporary / "findings.json"
    evidence = temporary / "evidence.json"
    aggregate = temporary / "aggregate.json"
    state = temporary / "state.json"
    gate = temporary / "gate.json"

    write_json(
        coordination,
        {
            "schema_version": 1,
            "snapshot_id": "snap-1",
            "requirement_set": {"stabilized": True, "escalation_rounds_used": 0},
            "dimensions": {"required": ["general_engineering"]},
            "seams": {"required": []},
            "escalations": {"open": [], "resolved": []},
        },
    )
    write_json(
        dimension,
        {
            "schema_version": 1,
            "review_id": "review-1",
            "snapshot_id": "snap-1",
            "owned_scope": ["general_engineering"],
            "verdicts": {"general_engineering": {"verdict": "APPROVE", "confidence": "HIGH"}},
            "coverage": {},
        },
    )
    write_json(ledger, {"schema_version": 1, "findings": []})
    write_json(evidence, {"schema_version": 1, "sufficiency": "SUFFICIENT", "satisfied": ["test.targeted"], "unsatisfied": [], "stale": [], "contradictory": []})
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "aggregate_reviews.py"),
        "--coordination",
        str(coordination),
        "--dimension-review",
        str(dimension),
        "--ledger",
        str(ledger),
        "--evidence",
        str(evidence),
        "--output",
        str(aggregate),
    )
    result = json.loads(aggregate.read_text(encoding="utf-8"))
    assert result["status"] == "COMPLETE"

    write_json(
        state,
        {
            "schema_version": 1,
            "snapshot_id": "snap-1",
            "base_fresh": True,
            "merge_conflict": False,
            "branch_protection_satisfied": True,
            "dependencies_ready": True,
            "ci": {"required": True, "status": "MISSING", "snapshot_id": "snap-1"},
            "approvals": {"required": ["review"], "present": ["review"]},
            "evaluated_at": "2026-07-22T00:00:00Z",
            "exception": {"enabled": False},
        },
    )
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "evaluate_merge_gate.py"),
        "--aggregate",
        str(aggregate),
        "--repository-state",
        str(state),
        "--output",
        str(gate),
        expect=2,
    )
    gate_result = json.loads(gate.read_text(encoding="utf-8"))
    assert gate_result["decision"] == "BLOCK"
    assert any(item["type"] == "REQUIRED_CI_MISSING" for item in gate_result["blockers"])

    invalid_gate = temporary / "invalid-exception-gate.json"
    invalid_state = json.loads(state.read_text(encoding="utf-8"))
    invalid_state["exception"] = {
        "enabled": True,
        "bypasses": ["REQUIRED_CI_MISSING"],
        "decision_basis": "EMERGENCY_POLICY",
    }
    write_json(state, invalid_state)
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "evaluate_merge_gate.py"),
        "--aggregate",
        str(aggregate),
        "--repository-state",
        str(state),
        "--output",
        str(invalid_gate),
        expect=2,
    )
    invalid_result = json.loads(invalid_gate.read_text(encoding="utf-8"))
    assert any(item["type"] == "EXCEPTION_INVALID" for item in invalid_result["blockers"])

    allowed_gate = temporary / "allowed-exception-gate.json"
    invalid_state["exception"] = {
        "enabled": True,
        "authority_verified": True,
        "approved_by": "incident-commander",
        "scope": ["snap-1"],
        "expires_at": "2026-07-23T00:00:00Z",
        "decision_basis": "EMERGENCY_POLICY",
        "bypasses": ["REQUIRED_CI_MISSING"],
        "compensating_controls": ["manual deployment monitoring"],
        "post_merge_obligations": ["run full CI"],
    }
    write_json(state, invalid_state)
    run(
        sys.executable,
        str(SKILL_SCRIPTS / "evaluate_merge_gate.py"),
        "--aggregate",
        str(aggregate),
        "--repository-state",
        str(state),
        "--output",
        str(allowed_gate),
    )
    allowed_result = json.loads(allowed_gate.read_text(encoding="utf-8"))
    assert allowed_result["decision"] == "ALLOW"
    assert allowed_result["decision_basis"] == "EMERGENCY_POLICY"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="code-review-skill-test-") as temp:
        temporary = Path(temp)
        test_snapshot_and_requirements(temporary)
        test_review_store(temporary)
        test_reconciliation(temporary)
        test_aggregation_and_gate(temporary)
    print("Code review skill tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
