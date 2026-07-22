#!/usr/bin/env python3
"""Capture a target-neutral immutable review snapshot from Git state."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


class SnapshotError(RuntimeError):
    pass


def git(*args: str, binary: bool = False, check: bool = True):
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=not binary,
        check=False,
    )
    if check and result.returncode:
        stderr = result.stderr.decode() if binary else result.stderr
        raise SnapshotError(f"git {' '.join(args)} failed: {stderr.strip()}")
    return result.stdout


def ensure_repo() -> Path:
    if git("rev-parse", "--is-inside-work-tree", check=False).strip() != "true":
        raise SnapshotError("snapshot capture requires a Git working tree")
    return Path(git("rev-parse", "--show-toplevel").strip())


def full_sha(ref: str) -> str:
    value = git("rev-parse", "--verify", f"{ref}^{{commit}}", check=False).strip()
    if not value:
        raise SnapshotError(f"cannot resolve commit: {ref}")
    return value


def diff_args(args: argparse.Namespace) -> tuple[list[str], list[str], str | None, str | None]:
    common = ["--binary", "--full-index", "--no-ext-diff"]
    names = ["--name-only", "--no-ext-diff"]
    if args.target == "staged":
        return ["diff", "--cached", *common], ["diff", "--cached", *names], full_sha("HEAD"), None
    if args.target == "unstaged":
        return ["diff", *common], ["diff", *names], full_sha("HEAD"), None
    if args.target == "commit":
        if not args.commit:
            raise SnapshotError("commit target requires --commit")
        commit = full_sha(args.commit)
        parents = git("rev-list", "--parents", "-n", "1", commit).strip().split()
        base = parents[1] if len(parents) > 1 else None
        return ["show", "--format=", *common, commit], ["show", "--format=", *names, commit], base, commit
    if args.target in {"branch_diff", "github_pr"}:
        if not args.base or not args.head:
            raise SnapshotError(f"{args.target} requires --base and --head")
        base = full_sha(args.base)
        head = full_sha(args.head)
        range_spec = f"{base}...{head}"
        return ["diff", *common, range_spec], ["diff", *names, range_spec], base, head
    raise SnapshotError(f"unsupported target: {args.target}")


def is_dirty(*args: str, cwd: Path) -> bool:
    result = subprocess.run(["git", *args, "--quiet"], cwd=cwd, check=False)
    if result.returncode not in {0, 1}:
        raise SnapshotError(f"git {' '.join(args)} --quiet returned {result.returncode}")
    return result.returncode == 1


def canonical_hash(metadata: dict, patch: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    digest.update(b"\0")
    digest.update(patch)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["staged", "unstaged", "commit", "branch_diff", "github_pr"], default="staged")
    parser.add_argument("--commit")
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--omit-patch", action="store_true", help="write only manifest and changed-file list")
    args = parser.parse_args()

    try:
        root = ensure_repo()
        patch_command, names_command, base_commit, head_commit = diff_args(args)
        patch = git(*patch_command, binary=True)
        names_text = git(*names_command)
        changed_files = sorted({line for line in names_text.splitlines() if line})
        untracked = [line for line in git("ls-files", "--others", "--exclude-standard").splitlines() if line]
        staged_dirty = is_dirty("diff", "--cached", cwd=root)
        unstaged_dirty = is_dirty("diff", cwd=root)
        index_tree = git("write-tree").strip()
        patch_sha = hashlib.sha256(patch).hexdigest()
        identity = {
            "target_type": args.target,
            "base_commit": base_commit,
            "head_commit": head_commit,
            "index_tree": index_tree if args.target == "staged" else None,
            "diff_sha256": patch_sha,
            "changed_files": changed_files,
        }
        snapshot_hash = canonical_hash(identity, patch)
        snapshot_id = f"snapshot-{snapshot_hash[:16]}"
        manifest = {
            "schema_version": 1,
            "snapshot_id": snapshot_id,
            "snapshot_sha256": snapshot_hash,
            "diff_sha256": patch_sha,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "repository_root": str(root),
            "target": {
                "type": args.target,
                "base_commit": base_commit,
                "head_commit": head_commit,
            },
            "scope": {
                "included_paths": changed_files,
                "excluded_local_state": {
                    "unstaged_changes": args.target != "unstaged" and unstaged_dirty,
                    "staged_changes": args.target != "staged" and staged_dirty,
                    "untracked_files": bool(untracked),
                    "untracked_count": len(untracked),
                },
            },
            "local_state": {
                "index_tree_hash": index_tree,
                "staged_dirty": staged_dirty,
                "unstaged_dirty": unstaged_dirty,
            },
            "patch": {
                "included": not args.omit_patch,
                "bytes": len(patch),
                "sha256": patch_sha,
            },
        }
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (args.output / "changed-files.txt").write_text("\n".join(changed_files) + ("\n" if changed_files else ""), encoding="utf-8")
        if not args.omit_patch:
            (args.output / "diff.patch").write_bytes(patch)
        print(json.dumps({"snapshot_id": snapshot_id, "manifest": str(args.output / "manifest.json")}, indent=2))
        return 0
    except SnapshotError as exc:
        print(f"snapshot error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
