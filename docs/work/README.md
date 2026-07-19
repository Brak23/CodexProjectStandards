# Feature workspaces

Feature workspaces preserve the intent contract, machine-readable state, execution contract, decisions, and evidence for non-trivial changes.

Create one with:

```bash
task feature FEATURE=APP-001 NAME=user-authentication
```

The workspace contains:

- `state.yml`: Phase, risk, approvals, authorization, ownership, branch, milestones, blockers, review, and verification state.
- `brief.md`: Approved product and behavior specification.
- `plan.md`: Approved implementation and verification plan.
- `ux-requirements.md`: Conditional UX and interaction requirements for UI-significant work.
- `decisions.md`: Task-level consequential decisions and approved amendments.
- `verification.md`: Final engineering evidence and completion status.
- `ui-verification.md`: Conditional visual, responsive, content, usability, and accessibility evidence.

## State rules

- Agents may maintain operational state but may not approve their own brief, plan, implementation authorization, or release authorization.
- `state.yml` must agree with authenticated approvals, work artifacts, current branch, base commit, and observed repository state.
- Follow the amendment process when approved intent or scope changes.
- Record reviewer level, reviewer identity or agent identifier, and reviewed commit.
- Use the recovery protocol after context reset, interruption, or handoff.

After release, archive the workspace:

```bash
task archive-feature WORK=docs/work/APP-001-user-authentication
```

Preserve state, briefs, decisions, and verification. Progress detail may be condensed before archival, but do not delete evidence needed to explain behavior, authority, ownership, or risk.
