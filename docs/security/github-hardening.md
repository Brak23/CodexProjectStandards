# GitHub hardening checklist

## Repository settings

Enable the repository as a template when applicable. Disable unused merge methods and prefer squash merge. Enable automatic branch deletion only when desired.

## Branch protection for `main`

Require:

- Pull request before merging
- Required status checks
- Resolved conversations
- No force pushes
- No deletion
- Linear history or squash merge
- CODEOWNER review for sensitive paths

Team mode also requires at least one approval and dismissal of stale approvals after material changes. Apply rules to administrators except documented emergencies.

## Security features

Enable where available:

- Dependency graph
- Dependabot alerts and security updates
- Secret scanning and push protection
- Code scanning with CodeQL or equivalent
- Private vulnerability reporting
- Dependency review for pull requests

## GitHub Actions

- Default token permission is read-only.
- Grant permissions per job.
- Pin third-party actions to full commit SHAs.
- Do not execute fork-controlled code in privileged `pull_request_target` or `workflow_run` contexts.
- Use OIDC for cloud access.
- Protect staging and production environments.
- Prevent deployment initiators from self-approving.
- Use concurrency controls for deployments.
- Build once and promote the same immutable artifact.

## Manual steps after bootstrap

The bootstrap cannot configure repository settings. Complete this checklist in GitHub before production work begins.
