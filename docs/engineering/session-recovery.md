# Session recovery and handoff

Use this protocol after context compaction, interruption, model change, agent handoff, or a long pause.

## Recovery sequence

1. Read `AGENTS.md`, `agent-context.yml`, and `agent-policy.yml`.
2. Locate the active feature workspace and read `state.yml`.
3. Read the approved brief, plan, decisions, and latest verification evidence.
4. Inspect the current branch, base commit, working tree, staged changes, and diff.
5. Compare repository state with the recorded phase, milestone, blockers, and reviewed commit.
6. Confirm that approvals remain valid and no protected branch or external change invalidated the plan.
7. Re-run the last milestone's smallest deterministic verification when feasible.
8. Update the ownership lease and `updated_at` field.
9. Resume only when recorded and observed state agree.

## Mismatch handling

Do not guess when:

- The branch differs from `state.yml`.
- Unexplained changes exist.
- The base branch advanced across affected code or contracts.
- Approval fields conflict with the brief or plan.
- The recorded milestone cannot be reproduced.
- Another active agent owns the work.

Record the mismatch, pause the affected phase, and request human resolution or perform an approved re-plan.

## Handoff summary

Before handing work to another agent or human, record:

- Current phase and milestone.
- Completed and remaining acceptance criteria.
- Files changed and current branch/commit.
- Commands run and exact results.
- Failed approaches and unexpected findings.
- Active blockers, approvals, limitations, and next safe action.
