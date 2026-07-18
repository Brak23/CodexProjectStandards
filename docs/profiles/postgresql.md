# PostgreSQL profile

- Use parameterized queries.
- Define transaction boundaries around business invariants.
- Include tenant predicates where required.
- Review query plans for high-volume paths.
- Add indexes based on observed access patterns.
- Use expand-and-contract migrations.
- Test migrations against production-like row counts.
- Make backfills bounded, restartable, observable, and reconcilable.
- Document backup, restore, RPO, RTO, and retention.
