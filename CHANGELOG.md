# Changelog

All notable user, operator, and integrator-facing changes are documented here when curated context is useful.

This template also uses semantic-release to generate versions, Git tags, and GitHub release notes from Conventional Commits. GitHub releases are the authoritative automated release record. This file explains context that automated notes cannot express well.

## [Unreleased]

### Added

- End-to-end, two-pass bootstrap integration testing.
- Generated-project validation workflow.
- Committed canonical `project.yml` configuration.
- Deterministic license and CODEOWNERS generation.
- API, event, enforcement, exception, prompt, incident, migration, postmortem, root-cause, and release standards.

### Changed

- Made `task verify` and `scripts/verify_project.py` the shared local and CI verification contract.
- Made bootstrap atomic, idempotent, and compatible with organization team CODEOWNERS.
- Clarified that stack profiles are standards overlays rather than application generators.
- Pinned Task and explicitly configured Python and Node in CI.

### Fixed

- Prevented generated projects from retaining CI steps that require a deleted reference project.
- Replaced copied template README content with a safe provenance document.
- Ensured selected license metadata updates the generated `LICENSE` file.
- Stopped ignoring canonical project configuration.

### Deprecated

### Removed

### Security
