# Contributing

## Workflow

1. Open or select a structured issue.
2. Create a feature workspace under `docs/work/` for non-trivial work.
3. Approve the brief and plan before implementation.
4. Create `agent/<description>` for agent work or `feature/<description>` for human-led work.
5. Commit using Conventional Commits.
6. Run `task verify`, the same verification contract used by CI.
7. Open a draft pull request using the repository template.
8. Resolve review findings and rerun affected validation.
9. Human approval and required checks are mandatory before merge.

## Commit format

```text
<type>(optional-scope): concise description
```

Supported types include `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, and `revert`.

Use `!` or a `BREAKING CHANGE:` footer for incompatible changes.

## Pull request size

Target fewer than 400 meaningful changed lines. More than 800 meaningful lines requires explicit justification or decomposition. Generated files, lockfiles, snapshots, and mechanical renames should be identified separately.

## Exceptions

Do not bypass a standard silently. Use `docs/engineering/exception-process.md` and obtain the required human approval before merge.

## Definition of done

- Acceptance criteria have evidence.
- Architecture boundaries are preserved.
- Security and data impacts are reviewed.
- Tests cover success and failure behavior.
- `task verify` and required checks pass.
- Documentation reflects final behavior.
- Rollout and rollback are understood.
- No unrelated changes are included.
