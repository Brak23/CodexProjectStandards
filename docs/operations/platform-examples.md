# Platform-neutral deployment examples

These examples define the expected engineering shape, not copy-paste production configuration. Each destination project must add provider-specific identity, networking, data, scaling, cost, and recovery decisions.

## Docker Compose

Use for local development, integration environments, single-host deployments, and small internal services where a single-host failure domain is acceptable.

Required project artifacts:

- `compose.yml` with explicit health checks and named networks.
- Immutable image tags for deployed environments.
- Externalized secrets and configuration.
- Persistent volume backup and restore procedures.
- Reverse proxy, TLS, log rotation, and host patching ownership.

Do not present Docker Compose as highly available production orchestration.

## GitHub Container Registry

Use GHCR as an artifact registry, not as the deployment platform.

- Publish image tags using commit SHA and optionally a human release version.
- Record and deploy by digest.
- Use `GITHUB_TOKEN` with job-scoped package permissions for same-repository publishing.
- Generate SBOM and provenance during the same build.
- Apply retention rules without deleting currently deployed digests.

## Managed web platforms

Vercel and Cloudflare are strong defaults for compatible web applications when their runtime, networking, data, and compliance constraints fit.

- Separate preview, staging, and production configuration.
- Prevent preview deployments from receiving production credentials.
- Verify cache and edge behavior explicitly.
- Define rollback to a known deployment ID.
- Export logs and metrics needed for the project's SLOs.

## AWS, Azure, and Google Cloud

Use the same control model regardless of provider:

- GitHub OIDC to a narrowly scoped deployment identity.
- Infrastructure defined and reviewed as code.
- Separate accounts, subscriptions, or projects for production where practical.
- Private network paths and managed identity for service-to-service access.
- Provider-native secret management.
- Immutable artifacts promoted across environments.
- Budget, quota, backup, restore, and regional-failure decisions documented.

Provider selection is an architecture decision when it materially affects runtime behavior, data residency, cost, skills, or portability.

## Kubernetes

Use Kubernetes only when the project actually needs its deployment, scaling, policy, or multi-service orchestration model. It is not a default quality upgrade.

Required controls include:

- Resource requests and limits.
- Readiness, liveness, and startup probes.
- Pod security and non-root execution.
- Network policy.
- Workload identity instead of static cloud credentials.
- Progressive delivery and rollback.
- Disruption budgets and capacity planning.
- Cluster and application observability.
- Explicit ownership of the platform itself.
