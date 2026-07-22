# Mobile subsystem instructions

## Scope

Applies only to this mobile application subtree. Root `AGENTS.md`, `agent-policy.yml`, approved work artifacts, and applicable routed context remain authoritative.

## Local commands

Replace placeholders with repository commands before use:

- Build: `<mobile-build-command>`
- Unit tests: `<mobile-unit-test-command>`
- UI tests: `<mobile-ui-test-command>`
- Lint and format: `<mobile-lint-command>`

Do not invent substitute commands when a configured command fails.

## Boundaries

- Keep business, authorization, and data-normalization policy outside presentation components.
- Use the established navigation, dependency-injection, state-management, persistence, and networking patterns.
- Do not add a new package or architecture framework without explicit approval.
- Treat platform permissions, secure storage, background execution, deep links, and analytics as security-relevant surfaces.
- Preserve API compatibility and generated-client ownership rules.

## Verification

For affected behavior, run the narrowest relevant unit or component tests first, then the affected application suite and build. User-facing changes require interaction, accessibility, loading, empty, error, offline, permission-denied, and recovery-state evidence where applicable.

## Ownership

Do not edit shared API schemas, backend contracts, design-system sources, signing configuration, release credentials, or deployment workflows without assignment to those paths and coordination with their owner.
