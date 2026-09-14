# Release management

## Versioning

Use Semantic Versioning only when the project has a meaningful public contract. Internal continuously deployed applications may use release IDs based on date and commit SHA while still using Conventional Commits.

## Release decision and execution

The product owner decides whether a consequential release should ship. AI may prepare, merge, publish metadata, deploy, run smoke checks, and recover from a failed rollout when **agent-policy.yml**, the configured integration, and scoped authorization allow it.

Distinguish source merge, package or release metadata, preview, staging, production deployment, rollback, and repository settings. A successful GitHub release or deployment command does not prove production health.

Production authorization should name the commit or artifact, environment, and relevant release conditions. A project may record a bounded standing authorization for recurring qualifying releases. Credentials, branch protections, and deployment environments enforce controls where configured; repository prose does not.

## Release evidence

Every release record should identify:

- Version or release ID
- Commit SHA and immutable artifact digest
- User-visible changes and how to inspect them
- Breaking changes and migration steps
- Configuration, permission, and data changes
- Known limitations
- Deployment, health checks, and rollback information
- Technical verification and product acceptance state
