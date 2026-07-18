# Security policy

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub private vulnerability reporting when enabled, or contact the repository owner through the private security channel documented in repository settings.

Include:

- Affected component and version or commit
- Reproduction steps
- Security impact
- Required privileges or conditions
- Suggested mitigation when known

## Supported versions

The latest released major version receives security fixes unless the project documents a different support policy.

## Security baseline

This repository requires least privilege, protected branches, dependency review, automated updates, secret scanning, static analysis where applicable, full-SHA action pinning, OIDC for cloud authentication, and human review for high-risk changes.

See `docs/security/README.md` and `docs/security/github-hardening.md`.
