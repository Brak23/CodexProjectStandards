# Agent tool permissions

**agent-policy.yml** is the portable default-deny policy for AI tool use.

## Permission statuses

- **allowed:** The agent may act within listed constraints and the current product request.
- **approval_required:** The action needs scoped authorization for its resource, account, and environment.
- **prohibited:** The agent must not act. Human direction cannot override platform or organization policy.

## General rules

- Tool availability is not permission.
- A product request authorizes ordinary necessary engineering work, including equivalent permitted tools.
- Crossing an account, environment, spending, data, or irreversible-effect boundary needs explicit consideration.
- Use runtime-managed secrets without printing, exporting, committing, or broadly inspecting their values.
- When a required capability is unavailable, finish independent permitted work and report the exact blocker.

## Environment distinction

Disposable local resources differ from shared development, staging, and production. Local development of a migration does not authorize production execution. Production release execution requires configured integration and scoped authorization unless a project records a bounded standing authorization.

## Enforcement

The policy is portable guidance unless the agent runtime, CI, environment, or GitHub setting enforces it. Record actual enforcement and evidence in the project; do not claim that text alone blocked an action.
