# GitHub hardening checklist

Complete these settings after bootstrap. Repository files can recommend controls, but GitHub settings enforce them.

## 1. Repository identity and template status

For the standards source repository, enable **Template repository**. Generated projects should normally leave that setting off unless they are intentionally reusable templates.

Confirm visibility, description, topics, default branch, and vulnerability-reporting contact.

## 2. Merge behavior

- Enable squash merge.
- Disable merge commits and rebase merge unless the project intentionally uses them.
- Enable automatic deletion of head branches if desired.
- Require branches to be up to date only when the CI and queue strategy supports it.

## 3. Default Actions permissions

Set the default `GITHUB_TOKEN` permission to read-only. Grant write permissions only on the individual jobs that need them.

## 4. Security features

Enable where available:

- Dependency graph
- Dependabot alerts and security updates
- Secret scanning and push protection
- Code scanning with CodeQL or equivalent
- Private vulnerability reporting
- Dependency review for pull requests

Copy the optional workflows from `templates/github-actions/` only after selecting the actual languages and package ecosystems.

## 5. Ruleset for `main`

Require:

- Pull request before merging
- Required `verify` or project-validation status check
- Resolved review conversations
- No force pushes
- No deletion
- Linear history
- CODEOWNER review for sensitive paths when using team mode
- Rules applied to administrators except a documented emergency bypass role

### Solo versus team approval

A required approval needs a different eligible reviewer from the PR author. For a truly solo repository, omit the approval requirement but keep PRs, CI, conversations, CODEOWNERS visibility, and production approval. For team mode, require at least one approval and dismiss stale approvals after material changes.

## 6. Protected environments

Create `staging` and `production` environments before adding deployment workflows.

For production:

- Require named reviewers who did not initiate the deployment where practical.
- Restrict deployment branches or tags.
- Store only environment-specific secrets that cannot use OIDC.
- Prefer OIDC and short-lived cloud roles.
- Add concurrency controls to prevent overlapping deployments.

## 7. Supply-chain settings

- Require dependency review and code scanning checks where configured.
- Keep actions pinned to full commit SHAs.
- Generate SBOM and provenance for deployable artifacts.
- Build once and promote the exact digest.

## 8. Validate enforcement

Run `task verify`, open a test pull request, and confirm the ruleset blocks merge until required checks and reviews are satisfied. Record the actual enforcement state in `docs/engineering/enforcement-matrix.md`.
