# Project customization checklist

## Repository identity

- [ ] Project name and description are accurate.
- [ ] Repository visibility is correct.
- [ ] GitHub template source references are retained or removed intentionally.
- [ ] License is correct.
- [ ] CODEOWNERS uses valid users or teams.

## Product

- [ ] Users and problems are defined.
- [ ] Success metrics are measurable.
- [ ] Domain terminology is recorded.
- [ ] Non-goals are explicit.

## Architecture

- [ ] Runtime components are documented.
- [ ] Dependency direction is documented.
- [ ] Data ownership and system of record are documented.
- [ ] Authentication and authorization boundaries are documented.
- [ ] External dependencies and failure behavior are documented.

## Engineering

- [ ] `task setup`, `task dev`, `task test`, `task verify`, and `task build` are implemented as applicable.
- [ ] Formatting, lint, type checking, tests, and build run in CI.
- [ ] Stack-specific nested `AGENTS.md` files contain only local differences.
- [ ] Test strategy matches system risk.

## Security

- [ ] Branch protection is enabled.
- [ ] Secret scanning and push protection are enabled where available.
- [ ] Dependabot and dependency review are enabled.
- [ ] CodeQL or equivalent analysis is enabled.
- [ ] GitHub Actions are full-SHA pinned.
- [ ] Production uses OIDC rather than long-lived cloud credentials.
- [ ] Private vulnerability reporting is configured.

## Operations

- [ ] Deployment and rollback are executable.
- [ ] Staging and production environments are protected.
- [ ] Logs, metrics, traces, and release markers exist.
- [ ] SLOs and actionable alerts are defined.
- [ ] Backup restore has been tested where data is persistent.
