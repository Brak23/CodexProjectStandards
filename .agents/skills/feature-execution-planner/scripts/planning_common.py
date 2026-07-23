#!/usr/bin/env python3
"""Shared dependency-free planning record, graph, hashing, and workspace helpers."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[4]
SKILL = Path(__file__).resolve().parents[1]
CANONICALIZATION = "planning-canonical-json-v1"

AC_REF = re.compile(r"^AC-[0-9]{3,}@[0-9]+$")
MO_REF = re.compile(r"^MO-[0-9]{3,}@[0-9]+$")
DEC_REF = re.compile(r"^DEC-[0-9]{3,}@[0-9]+$")
TASK_ID = re.compile(r"^TASK-[0-9]{3,}$")
EXEC_REF = re.compile(r"^TASK-[0-9]{3,}/[0-9]+$")
MILESTONE_REF = re.compile(r"^MILESTONE-[0-9]{3,}/[0-9]+$")
PLAN_REF = re.compile(r"^PLAN-[0-9]{3,}/[0-9]+$")


class PlanningError(ValueError):
    pass


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PlanningError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicates)
    except (OSError, json.JSONDecodeError, PlanningError) as exc:
        raise PlanningError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PlanningError(f"{path} must contain a JSON object")
    return value


def dump_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def normalized_record(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("integrity", None)
    return result


def canonical_bytes(value: dict[str, Any]) -> bytes:
    normalized = normalized_record(value)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def content_hash(value: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_hash(content: str | bytes) -> str:
    data = content.encode("utf-8") if isinstance(content, str) else content
    return "sha256:" + hashlib.sha256(data).hexdigest()


def set_integrity(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result["integrity"] = {"algorithm": CANONICALIZATION, "content_hash": content_hash(result)}
    return result


def check_integrity(value: dict[str, Any], source: str, errors: list[dict[str, Any]], allow_pending: bool = False) -> None:
    integrity = value.get("integrity")
    if not isinstance(integrity, dict):
        errors.append(error("INTEGRITY_MISSING", source, "record has no integrity object"))
        return
    if integrity.get("algorithm") != CANONICALIZATION:
        errors.append(error("CANONICALIZATION_UNSUPPORTED", source, "record must use planning-canonical-json-v1"))
    expected = integrity.get("content_hash")
    if allow_pending and expected == "PENDING":
        return
    actual = content_hash(value)
    if expected != actual:
        errors.append(error("CONTENT_HASH_MISMATCH", source, f"expected {expected}, computed {actual}"))


def error(code: str, record: str, message: str, **details: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"code": code, "record": record, "message": message}
    if details:
        payload["details"] = details
    return payload


def current_ref(base: str, revision: int) -> str:
    return f"{base}@{revision}" if base.startswith(("AC-", "MO-", "DEC-")) else f"{base}/{revision}"


def workspace_paths(work: Path) -> dict[str, Path]:
    return {
        "model": work / "planning-model.json",
        "intent": work / "intent-manifest.json",
        "decisions": work / "decisions",
        "tasks": work / "tasks",
        "milestones": work / "milestones",
        "plans": work / "plans",
        "authorizations": work / "authorizations" / "implementation",
        "decisions_view": work / "decisions.md",
        "plan_view": work / "plan.md",
        "decision_graph": work / "decision-graph.json",
        "task_graph": work / "task-graph.json",
        "release_graph": work / "release-graph.json",
    }


def find_json(root: Path, pattern: str) -> list[Path]:
    return sorted(path for path in root.glob(pattern) if path.is_file()) if root.exists() else []


def load_records(paths: Iterable[Path], errors: list[dict[str, Any]]) -> list[tuple[Path, dict[str, Any]]]:
    result: list[tuple[Path, dict[str, Any]]] = []
    for path in paths:
        try:
            result.append((path, load_json(path)))
        except PlanningError as exc:
            errors.append(error("INVALID_JSON", path.as_posix(), str(exc)))
    return result


def record_ref(value: dict[str, Any]) -> str:
    identity = value.get("id")
    revision = value.get("revision")
    if isinstance(identity, str) and isinstance(revision, int):
        return current_ref(identity, revision)
    return str(identity or "UNKNOWN")


def newest_by_id(records: Iterable[tuple[Path, dict[str, Any]]]) -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path, record in records:
        identity = record.get("id")
        revision = record.get("revision", 0)
        if not isinstance(identity, str) or not isinstance(revision, int):
            continue
        current = result.get(identity)
        if current is None or int(current[1].get("revision", 0)) < revision:
            result[identity] = (path, record)
    return result


def detect_cycle(nodes: Iterable[str], edges: dict[str, set[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visited:
            return None
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        visiting.add(node)
        stack.append(node)
        for target in sorted(edges.get(node, set())):
            cycle = visit(target)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(set(nodes)):
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def transitive_dependents(start: Iterable[str], reverse_edges: dict[str, set[str]]) -> set[str]:
    seen = set(start)
    queue = deque(start)
    while queue:
        current = queue.popleft()
        for dependent in reverse_edges.get(current, set()):
            if dependent not in seen:
                seen.add(dependent)
                queue.append(dependent)
    return seen


def git(*args: str, cwd: Path = ROOT, check: bool = True) -> str:
    completed = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=False)
    if check and completed.returncode:
        raise PlanningError(completed.stderr.strip() or completed.stdout.strip() or "git command failed")
    return completed.stdout.strip()


def changed_paths(base_ref: str, cwd: Path = ROOT) -> list[str]:
    output = git("diff", "--name-only", f"{base_ref}...HEAD", cwd=cwd)
    return sorted(line for line in output.splitlines() if line)


def feature_workspaces(root: Path = ROOT) -> list[Path]:
    work_root = root / "docs" / "work"
    if not work_root.exists():
        return []
    return sorted(path for path in work_root.iterdir() if path.is_dir() and path.name != "_template" and (path / "planning-model.json").exists())


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def required_role_names(registry: dict[str, Any]) -> set[str]:
    roles = registry.get("roles", {})
    return set(roles) if isinstance(roles, dict) else set()


def graph_payload(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema_version": 1, "nodes": sorted(nodes, key=lambda item: str(item.get("id"))), "edges": sorted(edges, key=lambda item: (str(item.get("from")), str(item.get("to")), str(item.get("type", ""))))}
