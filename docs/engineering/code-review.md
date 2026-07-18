# Code review standard

Review the final diff against the approved brief and plan.

## Product correctness

- Does behavior satisfy each acceptance criterion?
- Are permissions, failure states, and edge cases correct?
- Did the change broaden behavior beyond scope?

## Design

- Does the change belong in these modules?
- Does it preserve dependency direction and data ownership?
- Is there a simpler implementation?
- Is complexity justified by current requirements?

## Security and reliability

- Can authorization be bypassed?
- Can data cross tenant or user boundaries?
- Are inputs, retries, timeouts, idempotency, concurrency, and partial failure handled?
- Does failure default safe?

## Data

- Are invariants preserved?
- Is migration safe for production volume and mixed versions?
- Are backfill, reconciliation, and recovery explicit?

## Tests

- Do tests verify behavior rather than implementation?
- Are mocks hiding integration failure?
- Were tests or controls weakened?
- Are composed and negative scenarios covered?

## Operations

- Can the change be observed, diagnosed, disabled, rolled back, and supported?
- Are telemetry, alerts, runbooks, and release markers adequate?

## Documentation

- Does documentation match final behavior?
- Were commands actually run?
- Are limitations and breaking changes explicit?

## Independent reviewer prompt

Search specifically for requirement mismatch, authorization bypass, tenant leakage, race conditions, fail-open behavior, rollback gaps, invalid assumptions, unnecessary changes, test gaming, and documentation contradictions. Do not merely summarize the diff.
