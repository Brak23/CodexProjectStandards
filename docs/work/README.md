# Feature workspaces

Feature workspaces preserve approved intent, immutable decision and plan records, operational state, execution history, release composition, and evidence for non-trivial changes.

Create a model-v2 workspace with:

```bash
task feature FEATURE=APP-001 NAME=user-authentication
```

## Model-v2 workspace

The workspace contains:

- `planning-model.json`: Selects the planning validator version.
- `brief.md`: Human-readable Gate 0 product specification.
- `intent-manifest.json`: Machine-readable active acceptance-criterion and maintenance-objective revisions.
- `decisions/`: Immutable Gate 1 decision revisions, separated by authority domain.
- `tasks/`: Stable obligations and immutable execution attempts.
- `milestones/`: Validated behavioral, enabling, or maintenance release compositions.
- `plans/`: Immutable Gate 2 plan manifests.
- `authorizations/implementation/`: Immutable events that grant, restrict, pause, revoke, or supersede implementation scope.
- `decisions.md` and `plan.md`: Generated review views. Do not edit them manually.
- `decision-graph.json`, `task-graph.json`, and `release-graph.json`: Generated dependency and coverage views.
- `planning-context.json`: Repository evidence inspected by the planner.
- `impact-assessment.json`: Amendment propagation and affected closure.
- `state.yml`: Operational projection of current planning, ownership, authorization, and verification state.
- `verification.md`: Final engineering evidence and completion status.
- `ux-requirements.md` and `ui-verification.md`: Conditional UI requirements and evidence.

## Gate sequence

1. Gate 0 approves intent and acceptance criteria.
2. Gate 1 approves technical decision revisions.
3. Gate 2 approves obligations, execution attempts, milestone compositions, evidence design, and the plan manifest.
4. A separate authorization event permits named implementation work to begin.

Use separate PRs for each gate. A mixed authority diff fails validation.

## State rules

- Agents may maintain operational state but may not approve their own intent, decisions, plan, implementation authorization, or release authorization.
- `state.yml` is not authority. It must agree with protected records, authenticated approvals, current branch, base commit, and observed repository state.
- Every active AC maps to an obligation and exactly one behavioral milestone.
- Every active obligation has one current execution attempt.
- Every current execution belongs to one current milestone revision.
- Follow the amendment process when approved intent, decisions, or release composition changes.
- Use the recovery protocol after context reset, interruption, or handoff.

## Legacy workspaces

Existing workspaces without `planning-model.json` remain model-v1. Migrate deliberately with:

```bash
task plan-migrate WORK=docs/work/APP-001-user-authentication
```

Migration preserves legacy artifacts, creates only draft model-v2 records, and grants no approval or implementation authority.

After release, archive the workspace:

```bash
task archive-feature WORK=docs/work/APP-001-user-authentication
```

Preserve intent, decisions, plan revisions, execution and release history, authorizations, and evidence needed to explain behavior, authority, ownership, and risk.
