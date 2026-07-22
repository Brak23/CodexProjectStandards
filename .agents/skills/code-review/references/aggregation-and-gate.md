# Aggregation and merge gate

## Aggregation

Aggregation preserves structure. It reports:

- snapshot identity and freshness,
- required and received dimensions,
- required and received seams,
- verdict per owned scope,
- open, addressed, disputed, regressed, resolved, withdrawn, superseded, and waived findings,
- evidence satisfaction by source,
- open escalations and unresolved owner assignments,
- blocking work grouped by owner.

Top-level aggregation status:

- `COMPLETE`
- `INCOMPLETE`
- `STALE`
- `CONTRADICTORY`
- `INVALID`

`COMPLETE` means the record set is coherent and fully evaluable. It does not mean reviewers approved.

## Dimensions and seams

General engineering owns seam detection, not automatic seam assessment. General-plus-specialist seams may default to the specialist when policy says so. Unregistered specialist-to-specialist seams require explicit owner assignment.

Seam review is phase two and consumes every constituent dimension result. A seam verdict may request changes while all constituent dimensions approve in isolation.

Static seam triggers operate directly on the diff and may instantiate missing dimensions. Reviewers may also add dimensions or seams through bounded judgment-based escalation.

## Merge gate

The gate is deterministic and consumes the aggregate, current policy, repository state, CI, approvals, dependency state, and exceptions. It returns only:

- `ALLOW`
- `BLOCK`

Conditions that remain unmet produce `BLOCK`, not a third conditional state. Emergency progression is `ALLOW` with `decision_basis: EMERGENCY_POLICY` and explicit bypassed normal requirements and post-merge obligations.

The gate checks, in order:

1. identity and freshness,
2. policy validity,
3. requirement-set stabilization,
4. dimension and seam coverage,
5. scoped verdicts,
6. finding-ledger state,
7. evidence sufficiency,
8. human approvals,
9. CI and repository controls,
10. dependency and release sequencing.

A previous `ALLOW` is invalidated by head changes, disallowed base drift, failed reruns, revoked approval, expired waiver, new required scope, regression, blocking current-policy changes, or dependency-state changes.
