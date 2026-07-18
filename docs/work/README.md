# Feature workspaces

Feature workspaces preserve the intent contract, execution contract, decisions, and evidence for non-trivial changes.

Create one with:

```bash
task feature FEATURE=APP-001 NAME=user-authentication
```

The workspace contains:

- `brief.md`: Approved product and behavior specification.
- `plan.md`: Approved implementation and verification plan.
- `decisions.md`: Task-level consequential decisions.
- `verification.md`: Final evidence and completion status.

After release, archive the workspace:

```bash
task archive-feature WORK=docs/work/APP-001-user-authentication
```

Preserve briefs, decisions, and verification. Progress detail may be condensed before archival, but do not delete evidence needed to explain behavior or risk.
