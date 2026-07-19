# When to use these project standards

## The answer to remember

**Use this template once for the entire repository and codebase.**

It stays with the project and provides the rules, documentation structure, verification expectations, security controls, and AI-agent instructions for the life of that codebase.

You do not create another copy for each feature or bug fix. Instead, choose how much of the workflow each change needs.

> **One template per codebase. More process for larger or riskier changes. Less process for tiny, low-risk changes.**

## Light workflow

Use this for a tiny, well-understood, low-risk change.

Examples:

- Typo or documentation correction.
- Small display fix.
- Simple bug contained to one area.
- Mechanical change with strong existing tests.

Do:

1. Confirm the current behavior.
2. Make the smallest focused change.
3. Run the relevant tests and `task verify`.
4. Use a branch and pull request.

A full feature brief, long execution plan, ADR, or threat model is normally unnecessary.

## Full feature workflow

Use this for a new feature or meaningful change.

Examples:

- New user-facing capability.
- Change spanning multiple files or modules.
- New API, integration, background job, or dependency.
- Significant refactor.
- Changed data handling, permissions, deployment, or public behavior.

Do:

1. Create and approve a feature brief.
2. Perform read-only repository discovery.
3. Create and approve an execution plan.
4. Implement on an `agent/*` branch.
5. Use independent review.
6. Record full verification evidence.
7. Keep merge and release under human control.

## High-risk workflow

Use the full feature workflow plus additional safeguards for:

- Authentication or authorization.
- Payments or financial calculations.
- Sensitive or regulated data.
- Production database migrations.
- Infrastructure IAM, secrets, or network access.
- Breaking public contracts.

Add the applicable threat model, migration plan, rollback plan, security review, staged rollout, and explicit human approval.

## Use the template for

- A new app, API, service, CLI, library, or monorepo you expect to maintain.
- An existing codebase that needs safer and more consistent AI-assisted development.
- A personal project likely to grow beyond a quick prototype.
- A professional or team project where Codex or Claude Code will make meaningful changes.

## Usually skip the template for

- A throwaway script.
- A one-file experiment.
- A disposable proof of concept.
- A tiny repository you do not expect to maintain.

## Quick examples

- **Starting a new app:** Use the template once when creating the repository.
- **Adding user authentication:** Use the full, high-risk workflow inside that repository.
- **Adding a normal feature:** Use the full feature workflow.
- **Fixing a small null-handling bug:** Use the light workflow.
- **Correcting a typo:** Use the light workflow.
- **Writing a one-time personal script:** Usually skip the template.

A bug fix does not require a new copy of the template. The repository already has the standards; the bug fix simply uses the appropriate workflow level.
