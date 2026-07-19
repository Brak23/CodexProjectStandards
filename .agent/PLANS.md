# Execution plan standard

An ExecPlan is the approved execution contract for non-trivial work. It must be self-contained enough that another engineer or agent can continue using only the repository, the plan, and the active `state.yml`.

## When required

Use an ExecPlan for features, cross-module changes, migrations, public contracts, security-sensitive work, infrastructure, significant refactors, or work expected to exceed 60 minutes.

## State synchronization

Before planning, confirm `state.yml` identifies the feature, phase, risk, ownership, branch, and approval state. The plan and state file must remain consistent throughout implementation.

Do not set approval or authorization fields on behalf of a human. Follow `docs/engineering/approval-amendments.md` whenever approved intent or technical scope changes materially.

## Required sections

### Purpose

State the user-visible or operational outcome and why it matters.

### Current behavior

Describe current implementation and the evidence used to establish it.

### Acceptance criteria

Copy or link every observable criterion from the approved brief. Do not rewrite criteria into weaker technical proxies.

### Non-goals

State what is deliberately excluded.

### Assumptions and unknowns

Classify each item as:

- Confirmed
- Low-risk and reversible assumption
- Blocking human decision

### Repository and agent context

Identify relevant modules, comparable patterns, tests, public contracts, persistence, deployment topology, external dependencies, applicable context groups from `agent-context.yml`, nested instructions, and the active branch/base commit.

### Proposed design

Describe component changes, data flow, error behavior, authorization, observability, and why the design fits existing architecture.

### Alternatives considered

Record materially different options and why they were rejected.

### Risk classification

State risk level and changed trust boundaries, sensitive data, authorization, dependencies, network access, migration impact, reversibility, operational blast radius, and material unknowns.

### Tool and environment permissions

List the tools, environments, accounts, external systems, package changes, and destructive operations required. Map each to `agent-policy.yml` as allowed, approval-required, or prohibited. Record required approvals and safe fallbacks.

### Expected change surface

List expected files and directories. Record explicit expectations for:

- New dependencies
- Public contract changes
- Database migrations
- Infrastructure changes
- Feature flags
- Documentation changes
- Agent governance or protected-surface changes

### Implementation milestones

Each milestone must leave the repository coherent and independently verifiable. Keep `state.yml` current with the active and completed milestone.

### Verification matrix

Map each acceptance criterion to implementation locations, tests, scanners, observed evidence, and the commit on which evidence will be valid.

### Independent review

Select the required review level from `docs/engineering/review-independence.md`, including any specialist reviewer. State who or what may review, whether the reviewer is read-only, and how findings will be recorded.

### Rollout

Describe sequencing, flags, canary or cohort strategy, release metrics, success thresholds, environment permissions, and human approval gates.

### Rollback or disablement

Describe the fastest safe recovery path and any irreversible effects.

### Progress

After every milestone record:

- Work completed
- Files changed
- Commands executed
- Results
- Unexpected findings
- Failed approaches
- Remaining work
- Current blockers
- State and ownership updates

### Decision log

Record consequential implementation decisions with date, decision, rationale, alternatives, consequences, and whether reapproval was required.

### Final evidence

Record the final commit, exact validation commands, results, review level and reviewer, remaining limitations, deployment notes, state transition, and final completion status.

## Replanning triggers

Stop and revise the plan when scope expands materially, risk increases, an unplanned dependency or migration is required, a public contract changes, tool permission requirements change, ownership or repository state conflicts, or two repair attempts fail for the same symptom.
