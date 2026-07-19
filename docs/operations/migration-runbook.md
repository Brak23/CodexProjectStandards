# Data migration runbook

## Scope and ownership

- Migration owner:
- Technical approver:
- Data owner:
- Tables or stores:
- Estimated records and bytes:
- Risk classification:

## Compatibility sequence

Describe expand, compatible deployment, bounded backfill, reconciliation, read/write switch, and later contraction.

## Execution design

- Batch size and rate limit
- Locking behavior
- Transaction boundary
- Restart and checkpoint behavior
- Idempotency
- Concurrency controls
- Expected runtime
- Monitoring and alert thresholds

## Validation

Provide preflight queries, invariant checks, reconciliation queries, sample validation, and success thresholds.

## Recovery

Document backup requirement, rollback feasibility, forward-fix, pause conditions, and maximum tolerable partial state.

## Approval and timeline

Record staging rehearsal, production window, approvers, operators, communication, and post-migration observation period.
