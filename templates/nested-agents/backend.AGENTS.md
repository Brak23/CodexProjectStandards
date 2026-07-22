# Backend subsystem instructions

## Scope

Applies only to this service or backend subtree. Root `AGENTS.md`, `agent-policy.yml`, approved work artifacts, and applicable routed context remain authoritative.

## Local commands

Replace placeholders with repository commands before use:

- Start locally: `<backend-start-command>`
- Unit tests: `<backend-unit-test-command>`
- Integration tests: `<backend-integration-test-command>`
- Lint and type check: `<backend-quality-command>`

Do not invent substitute commands when configured commands fail.

## Boundaries

- Keep transport, application, domain, and persistence responsibilities within established layers.
- Preserve transaction boundaries, idempotency, authorization checks, and error contracts.
- Do not change public APIs, events, schemas, migrations, or data retention behavior without approved contract impact.
- Do not introduce direct cross-service database access or bypass established clients.
- Treat authentication, tenant context, queues, caches, file processing, webhooks, and external calls as trust boundaries.

## Verification

Run targeted tests first, then affected module, contract, integration, migration, and build checks as applicable. Verify failure behavior, authorization, idempotency, retries, timeouts, and rollback for changed boundaries.

## Ownership

Do not edit shared schemas, infrastructure, production configuration, secrets, deployment workflows, or another service's implementation without explicit ownership and integration coordination.
