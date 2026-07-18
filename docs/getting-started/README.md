# Getting started

## New project checklist

1. Create a repository using this GitHub template.
2. Clone it locally.
3. Run `task bootstrap` or configure `project.yml` and run `task bootstrap-config`.
4. Review the generated README and `project.yml`.
5. Select and adapt stack profiles from `docs/profiles/`.
6. Replace base `task verify` with real stack checks while preserving the stable command.
7. Configure GitHub protections using `docs/security/github-hardening.md`.
8. Configure private vulnerability reporting.
9. Configure deployment environments and OIDC.
10. Run `task verify` before the first pull request.

## First feature

Create a workspace:

```bash
task feature FEATURE=APP-001 NAME=first-capability
```

Complete and approve `brief.md`, then have the agent perform discovery and draft `plan.md`. Do not allow implementation to begin while blocking product, security, data, cost, or compatibility decisions remain.

## Files you should customize immediately

- `README.md`
- `project.yml`
- `CODEOWNERS`
- `.github/ISSUE_TEMPLATE/config.yml`
- `docs/product/vision.md`
- `docs/product/domain-model.md`
- `docs/architecture/overview.md`
- `docs/architecture/boundaries.md`
- `docs/operations/deployment.md`
- `docs/operations/rollback.md`
- `docs/operations/observability.md`

See [`customization-checklist.md`](customization-checklist.md) for the full handoff checklist.
