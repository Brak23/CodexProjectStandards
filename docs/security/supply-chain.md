# Software supply-chain standard

## Dependencies

- Verify identity, publisher, source repository, license, maintenance, runtime compatibility, and vulnerability status.
- Commit lockfiles.
- Minimize production dependencies.
- Review dependency changes in pull requests.
- Use automated update tooling with CI.

## Build

- Use isolated reproducible builds.
- Pin actions and build images.
- Use least-privilege ephemeral credentials.
- Generate an SBOM for deployable artifacts.
- Generate provenance or attestations where supported.
- Sign artifacts when deployment infrastructure supports verification.

## Promotion

Build once, record commit and digest, verify in staging, and promote the exact artifact to production. Never rebuild independently per environment.
