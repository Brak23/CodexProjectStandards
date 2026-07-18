# Coding standards

## Required properties

Production code should have:

- One clear responsibility.
- Explicit inputs, outputs, side effects, and failure behavior.
- Types or schemas at system boundaries.
- Configuration validation at startup.
- Stable structured errors.
- Timeouts on network calls.
- Bounded retries with backoff and jitter.
- Idempotency for retryable writes.
- Transaction boundaries aligned to business invariants.
- Query limits and pagination.
- Structured logs without secrets or sensitive payloads.
- No silent exception swallowing.
- No unowned mutable global state.

## Design rules

- Prefer simple modules and explicit composition.
- Start with a modular monolith unless independent service ownership, scaling, deployment, data isolation, or fault containment is demonstrated.
- Keep domain policy centralized.
- Introduce abstractions after a stable repeated pattern exists, not in anticipation of hypothetical reuse.
- Make invalid states difficult to represent.
- Optimize for maintainability and operability before cleverness.

## Comments

Comments explain intent, constraints, non-obvious tradeoffs, or safety requirements. Do not narrate syntax.

## Change discipline

- Keep PRs coherent and reviewable.
- Avoid unrelated refactoring.
- Preserve backward compatibility unless the breaking change is explicit and approved.
- Delete obsolete code and documentation when replacement is complete.
