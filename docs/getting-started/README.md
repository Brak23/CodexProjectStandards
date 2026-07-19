# Getting started

## First decide how this applies

These standards are adopted **once for the whole repository**, not copied separately for every feature or bug fix.

Then each change uses a light, full, or high-risk workflow depending on scope and risk. Start with [`when-to-use-this.md`](when-to-use-this.md) when you are unsure which path applies.

## Create and configure a project

1. Create a repository from the GitHub template.
2. Clone it locally.
3. Install the versions in `.mise.toml` or equivalent pinned versions.
4. Run `task bootstrap`, or copy `project.config.example.yml` to `project.yml` and run `task bootstrap-config`.
5. Commit the generated `project.yml`. It contains non-secret canonical project metadata.
6. Review the generated README, CODEOWNERS, LICENSE, security link, and workflows.
7. Implement the selected stack profiles behind stable Task commands.
8. Run `task verify`.
9. Configure GitHub repository settings using the hardening checklist.
10. Start feature work only after the base repository passes CI.

## Configuration fields

`project.yml` records:

- `project.name`
- `project.type`: `web-app`, `api`, `service`, `cli`, `library`, `monorepo`, or `other`
- `project.description`
- `project.license`: `MIT`, `Apache-2.0`, or `Proprietary`
- `project.license_holder`
- `project.license_year`
- `repository.owner`
- `repository.name`
- `repository.mode`: `solo` or `team`
- `repository.codeowners`: valid GitHub users or `@organization/team` entries
- `profiles`
- `deployment_targets`
- bootstrap options

The repository owner and CODEOWNER are separate concepts. An organization repository normally uses a person or organization team as CODEOWNER.

## Selected profiles

Profiles are standards overlays, not application generators. For every selected profile:

1. Read its document under `docs/profiles/`.
2. Add the relevant runtime, package, build, test, and security configuration.
3. Implement stable Task commands.
4. Add stack-specific checks under `scripts/verify.d/`; `task verify` and CI execute them through the same script.
5. Add nested `AGENTS.md` only when a directory has genuinely different rules.

## First feature

```bash
task feature FEATURE=APP-001 NAME=first-capability
```

Complete and approve `brief.md`, then have the agent perform discovery and draft `plan.md`. Do not allow implementation while blocking product, security, data, cost, or compatibility decisions remain.

## Bootstrap safety

- Bootstrap is deterministic and idempotent.
- It writes files atomically.
- It regenerates managed ownership, security, README, license, and workflow files from `project.yml`.
- It replaces template-only validation with project validation.
- It removes the reference project only when configured.
- `task verify` includes a real two-pass bootstrap integration test while this repository remains a template source.
