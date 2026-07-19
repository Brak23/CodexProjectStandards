# Release management

## Versioning

Use Semantic Versioning only when the project has a meaningful public contract. Internal continuously deployed applications may use release IDs based on date and commit SHA while still using Conventional Commits.

## Commit and release classification

- `fix`: backward-compatible defect correction
- `feat`: backward-compatible capability
- `BREAKING CHANGE` or `!`: incompatible contract or behavior
- `perf`: measurable performance change
- Other types do not create a release unless project policy says otherwise

## Release evidence

Every release record should identify:

- Version or release ID
- Commit SHA and immutable artifact digest
- User-visible changes
- Breaking changes and migration steps
- Configuration, permission, and data changes
- Security fixes
- Known limitations
- Deployment and rollback information
- Verification evidence

## Prereleases and hotfixes

Define prerelease channels and maintenance branches before using them. Hotfixes still require verification and production approval. Emergency process may reduce waiting time, not remove auditability or recovery requirements.

## Changelog

Use `CHANGELOG.md` for curated context. Use generated GitHub release notes as a seed, not a substitute for explaining migration, risk, or operational impact.
