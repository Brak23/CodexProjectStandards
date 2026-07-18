# Deployment standard

## Artifact

Record commit SHA, artifact digest, SBOM, provenance, and build workflow.

## Environments

Use development, staging, and production with configuration separated from code. Protect production with explicit approval and least-privilege OIDC credentials.

## Release sequence

1. Complete required CI.
2. Build one immutable artifact.
3. Deploy the artifact to staging.
4. Run smoke, integration, security, accessibility, and performance checks as applicable.
5. Approve production deployment.
6. Use canary, percentage, tenant, or cohort rollout where risk warrants.
7. Verify health and business behavior.
8. Complete rollout or execute rollback.

## Deployment evidence

Record release ID, artifact digest, environment, approver, strategy, migration sequence, checks, dashboard, alerts, and release marker.
