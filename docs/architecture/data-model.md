# Data architecture

## Systems of record

| Data domain | System of record | Owner | Classification | Retention |
| --- | --- | --- | --- | --- |
| [Domain] | [System] | [Owner] | [Public/Internal/Confidential/Restricted] | [Policy] |

## Consistency

Document which workflows require strong consistency, eventual consistency, idempotency, ordering, and reconciliation.

## Schema changes

Use expand-and-contract for changes that cross deployments:

1. Add backward-compatible schema.
2. Deploy compatible application behavior.
3. Backfill in bounded restartable batches.
4. Reconcile and verify.
5. Switch reads and writes.
6. Remove legacy schema in a later release.

## Migration requirements

Every material migration must state row volume, locking behavior, mixed-version compatibility, batch size, restartability, reconciliation query, backup requirement, and rollback or forward-fix path.
