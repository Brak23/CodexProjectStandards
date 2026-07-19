# Event contract standard

## Event identity

Every event defines:

- Stable event type and schema version
- Unique event identifier
- Occurred-at timestamp
- Producer and owning domain
- Subject or aggregate identifier
- Correlation and causation identifiers
- Tenant or security context where applicable

## Semantics

Document whether the event is a fact, command, notification, or state transfer. State ordering, duplication, delivery, retention, and replay expectations.

## Evolution

Prefer backward-compatible additive schema changes. Never silently change field meaning. Document consumer migration and deprecation before removing fields or event types.

## Consumer safety

Consumers must be idempotent, tolerate duplicates, define poison-message handling, and expose lag and failure telemetry. Sensitive data should be minimized and protected according to classification.

## Verification

Validate schemas, producer output, consumer compatibility, replay behavior, duplicate handling, and failure recovery in CI or a production-like environment.
