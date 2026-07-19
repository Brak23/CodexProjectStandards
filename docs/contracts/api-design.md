# HTTP API design standard

## Source of truth

Use OpenAPI for machine-consumable HTTP contracts. Validate it in CI and generate documentation or clients only from the reviewed contract.

## Resource and operation design

- Use stable nouns for resources and predictable HTTP semantics.
- Make mutating retryable operations idempotent where clients may retry.
- Define request and response size limits.
- Define pagination, filtering, sorting, and field selection consistently.
- Use explicit timestamps, time zones, identifiers, and money representations.

## Errors

Use a stable structured format containing a machine-readable code, safe message, correlation identifier, and field-level details when applicable. Do not expose stack traces, secrets, or internal infrastructure.

## Authentication and authorization

Document authentication scheme, scopes or permissions, resource ownership, tenant boundaries, and server-side enforcement. A successful authentication does not imply resource authorization.

## Compatibility and versioning

Classify changes as additive, behavior-changing, deprecated, or breaking. Document consumers, migration, support window, and removal date. Prefer additive evolution over URL version proliferation when semantics remain compatible.

## Reliability

Document timeouts, rate limits, retry guidance, idempotency keys, concurrency behavior, partial failure, and eventual consistency.

## Verification

Require schema validation, contract tests, authorization tests, negative tests, compatibility checks, and production smoke tests for critical endpoints.
