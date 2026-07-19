# Multi-agent coordination

Multiple agents may work in the same repository only when ownership, role, branch, and reviewed state are explicit.

## Work ownership

The active feature `state.yml` records:

- Human owner.
- Active agent identifier.
- Agent role.
- Agent-owned branch.
- Base commit.
- Lease update time.

Only one implementer may own a feature workspace at a time unless the plan explicitly partitions independent workstreams.

## Roles

- **Implementer:** May modify approved scope on the assigned branch.
- **Reviewer:** Read-only by default. Reports findings against a specific commit.
- **Verifier:** Runs deterministic checks and records evidence without changing implementation.
- **Planner:** Performs discovery and prepares artifacts but does not implement before approval.

Role changes require an update to `state.yml`. A reviewer does not become an implementer merely by proposing a fix.

## Coordination rules

- Use separate branches or worktrees for concurrent work.
- Do not share an uncommitted working tree between agents.
- Record the base commit and refresh it after rebases or merges.
- Re-check overlapping files, contracts, migrations, and dependencies before integrating concurrent branches.
- Invalidate review and verification evidence when later changes affect the reviewed surface.
- Stop when another active lease exists and ownership cannot be confirmed.
- Resolve conflicting plans or state through the human owner, not through agent negotiation alone.

## Stale work

Before resuming stale work, follow `session-recovery.md`. If the default branch changed materially, update discovery and the plan before implementation continues.

## Lease guidance

A lease is coordination metadata, not a lock enforced by Git. Projects may define an expiration appropriate to their cadence. An expired lease permits reassignment only after repository state and the previous agent's recorded work are reconciled.
