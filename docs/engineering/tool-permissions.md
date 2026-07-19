# Agent tool permissions

`agent-policy.yml` is the portable default-deny policy for AI tool use.

## Permission statuses

- **allowed:** The agent may act within the listed constraints and approved task scope.
- **approval_required:** The agent must obtain explicit, authenticated, scoped approval and record it in the active work artifact.
- **prohibited:** The agent must not act. Human direction cannot override platform or organization policy.

## General rules

- Tool availability is not permission.
- Read permission does not imply write permission.
- Approval for one environment, command, account, or resource does not transfer to another.
- Prefer the narrowest tool and smallest scope that can establish correctness.
- Do not expose secrets in prompts, logs, command output, commits, tests, or evidence.
- Do not silently substitute an unapproved tool when the preferred capability is unavailable.
- Report `BLOCKED` when required access cannot be obtained safely.

## Destructive operations

Deletion, force operations, irreversible migrations, history rewriting, production mutation, credential changes, and broad recursive commands require explicit treatment in the approved plan and applicable human authorization. Production database mutation, production deployment, repository merge, release authorization, and external communication remain human-controlled under the default policy.

## Environment distinction

Agents must distinguish disposable local resources, shared development resources, staging, and production. A command that is safe locally may require approval or be prohibited in another environment.

## Project customization

Generated projects may tighten `agent-policy.yml`. Relaxing a default restriction requires a documented exception, compensating controls, named human approval, expiration, and repository-specific validation.
