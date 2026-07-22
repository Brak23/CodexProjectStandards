# Review record model

Review records use a shared envelope and typed payloads. Do not collapse records with different authority into one generic finding.

## Record types

- `dimension_finding`: binding or advisory conclusion from the owner of one dimension.
- `seam_finding`: binding or advisory conclusion about an interaction between dimensions.
- `routed_observation`: non-binding observation sent to the owning specialist.
- `plan_defect`: defect in the approved implementation or evidence plan.
- `evidence_gap`: required predicate that is unsatisfied, partial, stale, or contradictory.
- `escalation_request`: adds a dimension, seam, integration review, evidence requirement, or owner assignment.
- `strength`: zero to three evidence-backed examples of code-health improvement.
- `coverage_statement`: structural declaration of reviewed scope, omissions, and limitations.

## Scoped verdicts

A reviewer emits verdicts only for owned dimensions or seams:

- `APPROVE`
- `APPROVE_WITH_COMMENTS`
- `CHANGES_REQUESTED`
- `CANNOT_ASSESS`

No verdict is emitted for unowned scope. Missing required scope is detected by aggregation.

## Binding finding requirements

Every binding finding requires:

- stable record ID and fingerprint,
- owned dimension or seam,
- `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` severity based on consequence,
- `HIGH`, `MEDIUM`, or `LOW` confidence,
- concrete location or affected contract,
- problem and impact,
- decision-bearing evidence excerpts,
- named authority basis,
- written acceptance criterion,
- resolution owner,
- estimated fix cost.

Nits never block and should normally be enforced by tooling.

## Closure

Implementers may submit `ADDRESSED` or `DISPUTED`. Their statement is navigation context, not evidence. A qualified fresh reviewer owning the same dimension or seam verifies the acceptance criterion against the new snapshot and remediation delta.

Owner-only outcomes are:

- `RESOLVED`
- `STILL_OPEN`
- `WITHDRAWN`
- `SUPERSEDED`

Human-controlled outcomes are:

- `WAIVED`
- authority override or delegation

Every waiver includes authenticated authority, scope, reason, expiry, compensating controls, and follow-up.

## Reconciliation

Line numbers are supporting data, not identity. Fingerprints use record type, authority scope, defect class, affected contract, normalized path or symbol, and acceptance-criterion hash.

Candidate outcomes:

- `NEW`
- `UNCHANGED_OPEN`
- `POSSIBLE_DUPLICATE`
- `MOVED`
- `SUPERSEDING`
- `REGRESSION`

Fuzzy matching may propose a relationship but must never automatically resolve, withdraw, merge, or supersede a binding finding.
