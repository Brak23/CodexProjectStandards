#!/usr/bin/env python3
"""Store review bundles in synthetic commits under refs/reviews/*.

This tool deliberately keeps durable review state outside the reviewed working
branch. It uses only Git plumbing and the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

ZERO_SHA = "0" * 40
SAFE = re.compile(r"^[A-Za-z0-9._-]+$")
REFSPEC = "+refs/reviews/*:refs/reviews/*"


class ReviewStoreError(RuntimeError):
    pass


def git(*args: str, input_text: str | None = None, check: bool = True) -> str:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Review System")
    env.setdefault("GIT_AUTHOR_EMAIL", "review-system@local.invalid")
    env.setdefault("GIT_COMMITTER_NAME", env["GIT_AUTHOR_NAME"])
    env.setdefault("GIT_COMMITTER_EMAIL", env["GIT_AUTHOR_EMAIL"])
    result = subprocess.run(
        ["git", *args],
        input=input_text,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ReviewStoreError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def require_repo() -> None:
    if git("rev-parse", "--is-inside-work-tree", check=False) != "true":
        raise ReviewStoreError("review store requires a Git working tree")


def safe_component(value: str, label: str) -> str:
    if not SAFE.fullmatch(value):
        raise ReviewStoreError(f"invalid {label}: {value!r}; use letters, numbers, dot, underscore, or hyphen")
    return value


def current_ref(ref: str) -> str | None:
    value = git("rev-parse", "--verify", "--quiet", ref, check=False)
    return value or None


def hash_file(path: Path) -> str:
    return git("hash-object", "-w", "--", str(path))


def build_tree(directory: Path) -> str:
    entries: list[str] = []
    for child in sorted(directory.iterdir(), key=lambda item: item.name):
        if child.is_symlink():
            raise ReviewStoreError(f"review bundle may not contain symlinks: {child}")
        if child.is_dir():
            sha = build_tree(child)
            entries.append(f"040000 tree {sha}\t{child.name}")
        elif child.is_file():
            sha = hash_file(child)
            executable = bool(child.stat().st_mode & 0o111)
            mode = "100755" if executable else "100644"
            entries.append(f"{mode} blob {sha}\t{child.name}")
    payload = "\n".join(entries) + ("\n" if entries else "")
    return git("mktree", input_text=payload)


def commit_tree(tree_sha: str, message: str, parent: str | None, sign: bool) -> str:
    args = ["commit-tree"]
    if sign:
        args.append("-S")
    args.extend([tree_sha, "-m", message])
    if parent:
        args.extend(["-p", parent])
    return git(*args)


def validate_bundle(directory: Path) -> None:
    if not directory.is_dir():
        raise ReviewStoreError(f"bundle directory does not exist: {directory}")
    files = [path for path in directory.rglob("*") if path.is_file()]
    if not files:
        raise ReviewStoreError("review bundle is empty")
    for path in files:
        if path.stat().st_size > 2_000_000:
            raise ReviewStoreError(f"durable review bundle file exceeds 2 MB: {path}")


def write_ref(ref: str, bundle: Path, message: str, *, immutable: bool, sign: bool) -> str:
    validate_bundle(bundle)
    previous = current_ref(ref)
    if immutable and previous:
        raise ReviewStoreError(f"immutable review ref already exists: {ref}")
    tree_sha = build_tree(bundle)
    commit_sha = commit_tree(tree_sha, message, None if immutable else previous, sign)
    expected = ZERO_SHA if previous is None else previous
    git("update-ref", ref, commit_sha, expected)
    return commit_sha


def init_store(remote: str) -> None:
    require_repo()
    remotes = git("remote").splitlines()
    if remote not in remotes:
        raise ReviewStoreError(f"remote {remote!r} does not exist")
    existing = git("config", "--get-all", f"remote.{remote}.fetch", check=False).splitlines()
    if REFSPEC not in existing:
        git("config", "--add", f"remote.{remote}.fetch", REFSPEC)
    print(f"Configured {remote} to fetch {REFSPEC}")
    print("Push review refs explicitly with: git push <remote> 'refs/reviews/*:refs/reviews/*'")


def put_snapshot(args: argparse.Namespace) -> None:
    snapshot_id = safe_component(args.snapshot_id, "snapshot id")
    ref = f"refs/reviews/snapshots/{snapshot_id}"
    sha = write_ref(ref, args.bundle, f"review snapshot {snapshot_id}", immutable=True, sign=args.sign)
    print(json.dumps({"ref": ref, "commit": sha}, indent=2))


def append_ledger(args: argparse.Namespace) -> None:
    work_id = safe_component(args.work_id, "work id")
    ref = f"refs/reviews/ledgers/{work_id}"
    sha = write_ref(ref, args.bundle, f"review ledger {work_id}", immutable=False, sign=args.sign)
    print(json.dumps({"ref": ref, "commit": sha}, indent=2))


def put_merge_alias(args: argparse.Namespace) -> None:
    merge_commit = args.merge_commit.lower()
    if not re.fullmatch(r"[0-9a-f]{40}", merge_commit):
        raise ReviewStoreError("merge commit must be a full 40-character SHA")
    snapshots = [safe_component(item, "snapshot id") for item in args.snapshot_id]
    with tempfile.TemporaryDirectory(prefix="review-merge-alias-") as temporary:
        bundle = Path(temporary)
        manifest = {
            "schema_version": 1,
            "merge_commit": merge_commit,
            "merge_method": args.merge_method,
            "reviewed_head": args.reviewed_head,
            "base_commit": args.base_commit,
            "snapshot_ids": snapshots,
            "snapshot_refs": [f"refs/reviews/snapshots/{item}" for item in snapshots],
        }
        (bundle / "aliases.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        ref = f"refs/reviews/merges/{merge_commit}"
        sha = write_ref(ref, bundle, f"review merge alias {merge_commit}", immutable=True, sign=args.sign)
    print(json.dumps({"ref": ref, "commit": sha}, indent=2))


def show_ref(args: argparse.Namespace) -> None:
    ref = args.ref
    sha = current_ref(ref)
    if not sha:
        raise ReviewStoreError(f"review ref does not exist: {ref}")
    print(git("ls-tree", "-r", sha))


def iter_review_refs() -> Iterable[str]:
    output = git("for-each-ref", "--format=%(refname)", "refs/reviews/")
    return [line for line in output.splitlines() if line]


def verify_store() -> None:
    require_repo()
    errors: list[str] = []
    refs = list(iter_review_refs())
    for ref in refs:
        sha = current_ref(ref)
        if not sha:
            errors.append(f"unresolvable review ref: {ref}")
            continue
        object_type = git("cat-file", "-t", sha, check=False)
        if object_type != "commit":
            errors.append(f"review ref does not point to commit: {ref} -> {object_type or 'missing'}")
        if ref.startswith("refs/reviews/merges/"):
            try:
                git("cat-file", "-e", f"{sha}:aliases.json")
            except ReviewStoreError:
                errors.append(f"merge alias lacks aliases.json: {ref}")
    if errors:
        print("Review store validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Review store validation passed for {len(refs)} refs.")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="configure remote fetch for refs/reviews/*")
    init.add_argument("--remote", default="origin")
    init.set_defaults(function=lambda args: init_store(args.remote))

    snapshot = commands.add_parser("put-snapshot", help="write an immutable snapshot bundle")
    snapshot.add_argument("--snapshot-id", required=True)
    snapshot.add_argument("--bundle", type=Path, required=True)
    snapshot.add_argument("--sign", action="store_true")
    snapshot.set_defaults(function=put_snapshot)

    ledger = commands.add_parser("append-ledger", help="append a work-ledger bundle")
    ledger.add_argument("--work-id", required=True)
    ledger.add_argument("--bundle", type=Path, required=True)
    ledger.add_argument("--sign", action="store_true")
    ledger.set_defaults(function=append_ledger)

    alias = commands.add_parser("put-merge-alias", help="map pre-merge snapshots to a final merge commit")
    alias.add_argument("--merge-commit", required=True)
    alias.add_argument("--merge-method", choices=["merge", "squash", "rebase"], required=True)
    alias.add_argument("--reviewed-head")
    alias.add_argument("--base-commit")
    alias.add_argument("--snapshot-id", action="append", required=True)
    alias.add_argument("--sign", action="store_true")
    alias.set_defaults(function=put_merge_alias)

    show = commands.add_parser("show", help="list files in a review ref")
    show.add_argument("ref")
    show.set_defaults(function=show_ref)

    verify = commands.add_parser("verify", help="validate local review refs")
    verify.set_defaults(function=lambda args: verify_store())
    return root


def main() -> int:
    try:
        require_repo()
        args = parser().parse_args()
        args.function(args)
    except ReviewStoreError as exc:
        print(f"review store error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
