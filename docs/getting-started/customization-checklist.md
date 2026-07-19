# Project customization checklist

## Repository identity

- [ ] `project.yml` is committed and accurate.
- [ ] Project name, type, description, and repository path are accurate.
- [ ] Repository visibility is correct.
- [ ] License file, holder, and year match `project.yml`.
- [ ] CODEOWNERS contains valid users or organization teams with repository access.
- [ ] Private security reporting link targets the generated repository.

## Product

- [ ] Users and problems are defined.
- [ ] Success metrics are measurable.
- [ ] Domain terminology is recorded.
- [ ] Non-goals are explicit.

## Architecture

- [ ] Runtime components are documented.
- [ ] Dependency direction is documented.
- [ ] Data ownership and systems of record are documented.
- [ ] Authentication and authorization boundaries are documented.
- [ ] External dependencies and failure behavior are documented.

## Engineering

- [ ] Selected stack profiles have been implemented, not merely listed.
- [ ] `task setup`, `task dev`, `task test`, `task verify`, and `task build` are implemented as applicable.
- [ ] Formatting, linting, type checking, tests, security checks, and build are implemented as `scripts/verify.d/` hooks and reachable through `task verify`.
- [ ] GitHub Actions uses the same verification contract.
- [ ] Nested `AGENTS.md` files contain only local differences.
- [ ] Enforcement matrix reflects actual mechanisms.

## Security

- [ ] Branch ruleset is enabled.
- [ ] Solo or team approval mode is selected intentionally.
- [ ] Secret scanning and push protection are enabled where available.
- [ ] Dependabot and dependency review are enabled.
- [ ] CodeQL or equivalent analysis is enabled.
- [ ] GitHub Actions are full-SHA pinned.
- [ ] Production uses OIDC rather than long-lived cloud credentials.
- [ ] Private vulnerability reporting is configured.

## Operations

- [ ] Staging and production environments are protected.
- [ ] Deployment and rollback are executable.
- [ ] Logs, metrics, traces, and release markers exist.
- [ ] SLOs and actionable alerts are defined.
- [ ] Backup restore has been tested where data is persistent.
- [ ] Incident and postmortem ownership is defined.
